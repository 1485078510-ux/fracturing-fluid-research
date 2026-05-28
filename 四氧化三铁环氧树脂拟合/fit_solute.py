# -*- coding: utf-8 -*-
"""
Piecewise solute transport model with SMOOTH transition.

t < t0:  C = c_bg + A*d/sqrt(16*alpha*Q*t) * exp(-z^2)
t >= t0: C = c_bg + a/2 * erfc(-z)

Smooth blending via tanh:
  weight(t) = 0.5 * (1 + tanh((t0 - t) / sigma))
  C(t) = weight * C_rise + (1 - weight) * C_fall

where z = (x*pi*d^2 - 4*Q*t) / sqrt(16*alpha*Q*t*pi*d^2)
"""
import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.special import erfc
import matplotlib.pyplot as plt
import sys, io
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
t_fit = t_data[mask]
c_fit = c_data[mask]
N = len(t_fit)

# ========== Constants ==========
x_val = 100.0; d_val = 5.0; PI = np.pi
XPD2 = x_val * PI * d_val * d_val

def model_smooth(t, c_bg, A, a_param, alpha, Q, t0, sigma):
    """
    Smooth blended piecewise model.
    sigma controls transition width (smaller = sharper).
    """
    denom = np.sqrt(np.abs(16.0 * alpha * Q * t * PI * d_val * d_val)) + 1e-300
    z = (XPD2 - 4.0 * Q * t) / denom

    c_rise = c_bg + (A * d_val) / denom * np.exp(-z * z)
    c_fall = c_bg + (a_param / 2.0) * erfc(-z)

    # Tanh blending: 1 at t << t0, 0 at t >> t0
    weight = 0.5 * (1.0 + np.tanh((t0 - t) / sigma))
    return weight * c_rise + (1.0 - weight) * c_fall

# Also keep piecewise version for comparison
def model_piecewise(t, c_bg, A, a_param, alpha, Q, t0):
    denom = np.sqrt(np.abs(16.0 * alpha * Q * t * PI * d_val * d_val)) + 1e-300
    z = (XPD2 - 4.0 * Q * t) / denom
    c_rise = c_bg + (A * d_val) / denom * np.exp(-z * z)
    c_fall = c_bg + (a_param / 2.0) * erfc(-z)
    return np.where(t < t0, c_rise, c_fall)

def mse_smooth(p):
    c_bg, A, a_param, alpha, Q, t0, sigma = p
    if c_bg < 0 or c_bg > 0.5 or A <= 0 or A > 1e6:
        return 1e10
    if a_param <= 0 or a_param > 100 or alpha <= 0 or alpha > 1e6:
        return 1e10
    if Q < 1 or Q > 1e4 or t0 < 1 or t0 > 55:
        return 1e10
    if sigma < 0.1 or sigma > 20:
        return 1e10
    pred = model_smooth(t_fit, c_bg, A, a_param, alpha, Q, t0, sigma)
    return np.mean((pred - c_fit)**2)

# Bounds: c_bg, A, a, alpha, Q, t0, sigma
bounds_smooth = [
    (0.0, 0.4),       # c_bg
    (0.1, 1e6),       # A
    (0.1, 50.0),      # a
    (0.01, 1e5),      # alpha
    (10.0, 5000.0),   # Q
    (5.0, 40.0),      # t0
    (0.5, 15.0),      # sigma (transition width)
]

print("=== Smooth transition model (tanh blending) ===")
best_s = None
for seed in [42, 123, 456, 789]:
    r = differential_evolution(
        mse_smooth, bounds_smooth, seed=seed, maxiter=2000, tol=1e-12,
        popsize=50, mutation=(0.5, 1.5), recombination=0.9, polish=True
    )
    print(f"  Seed {seed:>4d}: cost={r.fun:.8f} | sigma={r.x[6]:.2f}, "
          f"t0={r.x[5]:.2f}, Q={r.x[4]:.1f}, alpha={r.x[3]:.2f}")
    if best_s is None or r.fun < best_s.fun:
        best_s = r

# Fine tune smooth model
res_s = minimize(mse_smooth, best_s.x, method='L-BFGS-B', bounds=bounds_smooth,
                 options={'maxiter': 20000, 'ftol': 1e-16, 'gtol': 1e-16})
if res_s.fun < best_s.fun:
    best_s = res_s

c_bg_s, A_s, a_s, alpha_s, Q_s, t0_s, sigma_s = best_s.x
cost_s = best_s.fun
c_pred_s = model_smooth(t_fit, c_bg_s, A_s, a_s, alpha_s, Q_s, t0_s, sigma_s)
res_s_arr = c_fit - c_pred_s
ss_res_s = np.sum(res_s_arr**2)
ss_tot = np.sum((c_fit - np.mean(c_fit))**2)
r2_s = 1 - ss_res_s / ss_tot
rmse_s = np.sqrt(cost_s)

# Also fit piecewise for comparison
def mse_pw(p):
    c_bg, A, a_param, alpha, Q, t0 = p
    if any(v <= 0 for v in [A, a_param, alpha, Q]): return 1e10
    if c_bg < 0 or c_bg > 0.5 or t0 < 1 or t0 > 55: return 1e10
    if Q > 5000: return 1e10
    pred = model_piecewise(t_fit, c_bg, A, a_param, alpha, Q, t0)
    return np.mean((pred - c_fit)**2)

bounds_pw = [
    (0.0, 0.4), (0.1, 1e6), (0.1, 50.0), (0.01, 1e5), (10.0, 5000.0), (1.0, 50.0)
]

print()
print("=== Piecewise model (hard switch) ===")
best_p = None
for seed in [42, 123, 456]:
    r = differential_evolution(
        mse_pw, bounds_pw, seed=seed, maxiter=2000, tol=1e-12,
        popsize=50, mutation=(0.5, 1.5), recombination=0.9, polish=True
    )
    bt = XPD2 / (4.0 * r.x[4])
    print(f"  Seed {seed:>4d}: cost={r.fun:.8f} | t0={r.x[5]:.2f}, Q={r.x[4]:.1f} (t_bt={bt:.2f})")
    if best_p is None or r.fun < best_p.fun:
        best_p = r

res_p = minimize(mse_pw, best_p.x, method='L-BFGS-B', bounds=bounds_pw,
                 options={'maxiter': 20000, 'ftol': 1e-16, 'gtol': 1e-16})
if res_p.fun < best_p.fun:
    best_p = res_p

c_bg_p, A_p, a_p, alpha_p, Q_p, t0_p = best_p.x
c_pred_p = model_piecewise(t_fit, c_bg_p, A_p, a_p, alpha_p, Q_p, t0_p)
res_p_arr = c_fit - c_pred_p
ss_res_p = np.sum(res_p_arr**2)
r2_p = 1 - ss_res_p / ss_tot
rmse_p = np.sqrt(best_p.fun)
t_bt_p = XPD2 / (4.0 * Q_p)

# ========== Results Summary ==========
print()
print("=" * 65)
print("FINAL RESULTS")
print("=" * 65)
print()
print("  MODEL           R^2       RMSE")
print("  " + "-" * 45)
print(f"  Smooth tanh     {r2_s:.6f}  {rmse_s:.6f}")
print(f"  Piecewise       {r2_p:.6f}  {rmse_p:.6f}")
print()

print("  Smooth model parameters:")
print(f"    c_bg  = {c_bg_s:.8f}")
print(f"    A     = {A_s:.6f}")
print(f"    a     = {a_s:.8f}")
print(f"    alpha = {alpha_s:.8f}")
print(f"    Q     = {Q_s:.6f}")
print(f"    t0    = {t0_s:.6f}")
print(f"    sigma = {sigma_s:.6f}")
print()
print("  Piecewise model parameters:")
print(f"    c_bg  = {c_bg_p:.8f}")
print(f"    A     = {A_p:.6f}")
print(f"    a     = {a_p:.8f}")
print(f"    alpha = {alpha_p:.8f}")
print(f"    Q     = {Q_p:.6f}")
print(f"    t0    = {t0_p:.6f}")
print(f"    t_bt  = {t_bt_p:.6f}  (breakthrough = x*pi*d^2/(4*Q))")
print()

# Data comparison for smooth model
print(f"  {'t':>6s}  {'Meas C':>10s}  {'Fit C':>10s}  {'Res':>10s}")
print(f"  {'-'*44}")
for i in range(N):
    print(f"  {t_fit[i]:6.1f}  {c_fit[i]:10.5f}  {c_pred_s[i]:10.5f}  {res_s_arr[i]:10.5f}")
print()

# ========== Plot ==========
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
t_smooth = np.linspace(0.01, 110, 3000)

c_ss = model_smooth(t_smooth, c_bg_s, A_s, a_s, alpha_s, Q_s, t0_s, sigma_s)
c_sp = model_piecewise(t_smooth, c_bg_p, A_p, a_p, alpha_p, Q_p, t0_p)

# Compute individual components for smooth model
denom = np.sqrt(np.abs(16.0 * alpha_s * Q_s * t_smooth * PI * d_val * d_val)) + 1e-300
z = (XPD2 - 4.0 * Q_s * t_smooth) / denom
c_rise_comp = c_bg_s + (A_s * d_val) / denom * np.exp(-z * z)
c_fall_comp = c_bg_s + (a_s / 2.0) * erfc(-z)
weight = 0.5 * (1.0 + np.tanh((t0_s - t_smooth) / sigma_s))

# Main: both models
ax1 = axes[0, 0]
ax1.plot(t_smooth, c_ss, 'r-', lw=3, label=f'Smooth tanh (R^2={r2_s:.4f})')
ax1.plot(t_smooth, c_sp, 'b--', lw=2, alpha=0.6, label=f'Piecewise (R^2={r2_p:.4f})')
ax1.plot(t_data, c_data, 'ko', ms=8, mfc='k', label='Measured data')
ax1.axvline(x=t0_s, color='red', ls=':', lw=1.5, alpha=0.6, label=f't0_smooth={t0_s:.2f}')
ax1.axvline(x=t0_p, color='blue', ls=':', lw=1.5, alpha=0.6, label=f't0_piecewise={t0_p:.2f}')
ax1.axhline(y=c_bg_s, color='gray', ls='--', lw=1, alpha=0.5)
ax1.set_xlabel('t', fontsize=13)
ax1.set_ylabel('C', fontsize=13)
ax1.set_title('Model Comparison: Smooth vs Piecewise', fontsize=14)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-2, 112)

# Smooth model detail
ax2 = axes[0, 1]
ax2.fill_between(t_smooth, 0, c_rise_comp, alpha=0.12, color='blue', label='Rise component')
ax2.fill_between(t_smooth, 0, c_fall_comp, alpha=0.12, color='green', label='Fall component')
ax2.plot(t_smooth, c_rise_comp, 'b--', lw=1, alpha=0.6)
ax2.plot(t_smooth, c_fall_comp, 'g--', lw=1, alpha=0.6)
ax2.plot(t_smooth, c_ss, 'r-', lw=2.5, label='Blended result')
ax2.plot(t_smooth, weight, 'm-', lw=1, alpha=0.5, label='Blend weight')
ax2.plot(t_data, c_data, 'ko', ms=8, mfc='k', label='Measured')
ax2.axvline(x=t0_s, color='orange', ls=':', lw=2, alpha=0.7, label=f't0={t0_s:.2f}')
ax2.axhline(y=c_bg_s, color='gray', ls='--', lw=1, alpha=0.5)
ax2.set_xlabel('t', fontsize=13)
ax2.set_ylabel('C', fontsize=13)
ax2.set_title('Smooth Model: Components & Blending', fontsize=14)
ax2.legend(fontsize=8, loc='upper right')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-2, 112)

info = (f"c_bg = {c_bg_s:.4f}\nA = {A_s:.2f}\na = {a_s:.4f}\n"
        f"alpha = {alpha_s:.3f}\nQ = {Q_s:.2f}\nt0 = {t0_s:.3f}\n"
        f"sigma = {sigma_s:.3f}\nR^2 = {r2_s:.6f}\nRMSE = {rmse_s:.6f}")
ax2.text(0.98, 0.97, info, transform=ax2.transAxes, fontsize=8,
         verticalalignment='top', horizontalalignment='right',
         family='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

# Zoom: transition region
ax3 = axes[1, 0]
t_zoom = np.linspace(max(0.1, t0_s - 3*sigma_s), t0_s + 3*sigma_s, 500)
c_zoom_s = model_smooth(t_zoom, c_bg_s, A_s, a_s, alpha_s, Q_s, t0_s, sigma_s)
c_zoom_p = model_piecewise(t_zoom, c_bg_p, A_p, a_p, alpha_p, Q_p, t0_p)
ax3.plot(t_zoom, c_zoom_s, 'r-', lw=3, label=f'Smooth (sigma={sigma_s:.2f})')
ax3.plot(t_zoom, c_zoom_p, 'b--', lw=2, label='Piecewise')
mask_z = (t_data >= t_zoom[0]) & (t_data <= t_zoom[-1])
ax3.plot(t_data[mask_z], c_data[mask_z], 'ko', ms=8, mfc='k')
ax3.axvline(x=t0_s, color='red', ls=':', lw=1.5)
ax3.axvline(x=t0_p, color='blue', ls=':', lw=1.5)
ax3.set_xlabel('t', fontsize=13)
ax3.set_ylabel('C', fontsize=13)
ax3.set_title(f'Zoom: Transition region (t0 +/- 3*sigma = {t0_s:.1f} +/- {3*sigma_s:.1f})', fontsize=13)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)

# Residuals
ax4 = axes[1, 1]
ax4.plot(t_fit, res_s_arr * 100, 'o-', color='steelblue', ms=7, mfc='steelblue', lw=1.2,
         label=f'Smooth (R^2={r2_s:.4f})')
ax4.plot(t_fit, res_p_arr * 100, 's-', color='coral', ms=6, mfc='coral', lw=1,
         alpha=0.7, label=f'Piecewise (R^2={r2_p:.4f})')
ax4.axhline(y=0, color='gray', ls='-', lw=1)
ax4.set_xlabel('t', fontsize=13)
ax4.set_ylabel('Residual x100', fontsize=13)
ax4.set_title('Residuals Comparison (x100)', fontsize=14)
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.3)
ax4.set_xlim(-2, 112)

plt.tight_layout()
out = r'c:\Users\郝\Desktop\claude\fit_result.png'
plt.savefig(out, dpi=150, bbox_inches='tight')
print(f"Plot saved: {out}")
plt.show()
