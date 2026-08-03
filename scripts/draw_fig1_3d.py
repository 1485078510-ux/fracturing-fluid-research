# -*- coding: utf-8 -*-
"""Fig 1 — SCI-style 3D core-shell phosphor structure. High-res raster + SVG."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
import numpy as np

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'axes.unicode_minus': False,
    'svg.fonttype': 'none',
})
OUT = r'c:\Users\郝\Desktop\claude\荧光压裂液'

# -- COLOR PALETTE (muted, SCI) --
C_CORE       = '#3A7CA5'   # phosphor core
C_CORE_DARK  = '#1A4A6B'
C_CORE_LIGHT = '#6BB3D9'
C_KH550      = '#8B5CF6'   # silane layer
C_KH550_DK   = '#5B2D8E'
C_PEG        = '#E8903A'   # PEG outer
C_PEG_DK     = '#B8651A'
C_SANDSTONE  = '#9B7B6B'
C_BG         = '#FFFFFF'
C_TEXT       = '#2D2D2D'
C_GRAY       = '#8C8C8C'

# ================================================================
# 3D SPHERE RENDERING via nested radial gradients
# ================================================================
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-4.5, 4.5); ax.set_ylim(-4.5, 4.5)
ax.set_aspect('equal'); ax.axis('off')

cx, cy = 0, 0
n_layers = 80  # granularity of radial gradient

# --- PEG outer halo (3D lighting: top-left highlight) ---
r_peg = 3.55
# Gradient: many thin concentric circles, opacity decreases outward
for i in range(n_layers):
    frac = i / n_layers
    r = r_peg - 0.6 + 0.8 * frac
    # opacity peaks at the ring boundary, fades in/out
    alpha = 0.02 + 0.12 * np.exp(-((frac - 0.55) / 0.25) ** 2)
    color = (232/255, 144/255, 58/255, alpha)
    ax.add_patch(Circle((cx, cy), r, fc='none', ec=color, lw=0.8))

# PEG dashed boundary rings (2 lines for depth)
for off, lw, alpha, dash in [(0, 2.5, 0.9, (8, 4)), (0.08, 1.2, 0.5, (4, 5)), (-0.06, 1.5, 0.35, (6, 5))]:
    c = Circle((cx+0.02, cy-0.02), r_peg+off, fc='none', ec=C_PEG, lw=lw, ls=(0, dash), alpha=alpha)
    ax.add_patch(c)

# --- KH550 shell (3D: thick ring with highlight) ---
r_kh = 2.85
# Back layer (darker, offset)
for off_x, off_y, color, alpha, lw in [(0.04, -0.04, C_KH550_DK, 0.3, 6),
                                          (0.02, -0.02, C_KH550_DK, 0.5, 4),
                                          (0, 0, C_KH550, 0.9, 5)]:
    ax.add_patch(Circle((cx+off_x, cy+off_y), r_kh, fc='none', ec=color, lw=lw, alpha=alpha))
# Surface highlight dots on KH550 layer
for angle in np.linspace(15, 355, 8):
    rad = np.radians(angle)
    ax.plot(r_kh * np.cos(rad), r_kh * np.sin(rad), '.', color='#C4A8F5', markersize=7, alpha=0.8)

# --- Core sphere (3D: radial gradient + specular highlight) ---
r_core = 2.2
# Dark base
ax.add_patch(Circle((cx, cy), r_core, fc=C_CORE_DARK, ec='none'))

# Radial gradient — many concentric circles from dark edge to bright center
for i in range(n_layers):
    frac = i / n_layers
    r = r_core * (1 - frac * 0.98)
    # Color transitions from center (bright) to edge (dark)
    t = frac ** 1.5  # nonlinear
    rr = int(C_CORE_LIGHT[1:3], 16) * (1-t) + int(C_CORE_DARK[1:3], 16) * t
    gg = int(C_CORE_LIGHT[3:5], 16) * (1-t) + int(C_CORE_DARK[3:5], 16) * t
    bb = int(C_CORE_LIGHT[5:7], 16) * (1-t) + int(C_CORE_DARK[5:7], 16) * t
    alpha = 0.15 + 0.6 * (1-t)
    ax.add_patch(Circle((cx, cy), r, fc=f'#{int(rr):02x}{int(gg):02x}{int(bb):02x}', ec='none', alpha=alpha))

# Specular highlight (top-left bright spot simulating light source)
hx, hy = -0.55, 0.55
hr = 0.65
for j in range(30):
    frac = j / 30
    r_spot = hr * (1 - frac * 0.9)
    alpha = 0.4 * (1 - frac)
    ax.add_patch(Circle((hx, hy), r_spot, fc='white', ec='none', alpha=alpha))

# Secondary specular (smaller, bottom-right)
hx2, hy2 = 0.4, -0.3
for j in range(15):
    frac = j / 15
    r_spot2 = 0.3 * (1 - frac * 0.85)
    alpha = 0.15 * (1 - frac)
    ax.add_patch(Circle((hx2, hy2), r_spot2, fc='white', ec='none', alpha=alpha))

# Core labels
ax.text(cx, cy+0.15, 'SrAl2O4', fontsize=14, ha='center', va='center', color='white', weight='bold')
ax.text(cx, cy-0.55, 'Eu2+, Dy3+', fontsize=11, ha='center', va='center', color='#D4EAF7')

# --- Callout lines (clean, thin) ---
# KH550 callout
ax.annotate('KH550 silane\nanchoring layer', xy=(-0.3, 2.85), xytext=(1.5, 4.0),
            fontsize=9, ha='center', color=C_KH550, weight='bold', va='center',
            arrowprops=dict(arrowstyle='->', color=C_KH550, lw=1.0, connectionstyle='arc3,rad=0.3'))
# PEG callout
ax.annotate('PEG4000\nshielding shell', xy=(3.55, -0.5), xytext=(2.2, -3.4),
            fontsize=9, ha='center', color=C_PEG, weight='bold', va='center',
            arrowprops=dict(arrowstyle='->', color=C_PEG, lw=1.0, connectionstyle='arc3,rad=-0.35'))

# --- Cutaway indicator (dashed line suggesting cross-section plane) ---
cut_theta = np.linspace(np.pi*0.35, np.pi*1.65, 40)
cut_r = r_peg + 0.3
cut_x = cut_r * np.cos(cut_theta)
cut_y = cut_r * np.sin(cut_theta)
ax.plot(cut_x, cut_y, color=C_GRAY, lw=1, ls='--', alpha=0.6, dashes=(5, 4))

# --- Legend panel (floating card) ---
legend_box = FancyBboxPatch((-4.2, -4.2), 3.8, 1.8, boxstyle='round,pad=0.15', fc='#FCFCFC', ec='#E0E0E0', lw=1, zorder=20)
ax.add_patch(legend_box)
items = [(C_CORE, 'Core: SrAl2O4:Eu2+,Dy3+'), (C_KH550, 'KH550 silane layer'), (C_PEG, 'PEG4000 shielding')]
for i, (color, label) in enumerate(items):
    ly = -4.0 + i * 0.55
    ax.add_patch(Rectangle((-4.0, ly-0.12), 0.3, 0.24, fc=color, ec='none', zorder=21))
    ax.text(-3.55, ly, label, fontsize=8, va='center', color=C_TEXT, zorder=21)

# --- Title ---
ax.set_title('Modified SrAl2O4:Eu2+,Dy3+ Phosphor Particle', fontsize=13, weight='bold', color=C_TEXT, pad=15)
# Subtitle
ax.text(0, -4.5, 'Figure 1. Core-shell architecture of the surface-modified persistent phosphor tracer.',
        fontsize=8, ha='center', color=C_GRAY, style='italic')

fig.savefig(f'{OUT}/fig1_sci_3d.png', dpi=400, bbox_inches='tight', facecolor=C_BG, edgecolor='none')
fig.savefig(f'{OUT}/fig1_sci_3d.svg', dpi=200, bbox_inches='tight', facecolor=C_BG, edgecolor='none')
plt.close(fig)
print('Fig1 SCI 3D core-shell saved.')