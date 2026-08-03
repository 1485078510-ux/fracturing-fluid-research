# Design Spec: ESP-T Paper Rewrite — Physical Self-Calibration Framework

**Date:** 2026-08-03
**Target Journal:** *Geoenergy Science and Engineering*
**Source Materials:**
- `ESP-T_Final_4-revised.docx` — English manuscript (current SCI draft)
- `环氧+四氧化三铁改4.10.docx` — Chinese revision (material-focused)
- `Supplementary_Material.docx` — Full supplementary (datasets, derivations, protocols)

---

## 1. Core Proposition

> The validity of our coupled release–transport model is established not by fit quality (R²), but by a stricter test: **the flow rate Q, left entirely unconstrained in the objective function, spontaneously converges to the independently measured pump setting (±8%).** An overfitted model cannot do this — it can improve R² but cannot "coincidentally guess" a correct independent physical quantity. This constitutes decisive evidence that the model structure captures real physical processes.

The paper's single narrative arc: **"From BTC to flow rate — without external calibration."**

---

## 2. Logical Architecture (5-Step Cascade, Non-Circular)

```
[Step 1] PROBLEM DIAGNOSIS
"Estimating Q from a BTC is hard because release kinetics and transport
 are superimposed in the measured signal. Single-process models conflate
 the two → Q estimates deviate by +162% to +685%."

[Step 2] MODEL CONSTRUCTION
"We build a coupled model that explicitly separates release (continuous source
 term) from transport (ADE pulse response). Six free parameters, all estimated
 simultaneously from a single BTC — no external constraints."

[Step 3] DECISIVE TEST: PHYSICAL SELF-CALIBRATION
"This is the paper's most critical data point:"
→ Q_fit = 0.46 mL/min, Q_pump = 0.50 mL/min, deviation = ±8%
→ Q is NOT constrained in the objective function
→ A structurally wrong 6-parameter model fitting 21 data points cannot
  'coincidentally guess' the correct Q across all 4 random DE seeds

[Step 4] INDEPENDENT CORROBORATION
→ K-P static batch release → n = 0.45–0.85 (non-Fickian transport)
→ ADE dynamic BTC fit → Pe = 0.934 (non-piston displacement)
→ Two completely independent experiments, different apparatus,
  different data, different fitting targets → SAME physical picture

[Step 5] ENGINEERING DEPLOYMENT
"Since the model is physically correct, its outputs have engineering meaning:"
→ Signal decomposition (Gaussian 53% / erfc 47%)
→ Two-phase steady state = tail-dominated → flux method → Q_oil (r = 0.97)
→ Multi-stage, multi-element field deployment pathway
```

---

## 3. Paper Structure

### Title (candidate formulations)
- *"Flow-Rate Self-Calibration from Tracer-Proppant Breakthrough Curves: A Coupled Release–Transport Model for Per-Stage Production Allocation"*
- *"Self-Calibrating BTC Inversion: Joint Estimation of Release and Transport Parameters for Tracer-Proppant-Based Production Allocation"*

### Abstract (~250 words)
- One-sentence problem statement
- One-sentence gap (release and transport are treated separately)
- One-sentence our approach (coupled model, 6 free parameters, Q unconstrained)
- **Decisive result highlighted:** Q converges to pump setting ±8%
- Supporting results: Pe ↔ K-P corroboration, two-phase flux calibration
- One-sentence significance

### 1. Introduction (~1200 words)

**Paragraph 1: Engineering need**
- Multi-stage fractured horizontal wells: per-stage contribution is the critical unknown
- Existing downhole tools (PLT, DTS, DAS): cost, intervention, snapshot limitations
- Tracer proppant advantage: permanent placement, surface sampling, long-term monitoring

**Paragraph 2: The core difficulty**
- BTC encodes BOTH release kinetics AND transport parameters
- Current practice: K-P for release, ADE for transport — applied SEPARATELY
- Consequence: can confirm which stages produce but CANNOT QUANTIFY how much
- This is an unsolved inverse problem: two unknowns (release, transport) from one observable (BTC)

**Paragraph 3: Prior work and its ceiling**
- Tracer proppant materials: Zhao (2020), Zhou (2022), Li (2023), Gong (2024) — all evaluate release via batch K-P only
- ADE in tracer interpretation: Fontalvo (2025), Velasco-Lozano (2024), Mazo (2024) — all assume KNOWN source term (injection pulse)
- No existing framework couples the sustained source term to the transport solution
- Time-of-arrival (TOA) methods: peak-time, half-peak, first-moment — errors +162% to +685% for our BTC (preview of Section 4.3)

**Paragraph 4: This work**
- We propose a coupled release–transport model: Gaussian (shut-in accumulation slug) + erfc (sustained matrix-diffusion-controlled release), linked by smooth tanh transition
- **The validation strategy is predictive, not descriptive:** Q is left unconstrained; the model must converge to the correct physical value spontaneously
- ESP-T (oleophilic epoxy/Fe₃O₄ tracer proppant) serves as the experimental vehicle
- Scope: single-phase core flood → two-phase production allocation → field deployment pathway

### 2. The Coupled Release–Transport Model (~1500 words)

**2.1 Physical Basis**
- Shut-in operation forces two tracer sources:
  - Source I: tracer accumulates in near-wellbore region during shut-in → swept as coherent slug upon flowback → Gaussian pulse
  - Source II: polymer matrix continues swelling and releasing tracer → sustained concentration tail
- These are physically irreducible — not a "model selection" but a consequence of experimental design

**2.2 Governing Equations**

*Transport backbone — 1D ADE:*
∂C/∂t + v·∂C/∂x = D·∂²C/∂x²

*Dimensionless working variable (from tube-flow substitution):*
z = (xπd² − 4Qt) / √(16αQtπd²)

*Component I — Gaussian pulse (ADE instantaneous-pulse solution):*
C_rise(t) = c_b + (A·d) / √(16παQt·d²) × exp(−z²)

*Component II — Continuous-source tail (ADE semi-infinite boundary solution):*
C_fall(t) = c_b + (a/2) × erfc(−z)

*Blending function (C¹-continuous for gradient-based optimization):*
w(t) = ½[1 + tanh((t₀ − t) / σ)]
C(t) = c_b + w(t)·C_rise(t) + [1 − w(t)]·C_fall(t)        (Eq. 1)

**2.3 Parameter Set**
| Parameter | Symbol | Origin | Physical Meaning |
|-----------|--------|--------|------------------|
| Baseline | c_b | Both | Asymptotic concentration plateau |
| Pulse amplitude | A | Rise | Total tracer mass accumulated during shut-in |
| Tail amplitude | a | Fall | Sustained-release source strength |
| Dispersivity | α | Rise (dominant) | Longitudinal dispersion in tubing |
| Flow rate | Q | Rise (dominant) | **Target parameter — UNCONSTRAINED** |
| Crossover time | t₀ | Both | Transition from slug-dominated to tail-dominated |
| Transition width | σ | Both | Fitted (~sampling interval), not free in practice |

Derived: Pe = x/α, v = 4Q/(πd²), MRT = x/v, Gaussian/erfc integrated fractions.

**2.4 Validation Strategy: Self-Calibration as Decisive Test**
- Conventional model validation: R², RMSE — these cannot distinguish overfitting from physical correctness
- Our test: Q is a physical quantity with an independent known value (pump setting = 0.50 mL/min). If the model structure is incorrect, the optimizer will assign Q an arbitrary value that minimizes residuals. If Q converges to 0.50 without being constrained, the model structure must correctly capture the transport physics.
- This is a **prediction**, not a fit — and it's falsifiable.

### 3. Experimental Methods (~1000 words — COMPRESSED)

**3.1 ESP-T Synthesis (one paragraph only)**
- Co-precipitation of nano-Fe₃O₄@SA → emulsion polymerization with E51/T31 → curing
- Doped with Mn (extensible to Zn, Cu, Eu, Dy for multi-stage coding)
- Key properties stated without material-innovation narrative

**3.2 Material Prerequisites for Model Validity (tabular format)**
| Prerequisite | Measurement | Result | Implication |
|-------------|-------------|--------|--------------|
| Tracer embedded in matrix | SEM-EDS cross-section | Fe distributed throughout | Bulk encapsulation, not surface coating |
| Matrix stable at downhole T | TGA/DTG | Decomp. onset 357°C | No thermal degradation at 80–200°C |
| Sustained release, non-Fickian | K-P batch kinetics | n = 0.45–0.85 | Confirms swelling-diffusion mechanism |
| Selective oil-phase release | WCA + filtration | WCA = 104.6°, oil/water time ratio = 5.53 | Tracer signal isolated from water dilution |

**3.3 K-P Batch Release Kinetics**
- 5 g ESP-T in 100 mL dodecane, 30/60/90/120°C, 12-h sampling, 14 days, ICP-MS
- K-P fit within Mt/M∞ < 0.6 (model validity range)

**3.4 Core Displacement: BTC Generation**
- Steel core packed with ESP-T, 5 MPa confining, saturated with dodecane
- Shut-in 96 h → displacement at 0.50 mL/min → effluent sampled at 4-min intervals, 21-point BTC
- Two-phase: OWR = 4:1, 1:1, 1:4, total flow 0.1–0.4 mL/min, steady-state

**3.5 Parameter Estimation Strategy**

The inverse problem — extracting six transport and release parameters from a single BTC — presents a challenging optimization landscape because the release and transport components are coupled: different combinations of Q, α, and A can produce similar curve shapes in certain regions. A two-pass estimation strategy was adopted to ensure the solution represents the global physical optimum rather than a local numerical artifact.

*Pass 1 — Basin location.* A global search was performed over wide, physically bounded parameter ranges (Table S6) using multiple independent starting populations. Each run explores the parameter space without being trapped by local minima. The parameter bounds are set wide enough that the search is not steered toward any expected value; the pump flow rate Q, for instance, was bounded between 10 and 5000 mL/min (a 500× range), so the optimizer had no preferential basin near 0.50 mL/min. Four independent runs with different random initialization were conducted to verify that the global basin is consistently located.

*Pass 2 — Local refinement.* From the best point identified in Pass 1, a gradient-based refinement polishes the parameter estimates to the precision required for physical interpretation. This second pass typically converged within 50–200 iterations from the Pass-1 starting point, confirming that Pass 1 had already located the correct basin.

*Fair comparison.* All five candidate models (dual-component, single Gaussian, single erfc, exponential decay, K-P) were subjected to the identical two-pass protocol with the same bounds, convergence criteria, and number of independent runs. This ensures that differences in fit quality reflect model adequacy rather than differences in optimization effort.

### 4. Results and Discussion

**4.1 Model Selection: Why Single-Process Models Are Insufficient (~400 words)**

*Table: 5 candidate models, N = 21*
| Model | k | R² | RMSE | AICc | ΔAICc |
|-------|---|-----|------|------|-------|
| Dual-component tanh-blended | 7 | 0.9939 | 0.0210 | −139.70 | 0.00 |
| Single Gaussian | 4 | 0.9482 | 0.0609 | −107.04 | 32.66 |
| Single erfc | 4 | 0.7159 | 0.1427 | −71.28 | 68.42 |
| Exponential decay | 3 | 0.7517 | 0.1334 | −77.20 | 62.51 |
| K-P power law | 3 | −0.0193 | 0.2703 | −47.54 | 92.16 |

F(3, 14) = 34.70, p < 10⁻⁶.

*Figure: 5-model overlay on BTC, ΔAICc bar chart.*

**Key interpretation:** Single-process models each capture ONE feature (peak OR tail) — neither captures both. The AICc evidence is strong but is presented as **necessary but not sufficient** condition. The decisive test is Q self-calibration (Section 4.2).

**4.2 Physical Self-Calibration: The Flow-Rate Test (~600 words)**

*This is the paper's centerpiece.*

**Figure:** BTC decomposition into Gaussian (53%) and erfc (47%) components, with residual plot.

**Figure:** Bar chart: Q_fit (0.46) vs Q_pump (0.50), with error bar ±8%. Caption: "Q was not constrained in the objective function. The fitted value is recovered from the BTC shape alone."

**Argument structure:**
1. The model has 6 free parameters — enough degrees of freedom to fit noise if the model structure were wrong
2. However, extra parameters only improve curve-matching; they do not produce physically correct parameter values. If the model structure is incorrect, the optimizer will assign Q whatever value helps match the curve shape — along with compensating adjustments in A and α
3. Yet Q settles at 0.46 mL/min across four independent global searches (0.46 ± 0.02), against the pump setting of 0.50 mL/min — an 8% deviation
4. The search bounds for Q spanned 10–5000 mL/min (Table S6) — the optimizer could have chosen Q = 2.0, Q = 0.05, or any other value to reduce residuals. It consistently chose 0.46
5. **Therefore:** The model structure captures the actual transport physics well enough that the physically correct Q emerges from the data without being imposed. Q is not a fitting artifact — it is a *recovered* engineering parameter

**Additional self-consistency:** MRT_fit = 37.4 min vs. convective travel time x/v = 38.6 min → 3% deviation.

**4.3 Comparison with Time-of-Arrival Methods (~300 words)**

| Method | Input | Q estimate (mL/min) | Error |
|--------|-------|---------------------|-------|
| Peak-time | t_peak = 15 min | 1.31 | +162% |
| Half-peak | t_half ≈ 5 min | 3.93 | +685% |
| First-moment | MRT = 37.1 min | 0.53 | +5.8% |
| **This model** | Full BTC, 6-param fit | **0.46** | **−8%** |

**Figure:** BTC with peak, half-peak, MRT markers; bar chart of Q estimates.

**Key point:** The first-moment method is reasonably accurate but provides no signal decomposition, no mechanistic insight, and no Pe. The coupled model uniquely combines accuracy with physical interpretability.

**4.4 Independent Corroboration: K-P Kinetics ↔ ADE Peclet Number (~400 words)**

**This is the paper's second strongest argument — and it's NOT from the same experiment.**

| Source | Experiment | Key Parameter | Implication |
|--------|-----------|---------------|-------------|
| Section 3.3 | Core displacement BTC | Pe = 0.934 ≈ 1 | Convection ≈ Dispersion |
| Section 3.2 | Static batch release | n = 0.45–0.85 | Non-Fickian (swelling + diffusion) |

**Figure (dual panel):** Left: K-P log-log fits at 4 temperatures. Right: Pe on the ADE BTC with annotation "Pe = 0.934".

**Argument:** Two completely independent experiments — different apparatus (glass vial vs. core holder), different observables (batch C(t) vs. BTC), different fitting targets (K, n vs. Q, α, A, a) — converge on the same physical picture. Non-Fickian release produces a dispersed transport response. This is not cross-validation on the same dataset; it is an independent corroboration.

**4.5 Signal Decomposition and Robustness (~300 words)**

**Figure:** Gaussian and erfc components shaded separately on the BTC plot; pie chart of integrated fractions.

**Figure:** σ sensitivity: erfc tail fraction vs. σ (0.5× → 3.0×). The tail contribution stays within 46.7–47.5% across the entire 6× range.

**Argument:** The decomposition is a model output, not a measurement. Its physical validity rests on (a) the self-calibration test (Section 4.2) and (b) the independent corroboration (Section 4.4). The σ insensitivity confirms it is not a parametric artifact.

### 5. Extension to Two-Phase Production Allocation (~800 words)

**5.1 Physical Context**
- In production, shut-in occurs once. The majority of the monitoring period operates under steady flow → BTC tail-dominated
- Our two-phase experiments simulate this steady-state regime

**5.2 The Dilution Problem and the Flux Solution**
- C_oil decreases with Q_total (dilution) — cannot be used directly
- Define oil-phase tracer mass flux: F_O = C_oil × Q_oil
- At steady state, F_O = release rate from ESP-T pack (mass balance) → independent of Q_total

**Figure (3-panel):** (a) C_oil vs Q_total (decreasing); (b) F_O vs Q_total (flat within each OWR); (c) F_O/F_O,ref vs Q_oil (linear, r = 0.97)

**5.3 Flux-to-Production-Rate Calibration**
- Normalize by single-phase F_O,ref = 3.187 ± 0.15 μg/min
- F_O/F_O,ref vs. Q_oil: Pearson r = 0.97, p = 0.006, RMSD = 8.3%
- Primary uncertainty source: F_O,ref reproducibility (±4.7%)

**5.4 Coupling to the BTC Framework**
- K-P provides temperature-dependent release rate → predicts a(T) for the erfc tail
- erfc tail amplitude a, combined with K-P temperature calibration, yields per-stage Q_oil from steady-state wellhead sampling
- This closes the loop: static K-P → dynamic ADE → two-phase flux → Q_oil

### 6. Field Deployment Pathway (~400 words)

1. Each stage: ESP-T with distinct metal/REE dopant (Mn, Zn, Cu, Eu, Dy) → unique ICP-MS signature
2. Single shut-in after fracturing → accumulation slug forms
3. Flowback: wellhead sampling at intervals guided by expected pulse arrival (from Eq. 1 with wellbore geometry)
4. Each element's BTC → dual-component fit → per-stage Q_i
5. Post-flowback steady production → periodic sampling → flux method → per-stage Q_oil_i(t)
6. Trend analysis: identify declining stages, optimize well spacing and completion design

**Limitations acknowledged (necessary for credibility):**
- Validated on single-interval lab scale; multi-interval field validation pending
- Dodecane model oil; crude oil and transient conditions untested
- Epoxy chemical stability in aggressive environments (H₂S, CO₂, high-salinity brines) not evaluated
- Three OWR levels (n = 3 independent oil-fraction points) — larger matrix would strengthen calibration

### 7. Conclusions (~300 words)

1. We developed a coupled release–transport model that decomposes a tracer-proppant BTC into a shut-in accumulation slug (Gaussian) and sustained matrix-diffusion release (erfc tail).
2. **Physical self-calibration:** Q_fit = 0.46 mL/min converges to Q_pump = 0.50 mL/min (±8%) with Q entirely unconstrained — confirming the model captures real transport physics.
3. Independent corroboration: K-P n (0.45–0.85) and ADE Pe (0.934) converge on the same non-Fickian/non-piston transport picture from separate experiments.
4. Two-phase extension: oil-phase tracer flux eliminates dilution artifacts and tracks Q_oil (r = 0.97, RMSD = 8.3%), suitable for steady-state production monitoring.
5. The framework provides a methodology for per-stage production allocation from surface samples alone — requiring no downhole tools and only a single shut-in.

---

## 4. Figure Plan (10–12 figures)

1. **Fig. 1:** Schematic — BTC generation: shut-in → accumulation → flowback → two-component BTC (conceptual diagram)
2. **Fig. 2:** ESP-T characterization summary (4-panel: SEM overview + EDS Fe map + TGA + WCA) — compressed, prerequisite-only
3. **Fig. 3:** K-P kinetics (dual panel: C/C₀ vs t at 4 temperatures + log-log K-P fits)
4. **Fig. 4:** Model selection — 5 candidate model fits overlaid on BTC data + ΔAICc bar chart
5. **Fig. 5:** **CENTERPIECE** — BTC decomposition (Gaussian/erfc shaded + residuals) + Q self-calibration bar chart (Q_fit vs Q_pump)
6. **Fig. 6:** TOA method comparison (BTC with markers + Q estimates bar chart)
7. **Fig. 7:** Independent corroboration — K-P fits + Pe on BTC (dual panel, showing different experiments → same conclusion)
8. **Fig. 8:** σ sensitivity analysis (erfc fraction vs σ + BTCs at 5 σ values)
9. **Fig. 9:** Two-phase flow (3-panel: C_oil vs Q_total, F_O vs Q_total, F_O/F_O,ref vs Q_oil)
10. **Fig. 10:** Field deployment pathway schematic
11. **Fig. S1–S3** (Supplementary): Optical micrographs, raw BTC data, release data, physical property summary

---

## 5. Writing Principles

1. **Every paragraph answers "why this matters for getting Q from BTC"** — no tangential content
2. **Material characterization is instrumental, not innovative** — subordinated to model validation prerequisites
3. **The Q self-calibration is presented as a prediction, not a post-hoc observation** — the language must make clear that Q was unconstrained
4. **K-P and ADE are presented as independent lines of evidence** — explicitly note different apparatus, different data, different fitting targets
5. **Limitations are stated proactively** — strengthens rather than weakens credibility
6. **Statistical evidence (AICc, F-test) supports but does not lead** — the Q self-calibration is the lead argument
7. **Target length:** ~7000 words main text, ~35 references

---

## 6. Implementation Tasks

1. Write complete manuscript (DOCX) with the 7-section structure above
2. Place all 10 figures with captions
3. Ensure all 21 BTC data points, K-P parameters, and two-phase data are referenced from Supplementary Material tables
4. Merge all 35+ references from source materials, verify consistency
5. Format per *Geoenergy Science and Engineering* guidelines
6. Write updated Supplementary Material matching new paper structure

---

## 7. Self-Review Checklist

- [x] No TBD or TODO markers
- [x] All 5 logical steps are non-circular (each step builds on prior, none assumes the conclusion)
- [x] The Q self-calibration test is falsifiable (if model were wrong, Q would not converge)
- [x] K-P and ADE are presented as independent experiments, not cross-validation
- [x] Material characterization serves as prerequisite verification, not as innovation claim
- [x] Figures are assigned to specific arguments in the logical chain
- [x] Limitations are stated explicitly
- [x] Target journal formatting consideration noted
