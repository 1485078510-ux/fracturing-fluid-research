# -*- coding: utf-8 -*-
"""Export all figures as editable SVG + retain PDF/PNG."""
import numpy as np
from scipy.special import erfc
from scipy.integrate import trapezoid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'stix', 'font.size': 10,
    'axes.labelsize': 11, 'xtick.labelsize': 9, 'ytick.labelsize': 9,
    'legend.fontsize': 9, 'figure.facecolor': 'white', 'axes.facecolor': 'white',
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.linewidth': 0.8, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})

BASE = r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合'

# ============================================================
# FIGURE 3-8: BTC Fitting
# ============================================================
cb=0.045908; A=2334.0; a=0.43117; alpha=107.09; Q=50.823; t0=25.661; sigma0=3.963
x_val,d_val=100.0,5.0; XPD2=x_val*np.pi*d_val*d_val

def model(t,sigma):
    denom=np.sqrt(np.abs(16*alpha*Q*t*np.pi*d_val*d_val))+1e-300
    z=(XPD2-4*Q*t)/denom
    cr=cb+(A*d_val)/denom*np.exp(-z*z)
    cf=cb+(a/2)*erfc(-z)
    w=0.5*(1+np.tanh((t0-t)/sigma))
    return cr,cf,w,w*cr+(1-w)*cf

t_data=np.array([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105])
c_data=np.array([0,0.58438,0.83879,1.0,0.92443,0.64736,0.35516,0.29471,0.27204,
                  0.24433,0.20907,0.21914,0.19144,0.19899,0.17128,0.20403,
                  0.17884,0.16373,0.16877,0.15617,0.15617,0.15113])
mask=t_data>0; t_fit=t_data[mask]; c_fit=c_data[mask]
t_smooth=np.linspace(0.01,110,2000)
cr,cf,w,blend=model(t_smooth,sigma0)
pred=blend[np.searchsorted(t_smooth,t_fit)]
r2=1-np.sum((c_fit-pred)**2)/np.sum((c_fit-np.mean(c_fit))**2)
total_integ=trapezoid(blend,t_smooth)
tail_pct=100*trapezoid((1-w)*cf,t_smooth)/total_integ

C_BLEND='#d7191c'; C_GAUSS='#2c7bb6'; C_TAIL='#fdae61'; C_DATA='#333333'

fig,axes=plt.subplots(1,3,figsize=(12,4.2),gridspec_kw={'width_ratios':[1.3,1,1]})
ax=axes[0]
ax.fill_between(t_smooth,0,cr,alpha=0.10,color=C_GAUSS,ec='none')
ax.fill_between(t_smooth,0,cf,alpha=0.10,color=C_TAIL,ec='none')
ax.plot(t_smooth,cr,'--',color=C_GAUSS,lw=1.2,alpha=0.7,label='Gaussian (pulse)')
ax.plot(t_smooth,cf,'--',color=C_TAIL,lw=1.2,alpha=0.7,label='erfc (tail)')
ax.plot(t_smooth,blend,'-',color=C_BLEND,lw=2.5,label='Blended model')
ax.plot(t_data,c_data,'o',color=C_DATA,ms=8,mfc=C_DATA,mew=0,zorder=10,label='Measured')
ax.axvline(x=t0,color='gray',ls=':',lw=1.2,alpha=0.6,label=f't₀ = {t0:.1f} min')
ax.set_xlabel('Time (min)'); ax.set_ylabel('Normalized concentration C/C₀')
ax.set_title('(a) Model fit',loc='left',fontweight='bold')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8,loc='upper right')
ax.set_xlim(-2,112); ax.set_ylim(-0.05,1.15)
ax.annotate(f'R² = {r2:.4f}\nGauss: {100*trapezoid(w*cr,t_smooth)/total_integ:.0f}%\nerfc:  {tail_pct:.0f}%',
            xy=(0.97,0.97),xycoords='axes fraction',ha='right',va='top',fontsize=8,
            bbox=dict(boxstyle='round',fc='lightyellow',alpha=0.9))

ax=axes[1]
ax.bar(t_fit,(c_fit-pred)*100,color='steelblue',width=3,alpha=0.7,edgecolor='white',lw=0.3)
ax.axhline(y=0,color='gray',lw=0.8)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Residual x100')
ax.set_title('(b) Residuals',loc='left',fontweight='bold'); ax.set_xlim(-2,112)

ax=axes[2]
ax.barh(['Pump set','Fitted'],[0.50,0.46],height=0.4,color=['#999','#d7191c'],edgecolor='white')
ax.set_xlabel('Flow rate Q (mL/min)')
ax.set_title('(c) Flow rate validation',loc='left',fontweight='bold'); ax.set_xlim(0,0.6)
for i,(v,x) in enumerate([(0.50,0),(0.46,1)]):
    ax.text(v+0.01,x,f'{v:.2f}',va='center',fontsize=10,fontweight='bold')
ax.annotate('8% difference',xy=(0.48,0.3),fontsize=9,color=C_BLEND,fontweight='bold')

plt.tight_layout(pad=1.5)
fig.savefig(f'{BASE}\\Figure_BTC.svg',dpi=300,facecolor='white')
fig.savefig(f'{BASE}\\Figure_BTC.pdf',dpi=300,facecolor='white')
fig.savefig(f'{BASE}\\Figure_BTC.png',dpi=300,facecolor='white')
plt.close()
print('Figure_BTC.svg saved')

# ============================================================
# FIGURE S1: Sigma Sensitivity (reuse data from earlier scripts)
# ============================================================
multipliers=np.arange(0.5,3.01,0.25)
sigmas=sigma0*multipliers
tail_pcts=[]
for sv in sigmas:
    _,cf_s,w_s,bl_s=model(t_smooth,sv)
    tail_pcts.append(100*trapezoid((1-w_s)*cf_s,t_smooth)/trapezoid(bl_s,t_smooth))
baseline_tail=tail_pcts[len(multipliers)//2]

fig=plt.figure(figsize=(6.5,5))
ax=fig.add_subplot(111)
ax.plot(sigmas,tail_pcts,'o-',color=C_TAIL,lw=2,ms=8,mew=1.5,mfc='white',zorder=3)
ax.axvline(x=sigma0,color='#5e3c99',ls='--',lw=1.8,alpha=0.8,label=f'Fitted sigma = {sigma0:.2f}')
ax.fill_between([min(sigmas),max(sigmas)],[baseline_tail-1]*2,[baseline_tail+1]*2,
                alpha=0.08,color=C_TAIL,ec='none')
ax.set_xlabel('sigma (min)',fontweight='bold')
ax.set_ylabel('erfc Tail Contribution (%)',fontweight='bold')
ax.set_title('Figure S1: sigma Sensitivity Analysis',fontsize=11,fontweight='bold')
ax.legend(frameon=True,framealpha=0.9,edgecolor='#ccc',fontsize=9)
ax.set_ylim(44,50)
ax.annotate(f'Range: {min(tail_pcts):.1f}-{max(tail_pcts):.1f}%\nSpan: {max(tail_pcts)-min(tail_pcts):.1f} pp',
            xy=(8,45.5),fontsize=9,color='#333',
            bbox=dict(boxstyle='round',fc='#f8f8f8',ec='#ccc',alpha=0.9))
plt.tight_layout()
fig.savefig(f'{BASE}\\Figure_S1.svg',dpi=300,facecolor='white')
fig.savefig(f'{BASE}\\Figure_S1.pdf',dpi=300,facecolor='white')
fig.savefig(f'{BASE}\\Figure_S1.png',dpi=300,facecolor='white')
plt.close()
print('Figure_S1.svg saved')

# ============================================================
# FIGURE S2: Model Comparison
# ============================================================
models=['Dual tanh','Gaussian','erfc','Exponential','K-P']
aicc=[0,32.66,68.42,62.51,92.16]
colors=['#d7191c','#2c7bb6','#fdae61','#5e3c99','#999999']

fig=plt.figure(figsize=(7,4))
ax=fig.add_subplot(111)
bars=ax.barh(models,aicc,color=colors,height=0.55,edgecolor='white',lw=0.8,zorder=3)
for bar,v in zip(bars,aicc):
    ax.text(bar.get_width()+0.8,bar.get_y()+bar.get_height()/2,f'Delta AICc = {v:.1f}',
            va='center',fontsize=9,color='#333')
ax.set_xlabel('Delta AICc (lower = better)',fontweight='bold')
ax.set_title('Figure S2: Model Comparison',fontsize=11,fontweight='bold')
ax.invert_yaxis(); ax.set_xlim(0,105)
ax.grid(True,alpha=0.2,axis='x',zorder=0)
ax.annotate('F-test (Dual vs Gaussian):\nF(3,14) = 34.7, p < 0.0001',
            xy=(0.95,0.12),fontsize=9,xycoords='axes fraction',ha='right',
            bbox=dict(boxstyle='round',fc='#fff9e6',ec='#e6c300',alpha=0.9,lw=1))
plt.tight_layout()
fig.savefig(f'{BASE}\\Figure_S2.svg',dpi=300,facecolor='white')
fig.savefig(f'{BASE}\\Figure_S2.pdf',dpi=300,facecolor='white')
fig.savefig(f'{BASE}\\Figure_S2.png',dpi=300,facecolor='white')
plt.close()
print('Figure_S2.svg saved')

# Copy to folder
import shutil
folder = r'C:\Users\郝\Desktop\ESP-T_投稿文件'
for f in ['Figure_BTC.svg','Figure_S1.svg','Figure_S2.svg']:
    src = f'{BASE}\\{f}'
    if os.path.exists(src):
        shutil.copy2(src, f'{folder}\\{f}')
        print(f'{f} -> folder')
print('All SVG files exported.')
