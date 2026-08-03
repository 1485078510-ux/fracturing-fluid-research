# Paper Extraction Templates — Complete Reference

## Template: Original Research (Full)

```yaml
study_id: "Author (Year)"
doi: "10.xxxx/yyyy"
paper_type: "original_research"

# Bibliographic
title: ""
authors:
  - name: "First Author"
    affiliation: "Institution"
    role: "corresponding"
journal: ""
year: 2024
volume: ""
pages: ""

# Research Question
research_question:
  primary: "What is the effect of I on O in P?"
  secondary:
    - "Does the effect differ by subgroup?"
    - "What are the safety outcomes?"
  hypothesis: "We hypothesized that I would improve O compared to C"

# Population
population:
  species: "human | animal | in_silico"
  description: "Adults aged 18-65 with diagnosis of X"
  sample_size: 500
  sample_size_justification: "Power analysis indicated n=450 needed for 80% power"
  setting: "multi-center hospital | community | laboratory | online"
  country: "USA, UK, Germany"
  demographics:
    age_mean: 45.2
    age_sd: 12.3
    age_range: "18-65"
    sex_female_pct: 52
    ethnicity: "..."
  inclusion_criteria:
    - "Age 18-65"
    - "Diagnosed with X"
  exclusion_criteria:
    - "Pregnant"
    - "Prior treatment with Y"
  recruitment: "Consecutive patients from clinic"
  retention_rate: 0.94

# Intervention
intervention:
  name: "Drug X"
  description: "Oral administration of Drug X at 10mg daily"
  duration: "12 months"
  dose: "10mg/day"
  route: "oral"
  mechanism: "Inhibits Z pathway"
  comparator:
    type: "placebo | active_control | usual_care | before_after | none"
    name: "Placebo"
    description: "Matching placebo tablet"

# Outcomes
outcomes:
  primary:
    name: "Symptom severity score"
    measure: "Disease-Specific Rating Scale (0-100)"
    timepoint: "12 months"
    result:
      direction: "improved | worsened | no_change"
      intervention_group: "32.5 (SD 8.2)"
      control_group: "45.1 (SD 9.1)"
      difference: "-12.6"
      effect_size: "Cohen's d = 0.82"
      confidence_interval: "95% CI: -15.1 to -10.1"
      p_value: "<0.001"
      clinical_significance: "Exceeds MCID of 8 points"
  secondary:
    - name: "Quality of life"
      measure: "SF-36"
      result: "Improved by 8.3 points (p=0.003)"

# Key Claims
key_claims:
  - claim: "Drug X significantly reduces symptom severity"
    evidence: "30% improvement vs placebo, p<0.001, d=0.82"
    strength: "strong"
    section: "results"
    caveats: "Effect may be smaller in real-world settings"
  - claim: "Drug X is safe and well-tolerated"
    evidence: "Adverse event rate 12% vs 11% for placebo"
    strength: "moderate"
    section: "results"

# Methods Detail
methods:
  design: "randomized_controlled_trial | cohort | case_control | cross_sectional | longitudinal | qualitative"
  randomization: "computer-generated block randomization"
  blinding: "double-blind | single-blind | open-label"
  allocation_concealment: "central pharmacy | sealed envelopes | none"
  data_collection: "structured interviews | medical records | surveys | lab tests"
  analysis: "intention_to_treat | per_protocol | as_treated"
  statistical_methods: "mixed-effects model, adjusted for baseline severity"
  power_analysis: "80% power to detect d=0.3 at alpha=0.05"
  preregistration: "ClinicalTrials.gov NCT0123456"

# Limitations
limitations:
  author_stated:
    - "12-month duration may not capture long-term effects"
    - "Excluded patients with comorbidities"
  reviewer_identified:
    - "Industry-funded (potential bias)"
    - "Primary outcome is subjective"

# Funding
funding:
  source: "PharmaCorp Inc."
  role: "Funded the study; authors had full control of data"
  conflict_of_interest: "Dr. Smith is a consultant for PharmaCorp"

# Data Availability
data_availability:
  data: "available_on_request | public | not_available"
  code: "github.com/..."
  registration: "ClinicalTrials.gov: NCT0123456"
```

## Template: Systematic Review / Meta-Analysis

```yaml
study_id: "Author (Year)"
paper_type: "systematic_review"

research_question:
  structured_format: "PICO"
  population: "..."
  intervention: "..."
  comparison: "..."
  outcome: "..."

search_strategy:
  databases: ["PubMed", "Embase", "Cochrane Library", "S2"]
  date_range: "2015-2024"
  search_terms: "..."
  filters: "English language, human studies"
  supplementary_methods: ["hand-searching reference lists", "contacting authors"]

screening:
  total_identified: 2838
  duplicates_removed: 423
  screened_title_abstract: 2415
  full_text_reviewed: 492
  included: 69

quality_assessment:
  tool_used: "Cochrane RoB 2"
  results: "45 low risk, 15 some concerns, 9 high risk"

synthesis:
  type: "narrative | meta-analysis | mixed"
  meta_analysis_results:
    pooled_effect: "RR 0.72 (95% CI: 0.65-0.80)"
    heterogeneity_i2: "45%"
    publication_bias: "Egger's test p=0.12 (no evidence of bias)"
  main_findings:
    - "Intervention X reduces the risk of Y by 28%"
    - "Effect is consistent across subgroups"
  certainty_of_evidence: "GRADE: moderate certainty"

research_gaps:
  - "No studies in pediatric population"
  - "Long-term follow-up data lacking"
```

## Template: Methodology Paper

```yaml
study_id: "Author (Year)"
paper_type: "methodology"

problem:
  existing_gap: "Current methods for X are slow and inaccurate"
  proposed_solution: "We introduce Method Y that addresses gap Z"

proposed_method:
  name: "MethodY"
  key_innovation: "Novel use of attention mechanism for X"
  architecture: "Transformer-based encoder-decoder"
  inputs: "Raw sequence data"
  outputs: "Classification labels + confidence scores"
  computational_requirements: "1x A100 GPU, 24h training"
  implementation: "PyTorch, code available at github.com/..."

evaluation:
  benchmarks: ["Benchmark A", "Benchmark B", "Benchmark C"]
  metrics: ["accuracy", "F1", "AUC-ROC", "inference time"]
  baseline_comparisons:
    - method: "Previous SOTA"
      results: "MethodY achieves 95.2% vs 91.8% on Benchmark A"
  ablation_study: true
  statistical_significance: true

limitations:
  - "Only tested on English data"
  - "Requires large training set"
```

## Template: Case Report (CARE)

```yaml
study_id: "Author (Year)"
paper_type: "case_report"

patient:
  age: 45
  sex: "female"
  presenting_complaint: "..."
  medical_history: "..."
  diagnoses: ["..."]

timeline:
  - event: "Presentation"
    date: "2024-01-15"
    findings: "..."
  - event: "Diagnosis"
    date: "2024-01-20"
    findings: "..."
  - event: "Treatment"
    date: "2024-01-25"
    details: "..."
  - event: "Follow-up"
    date: "2024-06-15"
    outcome: "..."

intervention: "..."
outcome: "..."
adverse_events: "..."
key_learning: "..."
```
