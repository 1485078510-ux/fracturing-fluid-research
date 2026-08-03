"""
Complete rewrite of Introduction — fluid narrative, methods with citations, simplified tracer section.
"""
import sys, io, re, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from lxml import etree
from copy import deepcopy

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
all_c = list(body)

intro_h = exp_h = None
for i, c in enumerate(all_c):
    if c.tag == f'{{{W}}}p':
        t = pt(c).strip()
        if t == '1. Introduction': intro_h = i
        if t == '2. Experimental Section': exp_h = i; break

old = [i for i in range(intro_h+1, exp_h) if all_c[i].tag == f'{{{W}}}p']
for i in sorted(old, reverse=True):
    all_c[i].getparent().remove(all_c[i])
print(f"Removed {len(old)} old paragraphs")

# ================================================================
# COMPLETELY NEW INTRODUCTION — 6 paragraphs, fluid narrative
# ================================================================

P1 = (
    "Multi-stage hydraulic fracturing of horizontal wells has made unconventional "
    "reservoirs a cornerstone of global hydrocarbon supply [1–4]. A single well "
    "may contain 10 to 30 individually fractured stages, yet no routine method "
    "exists for determining how much each stage contributes to total production "
    "[5,6]; without such data, underperforming intervals go undiagnosed and "
    "completion designs remain unvalidated against production outcomes [7,8]. "
    "Production logging requires well intervention and captures only a snapshot "
    "[9]; fiber-optic sensing demands permanent downhole cable installation "
    "[10,11]; and microseismic monitoring images fracture geometry rather than "
    "flow contribution [12]. Tracer-based diagnostics circumvent these "
    "limitations: they require no downhole tools, can be deployed during "
    "completion, and provide direct chemical evidence linking each labeled "
    "interval to its produced fluids [13,14]."
)

P2 = (
    "Among tracer-based approaches, the tracer proppant—a composite particle in "
    "which a chemical tracer is immobilized within a solid carrier and co-injected "
    "with fracturing fluid—offers a critical operational advantage over dissolved "
    "tracers. Because the particle remains in the fracture after placement, a "
    "single deployment enables long-term, stage-specific monitoring without "
    "repeated well intervention [21]. Chemical tracers have been deployed in "
    "oilfield operations since the 1950s [15], and multi-tracer field campaigns "
    "have recently demonstrated quantitative per-stage production allocation at "
    "field scale [18–20], confirming that tracer-based diagnostics are technically "
    "viable. Recent tracer proppant designs span ceramic carriers with organic-dye "
    "or quantum-dot tracers [21,22], rare-earth-doped polymer coatings for multi-"
    "element coding [23], oleophilic Fe₃O₄/polystyrene microspheres [24], dual-"
    "zone tracer-coded proppants [25], and multi-colored dye-tracer proppants "
    "[26]. Despite this diversity of carrier materials and tracer chemistries, "
    "all of these studies share an identical methodological structure: tracer "
    "release is measured in batch experiments and fitted to the Korsmeyer-Peppas "
    "(K-P) power law, C/C₀ = K·tⁿ [28–30]. The K-P model classifies the release "
    "mechanism—Fickian diffusion for n ≤ 0.43, anomalous transport for "
    "0.43 < n < 0.85, or Case-II relaxation for n ≥ 0.85—and yields the "
    "temperature-dependent rate constant K. This information characterizes "
    "release in a well-mixed vessel, but it provides no connection to the "
    "concentration that will be observed at a wellhead sampling point after the "
    "released tracer has traversed the proppant pack and production tubing. The "
    "transport step—advection, dispersion, and the convolution of sustained "
    "release with flow—is absent from the model. Consequently, existing tracer "
    "proppants can confirm which stages are producing, but they cannot translate "
    "a breakthrough curve into a production rate."
)

P3 = (
    "The interpretation of tracer breakthrough curves (BTCs) has been studied "
    "extensively in the context of inter-well tracer tests, where the tracer "
    "source—an injection of known mass, concentration, and duration—is a "
    "controlled experimental input. The classical approach fits an analytical "
    "solution of the one-dimensional advection-dispersion equation (ADE), "
    "∂C/∂t + v·∂C/∂x = D·∂²C/∂x², to the observed BTC to recover the transport "
    "parameters: velocity v, dispersivity α, and volumetric flow rate Q. Van "
    "Genuchten and Alves [31] compiled analytical solutions for a comprehensive "
    "range of initial and boundary conditions, and these remain the standard "
    "reference. Shook et al. [32] advanced beyond direct curve fitting by "
    "applying residence-time-distribution moment analysis to tracer BTCs; their "
    "method extracts swept volume, sweep efficiency, and remaining oil saturation "
    "without requiring a numerical reservoir simulator. Fontalvo et al. [16] "
    "subsequently demonstrated that physically justified model selection carries "
    "direct operational consequences: applying an inappropriate transport model "
    "to partitioning tracer data can systematically overestimate or underestimate "
    "remaining oil saturation. In parallel, deconvolution-based methods express "
    "the BTC as the convolution of the injection history with a tracer transfer "
    "function and recover the kernel via parametric or nonparametric inversion, "
    "an approach made robust to variable flow rates by expressing the convolution "
    "in terms of cumulative flow rather than clock time. For fractured and "
    "heterogeneous media, where classical ADE solutions fail to capture the "
    "characteristic early breakthrough and prolonged late-time tailing, a family "
    "of non-Fickian transport models has been developed: dual-porosity mobile-"
    "immobile formulations with first-order or multirate mass transfer between "
    "fractures and matrix, continuous-time random walk (CTRW) frameworks with "
    "heavy-tailed transition-time distributions, and full-physics numerical "
    "inversion accelerated by streamline-based sensitivity computations. Most "
    "recently, analytical ADE solutions have been extended to two-phase, "
    "advection-dominated transport of partitioning tracers [33], and stream-tube "
    "decomposition has been applied to multi-stage fractured wells with explicit "
    "tracer partitioning between oil and water phases, achieving the computational "
    "efficiency necessary for per-stage parameter estimation [34]."
)

P4 = (
    "A single structural premise runs through every method described above, from "
    "peak-time estimation through CTRW to full numerical inversion: the tracer "
    "source is treated as a known input. Whether a Dirac delta pulse, a finite-"
    "duration injection of measured concentration, or a continuous source of "
    "prescribed strength, the source function is an experimental boundary "
    "condition, and the inverse problem is to estimate transport parameters given "
    "that known source. A tracer proppant does not satisfy this premise. The "
    "tracer is not injected as a discrete event; it is released continuously "
    "from a polymeric matrix at a rate governed by matrix diffusion and polymer "
    "relaxation—the very processes characterized by K-P kinetics—and this release "
    "evolves throughout the production period. The BTC measured at the wellhead "
    "is therefore the convolution of two unknown functions: a release rate "
    "governed by matrix-diffusion kinetics and a transport operator governed by "
    "advection and dispersion. Neither function is known independently, and both "
    "must be recovered from the shape of a single concentration history. To our "
    "knowledge, this coupled release-transport inverse problem has not been "
    "addressed in the literature. Its practical consequence is that tracer "
    "proppants, despite their operational advantages, remain qualitative tools "
    "that can confirm stage activity but cannot quantify it."
)

P5 = (
    "We resolve this coupled inverse problem by exploiting a feature of the "
    "measurement geometry that has not been utilized in previous BTC "
    "interpretation methods. A tracer proppant BTC obtained after an extended "
    "shut-in carries the superimposed signatures of two physically distinct "
    "processes. During the shut-in period, tracer continuously diffuses out of "
    "the proppant matrix and accumulates in the surrounding pack and near-"
    "wellbore region; when the well opens, this accumulated inventory is swept "
    "toward the sampling point as a coherent slug, producing a concentration peak "
    "governed by the advective-dispersive transport of a pre-existing spatial "
    "distribution—mathematically, a Gaussian. After passage of the main slug, "
    "residual tracer continues to diffuse out of the matrix at a lower but "
    "persistent rate, feeding a slowly decaying concentration tail governed by "
    "matrix-diffusion-controlled release into a flowing stream—mathematically, "
    "a complementary error function (erfc). These two contributions overlap in "
    "time but can be separated by expressing the BTC as the weighted sum of a "
    "Gaussian rise component and an erfc fall component, joined by a smooth "
    "hyperbolic-tangent weight function w(t) = ½[1 + tanh((t₀ − t)/σ)] that "
    "ensures C¹ continuity for gradient-based optimization. The resulting six-"
    "parameter model—baseline concentration, pulse amplitude, tail amplitude, "
    "dispersivity, flow rate, and transition center—is fitted to the observed "
    "BTC. Critically, the flow rate Q is recovered as a free parameter rather "
    "than being constrained by the pump setting, providing a built-in self-"
    "calibration check; the Peclet number Pe = x/α, computed from the fitted "
    "dispersivity, supplies an independent mechanistic diagnostic that can be "
    "cross-validated against the transport regime identified by K-P kinetics. "
    "The decomposition itself reveals the relative contribution of shut-in "
    "accumulation and sustained release to the total tracer signal, information "
    "that no single-component model can provide."
)

P6 = (
    "We validate this dual-regime model against single-phase and steady-state "
    "two-phase core displacement experiments using an oleophilic epoxy/Fe₃O₄ "
    "tracer proppant (ESP-T). The epoxy matrix was selected in preference to "
    "conventional ceramic (high-density [35,36]) and polystyrene (limited "
    "thermal stability [37,38]) carriers for its cross-linked-network-controlled "
    "release characteristics [39–41]; stearic acid surface modification of the "
    "encapsulated nano-Fe₃O₄ imparts oleophilic selectivity, enabling oil-phase "
    "tracer delivery. The model is validated through four complementary lines "
    "of evidence: statistical model selection against simpler single-component "
    "formulations, physical self-calibration of the fitted flow rate against "
    "the independently set pump rate, mechanistic consistency between the "
    "fitted Peclet number and the non-Fickian transport regime independently "
    "identified by K-P kinetics, and parametric robustness of the signal "
    "decomposition to the choice of transition width. The decomposition reveals "
    "that a substantial fraction of the integrated tracer signal originates "
    "from sustained matrix-diffusion-controlled release rather than the initial "
    "accumulation slug, establishing that a single shut-in suffices for long-"
    "term monitoring. Under steady-state two-phase flow, the oil-phase tracer "
    "mass flux eliminates water-dilution artifacts and quantitatively tracks "
    "per-interval oil production rates, providing a pathway from wellhead "
    "concentration measurements to per-stage production allocation that "
    "requires no downhole tools and only a single shut-in."
)

new_paras = [P1, P2, P3, P4, P5, P6]

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
    if stray: print(f"Removed {len(stray)} stray paragraphs")

all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        zout.writestr(name, data)

ttl = sum(len(t) for t in new_paras)
print(f"Saved: {out}")
print(f"{len(new_paras)} paragraphs, {ttl} chars total")
for i, t in enumerate(new_paras):
    print(f"  P{i+1}: {len(t)} chars")

# Verify refs
root2 = etree.fromstring(all_files['word/document.xml'])
all_p2 = root2.findall(f'.//{{{W}}}p')
ref_start = next(i for i,p in enumerate(all_p2) if pt(p).strip()=='References')
refs = []
for i, p in enumerate(all_p2):
    if i >= ref_start: break
    for m in re.finditer(r'\[([\d,\-–\s]+)\]', pt(p)):
        for part in re.split(r',', m.group(1)):
            part = part.strip()
            rm = re.match(r'(\d+)\s*[–\-]\s*(\d+)', part)
            if rm:
                for n in range(int(rm.group(1)), int(rm.group(2))+1):
                    if n not in refs: refs.append(n)
            elif part.isdigit() and int(part) not in refs:
                refs.append(int(part))
print(f'REFS: {len(refs)}, seq={all(refs[i]<=refs[i+1] for i in range(len(refs)-1))}')
if len(refs) < 41:
    print(f'Missing: {sorted(set(range(1,42))-set(refs))}')
for i in range(len(refs)-1):
    if refs[i+1] < refs[i]:
        print(f'  ORDER: [{refs[i]}] then [{refs[i+1]}]')
