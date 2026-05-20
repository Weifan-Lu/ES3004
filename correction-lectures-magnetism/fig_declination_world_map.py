"""fig_declination_world_map.py — global magnetic declination, epoch 2026.

Computes declination D = atan2(B_e, B_n) on a global lat/lon grid using
the IGRF-13 spherical-harmonic model (via the ppigrf library). Plots
contours at 5-degree intervals: solid blue for D > 0 (compass points
east of true north), dashed vermilion for D < 0, heavy black for the
agonic line D = 0. Annotates four reference cities.

ESS 314, Lecture 23 §1 (Earth Magnetism — Geoscientific Question).

The IGRF-13 model is open access from NOAA NCEI / IAGA. The WMM (the
DoD World Magnetic Model) gives nearly identical declination values for
this epoch.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import ppigrf

from _style import COLORS, apply_style


REFERENCE_CITIES = [
    # (lat, lon, name, label-offset-deg)
    (47.65, -122.30, "Seattle", (-25, -8)),
    (61.22, -149.90, "Anchorage", (-30, 4)),
    (51.50, -0.13,   "London", (5, 5)),
    (35.68, 139.65,  "Tokyo", (5, -8)),
]

EPOCH = dt.datetime(2026, 1, 1)


def compute_declination_grid(lon: np.ndarray, lat: np.ndarray) -> np.ndarray:
    """Compute declination (deg) on a lon-lat meshgrid using IGRF-13."""
    LON, LAT = np.meshgrid(lon, lat)
    shp = LON.shape
    # ppigrf expects flat arrays.
    Be, Bn, Bu = ppigrf.igrf(LON.ravel(), LAT.ravel(),
                              np.zeros_like(LON.ravel()), EPOCH)
    # Declination: angle east of geographic north.
    D = np.degrees(np.arctan2(Be, Bn))
    return D.reshape(shp)


def compute_point_declination(lat: float, lon: float) -> float:
    Be, Bn, Bu = ppigrf.igrf(lon, lat, 0, EPOCH)
    return float(np.degrees(np.arctan2(Be, Bn))[0])


def main(out: Path) -> None:
    apply_style()

    # Grid (1 degree resolution gives smooth contours).
    lon = np.linspace(-180, 180, 361)
    lat = np.linspace(-80, 80, 161)
    D = compute_declination_grid(lon, lat)

    fig = plt.figure(figsize=(14, 7.6))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson(central_longitude=0))
    ax.set_global()
    ax.set_facecolor("#FAFAFA")

    # Gridlines for geographic reference (in lieu of coastlines, which need
    # to download Natural Earth shapefiles).
    gl = ax.gridlines(draw_labels=True,
                       linewidth=0.4, color=COLORS["lightgrey"],
                       linestyle=":", alpha=0.8,
                       xlocs=np.arange(-180, 181, 30),
                       ylocs=np.arange(-60, 61, 30))
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 9, "color": COLORS["grey"]}
    gl.ylabel_style = {"size": 9, "color": COLORS["grey"]}

    # Positive declination contours (D > 0) — solid blue.
    levels_pos = np.arange(5, 51, 5)
    cs_pos = ax.contour(lon, lat, D, levels=levels_pos,
                        colors=COLORS["blue"],
                        linestyles="-", linewidths=1.0,
                        transform=ccrs.PlateCarree(), zorder=4)
    ax.clabel(cs_pos, levels=cs_pos.levels[::2], fontsize=9, fmt="%d°",
              colors=COLORS["blue"])

    # Negative declination contours (D < 0) — dashed vermilion.
    levels_neg = np.arange(-50, 0, 5)
    cs_neg = ax.contour(lon, lat, D, levels=levels_neg,
                        colors=COLORS["vermilion"],
                        linestyles="--", linewidths=1.0,
                        transform=ccrs.PlateCarree(), zorder=4)
    ax.clabel(cs_neg, levels=cs_neg.levels[::2], fontsize=9, fmt="%d°",
              colors=COLORS["vermilion"])

    # Agonic line D = 0 — heavy black.
    cs_zero = ax.contour(lon, lat, D, levels=[0],
                         colors=COLORS["black"], linewidths=2.0,
                         transform=ccrs.PlateCarree(), zorder=5)
    ax.clabel(cs_zero, fontsize=10, fmt="0° (agonic)",
              colors=COLORS["black"])

    # Reference cities.
    for clat, clon, name, (dx, dy) in REFERENCE_CITIES:
        D_city = compute_point_declination(clat, clon)
        sign = "+" if D_city >= 0 else ""
        label = f"{name}\n$D = {sign}{D_city:.1f}^\\circ$"
        ax.plot(clon, clat, "o", color=COLORS["black"], markersize=7,
                transform=ccrs.PlateCarree(), zorder=10)
        ax.text(clon + dx, clat + dy, label,
                transform=ccrs.PlateCarree(),
                fontsize=10, fontweight="bold",
                color=COLORS["black"], ha="left", va="center",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                          edgecolor=COLORS["grey"], linewidth=0.6,
                          alpha=0.85),
                zorder=11)

    # Title.
    ax.set_title("Global magnetic declination — epoch 2026.0 (IGRF-13)",
                 fontsize=14, fontweight="bold", pad=12)

    # Legend stripe.
    legend_handles = [
        plt.Line2D([], [], color=COLORS["blue"], lw=1.6, linestyle="-",
                   label="$D > 0$  (compass east of true N)"),
        plt.Line2D([], [], color=COLORS["vermilion"], lw=1.6, linestyle="--",
                   label="$D < 0$  (compass west of true N)"),
        plt.Line2D([], [], color=COLORS["black"], lw=2.5,
                   label="$D = 0$  (agonic line)"),
    ]
    ax.legend(handles=legend_handles, loc="lower left", fontsize=11,
              framealpha=0.9)

    # Source / attribution.
    fig.text(0.5, 0.02,
             "Data: IGRF-13 model {Alken et al. 2021, Earth Planets Space 73:49}. "
             "Public domain (IAGA).",
             ha="center", fontsize=9, color=COLORS["grey"], style="italic")

    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir / "fig_declination_world_map.png")
    print("wrote", out_dir / "fig_declination_world_map.png")
