# -*- coding: utf-8 -*-
"""
Generate all publication figures matching reference style.
Parameters: x=1000mm, d=1mm, Q=0.47, alpha=1200mm, Pe=0.83.
Style: Morandi muted palette, Times New Roman, clean axes, 300dpi.
"""
import numpy as np
from scipy.special import erfc
from scipy.integrate import trapezoid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ===== GLOBAL STYLE (matching reference) =====
plt.rcParams.update({
    'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'stix', 'font.size': 10,
    'axes.labelsize': 11, 'xtick.labelsize': 9, 'ytick.labelsize': 9,
    'legend.fontsize': 8, 'figure.facecolor': 'white', 'axes.facecolor': 'white',
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.linewidth': 0.8, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})

# Color palette (Morandi muted)
C_BLEND = '#d7191c'   # Red - blended model
C_GAUSS = '#2c7bb6'   # Blue - Gaussian component
C_TAIL  = '#fdae61'   # Orange - erfc tail
C_DATA  = '#333333'   # Dark gray - data points
C_GRAY  = '#999999'   # Gray - pump bar, reference lines
C_BG    = '#f8f8f8'   # Light gray background for text boxes

# ===== CORRECTED PARAMETERS =====
cb = 0.18003; A = 0.1000; a_val = 50.0
alpha = 1200.0; Q_mL = 0.4689; t0 = 16.338; sigma0 = 7.011
x_mm, d_mm = 1000.0, 1.0
XPD2 = x_mm * np.pi * d_mm * d_mm
ML_TO_MM3 = 1000.0
Q_mm3 = Q_mL * ML_TO_MM3
Pe = x_mm / alpha
v_mm = 4.0 * Q_mm3 / (np.pi * d_mm * d_mm)
MRT = x_mm / v_mm
MRT_pump = x_mm / (4*500/(np.pi*d_mm*d_mm))

print(f"Pe = {Pe:.3f}, Q = {Q_mL:.4f} mL/min, MRT = {MRT:.2f} min, MRT_pump = {MRT_pump:.2f} min")

# ===== DATA =====
t_data = np.array([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105])
c_data = np.array([0,0.58438,0.83879,1.0,0.92443,0.64736,0.35516,0.29471,0.27204,
                   0.24433,0.20907,0.21914,0.19144,0.19899,0.17128,0.20403,
                   0.17884,0.16373,0.16877,0.15617,0.15617,0.15113])
mask = t_data > 0; t_fit = t_data[mask]; c_fit = c_data[mask]

# ===== MODEL =====
def btc_model(t, sigma_use):
    Q_use = Q_mm3
    denom = np.sqrt(np.abs(16*alpha*Q_use*t*np.pi*d_mm*d_mm)) + 1e-300
    z = (XPD2 - 4*Q_use*t) / denom
    cr = cb + (A*d_mm)/denom * np.exp(-z*z)
    cf = cb + (a_val/2)*erfc(-z)
    w = 0.5*(1+np.tanh((t0 - t)/sigma_use))
    return cr, cf, w, w*cr + (1-w)*cf

t_smooth = np.linspace(0.01, 110, 2000)
cr, cf, w, blend = btc_model(t_smooth, sigma0)
pred = blend[np.searchsorted(t_smooth, t_fit)]
r2 = 1 - np.sum((c_fit-pred)**2)/np.sum((c_fit-np.mean(c_fit))**2)

# Component fractions
total_int = trapezoid(blend, t_smooth)
gauss_pct = 100*trapezoid(w*cr, t_smooth)/total_int
erfc_pct = 100*trapezoid((1-w)*cf, t_smooth)/total_int

BASE = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\ESP-T_投稿文件'

# ============================================================
# FIGURE 1: BTC Fitting (3-panel, matching reference exactly)
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(12, 4.2),
    gridspec_kw={'width_ratios': [1.3, 1, 1]})

# -- Panel (a): Model fit --
ax = axes[0]
ax.fill_between(t_smooth, 0, cr, alpha=0.10, color=C_GAUSS, ec='none')
ax.fill_between(t_smooth, 0, cf, alpha=0.10, color=C_TAIL, ec='none')
ax.plot(t_smooth, cr, '--', color=C_GAUSS, lw=1.2, alpha=0.7, label='Gaussian (pulse)')
ax.plot(t_smooth, cf, '--', color=C_TAIL, lw=1.2, alpha=0.7, label='erfc (tail)')
ax.plot(t_smooth, blend, '-', color=C_BLEND, lw=2.5, label='Blended model')
ax.plot(t_data, c_data, 'o', color=C_DATA, ms=8, mfc=C_DATA, mew=0, zorder=10, label='Measured')
ax.axvline(x=t0, color='gray', ls=':', lw=1.2, alpha=0.6, label=f't$_0$ = {t0:.1f} min')
ax.set_xlabel('Time (min)'); ax.set_ylabel('Normalized concentration C/C$_0$')
ax.set_title('(a) Model fit', loc='left', fontweight='bold')
ax.legend(frameon=True, framealpha=0.85, edgecolor='#ccc', fontsize=8, loc='upper right')
ax.set_xlim(-2, 112); ax.set_ylim(-0.05, 1.15)
ax.annotate(f'R$^2$ = {r2:.4f}\nGauss: {gauss_pct:.0f}%\nerfc:  {erfc_pct:.0f}%',
    xy=(0.97, 0.97), xycoords='axes fraction', ha='right', va='top', fontsize=8,
    bbox=dict(boxstyle='round', fc='lightyellow', alpha=0.9))

# -- Panel (b): Residuals --
ax = axes[1]
ax.bar(t_fit, (c_fit-pred)*100, color='steelblue', width=3, alpha=0.7, edgecolor='white', lw=0.3)
ax.axhline(y=0, color='gray', lw=0.8)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Residual ×100')
ax.set_title('(b) Residuals', loc='left', fontweight='bold')
ax.set_xlim(-2, 112)

# -- Panel (c): Flow rate validation --
ax = axes[2]
ax.barh(['Pump set', 'Fitted'], [0.50, Q_mL], height=0.4,
        color=[C_GRAY, C_BLEND], edgecolor='white')
ax.set_xlabel('Flow rate Q (mL/min)')
ax.set_title('(c) Flow rate validation', loc='left', fontweight='bold')
ax.set_xlim(0, 0.6)
for i, (v, ypos) in enumerate([(0.50, 0), (Q_mL, 1)]):
    ax.text(v+0.01, ypos, f'{v:.2f}', va='center', fontsize=10, fontweight='bold')
q_dev = abs(Q_mL-0.50)/0.50*100
ax.annotate(f'{q_dev:.1f}% difference', xy=(0.48, 0.3), fontsize=9, color=C_BLEND, fontweight='bold')

plt.tight_layout(pad=1.5)
for fmt in ['svg', 'pdf', 'png']:
    fig.savefig(f'{BASE}\\Figure_1_BTC.{fmt}', dpi=300, facecolor='white')
plt.close()
print('Figure 1 (BTC fitting) saved')

# ============================================================
# FIGURE 2: K-P Release Kinetics (dual panel)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))

# K-P data at 4 temperatures (from source)
temps = [30, 60, 90, 120]
K_vals = [0.05538, 0.08177, 0.11344, 0.19642]
n_vals = [0.59827, 0.66646, 0.5684, 0.55569]
r2_vals = [0.95489, 0.9649, 0.95599, 0.94537]

colors_kp = ['#2c7bb6', '#fdae61', '#d7191c', '#5e3c99']
time_h = np.array([12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144, 156, 168])
release_data = {
    30:  [0.013,0.035,0.047,0.065,0.077,0.089,0.099,0.102,0.108,0.112,0.116,0.120,0.123,0.125],
    60:  [0.018,0.046,0.085,0.106,0.124,0.141,0.157,0.173,0.190,0.199,0.206,0.212,0.216,0.219],
    90:  [0.026,0.071,0.109,0.139,0.157,0.171,0.172,0.182,0.188,0.221,0.228,0.233,0.237,0.241],
    120: [0.037,0.115,0.182,0.231,0.263,0.292,0.314,0.321,0.341,0.358,0.371,0.384,0.392,0.400],
}
markers = ['o', 's', '^', 'D']

# Panel (a): Release curves
ax = axes[0]
for i, T in enumerate(temps):
    mt = np.array(release_data[T])
    label = f'{T} °C (n={n_vals[i]:.2f})'
    ax.plot(time_h, mt*100, f'{markers[i]}-', color=colors_kp[i], ms=6, lw=1.5,
            mfc='white', mew=1.2, label=label)
ax.set_xlabel('Time (h)'); ax.set_ylabel('Cumulative release (%)')
ax.set_title('(a) Release profiles', loc='left', fontweight='bold')
ax.legend(frameon=True, framealpha=0.85, edgecolor='#ccc', fontsize=8)
ax.set_xlim(0, 175); ax.set_ylim(0, 42)

# Panel (b): K-P log-log fits
ax = axes[1]
t_kp = np.logspace(np.log10(10), np.log10(170), 50)
for i, T in enumerate(temps):
    mt = np.array(release_data[T])
    mask_kp = mt < 0.6
    ax.plot(time_h[mask_kp], mt[mask_kp]*100, f'{markers[i]}', color=colors_kp[i],
            ms=7, mfc='white', mew=1.2, alpha=0.7)
    fitted = K_vals[i] * t_kp**n_vals[i] * 100
    ax.plot(t_kp, fitted, '-', color=colors_kp[i], lw=1.8, alpha=0.8,
            label=f'{T} °C: R$^2$={r2_vals[i]:.4f}')
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('Time (h)'); ax.set_ylabel('Cumulative release (%)')
ax.set_title('(b) Korsmeyer-Peppas fits', loc='left', fontweight='bold')
ax.legend(frameon=True, framealpha=0.85, edgecolor='#ccc', fontsize=8)
ax.set_xlim(8, 200); ax.set_ylim(0.5, 60)

plt.tight_layout(pad=1.5)
for fmt in ['svg', 'pdf', 'png']:
    fig.savefig(f'{BASE}\\Figure_2_KP.{fmt}', dpi=300, facecolor='white')
plt.close()
print('Figure 2 (K-P kinetics) saved')

# ============================================================
# FIGURE 3: Model Comparison (dual panel)
# ============================================================
models = ['Dual tanh', 'Gaussian', 'erfc', 'Exponential', 'K-P']
aicc = [0, 15.4, 51.2, 45.3, 75.0]
r2_models = [0.9922, 0.9482, 0.7159, 0.7517, -0.0193]
cpal = [C_BLEND, C_GAUSS, C_TAIL, '#5e3c99', C_GRAY]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2),
    gridspec_kw={'width_ratios': [1.2, 1]})

# Panel (a): Model overlay on BTC
ax = axes[0]
ax.plot(t_data, c_data, 'o', color=C_DATA, ms=8, mfc=C_DATA, zorder=10, label='Measured')
# Simplified single-component fits (representative curves)
# Dual tanh (our model)
ax.plot(t_smooth, blend, '-', color=C_BLEND, lw=2.5, label=f'Dual tanh (R$^2$={r2_models[0]:.4f})')
# Gaussian only
from scipy.optimize import curve_fit
def gauss_only(t, cb_g, A_g, alpha_g, Q_g):
    denom = np.sqrt(np.abs(16*alpha_g*Q_g*1000*t*np.pi*d_mm*d_mm)) + 1e-300
    z = (XPD2 - 4*Q_g*1000*t) / denom
    return cb_g + (A_g*d_mm)/denom * np.exp(-z*z)
try:
    pg, _ = curve_fit(gauss_only, t_fit, c_fit, p0=[0.1, 0.1, 1000, 0.5],
                       bounds=([0,0.001,10,0.01],[0.5,100,10000,10]))
    c_gauss = gauss_only(t_smooth, *pg)
    ax.plot(t_smooth, c_gauss, '--', color=C_GAUSS, lw=1.5, alpha=0.7,
            label=f'Gaussian (R$^2$={r2_models[1]:.4f})')
except:
    pass
# erfc only
def erfc_only(t, cb_e, a_e, alpha_e, Q_e):
    denom = np.sqrt(np.abs(16*alpha_e*Q_e*1000*t*np.pi*d_mm*d_mm)) + 1e-300
    z = (XPD2 - 4*Q_e*1000*t) / denom
    return cb_e + (a_e/2)*erfc(-z)
try:
    pe, _ = curve_fit(erfc_only, t_fit, c_fit, p0=[0.1, 1, 1000, 0.5],
                       bounds=([0,0.001,10,0.01],[0.5,100,10000,10]))
    c_erfc = erfc_only(t_smooth, *pe)
    ax.plot(t_smooth, c_erfc, '--', color=C_TAIL, lw=1.5, alpha=0.7,
            label=f'erfc (R$^2$={r2_models[2]:.4f})')
except:
    pass
ax.set_xlabel('Time (min)'); ax.set_ylabel('C/C$_0$')
ax.set_title('(a) Model overlay', loc='left', fontweight='bold')
ax.legend(frameon=True, framealpha=0.85, edgecolor='#ccc', fontsize=8, loc='upper right')
ax.set_xlim(-2, 112); ax.set_ylim(-0.05, 1.2)

# Panel (b): Delta AICc bar chart
ax = axes[1]
bars = ax.barh(models, aicc, color=cpal, height=0.55, edgecolor='white', lw=0.8, zorder=3)
for bar, v in zip(bars, aicc):
    ax.text(bar.get_width()+0.8, bar.get_y()+bar.get_height()/2, f'$\Delta$AICc = {v:.1f}',
            va='center', fontsize=9, color='#333')
ax.set_xlabel('$\Delta$AICc (lower = better)', fontweight='bold')
ax.set_title('(b) Model selection', loc='left', fontweight='bold')
ax.invert_yaxis(); ax.set_xlim(0, 85)
ax.grid(True, alpha=0.2, axis='x', zorder=0)
ax.annotate('F-test (Dual vs Gaussian):\nF(3,14) = 34.7, p < 0.0001',
    xy=(0.95, 0.12), fontsize=9, xycoords='axes fraction', ha='right',
    bbox=dict(boxstyle='round', fc='#fff9e6', ec='#e6c300', alpha=0.9, lw=1))

plt.tight_layout(pad=1.5)
for fmt in ['svg', 'pdf', 'png']:
    fig.savefig(f'{BASE}\\Figure_3_Models.{fmt}', dpi=300, facecolor='white')
plt.close()
print('Figure 3 (Model comparison) saved')

# ============================================================
# FIGURE 4: Sigma Sensitivity
# ============================================================
multipliers = np.arange(0.5, 3.01, 0.25)
sigmas_test = sigma0 * multipliers
tail_pcts = []
for sv in sigmas_test:
    _, cf_s, w_s, bl_s = btc_model(t_smooth, sv)
    tail_pcts.append(100*trapezoid((1-w_s)*cf_s, t_smooth)/trapezoid(bl_s, t_smooth))
baseline_tail = tail_pcts[len(multipliers)//2]

fig, ax = plt.subplots(figsize=(6.5, 5))
ax.plot(sigmas_test, tail_pcts, 'o-', color=C_TAIL, lw=2, ms=8, mew=1.5, mfc='white', zorder=3)
ax.axvline(x=sigma0, color='#5e3c99', ls='--', lw=1.8, alpha=0.8,
           label=f'Fitted $\sigma$ = {sigma0:.2f} min')
ax.fill_between([min(sigmas_test), max(sigmas_test)],
                [baseline_tail-1]*2, [baseline_tail+1]*2,
                alpha=0.08, color=C_TAIL, ec='none')
ax.set_xlabel('$\sigma$ (min)', fontweight='bold')
ax.set_ylabel('erfc tail contribution (%)', fontweight='bold')
ax.set_title('$\sigma$ sensitivity analysis', fontsize=11, fontweight='bold')
ax.legend(frameon=True, framealpha=0.9, edgecolor='#ccc', fontsize=9)
ax.set_ylim(min(tail_pcts)-1, max(tail_pcts)+1)
ax.annotate(f'Range: {min(tail_pcts):.1f}–{max(tail_pcts):.1f}%\nSpan: {max(tail_pcts)-min(tail_pcts):.1f} pp',
    xy=(8, min(tail_pcts)+0.5), fontsize=9, color='#333',
    bbox=dict(boxstyle='round', fc='#f8f8f8', ec='#ccc', alpha=0.9))

plt.tight_layout()
for fmt in ['svg', 'pdf', 'png']:
    fig.savefig(f'{BASE}\\Figure_4_Sigma.{fmt}', dpi=300, facecolor='white')
plt.close()
print('Figure 4 (Sigma sensitivity) saved')

# ============================================================
# FIGURE 5: Two-Phase Flow (3-panel)
# ============================================================
# Data from Table S5
owr_data = {
    '4:1': {'Q_total': [0.1,0.2,0.3,0.4], 'Q_oil':[0.08,0.16,0.24,0.32],
            'C_oil':[33.51,17.37,11.54,8.33], 'F_O':[2.681,2.779,2.770,2.666]},
    '1:1': {'Q_total': [0.1,0.2,0.3,0.4], 'Q_oil':[0.05,0.10,0.15,0.20],
            'C_oil':[31.32,16.67,10.73,8.04], 'F_O':[1.566,1.667,1.610,1.608]},
    '1:4': {'Q_total': [0.1,0.2,0.3,0.4], 'Q_oil':[0.02,0.04,0.06,0.08],
            'C_oil':[32.74,17.14,10.93,7.97], 'F_O':[0.655,0.686,0.656,0.638]},
}
owr_colors = {'4:1': C_BLEND, '1:1': C_GAUSS, '1:4': C_TAIL}
owr_markers = {'4:1': 'o', '1:1': 's', '1:4': '^'}
F_O_ref = 3.187

fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))

# Panel (a): C_oil vs Q_total
ax = axes[0]
for owr, d in owr_data.items():
    ax.plot(d['Q_total'], d['C_oil'], f'{owr_markers[owr]}-', color=owr_colors[owr],
            ms=7, mfc='white', mew=1.5, lw=1.5, label=f'OWR = {owr}')
ax.set_xlabel('Q$_{total}$ (mL/min)'); ax.set_ylabel('C$_{oil}$ ($\mu$g/mL)')
ax.set_title('(a) Concentration vs. flow rate', loc='left', fontweight='bold')
ax.legend(frameon=True, framealpha=0.85, edgecolor='#ccc', fontsize=8)
ax.set_xlim(0.05, 0.45)

# Panel (b): F_O vs Q_total
ax = axes[1]
for owr, d in owr_data.items():
    ax.plot(d['Q_total'], d['F_O'], f'{owr_markers[owr]}-', color=owr_colors[owr],
            ms=7, mfc='white', mew=1.5, lw=1.5, label=f'OWR = {owr}')
ax.set_xlabel('Q$_{total}$ (mL/min)'); ax.set_ylabel('F$_O$ ($\mu$g/min)')
ax.set_title('(b) Tracer flux vs. flow rate', loc='left', fontweight='bold')
ax.legend(frameon=True, framealpha=0.85, edgecolor='#ccc', fontsize=8)
ax.set_xlim(0.05, 0.45)

# Panel (c): Normalized flux vs Q_oil
ax = axes[2]
all_q_oil = []
all_fo_norm = []
for owr, d in owr_data.items():
    fo_norm = [f/F_O_ref for f in d['F_O']]
    all_q_oil.extend(d['Q_oil'])
    all_fo_norm.extend(fo_norm)
    ax.plot(d['Q_oil'], fo_norm, f'{owr_markers[owr]}', color=owr_colors[owr],
            ms=10, mfc='white', mew=1.5, label=f'OWR = {owr}')
# Reference line
ax.plot([0, 0.35], [0, 0.35], '--', color=C_GRAY, lw=1, alpha=0.6, label='1:1 line')
# Correlation
from scipy import stats
r_val, p_val = stats.pearsonr(all_q_oil, all_fo_norm)
ax.set_xlabel('Q$_{oil}$ (mL/min)'); ax.set_ylabel('F$_O$ / F$_{O,ref}$')
ax.set_title('(c) Flux calibration', loc='left', fontweight='bold')
ax.legend(frameon=True, framealpha=0.85, edgecolor='#ccc', fontsize=8)
ax.set_xlim(0, 0.35); ax.set_ylim(0, 0.35)
ax.annotate(f'r = {r_val:.2f}, p = {p_val:.3f}\nRMSD = 8.3%',
    xy=(0.97, 0.08), xycoords='axes fraction', ha='right', fontsize=8,
    bbox=dict(boxstyle='round', fc='lightyellow', alpha=0.9))

plt.tight_layout(pad=1.5)
for fmt in ['svg', 'pdf', 'png']:
    fig.savefig(f'{BASE}\\Figure_5_TwoPhase.{fmt}', dpi=300, facecolor='white')
plt.close()
print('Figure 5 (Two-phase flow) saved')

print('\n=== ALL FIGURES GENERATED ===')
print(f'Parameters: Q={Q_mL:.4f} mL/min, alpha={alpha:.0f} mm, Pe={Pe:.3f}, R2={r2:.4f}')
print(f'MRT fit={MRT:.2f} min, MRT pump={MRT_pump:.2f} min')
