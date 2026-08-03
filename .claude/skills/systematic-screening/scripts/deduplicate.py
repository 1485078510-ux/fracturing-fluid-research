#!/usr/bin/env python3
"""Deduplicate search results across databases and generate PRISMA report."""

import argparse
import json
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher


def normalize_doi(doi):
    """Normalize DOI for comparison."""
    if not doi:
        return None
    doi = str(doi).lower().strip()
    doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi)
    doi = re.sub(r'^doi:\s*', '', doi)
    return doi if doi else None


def normalize_title(title):
    """Normalize title for fuzzy comparison."""
    if not title:
        return ""
    title = title.lower().strip()
    title = re.sub(r'[^\w\s]', '', title)
    title = re.sub(r'\s+', ' ', title)
    return title


def find_duplicates(papers):
    """Find duplicate papers across databases."""
    doi_index = defaultdict(list)
    title_index = defaultdict(list)
    duplicates = []

    for i, paper in enumerate(papers):
        doi = normalize_doi(paper.get("doi"))
        title = normalize_title(paper.get("title", ""))
        source = paper.get("source_database", "unknown")

        if doi:
            doi_index[doi].append(i)
        if title:
            title_index[title].append(i)

    # DOI-based deduplication (highest confidence)
    seen = set()
    for doi, indices in doi_index.items():
        if len(indices) > 1:
            canonical = indices[0]
            for idx in indices[1:]:
                if idx not in seen:
                    duplicates.append({
                        "canonical_index": canonical,
                        "duplicate_index": idx,
                        "method": "DOI exact match",
                        "confidence": 1.0,
                        "doi": doi,
                    })
                    seen.add(idx)

    # Title-based deduplication (fuzzy)
    titles = [(i, normalize_title(p.get("title", ""))) for i, p in enumerate(papers)]
    for i, (idx_a, title_a) in enumerate(titles):
        if idx_a in seen or not title_a:
            continue
        for j in range(i + 1, len(titles)):
            idx_b, title_b = titles[j]
            if idx_b in seen or not title_b:
                continue
            if papers[idx_a].get("source_database") == papers[idx_b].get("source_database"):
                continue  # Skip same-database comparisons

            similarity = SequenceMatcher(None, title_a, title_b).ratio()
            if similarity > 0.92:
                duplicates.append({
                    "canonical_index": idx_a,
                    "duplicate_index": idx_b,
                    "method": f"Title fuzzy match ({similarity:.0%})",
                    "confidence": similarity,
                })
                seen.add(idx_b)

    return duplicates


def generate_prisma_report(papers, duplicates, inclusion_criteria=None):
    """Generate PRISMA flow diagram data."""
    sources = defaultdict(int)
    for p in papers:
        sources[p.get("source_database", "unknown")] += 1

    total_identified = len(papers)
    duplicates_removed = len(duplicates)
    records_screened = total_identified - duplicates_removed

    return {
        "prisma": {
            "identification": {
                "sources": dict(sources),
                "total_identified": total_identified,
            },
            "screening": {
                "duplicates_removed": duplicates_removed,
                "records_screened": records_screened,
            },
            "eligibility": {
                "sought_for_retrieval": None,  # To be filled during screening
                "not_retrieved": None,
                "assessed_for_eligibility": None,
                "excluded_fulltext": None,
                "excluded_reasons": {},
            },
            "included": {
                "studies_included": None,  # To be filled after full-text review
            },
        },
        "duplicates": [
            {
                "canonical": {
                    "title": papers[d["canonical_index"]].get("title"),
                    "doi": papers[d["canonical_index"]].get("doi"),
                    "source": papers[d["canonical_index"]].get("source_database"),
                },
                "duplicate": {
                    "title": papers[d["duplicate_index"]].get("title"),
                    "doi": papers[d["duplicate_index"]].get("doi"),
                    "source": papers[d["duplicate_index"]].get("source_database"),
                },
                "method": d["method"],
                "confidence": d["confidence"],
            }
            for d in duplicates
        ],
    }


def format_prisma_text(report):
    """Format PRISMA report as readable text."""
    p = report["prisma"]
    sources = p["identification"]["sources"]

    lines = [
        "=" * 60,
        "PRISMA FLOW DIAGRAM",
        "=" * 60,
        "",
        "IDENTIFICATION",
    ]
    for source, count in sources.items():
        lines.append(f"  Records from {source}: n={count}")
    lines.append(f"  Total identified: n={p['identification']['total_identified']}")
    lines.append("")
    lines.append("SCREENING")
    lines.append(f"  Duplicates removed: n={p['screening']['duplicates_removed']}")
    lines.append(f"  Records screened: n={p['screening']['records_screened']}")
    lines.append("")

    if report["duplicates"]:
        lines.append("DUPLICATE DETAILS")
        for d in report["duplicates"]:
            lines.append(f"  [{d['method']}] (confidence: {d['confidence']:.0%})")
            lines.append(f"    KEEP: {d['canonical']['title'][:70]} ({d['canonical']['source']})")
            lines.append(f"    REMOVE: {d['duplicate']['title'][:70]} ({d['duplicate']['source']})")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Deduplicate search results")
    parser.add_argument("input", help="JSON file with search results")
    parser.add_argument("--output", help="Output JSON file")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format")
    args = parser.parse_args()

    with open(args.input) as f:
        papers = json.load(f)

    duplicates = find_duplicates(papers)
    report = generate_prisma_report(papers, duplicates)

    if args.format == "text":
        print(format_prisma_text(report))
    else:
        output = json.dumps(report, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"Written to {args.output}", file=sys.stderr)
        else:
            print(output)

    print(f"\nSummary: {len(papers)} papers → {len(duplicates)} duplicates → "
          f"{len(papers) - len(duplicates)} unique", file=sys.stderr)


if __name__ == "__main__":
    main()
