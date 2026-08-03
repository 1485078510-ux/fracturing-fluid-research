# Research Trend Patterns Reference

## Pattern Catalog

### 1. The Sleeper
- **Profile**: Published 2-3 years ago, initially low citations, now rapidly accelerating
- **Detection**: Citation velocity > 5/month, age > 12 months, total citations < 100
- **Interpretation**: Initially overlooked work whose importance is being recognized
- **Action**: Read immediately — may be an underappreciated breakthrough
- **Example**: A niche methodology paper that becomes standard practice after 2 years

### 2. The Burst
- **Profile**: Published <12 months ago, already high citation count
- **Detection**: Citation velocity > 10/month, age < 12 months
- **Interpretation**: Immediate high-impact, likely from well-known group or hot topic
- **Action**: Evaluate whether impact is genuine or hype-driven
- **Example**: LLM paper from major lab released with fanfare

### 3. The Steady Classic
- **Profile**: Published 5+ years ago, consistent citation rate over time
- **Detection**: Citation velocity stable (not accelerating), high total citations
- **Interpretation**: Foundational work with enduring relevance
- **Action**: Essential background reading for the field
- **Example**: "Attention Is All You Need" (Vaswani et al., 2017)

### 4. The Flash
- **Profile**: High initial citations that rapidly decline
- **Detection**: Citation velocity peaked and now declining, novelty-driven
- **Interpretation**: Trendy but ultimately less impactful
- **Action**: May not warrant deep investment; likely superseded
- **Example**: Initial papers on a hyped technique that was later abandoned

### 5. The Rising Tide
- **Profile**: Entire topic area showing rapid growth in publication volume
- **Detection**: Year-over-year publication count growth > 50%
- **Interpretation**: Emerging research frontier
- **Action**: Enter early to establish presence; high potential but uncertain direction
- **Example**: Graph neural networks circa 2018-2019

### 6. The Convergence
- **Profile**: Multiple independent groups publishing similar findings simultaneously
- **Detection**: Multiple papers from different groups with similar keywords/results in same period
- **Interpretation**: A problem whose time has come; multiple approaches converging
- **Action**: Compare approaches; look for the one that will become standard
- **Example**: Diffusion models in 2020-2021

### 7. The Fork
- **Profile**: A seminal paper spawning divergent research directions
- **Detection**: High citation count with citations clustering into distinct topic groups
- **Interpretation**: Foundational work enabling multiple lines of inquiry
- **Action**: Map the branching tree; identify which branch is most promising
- **Example**: BERT (2018) spawned encoder-only, fine-tuning, and pre-training research

### 8. The Twilight
- **Profile**: Previously active topic with declining publication rate
- **Detection**: Year-over-year publication count declining > 20%
- **Interpretation**: Solved problem, superseded approach, or funding shifted elsewhere
- **Action**: Don't start new projects here unless addressing remaining gaps
- **Example**: Traditional RNN variants after Transformer adoption

## Temporal Analysis Methods

### Publication Volume Curve
```
Papers
  ^
  |              *
  |            *   *
  |          *       *
  |        *           *
  |      *               *
  |    *                   *
  |  *                       *
  +------|------|------|------> Year
        2020   2021   2022   2023
```

Patterns:
- **Exponential growth** = emerging hot topic
- **Linear growth** = steadily active area
- **Plateau** = mature field
- **Decline** = fading topic

### Citation Velocity Heatmap
For papers in a topic, plot citation velocity vs. publication date:

```
Velocity
  ^
  |  *           * * *
  |    *       *       *
  |      *   *           *
  |        *               *
  +------|------|------|------> Year
        2021   2022   2023   2024

  Newer papers with high velocity = current hot papers
  Older papers with sustained velocity = classics
```

### Topic Evolution Tree
Map how sub-topics branch from a main topic over time:
```
                [Main Topic 2020]
               /        |        \
        [Sub A 2021]  [Sub B 2021]  [Sub C 2022]
         /      \          |
    [A1 2022] [A2 2023]  [B1 2023]
```

## Quantitative Trend Metrics

### Compound Annual Growth Rate (CAGR)
```
CAGR = (Final_Count / Initial_Count)^(1/Years) - 1
```
- CAGR > 30%: Explosive growth
- CAGR 10-30%: Strong growth
- CAGR 0-10%: Stable
- CAGR < 0%: Declining

### Citation Half-Life
Time for a paper to receive half its total citations:
- Short half-life (<1 year): Flash-in-pan or immediately impactful
- Medium half-life (1-3 years): Normal impact cycle
- Long half-life (>3 years): Enduring contribution or sleeper

### Field Momentum Index
```
Momentum = (Recent_Papers * Avg_Recent_Velocity) / (Total_Papers * Avg_Velocity)
```
- Momentum > 2.0: Field is accelerating
- Momentum 1.0-2.0: Healthy activity
- Momentum < 1.0: Field is decelerating
