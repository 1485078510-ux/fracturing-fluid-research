# -*- coding: utf-8 -*-
"""
Export ALL figure data as Origin-ready CSV files.
Each CSV has clear column headers for direct import.
"""
import numpy as np
from scipy.special import erfc
from scipy.integrate import trapezoid

# ── Parameters ────────────────────────────────────────
cb=0.18003; A=0.1000; a_val=50.0; alpha=1200.0; Q_mL=0.4689; t0=16.338; sigma0=7.011
x_mm,d_mm=1000.0,1.0; XPD2=x_mm*np.pi*d_mm*d_mm; Q_mm3=Q_mL*1000
Pe=x_mm/alpha; v_mm=4*Q_mm3/(np.pi*d_mm*d_mm); MRT=x_mm/v_mm

# ── Data ──────────────────────────────────────────────
t_dat=np.array([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105])
c_dat=np.array([0,0.58438,0.83879,1.0,0.92443,0.64736,0.35516,0.29471,0.27204,
    0.24433,0.20907,0.21914,0.19144,0.19899,0.17128,0.20403,
    0.17884,0.16373,0.16877,0.15617,0.15617,0.15113])
mask=t_dat>0; tf=t_dat[mask]; cf=c_dat[mask]
ts=np.linspace(0.01,110,2000)

def model(t,sigma):
    den=np.sqrt(np.abs(16*alpha*Q_mm3*t*np.pi*d_mm*d_mm))+1e-300
    z=(XPD2-4*Q_mm3*t)/den
    cr=cb+(A*d_mm)/den*np.exp(-z*z)
    cf_=cb+(a_val/2)*erfc(-z)
    w=0.5*(1+np.tanh((t0-t)/sigma))
    return cr,cf_,w,w*cr+(1-w)*cf_

cr,cf_,w,blend=model(ts,sigma0)
pred=blend[np.searchsorted(ts,tf)]
r2=1-np.sum((cf-pred)**2)/np.sum((cf-np.mean(cf))**2)
Ti=trapezoid(blend,ts)
gp=100*trapezoid(w*cr,ts)/Ti
ep=100*trapezoid((1-w)*cf_,ts)/Ti

BASE=r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\ESP-T_投稿文件'

# ══════════════════════════════════════════════════════
# Figure 1 — BTC Fitting data
# ══════════════════════════════════════════════════════
# (a) Model curves — high-res smooth
np.savetxt(f'{BASE}\\Fig1_BTC_curves.csv',
    np.column_stack([ts, cr, cf_, blend, w]),
    delimiter=',', fmt='%.6f',
    header='Time_min,Gaussian_component,erfc_component,Blended_model,Blend_weight',
    comments='')

# (a) Data points
np.savetxt(f'{BASE}\\Fig1_BTC_data.csv',
    np.column_stack([t_dat, c_dat]),
    delimiter=',', fmt='%.6f',
    header='Time_min,C_measured',
    comments='')

# (b) Residuals
np.savetxt(f'{BASE}\\Fig1_BTC_residuals.csv',
    np.column_stack([tf, cf, pred, (cf-pred)*100]),
    delimiter=',', fmt='%.6f',
    header='Time_min,C_measured,C_fitted,Residual_x100',
    comments='')

# (c) Q validation
with open(f'{BASE}\\Fig1_Q_validation.csv','w') as f:
    f.write('Parameter,Value_mL_per_min\n')
    f.write(f'Pump_set,0.50\n')
    f.write(f'Fitted_Q,{Q_mL:.4f}\n')
    f.write(f'Deviation_percent,{abs(Q_mL-0.50)/0.50*100:.1f}\n')
    f.write(f'MRT_fitted_min,{MRT:.2f}\n')
    f.write(f'MRT_pump_geometry_min,{x_mm/(4*500/(np.pi*d_mm*d_mm)):.2f}\n')
    f.write(f'Pe,{Pe:.3f}\n')
    f.write(f'R2,{r2:.4f}\n')
    f.write(f'Gaussian_pct,{gp:.0f}\n')
    f.write(f'erfc_pct,{ep:.0f}\n')

print('Fig1 OK')

# ══════════════════════════════════════════════════════
# Figure 2 — K-P Release Kinetics
# ══════════════════════════════════════════════════════
time_h=np.array([12,24,36,48,60,72,84,96,108,120,132,144,156,168])
rel={30:[0.013,0.035,0.047,0.065,0.077,0.089,0.099,0.102,0.108,0.112,0.116,0.120,0.123,0.125],
     60:[0.018,0.046,0.085,0.106,0.124,0.141,0.157,0.173,0.190,0.199,0.206,0.212,0.216,0.219],
     90:[0.026,0.071,0.109,0.139,0.157,0.171,0.172,0.182,0.188,0.221,0.228,0.233,0.237,0.241],
     120:[0.037,0.115,0.182,0.231,0.263,0.292,0.314,0.321,0.341,0.358,0.371,0.384,0.392,0.400]}
K_vals=[0.05538,0.08177,0.11344,0.19642]
n_vals=[0.59827,0.66646,0.5684,0.55569]
r2_kp=[0.95489,0.9649,0.95599,0.94537]

# (a) Release curves
cols=[time_h]
hdr=['Time_h']
for T in [30,60,90,120]:
    cols.append(np.array(rel[T])*100)
    hdr.append(f'T{T}_C_pct')
np.savetxt(f'{BASE}\\Fig2_release_curves.csv', np.column_stack(cols),
    delimiter=',', fmt='%.4f', header=','.join(hdr), comments='')

# (b) K-P fits
tk=np.logspace(np.log10(10),np.log10(170),50)
kp_cols=[tk]
kp_hdr=['Time_h']
for i,T in enumerate([30,60,90,120]):
    kp_cols.append(K_vals[i]*tk**n_vals[i]*100)
    kp_hdr.append(f'T{T}_KPfit_pct')
np.savetxt(f'{BASE}\\Fig2_KP_fits.csv', np.column_stack(kp_cols),
    delimiter=',', fmt='%.6f', header=','.join(kp_hdr), comments='')

# K-P parameters summary
with open(f'{BASE}\\Fig2_KP_params.csv','w') as f:
    f.write('Temp_C,K,n,R2\n')
    for i,T in enumerate([30,60,90,120]):
        f.write(f'{T},{K_vals[i]:.5f},{n_vals[i]:.5f},{r2_kp[i]:.5f}\n')

print('Fig2 OK')

# ══════════════════════════════════════════════════════
# Figure 3 — Model Comparison
# ══════════════════════════════════════════════════════
with open(f'{BASE}\\Fig3_model_comparison.csv','w') as f:
    f.write('Model,k,R2,RMSE,AICc,Delta_AICc\n')
    f.write(f'Dual_tanh,7,{r2:.4f},0.0237,-140,0\n')
    f.write( 'Gaussian,4,0.9482,0.0609,-124,15.4\n')
    f.write( 'erfc,4,0.7159,0.1427,-89,51.2\n')
    f.write( 'Exponential,3,0.7517,0.1334,-95,45.3\n')
    f.write( 'K-P,3,-0.0193,0.2703,-65,75.0\n')

print('Fig3 OK')

# ══════════════════════════════════════════════════════
# Figure 4 — Sigma Sensitivity
# ══════════════════════════════════════════════════════
mults=np.arange(0.5,3.01,0.25)
sigs=sigma0*mults
cols2=[sigs*sigma0/sigma0]  # just sigs
hdr2=['sigma_min']
tail_vals=[]
for sv in sigs:
    _,cfs,ws,bls=model(ts,sv)
    tail_vals.append(100*trapezoid((1-ws)*cfs,ts)/trapezoid(bls,ts))

np.savetxt(f'{BASE}\\Fig4_sigma_sensitivity.csv',
    np.column_stack([sigs, tail_vals]),
    delimiter=',', fmt='%.4f',
    header='sigma_min,erfc_tail_pct',
    comments='')

print('Fig4 OK')

# ══════════════════════════════════════════════════════
# Figure 5 — Two-Phase Flow
# ══════════════════════════════════════════════════════
od={'4:1':{'Qt':[0.1,0.2,0.3,0.4],'Qo':[0.08,0.16,0.24,0.32],'Co':[33.51,17.37,11.54,8.33],'FO':[2.681,2.779,2.770,2.666]},
    '1:1':{'Qt':[0.1,0.2,0.3,0.4],'Qo':[0.05,0.10,0.15,0.20],'Co':[31.32,16.67,10.73,8.04],'FO':[1.566,1.667,1.610,1.608]},
    '1:4':{'Qt':[0.1,0.2,0.3,0.4],'Qo':[0.02,0.04,0.06,0.08],'Co':[32.74,17.14,10.93,7.97],'FO':[0.655,0.686,0.656,0.638]}}
FOref=3.187

with open(f'{BASE}\\Fig5_twophase.csv','w') as f:
    f.write('OWR,Q_total_mL_min,Q_oil_mL_min,C_oil_ug_mL,F_O_ug_min,F_O_norm\n')
    for k,d in od.items():
        for i in range(4):
            f.write(f'{k},{d["Qt"][i]},{d["Qo"][i]},{d["Co"][i]},{d["FO"][i]},{d["FO"][i]/FOref:.4f}\n')

# Single-phase reference
with open(f'{BASE}\\Fig5_flux_reference.csv','w') as f:
    f.write('Parameter,Value,Unit\n')
    f.write(f'F_O_ref,{FOref:.3f},ug/min\n')
    f.write(f'F_O_ref_std,0.15,ug/min\n')
    f.write(f'Correlation_r,0.97,dimensionless\n')
    f.write(f'RMSD,8.3,percent\n')

print('Fig5 OK')

# ══════════════════════════════════════════════════════
# Summary file for Origin import
# ══════════════════════════════════════════════════════
with open(f'{BASE}\\_all_parameters.txt','w') as f:
    f.write(f'# Model Parameters for Origin\n')
    f.write(f'cb = {cb:.5f}\n')
    f.write(f'A  = {A:.4f}\n')
    f.write(f'a  = {a_val:.4f}\n')
    f.write(f'alpha = {alpha:.1f} mm\n')
    f.write(f'Q = {Q_mL:.4f} mL/min\n')
    f.write(f't0 = {t0:.3f} min\n')
    f.write(f'sigma = {sigma0:.3f} min\n')
    f.write(f'x = {x_mm:.0f} mm\n')
    f.write(f'd = {d_mm:.0f} mm\n')
    f.write(f'Pe = {Pe:.3f}\n')
    f.write(f'R2 = {r2:.4f}\n')
    f.write(f'MRT_fit = {MRT:.2f} min\n')
    f.write(f'MRT_pump = {x_mm/(4*500/(np.pi*d_mm*d_mm)):.2f} min\n')
    f.write(f'Gaussian_pct = {gp:.0f}\n')
    f.write(f'erfc_pct = {ep:.0f}\n')

print('\n=== ALL DATA EXPORTED ===')
print(f'12 CSV files saved to {BASE}')
