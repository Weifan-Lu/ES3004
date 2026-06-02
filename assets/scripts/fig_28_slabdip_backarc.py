"""
fig_28_slabdip_backarc.py  -> SF5_slabdip_backarc.png

Scientific content: The relationship between deep slab dip and the deformation
regime of the overriding plate (Lallemand, Heuret & Boutelier 2005). Subduction
zones with steep deep-slab dip (> ~50 deg) tend to have back-arc EXTENSION
(trench rollback, active back-arc spreading: Mariana, Tonga, Izu-Bonin); zones
with shallow dip (< ~30 deg) tend to have upper-plate SHORTENING (Andean
orogeny: Chile, Peru). Intermediate dips are near-neutral. The two grey bands
mark the ~30 deg and ~50 deg thresholds identified by Lallemand et al. (2005).

DATA PROVENANCE: representative deep-dip and back-arc-strain values are compiled
from Lallemand, Heuret & Boutelier (2005, G-Cubed, doi:10.1029/2005GC000917) and
Heuret & Lallemand (2005, Phys. Earth Planet. Inter.). The back-arc strain index
is an ordinal teaching simplification (-1 strong shortening ... +1 strong
extension), not a measured continuous quantity. Values rounded for teaching.

Reproduces the scientific content of (original figure NOT used):
  Lallemand, S., Heuret, A. & Boutelier, D. (2005). On the relationships between
  slab dip, back-arc stress, upper plate absolute motion, and crustal nature in
  subduction zones. Geochem. Geophys. Geosyst. 6, Q09006.

Output: assets/figures/SF5_slabdip_backarc.png
License: CC-BY 4.0 (this script)
"""
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 11,
    "figure.dpi": 150, "savefig.dpi": 300,
})

BLUE, ORANGE, SKY, GREEN, VERM, PINK, BLACK = (
    "#0072B2", "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7", "#000000")

# name, deep_dip_deg, backarc_strain_index (-1 shortening .. +1 extension)
zones = [
    ("Mariana",        78,  0.95),
    ("Tonga",          60,  0.85),
    ("Izu–Bonin",      62,  0.70),
    ("Kermadec",       55,  0.60),
    ("New Hebrides",   58,  0.55),
    ("Ryukyu",         50,  0.45),
    ("Lesser Antilles",50,  0.25),
    ("Japan/Tohoku",   32,  0.05),
    ("Kuril",          42,  0.10),
    ("Aleutians",      45,  0.00),
    ("Sunda/Java",     48,  0.05),
    ("Alaska",         30, -0.10),
    ("Sumatra",        40, -0.05),
    ("Cascadia",       25, -0.30),
    ("Nankai",         22, -0.35),
    ("C. Chile",       22, -0.70),
    ("Peru (flat)",    12, -0.90),
]
names = [z[0] for z in zones]
dip = np.array([z[1] for z in zones], float)
strain = np.array([z[2] for z in zones], float)

fig, ax = plt.subplots(figsize=(11.0, 6.6))

# regime background bands
ax.axhspan(0.15, 1.05, color=GREEN, alpha=0.07)
ax.axhspan(-1.05, -0.15, color=VERM, alpha=0.07)
# dip thresholds
ax.axvspan(0, 30, color=VERM, alpha=0.05)
ax.axvspan(50, 90, color=GREEN, alpha=0.05)
ax.axvline(30, color="#999999", ls="--", lw=1.2)
ax.axvline(50, color="#999999", ls="--", lw=1.2)
ax.axhline(0, color=BLACK, lw=1.0)

# colour points by regime
colors = [GREEN if s > 0.15 else VERM if s < -0.15 else ORANGE for s in strain]
ax.scatter(dip, strain, s=110, c=colors, edgecolor=BLACK, lw=0.7, zorder=4)

# explicit label offsets (dx in deg, dy in strain units, ha) to avoid overlaps
offsets = {
    "Mariana":        (1.6, 0.02, "left"),
    "Tonga":          (1.6, 0.03, "left"),
    "Izu–Bonin":      (1.6, 0.02, "left"),
    "Kermadec":       (-1.6, 0.05, "right"),
    "New Hebrides":   (1.6, -0.04, "left"),
    "Ryukyu":         (1.6, 0.0, "left"),
    "Lesser Antilles":(1.6, -0.06, "left"),
    "Japan/Tohoku":   (0.0, 0.07, "center"),
    "Kuril":          (-1.6, 0.06, "right"),
    "Aleutians":      (1.6, -0.07, "left"),
    "Sunda/Java":     (1.8, -0.02, "left"),
    "Alaska":         (-1.6, 0.06, "right"),
    "Sumatra":        (-1.8, -0.07, "right"),
    "Cascadia":       (1.8, 0.04, "left"),
    "Nankai":         (-1.8, 0.05, "right"),
    "C. Chile":       (1.8, 0.0, "left"),
    "Peru (flat)":    (1.8, 0.0, "left"),
}
for n, d, s in zip(names, dip, strain):
    dx, dy, ha = offsets.get(n, (1.4, 0.05, "left"))
    ax.annotate(n, xy=(d, s), xytext=(d + dx, s + dy), fontsize=9, ha=ha)

# threshold labels
ax.text(15, 0.98, "< 30°", ha="center", fontsize=10.5, color="#666666")
ax.text(70, 0.98, "> 50°", ha="center", fontsize=10.5, color="#666666")
ax.text(89, 0.72, "back-arc\nEXTENSION", ha="right", va="center",
        color=GREEN, fontsize=12, fontweight="bold")
ax.text(89, -0.72, "upper-plate\nSHORTENING", ha="right", va="center",
        color=VERM, fontsize=12, fontweight="bold")

ax.set_xlabel("deep slab dip (degrees)")
ax.set_ylabel("back-arc strain    (shortening  ←   0   →  extension)")
ax.set_xlim(5, 90)
ax.set_ylim(-1.05, 1.05)
ax.set_yticks([-1, -0.5, 0, 0.5, 1])
ax.set_title("Deep slab dip controls upper-plate deformation "
             "(Lallemand et al. 2005)")
ax.grid(alpha=0.2)

fig.tight_layout()
out = "../figures/SF5_slabdip_backarc.png"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")
