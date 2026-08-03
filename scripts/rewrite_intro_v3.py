"""
Complete reconstruction of Introduction based on paper content.
Natural narrative flow: problem → what's been tried → why it fails → what we do.
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

# Find boundaries & remove old intro
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
# COMPLETELY NEW INTRODUCTION — 7 paragraphs
# ================================================================

P1 = (
    "Multi-stage hydraulic fracturing of horizontal wells has made unconventional "
    "reservoirs—tight oil, shale gas, and coalbed methane—a dominant component of "
    "global hydrocarbon supply [1–4]. A single horizontal well may contain 10 to "
    "30 individually fractured stages, yet the industry lacks a routine method for "
    "determining how much each stage contributes to total production [5,6]. Without "
    "per-stage allocation data, operators cannot identify underperforming intervals, "
    "optimize stage spacing, or validate completion designs against production "
    "outcomes [7,8]. Production logging tools require well intervention and provide "
    "only snapshot measurements [9]; fiber-optic sensing demands permanent cable "
    "installation [10,11]; and microseismic monitoring characterizes fracture "
    "geometry rather than flow contribution [12]. Tracer-based methods avoid these "
    "limitations: they require no downhole instrumentation, can be deployed during "
    "completion, and provide direct chemical evidence linking each labeled interval "
    "to its produced fluids [13,14]."
)

P2 = (
    "Chemical tracers have been deployed in oilfield operations since the 1950s "
    "[15] and have evolved from simple inter-well waterflood monitors to "
    "sophisticated partitioning tracer tests capable of quantifying residual oil "
    "saturation [16,17]. Recent multi-tracer field campaigns have demonstrated "
    "quantitative per-stage production allocation—Yang et al. [18] deployed 18 "
    "distinct tracers across 12 stages and tracked contributions over 285 days, "
    "while Arshad et al. [19] and Al Raisi et al. [20] independently validated "
    "tracer-based stage contribution profiling—confirming that tracer diagnostics "
    "are technically viable at field scale. Among tracer-based approaches, the "
    "tracer proppant offers a distinct operational advantage: a composite particle "
    "in which the tracer agent is immobilized within a solid carrier co-injected "
    "with fracturing fluid, the tracer proppant remains in the fracture after a "
    "single placement, enabling long-term monitoring without repeated intervention "
    "[21]. Recent designs include ceramic-based carriers [21,22], rare-earth-doped "
    "polymer coatings [23], oleophilic Fe₃O₄/polystyrene microspheres [24], dual-"
    "zone tracer-coded proppants [25], multi-colored dye-tracer proppants [26], "
    "and marked proppant transport tracers [27]."
)

P3 = (
    "All of these tracer proppant studies, despite their diversity of materials "
    "and tracer chemistries, share an identical methodological structure: tracer "
    "release is measured in batch experiments and fitted to the Korsmeyer-Peppas "
    "(K-P) power law, C/C₀ = K·tⁿ [28–30]. The K-P model identifies the release "
    "mechanism—Fickian diffusion (n ≤ 0.43), anomalous transport (0.43 < n < 0.85), "
    "or Case-II relaxation (n ≥ 0.85)—and yields the temperature-dependent rate "
    "constant K. These parameters characterize the release process, but they are "
    "obtained in a well-mixed vessel with no spatial coordinate and no flow field. "
    "The K-P model can quantify how fast tracer leaves the proppant in a beaker; "
    "it cannot predict the concentration that will be observed at a wellhead "
    "sampling point located meters downstream, after the released tracer has "
    "traveled through the proppant pack and production tubing. The transport "
    "step—advection, dispersion, and the convolution of sustained release with "
    "flow—is simply not part of the model. Consequently, existing tracer "
    "proppants can confirm that a given stage is producing but cannot translate "
    "a breakthrough curve into a production rate."
)

P4 = (
    "The transport side of the problem has been studied extensively, but in a "
    "different context. The one-dimensional advection-dispersion equation (ADE), "
    "∂C/∂t + v·∂C/∂x = D·∂²C/∂x², has served for decades as the standard framework "
    "for interpreting tracer breakthrough curves (BTCs) in porous media [31]. In "
    "petroleum engineering, the ADE has been applied primarily to inter-well tracer "
    "tests, where the tracer source—an injection of known mass, concentration, and "
    "duration—is a controlled experimental input. Shook et al. [32] used residence-"
    "time-distribution moment analysis of tracer BTCs to extract swept volume, "
    "sweep efficiency, and remaining oil saturation without requiring numerical "
    "simulation. Fontalvo et al. [16] showed that physically justified model "
    "selection in such tests is not merely an academic concern: applying an "
    "inappropriate transport model to partitioning tracer data can systematically "
    "overestimate or underestimate remaining oil, with direct financial "
    "consequences for field-development decisions. More recently, analytical "
    "solutions have been extended to two-phase flow [33] and to multi-stage "
    "fractured wells with explicit tracer partitioning between phases [34], "
    "demonstrating that per-stage allocation from tracer signals is theoretically "
    "achievable when the source function is known."
)

P5 = (
    "A tracer proppant, however, does not provide a known source function. The "
    "tracer is not injected as a discrete pulse at a known time and concentration; "
    "it is released continuously from a polymeric matrix at a rate governed by "
    "matrix diffusion and polymer relaxation—the very processes characterized by "
    "K-P kinetics—and this release evolves over the entire production period. The "
    "BTC measured at the wellhead is therefore the convolution of an unknown "
    "release function with advective-dispersive transport through an unknown flow "
    "field. This is a coupled inverse problem: neither the source term nor the "
    "transport parameters are known independently, and both must be recovered "
    "from the shape of a single concentration history. To our knowledge, no "
    "existing method—neither direct ADE fitting, nor moment analysis, nor "
    "numerical inversion—addresses this coupled problem. Its practical consequence "
    "is that tracer proppants, despite their operational advantages, remain a "
    "qualitative diagnostic tool: they can confirm which stages are producing, "
    "but they cannot answer the quantitative question that operators need "
    "answered—how much."
)

P6 = (
    "In this work, we resolve the coupled release-transport inverse problem by "
    "recognizing that a tracer BTC obtained after an extended shut-in carries the "
    "signatures of two physically distinct processes. Process I: during shut-in, "
    "tracer continuously diffuses from the epoxy matrix into the proppant pack "
    "and near-wellbore region; when the well opens, this accumulated tracer is "
    "swept toward the sampling point as a coherent slug, producing a Gaussian-"
    "shaped concentration peak governed by advective-dispersive transport. "
    "Process II: after the main slug has passed, residual tracer continues to "
    "diffuse out of the matrix at a lower but persistent rate, feeding a slowly "
    "decaying concentration tail described by the complementary error function "
    "(erfc). These two contributions overlap in time, but they can be separated "
    "mathematically. We accordingly develop a dual-regime piecewise ADE model in "
    "which the BTC is expressed as the weighted sum of a Gaussian rise component "
    "and an erfc fall component, joined by a smooth hyperbolic-tangent (tanh) "
    "transition that ensures C¹ continuity for gradient-based optimization. The "
    "model contains six free parameters—baseline concentration, pulse amplitude, "
    "tail amplitude, dispersivity, flow rate, and transition center—each with a "
    "clear physical interpretation. The decomposition is the central innovation: "
    "it separates the shut-in accumulation signal from the sustained-release "
    "signal, recovers the per-interval flow rate directly from the concentration "
    "history, and reveals the relative contribution of each process to the total "
    "tracer signal."
)

P7 = (
    "We validate this model against single-phase and two-phase core displacement "
    "experiments using an oleophilic epoxy/Fe₃O₄ tracer proppant (ESP-T) "
    "synthesized via emulsion polymerization. The epoxy matrix, chosen for its "
    "thermal stability and cross-linked-network-controlled release [39–41], is "
    "rendered oleophilic through stearic acid surface modification of the "
    "encapsulated nano-Fe₃O₄, enabling selective oil-phase tracer delivery. The "
    "dual-regime model is validated through four independent lines of evidence: "
    "statistical model selection decisively favors it over four simpler single-"
    "component alternatives (ΔAICc = 32.7, p < 10⁻⁶); the fitted flow rate self-"
    "calibrates against the independently set pump rate (0.46 vs. 0.50 mL/min, "
    "error 8%); the Peclet number (Pe = 0.934) independently confirms the non-"
    "Fickian transport regime identified by K-P kinetics; and the signal "
    "decomposition into Gaussian (53%) and erfc (47%) components is robust to a "
    "six-fold variation in the transition width. Under steady-state two-phase "
    "flow, the oil-phase tracer mass flux eliminates water-dilution artifacts and "
    "quantitatively tracks oil production rates (r = 0.97, RMSD = 8.3%). Together, "
    "these results establish a methodology for per-interval production allocation "
    "that requires only wellhead sampling and a single shut-in."
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
        if 'only wellhead sampling and a single shut-in' in t: nl = i
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
print(f"{len(new_paras)} paragraphs, {ttl} chars total")
for i, t in enumerate(new_paras):
    print(f"  P{i+1}: {len(t)} chars")
