#!/usr/bin/env python3
"""缩小权利要求和说明书范围"""

import docx

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

# ============================================================
# 1. CLAIM 1 基体：限缩为 SrAl₂O₄:Eu²⁺,Dy³⁺ 一种
# ============================================================
for i, p in enumerate(paras):
    if 'SrAl₂O₄' in p.text and 'Sr₄Al₁₄O₂₅' in p.text and 'CaAl₂O₄' in p.text:
        replace_in_para(p,
            '所述稀土铝酸盐长余辉荧光粉基体为SrAl₂O₄:Eu²⁺,Dy³⁺、Sr₄Al₁₄O₂₅:Eu²⁺,Dy³⁺、CaAl₂O₄:Eu²⁺,Nd³⁺中的一种或多种；',
            '所述稀土铝酸盐长余辉荧光粉基体为SrAl₂O₄:Eu²⁺,Dy³⁺；')
        print(f"P{i}: Claim 1 base narrowed to SrAl₂O₄ only")

# Also narrow description P25 (the 发明内容 first aspect)
for i, p in enumerate(paras):
    if '所述稀土铝酸盐长余辉荧光粉基体为SrAl₂O₄' in p.text and '粒度为' in p.text:
        replace_in_para(p,
            '所述稀土铝酸盐长余辉荧光粉基体为SrAl₂O₄:Eu²⁺,Dy³⁺、Sr₄Al₁₄O₂₅:Eu²⁺,Dy³⁺、CaAl₂O₄:Eu²⁺,Nd³⁺中的一种或多种，优选SrAl₂O₄:Eu²⁺,Dy³⁺，粒度为400~2000目，优选800~1200目（对应中位粒径D50约为8~18 μm）；',
            '所述稀土铝酸盐长余辉荧光粉基体为SrAl₂O₄:Eu²⁺,Dy³⁺，粒度为800~1200目（对应中位粒径D50约为8~18 μm）；')
        print(f"P{i}: Description base + particle size narrowed")
        break

# ============================================================
# 2. CLAIM 3: PEG Mn 从 1000~10000 缩小到 2000~6000
# ============================================================
for i, p in enumerate(paras):
    if '3. 根据权利要求1所述的改性稀土铝酸盐荧光粉' in p.text and 'Mn为1000~10000' in p.text:
        replace_in_para(p,
            '所述聚乙二醇的数均分子量Mn为1000~10000，优选2000~6000，更优选约4000',
            '所述聚乙二醇的数均分子量Mn为2000~6000，优选约4000')
        print(f"P{i}: Claim 3 PEG Mn narrowed to 2000~6000")
        break

# Description P28: PEG Mn
for i, p in enumerate(paras):
    if '外层为聚乙二醇（PEG）物理屏蔽层' in p.text and 'Mn为1000~10000' in p.text:
        replace_in_para(p,
            '所述聚乙二醇的数均分子量Mn为1000~10000，优选2000~6000，更优选4000',
            '所述聚乙二醇的数均分子量Mn为2000~6000，优选4000')
        print(f"P{i}: Description PEG Mn narrowed")
        break

# ============================================================
# 3. CLAIM 4: 粒度从 400~2000目 缩小到 800~1200目
# ============================================================
for i, p in enumerate(paras):
    if '4. 根据权利要求1所述的改性稀土铝酸盐荧光粉' in p.text and '粒度为400~2000目' in p.text:
        replace_in_para(p,
            '所述荧光粉基体的粒度为400~2000目，优选800~1200目。',
            '所述荧光粉基体的粒度为800~1200目。')
        print(f"P{i}: Claim 4 particle size narrowed")
        break

# ============================================================
# 4. CLAIM 7(b): 稠化剂 → 仅HPG
# ============================================================
for i, p in enumerate(paras):
    if '（b）稠化剂，选自羟丙基胍胶（HPG）、瓜尔胶、羧甲基羟丙基胍胶（CMHPG）' in p.text:
        replace_in_para(p,
            '（b）稠化剂，选自羟丙基胍胶（HPG）、瓜尔胶、羧甲基羟丙基胍胶（CMHPG）中的一种或多种，优选HPG，在压裂液终液中的浓度为0.3~1.0 wt%；',
            '（b）稠化剂，为羟丙基胍胶（HPG），在压裂液终液中的浓度为0.3~1.0 wt%；')
        print(f"P{i}: Claim 7(b) thickener narrowed to HPG only")
        break

# Description P40 (thickener in 发明内容)
for i, p in enumerate(paras):
    if '（b）稠化剂，选自羟丙基胍胶（HPG）、瓜尔胶、羧甲基羟丙基胍胶（CMHPG）' in p.text and '优选HPG' in p.text:
        replace_in_para(p,
            '（b）稠化剂，选自羟丙基胍胶（HPG）、瓜尔胶、羧甲基羟丙基胍胶（CMHPG）中的一种或多种，优选HPG，在压裂液终液中的浓度为0.3~1.0 wt%；',
            '（b）稠化剂，为羟丙基胍胶（HPG），在压裂液终液中的浓度为0.3~1.0 wt%；')
        print(f"P{i}: Description thickener narrowed")
        break

# ============================================================
# 5. CLAIM 7(c): 交联剂 → 仅有机硼
# ============================================================
for i, p in enumerate(paras):
    if '（c）交联剂，选自有机硼交联剂、有机锆交联剂或有机钛交联剂' in p.text:
        replace_in_para(p,
            '（c）交联剂，选自有机硼交联剂、有机锆交联剂或有机钛交联剂中的一种或多种，优选有机硼延缓交联剂，在压裂液终液中的浓度为0.1~0.5 vol%；',
            '（c）交联剂，为有机硼延缓交联剂，在压裂液终液中的浓度为0.1~0.5 vol%；')
        print(f"P{i}: Claim 7(c) crosslinker narrowed to organic boron only")
        break

# Description P41 (crosslinker in 发明内容)
for i, p in enumerate(paras):
    if '（c）交联剂，选自有机硼交联剂、有机锆交联剂或有机钛交联剂' in p.text and '优选有机硼' in p.text:
        replace_in_para(p,
            '（c）交联剂，选自有机硼交联剂、有机锆交联剂或有机钛交联剂中的一种或多种，优选有机硼延缓交联剂，在压裂液终液中的浓度为0.1~0.5 vol%；',
            '（c）交联剂，为有机硼延缓交联剂，在压裂液终液中的浓度为0.1~0.5 vol%；')
        print(f"P{i}: Description crosslinker narrowed")
        break

# ============================================================
# 6. CLAIM 7(d): 破胶剂 → 仅过硫酸铵/过硫酸钾
# ============================================================
for i, p in enumerate(paras):
    if '（d）破胶剂，选自过硫酸铵、过硫酸钾、胶囊包裹过硫酸盐或酶破胶剂' in p.text:
        replace_in_para(p,
            '（d）破胶剂，选自过硫酸铵、过硫酸钾、胶囊包裹过硫酸盐或酶破胶剂中的一种或多种，优选过硫酸铵，在压裂液终液中的浓度为0.02~0.3 wt%；',
            '（d）破胶剂，为过硫酸铵或过硫酸钾，在压裂液终液中的浓度为0.02~0.3 wt%；')
        print(f"P{i}: Claim 7(d) breaker narrowed to persulfates only")
        break

# Description P42 (breaker in 发明内容)
for i, p in enumerate(paras):
    if '（d）破胶剂，选自过硫酸铵、过硫酸钾、胶囊包裹过硫酸盐或酶破胶剂' in p.text and '优选过硫酸铵' in p.text:
        replace_in_para(p,
            '（d）破胶剂，选自过硫酸铵、过硫酸钾、胶囊包裹过硫酸盐或酶破胶剂中的一种或多种，优选过硫酸铵，在压裂液终液中的浓度为0.02~0.3 wt%；',
            '（d）破胶剂，为过硫酸铵或过硫酸钾，在压裂液终液中的浓度为0.02~0.3 wt%；')
        print(f"P{i}: Description breaker narrowed")
        break

# ============================================================
# SAVE
# ============================================================
doc.save(r'荧光压裂液/专利申请文件_正式格式_修改版.docx')
print("\n范围缩小完成，已保存。")