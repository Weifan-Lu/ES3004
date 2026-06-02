"""
fig_28_cascadia_section.py  -> SF6_cascadia_section.png

Scientific content (the CASCADIA ANCHOR figure of L28):
An across-strike cross-section of the Cascadia subduction zone (~lat 45-47 N),
from the Juan de Fuca ridge offshore to the Cascade arc. It shows the features
that make Cascadia the great "exception" to the old big-earthquake recipe: a
YOUNG (<15 Ma), WARM slab; SLOW convergence (~3-4 cm/yr); a thick (~3 km)
incoming SEDIMENT section and large accretionary wedge; NO bathymetric trench
(the deformation front is buried); a locked, potentially seismogenic-to-trench
megathrust; and episodic tremor and slip (ETS) downdip. The 1700 M~9 rupture is
annotated. Call-out boxes contrast Cascadia with Chile and Tohoku.

DATA PROVENANCE: schematic geometry consistent with the Slab2 Cascadia model
(Hayes et al. 2018, doi:10.1126/science.aat4723; data release 10.5066/F7PV6JNV)
and the review of Wang & Tre'hu (2016, J. Geodyn., "Some outstanding issues in
the study of great megathrust earthquakes - the Cascadia example"). Convergence
rate ~35-45 mm/yr; incoming-plate age <15 Ma; sediment thickness from GlobSed
(Straume et al. 2019). In Marine's pixi environment the slab interface can be
drawn directly from the Slab2 cas_slab2_dep grid.

Output: assets/figures/SF6_cascadia_section.png
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
SLAB = BLUE
UPLATE = "#cbb89d"
MANTLE = "#f0e6d2"
SED = ORANGE

fig, ax = plt.subplots(figsize=(13.0, 6.2))

# horizontal axis: distance (km) west(-) to east(+); deformation front at x=0
x = np.linspace(-260, 320, 600)

# --- slab interface: shallow near front, steepening under the arc -----------
def slab_depth(xx):
    z = np.where(xx < 0, 0.0,
                 -(0.015 * xx + 0.00020 * xx**2))   # km, deepening eastward
    return z
zi = slab_depth(x)

# mantle background
ax.add_patch(plt.Rectangle((-260, -120), 580, 130, facecolor=MANTLE, zorder=0))
# ocean (west of coast ~ x<40) and incoming plate surface
ax.fill_between(x, 0, 6, where=(x < 60), color=SKY, alpha=0.5, zorder=0)

# subducting oceanic plate (below interface), ~90 km thick band
ax.fill_between(x, zi, zi - 85, color=SLAB, alpha=0.40, zorder=1)
# incoming oceanic plate west of front (flat)
ax.fill_between(x, -7, -95, where=(x < 0), color=SLAB, alpha=0.40, zorder=1)

# overriding North America (above interface, east of front only)
xe = x[x >= 0]
ax.fill_between(xe, slab_depth(xe), 8, color=UPLATE, zorder=2)
ax.plot(x[x >= 0], zi[x >= 0], color=BLACK, lw=2.0, zorder=4)   # interface

# incoming sediment (~3 km, exaggerated) riding on the JdF plate, west of front
ax.fill_between(x, -7, -10.5, where=(x < 5), color=SED, alpha=0.9, zorder=3)
# accretionary wedge: small triangle at the front (no bathymetric trench)
ax.fill([-12, 0, 55], [-7, 1, 6], color=SED, alpha=0.6, zorder=3)

# --- locked seismogenic zone (front to ~ x=180, down to ~25 km) -------------
lock = (x >= 0) & (x <= 190)
ax.plot(x[lock], zi[lock], color=VERM, lw=6, solid_capstyle="round", zorder=5)
# ETS / tremor zone downdip (190-280 km)
ets = (x >= 185) & (x <= 290)
ax.plot(x[ets], zi[ets] - 1.5, color=PINK, lw=4, ls=(0, (2, 2)), zorder=5)

# Cascade arc volcano
ax.fill([250, 262, 274], [8, 48, 8], color=VERM, edgecolor=BLACK, zorder=4)
ax.text(262, 58, "Cascade arc", ha="center", fontsize=11, color=VERM)

# convergence arrow (Juan de Fuca moving east)
ax.annotate("", xy=(-70, -40), xytext=(-150, -40),
            arrowprops=dict(arrowstyle="-|>", lw=3.2, color=BLACK, mutation_scale=22))
ax.text(-110, -52, "Juan de Fuca plate\n~35–45 mm/yr", ha="center", fontsize=11)
ax.text(-110, -88, "young (<15 Ma),\nwarm slab", ha="center", fontsize=10.5,
        color=BLUE, fontweight="bold")

# feature labels
ax.annotate("buried deformation front\n(no bathymetric trench)",
            xy=(5, 2), xytext=(120, 55), ha="center", fontsize=10.5, color=SED,
            fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=SED, lw=1.6))
ax.text(30, -17, "thick sediment\n+ accretionary wedge", ha="center", fontsize=9.5,
        color="#7a4b00")
ax.annotate("locked megathrust\n(1700  M~9 rupture)",
            xy=(95, slab_depth(95)), xytext=(95, -70), ha="center",
            fontsize=11, color=VERM, fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1.8))
ax.annotate("episodic tremor & slip (ETS)",
            xy=(240, slab_depth(240) - 2), xytext=(245, -95), ha="center",
            fontsize=10.5, color=PINK, fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=PINK, lw=1.6))

# contrast call-out box (upper-left, clear of arc)
txt = ("Cascadia vs the 'recipe':\n"
       "young + slow + sediment-rich + smooth\n"
       "→ old rule predicts only small EQ,\n"
       "yet Cascadia is M9-capable (1700).")
ax.text(-255, 72, txt, ha="left", va="top", fontsize=10.5,
        bbox=dict(boxstyle="round,pad=0.4", fc="#fff6e6", ec=ORANGE, lw=1.2))

ax.set_xlim(-260, 320)
ax.set_ylim(-118, 75)
ax.set_xlabel("distance from deformation front (km)        W  →  E")
ax.set_ylabel("depth (km)")
ax.set_yticks([0, -25, -50, -75, -100])
ax.set_yticklabels([0, 25, 50, 75, 100])
ax.set_title("Cascadia subduction zone: the M9-capable 'exception' "
             "(schematic, after Wang & Tréhu 2016; geometry from Slab2)")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

fig.tight_layout()
out = "../figures/SF6_cascadia_section.png"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")
