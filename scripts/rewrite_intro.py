"""
Rewrite Introduction: focus on modeling review, materials brief.
Save as new file ESP-T_Final_4-intro_rewritten.docx
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from lxml import etree
from copy import deepcopy
import zipfile

src = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_3-revised_clean.docx"
out = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_4-intro_rewritten.docx"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def pt(p):
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))

def make_para(text, template=None):
    """Create a new paragraph element with text."""
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

# Load
with zipfile.ZipFile(src, 'r') as zin:
    all_files = {name: zin.read(name) for name in zin.namelist()}

root = etree.fromstring(all_files['word/document.xml'])
body = root.find(f'{{{W}}}body')

# Find all paragraphs and locate boundaries
all_p = list(body)  # all direct children (including non-paragraph elements)

# Find "1. Introduction" and "2. Experimental Section" paragraph indices
intro_h_idx = None
exp_h_idx = None
para_elements = []
for i, child in enumerate(all_p):
    if child.tag == f'{{{W}}}p':
        para_elements.append(i)
        txt = pt(child).strip()
        if txt == '1. Introduction':
            intro_h_idx = i
        if txt == '2. Experimental Section':
            exp_h_idx = i
            break

print(f"Introduction heading at element index: {intro_h_idx}")
print(f"Experimental heading at element index: {exp_h_idx}")

# Collect indices of old intro body paragraphs (between heading and Experimental)
old_body_indices = []
for i in range(intro_h_idx + 1, exp_h_idx):
    if all_p[i].tag == f'{{{W}}}p':
        old_body_indices.append(i)

print(f"Old intro body paragraphs: {len(old_body_indices)} at indices {old_body_indices}")

# ============================================================
# NEW INTRODUCTION TEXT
# ============================================================

new_paras = [
    # P1: Energy context + per-stage need
    (
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
    ),
    # P2: Monitoring technologies → tracers
    (
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
    ),
    # P3: Tracer evolution → proppant designs
    (
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
    ),
    # P4: K-P limitations (MODELING FOCUS)
    (
        "Despite this diversity of proppant designs, all studies cited above share "
        "a fundamental methodological limitation: tracer release is characterized "
        "exclusively in batch experiments and fitted to the Korsmeyer-Peppas (K-P) "
        "power law, C/C₀ = K·tⁿ [28–30]. The K-P model identifies the dominant "
        "release mechanism (Fickian diffusion for n ≤ 0.43, anomalous transport for "
        "0.43 < n < 0.85, and Case-II relaxation for n ≥ 0.85) and provides the "
        "temperature-dependent rate constant K—valuable information for the release "
        "side of the problem. However, K-P is fundamentally a zero-dimensional "
        "batch model: it characterizes the temporal evolution of the released mass "
        "fraction in a well-mixed vessel, with no spatial coordinate, no flow field, "
        "and no mechanism for translating a release rate into an observable "
        "concentration at a distant sampling point. The K-P model can quantify how "
        "fast the tracer leaves the proppant, but it cannot predict the wellhead "
        "concentration history, the peak arrival time, the tail persistence, or "
        "the per-interval production rate."
    ),
    # P5: ADE framework + petroleum applications (DETAILED MODELING REVIEW)
    (
        "The one-dimensional advection-dispersion equation (ADE), "
        "∂C/∂t + v·∂C/∂x = D·∂²C/∂x², provides the canonical framework for solute "
        "transport in tubular and porous-media flow. Its analytical solutions for "
        "a comprehensive range of initial and boundary conditions were compiled by "
        "van Genuchten and Alves [31] and remain the standard reference for tracer "
        "test interpretation. Within petroleum engineering, the ADE has been applied "
        "extensively to inter-well tracer tests for reservoir characterization. "
        "Shook et al. [32] developed moment analysis methods to determine reservoir "
        "properties and flood performance directly from tracer breakthrough curves. "
        "Fontalvo et al. [16] provided a physical interpretation framework for "
        "partitioning inter-well tracer tests via ADE-based parameter estimation "
        "with upstream-upwind numerical coupling. More recently, Velasco-Lozano "
        "et al. [33] derived analytical solutions for partitioning tracer transport "
        "in two-phase, advection-dominated porous media, establishing closed-form "
        "expressions for tracer concentration in each phase. Mazo et al. [34] "
        "developed a two-phase multicomponent flow model incorporating multi-stage "
        "hydraulic fractures with explicit tracer transfer between aqueous and "
        "oleic phases, demonstrating that per-stage production allocation is "
        "theoretically achievable when both transport physics and tracer "
        "partitioning behavior are adequately resolved. These advances establish "
        "that the ADE framework can handle increasingly complex transport "
        "scenarios relevant to fractured well environments."
    ),
    # P6: The critical gap
    (
        "Critically, however, all of these ADE-based approaches share a common "
        "assumption: the tracer source is treated as a known input—either an "
        "instantaneous pulse or a finite-duration injection with a prescribed "
        "initial condition [16,31,32]. None has been coupled to a sustained-release "
        "source term representing matrix-diffusion-controlled tracer liberation "
        "from a polymeric carrier. A tracer proppant presents a fundamentally "
        "different problem: the source term is itself unknown, governed by the "
        "same matrix-diffusion kinetics characterized in batch K-P experiments, "
        "and the observed breakthrough curve reflects the convolution of this "
        "unknown release function with advective-dispersive transport. To our "
        "knowledge, this coupled release-transport inverse problem—in which "
        "neither the source function nor the transport parameters are known "
        "independently—has not been addressed in the literature. Its practical "
        "consequence is that existing tracer proppants can confirm which stages "
        "are producing but cannot quantify production rates from the breakthrough "
        "curve alone: the full information encoded in the curve shape (flow rate, "
        "dispersion, and the relative contributions of shut-in accumulation and "
        "sustained release) remains uninterpreted."
    ),
    # P7: Material constraints — BRIEF
    (
        "Beyond the modeling gap, practical deployment imposes ancillary material "
        "constraints on the tracer carrier. Conventional proppant materials face "
        "limitations: ceramic carriers exhibit high density (~1.5 g/cm³), impeding "
        "transport in low-viscosity fracturing fluids [35,36], and polymer-based "
        "alternatives such as polystyrene offer limited thermal stability at "
        "downhole conditions [37,38]. Epoxy resin has recently emerged as a "
        "promising alternative: its highly cross-linked network enables sustained, "
        "matrix-diffusion-controlled release [39–41], and its surface chemistry can "
        "be tailored for oleophilic selectivity, enabling selective oil-phase "
        "tracer delivery."
    ),
    # P8: This work
    (
        "In this work, we address both the transport-modeling gap and the "
        "material-design challenge at the single-interval laboratory scale. On "
        "the modeling side, we develop a piecewise ADE-based formulation that "
        "decomposes the breakthrough curve into a Gaussian pulse (representing "
        "the shut-in accumulation slug) and an erfc tail (representing sustained "
        "matrix-diffusion-controlled release), linked by a smooth tanh transition. "
        "This decomposition establishes a direct, quantitative relationship "
        "between the measured concentration history and the per-interval flow "
        "rate, transforming what would otherwise be empirical fitting parameters "
        "into physically interpretable quantities. The six-parameter model is "
        "validated through statistical model selection against four alternative "
        "formulations, physical self-calibration of the fitted flow rate against "
        "the independently set pump rate, mechanistic consistency with independent "
        "kinetic measurements, and parametric robustness analysis. On the material "
        "side, we synthesize an oleophilic epoxy/Fe₃O₄ tracer proppant (ESP-T) "
        "via emulsion polymerization, with stearic acid-modified nano-Fe₃O₄ "
        "imparting oleophilic character for selective oil-phase release. Under "
        "steady-state two-phase flow, the oil-phase tracer mass flux eliminates "
        "water-dilution artifacts and quantitatively tracks per-interval oil "
        "production rates, providing a pathway to per-stage production allocation "
        "that requires only wellhead measurements and a single shut-in."
    ),
]

# ============================================================
# Replace paragraphs
# ============================================================

# Remove old intro body paragraphs (reverse order)
for idx in sorted(old_body_indices, reverse=True):
    parent = all_p[idx].getparent()
    parent.remove(all_p[idx])

print(f"Removed {len(old_body_indices)} old intro paragraphs")

# Re-fetch body children after removal
body = root.find(f'{{{W}}}body')
all_children = list(body)

# Find "1. Introduction" again
intro_h_idx = None
for i, child in enumerate(all_children):
    if child.tag == f'{{{W}}}p' and pt(child).strip() == '1. Introduction':
        intro_h_idx = i
        break

# Insert new paragraphs after the heading
for j, text in enumerate(new_paras):
    new_p = make_para(text)
    # Insert after heading + already-inserted paragraphs
    insert_after = all_children[intro_h_idx + j]
    insert_after.addnext(new_p)
    # Update all_children for next iteration
    all_children = list(body)

print(f"Inserted {len(new_paras)} new intro paragraphs")

# Check for stray paragraphs between new content and Experimental
all_children = list(body)
new_last_idx = None
exp_idx = None
for i, child in enumerate(all_children):
    if child.tag == f'{{{W}}}p':
        txt = pt(child).strip()
        if 'providing a pathway to per-stage production allocation' in txt:
            new_last_idx = i
        if txt == '2. Experimental Section':
            exp_idx = i
            break

if new_last_idx is not None and exp_idx is not None:
    stray = list(range(new_last_idx + 1, exp_idx))
    stray_paras = [i for i in stray if all_children[i].tag == f'{{{W}}}p']
    if stray_paras:
        for idx in reversed(stray_paras):
            all_children[idx].getparent().remove(all_children[idx])
        print(f"Removed {len(stray_paras)} stray paragraphs between intro and Experimental")

# ============================================================
# Write
# ============================================================
all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        zout.writestr(name, data)

total_chars = sum(len(t) for t in new_paras)
print(f"\nSaved: {out}")
print(f"New intro: {len(new_paras)} paragraphs, {total_chars} total chars")
