"""F12 — North America Moho depth from CRUST1.0 (Laske et al. 2013).

Fetches the ready-made depth-to-Moho XYZ file directly from UCSD,
parses it into a 1° grid, crops to North America, and renders an imshow
map with viridis colormap.

Source: https://igppweb.ucsd.edu/~gabi/crust1.html → "depthtomoho.xyz.zip"

Writes assets/figures/F12_north_america_moho.png.
"""
from __future__ import annotations

from pathlib import Path
import sys
import urllib.request
import zipfile
import io

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from _style import COLORS, apply_style  # noqa: E402

apply_style()

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "figures" / "F12_north_america_moho.png"
CACHE = ROOT / "data" / "crust1_depthtomoho.xyz"
URL = "https://igppweb.ucsd.edu/~gabi/crust1/depthtomoho.xyz.zip"


def _fetch() -> Path:
    if CACHE.exists() and CACHE.stat().st_size > 100_000:
        return CACHE
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    print(f"[F12] fetching {URL}")
    req = urllib.request.Request(URL, headers={"User-Agent": "ess314/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        blob = r.read()
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        names = [n for n in zf.namelist() if n.lower().endswith(".xyz")]
        if not names:
            names = zf.namelist()
        with zf.open(names[0]) as f, CACHE.open("wb") as out:
            out.write(f.read())
    return CACHE


def main() -> None:
    path = _fetch()
    data = np.loadtxt(path)
    lon, lat, moho = data[:, 0], data[:, 1], data[:, 2]
    # File convention: depth to Moho is given as negative (below sea level).
    moho_pos = -moho if np.nanmean(moho) < 0 else moho

    lons = np.arange(-179.5, 180.0, 1.0)
    lats = np.arange(-89.5, 90.0, 1.0)
    grid = np.full((lats.size, lons.size), np.nan)
    j = np.round(lon - lons[0]).astype(int) % lons.size
    i = np.round(lat - lats[0]).astype(int)
    valid = (i >= 0) & (i < lats.size)
    grid[i[valid], j[valid]] = moho_pos[valid]

    lat_mask = (lats >= 15) & (lats <= 75)
    lon_mask = (lons >= -170) & (lons <= -50)
    sub = grid[np.ix_(lat_mask, lon_mask)]
    sub_lats = lats[lat_mask]
    sub_lons = lons[lon_mask]

    fig, ax = plt.subplots(figsize=(9.5, 6.0))
    im = ax.imshow(
        sub,
        extent=(sub_lons.min(), sub_lons.max(), sub_lats.min(), sub_lats.max()),
        origin="lower",
        cmap="viridis",
        aspect="equal",
        vmin=5, vmax=55,
    )
    cb = fig.colorbar(im, ax=ax, shrink=0.85, label="Moho depth (km below sea level)")
    cb.outline.set_visible(False)

    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    ax.set_title("North American Moho depth — CRUST1.0 (Laske et al. 2013)",
                 loc="left", fontsize=13)
    ax.grid(alpha=0.25, color="white", lw=0.4)
    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    print(f"[F12] wrote {OUT}")


if __name__ == "__main__":
    main()
