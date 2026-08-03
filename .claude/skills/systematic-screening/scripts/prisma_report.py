#!/usr/bin/env python3
"""Generate PRISMA flow diagram from screening data."""

import argparse
import json
import sys


def generate_dot_diagram(data):
    """Generate Graphviz DOT for PRISMA flow diagram."""
    p = data.get("prisma", data)
    ident = p.get("identification", {})
    screen = p.get("screening", {})
    elig = p.get("eligibility", {})
    incl = p.get("included", {})

    sources = ident.get("sources", {})
    total = ident.get("total_identified", 0)
    dupes = screen.get("duplicates_removed", 0)
    screened = screen.get("records_screened", 0)
    excluded_ta = screened - (elig.get("sought_for_retrieval") or screened)
    sought = elig.get("sought_for_retrieval", screened - excluded_ta)
    not_retrieved = elig.get("not_retrieved", 0)
    assessed = elig.get("assessed_for_eligibility", sought - not_retrieved)
    excluded_ft = elig.get("excluded_fulltext", 0)
    included = incl.get("studies_included", assessed - excluded_ft)

    source_lines = "\\l".join([f"  {name}: n={count}" for name, count in sources.items()])

    dot = f"""digraph prisma {{
    rankdir=TB;
    node [shape=box, style="filled,rounded", fontname="Helvetica", fontsize=10,
          width=4, height=0.8, fillcolor="#F8F9FA", color="#DEE2E6"];
    edge [color="#6C757D", arrowsize=0.8];

    // Identification
    sources [label="Identification\\l{source_lines}\\l  Total: n={total}",
             fillcolor="#E3F2FD", color="#1565C0"];

    // Screening
    screened_node [label="Records screened\\nn={screened}",
                   fillcolor="#E8F5E9", color="#2E7D32"];
    dupes_node [label="Duplicates removed\\nn={dupes}",
                fillcolor="#FFF3E0", color="#E65100", style=filled];
    excluded_ta_node [label="Excluded by title/abstract\\nn={excluded_ta}",
                      fillcolor="#FFEBEE", color="#C62828"];

    // Eligibility
    sought_node [label="Sought for retrieval\\nn={sought}",
                 fillcolor="#E8F5E9", color="#2E7D32"];
    not_retrieved_node [label="Not retrieved\\nn={not_retrieved}",
                        fillcolor="#FFF3E0", color="#E65100"];
    assessed_node [label="Assessed for eligibility\\nn={assessed}",
                   fillcolor="#E8F5E9", color="#2E7D32"];
    excluded_ft_node [label="Excluded (full text)\\nn={excluded_ft}",
                      fillcolor="#FFEBEE", color="#C62828"];

    // Included
    included_node [label="Included in synthesis\\nn={included}",
                   fillcolor="#C8E6C9", color="#1B5E20", penwidth=2.0];

    // Edges
    sources -> screened_node;
    screened_node -> dupes_node [style=dashed];
    screened_node -> excluded_ta_node [style=dashed];
    screened_node -> sought_node;
    sought_node -> not_retrieved_node [style=dashed];
    sought_node -> assessed_node;
    assessed_node -> excluded_ft_node [style=dashed];
    assessed_node -> included_node;
}}"""

    return dot


def generate_text_diagram(data):
    """Generate ASCII PRISMA flow diagram."""
    p = data.get("prisma", data)
    ident = p.get("identification", {})
    screen = p.get("screening", {})
    elig = p.get("eligibility", {})
    incl = p.get("included", {})

    sources = ident.get("sources", {})
    total = ident.get("total_identified", "?")
    dupes = screen.get("duplicates_removed", "?")
    screened = screen.get("records_screened", "?")
    excluded_ta = screened - (elig.get("sought_for_retrieval") or screened) if isinstance(screened, int) else "?"
    sought = elig.get("sought_for_retrieval", "?")
    not_retrieved = elig.get("not_retrieved", 0)
    assessed = elig.get("assessed_for_eligibility", "?")
    excluded_ft = elig.get("excluded_fulltext", "?")
    included = incl.get("studies_included", "?")

    source_lines = "\n".join([f"  ├─ {name}: n={count}" for name, count in sources.items()])

    lines = [
        "┌──────────────────────────────────────────────────┐",
        "│              PRISMA 2020 Flow Diagram              │",
        "├──────────────────────────────────────────────────┤",
        "│                                                    │",
        "│  IDENTIFICATION                                    │",
        f"{source_lines}",
        f"  └─ Total identified: n={total}",
        "│                    ↓                               │",
        f"│  SCREENING                                         │",
        f"│  ├─ Duplicates removed: n={dupes}",
        f"│  └─ Records screened: n={screened}",
        f"│       ├─ Excluded (title/abstract): n={excluded_ta}",
        f"│       └─ Sought for retrieval: n={sought}",
        f"│            ├─ Not retrieved: n={not_retrieved}",
        f"│            └─ Assessed for eligibility: n={assessed}",
        f"│                 ├─ Excluded (full text): n={excluded_ft}",
        "│                 │   " + ", ".join(
            f"{k}: {v}" for k, v in (elig.get("excluded_reasons") or {}).items()
        ),
        f"│                 └─ INCLUDED: n={included}",
        "│                                                    │",
        "└──────────────────────────────────────────────────┘",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate PRISMA flow diagram")
    parser.add_argument("input", help="JSON file with screening data")
    parser.add_argument("--output", help="Output file (.dot, .png, or .txt)")
    parser.add_argument("--format", choices=["dot", "text", "png"], default="text")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    if args.format == "dot":
        result = generate_dot_diagram(data)
    elif args.format == "png":
        dot = generate_dot_diagram(data)
        import subprocess
        output_file = args.output or "prisma_flow.png"
        subprocess.run(["dot", "-Tpng", "-o", output_file],
                       input=dot, text=True, check=True)
        print(f"PRISMA diagram saved to {output_file}", file=sys.stderr)
        return
    else:
        result = generate_text_diagram(data)

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
