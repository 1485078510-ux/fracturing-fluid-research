# -*- coding: utf-8 -*-
"""Figure 3-8: Breakthrough curve fitting — THE main figure."""
import numpy as np
from scipy.special import erfc
from scipy.integrate import trapezoid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'stix', 'font.size': 10,
    'axes.labelsize': 11, 'axes.titlesize': 12,
    'xtick.labelsize': 9, 'ytick.labelsize': 9, 'legend.fontsize': 9,
    'figure.facecolor': 'white', 'axes.facecolor': 'white',
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.linewidth': 0.8, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})

# Best-fit parameters
cb=0.045908; A=2334.0; a=0.43117; alpha=107.09; Q=50.823; t0=25.661; sigma0=3.963
x_val,d_val=100.0,5.0; XPD2=x_val*np.pi*d_val*d_val

def model(t,sigma):
    denom=np.sqrt(np.abs(16*alpha*Q*t*np.pi*d_val*d_val))+1e-300
    z=(XPD2-4*Q*t)/denom
    cr=cb+(A*d_val)/denom*np.exp(-z*z)
    cf=cb+(a/2)*erfc(-z)
    w=0.5*(1+np.tanh((t0-t)/sigma))
    return cr,cf,w,w*cr+(1-w)*cf

# Data
t_data=np.array([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105])
c_data=np.array([0,0.58438,0.83879,1.0,0.92443,0.64736,0.35516,0.29471,0.27204,
                  0.24433,0.20907,0.21914,0.19144,0.19899,0.17128,0.20403,
                  0.17884,0.16373,0.16877,0.15617,0.15617,0.15113])
mask=t_data>0; t_fit=t_data[mask]; c_fit=c_data[mask]
N=len(t_fit)

t_smooth=np.linspace(0.01,110,2000)
cr,cf,w,blend=model(t_smooth,sigma0)

# Compute R2
pred=blend[np.searchsorted(t_smooth,t_fit)]
ss_res=np.sum((c_fit-pred)**2)
ss_tot=np.sum((c_fit-np.mean(c_fit))**2)
r2=1-ss_res/ss_tot
rmse=np.sqrt(np.mean((c_fit-pred)**2))

# Compute component fractions
total_integ=trapezoid(blend,t_smooth)
tail_integ=trapezoid((1-w)*cf,t_smooth)
gauss_integ=trapezoid(w*cr,t_smooth)
tail_pct=100*tail_integ/total_integ

# ==== FIGURE ====
fig,axes=plt.subplots(1,3,figsize=(12,4.2),gridspec_kw={'width_ratios':[1.3,1,1]})

C_BLEND='#d7191c'; C_GAUSS='#2c7bb6'; C_TAIL='#fdae61'; C_DATA='#333333'

# (a) Main fitting plot
ax=axes[0]
ax.fill_between(t_smooth,0,cr,alpha=0.10,color=C_GAUSS,ec='none')
ax.fill_between(t_smooth,0,cf,alpha=0.10,color=C_TAIL,ec='none')
ax.plot(t_smooth,cr,'--',color=C_GAUSS,lw=1.2,alpha=0.7,label='Gaussian (pulse)')
ax.plot(t_smooth,cf,'--',color=C_TAIL,lw=1.2,alpha=0.7,label='erfc (tail)')
ax.plot(t_smooth,blend,'-',color=C_BLEND,lw=2.5,label='Blended model')
ax.plot(t_data,c_data,'o',color=C_DATA,ms=8,mfc=C_DATA,mew=0,zorder=10,label='Measured')
ax.axvline(x=t0,color='gray',ls=':',lw=1.2,alpha=0.6,label=f't₀ = {t0:.1f} min')
ax.set_xlabel('Time (min)')
ax.set_ylabel('Normalized concentration C/C₀')
ax.set_title('(a) Model fit',loc='left',fontweight='bold')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8,loc='upper right')
ax.set_xlim(-2,112); ax.set_ylim(-0.05,1.15)
ax.annotate(f'R² = {r2:.4f}\nRMSE = {rmse:.4f}\nGauss: {gauss_integ/total_integ*100:.0f}%\nerfc:  {tail_pct:.0f}%',
            xy=(0.97,0.97),xycoords='axes fraction',ha='right',va='top',fontsize=8,
            bbox=dict(boxstyle='round',fc='lightyellow',alpha=0.9))

# (b) Residuals
ax=axes[1]
res=c_fit-pred
ax.bar(t_fit,res*100,color='steelblue',width=3,alpha=0.7,edgecolor='white',lw=0.3)
ax.axhline(y=0,color='gray',lw=0.8)
ax.set_xlabel('Time (min)')
ax.set_ylabel('Residual x100')
ax.set_title('(b) Residuals',loc='left',fontweight='bold')
ax.set_xlim(-2,112)

# (c) Flow rate validation
ax=axes[2]
ax.barh(['Pump set','Fitted'],[0.50,0.46],height=0.4,color=['#999','#d7191c'],edgecolor='white')
ax.set_xlabel('Flow rate Q (mL/min)')
ax.set_title('(c) Flow rate validation',loc='left',fontweight='bold')
ax.set_xlim(0,0.6)
for i,(v,x) in enumerate([(0.50,0),(0.46,1)]):
    ax.text(v+0.01,x,f'{v:.2f}',va='center',fontsize=10,fontweight='bold')
ax.annotate('8% difference',xy=(0.48,0.3),fontsize=9,color=C_BLEND,fontweight='bold')

plt.tight_layout(pad=1.5)
out_svg=r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\Figure_BTC.svg'
out_pdf=r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\Figure_BTC.pdf'
out_png=r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\Figure_BTC.png'
fig.savefig(out_svg,dpi=300,facecolor='white')
fig.savefig(out_pdf,dpi=300,facecolor='white')
fig.savefig(out_png,dpi=300,facecolor='white')
plt.close()

# Export data for Origin
import csv
with open(r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\BTC_fitting.csv','w',newline='',encoding='utf-8') as f:
    wr=csv.writer(f)
    wr.writerow(['Time_min','Measured','Fitted','Gaussian_comp','erfc_comp','Weight'])
    for ti,ci in zip(t_data,c_data):
        idx=np.argmin(np.abs(t_smooth-ti))
        wr.writerow([f'{ti:.1f}',f'{ci:.5f}',f'{blend[idx]:.5f}',f'{cr[idx]:.5f}',f'{cf[idx]:.5f}',f'{w[idx]:.5f}'])

import shutil
for f in ['Figure_BTC.pdf','Figure_BTC.png','BTC_fitting.csv']:
    shutil.copy2(rf'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\{f}', rf'c:\Users\郝\Desktop\{f}')

print(f'R2={r2:.4f}, RMSE={rmse:.4f}, erfc tail={tail_pct:.0f}%')
print('Figure_BTC.pdf + BTC_fitting.csv -> desktop')
