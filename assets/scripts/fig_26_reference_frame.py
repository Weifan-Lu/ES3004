"""
fig_26_reference_frame.py

Scientific content: The relative velocity between two plates is independent of
the reference frame. Top: with Plate A held fixed, Plate B moves to the right at
the full relative rate. Bottom: with Plate B held fixed, Plate A moves to the
left at the same rate. The relative-velocity vector (A->B) is the physical
invariant; only the frame differs. The half-rate / full-rate distinction for
seafloor spreading is annotated.

Reproduces the scientific content of (original figure NOT used):
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Cambridge University Press, Ch. 2 (relative plate velocity, reference frames).

Output: assets/figures/fig_26_reference_frame.png
License: CC-BY 4.0 (this script)
"""
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

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


def block(ax, x0, x1, color, label, fixed=False):
    ax.fill([x0, x1, x1, x0], [0.25, 0.25, 0.75, 0.75], color=color, alpha=0.40)
    ax.plot([x0, x1, x1, x0, x0], [0.25, 0.25, 0.75, 0.75, 0.25],
            color=BLACK, lw=1.2)
    tag = f"{label}\n(fixed)" if fixed else label
    ax.text(0.5 * (x0 + x1), 0.50, tag, ha="center", va="center", fontsize=13.5)


def arrow(ax, x0, y0, x1, y1, color=BLACK, lw=3.2):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color,
                                mutation_scale=24))


fig, axes = plt.subplots(2, 1, figsize=(8.2, 6.6))
for ax in axes:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

# ---- Top: Plate A fixed ---------------------------------------------------
ax = axes[0]
block(ax, 0.08, 0.50, SKY, "Plate A", fixed=True)
block(ax, 0.50, 0.92, ORANGE, "Plate B")
arrow(ax, 0.71, 0.82, 0.89, 0.82)
ax.text(0.80, 0.90, r"$v = $ full rate", ha="center", fontsize=12.5)
ax.set_title("Reference frame 1 — Plate A fixed", loc="left")

# ---- Bottom: Plate B fixed ------------------------------------------------
ax = axes[1]
block(ax, 0.08, 0.50, SKY, "Plate A")
block(ax, 0.50, 0.92, ORANGE, "Plate B", fixed=True)
arrow(ax, 0.29, 0.82, 0.11, 0.82)
ax.text(0.20, 0.90, r"$v = $ full rate", ha="center", fontsize=12.5)
ax.set_title("Reference frame 2 — Plate B fixed", loc="left")

fig.text(0.5, 0.005,
         r"The relative velocity $_{A}\mathbf{v}_{B}$ is identical in both frames — "
         r"only the choice of fixed plate changes." "\n"
         r"Spreading: each flank moves at the half-rate relative to the ridge; "
         r"the full rate is the plate-to-plate relative velocity.",
         ha="center", va="bottom", fontsize=11.5)

fig.suptitle("Relative velocity is frame-independent", fontsize=16, y=0.99)
fig.tight_layout(rect=[0, 0.10, 1, 0.96])
out = "../figures/fig_26_reference_frame.png"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")
