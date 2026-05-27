"""
F1_ridge_magmatic_system.py

Mid-ocean ridge magmatic system schematic — pedagogical cross-section
showing layered crustal structure from the axis outward to mature crust.

Pedagogical content: shows the canonical four-layer oceanic crustal stack
(extrusives → sheeted dykes → upper gabbro → lower gabbro/Moho transition)
with axial magma lens / mush zone in the centre. Compatible with both
slow- and fast-spreading ridge end-members.

After: Sinton & Detrick 1992; Bell et al. 2022 (Frontiers, CC-BY 4.0).

Output: assets/figures/F1_ridge_magmatic_system.png
License: CC-BY 4.0 (this script)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _ess314_style import apply_style, PALETTE, save

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import matplotlib.patches as mpatches


def make_figure():
    apply_style()

    fig, ax = plt.subplots(figsize=(11, 6))

    # Geometry: x in km from ridge axis (-30 .. +30), y in km depth below seafloor
    x_min, x_max = -30, 30
    y_max = 7.5
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_max, -1.2)   # depth increases downward; never invert_yaxis
    ax.set_xlabel("Distance from ridge axis (km)")
    ax.set_ylabel("Depth below seafloor (km)")
    ax.set_title("Mid-ocean ridge magmatic system — schematic cross-section",
                 loc="left")

    # Water column
    ax.add_patch(mpatches.Rectangle((x_min, -1.2), x_max - x_min, 1.2,
                                     facecolor="#cfe6f5", edgecolor="none",
                                     zorder=1))
    ax.text(x_min + 1.5, -0.7, "Seawater", fontsize=10, color="#1c4e80",
            style="italic", zorder=2)

    # Seafloor topography — broad axial high, slight valley near axis
    xseaf = np.linspace(x_min, x_max, 400)
    seafloor = 0.0 + 0.15 * np.exp(-(xseaf**2) / 200)  # mild axial high
    # Add a narrow axial valley for the slow-spreading flavour
    seafloor -= 0.20 * np.exp(-(xseaf**2) / 8)

    # Layer 2A — extrusives (pillow basalts + flows)
    base_2A = seafloor + 0.55
    ax.fill_between(xseaf, seafloor, base_2A,
                    facecolor="#3a3a3a", edgecolor="none", zorder=3,
                    label="Layer 2A — extrusives")

    # Layer 2B/2C — sheeted dykes
    base_dykes = base_2A + 1.45
    ax.fill_between(xseaf, base_2A, base_dykes,
                    facecolor="#8a8a8a", edgecolor="none", zorder=3)
    # Dyke hatching: thin vertical lines
    for xd in np.linspace(x_min + 1, x_max - 1, 90):
        ax.plot([xd, xd],
                [np.interp(xd, xseaf, base_2A),
                 np.interp(xd, xseaf, base_dykes)],
                color="#555555", lw=0.4, zorder=4)

    # Layer 3 — gabbro
    moho_depth = 5.8
    base_gabbro = np.full_like(xseaf, moho_depth)
    ax.fill_between(xseaf, base_dykes, base_gabbro,
                    facecolor="#bfbfbf", edgecolor="none", zorder=3)

    # Mantle below Moho — peridotite
    ax.fill_between(xseaf, base_gabbro, y_max,
                    facecolor="#e8d8b8", edgecolor="none", zorder=3)

    # ── Axial magma lens (thin sill at ~1.8 km below seafloor) ──
    amc_x = np.array([-2.0, -0.9, 0.0, 0.9, 2.0])
    amc_top = np.array([2.05, 1.85, 1.78, 1.85, 2.05])
    amc_bot = amc_top + 0.18
    ax.fill_between(amc_x, amc_top, amc_bot,
                    facecolor=PALETTE["verm"], edgecolor="black", lw=0.8,
                    zorder=5, label="Axial magma lens (melt-rich)")

    # ── Crystal mush zone surrounding the lens ──
    mush_x = np.linspace(-7, 7, 120)
    mush_top = 2.0 + 0.3 * (mush_x / 7) ** 2
    mush_bot = 4.4 + 0.6 * (mush_x / 7) ** 2
    ax.fill_between(mush_x, mush_top, mush_bot,
                    facecolor=PALETTE["orange"], alpha=0.55, edgecolor="black",
                    lw=0.6, zorder=4, label="Crystal mush zone")

    # ── Mantle upwelling arrows below the mush zone ──
    for xu, ystart in [(-3.5, 7.0), (0.0, 7.2), (3.5, 7.0)]:
        ax.annotate("", xy=(xu, 5.2), xytext=(xu, ystart),
                    arrowprops=dict(arrowstyle="->", color=PALETTE["verm"],
                                    lw=1.8), zorder=6)

    # ── Plate motion arrows at top (above seafloor) ──
    ax.annotate("", xy=(x_min + 3, -0.95), xytext=(x_min + 12, -0.95),
                arrowprops=dict(arrowstyle="->", color=PALETTE["black"], lw=1.6))
    ax.annotate("", xy=(x_max - 3, -0.95), xytext=(x_max - 12, -0.95),
                arrowprops=dict(arrowstyle="->", color=PALETTE["black"], lw=1.6))
    ax.text(x_min + 7, -0.55, "Plate motion", fontsize=10, ha="center",
            color=PALETTE["black"])

    # Layer labels (right side, off-axis where layers are clean)
    label_x = 22
    ax.text(label_x, 0.27, "Layer 2A — pillow basalts",
            fontsize=9.5, ha="center", va="center", color="white",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="#3a3a3a",
                      edgecolor="none"))
    ax.text(label_x, 1.30, "Layer 2B/2C — sheeted dykes",
            fontsize=9.5, ha="center", va="center", color="black",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="#cccccc",
                      edgecolor="none"))
    ax.text(label_x, 4.20, "Layer 3 — gabbro",
            fontsize=9.5, ha="center", va="center", color="black",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="#dddddd",
                      edgecolor="none"))
    ax.text(label_x, 6.60, "Mantle peridotite",
            fontsize=9.5, ha="center", va="center", color="black",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="#f0e0c0",
                      edgecolor="none"))

    # Moho line
    ax.axhline(moho_depth, color="black", lw=0.8, ls="--", alpha=0.5)
    ax.text(x_min + 1.5, moho_depth - 0.10, "Moho",
            fontsize=10, ha="left", va="bottom", style="italic")

    # Axial labels
    ax.text(0, 2.60, "AML", fontsize=9.5, ha="center", va="center",
            fontweight="bold", color="white",
            bbox=dict(boxstyle="round,pad=0.10",
                      facecolor=PALETTE["verm"], edgecolor="black", lw=0.5))
    ax.text(5.5, 3.20, "mush", fontsize=9.5, ha="left", va="center",
            color="black", style="italic")

    # Decoration
    ax.set_xticks(np.arange(-30, 31, 10))
    ax.grid(False)

    # Legend (top-left, away from ridge axis content)
    handles = [
        mpatches.Patch(facecolor=PALETTE["verm"], edgecolor="black",
                       label="Axial magma lens (high melt fraction)"),
        mpatches.Patch(facecolor=PALETTE["orange"], alpha=0.55,
                       edgecolor="black", label="Crystal mush zone"),
    ]
    ax.legend(handles=handles, loc="lower left", framealpha=0.92, fontsize=9.5)

    return fig


if __name__ == "__main__":
    fig = make_figure()
    out = os.path.join(os.path.dirname(__file__), "..", "figures",
                       "F1_ridge_magmatic_system.png")
    save(fig, out)
    print(f"Wrote {out}")
