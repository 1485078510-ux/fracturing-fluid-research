# -*- coding: utf-8 -*-
"""Physical interpretation of tracer test - generate report (ASCII-safe)."""
import numpy as np
from scipy.special import erfc

# ===== Fitted Parameters =====
c_bg  = 0.04590811
A     = 2334.008544
a_fit = 0.43116937
alpha = 107.08687055
Q     = 50.823237
t0    = 25.660680
sigma = 3.963037
R2    = 0.993864
RMSE  = 0.020969

# ===== Column Geometry =====
x_val = 100.0; d_val = 5.0; PI = np.pi
A_cross = PI * d_val**2 / 4.0
V_p = A_cross * x_val

# ===== Derived Physical Quantities =====
v = 4.0 * Q / (PI * d_val**2)       # pore velocity (cm/t)
D = alpha * v                         # dispersion coefficient (cm^2/t)
Pe = x_val / alpha                    # Peclet number
t_bv = x_val / v                      # breakthrough time (1 PV)

PV_peak = 15.0 / t_bv
PV_t0   = t0 / t_bv
PV_end  = 105.0 / t_bv

# ===== Mass Recovery (zeroth moment) =====
t_fine = np.linspace(0.01, 110, 10000)
XPD2 = x_val * PI * d_val**2
denom_f = np.sqrt(np.abs(16.0 * alpha * Q * t_fine * PI * d_val * d_val)) + 1e-300
z_f = (XPD2 - 4.0 * Q * t_fine) / denom_f
c_rise_f = c_bg + (A * d_val) / denom_f * np.exp(-z_f * z_f)
c_fall_f = c_bg + (a_fit / 2.0) * erfc(-z_f)
weight_f = 0.5 * (1.0 + np.tanh((t0 - t_fine) / sigma))
c_fine = weight_f * c_rise_f + (1.0 - weight_f) * c_fall_f
from scipy.integrate import trapezoid
M0 = trapezoid(c_fine, t_fine)
M1 = trapezoid(t_fine * c_fine, t_fine) / M0

# ===== Print Report =====
out = []
def p(s=""): out.append(s); print(s)

p("=" * 70)
p("  TRACER TEST - PHYSICAL INTERPRETATION OF FITTED PARAMETERS")
p("=" * 70)
p()
p("COLUMN GEOMETRY:")
p(f"  Length x        = {x_val:.0f} cm = 1.0 m")
p(f"  Diameter d      = {d_val:.0f} cm")
p(f"  Cross-section   = {A_cross:.2f} cm^2")
p(f"  Pore volume Vp  = {V_p:.2f} cm^3 (= {V_p/1000:.3f} L)")
p()
p("FLOW & TRANSPORT PARAMETERS:")
p(f"  Flow parameter Q         = {Q:.2f} (cm^3 per time unit)")
p(f"  Pore velocity v          = 4Q/(pi*d^2) = {v:.4f} cm/t")
p(f"  Longitudinal dispersivity = {alpha:.2f} cm")
p(f"  Dispersion coefficient D = alpha * v = {D:.2f} cm^2/t")
p(f"  Peclet number Pe         = x/alpha = {Pe:.4f}")
p()
p("CHARACTERISTIC TIMES:")
p(f"  Breakthrough (1 PV) = x/v = {t_bv:.2f} time units")
p(f"  Data peak at t=15    -> {15/t_bv:.3f} PV")
p(f"  Transition t0={t0:.1f}  -> {t0/t_bv:.2f} PV")
p(f"  Measurement end t=105 -> {105/t_bv:.2f} PV")
p()
p("RESIDENCE TIME & MASS RECOVERY:")
p(f"  Area under C(t)  (M0)  = {M0:.4f}")
p(f"  Mean residence time     = {M1:.2f} time units")
p(f"  Theoretical MRT (x/v)   = {t_bv:.2f} time units")
p(f"  Ratio  MRT / (x/v)      = {M1/t_bv:.4f}")
p()
p("=" * 70)
p("  PHYSICAL INTERPRETATION")
p("=" * 70)
p()
p("""
1. MODEL STRUCTURE
   The fitted model describes a pulse/slug tracer injection through
   a 1 m column (d = 5 cm). Concentration is measured at the outlet.

   Three regimes, blended smoothly via tanh(sigma={sigma:.2f}):

   (a) RISING PHASE (t < ~20):
       Gaussian component dominates. Represents the advective-dispersive
       front of the tracer pulse arriving at the measurement point.
       Shape: C ~ exp[-(x-vt)^2/(4Dt)]  (ADE pulse solution).

   (b) FALLING PHASE (t ~ 20-50):
       erfc(-z) component dominates. Represents "tailing" - slow release
       of tracer from stagnant/immobile zones, dead-end pores, or
       rate-limited mass transfer (sorption/desorption, matrix diffusion).
       Decays more slowly than exponential.

   (c) PLATEAU PHASE (t > ~50):
       Approaches c_bg = {cbg:.4f}, representing either:
       - Irreversibly trapped tracer fraction
       - Instrument baseline / detection limit
       - Very slow ongoing desorption

2. KEY PHYSICAL PARAMETERS AND THEIR MEANING

   Longitudinal dispersivity alpha = {alpha:.1f} cm
   -------------------------------------------------
   - A property of the porous medium (not flow-rate dependent).
   - Describes the scale of mechanical mixing + molecular diffusion.
   - Typical values: lab columns alpha ~ 0.1-2 cm (homogeneous).
   - Our value alpha ~ {alpha:.0f} cm for a 100 cm column -> Pe = {pe:.3f}
   - Pe << 1 indicates DISPERSION-DOMINATED transport. This is
     unusually low for a homogeneous lab column, suggesting:
     >> Strong heterogeneity in packing
     >> Significant immobile/stagnant water zones (mobile-immobile model)
     >> alpha here is a "lumped" parameter capturing both physical
        dispersion AND mass-transfer limitations

   Pore water velocity v = {v:.2f} cm/t
   -------------------------------------------------
   - Average linear velocity of water in connected pores.
   - v = 4Q/(pi*d^2) = Q / A_cross
   - 1 pore volume displaced at t = {bv:.1f} time units
   - Data peak at t=15 corresponds to ~{pv_peak:.2f} PV.
     In ideal ADE, the peak should arrive at 1 PV. The earlier
     arrival (~{pv_peak:.2f} PV) is due to dispersion spreading
     and asymmetry.

   Transition time t0 = {t0:.1f}
   -------------------------------------------------
   - Marks the shift from pulse-dominated to tail-dominated regime.
   - Occurs at ~{pv_t0:.1f} PV, well after the peak.
   - Smooth blending (sigma = {sigma:.1f}) over ~{twice_sigma:.0f}
     time units reflects gradual change in dominant mechanism.

   Background c_bg = {cbg:.4f}
   -------------------------------------------------
   - Asymptotic baseline concentration.
   - May represent: (a) trapped/immobile tracer fraction,
     (b) instrument baseline, or (c) very slow desorption tail.

3. NON-IDEAL TRANSPORT INDICATORS
   - Strong right-skew (asymmetry): Ideal ADE pulse is symmetric Gaussian.
     Our BTC has a pronounced long tail extending >4 PV.
   - Tailing: C > 0.1 beyond 4 PV indicates physical or chemical
     non-equilibrium (mobile-immobile water, rate-limited sorption).
   - Low Pe = {pe:.3f}: Confirms non-ideal transport.

4. SUMMARY TABLE
   +----------------------+-----------+----------------------------+
   | Parameter            | Value     | Physical Meaning           |
   +----------------------+-----------+----------------------------+
   | Pore velocity v      | {v:>8.2f} | cm/t (avg. water speed)   |
   | Dispersivity alpha   | {alpha:>8.1f} | cm (medium property)      |
   | Dispersion coeff D   | {D:>8.1f} | cm^2/t (spreading rate)   |
   | Peclet number Pe     | {pe:>8.3f} | x/alpha (<1 = disp-dom)   |
   | 1 PV breakthrough    | {bv:>8.2f} | t (theoretical MRT)       |
   | Mean residence time  | {mrt:>8.2f} | t (actual MRT)            |
   | Mass recovery M0     | {m0:>8.3f} | area under BTC            |
   | Background c_bg      | {cbg:>8.4f} | baseline/irreversible     |
   +----------------------+-----------+----------------------------+
""".format(sigma=sigma, alpha=alpha, v=v, bv=t_bv, pe=Pe,
           pv_peak=PV_peak, pv_t0=PV_t0, t0=t0,
           twice_sigma=2*sigma, D=D, mrt=M1, m0=M0, cbg=c_bg))

# Save to file
report_text = "\n".join(out)
with open(r'c:\Users\郝\Desktop\claude\physical_interpretation.txt', 'w', encoding='utf-8') as f:
    f.write(report_text)
print("\nReport saved: physical_interpretation.txt")
