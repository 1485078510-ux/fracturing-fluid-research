# -*- coding: utf-8 -*-
"""
Export fitting results to text, CSV, and enhanced plot.
"""
import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.special import erfc
import matplotlib.pyplot as plt
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ========== Data ==========
t_data = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55,
                   60, 65, 70, 75, 80, 85, 90, 95, 100, 105])
c_data = np.array([0, 0.58438, 0.83879, 1.0, 0.92443, 0.64736, 0.35516,
                   0.29471, 0.27204, 0.24433, 0.20907, 0.21914, 0.19144,
                   0.19899, 0.17128, 0.20403, 0.17884, 0.16373, 0.16877,
                   0.15617, 0.15617, 0.15113])

mask = t_data > 0
t_fit = t_data[mask]; c_fit = c_data[mask]; N = len(t_fit)

# ========== Constants ==========
x_val, d_val, PI = 100.0, 5.0, np.pi
XPD2 = x_val * PI * d_val * d_val
OUT_DIR = r'c:\Users\郝\Desktop\claude'

def model_smooth(t, c_bg, A, a_param, alpha, Q, t0, sigma):
    denom = np.sqrt(np.abs(16.0 * alpha * Q * t * PI * d_val * d_val)) + 1e-300
    z = (XPD2 - 4.0 * Q * t) / denom
    c_rise = c_bg + (A * d_val) / denom * np.exp(-z * z)
    c_fall = c_bg + (a_param / 2.0) * erfc(-z)
    weight = 0.5 * (1.0 + np.tanh((t0 - t) / sigma))
    return weight * c_rise + (1.0 - weight) * c_fall

def mse(p):
    c_bg, A, a_param, alpha, Q, t0, sigma = p
    if c_bg<0 or c_bg>0.5 or A<=0 or A>1e6: return 1e10
    if a_param<=0 or a_param>100 or alpha<=0 or alpha>1e6: return 1e10
    if Q<1 or Q>1e4 or t0<1 or t0>55: return 1e10
    if sigma<0.1 or sigma>20: return 1e10
    return np.mean((model_smooth(t_fit, *p) - c_fit)**2)

bounds = [(0,0.4),(0.1,1e6),(0.1,50),(0.01,1e5),(10,5000),(5,40),(0.5,15)]

# Fit
best = None
for seed in [42, 123, 456, 789, 1024]:
    r = differential_evolution(mse, bounds, seed=seed, maxiter=2000, tol=1e-12,
                               popsize=50, mutation=(0.5,1.5), recombination=0.9, polish=True)
    if best is None or r.fun < best.fun: best = r
res = minimize(mse, best.x, method='L-BFGS-B', bounds=bounds,
               options={'maxiter':20000, 'ftol':1e-16, 'gtol':1e-16})
if res.fun < best.fun: best = res

c_bg, A, a_param, alpha, Q, t0, sigma = best.x
c_pred = model_smooth(t_fit, *best.x)
residuals = c_fit - c_pred
ss_res = np.sum(residuals**2)
ss_tot = np.sum((c_fit - np.mean(c_fit))**2)
r2 = 1 - ss_res/ss_tot
rmse = np.sqrt(best.fun)

# Hessian SE
try:
    eps=1e-6; hes=np.zeros((7,7)); f0=best.fun
    for i in range(7):
        for j in range(7):
            pp=best.x.copy(); pp[i]+=eps; pp[j]+=eps
            pi_=best.x.copy(); pi_[i]+=eps
            pj_=best.x.copy(); pj_[j]+=eps
            hes[i,j]=(mse(pp)-mse(pi_)-mse(pj_)+f0)/(eps*eps)
    cov = np.linalg.inv(0.5*hes)*(best.fun*N/max(1,N-7))
    std = np.sqrt(np.abs(np.diag(cov)))
except: std = np.full(7, np.nan)

# ========== EXPORT 1: Text report ==========
report_path = os.path.join(OUT_DIR, 'fit_report.txt')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("=" * 65 + "\n")
    f.write("   Piecewise Solute Transport Model - Fitting Report\n")
    f.write("=" * 65 + "\n\n")
    f.write(f"Date: 2026-05-27\n")
    f.write(f"Data points: {len(t_data)} (t=0..105), fitted on {N} points (t>0)\n\n")

    f.write("--- Model Formula ---\n")
    f.write("  Constants: x = 1 m = 100 cm,  d = 5 cm\n")
    f.write("  z = (x*pi*d^2 - 4*Q*t) / sqrt(16*alpha*Q*t*pi*d^2)\n\n")
    f.write("  t < t0 (rise):  C_rise = c_bg + A*d/sqrt(16*alpha*Q*t) * exp(-z^2)\n")
    f.write("  t >= t0 (fall): C_fall = c_bg + a/2 * erfc(-z)\n\n")
    f.write("  Smooth blending: C = w*C_rise + (1-w)*C_fall\n")
    f.write("    w = 0.5*(1 + tanh((t0 - t)/sigma))\n\n")

    f.write("--- Fitted Parameters ---\n")
    labels = ['c_bg', 'A', 'a', 'alpha', 'Q', 't0', 'sigma']
    for i, lbl in enumerate(labels):
        f.write(f"  {lbl:<8s} = {best.x[i]:.10f}  +/- {std[i]:.10f}\n")

    t_bt = XPD2 / (4.0 * Q)
    f.write(f"\n  Derived: t_breakthrough = x*pi*d^2/(4*Q) = {t_bt:.6f}\n")

    f.write(f"\n--- Goodness of Fit ---\n")
    f.write(f"  R-squared  (R^2)  = {r2:.6f}\n")
    f.write(f"  RMSE               = {rmse:.6f}\n")
    f.write(f"  SSR  (residuals)   = {ss_res:.6f}\n")
    f.write(f"  SST  (total)       = {ss_tot:.6f}\n")
    f.write(f"  N (fitted points)  = {N}\n")
    f.write(f"  N_params           = 7\n")

    f.write(f"\n--- Data vs Fitted ---\n")
    f.write(f"  {'t':>6s}  {'Meas C':>10s}  {'Fitted C':>10s}  {'Residual':>10s}\n")
    f.write(f"  {'-'*44}\n")
    for i in range(N):
        f.write(f"  {t_fit[i]:6.1f}  {c_fit[i]:10.5f}  {c_pred[i]:10.5f}  {residuals[i]:10.5f}\n")

print(f"Report saved: {report_path}")

# ========== EXPORT 2: CSV data ==========
csv_path = os.path.join(OUT_DIR, 'fit_data.csv')
with open(csv_path, 'w', encoding='utf-8-sig') as f:
    f.write("t,Measured_C,Fitted_C,Residual\n")
    f.write("0,0.00000,0.00000,0.00000\n")
    for i in range(N):
        f.write(f"{t_fit[i]:.1f},{c_fit[i]:.5f},{c_pred[i]:.5f},{residuals[i]:.5f}\n")
print(f"CSV data saved: {csv_path}")

# ========== EXPORT 3: Parameters CSV ==========
param_path = os.path.join(OUT_DIR, 'fit_parameters.csv')
with open(param_path, 'w', encoding='utf-8-sig') as f:
    f.write("Parameter,Value,StdError\n")
    f.write(f"c_bg,{c_bg:.10f},{std[0]:.10f}\n")
    f.write(f"A,{A:.10f},{std[1]:.10f}\n")
    f.write(f"a,{a_param:.10f},{std[2]:.10f}\n")
    f.write(f"alpha,{alpha:.10f},{std[3]:.10f}\n")
    f.write(f"Q,{Q:.10f},{std[4]:.10f}\n")
    f.write(f"t0,{t0:.10f},{std[5]:.10f}\n")
    f.write(f"sigma,{sigma:.10f},{std[6]:.10f}\n")
    f.write(f"R_squared,{r2:.10f},\n")
    f.write(f"RMSE,{rmse:.10f},\n")
    f.write(f"t_breakthrough,{t_bt:.10f},\n")
print(f"Parameters CSV saved: {param_path}")

# ========== EXPORT 4: High-quality plot ==========
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
t_smooth = np.linspace(0.01, 110, 3000)
c_s = model_smooth(t_smooth, *best.x)

# Components
denom = np.sqrt(np.abs(16.0 * alpha * Q * t_smooth * PI * d_val * d_val)) + 1e-300
z_arr = (XPD2 - 4.0 * Q * t_smooth) / denom
c_rise_comp = c_bg + (A * d_val) / denom * np.exp(-z_arr * z_arr)
c_fall_comp = c_bg + (a_param / 2.0) * erfc(-z_arr)
weight = 0.5 * (1.0 + np.tanh((t0 - t_smooth) / sigma))

# Panel 1: Main fit
ax1 = axes[0, 0]
ax1.fill_between(t_smooth, 0, c_rise_comp, alpha=0.10, color='blue')
ax1.fill_between(t_smooth, 0, c_fall_comp, alpha=0.10, color='green')
ax1.plot(t_smooth, c_rise_comp, 'b--', lw=1, alpha=0.5, label='Rise component')
ax1.plot(t_smooth, c_fall_comp, 'g--', lw=1, alpha=0.5, label='Fall component')
ax1.plot(t_smooth, c_s, 'r-', lw=2.5, label='Fitted (blended)')
ax1.plot(t_data, c_data, 'ko', ms=8, mfc='k', label='Measured data')
ax1.axvline(x=t0, color='orange', ls=':', lw=2, alpha=0.7, label=f't0 = {t0:.2f}')
ax1.axhline(y=c_bg, color='gray', ls='--', lw=1, alpha=0.5, label=f'c_bg = {c_bg:.4f}')
ax1.set_xlabel('t', fontsize=13)
ax1.set_ylabel('C', fontsize=13)
ax1.set_title('Solute Transport Model - Smooth Fit', fontsize=14)
ax1.legend(fontsize=8, loc='upper right')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-2, 112)

info = (f"c_bg = {c_bg:.4f}   A = {A:.2f}\n"
        f"a = {a_param:.4f}   alpha = {alpha:.3f}\n"
        f"Q = {Q:.2f}   t0 = {t0:.3f}\n"
        f"sigma = {sigma:.3f}\n"
        f"R^2 = {r2:.6f}\n"
        f"RMSE = {rmse:.6f}")
ax1.text(0.02, 0.97, info, transform=ax1.transAxes, fontsize=8,
         verticalalignment='top', family='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

# Panel 2: Transition zoom
ax2 = axes[0, 1]
tz = np.linspace(max(0.1, t0 - 3*sigma), t0 + 3*sigma, 500)
cz = model_smooth(tz, *best.x)
wz = 0.5*(1.0+np.tanh((t0-tz)/sigma))
ax2.plot(tz, cz, 'r-', lw=3)
mask_z = (t_data >= tz[0]) & (t_data <= tz[-1])
ax2.plot(t_data[mask_z], c_data[mask_z], 'ko', ms=8, mfc='k')
ax2.axvline(x=t0, color='orange', ls=':', lw=2)
ax2_twin = ax2.twinx()
ax2_twin.plot(tz, wz, 'm-', lw=1.5, alpha=0.6, label='Blend weight')
ax2_twin.set_ylabel('Blend weight', color='magenta', fontsize=11)
ax2.set_xlabel('t', fontsize=13)
ax2.set_ylabel('C', fontsize=13)
ax2.set_title(f'Transition Region (t0 +/- 3*sigma)', fontsize=13)
ax2.grid(True, alpha=0.3)

# Panel 3: Residuals
ax3 = axes[1, 0]
ax3.plot(t_fit, residuals * 100, 'o-', color='steelblue', ms=8, mfc='steelblue', lw=1.5)
ax3.axhline(y=0, color='gray', ls='-', lw=1)
ax3.fill_between([-2, 112], -2*rmse*100, 2*rmse*100, alpha=0.12, color='red',
                  label=f'+/- 2*RMSE = +/- {2*rmse:.4f}')
ax3.set_xlabel('t', fontsize=13)
ax3.set_ylabel('Residual x100', fontsize=13)
ax3.set_title('Residuals', fontsize=14)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(-2, 112)

# Panel 4: Semilog tail
ax4 = axes[1, 1]
ax4.semilogy(t_smooth, np.maximum(c_s, 1e-10), 'r-', lw=2.5, label='Fitted')
ax4.semilogy(t_data, c_data, 'ko', ms=8, mfc='k', label='Measured')
ax4.axhline(y=c_bg, color='gray', ls='--', lw=1, alpha=0.5, label=f'c_bg = {c_bg:.4f}')
ax4.set_xlabel('t', fontsize=13)
ax4.set_ylabel('C (log scale)', fontsize=13)
ax4.set_title('Semilog: Tail Decay', fontsize=14)
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plot_path = os.path.join(OUT_DIR, 'fit_result.png')
plt.savefig(plot_path, dpi=200, bbox_inches='tight')
plot_hd = os.path.join(OUT_DIR, 'fit_result_hd.png')
plt.savefig(plot_hd, dpi=400, bbox_inches='tight')
print(f"Plot saved: {plot_path}")
print(f"HD plot saved: {plot_hd}")
plt.show()

print("\n=== Export complete ===")
print(f"  {report_path}")
print(f"  {csv_path}")
print(f"  {param_path}")
print(f"  {plot_path}")
