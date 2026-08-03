#!/usr/bin/env python3
"""Build author profile and collaboration graph from S2 API."""

import argparse
import json
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode
from collections import Counter, defaultdict

BASE_URL = "https://api.semanticscholar.org/graph/v1"
RATE_DELAY = 1.0


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


def search_author(name, limit=5):
    params = urlencode({"query": name, "limit": str(limit),
                         "fields": "name,affiliations,paperCount,citationCount,hIndex"})
    url = f"{BASE_URL}/author/search?{params}"
    time.sleep(RATE_DELAY)
    return api_get(url).get("data", [])


def get_author_papers(author_id, limit=500):
    params = urlencode({
        "fields": "title,year,citationCount,authors,venue,fieldsOfStudy",
        "limit": str(limit),
        "sort": "year:desc"
    })
    url = f"{BASE_URL}/author/{author_id}/papers?{params}"
    time.sleep(RATE_DELAY)
    return api_get(url).get("data", [])


def build_collaboration_graph(papers, target_id):
    """Build co-authorship graph."""
    collab = defaultdict(lambda: {"count": 0, "name": "", "years": []})

    for paper in papers:
        coauthors = [a for a in (paper.get("authors") or [])
                     if str(a.get("authorId", "")) != str(target_id)]
        for a in coauthors:
            aid = a.get("authorId", "unknown")
            collab[aid]["count"] += 1
            collab[aid]["name"] = a.get("name", "Unknown")
            if paper.get("year"):
                collab[aid]["years"].append(paper["year"])

    # Sort by collaboration frequency
    sorted_collabs = sorted(collab.items(), key=lambda x: x[1]["count"], reverse=True)

    nodes = []
    edges = []
    for aid, data in sorted_collabs[:50]:
        count = data["count"]
        if count >= 10:
            ctype = "core"
        elif count >= 5:
            ctype = "frequent"
        elif count >= 2:
            ctype = "occasional"
        else:
            ctype = "one_time"

        nodes.append({
            "id": aid,
            "name": data["name"],
            "papers_together": count,
            "type": ctype,
            "year_range": f"{min(data['years'])}-{max(data['years'])}" if data["years"] else "",
        })
        edges.append({
            "source": target_id,
            "target": aid,
            "weight": count,
        })

    return nodes, edges


def detect_evolution(papers):
    """Detect research direction changes over time."""
    periods = defaultdict(list)
    for p in papers:
        year = p.get("year")
        if not year:
            continue
        period = (year // 3) * 3
        periods[period].append(p)

    evolution = []
    for period in sorted(periods.keys()):
        pp = periods[period]
        words = Counter()
        for p in pp:
            title = (p.get("title") or "").lower()
            for w in title.split():
                if len(w) > 4 and w.isalpha():
                    words[w] += 1

        venues = Counter(p.get("venue") for p in pp if p.get("venue"))
        fields = Counter()
        for p in pp:
            for f in (p.get("fieldsOfStudy") or []):
                fields[f] += 1

        evolution.append({
            "period": f"{period}-{period+2}",
            "papers": len(pp),
            "top_keywords": [w for w, _ in words.most_common(5)],
            "top_venues": [v for v, _ in venues.most_common(3)],
            "fields": [f for f, _ in fields.most_common(3)],
        })

    return evolution


def format_report(author, papers, nodes, evolution):
    """Format author report."""
    lines = [
        f"# Author Profile: {author.get('name', 'Unknown')}",
        "",
        f"**Affiliation:** {', '.join(author.get('affiliations') or ['Unknown'])}",
        f"**Papers:** {author.get('paperCount', '?')} | "
        f"**Citations:** {author.get('citationCount', '?')} | "
        f"**h-index:** {author.get('hIndex', '?')}",
        "",
    ]

    # Research evolution
    lines.append("## Research Evolution")
    lines.append("")
    for evo in evolution:
        lines.append(f"**{evo['period']}** ({evo['papers']} papers)")
        lines.append(f"  Keywords: {', '.join(evo['top_keywords'])}")
        if evo["top_venues"]:
            lines.append(f"  Venues: {', '.join(evo['top_venues'][:3])}")
        lines.append("")

    # Top collaborators
    lines.append("## Top Collaborators")
    lines.append("")
    lines.append(f"{'Name':<30} {'Papers':<8} {'Type':<12} {'Years'}")
    lines.append("-" * 70)
    for n in nodes[:20]:
        lines.append(f"{n['name']:<30} {n['papers_together']:<8} "
                     f"{n['type']:<12} {n['year_range']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Build author profile and network")
    parser.add_argument("name", help="Author name to search")
    parser.add_argument("--limit", type=int, default=200, help="Max papers to analyze")
    parser.add_argument("--output", help="Output file (JSON or text)")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    # Search author
    authors = search_author(args.name)
    if not authors:
        print(f"Author not found: {args.name}", file=sys.stderr)
        sys.exit(1)

    author = authors[0]
    author_id = author["authorId"]
    print(f"Found: {author['name']} (ID: {author_id})", file=sys.stderr)

    # Get papers
    papers = get_author_papers(author_id, args.limit)
    print(f"Papers fetched: {len(papers)}", file=sys.stderr)

    # Build network
    nodes, edges = build_collaboration_graph(papers, author_id)
    evolution = detect_evolution(papers)

    if args.format == "json":
        result = {
            "author": author,
            "papers_count": len(papers),
            "collaborators": nodes,
            "edges": edges,
            "evolution": evolution,
        }
        output = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"Written to {args.output}", file=sys.stderr)
        else:
            print(output)
    else:
        report = format_report(author, papers, nodes, evolution)
        if args.output:
            with open(args.output, "w") as f:
                f.write(report)
            print(f"Written to {args.output}", file=sys.stderr)
        else:
            print(report)


if __name__ == "__main__":
    main()
