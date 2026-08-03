"""
One-pass rebuild: new intro + 5 new refs + correct numbering.
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

def make_ref_para(num, text):
    p = etree.Element(f'{{{W}}}p')
    ppr = etree.SubElement(p, f'{{{W}}}pPr')
    ind = etree.SubElement(ppr, f'{{{W}}}ind')
    ind.set(f'{{{W}}}left', '420')
    ind.set(f'{{{W}}}hanging', '420')
    r = etree.SubElement(p, f'{{{W}}}r')
    rpr = etree.SubElement(r, f'{{{W}}}rPr')
    etree.SubElement(rpr, f'{{{W}}}rFonts').set(f'{{{W}}}cs', 'Times New Roman')
    sz = etree.SubElement(rpr, f'{{{W}}}sz')
    sz.set(f'{{{W}}}val', '18')
    t = etree.SubElement(r, f'{{{W}}}t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = f'[{num}] {text}'
    return p

# ================================================================
# LOAD
# ================================================================
with zipfile.ZipFile(src, 'r') as zin:
    all_files = {n: zin.read(n) for n in zin.namelist()}
root = etree.fromstring(all_files['word/document.xml'])
body = root.find(f'{{{W}}}body')
all_c = list(body)

# Find intro & refs boundaries
intro_h = exp_h = ref_h = None
for i, c in enumerate(all_c):
    if c.tag == f'{{{W}}}p':
        t = pt(c).strip()
        if t == '1. Introduction': intro_h = i
        if t == '2. Experimental Section': exp_h = i
        if t == 'References': ref_h = i

# ================================================================
# REMOVE OLD INTRO
# ================================================================
old = [i for i in range(intro_h+1, exp_h) if all_c[i].tag == f'{{{W}}}p']
for i in sorted(old, reverse=True):
    all_c[i].getparent().remove(all_c[i])

# ================================================================
# ADD 5 NEW REFERENCES after [32]
# The old [33-41] become [38-46]
# New refs: [33] Ogata, [34] Juliusson, [35] van Genuchten-W, [36] Haggerty, [37] Berkowitz
# ================================================================
new_ref_texts = [
    'OGATA A, BANKS R B. A solution of the differential equation of longitudinal dispersion in porous media. U.S. Geological Survey Professional Paper 411-A, 1961. https://doi.org/10.3133/pp411A',
    'JULIUSSON E, HORNE R N. Characterization of fractured reservoirs using tracer and flow-rate data. Water Resources Research, 2013, 49(5): 2327-2342. https://doi.org/10.1002/wrcr.20220',
    'VAN GENUCHTEN M T, WIERENGA P J. Mass transfer studies in sorbing porous media I. Analytical solutions. Soil Science Society of America Journal, 1976, 40(4): 473-480. https://doi.org/10.2136/sssaj1976.03615995004000040011x',
    'HAGGERTY R, GORELICK S M. Multiple-rate mass transfer for modeling diffusion and surface reactions in media with pore-scale heterogeneity. Water Resources Research, 1995, 31(10): 2383-2400. https://doi.org/10.1029/95WR10583',
    'BERKOWITZ B, CORTIS A, DENTZ M, et al. Modeling non-Fickian transport in geological formations as a continuous time random walk. Reviews of Geophysics, 2006, 44(2): RG2003. https://doi.org/10.1029/2005RG000178',
]

# Find [32] in ref list
all_c = list(body)
ref32_idx = None
for i in range(ref_h + 1, len(all_c)):
    t = pt(all_c[i]).strip()
    if t.startswith('[32]'):
        ref32_idx = i
        break

# Insert new refs after [32]
for j, ref_text in enumerate(new_ref_texts):
    new_p = make_ref_para(33 + j, ref_text)
    all_c[ref32_idx + j].addnext(new_p)
    all_c = list(body)

# Renumber old [33-41] -> [38-46]
renum = {old: old + 5 for old in range(33, 42)}
all_c = list(body)
for i in range(ref_h + 1, len(all_c)):
    p = all_c[i]
    t = pt(p).strip()
    m = re.match(r'\[(\d+)\]', t)
    if m:
        old = int(m.group(1))
        if old in renum:
            for r in p.findall(f'.//{{{W}}}r'):
                for te in r.findall(f'.//{{{W}}}t'):
                    if te.text and te.text.startswith(f'[{old}]'):
                        te.text = te.text.replace(f'[{old}]', f'[{renum[old]}]', 1)

# Update ALL body text citations (old [33-41] -> [38-46])
all_c = list(body)
for i in range(0, ref_h):
    p = all_c[i]
    if p.tag != f'{{{W}}}p': continue

    for r in p.findall(f'.//{{{W}}}r'):
        for te in r.findall(f'.//{{{W}}}t'):
            if te.text is None: continue

            def reb(m):
                c = m.group(1)
                parts = re.split(r',', c)
                np = []
                for part in parts:
                    ps = part.strip()
                    rm = re.match(r'(\d+)\s*[–\-]\s*(\d+)', ps)
                    if rm:
                        a, b = int(rm.group(1)), int(rm.group(2))
                        an = renum.get(a, a)
                        bn = renum.get(b, b)
                        np.append(f'{an}-{bn}')
                    elif ps.isdigit():
                        n = int(ps)
                        np.append(str(renum.get(n, n)))
                    else:
                        np.append(part)
                return '[' + ','.join(np) + ']'

            te.text = re.sub(
                r'\[(\d+(?:[–\-]\d+)*(?:,\d+(?:[–\-]\d+)*)*)\]',
                reb, te.text
            )

# ================================================================
# NEW INTRODUCTION (uses [33-37] for new refs, [38-46] for old refs)
# ================================================================
P1 = (
    "Multi-stage hydraulic fracturing of horizontal wells has made unconventional "
    "reservoirs a cornerstone of global hydrocarbon supply [1–4]. A single well "
    "may contain 10 to 30 individually fractured stages, yet no routine method "
    "exists for determining how much each stage contributes to total production "
    "[5,6]; without such data, underperforming intervals go undiagnosed and "
    "completion designs remain unvalidated [7,8]. Production logging requires "
    "well intervention and captures only a snapshot [9]; fiber-optic sensing "
    "demands permanent downhole cable installation [10,11]; and microseismic "
    "monitoring images fracture geometry rather than flow contribution [12]. "
    "Tracer-based diagnostics circumvent these limitations: they require no "
    "downhole tools, can be deployed during completion, and provide direct "
    "chemical evidence linking each labeled interval to its produced fluids [13,14]."
)

P2 = (
    "Chemical tracers have been deployed in oilfield operations since the 1950s "
    "[15], progressing from radioactive inter-well waterflood monitors to "
    "contemporary partitioning inter-well tracer tests for residual oil "
    "measurement [16,17]. Recent multi-tracer field campaigns have demonstrated "
    "quantitative per-stage production allocation at field scale [18–20], "
    "confirming that tracer-based diagnostics are technically viable. Among "
    "tracer-based approaches, the tracer proppant—a composite particle in which "
    "a chemical tracer is immobilized within a solid carrier and co-injected "
    "with fracturing fluid—offers a critical operational advantage over dissolved "
    "tracers. Because the particle remains in the fracture after placement, a "
    "single deployment enables long-term, stage-specific monitoring without "
    "repeated well intervention [21]. Recent designs span ceramic carriers with "
    "organic-dye or quantum-dot tracers [21,22], rare-earth-doped polymer coatings "
    "for multi-element coding [23], oleophilic Fe₃O₄/polystyrene microspheres "
    "[24], dual-zone tracer-coded proppants [25], multi-colored dye-tracer "
    "proppants [26], and marked proppant transport tracers [27]. Despite this "
    "diversity of carrier materials and tracer chemistries, all of these studies "
    "share an identical methodological structure: tracer release is measured in "
    "batch experiments and fitted to the Korsmeyer-Peppas (K-P) power law, "
    "C/C₀ = K·tⁿ [28–30]. The K-P model classifies the release mechanism—Fickian "
    "diffusion for n ≤ 0.43, anomalous transport for 0.43 < n < 0.85, or Case-II "
    "relaxation for n ≥ 0.85—and yields the temperature-dependent rate constant "
    "K. This information characterizes release in a well-mixed vessel, but it "
    "provides no connection to the concentration that will be observed at a "
    "wellhead sampling point after the released tracer has traversed the proppant "
    "pack and production tubing. The transport step—advection, dispersion, and "
    "the convolution of sustained release with flow—is absent from the model. "
    "Consequently, existing tracer proppants can confirm which stages are "
    "producing, but they cannot translate a breakthrough curve into a "
    "production rate."
)

P3 = (
    "The interpretation of tracer breakthrough curves (BTCs) has been studied "
    "extensively in the context of inter-well tracer tests, where the tracer "
    "source—an injection of known mass, concentration, and duration—is a "
    "controlled experimental input. The classical approach fits an analytical "
    "solution of the one-dimensional advection-dispersion equation (ADE), "
    "∂C/∂t + v·∂C/∂x = D·∂²C/∂x², to the observed BTC [33] to recover the "
    "transport parameters: velocity v, dispersivity α, and volumetric flow rate "
    "Q. Van Genuchten and Alves [31] compiled analytical solutions for a "
    "comprehensive range of initial and boundary conditions, and these remain "
    "the standard reference. Shook et al. [32] advanced beyond direct curve "
    "fitting by applying residence-time-distribution moment analysis to tracer "
    "BTCs; their method extracts swept volume, sweep efficiency, and remaining "
    "oil saturation without requiring a numerical reservoir simulator. Fontalvo "
    "et al. [16] subsequently demonstrated that physically justified model "
    "selection carries direct operational consequences: applying an inappropriate "
    "transport model to partitioning tracer data can systematically overestimate "
    "or underestimate remaining oil saturation. In parallel, deconvolution-based "
    "methods express the BTC as the convolution of the injection history with a "
    "tracer transfer function and recover the kernel via parametric or "
    "nonparametric inversion [34], an approach made robust to variable flow "
    "rates by expressing the convolution in terms of cumulative flow rather "
    "than clock time."
)

P4 = (
    "For fractured and heterogeneous media, where classical ADE solutions fail "
    "to capture the characteristic early breakthrough and prolonged late-time "
    "tailing, a family of non-Fickian transport models has been developed. "
    "Dual-porosity mobile-immobile formulations partition the flow domain into "
    "a mobile region (fractures) and an immobile region (matrix), with first-"
    "order mass transfer between the two domains [35] and multirate extensions "
    "that treat the mass-transfer coefficient as a statistical distribution "
    "reflecting the spatial variability of matrix block sizes and diffusion "
    "path lengths [36]. The continuous-time random walk (CTRW) framework "
    "provides a more general stochastic description in which solute transport "
    "is modeled as a sequence of discrete transitions with a heavy-tailed "
    "waiting-time distribution, parameterized by an exponent that quantifies "
    "the degree of non-Fickian behavior [37]. At the highest level of "
    "complexity, full-physics numerical inversion treats the reservoir model "
    "as the unknown and adjusts it iteratively to match the observed BTC "
    "through history matching, often accelerated by streamline-based "
    "sensitivity computations. Most recently, analytical ADE solutions have "
    "been extended to two-phase, advection-dominated transport of partitioning "
    "tracers [38], and stream-tube decomposition has been applied to multi-"
    "stage fractured wells with explicit tracer partitioning between oil and "
    "water phases, achieving the computational efficiency necessary for per-"
    "stage parameter estimation [39]."
)

P5 = (
    "A single structural premise runs through every method described above, "
    "from Ogata-Banks through CTRW to full numerical inversion: the tracer "
    "source is treated as a known input. Whether a Dirac delta pulse, a finite-"
    "duration injection of measured concentration, or a continuous source of "
    "prescribed strength, the source function is an experimental boundary "
    "condition, and the inverse problem is to estimate transport parameters "
    "given that known source. A tracer proppant does not satisfy this premise. "
    "The tracer is not injected as a discrete event; it is released continuously "
    "from a polymeric matrix at a rate governed by matrix diffusion and polymer "
    "relaxation—the very processes characterized by K-P kinetics—and this "
    "release evolves throughout the production period. The BTC measured at the "
    "wellhead is therefore the convolution of two unknown functions: a release "
    "rate governed by matrix-diffusion kinetics and a transport operator "
    "governed by advection and dispersion. Neither function is known "
    "independently, and both must be recovered from the shape of a single "
    "concentration history. To our knowledge, this coupled release-transport "
    "inverse problem has not been addressed in the literature. Its practical "
    "consequence is that tracer proppants, despite their operational advantages, "
    "remain qualitative tools that can confirm stage activity but cannot "
    "quantify it."
)

P6 = (
    "We resolve this coupled inverse problem by exploiting a feature of the "
    "measurement geometry that has not been utilized in previous BTC "
    "interpretation methods. A tracer proppant BTC obtained after an extended "
    "shut-in carries the superimposed signatures of two physically distinct "
    "processes. During the shut-in period, tracer continuously diffuses out of "
    "the proppant matrix and accumulates in the surrounding pack and near-"
    "wellbore region; when the well opens, this accumulated inventory is swept "
    "toward the sampling point as a coherent slug, producing a concentration "
    "peak governed by the advective-dispersive transport of a pre-existing "
    "spatial distribution—mathematically, a Gaussian. After passage of the main "
    "slug, residual tracer continues to diffuse out of the matrix at a lower "
    "but persistent rate, feeding a slowly decaying concentration tail governed "
    "by matrix-diffusion-controlled release into a flowing stream—mathematically, "
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

P7 = (
    "We validate this dual-regime model against single-phase and steady-state "
    "two-phase core displacement experiments using an oleophilic epoxy/Fe₃O₄ "
    "tracer proppant (ESP-T). The epoxy matrix was selected in preference to "
    "conventional ceramic (high-density [40,41]) and polystyrene (limited "
    "thermal stability [42,43]) carriers for its cross-linked-network-controlled "
    "release characteristics [44–46]; stearic acid surface modification of the "
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

new_paras = [P1, P2, P3, P4, P5, P6, P7]

# ================================================================
# INSERT NEW INTRO
# ================================================================
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

# ================================================================
# SAVE
# ================================================================
all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
    for n, d in all_files.items(): zout.writestr(n, d)

print(f"Saved: {out}")
print(f"Intro: {len(new_paras)} paragraphs, {sum(len(t) for t in new_paras)} chars")

# ================================================================
# VERIFY
# ================================================================
root2 = etree.fromstring(all_files['word/document.xml'])
all_p2 = root2.findall(f'.//{{{W}}}p')
rs = next(i for i,p in enumerate(all_p2) if pt(p).strip()=='References')

rns = []
for i in range(rs+1, len(all_p2)):
    m = re.match(r'\[(\d+)\]', pt(all_p2[i]).strip())
    if m:
        n = int(m.group(1))
        if n in rns: print(f'DUP REF: [{n}]')
        rns.append(n)
print(f'Ref list: {len(rns)}, seq={rns==list(range(1,len(rns)+1))}')

body_refs = []
for i, p in enumerate(all_p2):
    if i >= rs: break
    for m in re.finditer(r'\[(\d+(?:[–\-]\d+)*(?:,\d+(?:[–\-]\d+)*)*)\]', pt(p)):
        for part in re.split(r',', m.group(1)):
            part = part.strip()
            rm = re.match(r'(\d+)\s*[–\-]\s*(\d+)', part)
            if rm:
                for n in range(int(rm.group(1)), int(rm.group(2))+1):
                    if n not in body_refs: body_refs.append(n)
            elif part.isdigit() and int(part) not in body_refs:
                body_refs.append(int(part))
print(f'Body refs: {len(body_refs)}, seq={all(body_refs[i]<=body_refs[i+1] for i in range(len(body_refs)-1))}')
if len(body_refs) < len(rns):
    print(f'Missing from body: {sorted(set(range(1,len(rns)+1))-set(body_refs))}')
