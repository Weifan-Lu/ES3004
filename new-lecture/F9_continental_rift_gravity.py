"""
F9_continental_rift_gravity.py

Continental rift gravity decomposition — a forward model showing how the
Bouguer anomaly over a continental rift arises from three additive
contributions:

  1. Topography (positive, narrow): the central rift valley's high-density
     basaltic infill and uplifted shoulders contribute positively.
  2. Moho relief (positive): rift-thinned crust brings dense mantle closer
     to the surface, raising the anomaly.
  3. Lithosphere–asthenosphere boundary (negative, broad): thinned mantle
     lithosphere replaced by hotter, less dense asthenosphere lowers the
     long-wavelength gravity.

The sum produces the canonical broad negative anomaly with smaller central
features that characterises continental rifts at the gravity-method scale.
This is the "physics-math" decomposition figure — its purpose is to show
that the observed Bouguer anomaly is the *sum* of identifiable physical
contributions, each tied to a structural element of the rift.

After: Lowrie & Fichtner (2020), Fundamentals of Geophysics, §8.5 Fig. 8.42.
For pedagogical comparison with the cratonic baseline, see also Fig. 8.41.

Output: assets/figures/F9_continental_rift_gravity.png
License: CC-BY 4.0 (this script)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _ess314_style import apply_style, PALETTE, save

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def gauss(x, amp, x0, sigma):
    return amp * np.exp(-((x - x0) ** 2) / (2.0 * sigma ** 2))


def make_figure():
    apply_style()

    x = np.linspace(-500, 500, 1001)

    # ── Three contributions ──
    # 1. Topographic (rift valley + flanking uplift): small positive narrow
    g_topo = gauss(x, 35, 0, 60) - gauss(x, 25, 0, 18)
    # Net "topography" trace dominated by uplifted shoulders + axial high

    # 2. Moho relief: positive, intermediate width (~60 km)
    # Δρ = +0.4 g/cm³ across the crust-mantle interface; rift Moho shallowed
    g_moho = gauss(x, 90, 0, 70)

    # 3. Lith/asth thinning: negative, very broad (~200 km)
    # Δρ = −0.04 g/cm³ across the LAB; large width → large total mass deficit
    g_lab = -gauss(x, 220, 0, 180)

    # Net Bouguer anomaly is the sum
    g_total = g_topo + g_moho + g_lab

    # ── Build figure ──
    fig = plt.figure(figsize=(12, 9.5))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.3], hspace=0.32)

    ax_g = fig.add_subplot(gs[0])
    ax_m = fig.add_subplot(gs[1], sharex=ax_g)

    # ── (a) Gravity contributions ──
    ax_g.plot(x, g_topo, color=PALETTE["orange"], lw=2.0, ls="--",
              label="Topography contribution (narrow, positive)")
    ax_g.plot(x, g_moho, color=PALETTE["green"], lw=2.0, ls="-.",
              label="Moho relief contribution (intermediate, positive)")
    ax_g.plot(x, g_lab, color=PALETTE["blue"], lw=2.0, ls=":",
              label="Lith–asth thinning contribution (broad, negative)")
    ax_g.plot(x, g_total, color=PALETTE["black"], lw=2.6,
              label="Total Bouguer anomaly = sum")

    ax_g.axhline(0, color="k", lw=0.5, alpha=0.5)
    ax_g.set_xlim(-500, 500)
    ax_g.set_ylim(-280, 200)
    ax_g.set_ylabel("Bouguer anomaly contribution (mGal)")
    ax_g.set_title("(a) Decomposition of the continental-rift Bouguer "
                   "anomaly into three additive contributions",
                   loc="left", fontsize=11)
    ax_g.legend(loc="lower right", framealpha=0.95, fontsize=9.5)
    ax_g.grid(True, alpha=0.3)

    # Annotation on the total
    idx_min = int(np.argmin(g_total))
    ax_g.annotate(f"total\n~{g_total[idx_min]:.0f} mGal",
                  xy=(x[idx_min], g_total[idx_min]),
                  xytext=(180, -200),
                  fontsize=10, color=PALETTE["black"],
                  arrowprops=dict(arrowstyle="->", color=PALETTE["black"],
                                  lw=1.0))

    # ── (b) Cross-section schematic ──
    ax_m.set_xlim(-500, 500)
    ax_m.set_ylim(220, -3)  # depth km, surface at top (slight headroom)
    ax_m.set_xlabel("Distance from rift axis (km)")
    ax_m.set_ylabel("Depth (km)")
    ax_m.set_title("(b) Density model — each contribution traced to a "
                   "structural element",
                   loc="left", fontsize=11)

    # Sky
    ax_m.fill_between(x, -3, 0, facecolor="#e7f1f7", edgecolor="none")
    # Topography: uplifted shoulders + axial graben (rift valley)
    topo_km = -0.0014 * gauss(x, 1100, 0, 60) + 0.0010 * gauss(x, 700, 0, 18)
    # Actually compute topo_km positive = uplift, negative = subsidence
    topo_km = -(1.7 * np.exp(-(x ** 2) / (60 ** 2))) \
              + 1.1 * np.exp(-(x ** 2) / (18 ** 2))
    # In a "depth-below-mean-sea-level" frame, negative topo = above sea level
    # We render surface as a line; positive on the elevation axis goes up.
    # Convert to depth coordinate (negative depths = above): we plot ax_m.fill
    # between surface and crust base.
    surface_y = topo_km  # negative numbers float above 0

    # Upper crust: surface → 18 km
    crust_top = surface_y
    # Moho geometry: 30 km off-axis, rises to 22 km at axis (rift)
    moho = 32 - 10 * np.exp(-(x ** 2) / (60 ** 2))

    # ── Layers ──
    # Upper crust (granitic, ~2.7 g/cm³)
    crust_mid = 0.5 * (crust_top + moho)
    ax_m.fill_between(x, crust_top, crust_mid,
                      facecolor="#c8a070", edgecolor="none")
    # Lower crust (mafic, ~2.9)
    ax_m.fill_between(x, crust_mid, moho,
                      facecolor="#a07050", edgecolor="none")
    # Background mantle lithosphere (3.30, depleted)
    lab = 150 - 30 * np.exp(-(x ** 2) / (180 ** 2))
    ax_m.fill_between(x, moho, lab,
                      facecolor="#e8d8b8", edgecolor="none")
    # Asthenosphere below (3.26, less dense than mantle litho)
    ax_m.fill_between(x, lab, 220, facecolor="#f7c79a", edgecolor="none")
    # Highlight the thinned mantle litho / asthenosphere upwelling
    ax_m.fill_between(x, moho, lab, where=(np.abs(x) < 200),
                      facecolor=PALETTE["verm"], alpha=0.12)

    # Annotate structural elements
    # Topography arrow
    ax_m.annotate("rift shoulders + axial graben",
                  xy=(0, -1.5), xytext=(-280, -2.5), fontsize=9.5,
                  color=PALETTE["orange"], ha="left",
                  arrowprops=dict(arrowstyle="->", color=PALETTE["orange"],
                                  lw=1.0))
    # Moho arrow
    ax_m.annotate("Moho rises from 32 → 22 km",
                  xy=(15, 23), xytext=(-260, 50), fontsize=9.5,
                  color=PALETTE["green"], ha="left",
                  arrowprops=dict(arrowstyle="->", color=PALETTE["green"],
                                  lw=1.0))
    # LAB arrow
    ax_m.annotate("LAB shallows from 150 → 120 km\n"
                  "(asthenospheric upwelling)",
                  xy=(0, 122), xytext=(120, 180), fontsize=9.5,
                  color=PALETTE["blue"], ha="left",
                  arrowprops=dict(arrowstyle="->", color=PALETTE["blue"],
                                  lw=1.0))

    # Moho line
    ax_m.plot(x, moho, color="black", lw=1.0, alpha=0.7)
    # LAB line
    ax_m.plot(x, lab, color="black", lw=1.0, ls="--", alpha=0.6)

    # Side labels
    ax_m.text(-480, 8, "upper crust\n2.7 g/cm³", fontsize=9.5)
    ax_m.text(-480, 23, "lower crust\n2.9", fontsize=9, color="white")
    ax_m.text(-480, 90, "mantle lithosphere\n3.30 g/cm³", fontsize=9.5)
    ax_m.text(-480, 200, "asthenosphere 3.26", fontsize=9.5)

    fig.suptitle("Continental-rift gravity decomposition "
                  "(after Lowrie & Fichtner 2020, Fig. 8.42)",
                  fontsize=13, y=0.995)

    return fig


if __name__ == "__main__":
    fig = make_figure()
    out = os.path.join(os.path.dirname(__file__), "..", "figures",
                       "F9_continental_rift_gravity.png")
    save(fig, out)
    print(f"Wrote {out}")
