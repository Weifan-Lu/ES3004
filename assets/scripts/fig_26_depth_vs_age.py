"""F3 / F5 — Real-data depth vs. seafloor age relation.

Joins Müller et al. 2019 v2.0 seafloor-age grid (cached by F1) with a
global GMRT bathymetry grid (1° downsampled) to make:

  F3 : single-panel scatter of binned depth vs sqrt(age) with HSC and
       plate-model curves overlaid.
  F5 : three-panel comparison (depth vs age, q vs age, depth vs sqrt(age))
       showing where the two models agree and diverge.

Outputs:
  assets/figures/F3_depth_vs_age.png
  assets/figures/F5_model_comparison_3panel.png
"""
from __future__ import annotations

from pathlib import Path
import sys
import urllib.request

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from _style import COLORS, apply_style  # noqa: E402

apply_style()

ROOT = Path(__file__).resolve().parent.parent
F3_OUT = ROOT / "figures" / "F3_depth_vs_age.png"
F5_OUT = ROOT / "figures" / "F5_model_comparison_3panel.png"
AGE_CACHE = ROOT / "data" / "muller2019_agegrid_0.nc"
BATHY_CACHE = ROOT / "data" / "gmrt_global_1deg.nc"

# GMRT global subset at low resolution. World extent.
GMRT_URL = (
    "https://www.gmrt.org/services/GridServer?"
    "north=80&south=-80&east=180&west=-180"
    "&layer=topo&format=netcdf&resolution=low"
)


def _fetch_bathy() -> Path:
    if BATHY_CACHE.exists() and BATHY_CACHE.stat().st_size > 100_000:
        return BATHY_CACHE
    BATHY_CACHE.parent.mkdir(parents=True, exist_ok=True)
    print(f"[F3/F5] fetching global GMRT: {GMRT_URL}")
    req = urllib.request.Request(GMRT_URL, headers={"User-Agent": "ess314/1.0"})
    with urllib.request.urlopen(req, timeout=240) as r:
        BATHY_CACHE.write_bytes(r.read())
    return BATHY_CACHE


def _load_grids():
    import xarray as xr

    ds_age = xr.open_dataset(AGE_CACHE)
    # Müller grid: variable z, dims (lat, lon) or (y, x); ages in Ma; mask continents = NaN
    age_var = "z" if "z" in ds_age else list(ds_age.data_vars)[0]
    age = ds_age[age_var]
    # Identify lat/lon
    lat_name = next((n for n in ("lat", "y", "latitude") if n in age.dims), age.dims[0])
    lon_name = next((n for n in ("lon", "x", "longitude") if n in age.dims), age.dims[1])
    age_lats = age[lat_name].values
    age_lons = age[lon_name].values
    age_arr = age.values

    # GMRT GMT-binary
    ds_b = xr.open_dataset(_fetch_bathy())
    x0, x1 = ds_b["x_range"].values
    y0, y1 = ds_b["y_range"].values
    nx, ny = ds_b["dimension"].values.astype(int)
    z = ds_b["z"].values.reshape((ny, nx))
    b_lats = np.linspace(y1, y0, ny)  # top-to-bottom
    b_lons = np.linspace(x0, x1, nx)

    return age_lats, age_lons, age_arr, b_lats, b_lons, z


def _sample(age_lats, age_lons, age_arr, b_lats, b_lons, b_arr, step=2.0):
    """Sample both grids on a common 2°×2° world grid and pair the values."""
    lats = np.arange(-70, 70 + step, step)
    lons = np.arange(-180, 180, step)
    ages = []
    depths = []
    for la in lats:
        ia = int(np.argmin(np.abs(age_lats - la)))
        ib = int(np.argmin(np.abs(b_lats - la)))
        for lo in lons:
            ja = int(np.argmin(np.abs(age_lons - lo)))
            jb = int(np.argmin(np.abs(b_lons - lo)))
            a = age_arr[ia, ja]
            d = b_arr[ib, jb]
            if np.isnan(a) or a <= 0 or a > 200:
                continue
            if d > -2000:  # exclude shelves and land
                continue
            ages.append(float(a))
            depths.append(-float(d) / 1000.0)  # km below sea level
    return np.array(ages), np.array(depths)


def _bin_stats(age, depth, edges):
    centres = 0.5 * (edges[1:] + edges[:-1])
    mean = np.full(centres.size, np.nan)
    p25  = np.full(centres.size, np.nan)
    p75  = np.full(centres.size, np.nan)
    for i in range(centres.size):
        m = (age >= edges[i]) & (age < edges[i + 1])
        if m.sum() < 5:
            continue
        mean[i] = np.mean(depth[m])
        p25[i]  = np.percentile(depth[m], 25)
        p75[i]  = np.percentile(depth[m], 75)
    return centres, mean, p25, p75


def main() -> None:
    age_lats, age_lons, age_arr, b_lats, b_lons, b_arr = _load_grids()
    age, depth = _sample(age_lats, age_lons, age_arr, b_lats, b_lons, b_arr)
    print(f"[F3/F5] paired {age.size} ocean cells")

    # Bins by age (linear) and by sqrt(age)
    edges = np.arange(0, 175, 5)
    centres, mean_d, p25, p75 = _bin_stats(age, depth, edges)

    # Models
    a = np.linspace(0.1, 170, 500)
    # HSC: d(a) = 2.5 + 0.35 * sqrt(a)  (km, classical Parsons & Sclater 1977)
    hsc = 2.5 + 0.35 * np.sqrt(a)
    # Plate (GDH1, Stein & Stein 1992 simplified): asymptotes near 5.65 km
    plate = 5.65 - 2.47 * np.exp(-0.0278 * a)  # km, depth from sea level

    # -------------------- F3 single panel --------------------
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.scatter(np.sqrt(age), depth, s=2, alpha=0.08, color=COLORS["grey"],
               label="ocean cells (2°×2°)")
    ax.errorbar(np.sqrt(centres), mean_d, yerr=[mean_d - p25, p75 - mean_d],
                fmt="o", ms=5, color=COLORS["black"], ecolor=COLORS["grey"],
                lw=0, elinewidth=0.8, capsize=2,
                label="binned mean ± IQR")
    ax.plot(np.sqrt(a), hsc,  color=COLORS["vermilion"], lw=2, label="HSC")
    ax.plot(np.sqrt(a), plate, color=COLORS["blue"], lw=2, label="Plate (GDH1)")
    ax.set_xlabel(r"$\sqrt{\mathrm{age}}$ (Ma$^{1/2}$)")
    ax.set_ylabel("Depth (km below sea level)")
    ax.set_ylim(7.0, 2.0)
    ax.set_xlim(0, np.sqrt(170))
    ax.set_title("Ocean depth vs. seafloor age — real GMRT × Müller 2019", loc="left")
    ax.legend(loc="lower left", framealpha=0.92)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(F3_OUT, bbox_inches="tight")
    print(f"[F3] wrote {F3_OUT}")

    # -------------------- F5 three-panel comparison --------------------
    fig2, axs = plt.subplots(1, 3, figsize=(13.5, 4.3))

    # Panel A: depth vs age
    ax = axs[0]
    ax.errorbar(centres, mean_d, yerr=[mean_d - p25, p75 - mean_d],
                fmt="o", ms=4, color=COLORS["black"], ecolor=COLORS["grey"],
                lw=0, elinewidth=0.8, capsize=2)
    ax.plot(a, hsc,  color=COLORS["vermilion"], lw=2, label="HSC")
    ax.plot(a, plate, color=COLORS["blue"], lw=2, label="Plate")
    ax.set_xlabel("Age (Ma)")
    ax.set_ylabel("Depth (km)")
    ax.set_ylim(7.0, 2.0)
    ax.set_xlim(0, 170)
    ax.set_title("(a) Depth vs. age", loc="left")
    ax.legend(loc="lower left")
    ax.grid(alpha=0.25)

    # Panel B: heat flow vs age (model curves only — data sparse)
    ax = axs[1]
    # q_HSC = C / sqrt(a),  C ≈ 510 mW m^-2 Ma^1/2  (Stein & Stein 1992)
    q_hsc = 510.0 / np.sqrt(a)
    # q_plate: asymptotic to ~48 mW/m² at old age
    q_plate = 48.0 + 462.0 * np.exp(-0.030 * a)
    ax.plot(a, q_hsc,  color=COLORS["vermilion"], lw=2, label="HSC")
    ax.plot(a, q_plate, color=COLORS["blue"], lw=2, label="Plate")
    ax.set_xlabel("Age (Ma)")
    ax.set_ylabel(r"Heat flow (mW m$^{-2}$)")
    ax.set_ylim(0, 250)
    ax.set_xlim(0, 170)
    ax.set_title("(b) Heat flow vs. age", loc="left")
    ax.legend()
    ax.grid(alpha=0.25)

    # Panel C: depth vs sqrt(age) — HSC linearises
    ax = axs[2]
    ax.errorbar(np.sqrt(centres), mean_d, yerr=[mean_d - p25, p75 - mean_d],
                fmt="o", ms=4, color=COLORS["black"], ecolor=COLORS["grey"],
                lw=0, elinewidth=0.8, capsize=2)
    ax.plot(np.sqrt(a), hsc,  color=COLORS["vermilion"], lw=2)
    ax.plot(np.sqrt(a), plate, color=COLORS["blue"], lw=2)
    ax.set_xlabel(r"$\sqrt{\mathrm{age}}$ (Ma$^{1/2}$)")
    ax.set_ylabel("Depth (km)")
    ax.set_ylim(7.0, 2.0)
    ax.set_xlim(0, np.sqrt(170))
    ax.set_title("(c) Depth vs " r"$\sqrt{\mathrm{age}}$", loc="left")
    ax.grid(alpha=0.25)

    fig2.suptitle("Half-space cooling vs. plate model — global ocean data",
                  y=1.02, fontsize=14)
    fig2.tight_layout()
    fig2.savefig(F5_OUT, bbox_inches="tight")
    print(f"[F5] wrote {F5_OUT}")


if __name__ == "__main__":
    main()
