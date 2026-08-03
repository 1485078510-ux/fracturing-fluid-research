# -*- coding: utf-8 -*-
"""Final rewrite: engineering-focused title, abstract, introduction."""
import sys, io, re, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from lxml import etree
from copy import deepcopy

SRC = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_3-revised_clean.docx"
OUT = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_4-intro_rewritten.docx"
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

# ===== TITLE =====
set_text(body.findall(f'.//{{{W}}}p')[0],
    "Recovering Per-Interval Flow Rates from Tracer-Proppant Breakthrough "
    "Curves by Separating Shut-In Accumulation and Sustained-Release Signals"
)

# ===== ABSTRACT =====
set_text(body.findall(f'.//{{{W}}}p')[2],
    "Tracer proppants can identify which fractured stages are producing, "
    "but existing methods cannot determine how much each stage produces from "
    "the wellhead breakthrough curve alone. Production logging and fiber-optic "
    "sensing provide quantitative flow profiles but require downhole intervention "
    "or permanent installation. Tracer mass-balance methods allocate production "
    "by recovered tracer ratios but discard the information encoded in the curve "
    "shape. All physics-based breakthrough curve interpretation methods, from "
    "analytical advection-dispersion fitting to numerical history matching, "
    "treat the tracer source as a known input, a condition that a tracer "
    "proppant, which releases tracer continuously from a polymeric matrix, does "
    "not satisfy. A recent study coupled Korsmeyer-Peppas release kinetics with "
    "the advection-dispersion equation to extract the dispersion coefficient, "
    "but the per-interval flow rate was not recovered. Here we show that a "
    "tracer-proppant breakthrough curve obtained after an extended shut-in "
    "carries the superimposed signatures of two separable processes: a Gaussian "
    "pulse produced by the advective sweep of tracer accumulated in the near-"
    "wellbore region during shut-in, and an erfc tail produced by sustained "
    "matrix-diffusion-controlled release during the production period. By "
    "expressing the breakthrough curve as the weighted sum of these two "
    "components joined by a smooth tanh transition, the six-parameter model "
    "recovers the per-interval flow rate directly from the concentration "
    "history. The fitted flow rate (0.46 mL/min) agrees with the independently "
    "set pump rate (0.50 mL/min) within 8 percent without the pump rate being "
    "used as a constraint. Additional validation includes decisive statistical "
    "preference over four single-component alternatives (Delta AICc = 32.7, "
    "p less than 10^{-6}, R-squared = 0.9939), mechanistic consistency between "
    "the fitted Peclet number (Pe = 0.934) and independently measured Korsmeyer-"
    "Peppas kinetics, parametric robustness of the 47 percent sustained-release "
    "fraction to a six-fold variation in the transition width, and quantitative "
    "tracking of oil production rates under steady-state two-phase flow (Pearson "
    "r = 0.97, RMSD = 8.3 percent). This methodology requires only wellhead "
    "sampling and a single shut-in, providing a pathway to routine per-stage "
    "production allocation without downhole tools."
)

# ===== REMOVE OLD INTRO =====
old = [i for i in range(intro_h+1, exp_h) if all_c[i].tag == f'{{{W}}}p']
for i in sorted(old, reverse=True): all_c[i].getparent().remove(all_c[i])

# ===== ADD 3 NEW REFS after [32] =====
NEW_REFS = [
    'OGATA A, BANKS R B. A solution of the differential equation of longitudinal dispersion in porous media. U.S. Geological Survey Professional Paper 411-A, 1961.',
    'JULIUSSON E, HORNE R N. Characterization of fractured reservoirs using tracer and flow-rate data. Water Resources Research, 2013, 49(5): 2327-2342.',
    'LI N, ZHENG J, CHENG Q, et al. Release kinetics of nano-Fe3O4 tracers from polymer-coated proppants in simulated reservoir environments. Colloids and Surfaces A: Physicochemical and Engineering Aspects, 2026, 707: 137892.',
]
all_c = list(body)
ref32 = next(i for i in range(ref_h+1, len(all_c)) if pt(all_c[i]).strip().startswith('[32]'))
for j, t in enumerate(NEW_REFS):
    np = mkr(33+j, t); all_c[ref32+j].addnext(np); all_c = list(body)

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

# ===== NEW INTRODUCTION (6 paragraphs) =====

P1 = (
    "Multi-stage hydraulic fracturing of horizontal wells has made unconventional "
    "reservoirs a cornerstone of global hydrocarbon supply, yet no routine method "
    "exists for determining per-stage contributions to total production in wells "
    "containing 10 to 30 individually fractured intervals [1-6]. Without per-stage "
    "production data, operators cannot identify underperforming intervals, optimize "
    "stage spacing, or validate completion designs against production outcomes "
    "[7,8]. Production logging provides accurate downhole flow profiles but "
    "requires well intervention and captures only a snapshot of well condition "
    "[9]; distributed fiber-optic sensing enables continuous monitoring but "
    "demands permanent cable installation during completion [10,11]; and "
    "microseismic monitoring characterizes fracture geometry rather than flow "
    "[12]. Tracer-based diagnostics offer an alternative that requires no "
    "downhole tools and can be deployed during completion [13,14]."
)

P2 = (
    "Chemical tracers have been used in oilfield operations since the 1950s [15], "
    "and recent multi-tracer field campaigns have demonstrated quantitative "
    "per-stage production allocation at field scale [16-20]. Among tracer-based "
    "approaches, the tracer proppant, a composite particle that immobilizes a "
    "tracer agent within a solid carrier co-injected with fracturing fluid, "
    "offers a critical operational advantage: the tracer remains in the fracture "
    "after a single placement, enabling long-term stage-specific monitoring "
    "without repeated well intervention [21]. Recent designs span ceramic, "
    "polymer-coated, and polymer-matrix carriers with diverse tracer chemistries "
    "[21-27]. Despite this diversity, all existing tracer proppant studies share "
    "a common workflow: tracer release is measured in batch experiments and "
    "fitted to the Korsmeyer-Peppas (K-P) power law [28-30]. The K-P model "
    "identifies the release mechanism, Fickian diffusion for n at most 0.43, "
    "anomalous transport for n between 0.43 and 0.85, Case-II relaxation for "
    "n at least 0.85, and provides the rate constant K. Li et al. [35] recently "
    "extended this approach by coupling K-P kinetics with the advection-"
    "dispersion equation (ADE) to extract the hydrodynamic dispersion "
    "coefficient from experimental breakthrough curves (BTCs), representing "
    "the first integration of release kinetics and transport modeling for tracer "
    "proppants. However, the dispersion coefficient was fitted as an independent "
    "parameter; the per-interval flow rate, the quantity of direct engineering "
    "interest, was not recovered. In all cases, the transport step, how the "
    "released tracer travels through the proppant pack and production tubing "
    "to the sampling point, is either absent from the analysis or treated "
    "separately from release characterization. Tracer proppants can therefore "
    "answer which stages are producing, but cannot answer how much."
)

P3 = (
    "The question of how much each stage produces has been addressed in inter-"
    "well tracer tests through several established methods, all of which share "
    "a common premise: the tracer is introduced as a controlled pulse of known "
    "mass, concentration, and duration. The simplest field approaches are time-"
    "of-arrival methods: the peak-concentration time gives a flow rate estimate "
    "under piston-like displacement, and the mean residence time computed from "
    "the first moment of the BTC offers improved robustness. Tracer mass-balance "
    "methods allocate production among stages in proportion to the recovered "
    "tracer mass from each interval; these methods are operationally "
    "straightforward but discard all information encoded in the BTC shape. "
    "Analytical ADE solutions fitted to the observed BTC recover velocity, "
    "dispersivity, and flow rate by least-squares optimization [31,33]. Shook "
    "et al. [32] advanced beyond direct fitting by applying moment analysis "
    "to extract swept volume and remaining oil saturation without numerical "
    "simulation. Deconvolution methods recover a tracer transfer function via "
    "parametric or nonparametric inversion of the convolution between injection "
    "history and observed BTC [34]. For heterogeneous reservoirs, numerical "
    "history matching iteratively adjusts the reservoir model to reproduce the "
    "observed BTC. Most recently, analytical ADE solutions have been extended "
    "to two-phase transport of partitioning tracers [36], and stream-tube "
    "decomposition has been applied to multi-stage fractured wells [37]."
)

P4 = (
    "Every method described above, from peak-time estimation through numerical "
    "history matching, treats the tracer source as a known input. A tracer "
    "proppant does not satisfy this condition. The tracer is not injected as "
    "a discrete pulse; it is released continuously from a polymeric matrix at "
    "a rate governed by matrix diffusion and polymer relaxation, the very "
    "processes characterized by K-P kinetics, and this release evolves "
    "throughout the production period. The BTC measured at the wellhead is "
    "therefore the convolution of two unknown functions: a release rate "
    "governed by matrix-diffusion kinetics, and a transport operator governed "
    "by advection and dispersion. Neither function is known independently; "
    "both must be recovered from a single concentration history. To our "
    "knowledge, no existing method recovers the per-interval flow rate from "
    "a tracer-proppant BTC without independent knowledge of the source term."
)

P5 = (
    "We resolve this problem by recognizing that a tracer-proppant BTC obtained "
    "after an extended shut-in carries the superimposed signatures of two "
    "physically distinct processes that constrain different regions of the "
    "curve. During shut-in, tracer diffuses from the proppant matrix and "
    "accumulates in the surrounding pack and near-wellbore region; when the "
    "well opens, this accumulated inventory is swept downstream as a coherent "
    "slug, producing a concentration peak whose shape is governed by advective-"
    "dispersive transport of a pre-existing spatial distribution, a Gaussian "
    "pulse. After passage of the main slug, residual tracer continues to "
    "diffuse from the matrix at a lower but persistent rate, feeding a slowly "
    "decaying tail governed by matrix-diffusion-controlled release into a "
    "flowing stream, a complementary error function (erfc). These two "
    "contributions overlap in time but constrain different regions of the "
    "BTC: the Gaussian component anchors the rising limb and peak region, "
    "determining the flow rate Q and dispersivity; the erfc component anchors "
    "the tail region, determining the sustained-release amplitude and baseline "
    "concentration; and the crossover between the two regimes determines the "
    "transition center. We accordingly decompose the BTC into the weighted sum "
    "of a Gaussian rise component and an erfc fall component, joined by a "
    "smooth tanh weight function that ensures C1 continuity for gradient-based "
    "optimization. The resulting six-parameter model, baseline concentration, "
    "pulse amplitude, tail amplitude, dispersivity, flow rate, and transition "
    "center, is fitted to the observed BTC by global optimization. The flow "
    "rate Q is recovered as a free parameter: its convergence to 0.46 mL/min "
    "against an independently set pump rate of 0.50 mL/min (8 percent error) "
    "is driven entirely by the shape of the BTC, not by the pump setting. The "
    "fitted Peclet number (Pe = 0.934) independently confirms the non-Fickian "
    "transport regime identified by K-P kinetics."
)

P6 = (
    "We validate this methodology against single-phase and steady-state two-"
    "phase core displacement experiments using an oleophilic epoxy/Fe3O4 "
    "tracer proppant (ESP-T). The epoxy matrix was selected over conventional "
    "ceramic and polystyrene carriers for its cross-linked-network-controlled "
    "release characteristics [38-44]; stearic acid modification imparts "
    "oleophilic selectivity for oil-phase tracer delivery. Four complementary "
    "lines of evidence support the model: statistical model selection decisively "
    "favors the dual-regime formulation over four single-component alternatives "
    "(Delta AICc = 32.7, p less than 10^{-6}, R-squared = 0.9939); the fitted "
    "flow rate self-calibrates against the independently set pump rate; the "
    "Peclet number is consistent with independent K-P kinetic measurements; "
    "and the signal decomposition, which attributes 47 percent of the "
    "integrated tracer signal to sustained release, is robust to a six-fold "
    "variation in the transition width. This sustained-release fraction "
    "establishes that a single shut-in suffices for long-term monitoring. "
    "Under steady-state two-phase flow, the oil-phase tracer mass flux "
    "eliminates water-dilution artifacts and tracks per-interval oil production "
    "rates (Pearson r = 0.97, RMSD = 8.3 percent), providing a pathway from "
    "wellhead concentration measurements to per-stage production allocation "
    "without downhole tools or repeated intervention."
)

PARAS = [P1, P2, P3, P4, P5, P6]

# Insert
all_c = list(body)
ih = next(i for i,c in enumerate(all_c) if c.tag==f'{{{W}}}p' and pt(c).strip()=='1. Introduction')
for j, text in enumerate(PARAS):
    np = mkp(text); all_c[ih+j].addnext(np); all_c = list(body)

# Remove strays
all_c = list(body)
nl = next(i for i,c in enumerate(all_c) if c.tag==f'{{{W}}}p' and 'without downhole tools or repeated intervention' in pt(c))
el = next(i for i,c in enumerate(all_c) if c.tag==f'{{{W}}}p' and pt(c).strip()=='2. Experimental Section')
stray = [i for i in range(nl+1, el) if all_c[i].tag == f'{{{W}}}p']
for i in reversed(stray): all_c[i].getparent().remove(all_c[i])

# Fix new ref numbers affected by renumbering
all_c = list(body)
rs = next(i for i,c in enumerate(all_c) if c.tag==f'{{{W}}}p' and pt(c).strip()=='References')
fix_kw = {'OGATA': 33, 'JULIUSSON': 34, 'LI N, ZHENG': 35}
for p in all_c[rs+1:]:
    t = pt(p).strip()
    for kw, new_num in fix_kw.items():
        if kw in t:
            m = re.match(r'\[(\d+)\]', t)
            if m and int(m.group(1)) != new_num:
                old_n = m.group(1)
                for r in p.findall(f'.//{{{W}}}r'):
                    for te in r.findall(f'.//{{{W}}}t'):
                        if te.text and te.text.startswith(f'[{old_n}]'):
                            te.text = te.text.replace(f'[{old_n}]', f'[{new_num}]', 1); break

# Save
all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for n, d in all_files.items(): zout.writestr(n, d)

# Quick verify
root2 = etree.fromstring(all_files['word/document.xml'])
all_p2 = root2.findall(f'.//{{{W}}}p')
rs = next(i for i,p in enumerate(all_p2) if pt(p).strip()=='References')
rns = []; dups = []
for i in range(rs+1, len(all_p2)):
    m = re.match(r'\[(\d+)\]', pt(all_p2[i]).strip())
    if m:
        n = int(m.group(1))
        if n in rns: dups.append(n)
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
print(f'Refs: {len(rns)}, dups={dups if dups else "NONE"}, seq={rns==list(range(1,len(rns)+1))}')
print(f'Body cited: {len(body_refs)}, missing={sorted(set(rns)-body_refs) if set(rns)-body_refs else "NONE"}')
