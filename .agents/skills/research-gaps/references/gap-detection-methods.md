# Gap Detection Methods — Detailed Reference

## Coverage Matrix Construction

### Building the Matrix
A coverage matrix maps papers (rows) against analysis dimensions (columns):

```
| Paper | Pop:Adults | Pop:Elderly | Pop:Children | Method:RCT | Method:Cohort | Out:Primary | Out:QoL |
|-------|:----------:|:-----------:|:------------:|:----------:|:-------------:|:-----------:|:-------:|
| A     |     ✓      |             |              |     ✓      |               |      ✓      |    ✓    |
| B     |     ✓      |             |              |            |       ✓       |      ✓      |         |
| C     |     ✓      |      ✓      |              |     ✓      |               |      ✓      |         |
| D     |            |             |      ✓       |            |       ✓       |      ✓      |         |
| E     |     ✓      |             |              |     ✓      |               |             |    ✓    |
|-------|:----------:|:-----------:|:------------:|:----------:|:-------------:|:-----------:|:-------:|
| Count |     4      |      1      |      1       |     3      |       2       |      4      |    2    |
| GAP?  |            |     ⚠️      |     ⚠️       |            |               |             |   ⚠️    |
```

### Gap Thresholds

| Papers on Topic | Relative to Mean | Gap Classification |
|---|---|---|
| 0 | — | **Complete gap** — no evidence exists |
| 1-2 | <20% of mean | **Severe gap** — minimal evidence |
| 3-5 | 20-50% of mean | **Moderate gap** — insufficient evidence |
| 6-10 | 50-80% of mean | **Mild gap** — emerging evidence |
| 10+ | >80% of mean | **Adequate coverage** |

## Automated Gap Detection Algorithms

### Algorithm 1: Keyword Co-occurrence Gap

```
1. Extract keywords from all papers (TF-IDF on titles + abstracts)
2. Build keyword co-occurrence matrix
3. For each keyword pair (A, B):
   - If A appears in N papers
   - And B appears in M papers
   - But A AND B appear in < expected papers
   - Expected = (N / total) * M
   - Gap score = expected - observed
4. High gap score = topic intersection that should exist but doesn't
```

### Algorithm 2: Method-Domain Transfer Gap

```
1. Catalog all (method, domain) pairs in the corpus
2. For each method used in domain X:
   - Check if method is also used in domain Y (adjacent domain)
   - If not, flag as transfer gap
3. Priority: methods with strong results in domain X
   that haven't been tried in adjacent domain Y
```

### Algorithm 3: Temporal Gap Detection

```
1. Group papers by topic (keyword clustering)
2. For each topic cluster:
   - Compute publication count per year
   - Fit a trend line
   - If trend is declining AND topic is not "solved":
     → Flag as abandoned topic (opportunity for revival)
   - If topic has 0 papers in most recent 2 years:
     → Flag as temporal gap
```

### Algorithm 4: Population Coverage Gap

```
1. For each paper, extract population descriptors
2. Build population taxonomy:
   - Age groups: neonatal, pediatric, adolescent, adult, elderly
   - Sex: male, female, mixed
   - Geography: by continent/country
   - Setting: hospital, community, rural, urban
   - Condition severity: mild, moderate, severe
3. For each cell in the taxonomy:
   - Count papers
   - Flag cells with 0 or significantly below average
4. Priority gaps: cells where adjacent cells are well-studied
   (e.g., adults well-studied but elderly not → strong gap signal)
```

## Gap Scoring Framework

### Multi-Criteria Gap Score

```
Gap_Score = w1 * Impact + w2 * Feasibility + w3 * Novelty + w4 * Timeliness

Default weights: w1=0.35, w2=0.25, w3=0.25, w4=0.15
```

### Impact Score (1-10)
- How many people would this research affect?
- How clinically/ practically significant is filling this gap?
- Is this a prerequisite for other important research?

### Feasibility Score (1-10)
- Can this be studied with existing methods?
- Are there existing datasets that could be used?
- How large a study would be needed?
- Are there ethical barriers?

### Novelty Score (1-10)
- How original would this research be?
- Is anyone else likely working on this?
- Would it create a new sub-field?

### Timeliness Score (1-10)
- Is there current momentum in this direction?
- Are there recent policy/regulatory changes creating urgency?
- Is this gap growing (becoming more important over time)?

## Gap Map Visualization

### Heatmap Format
```
              Method A  Method B  Method C  Method D
Population 1   ████████  ██████    ░░░░░░░░  ████░░░░
Population 2   ██████    ████░░    ░░░░░░░░  ░░░░░░░░ ← GAP
Population 3   ████░░    ░░░░░░    ░░░░░░░░  ██████
Population 4   ░░░░░░←G  ████░░    ██████    ████░░
```

█ = Well-studied (7+ papers)
░ = Gap (0-2 papers)

### Bubble Chart Format
- X-axis: Impact score
- Y-axis: Feasibility score
- Bubble size: Number of adjacent studies (potential for building on existing work)
- Color: Gap type (topic=blue, method=green, population=orange, outcome=red)

## Integration with Review Phases

Research gap identification is most valuable at two points:

1. **After initial literature search** — Identifies gaps before committing to a specific research question
2. **After systematic screening** — Identifies gaps in the included evidence base, informing the discussion section of a review

The second point is more reliable because it's based on a verified, deduplicated corpus.
