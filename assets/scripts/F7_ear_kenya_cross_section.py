"""
F7_ear_kenya_cross_section.py

East African Rift cross-section through the Kenya Rift at ~0–1°N
showing the canonical three-panel structure:

(a) Bouguer gravity along an E–W transect — broad gravity low (~−250 mGal)
    bounded by negative shoulders and a small central positive over the
    rift axis from shallow magmatic intrusion.
(b) Topography along the same transect — broad uplift with a central axial
    graben.
(c) Density / Vp cross-section to 80 km depth — thinned crust under the
    rift axis (Moho rises from ~37 km to ~22 km), low-velocity mantle
    "Kenya dome" beneath, magmatic dyke injection zone in the upper crust.

After: Mechie, J. et al. (1997). A model for the structure, composition
and evolution of the Kenya Rift. Tectonophysics 278, 95–119.
Baker, B. H. & Wohlenberg, J. (1971). Structure and evolution of the
Kenya Rift Valley. Nature 229, 538–542. KRISP working group (1991,
1995). Both summarised in Lowrie & Fichtner 2020 §10.

For the canonical open-access modern reference, see:
  Plasman, M. et al. (2017). Lithospheric structure under the central
  Main Ethiopian Rift from passive seismic imaging. Geophys. J. Int.
  210, 1481–1494. doi:10.1093/gji/ggx245. [verify license at fetch time]

Output: assets/figures/F7_ear_kenya_cross_section.png
License: CC-BY 4.0 (this script)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _ess314_style import apply_style, PALETTE, save

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def make_figure():
    apply_style()

    # Transect: 200 km wide centred on rift axis at ~36°E
    x = np.linspace(-100, 100, 401)

    # ── (a) Bouguer anomaly ──
    # Broad negative low over the rift ~ −230 mGal from Mechie 1997 model
    # with small central positive from shallow magmatic high-density body
    bouguer = -120.0 \
              - 130.0 * np.exp(-(x ** 2) / (50 ** 2)) \
              + 25.0 * np.exp(-(x ** 2) / (10 ** 2))

    # ── (b) Topography ──
    # Broad uplift ~1700 m with central axial graben at ~900 m
    topo_m = 800.0 \
             + 1100.0 * np.exp(-(x ** 2) / (60 ** 2)) \
             - 600.0 * np.exp(-(x ** 2) / (15 ** 2))

    # ── Build figure ──
    fig = plt.figure(figsize=(11, 9))
    gs = fig.add_gridspec(3, 1, height_ratios=[0.9, 0.9, 2.0], hspace=0.35)

    ax_g = fig.add_subplot(gs[0])
    ax_t = fig.add_subplot(gs[1], sharex=ax_g)
    ax_c = fig.add_subplot(gs[2], sharex=ax_g)

    # ── Gravity panel ──
    ax_g.plot(x, bouguer, color=PALETTE["verm"], lw=2.0)
    ax_g.axhline(0, color="k", lw=0.5, ls=":", alpha=0.5)
    ax_g.set_ylabel("Bouguer (mGal)")
    ax_g.set_title("(a) Bouguer gravity anomaly — broad rift low "
                   "with central magmatic high",
                   loc="left", fontsize=11)
    ax_g.text(0, -200, "central magmatic high",
              fontsize=9, ha="center", color=PALETTE["verm"], style="italic")
    ax_g.text(0, -280, "broad rift low (~−250 mGal)",
              fontsize=9, ha="center", color=PALETTE["verm"], style="italic")
    ax_g.grid(True, alpha=0.3)
    ax_g.set_ylim(-300, 60)

    # ── Topography panel ──
    ax_t.fill_between(x, 0, topo_m,
                       where=(topo_m > 0),
                       facecolor="#c89060", alpha=0.6)
    ax_t.plot(x, topo_m, color=PALETTE["black"], lw=1.2)
    ax_t.set_ylabel("Elevation (m)")
    ax_t.set_title("(b) Topography — broad rift uplift with axial graben",
                   loc="left", fontsize=11)
    ax_t.text(0, 250, "axial\ngraben", fontsize=9, ha="center", style="italic")
    ax_t.text(-65, 1750, "rift shoulder", fontsize=9, ha="center", style="italic")
    ax_t.text(65, 1750, "rift shoulder", fontsize=9, ha="center", style="italic")
    ax_t.grid(True, alpha=0.3)
    ax_t.set_ylim(-100, 2300)

    # ── Cross-section panel ──
    ax_c.set_xlim(-100, 100)
    ax_c.set_ylim(80, 0)
    ax_c.set_xlabel("Distance from rift axis (km)")
    ax_c.set_ylabel("Depth (km)")
    ax_c.set_title("(c) Density / Vp cross-section — thinned crust, "
                    "low-velocity mantle 'Kenya dome'",
                    loc="left", fontsize=11)

    # Moho geometry: 37 km off-axis, rises to 22 km at axis over ~60 km width
    moho = 22 + 15 * (1 - np.exp(-(x ** 2) / (35 ** 2)))

    # Upper crust top: rift axis is at sea-level-equivalent
    crust_top = -topo_m / 1000.0  # negative = above sea level
    crust_top = np.clip(crust_top, -2.5, 0.6)

    # ── Crustal layers ──
    # Upper crust (granitic, ~2.7 g/cm³)
    ax_c.fill_between(x, crust_top, moho * 0.55,
                      facecolor="#c8a070", edgecolor="none", zorder=2)
    # Lower crust (mafic, ~2.9 g/cm³)
    ax_c.fill_between(x, moho * 0.55, moho,
                      facecolor="#a07050", edgecolor="none", zorder=2)
    # Upper mantle background (3.3 g/cm³)
    ax_c.fill_between(x, moho, 80,
                      facecolor="#e8d8b8", edgecolor="none", zorder=1)

    # Low-velocity / low-density mantle dome (Kenya dome)
    kdome_x = np.linspace(-90, 90, 200)
    kdome_top = 22 + 15 * (1 - np.exp(-(kdome_x ** 2) / (40 ** 2))) + 1.5
    kdome_bot = 80 * np.ones_like(kdome_x)
    ax_c.fill(np.concatenate([kdome_x, kdome_x[::-1]]),
              np.concatenate([kdome_top, kdome_bot[::-1]]),
              facecolor=PALETTE["verm"], alpha=0.30,
              edgecolor=PALETTE["verm"], lw=1.0, zorder=3)
    ax_c.text(0, 55, "low-velocity / low-density\nmantle dome\n"
                       "(Vp ~ 7.4 km/s; Δρ ~ −0.04)",
              fontsize=10, ha="center", va="center",
              bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                          edgecolor=PALETTE["verm"], alpha=0.9))

    # Dyke injection zone (narrow vertical strip in upper crust)
    ax_c.add_patch(mpatches.Rectangle((-5, -1), 10, 18,
                                         facecolor="#8e3500",
                                         edgecolor=PALETTE["verm"], lw=0.8,
                                         alpha=0.8, zorder=4))
    ax_c.text(8, 9, "dyke injection\n(magmatic\nsegment)", fontsize=9,
              ha="left", va="center", color=PALETTE["verm"])

    # Moho line
    ax_c.plot(x, moho, color="black", lw=1.5, zorder=5)
    ax_c.text(-95, 22, "Moho", fontsize=10, style="italic")

    # Labels
    ax_c.text(-95, 8, "upper crust\n(~2.7 g/cm³)", fontsize=9.5,
              color="black")
    ax_c.text(-95, 17, "lower crust\n(~2.9)", fontsize=9.5, color="white")
    ax_c.text(-95, 75, "fertile mantle (3.3 g/cm³)", fontsize=9.5,
              color="black")

    fig.suptitle("East African Rift — geophysical cross-section through "
                  "Kenya Rift (after Mechie et al. 1997)",
                  fontsize=13, y=0.995)

    return fig


if __name__ == "__main__":
    fig = make_figure()
    out = os.path.join(os.path.dirname(__file__), "..", "figures",
                       "F7_ear_kenya_cross_section.png")
    save(fig, out)
    print(f"Wrote {out}")
