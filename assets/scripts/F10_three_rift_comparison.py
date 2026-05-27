"""
F10_three_rift_comparison.py

Three-rift comparison panel — Bouguer gravity profile + density cross-section
for three rift case studies that span the continental rifting continuum:

  (a) Basin and Range Province (Cenozoic, active extensional province) —
      broad gravity low ~−100 mGal, thinned crust (~30 km), elevated
      asthenosphere
  (b) East African Rift (Kenya segment, modern active rifting) —
      broad gravity low ~−250 mGal, thinned crust beneath axis (~22 km),
      "Kenya dome" mantle low-density zone
  (c) Keweenawan Rift (Midcontinent Rift, 1.1 Ga failed rift, USA) —
      central gravity high ~+60 mGal from dense gabbroic rift fill,
      flanked by sediment-filled basins (negative anomalies)

The contrast between an active rift (EAR) and a failed/buried rift
(Keweenawan) shows that the geophysical signature evolves dramatically
once thermal subsidence ends and dense magmatic underplating dominates.

After: Lowrie & Fichtner 2020 §10 Fig. 8.43; Saltus & Thompson 1995
(B&R); Mechie et al. 1997 (EAR Kenya); Ocola & Meyer 1973 (Keweenawan).

Output: assets/figures/F10_three_rift_comparison.png
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


def panel_BR(ax_g, ax_m):
    """Basin & Range Province — N-S transect ~38°N, ~600 km wide."""
    x = np.linspace(-300, 300, 601)

    # Bouguer: broad regional low ~−100 mGal
    bg = -40 - gauss(x, 70, 0, 130) + 8 * np.cos(x / 30)
    ax_g.plot(x, bg, color=PALETTE["verm"], lw=2.0)
    ax_g.axhline(0, color="k", lw=0.5, alpha=0.5)
    ax_g.set_xlim(-300, 300)
    ax_g.set_ylim(-150, 30)
    ax_g.set_title("(a) Basin & Range Province",
                   loc="left", fontsize=11, color=PALETTE["blue"])
    ax_g.set_ylabel("Bouguer (mGal)")
    ax_g.grid(True, alpha=0.3)

    # Cross-section
    ax_m.set_xlim(-300, 300)
    ax_m.set_ylim(80, 0)
    ax_m.set_xlabel("Distance (km)")
    ax_m.set_ylabel("Depth (km)")

    moho = 32 - 4 * np.exp(-(x ** 2) / (150 ** 2)) + 0.4 * np.sin(x / 20)
    lab = 70 - 15 * np.exp(-(x ** 2) / (180 ** 2))

    # Surface: gentle uplift
    surface = -0.5 * np.exp(-(x ** 2) / (180 ** 2))
    crust_top = surface
    crust_mid = 0.5 * (crust_top + moho)

    ax_m.fill_between(x, crust_top, crust_mid,
                      facecolor="#c8a070", edgecolor="none")
    ax_m.fill_between(x, crust_mid, moho,
                      facecolor="#a07050", edgecolor="none")
    ax_m.fill_between(x, moho, lab,
                      facecolor="#e8d8b8", edgecolor="none")
    ax_m.fill_between(x, lab, 80,
                      facecolor="#f7c79a", edgecolor="none")
    # Highlight elevated asthenosphere
    ax_m.fill_between(x, lab, 80, where=(np.abs(x) < 200),
                      facecolor=PALETTE["verm"], alpha=0.18)

    ax_m.plot(x, moho, color="black", lw=1.0)
    ax_m.plot(x, lab, color="black", lw=0.8, ls="--", alpha=0.7)

    ax_m.text(-280, 14, "thinned crust\n(~28 km)", fontsize=8.5)
    ax_m.text(0, 75, "asthenospheric upwelling",
              fontsize=9, ha="center", color="white",
              bbox=dict(boxstyle="round,pad=0.15",
                        facecolor=PALETTE["verm"], edgecolor="none",
                        alpha=0.85))
    ax_m.text(-280, 30, "Moho", fontsize=8, style="italic")
    ax_m.text(-280, 68, "LAB", fontsize=8, style="italic")


def panel_EAR(ax_g, ax_m):
    """East African Rift — Kenya transect, 600 km wide."""
    x = np.linspace(-300, 300, 601)

    # Bouguer: deep regional low ~−250 mGal with small central magmatic high
    bg = -130 - gauss(x, 130, 0, 90) + gauss(x, 30, 0, 25) + 6 * np.cos(x / 35)
    ax_g.plot(x, bg, color=PALETTE["verm"], lw=2.0)
    ax_g.axhline(0, color="k", lw=0.5, alpha=0.5)
    ax_g.set_xlim(-300, 300)
    ax_g.set_ylim(-320, 0)
    ax_g.set_title("(b) East African Rift — Kenya",
                   loc="left", fontsize=11, color=PALETTE["green"])
    ax_g.grid(True, alpha=0.3)

    ax_m.set_xlim(-300, 300)
    ax_m.set_ylim(80, 0)
    ax_m.set_xlabel("Distance (km)")

    moho = 35 - 13 * np.exp(-(x ** 2) / (60 ** 2))
    lab = 60 - 25 * np.exp(-(x ** 2) / (110 ** 2))

    surface = -1.7 * np.exp(-(x ** 2) / (90 ** 2)) \
              + 1.1 * np.exp(-(x ** 2) / (25 ** 2))
    crust_top = surface
    crust_mid = 0.5 * (crust_top + moho)

    ax_m.fill_between(x, crust_top, crust_mid,
                      facecolor="#c8a070", edgecolor="none")
    ax_m.fill_between(x, crust_mid, moho,
                      facecolor="#a07050", edgecolor="none")
    ax_m.fill_between(x, moho, lab,
                      facecolor="#e8d8b8", edgecolor="none")
    ax_m.fill_between(x, lab, 80,
                      facecolor="#f7c79a", edgecolor="none")
    # Mantle dome
    ax_m.fill_between(x, lab, 80, where=(np.abs(x) < 150),
                      facecolor=PALETTE["verm"], alpha=0.25)
    # Dyke injection zone
    ax_m.add_patch(mpatches.Rectangle((-4, -1), 8, 16,
                                       facecolor="#8e3500", alpha=0.85,
                                       edgecolor="none", zorder=5))

    ax_m.plot(x, moho, color="black", lw=1.0)
    ax_m.plot(x, lab, color="black", lw=0.8, ls="--", alpha=0.7)

    ax_m.text(-280, 18, "Moho 22 → 35 km", fontsize=8.5)
    ax_m.text(0, 75, "Kenya dome",
              fontsize=9, ha="center", color="white",
              bbox=dict(boxstyle="round,pad=0.15",
                        facecolor=PALETTE["verm"], edgecolor="none",
                        alpha=0.85))
    ax_m.text(10, 8, "dyke\ninjection", fontsize=8,
              color=PALETTE["verm"])


def panel_Keweenawan(ax_g, ax_m):
    """Keweenawan / Midcontinent Rift — 1.1 Ga failed rift, 200 km wide."""
    x = np.linspace(-150, 150, 601)

    # Bouguer: central HIGH from dense gabbroic intrusion, flanking lows
    # from low-density sediment-filled basins
    bg = -10 + gauss(x, 75, 0, 18) - gauss(x, 35, -45, 25) \
              - gauss(x, 35, 45, 25)
    ax_g.plot(x, bg, color=PALETTE["verm"], lw=2.0)
    ax_g.axhline(0, color="k", lw=0.5, alpha=0.5)
    ax_g.set_xlim(-150, 150)
    ax_g.set_ylim(-80, 100)
    ax_g.set_title("(c) Keweenawan (Midcontinent) Rift, 1.1 Ga — failed",
                   loc="left", fontsize=11, color=PALETTE["pink"])
    ax_g.grid(True, alpha=0.3)

    ax_m.set_xlim(-150, 150)
    ax_m.set_ylim(40, 0)
    ax_m.set_xlabel("Distance (km)")

    # Geometry: dense gabbroic intrusion at centre, flanking sedimentary basins
    moho = np.full_like(x, 38.0)

    # Surface flat (deep burial; surface at sea level)
    crust_top = np.zeros_like(x)
    # Sedimentary basin: −2 km depth on either side
    sed_bot = 2.5 * (np.exp(-((x + 45) ** 2) / (20 ** 2))
                       + np.exp(-((x - 45) ** 2) / (20 ** 2)))
    # Upper crust
    upper_crust_bot = 18 - 5 * np.exp(-(x ** 2) / (15 ** 2))
    upper_crust_bot = np.maximum(upper_crust_bot, sed_bot + 0.5)

    # Sediments (low density)
    ax_m.fill_between(x, crust_top, sed_bot,
                      facecolor="#e6cd95", edgecolor="none")
    # Upper crust
    ax_m.fill_between(x, sed_bot, upper_crust_bot,
                      facecolor="#c8a070", edgecolor="none")
    # Gabbroic intrusion (central, dense)
    gabbro_top = sed_bot
    gabbro_bot = moho * (1 - 0.02 * np.exp(-(x ** 2) / (15 ** 2)))
    gabbro_mask = np.abs(x) < 22
    gx = x[gabbro_mask]
    gtop = gabbro_top[gabbro_mask]
    gbot = gabbro_bot[gabbro_mask]
    ax_m.fill(np.concatenate([gx, gx[::-1]]),
              np.concatenate([gtop, gbot[::-1]]),
              facecolor="#604a3a", edgecolor="none")
    # Lower crust outside gabbro
    ax_m.fill_between(x, upper_crust_bot, moho,
                      facecolor="#a07050", edgecolor="none",
                      where=(np.abs(x) > 22))
    # Mantle below
    ax_m.fill_between(x, moho, 40, facecolor="#e8d8b8", edgecolor="none")

    ax_m.plot(x, moho, color="black", lw=1.0)

    ax_m.text(-140, 14, "upper\ncrust", fontsize=8)
    ax_m.text(0, 22, "gabbroic\nintrusion\n(ρ ≈ 3.08)",
              fontsize=9, ha="center", color="white",
              bbox=dict(boxstyle="round,pad=0.15",
                        facecolor="#604a3a", edgecolor="none",
                        alpha=0.85))
    ax_m.text(-45, 1.5, "sediments", fontsize=8, ha="center",
              color="black")
    ax_m.text(45, 1.5, "sediments", fontsize=8, ha="center",
              color="black")
    ax_m.text(-140, 36, "Moho", fontsize=8, style="italic")


def make_figure():
    apply_style()

    fig = plt.figure(figsize=(15, 8.5))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 1.5], hspace=0.30,
                          wspace=0.22)

    ax_g_BR = fig.add_subplot(gs[0, 0])
    ax_m_BR = fig.add_subplot(gs[1, 0])
    ax_g_EA = fig.add_subplot(gs[0, 1])
    ax_m_EA = fig.add_subplot(gs[1, 1])
    ax_g_KE = fig.add_subplot(gs[0, 2])
    ax_m_KE = fig.add_subplot(gs[1, 2])

    panel_BR(ax_g_BR, ax_m_BR)
    panel_EAR(ax_g_EA, ax_m_EA)
    panel_Keweenawan(ax_g_KE, ax_m_KE)

    fig.suptitle("Three rifts at three stages — gravity signature evolves "
                  "from active broad low to failed central high",
                  fontsize=13, y=0.995)

    return fig


if __name__ == "__main__":
    fig = make_figure()
    out = os.path.join(os.path.dirname(__file__), "..", "figures",
                       "F10_three_rift_comparison.png")
    save(fig, out)
    print(f"Wrote {out}")
