# Author Network API Patterns Reference

## Semantic Scholar Author API

### Search for Author
```bash
GET https://api.semanticscholar.org/graph/v1/author/search?query=Andrew+Ng&limit=5&fields=name,affiliations,paperCount,citationCount,hIndex
```

Response:
```json
{
  "data": [
    {
      "authorId": "1739253",
      "name": "Andrew Y. Ng",
      "affiliations": ["Stanford University"],
      "paperCount": 398,
      "citationCount": 189543,
      "hIndex": 142
    }
  ]
}
```

### Get Author Details
```bash
GET https://api.semanticscholar.org/graph/v1/author/1739253?fields=name,affiliations,paperCount,citationCount,hIndex,homepage
```

### Get Author's Papers (sorted by year)
```bash
GET https://api.semanticscholar.org/graph/v1/author/1739253/papers?fields=title,year,citationCount,authors,venue&limit=500&sort=year:desc
```

### Get Author's Papers (sorted by citations)
```bash
GET https://api.semanticscholar.org/graph/v1/author/1739253/papers?fields=title,year,citationCount,authors,venue&limit=500&sort=citationCount:desc
```

## OpenAlex Author API

### Search Author
```bash
GET https://api.openalex.org/authors?search=Andrew+Ng&per_page=5
```

### Get Author Details
```bash
GET https://api.openalex.org/authors/A502388
```

Response includes:
- `works_count` — Total publications
- `cited_by_count` — Total citations
- `summary_stats` — h-index, i10-index, 2yr mean citedness
- `affiliations` — Current and past institutions with dates
- `topics` — Research topic distribution with counts
- `x_concepts` — Concept areas with scores

### Get Author's Works
```bash
GET https://api.openalex.org/works?filter=author.id:A502388&sort=publication_year:desc&per_page=50
```

### Get Co-Authors
```bash
GET https://api.openalex.org/authors?filter=coauthor_with:A502388&per_page=50
```

## Collaboration Graph Building Pattern

```python
from collections import defaultdict

def build_collaboration_graph(papers, target_author_id):
    """Build co-authorship graph from author's papers."""
    collaborator_weights = defaultdict(int)
    collaborator_years = defaultdict(list)

    for paper in papers:
        coauthors = [a for a in paper.get("authors", [])
                     if a.get("authorId") != target_author_id]
        for coauthor in coauthors:
            aid = coauthor.get("authorId")
            collaborator_weights[aid] += 1
            collaborator_years[aid].append(paper.get("year"))

    # Classify collaborators
    graph_nodes = []
    graph_edges = []
    for aid, weight in collaborator_weights.items():
        if weight >= 10:
            collab_type = "core"
        elif weight >= 5:
            collab_type = "frequent"
        elif weight >= 2:
            collab_type = "occasional"
        else:
            collab_type = "one_time"

        years = collaborator_years[aid]
        graph_nodes.append({
            "id": aid,
            "name": next((a["name"] for p in papers for a in p.get("authors", [])
                         if a.get("authorId") == aid), "Unknown"),
            "papers_together": weight,
            "type": collab_type,
            "years": sorted(set(y for y in years if y)),
        })
        graph_edges.append({
            "source": target_author_id,
            "target": aid,
            "weight": weight,
            "type": "coauthor",
        })

    return {"nodes": graph_nodes, "edges": graph_edges}
```

## Research Evolution Detection Pattern

```python
from collections import Counter

def detect_research_evolution(papers, target_author_id):
    """Detect how research focus changes over time."""
    # Group papers by year period (2-year windows)
    periods = defaultdict(list)
    for paper in papers:
        year = paper.get("year")
        if not year:
            continue
        period_start = (year // 2) * 2
        period_label = f"{period_start}-{period_start+1}"
        periods[period_label].append(paper)

    evolution = []
    for period in sorted(periods.keys()):
        period_papers = periods[period]
        # Extract top keywords from titles
        words = Counter()
        for p in period_papers:
            title = (p.get("title") or "").lower()
            for word in title.split():
                if len(word) > 4 and word.isalpha():
                    words[word] += 1

        # Get venues
        venues = Counter(p.get("venue") for p in period_papers if p.get("venue"))

        evolution.append({
            "period": period,
            "paper_count": len(period_papers),
            "top_keywords": words.most_common(5),
            "top_venues": venues.most_common(3),
        })

    return evolution
```

## Academic Genealogy Detection Heuristics

```python
def detect_genealogy(papers, target_author_id):
    """Infer academic lineage from publication patterns."""
    # Find earliest papers
    early_papers = sorted(
        [p for p in papers if p.get("year")],
        key=lambda p: p["year"]
    )[:10]

    # Identify likely advisor: senior author on multiple early papers
    advisor_candidates = Counter()
    for paper in early_papers:
        authors = paper.get("authors", [])
        if len(authors) >= 2:
            # Last author on early papers is often the advisor
            last_author = authors[-1]
            if last_author.get("authorId") != target_author_id:
                advisor_candidates[last_author.get("authorId")] += 1

    likely_advisor = advisor_candidates.most_common(1)

    # Identify likely mentees: first author on recent papers where target is last author
    recent_papers = sorted(papers, key=lambda p: p.get("year", 0), reverse=True)[:20]
    mentee_candidates = Counter()
    for paper in recent_papers:
        authors = paper.get("authors", [])
        if len(authors) >= 2:
            if authors[-1].get("authorId") == target_author_id:
                first_author = authors[0]
                if first_author.get("authorId") != target_author_id:
                    mentee_candidates[first_author.get("authorId")] += 1

    likely_mentees = mentee_candidates.most_common(5)

    return {
        "likely_advisor": likely_advisor,
        "likely_mentees": likely_mentees,
    }
```
