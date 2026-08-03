"""Clean manuscript: accept tracked changes, remove yellow highlights, rename Two-Component -> Dual-Regime."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from lxml import etree
import zipfile

doc_path = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_3-revised.docx"
output_path = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_3-revised_clean.docx"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# Read the docx
with zipfile.ZipFile(doc_path, "r") as zin:
    all_files = {name: zin.read(name) for name in zin.namelist()}

# Parse document.xml
root = etree.fromstring(all_files["word/document.xml"])

stats = {"highlights_removed": 0, "tracked_changes_accepted": 0, "name_replacements": 0}

# === 1. Accept tracked changes ===
# Remove <w:ins> wrapper, keep its children
for ins in root.findall(f".//{{{W}}}ins"):
    parent = ins.getparent()
    idx = list(parent).index(ins)
    for child in reversed(list(ins)):
        parent.insert(idx, child)
    parent.remove(ins)
    stats["tracked_changes_accepted"] += 1

# Remove <w:del> and its content entirely
for dels in root.findall(f".//{{{W}}}del"):
    dels.getparent().remove(dels)
    stats["tracked_changes_accepted"] += 1

# Remove rPr ins/del markers
for tag in [f"{{{W}}}ins", f"{{{W}}}del"]:
    for elem in root.findall(f".//{{{W}}}rPr/{tag}"):
        elem.getparent().remove(elem)

print(f"[OK] Accepted tracked changes: {stats['tracked_changes_accepted']}")

# === 2. Remove yellow highlighting ===
for hl in root.findall(f".//{{{W}}}highlight"):
    val = hl.get(f"{{{W}}}val", "")
    if val.lower() == "yellow":
        hl.getparent().remove(hl)
        stats["highlights_removed"] += 1

print(f"[OK] Removed yellow highlights: {stats['highlights_removed']}")

# === 3. Replace terminology ===
phrase_replacements = [
    ("Two-Component Transport Model", "Dual-Regime Transport Model"),
    ("two-component transport model", "dual-regime transport model"),
    ("Two-component piecewise", "Dual-regime piecewise"),
    ("two-component piecewise", "dual-regime piecewise"),
    ("two-component BTC", "dual-regime BTC"),
    ("two-component model", "dual-regime model"),
    ("two-component structure", "dual-regime structure"),
    ("Two-Component", "Dual-Regime"),
    ("two-component", "dual-regime"),
    ("Dual-component tanh-blended", "Dual-regime tanh-blended"),
    ("dual-component tanh-blended", "dual-regime tanh-blended"),
    ("dual-component formulation", "dual-regime formulation"),
    ("Dual-component", "Dual-regime"),
    ("dual-component", "dual-regime"),
]

for t_elem in root.iter(f"{{{W}}}t"):
    if t_elem.text:
        original = t_elem.text
        modified = original
        for old, new in phrase_replacements:
            modified = modified.replace(old, new)
        if modified != original:
            stats["name_replacements"] += 1
            t_elem.text = modified

print(f"[OK] Name replacements: {stats['name_replacements']}")

# === 4. Clean settings.xml ===
if "word/settings.xml" in all_files:
    sr = etree.fromstring(all_files["word/settings.xml"])
    for tr in sr.findall(f".//{{{W}}}trackRevisions"):
        tr.getparent().remove(tr)
    all_files["word/settings.xml"] = etree.tostring(sr, xml_declaration=True, encoding="UTF-8", standalone=True)

# Serialize and write
all_files["word/document.xml"] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)

with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        zout.writestr(name, data)

print(f"\nSaved: {output_path}")
print(f"Total changes: {stats}")
