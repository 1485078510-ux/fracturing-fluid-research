# -*- coding: utf-8 -*-
"""
Publication-quality figure for Fe3O4/epoxy microsphere proppant BTC.
Optimized for thesis / journal paper.
"""
import numpy as np
from scipy.special import erfc
from scipy.integrate import trapezoid
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ==== Global style: clean, publication-ready ====
matplotlib.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 8,
    'figure.dpi': 300,
    'savefig.dpi': 600,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'axes.linewidth': 0.8,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
    'xtick.major.size': 3,
    'ytick.major.size': 3,
    'lines.linewidth': 1.5,
    'lines.markersize': 5,
})

# ==== Fitted parameters ====
c_bg  = 0.04590811
A     = 2334.008544
a_fit = 0.43116937
alpha = 107.08687055
Q     = 50.823237
t0    = 25.660680
sigma = 3.963037
R2    = 0.993864
RMSE  = 0.020969

# ==== Geometry & derived ====
x_val, d_val = 100.0, 5.0
PI = np.pi; XPD2 = x_val * PI * d_val**2
A_cross = PI * d_val**2 / 4.0
v = 4.0 * Q / (PI * d_val**2)
D_disp = alpha * v
Pe = x_val / alpha
t_pv = x_val / v

# ==== Data ====
t_data = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55,
                   60, 65, 70, 75, 80, 85, 90, 95, 100, 105])
c_data = np.array([0, 0.58438, 0.83879, 1.0, 0.92443, 0.64736, 0.35516,
                   0.29471, 0.27204, 0.24433, 0.20907, 0.21914, 0.19144,
                   0.19899, 0.17128, 0.20403, 0.17884, 0.16373, 0.16877,
                   0.15617, 0.15617, 0.15113])

def model(t, cb, A, a, al, Q, t0, s):
    dn = np.sqrt(np.abs(16.0*al*Q*t*PI*d_val**2)) + 1e-300
    z = (XPD2 - 4.0*Q*t) / dn
    cr = cb + (A*d_val)/dn * np.exp(-z*z)
    cf = cb + (a/2.0) * erfc(-z)
    w = 0.5*(1.0 + np.tanh((t0 - t)/s))
    return w*cr + (1.0-w)*cf

mask = t_data > 0
t_fit = t_data[mask]; c_fit = c_data[mask]
c_pred = model(t_fit, c_bg, A, a_fit, alpha, Q, t0, sigma)
residuals = c_fit - c_pred

t_smooth = np.linspace(0.01, 110, 3000)
c_smooth = model(t_smooth, c_bg, A, a_fit, alpha, Q, t0, sigma)

# Components for shading
dn_s = np.sqrt(np.abs(16.0*alpha*Q*t_smooth*PI*d_val**2)) + 1e-300
z_s = (XPD2 - 4.0*Q*t_smooth) / dn_s
cr_s = c_bg + (A*d_val)/dn_s * np.exp(-z_s*z_s)
cf_s = c_bg + (a_fit/2.0) * erfc(-z_s)
w_s = 0.5*(1.0 + np.tanh((t0 - t_smooth)/sigma))

# Mass recovery
M0 = trapezoid(c_smooth, t_smooth)
MRT = trapezoid(t_smooth*c_smooth, t_smooth) / M0
M0_tail = trapezoid((1-w_s)*cf_s, t_smooth)

# ==== Color palette (colorblind-friendly) ====
C_DATA  = '#000000'   # black for data
C_FIT   = '#D62728'   # red for fitted
C_RISE  = '#1F77B4'   # blue for rise
C_FALL  = '#2CA02C'   # green for fall
C_T0    = '#7F7F7F'   # gray for t0 line
C_BG    = '#BCBD22'   # olive for background

# ====== FIGURE 1: Main BTC (single panel, full-width) ======
fig1, ax1 = plt.subplots(1, 1, figsize=(7.0, 4.5))

# Shaded regions
ax1.fill_between(t_smooth, 0, cr_s, alpha=0.10, color=C_RISE, lw=0)
ax1.fill_between(t_smooth, 0, cf_s, alpha=0.10, color=C_FALL, lw=0)

# Component curves (thin dashed)
ax1.plot(t_smooth, cr_s, '--', color=C_RISE, lw=0.8, alpha=0.6)
ax1.plot(t_smooth, cf_s, '--', color=C_FALL, lw=0.8, alpha=0.6)

# Fitted curve
ax1.plot(t_smooth, c_smooth, '-', color=C_FIT, lw=1.8, zorder=5)

# Data points
ax1.plot(t_data, c_data, 'o', ms=5, mfc='white', mec=C_DATA, mew=1.2, zorder=6)

# Annotations
ax1.axvline(x=t0, color=C_T0, ls=':', lw=1.2, alpha=0.7)
ax1.axhline(y=c_bg, color=C_T0, ls='--', lw=0.8, alpha=0.5)

# Labels
ax1.set_xlabel('Time, $t$ (min)', fontsize=12)
ax1.set_ylabel('Normalized Fe Concentration, $C/C_{\\rm max}$', fontsize=12)

# Ticks
ax1.set_xlim(-2, 112)
ax1.set_ylim(-0.02, 1.12)
ax1.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax1.xaxis.set_minor_locator(ticker.MultipleLocator(5))
ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
ax1.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

# Legend
from matplotlib.lines import Line2D
leg = [
    Line2D([0],[0], marker='o', ms=5, mfc='white', mec=C_DATA, mew=1.2, lw=0,
           label='Experimental data'),
    Line2D([0],[0], color=C_FIT, lw=1.8, label='Fitted curve (Eq. 2)'),
    Line2D([0],[0], color=C_RISE, ls='--', lw=0.8, alpha=0.7,
           label='Rise component (pulse breakthrough)'),
    Line2D([0],[0], color=C_FALL, ls='--', lw=0.8, alpha=0.7,
           label='Fall component (retention tail)'),
    Line2D([0],[0], color=C_T0, ls=':', lw=1.2, label=f'$t_0$ = {t0:.1f} min'),
]
ax1.legend(handles=leg, loc='upper right', framealpha=0.9, edgecolor='#ccc',
           fontsize=8, ncol=1)

# Inset stats box
stats = (f"$R^2$ = {R2:.4f}\n"
         f"RMSE = {RMSE:.4f}\n"
         f"$v$ = {v:.2f} cm/min\n"
         f"$\\alpha$ = {alpha:.0f} cm\n"
         f"$Pe$ = {Pe:.3f}\n"
         f"1 PV = {t_pv:.1f} min")
ax1.text(0.02, 0.97, stats, transform=ax1.transAxes, fontsize=7,
         va='top', family='monospace',
         bbox=dict(boxstyle='round,pad=0.4', fc='#f8f8f8', ec='#ccc', alpha=0.9))

ax1.grid(True, alpha=0.2, lw=0.3)

plt.tight_layout()
fig1.savefig(r'c:\Users\郝\Desktop\claude\fig_btc_main.png', dpi=600)
fig1.savefig(r'c:\Users\郝\Desktop\claude\fig_btc_main.pdf', format='pdf')
fig1.savefig(r'c:\Users\郝\Desktop\claude\fig_btc_main.svg', format='svg')
print("Saved: fig_btc_main.png / .pdf / .svg")

# ====== FIGURE 2: Full multi-panel for thesis ======
fig2, axes = plt.subplots(2, 2, figsize=(7.5, 6.5))
(ax_a, ax_b), (ax_c, ax_d) = axes

# (a) Main BTC with components
ax_a.fill_between(t_smooth, 0, cr_s, alpha=0.08, color=C_RISE, lw=0)
ax_a.fill_between(t_smooth, 0, cf_s, alpha=0.08, color=C_FALL, lw=0)
ax_a.plot(t_smooth, c_smooth, '-', color=C_FIT, lw=1.5, zorder=5)
ax_a.plot(t_data, c_data, 'o', ms=4, mfc='white', mec=C_DATA, mew=1.0, zorder=6)
ax_a.axvline(x=t0, color=C_T0, ls=':', lw=1.0, alpha=0.6)
ax_a.axhline(y=c_bg, color=C_T0, ls='--', lw=0.6, alpha=0.4)
ax_a.set_xlabel('$t$ (min)')
ax_a.set_ylabel('$C/C_{\\rm max}$')
ax_a.set_title('(a) Breakthrough curve', fontsize=11, fontweight='bold')
ax_a.set_xlim(-2, 112); ax_a.set_ylim(-0.02, 1.12)
ax_a.text(0.02, 0.97, f'$R^2$ = {R2:.4f}', transform=ax_a.transAxes,
          fontsize=8, va='top', family='monospace',
          bbox=dict(boxstyle='round', fc='wheat', alpha=0.7, pad=0.3))
ax_a.grid(True, alpha=0.2, lw=0.3)

# (b) Log-linear tail
ax_b.semilogy(t_smooth, np.maximum(c_smooth,1e-8), '-', color=C_FIT, lw=1.5)
ax_b.semilogy(t_data, c_data, 'o', ms=4, mfc='white', mec=C_DATA, mew=1.0)
ax_b.axhline(y=c_bg, color=C_T0, ls='--', lw=0.8, alpha=0.5,
             label=f'$c_{{\\rm bg}}$ = {c_bg:.4f}')
ax_b.set_xlabel('$t$ (min)')
ax_b.set_ylabel('$C/C_{\\rm max}$')
ax_b.set_title('(b) Tail decay (log scale)', fontsize=11, fontweight='bold')
ax_b.legend(fontsize=7, framealpha=0.8)
ax_b.grid(True, alpha=0.2, lw=0.3)
ax_b.set_xlim(-2, 112)

# (c) Residuals
ax_c.axhline(y=0, color='gray', ls='-', lw=0.8)
ax_c.fill_between([-2,112], -2*RMSE, 2*RMSE, alpha=0.10, color='red', lw=0)
ax_c.plot(t_fit, residuals*100, 'o-', color='#2c3e50', ms=4, mfc='#2c3e50',
          lw=0.8)
ax_c.set_xlabel('$t$ (min)')
ax_c.set_ylabel('Residual $\\times 10^2$')
ax_c.set_title('(c) Residuals', fontsize=11, fontweight='bold')
ax_c.text(0.98, 0.95, f'$\\pm 2\\sigma$ = $\\pm${2*RMSE:.4f}',
          transform=ax_c.transAxes, fontsize=7, ha='right', va='top',
          bbox=dict(boxstyle='round', fc='white', alpha=0.8, pad=0.3))
ax_c.grid(True, alpha=0.2, lw=0.3)
ax_c.set_xlim(-2, 112)

# (d) Physical parameters summary
ax_d.axis('off')
summary = (
    "Physical Parameters\n"
    "===================\n\n"
    f"Interstitial velocity\n"
    f"  $v = 4Q/(\\pi d^2) = {v:.3f}$ cm/min\n\n"
    f"Dispersivity\n"
    f"  $\\alpha = {alpha:.1f}$ cm\n\n"
    f"Dispersion coefficient\n"
    f"  $D = \\alpha v = {D_disp:.1f}$ cm$^2$/min\n\n"
    f"Peclet number\n"
    f"  $Pe = L/\\alpha = {Pe:.4f}$\n\n"
    f"1 PV = {t_pv:.1f} min\n"
    f"MRT = {MRT:.1f} min\n"
    f"Tailing fraction = {M0_tail/M0*100:.1f}%\n\n"
    f"Column: $L$ = 100 cm, $d$ = 5 cm\n"
    f"Tracer: Fe$_3$O$_4$/epoxy microspheres"
)
ax_d.text(0.08, 0.95, summary, transform=ax_d.transAxes, fontsize=8,
          va='top', family='monospace',
          bbox=dict(boxstyle='round,pad=0.8', fc='#f0f4f8', ec='#bdc3c7',
                    alpha=0.95))

plt.tight_layout(pad=1.2)
fig2.savefig(r'c:\Users\郝\Desktop\claude\fig_multipanel.png', dpi=600)
fig2.savefig(r'c:\Users\郝\Desktop\claude\fig_multipanel.pdf', format='pdf')
fig2.savefig(r'c:\Users\郝\Desktop\claude\fig_multipanel.svg', format='svg')
print("Saved: fig_multipanel.png / .pdf / .svg")

print("\n=== All publication figures exported ===")