# Quality Assessment Tools — Complete Scoring Reference

## RoB 2 — Detailed Scoring (Randomized Controlled Trials)

### Domain 1: Risk of Bias Arising from the Randomization Process

| Question | Response | Signal |
|---|---|---|
| 1.1 Was the allocation sequence random? | Y/PY/PN/N/NI | |
| 1.2 Was the allocation sequence concealed? | Y/PY/PN/N/NI | |
| 1.3 Did baseline differences suggest a problem? | Y/PY/PN/N/NI | |

**Domain rating:**
- **Low**: Y/PY to 1.1 AND 1.2, AND N/PN to 1.3
- **Some concerns**: NI to 1.1 or 1.2, OR Y/PY to 1.3 with adequate randomization
- **High**: N/PN to 1.1 OR 1.2 AND Y/PY to 1.3

### Domain 2: Deviations from the Intended Interventions

| Question | Response |
|---|---|
| 2.1 Were participants aware of assignment? | Y/PY/PN/N/NI |
| 2.2 Were carers aware of assignment? | Y/PY/PN/N/NI |
| 2.3 Was there deviation from intended intervention? | Y/PY/PN/N/NI |
| 2.4 Were deviations likely to affect outcome? | Y/PY/PN/N/NI |
| 2.5 Were deviations balanced between groups? | Y/PY/PN/N/NI |
| 2.6 Was appropriate analysis used? | Y/PY/PN/N/NI |

**Domain rating:**
- **Low**: Participants AND carers blinded (PN/N to 2.1, 2.2), OR deviations not likely to affect
- **Some concerns**: Unblinded but no evidence of problematic deviations
- **High**: Unblinded AND evidence of problematic deviations

### Domain 3: Missing Outcome Data

| Question | Response |
|---|---|
| 3.1 Data for all randomized participants? | Y/PY/PN/N/NI |
| 3.2 Missing data for primary outcome? | Y/PY/PN/N/NI |
| 3.3 Missing data balanced between groups? | Y/PY/PN/N/NI |
| 3.4 Potential impact of missing data assessed? | Y/PY/PN/N/NI |

**Domain rating:**
- **Low**: No missing data, OR missing data unlikely to bias results
- **Some concerns**: Missing data but sensitivity analyses suggest robustness
- **High**: Missing data likely to bias results

### Domain 4: Measurement of the Outcome

| Question | Response |
|---|---|
| 4.1 Inappropriate measurement method? | Y/PY/PN/N/NI |
| 4.2 Could measurement differ between groups? | Y/PY/PN/N/NI |
| 4.3 Assessors aware of intervention received? | Y/PY/PN/N/NI |
| 4.4 Assessment likely influenced by knowledge? | Y/PY/PN/N/NI |

**Domain rating:**
- **Low**: Outcome measured objectively, OR assessors blinded
- **Some concerns**: Subjective outcome, blinding uncertain
- **High**: Subjective outcome AND unblinded assessment

### Domain 5: Selection of the Reported Result

| Question | Response |
|---|---|
| 5.1 Results selected from multiple measurements? | Y/PY/PN/N/NI |
| 5.2 Results selected from multiple analyses? | Y/PY/PN/N/NI |
| 5.3 Registration consistent with publication? | Y/PY/PN/N/NI |

**Domain rating:**
- **Low**: Pre-registered protocol matches publication
- **Some concerns**: No registration, or minor discrepancies
- **High**: Major discrepancies between registered and published results

### Overall Rating Algorithm

```
IF any domain = high:
    overall = HIGH
ELIF multiple domains = some_concerns:
    overall = HIGH  (multiple concerns compound)
ELIF any domain = some_concerns:
    overall = SOME_CONCERNS
ELSE:
    overall = LOW
```

## Newcastle-Ottawa Scale — Cohort Studies

### Selection (max 4 stars)

| Item | ★ Criteria | 0 Criteria |
|---|---|---|
| Representativeness of exposed cohort | Truly representative OR somewhat representative | Selected group OR no description |
| Selection of non-exposed cohort | From same community | Different community OR no description |
| Ascertainment of exposure | Secure record OR structured interview | Written self-report OR no description |
| Demonstration that outcome not present at start | Yes | No |

### Comparability (max 2 stars)

| Item | ★ Criteria |
|---|---|
| Comparability on main factor | Controlled for age/sex/other main factor |
| Comparability on additional factor | Controlled for any additional factor |

### Outcome (max 3 stars)

| Item | ★ Criteria | 0 Criteria |
|---|---|---|
| Assessment of outcome | Independent blind assessment OR record linkage | Self-report OR no description |
| Was follow-up long enough? | Yes (justify based on outcome) | No |
| Adequacy of follow-up | >80% follow-up | <80% OR no description |

### Quality Thresholds

| Stars | Rating | Interpretation |
|---|---|---|
| 7-9 | Good | High quality, reliable results |
| 4-6 | Fair | Moderate quality, some concerns |
| 0-3 | Poor | Low quality, results should be interpreted cautiously |

## AMSTAR 2 — Critical Items

Items 4, 7, 9, 11, 12, and 15 are **critical weaknesses**. The overall confidence depends on critical weaknesses:

| Critical Weaknesses | Non-Critical Weaknesses | Overall Confidence |
|---|---|---|
| 0 | ≤4 | High |
| 0 | >4 | Moderate |
| 1 | ≤4 | Moderate |
| 1 | >4 | Low |
| >1 | Any | Critically Low |

## CASP Qualitative — Decision Algorithm

```
Screening:
  Q1 (clear aims?): Yes → continue; No/Can't tell → consider excluding
  Q2 (qualitative appropriate?): Yes → continue; No → wrong design

Design:
  Q3 (appropriate design?): evaluate rigor
  Q4 (appropriate recruitment?): consider selection bias
  Q5 (appropriate data collection?): evaluate data quality

Data:
  Q6 (researcher-participant relationship?): consider reflexivity
  Q7 (ethical issues?): consider ethics approval, informed consent
  Q8 (rigorous analysis?): consider audit trail, triangulation

Findings:
  Q9 (clear findings?): evaluate clarity and sufficiency
  Q10 (how valuable?): assess contribution to knowledge

Overall:
  All Yes → Rigorous
  Some Can't Tell → Acceptable (with caveats)
  Any No → Flawed (in that dimension)
```

## QUADAS-2 — Diagnostic Accuracy Studies

### 4 Domains

1. **Patient Selection**: Was selection consecutive/random? Were case-control design or inappropriate exclusions avoided?
2. **Index Test**: Were conduct and interpretation pre-specified? Was blinding applied?
3. **Reference Standard**: Is the reference standard accurate? Was it interpreted without knowledge of index test?
4. **Flow and Timing**: Was interval between tests appropriate? Were all patients verified by reference standard? Were withdrawals explained?

Each domain rated: **Low / High / Unclear** risk of bias + applicability concerns.
