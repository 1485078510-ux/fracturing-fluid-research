#!/usr/bin/env python3
r"""
Generate 3 patent figures in SCI journal style (Nature Publishing Group conventions).

Design principles applied:
- NPG-inspired muted, colorblind-friendly palette
- Arial/Helvetica sans-serif typography (8-10 pt)
- Thin borders (1 pt), no shadows, no 3D effects
- Clean white space, subtle fills with 80-90% opacity
- Panel-based organization with lowercase labels (a, b, c)
- Suitable for direct export to SVG/PDF at 300+ DPI
"""

import os

output_dir = r'c:\Users\郝\Desktop\claude\荧光压裂液'

# ── SCI Journal Color Palette (NPG-inspired) ──
# Structural colors
C_BLUE      = '#4472C4'   # primary blue - KH550 / structures
C_BLUE_LT   = '#D6E4F0'   # light blue fill
C_GREEN     = '#548235'   # green - PEG / success states
C_GREEN_LT  = '#E2EFDA'   # light green fill
C_RED       = '#BF4848'   # red - active groups / key points
C_RED_LT    = '#F5E4E4'   # light red fill
C_ORANGE    = '#C58B3D'   # orange - transitions / warnings
C_ORANGE_LT = '#FBEAD6'   # light orange fill
C_GRAY      = '#808080'   # mid gray - neutral
C_GRAY_DK   = '#595959'   # dark gray - text
C_GRAY_LT   = '#F2F2F2'   # light gray - backgrounds
C_GRAY_BG   = '#FAFAFA'   # off-white page
C_PURPLE    = '#7B5EA7'   # purple - mixing / processing
C_PURPLE_LT = '#E8E2F2'   # light purple fill
C_BLACK     = '#333333'   # soft black for text (not pure #000)
C_WHITE     = '#FFFFFF'

# ── Common XML header/footer for SCI style ──
XML_HEADER = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="drawio" version="26.0.0">
  <diagram name="Page-1">
    <mxGraphModel dx="1200" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{pw}" pageHeight="{ph}" math="0" shadow="0" background="{bg}">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
'''

XML_FOOTER = '''
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

def edge_xml(id_, source, target, label='', style_extra='', points=None):
    """Generate clean SCI-style edge XML."""
    style = f'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={C_GRAY};strokeWidth=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;fontFamily=Arial;fontSize=8;fontColor={C_GRAY_DK};{style_extra}'
    pts = ''
    if points:
        pts = '<Array as="points">' + ''.join(f'<mxPoint x="{p[0]}" y="{p[1]}" />' for p in points) + '</Array>'
    return f'''<mxCell id="{id_}" value="{label}" style="{style}" edge="1" parent="1" source="{source}" target="{target}">
  <mxGeometry relative="1" as="geometry">{pts}
  </mxGeometry>
</mxCell>
'''

def rect(id_, x, y, w, h, label, fill, stroke, font_size=9, bold=False, italic=False, rounded=True, parent='1', extra_style=''):
    """Generate a clean rounded rect."""
    fs = f'fontStyle={(1 if bold else 0) + (2 if italic else 0)}'
    style = f'rounded={"1" if rounded else "0"};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=1;fontFamily=Arial;fontSize={font_size};fontColor={C_BLACK};{fs};{extra_style}'
    return f'''<mxCell id="{id_}" value="{label}" style="{style}" vertex="1" parent="{parent}">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>
'''

def ellipse(id_, x, y, w, h, label, fill, stroke, font_size=8, bold=False, parent='1', extra_style=''):
    """Generate an ellipse."""
    fs = f'fontStyle={(1 if bold else 0)}'
    style = f'ellipse;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=1;fontFamily=Arial;fontSize={font_size};fontColor={C_BLACK};{fs};{extra_style}'
    return f'''<mxCell id="{id_}" value="{label}" style="{style}" vertex="1" parent="{parent}">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>
'''

def text(id_, x, y, w, h, label, font_size=8, bold=False, italic=False, align='center', color=C_BLACK, parent='1'):
    """Generate a text label."""
    fs = f'fontStyle={(1 if bold else 0) + (2 if italic else 0)}'
    style = f'text;html=1;align={align};verticalAlign=middle;fontFamily=Arial;fontSize={font_size};fontColor={color};{fs};'
    return f'''<mxCell id="{id_}" value="{label}" style="{style}" vertex="1" parent="{parent}">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>
'''

def leader_line(id_, x1, y1, x2, y2, stroke=C_GRAY, dash=False):
    """Generate a dashed leader line for callouts."""
    dash_s = 'dashed=1;' if dash else ''
    return f'''<mxCell id="{id_}" value="" style="endArrow=none;html=1;strokeColor={stroke};strokeWidth=0.75;{dash_s}" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="{x1}" y="{y1}" as="sourcePoint" />
    <mxPoint x="{x2}" y="{y2}" as="targetPoint" />
  </mxGeometry>
</mxCell>
'''

def cylinder(id_, x, y, w, h, label, fill, stroke, font_size=9, parent='1'):
    """Generate a cylinder shape."""
    style = f'shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor={fill};strokeColor={stroke};strokeWidth=1;fontFamily=Arial;fontSize={font_size};fontColor={C_BLACK};size=12;'
    return f'''<mxCell id="{id_}" value="{label}" style="{style}" vertex="1" parent="{parent}">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>
'''

def swimlane(id_, x, y, w, h, title, fill, stroke, font_size=10, parent='1'):
    """Generate a swimlane container."""
    style = f'swimlane;startSize=24;fillColor={fill};strokeColor={stroke};strokeWidth=1;fontFamily=Arial;fontSize={font_size};fontColor={C_BLACK};fontStyle=1;swimlaneLine=0;'
    return f'''<mxCell id="{id_}" value="{title}" style="{style}" vertex="1" parent="{parent}">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>
'''


# ═══════════════════════════════════════════════════════════════
# FIGURE 1 — Core-Shell Structure Schematic
# SCI style: clean cross-section with detail callout panel
# ═══════════════════════════════════════════════════════════════
def build_fig1():
    pw, ph = 1050, 680
    xml = XML_HEADER.format(pw=pw, ph=ph, bg=C_WHITE)

    # ── Panel (a) label ──
    xml += text('2', 25, 18, 30, 20, 'a', font_size=12, bold=True, color=C_BLACK)
    xml += text('3', 60, 20, 280, 20, 'Core-shell particle structure', font_size=10, bold=True, color=C_BLACK, align='left')

    # ── Three concentric circles for core-shell ──
    # PEG outer layer (draw first = back)
    xml += ellipse('10', 60, 70, 370, 370, '', C_GREEN_LT, C_GREEN, extra_style='opacity=85;')
    # KH550 middle layer
    xml += ellipse('11', 100, 110, 290, 290, '', C_BLUE_LT, C_BLUE, extra_style='opacity=85;')
    # Core
    xml += ellipse('12', 140, 150, 210, 210, '', C_GRAY_LT, C_GRAY, extra_style='opacity=90;')

    # ── Layer labels (on the structure itself) ──
    xml += text('13', 170, 300, 150, 25, 'SrAl₂O₄', font_size=9, bold=True, color=C_GRAY_DK)
    xml += text('14', 170, 318, 150, 25, 'Eu²⁺,Dy³⁺', font_size=8, color=C_GRAY)

    # KH550 ring label
    xml += text('15', 315, 220, 120, 20, 'KH550', font_size=8, bold=True, color=C_BLUE)

    # PEG ring label
    xml += text('16', 345, 70, 120, 20, 'PEG4000', font_size=8, bold=True, color=C_GREEN)

    # ── Callout lines from structure to labels ──
    xml += leader_line('20', 265, 160, 480, 80, C_GREEN)
    xml += leader_line('21', 240, 245, 480, 115, C_BLUE)
    xml += leader_line('22', 290, 380, 480, 260, C_RED)

    # ── Right-side annotations ──
    xml += text('23', 485, 65, 200, 35,
        'PEG physical shielding layer\n(steric repulsion + osmotic exclusion)',
        font_size=7.5, color=C_GREEN, align='left')
    xml += text('24', 485, 108, 200, 35,
        'KH550 chemical bonding layer\n(Si−O−Al covalent anchor)',
        font_size=7.5, color=C_BLUE, align='left')

    # -NH2 callout
    xml += text('25', 485, 248, 200, 35,
        '−NH₂ active amino groups\n(exposed after PEG desorption)',
        font_size=7.5, color=C_RED, align='left', bold=True)

    # ── Separation line ──
    xml += f'''<mxCell id="30" value="" style="endArrow=none;html=1;strokeColor={C_GRAY_LT};strokeWidth=1;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="40" y="460" as="sourcePoint" />
    <mxPoint x="710" y="460" as="targetPoint" />
  </mxGeometry>
</mxCell>
'''

    # ── Panel (b) — Molecular-level detail ──
    xml += text('31', 25, 475, 30, 20, 'b', font_size=12, bold=True, color=C_BLACK)
    xml += text('32', 60, 477, 280, 20, 'Chemical bonding detail at the particle–rock interface', font_size=10, bold=True, color=C_BLACK, align='left')

    # Rock surface
    xml += rect('40', 60, 610, 660, 160, 'Sandstone fracture surface (Si−OH)', C_GRAY_LT, C_GRAY, font_size=9, bold=False, rounded=False)

    # Surface -OH groups
    for xi in [120, 220, 320, 420, 520]:
        xml += text(f's{xi}', xi, 600, 35, 18, '−OH', font_size=7, color=C_GRAY, italic=True)

    # KH550 molecules
    xml += rect('50', 120, 530, 100, 40, 'KH550 silane', C_BLUE_LT, C_BLUE, font_size=8, bold=True)
    xml += rect('51', 320, 530, 100, 40, 'KH550 silane', C_BLUE_LT, C_BLUE, font_size=8, bold=True)

    # Si-O-Al bond annotation
    xml += text('52', 140, 570, 65, 20, 'Si−O−Al', font_size=7, italic=True, color=C_BLUE)
    xml += text('53', 340, 570, 65, 20, 'Si−O−Al', font_size=7, italic=True, color=C_BLUE)

    # -NH2 on KH550
    xml += text('54', 155, 498, 65, 25, '↑ −NH₂', font_size=7, bold=True, color=C_RED)
    xml += text('55', 355, 498, 65, 25, '↑ −NH₂', font_size=7, bold=True, color=C_RED)

    # PEG chains above
    xml += text('56', 110, 460, 130, 25, 'PEG4000 chains ~~~~~~~~', font_size=7, color=C_GREEN, italic=True)
    xml += text('57', 310, 460, 130, 25, 'PEG4000 chains ~~~~~~~~', font_size=7, color=C_GREEN, italic=True)

    # Anchoring arrow labels
    xml += text('58', 440, 500, 260, 70,
        'Anchoring mechanism:\n• Electrostatic attraction (−NH₃⁺ ↔ −SiO⁻)\n'
        '• Hydrogen bonding (NH↔O−Si)\n• Possible Si−O−Si / Si−N condensation',
        font_size=7.5, color=C_BLACK, align='left')

    # ── Panel (c) — State switching ──
    xml += text('60', 720, 18, 30, 20, 'c', font_size=12, bold=True, color=C_BLACK)
    xml += text('61', 755, 20, 270, 20, 'Dispersion → Anchoring switch', font_size=10, bold=True, color=C_BLACK, align='left')

    # Dispersion state
    xml += rect('62', 730, 60, 130, 50, 'Dispersion state\n(injection phase)', C_GREEN_LT, C_GREEN, font_size=8, bold=False)
    # Arrow
    xml += f'''<mxCell id="63" value="PEG desorption" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={C_ORANGE};strokeWidth=1.5;fontFamily=Arial;fontSize=7;fontColor={C_ORANGE};exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="62" target="64">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
'''
    # Anchoring state
    xml += rect('64', 900, 60, 130, 50, 'Anchoring state\n(post-breakdown)', C_RED_LT, C_RED, font_size=8, bold=False)

    # Trigger annotation
    xml += text('65', 845, 120, 80, 25, 'Trigger:', font_size=7, bold=True, color=C_GRAY_DK, align='right')
    xml += text('66', 845, 140, 80, 25, '(NH₄)₂S₂O₈ + ΔT', font_size=7, color=C_ORANGE, align='right', italic=True)

    # ── Legend ──
    xml += text('70', 730, 200, 60, 18, 'Legend', font_size=8, bold=True, color=C_BLACK, align='left')
    legend_items = [
        (C_GRAY_LT, C_GRAY, 'SrAl₂O₄:Eu,Dy core'),
        (C_BLUE_LT, C_BLUE, 'KH550 bonding layer'),
        (C_GREEN_LT, C_GREEN, 'PEG shielding layer'),
        (C_RED, C_RED, '−NH₂ active group'),
    ]
    yi = 222
    for fill, stroke, txt in legend_items:
        xml += rect(f'L{yi}', 730, yi, 16, 12, '', fill, stroke, rounded=False)
        xml += text(f'L{yi}t', 752, yi, 180, 12, txt, font_size=7, color=C_BLACK, align='left')
        yi += 18

    # Figure caption guidance
    xml += text('80', 25, 645, 700, 25,
        'Fig. 1 | Core-shell structure of the modified rare-earth aluminate phosphor and its functional switching mechanism.',
        font_size=8, italic=True, color=C_GRAY, align='left')

    xml += XML_FOOTER
    return xml


# ═══════════════════════════════════════════════════════════════
# FIGURE 2 — Process Flow Diagram
# SCI style: clean horizontal flow, minimal design
# ═══════════════════════════════════════════════════════════════
def build_fig2():
    pw, ph = 1550, 480
    xml = XML_HEADER.format(pw=pw, ph=ph, bg=C_WHITE)

    # ── Title ──
    xml += text('2', 25, 15, 30, 22, 'a', font_size=12, bold=True, color=C_BLACK)
    xml += text('3', 60, 17, 300, 22, 'Mother-liquor preparation &amp; online dilution process', font_size=10, bold=True, color=C_BLACK, align='left')

    # ── Row 1: Mother Liquor Preparation ──
    xml += text('4', 30, 55, 160, 18, 'Mother-liquor preparation', font_size=8, bold=True, color=C_BLUE, align='left')

    # Raw materials
    xml += rect('10', 30, 80, 130, 60, 'Modified\nphosphor\n+ Additives\n+ DI water', C_GRAY_LT, C_GRAY, font_size=8)

    # Arrow
    xml += edge_xml('11', '10', '20')

    # Shear mixing
    xml += rect('20', 200, 80, 130, 60, 'High-shear\ndispersion\n(5,000−15,000 rpm)\n+ Ultrasonication', C_BLUE_LT, C_BLUE, font_size=8)

    # Arrow
    xml += edge_xml('21', '20', '30')

    # Mother liquor tank
    xml += cylinder('30', 370, 72, 130, 76, 'Fluorescent\nmother liquor\n(20−80 g/L)', C_BLUE_LT, C_BLUE, font_size=8)

    # Down arrow with label
    xml += f'''<mxCell id="31" value="Online metering" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={C_GRAY};strokeWidth=1;fontFamily=Arial;fontSize=7;fontColor={C_GRAY};exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="30" target="40">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="435" y="185" />
      <mxPoint x="610" y="185" />
    </Array>
  </mxGeometry>
</mxCell>
'''

    # ── Row 2: Online Dilution and Pumping ──
    xml += text('32', 30, 210, 180, 18, 'Online dilution &amp; pumping', font_size=8, bold=True, color=C_GREEN, align='left')

    # Metering pump
    xml += rect('40', 560, 210, 120, 55, 'Online metering\npump\n(0.3−1.0 vol%)', C_GREEN_LT, C_GREEN, font_size=8)

    # Arrow
    xml += edge_xml('41', '40', '50')

    # Static mixer
    xml += rect('50', 720, 210, 130, 55, 'Static mixer', C_PURPLE_LT, C_PURPLE, font_size=9, bold=True)

    # HPG inlet from top
    xml += rect('55', 735, 110, 100, 45, 'HPG base fluid\n(0.3−1.0 wt%)', C_GRAY_LT, C_GRAY, font_size=8)
    xml += f'''<mxCell id="56" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={C_GRAY};strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="55" target="50">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
'''

    # Arrow
    xml += edge_xml('51', '50', '60')

    # Final fluid
    xml += rect('60', 890, 210, 130, 55, 'Fluorescent\nfracturing fluid', C_GREEN_LT, C_GREEN, font_size=9, bold=True)

    # Arrow
    xml += edge_xml('61', '60', '70')

    # Pump truck
    xml += rect('70', 1060, 210, 120, 55, 'Fracturing\npump truck', C_ORANGE_LT, C_ORANGE, font_size=9, bold=False)

    # Arrow
    xml += edge_xml('71', '70', '80')

    # Wellhead / target zone
    xml += rect('80', 1220, 205, 130, 55, 'Wellhead →\nTarget formation', C_RED_LT, C_RED, font_size=8, bold=True)

    # ── Bottom annotations ──
    xml += text('90', 30, 310, 400, 25,
        'Compliance: SY/T 6376-2008 &amp; SY/T 5107-2016 | Conditions: T = 60−150 °C, shut-in 6−48 h',
        font_size=7, color=C_GRAY, align='left', italic=True)

    # Proppant addition note
    xml += rect('92', 1060, 290, 120, 45, 'Proppant\n(blended before\npumping)', C_GRAY_LT, C_GRAY, font_size=7.5, rounded=True, extra_style='dashed=1;')
    xml += f'''<mxCell id="93" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={C_GRAY};strokeWidth=0.75;dashed=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;" edge="1" parent="1" source="92" target="70">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
'''

    # Flow direction indicator
    xml += text('95', 30, 370, 530, 20, '← Flow direction →', font_size=7, color=C_GRAY, align='center', italic=True)

    # Figure caption
    xml += text('96', 25, 430, 700, 25,
        'Fig. 2 | Mother-liquor pre-mixing and online dilution process for preparing fluorescent fracturing fluid at the wellsite.',
        font_size=8, italic=True, color=C_GRAY, align='left')

    xml += XML_FOOTER
    return xml


# ═══════════════════════════════════════════════════════════════
# FIGURE 3 — Method Flowchart (4-stage)
# SCI style: clean vertical phases, subtle color-coding
# ═══════════════════════════════════════════════════════════════
def build_fig3():
    pw, ph = 980, 1050
    xml = XML_HEADER.format(pw=pw, ph=ph, bg=C_WHITE)

    # ── Title ──
    xml += text('2', 25, 12, 30, 22, '', font_size=0, bold=True)  # no panel label needed
    xml += text('3', 40, 14, 500, 22, 'Fracturing fluorescence tracing method — four-stage workflow', font_size=10, bold=True, color=C_BLACK, align='left')

    # ── Stage box builder ──
    def stage_box(sid, sy, title, steps, fill, stroke, accent_color):
        """Build a stage swimlane with step boxes inside."""
        box_h = 190
        s = f'''<mxCell id="{sid}" value="  {title}" style="swimlane;startSize=26;fillColor={fill};strokeColor={stroke};strokeWidth=1.25;fontFamily=Arial;fontSize=10;fontColor={C_BLACK};fontStyle=1;swimlaneLine=0;rounded=1;" vertex="1" parent="1">
  <mxGeometry x="40" y="{sy}" width="900" height="{box_h}" as="geometry" />
</mxCell>
'''
        prev_id = None
        x_start = 30
        for i, (label, is_key) in enumerate(steps):
            step_id = f'{sid}s{i}'
            step_w = max(110, len(label) * 7 + 20)
            if is_key:
                s += rect(step_id, x_start, 50, step_w, 60, label, accent_color if 'LT' not in accent_color else f'{accent_color}', stroke, font_size=8, bold=True, parent=sid, extra_style='opacity=70;')
            else:
                s += rect(step_id, x_start, 50, step_w, 60, label, fill, stroke, font_size=8, parent=sid)

            if prev_id:
                s += f'''<mxCell id="{sid}e{i}" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={C_GRAY};strokeWidth=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="{sid}" source="{prev_id}" target="{step_id}">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
'''
            prev_id = step_id
            x_start += step_w + 30

        # Extra annotation
        if sid == 'st2':
            s += text(f'{sid}note', 30, 120, 840, 50, 'PEG desorption mechanism: (i) SO₄•⁻ radical attack on PEG ether bonds → chain scission  (ii) Low-MW fragments dissolve  (iii) Acidic micro-environment weakens physisorption',
                font_size=7, italic=True, color=C_GRAY, align='left', parent=sid)

        return s

    # ── Stage I: Injection ──
    xml += stage_box('st1', 50,
        'I. Injection phase',
        [('Fluorescent fluid\n+ proppant', False),
         ('Pumped into\ntarget zone', False),
         ('Phosphor transported\ninto fracture', False),
         ('Uniform dispersion\n(PEG steric stability)', False)],
        C_BLUE_LT, C_BLUE, C_BLUE)

    # Arrow I → II
    xml += f'''<mxCell id="a12" value="Shut-in" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={C_ORANGE};strokeWidth=1.75;fontFamily=Arial;fontSize=8;fontColor={C_ORANGE};fontStyle=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="st1" target="st2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
'''

    # ── Stage II: Shut-in & Breakdown ──
    xml += stage_box('st2', 270,
        'II. Shut-in &amp; breakdown phase (60–150 °C, 6–48 h)',
        [('(NH₄)₂S₂O₈\n→ SO₄•⁻', False),
         ('Gel network\ndegradation', True),
         ('PEG oxidative\ndesorption', True),
         ('−NH₂ exposure\non KH550', True),
         ('Anchoring to\nSi−OH on rock', True)],
        C_ORANGE_LT, C_ORANGE, f'{C_ORANGE}')

    # Arrow II → III
    xml += f'''<mxCell id="a23" value="Flowback" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={C_GRAY};strokeWidth=1.75;fontFamily=Arial;fontSize=8;fontColor={C_GRAY};fontStyle=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="st2" target="st3">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
'''

    # ── Stage III: Flowback ──
    xml += stage_box('st3', 510,
        'III. Flowback phase',
        [('Wellbore\nflowback', False),
         ('Residue + unanchored\nphosphor → expelled', False),
         ('Anchored phosphor\nretained on fracture face', True)],
        C_PURPLE_LT, C_PURPLE, C_PURPLE)

    # Annotation: retention rate
    xml += text('st3note', 750, 560, 160, 30, 'Net retention\n> 90%', font_size=8, bold=True, color=C_GREEN, align='center', parent='st3')

    # Arrow III → IV
    xml += f'''<mxCell id="a34" value="Coring" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={C_GRAY};strokeWidth=1.75;fontFamily=Arial;fontSize=8;fontColor={C_GRAY};fontStyle=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="st3" target="st4">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
'''

    # ── Stage IV: Coring & Detection ──
    xml += stage_box('st4', 750,
        'IV. Coring &amp; detection phase',
        [('Post-frac\ncoring', False),
         ('UV illumination\n(365 nm)', False),
         ('Fluorescence\nimaging', False),
         ('Map fluid-covered\nfracture area', True)],
        C_GREEN_LT, C_GREEN, C_GREEN)

    # Green emission note
    xml += text('st4note', 780, 800, 120, 30, 'Green emission\n~520 nm', font_size=8, bold=True, color=C_GREEN, align='center', parent='st4')

    # ── Bottom: Key innovation summary ──
    xml += rect('99', 230, 980, 520, 40,
        'Key innovation: Spontaneous "dispersion → anchoring" switch driven by fracturing sequence (inject → shut-in → flowback); no external triggering agent required.',
        C_RED_LT, C_RED, font_size=9, bold=True, italic=True, extra_style='opacity=70;')

    # Figure caption
    xml += text('100', 40, 1020, 800, 22,
        'Fig. 3 | Method workflow for fracturing fluorescence tracing, illustrating the four operational stages and the chemical switching mechanism.',
        font_size=8, italic=True, color=C_GRAY, align='left')

    xml += XML_FOOTER
    return xml


# ═══════════════════════════════════════════════════════════════
# Write files
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    builds = [
        ('fig1_core_shell_structure.drawio', build_fig1),
        ('fig2_process_flow.drawio', build_fig2),
        ('fig3_method_flowchart.drawio', build_fig3),
    ]

    for fname, builder in builds:
        xml = builder()
        fpath = os.path.join(output_dir, fname)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(xml)
        print(f'[OK] {fname}  ({len(xml):,} bytes)')

    print(f'\nAll 3 SCI-style figures saved to: {output_dir}')
    print('Open in draw.io desktop or https://app.diagrams.net/ to export as SVG/PDF (vector, journal-ready).')