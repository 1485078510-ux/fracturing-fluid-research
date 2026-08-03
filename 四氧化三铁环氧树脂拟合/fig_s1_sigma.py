# -*- coding: utf-8 -*-
"""Figure S1: σ sensitivity analysis — publication quality.
Core conclusion: tail fraction varies < 1 pp across 6× σ range."""
import numpy as np
from scipy.special import erfc
from scipy.integrate import trapezoid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ---- Global style ----
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'stix',
    'font.size': 9,
    'axes.titlesize': 10,
    'axes.labelsize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 7.5,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'lines.linewidth': 1.5,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})

# ---- Color palette (colorblind-friendly) ----
C_RISE  = '#2c7bb6'  # blue — Gaussian
C_TAIL  = '#fdae61'  # orange — erfc tail
C_BLEND = '#d7191c'  # red — blended
C_SIGMA = '#5e3c99'  # purple — sigma marker
C_WEIGHT = '#999999' # gray — weight

# ---- Best-fit parameters ----
c_bg   = 0.0459081074
A      = 2334.0085437438
a      = 0.4311693745
alpha  = 107.0868705464
Q      = 50.8232372062
t0     = 25.6606800398
sigma0 = 3.9630374241

x_val, d_val = 100.0, 5.0
XPD2 = x_val * np.pi * d_val * d_val

def components(t, sigma):
    denom = np.sqrt(np.abs(16.0 * alpha * Q * t * np.pi * d_val * d_val)) + 1e-300
    z = (XPD2 - 4.0 * Q * t) / denom
    c_rise = c_bg + (A * d_val) / denom * np.exp(-z * z)
    c_fall = c_bg + (a / 2.0) * erfc(-z)
    weight = 0.5 * (1.0 + np.tanh((t0 - t) / sigma))
    c_blend = weight * c_rise + (1.0 - weight) * c_fall
    return c_rise, c_fall, weight, c_blend

# ---- Compute sigma scan ----
multipliers = np.arange(0.5, 3.01, 0.25)
sigmas = sigma0 * multipliers
tail_pcts = []
t_fine = np.linspace(0.01, 110, 5000)

for sv in sigmas:
    cr, cf, w, cb = components(t_fine, sv)
    total = trapezoid(cb, t_fine)
    tail_integ = trapezoid((1 - w) * cf, t_fine)
    tail_pcts.append(100 * tail_integ / total)

gauss_pcts = [100 - tp for tp in tail_pcts]

# At sigma=4.0
_, _, _, cb4 = components(t_fine, 4.0)
cr4, cf4, w4, _ = components(t_fine, 4.0)
tail4 = 100 * trapezoid((1 - w4) * cf4, t_fine) / trapezoid(cb4, t_fine)
baseline_tail = tail_pcts[len(multipliers)//2]  # at sigma0

# ---- Build figure ----
fig = plt.figure(figsize=(7.2, 5.8))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1],
                       hspace=0.35, wspace=0.32)

# ======== Panel (a): Tail fraction vs σ ========
ax_a = fig.add_subplot(gs[0, 0])
ax_a.plot(sigmas, tail_pcts, 'o-', color=C_TAIL, lw=2, ms=6,
          markeredgecolor='white', markeredgewidth=1.2, zorder=3,
          label='erfc tail contribution')
ax_a.axvline(x=sigma0, color=C_SIGMA, ls='--', lw=1.6, alpha=0.8,
             label=f'fitted σ = {sigma0:.2f} min')
ax_a.axvline(x=4.0, color='#555555', ls=':', lw=1.2, alpha=0.7,
             label='σ = 4.0 min')

# Stability band
ax_a.fill_between([min(sigmas), max(sigmas)],
                  [baseline_tail - 1, baseline_tail - 1],
                  [baseline_tail + 1, baseline_tail + 1],
                  alpha=0.08, color=C_TAIL, ec='none')

ax_a.set_xlabel('σ (min)', fontweight='bold')
ax_a.set_ylabel('erfc tail fraction (%)', fontweight='bold')
ax_a.set_title('a', loc='left', fontweight='bold', fontsize=11)
# Secondary title
ax_a.set_title('Tail fraction vs. transition width', loc='center',
               fontsize=9, pad=8)
ax_a.legend(frameon=True, framealpha=0.9, edgecolor='#cccccc',
            fontsize=7, loc='lower left')
ax_a.yaxis.set_major_locator(MultipleLocator(5))
ax_a.set_ylim(44, 50)

# Annotate stability
ax_a.annotate(f'Range: {min(tail_pcts):.1f}–{max(tail_pcts):.1f}%\n'
              f'Span: {max(tail_pcts)-min(tail_pcts):.1f} pp',
              xy=(8, 45.5), fontsize=7.5, color='#333333',
              bbox=dict(boxstyle='round,pad=0.4', fc='#f8f8f8',
                        ec='#cccccc', alpha=0.9))

# ======== Panel (b): Component decomposition ========
ax_b = fig.add_subplot(gs[0, 1])
t_plot = np.linspace(0.01, 110, 1500)
cr_p, cf_p, w_p, cb_p = components(t_plot, sigma0)

ax_b.fill_between(t_plot, 0, cr_p, alpha=0.12, color=C_RISE, ec='none')
ax_b.fill_between(t_plot, 0, cf_p, alpha=0.12, color=C_TAIL, ec='none')
ax_b.plot(t_plot, cr_p, '--', color=C_RISE, lw=1.2, alpha=0.7,
          label='Gaussian (rise)')
ax_b.plot(t_plot, cf_p, '--', color=C_TAIL, lw=1.2, alpha=0.7,
          label='erfc (tail)')
ax_b.plot(t_plot, cb_p, '-', color=C_BLEND, lw=2.2, label='Blended')
ax_b.plot(t_plot, w_p, '-', color=C_WEIGHT, lw=0.9, alpha=0.6,
          label='Weight w(t)')
ax_b.axvline(x=t0, color='gray', ls=':', lw=1, alpha=0.6)

# Annotate component percentages
gauss_base = gauss_pcts[len(multipliers)//2]
tail_base = tail_pcts[len(multipliers)//2]
ax_b.annotate(f'Gaussian\n{gauss_base:.0f}%', xy=(12, 0.58), fontsize=8,
              color=C_RISE, fontweight='bold', ha='center',
              bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=C_RISE,
                        alpha=0.85, lw=0.8))
ax_b.annotate(f'erfc tail\n{tail_base:.0f}%', xy=(65, 0.24), fontsize=8,
              color=C_TAIL, fontweight='bold', ha='center',
              bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=C_TAIL,
                        alpha=0.85, lw=0.8))

ax_b.set_xlabel('Time (min)', fontweight='bold')
ax_b.set_ylabel('Normalized concentration C/C₀', fontweight='bold')
ax_b.set_title('b', loc='left', fontweight='bold', fontsize=11)
ax_b.set_title(f'Component decomposition (σ = {sigma0:.2f} min)',
               loc='center', fontsize=9, pad=8)
ax_b.legend(frameon=True, framealpha=0.9, edgecolor='#cccccc',
            fontsize=7, loc='upper right', ncol=2)
ax_b.set_xlim(-2, 112)

# ======== Panel (c): Blended BTCs at different σ ========
ax_c = fig.add_subplot(gs[1, 0])
sigma_vals = [sigma0*0.5, sigma0*0.75, sigma0, sigma0*1.5, sigma0*2.5, sigma0*3.0]
colors = plt.cm.RdYlBu_r(np.linspace(0.1, 0.85, len(sigma_vals)))

for sv, col in zip(sigma_vals, colors):
    _, _, _, cb_s = components(t_plot, sv)
    lw = 2.5 if abs(sv - sigma0) < 0.1 else 1.2
    ls = '-' if abs(sv - sigma0) < 0.1 else '--'
    label = f'σ = {sv:.1f}' + (' (fitted)' if abs(sv-sigma0) < 0.1 else '')
    ax_c.plot(t_plot, cb_s, color=col, lw=lw, ls=ls, alpha=0.9, label=label)

ax_c.set_xlabel('Time (min)', fontweight='bold')
ax_c.set_ylabel('Normalized concentration C/C₀', fontweight='bold')
ax_c.set_title('c', loc='left', fontweight='bold', fontsize=11)
ax_c.set_title('BTC insensitivity to σ', loc='center', fontsize=9, pad=8)
ax_c.legend(frameon=True, framealpha=0.9, edgecolor='#cccccc',
            fontsize=7, loc='upper right')
ax_c.set_xlim(-2, 112)

# ======== Panel (d): Key insights text ========
ax_d = fig.add_subplot(gs[1, 1])
ax_d.axis('off')
insights = (
    'Key findings\n'
    '──────────────\n'
    f'• Fitted σ = {sigma0:.2f} min\n'
    f'  erfc tail = {tail_base:.1f}%\n'
    f'• σ = 4.0 min (sampling interval)\n'
    f'  erfc tail = {tail4:.1f}%\n'
    f'• Sigma range:\n'
    f'  [{min(sigmas):.1f}, {max(sigmas):.1f}] min\n'
    f'  (0.5× to 3× fitted value)\n'
    f'• Tail range: {min(tail_pcts):.1f}–{max(tail_pcts):.1f}%\n'
    f'• Total span: {max(tail_pcts)-min(tail_pcts):.1f} pp\n'
    f'\n'
    f'Conclusion\n'
    f'──────────────\n'
    f'The 47% tail decomposition\n'
    f'is robust to σ choice.\n'
    f'A single shut-in suffices.'
)
ax_d.text(0.05, 0.95, insights, transform=ax_d.transAxes,
          fontsize=8.5, fontfamily='serif', va='top',
          bbox=dict(boxstyle='round,pad=0.8', fc='#fafafa',
                    ec='#cccccc', alpha=0.9))

# ---- Save ----
out_svg = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\Figure_S1.svg'
out_pdf = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\Figure_S1.pdf'
out_png = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\Figure_S1.png'
fig.savefig(out_svg, format='svg', dpi=300, facecolor='white')
fig.savefig(out_pdf, format='pdf', dpi=300, facecolor='white')
fig.savefig(out_png, format='png', dpi=600, facecolor='white')
plt.close(fig)
print(f'Saved: {out_pdf}')
print(f'Saved: {out_png}')