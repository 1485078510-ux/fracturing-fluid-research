"""
绘制 水力裂缝与天然裂缝三种相互作用模式示意图 (真实感版)
按照真实岩石力学机理绘制，无穿模。
- 天然裂缝在交互处有明显张开/扩张
- 水力裂缝尖端形态真实 (钝化/偏转/重新起裂)
- 流体在裂缝中的填充效果
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import Arc, FancyBboxPatch
from matplotlib.lines import Line2D
from scipy.ndimage import gaussian_filter

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
np.random.seed(42)

# ================================================================
# 1. 岩石背景
# ================================================================
def generate_rock_bg(width=800, height=320):
    """层理 + 矿物斑块 + 颗粒纹理 — 安全广播"""
    yy, xx = np.mgrid[0:height, 0:width] / width

    def safe_repeat(arr, factor, target_h, target_w):
        """重复数组并严格裁剪到目标尺寸"""
        out = np.repeat(np.repeat(arr, factor, axis=0), factor, axis=1)
        out = out[:target_h, :target_w]
        return out

    # 多尺度噪声 — 使用整除因子
    n0 = safe_repeat(np.random.rand(height // 25 + 1, width // 25 + 1), 25, height, width)
    n1 = safe_repeat(np.random.rand(height // 10 + 1, width // 10 + 1), 10, height, width)
    n2 = safe_repeat(np.random.rand(height // 3 + 1, width // 3 + 1), 3, height, width)

    # 水平层理
    y_norm = yy * height / width
    bedding = np.sin(y_norm * 16 + np.sin(xx * np.pi * 4) * 3) * 0.35
    bedding += np.sin(y_norm * 32 + 1.5) * 0.12

    tex = n0 * 0.35 + n1 * 0.25 + n2 * 0.15 + (bedding + 0.5) * 0.25
    tex = (tex - tex.min()) / (tex.max() - tex.min())

    # 微孔隙
    pores = np.random.rand(height, width) > 0.992
    tex = tex * (1 - gaussian_filter(pores.astype(float), sigma=0.7) * 0.55)
    return np.clip(tex, 0, 1)


# ================================================================
# 2. 天然裂缝 — 弱面，关键在交互处有明显张开
# ================================================================
def draw_natural_fracture(ax, x0, x1, y_center, width=0.06, z0=1, seed=0):
    """
    绘制天然裂缝弱面。基础宽度较窄 (闭合状态)，
    在交互段可以被水力裂缝流体扩张。
    返回：裂缝的top/bottom/mid y坐标供水力裂缝交互使用。
    """
    rng = np.random.RandomState(42 + seed)
    n_pts = 80
    xs = np.linspace(x0, x1, n_pts)

    # 不规则边界波动
    phase_t = seed * 1.7
    phase_b = seed * 1.7 + 1.2
    yt = (np.full(n_pts, y_center + width / 2) +
          np.sin(np.linspace(phase_t, 5.5 * np.pi + phase_t, n_pts)) * 0.009 +
          np.sin(np.linspace(phase_t, 15 * np.pi + phase_t, n_pts)) * 0.004 +
          rng.randn(n_pts) * 0.0025)
    yb = (np.full(n_pts, y_center - width / 2) +
          np.sin(np.linspace(phase_b, 5.5 * np.pi + phase_b, n_pts)) * 0.009 +
          np.sin(np.linspace(phase_b, 15 * np.pi + phase_b, n_pts)) * 0.004 +
          rng.randn(n_pts) * 0.0025)

    verts = list(zip(xs, yt)) + list(zip(xs[::-1], yb[::-1]))

    # 阴影
    sv = [(x + 0.006, y - 0.004) for x, y in verts]
    ax.add_patch(patches.Polygon(sv, closed=True, fill=True,
                                  color='black', alpha=0.06, zorder=z0, linewidth=0))

    # NF 主体 (暖灰，充填矿物)
    ax.add_patch(patches.Polygon(verts, closed=True, fill=True,
                                  facecolor='#E3DBD2', edgecolor='#B5ADA2',
                                  linewidth=0.5, alpha=0.85, zorder=z0 + 1))

    # 内部层理细线
    for j in range(1, 4):
        frac_y = y_center - width / 2 + j * width / 4
        ax.plot(xs, np.full(n_pts, frac_y),
                color='#C8BFB5', linewidth=0.25, alpha=0.5, zorder=z0 + 2)

    return y_center + width / 2, y_center - width / 2, y_center  # top, bot, mid


# ================================================================
# 3. 水力裂缝 — 有机变宽度 + 尖端形态
# ================================================================
def make_wavy_edges(x0, y0, x1, y1, base_width, n_pts=100, seed=0):
    """生成裂缝左右边缘坐标。返回 (left_xy), (right_xy), (center_xy)"""
    rng = np.random.RandomState(42 + seed)
    t = np.linspace(0, 1, n_pts)
    cx = x0 + (x1 - x0) * t
    cy = y0 + (y1 - y0) * t
    dx, dy = x1 - x0, y1 - y0
    L = np.hypot(dx, dy)
    if L < 0.001:
        return None, None, None
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux

    # 宽度包络：两端尖 (0.08倍宽)，中间宽
    w_env = 1.0 - (2 * t - 1) ** 2
    w_env = np.clip(w_env, 0.08, 1.0)
    w = base_width * w_env

    # 壁面波动
    wb_L = (np.sin(t * 14.3 + 0.4 * seed) * 0.42 +
            np.sin(t * 28.7 + 1.9 * seed) * 0.27 +
            np.sin(t * 43.2 + 3.3 * seed) * 0.14 +
            np.sin(t * 56.5 + 1.1 * seed) * 0.07 +
            rng.randn(n_pts) * 0.035) * base_width * 0.7
    wb_R = (np.sin(t * 13.5 + 0.9 * seed) * 0.42 +
            np.sin(t * 27.1 + 2.3 * seed) * 0.27 +
            np.sin(t * 44.8 + 3.7 * seed) * 0.14 +
            np.sin(t * 55.2 + 1.6 * seed) * 0.07 +
            rng.randn(n_pts) * 0.035) * base_width * 0.7

    hw = w / 2
    lx = cx + (wb_L - hw) * nx
    ly = cy + (wb_L - hw) * ny
    rx = cx + (wb_R + hw) * nx
    ry = cy + (wb_R + hw) * ny

    return (lx, ly), (rx, ry), (cx, cy)


def draw_hf_segment(ax, x0, y0, x1, y1, width, seed=0, z0=10):
    """绘制水力裂缝段: 简洁条带状，仅一层填充 + 细边线"""
    L, R, C = make_wavy_edges(x0, y0, x1, y1, width, seed=seed)
    if L is None:
        return None

    lx, ly = L
    rx, ry = R
    poly = list(zip(lx, ly)) + list(zip(rx[::-1], ry[::-1]))

    # 主体填充
    ax.add_patch(patches.Polygon(poly, closed=True, fill=True,
                                  facecolor='#1B6CB5', alpha=0.85,
                                  zorder=z0, linewidth=0))
    # 细边线
    ax.add_patch(patches.Polygon(poly, closed=True, fill=False,
                                  edgecolor='#0B3D66', linewidth=0.5,
                                  alpha=0.55, zorder=z0 + 1))
    return C


def draw_hf_tip(ax, tip_x, tip_y, width, z0=10):
    """水力裂缝尖端: 小圆点标记停止位置"""
    ax.plot([tip_x], [tip_y], 'o', color='#1B6CB5',
            markersize=width * 4, alpha=0.7,
            zorder=z0, markeredgecolor='#0B3D66', markeredgewidth=0.4)


def draw_nf_dilation(ax, x_center, y_center, nf_half_w, dilate_region, dilate_factor,
                     z0=8):
    """
    NF在交互处轻微扩张，仅呈现条状裂缝宽度变化，避免三角形膨胀。
    dilate_factor: 0=无变化, 0.3=轻微张开, 0.6=中等张开
    """
    x_left, x_right = dilate_region
    n_pts = 80
    xs = np.linspace(x_left - 0.01, x_right + 0.01, n_pts)

    # 平顶钟形 — 在交互中心附近保持均宽，远处快速衰减
    dist_from_center = np.abs(xs - x_center)
    half_span = (x_right - x_left) / 2 + 0.01
    # 使用更平缓的包络
    dilate_envelope = np.exp(-(dist_from_center ** 3) / (2 * (half_span / 2.0) ** 3))
    dilate_envelope = np.clip(dilate_envelope, 0.02, 1.0) * dilate_factor

    # 额外张开量 — 控制在较小的条状范围
    extra = nf_half_w * 0.35 * dilate_envelope

    phase = np.linspace(0, 5.5 * np.pi, n_pts)
    yt = np.full(n_pts, y_center + nf_half_w) + np.sin(phase) * 0.006 + extra
    yb = np.full(n_pts, y_center - nf_half_w) - np.sin(phase + 1.2) * 0.006 - extra

    verts = list(zip(xs, yt)) + list(zip(xs[::-1], yb[::-1]))

    # 轻微蓝色充填
    ax.add_patch(patches.Polygon(verts, closed=True, fill=True,
                                  facecolor='#1B6CB5', alpha=0.13 * dilate_factor,
                                  zorder=z0, linewidth=0))
    ax.add_patch(patches.Polygon(verts, closed=True, fill=False,
                                  edgecolor='#1B6CB5', linewidth=0.5 * dilate_factor,
                                  alpha=0.35 * dilate_factor, zorder=z0 + 1))


# ================================================================
# 4. 辅助元素
# ================================================================
STRESS_COLOR = '#CB181D'
STRESS_H_COLOR = '#E65933'
ANGLE_COLOR = '#1B7837'
HF_COLOR = '#1B6CB5'
BG_COLOR = '#F5F2EC'
TEXT_DARK = '#2C2C2C'


def stress_arrow(ax, x, y, dx, dy, label, color, fs=9):
    ax.annotate('', xy=(x + dx, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', lw=2.0, color=color), zorder=20)
    ax.text(x + dx * 0.55, y + dy * 0.55, label,
            fontsize=fs, color=color, fontweight='bold',
            ha='center', va='center',
            bbox=dict(facecolor='white', alpha=0.82, edgecolor='none',
                      boxstyle='round,pad=0.15'))


def angle_arc(ax, center, rad, t1, t2, label, fs=10):
    arc = Arc(center, 2 * rad, 2 * rad, angle=0,
              theta1=t1, theta2=t2, color=ANGLE_COLOR, lw=2.0, zorder=18)
    ax.add_patch(arc)
    ma = np.radians((t1 + t2) / 2)
    ax.text(center[0] + (rad + 0.11) * np.cos(ma),
            center[1] + (rad + 0.11) * np.sin(ma),
            label, fontsize=fs, color=ANGLE_COLOR, fontweight='bold',
            ha='center', va='center')


# ================================================================
# 5. 主绘图
# ================================================================
fig, axes = plt.subplots(1, 3, figsize=(19, 5.5))
plt.subplots_adjust(wspace=0.05, left=0.03, right=0.98, top=0.85, bottom=0.15)

texture = generate_rock_bg()

panel_titles = [
    r'(a) 穿过 — HF穿越NF继续扩展',
    r'(b) 止裂 — HF被NF捕获停止扩展',
    r'(c) 转向 — HF沿NF转向形成复杂缝网',
]
panel_notes = [
    '高逼近角 (60°~90°)  |  高应力差  |  NF强胶结',
    '中等逼近角 (30°~60°)  |  NF弱胶结 / 大开度',
    '低逼近角 (<30°)  |  低应力差  |  NF弱面 / 压裂液沿NF分流',
]
angle_data = [(15, 88, r'$\theta \approx 85^\circ$'),
              (15, 45, r'$\theta \approx 45^\circ$'),
              (15, 28, r'$\theta \approx 20^\circ$')]

for i, ax in enumerate(axes):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(BG_COLOR)
    ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])

    # 岩石背景
    ax.imshow(texture, extent=[0, 1, 0, 1], cmap='YlOrBr',
              alpha=0.58, zorder=0, aspect='auto')

    # --- 天然裂缝 ---
    nf_y = 0.64
    nf_hw = 0.04  # 半宽 (闭合状态)
    nf_top, nf_bot, nf_mid = draw_natural_fracture(
        ax, 0.04, 0.96, nf_y, width=nf_hw * 2, z0=1, seed=10 + i)

    # NF 标签
    ax.annotate('天然裂缝 (NF)', xy=(0.12, nf_y + nf_hw + 0.06),
                fontsize=11, color='#6B6258', fontweight='bold',
                ha='center', va='bottom', zorder=22)

    # --- 水力裂缝交互模式 ---
    hf_cx = 0.5
    hf_w = 0.10

    if i == 0:  # ===== (a) 穿过 =====
        # NF在交叉处轻微张开
        draw_nf_dilation(ax, hf_cx, nf_y, nf_hw,
                         dilate_region=(0.43, 0.57), dilate_factor=0.25, z0=5)

        draw_hf_segment(ax, hf_cx, 0.06, hf_cx, nf_bot, hf_w, seed=0, z0=10)
        draw_hf_tip(ax, hf_cx, nf_bot, hf_w, z0=12)

        draw_hf_segment(ax, hf_cx - 0.012, nf_top, hf_cx - 0.005, 0.97, hf_w,
                        seed=1, z0=10)
        ax.plot([hf_cx - 0.008], [nf_top], 'o', color='#5BB5ED',
                markersize=hf_w * 2.5, alpha=0.5, zorder=14,
                markeredgecolor='#1B6CB5', markeredgewidth=0.4)

        # NF 交叉处微弱蓝色 (窄条)
        ax.fill_between([hf_cx - 0.055, hf_cx + 0.055],
                         [nf_bot + 0.001, nf_bot + 0.001],
                         [nf_top - 0.001, nf_top - 0.001],
                         color='#5BB5ED', alpha=0.12, linewidth=0, zorder=7)

    elif i == 1:  # ===== (b) 止裂 =====
        draw_hf_segment(ax, hf_cx, 0.06, hf_cx, nf_bot, hf_w, seed=2, z0=10)
        draw_hf_tip(ax, hf_cx, nf_bot, hf_w, z0=12)

        # NF交互区轻微扩张
        draw_nf_dilation(ax, hf_cx, nf_y, nf_hw,
                         dilate_region=(0.38, 0.62), dilate_factor=0.45, z0=5)

        # 窄条状流体充填 (模拟压裂液进入NF形成的薄层)
        span = 0.10
        xs_b = np.linspace(hf_cx - span, hf_cx + span, 40)
        for k in range(1, 4):
            f = k / 4
            y_mid = nf_bot + f * nf_hw * 2
            ax.fill_between(xs_b,
                            np.full_like(xs_b, y_mid - 0.004),
                            np.full_like(xs_b, y_mid + 0.004),
                            color='#5BB5ED', alpha=0.22, linewidth=0, zorder=9)

        ax.annotate('止裂', xy=(hf_cx, nf_bot - 0.02),
                    fontsize=9, color=HF_COLOR, fontweight='bold',
                    ha='center', va='top', zorder=20,
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor=HF_COLOR,
                              linewidth=0.5, boxstyle='round,pad=0.15'))

    elif i == 2:  # ===== (c) 转向 =====
        # 中央交互区轻微扩张
        draw_nf_dilation(ax, hf_cx, nf_y, nf_hw,
                         dilate_region=(0.32, 0.68), dilate_factor=0.40, z0=5)

        # HF竖直段: 从底部延伸到NF中点
        draw_hf_segment(ax, hf_cx, 0.06, hf_cx, nf_mid, hf_w, seed=3, z0=10)
        draw_hf_tip(ax, hf_cx, nf_mid, hf_w, z0=12)

        # --- 左翼: 窄条状裂缝充填 (压裂液沿NF向左) ---
        draw_nf_dilation(ax, 0.28, nf_y, nf_hw,
                         dilate_region=(0.08, 0.48), dilate_factor=0.35, z0=5)
        xn_L = np.linspace(0.08, hf_cx, 40)
        for k in range(1, 4):
            f = k / 4
            y_mid = nf_mid - nf_hw + f * nf_hw * 2
            ax.fill_between(xn_L,
                            np.full_like(xn_L, y_mid - 0.003),
                            np.full_like(xn_L, y_mid + 0.003),
                            color='#5BB5ED', alpha=0.20, linewidth=0, zorder=9)

        # --- 右翼: 窄条状裂缝充填 (压裂液沿NF向右) ---
        draw_nf_dilation(ax, 0.72, nf_y, nf_hw,
                         dilate_region=(0.52, 0.92), dilate_factor=0.35, z0=5)
        xn_R = np.linspace(hf_cx, 0.92, 40)
        for k in range(1, 4):
            f = k / 4
            y_mid = nf_mid - nf_hw + f * nf_hw * 2
            ax.fill_between(xn_R,
                            np.full_like(xn_R, y_mid - 0.003),
                            np.full_like(xn_R, y_mid + 0.003),
                            color='#5BB5ED', alpha=0.20, linewidth=0, zorder=9)

        # 转向标记
        ax.annotate('转向', xy=(hf_cx + 0.07, nf_mid + 0.04),
                    fontsize=9, color=HF_COLOR, fontweight='bold',
                    ha='left', va='bottom', zorder=20)
        ax.annotate('转向', xy=(hf_cx - 0.07, nf_mid + 0.04),
                    fontsize=9, color=HF_COLOR, fontweight='bold',
                    ha='right', va='bottom', zorder=20)

    # --- 应力箭头 ---
    stress_arrow(ax, 0.70, 0.06, 0.18, 0, r'$\mathbf{\sigma_H}$',
                 STRESS_COLOR, fs=9)
    stress_arrow(ax, 0.88, 0.28, 0, -0.16, r'$\mathbf{\sigma_h}$',
                 STRESS_H_COLOR, fs=9)

    # --- 逼近角弧线 ---
    t1, t2, tl = angle_data[i]
    angle_arc(ax, (0.5, nf_mid), 0.20, t1, t2, tl, fs=10)

    # --- HF标签 ---
    ax.text(0.31, 0.23, '水力裂缝 (HF)',
            fontsize=10, color=HF_COLOR, fontweight='bold',
            ha='center', va='center', zorder=25,
            bbox=dict(facecolor='white', alpha=0.88, edgecolor=HF_COLOR,
                      linewidth=0.7, boxstyle='round,pad=0.25'))

    # --- 条件说明 ---
    ax.text(0.5, -0.07, panel_notes[i], fontsize=11, color='#666666',
            ha='center', va='top', style='italic', zorder=10)

    # --- 标题 ---
    ax.set_title(panel_titles[i], fontsize=14, fontweight='bold',
                 color=TEXT_DARK, pad=8)

    # --- 细框 ---
    for sp in ax.spines.values():
        sp.set_visible(True); sp.set_color('#CCCCCC'); sp.set_linewidth(0.5)

# --- 总标题 ---
fig.suptitle('图4  水力裂缝与天然裂缝三种相互作用模式示意图',
             fontsize=17, fontweight='bold', color='#111111', y=0.99)

# --- 图例 ---
legend_elements = [
    patches.Patch(facecolor=HF_COLOR, edgecolor='#0B3D66', label='水力裂缝 (HF)'),
    patches.Patch(facecolor='#E3DBD2', edgecolor='#B5ADA2', label='天然裂缝 (NF)'),
    Line2D([0], [0], color=STRESS_COLOR, lw=2.5, label=r'$\sigma_H$ (最大水平主应力)'),
    Line2D([0], [0], color=STRESS_H_COLOR, lw=2.5, label=r'$\sigma_h$ (最小水平主应力)'),
]
fig.legend(handles=legend_elements, loc='upper center', ncol=4,
           fontsize=9, frameon=True, edgecolor='#DDDDDD',
           bbox_to_anchor=(0.5, 0.93))

# --- 保存 ---
png_path = r'c:\Users\郝\Desktop\claude\向晶\Figure_4_HF_NF_Interaction.png'
svg_path = r'c:\Users\郝\Desktop\claude\向晶\Figure_4_HF_NF_Interaction.svg'
fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
fig.savefig(svg_path, format='svg', bbox_inches='tight', facecolor='white', edgecolor='none')
print(f'PNG: {png_path}')
print(f'SVG: {svg_path}')
plt.close()
