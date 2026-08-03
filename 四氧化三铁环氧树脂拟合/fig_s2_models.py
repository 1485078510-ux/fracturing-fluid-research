# -*- coding: utf-8 -*-
"""Figure S2: Model comparison — publication quality.
Core conclusion: dual-component model overwhelmingly preferred (ΔAICc=32.7)."""
import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.special import erfc
from scipy.stats import f as f_dist
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
C_DUAL  = '#d7191c'  # red — dual-component (best)
C_GAUSS = '#2c7bb6'  # blue — single Gaussian
C_ERFC  = '#fdae61'  # orange — single erfc
C_EXP   = '#5e3c99'  # purple — exponential
C_KP    = '#999999'  # gray — K-P
COLORS  = [C_DUAL, C_GAUSS, C_ERFC, C_EXP, C_KP]

# ---- Data ----
t_data = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55,
                   60, 65, 70, 75, 80, 85, 90, 95, 100, 105])
c_data = np.array([0, 0.58438, 0.83879, 1.0, 0.92443, 0.64736, 0.35516,
                   0.29471, 0.27204, 0.24433, 0.20907, 0.21914, 0.19144,
                   0.19899, 0.17128, 0.20403, 0.17884, 0.16373, 0.16877,
                   0.15617, 0.15617, 0.15113])
mask = t_data > 0
t_fit, c_fit = t_data[mask], c_data[mask]
N = len(t_fit)
x_val, d_val = 100.0, 5.0
XPD2 = x_val * np.pi * d_val * d_val

# ---- Model functions ----
def model_dual(t, c_bg, A, ap, alpha, Q, t0, sigma):
    denom = np.sqrt(np.abs(16.0*alpha*Q*t*np.pi*d_val*d_val)) + 1e-300
    z = (XPD2 - 4.0*Q*t) / denom
    cr = c_bg + (A*d_val)/denom * np.exp(-z*z)
    cf = c_bg + (ap/2.0) * erfc(-z)
    w = 0.5 * (1.0 + np.tanh((t0 - t)/sigma))
    return w*cr + (1-w)*cf

def model_gauss(t, c_bg, A, alpha, Q):
    denom = np.sqrt(np.abs(16.0*alpha*Q*t*np.pi*d_val*d_val)) + 1e-300
    z = (XPD2 - 4.0*Q*t) / denom
    return c_bg + (A*d_val)/denom * np.exp(-z*z)

def model_erfc(t, c_bg, ap, alpha, Q):
    denom = np.sqrt(np.abs(16.0*alpha*Q*t*np.pi*d_val*d_val)) + 1e-300
    z = (XPD2 - 4.0*Q*t) / denom
    return c_bg + (ap/2.0) * erfc(-z)

def model_exp(t, c_bg, c0, k):
    return c_bg + c0 * np.exp(-k*t)

def model_kp(t, c_bg, K, n):
    return c_bg + K * (t**n)

# ---- Universal fitting ----
def fit_model(fn, bounds, seeds=[42, 123, 456, 789]):
    def mse(p):
        pred = fn(t_fit, *p)
        return np.mean((pred - c_fit)**2)
    best = None
    for s in seeds:
        r = differential_evolution(mse, bounds, seed=s, maxiter=2000,
                                   tol=1e-12, popsize=50, polish=True)
        if best is None or r.fun < best.fun: best = r
    res = minimize(mse, best.x, method='L-BFGS-B', bounds=bounds,
                   options={'maxiter': 20000, 'ftol': 1e-16})
    if res.fun < best.fun: best = res
    pred = fn(t_fit, *best.x)
    rss = np.sum((c_fit - pred)**2)
    ss_tot = np.sum((c_fit - np.mean(c_fit))**2)
    return best.x, 1 - rss/ss_tot, np.sqrt(best.fun), rss, pred

# ---- Dual-component: use KNOWN best-fit parameters (from fit_solute.py, R²=0.9939) ----
p_dual = np.array([0.0459081074, 2334.0085437438, 0.4311693745, 107.0868705464, 50.8232372062, 25.6606800398, 3.9630374241])
pred_d = model_dual(t_fit, *p_dual)
rssd = np.sum((c_fit - pred_d)**2)
ss_tot = np.sum((c_fit - np.mean(c_fit))**2)
r2d = 1 - rssd / ss_tot
rmsed = np.sqrt(rssd / N)

# ---- Other 4 models: fit from scratch ----
bounds_gauss = [(0,0.4),(0.1,1e6),(0.01,1e5),(10,5000)]
bounds_erfc = [(0,0.4),(0.1,50),(0.01,1e5),(10,5000)]
bounds_exp = [(0,0.3),(0.1,2),(0.001,0.5)]
bounds_kp = [(0,0.3),(0.01,1),(0.1,1)]

print("Fitting 4 simpler models...")
p_gauss, r2g, rmseg, rssg, pred_g = fit_model(model_gauss, bounds_gauss)
p_erfc, r2e, rmsee, rsse, pred_e = fit_model(model_erfc, bounds_erfc)
p_exp, r2x, rmsex, rssx, pred_x = fit_model(model_exp, bounds_exp)
p_kp, r2k, rmsek, rssk, pred_k = fit_model(model_kp, bounds_kp)

# ---- AICc / BIC ----
def compute_ic(rss, N, k):
    aicc = N*np.log(rss/N) + 2*k + 2*k*(k+1)/(N-k-1) if N > k+1 else np.inf
    bic = N*np.log(rss/N) + k*np.log(N)
    return aicc, bic

models = [
    ('Dual-component\ntanh-blended', 7, r2d, rmsed, rssd, pred_d, p_dual),
    ('Single\nGaussian', 4, r2g, rmseg, rssg, pred_g, p_gauss),
    ('Single\nerfc', 4, r2e, rmsee, rsse, pred_e, p_erfc),
    ('Exponential\ndecay', 3, r2x, rmsex, rssx, pred_x, p_exp),
    ('Korsmeyer-\nPeppas', 3, r2k, rmsek, rssk, pred_k, p_kp),
]

for i, (name, k, r2, rmse, rss, pred, params) in enumerate(models):
    aicc, bic = compute_ic(rss, N, k)
    models[i] = (name, k, r2, rmse, rss, pred, params, aicc, bic)

best_aicc = min(m[7] for m in models)
best_bic  = min(m[8] for m in models)

# Akaike weights
deltas = np.array([m[7] - best_aicc for m in models])
weights = np.exp(-0.5 * deltas)
weights /= weights.sum()

# F-test dual vs gauss
F_stat = ((rssg - rssd)/(7-4)) / (rssd/(N-7))
p_val = 1 - f_dist.cdf(F_stat, 3, N-7)

# ---- Build figure ----
fig = plt.figure(figsize=(7.5, 5.5))
gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 0.9], wspace=0.28)

# ======== Panel (a): Model fits overlay ========
ax_a = fig.add_subplot(gs[0, 0])
t_smooth = np.linspace(0.01, 110, 2000)

# Plot data
ax_a.plot(t_fit, c_fit, 'o', color='#333333', ms=7, mfc='#333333',
          mew=0, zorder=10, label='Measured')

# Plot models in order of quality
plot_order = [
    (model_dual, p_dual, C_DUAL, '-', 2.8, 'Dual-comp. tanh'),
    (model_gauss, p_gauss, C_GAUSS, '--', 1.5, 'Single Gaussian'),
    (model_erfc, p_erfc, C_ERFC, '-.', 1.5, 'Single erfc'),
    (model_exp, p_exp, C_EXP, ':', 1.5, 'Exponential'),
    (model_kp, p_kp, C_KP, (0, (3,2,1,2)), 1.2, 'K-P power law'),
]

for fn, params, color, ls, lw, label in plot_order:
    y = fn(t_smooth, *params)
    ax_a.plot(t_smooth, y, color=color, ls=ls, lw=lw, alpha=0.85, label=label)

# R² annotations
r2_labels = [
    (80, 0.25, f'R² = {r2d:.4f}', C_DUAL),
    (80, 0.22, f'R² = {r2g:.4f}', C_GAUSS),
    (80, 0.19, f'R² = {r2e:.4f}', C_ERFC),
    (80, 0.16, f'R² = {r2x:.4f}', C_EXP),
    (80, 0.13, f'R² = {r2k:.4f}', C_KP),
]
for x, y, txt, c in r2_labels:
    ax_a.text(x, y, txt, fontsize=6.5, color=c, fontweight='bold',
              fontfamily='serif')

ax_a.set_xlabel('Time (min)', fontweight='bold')
ax_a.set_ylabel('Normalized concentration C/C₀', fontweight='bold')
ax_a.set_title('a', loc='left', fontweight='bold', fontsize=11)
ax_a.set_title('Candidate model fits', loc='center', fontsize=9, pad=8)
ax_a.legend(frameon=True, framealpha=0.9, edgecolor='#cccccc',
            fontsize=7, loc='upper right', ncol=1)
ax_a.set_xlim(-2, 112)
ax_a.set_ylim(-0.05, 1.15)

# Highlight tail region
ax_a.axvspan(50, 110, alpha=0.04, color=C_ERFC, ec='none')
ax_a.annotate('Tail region\n(t > 50 min)', xy=(80, 0.95), fontsize=7,
              color='#666666', ha='center',
              bbox=dict(boxstyle='round', fc='white', alpha=0.7))

# ======== Panel (b): ΔAICc bar chart ========
ax_b = fig.add_subplot(gs[0, 1])
names = [m[0] for m in models]
aicc_vals = [m[7] for m in models]
deltas_plot = [m[7] - best_aicc for m in models]

y_pos = range(len(models))
bars = ax_b.barh(y_pos, deltas_plot, height=0.55, color=COLORS,
                 edgecolor='white', linewidth=0.8, zorder=3)

# Value labels on bars
for i, (bar, d, w) in enumerate(zip(bars, deltas_plot, weights)):
    x_pos = bar.get_width() + 0.8
    ax_b.text(x_pos, bar.get_y() + bar.get_height()/2,
              f'ΔAICc = {d:.1f}    w = {w:.4f}',
              va='center', fontsize=7.5, fontfamily='serif',
              color='#333333')

# R² labels inside bars
for i, (bar, m) in enumerate(zip(bars, models)):
    if bar.get_width() > 10:
        ax_b.text(bar.get_width()/2, bar.get_y() + bar.get_height()/2,
                  f'R² = {m[2]:.4f}', va='center', ha='center',
                  fontsize=7, color='white', fontweight='bold',
                  fontfamily='serif')

ax_b.set_yticks(y_pos)
ax_b.set_yticklabels(names, fontsize=8)
ax_b.set_xlabel('ΔAICc (lower is better)', fontweight='bold')
ax_b.set_title('b', loc='left', fontweight='bold', fontsize=11)
ax_b.set_title('Model selection by AICc', loc='center', fontsize=9, pad=8)
ax_b.invert_yaxis()
ax_b.grid(True, alpha=0.2, axis='x', zorder=0)
ax_b.set_xlim(0, max(deltas_plot) * 1.25)

# F-test annotation
ax_b.annotate(f'F-test (Dual vs. Gaussian):\n'
              f'F(3, 14) = {F_stat:.1f}\n'
              f'p = {p_val:.1e}',
              xy=(0.95, 0.12), fontsize=7.5, fontfamily='serif',
              xycoords='axes fraction', ha='right',
              bbox=dict(boxstyle='round,pad=0.5', fc='#fff9e6',
                        ec='#e6c300', alpha=0.9, lw=1))

# ---- Save ----
out_svg = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\Figure_S2.svg'
out_pdf = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\Figure_S2.pdf'
out_png = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\Figure_S2.png'
fig.savefig(out_svg, format='svg', dpi=300, facecolor='white')
fig.savefig(out_pdf, format='pdf', dpi=300, facecolor='white')
fig.savefig(out_png, format='png', dpi=600, facecolor='white')
plt.close(fig)
print(f'Saved: {out_pdf}')
print(f'Saved: {out_png}')