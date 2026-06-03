"""
fig_synthesis_forward_operators.py

A flow diagram showing how one Earth model fans out through five forward
operators to five observable types, with a dashed return arrow labeling
the joint inverse problem.

Concepts follow standard geophysical inference (Tarantola 2005, Ch. 1).
Original schematic; carries no data.

Output: assets/figures/fig_synthesis_forward_operators.png
License: CC-BY 4.0
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

mpl.rcParams.update({
    "font.size": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

# ── Layout constants ────────────────────────────────────────────────────
FIG_W, FIG_H = 13, 7.0

# Column x-centres (normalised to figure width)
X_MODEL = 0.10      # left column: model box
X_OPS   = 0.45      # middle column: forward operators
X_DATA  = 0.82      # right column: observables

BOX_W_MODEL = 0.16
BOX_H_MODEL = 0.82
BOX_W_OP    = 0.20
BOX_H_OP    = 0.10
BOX_W_DAT   = 0.22
BOX_H_DAT   = 0.10

# Rows for 5 operators/observables  (y, in axes fraction, top to bottom)
ROWS = [0.82, 0.64, 0.46, 0.28, 0.10]

# Colors
C_MODEL = "#4A90D9"
C_OP    = "#7B68EE"
C_DATA  = "#2CA25F"
C_ARROW = "#555555"
C_DASHED= "#CC5500"

OPERATORS = [
    "Elastic wave\nequation",
    "Newtonian\ngravity",
    "Magnetic\npotential field",
    "Fourier heat\nconduction",
    "Elastic flexure\n& geodesy",
]
OBSERVABLES = [
    "Seismic travel times\n& waveforms",
    "Gravity anomaly\n$\\Delta g$",
    "Magnetic anomaly\n$\\Delta B$",
    "Surface\nheat flow $q$",
    "GPS / InSAR\ndisplacement",
]
PROPERTIES = [
    "velocity, density",
    "density",
    "magnetization",
    "temperature",
    "rheology",
]

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# ── Model box ───────────────────────────────────────────────────────────
model_y0 = 0.07
model_y1 = 0.95
model_xc = X_MODEL
model_x0 = model_xc - BOX_W_MODEL / 2

ax.add_patch(FancyBboxPatch(
    (model_x0, model_y0),
    BOX_W_MODEL, model_y1 - model_y0,
    boxstyle="round,pad=0.01",
    facecolor=C_MODEL, edgecolor="white", lw=2, alpha=0.25, zorder=2))
ax.text(model_xc, 0.97, "ONE\nEarth model $m$",
        ha="center", va="top", fontsize=12, fontweight="bold",
        color=C_MODEL, zorder=3)

model_items = [
    "geometry",
    "density $\\rho$",
    "$V_P$, $V_S$",
    "temperature $T$",
    "magnetization",
    "rheology",
]
for i, item in enumerate(model_items):
    ax.text(model_xc, 0.78 - i * 0.115, f"• {item}",
            ha="center", va="center", fontsize=10, color="#1a1a1a", zorder=3)

# ── Forward operator and observable boxes ───────────────────────────────
for i, (row_y, op, obs, prop) in enumerate(
        zip(ROWS, OPERATORS, OBSERVABLES, PROPERTIES)):
    y0_op  = row_y - BOX_H_OP / 2
    xc_op  = X_OPS
    x0_op  = xc_op - BOX_W_OP / 2

    y0_dat = row_y - BOX_H_DAT / 2
    xc_dat = X_DATA
    x0_dat = xc_dat - BOX_W_DAT / 2

    # operator box
    ax.add_patch(FancyBboxPatch(
        (x0_op, y0_op), BOX_W_OP, BOX_H_OP,
        boxstyle="round,pad=0.01",
        facecolor=C_OP, edgecolor="white", lw=1.5, alpha=0.20, zorder=2))
    ax.text(xc_op, row_y, op,
            ha="center", va="center", fontsize=9,
            color="#2d0080", fontweight="bold", zorder=3)

    # observable box
    ax.add_patch(FancyBboxPatch(
        (x0_dat, y0_dat), BOX_W_DAT, BOX_H_DAT,
        boxstyle="round,pad=0.01",
        facecolor=C_DATA, edgecolor="white", lw=1.5, alpha=0.20, zorder=2))
    ax.text(xc_dat, row_y, obs,
            ha="center", va="center", fontsize=9,
            color="#00451e", fontweight="bold", zorder=3)

    # arrow: model → operator
    ax.annotate("",
        xy=(x0_op, row_y), xytext=(model_x0 + BOX_W_MODEL, 0.5),
        arrowprops=dict(arrowstyle="->", color=C_ARROW, lw=1.4,
                        connectionstyle=f"arc3,rad=0.0"))

    # label on arrow (property sensed)
    mid_x = (model_x0 + BOX_W_MODEL + x0_op) / 2
    ax.text(mid_x, row_y + 0.035, prop,
            ha="center", va="bottom", fontsize=8, color="#444444",
            style="italic")

    # arrow: operator → observable
    ax.annotate("",
        xy=(x0_dat, row_y), xytext=(x0_op + BOX_W_OP, row_y),
        arrowprops=dict(arrowstyle="->", color=C_ARROW, lw=1.4))

    # label: forward operator symbol
    ax.text(xc_op - BOX_W_OP / 2 + BOX_W_OP / 2 + BOX_W_DAT / 2 - BOX_W_DAT / 2 - 0.03,
            row_y - BOX_H_OP / 2 - 0.022,
            f"$G_{i+1}(m)$", ha="center", va="top", fontsize=8, color="#555555")

# ── Dashed return arrow (bottom) ────────────────────────────────────────
ax.annotate("",
    xy=(model_x0 + BOX_W_MODEL / 2, model_y0 - 0.0),
    xytext=(X_DATA + BOX_W_DAT / 2, 0.01),
    arrowprops=dict(arrowstyle="->", color=C_DASHED, lw=2.0,
                    linestyle="dashed",
                    connectionstyle="arc3,rad=-0.25"))

ax.text(0.50, 0.015,
        "joint inverse problem: find one $m$ consistent with all data"
        "   →   combining independent observables reduces non-uniqueness",
        ha="center", va="bottom", fontsize=9, color=C_DASHED,
        style="italic", fontweight="bold")

fig.tight_layout()
out = "assets/figures/fig_synthesis_forward_operators.png"
fig.savefig(out, bbox_inches="tight")
print(f"Saved: {out}")
