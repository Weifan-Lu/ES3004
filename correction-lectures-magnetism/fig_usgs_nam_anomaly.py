"""fig_usgs_nam_anomaly.py — USGS Magnetic Anomaly Map of North America.

DEPLOYMENT (in the ESS 314 pixi environment with network access):
    The recommended path is to download the USGS Magnetic Anomaly Map of
    North America (Bankey et al. 2002) GeoTIFF from
    https://mrdata.usgs.gov/magnetic/ and render it with cartopy + rasterio.
    The dataset is public domain (US Government work).

SANDBOX (this script, run without USGS network path):
    Generates a synthetic stand-in that has the same qualitative structure:
    Canadian Shield positive anomaly, Mid-Continent Rift linear positive,
    Cordilleran complexity, Coastal Plain quieter. The synthetic grid is
    enough to test layout and styling — replace with real data for
    deployment.

ESS 314, Lecture 25 §7.1 (Magnetic Anomalies — Continental scale).
"""
from __future__ import annotations

import os
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

from _style import COLORS, apply_style


USGS_NAM_URL = "https://mrdata.usgs.gov/magnetic/"


def try_load_real_usgs_nam(local_path: Path | None = None):
    """Attempt to load the USGS NAm anomaly GeoTIFF from disk."""
    if local_path is None:
        env_path = os.environ.get("ESS314_USGS_NAM_PATH")
        if env_path:
            local_path = Path(env_path)
    if local_path is None or not local_path.exists():
        return None
    try:
        import rasterio
        with rasterio.open(local_path) as src:
            anomaly = src.read(1)
            transform = src.transform
            # Build lon/lat arrays from the affine transform.
            n_y, n_x = anomaly.shape
            xs = transform * (np.arange(n_x), np.zeros(n_x))
            ys = transform * (np.zeros(n_y), np.arange(n_y))
            return xs[0], ys[1], anomaly, src.crs
    except Exception as exc:  # pragma: no cover
        print(f"[note] could not read USGS NAm from {local_path}: {exc}")
        return None


def synthesize_nam(lon: np.ndarray, lat: np.ndarray) -> np.ndarray:
    """Synthetic North American anomaly with the major regional features.

    Features:
      1. Canadian Shield positive (Archean / Paleoproterozoic crust).
      2. Mid-Continent Rift (1.1 Ga failed rift), strong linear feature
         curving through Minnesota / Iowa down to Kansas.
      3. Appalachian fabric (NE-SW linear trends in the eastern US).
      4. Cordilleran complexity (PNW, Cascades, Idaho Batholith, Sierra).
      5. Coastal Plain quiet zone.
      6. Mexican volcanic belt and Yucatan.
    """
    LON, LAT = np.meshgrid(lon, lat)
    anomaly = np.zeros_like(LON)

    def gaussian2d(lon0, lat0, amplitude, sigma_lon, sigma_lat, rot_deg=0):
        # Allow rotated Gaussians for linear features.
        theta = np.radians(rot_deg)
        c, s = np.cos(theta), np.sin(theta)
        dLON = LON - lon0
        dLAT = LAT - lat0
        u = c * dLON + s * dLAT
        v = -s * dLON + c * dLAT
        return amplitude * np.exp(-((u / sigma_lon) ** 2 + (v / sigma_lat) ** 2))

    # Canadian Shield — strong positive blob covering most of central / eastern Canada.
    anomaly += gaussian2d(-95, 58, 350, 18, 12)
    anomaly += gaussian2d(-75, 55, 280, 12, 8)
    anomaly += gaussian2d(-105, 60, 220, 10, 8)
    # Hudson Bay shield extension.
    anomaly += gaussian2d(-85, 60, 200, 8, 5)

    # Mid-Continent Rift — strong linear positive curving south.
    # Approximate path: (-92, 47) → (-91, 45) → (-94, 42) → (-97, 38)
    rift_path = [(-92, 47), (-91, 45), (-94, 42), (-97, 38), (-100, 34)]
    for lon0, lat0 in rift_path:
        anomaly += gaussian2d(lon0, lat0, 400, 1.8, 4, rot_deg=15)

    # Appalachian fabric — linear NE-SW positive trends in the eastern US.
    for lon0, lat0 in [(-78, 38), (-80, 35), (-82, 32)]:
        anomaly += gaussian2d(lon0, lat0, 150, 4, 1.5, rot_deg=50)

    # Cordilleran — complex pattern (positive over Cascades + Idaho Batholith).
    anomaly += gaussian2d(-122, 46, 200, 2.5, 3)   # Cascades / Siletzia
    anomaly += gaussian2d(-115, 44, 180, 4, 5)     # Idaho Batholith
    anomaly += gaussian2d(-119, 38, 160, 3, 4)     # Sierra
    anomaly += gaussian2d(-108, 36, -120, 3, 3)    # Colorado Plateau (quiet/negative)
    # Cordilleran linear NW-SE fabric for grain.
    for k in range(8):
        lat0 = 32 + k * 2
        anomaly += gaussian2d(-116 + 0.5 * k, lat0, 100 * (-1) ** k,
                              1.2, 1.0, rot_deg=20)

    # Coastal Plain (quiet zone) — broad weak negative SE of Appalachians.
    anomaly += gaussian2d(-83, 30, -80, 8, 4)

    # Mexican Volcanic Belt and Yucatan/Chicxulub.
    anomaly += gaussian2d(-99, 19, 130, 4, 2)      # TMVB
    anomaly += gaussian2d(-89, 21, -200, 1.5, 1.5)  # Chicxulub (negative ring)
    anomaly += gaussian2d(-89, 21, 180, 0.5, 0.5)  # Chicxulub central peak

    # Small-scale noise for texture.
    from scipy.ndimage import gaussian_filter
    np.random.seed(2024)
    smooth_noise = gaussian_filter(np.random.randn(*LON.shape), sigma=1.5) * 70
    anomaly += smooth_noise

    return anomaly


def main(out: Path) -> None:
    apply_style()

    real = try_load_real_usgs_nam()
    if real is None:
        print("[note] using synthetic placeholder; real USGS NAm data not "
              "available in this environment.")
        lon = np.linspace(-170, -55, 461)
        lat = np.linspace(15, 75, 241)
        anomaly = synthesize_nam(lon, lat)
        synthetic = True
    else:
        lon, lat, anomaly, _ = real
        synthetic = False

    fig = plt.figure(figsize=(13, 9))
    ax = fig.add_subplot(
        1, 1, 1,
        projection=ccrs.LambertConformal(central_longitude=-100,
                                          central_latitude=40))
    ax.set_extent([-130, -65, 20, 60], crs=ccrs.PlateCarree())
    ax.set_facecolor("#FAFAFA")

    # Gridlines for geographic reference (no coastlines).
    gl = ax.gridlines(draw_labels=True,
                       linewidth=0.5, color=COLORS["lightgrey"],
                       linestyle=":", alpha=0.7,
                       xlocs=np.arange(-180, -50, 15),
                       ylocs=np.arange(20, 75, 10))
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 10, "color": COLORS["grey"]}
    gl.ylabel_style = {"size": 10, "color": COLORS["grey"]}

    # Diverging colourmap; saturate at ±500 nT.
    pm = ax.pcolormesh(lon, lat, anomaly,
                        transform=ccrs.PlateCarree(),
                        cmap=plt.get_cmap("RdBu_r"),
                        shading="auto",
                        vmin=-500, vmax=500)

    cbar = fig.colorbar(pm, ax=ax, orientation="horizontal", pad=0.06,
                        shrink=0.55, aspect=40)
    cbar.set_label("Magnetic anomaly $\\Delta F$  (nT)", fontsize=11)
    cbar.ax.tick_params(labelsize=10)

    # Annotate key features.
    annotations = [
        (-95, 58, "Canadian\nShield", 0, 0),
        (-93, 44, "Mid-Continent\nRift", 18, 4),
        (-122, 47, "Pacific\nNW", -20, 6),
        (-78, 36, "Appalachians", 8, -6),
        (-89, 21, "Chicxulub", 0, -6),
    ]
    for lon0, lat0, txt, dx, dy in annotations:
        ax.annotate(
            txt, xy=(lon0, lat0), xytext=(lon0 + dx, lat0 + dy),
            xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
            fontsize=10, fontweight="bold", color=COLORS["black"],
            ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                      edgecolor=COLORS["grey"], lw=0.6, alpha=0.85),
            arrowprops=dict(arrowstyle="->",
                            color=COLORS["grey"], lw=0.8),
            zorder=10,
        )

    # Title.
    title_label = ("Magnetic Anomaly Map of North America  "
                    "(USGS, public domain)")
    if synthetic:
        title_label = ("Magnetic Anomaly Map of North America — "
                        "SYNTHETIC PLACEHOLDER  (replace with USGS Bankey et al. 2002)")
    ax.set_title(title_label, fontsize=13, fontweight="bold", pad=14)

    fig.text(0.5, 0.04,
             "Data source: USGS — Bankey et al. (2002), Magnetic Anomaly Map of "
             "North America (https://mrdata.usgs.gov/magnetic/). Public domain.",
             ha="center", fontsize=9, color=COLORS["grey"], style="italic")

    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir / "fig_usgs_nam_anomaly.png")
    print("wrote", out_dir / "fig_usgs_nam_anomaly.png")
