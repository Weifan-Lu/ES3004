"""
F6_ear_system_map.py

East African Rift system overview — map showing the Nubian, Somalian,
and Arabian plates with the Eastern (Kenya/Ethiopia/Afar) and Western
(Western Branch) rift arms, plate motion arrows, and major volcanic centres.

This figure complements (but does not replace) the canonical research-grade
map of the EAR system. For deployment, the preferred figure is:

    Biggs, J. et al. (2021). Volcanic activity and hazard in the East
    African Rift Zone. Nature Communications 12, 6881. CC-BY 4.0.
    doi:10.1038/s41467-021-27166-y. Figure 1.

That figure should be downloaded by the build agent and saved as
'F6_ear_system_map.png' in assets/figures/ with the CC-BY attribution
caption. This Python script provides a fallback synthesised version
that the sandbox can render when the Biggs 2021 PNG is unavailable.

Coastlines: Natural Earth 110m via local cache (assets/data/).

Output: assets/figures/F6_ear_system_map.png
License: CC-BY 4.0 (this script)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _ess314_style import apply_style, PALETTE, save

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def plot_real_coastlines(ax, lon_min, lon_max, lat_min, lat_max):
    """Plot Natural Earth land polygons clipped to the map window."""
    import json
    data_path = os.path.join(os.path.dirname(__file__),
                              "..", "data", "ne_110m_land.geojson")
    with open(data_path) as f:
        data = json.load(f)
    from matplotlib.patches import Polygon as MplPolygon

    def _emit_ring(coords):
        arr = np.asarray(coords)
        if (arr[:, 0].max() < lon_min or arr[:, 0].min() > lon_max
            or arr[:, 1].max() < lat_min or arr[:, 1].min() > lat_max):
            return
        poly = MplPolygon(arr, closed=True, facecolor="#f2e9d0",
                          edgecolor="#666666", linewidth=0.5, zorder=2)
        ax.add_patch(poly)

    for feat in data["features"]:
        geom = feat["geometry"]
        if geom["type"] == "Polygon":
            for ring in geom["coordinates"]:
                _emit_ring(ring)
        elif geom["type"] == "MultiPolygon":
            for poly in geom["coordinates"]:
                for ring in poly:
                    _emit_ring(ring)


def make_figure():
    apply_style()

    fig, ax = plt.subplots(figsize=(9.5, 9.5))

    # Map extent: 25°E – 53°E, 14°S – 22°N (covers Afar through southern EAR)
    lon_min, lon_max = 25, 53
    lat_min, lat_max = -14, 22

    # Ocean background
    ax.set_facecolor("#cfe6f5")
    ax.set_xlim(lon_min, lon_max)
    ax.set_ylim(lat_min, lat_max)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°)")
    ax.set_aspect("equal")

    # Real coastlines
    plot_real_coastlines(ax, lon_min, lon_max, lat_min, lat_max)

    # ── Rift axes ──
    rift_segments = [
        # Red Sea
        ([38.5, 40, 42.5, 43.5],          [21.5, 19, 15, 12.7]),
        # Gulf of Aden
        ([43.5, 47, 51],                   [12.7, 12.5, 12.2]),
        # Main Ethiopian Rift (Afar → Turkana)
        ([41.5, 39.5, 38.5, 37],           [11.5, 9, 6.5, 4]),
        # Eastern (Kenya) Rift
        ([37, 36.7, 36.4, 36, 35.5],       [4, 2, 0, -2, -4]),
        # Tanzanian → Malawi (southern branch eastern)
        ([35.5, 35, 34.5, 34.3],           [-4, -7, -10, -13]),
        # Western Rift (Albertine → Tanganyika)
        ([30, 30.3, 30.5, 30.0, 29.5],     [3, 1, -2, -4, -7]),
        ([29.5, 30, 30.3],                 [-7, -8.5, -10.5]),
        # Lake Kivu / Virunga
        ([29.5, 29.2],                     [-1, -2.5]),
    ]
    for lons, lats in rift_segments:
        ax.plot(lons, lats, color=PALETTE["verm"], lw=2.8, zorder=6)

    # Plate motion arrows (relative to Nubia)
    arrow_kw = dict(arrowstyle="->", color=PALETTE["blue"], lw=2.2)
    ax.annotate("", xy=(49, 2), xytext=(43.5, 2),
                arrowprops=arrow_kw, zorder=6)
    ax.text(46.5, 3, "Somalian plate\n~10 mm/yr", fontsize=9,
            color=PALETTE["blue"], ha="center")

    ax.annotate("", xy=(49, -10), xytext=(43.5, -10),
                arrowprops=arrow_kw, zorder=6)
    ax.text(46.5, -9, "Somalian\n~6 mm/yr", fontsize=9,
            color=PALETTE["blue"], ha="center")

    ax.annotate("", xy=(46, 18), xytext=(42, 14),
                arrowprops=arrow_kw, zorder=6)
    ax.text(44, 16.3, "Arabian\n~16 mm/yr",
            fontsize=9, color=PALETTE["blue"], ha="center")

    # Plate name labels
    plate_label_kw = dict(fontsize=11, fontweight="bold", color="#553300")
    ax.text(28, -10, "Nubian\nplate", ha="center", **plate_label_kw)
    ax.text(50, 19, "Arabian\nplate", ha="center", **plate_label_kw)
    ax.text(50, -5, "Somalian\nplate", ha="center", **plate_label_kw)

    # Major volcanic centres
    volcanoes = [
        ("Dabbahu",         40.5, 12.4, "right"),
        ("Erta Ale",        40.7, 13.6, "left"),
        ("Aluto",           38.8, 7.8,  "right"),
        ("Nyiragongo",      29.25, -1.5, "left"),
        ("Oldoinyo Lengai", 35.9, -2.75, "right"),
        ("Kilimanjaro",     37.35, -3.07, "right"),
        ("Mount Kenya",     37.31, -0.16, "right"),
    ]
    for name, lon, lat, side in volcanoes:
        ax.scatter(lon, lat, marker="^", s=85, c=PALETTE["orange"],
                   edgecolor="black", lw=0.8, zorder=7)
        dx = 0.35 if side == "right" else -0.35
        ha = "left" if side == "right" else "right"
        ax.annotate(name, xy=(lon, lat), xytext=(lon + dx, lat - 0.05),
                    fontsize=8, color=PALETTE["black"], zorder=8, ha=ha)

    # Rifting-continuum stage markers — green circles at key locations
    stage_markers = [
        ("Full spreading",      49, 12),    # Gulf of Aden
        ("Rift-to-spreading",   41.5, 13),  # Afar
        ("Mature rift",         38.5, 7.5), # Main Ethiopian
        ("Mature rift",         37, 0),     # Kenya
        ("Incipient",           34.3, -12), # Malawi
    ]
    for stage, lon, lat in stage_markers:
        ax.scatter([lon], [lat], marker="o", s=240, facecolors="none",
                    edgecolors=PALETTE["green"], lw=2.5, zorder=8)

    # Legend
    rift_line = plt.Line2D([0], [0], color=PALETTE["verm"], lw=2.8,
                            label="Rift axis / spreading boundary")
    motion_arrow = plt.Line2D([0], [0], color=PALETTE["blue"], lw=2.2,
                               label="Plate motion (rel. Nubia)")
    volc = plt.Line2D([0], [0], marker="^", color="w",
                       markerfacecolor=PALETTE["orange"],
                       markeredgecolor="black", markersize=10,
                       label="Volcanic centre")
    stage_marker = plt.Line2D([0], [0], marker="o", color="w",
                                markeredgecolor=PALETTE["green"],
                                markerfacecolor="none", markersize=12,
                                markeredgewidth=2,
                                label="Rifting-continuum stage marker")
    ax.legend(handles=[rift_line, motion_arrow, volc, stage_marker],
              loc="lower left", bbox_to_anchor=(0.0, 0.18),
              framealpha=0.95, fontsize=9)

    ax.set_title("East African Rift system — plates, rift axes, "
                  "and volcanic centres",
                  fontsize=12, loc="left")

    # Provenance note
    ax.text(0.98, 0.02,
             "Schematic; for the research-grade map see\n"
             "Biggs et al. 2021 Nat Comms 12:6881 (CC-BY 4.0)",
             transform=ax.transAxes, fontsize=8, ha="right", va="bottom",
             style="italic", color="#444444",
             bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                        edgecolor="none", alpha=0.9))

    return fig


if __name__ == "__main__":
    fig = make_figure()
    out = os.path.join(os.path.dirname(__file__), "..", "figures",
                       "F6_ear_system_map.png")
    save(fig, out)
    print(f"Wrote {out}")
