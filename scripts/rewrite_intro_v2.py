"""
Rewrite Introduction v2: Focus on BTC interpretation methods review.
Emphasize how our dual-regime approach differs from previous methods.
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

# Find boundaries
intro_h_idx = None
exp_h_idx = None
for i, child in enumerate(all_children):
    if child.tag == f'{{{W}}}p':
        txt = pt(child).strip()
        if txt == '1. Introduction':
            intro_h_idx = i
        if txt == '2. Experimental Section':
            exp_h_idx = i
            break

# Remove old intro body paragraphs
old_body = []
for i in range(intro_h_idx + 1, exp_h_idx):
    if all_children[i].tag == f'{{{W}}}p':
        old_body.append(i)

for idx in sorted(old_body, reverse=True):
    all_children[idx].getparent().remove(all_children[idx])

print(f"Removed {len(old_body)} old paragraphs")

# ================================================================
# NEW INTRODUCTION
# ================================================================

P1 = (
    "Global primary energy consumption is projected to grow by nearly 20% "
    "through 2050, with fossil fuels retaining a dominant share of the energy "
    "mix [1,2]. Unconventional reservoirs (tight oil, shale gas, and coalbed "
    "methane) account for an increasing fraction of hydrocarbon supply, driven "
    "by advances in horizontal drilling and multi-stage hydraulic fracturing "
    "[3,4]. A typical horizontal well may contain 10 to 30 individually "
    "fractured stages, yet the industry still lacks a routine, cost-effective "
    "method for determining per-stage contributions to total production [5,6]. "
    "Without per-stage production data, operators cannot reliably identify "
    "underperforming stages, optimize inter-well spacing, or validate completion "
    "designs against production outcomes [7,8]."
)

P2 = (
    "Each available monitoring technology involves inherent trade-offs. "
    "Production logging tools (PLT) provide accurate downhole flow profiles "
    "but require well intervention and capture only a snapshot in time [9]. "
    "Distributed fiber-optic sensing (DAS/DTS) enables continuous monitoring "
    "but demands permanent cable installation during completion and incurs "
    "capital costs difficult to justify for marginal wells [10,11]. Microseismic "
    "monitoring characterizes fracture geometry rather than production "
    "contribution [12]. Tracer-based diagnostics have consequently emerged as "
    "a compelling alternative: they require no downhole instrumentation, need "
    "no well intervention, and provide direct chemical evidence linking each "
    "labeled interval to its produced fluids [13,14]."
)

P3 = (
    "Chemical tracers have been deployed in oilfield operations since the "
    "1950s [15], progressing from radioactive inter-well waterflood monitors "
    "to contemporary partitioning inter-well tracer tests for residual oil "
    "measurement [16,17]. Recent multi-tracer field campaigns have demonstrated "
    "quantitative per-stage production allocation in fractured horizontal wells "
    "[18–20], confirming that tracer-based production profiling is technically "
    "viable at field scale. Among tracer-based approaches, the tracer "
    "proppant—a composite particle that immobilizes a tracer agent within a "
    "solid carrier and is co-injected with fracturing fluid—offers a distinct "
    "advantage: the tracer remains in the fracture after a single placement, "
    "enabling long-term, stage-specific monitoring without repeated intervention "
    "[21]. Recent designs encompass ceramic carriers with rhodamine 6G [21] "
    "or carbon quantum dots [22], rare-earth-doped polymer coatings for "
    "multi-element coding [23], oleophilic Fe₃O₄/polystyrene microspheres for "
    "selective oil-phase release [24], polymer-coated proppants with dual "
    "near-zone and far-zone tracer codes [25], multi-colored dye-tracer "
    "proppants for quantitative flowback assessment [26], and marked proppant "
    "transport studies [27]."
)

P4 = (
    "Despite this diversity of proppant designs, all tracer proppant studies "
    "cited above share a fundamental methodological structure: tracer release "
    "is characterized in batch experiments and fitted to the Korsmeyer-Peppas "
    "(K-P) power law, C/C₀ = K·tⁿ [28–30], while the transport step—how "
    "released tracer travels from the proppant pack through the production "
    "tubing to the sampling point—is not modeled. The K-P model identifies "
    "the dominant release mechanism (Fickian diffusion for n ≤ 0.43, anomalous "
    "transport for 0.43 < n < 0.85, Case-II relaxation for n ≥ 0.85) and "
    "provides the temperature-dependent rate constant K. These are valuable "
    "descriptors of the release process, but K-P is fundamentally a zero-"
    "dimensional batch model: it characterizes the temporal evolution of the "
    "released mass fraction in a well-mixed vessel, with no spatial coordinate, "
    "no flow field, and no mechanism for translating a release rate into an "
    "observable concentration at a distant sampling point. The K-P model can "
    "quantify how fast the tracer leaves the proppant; it cannot predict the "
    "wellhead concentration history, the peak arrival time, the tail "
    "persistence, or the per-interval production rate."
)

P5 = (
    "The interpretation of tracer breakthrough curves (BTCs) in petroleum "
    "applications has evolved through several methodological stages, each "
    "adding capability but none designed for the coupled release-transport "
    "problem posed by tracer proppants. The classical approach fits the one-"
    "dimensional advection-dispersion equation (ADE), ∂C/∂t + v·∂C/∂x = "
    "D·∂²C/∂x², to observed concentration histories. Van Genuchten and "
    "Alves [31] compiled analytical solutions for a comprehensive set of "
    "initial and boundary conditions—instantaneous pulses, finite-duration "
    "injections, and continuous sources—and these remain the standard "
    "reference. Shook et al. [32] advanced beyond direct curve fitting by "
    "applying residence-time-distribution moment analysis to tracer BTCs. "
    "Their method extracts swept volume, sweep efficiency, and remaining oil "
    "saturation directly from the integrated breakthrough signal without "
    "requiring numerical simulation—a significant practical advance, but one "
    "that treats the tracer source as a known, completed injection. Fontalvo "
    "et al. [16] demonstrated that the choice of transport model carries direct "
    "operational consequence: applying a physically inappropriate model to "
    "partitioning inter-well tracer tests can systematically overestimate or "
    "underestimate remaining oil saturation, making model selection a reservoir-"
    "management necessity rather than an academic exercise. More recently, "
    "Velasco-Lozano et al. [33] derived the first analytical solutions for "
    "partitioning tracer transport in two-phase, advection-dominated porous "
    "media, establishing closed-form expressions for tracer concentration in "
    "each phase under simultaneous oil-water flow. Mazo et al. [34] developed "
    "a two-phase multicomponent flow model coupling multi-stage hydraulic "
    "fractures with explicit tracer transfer between aqueous and oleic phases; "
    "through stream-tube decomposition, they demonstrated that per-stage "
    "production allocation from tracer data is theoretically achievable when "
    "both transport physics and tracer partitioning are adequately resolved."
)

P6 = (
    "A common structural limitation runs through all of these methods: the "
    "tracer source is treated as a known input—an instantaneous pulse, a "
    "finite-duration injection, or a prescribed initial condition [16,31,32]. "
    "A tracer proppant breaks this assumption. The source term is not a Dirac "
    "delta administered at t = 0; it is a sustained, matrix-diffusion-controlled "
    "release function that evolves over the production period, and the observed "
    "BTC reflects the convolution of this unknown release with advective-"
    "dispersive transport. To our knowledge, no existing method has addressed "
    "this coupled inverse problem in which neither the source function nor the "
    "transport parameters are known independently. In this work, we resolve "
    "this by decomposing the BTC into two physically motivated components—a "
    "Gaussian pulse representing the shut-in accumulation slug (advective-"
    "dispersive transport of tracer that diffused into the near-wellbore region "
    "during shut-in) and an erfc tail representing sustained matrix-diffusion-"
    "controlled release from the proppant pack—joined by a smooth hyperbolic-"
    "tangent (tanh) transition. This decomposition is the central innovation: "
    "rather than fitting the entire BTC to a single transport equation with a "
    "prescribed source, we separate the signal into its physically distinct "
    "contributions and recover the per-interval flow rate directly from the "
    "concentration history. The model self-calibrates: the fitted flow rate "
    "agrees with the independently set pump rate within 8% without being "
    "constrained in the objective function, and the Peclet number independently "
    "confirms the non-Fickian transport mechanism identified via K-P kinetics. "
    "Critically, the decomposition reveals that approximately 47% of the "
    "integrated tracer signal originates from sustained release rather than "
    "the initial accumulation slug, establishing that a single shut-in suffices "
    "for long-term monitoring—a significant operational advantage. This shift "
    "from empirical release characterization to predictive transport modeling "
    "is the basis for translating wellhead concentration histories into "
    "quantitative per-interval production allocation."
)

P7 = (
    "Beyond the modeling gap, practical deployment imposes ancillary material "
    "constraints on the tracer carrier. Conventional proppant materials face "
    "limitations: ceramic carriers exhibit high density (~1.5 g/cm³), impeding "
    "transport in low-viscosity fracturing fluids [35,36], and polymer-based "
    "alternatives such as polystyrene offer limited thermal stability at "
    "downhole conditions [37,38]. Epoxy resin has recently emerged as a "
    "promising alternative matrix: its highly cross-linked network enables "
    "sustained, matrix-diffusion-controlled release [39–41], and its surface "
    "chemistry can be tailored for oleophilic selectivity, enabling selective "
    "oil-phase tracer delivery."
)

P8 = (
    "In this work, we address both the transport-modeling gap and the "
    "material-design challenge at the single-interval laboratory scale. On "
    "the modeling side, we develop a piecewise ADE-based formulation that "
    "decomposes the BTC into a Gaussian pulse (shut-in accumulation slug) and "
    "an erfc tail (sustained matrix-diffusion-controlled release), linked by "
    "a smooth tanh transition. The six-parameter model is validated through "
    "four complementary lines of evidence: statistical model selection against "
    "simpler single-component formulations, physical self-calibration of the "
    "fitted flow rate against the independently set pump rate, mechanistic "
    "consistency with independent K-P kinetic measurements, and parametric "
    "robustness analysis across a six-fold variation in transition width. On "
    "the material side, we synthesize an oleophilic epoxy/Fe₃O₄ tracer "
    "proppant (ESP-T) via emulsion polymerization, with stearic acid-modified "
    "nano-Fe₃O₄ imparting oleophilic character for selective oil-phase release. "
    "Under steady-state two-phase flow, the oil-phase tracer mass flux "
    "eliminates water-dilution artifacts and quantitatively tracks per-interval "
    "oil production rates, providing a pathway to per-stage production "
    "allocation requiring only wellhead measurements and a single shut-in."
)

new_paras = [P1, P2, P3, P4, P5, P6, P7, P8]

# ================================================================
# Insert new paragraphs
# ================================================================
body = root.find(f'{{{W}}}body')
all_children = list(body)

# Find intro heading again
intro_h_idx = None
for i, child in enumerate(all_children):
    if child.tag == f'{{{W}}}p' and pt(child).strip() == '1. Introduction':
        intro_h_idx = i
        break

for j, text in enumerate(new_paras):
    new_p = make_para(text)
    insert_after = all_children[intro_h_idx + j]
    insert_after.addnext(new_p)
    all_children = list(body)

# Remove strays
all_children = list(body)
new_last = None
exp_idx = None
for i, child in enumerate(all_children):
    if child.tag == f'{{{W}}}p':
        txt = pt(child).strip()
        if 'requiring only wellhead measurements and a single shut-in' in txt:
            new_last = i
        if txt == '2. Experimental Section':
            exp_idx = i
            break

if new_last and exp_idx:
    stray = [i for i in range(new_last + 1, exp_idx) if all_children[i].tag == f'{{{W}}}p']
    for i in reversed(stray):
        all_children[i].getparent().remove(all_children[i])
    if stray:
        print(f"Removed {len(stray)} stray paragraphs")

# Save
all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        zout.writestr(name, data)

total = sum(len(t) for t in new_paras)
print(f"Saved: {out}")
print(f"New intro: {len(new_paras)} paragraphs, {total} chars")
