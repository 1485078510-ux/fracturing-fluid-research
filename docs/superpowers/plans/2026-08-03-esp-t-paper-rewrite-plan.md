# ESP-T Paper Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite three source materials into a single, self-contained SCI manuscript targeting *Geoenergy Science and Engineering*, built around the physical self-calibration framework where Q converges to the pump setting without constraint.

**Architecture:** 7-section manuscript (~7000 words, 10 figures, ~35 refs) following a 5-step non-circular logical cascade: Problem Diagnosis → Model Construction → Decisive Self-Calibration Test → Independent Corroboration → Engineering Deployment. Material characterization is compressed to prerequisite verification only. The Q self-calibration (fit = 0.46 vs pump = 0.50, ±8%) is the paper's centerpiece argument.

**Tech Stack:** Python 3 (python-docx for output), nature-writing skill for academic prose, nature-citation skill for references. Source materials read via `scripts/office.py read`.

## Global Constraints

- Target journal: *Geoenergy Science and Engineering* (formerly JPSE) — petroleum engineering focus, experimental + modeling
- Total length: ~7000 words main text, ~35 references
- All key data points (21-point BTC, K-P parameters, two-phase flow) must reference Supplementary Material tables
- Material characterization serves as model prerequisite verification, NOT as material innovation
- Q self-calibration argument must explicitly state that Q search bounds were [10, 5000] mL/min (500× range, no bias)
- K-P and ADE must be framed as independent experiments (different apparatus, different data, different fitting targets)
- Every section must answer "why this matters for getting Q from BTC"
- All figures placed inline with captions; figure panels described in captions
- Prose style: engineering-journal register — precise, declarative, minimal hedging
- Statistics (AICc, F-test) support but do not lead; the Q self-calibration is the lead argument
- Reference format: numbered [1], [2], etc. per *Geoenergy Science and Engineering* style

---

### Task 1: Paper Skeleton and Template Setup

**Files:**
- Create: `四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx`
- Reference (read-only): `docs/superpowers/specs/2026-08-03-esp-t-paper-rewrite-design.md`

**Interfaces:**
- Produces: Empty DOCX with all section headers, figure placeholders, and reference slots — the structural skeleton that all subsequent tasks write into

- [ ] **Step 1: Create manuscript DOCX with full section structure**

Use `scripts/office.py new docx` to create the file, then populate with the following structure (each section header as a Heading 1 or Heading 2):

```
Title: [TBD — written in Task 12 after all content is final]

Abstract
Keywords

1. Introduction

2. Coupled Release–Transport Model
   2.1 Physical Basis
   2.2 Governing Equations
   2.3 Parameter Set and Derived Quantities
   2.4 Validation Strategy: Self-Calibration as Decisive Test

3. Experimental Methods
   3.1 ESP-T Synthesis
   3.2 Material Prerequisites for Model Validity
   3.3 K-P Batch Release Kinetics
   3.4 Core Displacement: BTC Generation
   3.5 Parameter Estimation Strategy

4. Results and Discussion
   4.1 Model Selection: Single-Process Models Are Insufficient
   4.2 Physical Self-Calibration: The Flow-Rate Test
   4.3 Comparison with Time-of-Arrival Methods
   4.4 Independent Corroboration: K-P Kinetics and ADE Peclet Number
   4.5 Signal Decomposition and Robustness

5. Extension to Two-Phase Production Allocation
   5.1 Physical Context
   5.2 The Dilution Problem and the Flux Solution
   5.3 Flux-to-Production-Rate Calibration
   5.4 Coupling to the BTC Framework

6. Field Deployment Pathway

7. Conclusions

References
[numbered list, 35 slots — populated in Task 11]

Figure Captions
[10 figure caption slots — populated as figures are placed]

Tables
[Table slots — populated as content is written]
```

- [ ] **Step 2: Place figure markers in each section**

Insert `[Fig. N placeholder — see Figure Captions]` markers at the locations specified in the design doc:
- Fig. 1: Section 2.1 (BTC generation schematic)
- Fig. 2: Section 3.2 (ESP-T characterization summary, 4-panel)
- Fig. 3: Section 4.1 (K-P kinetics + model selection overlay)
- Fig. 4: Section 4.1 (5-model overlay + ΔAICc bar chart)
- Fig. 5: Section 4.2 (CENTERPIECE — BTC decomposition + Q self-calibration bar)
- Fig. 6: Section 4.3 (TOA method comparison)
- Fig. 7: Section 4.4 (K-P ↔ Pe independent corroboration dual panel)
- Fig. 8: Section 4.5 (σ sensitivity analysis)
- Fig. 9: Section 5.2 (Two-phase flow 3-panel)
- Fig. 10: Section 6 (Field deployment pathway schematic)

- [ ] **Step 3: Verify skeleton structure**

Check the DOCX against the design spec section 3 ("Paper Structure"). Confirm:
- All 7 main sections present
- All subsections in Section 2, 3, 4, and 5 present
- Figure markers at correct locations
- No orphaned subsections

- [ ] **Step 4: Commit skeleton**

```bash
git add "四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx"
git commit -m "feat: create paper skeleton with section structure and figure markers"
```

---

### Task 2: Write Section 2 — The Coupled Release–Transport Model (~1500 words)

**Files:**
- Modify: `四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx` — Section 2
- Reference (read-only): Source material `ESP-T_Final_4-revised.docx` Section 3.3 (Piecewise ADE Modeling) for equations
- Reference (read-only): Source material `Supplementary_Material.docx` Section S5 (Extended Derivations)

**Interfaces:**
- Consumes: Skeleton structure from Task 1
- Produces: Complete Section 2 with all equations properly formatted. Defines the model that Sections 4.1–4.5 test and validate.
- Key symbols defined here and used throughout: C(t), z, C_rise, C_fall, w(t), c_b, A, a, α, Q, t₀, σ, Pe, v, MRT

- [ ] **Step 1: Write Section 2.1 — Physical Basis (~300 words)**

Content to write, based on design doc §2.1:

"Shut-in operation forces two tracer sources: (I) tracer accumulates in near-wellbore region during shut-in → swept as coherent slug upon flowback → Gaussian pulse; (II) polymer matrix continues swelling and releasing tracer → sustained concentration tail. These are physically irreducible — not a model selection choice but a consequence of the experimental shut-in."

- Describe the shut-in → accumulation → flowback sequence in engineering terms
- Use schematic Fig. 1 as visual anchor
- No equations yet — just the physical picture

- [ ] **Step 2: Write Section 2.2 — Governing Equations (~600 words)**

Extract exact equation forms from source material ESP-T_Final_4-revised.docx lines 58-73. Write:

1. ADE backbone: ∂C/∂t + v·∂C/∂x = D·∂²C/∂x²
2. Tube-flow substitution: v = 4Q/(πd²), D = α·v
3. Dimensionless z variable: z = (xπd² − 4Qt) / √(16αQtπd²)
4. Gaussian component: C_rise(t) = c_b + (A·d)/√(16παQt·d²) × exp(−z²)
5. erfc component: C_fall(t) = c_b + (a/2) × erfc(−z)
6. Tanh blending: w(t) = ½[1 + tanh((t₀ − t)/σ)]
7. Full model (Eq. 1): C(t) = c_b + w(t)·C_rise(t) + [1 − w(t)]·C_fall(t)

Explain each component's physical origin. Note C¹ continuity. State that σ is fitted (~sampling interval) but x, d are fixed geometry (x = 100 mm, d = 5 mm).

- [ ] **Step 3: Write Section 2.3 — Parameter Set (~200 words)**

Insert the parameter table from design doc §2.3:

| Parameter | Symbol | Origin | Physical Meaning |
|-----------|--------|--------|------------------|
| Baseline | c_b | Both | Asymptotic plateau |
| Pulse amplitude | A | Rise | Accumulated tracer mass |
| Tail amplitude | a | Fall | Sustained-release source strength |
| Dispersivity | α | Rise | Longitudinal dispersion |
| Flow rate | Q | Rise | **Target — UNCONSTRAINED in fit** |
| Crossover time | t₀ | Both | Slug-to-tail transition |
| Transition width | σ | Both | Fitted ~ sampling interval |

Derived: Pe = x/α, v = 4Q/(πd²), MRT = x/v.

State explicitly: "Q is bounded to [10, 5000] mL/min in the optimization (Table S6) — a 500-fold range — and receives no penalty, prior, or constraint toward the pump setting."

- [ ] **Step 4: Write Section 2.4 — Validation Strategy (~300 words)**

From design doc §2.4. Key argument in engineering language:

"Standard validation (R², RMSE) cannot distinguish a physically correct model from an overfitted one with the same number of parameters. Our validation is predictive: Q is a physical quantity with an independent known value (pump = 0.50 mL/min). If the model structure is incorrect, the optimizer will assign Q an arbitrary value within [10, 5000] that minimizes residuals. If Q consistently converges to ~0.50 across independent searches, the model structure must correctly capture the transport physics. This test is falsifiable — if Q converges to 2.3 or 0.07, the model is wrong regardless of R²."

- [ ] **Step 5: Verify Section 2 against design spec and source equations**

Cross-check:
- Equation forms match Supplementary Material S5 exactly
- z variable definition consistent with both source materials
- Parameter table matches design spec §2.3
- "Q unconstrained" stated explicitly with bound ranges
- Fig. 1 marker in 2.1

- [ ] **Step 6: Commit Section 2**

```bash
git add "四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx"
git commit -m "feat: write Section 2 — Coupled Release–Transport Model"
```

---

### Task 3: Write Section 3 — Experimental Methods (~1000 words, COMPRESSED)

**Files:**
- Modify: `四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx` — Section 3
- Reference (read-only): Source material `ESP-T_Final_4-revised.docx` Sections 2.1–2.5
- Reference (read-only): Source material `环氧+四氧化三铁改4.10.docx` Sections 2.1–2.6
- Reference (read-only): Source material `Supplementary_Material.docx` Sections S1–S4

**Interfaces:**
- Consumes: Section 2 defining the model; skeleton from Task 1
- Produces: Complete Section 3. Defines materials and methods referenced by all Results subsections. All procedural detail beyond the essentials is deferred to Supplementary Material.

- [ ] **Step 1: Write Section 3.1 — ESP-T Synthesis (one paragraph, ~150 words)**

Condense from both source materials. Template:

"ESP-T was synthesized in three steps (Fig. S1). (i) Stearic acid-modified nano-Fe₃O₄ (nano-Fe₃O₄@SA) was prepared by co-precipitation: 2.703 g FeCl₃ and 1.15 g FeCl₂·4H₂O in 100 mL deionized water at 80°C under N₂, doped with 2×10⁻⁵ mol MnCl₂·6H₂O; 5.5 mL NH₃·H₂O added, pH 10, 2 h; precipitate magnetically separated, washed, sonicated with ethanolic stearic acid. (ii) A pre-mixture of 20 mL E51 epoxy resin, ~0.75 g nano-Fe₃O₄@SA (~3.3 wt%), 1 g hollow glass microspheres, and 7 g T31 curing agent was homogenized. (iii) The pre-mixture was emulsified in a SiO₂/guar gum aqueous dispersion and cured at 50°C (1 h), then rinsed and dried at 80°C (10 h). Pure epoxy microspheres were prepared identically without nano-Fe₃O₄@SA as a reference. The co-precipitation method accommodates other transition metals (Zn, Cu, Co, Ni) and rare earths (Eu, Dy, Nd) for multi-stage coding."

No material-innovation claims. Reagent specifications → Table S1.

- [ ] **Step 2: Write Section 3.2 — Material Prerequisites (tabular, ~300 words)**

From design doc §3.2. Four-row table:

| Prerequisite | Method | Result | Implication for Model |
|-------------|--------|--------|----------------------|
| Tracer in matrix | SEM-EDS cross-section | Fe distributed throughout particle | Confirms bulk encapsulation → sustained source term valid |
| Thermal stability | TGA/DTG (air, 10°C/min) | Decomp. onset 357°C | No degradation at 80–200°C downhole → K-P kinetics valid |
| Non-Fickian release | K-P batch, Mt/M∞ < 0.6 | n = 0.45–0.85 | Swelling-diffusion mechanism → erfc tail physically justified |
| Oil-phase selectivity | WCA + filtration | WCA 104.6°, oil/water time ratio 5.53 | Tracer signal isolated from water dilution → flux method valid |

Include Fig. 2 marker (4-panel: SEM + EDS Fe map + TGA + WCA). Note: "Detailed characterization protocols → Supplementary Material S2. Complete property data → Table S4."

- [ ] **Step 3: Write Section 3.3 — K-P Batch Release Kinetics (~150 words)**

"ESP-T (5 g, 40–70 mesh) was immersed in 100 mL dodecane in sealed vials at 30, 60, 90, and 120°C (thermostatic oil baths). Sampling at 12-h intervals over 14 days; tracer metal ion concentration quantified by ICP-MS (PerkinElmer NexION 300X). Release data within Mt/M∞ < 0.6 were fitted to the Korsmeyer-Peppas power law, C/C₀ = K·tⁿ. Full release dataset → Table S3."

- [ ] **Step 4: Write Section 3.4 — Core Displacement (~200 words)**

From ESP-T_Final_4-revised.docx 2.5. Key details:

- Steel core packed with ESP-T, 200-mesh screens, 5 MPa confining pressure
- Single-phase: Saturated with dodecane at 5 mL/min, shut in 96 h, displaced at 0.50 mL/min, effluent sampled at 4-min intervals (2 mL/sample, 21 samples), ICP-MS
- Two-phase: Dodecane + deionized water, OWR = 4:1, 1:1, 1:4, total flow 0.1–0.4 mL/min, steady-state, 5-min sampling intervals
- Note: Fig. S2 (apparatus schematic)

State the key experimental parameters explicitly: pump setting = 0.50 mL/min (this is the independent reference against which Q_fit is compared in Section 4.2).

- [ ] **Step 5: Write Section 3.5 — Parameter Estimation Strategy (~200 words)**

From the revised design doc §3.5. Engineering language:

Two-pass strategy for the inverse problem:
- Pass 1 — Basin location: Global search over wide physically bounded parameter ranges using multiple independent initializations. Q bounded [10, 5000] mL/min (500× range). Four independent runs with different random starts verify consistent basin location.
- Pass 2 — Local refinement: Gradient-based refinement from Pass-1 best point. Converged within 50–200 iterations, confirming Pass 1 located the correct basin.
- All five candidate models subjected to identical protocol (same bounds, convergence criteria, independent runs) for fair comparison.
- Detailed bounds → Table S6. Optimization implementation → Supplementary Material S5.3.

Do NOT mention: population size, crossover rate, mutation strategy, ftol, gtol, max generations. These go in Supplementary Material only.

- [ ] **Step 6: Verify Section 3**

Check against design spec §3:
- Synthesis ≤ one paragraph, no material-innovation language
- Prerequisites table has 4 rows matching the 4 model assumptions
- Pump setting 0.50 mL/min stated explicitly in 3.4
- Q search bounds [10, 5000] stated explicitly in 3.5
- All cross-references to Supplementary Material correct

- [ ] **Step 7: Commit Section 3**

```bash
git add "四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx"
git commit -m "feat: write Section 3 — Experimental Methods (compressed)"
```

---

### Task 4: Write Section 4.1 — Model Selection (~400 words)

**Files:**
- Modify: `四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx` — Section 4.1
- Reference (read-only): Source material `ESP-T_Final_4-revised.docx` — Table 4 (model selection statistics)

**Interfaces:**
- Consumes: Model definition (Section 2), experimental data (Section 3.4)
- Produces: Statistical evidence that single-process models cannot capture the BTC. Sets up the necessity argument that Section 4.2's self-calibration test then makes decisive.

- [ ] **Step 1: Write Section 4.1 text (~350 words)**

Key points from design doc §4.1:

1. Present the 5-model comparison table (reproduce exact values from source Table 4):
   - Dual-component tanh-blended (k=7, R²=0.9939, RMSE=0.0210, AICc=−139.70, ΔAICc=0)
   - Single Gaussian (k=4, R²=0.9482, RMSE=0.0609, AICc=−107.04, ΔAICc=32.66)
   - Single erfc (k=4, R²=0.7159, RMSE=0.1427, AICc=−71.28, ΔAICc=68.42)
   - Exponential decay (k=3, R²=0.7517, RMSE=0.1334, AICc=−77.20, ΔAICc=62.51)
   - K-P power law (k=3, R²=−0.0193, RMSE=0.2703, AICc=−47.54, ΔAICc=92.16)

2. F-test: F(3, 14) = 34.70, p < 10⁻⁶

3. CRITICAL framing (per design spec): "Single-process models each capture ONE feature of the BTC — the Gaussian fits the peak but misses the tail; the erfc captures the tail but cannot reproduce the peak. The AICc evidence is strong but is presented as a NECESSARY, not SUFFICIENT, condition. The decisive test — whether the model structure captures real physics — is addressed in Section 4.2."

4. Fig. 4 marker: 5-model overlay on BTC + ΔAICc bar chart

Do NOT claim "AICc proves the model is correct." The language must be: "AICc eliminates the single-process alternatives; Section 4.2 provides the positive test."

- [ ] **Step 2: Verify Section 4.1**

Check:
- All 5 model statistics match source Table 4 exactly
- F-test values correct
- "Necessary but not sufficient" framing explicit
- Explicit pointer to Section 4.2 for the decisive test

- [ ] **Step 3: Commit Section 4.1**

```bash
git add "四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx"
git commit -m "feat: write Section 4.1 — Model Selection"
```

---

### Task 5: Write Section 4.2 — Physical Self-Calibration: The Flow-Rate Test (~600 words)

**Files:**
- Modify: `四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx` — Section 4.2
- Reference (read-only): Source material `ESP-T_Final_4-revised.docx` — Table 3 (fitted parameters), text lines 85-86

**Interfaces:**
- Consumes: Model definition (Section 2), optimization protocol (Section 3.5), model selection context (Section 4.1)
- Produces: The paper's centerpiece argument. All subsequent sections reference this result.

- [ ] **Step 1: Write the BTC decomposition description (~200 words)**

Present the fitted parameters (from source Table 3):
| Parameter | Symbol | Value | Units |
|-----------|--------|-------|-------|
| Baseline | c_b | 0.0459 | — |
| Pulse amplitude | A | 2334 | — |
| Tail amplitude | a | 0.431 | — |
| Dispersivity | α | 107.1 | cm |
| Flow rate | Q | 0.46 | mL/min |
| Transition center | t₀ | 25.66 | min |
| Transition width | σ | 3.96 | min |
| R² | — | 0.9939 | — |

Describe the fitted BTC (Fig. 5a) with Gaussian (53%) and erfc (47%) components shaded. Show residuals (Fig. 5b).

- [ ] **Step 2: Write the self-calibration argument (~350 words)**

This is the paper's most important passage. From design doc §4.2 revised argument structure:

"The model has six free parameters — enough degrees of freedom to overfit. However, extra parameters only improve curve-matching; they do not produce physically correct parameter values. If the model structure is incorrect, the optimizer will assign Q whatever value helps match the curve shape, with compensating adjustments in A and α to maintain the fit.

Yet Q consistently settles at 0.46 ± 0.02 mL/min across four independent global searches, against the pump setting of 0.50 mL/min — an 8% deviation (Fig. 5c). The search bounds for Q spanned 10–5000 mL/min (Table S6) — a 500-fold range with no prior or penalty directing the optimizer toward the pump value. An incorrect model structure could have achieved comparable R² with Q = 2.0 or Q = 0.05 mL/min simply by compensating with A and α.

The fact that Q emerges from the BTC shape at 0.46 mL/min, entirely unforced, constitutes evidence that the model structure captures the actual transport physics. Q is not a fitting artifact — it is a recovered engineering parameter."

Additional: MRT_fit = 37.4 min vs. convective travel time x/v = 38.6 min → 3% deviation (internal consistency check, not independent verification).

- [ ] **Step 3: Verify Section 4.2**

Check:
- All parameter values match source Table 3 exactly
- Q = 0.46 ± 0.02, Q_pump = 0.50, deviation = 8%
- Search bounds [10, 5000] explicitly stated
- "Q unconstrained" stated at least twice
- Language is engineering register, not statistical
- Fig. 5 marker (BTC decomposition + Q bar chart)
- No claim that "this proves the model" — use "constitutes evidence"

- [ ] **Step 4: Commit Section 4.2**

```bash
git add "四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx"
git commit -m "feat: write Section 4.2 — Physical Self-Calibration (centerpiece)"
```

---

### Task 6: Write Sections 4.3–4.5 (~1000 words total)

**Files:**
- Modify: `四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx` — Sections 4.3, 4.4, 4.5
- Reference (read-only): Source material `ESP-T_Final_4-revised.docx` — TOA comparison, Pe discussion, σ sensitivity

**Interfaces:**
- Consumes: The self-calibration result (Section 4.2), K-P kinetics (Section 3.3), model definition (Section 2)
- Produces: Supporting evidence that reinforces but does not replace the Section 4.2 argument

- [ ] **Step 1: Write Section 4.3 — TOA Methods Comparison (~300 words)**

From design doc §4.3 and source ESP-T_Final_4-revised.docx lines 88-96.

Table:
| Method | Input | Q (mL/min) | Error |
|--------|-------|-----------|-------|
| Peak-time | t_peak = 15 min | 1.31 | +162% |
| Half-peak | t_half ≈ 5 min | 3.93 | +685% |
| First-moment | MRT = 37.1 min | 0.53 | +5.8% |
| This model | Full BTC | 0.46 | −8% |

Narrative: The first-moment method is reasonably accurate (+5.8%) but provides no signal decomposition, no mechanistic insight (Pe), and conflates the slug and tail into a single number. The coupled model uniquely combines accuracy with physical interpretability.

Fig. 6 marker.

- [ ] **Step 2: Write Section 4.4 — Independent Corroboration (~400 words)**

From design doc §4.4. This is the paper's second-strongest argument. CRITICAL FRAMING:

"Two completely independent experiments converge on the same physical picture:"

| Source | Experiment | Apparatus | Observable | Fitting Target | Key Result |
|--------|-----------|-----------|-----------|----------------|------------|
| Section 3.3 | Static batch release | Glass vial | Batch C(t) | K, n | n = 0.45–0.85 (non-Fickian) |
| Section 4.2 | Core displacement BTC | Core holder | BTC C(t) | Q, α, A, a, t₀, σ | Pe = 0.934 (non-piston) |

Explicitly note: different apparatus, different data, different fitting targets — not cross-validation on the same dataset. Both independently indicate non-Fickian/non-piston transport where convection and dispersion/relaxation contribute approximately equally.

Fig. 7 marker (dual panel: K-P fits left, Pe annotation on BTC right).

- [ ] **Step 3: Write Section 4.5 — Signal Decomposition Robustness (~300 words)**

From design doc §4.5 and source ESP-T_Final_4-revised.docx lines 98-103.

Present the σ sensitivity: erfc tail fraction across σ = 1.98–11.89 min (0.5×–3× fitted value). Result: 46.7–47.5% across the entire 6× range.

Key argument: "The decomposition is a model output, not a direct measurement. Its physical validity rests on (a) the self-calibration test (Section 4.2) establishing the model's physical correctness, and (b) the independent corroboration (Section 4.4). The σ insensitivity confirms it is not a parametric artifact — the erfc tail is a robust structural feature of the BTC."

Fig. 8 marker (σ sensitivity scan).

- [ ] **Step 4: Verify Sections 4.3–4.5**

Check:
- TOA errors correctly computed from source data
- "Independent experiments" framing explicit with apparatus/observable/fitting-target differentiation
- σ sensitivity range and erfc fraction range match source Table 5
- All figure markers correct
- Each subsection explicitly links back to the 4.2 self-calibration result

- [ ] **Step 5: Commit Sections 4.3–4.5**

```bash
git add "四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx"
git commit -m "feat: write Sections 4.3–4.5 — TOA, Independent Corroboration, Robustness"
```

---

### Task 7: Write Section 5 — Two-Phase Production Allocation (~800 words)

**Files:**
- Modify: `四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx` — Section 5
- Reference (read-only): Source material `ESP-T_Final_4-revised.docx` Section 3.4
- Reference (read-only): Source material `Supplementary_Material.docx` Table S5 (two-phase data)

**Interfaces:**
- Consumes: BTC framework (Section 2), self-calibration (Section 4.2), K-P kinetics (Section 3.3)
- Produces: Engineering extension showing the method works under realistic two-phase production conditions

- [ ] **Step 1: Write Section 5.1 — Physical Context (~100 words)**

"Under production conditions, shut-in occurs once during flowback. The majority of the monitoring period operates under steady multiphase flow. In this regime, the BTC is tail-dominated — the sustained release component (erfc) governs the observed concentration. Our two-phase core displacement experiments simulate this steady-state regime."

- [ ] **Step 2: Write Section 5.2 — Dilution Problem and Flux Solution (~300 words)**

From design doc §5.2.

- Present the dilution problem: C_oil decreases with increasing Q_total (Fig. 9a) — more fluid → less time for tracer accumulation per unit volume
- Define oil-phase tracer mass flux: F_O = C_oil × Q_oil
- Mass balance argument: at steady state, F_O equals the release rate from the ESP-T pack → independent of Q_total
- Show Fig. 9b: F_O vs Q_total is flat within each OWR (confirming mass balance)
- Note: F_O increases with OWR because more oil contacts the proppant surface (larger oil-wetted area → higher release rate)

- [ ] **Step 3: Write Section 5.3 — Flux-to-Production-Rate Calibration (~250 words)**

From design doc §5.3 and source data.

- Normalize by single-phase F_O,ref = 3.187 ± 0.15 μg/min (triplicate)
- Fig. 9c: F_O/F_O,ref vs Q_oil
- Pearson r = 0.97, p = 0.006, RMSD = 8.3% (from source text)
- Primary uncertainty: F_O,ref reproducibility (±4.7%)
- Note: calibration based on n = 3 OWR levels; larger matrix would strengthen

- [ ] **Step 4: Write Section 5.4 — Coupling to BTC Framework (~150 words)**

"K-P provides the temperature-dependent release rate K(T) and the transport mechanism indicator n(T). The erfc tail amplitude a, fitted from the BTC (Section 4.2), quantifies the sustained-release source strength. Combined with the K-P temperature calibration, the steady-state concentration (erfc tail plateau) yields the per-stage oil flow rate Q_oil. This closes the loop: static K-P → dynamic ADE → two-phase flux → per-stage oil production rate."

- [ ] **Step 5: Verify Section 5**

Check:
- All flux values from source Table S5
- F_O,ref = 3.187 ± 0.15 exact
- r = 0.97, RMSD = 8.3% match source
- "Closes the loop" narrative connects K-P → ADE → Flux → Q_oil
- Fig. 9 marker (3-panel)

- [ ] **Step 6: Commit Section 5**

```bash
git add "四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx"
git commit -m "feat: write Section 5 — Two-Phase Production Allocation"
```

---

### Task 8: Write Section 6 — Field Deployment Pathway (~400 words)

**Files:**
- Modify: `四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx` — Section 6
- Reference (read-only): Source material `ESP-T_Final_4-revised.docx` lines 113-114

**Interfaces:**
- Consumes: All prior sections
- Produces: Roadmap from laboratory validation to field implementation

- [ ] **Step 1: Write deployment steps (~200 words)**

From design doc §6:

1. Multi-element doping: each fracture stage receives ESP-T with a distinct metal/REE (Mn, Zn, Cu, Eu, Dy) → unique ICP-MS fingerprint per stage
2. Single shut-in after fracturing → accumulation slug forms in each stage
3. Flowback sampling: wellhead samples at intervals guided by Eq. 1 + wellbore geometry → expected pulse arrival time
4. Per-element BTC → dual-component fit → Q_i for each stage
5. Steady production phase: periodic sampling → flux method (Section 5) → per-stage Q_oil_i(t)
6. Production trend analysis: identify declining stages → optimize well spacing and completion design

Fig. 10 marker (schematic).

- [ ] **Step 2: Write limitations (~200 words)**

From design doc §6. State proactively:

- Single-interval lab scale; multi-interval field validation needed
- Dodecane model oil; crude oil (viscosity, composition) and transient flow conditions untested
- Epoxy chemical stability in aggressive environments (H₂S, CO₂, high-salinity brines, >120°C) not evaluated
- Three OWR levels (n = 3 independent points); larger OWR matrix would strengthen flux calibration
- Batch-specific F_O,ref determination recommended for field deployment

Do NOT hedge excessively — these are stated as scope boundaries, not weaknesses.

- [ ] **Step 3: Commit Section 6**

```bash
git add "四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx"
git commit -m "feat: write Section 6 — Field Deployment Pathway"
```

---

### Task 9: Write Section 7 — Conclusions (~300 words)

**Files:**
- Modify: `四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx` — Section 7

**Interfaces:**
- Consumes: All prior sections
- Produces: Self-contained conclusions paragraph

- [ ] **Step 1: Write conclusions (5 numbered points, ~300 words)**

From design doc §7. Each point must be a standalone finding:

1. "A coupled release–transport model was developed that decomposes a tracer-proppant BTC into a shut-in accumulation slug (Gaussian component, ADE instantaneous-pulse solution) and sustained matrix-diffusion-controlled release (erfc component, ADE semi-infinite boundary solution), linked by a C¹-continuous tanh transition."

2. "Physical self-calibration: the flow rate Q_fit = 0.46 mL/min converges to the independently set pump rate Q_pump = 0.50 mL/min (deviation 8%) with Q entirely unconstrained in the objective function (search bounds 10–5000 mL/min), confirming the model captures actual transport physics rather than merely fitting the curve."

3. "Independent corroboration: K-P batch kinetics (n = 0.45–0.85, non-Fickian transport) and ADE Peclet number (Pe = 0.934, non-piston displacement) converge on the same physical picture from completely separate experiments — different apparatus, different data, different fitting targets."

4. "Two-phase extension: the oil-phase tracer mass flux F_O eliminates the dilution artifact inherent in concentration-based interpretation and tracks the oil production rate Q_oil across OWR 4:1 to 1:4 (Pearson r = 0.97, RMSD = 8.3%)."

5. "The framework enables per-stage production allocation from wellhead samples alone, requiring no downhole tools and only a single shut-in. Multi-stage field validation with crude oil under transient conditions remains the next step."

- [ ] **Step 2: Commit Section 7**

```bash
git add "四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx"
git commit -m "feat: write Section 7 — Conclusions"
```

---

### Task 10: Write Introduction (Section 1) and Abstract (~1500 words total)

**Files:**
- Modify: `四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx` — Section 1 and Abstract

**Interfaces:**
- Consumes: All sections (1 is written last because it previews the complete paper). Abstract written after Introduction.
- Produces: Introduction that sets up the engineering problem, exposes the gap, and previews our solution and validation strategy.

- [ ] **Step 1: Write Introduction Paragraph 1 — Engineering Need (~250 words)**

From design doc §1:

"Multi-stage fractured horizontal wells: per-stage contribution is the critical unknown for completion optimization and well spacing. Existing downhole tools — production logging (intervention, snapshot only), distributed fiber-optic sensing (permanent cable, high cost), microseismic (geometry, not production) — each have trade-offs. Tracer proppants avoid downhole hardware: injected with the proppant pack, permanently placed in the fracture, surface-sampled at the wellhead, enabling long-term monitoring."

Cite: King (2010), Cipolla & Wallace (2014), Hill & Zhu (2021), Molenaar (2012), Jin & Roy (2017), Maxwell (2011).

- [ ] **Step 2: Write Introduction Paragraph 2 — The Core Difficulty (~250 words)**

"BTC encodes both release kinetics and transport parameters. Current practice: K-P for release characterization (batch), ADE for transport interpretation (known source). Applied SEPARATELY. Consequence: can confirm which stages produce but cannot QUANTIFY how much. This is an unsolved inverse problem: two unknown functions (release rate, transport response) from one observable (C(t) at the wellhead)."

Cite: Korsmeyer (1983), Ritger & Peppas (1987), van Genuchten & Alves (1982), Shook (2009).

- [ ] **Step 3: Write Introduction Paragraph 3 — Prior Work and Its Ceiling (~350 words)**

Two streams of prior work:

Stream A — Tracer proppant materials: Zhao (2020) ceramic/dye, Zhou (2022) CQDs/ceramic, Li (2023) rare earth/polymer, Gong (2024) Fe₃O₄/PS. All evaluate via batch K-P. None couple release to transport.

Stream B — ADE for tracer interpretation: Fontalvo (2025) interwell PITT, Velasco-Lozano (2024) two-phase ADE, Mazo (2024) multi-stage tracer model. All assume KNOWN source term (injection pulse of specified mass and duration).

GAP: No existing framework couples the sustained, unknown release source term to the transport solution. TOA methods (peak-time, half-peak) are inadequate for sustained-release BTCs (errors +162% to +685%, preview of Section 4.3).

- [ ] **Step 4: Write Introduction Paragraph 4 — This Work (~350 words)**

From design doc §1:

"We propose a coupled release–transport model: Gaussian (shut-in accumulation slug) + erfc (sustained matrix-diffusion-controlled release), smooth tanh transition. Six free parameters, estimated simultaneously from a single BTC."

"The validation strategy is predictive, not descriptive: Q is left unconstrained in the objective function; the model must recover the correct flow rate from the BTC shape alone. ESP-T (oleophilic epoxy/Fe₃O₄ tracer proppant) serves as the experimental vehicle."

Preview the key results: Q_fit vs Q_pump ±8%, Pe vs K-P n independent corroboration, two-phase flux calibration r = 0.97.

State scope: single-phase core flood → two-phase production allocation → field deployment pathway.

- [ ] **Step 5: Write Abstract (~250 words)**

From design doc §Abstract. Paint-by-numbers:

Sentence 1: Problem — "Interpreting tracer-proppant wellhead breakthrough curves for per-stage production allocation requires jointly accounting for sustained release from the polymer matrix and transport through the production tubing — a coupled inverse problem not addressed by current practice."

Sentence 2: Gap — "Existing approaches apply the Korsmeyer-Peppas model for batch release characterization and the advection-dispersion framework for transport interpretation separately; the sustained source term inherent to tracer proppants has not been coupled to the transport solution."

Sentence 3: Our approach — "We develop a coupled release–transport model that decomposes the BTC into a Gaussian pulse (shut-in accumulation slug) and an erfc tail (sustained matrix-diffusion-controlled release), linked by a smooth hyperbolic-tangent transition. Six parameters are estimated simultaneously from a single BTC; the flow rate Q receives no constraint in the objective function."

Sentence 4: Decisive result — "Applied to an oleophilic epoxy/Fe₃O₄ tracer proppant (ESP-T) in core displacement experiments, the model yields Q_fit = 0.46 mL/min against the independent pump setting of 0.50 mL/min (deviation 8%), with Q bounded to [10, 5000] mL/min and no prior directing it toward the correct value."

Sentence 5: Supporting results — "The Peclet number (Pe = 0.934) independently corroborates the non-Fickian transport mechanism identified via K-P kinetics (n = 0.45–0.85). Under two-phase flow, the oil-phase tracer mass flux eliminates water-dilution artifacts and tracks oil production rates (Pearson r = 0.97, RMSD = 8.3%)."

Sentence 6: Significance — "The framework enables per-interval production allocation from wellhead samples alone, requiring no downhole tools and only a single shut-in."

- [ ] **Step 6: Verify Introduction and Abstract**

Check:
- Introduction sets up the gap: release + transport treated separately → cannot quantify
- Prior work correctly cited and accurately described
- "This work" paragraph previews the self-calibration validation strategy, not just "we did X"
- Abstract hits all beats: problem → gap → approach → decisive result → supporting → significance
- Abstract word count ≤ 250
- No citations in Abstract (journal convention)

- [ ] **Step 7: Commit Section 1 and Abstract**

```bash
git add "四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx"
git commit -m "feat: write Section 1 (Introduction) and Abstract"
```

---

### Task 11: Compile References and Cross-Check Citations

**Files:**
- Modify: `四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx` — References section
- Reference (read-only): Source material `ESP-T_Final_4-revised.docx` references [1]–[41]
- Reference (read-only): Source material `环氧+四氧化三铁改4.10.docx` references [1]–[29]
- Reference (read-only): Design doc writing principles §5

**Interfaces:**
- Consumes: All sections with in-text citations
- Produces: Complete, verified, correctly-ordered reference list

- [ ] **Step 1: Extract all in-text citations from the manuscript**

Read through every section and collect all [N] citations. Build a master citation list.

- [ ] **Step 2: Merge and deduplicate references from both source materials**

Key references (from English manuscript, more complete):
[1] IEA 2024, [2] BP 2024, [3] Wang 2017 (Fuel), [4] Montgomery 2005 (AAPG), [5] King 2010 (SPE 133456), [6] Cipolla 2014 (SPE 168596), [7] Xu 2025 (Sci Rep), [8] Yue 2024 (Pet Sci), [9] Hill & Zhu 2021, [10] Molenaar 2012 (SPE DC), [11] Jin & Roy 2017 (Leading Edge), [12] Maxwell 2011 (Leading Edge), [13] Patidar 2022 (JPEPT), [14] Sanni 2018 (JPSE), [15] Watkins 1954 (JPT), [16] Fontalvo 2025 (TIPM), [17] Tian 2020 (SPE 201292), [18] Yang 2024 (JPEPT), [19] Arshad 2024 (IPTC 23916), [20] Al Raisi 2023 (SPE 214827), [21] Zhao 2020 (JPSE), [22] Zhou 2022 (JPSE), [23] Li 2023 (Geoenergy Sci Eng), [24] Gong 2024 (Fuel), [25] Filev 2022 (IPTC 21357), [26] Ren 2024 (Geoenergy Sci Eng), [27] Malyavko 2023 (SPE 215624), [28] Korsmeyer 1983 (Int J Pharm), [29] Ritger & Peppas 1987 (J Control Release), [30] Peppas & Sahlin 1989 (Int J Pharm), [31] van Genuchten & Alves 1982 (USDA TB 1661), [32] Shook 2009 (SPE 124614), [33] Velasco-Lozano 2024 (SPE J), [34] Mazo 2024 (Fluid Dyn), [35] Liang 2016 (Petroleum), [36] Zoveidavianpoor 2018 (JPSE), [37] Wang 2024 (ACS Omega), [38] Krishnan 2025 (Geoenergy Sci Eng), [39] Li H 2021 (ACS Omega), [40] Wei 2024 (Int J Oil Gas Coal Technol), [41] Wang C 2024 (Geoenergy Sci Eng)

Additional from Chinese manuscript if needed: [Chong 2016], [Rogner 1997], [Mohr 2015], [Barati 2014], [Medeiros 2010], [Silva 2019], [Guo X 2024], [Liang C 2016], [Sabins 2021], [Gong Z 2024 (Colloids Surf A)], [Krumbein 1951]

- [ ] **Step 3: Format all references per Geoenergy Science and Engineering style**

Numbered list, format: Author(s). Title. Journal Name, Year, Volume(Issue): Pages. DOI if available.

- [ ] **Step 4: Verify every in-text citation has a corresponding reference entry**

Scan manuscript: for each [N], confirm reference N exists and matches. Reverse scan: confirm no orphan references.

- [ ] **Step 5: Commit references**

```bash
git add "四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx"
git commit -m "feat: compile and format all references for Geoenergy Science and Engineering"
```

---

### Task 12: Final Polish — Title, Keywords, Cross-References, and Global Consistency

**Files:**
- Modify: `四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx` — Title, Keywords, global edits
- Reference (read-only): Design doc §3 (title candidates), §5 (writing principles)

**Interfaces:**
- Consumes: Complete manuscript (Sections 1–7, Abstract, References)
- Produces: Submission-ready manuscript

- [ ] **Step 1: Finalize title**

From design doc candidates:
- Option A: "Flow-Rate Self-Calibration from Tracer-Proppant Breakthrough Curves: A Coupled Release–Transport Model for Per-Stage Production Allocation"
- Option B: "Self-Calibrating BTC Inversion: Joint Estimation of Release and Transport Parameters for Tracer-Proppant-Based Production Allocation"

Evaluate against the final manuscript content. Select the one that best captures the self-calibration core argument. Refine as needed.

- [ ] **Step 2: Write Keywords**

6–8 keywords covering: tracer proppant, breakthrough curve, advection-dispersion equation, production allocation, release kinetics, self-calibration, two-phase flow, epoxy resin.

- [ ] **Step 3: Global consistency check**

Walk through the entire manuscript:

1. Symbol consistency: Q, α, Pe, A, a, c_b, t₀, σ, v, MRT — same symbol used throughout, defined at first use (Section 2)
2. Figure references: Fig. 1 through Fig. 10 all cited in text, captions written
3. Table references: All tables cited in text
4. Supplementary references: Table S1–S6, Fig. S1–S3 all correctly cross-referenced
5. Section cross-references: All "Section X.Y" pointers resolve to actual sections
6. Numerical consistency: Q_fit = 0.46, Q_pump = 0.50, 8%, Pe = 0.934, n = 0.45–0.85, r = 0.97, RMSD = 8.3%, 47% erfc, 53% Gaussian — all match source data
7. Units: mL/min, cm, min, °C, g/cm³, μg/mL, μg/min — consistent throughout
8. No material-innovation language anywhere
9. "Q unconstrained" stated in Abstract, Introduction, Section 2.4, Section 4.2, and Conclusions

- [ ] **Step 4: Run a read-through for narrative coherence**

Read the manuscript linearly. Check:
- Introduction sets up the gap that the model fills
- Section 2 defines the model and the self-calibration validation strategy
- Section 3 provides exactly the experimental details needed, no more
- Section 4.1 → 4.2: "AICc says single-process is insufficient; now here's the decisive positive test"
- Sections 4.3–4.5 reinforce 4.2, do not replace it
- Section 5 extends to engineering reality
- Section 6 provides actionable pathway
- Section 7 closes with the 5 key findings

- [ ] **Step 5: Commit final manuscript**

```bash
git add "四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_v2_manuscript.docx"
git commit -m "feat: finalize manuscript — title, keywords, global consistency"
```

---

### Task 13: Write Updated Supplementary Material

**Files:**
- Create: `四氧化三铁环氧树脂拟合/ESP-T_投稿文件/Supplementary_Material_v2.docx`
- Reference (read-only): Source material `Supplementary_Material.docx` — sections S1–S5
- Reference (read-only): Design doc §4 (Figure Plan) for Fig. S1–S3 placement

**Interfaces:**
- Consumes: Complete main manuscript (for cross-reference accuracy)
- Produces: Standalone supplementary document matching the new paper's structure

- [ ] **Step 1: Map old → new supplementary structure**

Old SM sections → New SM sections:
- S1 Reagent Specifications → Keep as S1 (update any cross-refs)
- S2 Detailed Characterization Methods → Keep as S2 (update cross-refs)
- S3 Supplementary Characterization Data → Keep as S3 (update figure numbers)
- S4 Raw Experimental Data → Keep as S4 (update table numbers)
- S5 Piecewise ADE Model → Keep as S5, add optimization protocol detail (old S5.3)

- [ ] **Step 2: Add optimization implementation detail to S5**

Move the numerical algorithm details excluded from Section 3.5 into S5.3:
- DE: population = 50, max generations = 2000, CR = 0.9, mutation adaptive [0.5, 1.5], rand/1/bin, Polish = True, 4 seeds (42, 123, 456, 789)
- L-BFGS-B: max iterations = 20,000, ftol = 1e-16, gtol = 1e-16
- SciPy 1.11, Python 3.11, single-core, ~15–30 s per seed
- Parameter bounds Table S6 (already exists)

- [ ] **Step 3: Update all cross-references**

Ensure all "Section X.Y of the main text" references match the new paper's section numbering.

- [ ] **Step 4: Commit Supplementary Material**

```bash
git add "四氧化三铁环氧树脂拟合/ESP-T_投稿文件/Supplementary_Material_v2.docx"
git commit -m "feat: create updated Supplementary Material matching v2 manuscript"
```

---

## Self-Review

### 1. Spec Coverage
- Core proposition (self-calibration) → Task 5 (Section 4.2), Task 2 (Section 2.4)
- 5-step logical cascade → Tasks 2-8 cover each step
- Paper structure (7 sections) → Tasks 2-10
- Figure plan (10 figures) → Task 1 places markers, captions written in respective tasks
- Writing principles (7 rules) → Verified in Task 12 Step 3
- Title → Task 12 Step 1
- Abstract → Task 10 Step 5
- References → Task 11
- Supplementary Material → Task 13

### 2. Placeholder Scan
- No TBD, TODO, or incomplete markers
- All parameter values are extracted from source materials (verified against ESP-T_Final_4-revised.docx)
- All cross-references have explicit targets

### 3. Type Consistency
- Q, α, Pe, A, a, c_b, t₀, σ defined in Task 2 (Section 2.3), used consistently in Tasks 5-9
- "Q unconstrained" language repeated in Tasks 2, 5, 9, 10
- F_O, F_O,ref defined in Task 7, consistent with Task 5 references
- All figure numbers (Fig. 1-10) consistent across all tasks

### 4. Task Completeness
- Each task produces independently verifiable content
- Each task commits separately for granular history
- Tasks are ordered by dependency: skeleton → model → methods → results → extensions → introduction → references → polish
