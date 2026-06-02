"""
fig_26_plate_boundary_types.py

Scientific content: Map-view schematic of the three kinematic classes of plate
boundary — divergent, convergent, transform — each defined by the orientation of
the relative-velocity vector across the boundary (away from, toward, or parallel
to the boundary). Subduction polarity (teeth) and ridge axis are shown as the
geologic expressions of the convergent and divergent cases.

Reproduces the scientific content of (original figure NOT used):
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Cambridge University Press, Ch. 2 (plate boundary classification).

Output: assets/figures/fig_26_plate_boundary_types.png
License: CC-BY 4.0 (this script)
"""
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# -- Global rcParams (MANDATORY) -------------------------------------------
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

# Colorblind-safe palette (Wong 2011 / WCAG AA)
BLUE, ORANGE, SKY, GREEN, VERM, PINK, BLACK = (
    "#0072B2", "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7", "#000000")
PLATE_L = SKY      # left plate fill
PLATE_R = ORANGE   # right plate fill
RIDGE = VERM       # ridge axis


def arrow(ax, x0, y0, x1, y1, color=BLACK, lw=3.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color,
                                mutation_scale=22))


def teeth(ax, x, y0, y1, n=6, size=0.045, point_right=True):
    """Subduction teeth along a vertical boundary at x, pointing into overriding plate."""
    ys = np.linspace(y0, y1, n + 1)
    dx = size if point_right else -size
    for i in range(n):
        ymid = 0.5 * (ys[i] + ys[i + 1])
        tri = np.array([[x, ys[i]], [x, ys[i + 1]], [x + dx, ymid]])
        ax.fill(tri[:, 0], tri[:, 1], color=BLACK, zorder=5)


fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6))

for ax in axes:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")

# ---- (a) Divergent --------------------------------------------------------
ax = axes[0]
ax.fill([0, 0.5, 0.5, 0], [0.18, 0.18, 0.82, 0.82], color=PLATE_L, alpha=0.40)
ax.fill([0.5, 1, 1, 0.5], [0.18, 0.18, 0.82, 0.82], color=PLATE_R, alpha=0.40)
ax.plot([0.5, 0.5], [0.18, 0.82], color=RIDGE, lw=5, solid_capstyle="round")
arrow(ax, 0.40, 0.50, 0.16, 0.50)
arrow(ax, 0.60, 0.50, 0.84, 0.50)
ax.text(0.25, 0.88, "Plate L", ha="center", fontsize=12)
ax.text(0.75, 0.88, "Plate R", ha="center", fontsize=12)
ax.text(0.5, 0.07, "ridge axis", ha="center", color=RIDGE, fontsize=12)
ax.set_title("(a) Divergent")
ax.text(0.5, -0.04, "plates move apart  •  new lithosphere",
        ha="center", va="top", fontsize=11.5)

# ---- (b) Convergent -------------------------------------------------------
ax = axes[1]
ax.fill([0, 0.5, 0.5, 0], [0.18, 0.18, 0.82, 0.82], color=PLATE_L, alpha=0.40)
ax.fill([0.5, 1, 1, 0.5], [0.18, 0.18, 0.82, 0.82], color=PLATE_R, alpha=0.40)
ax.plot([0.5, 0.5], [0.18, 0.82], color=BLACK, lw=2)
teeth(ax, 0.5, 0.22, 0.78, n=6, point_right=True)  # right plate overrides
arrow(ax, 0.30, 0.50, 0.46, 0.50)
arrow(ax, 0.84, 0.50, 0.66, 0.50)
ax.text(0.22, 0.88, "subducting", ha="center", fontsize=12)
ax.text(0.78, 0.88, "overriding", ha="center", fontsize=12)
ax.set_title("(b) Convergent")
ax.text(0.5, -0.04, "plates move together  •  lithosphere consumed",
        ha="center", va="top", fontsize=11.5)

# ---- (c) Transform --------------------------------------------------------
ax = axes[2]
ax.fill([0, 0.5, 0.5, 0], [0.18, 0.18, 0.82, 0.82], color=PLATE_L, alpha=0.40)
ax.fill([0.5, 1, 1, 0.5], [0.18, 0.18, 0.82, 0.82], color=PLATE_R, alpha=0.40)
ax.plot([0.5, 0.5], [0.18, 0.82], color=BLACK, lw=3)
arrow(ax, 0.36, 0.34, 0.36, 0.70)   # left plate up
arrow(ax, 0.64, 0.66, 0.64, 0.30)   # right plate down
ax.text(0.25, 0.88, "Plate L", ha="center", fontsize=12)
ax.text(0.75, 0.88, "Plate R", ha="center", fontsize=12)
ax.set_title("(c) Transform")
ax.text(0.5, -0.04, "plates slide past  •  lithosphere conserved",
        ha="center", va="top", fontsize=11.5)

fig.suptitle("Three kinematic classes of plate boundary (map view)",
             fontsize=17, y=1.02)
fig.tight_layout()
out = "../figures/fig_26_plate_boundary_types.png"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")
