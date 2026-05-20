"""fig_emag2_global.py — global lithospheric magnetic-anomaly map.

DEPLOYMENT (in the ESS 314 pixi environment with network access):
    The recommended path is to download the EMAG2 v3 NetCDF grid from
    NOAA NCEI (https://www.ncei.noaa.gov/products/earth-magnetic-anomaly-grid-2-arc-minute)
    and render it directly with cartopy + matplotlib. The dataset is
    public domain (US Government work).

SANDBOX (this script, run without the network path to NOAA):
    Generates a synthetic stand-in that has the same qualitative
    structure: striped patterns parallel to mid-ocean ridges, broad
    continental anomalies, color saturation at ±250 nT. The synthetic
    grid is enough to test layout, color scaling, and styling — replace
    with the real grid for deployment.

ESS 314, Lecture 25 §1 (Magnetic Anomalies — Geoscientific Question).
"""
from __future__ import annotations

import os
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

from _style import COLORS, apply_style


# Public-domain dataset URL — used when real-data path is available.
EMAG2_URL = (
    "https://www.ncei.noaa.gov/products/earth-magnetic-anomaly-grid-2-arc-minute"
)


def try_load_real_emag2(local_path: Path | None = None) -> np.ndarray | None:
    """Attempt to load the real EMAG2 v3 NetCDF grid from disk.

    In the deployment environment, point ``local_path`` to the downloaded
    EMAG2 NetCDF file. Returns (lon_1d, lat_1d, anomaly_2d) or None.
    """
    if local_path is None:
        env_path = os.environ.get("ESS314_EMAG2_PATH")
        if env_path:
            local_path = Path(env_path)
    if local_path is None or not local_path.exists():
        return None
    try:
        import xarray as xr
        ds = xr.open_dataset(local_path)
        # EMAG2 v3 has variable name 'z' or 'anomaly' depending on packaging.
        var_name = "z" if "z" in ds.variables else list(ds.data_vars)[0]
        anomaly = ds[var_name].values
        lon = ds["lon"].values if "lon" in ds.variables else ds["x"].values
        lat = ds["lat"].values if "lat" in ds.variables else ds["y"].values
        return lon, lat, anomaly
    except Exception as exc:  # pragma: no cover
        print(f"[note] could not read EMAG2 from {local_path}: {exc}")
        return None


def synthesize_emag2(lon: np.ndarray, lat: np.ndarray) -> np.ndarray:
    """Build a synthetic global anomaly grid that captures EMAG2-like patterns.

    Three signal classes added together:
      1. Mid-ocean ridge stripes: alternating ±polarity bands running
         roughly N-S across the Pacific, NE-SW across the Atlantic, and
         varying across the Indian Ocean.
      2. Long-wavelength continental anomalies: large Gaussian bumps over
         major shields (Canadian, African, Australian, Antarctic).
      3. Some additional smaller-scale noise for texture.

    Output is in nT, saturating at ~±300 nT. NOT a substitute for the
    real dataset.
    """
    LON, LAT = np.meshgrid(lon, lat)
    anomaly = np.zeros_like(LON)

    # ---- 1. Mid-ocean ridge stripes ----
    # Pacific (E-W ridge stripes, oriented roughly N-S): East Pacific Rise.
    # Stripes run parallel to ridge (N-S), oscillate in x.
    in_pacific = ((LON > 100) | (LON < -70)) & (np.abs(LAT) < 60)
    pac_x = np.where(LON < -70, LON + 110, LON - 180)  # distance from EPR
    pac_stripes = 220 * np.sin(2 * np.pi * pac_x / 4.5) * np.exp(-((LAT - (-30)) / 60) ** 2)
    anomaly = np.where(in_pacific, anomaly + pac_stripes * 0.7, anomaly)

    # Atlantic stripes (running roughly N-S, mid-Atlantic ridge ~ -30°W).
    in_atlantic = ((LON > -75) & (LON < 20)) & (np.abs(LAT) < 50)
    atl_x = LON + 30
    atl_stripes = 200 * np.sin(2 * np.pi * atl_x / 3.5) * np.exp(-((LAT - 0) / 50) ** 2)
    anomaly = np.where(in_atlantic, anomaly + atl_stripes * 0.7, anomaly)

    # Indian Ocean.
    in_indian = (LON > 20) & (LON < 100) & (LAT < 30)
    ind_x = LON - 80
    ind_stripes = 160 * np.sin(2 * np.pi * ind_x / 4.0) * np.exp(-((LAT + 20) / 40) ** 2)
    anomaly = np.where(in_indian, anomaly + ind_stripes * 0.6, anomaly)

    # ---- 2. Long-wavelength continental anomalies ----
    def gaussian2d(lon0, lat0, amplitude, sigma_lon, sigma_lat):
        return amplitude * np.exp(-(((LON - lon0) / sigma_lon) ** 2 +
                                     ((LAT - lat0) / sigma_lat) ** 2))

    # Canadian Shield — large positive.
    anomaly += gaussian2d(lon0=-95, lat0=58, amplitude=180,
                          sigma_lon=20, sigma_lat=12)
    # Mid-Continent Rift (positive linear feature through Minnesota/Iowa).
    rift_strength = 220 * np.exp(-((LON + 92) / 4) ** 2) \
                          * np.exp(-((LAT - 45) / 8) ** 2)
    anomaly += rift_strength
    # African shield (broad positive over Central Africa).
    anomaly += gaussian2d(lon0=20, lat0=5, amplitude=130,
                          sigma_lon=18, sigma_lat=15)
    # West Africa negative.
    anomaly += gaussian2d(lon0=-5, lat0=18, amplitude=-110,
                          sigma_lon=12, sigma_lat=10)
    # Australian shield.
    anomaly += gaussian2d(lon0=130, lat0=-22, amplitude=150,
                          sigma_lon=15, sigma_lat=10)
    # Antarctic.
    anomaly += gaussian2d(lon0=80, lat0=-75, amplitude=100,
                          sigma_lon=40, sigma_lat=8)
    # Vredefort impact (South Africa).
    anomaly += gaussian2d(lon0=27, lat0=-27, amplitude=80,
                          sigma_lon=2, sigma_lat=2)
    # Sudbury (Canada).
    anomaly += gaussian2d(lon0=-81, lat0=46, amplitude=70,
                          sigma_lon=1.5, sigma_lat=1.5)
    # Pacific Northwest region — small positive (Cascade arc / Siletzia).
    anomaly += gaussian2d(lon0=-122, lat0=47, amplitude=60,
                          sigma_lon=3, sigma_lat=2.5)

    # ---- 3. Smaller-scale noise for texture (smoothed) ----
    np.random.seed(2024)
    noise = np.random.randn(*LON.shape)
    # Crude box-smoothing.
    from scipy.ndimage import gaussian_filter
    smooth_noise = gaussian_filter(noise, sigma=2.0) * 60
    anomaly += smooth_noise

    return anomaly


def main(out: Path) -> None:
    apply_style()

    # Either real or synthetic data.
    real = try_load_real_emag2()
    if real is None:
        print("[note] using synthetic placeholder; real EMAG2 not available "
              "in this environment.")
        lon = np.linspace(-180, 180, 361)
        lat = np.linspace(-80, 80, 161)
        anomaly = synthesize_emag2(lon, lat)
        synthetic = True
    else:
        lon, lat, anomaly = real
        synthetic = False

    fig = plt.figure(figsize=(14, 7.8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson(central_longitude=0))
    ax.set_global()
    ax.set_facecolor("#FAFAFA")

    # Gridlines.
    gl = ax.gridlines(draw_labels=True,
                       linewidth=0.4, color=COLORS["lightgrey"],
                       linestyle=":", alpha=0.8,
                       xlocs=np.arange(-180, 181, 30),
                       ylocs=np.arange(-60, 61, 30))
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 9, "color": COLORS["grey"]}
    gl.ylabel_style = {"size": 9, "color": COLORS["grey"]}

    # Diverging colormap, saturating at ±250 nT.
    cmap = plt.get_cmap("RdBu_r").copy()
    pm = ax.pcolormesh(lon, lat, anomaly,
                        transform=ccrs.PlateCarree(),
                        cmap=cmap, shading="auto",
                        vmin=-250, vmax=250)

    # Colour bar.
    cbar = fig.colorbar(pm, ax=ax, orientation="horizontal", pad=0.06,
                        shrink=0.55, aspect=40)
    cbar.set_label("Lithospheric anomaly $\\Delta F$  (nT)", fontsize=11)
    cbar.ax.tick_params(labelsize=10)

    # Annotation: PNW inset box.
    ax.plot([-130, -120, -120, -130, -130], [44, 44, 49, 49, 44],
             color=COLORS["green"], lw=2.0,
             transform=ccrs.PlateCarree(), zorder=8)
    ax.annotate("Pacific Northwest",
                xy=(-125, 49), xytext=(-100, 65),
                xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
                fontsize=10, fontweight="bold", color=COLORS["green"],
                arrowprops=dict(arrowstyle="->", color=COLORS["green"], lw=1.0))

    # Title and source note.
    title_label = ("EMAG2 v3 — Global Lithospheric Magnetic Anomaly  "
                    "(public-domain dataset, NOAA NCEI / CIRES)")
    if synthetic:
        title_label = ("Global Lithospheric Magnetic Anomaly — "
                        "SYNTHETIC PLACEHOLDER  (replace with EMAG2 v3 for deployment)")
    ax.set_title(title_label, fontsize=13, fontweight="bold", pad=12)

    fig.text(0.5, 0.04,
             "Data source: NOAA NCEI EMAG2 v3 — Meyer, Saltus & Chulliat (2017). "
             "Public domain (US Government work).",
             ha="center", fontsize=9, color=COLORS["grey"], style="italic")

    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir / "fig_emag2_global.png")
    print("wrote", out_dir / "fig_emag2_global.png")
