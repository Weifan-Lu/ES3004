"""
fig_28_chilean_mariana.py  -> SF2_chilean_mariana.png

Scientific content: The two end-member subduction modes of Uyeda & Kanamori
(1979). Chilean-type (left): a young, buoyant slab subducts at a shallow angle,
strongly coupled to the overriding plate, driving back-arc SHORTENING and a high
Andean arc; great (M9) earthquakes occur. Mariana-type (right): an old, dense
slab sinks near-vertically, weakly coupled, with trench rollback driving back-arc
EXTENSION (active back-arc spreading); no great earthquakes. The contrast is the
classic "dynamic" classification of convergent margins.

Reproduces the scientific content of (original figure NOT used):
  Uyeda, S. & Kanamori, H. (1979). Back-arc opening and the mode of subduction.
  J. Geophys. Res. 84, 1049-1061, doi:10.1029/JB084iB03p01049.

Output: assets/figures/SF2_chilean_mariana.png
License: CC-BY 4.0 (this script)
"""
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 12,
    "figure.dpi": 150, "savefig.dpi": 300,
})

BLUE, ORANGE, SKY, GREEN, VERM, PINK, BLACK = (
    "#0072B2", "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7", "#000000")
MANTLE = "#f0e6d2"
SLAB = BLUE
UPLATE = "#cbb89d"


def arrow(ax, x0, y0, x1, y1, color=BLACK, lw=2.6, scale=18):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color,
                                mutation_scale=scale))


def draw_margin(ax, dip_deg, title, mode_label, backarc, arc_h, sub_age, rate,
                couple_text, arc_gap):
    ax.set_xlim(0, 10)
    ax.set_ylim(-300, 90)
    ax.set_aspect(0.012)
    # mantle wedge background
    ax.add_patch(plt.Rectangle((0, -300), 10, 300, facecolor=MANTLE, zorder=0))
    # ocean
    ax.add_patch(plt.Rectangle((0, 0), 10, 12, facecolor=SKY, alpha=0.5, zorder=0))

    # overriding plate (right side), top at z=0
    trench_x = 3.0
    ax.fill([trench_x, 10, 10, trench_x + 0.6],
            [0, 0, -40, -5], facecolor=UPLATE, edgecolor=BLACK, lw=1.0, zorder=3)

    # subducting slab: incoming horizontal segment + dipping segment
    dip = np.radians(dip_deg)
    L = 360.0  # slab length (km) along dip
    # incoming oceanic plate (left of trench), 8 km thick lithosphere drawn thick
    ax.fill([0, trench_x, trench_x, 0], [-8, -8, -95, -95],
            facecolor=SLAB, edgecolor=BLACK, lw=1.0, zorder=2)
    # dipping slab as a thick band
    x0, z0 = trench_x, -8
    dxg, dzg = np.cos(dip), -np.sin(dip)
    # plate thickness 95 km perpendicular offset
    th = 95.0
    nx, nz = -np.sin(dip), -np.cos(dip)  # downward normal
    sx = x0 / 1.0
    # build slab polygon in (x[0-10], z[km]) — x scaled: 1 x-unit ~ 60 km horiz
    XKM = 60.0  # km per x-unit
    top = np.array([[x0, z0],
                    [x0 + (L*dxg)/XKM, z0 + L*dzg]])
    bot = np.array([[x0 + (th*nx)/XKM, z0 + th*nz],
                    [x0 + (L*dxg + th*nx)/XKM, z0 + L*dzg + th*nz]])
    poly = np.vstack([top, bot[::-1]])
    ax.add_patch(plt.Polygon(poly, closed=True, facecolor=SLAB,
                             edgecolor=BLACK, lw=1.0, zorder=2))

    # convergence arrow (incoming plate)
    arrow(ax, 0.9, -28, 2.4, -28, color=BLACK, lw=3, scale=20)
    ax.text(1.65, -52, f"{rate} mm/yr", ha="center", fontsize=10.5)

    # trench marker
    ax.plot([trench_x], [2], marker="v", ms=12, color=BLACK, zorder=5)
    ax.text(trench_x, 22, "trench", ha="center", fontsize=11)

    # volcanic arc — trench-arc gap scales inversely with dip (shallow dip => wider)
    arc_x = trench_x + arc_gap
    ax.fill([arc_x - 0.4, arc_x, arc_x + 0.4], [0, arc_h, 0],
            facecolor=VERM, edgecolor=BLACK, zorder=4)
    ax.text(arc_x, arc_h + 12, "arc", ha="center", fontsize=11, color=VERM)

    # back-arc strain arrows
    bx = arc_x + 2.2
    if backarc == "extension":
        arrow(ax, bx - 0.3, 35, bx - 1.3, 35, color=GREEN, scale=16)
        arrow(ax, bx + 0.3, 35, bx + 1.3, 35, color=GREEN, scale=16)
        ax.text(bx, 55, "back-arc\nEXTENSION", ha="center", color=GREEN,
                fontsize=11, fontweight="bold")
    else:
        arrow(ax, bx - 1.3, 35, bx - 0.3, 35, color=VERM, scale=16)
        arrow(ax, bx + 1.3, 35, bx + 0.3, 35, color=VERM, scale=16)
        ax.text(bx, 55, "back-arc\nSHORTENING", ha="center", color=VERM,
                fontsize=11, fontweight="bold")

    # coupling annotation near interface
    ax.text(trench_x + 0.4, -120, couple_text, fontsize=11, fontweight="bold",
            rotation=0, color=BLACK,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.8))

    # incoming-age label
    ax.text(0.9, -110, f"incoming\nplate age\n~{sub_age} Ma", ha="center",
            fontsize=10.5)

    ax.set_title(f"{title}\n({mode_label})", fontsize=14)
    ax.set_ylabel("depth (km)")
    ax.set_yticks([0, -100, -200, -300])
    ax.set_yticklabels([0, 100, 200, 300])
    ax.set_xticks([])
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)


fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.5, 6.2))
draw_margin(axL, dip_deg=25, title="Chilean type",
            mode_label="young, buoyant slab — strong coupling",
            backarc="shortening", arc_h=55, sub_age="35", rate="70",
            couple_text="strong\ncoupling\n→ M9", arc_gap=3.4)
draw_margin(axR, dip_deg=70, title="Mariana type",
            mode_label="old, dense slab — weak coupling",
            backarc="extension", arc_h=35, sub_age="150", rate="30",
            couple_text="weak\ncoupling\n→ no great EQ", arc_gap=2.0)

fig.suptitle("Two end-member modes of subduction (Uyeda & Kanamori 1979)",
             fontsize=16, y=1.00)
fig.tight_layout()
out = "../figures/SF2_chilean_mariana.png"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")
