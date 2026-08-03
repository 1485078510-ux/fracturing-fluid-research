# -*- coding: utf-8 -*-
"""Insert OMML math equations into ESP_polished_final.docx paragraph [148]."""
from docx import Document
from docx.oxml.ns import qn
from lxml import etree

MATH_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
M = '{%s}' % MATH_NS

def mr(text=''):
    """Math run with text."""
    e = etree.Element(M + 'r')
    if text:
        t = etree.SubElement(e, M + 't')
        t.text = text
        t.set(qn('xml:space'), 'preserve')
    return e

def msub(base, sub):
    e = etree.Element(M + 'sSub')
    e1 = etree.SubElement(e, M + 'e'); e1.append(mr(base))
    e2 = etree.SubElement(e, M + 'sub'); e2.append(mr(sub))
    return e

def mfrac(num, den):
    e = etree.Element(M + 'f')
    n = etree.SubElement(e, M + 'num'); n.append(mr(num))
    d = etree.SubElement(e, M + 'den'); d.append(mr(den))
    return e

def msqrt(arg):
    e = etree.Element(M + 'rad')
    a = etree.SubElement(e, M + 'e'); a.append(mr(arg))
    return e

def mfunc(name, arg):
    e = etree.Element(M + 'func')
    fn = etree.SubElement(e, M + 'fName'); fn.append(mr(name))
    a = etree.SubElement(e, M + 'e'); a.append(mr(arg))
    return e

def momath(*children):
    om = etree.Element(M + 'oMath')
    for c in children:
        om.append(c)
    return om

def add_eq(para, omath, label):
    """Add an oMath equation + right-aligned label to a paragraph."""
    mp = etree.Element(M + 'oMathPara')
    mp.append(omath)
    # Add to paragraph via a run
    r = etree.SubElement(para._element, qn('w:r'))
    r.append(mp)
    # Label run
    r2 = etree.SubElement(para._element, qn('w:r'))
    t = etree.SubElement(r2, qn('w:t'))
    t.text = '      ' + label
    t.set(qn('xml:space'), 'preserve')

# ===== Load =====
DST = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\ESP_with_eqs.docx'
SRC = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\ESP_polished_final.docx'
doc = Document(SRC)
p = doc.paragraphs[148]

# Clear existing runs
for r in list(p.runs):
    p._element.remove(r._element)

# ===== Eq (6): C(t) = w(t)·C_rise(t) + [1-w(t)]·C_fall(t) =====
eq6 = momath(
    mr('C(t) = w(t)·'),
    msub('C', 'rise'),
    mr('(t) + [1-w(t)]·'),
    msub('C', 'fall'),
    mr('(t)'),
)
add_eq(p, eq6, '(6)')

# ===== Eq (6a): C_rise(t) = c_b + (A·d)/sqrt(16alphaQt) · exp[-...] =====
eq6a = momath(
    msub('C', 'rise'),
    mr('(t) = '),
    msub('c', 'b'),
    mr(' + '),
    mfrac('A·d', '√(16αQt)'),
    mr(' exp[-'),
    mfrac('(xπd² - 4Qt)²', '16αQtπd²'),
    mr(']'),
)
add_eq(p, eq6a, '(6a)')

# ===== Eq (6b): C_fall(t) = c_b + a/2 · erfc(...) =====
eq6b = momath(
    msub('C', 'fall'),
    mr('(t) = '),
    msub('c', 'b'),
    mr(' + '),
    mfrac('a', '2'),
    mr(' erfc('),
    mfrac('4Qt - xπd²', '√(16αQtπd²)'),
    mr(')'),
)
add_eq(p, eq6b, '(6b)')

# ===== Eq (6c): w(t) = 1/2 [1 + tanh((t0-t)/sigma)] =====
eq6c = momath(
    mr('w(t) = '),
    mfrac('1', '2'),
    mr(' [1 + tanh('),
    mfrac('t₀ - t', 'σ'),
    mr(')]'),
)
add_eq(p, eq6c, '(6c)')

doc.save(DST)
print("Equations (6)-(6c) inserted as OMML into ESP_polished_final.docx")
print("Open in Word to view. Use 'Professional' display mode if equations appear linear.")