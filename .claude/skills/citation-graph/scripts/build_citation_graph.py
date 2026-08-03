#!/usr/bin/env python3
"""Build and visualize citation graphs from Semantic Scholar API data."""

import argparse
import json
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode, quote

BASE_URL = "https://api.semanticscholar.org/graph/v1"
RATE_DELAY = 1.0


def api_get(url):
    req = Request(url)
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        if e.code == 429:
            print("Rate limited. Waiting 10s...", file=sys.stderr)
            time.sleep(10)
            return api_get(url)
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def resolve_paper(query_or_id):
    """Resolve a query to a paper ID."""
    if query_or_id.startswith("DOI:") or query_or_id.startswith("PMID:") or \
       query_or_id.startswith("ARXIV:") or len(query_or_id) == 40:
        return query_or_id

    # Try as a search
    params = urlencode({"query": query_or_id, "limit": "1",
                         "fields": "paperId,title"})
    url = f"{BASE_URL}/paper/search?{params}"
    time.sleep(RATE_DELAY)
    data = api_get(url)
    papers = data.get("data", [])
    if not papers:
        print(f"No paper found for: {query_or_id}", file=sys.stderr)
        sys.exit(1)
    paper = papers[0]
    print(f"Resolved to: {paper.get('title', 'Unknown')} ({paper['paperId']})",
          file=sys.stderr)
    return paper["paperId"]


def fetch_references(paper_id, limit=50):
    """Fetch references (prior works) for a paper."""
    params = urlencode({
        "fields": "paperId,title,authors,year,citationCount,isInfluential",
        "limit": str(limit)
    })
    url = f"{BASE_URL}/paper/{quote(paper_id, safe='')}/references?{params}"
    time.sleep(RATE_DELAY)
    return api_get(url).get("data", [])


def fetch_citations(paper_id, limit=50):
    """Fetch citations (derivative works) for a paper."""
    params = urlencode({
        "fields": "paperId,title,authors,year,citationCount,isInfluential",
        "limit": str(limit)
    })
    url = f"{BASE_URL}/paper/{quote(paper_id, safe='')}/citations?{params}"
    time.sleep(RATE_DELAY)
    return api_get(url).get("data", [])


def format_node_id(pid):
    return pid[:8]


def build_dot(target_id, target_title, refs, cites, output_file):
    """Build a Graphviz DOT file."""
    lines = [
        'digraph citation_graph {',
        '    rankdir=BT;',
        '    node [shape=box, style="filled,rounded", fontname="Helvetica", fontsize=9];',
        '    edge [color="#888888", arrowsize=0.6];',
        '',
    ]

    # Target node
    tid = format_node_id(target_id)
    safe_title = target_title.replace('"', '\\"')[:60] if target_title else "Target Paper"
    lines.append(f'    "{tid}" [label="{safe_title}", fillcolor="#FF6B6B", penwidth=2.0];')
    lines.append('')

    # Prior works
    lines.append('    // Prior Works')
    for ref in refs:
        paper = ref.get("citedPaper", ref)
        pid = paper.get("paperId", "")
        if not pid:
            continue
        nid = format_node_id(pid)
        authors = ", ".join(a.get("name", "?") for a in (paper.get("authors") or [])[:2])
        year = paper.get("year", "")
        label = f"{authors} ({year})" if authors else f"Paper ({year})"
        label = label.replace('"', '\\"')[:50]
        cite_count = paper.get("citationCount", 0)
        penwidth = 2.0 if ref.get("isInfluential") else 1.0
        lines.append(f'    "{nid}" [label="{label}", fillcolor="#4ECDC4"];')
        lines.append(f'    "{tid}" -> "{nid}" [penwidth={penwidth}];')
    lines.append('')

    # Derivative works
    lines.append('    // Derivative Works')
    for cite in cites:
        paper = cite.get("citingPaper", cite)
        pid = paper.get("paperId", "")
        if not pid:
            continue
        nid = format_node_id(pid)
        authors = ", ".join(a.get("name", "?") for a in (paper.get("authors") or [])[:2])
        year = paper.get("year", "")
        label = f"{authors} ({year})" if authors else f"Paper ({year})"
        label = label.replace('"', '\\"')[:50]
        penwidth = 2.0 if cite.get("isInfluential") else 1.0
        lines.append(f'    "{nid}" [label="{label}", fillcolor="#FFE66D"];')
        lines.append(f'    "{nid}" -> "{tid}" [penwidth={penwidth}];')
    lines.append('')

    lines.append('}')
    dot_content = "\n".join(lines)

    with open(output_file, "w") as f:
        f.write(dot_content)

    return dot_content


def build_json(target_id, target_title, refs, cites, output_file):
    """Build a JSON graph file."""
    nodes = []
    edges = []

    # Target node
    nodes.append({
        "id": target_id,
        "label": target_title or "Target Paper",
        "type": "target",
        "year": None,
        "citations": None
    })

    # Prior works
    for ref in refs:
        paper = ref.get("citedPaper", ref)
        pid = paper.get("paperId", "")
        if not pid:
            continue
        nodes.append({
            "id": pid,
            "label": paper.get("title", ""),
            "type": "prior",
            "year": paper.get("year"),
            "citations": paper.get("citationCount", 0)
        })
        edges.append({
            "source": target_id,
            "target": pid,
            "type": "cites",
            "influential": ref.get("isInfluential", False)
        })

    # Derivative works
    for cite in cites:
        paper = cite.get("citingPaper", cite)
        pid = paper.get("paperId", "")
        if not pid:
            continue
        nodes.append({
            "id": pid,
            "label": paper.get("title", ""),
            "type": "derivative",
            "year": paper.get("year"),
            "citations": paper.get("citationCount", 0)
        })
        edges.append({
            "source": pid,
            "target": target_id,
            "type": "cites",
            "influential": cite.get("isInfluential", False)
        })

    graph = {
        "nodes": nodes,
        "edges": edges,
        "metadata": {
            "seed_paper": target_id,
            "total_prior": len(refs),
            "total_derivative": len(cites)
        }
    }

    with open(output_file, "w") as f:
        json.dump(graph, f, indent=2)

    return graph


def main():
    parser = argparse.ArgumentParser(description="Build citation graph from S2 API")
    parser.add_argument("paper", help="Paper ID (DOI, PMID, S2 ID) or search query")
    parser.add_argument("--depth", type=int, default=1, help="Graph depth (1 or 2)")
    parser.add_argument("--limit", type=int, default=50, help="Max refs/citations to fetch")
    parser.add_argument("--output", default="citation_graph.dot", help="Output file")
    parser.add_argument("--format", choices=["dot", "json"], default="dot", help="Output format")
    parser.add_argument("--render", action="store_true", help="Render to PNG (requires graphviz)")
    args = parser.parse_args()

    # Resolve paper ID
    paper_id = resolve_paper(args.paper)

    # Get paper details
    params = urlencode({"fields": "title"})
    url = f"{BASE_URL}/paper/{quote(paper_id, safe='')}?{params}"
    time.sleep(RATE_DELAY)
    paper_data = api_get(url)
    target_title = paper_data.get("title", "Unknown Paper")

    print(f"Building citation graph for: {target_title}", file=sys.stderr)

    # Fetch references and citations
    refs = fetch_references(paper_id, args.limit)
    cites = fetch_citations(paper_id, args.limit)

    print(f"Found {len(refs)} references, {len(cites)} citations", file=sys.stderr)

    # Build graph
    if args.format == "dot":
        build_dot(paper_id, target_title, refs, cites, args.output)
        print(f"DOT file written to {args.output}", file=sys.stderr)

        if args.render:
            import subprocess
            png_file = args.output.replace(".dot", ".png")
            subprocess.run(["dot", "-Tpng", args.output, "-o", png_file], check=True)
            print(f"Rendered to {png_file}", file=sys.stderr)
    else:
        build_json(paper_id, target_title, refs, cites, args.output)
        print(f"JSON file written to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
