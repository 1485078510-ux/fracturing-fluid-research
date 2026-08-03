# -*- coding: utf-8 -*-
"""图3：压裂裂缝荧光示踪方法流程框图"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

FIG_DIR = r"荧光压裂液\figures"
os.makedirs(FIG_DIR, exist_ok=True)

fig, ax = plt.subplots(1, 1, figsize=(14, 18))
ax.set_xlim(0, 14)
ax.set_ylim(0, 18)
ax.set_aspect('auto')
ax.axis('off')

def stage_box(ax, x, y, w, h, title, title_color, bg_color, edge_color, items, note=None):
    """Draw a stage box with items."""
    # Background
    box = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.3',
                          facecolor=bg_color, edgecolor=edge_color, linewidth=2.5, zorder=2)
    ax.add_patch(box)
    # Title badge
    title_badge = FancyBboxPatch((x, y + h - 0.5), 1.4, 0.5, boxstyle='round,pad=0.1',
                                  facecolor=title_color, edgecolor=title_color, linewidth=1, zorder=3)
    ax.add_patch(title_badge)
    ax.text(x + 0.7, y + h - 0.25, title, ha='center', va='center', fontsize=11,
            fontweight='bold', color='white', zorder=4)

    # Items
    item_y = y + h - 0.85
    for i, (item_text, is_highlight) in enumerate(items):
        itm_w = min(w - 0.9, max(len(item_text) * 0.35, 5.0))
        itm_c = '#FFFFFF' if not is_highlight else '#FFF9C4'
        itm_e = edge_color if not is_highlight else '#F57F17'
        itm = FancyBboxPatch((x + 0.4, item_y - 0.35), itm_w, 0.45,
                              boxstyle='round,pad=0.08', facecolor=itm_c,
                              edgecolor=itm_e, linewidth=1.2, zorder=3)
        ax.add_patch(itm)
        ax.text(x + 0.4 + itm_w/2, item_y - 0.125, item_text, ha='center', va='center',
                fontsize=9.5, fontweight='bold' if is_highlight else 'normal',
                color='#333333', zorder=4)
        # Draw small arrow between items
        if i < len(items) - 1:
            ax.annotate('', xy=(x + 0.4 + itm_w/2, item_y - 0.45),
                        xytext=(x + 0.4 + itm_w/2, item_y - 0.7),
                        arrowprops=dict(arrowstyle='->', color=edge_color, lw=1.0))
        item_y -= 0.8

    # Note box on the right side
    if note:
        note_box = FancyBboxPatch((x + w - note['w'] - 0.3, y + 0.3), note['w'], note['h'],
                                   boxstyle='round,pad=0.15', facecolor='white',
                                   edgecolor=edge_color, linewidth=1.2, linestyle='--', zorder=3)
        ax.add_patch(note_box)
        ax.text(x + w - note['w']/2 - 0.3, y + 0.3 + note['h']/2, note['text'],
                ha='center', va='center', fontsize=8, color='#555555', zorder=4)

# Stage transition arrow
def stage_arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=2.5,
                               connectionstyle='arc3,rad=0'))

# === Title ===
ax.text(7.0, 17.5, '图3  压裂裂缝荧光示踪方法流程框图', fontsize=16, fontweight='bold',
        ha='center', color='#212121')

# === Start node ===
start = FancyBboxPatch((5.5, 16.5), 3.0, 0.6, boxstyle='round,pad=0.15',
                        facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=2)
ax.add_patch(start)
ax.text(7.0, 16.8, '压裂施工开始', ha='center', va='center', fontsize=11, fontweight='bold', color='#1B5E20')

stage_arrow(ax, 7.0, 16.5, 7.0, 15.5)

# ========== STAGE 1: 注入阶段 ==========
stage_box(ax, 0.8, 11.5, 12.4, 3.8,
          '注入阶段', '#1565C0', '#E3F2FD', '#1565C0',
          items=[
              ('荧光压裂液终液 + 支撑剂 混合', False),
              ('通过压裂泵注系统泵入目标压裂层段', False),
              ('荧光粉随携砂液运移至水力裂缝各处（分散态）', True),
          ],
          note={'w': 3.6, 'h': 1.0,
                'text': '母液添加段位：前置液段/携砂液段/顶替液段\n（优选前置液+携砂液连续添加）'})

stage_arrow(ax, 7.0, 11.5, 7.0, 10.5)

# ========== STAGE 2: 关井破胶阶段 ==========
stage_box(ax, 0.8, 6.0, 12.4, 4.3,
          '关井破胶阶段', '#E65100', '#FFF3E0', '#E65100',
          items=[
              ('停泵关井 → 储层温度 60~150°C，密闭维持 6~48 h', False),
              ('过硫酸铵热分解 → SO4.- 攻击 PEG 醚键 → 氧化链断裂', False),
              ('PEG 外层脱附降解 → 暴露 KH550 活性氨基 (-NH2)', False),
              ('-NH2 + 砂岩 Si-OH → 静电吸引/氢键/化学缩合 → 牢固锚定', True),
          ],
          note={'w': 4.2, 'h': 1.5,
                'text': '功能切换核心机制：\n① PEG牺牲响应层→氧化脱附\n② KH550活性氨基暴露\n③ 氨基与砂岩硅羟基多点协同锚定\n④ 过硫酸铵破胶剂触发(无需额外触发剂)'})

stage_arrow(ax, 7.0, 6.0, 7.0, 5.2)

# ========== STAGE 3: 返排阶段 ==========
stage_box(ax, 0.8, 2.6, 12.4, 2.4,
          '返排阶段', '#2E7D32', '#E8F5E9', '#2E7D32',
          items=[
              ('开井返排 → 携带破胶残渣及未锚定游离荧光粉排出井筒', False),
              ('已锚定荧光粉牢固保留于裂缝壁面 (净残留率 > 90%)', True),
          ],
          note={'w': 2.8, 'h': 0.6,
                'text': '动态实验：锚定率 92.7±1.8%'})

stage_arrow(ax, 7.0, 2.6, 7.0, 1.8)

# ========== STAGE 4: 取心与检测阶段 ==========
stage_box(ax, 0.8, -0.6, 12.4, 2.6,
          '取心与检测阶段', '#7B1FA2', '#F3E5F5', '#7B1FA2',
          items=[
              ('压后取心作业 → 获取含裂缝岩心', False),
              ('紫外光源 365 nm 照射 → 绿色荧光发射 (~520 nm)', False),
              ('观察/拍照记录裂缝壁面荧光分布 → 确定压裂液波及范围', True),
          ],
          note={'w': 2.8, 'h': 0.8,
                'text': '荧光分布区域 =\n压裂液实际波及范围\n(定性-半定量实物验证)'})

stage_arrow(ax, 7.0, -0.6, 7.0, -1.5)

# === End node ===
end = FancyBboxPatch((3.5, -2.2), 7.0, 0.7, boxstyle='round,pad=0.15',
                      facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=2)
ax.add_patch(end)
ax.text(7.0, -1.85, '获得压裂裂缝的可实物验证荧光标记', ha='center', va='center',
        fontsize=12, fontweight='bold', color='#1B5E20')

# === Timeline annotation on the right ===
tl_x = 13.6
ax.text(tl_x + 0.7, 16.0, '工程\n时间线', fontsize=9, fontweight='bold', color='#333333', ha='center')

timeline_stages = [
    (13.4, '#1565C0', '注入'),
    (8.2, '#E65100', '关井破胶\n(6~48 h)'),
    (3.8, '#2E7D32', '返排'),
    (0.7, '#7B1FA2', '取心检测'),
]
for y, color, label in timeline_stages:
    badge = FancyBboxPatch((tl_x, y), 1.4, 0.5, boxstyle='round,pad=0.08',
                            facecolor=color, edgecolor=color, linewidth=1)
    ax.add_patch(badge)
    ax.text(tl_x + 0.7, y + 0.25, label, ha='center', va='center', fontsize=8,
            fontweight='bold', color='white')

# Vertical line connecting timeline
ax.plot([tl_x + 0.7, tl_x + 0.7], [1.2, 15.8], color='#BDBDBD', linewidth=2, linestyle=':', zorder=1)

# Save
for fmt in ['png', 'svg']:
    path = os.path.join(FIG_DIR, f'fig3_方法流程图.{fmt}')
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved: {path}")

plt.close()
print("Done: Figure 3")