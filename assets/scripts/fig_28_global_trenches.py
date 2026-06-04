"""
fig_28_global_trenches.py  -> SF1_global_trenches.png

The OPENING figure of L28: a Pacific-centred world map of the active subduction
trenches (the "Ring of Fire" plus the Tethyan/Atlantic systems) drawn on a real
global digital elevation model (topography + bathymetry), with the great
(Mw >= 8.5) megathrust earthquakes of the instrumental era overplotted as stars
sized by magnitude. The map motivates the lecture: subduction zones girdle the
Pacific and host every Mw >= 9 of the last century, yet those giants are
scattered across margins of very different plate age, convergence rate, and
sediment supply (developed quantitatively in SF3).

WHAT CHANGED FROM THE EARLIER VERSION
  1. Real DEM. The flat neutral backdrop is replaced by the 1-degree global
     GMRT elevation grid (assets/data/gmrt_global_1deg.nc), shaded with a
     combined bathymetry-topography colormap, plus Natural Earth coastlines.
  2. Correct subduction polarity. Trench teeth previously pointed to whichever
     side the segment normal happened to fall on (it flips with digitisation
     order), so the convergence sense was sometimes drawn backward. Each trench
     now carries an explicit overriding-plate reference point, and every tooth
     is oriented toward it. This encodes the true subduction polarity, including
     the polarity reversal at the New Hebrides (Vanuatu) arc.

DATA PROVENANCE
  - DEM: GMRT global grid, 1 deg (Ryan et al. 2009, doi:10.1029/2008GC002332),
    cached as assets/data/gmrt_global_1deg.nc.
  - Coastlines: Natural Earth 1:110m (public domain),
    assets/data/ne_110m_coastline.geojson.
  - Trench traces: approximate hand-digitised polylines after the global trench
    compilation of Hayes et al. (2018) Slab2 (doi:10.1126/science.aat4723; data
    release 10.5066/F7PV6JNV). Coordinates rounded for teaching.
  - Great-earthquake locations and magnitudes: USGS / Global CMT catalogues as
    summarised by Wirth et al. (2022, doi:10.1038/s43017-021-00245-w).

Output: assets/figures/SF1_global_trenches.png
License: CC-BY 4.0 (this script)
"""
from __future__ import annotations

from pathlib import Path
import json

import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

mpl.rcParams.update({
    "font.size": 12, "axes.titlesize": 15, "axes.labelsize": 12,
    "xtick.labelsize": 10, "ytick.labelsize": 10, "legend.fontsize": 10,
    "figure.dpi": 150, "savefig.dpi": 300,
})

ROOT = Path(__file__).resolve().parent.parent
DEM_NC = ROOT / "data" / "gmrt_global_1deg.nc"
COAST = ROOT / "data" / "ne_110m_coastline.geojson"
OUT = ROOT / "figures" / "SF1_global_trenches.png"

VERM, BLACK = "#D55E00", "#111111"


def wrap360(lon):
    """Map longitudes to the 0..360 Pacific-centred frame."""
    return np.mod(lon, 360.0)


# ---------------------------------------------------------------------------
# Trench polylines (lon, lat) with an explicit OVERRIDING-PLATE reference point.
# Teeth are drawn pointing from the trench toward `ref` -- i.e. in the direction
# the slab descends (the subduction polarity). `ref` sits on the concave / arc
# side of each trench, which is the overriding plate.
# ---------------------------------------------------------------------------
trenches = {
    "Aleutian":          dict(verts=[(-170, 52), (-165, 53), (-158, 54.5), (-150, 56)],
                              ref=(-162, 60)),
    "Alaska":            dict(verts=[(-150, 56), (-145, 58), (-140, 59)],
                              ref=(-143, 63)),
    "Cascadia":          dict(verts=[(-125, 40), (-125, 44), (-125.5, 48), (-126, 50)],
                              ref=(-119, 45)),
    "Middle America":    dict(verts=[(-105, 19), (-98, 16), (-92, 14), (-87, 12), (-83, 9)],
                              ref=(-92, 21)),
    "Peru\u2013Chile":   dict(verts=[(-81, 0), (-76, -14), (-72, -23), (-72, -33),
                                     (-74, -42), (-75, -47)],
                              ref=(-65, -25)),
    "Kuril\u2013Kamchatka": dict(verts=[(156, 51), (158, 47), (153, 44), (148, 43), (145, 41)],
                              ref=(150, 53)),
    "Japan":             dict(verts=[(145, 41), (144, 38), (142, 35), (140, 33)],
                              ref=(137, 37)),
    "Izu\u2013Bonin\u2013Mariana": dict(verts=[(140, 33), (142, 28), (143, 22), (144, 16),
                                       (147, 12)],
                              ref=(137, 21)),
    "Ryukyu":            dict(verts=[(131, 33), (128, 28), (124, 24), (122, 22)],
                              ref=(126, 30)),
    "Philippine":        dict(verts=[(127, 13), (127, 8), (126, 4), (125, 2)],
                              ref=(123, 8)),
    "Java\u2013Sunda":   dict(verts=[(95, 2), (100, -5), (108, -9), (118, -10), (122, -10)],
                              ref=(110, 0)),
    "Sumatra":           dict(verts=[(95, 2), (92, 6), (90, 10), (89, 14)],
                              ref=(99, 6)),
    "Tonga\u2013Kermadec": dict(verts=[(-173, -16), (-174, -22), (-176, -28), (-178, -34),
                                       (179, -38)],
                              ref=(-178, -26)),   # overriding (Australian) plate to the west
    "New Hebrides":      dict(verts=[(166, -12), (168, -16), (170, -20)],
                              ref=(173, -16)),    # REVERSED polarity: overriding plate to the EAST
    "Hikurangi":         dict(verts=[(179, -38), (178, -42), (176, -45)],
                              ref=(173, -42)),
    "Lesser Antilles":   dict(verts=[(-60, 18), (-59, 15), (-60, 12)],
                              ref=(-65, 15)),
    "Scotia":            dict(verts=[(-30, -56), (-26, -58), (-25, -60), (-27, -62)],
                              ref=(-33, -59)),
}

trench_labels = {
    "Aleutian": (-165, 58), "Cascadia": (-136, 45), "Middle America": (-108, 7),
    "Peru\u2013Chile": (-63, -30), "Kuril\u2013Kamchatka": (163, 52), "Japan": (151, 36),
    "Izu\u2013Bonin\u2013Mariana": (152, 19), "Java\u2013Sunda": (107, -17),
    "Tonga\u2013Kermadec": (-169, -27), "Philippine": (132, 5), "Sumatra": (81, 11),
    "Lesser Antilles": (-53, 16), "Ryukyu": (117, 29), "Hikurangi": (170, -47),
    "New Hebrides": (175, -12), "Scotia": (-22, -59),
}

# Great earthquakes: name, lon, lat, Mw
great_eqs = [
    ("Chile 1960",    -73.5, -38.0, 9.5),
    ("Alaska 1964",  -147.5,  61.0, 9.2),
    ("Sumatra 2004",   95.9,   3.3, 9.1),
    ("T\u014dhoku 2011", 142.4, 38.3, 9.1),
    ("Kamchatka 1952", 160.0, 52.8, 9.0),
    ("Cascadia 1700", -125.5, 46.0, 9.0),
    ("Maule 2010",    -72.9, -36.1, 8.8),
    ("Ecuador 1906",  -79.4,   1.0, 8.8),
    ("Aleutian 1957",-175.0,  51.5, 8.6),
    ("Sumatra 2005",   97.1,   2.1, 8.6),
]


def load_dem():
    """Return (lons_0_360_sorted, lats_top_to_bottom, Z) from the GMRT grid."""
    import xarray as xr
    ds = xr.open_dataset(DEM_NC)
    if "z" in ds and "x_range" in ds:            # GMT-binary style netCDF
        x0, x1 = ds["x_range"].values
        y0, y1 = ds["y_range"].values
        nx, ny = ds["dimension"].values.astype(int)
        z = ds["z"].values.reshape((ny, nx))
        lats = np.linspace(y1, y0, ny)           # top -> bottom
        lons = np.linspace(x0, x1, nx)
    else:                                        # CF-style netCDF
        zname = "z" if "z" in ds else list(ds.data_vars)[0]
        z = ds[zname].values
        lat_name = next(n for n in ("lat", "y", "latitude") if n in ds[zname].dims)
        lon_name = next(n for n in ("lon", "x", "longitude") if n in ds[zname].dims)
        lats = ds[lat_name].values
        lons = ds[lon_name].values
        if lats[0] < lats[-1]:                   # force top -> bottom
            lats = lats[::-1]
            z = z[::-1, :]
    # Roll to a Pacific-centred 0..360 frame
    lons360 = wrap360(lons)
    order = np.argsort(lons360)
    return lons360[order], lats, z[:, order]


def load_coast():
    with COAST.open() as f:
        gj = json.load(f)
    lines = []
    for feat in gj["features"]:
        geom = feat["geometry"]
        if geom["type"] == "LineString":
            lines.append(np.asarray(geom["coordinates"], float))
        elif geom["type"] == "MultiLineString":
            lines.extend(np.asarray(c, float) for c in geom["coordinates"])
    return lines


def resample(verts, ds=2.2):
    """Even-arc-length resampling of a polyline (in the 0..360 frame)."""
    v = np.asarray(verts, float)
    seg = np.hypot(*np.diff(v, axis=0).T)
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    if cum[-1] == 0:
        return v
    s = np.arange(0.0, cum[-1], ds)
    return np.column_stack([np.interp(s, cum, v[:, 0]),
                            np.interp(s, cum, v[:, 1])])


def draw_trench(ax, verts, ref, color=BLACK, tooth=1.7, hw=0.9):
    """Draw the trench polyline and polarity teeth pointing toward `ref`."""
    raw = np.asarray(verts, float)
    v = np.column_stack([wrap360(raw[:, 0]), raw[:, 1]])
    r = np.array([wrap360(ref[0]), ref[1]])
    ax.plot(v[:, 0], v[:, 1], color=color, lw=2.2, zorder=5,
            solid_capstyle="round")
    pts = resample(v, ds=2.2)
    tang = np.gradient(pts, axis=0)              # local tangents
    for p, t in zip(pts, tang):
        tl = np.hypot(*t)
        if tl == 0:
            continue
        u = t / tl                               # along-trench unit vector
        n = np.array([u[1], -u[0]])              # one side normal
        if np.dot(n, r - p) < 0:                 # flip to point toward overriding plate
            n = -n
        apex = p + n * tooth
        b1, b2 = p - u * hw, p + u * hw
        ax.fill([b1[0], b2[0], apex[0]], [b1[1], b2[1], apex[1]],
                color=color, zorder=6, lw=0)


def main():
    lons, lats, Z = load_dem()

    # Combined bathymetry (blues) + topography (earth) colormap, sea level = 0.
    ocean = plt.cm.Blues_r(np.linspace(0.10, 0.92, 256))
    land = plt.cm.gist_earth(np.linspace(0.32, 1.0, 256))
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "bathytopo", np.vstack([ocean, land]))
    cmap.set_bad("#dddddd")
    norm = mcolors.TwoSlopeNorm(vmin=-7500, vcenter=0.0, vmax=5000)

    fig, ax = plt.subplots(figsize=(14.0, 7.6))
    im = ax.imshow(Z, extent=[lons.min(), lons.max(), lats.min(), lats.max()],
                   origin="upper", cmap=cmap, norm=norm, aspect="auto",
                   interpolation="bilinear", zorder=0)

    # Coastlines (split at the Pacific-centred dateline seam)
    for line in load_coast():
        x = wrap360(line[:, 0]); y = line[:, 1]
        jumps = np.where(np.abs(np.diff(x)) > 180)[0]
        x = np.insert(x, jumps + 1, np.nan)
        y = np.insert(y, jumps + 1, np.nan)
        ax.plot(x, y, color="#3a3a3a", lw=0.45, zorder=2)

    # Trenches with correct polarity teeth
    for name, tr in trenches.items():
        draw_trench(ax, tr["verts"], tr["ref"])

    # Trench labels
    for name, (lx, ly) in trench_labels.items():
        ax.text(wrap360(lx), ly, name, fontsize=8.5, color="#f5f5f5", zorder=7,
                ha="center", va="center", style="italic",
                bbox=dict(boxstyle="round,pad=0.12", fc="#00000088", ec="none"))

    # Great earthquakes
    for name, lon, lat, mw in great_eqs:
        s = 70 + (mw - 8.5) ** 2 * 620
        big = mw >= 8.95
        ax.scatter(wrap360(lon), lat, marker="*", s=s, color=VERM,
                   edgecolor="white", lw=1.1 if big else 0.6, zorder=8)
        if big:
            ax.annotate(f"{name}  M{mw}", xy=(wrap360(lon), lat),
                        xytext=(wrap360(lon), lat - 7.5), ha="center",
                        fontsize=8.5, fontweight="bold", color="white", zorder=9,
                        bbox=dict(boxstyle="round,pad=0.18", fc="#00000099", ec="none"))

    # Legend
    ax.scatter([], [], marker="*", s=320, color=VERM, edgecolor="white",
               label="Great earthquake (M \u2265 8.5)")
    ax.plot([], [], color=BLACK, lw=2.2, marker="^", markersize=8,
            label="Subduction trench (teeth \u2192 overriding plate)")
    leg = ax.legend(loc="lower left", framealpha=0.95)
    leg.set_zorder(10)

    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01, extend="both")
    cbar.set_label("Elevation (m)")

    ax.set_xlim(0, 360)
    ax.set_ylim(-78, 83)
    ax.set_xlabel("Longitude (Pacific-centred)")
    ax.set_ylabel("Latitude (\u00b0N)")
    ax.set_xticks(range(0, 361, 60))
    ax.set_xticklabels(["0\u00b0", "60\u00b0E", "120\u00b0E", "180\u00b0",
                        "120\u00b0W", "60\u00b0W", "0\u00b0"])
    ax.set_yticks(range(-60, 81, 30))
    ax.set_title("The world's subduction zones host every M\u2009\u2265\u20099 "
                 "of the past century")

    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
