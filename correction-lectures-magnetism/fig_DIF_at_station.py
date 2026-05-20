"""fig_DIF_at_station.py — local representation of the field at a station.

Two panels:
  (a) map view (looking down): X = true north axis; Y = east; declination D
      is the angle of the horizontal field H east of true north.
  (b) side view: horizontal ground; Z axis points downward; total field F
      makes inclination angle I below horizontal; decomposed into
      H = F cos I (horizontal) and Z = F sin I (vertical, down-positive).

Values shown are for Seattle 2026 (IGRF-13): D = +15.5°, I = +68.9°, F = 52900 nT.

ESS 314, Lecture 23 §3 (Earth Magnetism — D, I, F at a station).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc

from _style import COLORS, apply_style


D_SEA = 15.5     # declination (deg E of true N), Seattle 2026
I_SEA = 68.9     # inclination (deg below horizontal)
F_SEA = 52_900   # total intensity (nT)


def draw_map_panel(ax) -> None:
    ax.set_title("(a) Map view  (looking down)", fontsize=13, pad=10)
    ax.set_aspect("equal")
    ax.set_xlim(-0.4, 1.5)
    ax.set_ylim(-0.4, 1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # X (true north) and Y (east) axes.
    ax.annotate("", xy=(1.45, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["grey"],
                                lw=1.2, mutation_scale=14))
    ax.annotate("", xy=(0, 1.45), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["grey"],
                                lw=1.2, mutation_scale=14))
    ax.text(1.50, 0, "Y (east)", ha="left", va="center",
            fontsize=11, color=COLORS["grey"])
    ax.text(0, 1.50, "X (true N)", ha="center", va="bottom",
            fontsize=11, color=COLORS["grey"])

    # Horizontal field H, rotated D degrees east of true north (X axis).
    D_rad = np.radians(D_SEA)
    h_x = np.cos(D_rad)   # north component (along X)
    h_y = np.sin(D_rad)   # east component (along Y)
    # Plot the H arrow scaled to length 1.2.
    L = 1.2
    ax.annotate("", xy=(L * h_y, L * h_x), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["blue"],
                                lw=2.5, mutation_scale=16))
    ax.text(L * h_y + 0.07, L * h_x + 0.05, r"$H$ (horizontal field)",
            color=COLORS["blue"], fontsize=12, fontweight="bold",
            ha="left", va="center")

    # Declination arc from +X (true N) to H.
    arc = Arc((0, 0), 0.6, 0.6, angle=0,
              theta1=90 - D_SEA, theta2=90,
              color=COLORS["vermilion"], lw=2.0)
    ax.add_patch(arc)
    ax.text(0.20, 0.42, f"$D = +{D_SEA:.1f}^\\circ$",
            color=COLORS["vermilion"], fontsize=13, fontweight="bold")

    # X and Y component drop-lines (dashed).
    ax.plot([L * h_y, L * h_y], [0, L * h_x], color=COLORS["lightgrey"],
            lw=0.8, linestyle="--")
    ax.plot([0, L * h_y], [L * h_x, L * h_x], color=COLORS["lightgrey"],
            lw=0.8, linestyle="--")
    # Component labels.
    ax.text(L * h_y, -0.10, f"$Y = {F_SEA * np.cos(np.radians(I_SEA)) * np.sin(D_rad):.0f}$ nT",
            ha="center", va="top", color=COLORS["grey"], fontsize=10)
    ax.text(-0.05, L * h_x, f"$X = {F_SEA * np.cos(np.radians(I_SEA)) * np.cos(D_rad):.0f}$ nT",
            ha="right", va="center", color=COLORS["grey"], fontsize=10)


def draw_side_panel(ax) -> None:
    ax.set_title("(b) Side view  (vertical section through $\\mathbf{F}$)",
                 fontsize=13, pad=10)
    ax.set_aspect("equal")
    ax.set_xlim(-0.4, 1.5)
    ax.set_ylim(-1.5, 0.4)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Horizontal ground line.
    ax.axhline(0, color=COLORS["black"], lw=1.2)
    ax.text(1.50, 0.04, "horizontal", ha="right", va="bottom",
            fontsize=10, color=COLORS["grey"])

    # Z axis pointing downward.
    ax.annotate("", xy=(0, -1.45), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["grey"],
                                lw=1.2, mutation_scale=14))
    ax.text(-0.08, -1.50, "Z (down)", ha="right", va="top",
            fontsize=11, color=COLORS["grey"])

    # The total-field vector F at inclination I below horizontal.
    I_rad = np.radians(I_SEA)
    L = 1.3
    fx = L * np.cos(I_rad)      # horizontal component
    fy = -L * np.sin(I_rad)     # vertical down (negative y in plot)
    ax.annotate("", xy=(fx, fy), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["vermilion"],
                                lw=2.5, mutation_scale=18))
    ax.text(fx + 0.04, fy - 0.05,
            r"$\mathbf{F}$ (total field)",
            color=COLORS["vermilion"], fontsize=12, fontweight="bold",
            ha="left", va="top")

    # H (horizontal) component as separate arrow.
    ax.annotate("", xy=(fx, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["blue"],
                                lw=2.0, mutation_scale=14))
    ax.text(fx / 2, 0.08, f"$H = F\\cos I = {F_SEA * np.cos(I_rad):.0f}$ nT",
            ha="center", va="bottom", color=COLORS["blue"], fontsize=11,
            fontweight="bold")

    # Z (vertical) component as separate arrow.
    ax.annotate("", xy=(fx, fy), xytext=(fx, 0),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["green"],
                                lw=2.0, mutation_scale=14))
    ax.text(fx + 0.04, fy / 2, f"$Z = F\\sin I = {F_SEA * np.sin(I_rad):.0f}$ nT",
            ha="left", va="center", color=COLORS["green"], fontsize=11,
            fontweight="bold")

    # Inclination arc from horizontal to F.
    arc = Arc((0, 0), 0.7, 0.7, angle=0,
              theta1=-I_SEA, theta2=0,
              color=COLORS["orange"], lw=2.0)
    ax.add_patch(arc)
    ax.text(0.40, -0.18, f"$I = +{I_SEA:.1f}^\\circ$",
            color=COLORS["orange"], fontsize=13, fontweight="bold")


def main(out: Path) -> None:
    apply_style()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.0))
    draw_map_panel(ax1)
    draw_side_panel(ax2)

    fig.suptitle("Seattle 2026 — local representation of the geomagnetic field "
                 f"($F = {F_SEA:,}$ nT)",
                 fontsize=14, fontweight="bold", y=1.00)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir / "fig_DIF_at_station.png")
    print("wrote", out_dir / "fig_DIF_at_station.png")
