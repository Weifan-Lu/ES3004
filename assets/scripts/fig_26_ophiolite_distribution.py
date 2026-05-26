"""F10 — Global distribution of major ophiolite belts.

Locations follow the Tethyan / Cordilleran compilation of Dilek & Furnes
(2011) and Dilek (2003), simplified to representative type localities.
Plotted as labelled markers on a simple lat/lon world map with PlateCarree-
style coastlines (matplotlib only — no cartopy dependency).

Writes assets/figures/F10_ophiolite_distribution.png.
"""
from __future__ import annotations

from pathlib import Path
import sys
import urllib.request
import json

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from _style import COLORS, apply_style  # noqa: E402

apply_style()

OUT = Path(__file__).resolve().parent.parent / "figures" / "F10_ophiolite_distribution.png"
COAST_CACHE = Path(__file__).resolve().parent.parent / "data" / "ne_110m_coastline.geojson"
COAST_URL = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
             "master/geojson/ne_110m_coastline.geojson")

# Representative ophiolite type localities (lon, lat, name)
OPHIOLITES = [
    (58.5,  23.0,  "Oman (Semail)"),
    (33.0,  35.0,  "Troodos (Cyprus)"),
    (8.6,   44.4,  "Ligurian (Italy)"),
    (-65.0, 47.0,  "Bay of Islands (Newfoundland)"),
    (-122.0, 41.0, "Klamath / Trinity (California)"),
    (-72.0, 42.6,  "Appalachian (New England)"),
    (39.0,  8.5,   "Yarlung Zangbo (Tibet)"),
    (130.0, 32.5,  "SW Japan (Akaishi)"),
    (-58.0, -32.0, "Argentine Precordillera"),
    (159.0, -10.0, "Papua New Guinea"),
    (-22.5, 66.0,  "Iceland (modern analog)"),
    (45.0,  37.0,  "Zagros (Iran)"),
    (-2.5,  52.0,  "Lizard (UK)"),
    (88.0,  29.0,  "Xigaze (Tibet)"),
]


def _fetch_coast() -> dict:
    if not COAST_CACHE.exists():
        COAST_CACHE.parent.mkdir(parents=True, exist_ok=True)
        print(f"[F10] fetching {COAST_URL}")
        with urllib.request.urlopen(COAST_URL, timeout=60) as r:
            COAST_CACHE.write_bytes(r.read())
    with COAST_CACHE.open() as f:
        return json.load(f)


def main() -> None:
    fig, ax = plt.subplots(figsize=(11.5, 5.4))

    # Coastlines
    try:
        gj = _fetch_coast()
        for feat in gj["features"]:
            geom = feat["geometry"]
            if geom["type"] == "LineString":
                coords = np.array(geom["coordinates"])
                ax.plot(coords[:, 0], coords[:, 1], color=COLORS["grey"], lw=0.5)
            elif geom["type"] == "MultiLineString":
                for line in geom["coordinates"]:
                    coords = np.array(line)
                    ax.plot(coords[:, 0], coords[:, 1], color=COLORS["grey"], lw=0.5)
    except Exception as e:
        print(f"[F10] coast fetch failed ({e}); plotting without coastlines")

    # Ophiolite markers
    for lon, lat, name in OPHIOLITES:
        ax.plot(lon, lat, "o", color=COLORS["vermilion"], ms=8,
                markeredgecolor="white", markeredgewidth=0.8, zorder=5)
        ax.annotate(name, (lon, lat), xytext=(6, 5), textcoords="offset points",
                    fontsize=8.5, color=COLORS["black"])

    ax.set_xlim(-180, 180)
    ax.set_ylim(-65, 80)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    ax.set_title("Major ophiolite belts — fossil oceanic lithosphere on land "
                 "(after Dilek 2003; Dilek & Furnes 2011)", loc="left", fontsize=12)
    ax.set_aspect("equal")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    print(f"[F10] wrote {OUT}")


if __name__ == "__main__":
    main()
