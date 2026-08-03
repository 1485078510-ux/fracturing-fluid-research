# -*- coding: utf-8 -*-
"""图1：改性稀土铝酸盐荧光粉结构示意图 - 核壳结构剖面图（紧凑布局，短指示线）"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'dejavusans'  # sans-serif math to match Chinese text

FIG_DIR = r"荧光压裂液\figures"
os.makedirs(FIG_DIR, exist_ok=True)

fig, ax = plt.subplots(1, 1, figsize=(16, 9))
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.set_aspect('equal')
ax.axis('off')

# === Colors ===
CORE_C = '#FFD54F'; CORE_E = '#F9A825'
KH550_C = '#FFCC80'; KH550_E = '#E65100'
PEG_C = '#BBDEFB'; PEG_E = '#1565C0'

# Core structure shifted LEFT: center at (4.5, 5.0)
cx, cy = 4.5, 5.0
peg_r, kh550_r, core_r = 2.5, 1.7, 1.0

# === Draw concentric circles ===
peg = Circle((cx, cy), peg_r, facecolor=PEG_C, edgecolor=PEG_E, linewidth=2.5,
             alpha=0.3, linestyle='--', zorder=1)
ax.add_patch(peg)
kh550 = Circle((cx, cy), kh550_r, facecolor=KH550_C, edgecolor=KH550_E, linewidth=2.5,
               alpha=0.55, zorder=2)
ax.add_patch(kh550)
core = Circle((cx, cy), core_r, facecolor=CORE_C, edgecolor=CORE_E, linewidth=3, zorder=3)
ax.add_patch(core)

# === Core label ===
ax.text(cx, cy, 'SrAl$_2$O$_4$:Eu$^{2+}$,Dy$^{3+}$\n荧光粉基体',
        ha='center', va='center', fontsize=11, fontweight='bold', color='#5D4037', zorder=4)
ax.text(cx, cy-0.4, '(800~1200目, D$_{50}$≈13μm)', ha='center', va='center',
        fontsize=8, color='#795548', zorder=4)

# === Layer name labels on the circles ===
ax.text(cx+2.55, cy+0.1, 'PEG4000', fontsize=9, fontweight='bold', color=PEG_E, va='center')
ax.text(cx+1.75, cy+0.1, 'KH550', fontsize=9, fontweight='bold', color=KH550_E, va='center')

# Si-O-Al mark inside KH550 layer
ax.text(cx+1.1, cy+0.75, 'Si-O-Al\n共价键', fontsize=7, color='#BF360C', fontstyle='italic',
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='#BF360C', alpha=0.7), zorder=5)

# === -NH2 groups on KH550 surface ===
nh2_pts = [(cx-1.4,cy+1.1), (cx-0.6,cy+1.55), (cx+1.65,cy+0.5),
           (cx+1.55,cy-0.75), (cx-1.0,cy-1.4), (cx+0.6,cy-1.7)]
for x, y in nh2_pts:
    ax.text(x, y, '-NH$_2$', fontsize=7, fontweight='bold', color='#D84315', ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.12', facecolor='#FFF3E0', edgecolor='#D84315', alpha=0.9), zorder=5)

# === Callout boxes: placed CLOSE to the circles on the RIGHT ===
box_x = 7.5   # circle right edge ≈ 4.5+2.5=7.0, so box at 7.5 is only 0.5 units away
box_w = 7.5   # wide enough for text

# ---- Callout 1: Core ----
y1 = 7.2
ax.annotate('', xy=(cx+core_r, cy),  # right edge of core
            xytext=(box_x+0.1, y1+0.7),
            arrowprops=dict(arrowstyle='->', color=CORE_E, lw=1.3, connectionstyle='arc3,rad=-0.15'))
ax.text(box_x+0.4, y1+0.85, '基体：稀土铝酸盐长余辉荧光粉', fontsize=10, fontweight='bold', color='#5D4037')
ax.text(box_x+0.4, y1+0.15, '发光中心Eu$^{2+}$嵌入刚性尖晶石型铝酸盐晶格中,\n受晶格物理屏蔽保护,对过硫酸铵等强氧化性破胶体系\n具有本征化学惰性,保障全流程荧光信号完整性.',
        fontsize=8.5, color='#555555')

# ---- Callout 2: KH550 ----
y2 = 5.2
ax.annotate('', xy=(cx+kh550_r, cy),  # right edge of KH550
            xytext=(box_x+0.1, y2+0.7),
            arrowprops=dict(arrowstyle='->', color=KH550_E, lw=1.3, connectionstyle='arc3,rad=-0.1'))
ax.text(box_x+0.4, y2+0.85, '内层：硅烷偶联剂化学键合层 (KH550)', fontsize=10, fontweight='bold', color='#BF360C')
ax.text(box_x+0.4, y2+0.1, '以Si-O-Al共价键锚固于基体表面,兼具三重作用:\n'
        '① 耐水解屏障  ② 为PEG沉积提供有机界面\n'
        '③ 预置活性氨基(-NH$_2$)锚定位点 (PEG脱附后暴露)',
        fontsize=8.5, color='#555555')

# ---- Callout 3: PEG ----
y3 = 2.8
ax.annotate('', xy=(cx+peg_r, cy),  # right edge of PEG
            xytext=(box_x+0.1, y3+0.5),
            arrowprops=dict(arrowstyle='->', color=PEG_E, lw=1.3, connectionstyle='arc3,rad=-0.1'))
ax.text(box_x+0.4, y3+0.65, '外层：PEG物理屏蔽层 (PEG4000)', fontsize=10, fontweight='bold', color='#0D47A1')
ax.text(box_x+0.4, y3+0.0, '注入阶段: 提供空间位阻稳定化 → 保障分散\n'
        '关井破胶阶段: 氧化脱附降解 → 暴露内层-NH$_2$\n'
        '→ 在同一颗粒上实现"注入时屏蔽,破胶时响应脱附"',
        fontsize=8.5, color='#555555')

# === Bottom: Function switch mechanism ===
ax.add_patch(FancyBboxPatch((0.5, 0.3), 15.0, 1.3, boxstyle='round,pad=0.3',
                             facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=1.5, zorder=6))
ax.text(8.0, 1.25, '功能切换机制', fontsize=10, fontweight='bold', color='#1B5E20', ha='center', zorder=7)
ax.text(8.0, 0.7, '注入阶段(分散态): PEG外层屏蔽保护 → 关井破胶: 过硫酸铵氧化+储层温度 → PEG脱附降解 → '
        'KH550活性-NH$_2$暴露 → 静电吸引+氢键+化学缩合 → 牢固锚定于砂岩壁面(锚定态)',
        fontsize=9, color='#2E7D32', ha='center', fontstyle='italic', zorder=7)

# === Title ===
ax.text(8.0, 8.6, '图1  改性稀土铝酸盐荧光粉结构示意图', fontsize=16, fontweight='bold',
        ha='center', color='#212121')

# Save
for fmt in ['png', 'svg']:
    path = os.path.join(FIG_DIR, f'fig1_结构示意图.{fmt}')
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved: {path}")

plt.close()
print("Done: Figure 1 (redesigned)")