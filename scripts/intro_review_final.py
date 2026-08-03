"""
New Introduction with comprehensive BTC interpretation methods review.
Scholar-level narrative establishing deep expertise.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from lxml import etree
import zipfile

src = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_3-revised_clean.docx"
out = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_4-intro_rewritten.docx"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def pt(p):
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))

def make_para(text):
    p = etree.Element(f'{{{W}}}p')
    ppr = etree.SubElement(p, f'{{{W}}}pPr')
    etree.SubElement(ppr, f'{{{W}}}jc').set(f'{{{W}}}val', 'both')
    r = etree.SubElement(p, f'{{{W}}}r')
    rpr = etree.SubElement(r, f'{{{W}}}rPr')
    etree.SubElement(rpr, f'{{{W}}}rFonts').set(f'{{{W}}}cs', 'Times New Roman')
    t = etree.SubElement(r, f'{{{W}}}t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text
    return p

with zipfile.ZipFile(src, 'r') as zin:
    all_files = {name: zin.read(name) for name in zin.namelist()}

root = etree.fromstring(all_files['word/document.xml'])
body = root.find(f'{{{W}}}body')
all_children = list(body)

intro_h = exp_h = None
for i, c in enumerate(all_children):
    if c.tag == f'{{{W}}}p':
        t = pt(c).strip()
        if t == '1. Introduction': intro_h = i
        if t == '2. Experimental Section': exp_h = i; break

old = [i for i in range(intro_h+1, exp_h) if all_children[i].tag == f'{{{W}}}p']
for i in sorted(old, reverse=True):
    all_children[i].getparent().remove(all_children[i])
print(f"Removed {len(old)} old paragraphs")

# ================================================================
# NEW INTRODUCTION — 8 paragraphs
# ================================================================

P1 = (
    "Multi-stage hydraulic fracturing of horizontal wells has made unconventional "
    "reservoirs—tight oil, shale gas, and coalbed methane—a cornerstone of global "
    "hydrocarbon supply [1–4]. A single well may contain 10 to 30 individually "
    "fractured stages, yet operators lack a routine method for determining per-stage "
    "contributions to total production [5,6]. Without per-stage allocation data, "
    "underperforming intervals go undiagnosed, stage spacing cannot be optimized, "
    "and completion designs remain unvalidated [7,8]. Existing monitoring technologies "
    "each involve inherent trade-offs: production logging requires well intervention "
    "and captures only a snapshot [9]; fiber-optic sensing demands permanent downhole "
    "cable installation [10,11]; and microseismic monitoring images fracture geometry "
    "rather than flow contribution [12]. Tracer-based diagnostics circumvent these "
    "limitations—they require no downhole tools, can be deployed during completion, "
    "and provide direct chemical evidence linking each labeled interval to its "
    "produced fluids [13,14]."
)

P2 = (
    "Chemical tracers have been deployed in oilfield operations since the 1950s "
    "[15] and have evolved from simple radioactive waterflood monitors to "
    "sophisticated partitioning inter-well tracer tests capable of quantifying "
    "residual oil saturation [16,17]. Recent multi-tracer field campaigns have "
    "demonstrated quantitative per-stage production allocation at field scale: "
    "Yang et al. [18] deployed 18 distinct tracers across 12 stages and tracked "
    "stage contributions over 285 days, while Arshad et al. [19] and Al Raisi "
    "et al. [20] independently validated tracer-based stage-contribution profiling "
    "in multi-stage completions. Among tracer-based approaches, the tracer "
    "proppant—a composite particle in which the tracer agent is immobilized "
    "within a solid carrier and co-injected with fracturing fluid—offers a "
    "critical operational advantage: the tracer remains in the fracture after a "
    "single placement, enabling long-term, stage-specific monitoring without "
    "repeated intervention [21]. Recent designs span ceramic carriers with "
    "organic-dye or quantum-dot tracers [21,22], rare-earth-doped polymer "
    "coatings for multi-element coding [23], oleophilic Fe₃O₄/polystyrene "
    "microspheres [24], dual-zone tracer-coded proppants [25], multi-colored "
    "dye-tracer proppants [26], and marked proppant transport tracers [27]."
)

P3 = (
    "The question that remains unanswered—and that this paper addresses—is "
    "whether a tracer proppant can deliver more than qualitative confirmation "
    "of stage activity: can it quantify how much each stage is producing, using "
    "only the shape of the tracer breakthrough curve (BTC) measured at the "
    "wellhead? Answering this question requires solving two distinct problems. "
    "The first is the release problem: at what rate does the tracer leave the "
    "proppant matrix? All existing tracer proppant studies address this through "
    "batch experiments fitted to the Korsmeyer-Peppas (K-P) power law, "
    "C/C₀ = K·tⁿ [28–30]. The K-P model classifies the release mechanism—"
    "Fickian diffusion (n ≤ 0.43), anomalous transport (0.43 < n < 0.85), or "
    "Case-II relaxation (n ≥ 0.85)—and yields the temperature-dependent rate "
    "constant K. These are valuable descriptors, but they are obtained in a "
    "well-mixed vessel with no spatial coordinate and no flow field. The K-P "
    "model characterizes release in a beaker; it does not predict the "
    "concentration that will be observed at a sampling point meters downstream, "
    "after the released tracer has traversed the proppant pack and production "
    "tubing under the combined influence of advection, dispersion, and the "
    "convolution of sustained release with flow."
)

P4 = (
    "The second is the transport problem: given a tracer source, how is the "
    "released tracer conveyed to the sampling point, and what does the shape "
    "of the resulting BTC reveal about the flow field? This problem has been "
    "studied extensively, and the methods developed for it constitute a rich "
    "methodological landscape. At the simplest level are empirical approaches "
    "that extract a single scalar metric from the BTC. The peak-concentration "
    "time, t_peak, can be converted to a flow rate via Q = xπd²/(4·t_peak) "
    "under the assumption of piston-like displacement; this works adequately "
    "only at high Péclet numbers (Pe > 100) where dispersion is negligible and "
    "the BTC is nearly symmetric. The mean residence time, computed as the "
    "first moment of the BTC, MRT = ∫t·C dt / ∫C dt, is more robust because it "
    "exploits the entire curve rather than a single point, but it conflates all "
    "transport processes into a single number and provides no mechanistic "
    "insight into the relative contributions of different release or transport "
    "regimes. Tracer mass-balance methods allocate production among stages in "
    "proportion to the total recovered tracer mass from each interval; these "
    "methods use the integral of the BTC—its zeroth moment—but discard all "
    "information encoded in the curve shape, including the peak arrival time, "
    "the dispersion signature, and the tail persistence. All three empirical "
    "approaches share a common limitation: none can decompose the BTC into "
    "physically distinct contributions, and none can recover a flow rate "
    "without an independent calibration of the source term."
)

P5 = (
    "The classical physics-based approach fits an analytical solution of the "
    "one-dimensional advection-dispersion equation (ADE), ∂C/∂t + v·∂C/∂x = "
    "D·∂²C/∂x², to the observed BTC. Van Genuchten and Alves [31] compiled "
    "analytical solutions for a comprehensive set of initial and boundary "
    "conditions—instantaneous pulses, finite-duration injections, and "
    "continuous sources—and these remain the standard reference. By least-"
    "squares fitting of the appropriate solution to the observed concentration "
    "history, one recovers the transport parameters: velocity v, dispersivity "
    "α, and, by extension, the volumetric flow rate Q and the swept pore "
    "volume. Shook et al. [32] advanced this paradigm from curve fitting to "
    "moment analysis: by integrating the BTC to compute its temporal moments, "
    "their method extracts swept volume, sweep efficiency, and remaining oil "
    "saturation directly, without requiring a numerical reservoir simulator—a "
    "significant practical advance, but one that still treats the tracer source "
    "as a completed, known injection. Juliusson and Horne [33] introduced a "
    "deconvolution framework in which the BTC is expressed as the convolution "
    "of the injection history with a tracer kernel κ(t)—a transfer function "
    "characterized by pore volume, Péclet number, and a dispersion correction "
    "factor—and recovered via parametric or nonparametric deconvolution under "
    "variable flow-rate conditions. An important insight from this work is "
    "that the convolution is more naturally expressed in terms of cumulative "
    "flow rather than clock time, making the method robust to rate variations. "
    "Fontalvo et al. [16] underscored that model selection is not a matter of "
    "convenience: applying a physically inappropriate transport model to "
    "partitioning tracer data can systematically overestimate or underestimate "
    "remaining oil saturation, with direct financial consequences for field-"
    "development decisions."
)

P6 = (
    "For heterogeneous and fractured media—precisely the environments in which "
    "tracer proppants are deployed—the classical ADE often fails to capture "
    "the characteristic early breakthrough and prolonged late-time tailing "
    "observed in measured BTCs, motivating the development of non-Fickian "
    "transport models. Dual-porosity (mobile-immobile) models partition the "
    "flow domain into a mobile region (fractures, where advection dominates) "
    "and an immobile region (matrix, where diffusion controls solute exchange), "
    "with first-order mass transfer between them producing the extended "
    "concentration tails that are the hallmark of matrix diffusion. Multirate "
    "mass transfer (MRMT) formulations extend this concept by treating the "
    "mass-transfer coefficient as a statistical distribution rather than a "
    "single value, reflecting the spatial variability of matrix block sizes "
    "and diffusion path lengths in realistic fracture networks; the late-time "
    "BTC tail then follows a characteristic power-law decay whose exponent "
    "is diagnostic of the underlying rate distribution. The Continuous Time "
    "Random Walk (CTRW) framework provides a more general stochastic "
    "description in which solute transport is modeled as a sequence of "
    "discrete transitions with a heavy-tailed waiting-time distribution, "
    "parameterized by an exponent β that quantifies the degree of non-Fickian "
    "behavior (β < 2 indicating anomalous transport). CTRW has been "
    "successfully applied to tracer tests in fractured crystalline rock and "
    "heterogeneous carbonate reservoirs, and the β parameter has been linked "
    "quantitatively to fracture network topology—specifically, fracture "
    "orientation relative to the mean flow direction. At the highest level "
    "of complexity, full-physics numerical inversion treats the reservoir "
    "model (permeability, porosity, fracture geometry) as the unknown and "
    "adjusts it iteratively to match the observed BTC through history "
    "matching, often accelerated by streamline-based sensitivity computations "
    "or reduced-order modeling. Velasco-Lozano et al. [34] recently derived "
    "analytical ADE solutions for two-phase, advection-dominated transport "
    "of partitioning tracers, and Mazo et al. [35] developed a stream-tube "
    "decomposition for multi-stage fractured wells with explicit tracer "
    "transfer between oil and water phases, achieving a hundredfold "
    "computational speedup that makes per-stage parameter estimation "
    "numerically tractable."
)

P7 = (
    "A single structural premise runs through every method described above—from "
    "peak-time estimation through CTRW to full numerical inversion: the tracer "
    "source is treated as a known input. Whether it is a Dirac delta pulse, a "
    "finite-duration injection of measured concentration, or a continuous "
    "source of prescribed strength, the source function is an experimental "
    "boundary condition, and the inverse problem is to estimate the transport "
    "parameters given that known source. A tracer proppant does not satisfy "
    "this premise. The tracer is not injected as a discrete event; it is "
    "released continuously from a polymeric matrix at a rate governed by "
    "matrix diffusion and polymer relaxation—the very processes characterized "
    "by K-P kinetics—and this release evolves throughout the production "
    "period. The BTC measured at the wellhead is therefore the convolution "
    "of two unknown functions: a release rate (governed by matrix-diffusion "
    "kinetics) and a transport operator (governed by advection and dispersion "
    "in the production tubing). Neither function is known independently, and "
    "both must be recovered from the shape of a single concentration history. "
    "To our knowledge, this coupled release-transport inverse problem has not "
    "been addressed in the literature. Its practical consequence is that "
    "existing tracer proppants—despite their operational advantages of single-"
    "placement longevity and freedom from downhole instrumentation—remain "
    "qualitative diagnostic tools: they can confirm which stages are producing "
    "but cannot answer the quantitative question that operators and reservoir "
    "engineers need answered."
)

P8 = (
    "We resolve this coupled inverse problem by exploiting a feature of the "
    "measurement geometry that has not been utilized in previous BTC "
    "interpretation methods. A tracer proppant BTC obtained after an extended "
    "shut-in carries the superimposed signatures of two physically distinct "
    "processes that can be separated mathematically. Process I: during the "
    "shut-in period, tracer continuously diffuses out of the proppant matrix "
    "and accumulates in the surrounding proppant pack and near-wellbore "
    "region, forming a spatially distributed tracer inventory; when the well "
    "opens, this accumulated inventory is swept toward the sampling point as "
    "a coherent slug, producing a concentration peak whose shape is governed "
    "by the advective-dispersive transport of a pre-existing spatial "
    "distribution—mathematically, a Gaussian. Process II: after passage of "
    "the main slug, residual tracer continues to diffuse out of the matrix "
    "at a lower but persistent rate, feeding a slowly decaying concentration "
    "tail governed by matrix-diffusion-controlled release into a flowing "
    "stream—mathematically, a complementary error function (erfc). These two "
    "contributions overlap in time but can be separated by expressing the BTC "
    "as the weighted sum of a Gaussian rise component and an erfc fall "
    "component, joined by a smooth hyperbolic-tangent weight function "
    "w(t) = ½[1 + tanh((t₀ − t)/σ)] that ensures C¹ continuity for gradient-"
    "based optimization. The resulting six-parameter model—baseline "
    "concentration, pulse amplitude, tail amplitude, dispersivity, flow rate, "
    "and transition center—is fitted to the observed BTC. Critically, the "
    "flow rate Q is recovered as a free parameter; it is not constrained by "
    "the pump setting, providing a built-in self-calibration check. The "
    "Peclet number Pe = x/α, computed from the fitted dispersivity, supplies "
    "an independent mechanistic diagnostic that can be cross-validated against "
    "the transport regime identified by K-P kinetics. The decomposition "
    "itself—Gaussian pulse versus erfc tail—reveals the relative contribution "
    "of shut-in accumulation and sustained release to the total tracer signal, "
    "information that no single-component model can provide."
)

P9 = (
    "We validate this dual-regime model against single-phase and steady-state "
    "two-phase core displacement experiments using an oleophilic epoxy/Fe₃O₄ "
    "tracer proppant (ESP-T). The epoxy matrix was selected in preference to "
    "conventional ceramic (high-density [36,37]) and polystyrene (limited "
    "thermal stability [38,39]) carriers for its cross-linked-network-"
    "controlled release characteristics [40–42]; stearic acid surface "
    "modification of the encapsulated nano-Fe₃O₄ imparts oleophilic "
    "selectivity. Four independent lines of evidence support the model. "
    "Statistically, the dual-regime formulation is decisively preferred over "
    "four simpler single-component alternatives (ΔAICc = 32.7, F-test "
    "p < 10⁻⁶; R² = 0.9939). Physically, the fitted flow rate (0.46 mL/min) "
    "agrees with the independently set pump rate (0.50 mL/min) within 8%, "
    "demonstrating self-calibration: the model recovers the correct flow rate "
    "from the concentration data alone. Mechanistically, the Peclet number "
    "(Pe = 0.934) independently confirms the non-Fickian transport regime "
    "identified by K-P kinetics (n = 0.45–0.85), establishing consistency "
    "between two entirely independent measurement modalities. The signal "
    "decomposition reveals that approximately 47% of the integrated tracer "
    "signal originates from sustained matrix-diffusion-controlled release "
    "rather than the initial accumulation slug—a result robust to a six-fold "
    "variation in the transition width (46.8–47.5%) and one that carries a "
    "significant operational implication: a single shut-in suffices for "
    "long-term monitoring, because nearly half of the detectable signal is "
    "generated during the production period itself. Under steady-state two-"
    "phase flow, the oil-phase tracer mass flux eliminates water-dilution "
    "artifacts and quantitatively tracks oil production rates (Pearson "
    "r = 0.97, RMSD = 8.3%), establishing a pathway from wellhead "
    "concentration measurements to per-interval production allocation that "
    "requires no downhole tools and only a single shut-in."
)

new_paras = [P1, P2, P3, P4, P5, P6, P7, P8, P9]

# Insert
body = root.find(f'{{{W}}}body')
all_c = list(body)
intro_h = None
for i, c in enumerate(all_c):
    if c.tag == f'{{{W}}}p' and pt(c).strip() == '1. Introduction':
        intro_h = i; break

for j, text in enumerate(new_paras):
    new_p = make_para(text)
    all_c[intro_h + j].addnext(new_p)
    all_c = list(body)

# Remove strays
all_c = list(body)
nl = el = None
for i, c in enumerate(all_c):
    if c.tag == f'{{{W}}}p':
        t = pt(c).strip()
        if 'no downhole tools and only a single shut-in' in t: nl = i
        if t == '2. Experimental Section': el = i; break
if nl and el:
    stray = [i for i in range(nl+1, el) if all_c[i].tag == f'{{{W}}}p']
    for i in reversed(stray): all_c[i].getparent().remove(all_c[i])
    if stray: print(f"Removed {len(stray)} stray")

all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        zout.writestr(name, data)

ttl = sum(len(t) for t in new_paras)
print(f"Saved: {out}")
print(f"{len(new_paras)} paragraphs, {ttl} chars")
for i, t in enumerate(new_paras):
    print(f"  P{i+1}: {len(t)} chars")
