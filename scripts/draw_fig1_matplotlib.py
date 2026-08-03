#!/usr/bin/env python3
"""
Figure 1 — Core-shell structure with 3D volumetric rendering.
Replicates the reference fig1_sci_3d.svg style: multi-layer concentric
ellipses with opacity gradients, warm accent color, thin strokes.

Matplotlib v3.10 — exports SVG/PDF for journal submission.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
import os

OUT = r'c:\Users\郝\Desktop\claude\荧光压裂液'

# ═══ Style (matching reference aesthetic) ═══
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['SimHei', 'Arial', 'DejaVu Sans'],
    'axes.unicode_minus': False,
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})

# ═══ Palette (from reference + colorblind-safe) ═══
WARM_ORANGE = '#D4743C'   # accent (active groups, anchoring)
COOL_BLUE   = '#3A7CB8'   # KH550 layer
MUTED_TEAL  = '#4A9C7F'   # PEG layer
NEUTRAL     = '#A0A0A0'   # core / neutral

# ═══ Panel layout ═══
fig = plt.figure(figsize=(13, 8.5))


# ── Panel (a): Core-shell cross-section ──
ax1 = fig.add_axes([0.02, 0.30, 0.42, 0.68])
ax1.set_xlim(-6, 6)
ax1.set_ylim(-6, 6)
ax1.set_aspect('equal')
ax1.axis('off')

# PEG outer layer — 5 rings, opacity 0.10→0.35
for i, r in enumerate(np.linspace(5.0, 3.5, 5)):
    alpha = 0.10 + 0.25 * (i / 4)
    e = Ellipse((0, 0), r*2, r*2, fill=False, edgecolor=MUTED_TEAL,
                linewidth=0.8, alpha=alpha)
    ax1.add_patch(e)

# KH550 middle layer — 5 rings, opacity 0.12→0.40
for i, r in enumerate(np.linspace(3.5, 2.2, 5)):
    alpha = 0.12 + 0.28 * (i / 4)
    e = Ellipse((0, 0), r*2, r*2, fill=False, edgecolor=COOL_BLUE,
                linewidth=0.8, alpha=alpha)
    ax1.add_patch(e)

# Core — 5 rings, opacity 0.15→0.45
for i, r in enumerate(np.linspace(2.2, 1.0, 5)):
    alpha = 0.15 + 0.30 * (i / 4)
    e = Ellipse((0, 0), r*2, r*2, fill=False, edgecolor=NEUTRAL,
                linewidth=0.8, alpha=alpha)
    ax1.add_patch(e)

# Solid center
core = Ellipse((0, 0), 2.0, 2.0, fill=True, facecolor='#F0F0F0',
               edgecolor=NEUTRAL, linewidth=0.8, alpha=0.7)
ax1.add_patch(core)

# Core label
ax1.text(0, -0.3, 'SrAl₂O₄', ha='center', va='center', fontsize=13,
         fontweight='bold', color='#333333')
ax1.text(0, -0.8, 'Eu²⁺,Dy³⁺', ha='center', va='center', fontsize=10,
         color='#666666')

# Layer labels
ax1.annotate('KH550', xy=(2.8, 0), xytext=(4.5, 1.2), fontsize=12,
             fontweight='bold', color=COOL_BLUE, ha='center',
             arrowprops=dict(arrowstyle='->', color=COOL_BLUE, lw=0.8))
ax1.annotate('PEG4000', xy=(4.2, 0), xytext=(5.5, 2.0), fontsize=12,
             fontweight='bold', color=MUTED_TEAL, ha='center',
             arrowprops=dict(arrowstyle='->', color=MUTED_TEAL, lw=0.8))

# Panel label
ax1.text(-5.5, 5.5, 'a', fontsize=16, fontweight='bold', color=COOL_BLUE,
         va='top', ha='left')


# ── Panel (b): Chemical bonding detail ──
ax2 = fig.add_axes([0.48, 0.30, 0.50, 0.68])
ax2.set_xlim(0, 14)
ax2.set_ylim(0, 10)
ax2.axis('off')

# Rock surface
ax2.axhline(y=3.0, xmin=0.05, xmax=0.95, color=NEUTRAL, linewidth=2)
ax2.text(7, 3.3, '砂岩裂缝壁面  Si−OH 硅羟基', ha='center', fontsize=11,
         fontweight='bold', color='#555555')

# -OH groups
for x in [1.5, 3, 5, 7, 9, 11, 12.5]:
    ax2.text(x, 2.85, '−OH', fontsize=9, fontstyle='italic', color=NEUTRAL,
             ha='center', fontweight='bold')

# KH550 molecules (as rectangles)
for x, label in [(2.2, 'KH550'), (6.0, 'KH550'), (10.0, 'KH550')]:
    rect = plt.Rectangle((x-0.8, 3.8), 1.6, 1.4, fill=True,
                          facecolor='#D6E4F0', edgecolor=COOL_BLUE,
                          linewidth=1.0, alpha=0.8)
    ax2.add_patch(rect)
    ax2.text(x, 4.5, f'{label}\n硅烷偶联剂', ha='center', va='center',
             fontsize=10, fontweight='bold', color=COOL_BLUE)

# Si-O-Al bond labels
for x in [2.2, 6.0, 10.0]:
    ax2.text(x, 3.5, 'Si−O−Al 共价键', ha='center', fontsize=8,
             fontstyle='italic', color=COOL_BLUE, fontweight='bold')

# -NH2 on top of KH550
for x in [2.2, 6.0, 10.0]:
    ax2.annotate('−NH₂', xy=(x, 5.2), xytext=(x, 6.2), fontsize=10,
                 fontweight='bold', color=WARM_ORANGE, ha='center',
                 arrowprops=dict(arrowstyle='->', color=WARM_ORANGE, lw=1.2))

# PEG chains above
for x, label in [(1.8, 'PEG4000 链段 ~'), (5.6, 'PEG4000 链段 ~'), (9.6, 'PEG4000 链段 ~')]:
    ax2.text(x, 7.0, label, fontsize=10, fontstyle='italic', color=MUTED_TEAL,
             fontweight='bold', ha='center')

# Anchoring mechanism box
ax2.text(7, 8.5, '锚定机制:\n① 静电吸引 (−NH₃⁺ ↔ −SiO⁻)\n② 氢键 (NH ↔ O−Si)\n③ 可能的 Si−O−Si / Si−N 缩合',
         fontsize=9, ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF8F0',
                   edgecolor=WARM_ORANGE, linewidth=0.8))

# Panel label
ax2.text(0.2, 9.5, 'b', fontsize=16, fontweight='bold', color=MUTED_TEAL,
         va='top', ha='left')


# ── Panel (c): State switching ──
ax3 = fig.add_axes([0.02, 0.02, 0.96, 0.20])
ax3.set_xlim(0, 14)
ax3.set_ylim(0, 3)
ax3.axis('off')

ax3.text(0.1, 2.7, 'c', fontsize=16, fontweight='bold', color=WARM_ORANGE,
         va='top', ha='left')
ax3.text(0.6, 2.7, '分散态 → 锚定态 功能切换', fontsize=14,
         fontweight='bold', ha='left', va='top')

# Dispersion state
rect1 = plt.Rectangle((0.3, 0.3), 3.5, 1.5, fill=True,
                       facecolor='#EAF4EE', edgecolor=MUTED_TEAL,
                       linewidth=1.2, alpha=0.8)
ax3.add_patch(rect1)
ax3.text(2.05, 1.05, '分散态（注入阶段）\nPEG 空间位阻稳定悬浮',
         ha='center', va='center', fontsize=12, fontweight='bold',
         color=MUTED_TEAL)

# Arrow
ax3.annotate('', xy=(4.2, 1.05), xytext=(3.8, 1.05),
             arrowprops=dict(arrowstyle='->', color=WARM_ORANGE, lw=2.5))
ax3.text(4.5, 2.1, '关井破胶\nPEG脱附降解', ha='center', fontsize=10,
         fontweight='bold', color=WARM_ORANGE)

# Anchoring state
rect2 = plt.Rectangle((5.0, 0.3), 3.5, 1.5, fill=True,
                       facecolor='#FDF1E8', edgecolor=WARM_ORANGE,
                       linewidth=1.2, alpha=0.8)
ax3.add_patch(rect2)
ax3.text(6.75, 1.05, '锚定态（关井破胶后）\n−NH₂ 与 Si−OH 多模式锚定',
         ha='center', va='center', fontsize=12, fontweight='bold',
         color=WARM_ORANGE)

# Trigger box
rect3 = plt.Rectangle((9.0, 0.3), 4.5, 1.5, fill=True,
                       facecolor='#F8F8F8', edgecolor=NEUTRAL,
                       linewidth=1.0, alpha=0.7)
ax3.add_patch(rect3)
ax3.text(11.25, 1.05, '触发条件:\n过硫酸铵 (NH₄)₂S₂O₈ + 储层温度 60−150 °C + 6−48 h',
         ha='center', va='center', fontsize=10, fontweight='bold',
         fontstyle='italic', color='#555555')

# ═══ Save ═══
svg_path = os.path.join(OUT, 'fig1_core_shell_matplotlib.svg')
pdf_path = os.path.join(OUT, 'fig1_core_shell_matplotlib.pdf')
png_path = os.path.join(OUT, 'fig1_core_shell_matplotlib.png')

fig.savefig(svg_path, format='svg', bbox_inches='tight', pad_inches=0.1)
fig.savefig(pdf_path, format='pdf', bbox_inches='tight', pad_inches=0.1)
fig.savefig(png_path, format='png', dpi=300, bbox_inches='tight', pad_inches=0.1)

plt.close(fig)

for p in [svg_path, pdf_path, png_path]:
    size_kb = os.path.getsize(p) / 1024
    print(f'  {os.path.basename(p)}  ({size_kb:.1f} KB)')

print('\nDone. Exported SVG/PDF (vector, journal-ready) + PNG (300 DPI).')