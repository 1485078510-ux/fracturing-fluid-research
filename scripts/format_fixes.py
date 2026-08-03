# -*- coding: utf-8 -*-
"""Fix formatting: Fe3O4 -> Fe₃O₄ (subscript), [refs] -> superscript."""
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt
import re
from copy import deepcopy

SRC = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\ESP_with_eqs.docx'
DST = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\ESP_formatted.docx'
doc = Document(SRC)

def make_subscript(run, text):
    """Create a subscript run."""
    r = deepcopy(run)
    r.text = text
    r.font.subscript = True
    return r

def make_superscript(run, text):
    """Create a superscript run."""
    r = deepcopy(run)
    r.text = text
    r.font.superscript = True
    return r

def make_normal(run, text):
    """Create a normal run."""
    r = deepcopy(run)
    r.text = text
    r.font.subscript = False
    r.font.superscript = False
    return r

def process_paragraph(para):
    """Fix Fe3O4 subscripts and reference superscripts in a paragraph."""
    new_runs = []

    for run in para.runs:
        text = run.text
        if not text:
            new_runs.append(run)
            continue

        # Process text for both Fe3O4 and references
        # We'll rebuild the run by splitting on patterns
        pieces = []
        remaining = text
        last_end = 0

        # Find all patterns: Fe3O4 variations and reference patterns [digits,-]
        # Pattern for Fe3O4 or Fe3O4@SA or nano-Fe3O4 etc.
        # Pattern for references: [1], [1-5], [1,2], [6,7], [1-5,8,10-12]
        pattern = r'(Fe\d+O\d+(?:@\w+)?)|(\[\d+(?:[-,]\d+)*\])'

        for m in re.finditer(pattern, text):
            start, end = m.start(), m.end()
            matched = m.group(0)

            # Add text before this match
            if start > last_end:
                pieces.append(('normal', text[last_end:start]))

            # Determine type
            if matched.startswith('Fe') or matched.startswith('nano-Fe'):
                pieces.append(('fe3o4', matched))
            elif matched.startswith('['):
                pieces.append(('ref', matched))
            else:
                pieces.append(('normal', matched))

            last_end = end

        # Add remaining text
        if last_end < len(text):
            pieces.append(('normal', text[last_end:]))

        if not pieces:
            new_runs.append(run)
            continue

        # Build new runs from pieces
        for ptype, ptext in pieces:
            if ptype == 'normal':
                new_runs.append(make_normal(run, ptext))
            elif ptype == 'fe3o4':
                # Split Fe3O4 into Fe(sub 3)O(sub 4)
                # Match: (Fe)(3)(O)(4)(@SA)?
                fm = re.match(r'(nano-)?(Fe)(\d+)(O)(\d+)(@\w+)?', ptext)
                if fm:
                    prefix = fm.group(1) or ''
                    fe = fm.group(2)
                    num3 = fm.group(3)
                    o = fm.group(4)
                    num4 = fm.group(5)
                    suffix = fm.group(6) or ''

                    if prefix:
                        # nano- is part of first run
                        new_runs.append(make_normal(run, prefix))
                    new_runs.append(make_normal(run, fe))
                    new_runs.append(make_subscript(run, num3))
                    new_runs.append(make_normal(run, o))
                    new_runs.append(make_subscript(run, num4))
                    if suffix:
                        new_runs.append(make_normal(run, suffix))
                else:
                    new_runs.append(make_normal(run, ptext))
            elif ptype == 'ref':
                new_runs.append(make_superscript(run, ptext))

    # Replace runs in paragraph
    if new_runs:
        # Clear existing runs
        for run in para.runs:
            run._element.getparent().remove(run._element)
        # Add new runs
        for run in new_runs:
            para._element.append(run._element)

# Process all paragraphs
count_fe3o4 = 0
count_ref = 0
for para in doc.paragraphs:
    text = para.text
    if 'Fe3O4' in text or 'Fe3O4' in text:
        count_fe3o4 += 1
    if re.search(r'\[\d', text):
        count_ref += 1
    process_paragraph(para)

doc.save(DST)
print(f"Formatted: {count_fe3o4} paragraphs with Fe3O4, {count_ref} paragraphs with references")
print(f"Saved: {DST}")