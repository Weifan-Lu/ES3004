"""
F12_rifting_continuum.py

Rifting continuum spectrum — a six-stage cartoon showing the geophysical
and structural evolution of the lithosphere from stable craton to fast
mid-ocean ridge:

  Stage 1: Stable continental craton (pre-rift)
  Stage 2: Incipient rifting (e.g., Rio Grande)
  Stage 3: Mature continental rift (e.g., EAR southern)
  Stage 4: Rifting → spreading transition (e.g., Afar / Red Sea)
  Stage 5: Slow-spreading MOR (e.g., MAR)
  Stage 6: Fast-spreading MOR (e.g., EPR)

For each stage, the figure shows a vertical cross-section sketch (rift
geometry, Moho relief, LAB depth) plus a six-symbol attribute strip
indicating sign and magnitude of the standard geophysical observables.

This figure is the visual anchor for the L27 §5 Round 2 active-learning
exercise (rifting continuum spectrum). Each row of the attribute matrix
maps to one column of this figure.

This is a pedagogical synthesis original to the lecture — no equivalent
single-figure summary exists in the open literature.

Output: assets/figures/F12_rifting_continuum.png
License: CC-BY 4.0 (this script)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _ess314_style import apply_style, PALETTE, save

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


STAGES = [
    {
        "label": "1. Stable craton",
        "example": "Canadian Shield",
        "x_width": 200,
        "moho_axis": 45,      # km
        "moho_off": 45,
        "lab_axis": 250,
        "lab_off": 250,
        "rift_topo": 0,        # km uplift / depression
        "valley_depth": 0,
        "bouguer": "~0",
        "heatflow": "30–45",
        "topo": "flat",
        "beta": "1.0",
        "magma": "none",
        "seis": "rare, deep",
        "color": "#9eb6c8",
    },
    {
        "label": "2. Incipient rifting",
        "example": "Rio Grande Rift",
        "x_width": 200,
        "moho_axis": 35,
        "moho_off": 38,
        "lab_axis": 130,
        "lab_off": 160,
        "rift_topo": 1.0,
        "valley_depth": 0.5,
        "bouguer": "small −",
        "heatflow": "60–70",
        "topo": "uplift",
        "beta": "1.1–1.3",
        "magma": "alkaline",
        "seis": "shallow brittle",
        "color": "#c7d1a8",
    },
    {
        "label": "3. Mature rift",
        "example": "EAR — Kenya",
        "x_width": 200,
        "moho_axis": 22,
        "moho_off": 35,
        "lab_axis": 100,
        "lab_off": 150,
        "rift_topo": 1.7,
        "valley_depth": 1.2,
        "bouguer": "−150 to −250",
        "heatflow": "80–120",
        "topo": "uplift +graben",
        "beta": "1.5–2.5",
        "magma": "bimodal",
        "seis": "shallow ext.",
        "color": "#e8c280",
    },
    {
        "label": "4. Rift → spread",
        "example": "Afar / Red Sea",
        "x_width": 200,
        "moho_axis": 12,
        "moho_off": 28,
        "lab_axis": 80,
        "lab_off": 130,
        "rift_topo": 0.4,
        "valley_depth": 1.8,
        "bouguer": "mixed",
        "heatflow": "120–200",
        "topo": "thin crust",
        "beta": "3–5",
        "magma": "dyke-dominated",
        "seis": "dyke swarms",
        "color": "#e89a60",
    },
    {
        "label": "5. Slow MOR",
        "example": "Mid-Atlantic Ridge",
        "x_width": 200,
        "moho_axis": 7,
        "moho_off": 9,
        "lab_axis": 50,
        "lab_off": 95,
        "rift_topo": -2.5,
        "valley_depth": 0.7,
        "bouguer": "broad −",
        "heatflow": "~250 axis",
        "topo": "axial valley",
        "beta": "→ ∞",
        "magma": "episodic",
        "seis": "axial brittle",
        "color": "#c87060",
    },
    {
        "label": "6. Fast MOR",
        "example": "East Pacific Rise",
        "x_width": 200,
        "moho_axis": 6,
        "moho_off": 8,
        "lab_axis": 35,
        "lab_off": 80,
        "rift_topo": -2.7,
        "valley_depth": 0,
        "bouguer": "small −",
        "heatflow": "very high",
        "topo": "axial high",
        "beta": "→ ∞",
        "magma": "continuous AMC",
        "seis": "small swarms",
        "color": "#8e3050",
    },
]


def draw_cross_section(ax, stage, lat_y_top=0.65, lat_y_bot=0.05):
    """Draw the cross-section sketch for a single stage."""
    # All cross-sections are in lat_y_top → lat_y_bot strip of the axes
    # (using axes-fraction coordinates so each subplot scales uniformly)

    # x range −1..+1 in axes fraction
    xline = np.linspace(-1, 1, 200)

    # Topography (only for continental-like stages 1-4)
    if stage["rift_topo"] >= 0:
        topo = stage["rift_topo"] / 6 * (
            np.exp(-(xline ** 2) / 0.4)) - stage["valley_depth"] / 6 * (
            np.exp(-(xline ** 2) / 0.03))
        topo_scaled = topo * 0.06
        surface_y = lat_y_top + topo_scaled
    else:
        # Ridges: bathymetry — deep on flanks, axial valley or high
        # depth in km; flank depth larger
        flank = abs(stage["rift_topo"])
        axial = flank - 0.6 if stage["valley_depth"] > 0 else flank - 0.3
        topo = -(axial + (flank - axial) * (1 - np.exp(-(xline ** 2) / 0.4)))
        # Map km depth to negative offset (water shows above surface_y)
        topo_scaled = topo * 0.04
        surface_y = lat_y_top + topo_scaled

    # Moho line
    moho_axis = stage["moho_axis"]
    moho_off = stage["moho_off"]
    moho_km = moho_off - (moho_off - moho_axis) * np.exp(-(xline ** 2) / 0.15)
    # Vertical scale: 0 km depth at lat_y_top, 300 km depth at lat_y_bot
    span_y = lat_y_top - lat_y_bot
    moho_y = lat_y_top - (moho_km / 300.0) * span_y

    # LAB line
    lab_axis = stage["lab_axis"]
    lab_off = stage["lab_off"]
    lab_km = lab_off - (lab_off - lab_axis) * np.exp(-(xline ** 2) / 0.20)
    lab_y = lat_y_top - (lab_km / 300.0) * span_y

    # Crust fill (between surface and Moho)
    ax.fill_between(xline, moho_y, surface_y,
                     facecolor="#c8a070", edgecolor="none",
                     transform=ax.transAxes, zorder=2)
    # Mantle lithosphere fill (between Moho and LAB)
    ax.fill_between(xline, lab_y, moho_y,
                     facecolor="#e8d8b8", edgecolor="none",
                     transform=ax.transAxes, zorder=2)
    # Asthenosphere fill (below LAB)
    ax.fill_between(xline, lat_y_bot, lab_y,
                     facecolor="#f7c79a", edgecolor="none",
                     transform=ax.transAxes, zorder=2)

    # Water for ridges
    if stage["rift_topo"] < 0:
        ax.fill_between(xline, surface_y, lat_y_top + 0.005,
                         facecolor="#cfe6f5", edgecolor="none",
                         transform=ax.transAxes, zorder=3)

    # Magmatic features
    if stage["magma"] == "continuous AMC":
        # Narrow axial melt lens
        ax.add_patch(mpatches.Rectangle(
            (-0.04, surface_y[100] - 0.018), 0.08, 0.012,
            facecolor=PALETTE["verm"], edgecolor="none",
            transform=ax.transAxes, zorder=4))
    elif stage["magma"] in ("dyke-dominated", "bimodal", "episodic"):
        # A small vertical dyke at the axis
        ax.plot([0, 0],
                 [surface_y[100], moho_y[100]],
                 color=PALETTE["verm"], lw=2.0, alpha=0.85,
                 transform=ax.transAxes, zorder=4)

    # Moho line on top of fills
    ax.plot(xline, moho_y, color="black", lw=0.8,
             transform=ax.transAxes, zorder=5)
    # LAB line
    ax.plot(xline, lab_y, color="black", lw=0.6, ls="--", alpha=0.6,
             transform=ax.transAxes, zorder=5)


def draw_attribute_table(ax, stage, y_start=0.42):
    """Render the six-attribute table at the bottom of each panel."""
    rows = [
        ("Bouguer",  stage["bouguer"]),
        ("Heat flow",stage["heatflow"]),
        ("Topo",     stage["topo"]),
        ("β",        stage["beta"]),
        ("Magma",    stage["magma"]),
        ("Seis",     stage["seis"]),
    ]
    line_height = 0.068
    for i, (key, val) in enumerate(rows):
        y = y_start - i * line_height
        ax.text(0.06, y, key, fontsize=9, fontweight="bold",
                 transform=ax.transAxes, color=PALETTE["black"])
        ax.text(0.42, y, val, fontsize=9, transform=ax.transAxes,
                 color=PALETTE["black"])


def make_figure():
    apply_style()

    fig, axes = plt.subplots(1, 6, figsize=(20, 6),
                              gridspec_kw=dict(wspace=0.08))

    for ax, stage in zip(axes, STAGES):
        ax.set_xlim(-1, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)

        # Header band
        ax.add_patch(mpatches.Rectangle((0, 0.92), 1, 0.08,
                                         facecolor=stage["color"],
                                         edgecolor="none",
                                         transform=ax.transAxes,
                                         clip_on=False))
        ax.text(0.5, 0.96, stage["label"], fontsize=11, fontweight="bold",
                 ha="center", va="center", transform=ax.transAxes,
                 color="black")
        ax.text(0.5, 0.88, f"e.g. {stage['example']}", fontsize=9,
                 ha="center", va="top", transform=ax.transAxes,
                 style="italic", color="#444444")

        # Cross-section
        draw_cross_section(ax, stage,
                            lat_y_top=0.78, lat_y_bot=0.50)

        # Depth labels at left of leftmost panel only
        if stage == STAGES[0]:
            ax.text(-0.06, 0.78, "0", fontsize=8, ha="right", va="center",
                     transform=ax.transAxes)
            ax.text(-0.06, 0.50, "300\nkm", fontsize=8, ha="right",
                     va="center", transform=ax.transAxes)

        # Attribute table
        draw_attribute_table(ax, stage)

    fig.suptitle("The rifting continuum — six stages, six geophysical "
                  "attributes",
                  fontsize=14, y=0.98)

    return fig


if __name__ == "__main__":
    fig = make_figure()
    out = os.path.join(os.path.dirname(__file__), "..", "figures",
                       "F12_rifting_continuum.png")
    save(fig, out)
    print(f"Wrote {out}")
