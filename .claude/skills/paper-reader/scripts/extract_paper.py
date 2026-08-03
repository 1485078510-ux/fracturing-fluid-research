#!/usr/bin/env python3
"""Parse academic paper text into structured JSON extraction."""

import argparse
import json
import re
import sys


def detect_paper_type(text):
    """Detect paper type from title and content."""
    text_lower = text[:3000].lower()

    if any(kw in text_lower for kw in ["systematic review", "meta-analysis", "meta analysis"]):
        return "systematic_review"
    if any(kw in text_lower for kw in ["case report", "case study"]) and "we report" in text_lower:
        return "case_report"
    if any(kw in text_lower for kw in ["we propose", "we introduce", "novel method", "we present a method"]):
        if any(kw in text_lower for kw in ["benchmark", "evaluation", "accuracy", "f1"]):
            return "methodology"
    if len(text) < 3000:
        return "abstract"

    return "original_research"


def extract_sections(text):
    """Split paper text into major sections."""
    section_patterns = [
        (r"(?i)^#{0,3}\s*(?:abstract|summary)\s*\n", "abstract"),
        (r"(?i)^#{0,3}\s*(?:\d?\.?\s*)?(?:introduction|background)\s*\n", "introduction"),
        (r"(?i)^#{0,3}\s*(?:\d?\.?\s*)?(?:related work|literature review)\s*\n", "related_work"),
        (r"(?i)^#{0,3}\s*(?:\d?\.?\s*)?(?:methods?|methodology|materials?\s+and\s+methods?|study\s+design)\s*\n", "methods"),
        (r"(?i)^#{0,3}\s*(?:\d?\.?\s*)?(?:results?|findings)\s*\n", "results"),
        (r"(?i)^#{0,3}\s*(?:\d?\.?\s*)?(?:discussion)\s*\n", "discussion"),
        (r"(?i)^#{0,3}\s*(?:\d?\.?\s*)?(?:conclusion[s]?)\s*\n", "conclusion"),
        (r"(?i)^#{0,3}\s*(?:references?|bibliography)\s*\n", "references"),
    ]

    sections = {}
    positions = []

    for pattern, name in section_patterns:
        for m in re.finditer(pattern, text, re.MULTILINE):
            positions.append((m.start(), name))

    positions.sort(key=lambda x: x[0])

    for i, (pos, name) in enumerate(positions):
        if name == "references":
            break
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        sections[name] = text[pos:end].strip()

    return sections


def extract_title(text):
    """Extract paper title from the beginning of text."""
    lines = text.strip().split("\n")
    for line in lines[:10]:
        line = line.strip("#").strip()
        if len(line) > 15 and len(line) < 300:
            return line
    return "Unknown Title"


def extract_authors(text):
    """Extract author names from the beginning of text."""
    lines = text.strip().split("\n")
    for i, line in enumerate(lines[1:8]):
        line = line.strip()
        if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+', line):
            authors = re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)?', line)
            if authors:
                return authors[:10]
    return []


def extract_pico(sections):
    """Extract PICO elements from paper sections."""
    pico = {"population": None, "intervention": None, "comparison": None, "outcome": None}

    abstract = sections.get("abstract", "")
    methods = sections.get("methods", "")
    combined = abstract + "\n" + methods

    # Population patterns
    pop_patterns = [
        r"(?i)(?:patients?|participants?|subjects?|sample)\s+(?:with|diagnosed|aged|N\s*=\s*)(\d+[\w\s,]+?)(?:\.)",
        r"(?i)(?:included|recruited|enrolled)\s+([\d,]+)\s+(?:patients?|participants?|subjects?)",
        r"(?i)(?:study\s+)?population[:\s]+(.*?)(?:\.)",
    ]
    for pat in pop_patterns:
        m = re.search(pat, combined)
        if m:
            pico["population"] = m.group(1).strip()[:200]
            break

    # Sample size
    n_match = re.search(r"(?i)(?:n\s*=\s*|sample\s+size\s*(?:of|:)?\s*)([\d,]+)", combined)
    if n_match:
        pico["sample_size"] = int(n_match.group(1).replace(",", ""))

    return pico


def extract_claims(sections):
    """Extract key claims from results and discussion."""
    claims = []
    results = sections.get("results", "")
    discussion = sections.get("discussion", "")

    # Find sentences with statistical evidence
    stat_pattern = r"(?i)([A-Z][^.]*?(?:p\s*[<>=]\s*[\d.]+|CI\s*[\d.\-]+|effect\s+size|odds\s+ratio|hazard\s+ratio|risk\s+ratio|[\d.]+%)[^.]*)"

    for source, text in [("results", results), ("discussion", discussion)]:
        for m in re.finditer(stat_pattern, text):
            claim_text = m.group(1).strip()
            if len(claim_text) > 20 and len(claim_text) < 500:
                claims.append({
                    "claim": claim_text,
                    "section": source,
                    "has_statistical_evidence": True,
                })

    return claims[:15]


def extract_paper(text, paper_id="unknown"):
    """Main extraction function."""
    paper_type = detect_paper_type(text)
    sections = extract_sections(text)
    title = extract_title(text)
    authors = extract_authors(text)
    pico = extract_pico(sections)
    claims = extract_claims(sections)

    extraction = {
        "study_id": paper_id,
        "paper_type": paper_type,
        "title": title,
        "authors": authors,
        "sections_found": list(sections.keys()),
        "pico": pico,
        "key_claims": claims,
        "section_lengths": {k: len(v) for k, v in sections.items()},
    }

    # Add sections content
    for name, content in sections.items():
        if name != "references":
            extraction[f"section_{name}"] = content[:2000]

    return extraction


def main():
    parser = argparse.ArgumentParser(description="Extract structured data from paper text")
    parser.add_argument("input", help="Input file (text or markdown)")
    parser.add_argument("--output", help="Output JSON file")
    parser.add_argument("--id", default="unknown", help="Paper identifier")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        text = f.read()

    extraction = extract_paper(text, args.id)

    output = json.dumps(extraction, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Extraction written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
