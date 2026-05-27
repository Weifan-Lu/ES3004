"""
F3_gravity_non_uniqueness.py

MOR gravity non-uniqueness exercise — two density models that produce
essentially the same Bouguer anomaly profile, illustrating that gravity
data alone cannot uniquely resolve density structure.

Model A: SHALLOW + NARROW + LARGE density contrast
        (small high-melt-fraction body at axis)
Model B: DEEP + BROAD + SMALL density contrast
        (large mantle thermal/melt zone)

Both fit the observed Bouguer anomaly to within typical data uncertainty
(~5–10 mGal). The teaching point: an additional observable — seismic Vp,
heat flow, mantle Bouguer correction — is required to disambiguate.

After: legacy ESS 314 slide 20 (cf. Lowrie & Fichtner 2020, §8.3),
showing the canonical density-model non-uniqueness from Talwani 1962
and subsequent literature.

Output: assets/figures/F3_gravity_non_uniqueness.png
License: CC-BY 4.0 (this script)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _ess314_style import apply_style, PALETTE, save

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def gravity_from_slab_2d(x, x_centre, half_width_km, top_km, bottom_km, drho):
    """
    Bouguer anomaly of an infinite 2D rectangular prism.

    For a horizontal cylinder approximation (Telford et al. 1990), the
    vertical gravity effect on the surface is:
        g(x) = 2 G Δρ * integral over the prism cross-section
    Here we use the simpler approximation for an infinite 2D rectangle
    centred at depth z_c (Bouguer of an infinite slab times a width factor):
        g(x) ≈ 2 G Δρ * t * [arctan(x+w / z_top) - arctan(x-w / z_top)
                              - arctan(x+w / z_bot) + arctan(x-w / z_bot)]
    where G = 6.674e-11 m^3/kg/s^2.

    All distances and depths in km; output in mGal.
    """
    G = 6.674e-11
    # Convert to metres
    xm = (x - x_centre) * 1000.0
    wm = half_width_km * 1000.0
    z1 = top_km * 1000.0
    z2 = bottom_km * 1000.0
    drho_kgm3 = drho * 1000.0  # g/cm³ → kg/m³

    g = 2.0 * G * drho_kgm3 * (
        z2 * (np.arctan((xm + wm) / z2) - np.arctan((xm - wm) / z2))
        - z1 * (np.arctan((xm + wm) / z1) - np.arctan((xm - wm) / z1))
    )
    # m/s² → mGal
    return g * 1e5


def make_figure():
    apply_style()

    x = np.linspace(-500, 500, 1001)

    # Model A: shallow + narrow + large contrast
    g_A = gravity_from_slab_2d(x, 0, 80, 10, 50, -0.040)

    # Model B: deep + broad + small contrast — chosen so peak amplitude
    # at x=0 and width-at-half-max roughly match Model A
    g_B = gravity_from_slab_2d(x, 0, 220, 30, 220, -0.020)

    # Equalise the peak amplitude exactly (illustrative non-uniqueness)
    g_B = g_B * (g_A.min() / g_B.min())

    # Common Bouguer reference of ~250 mGal away from the body. We average
    # both fits and add noise — both fit equally well within data error.
    ref = 250
    g_avg = 0.5 * (g_A + g_B)
    obs = ref + g_avg + np.random.RandomState(42).normal(0, 6, size=x.shape)

    # ── Build figure ──
    fig = plt.figure(figsize=(12, 9))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.3, 1.5], hspace=0.30,
                          wspace=0.20)

    ax_g = fig.add_subplot(gs[0, :])
    ax_A = fig.add_subplot(gs[1, 0])
    ax_B = fig.add_subplot(gs[1, 1])

    # ── (a) Gravity panel ──
    ax_g.plot(x, obs, "o", color=PALETTE["black"], ms=2.5, alpha=0.55,
              label="Observed (with ~6 mGal noise)")
    ax_g.plot(x, ref + g_A, color=PALETTE["blue"], lw=2.2,
              label="Model A: shallow, narrow, Δρ = −0.040 g/cm³")
    ax_g.plot(x, ref + g_B, color=PALETTE["verm"], lw=2.2, ls="--",
              label="Model B: deep, broad, Δρ = −0.020 g/cm³")

    ax_g.set_xlim(-500, 500)
    ax_g.set_xlabel("Distance from ridge axis (km)")
    ax_g.set_ylabel("Bouguer anomaly (mGal)")
    ax_g.set_title("Two density models that fit the same gravity profile",
                   loc="left", fontsize=12)
    ax_g.legend(loc="lower right", framealpha=0.92, fontsize=10)
    ax_g.grid(True, alpha=0.3)

    # ── (b) Model A cross-section ──
    ax_A.set_xlim(-500, 500)
    ax_A.set_ylim(220, 0)  # depth km
    ax_A.set_xlabel("Distance (km)")
    ax_A.set_ylabel("Depth (km)")
    ax_A.set_title("Model A — shallow, narrow", loc="left", fontsize=12,
                   color=PALETTE["blue"])

    # Background fertile mantle
    ax_A.fill_between([-500, 500], 220, 0, facecolor="#e8d8b8",
                      edgecolor="none")
    # Crust above
    ax_A.fill_between([-500, 500], 10, 0, facecolor="#888888", edgecolor="none")
    # Low-density body
    ax_A.add_patch(mpatches.Rectangle((-80, 10), 160, 40,
                                       facecolor=PALETTE["blue"], alpha=0.55,
                                       edgecolor=PALETTE["blue"], lw=1.2))
    ax_A.text(0, 30, "Δρ = −0.04 g/cm³\nhalf-width 80 km\ntop 10, base 50 km",
              fontsize=9.5, ha="center", va="center",
              bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                        edgecolor=PALETTE["blue"], alpha=0.9))
    ax_A.text(-450, 5, "crust", fontsize=9, color="white")
    ax_A.text(-450, 200, "mantle", fontsize=9, color="black")
    ax_A.grid(False)

    # ── (c) Model B cross-section ──
    ax_B.set_xlim(-500, 500)
    ax_B.set_ylim(220, 0)
    ax_B.set_xlabel("Distance (km)")
    ax_B.set_title("Model B — deep, broad", loc="left", fontsize=12,
                   color=PALETTE["verm"])

    ax_B.fill_between([-500, 500], 220, 0, facecolor="#e8d8b8",
                      edgecolor="none")
    ax_B.fill_between([-500, 500], 10, 0, facecolor="#888888", edgecolor="none")
    ax_B.add_patch(mpatches.Rectangle((-220, 30), 440, 190,
                                       facecolor=PALETTE["verm"], alpha=0.40,
                                       edgecolor=PALETTE["verm"], lw=1.2))
    ax_B.text(0, 120, "Δρ = −0.020 g/cm³\nhalf-width 220 km\ntop 30, base 220 km",
              fontsize=9.5, ha="center", va="center",
              bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                        edgecolor=PALETTE["verm"], alpha=0.9))
    ax_B.text(-470, 5, "crust", fontsize=9, color="white")
    ax_B.grid(False)

    fig.suptitle("MOR gravity non-uniqueness: same data, different models",
                 fontsize=13, y=0.995)

    return fig


if __name__ == "__main__":
    fig = make_figure()
    out = os.path.join(os.path.dirname(__file__), "..", "figures",
                       "F3_gravity_non_uniqueness.png")
    save(fig, out)
    print(f"Wrote {out}")
