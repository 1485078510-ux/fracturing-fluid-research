"""Add 2 references, split P3, add citations."""
import sys, io, re, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from lxml import etree
from copy import deepcopy

doc_path = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_4-intro_rewritten.docx"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def pt(p):
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))

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

def collapse_and_set(p, text):
    ref_rpr = None
    first_r = p.find(f'.//{{{W}}}r')
    if first_r is not None: ref_rpr = first_r.find(f'{{{W}}}rPr')
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

# Load
with zipfile.ZipFile(doc_path, 'r') as zin:
    all_files = {n: zin.read(n) for n in zin.namelist()}
root = etree.fromstring(all_files['word/document.xml'])
body = root.find(f'{{{W}}}body')
all_p = body.findall(f'.//{{{W}}}p')

ref_start = None
for i, p in enumerate(all_p):
    if pt(p).strip() == 'References':
        ref_start = i
        break

# New refs after [35] Berkowitz
new_refs = [
    'OGATA A, BANKS R B. A solution of the differential equation of longitudinal dispersion in porous media. U.S. Geological Survey Professional Paper 411-A, 1961. https://doi.org/10.3133/pp411A',
    'VAN GENUCHTEN M T, WIERENGA P J. Mass transfer studies in sorbing porous media I. Analytical solutions. Soil Science Society of America Journal, 1976, 40(4): 473-480. https://doi.org/10.2136/sssaj1976.03615995004000040011x',
]

# Find [35] in refs
ref35_idx = None
for i in range(ref_start + 1, len(all_p)):
    t = pt(all_p[i]).strip()
    if t.startswith('[35]') and 'BERKOWITZ' in t:
        ref35_idx = i
        break

print(f'[35] at {ref35_idx}')

# Insert new refs after [35]
for j, ref_text in enumerate(new_refs):
    new_p = make_ref_para(36 + j, ref_text)
    all_p[ref35_idx + j].addnext(new_p)
    all_p = body.findall(f'.//{{{W}}}p')

# Renumber old [36]..[44] -> [38]..[46]
all_p = body.findall(f'.//{{{W}}}p')
renum = {}
for old in range(44, 35, -1):
    renum[old] = old + 2

for i in range(ref_start + 1, len(all_p)):
    p = all_p[i]
    t = pt(p).strip()
    m = re.match(r'\[(\d+)\]', t)
    if m:
        old = int(m.group(1))
        if old in renum:
            for r in p.findall(f'.//{{{W}}}r'):
                for te in r.findall(f'.//{{{W}}}t'):
                    if te.text and te.text.startswith(f'[{old}]'):
                        te.text = te.text.replace(f'[{old}]', f'[{renum[old]}]', 1)

print('Renumbered refs')

# Update body citations
for i in range(0, ref_start):
    p = all_p[i]
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

print('Updated body citations')

# Split P3 into P3a + P3b at the non-Fickian transition
all_p = body.findall(f'.//{{{W}}}p')
for p in all_p[:ref_start]:
    t = pt(p).strip()
    if 'For fractured and heterogeneous media, where classical ADE solutions fail' in t:
        idx = t.find('For fractured and heterogeneous media,')
        p3a = t[:idx].strip()
        p3b = t[idx:].strip()
        collapse_and_set(p, p3a)

        new_p = etree.Element(f'{{{W}}}p')
        ppr = etree.SubElement(new_p, f'{{{W}}}pPr')
        etree.SubElement(ppr, f'{{{W}}}jc').set(f'{{{W}}}val', 'both')
        r = etree.SubElement(new_p, f'{{{W}}}r')
        rpr = etree.SubElement(r, f'{{{W}}}rPr')
        etree.SubElement(rpr, f'{{{W}}}rFonts').set(f'{{{W}}}cs', 'Times New Roman')
        te = etree.SubElement(r, f'{{{W}}}t')
        te.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        te.text = p3b
        p.addnext(new_p)
        print(f'Split P3: {len(p3a)}c + {len(p3b)}c')
        break

# Add MIM citation
all_p = body.findall(f'.//{{{W}}}p')
for p in all_p[:ref_start]:
    t = pt(p).strip()
    if 'first-order or multirate mass transfer between fractures and matrix [34]' in t:
        for r in p.findall(f'.//{{{W}}}r'):
            for te in r.findall(f'.//{{{W}}}t'):
                if te.text and 'first-order or multirate mass transfer between fractures and matrix [34]' in te.text:
                    te.text = te.text.replace(
                        'first-order or multirate mass transfer between fractures and matrix [34],',
                        'first-order mass transfer between the two domains [37], with multirate extensions [34],'
                    )
                    print('Added [37] van Genuchten for MIM')
                    break
        break

# Add ADE citation
all_p = body.findall(f'.//{{{W}}}p')
for p in all_p[:ref_start]:
    t = pt(p).strip()
    if 'The classical approach fits an analytical solution' in t:
        for r in p.findall(f'.//{{{W}}}r'):
            for te in r.findall(f'.//{{{W}}}t'):
                if te.text and 'to the observed BTC to recover the transport' in te.text:
                    te.text = te.text.replace(
                        'to the observed BTC to recover the transport',
                        'to the observed BTC [36] to recover the transport'
                    )
                    print('Added [36] Ogata-Banks for ADE')
                    break
        break

# Save
all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(doc_path, 'w', zipfile.ZIP_DEFLATED) as zout:
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
print(f'Refs: {len(rns)}, seq={rns==list(range(1,len(rns)+1))}')

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
print(f'Body: {len(body_refs)}, seq={all(body_refs[i]<=body_refs[i+1] for i in range(len(body_refs)-1))}')
