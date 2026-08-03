# -*- coding: utf-8 -*-
import sys, io, re, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from lxml import etree
from copy import deepcopy

DOC = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_4-intro_rewritten.docx"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def pt(p):
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))

def set_text(p, text):
    first_r = p.find(f'.//{{{W}}}r')
    ref_rpr = first_r.find(f'{{{W}}}rPr') if first_r is not None else None
    for child in list(p):
        if child.tag.split('}')[-1] != 'pPr': p.remove(child)
    r = etree.SubElement(p, f'{{{W}}}r')
    if ref_rpr is not None: r.append(deepcopy(ref_rpr))
    else:
        rpr = etree.SubElement(r, f'{{{W}}}rPr')
        etree.SubElement(rpr, f'{{{W}}}rFonts').set(f'{{{W}}}cs', 'Times New Roman')
    t = etree.SubElement(r, f'{{{W}}}t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text

with zipfile.ZipFile(DOC, 'r') as zin:
    all_files = {n: zin.read(n) for n in zin.namelist()}
root = etree.fromstring(all_files['word/document.xml'])
body = root.find(f'{{{W}}}body')
all_p = body.findall(f'.//{{{W}}}p')
rs = next(i for i, p in enumerate(all_p) if pt(p).strip() == 'References')

# ===== P1 =====
P1 = (
    "Multi-stage hydraulic fracturing has made unconventional reservoirs a "
    "cornerstone of global hydrocarbon supply, yet no routine method exists "
    "for determining per-stage contributions to total production in wells "
    "containing 10 to 30 individually fractured intervals [1-6]. Without "
    "per-stage production data, underperforming intervals go undiagnosed "
    "and completion designs remain unvalidated [7,8]. Production logging "
    "requires well intervention and captures only a snapshot [9]; fiber-optic "
    "sensing demands permanent downhole cable installation [10,11]; and "
    "microseismic imaging reveals fracture geometry rather than flow [12]. "
    "Tracer-based diagnostics avoid these limitations: they require no "
    "downhole tools, can be deployed during completion, and provide direct "
    "chemical evidence linking each labeled interval to its produced fluids "
    "[13,14]."
)

# ===== P2 =====
P2 = (
    "Chemical tracers have been used in oilfield operations since the 1950s "
    "[15], and recent multi-tracer field campaigns have demonstrated "
    "quantitative per-stage production allocation at field scale [16-20]. "
    "Among tracer-based approaches, the tracer proppant—a composite particle "
    "that immobilizes a tracer agent within a solid carrier co-injected with "
    "fracturing fluid—offers a critical operational advantage: the tracer "
    "remains in the fracture after a single placement, enabling long-term "
    "monitoring without repeated well intervention [21]. Recent designs span "
    "ceramic, polymer-coated, and polymer-matrix carriers with diverse tracer "
    "chemistries [21-27]. Despite this diversity, all existing tracer proppant "
    "studies share an identical workflow: tracer release is measured in batch "
    "experiments and fitted to the Korsmeyer-Peppas (K-P) power law, "
    "C/C0 = K t^n [28-30]. The K-P model identifies the release mechanism—"
    "Fickian diffusion (n <= 0.43), anomalous transport (0.43 < n < 0.85), "
    "or Case-II relaxation (n >= 0.85)—and provides the rate constant K, "
    "but it does so in a stirred vessel with no flow field. The transport "
    "step—how the released tracer travels through the proppant pack and "
    "production tubing to the sampling point—is not modeled. Consequently, "
    "existing tracer proppants can confirm which stages produce but cannot "
    "translate a breakthrough curve into a production rate."
)

# ===== P3: TOA-focused methods review =====
P3 = (
    "The interpretation of tracer breakthrough curves (BTCs) has been studied "
    "extensively in inter-well tracer tests, where the tracer is injected as "
    "a controlled pulse of known mass and duration. The simplest methods used "
    "in field practice are time-of-arrival (TOA) approaches, which estimate "
    "the inter-well flow rate from a single characteristic time extracted "
    "from the BTC. The peak-concentration time gives Q = x pi d^2 / (4 t_peak) "
    "under the assumption of piston-like displacement; the mean residence "
    "time, computed as the first moment of the BTC, MRT = integral t C dt / "
    "integral C dt, provides a more robust estimate because it uses the "
    "entire curve rather than a single point; and the half-peak time offers "
    "a rapid field approximation. Recent work has systematically evaluated "
    "the conditions under which each TOA method is applicable, showing that "
    "peak-time methods require high Peclet numbers (Pe > 100) for accuracy "
    "while MRT methods perform better when the full BTC is captured [39]. "
    "Tracer mass-balance methods allocate production among stages in "
    "proportion to the total recovered tracer mass from each interval, "
    "but these methods use only the integral of the BTC and discard all "
    "information encoded in the curve shape. All TOA and mass-balance "
    "approaches share a fundamental limitation: they reduce the BTC to one "
    "or two scalars and cannot decompose the signal into physically distinct "
    "contributions, nor can they recover a flow rate without independent "
    "knowledge of the source term."
)

# ===== P4: Physics-based methods =====
P4 = (
    "The classical physics-based approach fits an analytical solution of the "
    "one-dimensional advection-dispersion equation (ADE) to the observed BTC. "
    "Van Genuchten and Alves [31] compiled solutions for a comprehensive range "
    "of initial and boundary conditions; the Ogata-Banks solution [33] "
    "expresses concentration via the complementary error function for "
    "continuous injection and as a Gaussian pulse for slug injection. Fitting "
    "such a solution recovers the transport parameters—velocity, dispersivity, "
    "and flow rate—by least-squares optimization. Shook et al. [32] advanced "
    "beyond direct fitting by applying residence-time-distribution moment "
    "analysis, extracting swept volume, sweep efficiency, and remaining oil "
    "saturation without numerical simulation. Fontalvo et al. [16] "
    "demonstrated that model selection carries direct operational consequences: "
    "an inappropriate transport model can systematically overestimate or "
    "underestimate remaining oil saturation. Deconvolution-based methods "
    "express the BTC as the convolution of the injection history with a "
    "tracer transfer function and recover the kernel via parametric or "
    "nonparametric inversion [34]; expressing the convolution in terms of "
    "cumulative flow rather than clock time makes these methods robust to "
    "variable production rates. For heterogeneous and fractured reservoirs, "
    "numerical history matching adjusts the reservoir model iteratively to "
    "reproduce the observed BTC, often accelerated by streamline-based "
    "sensitivity computations [38]. Most recently, analytical ADE solutions "
    "have been extended to two-phase flow of partitioning tracers [40], and "
    "stream-tube decomposition has enabled per-stage parameter estimation "
    "in multi-stage fractured wells [41]."
)

# ===== P5: The gap =====
P5 = (
    "A single structural premise runs through every method described above, "
    "from peak-time estimation through numerical history matching: the tracer "
    "source is treated as a known input—a Dirac pulse, a finite-duration "
    "injection, or a continuous source of prescribed strength. The inverse "
    "problem is to estimate transport parameters given that known source. "
    "A tracer proppant does not satisfy this premise. The tracer is not "
    "injected as a discrete event; it is released continuously from a "
    "polymeric matrix at a rate governed by matrix diffusion and polymer "
    "relaxation—the very processes characterized by K-P kinetics—and this "
    "release evolves throughout the production period. The BTC measured at "
    "the wellhead is therefore the convolution of two unknown functions: "
    "a release rate governed by matrix-diffusion kinetics, and a transport "
    "operator governed by advection and dispersion in the production tubing. "
    "Neither function is known independently, and both must be recovered "
    "from a single concentration history. To our knowledge, this coupled "
    "release-transport inverse problem has not been addressed in the "
    "literature. Its practical consequence is that tracer proppants, despite "
    "their operational advantages, remain qualitative tools: they can confirm "
    "stage activity but cannot deliver a production rate."
)

# ===== P6: Our approach =====
P6 = (
    "We resolve this coupled problem by recognizing that a tracer proppant "
    "BTC obtained after an extended shut-in carries the superimposed "
    "signatures of two distinct processes. During shut-in, tracer diffuses "
    "from the proppant matrix and accumulates in the surrounding pack and "
    "near-wellbore region; when the well opens, this accumulated inventory "
    "is swept downstream as a coherent slug, producing a concentration peak "
    "governed by advective-dispersive transport of a pre-existing spatial "
    "distribution—a Gaussian pulse. After passage of the main slug, residual "
    "tracer continues to diffuse from the matrix at a lower but persistent "
    "rate, feeding a slowly decaying tail governed by matrix-diffusion-"
    "controlled release into a flowing stream—a complementary error function "
    "(erfc). These two contributions overlap in time but can be separated "
    "by expressing the BTC as the weighted sum of a Gaussian rise component "
    "and an erfc fall component, joined by a smooth tanh weight function "
    "that ensures continuity for gradient-based optimization. The resulting "
    "six-parameter model—baseline concentration, pulse amplitude, tail "
    "amplitude, dispersivity, flow rate, and transition center—is fitted to "
    "the observed BTC. Critically, the flow rate Q is recovered as a free "
    "parameter: it is not constrained by the pump setting, providing a "
    "built-in self-calibration check. The Peclet number, computed from the "
    "fitted dispersivity, supplies an independent diagnostic that can be "
    "cross-validated against the transport regime identified by K-P kinetics. "
    "The decomposition itself quantifies the relative contribution of shut-in "
    "accumulation and sustained release to the total tracer signal—information "
    "no single-component model can provide."
)

# ===== P7: Validation =====
P7 = (
    "We validate this dual-regime model against single-phase and steady-state "
    "two-phase core displacement experiments using an oleophilic epoxy/Fe3O4 "
    "tracer proppant (ESP-T). The epoxy matrix was selected over conventional "
    "ceramic and polystyrene carriers for its cross-linked-network-controlled "
    "release characteristics [42-48]; stearic acid modification of the "
    "encapsulated nano-Fe3O4 imparts oleophilic selectivity for oil-phase "
    "tracer delivery. The model is validated through four complementary lines "
    "of evidence: statistical model selection against simpler single-component "
    "formulations, physical self-calibration of the fitted flow rate against "
    "the pump setting, mechanistic consistency between the Peclet number and "
    "independently measured K-P kinetics, and parametric robustness of the "
    "signal decomposition. The decomposition reveals that a substantial "
    "fraction of the integrated signal originates from sustained release "
    "rather than the initial accumulation slug, establishing that a single "
    "shut-in suffices for long-term monitoring. Under steady-state two-phase "
    "flow, the oil-phase tracer mass flux eliminates water-dilution artifacts "
    "and tracks per-interval oil production rates, providing a pathway from "
    "wellhead measurements to per-stage allocation without downhole tools "
    "or repeated intervention."
)

PARAS = [P1, P2, P3, P4, P5, P6, P7]

# Apply: match by keyword in current text
keywords = [
    "Multi-stage hydraulic fracturing has made unconventional reservoirs a cornerstone",
    "Chemical tracers have been deployed in oilfield operations since the 1950s [15], progr",
    "The interpretation of tracer breakthrough curves (BTCs) has been studied extensively in inter-well tracer tests, where t",
    "For fractured and heterogeneous media, where classical ADE solutions fail to capture ",
    "A single structural premise runs through every method described above, from peak-time ",
    "We resolve this coupled inverse problem by exploiting a feature of the measurement geo",
    "We validate this dual-regime model against single-phase and steady-state two-phase cor",
]

for p in all_p[:rs]:
    t = pt(p).strip()
    for kw, new_text in zip(keywords, PARAS):
        if kw in t:
            set_text(p, new_text)
            print(f"OK: {len(new_text)}c")
            break

# Remove strays
all_p = body.findall(f'.//{{{W}}}p')
nl = None
for i, p in enumerate(all_p[:rs]):
    if p.tag == f'{{{W}}}p' and 'without downhole tools or repeated intervention' in pt(p):
        nl = i
el = next(i for i, p in enumerate(all_p) if pt(p).strip() == '2. Experimental Section')
if nl:
    stray = [i for i in range(nl + 1, el) if all_p[i].tag == f'{{{W}}}p']
    for i in reversed(stray): all_p[i].getparent().remove(all_p[i])
    if stray: print(f"Removed {len(stray)} stray")

# Save
all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(DOC, 'w', zipfile.ZIP_DEFLATED) as zout:
    for n, d in all_files.items(): zout.writestr(n, d)

# Verify
root2 = etree.fromstring(all_files['word/document.xml'])
all_p2 = root2.findall(f'.//{{{W}}}p')
rs2 = next(i for i, p in enumerate(all_p2) if pt(p).strip() == 'References')
body_refs = set()
for i, p in enumerate(all_p2):
    if i >= rs2: break
    if p.tag != f'{{{W}}}p': continue
    for m in re.finditer(r'\[(\d+(?:[–\-]\d+)*(?:,\d+(?:[–\-]\d+)*)*)\]', pt(p)):
        for part in re.split(r',', m.group(1)):
            part = part.strip()
            rm = re.match(r'(\d+)\s*[–\-]\s*(\d+)', part)
            if rm:
                for n in range(int(rm.group(1)), int(rm.group(2))+1): body_refs.add(n)
            elif part.isdigit(): body_refs.add(int(part))
rns = [int(re.match(r'\[(\d+)\]', pt(p)).group(1)) for p in all_p2[rs2+1:] if pt(p).strip() and re.match(r'\[(\d+)\]', pt(p).strip())]
missing = sorted(set(rns) - body_refs)
print(f"Body refs: {len(body_refs)}, missing={missing if missing else 'NONE'}")
ttl = sum(len(pt(p)) for p in all_p2[:rs2] if p.tag == f'{{{W}}}p' and pt(p).strip() and pt(p).strip() != '1. Introduction')
print(f"Intro: 7 paragraphs, {ttl} chars")
