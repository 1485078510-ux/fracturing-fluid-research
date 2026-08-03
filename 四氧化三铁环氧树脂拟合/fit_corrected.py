# -*- coding: utf-8 -*-
"""
Re-fit with CORRECTED geometry: x = 1 m = 1000 mm, d = 1 mm.
Pump: 0.50 mL/min = 500 mm^3/min.
"""
import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.special import erfc
from scipy.integrate import trapezoid
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PI = np.pi

# ========== CORRECTED GEOMETRY ==========
x_mm = 1000.0   # 1 m
d_mm = 1.0      # 1 mm
A_cross = PI * d_mm * d_mm / 4.0  # mm^2
V_tube = A_cross * x_mm  # mm^3
XPD2 = x_mm * PI * d_mm * d_mm  # mm^3
ML_TO_MM3 = 1000.0

print(f"=== Corrected Geometry ===")
print(f"x = {x_mm} mm = {x_mm/1000} m")
print(f"d = {d_mm} mm")
print(f"A = {A_cross:.4f} mm^2")
print(f"V_tube = {V_tube:.2f} mm^3 = {V_tube/ML_TO_MM3:.4f} mL")
print(f"XPD2 = {XPD2:.2f} mm^3 = {XPD2/ML_TO_MM3:.4f} mL")
print(f"Pump Q = 0.50 mL/min = 500 mm^3/min")
print(f"Ideal v = Q/A = {500/A_cross:.1f} mm/min = {500/A_cross/10:.1f} cm/min")
print(f"Ideal MRT = x/v = {x_mm/(500/A_cross):.2f} min")
print()

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

def model(t, c_bg, A, a_param, alpha, Q_mL, t0, sigma):
    """Q_mL in mL/min. Internal: Q_mm3 = Q_mL * 1000."""
    Q_mm3 = Q_mL * ML_TO_MM3
    denom = np.sqrt(np.abs(16.0 * alpha * Q_mm3 * t * PI * d_mm * d_mm)) + 1e-300
    z = (XPD2 - 4.0 * Q_mm3 * t) / denom
    c_rise = c_bg + (A * d_mm) / denom * np.exp(-z * z)
    c_fall = c_bg + (a_param / 2.0) * erfc(-z)
    weight = 0.5 * (1.0 + np.tanh((t0 - t) / sigma))
    return weight * c_rise + (1.0 - weight) * c_fall

def mse(p):
    c_bg, A, a_param, alpha, Q_mL, t0, sigma = p
    if c_bg < 0 or c_bg > 0.5 or A <= 0 or A > 1e6: return 1e10
    if a_param <= 0 or a_param > 100 or alpha <= 0 or alpha > 1e6: return 1e10
    if Q_mL < 0.001 or Q_mL > 10.0 or t0 < 1 or t0 > 55: return 1e10
    if sigma < 0.1 or sigma > 20: return 1e10
    pred = model(t_fit, c_bg, A, a_param, alpha, Q_mL, t0, sigma)
    return np.mean((pred - c_fit)**2)

# Bounds — Q in mL/min around pump 0.50
bounds = [
    (0.0, 0.4),       # c_bg
    (0.1, 1e6),       # A
    (0.1, 50.0),      # a
    (0.1, 1e5),       # alpha (mm)
    (0.01, 5.0),      # Q (mL/min)
    (1.0, 50.0),      # t0
    (0.5, 15.0),      # sigma
]

print("=== Fitting with corrected geometry ===")
best = None
for seed in [42, 123, 456, 789]:
    r = differential_evolution(
        mse, bounds, seed=seed, maxiter=2000, tol=1e-12,
        popsize=50, mutation=(0.5, 1.5), recombination=0.9, polish=True
    )
    Q_mL = r.x[4]; alpha = r.x[3]
    v_mm = 4.0 * Q_mL * ML_TO_MM3 / (PI * d_mm * d_mm)
    mrt_fit = x_mm / v_mm
    print(f"  Seed {seed:>4d}: cost={r.fun:.8f} | Q={Q_mL:.5f} mL/min, "
          f"alpha={alpha:.3f} mm, MRT={mrt_fit:.2f} min, t0={r.x[5]:.2f}, sigma={r.x[6]:.2f}")
    if best is None or r.fun < best.fun:
        best = r

res = minimize(mse, best.x, method='L-BFGS-B', bounds=bounds,
               options={'maxiter': 20000, 'ftol': 1e-16, 'gtol': 1e-16})
if res.fun < best.fun:
    best = res

c_bg_s, A_s, a_s, alpha_s, Q_s, t0_s, sigma_s = best.x
c_pred = model(t_fit, *best.x)
res_arr = c_fit - c_pred
ss_res = np.sum(res_arr**2)
ss_tot = np.sum((c_fit - np.mean(c_fit))**2)
r2 = 1 - ss_res / ss_tot
rmse = np.sqrt(best.fun)

Q_mm3 = Q_s * ML_TO_MM3
v_mm = 4.0 * Q_mm3 / (PI * d_mm * d_mm)
MRT_fit = x_mm / v_mm
Pe = x_mm / alpha_s
PV_time = XPD2 / (4.0 * Q_mm3)

print(f"\n{'='*65}")
print("FINAL RESULTS (corrected geometry)")
print(f"{'='*65}")
print(f"  R² = {r2:.6f}, RMSE = {rmse:.6f}")
print(f"  c_bg  = {c_bg_s:.8f}")
print(f"  A     = {A_s:.6f}")
print(f"  a     = {a_s:.8f}")
print(f"  alpha = {alpha_s:.3f} mm")
print(f"  Q     = {Q_s:.5f} mL/min")
print(f"  t0    = {t0_s:.3f} min")
print(f"  sigma = {sigma_s:.3f} min")
print()
print(f"  Derived:")
print(f"    Q in mm^3/min: {Q_mm3:.3f}")
print(f"    Pe = x/alpha = {Pe:.4f}")
print(f"    v = 4Q/(pi*d^2) = {v_mm:.3f} mm/min")
print(f"    MRT (fitted) = {MRT_fit:.3f} min")
print(f"    MRT (conv, z=0) = {PV_time:.3f} min")
print(f"    MRT (ideal, from pump) = {x_mm/(4*500/(PI*d_mm*d_mm)):.3f} min")
print()
print(f"  === SELF-CALIBRATION CHECK ===")
print(f"  Pump Q = 0.50 mL/min")
print(f"  Fitted Q = {Q_s:.5f} mL/min")
print(f"  |Q_fit - Q_pump|/Q_pump = {abs(Q_s-0.50)/0.50*100:.2f}%")
print(f"  MRT(fitted) = {MRT_fit:.3f} min")
print(f"  MRT(pump geometry) = {x_mm/(4*500/(PI*d_mm*d_mm)):.3f} min")
print(f"  |MRT_fit - MRT_pump|/MRT_pump = {abs(MRT_fit - x_mm/(4*500/(PI*d_mm*d_mm)))/(x_mm/(4*500/(PI*d_mm*d_mm)))*100:.2f}%")

# Integrated fractions
t_smooth = np.linspace(0.01, 110, 3000)
Q_mm3_s = Q_s * ML_TO_MM3
denom_s = np.sqrt(np.abs(16.0 * alpha_s * Q_mm3_s * t_smooth * PI * d_mm * d_mm)) + 1e-300
z = (XPD2 - 4.0 * Q_mm3_s * t_smooth) / denom_s
c_rise_comp = c_bg_s + (A_s * d_mm) / denom_s * np.exp(-z * z)
c_fall_comp = c_bg_s + (a_s / 2.0) * erfc(-z)
weight = 0.5 * (1.0 + np.tanh((t0_s - t_smooth) / sigma_s))
blend = weight * c_rise_comp + (1.0 - weight) * c_fall_comp

total_integ = trapezoid(blend, t_smooth)
gauss_pct = 100 * trapezoid(weight * c_rise_comp, t_smooth) / total_integ
erfc_pct = 100 * trapezoid((1 - weight) * c_fall_comp, t_smooth) / total_integ
print(f"\n  Gaussian fraction: {gauss_pct:.1f}%")
print(f"  erfc tail fraction: {erfc_pct:.1f}%")

# Residuals
print(f"\n  {'t':>6s}  {'C_meas':>10s}  {'C_fit':>10s}  {'Res':>10s}")
print(f"  {'-'*44}")
for i in range(N):
    print(f"  {t_fit[i]:6.1f}  {c_fit[i]:10.5f}  {c_pred[i]:10.5f}  {res_arr[i]:+10.5f}")
