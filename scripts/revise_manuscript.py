"""Revise manuscript: restore deleted bridge para, rename terminology, accept changes, remove highlights."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from lxml import etree
from copy import deepcopy
import zipfile, re

doc_path = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_3-revised.docx"
output_path = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_3-revised_clean.docx"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# Read docx
with zipfile.ZipFile(doc_path, "r") as zin:
    all_files = {name: zin.read(name) for name in zin.namelist()}

root = etree.fromstring(all_files["word/document.xml"])
body = root.find(f"{{{W}}}body")
paras = body.findall(f".//{{{W}}}p")

stats = {"bridge_restored": 0, "highlights_removed": 0, "tracked_changes_fixed": 0, "name_replacements": 0}

# ===================================================================
# 1. RESTORE condensed bridge paragraph between refs [14] and [21]
# ===================================================================
# Para [9] currently contains the tracked deletion. We replace the entire
# paragraph with a restored, condensed version.

bridge_text = (
    "Chemical tracers have been deployed in oilfield operations since the 1950s [15], "
    "progressing from radioactive inter-well waterflood monitors to contemporary "
    "partitioning inter-well tracer tests for residual oil measurement [16,17]. "
    "Recent field-scale multi-tracer campaigns have demonstrated quantitative "
    "per-stage production allocation in fractured horizontal wells [18–20], "
    "confirming that tracer-based production profiling is technically viable at field scale."
)

# Create a new paragraph to replace Para [9]
# First, find Para [9] in the XML
target_p = paras[9]

# Build a new paragraph from scratch, matching the style of Para [7] (a normal intro para)
# Clone the paragraph properties from Para [7] as a template
ref_p = paras[7]
new_p = deepcopy(ref_p)

# Now set the text content: create a single run with the bridge text
# Remove all existing runs from the cloned paragraph
for child in list(new_p):
    tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
    if tag in ("r", "ins", "del", "bookmarkStart", "bookmarkEnd", "commentRangeStart", "commentRangeEnd", "commentReference"):
        new_p.remove(child)

# Create a new run with the bridge text
r_elem = etree.SubElement(new_p, f"{{{W}}}r")
rpr = etree.SubElement(r_elem, f"{{{W}}}rPr")
rfonts = etree.SubElement(rpr, f"{{{W}}}rFonts")
rfonts.set(f"{{{W}}}cs", "Times New Roman")
sz = etree.SubElement(rpr, f"{{{W}}}sz")
sz.set(f"{{{W}}}val", "20")  # 10pt ~= 20 half-pts (common for manuscripts)
t_elem = etree.SubElement(r_elem, f"{{{W}}}t")
t_elem.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
t_elem.text = bridge_text

# Replace the old para in the tree
parent = target_p.getparent()
idx = list(parent).index(target_p)
parent.remove(target_p)
parent.insert(idx, new_p)

stats["bridge_restored"] = 1
print(f"[OK] Restored bridge paragraph with refs [15-20], {len(bridge_text)} chars")

# ===================================================================
# 2. Accept tracked changes
# ===================================================================
# Remove <w:del> elements and their content
for dels in root.findall(f".//{{{W}}}del"):
    dels.getparent().remove(dels)
    stats["tracked_changes_fixed"] += 1

# Remove <w:ins> wrappers, keep children
for ins in root.findall(f".//{{{W}}}ins"):
    parent = ins.getparent()
    idx = list(parent).index(ins)
    for child in reversed(list(ins)):
        parent.insert(idx, child)
    parent.remove(ins)
    stats["tracked_changes_fixed"] += 1

# Remove rPr ins/del markers in remaining runs
for tag in [f"{{{W}}}ins", f"{{{W}}}del"]:
    for elem in root.findall(f".//{{{W}}}rPr/{tag}"):
        elem.getparent().remove(elem)

print(f"[OK] Accepted tracked changes: {stats['tracked_changes_fixed']}")

# ===================================================================
# 3. Remove yellow highlights
# ===================================================================
for hl in root.findall(f".//{{{W}}}highlight"):
    val = hl.get(f"{{{W}}}val", "")
    if val.lower() == "yellow":
        hl.getparent().remove(hl)
        stats["highlights_removed"] += 1

print(f"[OK] Removed yellow highlights: {stats['highlights_removed']}")

# ===================================================================
# 4. Two-Component / dual-component -> Dual-Regime / dual-regime
# ===================================================================
terminology_map = [
    # Longest phrases first to avoid partial matches
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

for t_elem in root.iter(f"{{{W}}}t"):
    if t_elem.text:
        original = t_elem.text
        modified = original
        for old, new in terminology_map:
            modified = modified.replace(old, new)
        if modified != original:
            stats["name_replacements"] += 1
            t_elem.text = modified

print(f"[OK] Name replacements: {stats['name_replacements']}")

# ===================================================================
# 5. Fix "butit" -> "but it" (from tracked change spacing issue)
# ===================================================================
for t_elem in root.iter(f"{{{W}}}t"):
    if t_elem.text and "butit" in t_elem.text:
        t_elem.text = t_elem.text.replace("butit", "but it")
        print(f"[OK] Fixed 'butit' spacing")

# ===================================================================
# 6. Clean settings.xml
# ===================================================================
if "word/settings.xml" in all_files:
    sr = etree.fromstring(all_files["word/settings.xml"])
    for tr in sr.findall(f".//{{{W}}}trackRevisions"):
        tr.getparent().remove(tr)
    all_files["word/settings.xml"] = etree.tostring(sr, xml_declaration=True, encoding="UTF-8", standalone=True)

# ===================================================================
# 7. Serialize & write
# ===================================================================
all_files["word/document.xml"] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)

with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        zout.writestr(name, data)

print(f"\nSaved: {output_path}")
print(f"Summary: {stats}")
