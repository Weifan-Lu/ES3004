"""F13 — Siletzia potential-fields signature, Puget Lowland.

Two-panel real-data figure built entirely from public-domain US Government
grids (no Wiley/AGU figures, no synthetic data):

  (a) Isostatic residual gravity anomaly (USGS):
        https://mrdata.usgs.gov/geophysics/gravity/USgrv_iso_SDD_geog.tif
      Isostatic residual = Complete Bouguer Anomaly minus the long-wavelength
      isostatic regional, so it emphasises upper-crustal density variations —
      directly analogous to the residual gravity panel in Anderson et al.
      (2024, *Tectonics*, doi:10.1029/2022TC007720).

  (b) Magnetic anomaly, high-pass filtered at 500 km (USGS):
        https://mrdata.usgs.gov/magnetic/USmag_hp500.zip
      Bankey et al. (2002) North American magnetic anomaly compilation,
      reduced-to-pole, with wavelengths >500 km removed — the standard
      product for mapping crustal magnetic sources.

Both grids are US Government works (public domain). On first run the script
downloads the two grids into ``assets/data/`` (~50 MB total), crops to the
Puget Lowland window, reprojects the magnetic grid from its native
Transverse-Mercator CRS to WGS84, and writes
``assets/figures/F13_siletzia_potential_fields.png``.

ESS 314, Lecture 26 §5 (Siletzia, an in-between case).
"""
from __future__ import annotations

import json
import sys
import urllib.request
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import rasterio
from rasterio.transform import from_bounds as transform_from_bounds
from rasterio.warp import Resampling, reproject
from rasterio.windows import from_bounds

sys.path.append(str(Path(__file__).parent))
from _style import apply_style  # noqa: E402

# Puget Lowland window (lat/lon, WGS84).
LON_MIN, LON_MAX = -124.5, -121.0
LAT_MIN, LAT_MAX = 46.5, 49.0

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "assets" / "data"
FIG = REPO / "assets" / "figures" / "F13_siletzia_potential_fields.png"

GRAV_URL = "https://mrdata.usgs.gov/geophysics/gravity/USgrv_iso_SDD_geog.tif"
GRAV_TIF = DATA / "USgrv_iso_SDD_geog.tif"
MAG_URL = "https://mrdata.usgs.gov/magnetic/USmag_hp500.zip"
MAG_ZIP = DATA / "USmag_hp500.zip"
MAG_DIR = DATA / "usmag_hp500"
COAST_GEOJSON = DATA / "ne_110m_coastline.geojson"
COAST_URL = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    "master/geojson/ne_110m_coastline.geojson"
)


def _download(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"[F13] fetching {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "ess314/1.0"})
    with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as fh:
        fh.write(r.read())


def _ensure_data() -> None:
    _download(GRAV_URL, GRAV_TIF)
    if not MAG_DIR.exists():
        _download(MAG_URL, MAG_ZIP)
        with zipfile.ZipFile(MAG_ZIP) as zf:
            zf.extractall(DATA)
    _download(COAST_URL, COAST_GEOJSON)


def load_gravity_rgb_window() -> tuple[np.ndarray, float, float, float, float]:
    """Crop the USGS isostatic-residual gravity RGB GeoTIFF to the Puget window.

    The mrdata.usgs.gov GeoTIFF is a 3-band styled image (the official USGS
    colorized visualization, linear stretch over -225 to +105 mGal — see
    USgrv_iso_SDD_geog_meta.txt). The raw grid values live in a Geosoft .grd
    file that GDAL cannot read without a proprietary driver, so we present
    the styled image as-published.
    """
    with rasterio.open(GRAV_TIF) as src:
        win = from_bounds(LON_MIN, LAT_MIN, LON_MAX, LAT_MAX, transform=src.transform)
        rgb = src.read(window=win)  # shape (bands, rows, cols)
        wt = src.window_transform(win)
    rgb = np.transpose(rgb, (1, 2, 0))  # rows, cols, bands
    n_y, n_x, _ = rgb.shape
    # Extent for imshow (left, right, bottom, top) in lon/lat.
    left = wt.c
    right = wt.c + wt.a * n_x
    top = wt.f
    bottom = wt.f + wt.e * n_y
    return rgb, left, right, bottom, top


def load_magnetic_window(out_pixels: int = 600) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Reproject the Bankey-2002 high-pass magnetic grid to a WGS84 window."""
    aspect = (LAT_MAX - LAT_MIN) / (LON_MAX - LON_MIN)
    n_x = out_pixels
    n_y = max(2, int(round(out_pixels * aspect)))
    dst_transform = transform_from_bounds(LON_MIN, LAT_MIN, LON_MAX, LAT_MAX, n_x, n_y)
    dst = np.full((n_y, n_x), np.nan, dtype="float32")
    with rasterio.open(MAG_DIR) as src:
        reproject(
            source=rasterio.band(src, 1),
            destination=dst,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=dst_transform,
            dst_crs="EPSG:4326",
            resampling=Resampling.bilinear,
            src_nodata=src.nodata,
            dst_nodata=np.nan,
        )
    cols = np.arange(n_x) + 0.5
    rows = np.arange(n_y) + 0.5
    lons = dst_transform.a * cols + dst_transform.c
    lats = dst_transform.e * rows + dst_transform.f
    return lons, lats, dst


def _draw_coast(ax) -> None:
    if not COAST_GEOJSON.exists():
        return
    with open(COAST_GEOJSON) as fh:
        gj = json.load(fh)
    for feat in gj["features"]:
        geom = feat["geometry"]
        coords_list = geom["coordinates"]
        if geom["type"] == "LineString":
            coords_list = [coords_list]
        for ring in coords_list:
            arr = np.asarray(ring)
            if arr.ndim != 2:
                continue
            ax.plot(
                arr[:, 0],
                arr[:, 1],
                color="black",
                linewidth=0.8,
                solid_capstyle="round",
                zorder=4,
            )


CITIES = [
    ("Seattle", -122.33, 47.61),
    ("Tacoma", -122.45, 47.25),
    ("Olympia", -122.90, 47.04),
    ("Everett", -122.20, 47.98),
]


def _annotate(ax) -> None:
    _draw_coast(ax)
    for name, lon, lat in CITIES:
        ax.plot(lon, lat, marker="o", color="black", markersize=3.5, zorder=5)
        ax.annotate(
            name,
            (lon, lat),
            xytext=(4, 3),
            textcoords="offset points",
            fontsize=8,
            color="black",
            zorder=6,
        )
    # Approximate Seattle Fault Zone trace (E–W through Seattle).
    ax.plot(
        [-122.6, -121.9],
        [47.58, 47.58],
        color="black",
        linewidth=1.2,
        linestyle="--",
        zorder=4,
    )
    ax.annotate(
        "Seattle Fault Zone",
        (-122.55, 47.60),
        xytext=(0, 6),
        textcoords="offset points",
        fontsize=7,
        style="italic",
        color="black",
        zorder=6,
    )
    ax.set_xlim(LON_MIN, LON_MAX)
    ax.set_ylim(LAT_MIN, LAT_MAX)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    ax.set_aspect(1.0 / np.cos(np.deg2rad(0.5 * (LAT_MIN + LAT_MAX))))


def main() -> None:
    apply_style()
    _ensure_data()

    rgb, g_left, g_right, g_bottom, g_top = load_gravity_rgb_window()
    m_lon, m_lat, m_data = load_magnetic_window()

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.6))

    # (a) Isostatic residual gravity — USGS styled RGB image (as published).
    ax = axes[0]
    ax.imshow(
        rgb,
        extent=(g_left, g_right, g_bottom, g_top),
        origin="upper",
        interpolation="nearest",
        zorder=2,
    )
    _annotate(ax)
    ax.set_title("(a) Isostatic residual gravity — USGS styled image\n"
                 "(linear stretch over -225 to +105 mGal)")

    # (b) High-pass magnetic anomaly — real nT, diverging colormap.
    ax = axes[1]
    m_abs = np.nanpercentile(np.abs(m_data), 98) if np.isfinite(m_data).any() else 1.0
    vmax_m = float(np.clip(m_abs, 50, 1500))
    mesh = ax.pcolormesh(
        m_lon,
        m_lat,
        m_data,
        cmap="RdBu_r",
        vmin=-vmax_m,
        vmax=vmax_m,
        shading="auto",
        zorder=2,
    )
    cbar = fig.colorbar(mesh, ax=ax, orientation="vertical", pad=0.02, shrink=0.85)
    cbar.set_label("Magnetic anomaly, HP-500 km (nT)")
    _annotate(ax)
    ax.set_title("(b) High-pass magnetic anomaly — Bankey et al. (2002)")

    fig.suptitle(
        "Siletzia geophysical signature, Puget Lowland — USGS public-domain grids",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[F13] wrote {FIG}")


if __name__ == "__main__":
    main()
