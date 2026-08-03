"""
Revise manuscript v2 — with substantive text edits based on highlight analysis.
Edits:
  1. Condense Abstract (remove excessive quantitative detail)
  2. Shorten Materials paragraph (50% compression)
  3. Add hedging to ADE novelty claims
  4. Restore bridge paragraph for refs [15-20]
  5. Fix "butit" → "but it" spacing
  6. Two-Component → Dual-Regime globally
  7. Accept tracked changes + remove yellow highlights
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from lxml import etree
from copy import deepcopy
import zipfile

doc_path = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_3-revised.docx"
output_path = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_3-revised_clean.docx"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# ── Helpers ────────────────────────────────────────────────────────
def get_para_text(p):
    """Get full text of a paragraph."""
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))

def set_para_text(p, new_text):
    """Replace all text in a paragraph with new text, preserving paragraph properties."""
    # Remove all existing runs, ins, del
    for child in list(p):
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag in ('r', 'ins', 'del', 'bookmarkStart', 'bookmarkEnd',
                    'commentRangeStart', 'commentRangeEnd', 'commentReference'):
            p.remove(child)
    # Create a new run with the text
    r = etree.SubElement(p, f'{{{W}}}r')
    rpr = etree.SubElement(r, f'{{{W}}}rPr')
    rfonts = etree.SubElement(rpr, f'{{{W}}}rFonts')
    rfonts.set(f'{{{W}}}cs', 'Times New Roman')
    t = etree.SubElement(r, f'{{{W}}}t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = new_text

def replace_text_in_runs(p, old, new):
    """Replace text across all runs in a paragraph."""
    count = 0
    for t in p.iter(f'{{{W}}}t'):
        if t.text and old in t.text:
            t.text = t.text.replace(old, new)
            count += 1
    return count

def collapse_and_set_text(p, new_text):
    """Collapse all runs into one and set new text."""
    # Get paragraph properties
    ppr = p.find(f'{{{W}}}pPr')
    # Collect all runs
    runs = list(p.findall(f'.//{{{W}}}r'))
    # Get reference run properties from first run
    ref_rpr = None
    if runs:
        ref_rpr = runs[0].find(f'{{{W}}}rPr')
    # Remove all content children
    for child in list(p):
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag != 'pPr':
            p.remove(child)
    # Create single new run
    r = etree.SubElement(p, f'{{{W}}}r')
    if ref_rpr is not None:
        r.append(deepcopy(ref_rpr))
    else:
        rpr = etree.SubElement(r, f'{{{W}}}rPr')
        rfonts = etree.SubElement(rpr, f'{{{W}}}rFonts')
        rfonts.set(f'{{{W}}}cs', 'Times New Roman')
    t = etree.SubElement(r, f'{{{W}}}t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = new_text

# ── Read document ──────────────────────────────────────────────────
with zipfile.ZipFile(doc_path, 'r') as zin:
    all_files = {name: zin.read(name) for name in zin.namelist()}

root = etree.fromstring(all_files['word/document.xml'])
body = root.find(f'{{{W}}}body')
paras = body.findall(f'.//{{{W}}}p')

stats = {}

# ===================================================================
# 1. ABSTRACT — Condense (Para 2)
# ===================================================================
old_abs = get_para_text(paras[2])
new_abs = (
    "Per-interval production monitoring is essential for evaluating stimulation effectiveness "
    "in multi-stage fractured horizontal wells, yet existing tracer technologies lack a "
    "quantitative transport model linking sustained release kinetics to wellhead breakthrough "
    "signals. We address this gap by developing a piecewise advection-dispersion model that "
    "decomposes tracer breakthrough curves (BTCs) into a Gaussian pulse component (shut-in "
    "accumulation slug) and an erfc tailing component (sustained matrix-diffusion-controlled "
    "release), linked by a smooth tanh transition. The six-parameter model is validated with "
    "an oleophilic epoxy/Fe₃O₄ tracer proppant (ESP-T) fabricated via emulsion polymerization. "
    "The dual-regime formulation is statistically decisive over four simpler alternatives "
    "(ΔAICc = 32.7, p < 10⁻⁶), achieving R² = 0.9939. The erfc tail accounts for 47% of the "
    "integrated signal—a result robust to a six-fold variation in the transition width. "
    "Physical self-calibration is demonstrated: the fitted flow rate (0.46 mL/min) agrees with "
    "the pump setting (0.50 mL/min) within 8%, and the Peclet number (Pe = 0.934) independently "
    "confirms the non-Fickian transport mechanism identified via Korsmeyer-Peppas kinetics. "
    "Under steady-state two-phase flow, the oil-phase tracer mass flux (FO = Coil × Qoil) "
    "eliminates water-dilution artifacts and quantitatively tracks oil production rates "
    "(Pearson r = 0.97, RMSD = 8.3%). This framework enables per-interval production allocation "
    "requiring only wellhead measurements and a single shut-in."
)
collapse_and_set_text(paras[2], new_abs)
stats['abstract_condensed'] = f'{len(old_abs)} → {len(new_abs)} chars ({100-len(new_abs)*100//len(old_abs)}% reduction)'
print(f'[OK] Abstract: {stats["abstract_condensed"]}')

# ===================================================================
# 2. BRIDGE PARAGRAPH — Restore (Para 9)
# ===================================================================
bridge_text = (
    "Chemical tracers have been deployed in oilfield operations since the 1950s [15], "
    "progressing from radioactive inter-well waterflood monitors to contemporary partitioning "
    "inter-well tracer tests for residual oil measurement [16,17]. Recent field-scale "
    "multi-tracer campaigns have demonstrated quantitative per-stage production allocation "
    "in fractured horizontal wells [18–20], confirming that tracer-based production profiling "
    "is technically viable at field scale."
)
collapse_and_set_text(paras[9], bridge_text)
stats['bridge_restored'] = f'{len(bridge_text)} chars'
print(f'[OK] Bridge paragraph restored: {stats["bridge_restored"]}')

# ===================================================================
# 3. K-P PARAGRAPH — Fix "butit" (Para 11)
# ===================================================================
# The tracked change ", but" was inserted without trailing space.
# Fix: find run ending with ', but' and add a space
for r in paras[11].findall(f'.//{{{W}}}r'):
    t_elems = r.findall(f'.//{{{W}}}t')
    for t in t_elems:
        if t.text and t.text.rstrip() == ', but':
            t.text = t.text.rstrip() + ' '
            print(f'[OK] Fixed spacing after ", but"')
            break

# ===================================================================
# 4. ADE PARAGRAPH — Add hedging (Para 12)
# ===================================================================
ade_text = get_para_text(paras[12])
# "none of these ADE-based approaches has been coupled" → add "to our knowledge, "
old_claim = 'none of these ADE-based approaches has been coupled'
new_claim = 'to our knowledge, none of these ADE-based approaches has been coupled'
if old_claim in ade_text:
    replace_text_in_runs(paras[12], old_claim, new_claim)
    print(f'[OK] Added hedging to ADE novelty claim')

# "has not been addressed in the literature." → "has not been addressed in the literature to date."
old2 = 'has not been addressed in the literature.'
new2 = 'has not been addressed in the literature to date.'
if old2 in ade_text:
    replace_text_in_runs(paras[12], old2, new2)
    print(f'[OK] Added "to date" to literature gap claim')

# ===================================================================
# 5. MATERIALS PARAGRAPH — Shorten significantly (Para 13)
# ===================================================================
old_mat = get_para_text(paras[13])
new_mat = (
    "Beyond the modeling gap, the choice of tracer carrier material imposes independent "
    "constraints. Coated ceramic proppants exhibit high density (~1.5 g/cm³), impeding "
    "transport in low-viscosity fracturing fluids [35,36]; polystyrene microspheres offer "
    "lower density but limited thermal stability [37,38]; and water-phase release—the "
    "dominant mode in most reported designs—cannot distinguish oil from water production "
    "[23,26]. Epoxy resin has recently emerged as a promising alternative: its cross-linked "
    "network enables sustained, matrix-diffusion-controlled release [39–41], and surface "
    "modification can impart oleophilic selectivity. Integrating this epoxy carrier concept "
    "with a predictive transport model constitutes the dual objective of this work."
)
collapse_and_set_text(paras[13], new_mat)
stats['materials_shortened'] = f'{len(old_mat)} → {len(new_mat)} chars ({100-len(new_mat)*100//len(old_mat)}% reduction)'
print(f'[OK] Materials paragraph: {stats["materials_shortened"]}')

# ===================================================================
# 6. "THIS WORK" PARAGRAPH — Polish (Para 14)
# ===================================================================
# "four complementary lines of evidence: statistical model selection against four alternative
#  formulations, physical self-calibration of the fitted flow rate, consistency of the Peclet
#  number with independent kinetic measurements, and robustness of the signal decomposition
#  to the choice of transition width"
# → More concise version
old_list = (
    "statistical model selection against four alternative formulations, "
    "physical self-calibration of the fitted flow rate, "
    "consistency of the Peclet number with independent kinetic measurements, "
    "and robustness of the signal decomposition to the choice of transition width"
)
new_list = (
    "statistical model selection, physical self-calibration of the fitted flow rate, "
    "consistency of the Peclet number with independent kinetic measurements, "
    "and robustness of the signal decomposition"
)
replace_text_in_runs(paras[14], old_list, new_list)
print(f'[OK] Polished "four lines of evidence" list')

# ===================================================================
# 7. Accept tracked changes + remove highlights
# ===================================================================
for dels in root.findall(f'.//{{{W}}}del'):
    dels.getparent().remove(dels)
for ins in root.findall(f'.//{{{W}}}ins'):
    parent = ins.getparent()
    idx = list(parent).index(ins)
    for child in reversed(list(ins)):
        parent.insert(idx, child)
    parent.remove(ins)
for tag in [f'{{{W}}}ins', f'{{{W}}}del']:
    for elem in root.findall(f'.//{{{W}}}rPr/{tag}'):
        elem.getparent().remove(elem)

hl_count = 0
for hl in root.findall(f'.//{{{W}}}highlight'):
    if hl.get(f'{{{W}}}val', '').lower() == 'yellow':
        hl.getparent().remove(hl)
        hl_count += 1
print(f'[OK] Accepted tracked changes, removed {hl_count} yellow highlights')

# ===================================================================
# 8. Terminology: Two-Component → Dual-Regime
# ===================================================================
terminology_map = [
    ("Two-Component Transport Model", "Dual-Regime Transport Model"),
    ("two-component transport model", "dual-regime transport model"),
    ("Two-component piecewise", "Dual-regime piecewise"),
    ("two-component piecewise", "dual-regime piecewise"),
    ("two-component BTC", "dual-regime BTC"),
    ("two-component model", "dual-regime model"),
    ("two-component structure", "dual-regime structure"),
    ("Dual-component tanh-blended", "Dual-regime tanh-blended"),
    ("dual-component tanh-blended", "dual-regime tanh-blended"),
    ("dual-component formulation", "dual-regime formulation"),
    ("Two-Component", "Dual-Regime"),
    ("two-component", "dual-regime"),
    ("Dual-component", "Dual-regime"),
    ("dual-component", "dual-regime"),
]
name_count = 0
for t_elem in root.iter(f'{{{W}}}t'):
    if t_elem.text:
        orig = t_elem.text
        for old, new in terminology_map:
            t_elem.text = t_elem.text.replace(old, new)
        if t_elem.text != orig:
            name_count += 1
print(f'[OK] Terminology replacements: {name_count} runs')

# ===================================================================
# 9. Clean settings + write
# ===================================================================
if 'word/settings.xml' in all_files:
    sr = etree.fromstring(all_files['word/settings.xml'])
    for tr in sr.findall(f'.//{{{W}}}trackRevisions'):
        tr.getparent().remove(tr)
    all_files['word/settings.xml'] = etree.tostring(sr, xml_declaration=True, encoding='UTF-8', standalone=True)

all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        zout.writestr(name, data)

print(f'\n{"="*60}')
print(f'Saved: {output_path}')
print(f'Summary: {stats}')
