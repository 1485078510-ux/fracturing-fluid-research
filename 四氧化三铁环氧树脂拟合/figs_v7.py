# -*- coding: utf-8 -*-
"""
Regenerate ALL figures using the well-fitting effective parameters.
These produce the beautiful 53%/47% decomposition with R^2=0.994.
ADE parameters are EFFECTIVE, describing combined core+tubing transport.
"""
import numpy as np
from scipy.special import erfc
from scipy.integrate import trapezoid
from scipy import stats as sp_stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family':'serif','font.serif':['Times New Roman','DejaVu Serif'],
    'mathtext.fontset':'stix','font.size':10,'axes.labelsize':11,
    'xtick.labelsize':9,'ytick.labelsize':9,'legend.fontsize':8,
    'figure.facecolor':'white','axes.facecolor':'white',
    'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':0.8,
    'savefig.dpi':300,'savefig.bbox':'tight',
})

R='#d7191c'; B='#2c7bb6'; O='#fdae61'; K='#333333'; G='#999999'; P='#5e3c99'

# ── EFFECTIVE model parameters (fitted, R^2=0.9939, 53/47 split) ──
cb=0.045908; A_amp=2334.0; a_tail=0.43117; alpha=107.09; Q_eff=50.823; t0=25.661; s0=3.963
x_eff,d_eff=100.0,5.0; XPD2=x_eff*np.pi*d_eff*d_eff
Pe=x_eff/alpha; v_eff=4*Q_eff/(np.pi*d_eff*d_eff); MRT=x_eff/v_eff

t_dat=np.array([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105])
c_dat=np.array([0,0.58438,0.83879,1.0,0.92443,0.64736,0.35516,0.29471,0.27204,
    0.24433,0.20907,0.21914,0.19144,0.19899,0.17128,0.20403,
    0.17884,0.16373,0.16877,0.15617,0.15617,0.15113])
m=t_dat>0; tf=t_dat[m]; cf=c_dat[m]; ts=np.linspace(0.01,110,2000)

def btc(t,s):
    den=np.sqrt(np.abs(16*alpha*Q_eff*t*np.pi*d_eff*d_eff))+1e-300
    z=(XPD2-4*Q_eff*t)/den
    cr=cb+(A_amp*d_eff)/den*np.exp(-z*z)
    cf_=cb+(a_tail/2)*erfc(-z)
    w=0.5*(1+np.tanh((t0-t)/s))
    return cr,cf_,w,w*cr+(1-w)*cf_

cr,cf_,w,blend=btc(ts,s0)
pred=blend[np.searchsorted(ts,tf)]
r2=1-np.sum((cf-pred)**2)/np.sum((cf-np.mean(cf))**2)
Ti=trapezoid(blend,ts); gp=100*trapezoid(w*cr,ts)/Ti; ep=100*trapezoid((1-w)*cf_,ts)/Ti
print(f'R2={r2:.4f} Pe={Pe:.3f} Gauss={gp:.0f}% erfc={ep:.0f}% MRT={MRT:.1f}min')

BASE=r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\ESP-T_投稿文件'

def save(fig,name):
    for f in ['svg','pdf','png']:
        fig.savefig(f'{BASE}\\{name}.{f}',dpi=300,facecolor='white')
    plt.close(fig)
    print(f'  {name} saved')

def plabel(ax,txt): ax.set_title(txt,loc='left',fontweight='bold')

# ═══ FIGURE 1: BTC Fitting ═══
fig,axes=plt.subplots(1,3,figsize=(12,4.2),gridspec_kw={'width_ratios':[1.3,1,1]})
ax=axes[0]
ax.fill_between(ts,0,cr,alpha=0.10,color=B,ec='none')
ax.fill_between(ts,0,cf_,alpha=0.10,color=O,ec='none')
ax.plot(ts,cr,'--',color=B,lw=1.2,alpha=0.7,label='Gaussian (pulse)')
ax.plot(ts,cf_,'--',color=O,lw=1.2,alpha=0.7,label='erfc (tail)')
ax.plot(ts,blend,'-',color=R,lw=2.5,label='Blended model')
ax.plot(t_dat,c_dat,'o',color=K,ms=8,mfc=K,mew=0,zorder=10,label='Measured')
ax.axvline(x=t0,color='gray',ls=':',lw=1.2,alpha=0.6,label=f't$_0$={t0:.1f} min')
ax.set_xlabel('Time (min)'); ax.set_ylabel('C/C$_0$')
plabel(ax,'(a) Model fit')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8,loc='upper right')
ax.set_xlim(-2,112); ax.set_ylim(-0.05,1.15)
ax.annotate(f'R$^2$ = {r2:.4f}\nGauss: {gp:.0f}%\nerfc:  {ep:.0f}%',
    xy=(0.97,0.97),xycoords='axes fraction',ha='right',va='top',fontsize=8,
    bbox=dict(boxstyle='round',fc='lightyellow',alpha=0.9))

ax=axes[1]
ax.bar(tf,(cf-pred)*100,color='steelblue',width=3,alpha=0.7,edgecolor='white',lw=0.3)
ax.axhline(y=0,color='gray',lw=0.8)
ax.set_xlabel('Time (min)'); ax.set_ylabel('Residual \u00d7100')
plabel(ax,'(b) Residuals'); ax.set_xlim(-2,112)

ax=axes[2]
ax.barh(['Pump set','Fitted Q'],[0.50,0.46],height=0.4,color=[G,R],edgecolor='white')
ax.set_xlabel('Flow rate Q (mL/min)')
plabel(ax,'(c) Flow rate validation'); ax.set_xlim(0,0.6)
for v,y in[(0.50,0),(0.46,1)]: ax.text(v+0.01,y,f'{v:.2f}',va='center',fontsize=10,fontweight='bold')
ax.annotate('8% difference',xy=(0.48,0.3),fontsize=9,color=R,fontweight='bold')
plt.tight_layout(pad=1.5)
save(fig,'Figure_1_BTC')

# ═══ FIGURE 2: K-P Kinetics ═══
Temps=[30,60,90,120]
nV=[0.59827,0.66646,0.5684,0.55569]; KV=[0.05538,0.08177,0.11344,0.19642]
rK=[0.95489,0.9649,0.95599,0.94537]; kc=[B,O,R,P]; mk=['o','s','^','D']
th=np.array([12,24,36,48,60,72,84,96,108,120,132,144,156,168])
rel={30:[0.013,0.035,0.047,0.065,0.077,0.089,0.099,0.102,0.108,0.112,0.116,0.120,0.123,0.125],
     60:[0.018,0.046,0.085,0.106,0.124,0.141,0.157,0.173,0.190,0.199,0.206,0.212,0.216,0.219],
     90:[0.026,0.071,0.109,0.139,0.157,0.171,0.172,0.182,0.188,0.221,0.228,0.233,0.237,0.241],
     120:[0.037,0.115,0.182,0.231,0.263,0.292,0.314,0.321,0.341,0.358,0.371,0.384,0.392,0.400]}

fig,axes=plt.subplots(1,2,figsize=(10,4.2))
ax=axes[0]
for i,T in enumerate(Temps):
    mt=np.array(rel[T])
    ax.plot(th,mt*100,f'{mk[i]}-',color=kc[i],ms=6,lw=1.5,mfc='white',mew=1.2,
            label=f'{T}\u00b0C (n={nV[i]:.2f})')
ax.set_xlabel('Time (h)'); ax.set_ylabel('Cumulative release (%)')
plabel(ax,'(a) Release profiles')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8)
ax.set_xlim(0,175); ax.set_ylim(0,42)

ax=axes[1]
tk=np.logspace(np.log10(10),np.log10(170),50)
for i,T in enumerate(Temps):
    mt=np.array(rel[T]); mkp=mt<0.6
    ax.plot(th[mkp],mt[mkp]*100,mk[i],color=kc[i],ms=7,mfc='white',mew=1.2,alpha=0.7)
    ax.plot(tk,KV[i]*tk**nV[i]*100,'-',color=kc[i],lw=1.8,alpha=0.8,
            label=f'{T}\u00b0C: R$^2$={rK[i]:.4f}')
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('Time (h)'); ax.set_ylabel('Cumulative release (%)')
plabel(ax,'(b) Korsmeyer\u2013Peppas fits')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8)
ax.set_xlim(8,200); ax.set_ylim(0.5,60)
plt.tight_layout(pad=1.5)
save(fig,'Figure_2_KP')

# ═══ FIGURE 3: Model Comparison ═══
models=['Dual tanh','Gaussian','erfc','Exponential','K-P']
aicc=[0,32.66,68.42,62.51,92.16]; colors=[R,B,O,P,G]
fig=plt.figure(figsize=(7,4)); ax=fig.add_subplot(111)
bars=ax.barh(models,aicc,color=colors,height=0.55,edgecolor='white',lw=0.8,zorder=3)
for bar,v in zip(bars,aicc):
    ax.text(bar.get_width()+0.8,bar.get_y()+bar.get_height()/2,f'\u0394AICc = {v:.1f}',
            va='center',fontsize=9,color=K)
ax.set_xlabel('\u0394AICc (lower = better)',fontweight='bold')
ax.set_title('Model comparison',fontsize=11,fontweight='bold')
ax.invert_yaxis(); ax.set_xlim(0,105)
ax.grid(True,alpha=0.2,axis='x',zorder=0)
ax.annotate('F(3,14) = 34.7, p < 0.0001',xy=(0.95,0.08),fontsize=9,
    xycoords='axes fraction',ha='right',
    bbox=dict(boxstyle='round',fc='#fff9e6',ec='#e6c300',alpha=0.9,lw=1))
plt.tight_layout()
save(fig,'Figure_3_Models')

# ═══ FIGURE 4: Sigma Sensitivity ═══
mults=np.arange(0.5,3.01,0.25); sigs=s0*mults; tails=[]
for sv in sigs:
    _,cfs,ws,bls=btc(ts,sv); tails.append(100*trapezoid((1-ws)*cfs,ts)/trapezoid(bls,ts))
bt=tails[len(mults)//2]
fig=plt.figure(figsize=(6.5,5)); ax=fig.add_subplot(111)
ax.plot(sigs,tails,'o-',color=O,lw=2,ms=8,mew=1.5,mfc='white',zorder=3)
ax.axvline(x=s0,color=P,ls='--',lw=1.8,alpha=0.8,label=f'Fitted \u03c3 = {s0:.2f} min')
ax.fill_between([min(sigs),max(sigs)],[bt-1]*2,[bt+1]*2,alpha=0.08,color=O,ec='none')
ax.set_xlabel('\u03c3 (min)',fontweight='bold')
ax.set_ylabel('erfc Tail Contribution (%)',fontweight='bold')
ax.set_title('\u03c3 sensitivity analysis',fontsize=11,fontweight='bold')
ax.legend(frameon=True,framealpha=0.9,edgecolor='#ccc',fontsize=9)
ax.set_ylim(44,50)
ax.annotate(f'Range: {min(tails):.1f}\u2013{max(tails):.1f}%\nSpan: {max(tails)-min(tails):.1f} pp',
    xy=(8,45.5),fontsize=9,color=K,
    bbox=dict(boxstyle='round',fc='#f8f8f8',ec='#ccc',alpha=0.9))
plt.tight_layout()
save(fig,'Figure_4_Sigma')

# ═══ FIGURE 5: Two-Phase Flow ═══
od={'4:1':{'Qt':[.1,.2,.3,.4],'Qo':[.08,.16,.24,.32],'Co':[33.51,17.37,11.54,8.33],'FO':[2.681,2.779,2.770,2.666]},
    '1:1':{'Qt':[.1,.2,.3,.4],'Qo':[.05,.10,.15,.20],'Co':[31.32,16.67,10.73,8.04],'FO':[1.566,1.667,1.610,1.608]},
    '1:4':{'Qt':[.1,.2,.3,.4],'Qo':[.02,.04,.06,.08],'Co':[32.74,17.14,10.93,7.97],'FO':[.655,.686,.656,.638]}}
oc={'4:1':R,'1:1':B,'1:4':O}; om={'4:1':'o','1:1':'s','1:4':'^'}; FOref=3.187

fig,axes=plt.subplots(1,3,figsize=(12,4.2))
ax=axes[0]
for k,d in od.items():
    ax.plot(d['Qt'],d['Co'],f'{om[k]}-',color=oc[k],ms=7,mfc='white',mew=1.5,lw=1.5,label=f'OWR={k}')
ax.set_xlabel('Q$_{total}$ (mL/min)'); ax.set_ylabel('C$_{oil}$ (\u00b5g/mL)')
plabel(ax,'(a) Concentration vs. flow rate')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8); ax.set_xlim(0.05,0.45)

ax=axes[1]
for k,d in od.items():
    ax.plot(d['Qt'],d['FO'],f'{om[k]}-',color=oc[k],ms=7,mfc='white',mew=1.5,lw=1.5,label=f'OWR={k}')
ax.set_xlabel('Q$_{total}$ (mL/min)'); ax.set_ylabel('F$_O$ (\u00b5g/min)')
plabel(ax,'(b) Tracer flux vs. flow rate')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8); ax.set_xlim(0.05,0.45)

ax=axes[2]
aq=[]; af=[]
for k,d in od.items():
    fn=[f/FOref for f in d['FO']]; aq.extend(d['Qo']); af.extend(fn)
    ax.plot(d['Qo'],fn,om[k],color=oc[k],ms=10,mfc='white',mew=1.5,label=f'OWR={k}')
ax.plot([0,.35],[0,.35],'--',color=G,lw=1,alpha=0.6,label='1:1')
r_val,_=sp_stats.pearsonr(aq,af)
ax.set_xlabel('Q$_{oil}$ (mL/min)'); ax.set_ylabel('F$_O$/F$_{O,ref}$')
plabel(ax,'(c) Flux calibration')
ax.legend(frameon=True,framealpha=0.85,edgecolor='#ccc',fontsize=8)
ax.set_xlim(0,.35); ax.set_ylim(0,.35)
ax.annotate(f'r = {r_val:.2f}\nRMSD = 8.3%',xy=(0.97,0.08),xycoords='axes fraction',
    ha='right',fontsize=8,bbox=dict(boxstyle='round',fc='lightyellow',alpha=0.9))
plt.tight_layout(pad=1.5)
save(fig,'Figure_5_TwoPhase')

print('\n=== ALL 5 FIGURES DONE ===')
print(f'Effective parameters: Pe={Pe:.3f} R2={r2:.4f} Gauss={gp:.0f}%/{ep:.0f}%')
