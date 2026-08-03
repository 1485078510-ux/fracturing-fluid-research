#!/usr/bin/env python3
"""Semantic Scholar API utility for common operations."""

import argparse
import json
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode, quote

BASE_URL = "https://api.semanticscholar.org/graph/v1"
REC_URL = "https://api.semanticscholar.org/recommendations/v1"

DEFAULT_FIELDS = "paperId,title,abstract,authors,year,citationCount,referenceCount,venue,publicationDate,openAccessPdf,tldr,externalIds"

RATE_LIMIT_DELAY = 1.0  # seconds between requests (unauthenticated: be polite)


def api_get(url, api_key=None):
    """Make a GET request to the S2 API."""
    headers = {}
    if api_key:
        headers["x-api-key"] = api_key
    req = Request(url, headers=headers)
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        if e.code == 429:
            print("Rate limited. Waiting 10s...", file=sys.stderr)
            time.sleep(10)
            return api_get(url, api_key)
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def search_papers(query, limit=20, year=None, min_citations=None, sort="citationCount:desc",
                  fields=None, api_key=None):
    """Search papers by keyword."""
    params = {
        "query": query,
        "limit": str(limit),
        "fields": fields or DEFAULT_FIELDS,
        "sort": sort,
    }
    if year:
        params["year"] = year
    if min_citations:
        params["minCitationCount"] = str(min_citations)

    url = f"{BASE_URL}/paper/search?{urlencode(params)}"
    time.sleep(RATE_LIMIT_DELAY)
    return api_get(url, api_key)


def get_paper(paper_id, fields=None, api_key=None):
    """Get details for a single paper."""
    params = {"fields": fields or DEFAULT_FIELDS}
    url = f"{BASE_URL}/paper/{quote(paper_id, safe='')}?{urlencode(params)}"
    time.sleep(RATE_LIMIT_DELAY)
    return api_get(url, api_key)


def get_citations(paper_id, limit=100, fields=None, api_key=None):
    """Get papers that cite this paper."""
    params = {
        "fields": fields or "paperId,title,authors,year,citationCount,isInfluential",
        "limit": str(min(limit, 1000)),
    }
    url = f"{BASE_URL}/paper/{quote(paper_id, safe='')}/citations?{urlencode(params)}"
    time.sleep(RATE_LIMIT_DELAY)
    return api_get(url, api_key)


def get_references(paper_id, limit=100, fields=None, api_key=None):
    """Get papers cited by this paper."""
    params = {
        "fields": fields or "paperId,title,authors,year,citationCount,isInfluential",
        "limit": str(min(limit, 1000)),
    }
    url = f"{BASE_URL}/paper/{quote(paper_id, safe='')}/references?{urlencode(params)}"
    time.sleep(RATE_LIMIT_DELAY)
    return api_get(url, api_key)


def get_recommendations(paper_id, limit=50, fields=None, api_key=None):
    """Get recommended papers based on a seed paper."""
    params = {
        "fields": fields or DEFAULT_FIELDS,
        "limit": str(min(limit, 500)),
    }
    url = f"{REC_URL}/papers/forpaper/{quote(paper_id, safe='')}?{urlencode(params)}"
    time.sleep(RATE_LIMIT_DELAY)
    return api_get(url, api_key)


def format_paper(p):
    """Format a paper for display."""
    title = p.get("title", "No title")
    year = p.get("year", "N/A")
    citations = p.get("citationCount", 0)
    authors = ", ".join(a.get("name", "?") for a in (p.get("authors") or [])[:3])
    if len(p.get("authors") or []) > 3:
        authors += " et al."
    venue = p.get("venue", "")
    tldr = p.get("tldr", {}).get("text", "") if p.get("tldr") else ""
    pid = p.get("paperId", "")
    doi = (p.get("externalIds") or {}).get("DOI", "")

    lines = [
        f"## {title}",
        f"**Authors:** {authors} ({year})",
        f"**Venue:** {venue} | **Citations:** {citations}",
    ]
    if doi:
        lines.append(f"**DOI:** {doi}")
    if tldr:
        lines.append(f"**TLDR:** {tldr}")
    lines.append(f"**S2 ID:** {pid}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Semantic Scholar API utility")
    parser.add_argument("--api-key", help="S2 API key", default=None)
    sub = parser.add_subparsers(dest="command")

    # search
    s = sub.add_parser("search", help="Search papers")
    s.add_argument("query", help="Search query")
    s.add_argument("--limit", type=int, default=20)
    s.add_argument("--year", help="Year range (e.g., 2022-2024)")
    s.add_argument("--min-citations", type=int, help="Minimum citation count")
    s.add_argument("--sort", default="citationCount:desc")

    # paper
    p = sub.add_parser("paper", help="Get paper details")
    p.add_argument("paper_id", help="Paper ID (DOI, PMID, S2 ID, etc.)")

    # citations
    c = sub.add_parser("citations", help="Get papers citing this paper")
    c.add_argument("paper_id")
    c.add_argument("--limit", type=int, default=100)

    # references
    r = sub.add_parser("references", help="Get papers cited by this paper")
    r.add_argument("paper_id")
    r.add_argument("--limit", type=int, default=100)

    # recommend
    rec = sub.add_parser("recommend", help="Get paper recommendations")
    rec.add_argument("paper_id")
    rec.add_argument("--limit", type=int, default=50)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "search":
        result = search_papers(args.query, args.limit, args.year, args.min_citations,
                               args.sort, api_key=args.api_key)
        papers = result.get("data", [])
        print(f"Found {result.get('total', len(papers))} papers. Showing {len(papers)}:\n")
        for p in papers:
            print(format_paper(p))
            print()

    elif args.command == "paper":
        result = get_paper(args.paper_id, api_key=args.api_key)
        print(format_paper(result))
        if result.get("abstract"):
            print(f"\n**Abstract:** {result['abstract']}")

    elif args.command == "citations":
        result = get_citations(args.paper_id, args.limit, api_key=args.api_key)
        papers = result.get("data", [])
        print(f"Citations ({len(papers)}):\n")
        for c in papers:
            cp = c.get("citingPaper", c)
            print(format_paper(cp))
            print()

    elif args.command == "references":
        result = get_references(args.paper_id, args.limit, api_key=args.api_key)
        papers = result.get("data", [])
        print(f"References ({len(papers)}):\n")
        for r in papers:
            cp = r.get("citedPaper", r)
            inf = " [INFLUENTIAL]" if r.get("isInfluential") else ""
            print(format_paper(cp) + inf)
            print()

    elif args.command == "recommend":
        result = get_recommendations(args.paper_id, args.limit, api_key=args.api_key)
        papers = result.get("recommendedPapers", [])
        print(f"Recommendations ({len(papers)}):\n")
        for p in papers:
            print(format_paper(p))
            print()


if __name__ == "__main__":
    main()
