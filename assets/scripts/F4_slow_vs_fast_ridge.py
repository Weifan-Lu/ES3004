"""
F4_slow_vs_fast_ridge.py

Two-panel comparison of slow- vs. fast-spreading mid-ocean ridges:

(a) Axial magma chamber (AMC) depth as a function of spreading rate —
    a scatter-and-trend plot reproducing the qualitative content of
    Bell et al. (2022, Frontiers in Earth Science 10:970131, CC-BY 4.0,
    Figure 6) which compiled 277 seismic imaging studies. The trend:
    fast-spreading ridges (>80 mm/yr) host shallow continuous AMCs
    (~1–2 km below seafloor); slow-spreading ridges have deeper,
    discontinuous magma bodies (3–6 km, when imaged at all).

(b) Schematic Vp(z) profiles for a slow vs. fast ridge axis, showing
    the layered oceanic crustal structure and the depth of the AMC.

Reference (Tier 1 source acknowledgement — see lecture caption):
  Bell, S. W., Forsyth, D. W., Toomey, D. R. et al. (2022). Advances
  in seismic imaging of magma and crystal mush. Frontiers in Earth
  Science 10, 970131. doi:10.3389/feart.2022.970131. CC-BY 4.0.

Note: This Python figure reproduces the QUALITATIVE pattern of Bell
2022 Fig. 6 with synthetic data points. For the canonical research-grade
figure, see the open-access publication directly. The lecture markdown
cites Bell 2022 as the source of the underlying compilation.

Output: assets/figures/F4_slow_vs_fast_ridge.png
License: CC-BY 4.0 (this script)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _ess314_style import apply_style, PALETTE, save

import numpy as np
import matplotlib.pyplot as plt


def make_figure():
    apply_style()

    fig, (ax_s, ax_v) = plt.subplots(1, 2, figsize=(13, 5.5),
                                       gridspec_kw=dict(width_ratios=[1, 1],
                                                        wspace=0.30))

    # ─────────────────────────────────────────────────────────────────────
    # (a) AMC depth vs spreading rate — synthetic compilation
    # Pattern: fast ridges → shallow AMC; slow ridges → deep / no AMC
    # Logarithmic-like trend with substantial scatter
    rng = np.random.RandomState(11)

    # Slow-spreading ridges (10–40 mm/yr): deeper, sometimes no AMC detected
    n_slow = 18
    sr_slow = rng.uniform(10, 40, n_slow)
    amc_slow = 5.5 - 0.05 * sr_slow + rng.normal(0, 0.9, n_slow)
    amc_slow = np.clip(amc_slow, 2.2, 6.5)

    # Intermediate (40–80 mm/yr): mid-depth AMC, common
    n_inter = 16
    sr_inter = rng.uniform(40, 80, n_inter)
    amc_inter = 3.5 - 0.025 * sr_inter + rng.normal(0, 0.5, n_inter)
    amc_inter = np.clip(amc_inter, 1.5, 4.5)

    # Fast (80–160 mm/yr): shallow AMC, almost always continuous
    n_fast = 22
    sr_fast = rng.uniform(80, 160, n_fast)
    amc_fast = 2.5 - 0.012 * sr_fast + rng.normal(0, 0.4, n_fast)
    amc_fast = np.clip(amc_fast, 0.8, 2.6)

    # Scatter
    ax_s.scatter(sr_slow, amc_slow, s=58, c=PALETTE["blue"],
                 edgecolor="black", lw=0.7, label="Slow (MAR, SWIR)",
                 alpha=0.85, zorder=4)
    ax_s.scatter(sr_inter, amc_inter, s=58, c=PALETTE["green"], marker="s",
                 edgecolor="black", lw=0.7, label="Intermediate (JdF, GSC)",
                 alpha=0.85, zorder=4)
    ax_s.scatter(sr_fast, amc_fast, s=58, c=PALETTE["verm"], marker="^",
                 edgecolor="black", lw=0.7, label="Fast (EPR, Pacific–Antarctic)",
                 alpha=0.85, zorder=4)

    # Trend line
    sr_trend = np.linspace(10, 160, 100)
    amc_trend = 5.0 * np.exp(-sr_trend / 60.0) + 1.0
    ax_s.plot(sr_trend, amc_trend, ls="--", color=PALETTE["black"],
              lw=1.5, alpha=0.6, label="Trend")

    # Highlight Juan de Fuca Ridge (intermediate-spreading, with Axial)
    ax_s.scatter([57], [2.3], s=200, c="none", edgecolor=PALETTE["pink"],
                 lw=2.5, zorder=5)
    ax_s.annotate("Juan de Fuca\nRidge", xy=(57, 2.3), xytext=(78, 0.7),
                  fontsize=10, color=PALETTE["pink"], ha="left",
                  arrowprops=dict(arrowstyle="->", color=PALETTE["pink"],
                                  lw=1.2))

    ax_s.set_xlabel("Full spreading rate (mm/yr)")
    ax_s.set_ylabel("Depth to AMC reflector (km below seafloor)")
    ax_s.set_xlim(0, 170)
    ax_s.set_ylim(7.5, 0.0)
    ax_s.set_title("(a) AMC depth vs spreading rate — "
                   "trend after Bell et al. 2022",
                   loc="left", fontsize=11)
    ax_s.legend(loc="lower left", framealpha=0.92, fontsize=9.5)
    ax_s.grid(True, alpha=0.3)

    # ─────────────────────────────────────────────────────────────────────
    # (b) Schematic Vp(z) for slow vs fast ridge axes
    # Build piecewise profiles
    z = np.linspace(0, 7.5, 100)

    # Slow ridge: thicker Layer 2A, deeper AMC, lower mean velocity at top
    vp_slow = np.where(z < 0.3, 2.5 + 2.0 * z / 0.3,                # sed/2A
              np.where(z < 1.0, 4.5 + 1.2 * (z - 0.3) / 0.7,         # 2A → 2B
              np.where(z < 2.5, 5.7 + 0.7 * (z - 1.0) / 1.5,         # 2B → 2C
              np.where(z < 6.5, 6.4 + 0.4 * (z - 2.5) / 4.0,         # gabbro
                       7.0 + 1.1 * (z - 6.5) / 1.0))))                # mantle
    # AMC for slow ridge: ~ 3 km, narrow LVZ
    vp_slow_amc = vp_slow.copy()
    in_amc = (z > 2.9) & (z < 3.4)
    vp_slow_amc[in_amc] = 4.5

    # Fast ridge: thin Layer 2A, shallow AMC, sharper Moho
    vp_fast = np.where(z < 0.2, 2.5 + 2.5 * z / 0.2,
              np.where(z < 0.7, 5.0 + 1.0 * (z - 0.2) / 0.5,
              np.where(z < 1.5, 6.0 + 0.5 * (z - 0.7) / 0.8,
              np.where(z < 6.0, 6.5 + 0.4 * (z - 1.5) / 4.5,
                       7.0 + 1.1 * (z - 6.0) / 1.5))))
    vp_fast_amc = vp_fast.copy()
    in_amc_f = (z > 1.6) & (z < 1.9)
    vp_fast_amc[in_amc_f] = 4.2

    ax_v.plot(vp_slow_amc, z, color=PALETTE["blue"], lw=2.2,
              label="Slow ridge (≈ 25 mm/yr)")
    ax_v.plot(vp_fast_amc, z, color=PALETTE["verm"], lw=2.2, ls="--",
              label="Fast ridge (≈ 110 mm/yr)")

    # Annotate AMC depths
    ax_v.annotate("AMC ~ 3 km", xy=(4.5, 3.15), xytext=(2.7, 4.0),
                  fontsize=9.5, color=PALETTE["blue"],
                  arrowprops=dict(arrowstyle="->", color=PALETTE["blue"],
                                  lw=1.0))
    ax_v.annotate("AMC ~ 1.7 km", xy=(4.2, 1.75), xytext=(2.7, 0.7),
                  fontsize=9.5, color=PALETTE["verm"],
                  arrowprops=dict(arrowstyle="->", color=PALETTE["verm"],
                                  lw=1.0))

    # Mark Moho on each
    ax_v.axhline(6.5, color=PALETTE["blue"], lw=0.5, ls=":", alpha=0.6)
    ax_v.axhline(6.0, color=PALETTE["verm"], lw=0.5, ls=":", alpha=0.6)
    ax_v.text(7.8, 6.2, "Moho", fontsize=9, style="italic")

    ax_v.set_xlabel("P-wave velocity $V_p$ (km/s)")
    ax_v.set_ylabel("Depth below seafloor (km)")
    ax_v.set_xlim(2, 8.5)
    ax_v.set_ylim(7.5, 0.0)
    ax_v.set_title("(b) Schematic axial $V_p(z)$ — slow vs. fast",
                   loc="left", fontsize=11)
    ax_v.legend(loc="lower left", framealpha=0.92, fontsize=10)
    ax_v.grid(True, alpha=0.3)

    return fig


if __name__ == "__main__":
    fig = make_figure()
    out = os.path.join(os.path.dirname(__file__), "..", "figures",
                       "F4_slow_vs_fast_ridge.png")
    save(fig, out)
    print(f"Wrote {out}")
