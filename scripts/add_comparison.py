#!/usr/bin/env python3
"""调整过度缩小的范围 + 补充对比实验"""

import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

doc = docx.Document(r'荧光压裂液/专利申请文件_正式格式_修改版.docx')
paras = doc.paragraphs

def replace_in_para(para, old, new):
    full = para.text
    if old in full:
        new_full = full.replace(old, new)
        for i, run in enumerate(para.runs):
            if i == 0:
                run.text = new_full
            else:
                run.text = ''

def insert_paragraphs_before(ref_element, texts):
    """Insert multiple paragraphs before ref_element."""
    prev = ref_element
    for text in reversed(texts):
        new_p = OxmlElement('w:p')
        new_r = OxmlElement('w:r')
        new_t = OxmlElement('w:t')
        new_t.text = text
        new_t.set(qn('xml:space'), 'preserve')
        new_r.append(new_t)
        new_p.append(new_r)
        prev.addprevious(new_p)

# ============================================================
# STEP 1: Relax over-narrowed claims
# ============================================================

# 1a. Claim 1: revert phosphor base from 1 to 3 types
for i, p in enumerate(paras):
    txt = p.text.strip()
    if txt.startswith('所述稀土铝酸盐长余辉荧光粉基体为SrAl'):
        # Check if it's narrowed to just SrAl2O4 (no Sr4Al14O25)
        if 'SrAl₂O₄:Eu' in txt and 'Sr₄Al' not in txt and 'CaAl₂O₄' not in txt:
            replace_in_para(p,
                '所述稀土铝酸盐长余辉荧光粉基体为SrAl₂O₄:Eu²⁺,Dy³⁺；',
                '所述稀土铝酸盐长余辉荧光粉基体为SrAl₂O₄:Eu²⁺,Dy³⁺、Sr₄Al₁₄O₂₅:Eu²⁺,Dy³⁺或CaAl₂O₄:Eu²⁺,Nd³⁺中的一种或多种，优选SrAl₂O₄:Eu²⁺,Dy³⁺；')
            print(f"P{i}: Claim 1 phosphor base relaxed to 3 types")
            break

# 1b. Description: revert phosphor base + particle size
for i, p in enumerate(paras):
    if 'SrAl' in p.text and '800~1200目' in p.text:
        if 'Sr₄Al' not in p.text and 'CaAl' not in p.text:
            # Narrowed version - relax it
            old_d = '所述稀土铝酸盐长余辉荧光粉基体为SrAl₂O₄:Eu²⁺,Dy³⁺，粒度为800~1200目（对应中位粒径D50约为8~18 μm）；'
            new_d = '所述稀土铝酸盐长余辉荧光粉基体为SrAl₂O₄:Eu²⁺,Dy³⁺、Sr₄Al₁₄O₂₅:Eu²⁺,Dy³⁺或CaAl₂O₄:Eu²⁺,Nd³⁺中的一种或多种，优选SrAl₂O₄:Eu²⁺,Dy³⁺，粒度为400~2000目，优选800~1200目（对应中位粒径D50约为8~18 μm）；'
            if old_d in p.text:
                replace_in_para(p, old_d, new_d)
                print(f"P{i}: Description base + particle size relaxed")
                break

# 1c. Claim 4: revert particle size
for i, p in enumerate(paras):
    if '4. 根据权利要求1所述的改性稀土铝酸盐荧光粉' in p.text and '粒度为800~1200目。' in p.text:
        replace_in_para(p,
            '所述荧光粉基体的粒度为800~1200目。',
            '所述荧光粉基体的粒度为400~2000目，优选800~1200目。')
        print(f"P{i}: Claim 4 particle size relaxed")
        break

# 1d. Claim 7(b): relax thickener from HPG only to HPG + guar gum
for i, p in enumerate(paras):
    if '（b）稠化剂，为羟丙基胍胶（HPG），在压裂液终液中的浓度为0.3~1.0 wt%；' in p.text:
        replace_in_para(p,
            '（b）稠化剂，为羟丙基胍胶（HPG），在压裂液终液中的浓度为0.3~1.0 wt%；',
            '（b）稠化剂，为羟丙基胍胶（HPG）或瓜尔胶，优选HPG，在压裂液终液中的浓度为0.3~1.0 wt%；')
        print(f"P{i}: Claim 7(b) thickener relaxed")
        break

# 1e. Description thickener also relax
relaxed_thick = False
for i, p in enumerate(paras):
    txt = p.text.strip()
    if txt == '（b）稠化剂，为羟丙基胍胶（HPG），在压裂液终液中的浓度为0.3~1.0 wt%；':
        if i < 110 and not relaxed_thick:
            replace_in_para(p,
                '（b）稠化剂，为羟丙基胍胶（HPG），在压裂液终液中的浓度为0.3~1.0 wt%；',
                '（b）稠化剂，为羟丙基胍胶（HPG）或瓜尔胶，优选HPG，在压裂液终液中的浓度为0.3~1.0 wt%；')
            print(f"P{i}: Description thickener relaxed")
            relaxed_thick = True
            break

print("--- Relaxation complete ---")

# ============================================================
# STEP 2: Read and insert comparative experiment
# ============================================================
with open('scripts/comp_exp_content.txt', 'r', encoding='utf-8') as f:
    content = f.read()

comp_exp_paragraphs = [p.strip() for p in content.split('===') if p.strip()]
print(f"Read {len(comp_exp_paragraphs)} comparison experiment paragraphs")

# Find the concluding paragraph
ref_text = '以上实施例仅为本发明的优选实施方式，用于说明而非限定本发明的技术方案。'
for i, p in enumerate(paras):
    if ref_text in p.text:
        insert_paragraphs_before(p._element, comp_exp_paragraphs)
        print(f"P{i}: Inserted {len(comp_exp_paragraphs)} comparison paragraphs")
        break

# ============================================================
# SAVE
# ============================================================
doc.save(r'荧光压裂液/专利申请文件_正式格式_修改版.docx')
print("\nAll changes saved.")