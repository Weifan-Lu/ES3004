"""
fig_28_global_trenches.py  -> SF1_global_trenches.png

Scientific content (the OPENING figure of L28):
A world map of the active subduction trenches (the global "Ring of Fire" and the
Tethyan/Atlantic systems) with the great (Mw >= 8.5) megathrust earthquakes of
the instrumental era overplotted as stars sized by magnitude. The map motivates
the lecture: subduction zones girdle the Pacific and host every Mw >= 9 of the
last century, but those giants are scattered across zones of very different age,
rate, and sediment supply (developed quantitatively in SF3).

RENDERING NOTE: in the ESS 314 build sandbox, Cartopy's Natural Earth feature
downloads are blocked, so this script renders on a plain equirectangular axis
with hand-digitized trench polylines (approximate, for teaching) and a light
graticule. In Marine's pixi environment, swap the trench polylines for the Slab2
trench file and add Cartopy coastlines (PlateCarree); see the commented block.

DATA PROVENANCE: trench traces are approximate hand-digitized polylines after the
global trench compilation of Hayes et al. (2018) Slab2
(doi:10.1126/science.aat4723; data release 10.5066/F7PV6JNV). Great-earthquake
locations and magnitudes are from the USGS/Global CMT catalogues as summarised by
Wirth et al. (2022, doi:10.1038/s43017-021-00245-w). Coordinates rounded for
teaching.

Output: assets/figures/SF1_global_trenches.png
License: CC-BY 4.0 (this script)
"""
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 16, "axes.labelsize": 13,
    "xtick.labelsize": 11, "ytick.labelsize": 11, "legend.fontsize": 11,
    "figure.dpi": 150, "savefig.dpi": 300,
})

BLUE, ORANGE, SKY, GREEN, VERM, PINK, BLACK = (
    "#0072B2", "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7", "#000000")

# --- approximate trench polylines (lon, lat), hand-digitized for teaching -----
# Longitudes in -180..180. Each entry: name, label_xy, list of (lon,lat) vertices.
trenches = {
    "Aleutian": [(-170, 52), (-165, 53), (-158, 54.5), (-150, 56), (-160, 53)],
    "Alaska":   [(-150, 56), (-145, 58), (-140, 59)],
    "Cascadia": [(-125, 40), (-125, 44), (-125.5, 48), (-126, 50)],
    "Middle America": [(-105, 19), (-98, 16), (-92, 14), (-87, 12), (-83, 9)],
    "Peru–Chile": [(-81, 0), (-76, -14), (-72, -23), (-72, -33),
                   (-74, -42), (-75, -47)],
    "Kuril–Kamchatka": [(156, 51), (158, 47), (153, 44), (148, 43), (145, 41)],
    "Japan": [(145, 41), (144, 38), (142, 35), (140, 33)],
    "Izu–Bonin–Mariana": [(140, 33), (142, 28), (143, 22), (144, 16),
                          (147, 12), (148, 17)],
    "Ryukyu": [(131, 33), (128, 28), (124, 24), (122, 22)],
    "Philippine": [(127, 13), (127, 8), (126, 4), (125, 2)],
    "Java–Sunda": [(95, 2), (100, -5), (108, -9), (118, -10), (122, -10)],
    "Tonga–Kermadec": [(-173, -16), (-174, -22), (-176, -28), (-178, -34),
                       (179, -38)],
    "New Hebrides": [(166, -12), (168, -16), (170, -20)],
    "Hikurangi": [(179, -38), (178, -42), (176, -45)],
    "Lesser Antilles": [(-60, 18), (-59, 15), (-60, 12)],
    "Scotia": [(-58, -56), (-50, -58), (-44, -60)],
    "Sumatra": [(95, 2), (92, 6), (90, 10), (89, 14)],
}

# great earthquakes: name, lon, lat, Mw
great_eqs = [
    ("Chile 1960",   -73.5, -38.0, 9.5),
    ("Alaska 1964", -147.5,  61.0, 9.2),
    ("Sumatra 2004", 95.9,   3.3, 9.1),
    ("Tohoku 2011", 142.4,  38.3, 9.1),
    ("Kamchatka 1952",160.0, 52.8, 9.0),
    ("Cascadia 1700",-125.5, 46.0, 9.0),
    ("Maule 2010",  -72.9, -36.1, 8.8),
    ("Ecuador 1906",-79.4,   1.0, 8.8),
    ("Aleutian 1957",-175.0, 51.5, 8.6),
    ("Sumatra 2005",  97.1,   2.1, 8.6),
]

fig, ax = plt.subplots(figsize=(14.0, 7.4))

# Pacific-centred map: remap longitudes to 0..360 so Ring-of-Fire trenches that
# cross the +/-180 dateline render as continuous lines.
def wrap360(lon):
    return lon % 360

# ocean / land backdrop: light neutral fill + graticule (no coastlines available)
ax.set_facecolor("#eaf2f6")
for lon in range(0, 361, 30):
    ax.axvline(lon, color="#c8d4da", lw=0.6, zorder=0)
for lat in range(-90, 91, 30):
    ax.axhline(lat, color="#c8d4da", lw=0.6, zorder=0)

# plot trenches with subduction teeth
def draw_trench(verts, color=BLACK):
    v = np.array(verts, float)
    v[:, 0] = wrap360(v[:, 0])
    # guard against any residual wrap: split if a jump > 180 deg occurs
    lon = v[:, 0]
    jumps = np.where(np.abs(np.diff(lon)) > 180)[0]
    segments = np.split(np.arange(len(v)), jumps + 1)
    for seg in segments:
        if len(seg) < 2:
            continue
        vv = v[seg]
        ax.plot(vv[:, 0], vv[:, 1], color=color, lw=2.4, zorder=3,
                solid_capstyle="round")
        for i in range(len(vv) - 1):
            p0, p1 = vv[i], vv[i + 1]
            mid = 0.5 * (p0 + p1)
            d = p1 - p0
            n = np.array([d[1], -d[0]])
            nl = np.hypot(*n)
            if nl == 0:
                continue
            n = n / nl * 2.6
            ax.plot([mid[0], mid[0] + n[0]], [mid[1], mid[1] + n[1]],
                    color=color, lw=1.6, zorder=3)

for name, verts in trenches.items():
    draw_trench(verts)

# trench labels
trench_labels = {
    "Aleutian": (-165, 58), "Cascadia": (-138, 46), "Middle America": (-110, 8),
    "Peru–Chile": (-64, -30), "Kuril–Kamchatka": (162, 50), "Japan": (150, 36),
    "Izu–Bonin–Mariana": (151, 20), "Java–Sunda": (105, -16),
    "Tonga–Kermadec": (-171, -25), "Philippine": (132, 6), "Sumatra": (82, 12),
    "Lesser Antilles": (-54, 15), "Ryukyu": (118, 28), "Hikurangi": (171, -47),
    "New Hebrides": (172, -14), "Scotia": (-50, -52),
}
for name, (lx, ly) in trench_labels.items():
    ax.text(wrap360(lx), ly, name, fontsize=8.5, color="#333333", zorder=4,
            ha="center", style="italic")

# great earthquakes
for name, lon, lat, mw in great_eqs:
    s = 60 + (mw - 8.5) ** 2 * 600
    ringed = mw >= 8.95
    ax.scatter(wrap360(lon), lat, marker="*", s=s, color=VERM,
               edgecolor=BLACK, lw=1.0 if ringed else 0.5, zorder=6)
    if ringed:
        ax.annotate(f"{name}\nM{mw}", xy=(wrap360(lon), lat),
                    xytext=(wrap360(lon), lat - 9), ha="center", fontsize=8.5,
                    fontweight="bold", zorder=7)

# legend proxy
ax.scatter([], [], marker="*", s=300, color=VERM, edgecolor=BLACK,
           label="great earthquake (M ≥ 8.5)")
ax.plot([], [], color=BLACK, lw=2.4, label="subduction trench (teeth → overriding plate)")
ax.legend(loc="lower left", framealpha=0.92)

ax.set_xlim(0, 360)
ax.set_ylim(-75, 80)
ax.set_xlabel("longitude (°E, Pacific-centred)")
ax.set_ylabel("latitude (°N)")
ax.set_xticks(range(0, 361, 60))
ax.set_xticklabels(["0", "60E", "120E", "180", "120W", "60W", "0"])
ax.set_yticks(range(-60, 81, 30))
ax.set_title("The world's subduction zones host every Mw ≥ 9 of the past century")

fig.tight_layout()
out = "../figures/SF1_global_trenches.png"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")

# -----------------------------------------------------------------------------
# PRODUCTION VERSION (Marine's pixi env, Cartopy data cache populated):
#
#   import cartopy.crs as ccrs, cartopy.feature as cfeature
#   fig = plt.figure(figsize=(14, 7.4))
#   ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
#   ax.add_feature(cfeature.LAND, facecolor="#e8e4dc")
#   ax.add_feature(cfeature.COASTLINE, lw=0.4)
#   # load Slab2 trench file (e.g. Slab2Distribute/trenches_usgs_2017_depths.csv)
#   # and plot with transform=ccrs.PlateCarree(); overplot great_eqs the same way.
# -----------------------------------------------------------------------------
