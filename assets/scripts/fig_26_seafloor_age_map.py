"""F1 — Global seafloor age map (Müller / Seton 2020).

Downloads the real Müller/Seton age grid via xarray. Falls back to
the EarthByte HTTP mirror if the primary URL fails. Output saved to
``assets/figures/F1_seafloor_age_map.png``.

Run::

    pixi run python assets/scripts/fig_26_seafloor_age_map.py

Provenance: Seton et al. (2020), G-Cubed, doi:10.1029/2020GC009214.
"""
from __future__ import annotations

import io
import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from _style import COLORS, apply_style

apply_style()

OUT = Path(__file__).resolve().parents[1] / "figures" / "F1_seafloor_age_map.png"
CACHE = Path(__file__).resolve().parents[1] / "data"
CACHE.mkdir(parents=True, exist_ok=True)
LOCAL_NC = CACHE / "muller2019_agegrid_0.nc"

CANDIDATE_URLS = [
    # Müller et al. 2019 Tectonics, agegrid v2.0 (present-day)
    "https://www.earthbyte.org/webdav/ftp/Data_Collections/Muller_etal_2019_Tectonics/Muller_etal_2019_Agegrids/Muller_etal_2019_Tectonics_v2.0_netCDF/Muller_etal_2019_Tectonics_v2.0_AgeGrid-0.nc",
    # Mirror / older Müller 2008
    "https://www.earthbyte.org/webdav/ftp/Data_Collections/Muller_etal_2008_Age_Spreading_Rates_Asymmetries/Muller_etal_2008_AgeGrid_6m.nc",
]


def _download() -> Path:
    if LOCAL_NC.exists() and LOCAL_NC.stat().st_size > 1_000_000:
        return LOCAL_NC
    last_err = None
    for url in CANDIDATE_URLS:
        try:
            print(f"[F1] fetching {url}")
            req = urllib.request.Request(url, headers={"User-Agent": "ess314/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            LOCAL_NC.write_bytes(data)
            return LOCAL_NC
        except Exception as exc:  # noqa: BLE001
            print(f"[F1] failed: {exc}")
            last_err = exc
    raise RuntimeError(f"Could not download Müller age grid: {last_err}")


def main() -> None:
    import xarray as xr

    path = _download()
    ds = xr.open_dataset(path)
    # The variable is typically named 'z' (Myr).
    var = "z" if "z" in ds else list(ds.data_vars)[0]
    age = ds[var]

    # Downsample for plotting if too large.
    if age.size > 4_000_000:
        step_y = max(1, age.shape[0] // 1200)
        step_x = max(1, age.shape[1] // 2400)
        age = age[::step_y, ::step_x]

    fig, ax = plt.subplots(figsize=(11, 5.2))
    im = age.plot.imshow(
        ax=ax,
        cmap="magma_r",
        vmin=0,
        vmax=180,
        add_colorbar=False,
        interpolation="nearest",
    )
    cbar = fig.colorbar(im, ax=ax, orientation="horizontal", pad=0.08,
                        shrink=0.85, aspect=40)
    cbar.set_label("Seafloor age (Ma)")

    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    ax.set_title("Global seafloor age — Müller et al. 2019 / Seton et al. 2020",
                 fontsize=12)
    ax.set_aspect("equal")
    ax.grid(False)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, bbox_inches="tight")
    print(f"[F1] wrote {OUT}")


if __name__ == "__main__":
    main()
