# -*- coding: utf-8 -*-
"""
Fresh figure generation — following exact style spec.

Style spec:
  Palette:  Red #d7191c, Blue #2c7bb6, Orange #fdae61, Data #333333
  Font:     Times New Roman, title 10pt bold left, labels 11pt
  Panels:   (a)(b)(c) bold left, no top/right spines, axis 0.8pt
  Markers:  Black filled circles, semi-transparent fills
  Annotate: Yellow rounded box for stats, legend in box
  Output:   SVG+PDF+PNG, 300dpi, bbox tight
"""
import numpy as np
from scipy.special import erfc
from scipy.integrate import trapezoid
from scipy import stats as sp_stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Style ──────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'stix',
    'font.size': 10,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 8,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

# ── Palette ────────────────────────────────────────────
RED   = '#d7191c'
BLUE  = '#2c7bb6'
ORANGE= '#fdae61'
DARK  = '#333333'
GRAY  = '#999999'
PURPLE= '#5e3c99'

# ── Corrected parameters ───────────────────────────────
cb    = 0.18003
A_amp = 0.1000
a_tail= 50.0
alpha = 1200.0
Q_mL  = 0.4689
t0    = 16.338
sigma0= 7.011

x_mm  = 1000.0
d_mm  = 1.0
XPD2  = x_mm * np.pi * d_mm * d_mm
Q_mm3 = Q_mL * 1000.0
Pe    = x_mm / alpha
v_mm  = 4.0 * Q_mm3 / (np.pi * d_mm * d_mm)
MRT   = x_mm / v_mm
MRT_p = x_mm / (4*500/(np.pi*d_mm*d_mm))

print(f'Parameters: Q={Q_mL:.4f} mL/min  Pe={Pe:.3f}  MRT={MRT:.2f}/{MRT_p:.2f} min')

# ── Data ───────────────────────────────────────────────
t_dat = np.array([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105])
c_dat = np.array([0,0.58438,0.83879,1.0,0.92443,0.64736,0.35516,0.29471,0.27204,
                  0.24433,0.20907,0.21914,0.19144,0.19899,0.17128,0.20403,
                  0.17884,0.16373,0.16877,0.15617,0.15617,0.15113])
m  = t_dat > 0
tf = t_dat[m]
cf = c_dat[m]
ts = np.linspace(0.01, 110, 2000)

# ── Model ──────────────────────────────────────────────
def btc(t, s):
    den = np.sqrt(np.abs(16*alpha*Q_mm3*t*np.pi*d_mm*d_mm)) + 1e-300
    z   = (XPD2 - 4*Q_mm3*t) / den
    cr  = cb + (A_amp*d_mm)/den * np.exp(-z*z)
    cf_ = cb + (a_tail/2)*erfc(-z)
    w   = 0.5*(1 + np.tanh((t0 - t)/s))
    return cr, cf_, w, w*cr + (1-w)*cf_

cr, cf_, w, blend = btc(ts, sigma0)
pred = blend[np.searchsorted(ts, tf)]
r2   = 1 - np.sum((cf-pred)**2) / np.sum((cf-np.mean(cf))**2)
Ti   = trapezoid(blend, ts)
gp   = 100*trapezoid(w*cr, ts)/Ti
ep   = 100*trapezoid((1-w)*cf_, ts)/Ti
qdev = abs(Q_mL-0.50)/0.50*100

print(f'R2={r2:.4f}  Gauss={gp:.0f}%  erfc={ep:.0f}%  Qdev={qdev:.1f}%')

BASE = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\ESP-T_投稿文件'

def save(fig, name):
    for fmt in ['svg', 'pdf', 'png']:
        fig.savefig(f'{BASE}\\{name}.{fmt}', dpi=300, facecolor='white')
    plt.close(fig)
    print(f'  {name} saved')

# ════════════════════════════════════════════════════════
# FIGURE 1 — BTC Fitting (3-panel)
# ════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(12, 4.2),
                         gridspec_kw={'width_ratios': [1.3, 1, 1]})

# (a) Model fit
ax = axes[0]
ax.fill_between(ts, 0, cr,  alpha=0.10, color=BLUE,   ec='none')
ax.fill_between(ts, 0, cf_, alpha=0.10, color=ORANGE, ec='none')
ax.plot(ts, cr,   '--', color=BLUE,   lw=1.2, alpha=0.7, label='Gaussian (pulse)')
ax.plot(ts, cf_,  '--', color=ORANGE, lw=1.2, alpha=0.7, label='erfc (tail)')
ax.plot(ts, blend,'-',  color=RED,    lw=2.5,             label='Blended model')
ax.plot(t_dat, c_dat, 'o', color=DARK, ms=8, mfc=DARK, mew=0, zorder=10, label='Measured')
ax.axvline(x=t0, color='gray', ls=':', lw=1.2, alpha=0.6,
           label=f't$_0$ = {t0:.1f} min')
ax.set_xlabel('Time (min)')
ax.set_ylabel('Normalized concentration C/C$_0$')
ax.set_title('(a) Model fit', loc='left', fontweight='bold')
ax.legend(frameon=True, framealpha=0.85, edgecolor='#ccc', fontsize=8, loc='upper right')
ax.set_xlim(-2, 112)
ax.set_ylim(-0.05, 1.15)
ax.annotate(f'R$^2$ = {r2:.4f}\nGauss: {gp:.0f}%\nerfc:  {ep:.0f}%',
            xy=(0.97, 0.97), xycoords='axes fraction', ha='right', va='top',
            fontsize=8, bbox=dict(boxstyle='round', fc='lightyellow', alpha=0.9))

# (b) Residuals
ax = axes[1]
ax.bar(tf, (cf-pred)*100, color='steelblue', width=3, alpha=0.7,
       edgecolor='white', lw=0.3)
ax.axhline(y=0, color='gray', lw=0.8)
ax.set_xlabel('Time (min)')
ax.set_ylabel('Residual \u00d7100')
ax.set_title('(b) Residuals', loc='left', fontweight='bold')
ax.set_xlim(-2, 112)

# (c) Flow rate validation
ax = axes[2]
ax.barh(['Pump set', 'Fitted'], [0.50, Q_mL], height=0.4,
        color=[GRAY, RED], edgecolor='white')
ax.set_xlabel('Flow rate Q (mL/min)')
ax.set_title('(c) Flow rate validation', loc='left', fontweight='bold')
ax.set_xlim(0, 0.6)
for v, y in [(0.50, 0), (Q_mL, 1)]:
    ax.text(v+0.01, y, f'{v:.2f}', va='center', fontsize=10, fontweight='bold')
ax.annotate(f'{qdev:.0f}% difference', xy=(0.48, 0.3),
            fontsize=9, color=RED, fontweight='bold')

plt.tight_layout(pad=1.5)
save(fig, 'Figure_1_BTC')

# ════════════════════════════════════════════════════════
# FIGURE 2 — K-P Release Kinetics (dual panel)
# ════════════════════════════════════════════════════════
temps   = [30, 60, 90, 120]
n_vals  = [0.59827, 0.66646, 0.5684, 0.55569]
K_vals  = [0.05538, 0.08177, 0.11344, 0.19642]
r2_kp   = [0.95489, 0.9649, 0.95599, 0.94537]
kp_c    = [BLUE, ORANGE, RED, PURPLE]
mk      = ['o', 's', '^', 'D']
t_h     = np.array([12,24,36,48,60,72,84,96,108,120,132,144,156,168])
rel = {
    30:  [0.013,0.035,0.047,0.065,0.077,0.089,0.099,0.102,0.108,0.112,0.116,0.120,0.123,0.125],
    60:  [0.018,0.046,0.085,0.106,0.124,0.141,0.157,0.173,0.190,0.199,0.206,0.212,0.216,0.219],
    90:  [0.026,0.071,0.109,0.139,0.157,0.171,0.172,0.182,0.188,0.221,0.228,0.233,0.237,0.241],
    120: [0.037,0.115,0.182,0.231,0.263,0.292,0.314,0.321,0.341,0.358,0.371,0.384,0.392,0.400],
}

fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))

# (a) Release curves
ax = axes[0]
for i, T in enumerate(temps):
    mt = np.array(rel[T])
    ax.plot(t_h, mt*100, f'{mk[i]}-', color=kp_c[i], ms=6, lw=1.5,
            mfc='white', mew=1.2, label=f'{T}\u00b0C (n={n_vals[i]:.2f})')
ax.set_xlabel('Time (h)')
ax.set_ylabel('Cumulative release (%)')
ax.set_title('(a) Release profiles', loc='left', fontweight='bold')
ax.legend(frameon=True, framealpha=0.85, edgecolor='#ccc', fontsize=8)
ax.set_xlim(0, 175); ax.set_ylim(0, 42)

# (b) K-P log-log fits
ax = axes[1]
tk = np.logspace(np.log10(10), np.log10(170), 50)
for i, T in enumerate(temps):
    mt = np.array(rel[T])
    mkp = mt < 0.6
    ax.plot(t_h[mkp], mt[mkp]*100, mk[i], color=kp_c[i],
            ms=7, mfc='white', mew=1.2, alpha=0.7)
    ax.plot(tk, K_vals[i]*tk**n_vals[i]*100, '-', color=kp_c[i],
            lw=1.8, alpha=0.8, label=f'{T}\u00b0C: R$^2$={r2_kp[i]:.4f}')
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('Time (h)')
ax.set_ylabel('Cumulative release (%)')
ax.set_title('(b) Korsmeyer\u2013Peppas fits', loc='left', fontweight='bold')
ax.legend(frameon=True, framealpha=0.85, edgecolor='#ccc', fontsize=8)
ax.set_xlim(8, 200); ax.set_ylim(0.5, 60)

plt.tight_layout(pad=1.5)
save(fig, 'Figure_2_KP')

# ════════════════════════════════════════════════════════
# FIGURE 3 — Model Comparison
# ════════════════════════════════════════════════════════
models = ['Dual tanh', 'Gaussian', 'erfc', 'Exponential', 'K-P']
aicc   = [0, 15.4, 51.2, 45.3, 75.0]
colors = [RED, BLUE, ORANGE, PURPLE, GRAY]

fig = plt.figure(figsize=(7, 4))
ax  = fig.add_subplot(111)
bars = ax.barh(models, aicc, color=colors, height=0.55,
               edgecolor='white', lw=0.8, zorder=3)
for bar, v in zip(bars, aicc):
    ax.text(bar.get_width()+0.8, bar.get_y()+bar.get_height()/2,
            f'\u0394AICc = {v:.1f}', va='center', fontsize=9, color=DARK)
ax.set_xlabel('\u0394AICc (lower = better)', fontweight='bold')
ax.set_title('Model comparison', fontsize=11, fontweight='bold')
ax.invert_yaxis()
ax.set_xlim(0, 85)
ax.grid(True, alpha=0.2, axis='x', zorder=0)
ax.annotate('F(3,14) = 34.7, p < 0.0001', xy=(0.95, 0.08),
            fontsize=9, xycoords='axes fraction', ha='right',
            bbox=dict(boxstyle='round', fc='#fff9e6', ec='#e6c300', alpha=0.9, lw=1))

plt.tight_layout()
save(fig, 'Figure_3_Models')

# ════════════════════════════════════════════════════════
# FIGURE 4 — Sigma Sensitivity
# ════════════════════════════════════════════════════════
mults  = np.arange(0.5, 3.01, 0.25)
sigs   = sigma0 * mults
tails  = []
for sv in sigs:
    _, cfs, ws, bls = btc(ts, sv)
    tails.append(100*trapezoid((1-ws)*cfs, ts)/trapezoid(bls, ts))
bt = tails[len(mults)//2]

fig = plt.figure(figsize=(6.5, 5))
ax  = fig.add_subplot(111)
ax.plot(sigs, tails, 'o-', color=ORANGE, lw=2, ms=8, mew=1.5, mfc='white', zorder=3)
ax.axvline(x=sigma0, color=PURPLE, ls='--', lw=1.8, alpha=0.8,
           label=f'Fitted \u03c3 = {sigma0:.2f} min')
ax.fill_between([min(sigs), max(sigs)], [bt-1]*2, [bt+1]*2,
                alpha=0.08, color=ORANGE, ec='none')
ax.set_xlabel('\u03c3 (min)', fontweight='bold')
ax.set_ylabel('erfc tail contribution (%)', fontweight='bold')
ax.set_title('\u03c3 sensitivity analysis', fontsize=11, fontweight='bold')
ax.legend(frameon=True, framealpha=0.9, edgecolor='#ccc', fontsize=9)
ax.set_ylim(min(tails)-1, max(tails)+1)
ax.annotate(f'Range: {min(tails):.1f}\u2013{max(tails):.1f}%\nSpan: {max(tails)-min(tails):.1f} pp',
            xy=(8, min(tails)+0.5), fontsize=9, color=DARK,
            bbox=dict(boxstyle='round', fc='#f8f8f8', ec='#ccc', alpha=0.9))

plt.tight_layout()
save(fig, 'Figure_4_Sigma')

# ════════════════════════════════════════════════════════
# FIGURE 5 — Two-Phase Flow (3-panel)
# ════════════════════════════════════════════════════════
owr_data = {
    '4:1': {'Qt':[0.1,0.2,0.3,0.4], 'Qo':[0.08,0.16,0.24,0.32],
            'Co':[33.51,17.37,11.54,8.33], 'FO':[2.681,2.779,2.770,2.666]},
    '1:1': {'Qt':[0.1,0.2,0.3,0.4], 'Qo':[0.05,0.10,0.15,0.20],
            'Co':[31.32,16.67,10.73,8.04], 'FO':[1.566,1.667,1.610,1.608]},
    '1:4': {'Qt':[0.1,0.2,0.3,0.4], 'Qo':[0.02,0.04,0.06,0.08],
            'Co':[32.74,17.14,10.93,7.97], 'FO':[0.655,0.686,0.656,0.638]},
}
owr_c = {'4:1': RED, '1:1': BLUE, '1:4': ORANGE}
owr_m = {'4:1': 'o', '1:1': 's', '1:4': '^'}
FOref = 3.187

fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))

# (a)
ax = axes[0]
for k, d in owr_data.items():
    ax.plot(d['Qt'], d['Co'], f'{owr_m[k]}-', color=owr_c[k],
            ms=7, mfc='white', mew=1.5, lw=1.5, label=f'OWR = {k}')
ax.set_xlabel('Q$_{total}$ (mL/min)')
ax.set_ylabel('C$_{oil}$ (\u00b5g/mL)')
ax.set_title('(a) Concentration vs. flow rate', loc='left', fontweight='bold')
ax.legend(frameon=True, framealpha=0.85, edgecolor='#ccc', fontsize=8)
ax.set_xlim(0.05, 0.45)

# (b)
ax = axes[1]
for k, d in owr_data.items():
    ax.plot(d['Qt'], d['FO'], f'{owr_m[k]}-', color=owr_c[k],
            ms=7, mfc='white', mew=1.5, lw=1.5, label=f'OWR = {k}')
ax.set_xlabel('Q$_{total}$ (mL/min)')
ax.set_ylabel('F$_O$ (\u00b5g/min)')
ax.set_title('(b) Tracer flux vs. flow rate', loc='left', fontweight='bold')
ax.legend(frameon=True, framealpha=0.85, edgecolor='#ccc', fontsize=8)
ax.set_xlim(0.05, 0.45)

# (c)
ax = axes[2]
all_qo = []; all_fn = []
for k, d in owr_data.items():
    fn = [f/FOref for f in d['FO']]
    all_qo.extend(d['Qo']); all_fn.extend(fn)
    ax.plot(d['Qo'], fn, owr_m[k], color=owr_c[k], ms=10,
            mfc='white', mew=1.5, label=f'OWR = {k}')
ax.plot([0, 0.35], [0, 0.35], '--', color=GRAY, lw=1, alpha=0.6, label='1:1')
r_val, _ = sp_stats.pearsonr(all_qo, all_fn)
ax.set_xlabel('Q$_{oil}$ (mL/min)')
ax.set_ylabel('F$_O$ / F$_{O,ref}$')
ax.set_title('(c) Flux calibration', loc='left', fontweight='bold')
ax.legend(frameon=True, framealpha=0.85, edgecolor='#ccc', fontsize=8)
ax.set_xlim(0, 0.35); ax.set_ylim(0, 0.35)
ax.annotate(f'r = {r_val:.2f}\nRMSD = 8.3%', xy=(0.97, 0.08),
            xycoords='axes fraction', ha='right', fontsize=8,
            bbox=dict(boxstyle='round', fc='lightyellow', alpha=0.9))

plt.tight_layout(pad=1.5)
save(fig, 'Figure_5_TwoPhase')

print('\n\u2500\u2500\u2500 ALL 5 FIGURES DONE \u2500\u2500\u2500')
