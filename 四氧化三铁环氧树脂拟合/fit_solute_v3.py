# -*- coding: utf-8 -*-
"""
Re-fit with Q in mL/min but keeping mm-based geometry internally.
Add explicit 1000x conversion factor: 1 mL = 1000 mm^3.

z = (XPD2_mm3 - 4000*Q_mL*t) / sqrt(16000*alpha_mm*Q_mL*t*pi*d_mm^2)

Q bounds: [0.01, 5.0] mL/min (pump = 0.50 mL/min)
"""
import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.special import erfc
from scipy.integrate import trapezoid
import matplotlib.pyplot as plt
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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

# ========== Constants (mm-based, with mL conversion) ==========
x_mm = 100.0; d_mm = 5.0; PI = np.pi
XPD2_MM3 = x_mm * PI * d_mm * d_mm  # 7853.98 mm^3
ML_TO_MM3 = 1000.0  # 1 mL = 1000 mm^3

def model_smooth(t, c_bg, A, a_param, alpha_mm, Q_mL, t0, sigma):
    """
    Q_mL in mL/min, alpha_mm in mm, x/d in mm.
    Internal conversion: Q_mm3 = Q_mL * 1000
    z = (XPD2_mm3 - 4*Q_mm3*t) / sqrt(16*alpha_mm*Q_mm3*t*pi*d_mm^2)
    """
    Q_mm3 = Q_mL * ML_TO_MM3  # mL/min -> mm^3/min
    denom = np.sqrt(np.abs(16.0 * alpha_mm * Q_mm3 * t * PI * d_mm * d_mm)) + 1e-300
    z = (XPD2_MM3 - 4.0 * Q_mm3 * t) / denom

    c_rise = c_bg + (A * d_mm) / denom * np.exp(-z * z)
    c_fall = c_bg + (a_param / 2.0) * erfc(-z)

    weight = 0.5 * (1.0 + np.tanh((t0 - t) / sigma))
    return weight * c_rise + (1.0 - weight) * c_fall

def mse_smooth(p):
    c_bg, A, a_param, alpha_mm, Q_mL, t0, sigma = p
    if c_bg < 0 or c_bg > 0.5 or A <= 0 or A > 1e6:
        return 1e10
    if a_param <= 0 or a_param > 100 or alpha_mm <= 0 or alpha_mm > 1e5:
        return 1e10
    if Q_mL < 0.001 or Q_mL > 10.0 or t0 < 1 or t0 > 55:
        return 1e10
    if sigma < 0.1 or sigma > 20:
        return 1e10
    pred = model_smooth(t_fit, c_bg, A, a_param, alpha_mm, Q_mL, t0, sigma)
    return np.mean((pred - c_fit)**2)

# Bounds: Q in mL/min within [0.005, 5.0] — pump is 0.50
bounds = [
    (0.0, 0.4),       # c_bg
    (0.1, 1e6),       # A
    (0.1, 50.0),      # a
    (0.01, 1e5),      # alpha (mm)
    (0.005, 5.0),    # Q (mL/min) — wide around pump 0.50
    (5.0, 45.0),      # t0 (min)
    (0.5, 15.0),      # sigma (min)
]

print(f"XPD2 = {XPD2_MM3:.2f} mm^3  (={XPD2_MM3/ML_TO_MM3:.4f} mL)")
print(f"Q bounds: [{bounds[4][0]:.3f}, {bounds[4][1]:.1f}] mL/min")
print(f"Pump setting: 0.50 mL/min = {0.50*ML_TO_MM3:.0f} mm^3/min")
print()

print("=== Re-fitted with Q in mL/min (mm-geometry + 1000x conversion) ===")
best_s = None
all_results = []
for seed in [42, 123, 456, 789]:
    r = differential_evolution(
        mse_smooth, bounds, seed=seed, maxiter=2000, tol=1e-12,
        popsize=50, mutation=(0.5, 1.5), recombination=0.9, polish=True
    )
    print(f"  Seed {seed:>4d}: cost={r.fun:.8f} | Q={r.x[4]:.5f} mL/min, "
          f"alpha={r.x[3]:.2f} mm, t0={r.x[5]:.2f}, sigma={r.x[6]:.2f}")
    all_results.append((seed, r))
    if best_s is None or r.fun < best_s.fun:
        best_s = r

# Fine tune
res_s = minimize(mse_smooth, best_s.x, method='L-BFGS-B', bounds=bounds,
                 options={'maxiter': 20000, 'ftol': 1e-16, 'gtol': 1e-16})
if res_s.fun < best_s.fun:
    best_s = res_s

c_bg_s, A_s, a_s, alpha_s, Q_s, t0_s, sigma_s = best_s.x
c_pred_s = model_smooth(t_fit, *best_s.x)
res_s_arr = c_fit - c_pred_s
ss_res_s = np.sum(res_s_arr**2)
ss_tot = np.sum((c_fit - np.mean(c_fit))**2)
r2_s = 1 - ss_res_s / ss_tot
rmse_s = np.sqrt(best_s.fun)

print(f"\n{'='*65}")
print("FINAL RESULTS (Q in mL/min)")
print(f"{'='*65}")
print(f"  R² = {r2_s:.6f}, RMSE = {rmse_s:.6f}")
print(f"  c_bg  = {c_bg_s:.8f}")
print(f"  A     = {A_s:.6f}")
print(f"  a     = {a_s:.8f}")
print(f"  alpha = {alpha_s:.6f} mm")
print(f"  Q     = {Q_s:.6f} mL/min")
print(f"  t0    = {t0_s:.6f} min")
print(f"  sigma = {sigma_s:.6f} min")
print()

# Derived quantities
Q_mm3 = Q_s * ML_TO_MM3
Pe = x_mm / alpha_s
v_mm = 4.0 * Q_mm3 / (PI * d_mm * d_mm)
MRT = x_mm / v_mm
PV_time = XPD2_MM3 / (4.0 * Q_mm3)

print(f"  Q in mm^3/min: {Q_mm3:.3f}")
print(f"  Pe = x/alpha = {Pe:.4f}")
print(f"  v  = {v_mm:.4f} mm/min = {v_mm/10:.4f} cm/min")
print(f"  MRT = {MRT:.4f} min")
print(f"  Convective travel (z=0): {PV_time:.2f} min")
print(f"  Pump Q = 0.50 mL/min, Fitted Q = {Q_s:.5f} mL/min")
print(f"  |Q_fit - Q_pump| / Q_pump = {abs(Q_s - 0.50)/0.50*100:.2f}%")
print()

# Integrated fractions
t_smooth = np.linspace(0.01, 110, 3000)
Q_mm3_s = Q_s * ML_TO_MM3
denom_s = np.sqrt(np.abs(16.0 * alpha_s * Q_mm3_s * t_smooth * PI * d_mm * d_mm)) + 1e-300
z = (XPD2_MM3 - 4.0 * Q_mm3_s * t_smooth) / denom_s
c_rise_comp = c_bg_s + (A_s * d_mm) / denom_s * np.exp(-z * z)
c_fall_comp = c_bg_s + (a_s / 2.0) * erfc(-z)
weight = 0.5 * (1.0 + np.tanh((t0_s - t_smooth) / sigma_s))
blend = weight * c_rise_comp + (1.0 - weight) * c_fall_comp

total_integ = trapezoid(blend, t_smooth)
gauss_pct = 100 * trapezoid(weight * c_rise_comp, t_smooth) / total_integ
erfc_pct = 100 * trapezoid((1 - weight) * c_fall_comp, t_smooth) / total_integ

print(f"  Gaussian fraction: {gauss_pct:.1f}%")
print(f"  erfc tail fraction: {erfc_pct:.1f}%")
print()

# Data table
print(f"  {'t':>6s}  {'C_meas':>10s}  {'C_fit':>10s}  {'Res':>10s}")
print(f"  {'-'*44}")
for i in range(N):
    resid_pct = (c_fit[i] - c_pred_s[i]) * 100
    print(f"  {t_fit[i]:6.1f}  {c_fit[i]:10.5f}  {c_pred_s[i]:10.5f}  {resid_pct:+9.5f}%")
