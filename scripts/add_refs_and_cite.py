"""
Add 3 new references and renumber. Update P3 citations.
"""
import sys, io, re, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from lxml import etree
from copy import deepcopy

doc_path = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_4-intro_rewritten.docx"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def pt(p):
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))

def make_ref_para(num, text):
    """Create a reference paragraph matching existing style."""
    p = etree.Element(f'{{{W}}}p')
    ppr = etree.SubElement(p, f'{{{W}}}pPr')
    # Indentation for reference list
    ind = etree.SubElement(ppr, f'{{{W}}}ind')
    ind.set(f'{{{W}}}left', '420')  # ~0.5 inch
    ind.set(f'{{{W}}}hanging', '420')
    r = etree.SubElement(p, f'{{{W}}}r')
    rpr = etree.SubElement(r, f'{{{W}}}rPr')
    etree.SubElement(rpr, f'{{{W}}}rFonts').set(f'{{{W}}}cs', 'Times New Roman')
    sz = etree.SubElement(rpr, f'{{{W}}}sz')
    sz.set(f'{{{W}}}val', '18')  # 9pt
    t = etree.SubElement(r, f'{{{W}}}t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = f'[{num}] {text}'
    return p

with zipfile.ZipFile(doc_path, 'r') as zin:
    all_files = {n: zin.read(n) for n in zin.namelist()}

root = etree.fromstring(all_files['word/document.xml'])
body = root.find(f'{{{W}}}body')
all_p = body.findall(f'.//{{{W}}}p')

# Find reference list
ref_start = None
for i, p in enumerate(all_p):
    if pt(p).strip() == 'References':
        ref_start = i
        break

# New references to insert after [32] (old numbering)
new_refs = [
    (
        'JULIUSSON E, HORNE R N. Characterization of fractured reservoirs using '
        'tracer and flow-rate data. Water Resources Research, 2013, 49(5): 2327-2342. '
        'https://doi.org/10.1002/wrcr.20220'
    ),
    (
        'HAGGERTY R, GORELICK S M. Multiple-rate mass transfer for modeling '
        'diffusion and surface reactions in media with pore-scale heterogeneity. '
        'Water Resources Research, 1995, 31(10): 2383-2400. '
        'https://doi.org/10.1029/95WR10583'
    ),
    (
        'BERKOWITZ B, CORTIS A, DENTZ M, et al. Modeling non-Fickian transport '
        'in geological formations as a continuous time random walk. Reviews of '
        'Geophysics, 2006, 44(2): RG2003. https://doi.org/10.1029/2005RG000178'
    ),
]

# Find paragraph with [32] (Shook) in reference list
ref32_idx = None
for i in range(ref_start + 1, len(all_p)):
    t = pt(all_p[i]).strip()
    if t.startswith('[32]'):
        ref32_idx = i
        break

print(f"[32] at index {ref32_idx}")

# Insert 3 new reference paragraphs after [32]
for j, ref_text in enumerate(new_refs):
    new_p = make_ref_para(33 + j, ref_text)
    all_p[ref32_idx + j].addnext(new_p)
    all_p = body.findall(f'.//{{{W}}}p')
    print(f"  Inserted new ref [{33+j}]")

# Renumber old [33]→[36], [34]→[37], ... [41]→[44]
# The old refs are now shifted by 3 positions
all_p = body.findall(f'.//{{{W}}}p')
for i in range(ref_start + 1, len(all_p)):
    p = all_p[i]
    t = pt(p).strip()
    m = re.match(r'\[(\d+)\]', t)
    if m:
        old_num = int(m.group(1))
        if old_num >= 33 and old_num <= 41:
            new_num = old_num + 3
            # Update the number in the paragraph text
            for r in p.findall(f'.//{{{W}}}r'):
                for te in r.findall(f'.//{{{W}}}t'):
                    if te.text and te.text.startswith(f'[{old_num}]'):
                        te.text = te.text.replace(f'[{old_num}]', f'[{new_num}]', 1)
            if old_num <= 35:
                print(f"  Renumbered: [{old_num}] -> [{new_num}]")

# Now update all citations in body text (NOT reference list)
# Old [33]→[36], [34]→[37], [35]→[38], ... [41]→[44]
# We need to do this carefully - replace high numbers first to avoid conflicts
renumber_map = {41: 44, 40: 43, 39: 42, 38: 41, 37: 40, 36: 39, 35: 38, 34: 37, 33: 36}

for i in range(0, ref_start):  # body text only
    p = all_p[i]
    if p.tag != f'{{{W}}}p':
        continue
    for r in p.findall(f'.//{{{W}}}r'):
        for te in r.findall(f'.//{{{W}}}t'):
            if te.text is None:
                continue
            orig = te.text
            # Find citation brackets and replace numbers
            def replace_in_bracket(m):
                content = m.group(1)
                parts = re.split(r',', content)
                new_parts = []
                for part in parts:
                    part_s = part.strip()
                    range_m = re.match(r'(\d+)\s*[–\-]\s*(\d+)', part_s)
                    if range_m:
                        a, b = int(range_m.group(1)), int(range_m.group(2))
                        a_new = renumber_map.get(a, a)
                        b_new = renumber_map.get(b, b)
                        new_parts.append(f'{a_new}–{b_new}')
                    elif part_s.isdigit():
                        n = int(part_s)
                        new_parts.append(str(renumber_map.get(n, n)))
                    else:
                        new_parts.append(part)
                return '[' + ','.join(new_parts) + ']'

            new_text = re.sub(r'\[(\d+(?:[–\-]\d+)*(?:,\d+(?:[–\-]\d+)*)*)\]', replace_in_bracket, orig)
            if new_text != orig:
                te.text = new_text

print("Updated body text citations")

# Add new citations to P3 for the methods review
# Find P3 (BTC interpretation paragraph)
for p in all_p[:ref_start]:
    t = pt(p).strip()
    if 'deconvolution-based methods express the BTC' in t:
        # Add citations to the deconvolution, MRMT, and CTRW mentions
        for r in p.findall(f'.//{{{W}}}r'):
            for te in r.findall(f'.//{{{W}}}t'):
                if te.text is None:
                    continue
                # Add [42] after deconvolution mention
                if 'parametric or nonparametric inversion' in te.text:
                    te.text = te.text.replace(
                        'parametric or nonparametric inversion, an approach',
                        'parametric or nonparametric inversion [42], an approach'
                    )
                    print("  Cited [42] for deconvolution")
                # Add [43] after multirate mass transfer
                if 'multirate mass transfer between fractures and matrix' in te.text:
                    te.text = te.text.replace(
                        'multirate mass transfer between fractures and matrix,',
                        'multirate mass transfer between fractures and matrix [43],'
                    )
                    print("  Cited [43] for MRMT")
                # Add [44] after CTRW
                if 'continuous-time random walk (CTRW)' in te.text:
                    te.text = te.text.replace(
                        'continuous-time random walk (CTRW) frameworks',
                        'continuous-time random walk (CTRW) frameworks [44]'
                    )
                    print("  Cited [44] for CTRW")
        break

# Save
all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(doc_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for n, d in all_files.items(): zout.writestr(n, d)

# Verify
root2 = etree.fromstring(all_files['word/document.xml'])
all_p2 = root2.findall(f'.//{{{W}}}p')
ref_start2 = None
for i, p in enumerate(all_p2):
    if pt(p).strip() == 'References':
        ref_start2 = i
        break

refs = []
for i, p in enumerate(all_p2):
    if i >= ref_start2:
        break
    for m in re.finditer(r'\[(\d+(?:[–\-]\d+)*(?:,\d+(?:[–\-]\d+)*)*)\]', pt(p)):
        content = m.group(1)
        for part in re.split(r',', content):
            part = part.strip()
            rm = re.match(r'(\d+)\s*[–\-]\s*(\d+)', part)
            if rm:
                for n in range(int(rm.group(1)), int(rm.group(2))+1):
                    if n not in refs:
                        refs.append(n)
            elif part.isdigit():
                n = int(part)
                if n not in refs:
                    refs.append(n)

print(f'\nBody refs: {len(refs)}, seq={all(refs[i]<=refs[i+1] for i in range(len(refs)-1))}')
print(f'First: [{refs[0]}], Last: [{refs[-1]}]')

# Count ref list entries
ref_count = sum(1 for i in range(ref_start2+1, len(all_p2)) if pt(all_p2[i]).strip())
print(f'Reference list entries: {ref_count}')
