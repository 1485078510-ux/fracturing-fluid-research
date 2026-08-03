"""
Polish manuscript for submission quality:
  - Split sentences >30 words
  - Replace em dashes with commas/parentheses
  - Standardize terminology (BTC, K-P, etc.)
  - Improve logical flow and transitions
  - Overclaim check in conclusions
  - Minor wording improvements
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from lxml import etree
from copy import deepcopy
import zipfile, re

doc_path = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_3-revised_clean.docx"
output_path = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_3-revised_clean.docx"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def pt(p):
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))

def collapse_and_set_text(p, new_text):
    """Replace paragraph content with single run of new text, keeping pPr."""
    ref_rpr = None
    first_r = p.find(f'.//{{{W}}}r')
    if first_r is not None:
        ref_rpr = first_r.find(f'{{{W}}}rPr')
    for child in list(p):
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag != 'pPr':
            p.remove(child)
    r = etree.SubElement(p, f'{{{W}}}r')
    if ref_rpr is not None:
        r.append(deepcopy(ref_rpr))
    else:
        rpr = etree.SubElement(r, f'{{{W}}}rPr')
        etree.SubElement(rpr, f'{{{W}}}rFonts').set(f'{{{W}}}cs', 'Times New Roman')
    t = etree.SubElement(r, f'{{{W}}}t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = new_text

def replace_in_para(p, old, new):
    """Replace text across all runs in a paragraph."""
    c = 0
    for t in p.iter(f'{{{W}}}t'):
        if t.text and old in t.text:
            t.text = t.text.replace(old, new)
            c += 1
    return c

# ── Load document ──
with zipfile.ZipFile(doc_path, 'r') as zin:
    all_files = {name: zin.read(name) for name in zin.namelist()}

root = etree.fromstring(all_files['word/document.xml'])
body = root.find(f'{{{W}}}body')
paras = body.findall(f'.//{{{W}}}p')

edits = []

# ===================================================================
# ABSTRACT — tighten, split long sentences
# ===================================================================
new_abs = (
    "Per-interval production monitoring is essential for evaluating stimulation "
    "effectiveness in multi-stage fractured horizontal wells. Existing tracer "
    "technologies, however, lack a quantitative transport model linking sustained "
    "release kinetics to wellhead breakthrough signals. We address this gap by "
    "developing a piecewise advection-dispersion model that decomposes tracer "
    "breakthrough curves (BTCs) into a Gaussian pulse component (shut-in accumulation "
    "slug) and an erfc tail component (sustained matrix-diffusion-controlled release), "
    "linked by a smooth tanh transition. The six-parameter model is validated with "
    "an oleophilic epoxy/Fe₃O₄ tracer proppant (ESP-T) fabricated via emulsion "
    "polymerization. The dual-regime formulation is statistically decisive over four "
    "simpler alternatives (ΔAICc = 32.7, p < 10⁻⁶), achieving R² = 0.9939; the erfc "
    "tail accounts for 47% of the integrated signal, a result robust to a six-fold "
    "variation in the transition width. Physical self-calibration is demonstrated: "
    "the fitted flow rate (0.46 mL/min) agrees with the pump setting (0.50 mL/min) "
    "within 8%, and the Peclet number (Pe = 0.934) independently confirms the "
    "non-Fickian transport mechanism identified via Korsmeyer-Peppas kinetics. Under "
    "steady-state two-phase flow, the oil-phase tracer mass flux (FO = Coil × Qoil) "
    "eliminates water-dilution artifacts and quantitatively tracks oil production "
    "rates (Pearson r = 0.97, RMSD = 8.3%). This framework enables per-interval "
    "production allocation requiring only wellhead measurements and a single shut-in."
)
collapse_and_set_text(paras[2], new_abs)
edits.append("Abstract: split first sentence; tightened wording")

# ===================================================================
# INTRODUCTION — minor polishes
# ===================================================================

# Para 7: "yet the industry still lacks" → "the industry still lacks" (shorter, stronger)
replace_in_para(paras[7],
    "yet the industry still lacks a routine, cost-effective method",
    "the industry still lacks a routine, cost-effective method")
edits.append("Intro[7]: removed redundant 'yet'")

# Para 8: "involves trade-offs." → "involves inherent trade-offs."
replace_in_para(paras[8], "involves trade-offs.", "involves inherent trade-offs.")
edits.append("Intro[8]: trade-offs → inherent trade-offs")

# Para 10: replace em dash with comma
# "The tracer proppant—a composite particle..." → "The tracer proppant, a composite particle..."
replace_in_para(paras[10],
    "The tracer proppant—a composite particle that immobilizes",
    "The tracer proppant, a composite particle that immobilizes")
# "...without repeated injection [21]." — closing em dash needs to close properly
replace_in_para(paras[10],
    "monitoring without repeated injection [21].",
    "monitoring without repeated injection [21].")  # already handled
edits.append("Intro[10]: em dash → comma")

# Para 11: em dash replacement
replace_in_para(paras[11],
    "mechanism—Fickian diffusion for n",
    "mechanism (Fickian diffusion for n")
replace_in_para(paras[11],
    "relaxation for n ≥ 0.85—and provides",
    "relaxation for n ≥ 0.85) and provides")
edits.append("Intro[11]: em dashes → parentheses")

# Para 12: em dashes, hedging already added. Fix one em dash:
replace_in_para(paras[12],
    "the inverse problem in double—neither the release function",
    "the inverse problem in double: neither the release function")
replace_in_para(paras[12],
    "curve shape—flow rate, dispersion, and the",
    "curve shape (flow rate, dispersion, and the")
replace_in_para(paras[12],
    "sustained release—remains uninterpreted",
    "sustained release) remains uninterpreted")
edits.append("Intro[12]: em dashes → colons/parentheses")

# Para 13: em dash
replace_in_para(paras[13],
    "and water-phase release—the dominant mode in",
    "and water-phase release, the dominant mode in")
replace_in_para(paras[13],
    "designs—cannot distinguish oil from",
    "designs, cannot distinguish oil from")
edits.append("Intro[13]: em dashes → commas")

# Para 14: em dash in "oleophilic epoxy/Fe₃O₄ tracer proppant (ESP-T) via emulsion polymerization, with stearic acid-modified..."
# No em dash here, but check
replace_in_para(paras[14],
    "the water-dilution artifact",
    "the water-dilution artifact")  # already clean

# ===================================================================
# §3.1 — ESP-T Characterization: break up long paragraph [44]
# ===================================================================
old_p44 = pt(paras[44])
new_p44 = (
    "ESP-T exhibits a bulk density of 0.646 g/cm³, well below the 1.0 g/cm³ "
    "threshold for self-suspension in water-based fracturing fluids. Sphericity "
    "and roundness both exceed 0.9 (Krumbien-Sloss chart). Acid solubility is "
    "3.3%, well below the 5% limit specified by SY/T 5107–2016. The crush rate "
    "at 52 MPa is 2.9%, comparable to pure epoxy microspheres (2.6%); the slight "
    "increase is attributable to the hollow glass microspheres rather than matrix "
    "degradation. Complete physical properties are provided in Table S4."
)
collapse_and_set_text(paras[44], new_p44)
edits.append("§3.1[44]: broke up dense paragraph, explicit comparisons")

# Para 45 (was the permeability paragraph — now it's in the next index)
# Let me check what para 45 is now
# Actually the paragraph indices shifted when I replaced Para 44 text in-place
# The collapsed paragraph should be fine.

# ===================================================================
# §3.1 — Packed-bed paragraph: em dash
# ===================================================================
# "This water-resistant, oil-permeable characteristic means..." — this is the sentence
# It's in the same paragraph as the filtration results.
# Let me find it by searching for "water-resistant, oil-permeable"
for p_idx, p in enumerate(paras):
    txt = pt(p)
    if "water-resistant, oil-permeable characteristic" in txt:
        # This sentence has an em dash before "providing passive water-cut mitigation"
        replace_in_para(p,
            "providing passive water-cut mitigation.",
            "thereby providing passive water-cut mitigation.")
        edits.append(f"§3.1[{p_idx}]: improved transition to water-cut claim")
        break

# ===================================================================
# §3.3 — Physical origin paragraph: tighten
# ===================================================================
for p_idx, p in enumerate(paras):
    txt = pt(p)
    if "Physical origin of the dual-regime BTC" in txt:
        # This is a heading — skip to next paragraph
        continue
    if "A tracer BTC obtained after an extended shut-in reflects two physically distinct processes." in txt:
        # This is the physical origin paragraph. Tighten it.
        new_txt = (
            "A tracer BTC obtained after an extended shut-in reflects two physically "
            "distinct processes. Process I (shut-in accumulation slug): during the "
            "96 h shut-in, tracer continuously diffuses from the epoxy matrix into the "
            "proppant pack and the near-wellbore region; when the well opens, this "
            "accumulated tracer is swept toward the sampling point as a coherent slug, "
            "producing a Gaussian-shaped concentration peak. Process II (sustained "
            "matrix-diffusion-controlled release): after the main slug has passed, "
            "residual tracer continues to diffuse from the epoxy matrix at a lower but "
            "persistent rate, feeding a slowly decaying concentration tail. These two "
            "contributions overlap in time: the tail begins before the pulse has fully "
            "passed, and neither can be isolated by visual inspection of the "
            "concentration curve alone. A mathematical model capable of separating "
            "them is therefore required."
        )
        collapse_and_set_text(p, new_txt)
        edits.append(f"§3.3[{p_idx}]: tightened physical origin paragraph")
        break

# ===================================================================
# §3.3 — Synthesis paragraph (longest in paper): split into 2
# ===================================================================
for p_idx, p in enumerate(paras):
    txt = pt(p)
    if "Taken together, these results establish a perspective" in txt:
        # Split at "The 47% sustained-release fraction..."
        # Part 1: distinguishes approach from earlier efforts
        part1 = (
            "Taken together, these results establish a perspective that distinguishes "
            "the present approach from earlier efforts. Conventional ADE-based tracer "
            "interpretation treats transport as a means of characterizing the "
            "reservoir—extracting fracture geometry or inter-well connectivity—rather "
            "than as the direct source of a production metric. Tracer mass-balance "
            "methods allocate production among stages but do not exploit the shape of "
            "the breakthrough curve. The dual-regime model developed here reverses "
            "this logic: the transport itself, once decomposed into its Gaussian pulse "
            "and sustained erfc tail, yields the effective per-interval flow rate "
            "without requiring downhole instrumentation or repeated shut-ins."
        )
        part2 = (
            "The 47% sustained-release fraction within the measurement window carries "
            "a significant operational implication: a single shut-in suffices for "
            "long-term monitoring, because nearly half the tracer signal originates "
            "from ongoing matrix-diffusion-controlled release rather than from the "
            "initial accumulation slug. This shift from descriptive to predictive "
            "transport modeling provides the quantitative basis for translating a "
            "wellhead concentration history into actionable per-interval production "
            "allocation."
        )
        # Replace current paragraph with part1
        collapse_and_set_text(p, part1)
        # Insert part2 as a new paragraph after this one
        new_p = deepcopy(p)
        collapse_and_set_text(new_p, part2)
        parent = p.getparent()
        idx = list(parent).index(p)
        parent.insert(idx + 1, new_p)
        edits.append(f"§3.3[{p_idx}]: split synthesis into 2 paragraphs")
        break

# ===================================================================
# §3.4 — Limitation paragraph polish
# ===================================================================
for p_idx, p in enumerate(paras):
    txt = pt(p)
    if "Several limitations of the present study should be noted." in txt:
        new_txt = (
            "Several limitations of the present study should be noted. First, the "
            "model was validated on a single interval with uniform proppant packing; "
            "multi-interval configurations remain untested. Second, the FO "
            "calibration used dodecane under steady flow at a single temperature; "
            "transient conditions, crude oil, and site-specific thermal effects "
            "require dedicated follow-up studies. Third, the chemical stability of "
            "the epoxy matrix in aggressive downhole environments (H₂S, CO₂, "
            "high-salinity brines, temperatures exceeding 120 °C) was not evaluated. "
            "Addressing these limitations defines the path from laboratory "
            "demonstration to field deployment."
        )
        collapse_and_set_text(p, new_txt)
        edits.append(f"§3.4[{p_idx}]: polished limitations paragraph")
        break

# ===================================================================
# §3.4 — Field deployment paragraph: tighten
# ===================================================================
for p_idx, p in enumerate(paras):
    txt = pt(p)
    if "These results suggest an operational pathway toward field deployment" in txt:
        new_txt = (
            "These results suggest an operational pathway toward field deployment, "
            "though several validation steps remain. Each fracture stage would receive "
            "ESP-T particles doped with a distinct metal or rare earth element (e.g., "
            "Mn, Zn, Cu, Eu, Dy), producing a unique ICP-MS signature for per-stage "
            "signal separation. After a single shut-in period, produced fluid is "
            "sampled at the wellhead at intervals guided by the expected pulse arrival "
            "time predicted from the wellbore geometry and estimated flow velocity. "
            "The fitted Q for each stage, converted to an oil production rate via flux "
            "normalization, identifies underperforming intervals. Periodic sampling "
            "could track the evolution of each stage's contribution over time without "
            "requiring downhole tools or additional shut-ins, because the tracer "
            "remains in the fracture after a single placement."
        )
        collapse_and_set_text(p, new_txt)
        edits.append(f"§3.4[{p_idx}]: tightened field deployment paragraph")
        break

# ===================================================================
# §4 Conclusions — tighten, overclaim check
# ===================================================================

# Conclusion Para 1 (now find by content)
for p_idx, p in enumerate(paras):
    txt = pt(p)
    if "This work bridges the gap between tracer release kinetics and the quantitative interpretation" in txt:
        new_txt = (
            "This work bridges the gap between tracer release kinetics and the "
            "quantitative interpretation of wellhead breakthrough curves, enabling "
            "tracer proppants to deliver on their promise of per-interval production "
            "monitoring. We developed a dual-regime piecewise advection-dispersion "
            "model that decomposes the BTC into a Gaussian pulse (shut-in accumulation "
            "slug) and an erfc tail (sustained matrix-diffusion-controlled release), "
            "linked by a smooth tanh transition. The model was validated against "
            "single-phase and two-phase core displacement experiments using an "
            "oleophilic epoxy/Fe₃O₄ tracer proppant (ESP-T)."
        )
        collapse_and_set_text(p, new_txt)
        edits.append(f"Conclusion[{p_idx}]: tightened opening, split long sentence")
        break

# Conclusion Para with "Four complementary lines"
for p_idx, p in enumerate(paras):
    txt = pt(p)
    if "Four complementary lines of evidence support the model." in txt:
        new_txt = (
            "Four complementary lines of evidence support the model. Statistically, "
            "the dual-regime formulation is decisively preferred over four simpler "
            "alternatives (ΔAICc = 32.7, F-test p < 10⁻⁶). Physically, the model "
            "self-calibrates: the fitted flow rate (0.46 mL/min) and residence time "
            "(37.4 min) agree with independent measurements within 8% and 3%, "
            "respectively. Mechanistically, the Peclet number (Pe = 0.934) "
            "independently confirms the non-Fickian transport regime identified via "
            "Korsmeyer-Peppas kinetics. The erfc tail accounts for 47% of the "
            "integrated signal over the measurement period, a result robust to a "
            "six-fold variation in the transition width (Table 5). This sustained-"
            "release fraction implies that a single shut-in suffices for long-term "
            "monitoring, a significant operational advantage."
        )
        collapse_and_set_text(p, new_txt)
        edits.append(f"Conclusion[{p_idx}]: tightened evidence paragraph, removed redundancy")
        break

# Conclusion Para with "Under steady-state two-phase flow"
for p_idx, p in enumerate(paras):
    txt = pt(p)
    if "Under steady-state two-phase flow, the oil-phase tracer flux eliminates" in txt:
        new_txt = (
            "Under steady-state two-phase flow, the oil-phase tracer flux eliminates "
            "the water-dilution artifact inherent in concentration measurements and "
            "quantitatively tracks oil production rates (r = 0.97, RMSD = 8.3%) using "
            "only wellhead measurements and a laboratory-calibrated reference. Simple "
            "time-of-arrival methods fail for this class of breakthrough curves "
            "(errors of +162% to +685%), confirming that the full modeling framework "
            "is necessary. When combined with multi-element tracer coding, the "
            "methodology provides a pathway to per-stage production allocation in "
            "multi-fractured horizontal wells, requiring no downhole tools and only "
            "a single shut-in."
        )
        collapse_and_set_text(p, new_txt)
        edits.append(f"Conclusion[{p_idx}]: tightened two-phase flow paragraph")
        break

# Conclusion limitations paragraph
for p_idx, p in enumerate(paras):
    txt = pt(p)
    if "The present validation is limited to single-interval" in txt:
        new_txt = (
            "The present validation is limited to single-interval laboratory "
            "experiments with dodecane as the model oil. Extending the framework "
            "to field-scale, multi-interval conditions with crude oil under transient "
            "flow, elevated temperature, and aggressive fluid environments (H₂S, CO₂, "
            "high-salinity brines) constitutes the next step toward practical "
            "deployment."
        )
        collapse_and_set_text(p, new_txt)
        edits.append(f"Conclusion[{p_idx}]: tightened limitations paragraph")
        break

# ===================================================================
# Em dash cleanup — global pass for any remaining
# ===================================================================
dash_count = 0
for t in root.iter(f'{{{W}}}t'):
    if t.text and '—' in t.text:
        # Replace remaining em dashes
        t.text = t.text.replace('—', ', ')
        dash_count += 1
if dash_count:
    edits.append(f"Global: replaced {dash_count} remaining em dashes with commas")

# ===================================================================
# Terminology standardization
# ===================================================================
# "BTC" first use: already "(BTCs)" in abstract and intro
# "breakthrough curve (BTC)" should be consistent
# Check: K-P model vs Korsmeyer-Peppas
# First use in Para 11: "Korsmeyer-Peppas (K-P)" — correct

# "dual-regime" should be lowercase except in title
# Already handled in previous pass.

# ===================================================================
# Write output
# ===================================================================
all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        zout.writestr(name, data)

print(f"Saved: {output_path}")
print(f"Edits made ({len(edits)}):")
for e in edits:
    print(f"  - {e}")
