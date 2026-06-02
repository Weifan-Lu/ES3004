"""
fig_28_rupture_domains.py  -> SF4_rupture_domains.png

Scientific content: The four depth-varying megathrust rupture domains of
Lay et al. (2012). Along the subduction interface from the trench downdip:
  A (trench to ~15 km): near-trench domain; tsunami earthquakes, anelastic
    deformation, stable sliding; largest SEAFLOOR slip -> dominant TSUNAMI source.
  B (~15-35 km): central domain; large coseismic slip, modest short-period
    radiation; the core of great ruptures.
  C (~35-55 km): downdip domain; isolated patches, strong coherent short-period
    radiation -> dominant STRONG-GROUND-MOTION source.
  D (~30-45 km, only where young/warm slab & shallow dip): slow-slip events,
    tremor, low-frequency earthquakes; transition to stable sliding.

Reproduces the scientific content of (original figure NOT used):
  Lay, T., Kanamori, H., Ammon, C. J., et al. (2012). Depth-varying rupture
  properties of subduction zone megathrust faults. J. Geophys. Res. 117, B04311,
  doi:10.1029/2011JB009133.

Output: assets/figures/SF4_rupture_domains.png
License: CC-BY 4.0 (this script)
"""
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 16, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 11.5,
    "figure.dpi": 150, "savefig.dpi": 300,
})

BLUE, ORANGE, SKY, GREEN, VERM, PINK, BLACK = (
    "#0072B2", "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7", "#000000")

fig, ax = plt.subplots(figsize=(12.0, 6.4))

# Interface geometry: gently steepening megathrust from trench (0,0) downdip.
x = np.linspace(0, 320, 400)          # horizontal distance from trench (km)
# depth increases with a slightly increasing dip
z = -(0.06 * x + 0.00035 * x**2)       # km (negative down)

# overriding plate (above interface) and subducting slab (below)
ax.fill_between(x, z, 10, color="#cbb89d", alpha=0.55, zorder=1)   # upper plate
ax.fill_between(x, z, z - 45, color=BLUE, alpha=0.45, zorder=0)     # slab
ax.plot(x, z, color=BLACK, lw=2.2, zorder=3)                       # interface
# ocean layer
ax.fill_between(x, 0, 10, color=SKY, alpha=0.4, zorder=0)

# Domain boundaries by interface depth (km): A 0-15, B 15-35, C 35-55, D overlap
def x_at_depth(d):
    # invert z = -(0.06 x + 0.00035 x^2) = -d  ->  0.00035 x^2 + 0.06 x - d = 0
    a, b, c = 0.00035, 0.06, -d
    return (-b + np.sqrt(b**2 - 4*a*c)) / (2*a)

xb = {d: x_at_depth(d) for d in (15, 35, 55)}

dom_colors = {"A": GREEN, "B": ORANGE, "C": VERM, "D": PINK}
spans = [("A", 0, xb[15]), ("B", xb[15], xb[35]), ("C", xb[35], xb[55])]
for name, xa, xc in spans:
    m = (x >= xa) & (x <= xc)
    ax.plot(x[m], z[m], color=dom_colors[name], lw=6, solid_capstyle="butt",
            zorder=4, alpha=0.9)

# Domain D: slow-slip transition just downdip of C (overlapping depth band)
xD0, xD1 = xb[35], xb[55] + 35
mD = (x >= xD0) & (x <= xD1)
ax.plot(x[mD], z[mD] - 2.5, color=PINK, lw=3, ls=(0, (2, 2)), zorder=5)

# Labels for each domain (placed BELOW the interface, leaders pointing down)
def dom_label(name, dtxt, sub, xa, xc, dy):
    xm = 0.5 * (xa + xc)
    zm = -(0.06 * xm + 0.00035 * xm**2)
    ax.annotate(f"{name}", xy=(xm, zm), xytext=(xm, zm + dy),
                ha="center", fontsize=15, fontweight="bold",
                color=dom_colors[name],
                arrowprops=dict(arrowstyle="-", color=dom_colors[name], lw=1.2))
    ax.text(xm, zm + dy - 7, dtxt, ha="center", fontsize=10.5, color=BLACK,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75))
    ax.text(xm, zm + dy - 18, sub, ha="center", fontsize=9.5, color="#333333",
            style="italic",
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75))

dom_label("A", "near-trench", "tsunami EQ • stable slip", 0, xb[15], -26)
dom_label("B", "central", "large slip", xb[15], xb[35], -34)
dom_label("C", "downdip", "strong ground motion", xb[35], xb[55], -42)
ax.text(0.5*(xb[35]+xD1) + 20, z[mD][-1] - 16,
        "D: slow slip,\ntremor, LFEs", ha="center", fontsize=10, color=PINK,
        fontweight="bold")

# trench marker + tsunami arrow above domain A
ax.plot([0], [3], marker="v", ms=13, color=BLACK, zorder=6)
ax.text(0, 17, "trench", ha="center", fontsize=11)
ax.annotate("", xy=(20, 26), xytext=(20, 9),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.5, mutation_scale=18))
ax.text(34, 22, "seafloor uplift\n→ tsunami", fontsize=10.5, color=BLUE, va="center")

# depth grid lines
for d in (15, 35, 55):
    ax.axhline(-d, color="#999999", lw=0.7, ls=":", zorder=0)
    ax.text(318, -d + 1.5, f"{d} km", ha="right", fontsize=9.5, color="#666666")

ax.set_xlim(-8, 322)
ax.set_ylim(-118, 40)
ax.set_xlabel("distance from trench (km)")
ax.set_ylabel("depth (km)")
ax.set_yticks([0, -25, -50, -75, -100])
ax.set_yticklabels([0, 25, 50, 75, 100])
ax.set_title("Depth-varying megathrust rupture domains (Lay et al. 2012)", pad=14)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

fig.tight_layout()
out = "../figures/SF4_rupture_domains.png"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")
