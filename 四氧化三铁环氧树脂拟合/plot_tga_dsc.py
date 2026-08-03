# -*- coding: utf-8 -*-
"""Plot TGA/DTG and DSC curves — publication quality."""
import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.signal import find_peaks
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
from pathlib import Path
import sys, io

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'svg.fonttype': 'none',
    'font.size': 9, 'axes.labelsize': 10,
    'xtick.labelsize': 8, 'ytick.labelsize': 8,
    'legend.fontsize': 7.5,
    'figure.facecolor': 'white', 'axes.facecolor': 'white',
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'xtick.direction': 'in', 'ytick.direction': 'in',
    'xtick.major.size': 4, 'ytick.major.size': 4,
    'xtick.minor.size': 2.5, 'ytick.minor.size': 2.5,
    'savefig.dpi': 300, 'savefig.bbox': 'tight',
    'legend.frameon': True, 'legend.framealpha': 0.85,
    'legend.edgecolor': '#cccccc',
})

PAL = {
    'blue':   '#0F4D92',
    'red':    '#D62728',
    'green':  '#2CA02C',
    'orange': '#FD8D3C',
    'purple': '#9467BD',
    'grey_d': '#333333',
    'grey_m': '#767676',
    'grey_l': '#B0B0B0',
}

# === Parse data ===
data_path = Path(r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\ESP-T_投稿文件\!&]1[1 25081373691.txt')
with open(data_path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

sections = [i for i, l in enumerate(lines) if l.strip().startswith('Curve Name:')]
print(f'Found {len(sections)} curve sections')

def parse_section(start, end):
    data = []
    header = False
    for line in lines[start:end]:
        if 'Index' in line and 'Value' in line: header = True; continue
        if header and line.strip():
            p = line.split()
            if len(p) >= 5:
                try: data.append([float(p[2]), float(p[4])])
                except: continue
    return np.array(data)

# TGA: sample temp vs weight %
tga = parse_section(sections[0], sections[1])
# DSC: sample temp vs heat flow
dsc = parse_section(sections[1], sections[2])

Ts = tga[:, 0]; Weight = tga[:, 1]
Ts_dsc = dsc[:, 0]; HF = dsc[:, 1]

# DTG computed from TGA
ws = uniform_filter1d(Weight, size=7)
DTG = np.gradient(ws) / np.gradient(Ts) * 20.0  # %/min (20 K/min)

# Key values
dtg_min_i = np.argmin(DTG)
dtg_T = Ts[dtg_min_i]; dtg_V = abs(DTG[dtg_min_i])
mass_350 = Weight[np.argmin(np.abs(Ts - 350))]
mass_800 = Weight[-1]
print(f'DTG peak: {dtg_T:.1f}°C, {dtg_V:.1f} %/min')
print(f'350°C mass: {mass_350:.1f}%, 800°C mass: {mass_800:.1f}%')

# === FIGURE ===
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2))
fig.subplots_adjust(wspace=0.35)

# ---- (a) TGA + DTG ----
C_TGA = PAL['blue']; C_DTG = PAL['red']

ax1.plot(Ts, Weight, '-', color=C_TGA, lw=2.0, zorder=3, label='Weight (%)')
ax1.set_ylabel('Weight (%)', color=C_TGA, fontweight='bold')
ax1.tick_params(axis='y', labelcolor=C_TGA)
ax1.set_ylim(0, 105)

# Twin axis for DTG
ax1b = ax1.twinx()
ax1b.plot(Ts, DTG, '-', color=C_DTG, lw=1.5, alpha=0.85, zorder=2, label='DTG (%/min)')
ax1b.set_ylabel('Derivative weight (%/min)', color=C_DTG, fontweight='bold')
ax1b.tick_params(axis='y', labelcolor=C_DTG)

# DTG peak marker + annotation
dtg_x = dtg_T; dtg_y = DTG[dtg_min_i]
ax1b.plot(dtg_x, dtg_y, 'o', color=C_DTG, ms=8, mfc='white', mew=2, zorder=5)
ax1b.annotate(f'{dtg_x:.0f} °C',
              xy=(dtg_x, dtg_y), xytext=(dtg_x - 60, dtg_y * 0.85),
              fontsize=8.5, color=C_DTG, fontweight='bold',
              arrowprops=dict(arrowstyle='->', color=C_DTG, lw=1.5, connectionstyle='arc3,rad=0.2'),
              bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=C_DTG, alpha=0.9))

# Decomposition shading
ax1.axvspan(300, 500, alpha=0.05, color=PAL['orange'], ec='none')
ax1.annotate('Decomposition\nregion', xy=(400, 15), fontsize=7.5,
             color=PAL['grey_m'], ha='center',
             bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7))

# Legend
leg1 = [Line2D([0],[0], color=C_TGA, lw=2.0, label='Weight (TGA)'),
        Line2D([0],[0], color=C_DTG, lw=1.5, label='Derivative (DTG)'),
        Line2D([0],[0], marker='o', ms=7, mfc='white', mec=C_DTG, mew=2, lw=0,
               label=f'DTG peak ({dtg_T:.0f} °C)')]
ax1.legend(handles=leg1, loc='upper right', fontsize=7.5, framealpha=0.85)

ax1.set_xlabel('Temperature (°C)')
ax1.set_xlim(25, 800)
ax1.text(-0.08, 1.05, 'a', transform=ax1.transAxes, fontsize=12, fontweight='bold', va='bottom')

# ---- (b) DSC ----
C_DSC = PAL['green']
ax2.plot(Ts_dsc, HF, '-', color=C_DSC, lw=1.8, zorder=3, label='Heat flow')
ax2.axhline(y=0, color=PAL['grey_l'], ls='--', lw=0.8, alpha=0.6, zorder=1)

# Fill exothermic region
ax2.fill_between(Ts_dsc, 0, HF, where=(HF > 0), alpha=0.08, color=C_DSC, ec='none')
ax2.fill_between(Ts_dsc, 0, HF, where=(HF < 0), alpha=0.05, color=PAL['red'], ec='none')

# Find and label DSC peaks
for direction, color, offset in [(1, C_DSC, 12), (-1, PAL['red'], -14)]:
    peaks, props = find_peaks(HF * direction, height=0.15, distance=80, prominence=0.1)
    for pk in peaks[:2]:
        t_pk = Ts_dsc[pk]; v_pk = HF[pk]
        ax2.plot(t_pk, v_pk, 'o', color=color, ms=7, mfc='white', mew=1.8, zorder=5)
        ax2.annotate(f'{t_pk:.0f} °C', xy=(t_pk, v_pk),
                     xytext=(0, offset), textcoords='offset points',
                     fontsize=7.5, color=color, ha='center', fontweight='bold')

# Exo/Endo labels
ax2.annotate('Exothermic', xy=(600, 1.5), fontsize=7.5, color=C_DSC, fontstyle='italic')
ax2.annotate('Endothermic', xy=(600, -1.5), fontsize=7.5, color=PAL['red'], fontstyle='italic')

ax2.set_xlabel('Temperature (°C)')
ax2.set_ylabel('Heat flow (W/g)', fontweight='bold')
ax2.set_xlim(25, 800)
ax2.legend(fontsize=7.5, loc='upper left', framealpha=0.85)
ax2.text(-0.08, 1.05, 'b', transform=ax2.transAxes, fontsize=12, fontweight='bold', va='bottom')

# Save
out_dir = Path(r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\Fuel_Figures')
out_dir.mkdir(exist_ok=True)
for fmt, dpi in [('svg', 300), ('pdf', 300), ('png', 600)]:
    fig.savefig(str(out_dir / f'Figure4_TGA_DSC.{fmt}'), format=fmt, dpi=dpi, facecolor='white')
    print(f'Saved: Figure4_TGA_DSC.{fmt}')
plt.close(fig)
print('Done.')
