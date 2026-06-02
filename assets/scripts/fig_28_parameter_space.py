"""
fig_28_parameter_space.py  -> SF3_parameter_space.png

Scientific content (the CENTERPIECE figure of L28):
A scatter of major subduction-zone segments in the classic classification space —
incoming-plate AGE vs CONVERGENCE RATE — with marker size/colour encoding the
maximum observed moment magnitude (Mw). The Ruff & Kanamori (1980) hypothesis
predicted that old + fast slabs host the largest earthquakes (upper-right) and
young + slow slabs host only small ones (lower-left). The data overplotted here
show that the great (Mw >= 9) earthquakes span essentially the ENTIRE age-rate
plane: Chile-1960 (young, fast), Cascadia-1700 (young, slow), Tohoku-2011 (old,
fast), Sumatra-2004 (old, slow). The correlation the hypothesis predicted is not
present. A companion panel shows Mw vs trench sediment thickness, the
second-order control favoured by the modern literature.

This is the figure that demonstrates the "recipe -> falsification" arc.

DATA PROVENANCE: values are representative, literature-compiled, and rounded for
teaching. They are NOT a substitute for the primary databases. Per-zone age and
convergence rate follow the global compilations of Heuret & Lallemand (2005,
Phys. Earth Planet. Inter.) and the SubMap database; convergence rates are
consistent with MORVEL (DeMets et al. 2010, GJI). Trench sediment thickness is
read from GlobSed (Straume et al. 2019, G-Cubed, doi:10.1029/2018GC008115).
Maximum magnitudes are from the global instrumental/paleoseismic record as
summarised by Wirth et al. (2022, Nat. Rev. Earth Environ.,
doi:10.1038/s43017-021-00245-w) and the USGS/Global CMT catalogues. In Marine's
pixi environment the scatter can be regenerated exactly from Slab2 (geometry),
the Muller/Seton age grid, GlobSed, and a plate-motion model; see the companion
notebook subduction_parameter_space.ipynb.

Reproduces the scientific content of (original figures NOT used):
  Ruff, L. & Kanamori, H. (1980). Seismicity and the subduction process.
    Phys. Earth Planet. Inter. 23, 240-252.
  Wirth, E. A. et al. (2022). The occurrence and hazards of great subduction
    zone earthquakes. Nat. Rev. Earth Environ. 3, 125-140.

Output: assets/figures/SF3_parameter_space.png
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

# ---------------------------------------------------------------------------
# Curated per-zone table (representative, literature-compiled; see provenance).
# columns: name, age_Ma, rate_mm_yr, sediment_km, Mw_max, short_label
# ---------------------------------------------------------------------------
zones = [
    # name,                 age, rate, sed,  Mw,   label
    ("S. Chile (1960)",       20,   74, 1.3,  9.5, "Chile 1960"),
    ("Alaska (1964)",         48,   57, 3.5,  9.2, "Alaska 1964"),
    ("Sumatra–Andaman (2004)",55,   45, 2.5,  9.1, "Sumatra 2004"),
    ("Tohoku (2011)",        130,   83, 0.5,  9.1, "Tohoku 2011"),
    ("Kamchatka (1952)",      95,   80, 1.0,  9.0, "Kamchatka 1952"),
    ("Cascadia (1700)",       10,   40, 3.0,  9.0, "Cascadia 1700"),
    ("Maule, Chile (2010)",   33,   68, 1.0,  8.8, None),
    ("Ecuador–Colombia (1906)",18,  55, 1.5,  8.8, None),
    ("Aleutians (1957)",      55,   65, 1.5,  8.6, None),
    ("Kuril (1963)",         110,   82, 1.0,  8.5, None),
    ("Nankai (1707)",         20,   55, 2.0,  8.4, None),
    ("N. Chile/Peru",         48,   65, 0.2,  8.4, None),
    ("Sunda/Java",           110,   65, 1.2,  7.8, None),
    ("New Hebrides",          45,  110, 0.5,  7.9, None),
    ("Tonga",                130,  165, 0.4,  8.0, "Tonga"),
    ("Kermadec",             100,   55, 0.4,  8.1, None),
    ("Izu–Bonin",            145,   50, 0.4,  7.4, "Izu–Bonin"),
    ("Mariana",              155,   35, 0.4,  7.3, "Mariana"),
]
names = [z[0] for z in zones]
age = np.array([z[1] for z in zones], float)
rate = np.array([z[2] for z in zones], float)
sed = np.array([z[3] for z in zones], float)
Mw = np.array([z[4] for z in zones], float)
labels = [z[5] for z in zones]


def msize(mw):
    return 30 + (mw - 7.0) ** 2.4 * 95.0   # emphasise the great events


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 6.4),
                               gridspec_kw={"width_ratios": [1.35, 1]})

# ===== Panel (a): age vs rate, sized/coloured by Mw =========================
great = Mw >= 8.95
sc = ax1.scatter(age[~great], rate[~great], s=msize(Mw[~great]),
                 c=Mw[~great], cmap="viridis", vmin=7.0, vmax=9.6,
                 edgecolor=BLACK, lw=0.7, alpha=0.9, zorder=3)
# great earthquakes: same colour scale, ringed in vermillion + star
ax1.scatter(age[great], rate[great], s=msize(Mw[great]),
            c=Mw[great], cmap="viridis", vmin=7.0, vmax=9.6,
            edgecolor=VERM, lw=2.4, zorder=4)
ax1.scatter(age[great], rate[great], marker="*", s=70, color="white",
            edgecolor=BLACK, lw=0.4, zorder=5)

cb = fig.colorbar(sc, ax=ax1, pad=0.02)
cb.set_label("maximum observed $M_w$")

# the "classic recipe" prediction annotation
ax1.annotate("Ruff–Kanamori (1980) recipe:\nbig EQ expected here",
             xy=(150, 150), xytext=(95, 150), ha="left", va="center",
             fontsize=10.5, color="#555555", style="italic",
             arrowprops=dict(arrowstyle="-|>", color="#999999", lw=1.5))
ax1.add_patch(plt.Rectangle((90, 95), 80, 95, fill=False, ls="--",
                            ec="#999999", lw=1.3, zorder=1))

# label the great events
for n, a, r, lab, m in zip(names, age, rate, labels, Mw):
    if lab is not None:
        dx, dy = (4, 7)
        if lab == "Mariana":
            dx, dy = (-4, 9)
        elif lab == "Izu–Bonin":
            dx, dy = (4, 9)
        elif lab == "Tonga":
            dx, dy = (-6, 9)
        elif lab == "Kamchatka 1952":
            dx, dy = (-30, 12)
        elif lab == "Tohoku 2011":
            dx, dy = (4, -16)
        ax1.annotate(lab, xy=(a, r), xytext=(a + dx, r + dy), fontsize=9.5,
                     color=BLACK, fontweight="bold" if m >= 8.95 else "normal")

ax1.set_xlabel("incoming-plate age at trench (Ma)")
ax1.set_ylabel("convergence rate (mm/yr)")
ax1.set_xlim(0, 175)
ax1.set_ylim(25, 195)
ax1.set_title("(a)  The classic classification space")
ax1.grid(alpha=0.25)

# ===== Panel (b): Mw vs sediment thickness ==================================
ax2.scatter(sed[~great], Mw[~great], s=70, c=BLUE, edgecolor=BLACK, lw=0.6,
            alpha=0.85, zorder=3, label="$M_w$ < 9")
ax2.scatter(sed[great], Mw[great], s=150, marker="*", c=VERM,
            edgecolor=BLACK, lw=0.7, zorder=4, label="$M_w \\geq 9$")
for n, s_, m, lab in zip(names, sed, Mw, labels):
    if lab is not None and m >= 8.95:
        ax2.annotate(lab, xy=(s_, m), xytext=(s_ + 0.08, m - 0.06),
                     fontsize=9, color=BLACK)
ax2.set_xlabel("trench sediment thickness (km)")
ax2.set_ylabel("maximum observed $M_w$")
ax2.set_xlim(0, 4.0)
ax2.set_ylim(7.0, 9.8)
ax2.set_title("(b)  A second-order control:\nsediment smoothing")
ax2.grid(alpha=0.25)
ax2.legend(loc="lower right", framealpha=0.9)

fig.suptitle("Subduction zones in parameter space: the recipe that data "
             "dispelled", fontsize=16, y=1.01)
fig.tight_layout()
out = "../figures/SF3_parameter_space.png"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")

# quick console sanity check: do the great events span the plane?
print(f"Great (Mw>=9) events: age {age[great].min():.0f}-{age[great].max():.0f} Ma, "
      f"rate {rate[great].min():.0f}-{rate[great].max():.0f} mm/yr")
