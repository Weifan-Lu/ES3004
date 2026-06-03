"""
fig_28_convergence_spectrum.py  -> SF7_convergence_spectrum.png

Scientific content: the spectrum of convergent margins, ordered by the buoyancy
of the material arriving at the trench. As a subduction zone consumes its ocean,
the incoming material becomes progressively harder to subduct, and steady-state
subduction gives way to collision and mountain building:
  (a) INTRA-OCEANIC subduction (ocean-ocean): both plates oceanic; weak, thin
      overriding plate; steep slab; volcanic ISLAND arc; back-arc spreading.
      (Mariana, Tonga, Izu-Bonin.)
  (b) OCEAN-CONTINENT subduction: oceanic slab beneath thick, buoyant continental
      plate; shallower dip, stronger coupling; ANDEAN (continental) arc;
      back-arc shortening and a mountain belt. (Andes, Cascadia.)
  (c) ARC-CONTINENT collision: a continental margin arrives at the trench; the
      volcanic arc collides with it, building a doubly-vergent orogen; subduction
      polarity may flip. (Taiwan - collision caught in the act.)
  (d) CONTINENT-CONTINENT collision: buoyant continental crust cannot subduct;
      convergence is taken up by crustal thickening along a detachment megathrust,
      raising a plateau. (Himalaya-Tibet, Arabia-Zagros.)

Schematic, first-principles cross-sections (no copyrighted source). Example
margins and the kinematic ideas follow Uyeda & Kanamori (1979) for the
subduction modes, Teng (1990) for Taiwan arc-continent collision, and Molnar &
Tapponnier (1975) and Avouac et al. (2015) for continental collision and the
Main Himalayan Thrust.

Output: assets/figures/SF7_convergence_spectrum.png
License: CC-BY 4.0 (this script)
"""
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams.update({
    "font.size": 12, "axes.titlesize": 14, "axes.labelsize": 12,
    "xtick.labelsize": 11, "ytick.labelsize": 11, "legend.fontsize": 10.5,
    "figure.dpi": 150, "savefig.dpi": 300,
})

BLUE, ORANGE, SKY, GREEN, VERM, PINK, BLACK = (
    "#0072B2", "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7", "#000000")
OCEAN = BLUE          # oceanic lithosphere
CONT = "#cbb89d"      # continental lithosphere
MANTLE = "#f0e6d2"
SEA = SKY
ARC = VERM


def base(ax, title):
    ax.add_patch(plt.Rectangle((0, -160), 100, 160, facecolor=MANTLE, zorder=0))
    ax.set_xlim(0, 100)
    ax.set_ylim(-160, 70)
    ax.set_title(title, fontsize=13.5)
    ax.set_xticks([])
    ax.set_yticks([0, -50, -100, -150])
    ax.set_yticklabels([0, 50, 100, 150])
    ax.set_ylabel("depth (km)")
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)


def arrow(ax, x0, y0, x1, y1, color=BLACK, lw=2.6, scale=16):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color,
                                mutation_scale=scale))


def slab(ax, x_trench, dip_deg, color=OCEAN, length=210, thick=22, z0=-8):
    dip = np.radians(dip_deg)
    XKM = 2.6  # km per x-unit
    dx, dz = np.cos(dip), -np.sin(dip)
    nx, nz = -np.sin(dip), -np.cos(dip)
    top = np.array([[x_trench, z0],
                    [x_trench + length*dx/XKM, z0 + length*dz]])
    bot = np.array([[x_trench + thick*nx/XKM, z0 + thick*nz],
                    [x_trench + (length*dx+thick*nx)/XKM, z0 + length*dz+thick*nz]])
    ax.add_patch(plt.Polygon(np.vstack([top, bot[::-1]]), closed=True,
                             facecolor=color, edgecolor=BLACK, lw=1.0, zorder=2))


fig, axes = plt.subplots(2, 2, figsize=(13.6, 8.8))

# ---------------------------------------------------------------- (a) intra-oceanic
ax = axes[0, 0]; base(ax, "(a) Intra-oceanic subduction (ocean–ocean)")
ax.add_patch(plt.Rectangle((0, 0), 100, 8, facecolor=SEA, alpha=0.5, zorder=0))
# incoming oceanic plate (left)
ax.fill([0, 38, 38, 0], [-8, -8, -30, -30], facecolor=OCEAN, edgecolor=BLACK, lw=1, zorder=2)
# thin oceanic overriding plate (right)
ax.fill([40, 100, 100, 40], [0, 0, -22, -3], facecolor=OCEAN, alpha=0.6,
        edgecolor=BLACK, lw=1, zorder=3)
slab(ax, 38, 60)
arrow(ax, 8, -18, 22, -18, lw=2.8)
ax.plot([38], [3], marker="v", ms=11, color=BLACK, zorder=6)
# island arc (small, on thin crust)
ax.fill([54, 58, 62], [0, 22, 0], facecolor=ARC, edgecolor=BLACK, zorder=5)
ax.text(58, 30, "island arc", ha="center", fontsize=10.5, color=ARC)
# back-arc spreading
arrow(ax, 74, 14, 68, 14, color=GREEN, lw=2, scale=12)
arrow(ax, 80, 14, 86, 14, color=GREEN, lw=2, scale=12)
ax.text(77, 28, "back-arc\nspreading", ha="center", color=GREEN, fontsize=9.5,
        fontweight="bold")
ax.text(20, -44, "oceanic", ha="center", fontsize=9.5, color=BLUE)
ax.text(70, -34, "thin oceanic\nupper plate", ha="center", fontsize=9, color="#36506a")
ax.text(24, -150, "Mariana, Tonga", ha="center", fontsize=10, style="italic",
        color="#555555")

# ---------------------------------------------------------------- (b) ocean-continent
ax = axes[0, 1]; base(ax, "(b) Ocean–continent subduction")
ax.add_patch(plt.Rectangle((0, 0), 40, 8, facecolor=SEA, alpha=0.5, zorder=0))
ax.fill([0, 36, 36, 0], [-8, -8, -30, -30], facecolor=OCEAN, edgecolor=BLACK, lw=1, zorder=2)
# thick continental overriding plate
ax.fill([38, 100, 100, 39], [4, 4, -42, -6], facecolor=CONT, edgecolor=BLACK, lw=1, zorder=3)
slab(ax, 36, 28)
arrow(ax, 8, -18, 22, -18, lw=2.8)
ax.plot([36], [3], marker="v", ms=11, color=BLACK, zorder=6)
# Andean arc (tall, on thick crust)
ax.fill([60, 64, 68], [4, 40, 4], facecolor=ARC, edgecolor=BLACK, zorder=5)
ax.text(64, 48, "Andean arc", ha="center", fontsize=10.5, color=ARC)
# back-arc shortening
arrow(ax, 78, 16, 72, 16, color=VERM, lw=2, scale=12)
arrow(ax, 90, 16, 84, 16, color=VERM, lw=2, scale=12)
ax.text(82, 28, "shortening", ha="center", color=VERM, fontsize=9.5,
        fontweight="bold")
ax.text(18, -44, "oceanic", ha="center", fontsize=9.5, color=BLUE)
ax.text(80, -26, "thick continental\nupper plate", ha="center", fontsize=9,
        color="#6b5a3a")
ax.text(60, -150, "Andes, Cascadia", ha="center", fontsize=10, style="italic",
        color="#555555")

# ---------------------------------------------------------------- (c) arc-continent
ax = axes[1, 0]; base(ax, "(c) Arc–continent collision")
ax.add_patch(plt.Rectangle((0, 0), 30, 8, facecolor=SEA, alpha=0.5, zorder=0))
# incoming CONTINENTAL margin (left) - buoyant, resists subduction
ax.fill([0, 30, 33, 0], [2, 2, -34, -34], facecolor=CONT, edgecolor=BLACK, lw=1, zorder=2)
# small remnant oceanic slab pulling down (detaching)
slab(ax, 31, 45, length=120, thick=18)
# overriding plate carrying the volcanic arc (right, oceanic affinity)
ax.fill([40, 100, 100, 42], [6, 6, -26, -3], facecolor=OCEAN, alpha=0.55,
        edgecolor=BLACK, lw=1, zorder=3)
# colliding arc - thickening orogen at the join
ax.fill([30, 40, 50], [2, 46, 6], facecolor=ARC, alpha=0.85, edgecolor=BLACK, zorder=5)
ax.fill([34, 40, 47], [10, 40, 12], facecolor="#9c8059", edgecolor=BLACK, lw=0.8, zorder=6)
ax.text(40, 54, "accreted arc →\nrising orogen", ha="center", fontsize=10, color=ARC,
        fontweight="bold")
arrow(ax, 10, -16, 24, -16, lw=2.8)
# doubly-vergent thrusts
arrow(ax, 30, 8, 24, 6, color=BLACK, lw=1.6, scale=11)
arrow(ax, 50, 8, 56, 6, color=BLACK, lw=1.6, scale=11)
ax.text(18, -46, "continental\nmargin (buoyant)", ha="center", fontsize=8.8,
        color="#6b5a3a")
ax.text(72, -22, "arc on\nupper plate", ha="center", fontsize=8.8, color="#36506a")
ax.text(50, -150, "Taiwan (active, oblique)", ha="center", fontsize=10,
        style="italic", color="#555555")

# ---------------------------------------------------------------- (d) continent-continent
ax = axes[1, 1]; base(ax, "(d) Continent–continent collision")
# lower plate (India) underthrusting
ax.fill([0, 60, 72, 0], [-6, -6, -52, -40], facecolor=CONT, edgecolor=BLACK, lw=1,
        zorder=2)
# upper plate (Eurasia) overriding + thickened plateau
ax.fill([46, 100, 100, 58], [10, 10, -40, -8], facecolor="#bda884",
        edgecolor=BLACK, lw=1, zorder=3)
# thickened crust / plateau topography
ax.fill([40, 55, 70, 85, 96], [12, 34, 38, 30, 16],
        facecolor="#9c8059", edgecolor=BLACK, lw=1, zorder=4)
ax.text(68, 50, "thickened crust → plateau", ha="center", fontsize=10.5,
        color="#6b5a3a", fontweight="bold")
# detachment / Main Himalayan Thrust
ax.plot([10, 30, 48, 60], [-12, -16, -12, -4], color=VERM, lw=4,
        solid_capstyle="round", zorder=5)
ax.annotate("detachment megathrust\n(Main Himalayan Thrust:\ngreat earthquakes)",
            xy=(40, -13), xytext=(30, -90), ha="center", fontsize=9, color=VERM,
            fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1.5))
arrow(ax, 8, -26, 22, -26, lw=2.8)
# suture marker
ax.plot([52], [13], marker="v", ms=10, color=BLACK, zorder=6)
ax.text(52, 22, "suture", ha="center", fontsize=9)
ax.text(16, -52, "lower continent\n(India)", ha="center", fontsize=8.8,
        color="#6b5a3a")
ax.text(64, -150, "Himalaya–Tibet, Arabia–Zagros", ha="center", fontsize=10,
        style="italic", color="#555555")

fig.suptitle("The convergence spectrum: buoyancy of the incoming material "
             "decides subduction vs. collision", fontsize=15, y=0.995)
fig.text(0.5, 0.945,
         "Left to right, top to bottom: as the trench consumes ocean and meets "
         "ever more buoyant crust, steady subduction gives way to mountain-building collision.",
         ha="center", fontsize=10.5, color="#444444")
fig.tight_layout(rect=[0, 0, 1, 0.93])
out = "../figures/SF7_convergence_spectrum.png"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")
