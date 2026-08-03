#!/usr/bin/env python3
"""Analyze research trends from Semantic Scholar data."""

import argparse
import json
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode

BASE_URL = "https://api.semanticscholar.org/graph/v1"
RATE_DELAY = 1.0
FIELDS = "paperId,title,authors,year,citationCount,publicationDate,tldr"


def api_get(url):
    req = Request(url)
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        if e.code == 429:
            time.sleep(10)
            return api_get(url)
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def search_papers(query, year=None, limit=100, sort="citationCount:desc"):
    params = {
        "query": query,
        "fields": FIELDS,
        "limit": str(limit),
        "sort": sort,
    }
    if year:
        params["year"] = year
    url = f"{BASE_URL}/paper/search?{urlencode(params)}"
    time.sleep(RATE_DELAY)
    return api_get(url).get("data", [])


def compute_heat_score(paper):
    """Compute a heat score combining velocity and impact."""
    citations = paper.get("citationCount", 0) or 0
    pub_date = paper.get("publicationDate") or ""
    year = paper.get("year") or 2024

    # Estimate age in months
    try:
        parts = pub_date.split("-")
        pub_year = int(parts[0])
        pub_month = int(parts[1]) if len(parts) > 1 else 6
        age_months = max((2026 - pub_year) * 12 + (4 - pub_month), 1)
    except (ValueError, IndexError):
        age_months = max((2026 - year) * 12, 1)

    velocity = citations / age_months if age_months > 0 else 0
    recency_bonus = 12.0 / age_months if age_months > 0 else 0

    heat = (velocity * 2.0) + (citations / 100.0) + recency_bonus
    return {
        "heat": round(heat, 2),
        "velocity": round(velocity, 2),
        "age_months": age_months,
        "citations": citations,
    }


def detect_pattern(heat_data, paper):
    """Detect the trend pattern of a paper."""
    velocity = heat_data["velocity"]
    age = heat_data["age_months"]
    citations = heat_data["citations"]

    if age < 12 and velocity > 10:
        return "Burst"
    elif age > 24 and velocity > 5 and citations < 200:
        return "Sleeper"
    elif age > 60 and velocity > 1:
        return "Steady Classic"
    elif age < 24 and velocity < 2 and citations < 50:
        return "Flash"
    else:
        return "Active"


def main():
    parser = argparse.ArgumentParser(description="Analyze research trends from S2 data")
    parser.add_argument("query", help="Research topic query")
    parser.add_argument("--years-back", type=int, default=3, help="How many years to analyze")
    parser.add_argument("--limit", type=int, default=50, help="Papers per year")
    parser.add_argument("--output", help="Output file (JSON)")
    parser.add_argument("--top", type=int, default=20, help="Top papers to show")
    args = parser.parse_args()

    current_year = 2026
    start_year = current_year - args.years_back

    all_papers = []
    for year in range(start_year, current_year + 1):
        year_range = f"{year}"
        print(f"Searching {year_range}...", file=sys.stderr)
        papers = search_papers(args.query, year=year_range, limit=args.limit,
                                sort="citationCount:desc")
        for p in papers:
            p["_year_queried"] = year
        all_papers.extend(papers)

    print(f"\nTotal papers: {len(all_papers)}", file=sys.stderr)

    # Compute heat scores
    scored = []
    for p in all_papers:
        heat = compute_heat_score(p)
        pattern = detect_pattern(heat, p)
        scored.append({
            "title": p.get("title", "No title"),
            "year": p.get("year"),
            "authors": ", ".join(a.get("name", "?") for a in (p.get("authors") or [])[:3]),
            "citations": heat["citations"],
            "velocity": heat["velocity"],
            "heat_score": heat["heat"],
            "age_months": heat["age_months"],
            "pattern": pattern,
            "tldr": (p.get("tldr") or {}).get("text", ""),
            "paperId": p.get("paperId", ""),
        })

    # Sort by heat score
    scored.sort(key=lambda x: x["heat_score"], reverse=True)

    # Print top papers
    print(f"\n{'='*80}")
    print(f"Research Trends: {args.query}")
    print(f"{'='*80}\n")

    print(f"### Top {args.top} Trending Papers\n")
    print(f"{'#':<4} {'Heat':<8} {'Pattern':<16} {'Cit':<8} {'Vel':<8} {'Year':<6} Title")
    print("-" * 80)
    for i, p in enumerate(scored[:args.top]):
        print(f"{i+1:<4} {p['heat_score']:<8.1f} {p['pattern']:<16} "
              f"{p['citations']:<8} {p['velocity']:<8.1f} {p['year'] or '?':<6} "
              f"{p['title'][:50]}")

    # Pattern summary
    patterns = {}
    for p in scored:
        pat = p["pattern"]
        patterns[pat] = patterns.get(pat, 0) + 1

    print(f"\n### Pattern Summary\n")
    for pat, count in sorted(patterns.items(), key=lambda x: -x[1]):
        print(f"  {pat}: {count} papers")

    # Year-over-year volume
    print(f"\n### Publication Volume by Year\n")
    year_counts = {}
    for p in scored:
        y = p.get("year")
        if y:
            year_counts[y] = year_counts.get(y, 0) + 1
    for y in sorted(year_counts.keys()):
        bar = "█" * year_counts[y]
        print(f"  {y}: {bar} ({year_counts[y]})")

    # Output JSON
    if args.output:
        with open(args.output, "w") as f:
            json.dump({
                "query": args.query,
                "papers": scored,
                "patterns": patterns,
                "year_counts": year_counts,
            }, f, indent=2)
        print(f"\nJSON output written to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
