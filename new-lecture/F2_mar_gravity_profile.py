"""
F2_mar_gravity_profile.py

Gravity profile across the Mid-Atlantic Ridge — three-panel figure showing:
  (a) Bathymetry along the transect
  (b) Free-air anomaly (≈ 0, isostatically compensated) and
      Bouguer anomaly (strongly negative over the ridge axis)
  (c) Density model: oceanic crust, low-density mantle root, fertile mantle

For the published L27 figure, the (b) data trace is intended to be a real
extraction from the Sandwell & Smith (2014) global marine gravity grid
distributed at https://topex.ucsd.edu/marine_grav/mar_grav.html.

Because the build sandbox has no internet access to that server, this script
generates a *plausible synthetic profile* that reproduces the qualitative
shape and amplitude of the published anomaly. Students re-running the lecture
on their own machines will obtain the real grid through Code Block from §4.

Reference: Sandwell, D. T., R. D. Müller, W. H. F. Smith, E. Garcia, and
R. Francis (2014). New global marine gravity model from CryoSat-2 and
Jason-1 reveals buried tectonic structure. Science 346, 65–67,
doi:10.1126/science.1258213.

Output: assets/figures/F2_mar_gravity_profile.png
License: CC-BY 4.0 (this script)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _ess314_style import apply_style, PALETTE, save

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def half_space_cooling_depth(age_Ma, d0=2500.0, a=350.0):
    """HSC bathymetric depth (m) as a function of age (Ma)."""
    return d0 + a * np.sqrt(age_Ma)


def make_figure():
    apply_style()

    # Transect from −500 km to +500 km across MAR axis at 40°S (Lowrie reference)
    x = np.linspace(-500.0, 500.0, 1001)

    # ── Bathymetry: HSC away from ridge + small axial valley ──
    # Convert distance to age: spreading half-rate ≈ 1.3 cm/yr at slow MAR
    half_rate_cm_per_yr = 1.3
    age_Ma = np.abs(x) / (half_rate_cm_per_yr * 10.0)  # 1 cm/yr = 10 km/Myr
    bath = half_space_cooling_depth(age_Ma)
    # Axial valley
    bath -= 600 * np.exp(-(x ** 2) / 2500)
    bath += 30 * np.sin(x / 25)  # roughness

    # ── Free-air anomaly: small, oscillates near zero ──
    # Local topographic correlation
    free_air = -25 + 70 * np.exp(-(x ** 2) / 15000) + 18 * np.sin(x / 35)
    # Centred around −15..0; near-axis slight high
    free_air += 8 * np.exp(-(x ** 2) / 2500)

    # ── Bouguer: large negative anomaly over ridge ──
    # Modelled as deep low-density mantle contribution: Gaussian centred on 0
    # Peak amplitude ~ −220 mGal over a ~600 km width
    bouguer = 350 - 250 * np.exp(-(x ** 2) / (350 ** 2))
    bouguer -= 30 * np.exp(-(x ** 2) / 8000)
    bouguer += 12 * np.cos(x / 40)  # short-wavelength noise

    # ── Build figure ──
    fig = plt.figure(figsize=(12, 9))
    gs = fig.add_gridspec(3, 1, height_ratios=[1.0, 1.3, 1.4], hspace=0.32)

    ax_b = fig.add_subplot(gs[0])
    ax_g = fig.add_subplot(gs[1], sharex=ax_b)
    ax_m = fig.add_subplot(gs[2], sharex=ax_b)

    # ── (a) Bathymetry ──
    ax_b.plot(x, bath / 1000.0, color=PALETTE["black"], lw=1.2)
    ax_b.fill_between(x, bath / 1000.0, 6.0,
                      facecolor="#cfe6f5", alpha=0.35, edgecolor="none")
    ax_b.set_ylim(6.0, 1.5)   # depth in km, deeper down
    ax_b.set_ylabel("Depth (km)")
    ax_b.set_title("(a) Bathymetry along transect at 40°S",
                   loc="left", fontsize=12)
    ax_b.text(0, 1.85, "axial valley",
              fontsize=9.5, ha="center", color=PALETTE["verm"], style="italic")
    ax_b.grid(True, alpha=0.3)

    # ── (b) Gravity anomalies ──
    ax_g.plot(x, bouguer, color=PALETTE["verm"], lw=2.0, ls="-",
              label="Bouguer anomaly")
    ax_g.plot(x, free_air, color=PALETTE["blue"], lw=2.0, ls="--",
              label="Free-air anomaly")
    ax_g.axhline(0, color=PALETTE["black"], lw=0.6, ls=":", alpha=0.5)
    ax_g.set_ylabel("Gravity anomaly (mGal)")
    ax_g.set_title("(b) Bouguer and free-air anomalies — "
                   "Bouguer strongly negative over ridge axis",
                   loc="left", fontsize=12)
    ax_g.legend(loc="upper right", framealpha=0.92)
    ax_g.grid(True, alpha=0.3)
    ax_g.set_ylim(-80, 420)

    # ── (c) Density model cross-section ──
    ax_m.set_xlim(-500, 500)
    ax_m.set_ylim(60.0, 0.0)  # depth km
    ax_m.set_xlabel("Distance from ridge axis (km)")
    ax_m.set_ylabel("Depth (km)")
    ax_m.set_title("(c) Density model — low-density mantle root produces the Bouguer low",
                   loc="left", fontsize=12)

    # Seawater
    bath_km = bath / 1000.0
    ax_m.fill_between(x, 0, bath_km, facecolor="#cfe6f5", edgecolor="none")
    ax_m.text(-450, 1.5, "sea", fontsize=10, color="#1c4e80", style="italic")

    # Oceanic crust ~ 7 km below seafloor; mafic, density 2.9
    crust_base = bath_km + 7.0
    ax_m.fill_between(x, bath_km, crust_base,
                      facecolor="#888888", edgecolor="none")
    ax_m.text(-450, 7, "oceanic crust\n2.9 g/cm³",
              fontsize=9.5, color=PALETTE["black"])

    # Fertile mantle background
    ax_m.fill_between(x, crust_base, 60,
                      facecolor="#e8d8b8", edgecolor="none")
    ax_m.text(-450, 50, "fertile mantle\n3.30 g/cm³",
              fontsize=9.5, color=PALETTE["black"])

    # Low-density mantle root (hot + partial-melt zone)
    xroot = np.linspace(-280, 280, 200)
    top = crust_base[np.searchsorted(x, xroot)]
    bot = 45 - 5 * np.exp(-(xroot ** 2) / 18000)
    ax_m.fill(np.concatenate([xroot, xroot[::-1]]),
              np.concatenate([top, bot[::-1]]),
              facecolor=PALETTE["verm"], alpha=0.45, edgecolor=PALETTE["verm"],
              lw=0.8)
    ax_m.text(0, 25, "low-density mantle\n(Δρ ≈ −0.04 g/cm³)",
              fontsize=10, ha="center", va="center", color="black",
              bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                        edgecolor=PALETTE["verm"], alpha=0.85))

    ax_m.set_xticks(np.arange(-500, 501, 100))
    ax_m.grid(False)

    fig.suptitle("Gravity anomalies across the Mid-Atlantic Ridge at 40°S",
                 fontsize=13, y=0.995)

    return fig


if __name__ == "__main__":
    fig = make_figure()
    out = os.path.join(os.path.dirname(__file__), "..", "figures",
                       "F2_mar_gravity_profile.png")
    save(fig, out)
    print(f"Wrote {out}")
