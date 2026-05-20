"""fig_seattle_fault_aeromag.py — Seattle Fault Zone aeromagnetic survey.

DEPLOYMENT (in the ESS 314 pixi environment with network access):
    Download the USGS Puget Lowland aeromagnetic compilation from
    https://mrdata.usgs.gov/magnetic/ (search Puget Sound / Seattle).
    Reference paper: Blakely, Wells, Weaver & Johnson (2002), GSA Bulletin.

SANDBOX (this script, run without USGS network path):
    Generates a synthetic stand-in that captures the qualitative pattern
    of the SFZ aeromagnetic anomaly: a 30-km east-west zone of positive
    anomaly across central Puget Sound and downtown Seattle, with a sharp
    gradient on its north side (the fault trace).

ESS 314, Lecture 25 §7.2 (Magnetic Anomalies — Local scale).
"""
from __future__ import annotations

import os
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

from _style import COLORS, apply_style


def try_load_real_seattle(local_path: Path | None = None):
    if local_path is None:
        env_path = os.environ.get("ESS314_SEATTLE_FAULT_PATH")
        if env_path:
            local_path = Path(env_path)
    if local_path is None or not local_path.exists():
        return None
    try:
        import rasterio
        with rasterio.open(local_path) as src:
            anomaly = src.read(1)
            transform = src.transform
            n_y, n_x = anomaly.shape
            xs = transform * (np.arange(n_x), np.zeros(n_x))
            ys = transform * (np.zeros(n_y), np.arange(n_y))
            return xs[0], ys[1], anomaly
    except Exception as exc:  # pragma: no cover
        print(f"[note] could not read Seattle Fault data from {local_path}: {exc}")
        return None


def synthesize_seattle(lon: np.ndarray, lat: np.ndarray) -> np.ndarray:
    """Synthetic SFZ aeromagnetic anomaly.

    The SFZ is a south-dipping reverse fault with Crescent Formation
    (Eocene basalts) uplifted on the hanging wall (south side). Aeromagnetic
    signature is a 30-km E-W zone of strong positive anomaly with a sharp
    gradient on the north side marking the fault trace.
    """
    LON, LAT = np.meshgrid(lon, lat)
    anomaly = np.zeros_like(LON)

    # Fault trace: roughly east-west at lat = 47.58 N, lon -122.55 to -122.20.
    # Hanging-wall (south side) shows strong positive anomaly.
    fault_lat = 47.58
    sigma_north = 0.05   # tight gradient on north (fault edge)
    sigma_south = 0.10   # broader on south side

    # Asymmetric "fault edge" signature: positive south of fault, sharp drop on north.
    dist_from_fault = LAT - fault_lat
    # Use a step-like response.
    amplitude = 450  # nT — strong anomaly peak
    south_side = np.where(dist_from_fault < 0,
                          amplitude * np.exp(-(dist_from_fault / sigma_south) ** 2),
                          0)
    # On the north side, drop sharply (negative or near-zero).
    north_side = np.where(dist_from_fault >= 0,
                          amplitude * 0.2 * np.exp(-(dist_from_fault / sigma_north) ** 2)
                          - 50 * np.exp(-(dist_from_fault / 0.02) ** 2),
                          0)
    anomaly += south_side + north_side

    # Vary amplitude along strike — Crescent Formation thickness varies.
    along_strike = (np.cos(2 * np.pi * (LON - (-122.45)) / 0.45)
                    + 0.5 * np.cos(2 * np.pi * (LON - (-122.4)) / 0.15)) * 0.4
    anomaly *= (1 + along_strike)

    # Background regional + Puget Sound basin sediments (negative).
    anomaly += -40 * np.exp(-((LAT - 47.62) / 0.10) ** 2) * \
                       np.exp(-((LON + 122.35) / 0.18) ** 2)

    # Smaller-scale geological noise.
    from scipy.ndimage import gaussian_filter
    np.random.seed(2024)
    noise = gaussian_filter(np.random.randn(*LON.shape), sigma=2.0) * 40
    anomaly += noise

    return anomaly


def main(out: Path) -> None:
    apply_style()

    real = try_load_real_seattle()
    if real is None:
        print("[note] using synthetic placeholder; real Seattle Fault data not "
              "available in this environment.")
        lon = np.linspace(-122.65, -122.15, 200)
        lat = np.linspace(47.40, 47.75, 180)
        anomaly = synthesize_seattle(lon, lat)
        synthetic = True
    else:
        lon, lat, anomaly = real
        synthetic = False

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([-122.65, -122.15, 47.40, 47.75], crs=ccrs.PlateCarree())
    ax.set_facecolor("#FAFAFA")

    # Gridlines for geographic reference.
    gl = ax.gridlines(draw_labels=True,
                       linewidth=0.4, color=COLORS["lightgrey"],
                       linestyle=":", alpha=0.8,
                       xlocs=np.arange(-122.7, -122.0, 0.1),
                       ylocs=np.arange(47.4, 47.8, 0.05))
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 10, "color": COLORS["grey"]}
    gl.ylabel_style = {"size": 10, "color": COLORS["grey"]}

    # Anomaly raster.
    pm = ax.pcolormesh(lon, lat, anomaly,
                        transform=ccrs.PlateCarree(),
                        cmap=plt.get_cmap("RdBu_r"),
                        shading="auto",
                        vmin=-400, vmax=400)

    cbar = fig.colorbar(pm, ax=ax, orientation="vertical", pad=0.04,
                         shrink=0.75, aspect=30)
    cbar.set_label("Magnetic anomaly $\\Delta F$  (nT)", fontsize=11)
    cbar.ax.tick_params(labelsize=10)

    # Mark the Seattle Fault trace.
    fault_lon = np.array([-122.55, -122.20])
    fault_lat_arr = np.array([47.58, 47.58])
    ax.plot(fault_lon, fault_lat_arr, color=COLORS["black"], lw=2.5,
             transform=ccrs.PlateCarree(), zorder=8,
             label="Seattle Fault (trace)")
    # Reverse-fault hatches (small triangles on the hanging-wall side).
    for x in np.linspace(-122.50, -122.25, 6):
        ax.plot(x, 47.585, marker="v", color=COLORS["black"], markersize=8,
                 transform=ccrs.PlateCarree(), zorder=9)

    # Annotations.
    ax.annotate(
        "Crescent Fm. (Siletzia)\nhanging wall",
        xy=(-122.43, 47.50), xytext=(-122.45, 47.45),
        xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
        fontsize=11, color=COLORS["black"], fontweight="bold",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                  edgecolor=COLORS["grey"], lw=0.6, alpha=0.9),
        arrowprops=dict(arrowstyle="->", color=COLORS["grey"], lw=0.8),
    )
    ax.annotate(
        "Seattle basin sediments\n(footwall)",
        xy=(-122.40, 47.65), xytext=(-122.42, 47.70),
        xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
        fontsize=11, color=COLORS["black"], fontweight="bold",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                  edgecolor=COLORS["grey"], lw=0.6, alpha=0.9),
        arrowprops=dict(arrowstyle="->", color=COLORS["grey"], lw=0.8),
    )

    # Mark Seattle downtown.
    ax.plot(-122.33, 47.60, "*", color="#FFD700", markersize=14,
             markeredgecolor=COLORS["black"], markeredgewidth=0.8,
             transform=ccrs.PlateCarree(), zorder=10)
    ax.text(-122.33, 47.595, "Downtown\nSeattle",
             transform=ccrs.PlateCarree(),
             fontsize=9, fontweight="bold", ha="center", va="top",
             color=COLORS["black"], zorder=10)
    # Mark Bainbridge Island.
    ax.text(-122.53, 47.62, "Bainbridge\nIsland",
             transform=ccrs.PlateCarree(),
             fontsize=9, ha="center", color=COLORS["grey"],
             style="italic", zorder=10)

    title_label = ("Seattle Fault Zone — aeromagnetic anomaly  "
                    "(after Blakely et al. 2002, USGS public domain)")
    if synthetic:
        title_label = ("Seattle Fault Zone — aeromagnetic anomaly — SYNTHETIC PLACEHOLDER  "
                        "(replace with USGS Puget Lowland compilation)")
    ax.set_title(title_label, fontsize=12.5, fontweight="bold", pad=14)

    fig.text(0.5, 0.04,
             "Source: USGS aeromagnetic compilation — Blakely, Wells, Weaver & Johnson "
             "(2002), GSA Bulletin 114. Public domain.",
             ha="center", fontsize=9, color=COLORS["grey"], style="italic")

    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir / "fig_seattle_fault_aeromag.png")
    print("wrote", out_dir / "fig_seattle_fault_aeromag.png")
