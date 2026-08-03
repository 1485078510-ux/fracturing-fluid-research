# -*- coding: utf-8 -*-
"""Generate all three .drawio files with unified 3-color blue palette."""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FIG_DIR = r"荧光压裂液\figures"
os.makedirs(FIG_DIR, exist_ok=True)

from xml.sax.saxutils import escape as xml_escape

# === Unified 3-color palette ===
DEEP  = '#1565C0'   # 深蓝：边框、标题、重点线条
LIGHT = '#E3F2FD'   # 浅蓝：填充、背景区域
TEAL  = '#00897B'   # 蓝绿：强调、高亮、第二填充
LIGHT_TEAL = '#B2DFDB'  # 浅蓝绿：高亮填充
WHITE = '#FFFFFF'
GRAY  = '#78909C'

def drawio_file(name, cells):
    cells_xml = '\n'.join(cells)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="draw.io" version="26.0.0">
  <diagram name="{xml_escape(name)}">
    <mxGraphModel dx="1000" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
{cells_xml}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

def vertex(id, value, style, x, y, w, h, parent="1"):
    return f'        <mxCell id="{id}" value="{xml_escape(value)}" style="{style}" vertex="1" parent="{parent}">\n          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n        </mxCell>'

def edge(id, source, target, style="", value="", parent="1", waypoints=None):
    wp_xml = ""
    if waypoints:
        pts = '\n'.join(f'              <mxPoint x="{px}" y="{py}" />' for px, py in waypoints)
        wp_xml = f'\n            <Array as="points">\n{pts}\n            </Array>'
    return f'        <mxCell id="{id}" value="{xml_escape(value)}" style="{style}" edge="1" parent="{parent}" source="{source}" target="{target}">\n          <mxGeometry relative="1" as="geometry">{wp_xml}\n          </mxGeometry>\n        </mxCell>'

# Shorthand style builders
def vstyle(extra=""):
    return f"rounded=1;whiteSpace=wrap;html=1;fontSize=10;{extra}"
def edgestyle(extra=""):
    return f"edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;{extra}"


# ═══════════════ FIGURE 1: Core-Shell ═══════════════
F1 = []

F1.append(vertex("t1", "图1  改性稀土铝酸盐荧光粉结构示意图",
    "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=16;fontStyle=1;", 150, 15, 500, 30))

# Three layers: outer PEG (light blue), middle KH550 (teal tint), core (deep blue)
F1.append(vertex("peg", "",
    f"ellipse;whiteSpace=wrap;html=1;fillColor={LIGHT};strokeColor={DEEP};strokeWidth=2;opacity=40;dashed=1;dashPattern=8 4;",
    180, 90, 380, 380))
F1.append(vertex("kh550", "",
    f"ellipse;whiteSpace=wrap;html=1;fillColor={LIGHT_TEAL};strokeColor={TEAL};strokeWidth=2;opacity=50;",
    240, 150, 260, 260))
F1.append(vertex("core", "SrAl<sub>2</sub>O<sub>4</sub>:Eu<sup>2+</sup>,Dy<sup>3+</sup>\n荧光粉基体",
    f"ellipse;whiteSpace=wrap;html=1;fillColor={LIGHT};strokeColor={DEEP};strokeWidth=3;fontSize=11;fontStyle=1;",
    300, 210, 140, 140))

# Layer labels
F1.append(vertex("lbl_peg", "PEG4000", f"text;html=1;strokeColor=none;fillColor=none;fontSize=10;fontStyle=1;fontColor={DEEP};", 340, 95, 80, 18))
F1.append(vertex("lbl_kh550", "KH550", f"text;html=1;strokeColor=none;fillColor=none;fontSize=10;fontStyle=1;fontColor={TEAL};", 350, 155, 60, 18))
F1.append(vertex("sioal", "Si-O-Al 共价键", f"text;html=1;strokeColor={TEAL};fillColor={WHITE};fontSize=8;fontStyle=2;fontColor={TEAL};rounded=1;", 350, 200, 90, 20))

# -NH2 groups on KH550 surface
for i, (nx, ny) in enumerate([(250, 260), (230, 210), (470, 250), (480, 290), (310, 370)]):
    F1.append(vertex(f"nh2_{i}", "-NH<sub>2</sub>",
        f"rounded=1;whiteSpace=wrap;html=1;fillColor={LIGHT_TEAL};strokeColor={TEAL};fontSize=8;fontStyle=1;fontColor={TEAL};",
        nx, ny, 35, 16))

# Callout boxes
CO = "rounded=1;whiteSpace=wrap;html=1;align=left;verticalAlign=top;fontSize=9;spacingLeft=8;spacingTop=4;"

F1.append(vertex("co_core", "基体：稀土铝酸盐长余辉荧光粉\n\n- 发光中心Eu<sup>2+</sup>嵌入刚性晶格\n- 化学惰性，抗氧化破胶环境\n- 800~1200目，D<sub>50</sub>~13μm",
    CO + f"fillColor={LIGHT};strokeColor={DEEP};", 590, 110, 230, 80))
F1.append(edge("e_core", "core", "co_core", edgestyle(f"exitX=1;exitY=0.5;entryX=0;entryY=0.3;strokeColor={DEEP};strokeWidth=1.5;dashed=1;")))

F1.append(vertex("co_kh550", "内层：硅烷偶联剂化学键合层 (KH550)\n\n- Si-O-Al共价键锚固于基体\n- 提供耐水解屏障\n- 预置活性氨基(-NH<sub>2</sub>)锚定位点\n- 为PEG物理沉积提供有机界面",
    CO + f"fillColor={LIGHT_TEAL};strokeColor={TEAL};", 590, 220, 230, 95))
F1.append(edge("e_kh550", "kh550", "co_kh550", edgestyle(f"exitX=1;exitY=0.5;entryX=0;entryY=0.3;strokeColor={TEAL};strokeWidth=1.5;dashed=1;")))

F1.append(vertex("co_peg", "外层：PEG物理屏蔽层 (PEG4000)\n\n- 注入阶段：空间位阻保障分散\n- 破胶阶段：牺牲响应层脱附\n- 暴露内层NH<sub>2</sub>锚定位点",
    CO + f"fillColor={LIGHT};strokeColor={DEEP};", 590, 350, 230, 85))
F1.append(edge("e_peg", "peg", "co_peg", edgestyle(f"exitX=1;exitY=0.5;entryX=0;entryY=0.3;strokeColor={DEEP};strokeWidth=1.5;dashed=1;")))

# Bottom mechanism bar
F1.append(vertex("mech", "功能切换机制：注入阶段(分散态) PEG外层屏蔽 → 关井破胶 PEG氧化脱附 → 暴露KH550活性-NH<sub>2</sub> → 锚定于砂岩壁面(锚定态)",
    f"rounded=1;whiteSpace=wrap;html=1;fillColor={LIGHT_TEAL};strokeColor={TEAL};fontSize=9;align=center;fontStyle=2;",
    60, 500, 720, 30))


# ═══════════════ FIGURE 2: Process Flow (2-row compact for patent page) ═══════════════
F2 = []

F2.append(vertex("t2", "图2  荧光压裂液体系现场施工工艺流程图",
    "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=14;fontStyle=1;", 180, 8, 450, 28))

B = "rounded=1;whiteSpace=wrap;html=1;fontSize=10;fontStyle=1;"

# === Row 1: Mother liquor preparation (y=50) ===
R1 = [
    ("r1a", "改性荧光粉\n+ 分散助剂\n+ 去离子水",     30,  50, 140, 60, LIGHT, DEEP),
    ("r1b", "高速剪切/超声分散\n→ 荧光母液\n(30~60 g/L)", 210, 50, 160, 60, LIGHT_TEAL, TEAL),
    ("r1c", "在线计量泵\n→ 静态混合器\n(0.1~2.0 vol%)", 410, 50, 160, 60, LIGHT, DEEP),
]
for sid, txt, x, y, w, h, fc, ec in R1:
    F2.append(vertex(sid, txt, B + f"fillColor={fc};strokeColor={ec};", x, y, w, h))

# Row 1 arrows
F2.append(edge("ra1", "r1a", "r1b", edgestyle(f"exitX=1;exitY=0.5;entryX=0;entryY=0.5;strokeColor={GRAY};")))
F2.append(edge("ra2", "r1b", "r1c", edgestyle(f"exitX=1;exitY=0.5;entryX=0;entryY=0.5;strokeColor={GRAY};")))

# === Row 2: Dilution + pumping (y=165) ===
R2 = [
    ("r2a", "HPG基液主流\n(稠化剂0.3~1.0 wt%)\n+ 交联剂 + 破胶剂\n+ 支撑剂", 30, 165, 160, 70, LIGHT_TEAL, TEAL),
    ("r2b", "荧光压裂液终液",    230, 165, 130, 70, LIGHT, DEEP),
    ("r2c", "压裂泵车\n→ 井口",  400, 165, 120, 70, LIGHT_TEAL, TEAL),
    ("r2d", "目标压裂层段",      560, 165, 130, 70, LIGHT, DEEP),
]
for sid, txt, x, y, w, h, fc, ec in R2:
    shape = "ellipse;" if sid == "r2d" else ""
    F2.append(vertex(sid, txt, shape + B + f"fillColor={fc};strokeColor={ec};", x, y, w, h))

# Row 2 arrows
F2.append(edge("rb1", "r2a", "r2b", edgestyle(f"exitX=1;exitY=0.5;entryX=0;entryY=0.5;strokeColor={GRAY};")))
F2.append(edge("rb2", "r2b", "r2c", edgestyle(f"exitX=1;exitY=0.5;entryX=0;entryY=0.5;strokeColor={GRAY};")))
F2.append(edge("rb3", "r2c", "r2d", edgestyle(f"exitX=1;exitY=0.5;entryX=0;entryY=0.5;strokeColor={GRAY};")))

# === Vertical arrow: Row 1 mixer output → Row 2 HPG+mixer input ===
F2.append(edge("v1", "r1c", "r2a", edgestyle(f"exitX=0.5;exitY=1;entryX=0.5;entryY=0;strokeColor={GRAY};strokeWidth=1.5;"),
    "母液"))

# === Summary bar at bottom ===
F2.append(vertex("sum", "物料流向: 改性荧光粉+分散助剂+水 → 高速剪切/超声分散→荧光母液 → 在线计量泵→静态混合器 → HPG基液+交联剂+破胶剂+支撑剂 → 荧光压裂液终液 → 压裂泵车→井口 → 目标压裂层段",
    f"rounded=1;whiteSpace=wrap;html=1;fillColor={LIGHT};strokeColor={GRAY};fontSize=7;align=center;",
    30, 275, 660, 20))


# ═══════════════ FIGURE 3: Method Flow ═══════════════
F3 = []

F3.append(vertex("t3", "图3  压裂裂缝荧光示踪方法流程框图",
    "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=15;fontStyle=1;", 200, 8, 420, 30))
F3.append(vertex("start", "压裂施工开始",
    f"ellipse;whiteSpace=wrap;html=1;fillColor={LIGHT_TEAL};strokeColor={TEAL};fontSize=11;fontStyle=1;",
    310, 45, 180, 40))

def stage_box(cells, sid, y, title, items, note_text=None):
    """Stage box: alternating DEEP (odd) / TEAL (even) for titles."""
    tcolor = DEEP if sid % 2 == 1 else TEAL
    bcolor = LIGHT
    ecolor = tcolor
    h = len(items) * 52 + 70
    cells.append(vertex(f"s{sid}_bg", "", f"rounded=1;whiteSpace=wrap;html=1;fillColor={bcolor};strokeColor={ecolor};strokeWidth=2;", 60, y, 680, h))
    cells.append(vertex(f"s{sid}_title", title, f"text;html=1;strokeColor=none;fillColor={tcolor};fontColor=#FFFFFF;align=center;fontSize=11;fontStyle=1;rounded=1;", 60, y, 95, 26))

    item_y = y + 42
    for i, (txt, hl) in enumerate(items):
        ic = LIGHT_TEAL if hl else WHITE
        ie = TEAL if hl else ecolor
        fw = "fontStyle=1;" if hl else ""
        cells.append(vertex(f"s{sid}_i{i}", txt, f"rounded=1;whiteSpace=wrap;html=1;fillColor={ic};strokeColor={ie};fontSize=9;{fw}align=center;", 85, item_y, 420, 40))
        if i < len(items) - 1:
            cells.append(edge(f"s{sid}_a{i}", f"s{sid}_i{i}", f"s{sid}_i{i+1}", edgestyle(f"exitX=0.5;exitY=1;entryX=0.5;entryY=0;strokeColor={ecolor};")))
        item_y += 52

    if note_text:
        cells.append(vertex(f"s{sid}_note", note_text, f"rounded=1;whiteSpace=wrap;html=1;fillColor={WHITE};strokeColor={ecolor};strokeWidth=1;fontSize=8;align=center;dashed=1;", 530, y + 50, 190, h - 65))
    return y + h

y = 100
y = stage_box(F3, 1, y, "注入阶段",
    [("荧光压裂液终液 + 支撑剂 混合", False),
     ("通过压裂泵注系统泵入目标压裂层段", False),
     ("荧光粉随携砂液运移至水力裂缝各处 (分散态)", True)],
    "母液添加段位:\n前置液段/携砂液段/顶替液段\n(优选前置液+携砂液连续添加)")

F3.append(edge("a_s1s2", "s1_bg", "s2_bg", edgestyle("exitX=0.5;exitY=1;entryX=0.5;entryY=0;strokeColor=#455A64;strokeWidth=2;")))

y = stage_box(F3, 2, y+15, "关井破胶阶段",
    [("停泵关井 -> 储层温度60~150C, 密闭维持6~48 h", False),
     ("过硫酸铵热分解 -> SO<sub>4</sub><sup>.-</sup> 攻击PEG醚键 -> 氧化链断裂", False),
     ("PEG外层脱附降解 -> 暴露KH550活性氨基(-NH<sub>2</sub>)", False),
     ("-NH<sub>2</sub> + 砂岩Si-OH -> 静电吸引/氢键/化学缩合 -> 牢固锚定", True)],
    "功能切换核心机制:\n1.PEG牺牲响应层-氧化脱附\n2.KH550活性氨基暴露\n3.氨基与砂岩硅羟基\n多点协同锚定\n4.过硫酸铵破胶剂触发\n(无需额外触发剂)")

F3.append(edge("a_s2s3", "s2_bg", "s3_bg", edgestyle("exitX=0.5;exitY=1;entryX=0.5;entryY=0;strokeColor=#455A64;strokeWidth=2;")))

y = stage_box(F3, 3, y+15, "返排阶段",
    [("开井返排 -> 携带破胶残渣及未锚定游离荧光粉排出井筒", False),
     ("已锚定荧光粉牢固保留于裂缝壁面 (净残留率 > 90%)", True)],
    "动态驱替实验:\n锚定率 = 92.7 +/- 1.8%\nn=3")

F3.append(edge("a_s3s4", "s3_bg", "s4_bg", edgestyle("exitX=0.5;exitY=1;entryX=0.5;entryY=0;strokeColor=#455A64;strokeWidth=2;")))

y = stage_box(F3, 4, y+15, "取心与检测阶段",
    [("压后取心作业 -> 获取含裂缝岩心", False),
     ("紫外光源365 nm照射 -> 绿色荧光发射(~520 nm)", False),
     ("观察/拍照记录裂缝壁面荧光分布 -> 确定压裂液波及范围", True)],
    "荧光分布区域 =\n压裂液实际波及范围\n(定性-半定量实物验证)")

F3.append(edge("a_s4e", "s4_bg", "end", edgestyle("exitX=0.5;exitY=1;entryX=0.5;entryY=0;strokeColor=#455A64;strokeWidth=2;")))
F3.append(vertex("end", "获得压裂裂缝的可实物验证荧光标记",
    f"ellipse;whiteSpace=wrap;html=1;fillColor={LIGHT_TEAL};strokeColor={TEAL};fontSize=11;fontStyle=1;",
    230, y+30, 340, 40))


# ═══════════════ WRITE ═══════════════
for name, cells in [("fig1_结构示意图", F1), ("fig2_工艺流程图", F2), ("fig3_方法流程图", F3)]:
    xml = drawio_file(name, cells)
    fp = os.path.join(FIG_DIR, f"{name}.drawio")
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(xml)
    import xml.etree.ElementTree as ET
    try:
        ET.parse(fp)
        print(f"{name}.drawio: OK ({len(cells)} cells)")
    except ET.ParseError as e:
        print(f"{name}.drawio: FAIL - {e}")

print("Done.")