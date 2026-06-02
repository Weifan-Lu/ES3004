"""
fig_26_ridge_transform_fz.py

Scientific content: The ridge-transform-fracture-zone geometry. Two ridge
segments (X' and Y') are offset along a line W-X-Y-Z. The segment X-Y BETWEEN
the ridge tips is an active transform fault: the two plates move in OPPOSITE
directions across it, so it is seismically active. The outboard segments W-X and
Y-Z are fossil fracture zones: crust on both sides belongs to the same plate and
moves in the same direction, so they are aseismic topographic scars. The sense of
relative motion on the transform is OPPOSITE to the apparent offset of the ridge
— the classic Wilson (1965) transform-fault insight.

Reproduces the scientific content of (original figure NOT used):
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Cambridge University Press, Ch. 2 (transform faults and fracture zones).

Output: assets/figures/fig_26_ridge_transform_fz.png
License: CC-BY 4.0 (this script)
"""
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 16,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

BLUE, ORANGE, SKY, GREEN, VERM, PINK, BLACK = (
    "#0072B2", "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7", "#000000")
PLATE_B = SKY
PLATE_A = ORANGE


def arrow(ax, x0, y0, x1, y1, color=BLACK, lw=3.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color,
                                mutation_scale=20))


fig, ax = plt.subplots(figsize=(10.5, 6.4))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("auto")
ax.axis("off")

W, X, Y, Z = 0.06, 0.35, 0.65, 0.94
yline = 0.50

# Plate B (left of the stepped boundary): blue
B_poly = [(W, 0.95), (X, 0.95), (X, yline), (Y, yline), (Y, 0.05), (W, 0.05)]
# Plate A (right of the stepped boundary): orange
A_poly = [(X, 0.95), (Z, 0.95), (Z, 0.05), (Y, 0.05), (Y, yline), (X, yline)]
ax.add_patch(plt.Polygon(B_poly, closed=True, facecolor=PLATE_B, alpha=0.38,
                         edgecolor="none"))
ax.add_patch(plt.Polygon(A_poly, closed=True, facecolor=PLATE_A, alpha=0.38,
                         edgecolor="none"))

# Ridge segments (red, thick): upper at X, lower at Y
ax.plot([X, X], [yline, 0.95], color=VERM, lw=6, solid_capstyle="round", zorder=4)
ax.plot([Y, Y], [0.05, yline], color=VERM, lw=6, solid_capstyle="round", zorder=4)

# Active transform segment X-Y (bold black on the line)
ax.plot([X, Y], [yline, yline], color=BLACK, lw=4, zorder=4)
# Fossil fracture zones W-X and Y-Z (thin dashed)
ax.plot([W, X], [yline, yline], color=BLACK, lw=1.4, ls=(0, (6, 4)), zorder=3)
ax.plot([Y, Z], [yline, yline], color=BLACK, lw=1.4, ls=(0, (6, 4)), zorder=3)

# Relative-motion arrows: Plate B -> left, Plate A -> right
arrow(ax, 0.26, 0.74, 0.13, 0.74)   # B upper
arrow(ax, 0.30, 0.26, 0.17, 0.26)   # B lower
arrow(ax, 0.48, 0.74, 0.61, 0.74)   # A upper
arrow(ax, 0.74, 0.26, 0.87, 0.26)   # A lower

# Earthquake stars on the active transform only
xs = np.linspace(X + 0.04, Y - 0.04, 4)
ax.scatter(xs, [yline] * 4, marker="*", s=240, color=VERM,
           edgecolor=BLACK, lw=0.6, zorder=6)

# Labels
ax.text(0.19, 0.86, "Plate B", ha="center", fontsize=13)
ax.text(0.78, 0.86, "Plate A", ha="center", fontsize=13)
ax.text(X, 0.985, "X'  (ridge)", ha="center", color=VERM, fontsize=12)
ax.text(Y, 0.005, "Y'  (ridge)", ha="center", va="bottom", color=VERM, fontsize=12)
for px, lab in [(W, "W"), (X, "X"), (Y, "Y"), (Z, "Z")]:
    ax.text(px, yline - 0.045, lab, ha="center", va="top", fontsize=12.5,
            fontweight="bold")

ax.annotate("active transform\n(opposite motion — earthquakes)",
            xy=(0.50, yline), xytext=(0.50, 0.30),
            ha="center", color=VERM, fontsize=12.5, fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=VERM, lw=2))
ax.text((W + X) / 2, yline + 0.05, "fracture zone\n(same motion — aseismic)",
        ha="center", fontsize=11.5)
ax.text((Y + Z) / 2, yline + 0.05, "fracture zone\n(same motion — aseismic)",
        ha="center", fontsize=11.5)

ax.set_title("Ridge–transform–fracture zone: only the segment between the "
             "ridge tips is active", fontsize=14.5)
fig.tight_layout()
out = "../figures/fig_26_ridge_transform_fz.png"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")
