"""
Fresh introduction from scratch. Publication quality.
"""
import sys, io, re, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from lxml import etree
from copy import deepcopy

SRC = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_3-revised_clean.docx"
OUT = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_4-intro_rewritten.docx"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def pt(p):
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))

def mkp(text):
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

def mkr(num, text):
    p = etree.Element(f'{{{W}}}p')
    ppr = etree.SubElement(p, f'{{{W}}}pPr')
    ind = etree.SubElement(ppr, f'{{{W}}}ind')
    ind.set(f'{{{W}}}left', '420'); ind.set(f'{{{W}}}hanging', '420')
    r = etree.SubElement(p, f'{{{W}}}r')
    rpr = etree.SubElement(r, f'{{{W}}}rPr')
    etree.SubElement(rpr, f'{{{W}}}rFonts').set(f'{{{W}}}cs', 'Times New Roman')
    sz = etree.SubElement(rpr, f'{{{W}}}sz'); sz.set(f'{{{W}}}val', '18')
    t = etree.SubElement(r, f'{{{W}}}t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = f'[{num}] {text}'
    return p

# LOAD
with zipfile.ZipFile(SRC, 'r') as zin:
    all_files = {n: zin.read(n) for n in zin.namelist()}
root = etree.fromstring(all_files['word/document.xml'])
body = root.find(f'{{{W}}}body')
all_c = list(body)

intro_h = exp_h = ref_h = None
for i, c in enumerate(all_c):
    if c.tag == f'{{{W}}}p':
        t = pt(c).strip()
        if t == '1. Introduction': intro_h = i
        if t == '2. Experimental Section': exp_h = i
        if t == 'References': ref_h = i

# Remove old intro
old = [i for i in range(intro_h+1, exp_h) if all_c[i].tag == f'{{{W}}}p']
for i in sorted(old, reverse=True):
    all_c[i].getparent().remove(all_c[i])

# Add 3 new refs after [32]: [33] Ogata, [34] Juliusson, [35] Pedersen
NEW = [
    'OGATA A, BANKS R B. A solution of the differential equation of longitudinal dispersion in porous media. U.S. Geological Survey Professional Paper 411-A, 1961.',
    'JULIUSSON E, HORNE R N. Characterization of fractured reservoirs using tracer and flow-rate data. Water Resources Research, 2013, 49(5): 2327-2342.',
    'PEDERSEN J M, KLEPPE J. Evaluating simple chromatographic formulae for remaining oil saturation and EOR efficiency. Geoenergy Science and Engineering, 2025, 248: 214819.',
]
all_c = list(body)
ref32 = next(i for i in range(ref_h+1, len(all_c)) if pt(all_c[i]).strip().startswith('[32]'))
for j, t in enumerate(NEW):
    np = mkr(33+j, t)
    all_c[ref32+j].addnext(np)
    all_c = list(body)

# Renumber old [33-41] -> [36-44]
R = {old: old+3 for old in range(33, 42)}
all_c = list(body)
for i in range(ref_h+1, len(all_c)):
    p = all_c[i]; t = pt(p).strip()
    m = re.match(r'\[(\d+)\]', t)
    if m and int(m.group(1)) in R:
        o = int(m.group(1))
        for r in p.findall(f'.//{{{W}}}r'):
            for te in r.findall(f'.//{{{W}}}t'):
                if te.text and te.text.startswith(f'[{o}]'):
                    te.text = te.text.replace(f'[{o}]', f'[{R[o]}]', 1)

# Update body citations
all_c = list(body)
for i in range(0, ref_h):
    p = all_c[i]
    if p.tag != f'{{{W}}}p': continue
    for r in p.findall(f'.//{{{W}}}r'):
        for te in r.findall(f'.//{{{W}}}t'):
            if te.text is None: continue
            def reb(m):
                c = m.group(1); parts = re.split(r',', c); np = []
                for part in parts:
                    ps = part.strip()
                    rm = re.match(r'(\d+)\s*[–\-]\s*(\d+)', ps)
                    if rm:
                        a,b = int(rm.group(1)), int(rm.group(2))
                        np.append(f'{R.get(a,a)}-{R.get(b,b)}')
                    elif ps.isdigit(): np.append(str(R.get(int(ps), int(ps))))
                    else: np.append(part)
                return '[' + ','.join(np) + ']'
            te.text = re.sub(r'\[(\d+(?:[–\-]\d+)*(?:,\d+(?:[–\-]\d+)*)*)\]', reb, te.text)

# =====================================================================
# NEW INTRODUCTION (6 paragraphs)
# =====================================================================

P1 = (
    "Multi-stage hydraulic fracturing of horizontal wells has made "
    "unconventional reservoirs a cornerstone of global hydrocarbon supply "
    "[1-4]. A single well may contain 10 to 30 individually fractured stages, "
    "yet no routine method exists for determining per-stage contributions to "
    "total production [5,6]. Without per-stage allocation data, operators "
    "cannot identify underperforming intervals, optimize stage spacing, or "
    "validate completion designs against production outcomes [7,8]. Production "
    "logging requires well intervention and provides only a snapshot [9]; "
    "distributed fiber-optic sensing demands permanent cable installation "
    "[10,11]; and microseismic monitoring characterizes fracture geometry "
    "rather than flow [12]. Tracer-based diagnostics offer an alternative: "
    "they require no downhole tools, can be deployed during completion, and "
    "provide direct chemical evidence linking each labeled interval to its "
    "produced fluids [13,14]."
)

P2 = (
    "Chemical tracers have been used in oilfield operations since the 1950s "
    "[15], and recent multi-tracer field campaigns have demonstrated "
    "quantitative per-stage production allocation at field scale [16-20]. "
    "Among tracer-based approaches, the tracer proppant—a composite particle "
    "that immobilizes a tracer agent within a solid carrier and is co-injected "
    "with fracturing fluid—offers a distinct operational advantage: the tracer "
    "remains in the fracture after a single placement, enabling long-term "
    "stage-specific monitoring without repeated well intervention [21]. Recent "
    "designs span ceramic, polymer-coated, and polymer-matrix carriers with "
    "diverse tracer chemistries [21-27]. Despite this diversity, all existing "
    "tracer proppant studies share a common methodological structure: tracer "
    "release is measured in batch experiments and fitted to the Korsmeyer-"
    "Peppas (K-P) power law, C/C0 = K t^n [28-30]. The K-P model identifies "
    "the release mechanism—Fickian diffusion (n <= 0.43), anomalous transport "
    "(0.43 < n < 0.85), or Case-II relaxation (n >= 0.85)—and provides the "
    "rate constant K, but it does so in a stirred vessel with no spatial "
    "coordinate and no flow field. The transport step—advection, dispersion, "
    "and the convolution of sustained release with flow—is absent from the "
    "model. Consequently, existing tracer proppants can confirm which stages "
    "are producing but cannot translate a breakthrough curve into a "
    "production rate."
)

P3 = (
    "The interpretation of tracer breakthrough curves (BTCs) has been studied "
    "extensively in inter-well tracer tests, where the tracer is introduced "
    "as a controlled pulse of known mass, concentration, and duration. The "
    "simplest approaches used in field practice are time-of-arrival (TOA) "
    "methods: the peak-concentration time yields an estimate of the inter-well "
    "flow rate under the assumption of piston-like displacement, the mean "
    "residence time computed from the first moment of the BTC provides a more "
    "robust alternative, and the half-peak time offers a rapid field "
    "approximation. Recent work has systematically evaluated the conditions "
    "under which each TOA method is valid [35]. Tracer mass-balance methods "
    "allocate production among stages in proportion to the recovered tracer "
    "mass but discard all information encoded in the BTC shape. All such "
    "single-metric approaches share a fundamental limitation: they cannot "
    "decompose the BTC into physically distinct contributions, nor can they "
    "recover a flow rate without independent knowledge of the source term. "
    "The classical alternative fits an analytical solution of the one-"
    "dimensional advection-dispersion equation (ADE) to the observed BTC "
    "to recover transport parameters—velocity, dispersivity, and flow rate—"
    "by least-squares optimization [31,33]. Shook et al. [32] advanced "
    "beyond direct fitting by applying residence-time-distribution moment "
    "analysis, which extracts swept volume, sweep efficiency, and remaining "
    "oil saturation without numerical simulation. Fontalvo et al. [16] "
    "demonstrated that model selection is operationally consequential: an "
    "inappropriate transport model can systematically overestimate or "
    "underestimate remaining oil saturation. Deconvolution methods recover "
    "a tracer transfer function via parametric or nonparametric inversion "
    "of the convolution between injection history and observed BTC [34]. "
    "For heterogeneous reservoirs, numerical history matching iteratively "
    "adjusts the reservoir model to reproduce the observed BTC, often "
    "accelerated by streamline-based sensitivity computations; most recently, "
    "analytical ADE solutions have been extended to two-phase transport of "
    "partitioning tracers [36], and stream-tube decomposition has enabled "
    "per-stage parameter estimation in multi-stage fractured wells [37]."
)

P4 = (
    "A single structural premise runs through every BTC interpretation method "
    "described above: the tracer source is treated as a known input—a Dirac "
    "pulse, a finite-duration injection, or a continuous source of prescribed "
    "strength. The inverse problem is to estimate transport parameters given "
    "that known source. A tracer proppant does not satisfy this premise. The "
    "tracer is not injected as a discrete event; it is released continuously "
    "from a polymeric matrix at a rate governed by matrix diffusion and "
    "polymer relaxation—the very processes characterized by K-P kinetics—and "
    "this release evolves throughout the production period. The BTC measured "
    "at the wellhead is therefore the convolution of two unknown functions: "
    "a release rate governed by matrix-diffusion kinetics, and a transport "
    "operator governed by advection and dispersion in the production tubing. "
    "Neither function is known independently; both must be recovered from a "
    "single concentration history. To our knowledge, this coupled release-"
    "transport inverse problem has not been addressed in the literature. Its "
    "practical consequence is that tracer proppants, despite their operational "
    "advantages, remain qualitative tools: they can confirm which stages "
    "produce but cannot deliver a production rate."
)

P5 = (
    "We resolve this coupled problem by recognizing that a tracer proppant "
    "BTC obtained after an extended shut-in carries the superimposed "
    "signatures of two physically distinct processes. During shut-in, tracer "
    "diffuses from the proppant matrix and accumulates in the surrounding "
    "pack and near-wellbore region; when the well opens, this accumulated "
    "inventory is swept downstream as a coherent slug, producing a "
    "concentration peak governed by the advective-dispersive transport of "
    "a pre-existing spatial distribution—a Gaussian pulse. After passage of "
    "the main slug, residual tracer continues to diffuse from the matrix at "
    "a lower but persistent rate, feeding a slowly decaying tail governed "
    "by matrix-diffusion-controlled release into a flowing stream—a "
    "complementary error function (erfc). These two contributions overlap "
    "in time but can be separated by expressing the BTC as the weighted sum "
    "of a Gaussian rise component and an erfc fall component, joined by a "
    "smooth hyperbolic-tangent weight function that ensures C1 continuity "
    "for gradient-based optimization. The resulting six-parameter model—"
    "baseline concentration, pulse amplitude, tail amplitude, dispersivity, "
    "flow rate, and transition center—is fitted to the observed BTC. "
    "Critically, the flow rate Q is recovered as a free parameter: it is "
    "not constrained by the pump setting, providing a built-in self-"
    "calibration check. The Peclet number, computed from the fitted "
    "dispersivity, offers an independent diagnostic that can be cross-"
    "validated against the transport regime identified by K-P kinetics. "
    "The decomposition itself quantifies the relative contribution of "
    "shut-in accumulation and sustained release to the total tracer "
    "signal—information no single-component model can provide."
)

P6 = (
    "We validate this dual-regime model against single-phase and steady-state "
    "two-phase core displacement experiments using an oleophilic epoxy/Fe3O4 "
    "tracer proppant (ESP-T). The epoxy matrix was selected over conventional "
    "ceramic and polystyrene carriers for its cross-linked-network-controlled "
    "release characteristics [38-44]; stearic acid modification of the "
    "encapsulated nano-Fe3O4 imparts oleophilic selectivity for oil-phase "
    "tracer delivery. The model is validated through four complementary "
    "lines of evidence: statistical model selection against simpler single-"
    "component formulations, physical self-calibration of the fitted flow "
    "rate against the independently set pump rate, mechanistic consistency "
    "between the Peclet number and independent K-P kinetic measurements, "
    "and parametric robustness of the signal decomposition across a six-"
    "fold variation in the transition width. The decomposition reveals that "
    "a substantial fraction of the integrated signal originates from "
    "sustained release rather than the initial accumulation slug, "
    "establishing that a single shut-in suffices for long-term monitoring. "
    "Under steady-state two-phase flow, the oil-phase tracer mass flux "
    "eliminates water-dilution artifacts and tracks per-interval oil "
    "production rates, providing a pathway from wellhead concentration "
    "measurements to per-stage production allocation without downhole "
    "tools or repeated intervention."
)

PARAS = [P1, P2, P3, P4, P5, P6]

# Insert
all_c = list(body)
ih = next(i for i,c in enumerate(all_c) if c.tag==f'{{{W}}}p' and pt(c).strip()=='1. Introduction')
for j, text in enumerate(PARAS):
    np = mkp(text)
    all_c[ih+j].addnext(np)
    all_c = list(body)

# Remove strays
all_c = list(body)
nl = next(i for i,c in enumerate(all_c) if c.tag==f'{{{W}}}p' and 'without downhole tools or repeated intervention' in pt(c))
el = next(i for i,c in enumerate(all_c) if c.tag==f'{{{W}}}p' and pt(c).strip()=='2. Experimental Section')
stray = [i for i in range(nl+1, el) if all_c[i].tag == f'{{{W}}}p']
for i in reversed(stray): all_c[i].getparent().remove(all_c[i])

# Save
all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for n, d in all_files.items(): zout.writestr(n, d)

# Verify
root2 = etree.fromstring(all_files['word/document.xml'])
all_p2 = root2.findall(f'.//{{{W}}}p')
rs = next(i for i,p in enumerate(all_p2) if pt(p).strip()=='References')

rns = []
for i in range(rs+1, len(all_p2)):
    m = re.match(r'\[(\d+)\]', pt(all_p2[i]).strip())
    if m:
        n = int(m.group(1))
        if n in rns: print(f'DUP: [{n}]')
        rns.append(n)

body_refs = set()
for i, p in enumerate(all_p2):
    if i >= rs: break
    if p.tag != f'{{{W}}}p': continue
    for m in re.finditer(r'\[(\d+(?:[–\-]\d+)*(?:,\d+(?:[–\-]\d+)*)*)\]', pt(p)):
        for part in re.split(r',', m.group(1)):
            part = part.strip()
            rm = re.match(r'(\d+)\s*[–\-]\s*(\d+)', part)
            if rm:
                for n in range(int(rm.group(1)), int(rm.group(2))+1): body_refs.add(n)
            elif part.isdigit(): body_refs.add(int(part))

missing = sorted(set(rns) - body_refs)
ttl = sum(len(pt(p)) for p in all_p2[:rs] if p.tag==f'{{{W}}}p' and pt(p).strip() and pt(p).strip()!='1. Introduction')

print(f'Refs: {len(rns)} total, seq={rns==list(range(1,len(rns)+1))}')
print(f'Body cited: {len(body_refs)}, missing={missing if missing else "NONE"}')
print(f'Intro: {len(PARAS)} paragraphs, {ttl} chars')
