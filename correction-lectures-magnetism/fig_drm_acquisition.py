"""fig_drm_acquisition.py — schematic of detrital remanent magnetisation.

Water column at top with small magnetic grains (rod shapes) settling
downward. In the water column, grains rotate to align with the ambient
field H_0. At the sediment-water interface, aligned grains accumulate
into a sediment layer. Older sediment at depth records earlier states
of the field.

ESS 314, Lecture 24 §5.2 (Rock Magnetism — DRM Acquisition).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch

from _style import COLORS, apply_style


def draw_grain(ax, cx: float, cy: float, angle_deg: float,
               size: float = 0.12, color_n: str = None, color_s: str = None) -> None:
    """Draw a small magnetic grain (a dipole rod) at angle_deg.
    The 'north' end is drawn in primary blue, 'south' in vermilion.
    """
    if color_n is None:
        color_n = COLORS["blue"]
    if color_s is None:
        color_s = COLORS["vermilion"]
    theta = np.radians(angle_deg)
    dx = size * np.cos(theta) / 2
    dy = size * np.sin(theta) / 2
    # Draw two halves so each end is colour-coded.
    # North half (head):
    ax.plot([cx, cx + dx], [cy, cy + dy], color=color_n, lw=2.2,
            solid_capstyle="round", zorder=8)
    # South half (tail):
    ax.plot([cx, cx - dx], [cy, cy - dy], color=color_s, lw=2.2,
            solid_capstyle="round", zorder=8)
    # Tiny arrowhead at the north end.
    ax.plot(cx + dx, cy + dy, marker=">",
            markersize=4, color=color_n, zorder=9)


def main(out: Path) -> None:
    apply_style()

    fig, ax = plt.subplots(figsize=(11, 7.0))
    ax.set_aspect("equal")
    ax.set_xlim(0, 10)
    ax.set_ylim(-3, 6)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # ----- Water column (light blue) -----
    water = Rectangle((0, 0), 10, 6, facecolor=COLORS["skyblue"],
                      alpha=0.18, edgecolor="none", zorder=1)
    ax.add_patch(water)
    ax.text(0.3, 5.7, "water column", fontsize=11,
            color=COLORS["blue"], fontweight="bold", va="top")

    # ----- Sediment layers (older = deeper) -----
    # Recent (top) — aligned with present field (eastward at 30° below horizontal)
    recent = Rectangle((0, -1.0), 10, 1.0, facecolor="#E5D8B0",
                       edgecolor=COLORS["grey"], lw=0.6, zorder=2)
    ax.add_patch(recent)
    # Older — aligned with a different (reversed-direction) field
    older = Rectangle((0, -3.0), 10, 2.0, facecolor="#C8B888",
                      edgecolor=COLORS["grey"], lw=0.6, zorder=2)
    ax.add_patch(older)
    # Sediment-water interface line.
    ax.axhline(0, color=COLORS["black"], lw=1.2, zorder=3)
    ax.text(9.8, 0.06, "sediment-water\ninterface",
            ha="right", va="bottom", fontsize=9,
            color=COLORS["grey"], style="italic")

    # ----- Ambient field H_0 — arrow at top -----
    H0_angle = 15  # degrees above horizontal, pointing right
    ax.annotate("", xy=(9.0, 5.0 + 0.5 * np.tan(np.radians(H0_angle))),
                xytext=(7.0, 5.0),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["black"],
                                lw=2.2, mutation_scale=18))
    ax.text(8.0, 5.4, r"$\mathbf{H}_0$", fontsize=16, fontweight="bold",
            color=COLORS["black"], ha="center", va="bottom")
    ax.text(8.0, 4.5, "ambient field\n(present day)",
            fontsize=9, color=COLORS["grey"], ha="center", va="top",
            style="italic")

    # ----- Grains in the water column -----
    # Upper grains: randomly oriented (recently eroded, falling).
    np.random.seed(7)
    n_upper = 12
    xs_upper = np.random.uniform(0.5, 9.5, n_upper)
    ys_upper = np.random.uniform(3.8, 5.2, n_upper)
    angles_upper = np.random.uniform(0, 360, n_upper)
    for x, y, a in zip(xs_upper, ys_upper, angles_upper):
        draw_grain(ax, x, y, a, size=0.45)
        # Settling motion indicator.
        ax.annotate("", xy=(x, y - 0.45), xytext=(x, y - 0.20),
                    arrowprops=dict(arrowstyle="->", color=COLORS["grey"],
                                    lw=0.5, mutation_scale=6))

    # Middle grains: partially aligned (rotating into alignment with H_0).
    n_mid = 10
    xs_mid = np.random.uniform(0.5, 9.5, n_mid)
    ys_mid = np.random.uniform(2.0, 3.4, n_mid)
    # Partially aligned: angles cluster around H0_angle but with scatter.
    angles_mid = H0_angle + np.random.uniform(-50, 50, n_mid)
    for x, y, a in zip(xs_mid, ys_mid, angles_mid):
        draw_grain(ax, x, y, a, size=0.45)
        ax.annotate("", xy=(x, y - 0.55), xytext=(x, y - 0.20),
                    arrowprops=dict(arrowstyle="->", color=COLORS["grey"],
                                    lw=0.5, mutation_scale=6))

    # Lower grains (just above interface): well-aligned with H_0.
    n_lower = 10
    xs_lower = np.linspace(0.6, 9.4, n_lower)
    ys_lower = 0.5 * np.ones(n_lower) + np.random.uniform(-0.12, 0.12, n_lower)
    angles_lower = H0_angle + np.random.uniform(-8, 8, n_lower)
    for x, y, a in zip(xs_lower, ys_lower, angles_lower):
        draw_grain(ax, x, y, a, size=0.5)

    # ----- Sediment grains: locked-in orientations -----
    # Recent sediment: aligned with H_0 (modern field).
    xs_recent = np.linspace(0.5, 9.5, 14)
    ys_recent = -0.5 * np.ones_like(xs_recent) + np.random.uniform(-0.15, 0.15,
                                                                    len(xs_recent))
    angles_recent = H0_angle + np.random.uniform(-6, 6, len(xs_recent))
    for x, y, a in zip(xs_recent, ys_recent, angles_recent):
        draw_grain(ax, x, y, a, size=0.42)

    # Older sediment: aligned with a *different* field (e.g. opposite polarity).
    xs_old = np.linspace(0.5, 9.5, 14)
    ys_old = -1.7 * np.ones_like(xs_old) + np.random.uniform(-0.15, 0.15,
                                                              len(xs_old))
    older_angle = H0_angle + 180  # reversed polarity
    angles_old = older_angle + np.random.uniform(-6, 6, len(xs_old))
    for x, y, a in zip(xs_old, ys_old, angles_old):
        draw_grain(ax, x, y, a, size=0.42)
    # Second older horizon, intermediate direction.
    xs_oldx = np.linspace(0.5, 9.5, 14)
    ys_oldx = -2.55 * np.ones_like(xs_oldx) + np.random.uniform(-0.15, 0.15,
                                                                  len(xs_oldx))
    oldx_angle = H0_angle + 60
    angles_oldx = oldx_angle + np.random.uniform(-6, 6, len(xs_oldx))
    for x, y, a in zip(xs_oldx, ys_oldx, angles_oldx):
        draw_grain(ax, x, y, a, size=0.42)

    # ----- Annotations -----
    # Right side: depth/age axis.
    arrow_ax = FancyArrowPatch((10.4, 5.5), (10.4, -2.8),
                                arrowstyle="-|>", color=COLORS["grey"],
                                mutation_scale=12, lw=1.0)
    ax.add_patch(arrow_ax)
    ax.text(10.6, 1.5, "depth /\nincreasing age",
            ha="left", va="center", fontsize=10,
            color=COLORS["grey"], rotation=90, style="italic")

    # Stage labels on the left.
    stages = [
        (-0.4, 4.5, "Settling:\nrandom orientations"),
        (-0.4, 2.7, "Aligning:\nrotating toward $\\mathbf{H}_0$"),
        (-0.4, 0.5, "Deposition:\naligned with $\\mathbf{H}_0$"),
        (-0.4, -0.5, "Locked in:\nrecent field"),
        (-0.4, -1.7, "Older sediment:\nreversed field"),
        (-0.4, -2.55, "Older still:\ndifferent field"),
    ]
    # Use a wider left margin for these labels — switch to right-aligned at x=10.5
    for x, y, txt in stages:
        ax.text(0.05, y, txt, ha="left", va="center", fontsize=8.5,
                color=COLORS["grey"], style="italic",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                          edgecolor="none", alpha=0.85))

    ax.set_title("Detrital remanent magnetisation (DRM) — "
                 "aligning, settling, locking in",
                 fontsize=13, fontweight="bold", pad=10)

    # Legend for grain colour code.
    leg_x, leg_y = 0.4, -2.85
    ax.plot([leg_x, leg_x + 0.4], [leg_y, leg_y],
            color=COLORS["vermilion"], lw=2.2,
            solid_capstyle="round")
    ax.plot([leg_x + 0.4, leg_x + 0.8], [leg_y, leg_y],
            color=COLORS["blue"], lw=2.2,
            solid_capstyle="round")
    ax.plot(leg_x + 0.8, leg_y, marker=">", color=COLORS["blue"], markersize=4)
    ax.text(leg_x + 1.0, leg_y, "grain dipole (S → N)",
            ha="left", va="center", fontsize=9, color=COLORS["grey"])

    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir / "fig_drm_acquisition.png")
    print("wrote", out_dir / "fig_drm_acquisition.png")
