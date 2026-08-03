# -*- coding: utf-8 -*-
"""图2：荧光压裂液体系"母液预配+在线稀释"现场施工工艺流程图"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

FIG_DIR = r"荧光压裂液\figures"
os.makedirs(FIG_DIR, exist_ok=True)

fig, ax = plt.subplots(1, 1, figsize=(20, 8))
ax.set_xlim(0, 20)
ax.set_ylim(0, 8)
ax.set_aspect('auto')
ax.axis('off')

def draw_box(ax, x, y, w, h, text, color='#dae8fc', edge='#6c8ebf', fontsize=9, bold=False, subtext=None):
    """Draw a rounded box with centered text."""
    box = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.15',
                          facecolor=color, edgecolor=edge, linewidth=1.5, zorder=3)
    ax.add_patch(box)
    fs = fontsize
    fw = 'bold' if bold else 'normal'
    if subtext:
        ax.text(x + w/2, y + h*0.65, text, ha='center', va='center', fontsize=fs, fontweight=fw, zorder=4)
        ax.text(x + w/2, y + h*0.3, subtext, ha='center', va='center', fontsize=fs-2, color='#555555', zorder=4)
    else:
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fs, fontweight=fw, zorder=4)

def draw_tank(ax, x, y, w, h, text, subtext=None):
    """Draw a cylindrical tank shape."""
    # Body
    rect = FancyBboxPatch((x, y + h*0.15), w, h*0.85, boxstyle='round,pad=0.1',
                          facecolor='#d5e8d4', edgecolor='#82b366', linewidth=1.5, zorder=3)
    ax.add_patch(rect)
    # Top ellipse
    from matplotlib.patches import Ellipse
    ell = Ellipse((x + w/2, y + h*0.85), w, h*0.3, facecolor='#c8e6c9', edgecolor='#82b366', linewidth=1.5, zorder=3)
    ax.add_patch(ell)
    if subtext:
        ax.text(x + w/2, y + h*0.55, text, ha='center', va='center', fontsize=9, fontweight='bold', zorder=4)
        ax.text(x + w/2, y + h*0.25, subtext, ha='center', va='center', fontsize=7, color='#555555', zorder=4)
    else:
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=9, fontweight='bold', zorder=4)

def draw_arrow(ax, x1, y1, x2, y2, color='#555555', lw=1.5, label=''):
    """Draw an arrow between two points."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                               connectionstyle='arc3,rad=0'))
    if label:
        ax.text((x1+x2)/2, max(y1,y2) + 0.1, label, fontsize=7, color=color, ha='center')

# === Title ===
ax.text(10, 7.6, '图2  荧光压裂液体系"母液预配 + 在线稀释"现场施工工艺流程图',
        fontsize=15, fontweight='bold', ha='center', color='#212121')

# === Zone backgrounds ===
# Zone 1: 母液预配工段
zone1 = FancyBboxPatch((0.2, 1.2), 6.8, 5.8, boxstyle='round,pad=0.2',
                        facecolor='#E8EAF6', edgecolor='#3F51B5', linewidth=1.5,
                        linestyle='--', alpha=0.5, zorder=1)
ax.add_patch(zone1)
ax.text(0.5, 6.7, '母液预配工段', fontsize=11, fontweight='bold', color='#3F51B5', zorder=4)

# Zone 2: 在线稀释工段
zone2 = FancyBboxPatch((7.4, 1.2), 6.0, 5.8, boxstyle='round,pad=0.2',
                        facecolor='#E8F5E9', edgecolor='#4CAF50', linewidth=1.5,
                        linestyle='--', alpha=0.5, zorder=1)
ax.add_patch(zone2)
ax.text(7.7, 6.7, '在线稀释工段', fontsize=11, fontweight='bold', color='#4CAF50', zorder=4)

# Zone 3: 泵注工段
zone3 = FancyBboxPatch((13.8, 1.2), 6.0, 5.8, boxstyle='round,pad=0.2',
                        facecolor='#FFF3E0', edgecolor='#FF9800', linewidth=1.5,
                        linestyle='--', alpha=0.5, zorder=1)
ax.add_patch(zone3)
ax.text(14.1, 6.7, '泵注工段', fontsize=11, fontweight='bold', color='#FF9800', zorder=4)

# ===== Zone 1: Mother Liquor Preparation =====
# Row 1: Raw materials
draw_box(ax, 0.6, 5.3, 1.8, 0.8, '改性荧光粉', color='#dae8fc', edge='#6c8ebf', fontsize=10, bold=True)
draw_box(ax, 2.8, 5.3, 1.8, 0.8, '分散助剂', color='#dae8fc', edge='#6c8ebf', fontsize=10, bold=True,
         subtext='螯合剂+表面活性剂')
draw_box(ax, 5.0, 5.3, 1.8, 0.8, '去离子水', color='#dae8fc', edge='#6c8ebf', fontsize=10, bold=True)

# Mixing arrows down
for x_src in [1.5, 3.7, 5.9]:
    draw_arrow(ax, x_src, 5.3, x_src, 4.3, color='#888888', lw=1.2)

# Mixing unit
draw_box(ax, 1.8, 3.5, 3.5, 0.8, '高速剪切 / 超声分散',
         color='#fff2cc', edge='#d6b656', fontsize=10, bold=True,
         subtext='5000~15000 rpm | 20~60 kHz')

# Arrow down to tank
draw_arrow(ax, 3.55, 3.5, 3.55, 2.5, color='#888888', lw=1.5)

# Mother liquor tank
draw_tank(ax, 1.8, 1.8, 3.5, 1.5, '荧光母液储罐', subtext='浓度 30~60 g/L')

# === Arrow from Zone 1 to Zone 2 ===
draw_arrow(ax, 5.3, 2.55, 7.8, 2.55, color='#E65100', lw=2, label='母液引出')

# ===== Zone 2: Online Dilution =====
# Metering pump
draw_box(ax, 7.9, 3.8, 2.8, 0.8, '在线计量泵', color='#fff2cc', edge='#d6b656', fontsize=10, bold=True,
         subtext='添加量 0.1~2.0 vol%')

draw_arrow(ax, 9.3, 3.8, 9.3, 3.0, color='#888888', lw=1.5)

# Static mixer
draw_box(ax, 7.9, 2.2, 2.8, 0.8, '静态混合器', color='#ffe6cc', edge='#d79b00', fontsize=10, bold=True)

# HPG base fluid (enters from top)
draw_box(ax, 11.1, 4.5, 2.0, 0.8, 'HPG 基液主流', color='#dae8fc', edge='#6c8ebf', fontsize=10, bold=True,
         subtext='稠化剂 0.3~1.0 wt%')
# Arrow from HPG down to mixer
ax.annotate('', xy=(9.3, 3.0), xytext=(12.1, 4.5),
            arrowprops=dict(arrowstyle='->', color='#6c8ebf', lw=1.5,
                           connectionstyle='arc3,rad=-0.3'))
ax.text(10.0, 3.8, 'HPG基液', fontsize=7, color='#6c8ebf', ha='center')

# === Arrow from Zone 2 to Zone 3 ===
ax.annotate('', xy=(14.2, 2.6), xytext=(12.7, 2.6),
            arrowprops=dict(arrowstyle='->', color='#E65100', lw=2))
ax.text(13.45, 2.9, '混配完成', fontsize=7, color='#888888', ha='center')

# ===== Zone 3: Pumping =====
# Final fluid
draw_box(ax, 14.3, 3.8, 2.4, 0.8, '荧光压裂液终液', color='#d5e8d4', edge='#82b366', fontsize=10, bold=True,
         subtext='含交联剂+破胶剂')

# Additives (top-right)
draw_box(ax, 17.2, 3.8, 2.2, 1.0, '交联剂\n0.1~0.5 vol%', color='#f8cecc', edge='#b85450', fontsize=8)
draw_box(ax, 17.2, 4.9, 2.2, 0.7, '破胶剂\n0.02~0.3 wt%', color='#f8cecc', edge='#b85450', fontsize=8)
# Support agent
draw_box(ax, 17.2, 3.0, 2.2, 0.7, '+ 支撑剂', color='#f8cecc', edge='#b85450', fontsize=8)

# Dotted arrows from additives
ax.annotate('', xy=(16.7, 4.2), xytext=(17.2, 4.6),
            arrowprops=dict(arrowstyle='->', color='#b85450', lw=1, linestyle='dashed'))

draw_arrow(ax, 15.5, 3.8, 15.5, 3.0, color='#888888', lw=1.5)

# Pump truck
draw_box(ax, 14.3, 2.3, 2.4, 0.7, '压裂泵车', color='#ffe6cc', edge='#d79b00', fontsize=10, bold=True)

draw_arrow(ax, 15.5, 2.3, 15.5, 1.7, color='#888888', lw=1.5)

# Wellhead (triangle)
well_x, well_y = 14.5, 0.8
triangle = plt.Polygon([(well_x, well_y + 0.9), (well_x + 1.9, well_y + 0.9),
                         (well_x + 0.95, well_y)], closed=True,
                       facecolor='#d5e8d4', edgecolor='#82b366', linewidth=1.5, zorder=3)
ax.add_patch(triangle)
ax.text(well_x + 0.95, well_y + 0.5, '井口', ha='center', va='center', fontsize=9, fontweight='bold', zorder=4)

draw_arrow(ax, 15.45, 0.8, 15.45, 0.1, color='#E65100', lw=2, label='高压泵注')

# Target zone
draw_box(ax, 14.1, -0.6, 2.7, 0.6, '目标压裂层段', color='#f8cecc', edge='#b85450', fontsize=10, bold=True)

# === Bottom summary bar ===
ax.add_patch(FancyBboxPatch((0.2, -1.4), 19.6, 0.6, boxstyle='round,pad=0.1',
                             facecolor='#ECEFF1', edgecolor='#607D8B', linewidth=1, zorder=3))
flow_text = ('物料流向：改性荧光粉 + 分散助剂 + 去离子水 → 高速剪切/超声分散 → 荧光母液储罐 → '
             '在线计量泵 → 静态混合器 ← HPG基液主流 → 荧光压裂液终液 + 交联剂/破胶剂/支撑剂 → '
             '压裂泵车 → 井口 → 目标压裂层段')
ax.text(10, -1.1, flow_text, ha='center', va='center', fontsize=7.5, color='#455A64', zorder=4)

# Save
for fmt in ['png', 'svg']:
    path = os.path.join(FIG_DIR, f'fig2_工艺流程图.{fmt}')
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved: {path}")

plt.close()
print("Done: Figure 2")