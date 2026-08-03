#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Apply Chinese master's thesis formatting standards."""
import sys
from docx import Document
from docx.shared import Pt, Cm, Inches, Emu, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from lxml import etree

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DOC = r'荧光压裂液/论文初稿_v2.docx'
doc = Document(DOC)

# ================================================================
# 1. PAGE SETUP: A4 with Chinese thesis margins
# ================================================================
for section in doc.sections:
    # A4: 210mm x 297mm
    section.page_width  = Cm(21.0)
    section.page_height = Cm(29.7)
    # Margins: top 2.5cm, bottom 2.5cm, left 3.0cm (binding), right 2.5cm
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(3.0)
    section.right_margin  = Cm(2.5)
print('Page: A4, margins: top/bottom 2.5cm, left 3.0cm, right 2.5cm')

# ================================================================
# 2. Define a helper to set Chinese font on a run
# ================================================================
def set_run_font(run, cn_font='宋体', en_font='Times New Roman', size=Pt(12), bold=False):
    """Set both Chinese (east-asia) and Western font on a run."""
    run.font.size = size
    run.font.bold = bold
    run.font.name = en_font
    # Set East-Asian font
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = etree.SubElement(rPr, qn('w:rFonts'))
    rFonts.set(qn('w:eastAsia'), cn_font)
    rFonts.set(qn('w:ascii'), en_font)
    rFonts.set(qn('w:hAnsi'), en_font)

def set_para_spacing(para, line_spacing=1.5, space_before=0, space_after=0):
    """Set paragraph spacing."""
    pf = para.paragraph_format
    pf.line_spacing = line_spacing
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)

# ================================================================
# 3. Process all paragraphs
# ================================================================
print('Formatting paragraphs...')

chinese_body_font = '宋体'
english_body_font = 'Times New Roman'
heading_font_cn = '黑体'
heading_font_en = 'Times New Roman'

for i, para in enumerate(doc.paragraphs):
    t = para.text.strip()
    if not t:
        continue

    style_name = para.style.name
    pf = para.paragraph_format

    # --- TITLE PAGE ---
    if t == '硕士学位论文':
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_para_spacing(para, 1.5, 0, 12)
        for run in para.runs:
            set_run_font(run, heading_font_cn, heading_font_en, Pt(22), bold=True)
        continue

    if '用于压裂裂缝监测的荧光压裂液体系构建与性能研究' in t:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_para_spacing(para, 1.5, 6, 6)
        for run in para.runs:
            set_run_font(run, heading_font_cn, heading_font_en, Pt(18), bold=True)
        continue

    if any(t.startswith(p) for p in ['培养单位', '专    业', '研究方向', '导    师', '研 究 生']):
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_para_spacing(para, 1.5, 0, 0)
        for run in para.runs:
            set_run_font(run, chinese_body_font, english_body_font, Pt(14))
        continue

    # --- CHAPTER HEADINGS (Heading 1: 第一章, 第二章, etc.) ---
    if style_name == 'Heading 1' or any(t.startswith(p) for p in [
        '第一章', '第二章', '第三章', '第四章', '第五章', '第六章',
        '摘  要', 'Abstract', '参考文献', 'Keywords'
    ]):
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_para_spacing(para, 1.5, 12, 6)
        for run in para.runs:
            set_run_font(run, heading_font_cn, heading_font_en, Pt(16), bold=True)
        continue

    # --- SECTION HEADINGS (1.1, 2.1, etc. & 1.2, 1.3) ---
    if (style_name == 'Heading 2' or
        (len(t) < 60 and t[0].isdigit() and '.' in t[:6] and
         t[:4].count('.') == 1 and not t.startswith('1.2.') and not t.startswith('2.2.')
         and not t.startswith('3.2.') and not t.startswith('4.2.'))):
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_para_spacing(para, 1.5, 6, 3)
        for run in para.runs:
            set_run_font(run, heading_font_cn, heading_font_en, Pt(14), bold=True)
        continue

    # --- SUB-SECTION HEADINGS (1.2.1, 2.3.1, etc.) ---
    if len(t) < 60 and t[0].isdigit() and t.count('.') >= 2 and t[:8].replace('.','').replace(' ','').isdigit():
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_para_spacing(para, 1.5, 3, 3)
        for run in para.runs:
            set_run_font(run, heading_font_cn, heading_font_en, Pt(12), bold=True)
        continue

    # --- NORMAL BODY TEXT ---
    # Set alignment
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    # Set line spacing
    set_para_spacing(para, 1.5, 0, 0)
    # First line indent (2 chars ≈ 0.74cm for 小四 12pt Chinese)
    pf.first_line_indent = Cm(0.74)

    # Set font on all runs
    for run in para.runs:
        set_run_font(run, chinese_body_font, english_body_font, Pt(12))

    # Special: paragraphs starting with [图 or [表 or [实验数据 are placeholders
    if t.startswith('[图') or t.startswith('[表') or t.startswith('[实验数据待补充'):
        for run in para.runs:
            set_run_font(run, chinese_body_font, english_body_font, Pt(11))
        # Slightly smaller, keep indent
        pf.first_line_indent = Cm(0.74)

# ================================================================
# 4. Set default paragraph font for the document
# ================================================================
style = doc.styles['Normal']
style.font.name = english_body_font
style.font.size = Pt(12)
style.element.rPr.rFonts.set(qn('w:eastAsia'), chinese_body_font)
pf = style.paragraph_format
pf.line_spacing = 1.5

# ================================================================
# SAVE
# ================================================================
doc.save(DOC)
print(f'Saved to {DOC}')
print('Done: A4 paper, 3cm left binding margin, 宋体12pt body, 黑体 headings, 1.5 line spacing')