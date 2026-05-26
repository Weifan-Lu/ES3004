"""F2 — Mid-Atlantic transect from real bathymetry (GMRT grid service).

Downloads a thin 30°N strip of GMRT (Global Multi-Resolution Topography)
elevation as a netCDF subset via the public GridServer REST API, then
plots the seafloor profile from West Africa to Cape Hatteras.

Output: ``assets/figures/F2_matlantic_transect.png``.

Provenance: Ryan, W.B.F. et al. (2009), G-Cubed, GMRT
doi:10.1029/2008GC002332.
"""
from __future__ import annotations

import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from _style import COLORS, apply_style

apply_style()

OUT = Path(__file__).resolve().parents[1] / "figures" / "F2_matlantic_transect.png"
CACHE = Path(__file__).resolve().parents[1] / "data" / "gmrt_atlantic_30N.nc"
CACHE.parent.mkdir(parents=True, exist_ok=True)

LAT_TARGET = 30.0
LON_W, LON_E = -75.0, -10.0
LAT_S, LAT_N = LAT_TARGET - 0.25, LAT_TARGET + 0.25

GMRT_URL = (
    "https://www.gmrt.org/services/GridServer?"
    f"north={LAT_N}&south={LAT_S}&east={LON_E}&west={LON_W}"
    "&layer=topo&format=netcdf&resolution=med"
)


def _fetch() -> Path:
    if CACHE.exists() and CACHE.stat().st_size > 10_000:
        return CACHE
    print(f"[F2] fetching GMRT subset: {GMRT_URL}")
    req = urllib.request.Request(GMRT_URL, headers={"User-Agent": "ess314/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        CACHE.write_bytes(r.read())
    return CACHE


def main() -> None:
    import xarray as xr

    path = _fetch()
    ds = xr.open_dataset(path)
    # GMRT GMT-binary netCDF: x_range, y_range, dimension, z (flat).
    x0, x1 = ds["x_range"].values
    y0, y1 = ds["y_range"].values
    nx, ny = ds["dimension"].values.astype(int)
    z_flat = ds["z"].values.reshape((ny, nx))
    # GMT pixel registration: rows go from y1 (top) to y0 (bottom)
    lats = np.linspace(y1, y0, ny)
    lons = np.linspace(x0, x1, nx)
    # Pick the row nearest to the target latitude.
    i = int(np.argmin(np.abs(lats - LAT_TARGET)))
    elev = z_flat[i, :]
    lon = lons
    depth_km = -elev / 1000.0

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between(lon, depth_km, depth_km.max() + 1,
                    color=COLORS["lightgrey"], alpha=0.6, zorder=1)
    ax.plot(lon, depth_km, color=COLORS["blue"], lw=1.2, zorder=2)

    # Mark the Mid-Atlantic Ridge axis. At 30°N the spreading centre sits
    # near -41.5°E (between the Atlantis and Kane fracture zones); the
    # shallow spikes on the flanks are seamounts, not the axis.
    MAR_LON = -41.5
    i_mar = int(np.argmin(np.abs(lon - MAR_LON)))
    mar_lon = lon[i_mar]
    mar_depth = depth_km[i_mar]
    ax.annotate(
        "Mid-Atlantic Ridge axis",
        xy=(mar_lon, mar_depth),
        xytext=(mar_lon - 8, mar_depth - 1.4),
        arrowprops=dict(arrowstyle="->", color=COLORS["vermilion"], lw=1.2),
        color=COLORS["vermilion"], fontsize=11,
    )
    # Label the shallow flank features as seamounts (not the ridge)
    ax.text(0.985, 0.04, "shallow spikes on the flanks ≈ seamounts",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=9, color=COLORS["grey"], style="italic")

    ax.set_ylim(6.5, -0.5)  # depth axis: deep at bottom, NO invert_yaxis
    ax.set_xlim(LON_W, LON_E)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Depth (km below sea level)")
    ax.set_title("Mid-Atlantic transect at 30°N — GMRT (Ryan et al. 2009)",
                 fontsize=12)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, bbox_inches="tight")
    print(f"[F2] wrote {OUT}")


if __name__ == "__main__":
    main()
