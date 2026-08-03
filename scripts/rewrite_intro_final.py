"""
Complete reconstruction of Introduction — fresh approach.
Focus: how have people interpreted BTCs, and why can't those methods handle tracer proppants.
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

# Find & remove old intro
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
# COMPLETELY NEW INTRODUCTION
# ================================================================

P1 = (
    "Multi-stage hydraulic fracturing of horizontal wells has made unconventional "
    "reservoirs a cornerstone of global hydrocarbon supply [1–4]. A single well "
    "may contain 10 to 30 individually fractured stages, yet operators lack a "
    "routine method for determining how much each stage contributes to total "
    "production [5,6]. Without per-stage allocation data, underperforming intervals "
    "go undiagnosed, stage spacing cannot be optimized, and completion designs "
    "remain unvalidated against production outcomes [7,8]. Production logging "
    "requires well intervention and captures only a snapshot [9]; fiber-optic "
    "sensing demands permanent downhole installation [10,11]; and microseismic "
    "monitoring images fracture geometry, not flow [12]. Tracer-based diagnostics "
    "circumvent all of these limitations: they require no downhole tools, can be "
    "deployed during completion, and provide direct chemical evidence linking "
    "each labeled interval to its produced fluids [13,14]."
)

P2 = (
    "The tracer proppant—a composite particle in which a chemical tracer is "
    "immobilized within a solid carrier and co-injected with fracturing fluid—"
    "offers a particularly attractive implementation of this concept. Unlike "
    "dissolved tracers that are flushed from the formation within days to weeks, "
    "a tracer proppant remains in the fracture after placement, enabling "
    "long-term, stage-specific monitoring from a single deployment [21]. Recent "
    "designs span a wide range of carrier materials and tracer chemistries: "
    "ceramic-based carriers with organic dye or quantum-dot tracers [21,22], "
    "rare-earth-doped polymer coatings enabling multi-element coding [23], "
    "oleophilic Fe₃O₄/polystyrene microspheres for oil-phase selectivity [24], "
    "field-deployed proppants with dual near-zone and far-zone tracer codes [25], "
    "multi-colored dye-tracer proppants [26], and magnetically or visually marked "
    "proppants for transport studies [27]. Field trials have confirmed that tracer "
    "proppants can unambiguously identify which stages are producing [18–20,25]."
)

P3 = (
    "The question that remains unanswered—and that this paper addresses—is "
    "whether a tracer proppant can do more than confirm stage activity: can it "
    "quantify how much each stage is producing, using only the shape of the "
    "tracer breakthrough curve (BTC) measured at the wellhead? Answering this "
    "question requires solving two distinct problems. The first is the release "
    "problem: how fast does the tracer leave the proppant matrix? All existing "
    "tracer proppant studies address this through batch experiments fitted to "
    "the Korsmeyer-Peppas (K-P) power law, C/C₀ = K·tⁿ [28–30]. The K-P model "
    "identifies whether release is Fickian (n ≤ 0.43), anomalous (0.43 < n < 0.85), "
    "or Case-II (n ≥ 0.85), and provides the temperature-dependent rate constant "
    "K. This information is valuable, but it describes release in a stirred beaker—"
    "a zero-dimensional batch environment with no spatial coordinate, no flow "
    "field, and no mechanism for translating a release rate into a concentration "
    "at a downstream sampling point. The K-P model tells us how fast the tracer "
    "leaves the carrier; it does not tell us what concentration will be observed "
    "at the wellhead."
)

P4 = (
    "The second is the transport problem: once the tracer enters the flowing "
    "fluid, how is it conveyed to the sampling point? This is the domain of the "
    "advection-dispersion equation (ADE), ∂C/∂t + v·∂C/∂x = D·∂²C/∂x², which "
    "has been the standard framework for interpreting tracer BTCs in porous media "
    "for over four decades [31]. The classical approach fits an analytical ADE "
    "solution—typically the instantaneous pulse or continuous injection "
    "solution—to the observed BTC, recovering the transport parameters (velocity "
    "v, dispersivity α, and by extension the volumetric flow rate Q and pore "
    "volume). Shook et al. [32] advanced this paradigm by moving from curve "
    "fitting to moment analysis: integrating the BTC to extract swept volume, "
    "sweep efficiency, and remaining oil saturation directly, without requiring "
    "a numerical reservoir model. Fontalvo et al. [16] demonstrated that the "
    "choice of transport model is not an academic exercise—applying a physically "
    "inappropriate model to partitioning tracer data can systematically over- or "
    "underestimate remaining oil saturation, with direct consequences for field-"
    "development economics. More recently, analytical ADE solutions have been "
    "extended to two-phase flow in advection-dominated porous media [33], and "
    "stream-tube decomposition has been applied to multi-stage fractured wells "
    "with explicit tracer partitioning between oil and water phases [34]."
)

P5 = (
    "All of these ADE-based methods, regardless of their sophistication, share "
    "a single structural premise: the tracer source is known. In an inter-well "
    "tracer test, the injected mass, concentration, and duration are measured "
    "experimental inputs; the inverse problem is to estimate the transport "
    "parameters from the observed BTC, given a known source function. A tracer "
    "proppant does not satisfy this premise. The tracer is not injected as a "
    "discrete pulse; it is released continuously from a polymeric matrix at a "
    "rate governed by matrix diffusion and polymer relaxation—the very processes "
    "characterized by K-P kinetics—and this release evolves throughout the "
    "production period. The BTC measured at the wellhead is therefore the "
    "convolution of two unknown functions: the release rate (governed by matrix "
    "diffusion) and the transport operator (governed by advection and dispersion). "
    "Neither is known independently, and both must be recovered from the shape "
    "of a single concentration history. To our knowledge, this coupled release-"
    "transport inverse problem has not been addressed in the literature. Its "
    "practical consequence is that existing tracer proppants, despite their "
    "operational advantages, remain qualitative tools: they can confirm which "
    "stages are producing but cannot answer the quantitative question—how much."
)

P6 = (
    "We resolve this coupled inverse problem by exploiting a physical feature "
    "of the measurement that has not been utilized in previous BTC "
    "interpretation methods. A tracer proppant BTC obtained after an extended "
    "shut-in carries the superimposed signatures of two distinct processes. "
    "Process I: during shut-in, tracer continuously diffuses from the proppant "
    "matrix into the surrounding pack and near-wellbore region; when the well "
    "opens, this accumulated inventory is swept downstream as a coherent slug, "
    "producing a concentration peak whose shape is governed by advective-"
    "dispersive transport of a pre-existing spatial distribution—mathematically, "
    "a Gaussian. Process II: after passage of the main slug, tracer continues "
    "to diffuse out of the matrix at a lower but persistent rate, feeding a "
    "slowly decaying concentration tail governed by matrix-diffusion-controlled "
    "release into a flowing stream—mathematically, a complementary error "
    "function (erfc). These two contributions overlap in time, but they are "
    "mathematically separable. We accordingly decompose the BTC into a Gaussian "
    "rise component (Process I) and an erfc fall component (Process II), joined "
    "by a smooth hyperbolic-tangent (tanh) weight function w(t) = ½[1 + tanh((t₀ "
    "− t)/σ)] that provides C¹ continuity across the transition. The resulting "
    "six-parameter model—baseline concentration, pulse amplitude, tail amplitude, "
    "dispersivity, flow rate, and transition center—is fitted to the observed BTC "
    "by gradient-based optimization. Critically, the flow rate Q is recovered as "
    "a free parameter in the fit; it is not constrained by the pump setting, "
    "providing an internal self-calibration check. The Peclet number Pe = x/α, "
    "computed from the fitted dispersivity, provides independent mechanistic "
    "confirmation of the transport regime."
)

P7 = (
    "We validate this dual-regime model against single-phase and two-phase core "
    "displacement experiments using an oleophilic epoxy/Fe₃O₄ tracer proppant "
    "(ESP-T) synthesized via emulsion polymerization. The epoxy matrix [39–41] "
    "is rendered oleophilic through stearic acid surface modification, enabling "
    "selective oil-phase tracer delivery; it was chosen in preference to "
    "conventional ceramic carriers (high density [35,36]) and polystyrene "
    "matrices (limited thermal stability [37,38]). Four independent lines of "
    "evidence support the model. First, statistical model selection decisively "
    "favors the dual-regime formulation over four simpler single-component "
    "alternatives (ΔAICc = 32.7, F-test p < 10⁻⁶; R² = 0.9939). Second, the "
    "fitted flow rate (0.46 mL/min) agrees with the independently set pump rate "
    "(0.50 mL/min) within 8%, demonstrating physical self-calibration—the model "
    "recovers the correct flow rate from the concentration data alone. Third, "
    "the fitted Peclet number (Pe = 0.934) independently confirms the non-Fickian "
    "transport regime identified by K-P kinetics (n = 0.45–0.85), establishing "
    "mechanistic consistency between two entirely independent measurement "
    "modalities. Fourth, the decomposition reveals that approximately 47% of "
    "the integrated tracer signal originates from sustained matrix-diffusion-"
    "controlled release rather than the initial accumulation slug—a result that "
    "is robust to a six-fold variation in the transition width σ (46.8–47.5%) "
    "and that carries a significant operational implication: a single shut-in "
    "suffices for long-term monitoring, because nearly half of the detectable "
    "tracer signal is generated during the production period itself. Under "
    "steady-state two-phase flow, the oil-phase tracer mass flux eliminates "
    "water-dilution artifacts and quantitatively tracks oil production rates "
    "(Pearson r = 0.97, RMSD = 8.3%), providing a pathway from wellhead "
    "concentration measurements to per-interval production allocation without "
    "downhole tools or repeated intervention."
)

new_paras = [P1, P2, P3, P4, P5, P6, P7]

# ================================================================
# Insert
# ================================================================
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
        if 'without downhole tools or repeated intervention' in t: nl = i
        if t == '2. Experimental Section': el = i; break

if nl and el:
    stray = [i for i in range(nl+1, el) if all_c[i].tag == f'{{{W}}}p']
    for i in reversed(stray): all_c[i].getparent().remove(all_c[i])
    if stray: print(f"Removed {len(stray)} stray")

# Save
all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        zout.writestr(name, data)

ttl = sum(len(t) for t in new_paras)
print(f"Saved: {out}")
print(f"{len(new_paras)} paragraphs, {ttl} chars")
for i, t in enumerate(new_paras):
    print(f"  P{i+1}: {len(t)} chars")
