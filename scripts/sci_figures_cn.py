#!/usr/bin/env python3
"""
SCI journal figures — inspired by 3D volumetric rendering style.
Reference: fig1_sci_3d.svg — multi-layer concentric ellipses with opacity gradients,
single warm accent color (#e8903a), ultra-thin 0.8pt strokes, clean white bg.
"""

import os, zlib, base64

OUT = r'c:\Users\郝\Desktop\claude\荧光压裂液'

# ═══ Palette — refined, warm accent inspired by reference ═══
ACCENT   = '#D4743C'  # warm rust-orange (active / highlight)
ACCENT_F = '#FDF1E8'  # light warm fill
BLUE_S   = '#3A7CB8'  # cool blue (structure)
BLUE_F   = '#EAF2F9'
TEAL_S   = '#4A9C7F'  # muted teal (PEG)
TEAL_F   = '#EDF6F2'
GRAY_S   = '#A0A0A0'  # neutral
GRAY_F   = '#F5F5F5'
PURPLE_S = '#8B6DAD'  # processing
PURPLE_F = '#F4F0F8'

T_DARK   = '#2A2A2A'
T_SUB    = '#7A7A7A'
P_BG     = '#FFFFFF'

# ═══ Font sizes ═══
FONT       = 'Microsoft YaHei'
FS_MAIN    = 18   # figure title
FS_PANEL   = 15   # panel label
FS_STAGE   = 14   # stage/subtitle
FS_BODY    = 13   # shape label
FS_ANNO    = 12   # callout/annotation
FS_NOTE    = 11   # footnote
FS_SMALL   = 10   # chemistry labels

def mx_head(pw, ph):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="drawio" version="26.0.0">
  <diagram name="Page-1">
    <mxGraphModel dx="1600" dy="1100" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{pw}" pageHeight="{ph}" math="0" shadow="0" background="{P_BG}">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
'''
mx_foot = '''
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

# ═══ Shape helpers ═══
def rect(id_, x, y, w, h, label, fill, stroke, fs=FS_BODY, bold=False, italic=False, rounded=True, parent='1', extra=''):
    fl = (1 if bold else 0)+(2 if italic else 0); rd = '1' if rounded else '0'
    return f'''<mxCell id="{id_}" value="{label}" style="rounded={rd};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=0.8;fontFamily={FONT};fontSize={fs};fontColor={T_DARK};fontStyle={fl};{extra}" vertex="1" parent="{parent}">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>
'''

def ellipse(id_, x, y, w, h, label, fill, stroke, fs=FS_BODY, bold=False, parent='1', extra=''):
    fl = 1 if bold else 0
    return f'''<mxCell id="{id_}" value="{label}" style="ellipse;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=0.8;fontFamily={FONT};fontSize={fs};fontColor={T_DARK};fontStyle={fl};{extra}" vertex="1" parent="{parent}">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>
'''

def text(id_, x, y, w, h, label, fs=FS_BODY, bold=False, italic=False, align='center', color=T_DARK, parent='1'):
    fl = (1 if bold else 0)+(2 if italic else 0)
    return f'''<mxCell id="{id_}" value="{label}" style="text;html=1;align={align};verticalAlign=middle;fontFamily={FONT};fontSize={fs};fontColor={color};fontStyle={fl};" vertex="1" parent="{parent}">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>
'''

def cylinder(id_, x, y, w, h, label, fill, stroke, fs=FS_BODY, parent='1'):
    return f'''<mxCell id="{id_}" value="{label}" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor={fill};strokeColor={stroke};strokeWidth=0.8;fontFamily={FONT};fontSize={fs};fontColor={T_DARK};size=16;" vertex="1" parent="{parent}">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>
'''

def swimlane(id_, x, y, w, h, title, fill, stroke, fs=FS_STAGE, parent='1'):
    return f'''<mxCell id="{id_}" value="{title}" style="swimlane;startSize=34;fillColor={fill};strokeColor={stroke};strokeWidth=1.2;fontFamily={FONT};fontSize={fs};fontColor={T_DARK};fontStyle=1;swimlaneLine=0;rounded=1;" vertex="1" parent="{parent}">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>
'''

def edge(id_, src, tgt, label='', stroke=GRAY_S, w=1.2, dashed=False, src_x=1, src_y=0.5, tgt_x=0, tgt_y=0.5, parent='1', points=None, extra=''):
    dash = 'dashed=1;' if dashed else ''
    style = f'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={stroke};strokeWidth={w};fontFamily={FONT};fontSize=10;fontColor={stroke};fontStyle=1;exitX={src_x};exitY={src_y};exitDx=0;exitDy=0;entryX={tgt_x};entryY={tgt_y};entryDx=0;entryDy=0;{dash}{extra}'
    pts = '';
    if points: pts = '<Array as="points">'+''.join(f'<mxPoint x="{p[0]}" y="{p[1]}" />' for p in points)+'</Array>'
    return f'''<mxCell id="{id_}" value="{label}" style="{style}" edge="1" parent="{parent}" source="{src}" target="{tgt}">
  <mxGeometry relative="1" as="geometry">{pts}
  </mxGeometry>
</mxCell>
'''

def leader(id_, x1, y1, x2, y2, stroke=GRAY_S, w=0.8, dashed=True):
    d = 'dashed=1;' if dashed else ''
    return f'''<mxCell id="{id_}" value="" style="endArrow=none;html=1;strokeColor={stroke};strokeWidth={w};{d}" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="{x1}" y="{y1}" as="sourcePoint" />
    <mxPoint x="{x2}" y="{y2}" as="targetPoint" />
  </mxGeometry>
</mxCell>
'''

# ═══════════════════════════════════════════
# FIGURE 1 — Core-shell structure
# Inspired by: volumetric multi-layer rendering style
# ═══════════════════════════════════════════
def build_fig1():
    pw, ph = 1300, 860
    xml = mx_head(pw, ph)

    # Title
    xml += text('tt', 180, 8, 940, 36, '图1  改性稀土铝酸盐荧光粉核壳结构及功能切换示意图', fs=FS_MAIN, bold=True)

    # ── Panel (a) ──
    xml += text('pa', 30, 62, 36, 32, 'a', fs=FS_PANEL, bold=True, color=BLUE_S)
    xml += text('pat', 72, 64, 350, 30, '颗粒核壳截面结构', fs=FS_STAGE, bold=True, align='left')

    # Filled concentric ellipses — visible layered cross-section
    # PEG outer layer (teal, largest → smallest filled rings)
    xml += ellipse('peg1', 80, 130, 480, 480, '', TEAL_F, TEAL_S, extra='opacity=85;')
    xml += ellipse('peg2', 110, 160, 420, 420, '', TEAL_F, TEAL_S, extra='opacity=80;')
    xml += ellipse('peg3', 125, 175, 390, 390, '', TEAL_F, TEAL_S, extra='opacity=75;')

    # KH550 middle layer (blue)
    xml += ellipse('kh1', 135, 185, 370, 370, '', BLUE_F, BLUE_S, extra='opacity=85;')
    xml += ellipse('kh2', 155, 205, 330, 330, '', BLUE_F, BLUE_S, extra='opacity=80;')
    xml += ellipse('kh3', 170, 220, 300, 300, '', BLUE_F, BLUE_S, extra='opacity=75;')

    # Core (gray, solid center)
    xml += ellipse('core1', 180, 230, 280, 280, '', GRAY_F, GRAY_S, extra='opacity=90;')
    xml += ellipse('core2', 210, 260, 220, 220, '', GRAY_F, GRAY_S, extra='opacity=85;')

    # Core text label
    xml += text('c1', 240, 390, 160, 32, 'SrAl₂O₄', fs=FS_BODY, bold=True)
    xml += text('c2', 240, 420, 160, 22, 'Eu²⁺,Dy³⁺基体', fs=FS_NOTE, color=T_SUB)

    # Layer labels overlaid on rings
    xml += text('l1_l', 405, 296, 100, 24, 'KH550', fs=FS_BODY, bold=True, color=BLUE_S)
    xml += text('l2_l', 460, 125, 100, 24, 'PEG4000', fs=FS_BODY, bold=True, color=TEAL_S)

    # Leader lines
    xml += leader('d1', 350, 222, 620, 100, TEAL_S, 1.0)
    xml += leader('d2', 315, 335, 620, 162, BLUE_S, 1.0)
    xml += leader('d3', 388, 510, 620, 415, ACCENT, 1.0)

    # Right annotations
    xml += text('r1', 632, 72, 320, 56,
        'PEG4000 物理屏蔽层&#xa;空间位阻效应 · 构象熵排斥&#xa;渗透排斥 · 排除体积效应',
        fs=FS_ANNO, bold=True, color=TEAL_S, align='left')
    xml += text('r2', 632, 148, 320, 56,
        'KH550 硅烷偶联剂化学键合层&#xa;Si−O−Al 共价键锚固于基体表面&#xa;为外层PEG提供有机亲和界面',
        fs=FS_ANNO, bold=True, color=BLUE_S, align='left')
    xml += text('r3', 632, 400, 320, 55,
        '−NH₂ 活性氨基官能团（预置位点）&#xa;PEG脱附后暴露于水相&#xa;与砂岩 Si−OH 发生多模式锚定',
        fs=FS_ANNO, bold=True, color=ACCENT, align='left')

    # Separator
    xml += f'''<mxCell id="sep1" value="" style="endArrow=none;html=1;strokeColor={GRAY_F};strokeWidth=1.5;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="40" y="635" as="sourcePoint" />
    <mxPoint x="1260" y="635" as="targetPoint" />
  </mxGeometry>
</mxCell>
'''

    # ── Panel (b) ──
    xml += text('pb', 30, 658, 36, 32, 'b', fs=FS_PANEL, bold=True, color=TEAL_S)
    xml += text('pbt', 72, 660, 420, 30, '颗粒−岩石界面化学键合细节（放大示意）', fs=FS_STAGE, bold=True, align='left')

    # Rock surface
    xml += rect('rs', 70, 700, 780, 40, '砂岩裂缝壁面  ——  Si−OH 硅羟基密集分布', GRAY_F, GRAY_S, fs=FS_BODY, bold=True, rounded=False)

    for i, xi in enumerate([130, 230, 360, 490, 620, 740]):
        xml += text(f'oh{i}', xi, 688, 40, 18, '–OH', fs=FS_SMALL, italic=True, color=GRAY_S, bold=True)

    # KH550 molecules
    xml += rect('km1', 140, 610, 160, 58, 'KH550 硅烷偶联剂', BLUE_F, BLUE_S, fs=FS_BODY, bold=True)
    xml += rect('km2', 370, 610, 160, 58, 'KH550 硅烷偶联剂', BLUE_F, BLUE_S, fs=FS_BODY, bold=True)
    xml += rect('km3', 610, 610, 160, 58, 'KH550 硅烷偶联剂', BLUE_F, BLUE_S, fs=FS_BODY, bold=True)

    xml += text('bo1', 160, 668, 110, 24, 'Si−O−Al 共价键', fs=FS_SMALL, italic=True, color=BLUE_S, bold=True)
    xml += text('bo2', 390, 668, 110, 24, 'Si−O−Al 共价键', fs=FS_SMALL, italic=True, color=BLUE_S, bold=True)
    xml += text('bo3', 630, 668, 110, 24, 'Si−O−Al 共价键', fs=FS_SMALL, italic=True, color=BLUE_S, bold=True)

    xml += text('nh1', 200, 572, 60, 30, '↑ −NH₂', fs=FS_SMALL, bold=True, color=ACCENT)
    xml += text('nh2', 430, 572, 60, 30, '↑ −NH₂', fs=FS_SMALL, bold=True, color=ACCENT)
    xml += text('nh3', 670, 572, 60, 30, '↑ −NH₂', fs=FS_SMALL, bold=True, color=ACCENT)

    xml += text('pg1', 130, 528, 200, 32, 'PEG4000 链段 ~~~~~~~~', fs=FS_ANNO, italic=True, color=TEAL_S, bold=True)
    xml += text('pg2', 360, 528, 200, 32, 'PEG4000 链段 ~~~~~~~~', fs=FS_ANNO, italic=True, color=TEAL_S, bold=True)
    xml += text('pg3', 600, 528, 200, 32, 'PEG4000 链段 ~~~~~~~~', fs=FS_ANNO, italic=True, color=TEAL_S, bold=True)

    xml += text('am', 800, 530, 470, 90,
        '锚定机制:&#xa;① 静电吸引 (−NH₃⁺ ↔ −SiO⁻)&#xa;② 氢键 (NH ↔ O−Si)&#xa;③ 可能的 Si−O−Si / Si−N 化学缩合',
        fs=FS_NOTE, bold=True, align='left')

    # ── Panel (c) ──
    xml += text('pc', 30, 775, 36, 32, 'c', fs=FS_PANEL, bold=True, color=ACCENT)
    xml += text('pct', 72, 777, 550, 30, '分散态 → 锚定态 功能切换（利用压裂施工时序驱动）', fs=FS_STAGE, bold=True, align='left')

    xml += rect('ds', 80, 815, 230, 62, '分散态（注入阶段）&#xa;PEG 空间位阻稳定悬浮', TEAL_F, TEAL_S, fs=FS_BODY, bold=True)
    xml += f'''<mxCell id="sa" value="关井破胶&#xa;PEG脱附降解" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={ACCENT};strokeWidth=2;fontFamily={FONT};fontSize=10;fontColor={ACCENT};fontStyle=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="ds" target="as">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
'''
    xml += rect('as', 400, 815, 250, 62, '锚定态（关井破胶后）&#xa;−NH₂ 与 Si−OH 多模式锚定', ACCENT_F, ACCENT, fs=FS_BODY, bold=True)

    xml += rect('tr', 700, 815, 300, 62, '触发条件: 过硫酸铵 (NH₄)₂S₂O₈ 氧化&#xa;+ 储层温度 60−150 °C + 6−48 h', GRAY_F, GRAY_S, fs=FS_NOTE, bold=True, italic=True)

    xml += mx_foot
    return xml


# ═══════════════════════════════════════════
# FIGURE 2 — Process flow
# ═══════════════════════════════════════════
def build_fig2():
    pw, ph = 1850, 560
    xml = mx_head(pw, ph)
    xml += text('tt', 300, 8, 1250, 36, '图2  荧光压裂液体系「母液预配 + 在线稀释」现场施工工艺流程图', fs=FS_MAIN, bold=True)

    # Row 1 — Mother liquor
    xml += rect('rh1', 30, 62, 180, 32, '母液预配段', BLUE_F, BLUE_S, fs=FS_BODY, bold=True, extra='opacity=85;')
    xml += rect('m1', 30, 108, 175, 90, '① 改性荧光粉&#xa;② 分散助剂&#xa;③ 去离子水', GRAY_F, GRAY_S, fs=FS_BODY, bold=True)
    xml += edge('e1', 'm1', 'm2')
    xml += rect('m2', 255, 108, 200, 90, '高速剪切分散&#xa;（5000−15000 rpm）&#xa;+ 超声辅助脱泡', BLUE_F, BLUE_S, fs=FS_BODY, bold=True)
    xml += edge('e2', 'm2', 'm3')
    xml += cylinder('m3', 505, 98, 190, 110, '荧光悬浮母液&#xa;（20−80 g/L）&#xa;（优选 40 g/L）', BLUE_F, BLUE_S, fs=FS_BODY)

    xml += f'''<mxCell id="ed1" value="在线计量母液" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={GRAY_S};strokeWidth=1.5;fontFamily={FONT};fontSize=10;fontColor={GRAY_S};fontStyle=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="m3" target="m4">
  <mxGeometry relative="1" as="geometry">
    <Array as="points"><mxPoint x="600" y="240" /><mxPoint x="750" y="240" /></Array>
  </mxGeometry>
</mxCell>
'''

    # Row 2 — Online dilution
    xml += rect('rh2', 30, 280, 210, 32, '在线稀释与泵注段', TEAL_F, TEAL_S, fs=FS_BODY, bold=True, extra='opacity=85;')
    xml += rect('m4', 690, 298, 180, 85, '在线计量泵&#xa;（母液添加量&#xa;0.3−1.0 vol%）', TEAL_F, TEAL_S, fs=FS_BODY, bold=True)
    xml += edge('e4', 'm4', 'm5')
    xml += rect('m5', 920, 298, 180, 85, '静态混合器&#xa;（充分混合均化）', PURPLE_F, PURPLE_S, fs=FS_BODY, bold=True)

    xml += rect('mh', 938, 155, 145, 60, 'HPG 基液主流&#xa;（0.3−1.0 wt%）&#xa;（优选 0.5 wt%）', GRAY_F, GRAY_S, fs=FS_BODY, bold=True)
    xml += f'''<mxCell id="eh" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={GRAY_S};strokeWidth=1.2;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="mh" target="m5">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
'''

    xml += edge('e5', 'm5', 'm6')
    xml += rect('m6', 1150, 298, 180, 85, '荧光压裂液终液', TEAL_F, TEAL_S, fs=FS_BODY, bold=True)
    xml += edge('e6', 'm6', 'm7')
    xml += rect('m7', 1380, 298, 170, 85, '压裂泵车&#xa;（高压泵注）', ACCENT_F, ACCENT, fs=FS_BODY, bold=True)
    xml += edge('e7', 'm7', 'm8')
    xml += rect('m8', 1600, 295, 190, 90, '井口 →&#xa;目标压裂层段', ACCENT_F, ACCENT, fs=FS_BODY, bold=True)

    # Proppant
    xml += rect('mp', 1380, 420, 170, 45, '支撑剂（混合后泵入）', GRAY_F, GRAY_S, fs=FS_NOTE, bold=True, extra='dashed=1;')
    xml += f'''<mxCell id="ep" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={GRAY_S};strokeWidth=0.8;dashed=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;" edge="1" parent="1" source="mp" target="m7">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
'''

    xml += text('fn1', 30, 490, 900, 26,
        '技术标准: SY/T 6376-2008《压裂液通用技术条件》 | SY/T 5107-2016《水基压裂液性能评价方法》',
        fs=FS_NOTE, bold=True, italic=True, color=T_SUB, align='left')
    xml += text('fn2', 30, 518, 1100, 26,
        '适用条件: 储层温度 60−150 °C | 关井破胶 6−48 h | 交联剂 0.1−0.5 vol% | 破胶剂 0.02−0.3 wt%',
        fs=FS_NOTE, bold=True, italic=True, color=T_SUB, align='left')
    xml += mx_foot
    return xml


# ═══════════════════════════════════════════
# FIGURE 3 — Method flowchart
# ═══════════════════════════════════════════
def build_fig3():
    pw, ph = 1150, 1320
    xml = mx_head(pw, ph)
    xml += text('tt', 150, 8, 850, 36, '图3  压裂裂缝荧光示踪方法四阶段流程框图', fs=FS_MAIN, bold=True)

    def make_stage(sid, sy, title, steps, fill, stroke, extra_ann=None):
        bh = 260
        s = swimlane(sid, 60, sy, 1030, bh, f'  {title}', fill, stroke, fs=FS_STAGE)
        px = 30; prev = None
        for i, (label, highlight) in enumerate(steps):
            step_id = f'{sid}s{i}'; w = max(130, len(label)*13 + 40)
            if highlight:
                s += rect(step_id, px, 58, w, 90, label, fill, stroke, fs=FS_BODY, bold=True, parent=sid, extra='opacity=65;strokeWidth=1.5;')
            else:
                s += rect(step_id, px, 58, w, 90, label, fill, stroke, fs=FS_BODY, bold=True, parent=sid)
            if prev:
                s += f'''<mxCell id="{sid}e{i}" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={GRAY_S};strokeWidth=1.2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="{sid}" source="{prev}" target="{step_id}">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
'''
            prev = step_id; px += w + 24
        if extra_ann:
            for aid, ax, ay, aw, ah, atxt, ac in extra_ann:
                s += text(aid, ax, ay, aw, ah, atxt, fs=FS_NOTE, bold=True, italic=True, color=ac, align='left', parent=sid)
        return s, bh

    s1, _ = make_stage('st1', 58, 'I. 注入阶段',
        [('荧光压裂液终液&#xa;+ 支撑剂混合', False),
         ('压裂泵注系统&#xa;高压泵入目标层段', False),
         ('荧光粉随携砂液&#xa;运移至水力裂缝各处', False),
         ('PEG空间位阻&#xa;保障颗粒均匀分散', False)],
        BLUE_F, BLUE_S)
    xml += s1
    xml += f'''<mxCell id="a12" value="停泵关井" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={ACCENT};strokeWidth=2.2;fontFamily={FONT};fontSize=10;fontColor={ACCENT};fontStyle=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="st1" target="st2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
'''

    s2, _ = make_stage('st2', 350, 'II. 关井破胶阶段（储层温度 60−150 °C · 密闭 6−48 h · 过硫酸铵氧化环境）',
        [('过硫酸铵热分解&#xa;产生 SO₄•⁻ 自由基', False),
         ('有机硼交联键&#xa;氧化断裂 → 冻胶解体', True),
         ('SO₄•⁻ 攻击 PEG&#xa;醚键(C−O−C)氧化断链', True),
         ('PEG外层脱附降解&#xa;暴露KH550−NH₂活性基团', True),
         ('−NH₂ 与砂岩 Si−OH&#xa;静电吸引+氢键+缩合锚定', True)],
        ACCENT_F, ACCENT,
        extra_ann=[('s2n', 35, 168, 960, 65,
            'PEG脱附三重协同机制: (i) SO₄•⁻ 自由基攻击PEG醚键(C−O−C)引发氧化链断裂，生成低分子量PEG碎片和含氧低聚物；'
            '(ii) 低分子量产物的水溶性显著增大，从荧光粉表面向水相溶解释放；(iii) 破胶剂分解产生的酸性微环境（局部pH下降）促使PEG醚氧质子化，削弱PEG与硅烷偶联剂内层的物理吸附。',
            T_SUB)])
    xml += s2
    xml += f'''<mxCell id="a23" value="开井返排" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={GRAY_S};strokeWidth=2.2;fontFamily={FONT};fontSize=10;fontColor={GRAY_S};fontStyle=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="st2" target="st3">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
'''

    s3, _ = make_stage('st3', 670, 'III. 返排阶段',
        [('开井返排', False),
         ('破胶残渣 + 未锚定&#xa;荧光粉颗粒 → 排出井筒', False),
         ('锚定于壁面的&#xa;荧光粉牢固保留', True)],
        PURPLE_F, PURPLE_S)
    xml += s3
    xml += text('s3n', 780, 710, 200, 40, '净残留率（锚定率）\n92.7%  > 90%', fs=FS_BODY, bold=True, color=TEAL_S, align='center', parent='st3')
    xml += f'''<mxCell id="a34" value="压后取心作业" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor={GRAY_S};strokeWidth=2.2;fontFamily={FONT};fontSize=10;fontColor={GRAY_S};fontStyle=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="st3" target="st4">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
'''

    s4, _ = make_stage('st4', 990, 'IV. 取心与检测阶段',
        [('压后取心&#xa;获取含裂缝岩心', False),
         ('紫外光源照射&#xa;（波长 365 nm）', False),
         ('观察 / 拍照记录&#xa;裂缝壁面荧光分布', False),
         ('确定压裂液&#xa;实际波及范围', True)],
        TEAL_F, TEAL_S)
    xml += s4
    xml += text('s4n', 830, 1032, 180, 40, '绿色荧光信号\n~520 nm 特征发射', fs=FS_BODY, bold=True, color=TEAL_S, align='center', parent='st4')

    xml += rect('kbox', 180, 1260, 790, 48,
        '核心创新：利用压裂施工自身「注入 → 关井 → 返排」工序时序驱动，无需额外添加触发剂，实现「分散态 → 锚定态」自发功能切换',
        ACCENT_F, ACCENT, fs=FS_STAGE, bold=True, italic=True, extra='opacity=65;strokeWidth=2;')
    xml += mx_foot
    return xml


# ═══ Generate ═══
if __name__ == '__main__':
    for fname, builder, desc in [
        ('fig1_core_shell_structure.drawio', build_fig1, '图1'),
        ('fig2_process_flow.drawio', build_fig2, '图2'),
        ('fig3_method_flowchart.drawio', build_fig3, '图3'),
    ]:
        xml = builder()
        fpath = os.path.join(OUT, fname)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(xml)
        compressed = zlib.compress(xml.encode('utf-8'), level=9)[2:-4]
        b64 = base64.b64encode(compressed).decode('ascii').replace('+', '-').replace('/', '_')
        url = f'https://viewer.diagrams.net/?lightbox=1&edit=_blank&layers=1&nav=1&title={fname}#R{b64}'
        print(f'[{desc}] {len(xml):,} bytes  Preview: {url[:90]}...')
    print('Done.')