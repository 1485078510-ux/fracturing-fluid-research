# -*- coding: utf-8 -*-
"""专利附图 — 中文，精炼设计。"""
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Arc
import numpy as np

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Microsoft YaHei', 'SimHei', 'Arial'],
    'axes.unicode_minus': False,
    'svg.fonttype': 'none',
    'text.usetex': False,
})
OUT = r'c:\Users\郝\Desktop\claude\荧光压裂液'

# Palette — soft, professional
BLUE   = '#5B9BD5'
DARK   = '#2F5496'
RED    = '#E15759'
GREEN  = '#59A14F'
PURPLE = '#AF7AC5'
ORANGE = '#F28E2B'
BROWN  = '#8C564B'
GRAY   = '#7F7F7F'
LGRAY  = '#E0E0E0'
WHITE  = '#FFFFFF'

def dashed_circle(ax, x, y, r, color, lw=1.5, dash=(4,3)):
    """Draw a dashed circle with proper dashes."""
    ax.add_patch(Circle((x,y), r, fc='none', ec=color, lw=lw, ls=(0, dash)))

def particle(ax, x, y, r=0.3, core=BLUE, shell=PURPLE, halo=ORANGE, show_halo=True):
    ax.add_patch(Circle((x,y), r, fc=core, ec='none', zorder=3))
    ax.add_patch(Circle((x,y), r, fc='none', ec=shell, lw=1.5, zorder=4))
    if show_halo:
        ax.add_patch(Circle((x,y), r+0.18, fc='none', ec=halo, lw=1.2, ls=(0,(4,2.5)), alpha=0.7, zorder=2))

# ================================================================
# FIGURE 1 — Core-shell structure (clean, centered)
# ================================================================
fig, ax = plt.subplots(figsize=(5.5, 5.5))
ax.set_xlim(-5, 5); ax.set_ylim(-5, 5.5)
ax.set_aspect('equal'); ax.axis('off')

# Core
ax.add_patch(Circle((0,0), 2.6, fc=BLUE, ec=DARK, lw=1.8))
ax.text(0, 0.25, 'SrAl2O4', fontsize=13, ha='center', va='center', color='white', weight='bold')
ax.text(0, -0.55, 'Eu2+, Dy3+', fontsize=10, ha='center', va='center', color='#B8D4F0')

# KH550 — solid thick ring
ax.add_patch(Circle((0,0), 3.35, fc='none', ec=PURPLE, lw=5))
# Small dots on KH550 ring
for a in np.linspace(10, 350, 6):
    r = np.radians(a)
    ax.plot(3.35*np.cos(r), 3.35*np.sin(r), '.', color=PURPLE, markersize=9)

# PEG — two concentric dashed rings
dashed_circle(ax, 0, 0, 4.1, ORANGE, lw=2.5)
dashed_circle(ax, 0, 0, 4.25, ORANGE, lw=1.2)

# Callout lines
ax.annotate('KH550 化学锚固层', xy=(0.2, 3.35), xytext=(2.8, 4.4), fontsize=10, color=PURPLE, weight='bold', ha='center',
            arrowprops=dict(arrowstyle='->', color=PURPLE, lw=1.2, connectionstyle='arc3,rad=0.25'))
ax.annotate('PEG4000\n物理屏蔽层', xy=(4.1, 0.5), xytext=(2.6, -3.2), fontsize=10, color=ORANGE, weight='bold', ha='center',
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.2, connectionstyle='arc3,rad=-0.3'))

# Legend at bottom
for i, (c, lab) in enumerate([(BLUE, 'SrAl2O4:Eu2+,Dy3+ 基体'), (PURPLE, 'KH550 硅烷偶联剂'), (ORANGE, 'PEG4000 聚乙二醇')]):
    ax.add_patch(Rectangle((-2.8, -4.5+i*0.65), 0.45, 0.45, fc=c, ec='none'))
    ax.text(-2.1, -4.25+i*0.65, lab, fontsize=9, va='center', color='#333')

ax.set_title('图 1  改性稀土铝酸盐荧光粉颗粒结构', fontsize=14, weight='bold', color='#222', pad=12)
fig.savefig(f'{OUT}/fig_01_core_shell.svg', dpi=200, bbox_inches='tight', facecolor=WHITE, edgecolor='none')
fig.savefig(f'{OUT}/fig_01_core_shell.png', dpi=300, bbox_inches='tight', facecolor=WHITE, edgecolor='none')
plt.close(fig)

# ================================================================
# FIGURE 2 — Switching mechanism (three-panel horizontal)
# ================================================================
fig = plt.figure(figsize=(13, 5))

# Three sub-panels — equal width
gs = fig.add_gridspec(1, 3, wspace=0.15, left=0.04, right=0.96, top=0.88, bottom=0.08)

for idx, (title, accent, bg, lines, p_positions, extra) in enumerate([
    ('阶段一：注入\n分散态', BLUE, '#F0F6FC',
     ['PEG水合层完整', '空间位阻排斥', '颗粒均匀悬浮'],
     [(1.3,4.0), (2.2,3.4), (2.7,4.3), (1.6,2.8), (2.5,2.3), (3.0,3.1)],
     None),
    ('阶段二：关井破胶\n过渡态', RED, '#FDF2F2',
     ['过硫酸铵氧化', 'PEG链自由基降解', 'KH550氨基暴露'],
     [(1.2,4.1), (2.6,3.3), (2.0,2.5)],
     'shed'),
    ('阶段三：返排后\n锚定态', GREEN, '#F1F8F0',
     ['氨基-硅羟基锚定', '静电 + 氢键 + 缩合', '净残留率 > 90%'],
     [(1.1,4.2), (1.9,3.6), (2.7,4.5), (1.4,3.0), (2.3,2.5)],
     'anchored'),
]):
    ax = fig.add_subplot(gs[0, idx])
    ax.set_xlim(0, 4); ax.set_ylim(0, 5.5)
    ax.set_aspect('equal'); ax.axis('off')

    # Panel background
    ax.add_patch(Rectangle((0,0), 4, 5.5, fc=bg, ec='none', zorder=0))

    # Title bar
    ax.add_patch(Rectangle((0, 5.2), 4, 0.3, fc=accent, ec='none', zorder=5))
    ax.text(2, 5.35, title, fontsize=12, weight='bold', ha='center', va='center', color='white')

    # Info lines
    for i, line in enumerate(lines):
        ax.text(2, 1.8 - i*0.35, line, fontsize=9, ha='center', color='#555')

    # Particles
    for (px, py) in p_positions:
        if extra == 'shed':
            particle(ax, px, py, show_halo=False)
            # PEG fragment marks
            ax.add_patch(Circle((px,py), 0.3+0.18, fc='none', ec=ORANGE, lw=0.8, ls=(0,(3,2)), alpha=0.5))
            for dx, dy in [(0.3,0.25),(0.4,-0.1),(0.25,-0.3)]:
                ax.plot(px+dx, py+dy, 'x', color=ORANGE, markersize=6, lw=1, alpha=0.6)
        elif extra == 'anchored':
            particle(ax, px, py, show_halo=False)
            # Anchor to wall
            ax.plot([px, px], [py-0.3, 0.4], color=GREEN, lw=1.2, ls=':')
        else:
            particle(ax, px, py, show_halo=True)

    # Wall for anchored panel
    if extra == 'anchored':
        ax.add_patch(Rectangle((0, 0.28), 4, 0.12, fc=BROWN, ec='none'))

    # Panel border — subtle
    ax.add_patch(Rectangle((0,0), 4, 5.5, fc='none', ec=GRAY, lw=0.5, zorder=6))

# Arrows between panels — centered vertically
arrow_y = 4.7
fig.patches.extend([
    FancyArrowPatch((0.315, arrow_y/5.5), (0.355, arrow_y/5.5),
                    transform=fig.transFigure, arrowstyle='->', mutation_scale=18,
                    color=GRAY, lw=2, clip_on=False),
    FancyArrowPatch((0.648, arrow_y/5.5), (0.688, arrow_y/5.5),
                    transform=fig.transFigure, arrowstyle='->', mutation_scale=18,
                    color=GRAY, lw=2, clip_on=False),
])
# Bridge labels
fig.text(0.335, 0.91, '破胶', fontsize=9, ha='center', color=RED, weight='bold', transform=fig.transFigure)
fig.text(0.668, 0.91, '接触壁面', fontsize=9, ha='center', color=GREEN, weight='bold', transform=fig.transFigure)

fig.suptitle('图 2  "分散态 → 锚定态" 功能切换机制', fontsize=14, weight='bold', color='#222', y=0.97)
fig.savefig(f'{OUT}/fig_02_switching.svg', dpi=200, bbox_inches='tight', facecolor=WHITE, edgecolor='none')
fig.savefig(f'{OUT}/fig_02_switching.png', dpi=300, bbox_inches='tight', facecolor=WHITE, edgecolor='none')
plt.close(fig)

# ================================================================
# FIGURE 3 — Process flow (horizontal pipeline style)
# ================================================================
fig, ax = plt.subplots(figsize=(13, 4.5))
ax.set_xlim(0, 13); ax.set_ylim(0, 4.5)
ax.axis('off')

# Pipeline base line
ax.plot([0.8, 12.2], [2.5, 2.5], color=LGRAY, lw=3, solid_capstyle='round', zorder=0)

steps = [
    (1.5, 2.5, '母液配制罐', '荧光粉 + 水 + 分散剂\n高速搅拌 + 超声\n浓度 40 g/L', BLUE),
    (3.8, 2.5, '计量泵', '隔膜式\n精度 ±1%', PURPLE),
    (6.2, 2.5, '静态混合器', 'SMX 型, DN50\n在线稀释 0.5% v/v', ORANGE),
    (8.6, 2.5, '混砂车', '支撑剂 +\n荧光压裂液', GREEN),
    (11.0, 2.5, '高压泵组', '→ 井筒\n→ 裂缝', RED),
]

for x, y, name, desc, accent in steps:
    # Node circle
    ax.add_patch(Circle((x, y), 0.45, fc=accent, ec='white', lw=2.5, zorder=5))
    ax.text(x, y, str(steps.index((x,y,name,desc,accent))+1), fontsize=12, weight='bold', ha='center', va='center', color='white')
    # Name
    ax.text(x, y+0.85, name, fontsize=11, weight='bold', ha='center', color=accent)
    # Description below
    ax.text(x, y-0.85, desc, fontsize=8, ha='center', va='top', color='#555')

# Flow arrows on pipeline
for i in range(4):
    x1 = steps[i][0] + 0.5
    x2 = steps[i+1][0] - 0.5
    ax.annotate('', xy=(x2, 2.5), xytext=(x1, 2.5), arrowprops=dict(arrowstyle='->', color=GRAY, lw=2))

# HPG line
ax.annotate('', xy=(6.8, 3.8), xytext=(0.8, 3.8), arrowprops=dict(arrowstyle='->', color=BLUE, lw=2.5))
ax.text(3.8, 4.05, 'HPG 基液主管路  (0.5 wt%)', fontsize=10, ha='center', color=BLUE, weight='bold')

# QC mark
ax.plot(6.2, 3.4, 's', color=RED, markersize=12, markerfacecolor='white', markeredgewidth=2)
ax.text(6.2, 3.1, '在线取样\n1次/30min', fontsize=8, ha='center', color=RED, weight='bold')

# Support equipment row
ax.text(0.8, 5.5, '辅助设备', fontsize=9, weight='bold', color=GRAY)
sup_items = ['改性荧光粉料仓', '去离子水罐', '分散剂储罐', 'HPG 基液罐\n(20-50 m³)', '交联剂罐\n(有机硼)', '破胶剂罐\n(过硫酸铵)', '支撑剂料仓\n(20/40 目)', '地层水罐\n(返排用)']
sup_x = [1.5, 2.8, 4.1, 5.8, 7.2, 8.6, 10.0, 11.5]
for i, (sx, lab) in enumerate(zip(sup_x, sup_items)):
    ax.text(sx, 1.0, lab, fontsize=7, ha='center', va='top', color=GRAY)
    ax.plot(sx, 1.5, 's', color=GRAY, markersize=5, alpha=0.5)

ax.set_title('图 3  "母液预配 + 在线稀释" 现场施工工艺流程', fontsize=14, weight='bold', color='#222', pad=10)
fig.savefig(f'{OUT}/fig_03_process.svg', dpi=200, bbox_inches='tight', facecolor=WHITE, edgecolor='none')
fig.savefig(f'{OUT}/fig_03_process.png', dpi=300, bbox_inches='tight', facecolor=WHITE, edgecolor='none')
plt.close(fig)

# ================================================================
# FIGURE 4 — Method timeline (vertical, four stages)
# ================================================================
fig, ax = plt.subplots(figsize=(8, 10))
ax.set_xlim(0, 8); ax.set_ylim(0, 10)
ax.axis('off')

# Central spine
ax.plot([4, 4], [0.5, 9.5], color=LGRAY, lw=2, zorder=0)

stages = [
    (9.0, '1', '注入', '荧光 HPG 压裂液 + 支撑剂\n泵入目标压裂层段\n荧光粉随携砂液运移至裂缝', BLUE),
    (7.0, '2', '关井破胶', '密闭关井 6~48 h\n储层温度 60~150 °C\n过硫酸铵破胶, PEG 脱附', RED),
    (5.0, '3', '返排', '开井返排\n残渣与未锚定荧光粉排出\n>90% 锚定颗粒滞留裂缝壁面', GREEN),
    (3.0, '4', '取心检测', '压后取心 + 365 nm 紫外\n520 nm 带通滤光片成像\n荧光区域 = 压裂液波及范围', PURPLE),
]

for cy, num, title, desc, accent in stages:
    # Node circle
    ax.add_patch(Circle((4, cy), 0.5, fc=accent, ec='white', lw=3, zorder=5))
    ax.text(4, cy, num, fontsize=16, weight='bold', ha='center', va='center', color='white')

    # Title — left side
    ax.text(2.7, cy+0.15, title, fontsize=14, weight='bold', ha='right', va='center', color=accent)

    # Description — right side
    ax.text(5.3, cy, desc, fontsize=9, ha='left', va='center', color='#444')

    # Subtle background strip
    ax.add_patch(Rectangle((0.15, cy-0.75), 7.7, 1.5, fc=accent, ec='none', alpha=0.06, zorder=0))

# Connecting dashes between nodes
for y1, y2 in [(8.5, 7.5), (6.5, 5.5), (4.5, 3.5)]:
    ax.plot([4, 4], [y2, y1], color=GRAY, lw=1.5, ls='--', zorder=1)

# Bottom callout
ax.add_patch(FancyBboxPatch((1.2, 0.3), 5.6, 0.8, boxstyle='round,pad=0.15', fc='#FFF8E1', ec=ORANGE, lw=1.5))
ax.text(4, 0.7, '工程时序 (注入→关井→返排) 直接驱动功能切换  —  无需外部触发剂',
        fontsize=10, ha='center', va='center', weight='bold', color='#E65100')

ax.set_title('图 4  压裂裂缝荧光示踪方法流程', fontsize=14, weight='bold', color='#222', pad=12)
fig.savefig(f'{OUT}/fig_04_method.svg', dpi=200, bbox_inches='tight', facecolor=WHITE, edgecolor='none')
fig.savefig(f'{OUT}/fig_04_method.png', dpi=300, bbox_inches='tight', facecolor=WHITE, edgecolor='none')
plt.close(fig)

print('Done: 4 figures × SVG + PNG')
print(f'Output: {OUT}')