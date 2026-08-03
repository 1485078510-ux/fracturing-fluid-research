# Paper Comparison Framework — Extended Templates

## Clinical Trial Comparison Template

```markdown
| Dimension | Trial A | Trial B | Trial C |
|-----------|---------|---------|---------|
| **Study Design** | | | |
| Phase | | | |
| Blinding | | | |
| Randomization | | | |
| **Population** | | | |
| Sample Size | | | |
| Age Range | | | |
| Inclusion Criteria | | | |
| Exclusion Criteria | | | |
| **Intervention** | | | |
| Drug/Dose | | | |
| Duration | | | |
| Comparator | | | |
| **Outcomes** | | | |
| Primary Endpoint | | | |
| Primary Result | | | |
| p-value | | | |
| Effect Size | | | |
| Safety Profile | | | |
| **Quality** | | | |
| ITT Analysis | | | |
| Attrition Rate | | | |
| Funding Source | | | |
```

## Machine Learning Paper Comparison Template

```markdown
| Dimension | Paper A | Paper B | Paper C |
|-----------|---------|---------|---------|
| **Task** | | | |
| Problem Type | | | |
| Dataset(s) | | | |
| Metric(s) | | | |
| **Method** | | | |
| Architecture | | | |
| Training Strategy | | | |
| Key Innovation | | | |
| **Results** | | | |
| SOTA? | | | |
| Performance | | | |
| Ablation Done? | | | |
| **Reproducibility** | | | |
| Code Available | | | |
| Data Available | | | |
| Compute Required | | | |
| **Comparison** | | | |
| Shared Datasets | | | |
| Overlapping Methods | | | |
| Complementary? | | | |
```

## Social Science Paper Comparison Template

```markdown
| Dimension | Paper A | Paper B | Paper C |
|-----------|---------|---------|---------|
| **Theoretical Framework** | | | |
| Theory Used | | | |
| Key Constructs | | | |
| Hypotheses | | | |
| **Methodology** | | | |
| Qual/Quant/Mixed | | | |
| Data Collection | | | |
| Sampling Strategy | | | |
| Analysis Method | | | |
| **Sample** | | | |
| Size | | | |
| Demographics | | | |
| Context/Setting | | | |
| **Findings** | | | |
| Main Findings | | | |
| Effect Sizes | | | |
| Surprising Results | | | |
| **Validity** | | | |
| Internal Validity | | | |
| External Validity | | | |
| Reliability | | | |
```

## Agreement Matrix Template

For multi-paper comparison, create an agreement matrix:

```markdown
### Agreement Matrix: Does [intervention] improve [outcome]?

| Paper | Direction | Strength | Quality | Weight |
|-------|-----------|----------|---------|--------|
| A (2022) | Supports | Strong | High | ★★★ |
| B (2023) | Supports | Moderate | High | ★★★ |
| C (2022) | Neutral | N/A | Medium | ★★ |
| D (2023) | Refutes | Moderate | Medium | ★★ |
| E (2024) | Supports | Strong | High | ★★★ |

**Consensus: 3/5 Support, 1/5 Neutral, 1/5 Refute**
**Weighted Consensus: Strong Support** (high-quality papers converge)
```

## Methodological Rigor Comparison

```markdown
### Rigor Assessment

| Criterion | Paper A | Paper B | Paper C |
|-----------|---------|---------|---------|
| Pre-registration | ✓ | ✗ | ✓ |
| Power Analysis | ✓ | ✗ | ✗ |
| Replication | ✗ | ✓ | ✗ |
| Open Data | ✓ | ✓ | ✗ |
| Open Code | ✗ | ✗ | ✓ |
| Peer Review Type | Double | Single | Double |
| Conflict of Interest | None | Industry | None |

**Overall Rigor: A > C > B**
```
