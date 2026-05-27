"""
F11_conus_bouguer_map.py

Continental United States Bouguer gravity anomaly map with rift, craton,
and orogenic-belt annotations.

The deployment target for this figure is the open-access pre-rendered
color-shaded map distributed in:
  USGS Fact Sheet 78-95 (Phillips, J. D., Duval, J. S. & Ambroziak, R. A.,
  1993). National geophysical data grids; gamma-ray, gravity, magnetic
  and topographic data for the conterminous United States. USGS Digital
  Data Series DDS-9 / Fact Sheet 78-95.
  Public domain (US Government work product).

For this script's fallback (used when the USGS PNG is unavailable in the
build sandbox), we synthesise the qualitative pattern of the CONUS Bouguer
field from the underlying tectonic provinces:
  - Strong Bouguer low over the Basin & Range and Rocky Mountains
    (thick crust + warm asthenosphere)
  - Moderate low over the Appalachians (orogenic root)
  - Neutral-to-mild values over the stable craton
  - Localised feature over the Midcontinent (Keweenawan) Rift
  - Positive offshore (oceanic crust, free-air rather than Bouguer in the
    USGS product)

For the published lecture, the build agent should download the USGS
figure directly and replace this fallback PNG with appropriate caption.

Coastlines: Natural Earth 110m via local cache.

Output: assets/figures/F11_conus_bouguer_map.png
License: CC-BY 4.0 (this script)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _ess314_style import apply_style, PALETTE, save

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap


def plot_real_coastlines(ax, lon_min, lon_max, lat_min, lat_max,
                          edgecolor="#222222", lw=0.6, zorder=4):
    """Plot Natural Earth land outlines clipped to window."""
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
        poly = MplPolygon(arr, closed=True, facecolor="none",
                          edgecolor=edgecolor, linewidth=lw, zorder=zorder)
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


def synth_bouguer_field(lon, lat):
    """
    Construct a synthetic CONUS Bouguer field on the given longitude/latitude
    grid (1D arrays). Returns a 2D anomaly array in mGal.

    The construction is intentionally simple: a regional baseline plus
    localised Gaussian anomalies positioned at the major tectonic provinces.
    """
    LON, LAT = np.meshgrid(lon, lat)
    Z = np.full_like(LON, -50.0, dtype=float)

    def gauss(lon0, lat0, amp, slon, slat):
        return amp * np.exp(-((LON - lon0) ** 2) / (2 * slon ** 2)
                              - ((LAT - lat0) ** 2) / (2 * slat ** 2))

    # Basin & Range Province — broad gravity low
    Z += gauss(-116, 39, -180, 5.5, 4)
    # Rocky Mountains — strong narrow low
    Z += gauss(-108, 40, -200, 3.0, 5)
    # Colorado Plateau — moderate low
    Z += gauss(-110, 37, -50, 2.5, 2.5)
    # Sierra Nevada / California batholith — moderate low
    Z += gauss(-119, 37, -90, 2.0, 3.5)
    # Cascade arc / Pacific NW (Siletzia high)
    Z += gauss(-122.5, 47, 60, 2.2, 2.5)
    # Stable interior craton (Great Plains) — mild positive
    Z += gauss(-100, 40, 30, 6.0, 5)
    # Midcontinent Rift (Keweenawan) — localised high
    Z += gauss(-91, 45, 75, 1.5, 3)
    Z += gauss(-92, 42, 55, 1.0, 2)
    # Appalachians — moderate low
    Z += gauss(-82, 36, -100, 4.0, 3.5)
    # Gulf Coast / offshore (positive, oceanic-ish)
    Z += gauss(-90, 27, 110, 8.0, 3)
    # Atlantic offshore positive
    Z += gauss(-75, 35, 80, 4, 4)

    return Z


def make_figure():
    apply_style()

    fig = plt.figure(figsize=(13, 8))
    ax = fig.add_subplot(111)

    lon_min, lon_max = -130, -65
    lat_min, lat_max = 22, 52

    lon = np.linspace(lon_min, lon_max, 521)
    lat = np.linspace(lat_min, lat_max, 241)
    Z = synth_bouguer_field(lon, lat)

    # Clip to reasonable range
    Z = np.clip(Z, -280, 120)

    # Build a USGS-style colormap: red (low) → yellow → green → blue (high)
    usgs_cmap = LinearSegmentedColormap.from_list("usgs_bg", [
        "#aa1010",   # deepest low
        "#dd5020",
        "#f0a040",
        "#f0d860",
        "#a0c860",
        "#3c9050",
        "#1c6080",
        "#0040a0",   # high
    ])

    im = ax.imshow(Z, extent=[lon_min, lon_max, lat_min, lat_max],
                    origin="lower", cmap=usgs_cmap, vmin=-280, vmax=120,
                    aspect="equal", zorder=2)

    # Coastlines
    plot_real_coastlines(ax, lon_min, lon_max, lat_min, lat_max)

    # Tectonic-province annotations
    annotations = [
        ("Basin & Range",         -117, 39.5, "#222222"),
        ("Rocky Mountains",       -108, 41.5, "#222222"),
        ("Siletzia /\nCascadia",  -122.5, 47, "#222222"),
        ("Craton",                -100, 41, "#222222"),
        ("Midcontinent\nRift",    -91, 45.5, "#222222"),
        ("Appalachians",          -82, 36, "#222222"),
        ("Gulf Coast",            -90, 27.5, "#222222"),
    ]
    for label, lon0, lat0, color in annotations:
        ax.annotate(label, xy=(lon0, lat0), xytext=(lon0, lat0),
                    fontsize=10, ha="center", va="center", color=color,
                    fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                                edgecolor="black", alpha=0.85, lw=0.7),
                    zorder=10)

    ax.set_xlim(lon_min, lon_max)
    ax.set_ylim(lat_min, lat_max)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°)")
    ax.set_title("Bouguer gravity anomaly — Conterminous United States "
                  "(schematic after USGS FS 78-95)",
                  fontsize=12, loc="left")

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.85, label="Bouguer anomaly (mGal)")

    # Provenance note
    ax.text(0.99, 0.02,
             "Schematic; for the research-grade map see\n"
             "USGS Fact Sheet 78-95 (Phillips et al. 1993; public domain)",
             transform=ax.transAxes, fontsize=8, ha="right", va="bottom",
             style="italic", color="#222222",
             bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                         edgecolor="none", alpha=0.92))

    return fig


if __name__ == "__main__":
    fig = make_figure()
    out = os.path.join(os.path.dirname(__file__), "..", "figures",
                       "F11_conus_bouguer_map.png")
    save(fig, out)
    print(f"Wrote {out}")
