"""
Focused polish of Introduction section in ESP-T manuscript.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from lxml import etree
from copy import deepcopy
import zipfile, re

doc_path = r"四氧化三铁环氧树脂拟合/ESP-T_投稿文件/ESP-T_Final_3-revised_clean.docx"
output_path = doc_path

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def pt(p):
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))

def collapse_and_set_text(p, new_text):
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
    c = 0
    for t_elem in p.iter(f'{{{W}}}t'):
        if t_elem.text and old in t_elem.text:
            t_elem.text = t_elem.text.replace(old, new)
            c += 1
    return c

# Load
with zipfile.ZipFile(doc_path, 'r') as zin:
    all_files = {name: zin.read(name) for name in zin.namelist()}

root = etree.fromstring(all_files['word/document.xml'])
body = root.find(f'{{{W}}}body')
paras = body.findall(f'.//{{{W}}}p')

# Find intro paragraphs by content
intro_start = None
refs_start = None
for i, p in enumerate(paras):
    txt = pt(p).strip()
    if txt == '1. Introduction':
        intro_start = i
    if txt == '2. Experimental Section':
        exp_start = i
        break

edits = []

# Map paragraphs by function (using text content matching)
p_map = {}
for i in range(intro_start + 1, exp_start):
    txt = pt(paras[i])
    p_map[i] = txt

# ================================================================
# PARA 7 (Energy context) — fix grammar issues
# ================================================================
for i, txt in p_map.items():
    if 'Global primary energy consumption' in txt:
        # Fix 1: "Unconventional reservoirs, tight oil..." → parenthetical
        old = "Unconventional reservoirs, tight oil, shale gas, and coalbed methane, account for"
        new = "Unconventional reservoirs (tight oil, shale gas, and coalbed methane) account for"
        n = replace_in_para(paras[i], old, new)

        # Fix 2: "stages, the industry still lacks" → semicolon
        old2 = "stages, the industry still lacks"
        new2 = "stages; yet the industry still lacks"
        n2 = replace_in_para(paras[i], old2, new2)

        if n or n2:
            edits.append(f"Para {i}: fixed grammar (parentheses + semicolon)")
        break

# ================================================================
# PARA 10 (Proppant designs) — minor tightening
# ================================================================
for i, txt in p_map.items():
    if 'tracer proppant, a composite particle that immobilizes' in txt:
        new_txt = (
            "The tracer proppant—a composite particle that immobilizes a tracer agent "
            "within a solid carrier and is co-injected with fracturing fluid—offers a "
            "distinct advantage over dissolved tracers: the tracer remains in the "
            "fracture after a single placement, enabling long-term, stage-specific "
            "monitoring without repeated intervention [21]. Recent designs encompass "
            "ceramic carriers with rhodamine 6G [21] or carbon quantum dots [22], "
            "rare-earth-doped polymer coatings for multi-element coding [23], "
            "oleophilic Fe₃O₄/polystyrene microspheres for selective oil-phase "
            "release [24], polymer-coated proppants with dual near-zone and far-zone "
            "tracer codes [25], multi-colored dye-tracer proppants for quantitative "
            "flowback assessment [26], and marked proppant transport studies [27]."
        )
        collapse_and_set_text(paras[i], new_txt)
        edits.append(f"Para {i}: tightened proppant designs ({len(new_txt)} chars)")
        break

# ================================================================
# PARA 12 (ADE framework) — condense + split
# ================================================================
for i, txt in p_map.items():
    if 'one-dimensional advection-dispersion equation (ADE)' in txt:
        # Part A: ADE background + brief literature
        part_a = (
            "The one-dimensional advection-dispersion equation (ADE), "
            "∂C/∂t + v·∂C/∂x = D·∂²C/∂x², provides the canonical framework "
            "for solute transport in tubular and porous-media flow; its analytical "
            "solutions were comprehensively compiled by van Genuchten and Alves [31]. "
            "Within petroleum engineering, the ADE has been applied to inter-well "
            "tracer tests for reservoir characterization [16,32] and recently "
            "extended to two-phase porous media [33] and multi-stage fractured "
            "wells with tracer transfer [34]."
        )
        # Part B: The gap
        part_b = (
            "Critically, however, to our knowledge none of these ADE-based "
            "approaches has incorporated a sustained-release source term "
            "representing matrix-diffusion-controlled tracer liberation from "
            "a polymeric carrier. Inter-well tracer applications treat the source "
            "as a known pulse [16,32]; a tracer proppant presents a coupled inverse "
            "problem in which neither the release function nor the transport "
            "parameters are known independently. The observed breakthrough curve "
            "reflects their convolution. This coupled release-transport problem "
            "has not been addressed in the literature to date. Its practical "
            "consequence is that existing tracer proppants can confirm which "
            "stages are producing but cannot quantify production rates from "
            "the breakthrough curve alone: the information encoded in the curve "
            "shape—flow rate, dispersion, and the relative contributions of "
            "shut-in slug and sustained release—remains uninterpreted."
        )

        collapse_and_set_text(paras[i], part_a)
        edits.append(f"Para {i}: condensed ADE review ({len(part_a)} chars)")

        # Insert part_b as new paragraph
        new_p = deepcopy(paras[i])
        collapse_and_set_text(new_p, part_b)
        parent = paras[i].getparent()
        idx = list(parent).index(paras[i])
        parent.insert(idx + 1, new_p)
        edits.append(f"Para {i}+1: standalone gap paragraph ({len(part_b)} chars)")
        break

# ================================================================
# PARA 14 (This work) — remove Results detail, focus on approach
# ================================================================
for i, txt in p_map.items():
    if 'In this work, we address both the transport-modeling gap' in txt:
        new_txt = (
            "In this work, we address both the transport-modeling gap and the "
            "material-design challenge at the single-interval laboratory scale. "
            "On the modeling side, we develop a piecewise ADE-based formulation "
            "that decomposes the breakthrough curve into a Gaussian pulse (shut-in "
            "accumulation slug) and an erfc tail (sustained matrix-diffusion-"
            "controlled release), linked by a smooth tanh transition that ensures "
            "C¹ continuity. The six-parameter model is validated through statistical "
            "model selection, physical self-calibration, mechanistic consistency "
            "checks, and parametric robustness analysis; we further demonstrate "
            "that simple time-of-arrival methods fail for this class of breakthrough "
            "curves. On the material side, we synthesize an oleophilic epoxy/Fe₃O₄ "
            "tracer proppant (ESP-T) via emulsion polymerization, with stearic "
            "acid-modified nano-Fe₃O₄ imparting oleophilic character for selective "
            "oil-phase release. Under steady-state two-phase flow, the oil-phase "
            "tracer mass flux is used to eliminate water-dilution artifacts and "
            "quantitatively track per-interval oil production rates."
        )
        collapse_and_set_text(paras[i], new_txt)
        edits.append(f"Para {i}: removed Results-level detail ({len(new_txt)} chars)")
        break

# ================================================================
# Write
# ================================================================
all_files['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        zout.writestr(name, data)

print(f"Saved: {output_path}")
print(f"Changes ({len(edits)}):")
for e in edits:
    print(f"  - {e}")
