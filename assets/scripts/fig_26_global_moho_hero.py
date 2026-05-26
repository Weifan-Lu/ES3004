"""F0 — Hero figure: global CRUST1.0 Moho depth.

Same data source as F12 (CRUST1.0 depth-to-Moho XYZ, Laske 2013) but
plotted globally so the oceanic-vs-continental thickness contrast jumps
out at first glance: oceans sit at ~7–10 km Moho depth, continents at
30–50 km, cratonic roots near 55–70 km.

Writes assets/figures/F0_global_moho.png.
"""
from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from _style import COLORS, apply_style  # noqa: E402

apply_style()

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "figures" / "F0_global_moho.png"
CACHE = ROOT / "data" / "crust1_depthtomoho.xyz"


def main() -> None:
    if not CACHE.exists():
        raise SystemExit("Run fig_26_north_america_moho.py first to populate CRUST1.0 cache.")

    data = np.loadtxt(CACHE)
    lon, lat, moho = data[:, 0], data[:, 1], data[:, 2]
    moho_pos = -moho if np.nanmean(moho) < 0 else moho

    lons = np.arange(-179.5, 180.0, 1.0)
    lats = np.arange(-89.5, 90.0, 1.0)
    grid = np.full((lats.size, lons.size), np.nan)
    j = np.round(lon - lons[0]).astype(int) % lons.size
    i = np.round(lat - lats[0]).astype(int)
    valid = (i >= 0) & (i < lats.size)
    grid[i[valid], j[valid]] = moho_pos[valid]

    fig, ax = plt.subplots(figsize=(13.5, 6.4))
    im = ax.imshow(
        grid,
        extent=(lons.min(), lons.max(), lats.min(), lats.max()),
        origin="lower",
        cmap="viridis",
        aspect="equal",
        vmin=5, vmax=65,
    )
    cb = fig.colorbar(im, ax=ax, shrink=0.78, pad=0.02,
                      label="Moho depth (km below sea level)")
    cb.outline.set_visible(False)

    # Pedagogical annotations: oceanic vs continental
    ax.annotate("Oceanic crust\n~7–10 km", xy=(-150, -20), xytext=(-150, -45),
                ha="center", color="white", fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="white", lw=1.2))
    ax.annotate("Continental crust\n30–45 km", xy=(60, 35), xytext=(75, 5),
                ha="center", color="white", fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="white", lw=1.2))
    ax.annotate("Cratonic roots\n50–65 km", xy=(95, 55), xytext=(140, 75),
                ha="center", color="white", fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="white", lw=1.2))
    ax.annotate("Andean / Tibetan\norogens >60 km", xy=(-70, -20),
                xytext=(-100, -55), ha="center",
                color="white", fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="white", lw=1.2))

    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    ax.set_title("Global Moho depth — CRUST1.0 (Laske et al. 2013)",
                 loc="left", fontsize=14)
    ax.set_xlim(-180, 180)
    ax.set_ylim(-85, 85)
    ax.grid(alpha=0.2, color="white", lw=0.3)

    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    print(f"[F0] wrote {OUT}")


if __name__ == "__main__":
    main()
