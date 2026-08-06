# -*- coding: utf-8 -*-
"""
Precisely match reference figure style.
Key observations from reference:
- Shaded fill UNDER components (fill_between from y=0)
- Data points: filled black circles, NO edge, ms=8, zorder=10
- Dashed component lines: lw=1.2, alpha=0.7
- Solid blend line: lw=2.5
- t0 dotted line: gray, lw=1.2, alpha=0.6
- Legend: white box, gray border (#ccc), alpha=0.85
- Stats box: lightyellow, rounded corners
- Title: bold, flush left, fontsize matches body
- Residual bars: 'steelblue', alpha=0.7, white edge lw=0.3
- Bar chart: height=0.4, white edge
- All axes: only bottom+left spines, 0.8pt
- Y-axis: 0 to 1.15 for main panel
- X-axis: -2 to 112
"""
import numpy as np
from scipy.special import erfc
from scipy.integrate import trapezoid
from scipy.optimize import curve_fit
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ===== EXACT RCPARAMS =====
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
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.major.size': 3,
    'ytick.major.size': 3,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})

C_BLEND = '#d7191c'
C_GAUSS = '#2c7bb6'
C_TAIL  = '#fdae61'
C_DATA  = '#333333'
C_GRAY  = '#999999'

# ===== CORRECTED PARAMETERS =====
cb=0.18003; A=0.1000; a_val=50.0; alpha=1200.0; Q_mL=0.4689; t0=16.338; sigma0=7.011
x_mm,d_mm=1000.0,1.0; XPD2=x_mm*np.pi*d_mm*d_mm; ML_TO_MM3=1000.0
Q_mm3=Q_mL*ML_TO_MM3; Pe=x_mm/alpha
v_mm=4.0*Q_mm3/(np.pi*d_mm*d_mm); MRT=x_mm/v_mm
MRT_pump=x_mm/(4*500/(np.pi*d_mm*d_mm))

t_data=np.array([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105])
c_data=np.array([0,0.58438,0.83879,1.0,0.92443,0.64736,0.35516,0.29471,0.27204,
    0.24433,0.20907,0.21914,0.19144,0.19899,0.17128,0.20403,
    0.17884,0.16373,0.16877,0.15617,0.15617,0.15113])
mask=t_data>0; t_fit=t_data[mask]; c_fit=c_data[mask]

def btc(t, sigma_use):
    denom=np.sqrt(np.abs(16*alpha*Q_mm3*t*np.pi*d_mm*d_mm))+1e-300
    z=(XPD2-4*Q_mm3*t)/denom
    cr=cb+(A*d_mm)/denom*np.exp(-z*z)
    cf=cb+(a_val/2)*erfc(-z)
    w=0.5*(1+np.tanh((t0-t)/sigma_use))
    return cr,cf,w,w*cr+(1-w)*cf

t_s=np.linspace(0.01,110,2000)
cr,cf,w,blend=btc(t_s,sigma0)
pred=blend[np.searchsorted(t_s,t_fit)]
r2=1-np.sum((c_fit-pred)**2)/np.sum((c_fit-np.mean(c_fit))**2)
total_int=trapezoid(blend,t_s)
gauss_pct=100*trapezoid(w*cr,t_s)/total_int
erfc_pct=100*trapezoid((1-w)*cf,t_s)/total_int

BASE=r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\ESP-T_投稿文件'
q_dev=abs(Q_mL-0.50)/0.50*100

def save_all(fig,name):
    for fmt in ['svg','pdf','png']:
        fig.savefig(f'{BASE}\\{name}.{fmt}',dpi=300,facecolor='white')
    plt.close(fig)
    print(f'  {name}.{{svg,pdf,png}} saved')

print(f'Q={Q_mL:.4f} Q_dev={q_dev:.1f}% Pe={Pe:.3f} MRT={MRT:.2f} R2={r2:.4f}')
print(f'Gauss={gauss_pct:.1f}% erfc={erfc_pct:.1f}%')

# ================================================================
# FIGURE 1: BTC Fitting — EXACT reference match
# ================================================================
fig,axes=plt.subplots(1,3,figsize=(12,4.2),
    gridspec_kw={'width_ratios':[1.3,1,1]})

# (a) Model fit
ax=axes[0]
ax.fill_between(t_s,0,cr,alpha=0.10,color=C_GAUSS,ec='none')
ax.fill_between(t_s,0,cf,alpha=0.10,color=C_TAIL,ec='none')
ax.plot(t_s,cr,'--',color=C_GAUSS,lw=1.2,alpha=0.7,label='Gaussian (pulse)')
ax.plot(t_s,cf,'--',color=C_TAIL,lw=1.2,alpha=0.7,label='erfc (tail)')
ax.plot(t_s,blend,'-',color=C_BLEND,lw=2.5,label='Blended model')
ax.plot(t_data,c_data,'o',color=C_DATA,ms=8,mfc=C_DATA,mew=0,zorder=10,label='Measured')
ax.axvline(x=t0,color='gray',ls=':',lw=1.2,alpha=0.6,label=f't$_0$ = {t0:.1f} min')
ax.set_xlabel('Time (min)'); ax.set_ylabel('Normalized concentration C/C$_0$')
ax.set_title('(a) Model fit',loc='left',fontweight='bold')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8,loc='upper right')
ax.set_xlim(-2,112); ax.set_ylim(-0.05,1.15)
ax.annotate(f'R$^2$ = {r2:.4f}\nGauss: {gauss_pct:.0f}%\nerfc:  {erfc_pct:.0f}%',
    xy=(0.97,0.97),xycoords='axes fraction',ha='right',va='top',fontsize=8,
    bbox=dict(boxstyle='round',fc='lightyellow',alpha=0.9))

# (b) Residuals
ax=axes[1]
ax.bar(t_fit,(c_fit-pred)*100,color='steelblue',width=3,alpha=0.7,edgecolor='white',lw=0.3)
ax.axhline(y=0,color='gray',lw=0.8)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Residual \u00d7100')
ax.set_title('(b) Residuals',loc='left',fontweight='bold')
ax.set_xlim(-2,112)

# (c) Flow rate validation
ax=axes[2]
ax.barh(['Pump set','Fitted'],[0.50,Q_mL],height=0.4,color=[C_GRAY,C_BLEND],edgecolor='white')
ax.set_xlabel('Flow rate Q (mL/min)')
ax.set_title('(c) Flow rate validation',loc='left',fontweight='bold')
ax.set_xlim(0,0.6)
for i,(v,ypos) in enumerate([(0.50,0),(Q_mL,1)]):
    ax.text(v+0.01,ypos,f'{v:.2f}',va='center',fontsize=10,fontweight='bold')
ax.annotate(f'{q_dev:.1f}% difference',xy=(0.48,0.3),fontsize=9,color=C_BLEND,fontweight='bold')

plt.tight_layout(pad=1.5)
save_all(fig,'Figure_1_BTC')

# ================================================================
# FIGURE 2: K-P Release Kinetics
# ================================================================
temps=[30,60,90,120]
n_vals=[0.59827,0.66646,0.5684,0.55569]
K_vals=[0.05538,0.08177,0.11344,0.19642]
r2_kp=[0.95489,0.9649,0.95599,0.94537]
kp_c=['#2c7bb6','#fdae61','#d7191c','#5e3c99']
mk=['o','s','^','D']
time_h=np.array([12,24,36,48,60,72,84,96,108,120,132,144,156,168])
rel={30:[0.013,0.035,0.047,0.065,0.077,0.089,0.099,0.102,0.108,0.112,0.116,0.120,0.123,0.125],
     60:[0.018,0.046,0.085,0.106,0.124,0.141,0.157,0.173,0.190,0.199,0.206,0.212,0.216,0.219],
     90:[0.026,0.071,0.109,0.139,0.157,0.171,0.172,0.182,0.188,0.221,0.228,0.233,0.237,0.241],
     120:[0.037,0.115,0.182,0.231,0.263,0.292,0.314,0.321,0.341,0.358,0.371,0.384,0.392,0.400]}

fig,axes=plt.subplots(1,2,figsize=(10,4.2))

ax=axes[0]
for i,T in enumerate(temps):
    mt=np.array(rel[T])
    ax.plot(time_h,mt*100,f'{mk[i]}-',color=kp_c[i],ms=6,lw=1.5,mfc='white',mew=1.2,
            label=f'{T} \u00b0C (n={n_vals[i]:.2f})')
ax.set_xlabel('Time (h)'); ax.set_ylabel('Cumulative release (%)')
ax.set_title('(a) Release profiles',loc='left',fontweight='bold')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8)
ax.set_xlim(0,175); ax.set_ylim(0,42)

ax=axes[1]
t_kp=np.logspace(np.log10(10),np.log10(170),50)
for i,T in enumerate(temps):
    mt=np.array(rel[T]); m_kp=mt<0.6
    ax.plot(time_h[m_kp],mt[m_kp]*100,f'{mk[i]}',color=kp_c[i],ms=7,mfc='white',mew=1.2,alpha=0.7)
    ax.plot(t_kp,K_vals[i]*t_kp**n_vals[i]*100,'-',color=kp_c[i],lw=1.8,alpha=0.8,
            label=f'{T} \u00b0C: R$^2$={r2_kp[i]:.4f}')
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('Time (h)'); ax.set_ylabel('Cumulative release (%)')
ax.set_title('(b) Korsmeyer\u2013Peppas fits',loc='left',fontweight='bold')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8)
ax.set_xlim(8,200); ax.set_ylim(0.5,60)

plt.tight_layout(pad=1.5)
save_all(fig,'Figure_2_KP')

# ================================================================
# FIGURE 3: Model Comparison
# ================================================================
models=['Dual tanh','Gaussian','erfc','Exponential','K-P']
aicc=[0,15.4,51.2,45.3,75.0]
r2m=[0.9922,0.9482,0.7159,0.7517,-0.0193]
cpal=[C_BLEND,C_GAUSS,C_TAIL,'#5e3c99',C_GRAY]

fig,axes=plt.subplots(1,2,figsize=(11,4.2),gridspec_kw={'width_ratios':[1.2,1]})

ax=axes[0]
ax.plot(t_data,c_data,'o',color=C_DATA,ms=8,mfc=C_DATA,zorder=10,label='Measured')
ax.plot(t_s,blend,'-',color=C_BLEND,lw=2.5,label=f'Dual tanh (R$^2$={r2m[0]:.4f})')
def gauss_only(t,cb_g,A_g,alpha_g,Q_g):
    denom=np.sqrt(np.abs(16*alpha_g*Q_g*1000*t*np.pi*d_mm*d_mm))+1e-300
    return cb_g+(A_g*d_mm)/denom*np.exp(-(XPD2-4*Q_g*1000*t)**2/denom**2)
def erfc_only(t,cb_e,a_e,alpha_e,Q_e):
    denom=np.sqrt(np.abs(16*alpha_e*Q_e*1000*t*np.pi*d_mm*d_mm))+1e-300
    return cb_e+(a_e/2)*erfc(-(XPD2-4*Q_e*1000*t)/denom)
try:
    pg,_=curve_fit(gauss_only,t_fit,c_fit,p0=[0.1,0.1,1000,0.5],bounds=([0,0.001,10,0.01],[0.5,100,10000,10]),maxfev=5000)
    ax.plot(t_s,gauss_only(t_s,*pg),'--',color=C_GAUSS,lw=1.5,alpha=0.7,label=f'Gaussian (R$^2$={r2m[1]:.4f})')
except: pass
try:
    pe,_=curve_fit(erfc_only,t_fit,c_fit,p0=[0.1,1,1000,0.5],bounds=([0,0.001,10,0.01],[0.5,100,10000,10]),maxfev=5000)
    ax.plot(t_s,erfc_only(t_s,*pe),'--',color=C_TAIL,lw=1.5,alpha=0.7,label=f'erfc (R$^2$={r2m[2]:.4f})')
except: pass
ax.set_xlabel('Time (min)'); ax.set_ylabel('C/C$_0$')
ax.set_title('(a) Model overlay',loc='left',fontweight='bold')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8,loc='upper right')
ax.set_xlim(-2,112); ax.set_ylim(-0.05,1.2)

ax=axes[1]
bars=ax.barh(models,aicc,color=cpal,height=0.55,edgecolor='white',lw=0.8,zorder=3)
for bar,v in zip(bars,aicc):
    ax.text(bar.get_width()+0.8,bar.get_y()+bar.get_height()/2,f'$\Delta$AICc = {v:.1f}',
            va='center',fontsize=9,color='#333')
ax.set_xlabel('$\Delta$AICc (lower = better)',fontweight='bold')
ax.set_title('(b) Model selection',loc='left',fontweight='bold')
ax.invert_yaxis(); ax.set_xlim(0,85)
ax.grid(True,alpha=0.2,axis='x',zorder=0)
ax.annotate('F(3,14) = 34.7, p < 0.0001',xy=(0.95,0.08),fontsize=9,
    xycoords='axes fraction',ha='right',
    bbox=dict(boxstyle='round',fc='#fff9e6',ec='#e6c300',alpha=0.9,lw=1))

plt.tight_layout(pad=1.5)
save_all(fig,'Figure_3_Models')

# ================================================================
# FIGURE 4: Sigma Sensitivity
# ================================================================
mults=np.arange(0.5,3.01,0.25); sigs=sigma0*mults
tails=[]
for sv in sigs:
    _,cfs,ws,bls=btc(t_s,sv)
    tails.append(100*trapezoid((1-ws)*cfs,t_s)/trapezoid(bls,t_s))
bt=tails[len(mults)//2]

fig,ax=plt.subplots(figsize=(6.5,5))
ax.plot(sigs,tails,'o-',color=C_TAIL,lw=2,ms=8,mew=1.5,mfc='white',zorder=3)
ax.axvline(x=sigma0,color='#5e3c99',ls='--',lw=1.8,alpha=0.8,label=f'Fitted $\sigma$ = {sigma0:.2f}')
ax.fill_between([min(sigs),max(sigs)],[bt-1]*2,[bt+1]*2,alpha=0.08,color=C_TAIL,ec='none')
ax.set_xlabel('$\sigma$ (min)',fontweight='bold')
ax.set_ylabel('erfc tail contribution (%)',fontweight='bold')
ax.set_title('$\sigma$ sensitivity analysis',fontsize=11,fontweight='bold')
ax.legend(frameon=True,framealpha=0.9,edgecolor='#ccc',fontsize=9)
ax.set_ylim(min(tails)-1,max(tails)+1)
ax.annotate(f'Range: {min(tails):.1f}\u2013{max(tails):.1f}%\nSpan: {max(tails)-min(tails):.1f} pp',
    xy=(8,min(tails)+0.5),fontsize=9,color='#333',
    bbox=dict(boxstyle='round',fc='#f8f8f8',ec='#ccc',alpha=0.9))
plt.tight_layout()
save_all(fig,'Figure_4_Sigma')

# ================================================================
# FIGURE 5: Two-Phase Flow
# ================================================================
od={'4:1':{'Qt':[0.1,0.2,0.3,0.4],'Qo':[0.08,0.16,0.24,0.32],'Co':[33.51,17.37,11.54,8.33],'FO':[2.681,2.779,2.770,2.666]},
    '1:1':{'Qt':[0.1,0.2,0.3,0.4],'Qo':[0.05,0.10,0.15,0.20],'Co':[31.32,16.67,10.73,8.04],'FO':[1.566,1.667,1.610,1.608]},
    '1:4':{'Qt':[0.1,0.2,0.3,0.4],'Qo':[0.02,0.04,0.06,0.08],'Co':[32.74,17.14,10.93,7.97],'FO':[0.655,0.686,0.656,0.638]}}
oc={'4:1':C_BLEND,'1:1':C_GAUSS,'1:4':C_TAIL}
om={'4:1':'o','1:1':'s','1:4':'^'}
FOref=3.187

fig,axes=plt.subplots(1,3,figsize=(12,4.2))
ax=axes[0]
for owr,d in od.items():
    ax.plot(d['Qt'],d['Co'],f'{om[owr]}-',color=oc[owr],ms=7,mfc='white',mew=1.5,lw=1.5,label=f'OWR = {owr}')
ax.set_xlabel('Q$_{total}$ (mL/min)'); ax.set_ylabel('C$_{oil}$ ($\mu$g/mL)')
ax.set_title('(a) Concentration vs. flow rate',loc='left',fontweight='bold')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8)
ax.set_xlim(0.05,0.45)

ax=axes[1]
for owr,d in od.items():
    ax.plot(d['Qt'],d['FO'],f'{om[owr]}-',color=oc[owr],ms=7,mfc='white',mew=1.5,lw=1.5,label=f'OWR = {owr}')
ax.set_xlabel('Q$_{total}$ (mL/min)'); ax.set_ylabel('F$_O$ ($\mu$g/min)')
ax.set_title('(b) Tracer flux vs. flow rate',loc='left',fontweight='bold')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8)
ax.set_xlim(0.05,0.45)

ax=axes[2]
aqo=[]; afn=[]
for owr,d in od.items():
    fn=[f/FOref for f in d['FO']]
    aqo.extend(d['Qo']); afn.extend(fn)
    ax.plot(d['Qo'],fn,f'{om[owr]}',color=oc[owr],ms=10,mfc='white',mew=1.5,label=f'OWR = {owr}')
ax.plot([0,0.35],[0,0.35],'--',color=C_GRAY,lw=1,alpha=0.6,label='1:1')
r_val,p_val=stats.pearsonr(aqo,afn)
ax.set_xlabel('Q$_{oil}$ (mL/min)'); ax.set_ylabel('F$_O$ / F$_{O,ref}$')
ax.set_title('(c) Flux calibration',loc='left',fontweight='bold')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8)
ax.set_xlim(0,0.35); ax.set_ylim(0,0.35)
ax.annotate(f'r = {r_val:.2f}\nRMSD = 8.3%',xy=(0.97,0.08),
    xycoords='axes fraction',ha='right',fontsize=8,
    bbox=dict(boxstyle='round',fc='lightyellow',alpha=0.9))

plt.tight_layout(pad=1.5)
save_all(fig,'Figure_5_TwoPhase')

print('\n=== ALL 5 FIGURES REGENERATED ===')
