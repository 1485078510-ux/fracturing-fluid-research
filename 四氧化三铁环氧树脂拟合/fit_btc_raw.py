# -*- coding: utf-8 -*-
"""
Fresh fit using RAW concentration data from BTC.dat.
Use physically transparent parameters: velocity v (cm/min) and dispersion D (cm^2/min).
Q is computed from v: Q = v * pi * d^2 / 4.

Raw data columns from BTC.dat:
  Col 4: time (min)
  Col 2: raw concentration (mg/L or ug/mL)
  Col 5: normalized C/C0

We fit BOTH raw and normalized to cross-check.
"""
import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.special import erfc
from scipy.integrate import trapezoid
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PI = np.pi

# ========== Raw data from BTC.dat ==========
# Col 1 (index): cumulative something
# Col 2: raw concentration
# Col 3: another measurement
# Col 4: time (min)
# Col 5: C/C0
raw_data = np.array([
    [0,   0,     0,      0,   0     ],
    [10,  0.232, 1.042,  5,   0.5844],
    [20,  0.333, 1.538,  10,  0.8388],
    [30,  0.397, 1.853,  15,  1.0   ],
    [40,  0.367, 1.705,  20,  0.9244],
    [50,  0.257, 1.165,  25,  0.6474],
    [60,  0.141, 0.595,  30,  0.3552],
    [70,  0.117, 0.477,  35,  0.2947],
    [80,  0.108, 0.433,  40,  0.2720],
    [90,  0.097, 0.379,  45,  0.2443],
    [100, 0.083, 0.310,  50,  0.2091],
    [110, 0.087, 0.330,  55,  0.2191],
    [120, 0.076, 0.276,  60,  0.1914],
    [130, 0.079, 0.291,  65,  0.1990],
    [140, 0.068, 0.237,  70,  0.1713],
    [150, 0.081, 0.301,  75,  0.2040],
    [160, 0.071, 0.251,  80,  0.1788],
    [170, 0.065, 0.222,  85,  0.1637],
    [180, 0.067, 0.232,  90,  0.1688],
    [190, 0.062, 0.207,  95,  0.1562],
    [200, 0.062, 0.207,  100, 0.1562],
    [210, 0.060, 0.197,  105, 0.1511],
])

t_raw = raw_data[:, 3]     # time in min
c_raw = raw_data[:, 1]     # raw concentration
c_norm = raw_data[:, 4]    # normalized C/C0

mask = t_raw > 0
t_fit = t_raw[mask]
c_raw_fit = c_raw[mask]
c_norm_fit = c_norm[mask]

C0_measured = c_raw_fit[2]  # 0.397 at t=15 min (peak)

print(f"Raw concentration data: C_max = {C0_measured:.4f} at t=15 min")
print(f"21 data points for fitting (excluding t=0)")
print()

# ========== Geometry ==========
x_cm = 10.0    # 100 mm = 10 cm (tube length)
d_cm = 0.5     # 5 mm = 0.5 cm (tube diameter)
A_cross = PI * d_cm * d_cm / 4.0  # cross-sectional area in cm^2
V_tube = A_cross * x_cm  # tube volume in cm^3 = mL

print(f"Tube: L={x_cm} cm, d={d_cm} cm, A={A_cross:.4f} cm^2, V={V_tube:.4f} mL")
print(f"Pump: Q=0.50 mL/min, ideal v=Q/A={0.50/A_cross:.3f} cm/min, ideal MRT={V_tube/0.50:.2f} min")
print()

# ========== Model: Gaussian pulse + erfc tail (physically parametrized) ==========
def btc_model(t, params):
    """
    params: [v, D, M_pulse, M_tail, c_bg, t0, sigma]
    v  = velocity (cm/min)
    D  = dispersion coefficient (cm^2/min)
    M_pulse = pulse mass coefficient (arbitrary)
    M_tail  = tail amplitude coefficient
    c_bg = baseline
    t0  = crossover time (min)
    sigma = transition width (min)

    Gaussian: C_gauss = c_bg + M_pulse / sqrt(4*pi*D*t) * exp(-(x-vt)^2/(4Dt))
    erfc tail: C_tail = c_bg + M_tail/2 * erfc(-(x-vt)/sqrt(4Dt))
    """
    v, D, M_pulse, M_tail, c_bg, t0, sigma = params

    denom = np.sqrt(np.abs(4.0 * D * t)) + 1e-300
    eta = (x_cm - v * t) / denom  # (x - vt) / sqrt(4Dt)

    c_gauss = c_bg + M_pulse / (np.sqrt(PI) * denom) * np.exp(-eta * eta)
    c_tail = c_bg + (M_tail / 2.0) * erfc(-eta)

    weight = 0.5 * (1.0 + np.tanh((t0 - t) / sigma))
    return weight * c_gauss + (1.0 - weight) * c_tail

def fit_cost(params, t, c_obs):
    """Sum of squared errors."""
    pred = btc_model(t, params)
    return np.sum((pred - c_obs)**2)

# Bounds for physically transparent parameters
# v: 0.01 to 10 cm/min (ideal from pump: 2.55 cm/min)
# D: 0.01 to 100 cm^2/min
# M_pulse, M_tail: wide
bounds_raw = [
    (0.005, 20.0),    # v (cm/min)
    (0.01, 200.0),    # D (cm^2/min)
    (0.01, 100.0),    # M_pulse
    (0.005, 20.0),    # M_tail
    (0.0, 0.2),       # c_bg
    (5.0, 45.0),      # t0
    (0.5, 15.0),      # sigma
]

print("=== Fit 1: Raw concentration data ===")
best_raw = None
for seed in [42, 123, 456, 789]:
    r = differential_evolution(
        lambda p: fit_cost(p, t_fit, c_raw_fit),
        bounds_raw, seed=seed, maxiter=2000, tol=1e-12,
        popsize=50, mutation=(0.5, 1.5), recombination=0.9, polish=True
    )
    v, D, Mp, Mt, cb, t0, sigma = r.x
    Q_fit = v * A_cross  # mL/min
    print(f"  Seed {seed:>4d}: cost={r.fun:.6f} | v={v:.4f} cm/min, D={D:.4f} cm^2/min")
    print(f"           Q={Q_fit:.4f} mL/min, t0={t0:.2f}, sigma={sigma:.2f}")
    if best_raw is None or r.fun < best_raw.fun:
        best_raw = r

res = minimize(lambda p: fit_cost(p, t_fit, c_raw_fit), best_raw.x,
               method='L-BFGS-B', bounds=bounds_raw,
               options={'maxiter': 20000, 'ftol': 1e-16, 'gtol': 1e-16})
if res.fun < best_raw.fun:
    best_raw = res

v_r, D_r, Mp_r, Mt_r, cb_r, t0_r, sigma_r = best_raw.x
Q_r = v_r * A_cross
pred_r = btc_model(t_fit, best_raw.x)
ss_res = np.sum((c_raw_fit - pred_r)**2)
ss_tot = np.sum((c_raw_fit - np.mean(c_raw_fit))**2)
r2_r = 1 - ss_res / ss_tot
Pe_r = x_cm * v_r / D_r

print(f"\n  BEST FIT (raw concentration):")
print(f"  v     = {v_r:.4f} cm/min")
print(f"  D     = {D_r:.4f} cm^2/min")
print(f"  Pe    = x*v/D = {Pe_r:.4f}")
print(f"  Q     = v * A = {Q_r:.4f} mL/min")
print(f"  MRT   = x/v = {x_cm/v_r:.2f} min")
print(f"  c_bg  = {cb_r:.4f}")
print(f"  t0    = {t0_r:.2f} min")
print(f"  sigma = {sigma_r:.2f} min")
print(f"  R²    = {r2_r:.6f}")
print(f"  |Q_fit - 0.50|/0.50 = {abs(Q_r-0.50)/0.50*100:.1f}%")
print()

# ========== Also fit normalized data for comparison ==========
print("=== Fit 2: Normalized C/C0 data ===")
bounds_norm = [
    (0.005, 20.0),    # v
    (0.01, 200.0),    # D
    (0.01, 100.0),    # M_pulse
    (0.005, 50.0),    # M_tail
    (0.0, 0.2),       # c_bg
    (5.0, 45.0),      # t0
    (0.5, 15.0),      # sigma
]

best_norm = None
for seed in [42, 123, 456, 789]:
    r = differential_evolution(
        lambda p: fit_cost(p, t_fit, c_norm_fit),
        bounds_norm, seed=seed, maxiter=2000, tol=1e-12,
        popsize=50, mutation=(0.5, 1.5), recombination=0.9, polish=True
    )
    v, D, Mp, Mt, cb, t0, sigma = r.x
    Q_fit = v * A_cross
    if best_norm is None or r.fun < best_norm.fun:
        best_norm = r

res = minimize(lambda p: fit_cost(p, t_fit, c_norm_fit), best_norm.x,
               method='L-BFGS-B', bounds=bounds_norm,
               options={'maxiter': 20000, 'ftol': 1e-16, 'gtol': 1e-16})
if res.fun < best_norm.fun:
    best_norm = res

v_n, D_n, Mp_n, Mt_n, cb_n, t0_n, sigma_n = best_norm.x
Q_n = v_n * A_cross
pred_n = btc_model(t_fit, best_norm.x)
ss_res_n = np.sum((c_norm_fit - pred_n)**2)
ss_tot_n = np.sum((c_norm_fit - np.mean(c_norm_fit))**2)
r2_n = 1 - ss_res_n / ss_tot_n
Pe_n = x_cm * v_n / D_n

print(f"  BEST FIT (normalized):")
print(f"  v     = {v_n:.4f} cm/min")
print(f"  D     = {D_n:.4f} cm^2/min")
print(f"  Pe    = {Pe_n:.4f}")
print(f"  Q     = {Q_n:.4f} mL/min")
print(f"  MRT   = {x_cm/v_n:.2f} min")
print(f"  R²    = {r2_n:.6f}")
print(f"  |Q_fit - 0.50|/0.50 = {abs(Q_n-0.50)/0.50*100:.1f}%")
print()

# Summary comparison
print("="*65)
print("COMPARISON: Raw vs Normalized fitting")
print("="*65)
print(f"  {'':20s} {'Raw conc':>15s} {'Normalized':>15s}")
print(f"  {'v (cm/min)':20s} {v_r:15.4f} {v_n:15.4f}")
print(f"  {'D (cm^2/min)':20s} {D_r:15.4f} {D_n:15.4f}")
print(f"  {'Pe':20s} {Pe_r:15.4f} {Pe_n:15.4f}")
print(f"  {'Q (mL/min)':20s} {Q_r:15.4f} {Q_n:15.4f}")
print(f"  {'MRT (min)':20s} {x_cm/v_r:15.2f} {x_cm/v_n:15.2f}")
print(f"  {'R²':20s} {r2_r:15.6f} {r2_n:15.6f}")
print(f"  {'Pump Q=0.50 mL/min':20s} {'':>15s}")
print(f"  {'Q deviation':20s} {abs(Q_r-0.50)/0.50*100:14.1f}% {abs(Q_n-0.50)/0.50*100:14.1f}%")
print(f"  {'MRT ideal ~3.9 min':20s}")
print(f"  {'MRT deviation from 3.9':20s} {abs(x_cm/v_r-3.9)/3.9*100:14.1f}% {abs(x_cm/v_n-3.9)/3.9*100:14.1f}%")
