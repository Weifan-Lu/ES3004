"""
fig_26_circuit_closure.py

Scientific content: A three-plate (triple-junction) circuit-closure example in the
transform-transform-trench (FFT) configuration. Plate A meets Plate B and Plate C
along two transform boundaries; Plates B and C meet along a convergent boundary
(trench). The relative velocity is known on the two transforms and unknown across
the trench. Because each plate is rigid, the relative velocities close:
    _B v_C = _B v_A + _A v_C.
With the two transform rates 4 and 3 at right angles, the convergence across the
trench has magnitude 5 (a 3-4-5 triangle). Circuit closure is the standard tool
for recovering relative motion across convergent boundaries, where the spreading
record that would otherwise give the rate has been destroyed by subduction.

Real-world archetype: the Mendocino Triple Junction off Cape Mendocino, California
(Pacific - Juan de Fuca - North America): San Andreas (transform) + Mendocino
Fracture Zone (transform) + Cascadia subduction (trench).

Reproduces the scientific content of (original figure NOT used; reconfigured from
a ridge-transform-trench to a transform-transform-trench junction):
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Cambridge University Press, Ch. 2 (vector addition of plate velocities,
  three-plate circuits, triple junctions).

Output: assets/figures/fig_26_circuit_closure.png
License: CC-BY 4.0 (this script)
"""
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 15,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

BLUE, ORANGE, SKY, GREEN, VERM, PINK, BLACK = (
    "#0072B2", "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7", "#000000")


def varrow(ax, p0, p1, color=BLACK, lw=3.2, scale=22):
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color,
                                mutation_scale=scale))


def teeth(ax, p0, p1, normal, n=5, size=0.11, t0=0.18, t1=0.92):
    """Subduction teeth along segment p0->p1, apex offset along unit `normal`."""
    p0, p1, normal = map(np.asarray, (p0, p1, normal))
    for t in np.linspace(t0, t1, n):
        base_c = p0 + t * (p1 - p0)
        d = (p1 - p0)
        half = 0.045 * d / np.hypot(*d)
        b1, b2 = base_c - half, base_c + half
        apex = base_c + size * normal
        ax.fill([b1[0], b2[0], apex[0]], [b1[1], b2[1], apex[1]],
                color=BLACK, zorder=6)


fig, (axa, axb) = plt.subplots(1, 2, figsize=(12.8, 5.7))

# ===== Panel (a): transform-transform-trench triple junction ===============
axa.set_xlim(-1.18, 1.18)
axa.set_ylim(-1.18, 1.18)
axa.set_aspect("equal")
axa.axis("off")

O = (0, 0)
e_AB = (-1.0, 0.0)        # A-B transform ray (west)
e_AC = (0.0, -1.0)        # A-C transform ray (south)
e_BC = (0.75, 1.0)        # B-C trench ray (NE), dir (0.6, 0.8)

# Plate sectors
A_poly = [(0, 0), (-1, 0), (-1, -1), (0, -1)]                 # SW  -> A
B_poly = [(0, 0), (0.75, 1), (-1, 1), (-1, 0)]                # NW  -> B
C_poly = [(0, 0), (0, -1), (1, -1), (1, 1), (0.75, 1)]        # E   -> C
axa.add_patch(plt.Polygon(A_poly, facecolor=SKY, alpha=0.38, edgecolor="none"))
axa.add_patch(plt.Polygon(B_poly, facecolor=ORANGE, alpha=0.38, edgecolor="none"))
axa.add_patch(plt.Polygon(C_poly, facecolor=GREEN, alpha=0.30, edgecolor="none"))

# Boundaries
for e in (e_AB, e_AC, e_BC):
    axa.plot([0, e[0]], [0, e[1]], color=BLACK, lw=2.4, zorder=4)
# Trench teeth on B-C, apex toward Plate B (NW normal of dir (0.6,0.8) = (-0.8,0.6))
teeth(axa, O, e_BC, normal=(-0.8, 0.6), n=5, size=0.12)

# Plate labels
axa.text(-0.52, -0.52, "A", ha="center", va="center", fontsize=20, fontweight="bold")
axa.text(-0.42, 0.60, "B", ha="center", va="center", fontsize=20, fontweight="bold")
axa.text(0.58, -0.30, "C", ha="center", va="center", fontsize=20, fontweight="bold")

# Transform A-B (horizontal, west): B side (above) -> east, A side (below) -> west
varrow(axa, (-0.72, 0.10), (-0.45, 0.10), color=BLACK, lw=2.6, scale=16)
varrow(axa, (-0.45, -0.10), (-0.72, -0.10), color=BLACK, lw=2.6, scale=16)
axa.text(-0.58, 0.22, "transform", ha="center", fontsize=11)
axa.text(-0.585, -0.215, r"$4$", ha="center", fontsize=12.5)

# Transform A-C (vertical, south): C side (right) -> north, A side (left) -> south
varrow(axa, (0.10, -0.72), (0.10, -0.45), color=BLACK, lw=2.6, scale=16)
varrow(axa, (-0.10, -0.45), (-0.10, -0.72), color=BLACK, lw=2.6, scale=16)
axa.text(0.30, -0.58, "transform", ha="center", fontsize=11)
axa.text(-0.20, -0.585, r"$3$", ha="center", fontsize=12.5)

# Trench B-C convergence arrows (perpendicular, toward boundary) + unknown label
P = np.array([0.36, 0.48])                 # a point on the B-C boundary
nrm = np.array([-0.8, 0.6])                # toward B
varrow(axa, tuple(P + 0.30 * nrm), tuple(P + 0.06 * nrm), color=VERM, lw=3.0, scale=18)
varrow(axa, tuple(P - 0.30 * nrm), tuple(P - 0.06 * nrm), color=VERM, lw=3.0, scale=18)
axa.text(0.93, 0.62, "trench\n(convergent)", ha="center", color=VERM, fontsize=11.5,
         fontweight="bold")
axa.text(0.78, 0.15, r"$_{B}\mathbf{v}_{C}=\,?$", ha="center", color=VERM,
         fontsize=13.5, fontweight="bold")

axa.set_title("(a)  Transform–transform–trench triple junction")

# ===== Panel (b): velocity triangle ========================================
axb.set_xlim(-5.0, 1.0)
axb.set_ylim(-1.0, 4.0)
axb.set_aspect("equal")
axb.axis("off")

# _B v_A (west, 4) ; then _A v_C (north, 3) head-to-tail ; resultant _B v_C (5)
varrow(axb, (0, 0), (-4, 0), color=BLUE, lw=3.4, scale=24)
varrow(axb, (-4, 0), (-4, 3), color=GREEN, lw=3.4, scale=24)
varrow(axb, (0, 0), (-4, 3), color=VERM, lw=4.2, scale=24)
# right-angle marker at (-4,0)
axb.plot([-4, -3.7, -3.7], [0.3, 0.3, 0], color=BLACK, lw=1.2)
axb.text(-2.0, -0.42, r"$_{B}\mathbf{v}_{A}=4$", ha="center", color=BLUE, fontsize=13)
axb.text(-3.78, 1.5, r"$_{A}\mathbf{v}_{C}=3$", rotation=90, va="center",
         ha="right", color=GREEN, fontsize=13)
axb.text(-1.75, 1.95, r"$_{B}\mathbf{v}_{C}=5$", color=VERM, fontsize=14,
         fontweight="bold")
axb.text(-2.0, 3.55,
         r"$_{B}\mathbf{v}_{C} = {}_{B}\mathbf{v}_{A} + {}_{A}\mathbf{v}_{C}$",
         ha="center", fontsize=14.5)
axb.set_title("(b)  Closure: head-to-tail vector addition")

fig.suptitle("Circuit closure across a convergent boundary "
             "(archetype: Mendocino Triple Junction)", fontsize=15, y=1.02)
fig.tight_layout()
out = "../figures/fig_26_circuit_closure.png"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")
