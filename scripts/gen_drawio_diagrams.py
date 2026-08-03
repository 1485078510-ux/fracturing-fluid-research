# -*- coding: utf-8 -*-
"""Generate 3D-styled patent diagrams as .drawio XML."""
import os, html

OUT = r'c:\Users\郝\Desktop\claude\荧光压裂液\diagrams'

def wrap(inner_cells, w, h, name="Page-1"):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="drawio" version="26.0.0">
  <diagram name="{name}">
    <mxGraphModel dx="1400" dy="1000" grid="1" gridSize="10" guides="1" pageWidth="{w}" pageHeight="{h}">
      <root><mxCell id="0"/><mxCell id="1" parent="0"/>{inner_cells}</root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

# ================================================================
# FIG 1 — 3D Core-Shell Sphere with extrusion & radial gradient
# ================================================================
def fig1():
    cid = [2]
    def nid(): v=cid[0]; cid[0]+=1; return str(v)

    cells = []
    cells.append(f'<mxCell id="{nid()}" value="图1  改性稀土铝酸盐荧光粉颗粒结构" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=18;fontStyle=1;fontColor=#1a1a2e;" vertex="1" parent="1"><mxGeometry x="200" y="20" width="500" height="40" as="geometry"/></mxCell>')

    # === 3D SPHERE using layered ellipses ===
    cx, cy, r = 440, 380, 160  # center & radius

    # Shadow (bottom-right offset)
    cells.append(f'<mxCell id="{nid()}" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#CCCCCC;strokeColor=none;opacity=30;" vertex="1" parent="1"><mxGeometry x="{cx-r+15}" y="{cy-r+15}" width="{2*r}" height="{2*r}" as="geometry"/></mxCell>')

    # PEG outer layer — 3D: multiple offset rings
    for i, (off, alpha, dash) in enumerate([(0, 60, '8 4'), (3, 40, '6 4'), (6, 25, '4 4')]):
        cells.append(f'<mxCell id="{nid()}" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#F28E2B;strokeWidth=3;dashed=1;dashPattern={dash};opacity={alpha};" vertex="1" parent="1"><mxGeometry x="{cx-r-15-off}" y="{cy-r-15-off}" width="{2*(r+15)+2*off}" height="{2*(r+15)+2*off}" as="geometry"/></mxCell>')
    # PEG glow ring
    cells.append(f'<mxCell id="{nid()}" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#FDEBD0;strokeWidth=8;opacity=25;" vertex="1" parent="1"><mxGeometry x="{cx-r-18}" y="{cy-r-18}" width="{2*(r+18)}" height="{2*(r+18)}" as="geometry"/></mxCell>')

    # KH550 layer — purple ring with extrusion
    cells.append(f'<mxCell id="{nid()}" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#6C3483;strokeWidth=12;opacity=80;" vertex="1" parent="1"><mxGeometry x="{cx-r+3}" y="{cy-r+3}" width="{2*r-6}" height="{2*r-6}" as="geometry"/></mxCell>')
    cells.append(f'<mxCell id="{nid()}" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#AF7AC5;strokeWidth=10;" vertex="1" parent="1"><mxGeometry x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" as="geometry"/></mxCell>')

    # Core — blue sphere with gradient-like layering
    cells.append(f'<mxCell id="{nid()}" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#1a5276;strokeColor=none;opacity=70;" vertex="1" parent="1"><mxGeometry x="{cx-r+25}" y="{cy-r+25}" width="{2*r-50}" height="{2*r-50}" as="geometry"/></mxCell>')
    cells.append(f'<mxCell id="{nid()}" value="SrAl2O4" style="ellipse;whiteSpace=wrap;html=1;fillColor=#2E86C1;strokeColor=#1B4F72;strokeWidth=3;fontColor=#FFFFFF;fontSize=18;fontStyle=1;gradientColor=#2874A6;gradientDirection=north;" vertex="1" parent="1"><mxGeometry x="{cx-r+30}" y="{cy-r+30}" width="{2*r-60}" height="{2*r-60}" as="geometry"/></mxCell>')

    # Core label
    cells.append(f'<mxCell id="{nid()}" value="Eu2+,Dy3+" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=14;fontColor=#AED6F1;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="{cx-60}" y="{cy+30}" width="120" height="25" as="geometry"/></mxCell>')

    # Annotations — cleaner callout lines
    # KH550 callout
    cells.append(f'<mxCell id="{nid()}" value="" style="endArrow=classic;html=1;strokeColor=#AF7AC5;strokeWidth=2;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{cx}" y="{cy-r+5}" as="sourcePoint"/><mxPoint x="690" y="260" as="targetPoint"/></mxGeometry></mxCell>')
    cells.append(f'<mxCell id="{nid()}" value="&lt;b&gt;&lt;font color=&quot;#8E44AD&quot;&gt;KH550 化学锚固层&lt;/font&gt;&lt;/b&gt;&lt;br&gt;Si-O-Al 共价键合" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=13;" vertex="1" parent="1"><mxGeometry x="700" y="230" width="220" height="50" as="geometry"/></mxCell>')

    # PEG callout
    cells.append(f'<mxCell id="{nid()}" value="" style="endArrow=classic;html=1;strokeColor=#F28E2B;strokeWidth=2;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{cx-100}" y="{cy+140}" as="sourcePoint"/><mxPoint x="700" y="360" as="targetPoint"/></mxGeometry></mxCell>')
    cells.append(f'<mxCell id="{nid()}" value="&lt;b&gt;&lt;font color=&quot;#E67E22&quot;&gt;PEG4000 物理屏蔽层&lt;/font&gt;&lt;/b&gt;&lt;br&gt;空间位阻 + 水合屏障" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=13;" vertex="1" parent="1"><mxGeometry x="700" y="335" width="240" height="50" as="geometry"/></mxCell>')

    # Legend panel — 3D card
    cells.append(f'<mxCell id="{nid()}" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8F9FA;strokeColor=#BDC3C7;strokeWidth=1;shadow=1;" vertex="1" parent="1"><mxGeometry x="100" y="620" width="700" height="80" as="geometry"/></mxCell>')
    for i, (color, label) in enumerate([('#2E86C1', 'SrAl2O4:Eu2+,Dy3+ 基体'), ('#AF7AC5', 'KH550 硅烷偶联剂'), ('#F28E2B', 'PEG4000 聚乙二醇')]):
        lx = 140 + i*230
        cells.append(f'<mxCell id="{nid()}" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#333;strokeWidth=1;" vertex="1" parent="1"><mxGeometry x="{lx-12}" y="640" width="24" height="24" as="geometry"/></mxCell>')
        cells.append(f'<mxCell id="{nid()}" value="{label}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=12;fontColor=#333;" vertex="1" parent="1"><mxGeometry x="{lx+20}" y="637" width="180" height="30" as="geometry"/></mxCell>')

    return wrap(''.join(cells), 960, 750, "Fig1-3D-CoreShell")


# ================================================================
# FIG 2 — 3D Floating Cards with depth
# ================================================================
def fig2():
    cid = [2]
    def nid(): v=cid[0]; cid[0]+=1; return str(v)
    cells = []
    cells.append(f'<mxCell id="{nid()}" value="图2  "分散态 → 锚定态" 功能切换机制" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=18;fontStyle=1;fontColor=#1a1a2e;" vertex="1" parent="1"><mxGeometry x="250" y="15" width="550" height="45" as="geometry"/></mxCell>')

    panels = [
        (30, 80, 340, '阶段一：注入（分散态）', '#2E86C1', '#EBF5FB',
         ['PEG 水合层完整', '空间位阻排斥', '颗粒均匀悬浮于 HPG 基液'],
         [(40,60),(100,120),(160,80),(60,200),(140,170),(80,280),(170,230),(50,330),(150,300)],
         [(40,60),(100,120),(160,80),(60,200),(140,170),(80,280)]),
        (410, 80, 340, '阶段二：关井破胶（过渡态）', '#E74C3C', '#FDEDEC',
         ['过硫酸铵氧化降解 PEG', 'PEG 链断裂脱落', 'KH550 活性氨基暴露'],
         [(60,80),(150,120),(100,200),(60,280),(160,250),(110,330)],
         [(60,80),(150,120),(100,200),(60,280),(160,250)]),
        (790, 80, 340, '阶段三：返排后（锚定态）', '#27AE60', '#E8F8F5',
         ['氨基-硅羟基锚定', '静电吸引 + 氢键 + 化学缩合', '净残留率 > 90%'],
         [(50,120),(130,180),(80,260),(150,240),(60,340)],
         [(50,120),(130,180),(80,260),(150,240)]),
    ]

    for x, y, w, title, accent, bg, desc_lines, all_particles, halo_particles in panels:
        h = 440
        # 3D shadow card
        cells.append(f'<mxCell id="{nid()}" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#BBB;strokeColor=none;opacity=40;" vertex="1" parent="1"><mxGeometry x="{x+5}" y="{y+5}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        # Main card
        cells.append(f'<mxCell id="{nid()}" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor={bg};strokeColor={accent};strokeWidth=2;shadow=1;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        # Title bar — gradient fills for 3D
        cells.append(f'<mxCell id="{nid()}" value="{title}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={accent};strokeColor=none;fontColor=#FFFFFF;fontSize=15;fontStyle=1;gradientColor={accent};gradientDirection=east;" vertex="1" parent="1"><mxGeometry x="{x+10}" y="{y+10}" width="{w-20}" height="50" as="geometry"/></mxCell>')
        # Particles with halos
        for px, py in halo_particles:
            pelx, pely = x+px, y+py+70
            cells.append(f'<mxCell id="{nid()}" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#F28E2B;strokeWidth=2;dashed=1;dashPattern=5 3;opacity=50;" vertex="1" parent="1"><mxGeometry x="{pelx-21}" y="{pely-21}" width="42" height="42" as="geometry"/></mxCell>')
            cells.append(f'<mxCell id="{nid()}" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#2E86C1;strokeColor=#AF7AC5;strokeWidth=2;" vertex="1" parent="1"><mxGeometry x="{pelx-13}" y="{pely-13}" width="26" height="26" as="geometry"/></mxCell>')
        # Description
        for i, line in enumerate(desc_lines):
            cells.append(f'<mxCell id="{nid()}" value="{line}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=12;fontColor=#555;" vertex="1" parent="1"><mxGeometry x="{x+15}" y="{y+h-80+25*i}" width="{w-30}" height="22" as="geometry"/></mxCell>')

    # 3D arrows between panels
    for x1, x2, label_text, color in [(375, 405, '破胶', '#E74C3C'), (755, 785, '接触壁面', '#27AE60')]:
        cells.append(f'<mxCell id="{nid()}" value="" style="endArrow=classic;html=1;strokeColor={color};strokeWidth=4;shadow=1;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{x1}" y="300" as="sourcePoint"/><mxPoint x="{x2}" y="300" as="targetPoint"/></mxGeometry></mxCell>')
        cells.append(f'<mxCell id="{nid()}" value="{label_text}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;fontColor={color};" vertex="1" parent="1"><mxGeometry x="{x1-10}" y="265" width="60" height="25" as="geometry"/></mxCell>')

    # Bottom timeline arrow
    cells.append(f'<mxCell id="{nid()}" value="" style="endArrow=classic;startArrow=classic;html=1;strokeColor=#95A5A6;strokeWidth=2;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="50" y="560" as="sourcePoint"/><mxPoint x="1120" y="560" as="targetPoint"/></mxGeometry></mxCell>')
    cells.append(f'<mxCell id="{nid()}" value="时间序列：注入 (h)  →  关井破胶 (6-48 h)  →  返排 (d)  →  取心检测" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=12;fontStyle=1;fontColor=#7F8C8D;" vertex="1" parent="1"><mxGeometry x="250" y="568" width="670" height="30" as="geometry"/></mxCell>')

    return wrap(''.join(cells), 1200, 620, "Fig2-3D-Switching")


# ================================================================
# FIG 3 — Isometric Process Flow
# ================================================================
def fig3():
    cid = [2]
    def nid(): v=cid[0]; cid[0]+=1; return str(v)
    cells = []
    cells.append(f'<mxCell id="{nid()}" value="图3  "母液预配 + 在线稀释" 现场施工工艺流程" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=18;fontStyle=1;fontColor=#1a1a2e;" vertex="1" parent="1"><mxGeometry x="200" y="15" width="700" height="45" as="geometry"/></mxCell>')

    # Pipeline — 3D extruded
    cells.append(f'<mxCell id="{nid()}" value="" style="endArrow=none;html=1;strokeColor=#BDC3C7;strokeWidth=8;rounded=1;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="100" y="360" as="sourcePoint"/><mxPoint x="1100" y="360" as="targetPoint"/></mxGeometry></mxCell>')
    cells.append(f'<mxCell id="{nid()}" value="" style="endArrow=none;html=1;strokeColor=#ECF0F1;strokeWidth=5;rounded=1;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="102" y="358" as="sourcePoint"/><mxPoint x="1098" y="358" as="targetPoint"/></mxGeometry></mxCell>')

    nodes = [
        (200, 360, '母液配制罐', '改性荧光粉 + 水\n+ 分散助剂\n40 g/L', '#2E86C1'),
        (400, 360, '计量泵', '隔膜式\n精度 ±1%', '#8E44AD'),
        (600, 360, '静态混合器', 'SMX型 DN50\n稀释比 0.5% v/v', '#E67E22'),
        (800, 360, '混砂车', '荧光压裂液\n+ 20/40目支撑剂', '#27AE60'),
        (1000, 360, '高压泵组', '→ 井筒\n→ 裂缝', '#E74C3C'),
    ]

    for i, (nx, ny, name, desc, accent) in enumerate(nodes):
        # 3D node: shadow + main + highlight
        cells.append(f'<mxCell id="{nid()}" value="{i+1}" style="ellipse;whiteSpace=wrap;html=1;fillColor=#999;strokeColor=none;opacity=35;" vertex="1" parent="1"><mxGeometry x="{nx-24}" y="{ny-24}" width="48" height="48" as="geometry"/></mxCell>')
        cells.append(f'<mxCell id="{nid()}" value="{i+1}" style="ellipse;whiteSpace=wrap;html=1;fillColor={accent};strokeColor=#FFFFFF;strokeWidth=3;fontColor=#FFFFFF;fontSize=18;fontStyle=1;shadow=1;" vertex="1" parent="1"><mxGeometry x="{nx-28}" y="{ny-28}" width="56" height="56" as="geometry"/></mxCell>')
        # Name above
        cells.append(f'<mxCell id="{nid()}" value="&lt;b&gt;{name}&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=14;fontColor={accent};" vertex="1" parent="1"><mxGeometry x="{nx-70}" y="285" width="140" height="35" as="geometry"/></mxCell>')
        # Desc below (on card)
        cells.append(f'<mxCell id="{nid()}" value="{desc}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8F9FA;strokeColor={accent};strokeWidth=1;align=center;verticalAlign=middle;fontSize=10;fontColor=#555;shadow=1;" vertex="1" parent="1"><mxGeometry x="{nx-65}" y="390" width="130" height="55" as="geometry"/></mxCell>')
        # Flow arrow
        if i < 4:
            nx2 = nodes[i+1][0]
            cells.append(f'<mxCell id="{nid()}" value="" style="endArrow=classic;html=1;strokeColor={accent};strokeWidth=3;shadow=1;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{nx+32}" y="360" as="sourcePoint"/><mxPoint x="{nx2-32}" y="360" as="targetPoint"/></mxGeometry></mxCell>')

    # HPG line — dashed above
    cells.append(f'<mxCell id="{nid()}" value="" style="endArrow=classic;html=1;strokeColor=#2E86C1;strokeWidth=3;dashed=1;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="100" y="220" as="sourcePoint"/><mxPoint x="600" y="220" as="targetPoint"/></mxGeometry></mxCell>')
    cells.append(f'<mxCell id="{nid()}" value="HPG 基液主管路 (0.5 wt%)" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;fontColor=#2E86C1;" vertex="1" parent="1"><mxGeometry x="180" y="195" width="280" height="30" as="geometry"/></mxCell>')

    # QC badge — pill shape with shadow
    cells.append(f'<mxCell id="{nid()}" value="在线取样 1次/30min" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#E74C3C;strokeWidth=2;fontColor=#E74C3C;fontSize=11;fontStyle=1;shadow=1;" vertex="1" parent="1"><mxGeometry x="560" y="240" width="140" height="35" as="geometry"/></mxCell>')

    # Support row
    sup = ['荧光粉料仓','去离子水罐','分散剂罐','HPG基液罐\n(20-50m³)','交联剂罐\n(有机硼)','破胶剂罐\n(过硫酸铵)','支撑剂料仓\n(20/40目)','地层水罐\n(返排用)']
    for i, (lab, ix) in enumerate(zip(sup, [160,240,320,430,530,630,750,880])):
        cells.append(f'<mxCell id="{nid()}" value="{lab}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECEFF1;strokeColor=#CFD8DC;strokeWidth=1;fontColor=#78909C;fontSize=9;align=center;" vertex="1" parent="1"><mxGeometry x="{ix}" y="480" width="70" height="45" as="geometry"/></mxCell>')

    return wrap(''.join(cells), 1200, 560, "Fig3-3D-Process")


# ================================================================
# FIG 4 — 3D Timeline with depth nodes
# ================================================================
def fig4():
    cid = [2]
    def nid(): v=cid[0]; cid[0]+=1; return str(v)
    cells = []
    cells.append(f'<mxCell id="{nid()}" value="图4  压裂裂缝荧光示踪方法流程" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=18;fontStyle=1;fontColor=#1a1a2e;" vertex="1" parent="1"><mxGeometry x="180" y="15" width="450" height="45" as="geometry"/></mxCell>')

    # 3D spine
    cells.append(f'<mxCell id="{nid()}" value="" style="endArrow=none;html=1;strokeColor=#BDC3C7;strokeWidth=6;rounded=1;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="200" y="90" as="sourcePoint"/><mxPoint x="200" y="720" as="targetPoint"/></mxGeometry></mxCell>')
    cells.append(f'<mxCell id="{nid()}" value="" style="endArrow=none;html=1;strokeColor=#ECF0F1;strokeWidth=3;rounded=1;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="199" y="92" as="sourcePoint"/><mxPoint x="199" y="718" as="targetPoint"/></mxGeometry></mxCell>')

    stages = [
        (660, '1', '注入', '荧光HPG压裂液 + 支撑剂泵入目标层段\n荧光粉随携砂液运移至水力裂缝各处', '#2E86C1'),
        (520, '2', '关井破胶', '密闭关井 6-48 h，储层温度 60-150°C\n过硫酸铵破胶，PEG脱附→KH550氨基暴露', '#E74C3C'),
        (380, '3', '返排', '开井返排，残渣与未锚定荧光粉排出\n> 90% 锚定颗粒滞留裂缝壁面', '#27AE60'),
        (240, '4', '取心检测', '压后取心 + 365 nm紫外 + 520 nm滤光片\n荧光分布区域 = 压裂液实际波及范围', '#8E44AD'),
    ]

    for cy, num, title, desc, accent in stages:
        # Background strip — 3D card
        cells.append(f'<mxCell id="{nid()}" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor={accent};strokeColor=none;opacity=6;" vertex="1" parent="1"><mxGeometry x="30" y="{cy-45}" width="740" height="90" as="geometry"/></mxCell>')
        # Node — 3D sphere
        cells.append(f'<mxCell id="{nid()}" value="{num}" style="ellipse;whiteSpace=wrap;html=1;fillColor=#888;strokeColor=none;opacity=35;" vertex="1" parent="1"><mxGeometry x="172" y="{cy-26}" width="56" height="56" as="geometry"/></mxCell>')
        cells.append(f'<mxCell id="{nid()}" value="{num}" style="ellipse;whiteSpace=wrap;html=1;fillColor={accent};strokeColor=#FFFFFF;strokeWidth=3;fontColor=#FFFFFF;fontSize=20;fontStyle=1;shadow=1;" vertex="1" parent="1"><mxGeometry x="168" y="{cy-30}" width="64" height="64" as="geometry"/></mxCell>')
        # Title left
        cells.append(f'<mxCell id="{nid()}" value="&lt;b&gt;{title}&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;fontSize=16;fontColor={accent};" vertex="1" parent="1"><mxGeometry x="30" y="{cy-20}" width="120" height="40" as="geometry"/></mxCell>')
        # Desc right — on card
        cells.append(f'<mxCell id="{nid()}" value="{desc}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={accent};strokeWidth=1;fontColor=#444;fontSize=11;align=left;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="260" y="{cy-35}" width="490" height="70" as="geometry"/></mxCell>')

        # Dashed connector
    for y1, y2 in [(630,555),(490,415),(350,275)]:
        cells.append(f'<mxCell id="{nid()}" value="" style="endArrow=none;html=1;strokeColor=#BDC3C7;strokeWidth=1.5;dashed=1;dashPattern=6 4;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="200" y="{y1}" as="sourcePoint"/><mxPoint x="200" y="{y2}" as="targetPoint"/></mxGeometry></mxCell>')

    # Bottom callout — 3D banner
    cells.append(f'<mxCell id="{nid()}" value="◆ 工程时序（注入→关井→返排）直接驱动功能切换  —  无需外部触发剂" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF8E1;strokeColor=#F39C12;strokeWidth=2;fontColor=#E65100;fontSize=13;fontStyle=1;shadow=1;" vertex="1" parent="1"><mxGeometry x="80" y="80" width="550" height="45" as="geometry"/></mxCell>')

    return wrap(''.join(cells), 820, 780, "Fig4-3D-Method")


# ================================================================
# Generate all files
# ================================================================
files = [
    ('fig1_core_shell.drawio', fig1()),
    ('fig2_switching.drawio', fig2()),
    ('fig3_process.drawio', fig3()),
    ('fig4_method.drawio', fig4()),
]

for fname, xml in files:
    fpath = os.path.join(OUT, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(xml)
    print(f'{fname}: {len(xml):,} bytes')

print(f'\nAll 3D diagrams saved to {OUT}')