# -*- coding: utf-8 -*-
"""All 6 figures — strictly uniform style throughout."""
import numpy as np
from scipy.special import erfc
from scipy.optimize import curve_fit
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# ═══════════ UNIFORM STYLE ═══════════
SZ=dict(font='Arial',tick=4,label=4.5,title=5,legend=4,note=3.5,
        lw=0.8,spine=0.45,ms=2.5,mekw=0.12,
        fig_w=3.5,fig_h=1.45,left=0.12,right=0.96,bottom=0.22,top=0.85,wspace=0.35)
plt.rcParams.update({
    'font.family':'sans-serif','font.sans-serif':[SZ['font']],
    'font.size':SZ['tick'],'axes.titlesize':SZ['title'],'axes.labelsize':SZ['label'],
    'xtick.labelsize':SZ['tick'],'ytick.labelsize':SZ['tick'],'legend.fontsize':SZ['legend'],
    'figure.dpi':300,'savefig.dpi':300,'savefig.bbox':'tight','savefig.pad_inches':0.02,
    'axes.linewidth':SZ['spine'],'xtick.major.width':0.3,'ytick.major.width':0.3,
    'xtick.major.size':2,'ytick.major.size':2,
    'lines.linewidth':SZ['lw'],'lines.markersize':SZ['ms'],
    'axes.grid':False,'axes.facecolor':'white','figure.facecolor':'white',
})
C0='#333333';C1='#CC3333';C2='#3366AA';C3='#339955';C4='#CC8833';C5='#885599';C6='#339988';C7='#999999';C8='#DD6622'
TP=[C2,C3,C4,C1]

legkw=dict(frameon=True,fancybox=False,edgecolor='#ccc',fontsize=SZ['legend'],
           handletextpad=0.3,labelspacing=0.12,borderpad=0.25)

def setup():
    fig,axes=plt.subplots(1,3,figsize=(SZ['fig_w']*1.55,SZ['fig_h']))
    fig.subplots_adjust(wspace=SZ['wspace'],bottom=SZ['bottom'],top=SZ['top'],left=SZ['left'],right=SZ['right'])
    return fig,axes

def Lax(ax, nx=5, ny=5):
    ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(SZ['spine']);ax.spines['bottom'].set_linewidth(SZ['spine'])
    ax.tick_params(which='both',direction='in',top=False,right=False,left=True,bottom=True)
    ax.tick_params(which='major',length=2,width=0.3)
    ax.set_facecolor('white')
    ax.xaxis.set_major_locator(plt.MaxNLocator(nx))
    ax.yaxis.set_major_locator(plt.MaxNLocator(ny))

def save(fig,name):
    fig.savefig(OUT/name,dpi=300);plt.close(fig)

OUT=Path(r'c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\ESP-T_投稿文件\figures');OUT.mkdir(parents=True,exist_ok=True)
PI=np.pi;x0=100.;d0=5.;X2=x0*PI*d0*d0

# ═══════════ DATA ═══════════
ta=np.array([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105])
ca=np.array([0,0.58438,0.83879,1.0,0.92443,0.64736,0.35516,0.29471,0.27204,0.24433,0.20907,0.21914,0.19144,0.19899,0.17128,0.20403,0.17884,0.16373,0.16877,0.15617,0.15617,0.15113])
tf=ta[ta>0];cf=ca[ta>0]
p_btc=np.array([0.04590811,2334.008544,0.43116937,107.08687055,50.823237,25.660680,3.963037])
def btc(t,p):
    cb,A,a,al,Q,t0,s=p
    dn=np.sqrt(np.abs(16*al*Q*t*PI*d0*d0))+1e-300;z=(X2-4*Q*t)/dn
    cr=cb+(A*d0)/dn*np.exp(-z*z);cf2=cb+(a/2.0)*erfc(-z)
    w=0.5*(1+np.tanh((t0-t)/s));return w*cr+(1-w)*cf2,cr,cf2
td=np.linspace(0.1,110,400);Cb,Cr,Cf=btc(td,p_btc);Cp,_,_=btc(tf,p_btc)
res=(cf-Cp)*100;r2=1-np.sum((cf-Cp)**2)/np.sum((cf-cf.mean())**2);rmse=np.sqrt(np.mean((cf-Cp)**2))

# Refitted single models
pg=np.array([0.1612,1189.0,22.2,134.056]);pe=np.array([0.0,2.2409,974.5,992.923])
px=np.array([0.12,0.85,0.038]);pk=np.array([0.15,0.22])
def gc(t,p):cb,A,al,Q=p;dn=np.sqrt(np.abs(16*al*Q*t*PI*d0*d0))+1e-300;z=(X2-4*Q*t)/dn;return cb+(A*d0)/dn*np.exp(-z*z)
def ec(t,p):cb,a,al,Q=p;dn=np.sqrt(np.abs(16*al*Q*t*PI*d0*d0))+1e-300;z=(X2-4*Q*t)/dn;return cb+(a/2.0)*erfc(-z)
Cg=gc(td,pg);Ce=ec(td,pe);Cx_td=px[0]+px[1]*np.exp(-px[2]*td);Ck_td=pk[0]*td**pk[1]

# KP data
th=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14])
cd={30:np.array([0.013,0.035,0.047,0.065,0.077,0.089,0.099,0.102,0.108,0.112,0.116,0.120,0.123,0.125]),
    60:np.array([0.018,0.046,0.085,0.106,0.124,0.141,0.157,0.173,0.190,0.199,0.206,0.212,0.216,0.219]),
    90:np.array([0.026,0.071,0.109,0.139,0.157,0.171,0.172,0.182,0.188,0.221,0.228,0.233,0.237,0.241]),
    120:np.array([0.037,0.115,0.182,0.231,0.263,0.292,0.314,0.321,0.341,0.358,0.371,0.384,0.392,0.400])}
kp={}
for T,c in cd.items():kp[T],_=curve_fit(lambda t,K,n:K*t**n,th,c,p0=[0.05,0.5],maxfev=10000)

# Two-phase data
Qt=np.array([0.1,0.2,0.3,0.4])
C41=np.array([33.51,17.37,11.54,8.33]);C11=np.array([31.32,16.67,10.73,8.04]);C14=np.array([32.74,17.14,10.93,7.97])
F41=np.array([2.6808,2.7792,2.7696,2.6656]);F11=np.array([1.566,1.667,1.6095,1.608]);F14=np.array([0.6548,0.6856,0.6558,0.6376])
C41n=C41/np.max(C41);C11n=C11/np.max(C11);C14n=C14/np.max(C14)

# ═══════════ FIG 7 ═══════════
print("Fig 7")
fig,axes=setup()
for i,(ax,ti) in enumerate(zip(axes,['(a) Release profiles','(b) K-P model','(c) Release rate'])):
    for T,c,cl in [(30,cd[30],TP[0]),(60,cd[60],TP[1]),(90,cd[90],TP[2]),(120,cd[120],TP[3])]:
        K,n=kp[T]
        if i==0:tm=np.linspace(0.2,15,200);ax.plot(tm,K*tm**n,'-',color=cl,lw=0.8);ax.plot(th,c,'o',color=cl,ms=SZ['ms'],mec='white',mew=SZ['mekw'])
        elif i==1:tl=np.logspace(-0.5,1.2,200);ax.loglog(tl,K*tl**n,'-',color=cl,lw=0.8);ax.loglog(th,c,'o',color=cl,ms=SZ['ms'],mec='white',mew=SZ['mekw'])
        else:tm=np.linspace(0.3,15,200);ax.plot(tm,np.clip(K*n*tm**(n-1),0,0.12),'-',color=cl,lw=0.8)
    Lax(ax);ax.set_xlabel('Time (h)');ax.set_title(ti,fontweight='bold',pad=2)
    if i==0:
        ax.set_ylabel('$C/C_0$')
        for T,cl in [(30,TP[0]),(60,TP[1]),(90,TP[2]),(120,TP[3])]:ax.plot([],[],'o',color=cl,ms=3,mec='white',mew=0.15,label=f'{T} °C')
        ax.legend(ncol=4,loc='upper left',**legkw)
    elif i==1:ax.set_ylabel('$C/C_0$')
    else:
        ax.set_ylabel('d$(C/C_0)$/d$t$ (h$^{-1}$)')
        for T,cl in [(30,TP[0]),(60,TP[1]),(90,TP[2]),(120,TP[3])]:ax.plot([],[],'-',color=cl,lw=1.3,label=f'{T} °C')
        ax.legend(ncol=4,loc='upper right',**legkw)
save(fig,'Figure_3-7_release_kinetics.png');fig.savefig(OUT/'Figure_3-7_release_kinetics.pdf')

# ═══════════ FIG 8 ═══════════
print("Fig 8")
fig,axes=setup()
ax=axes[0]
ax.plot(ta,ca,'o',color=C0,ms=2.2,mec='white',mew=0.1,zorder=5)
ax.plot(td,Cb,'-',color=C1,lw=0.8);ax.plot(td,Cr,'--',color=C8,lw=0.65);ax.plot(td,Cf,'-',color=C6,lw=0.65)
ax.axvline(x=p_btc[5],color='gray',ls=':',lw=0.3)
ax.plot([],[],'o',color=C0,ms=2.8,label='Measured');ax.plot([],[],'-',color=C1,lw=1,label='Dual')
ax.plot([],[],'--',color=C8,lw=1,label='Gaussian');ax.plot([],[],'-',color=C6,lw=1,label='erfc')
ax.legend(ncol=2,loc='upper right',**legkw)
ax.text(75,0.22,f'$R^2$={r2:.4f}\nRMSE={rmse:.4f}\n$t_0$={p_btc[5]:.1f} min',fontsize=SZ['note'],color=C0,
        bbox=dict(boxstyle='round,pad=0.15',fc='white',alpha=0.85,ec='#ddd'))
ax.set_xlabel('Time (min)');ax.set_ylabel('$C/C_0$');ax.set_title('(a) BTC decomposition',fontweight='bold',pad=2)
ax.set_xlim(0,112);ax.set_ylim(0,1.15);Lax(ax)

ax=axes[1];ml,sl,bl=ax.stem(ta[ta>0],res,linefmt='-',markerfmt='o',basefmt='k-')
plt.setp(sl,lw=0.3,color=C0,alpha=0.3);plt.setp(ml,ms=2.2,color=C0,mec='white',mew=0.06);plt.setp(bl,lw=0.2,color='black')
ax.axhline(y=0,color='black',lw=0.2);ax.axhspan(-3,3,alpha=0.015,color='gray')
ax.set_xlabel('Time (min)');ax.set_ylabel('Residual (×10$^{-2}$)');ax.set_title('(b) Residuals',fontweight='bold',pad=2)
ax.set_xlim(0,110);ax.set_ylim(-8,8);Lax(ax)

ax=axes[2];ax.bar(['Pump','Fitted'],[0.50,0.46],color=[C7,C1],width=0.3,edgecolor='white',lw=0.06)
ax.text(0,0.53,'0.50',ha='center',fontsize=6,fontweight='bold',color=C7)
ax.text(1,0.49,'0.46',ha='center',fontsize=6,fontweight='bold',color=C1)
ax.set_ylabel('Flow rate (mL/min)');ax.set_title('(c) Self-calibration',fontweight='bold',pad=2)
ax.set_ylim(0,0.62);ax.set_xlim(-0.5,1.5);Lax(ax)
ax.text(0.5,0.58,'Δ = 8%',ha='center',fontsize=5.5,color=C1,fontweight='bold')
save(fig,'Figure_3-8_BTC_fitting.png');fig.savefig(OUT/'Figure_3-8_BTC_fitting.pdf')

# ═══════════ FIG 9 ═══════════
print("Fig 9")
fig,axes=plt.subplots(1,2,figsize=(SZ['fig_w']*1.55,SZ['fig_h']))
fig.subplots_adjust(wspace=SZ['wspace'],bottom=SZ['bottom'],top=SZ['top'],left=SZ['left'],right=SZ['right'])
ax=axes[0]
for nm,cl,cv,ls in [('Dual',C1,Cb,'-'),('Gaussian',C2,Cg,'--'),('erfc',C3,Ce,'--'),('Exponential',C5,Cx_td,'-.'),('K-P',C7,Ck_td,':')]:
    ax.plot(td,cv,color=cl,lw=0.8,ls=ls,label=nm)
ax.plot(ta,ca,'o',color=C0,ms=1.8,mec='white',mew=0.08,zorder=10)
ax.legend(ncol=2,loc='upper right',**legkw)
ax.set_xlabel('Time (min)');ax.set_ylabel('$C/C_0$');ax.set_title('(a) Model overlay',fontweight='bold',pad=2)
ax.set_xlim(0,112);ax.set_ylim(-0.02,1.15);Lax(ax)

ax=axes[1];yp=range(5)[::-1];dc=[92.16,62.51,68.42,32.66,0]
ax.barh(yp,dc[::-1],height=0.3,color=[C7,C5,C3,C2,C1][::-1],edgecolor='white',lw=0.06)
ax.set_yticks(yp);ax.set_yticklabels(['K-P','Exp.','erfc','Gaussian','Dual'][::-1],fontsize=SZ['tick'])
ax.set_xlabel('ΔAICc');ax.set_title('(b) Model selection',fontweight='bold',pad=2)
ax.axvline(x=10,color='gray',ls=':',lw=0.3)
ax.text(12,1,'Decisive',fontsize=4,color='gray',fontstyle='italic')
ax.text(3,3.3,'$w>0.9999$',fontsize=5.5,color=C1,fontweight='bold')
Lax(ax)
save(fig,'Figure_3-9_model_comparison.png');fig.savefig(OUT/'Figure_3-9_model_comparison.pdf')

# ═══════════ FIG 10 ═══════════
print("Fig 10")
tp=15.0;Qp=100*PI*0.5**2/(4*tp);ar=np.trapezoid(ca,ta);mrt=np.trapezoid(ta*ca,ta)/ar;Qm=100*PI*0.5**2/(4*mrt)
fig,axes=setup()
ax=axes[0];ax.plot(ta,ca,'o-',color=C0,ms=1.6,lw=0.3,zorder=5)
ax.axvline(x=tp,color=C2,ls='--',lw=0.4);ax.plot(tp,1.0,'s',color=C2,ms=3,mec='white',mew=0.1,zorder=10)
ax.axvline(x=mrt,color=C4,ls='-.',lw=0.4);ax.plot(mrt,np.interp(mrt,ta,ca),'D',color=C4,ms=2.8,mec='white',mew=0.1,zorder=10)
ax.text(65,1.07,f'$t_{{\\rm peak}}$={tp:.0f} min',fontsize=SZ['note'],color=C2,fontweight='bold')
ax.text(65,0.98,f'MRT={mrt:.1f} min',fontsize=SZ['note'],color=C4,fontweight='bold')
ax.set_xlabel('Time (min)');ax.set_ylabel('$C/C_0$');ax.set_title('(a) BTC with markers',fontweight='bold',pad=2)
ax.set_xlim(0,112);ax.set_ylim(0,1.15);Lax(ax)

ax=axes[1];qv=[0.50,Qp,3.93,Qm,0.46];er=[0,162,685,5.8,8];lb=['Pump','Peak','Half','MRT','ADE'];bc=[C7,C2,'#88BBE8',C4,C1]
bars=ax.bar(range(5),qv,color=bc,width=0.3,edgecolor='white',lw=0.06)
ax.set_xticks(range(5));ax.set_xticklabels(lb,fontsize=SZ['tick']);ax.set_ylabel('$Q$ (mL/min)');ax.set_title('(b) Flow rate',fontweight='bold',pad=2)
ax.axhline(y=0.50,color='gray',ls=':',lw=0.3)
for i,(b,e) in enumerate(zip(bars,er)):
    y=b.get_height()+0.06
    if e==0:ax.text(i,y,'Ref',ha='center',fontsize=4,color='gray')
    elif e>50:ax.text(i,y,f'+{e}%',ha='center',fontsize=4.5,color=C2,fontweight='bold')
    elif e>10:ax.text(i,y,f'+{e:.0f}%',ha='center',fontsize=4.5,color=C4,fontweight='bold')
    else:ax.text(i,y,'−8%',ha='center',fontsize=4.5,color=C1,fontweight='bold')
ax.set_ylim(0,max(qv)*1.4);Lax(ax)

ax=axes[2];sc=np.array([[0,0,0,0,0],[1,0,0,0,0],[3,0,1,1,0],[3,3,3,3,3]]);xp=np.arange(5);ct=['$Q$','Decomp.','Mechan.','$\\sigma$','Calib.']
for i,(lb,cl) in enumerate(zip(['Peak','Half','MRT','ADE'],[C2,'#88BBE8',C4,C1])):ax.bar(xp+i*0.18-0.27,sc[i],0.16,label=lb,color=cl,edgecolor='white',lw=0.06)
ax.set_xticks(xp);ax.set_xticklabels(ct,fontsize=SZ['note']);ax.set_ylabel('Score');ax.set_title('(c) Capability',fontweight='bold',pad=2)
ax.legend(ncol=4,loc='upper left',frameon=True,fancybox=False,edgecolor='#ccc',fontsize=4.5,columnspacing=0.3,handletextpad=0.15,labelspacing=0.1,borderpad=0.2)
ax.set_ylim(0,4);Lax(ax)
save(fig,'Figure_3-12_TOA_comparison.png');fig.savefig(OUT/'Figure_3-12_TOA_comparison.pdf')

# ═══════════ FIG 11 ═══════════
print("Fig 11")
ss=np.linspace(1.98,11.89,50);ef=[]
for s in ss:pt=p_btc.copy();pt[6]=s;Ct,Cr,Cf=btc(td,pt);ef.append(np.trapezoid(Cf,td)/np.trapezoid(Ct,td)*100)
ef=np.array(ef)
fig,axes=setup()
ax=axes[0];ax.plot(ss,ef,'-',color=C6,lw=0.9,marker='o',ms=1.2,mec='white',mew=0.05)
ax.axhline(y=47.0,color='gray',ls=':',lw=0.3);ax.axvline(x=3.96,color='gray',ls=':',lw=0.3)
ax.set_xlabel('$\\sigma$ (min)');ax.set_ylabel('erfc fraction (%)');ax.set_title('(a) Robustness',fontweight='bold',pad=2)
ax.text(7,47.2,'46.8−47.5% (Δ<1 pp)',fontsize=SZ['note'],ha='center',bbox=dict(boxstyle='round,pad=0.12',fc='white',alpha=0.9,ec='#ddd'))
ax.set_xlim(1,13);ax.set_ylim(46,48);Lax(ax)

ax=axes[1];p_fit=p_btc.copy();p_fit[6]=3.96;Ct2,Cr2,Cf2=btc(td,p_fit)
ax.fill_between(td,0,Cr2,alpha=0.07,color=C8);ax.fill_between(td,0,Cf2,alpha=0.07,color=C6)
ax.plot(td,Ct2,'-',color=C1,lw=0.8);ax.plot(ta,ca,'o',color=C0,ms=1.6,mec='white',mew=0.05,zorder=5)
ax.plot([],[],'-',color=C8,lw=2.5,alpha=0.2,label='Gaussian (53%)');ax.plot([],[],'-',color=C6,lw=2.5,alpha=0.2,label='erfc (47%)')
ax.legend(loc='upper right',**legkw)
ax.set_xlabel('Time (min)');ax.set_ylabel('$C/C_0$');ax.set_title('(b) $\\sigma$=3.96 min',fontweight='bold',pad=2)
ax.set_xlim(0,112);ax.set_ylim(0,1.12);Lax(ax)

ax=axes[2]
for s,al in zip([1.98,3.96,5.94,7.93,9.91,11.89],np.linspace(0.2,1.0,6)):
    pt=p_btc.copy();pt[6]=s;Cts,_,_=btc(td,pt);ax.plot(td,Cts,'-',lw=0.65,alpha=al,color=C1 if s<5 else C2)
ax.plot(ta,ca,'o',color=C0,ms=1.6,mec='white',mew=0.05,zorder=10)
ax.set_xlabel('Time (min)');ax.set_ylabel('$C/C_0$');ax.set_title('(c) Insensitivity',fontweight='bold',pad=2)
ax.set_xlim(0,112);ax.set_ylim(0,1.12);Lax(ax)
save(fig,'Figure_3-10_sigma_sensitivity.png');fig.savefig(OUT/'Figure_3-10_sigma_sensitivity.pdf')

# ═══════════ FIG 12 ═══════════
print("Fig 12")
fig,axes=setup()
ax=axes[0]
for c,cl,lb in [(C41n,C2,'OWR=4:1'),(C11n,C3,'OWR=1:1'),(C14n,C4,'OWR=1:4')]:ax.plot(Qt,c,'o-',color=cl,lw=0.8,ms=SZ['ms'],mec='white',mew=SZ['mekw'],label=lb)
ax.legend(loc='upper right',**legkw)
ax.set_xlabel('Total flow rate (mL/min)');ax.set_ylabel('$C_\\mathrm{oil}$ (norm.)');ax.set_title('(a) Dilution',fontweight='bold',pad=2);Lax(ax)

ax=axes[1]
for f,cl,lb in [(F41,C2,'OWR=4:1'),(F11,C3,'OWR=1:1'),(F14,C4,'OWR=1:4')]:
    ax.scatter(Qt,f,color=cl,s=14,ec='white',lw=0.06,label=lb);ax.axhline(y=np.mean(f),color=cl,ls='--',lw=0.25,alpha=0.25)
ax.legend(loc='upper right',**legkw)
ax.set_xlabel('Total flow rate (mL/min)');ax.set_ylabel('$F_\\mathrm{O}$ ($\\mu$g/min)');ax.set_title('(b) Flux',fontweight='bold',pad=2);Lax(ax)

ax=axes[2]
fr=np.array([0.6548,0.6856,0.6558,0.6376,1.566,1.667,1.6095,1.608,2.6808,2.7792,2.7696,2.6656])
qo=np.array([0.02]*4+[0.05]*4+[0.08]*4)
ax.scatter(qo,fr,c=C1,s=16,ec='white',lw=0.06,zorder=5);ax.plot([0,0.1],[0,3.0],'--',color='gray',lw=0.3)
ax.set_xlabel('Oil flow rate (mL/min)');ax.set_ylabel('$F_\\mathrm{O}$ ($\\mu$g/min)');ax.set_title('(c) Allocation',fontweight='bold',pad=2)
ax.text(0.04,2.6,'$r=0.97$, RMSD=8.3%',fontsize=SZ['note'],color=C1,fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.15',fc='white',alpha=0.9,ec='#ddd'))
Lax(ax)
save(fig,'Figure_3-11_twophase_flow.png');fig.savefig(OUT/'Figure_3-11_twophase_flow.pdf')

print(f"\nDone. 6 figures in {OUT}")
print(f"Style: uniform — {SZ['font']}, {SZ['title']}pt title, {SZ['label']}pt label, {SZ['tick']}pt tick, L-axes, boxed legends")
