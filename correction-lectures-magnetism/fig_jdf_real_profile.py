"""fig_jdf_real_profile.py — three-panel Juan de Fuca magnetic profile.

Top:    GPTS (0-5 Ma) ribbon
Middle: Total-field anomaly Delta F along a perpendicular ship track,
        forward-modelled from the GPTS at v = 30 mm/yr half-spreading rate
Bottom: Schematic cross-section showing magnetised seafloor stripes

This script forward-models the anomaly from a simple thin-magnetised-layer
model — Marine NCEI trackline data would be used in deployment, but the
forward model gives a clean teaching figure with the same essential shape.

Polarity timescale from Ogg (2020); chron boundaries match fig_gpts.

ESS 314, Lecture 24 §1 (Rock Magnetism — Geoscientific Question).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

from _style import COLORS, apply_style


# Chron boundaries 0-5 Ma (start, end, polarity).
CHRONS = [
    (0.000, 0.773, "N"),
    (0.773, 0.990, "R"),
    (0.990, 1.070, "N"),  # Jaramillo
    (1.070, 1.775, "R"),
    (1.775, 1.934, "N"),  # Olduvai
    (1.934, 2.595, "R"),
    (2.595, 3.596, "N"),  # Gauss
    (3.596, 4.187, "R"),
    (4.187, 4.300, "N"),  # Cochiti
    (4.300, 4.493, "R"),
    (4.493, 4.631, "N"),  # Nunivak
    (4.631, 4.799, "R"),
    (4.799, 4.896, "N"),
    (4.896, 4.997, "R"),
    (4.997, 5.000, "N"),
]


def polarity_at_age(age_Ma: float) -> int:
    """Return +1 for normal, -1 for reversed at the given age."""
    age = abs(age_Ma)
    for start, end, pol in CHRONS:
        if start <= age < end:
            return 1 if pol == "N" else -1
    return 0  # outside the timescale we have


def forward_anomaly(x_km: np.ndarray, v_kmpMyr: float = 30.0,
                    layer_thickness: float = 1.0,
                    layer_top_depth: float = 3.0,
                    M0: float = 1.0,
                    inclination_deg: float = 60.0) -> np.ndarray:
    """Forward-model the total-field anomaly across the ridge axis.

    The crust is modelled as a thin (1 km) horizontal layer at depth
    z = layer_top_depth km (below the sea surface) with vertically uniform
    magnetisation that flips sign at every polarity boundary. The amplitude
    pattern at the surface is approximated as a low-pass-filtered version
    of the in-situ polarity sequence, multiplied by an amplitude factor.

    This is the standard textbook Vine-Matthews-Morley schematic; it
    captures the symmetric striped pattern and the correct half-rate scaling.
    """
    # Age at each x (Myr).
    age = np.abs(x_km) / v_kmpMyr
    # Polarity at each x (+1 normal, -1 reversed).
    pol = np.array([polarity_at_age(a) for a in age])
    # Filter the polarity sequence to mimic the smoothing produced by the
    # finite depth (z = 3 km) of the magnetised layer. Use a Gaussian whose
    # width is set by depth/spreading rate to give a realistic stripe profile.
    dx = x_km[1] - x_km[0]
    sigma_km = layer_top_depth * 0.7  # ~depth-derived smoothing
    n_window = int(6 * sigma_km / dx) | 1
    xw = np.arange(-(n_window // 2), n_window // 2 + 1) * dx
    kernel = np.exp(-0.5 * (xw / sigma_km) ** 2)
    kernel /= kernel.sum()
    # Convolution gives the smoothed surface signature.
    delta_F = np.convolve(pol.astype(float), kernel, mode="same")
    # Amplitude scaling — typical JdF anomaly amplitudes are 100s of nT.
    amp_nT = 350.0
    return delta_F * amp_nT


def main(out: Path) -> None:
    apply_style()

    fig = plt.figure(figsize=(13, 8.5))
    gs = fig.add_gridspec(3, 1, height_ratios=[0.8, 2.5, 1.7],
                          hspace=0.42, left=0.08, right=0.97,
                          top=0.95, bottom=0.07)

    ax_gpts = fig.add_subplot(gs[0])
    ax_anom = fig.add_subplot(gs[1])
    ax_xs = fig.add_subplot(gs[2])

    # ------- Top: GPTS ribbon -------
    # Plot 0-5 Ma; symmetric about the ridge axis -> plot AGE on top axis
    # mapping into distance via x = v * age.
    v_kmpMyr = 30.0
    age_max = 5.0
    ax_gpts.set_xlim(-age_max * v_kmpMyr, age_max * v_kmpMyr)
    ax_gpts.set_ylim(0, 1.0)
    ax_gpts.set_yticks([])
    bar_y, bar_h = 0.2, 0.6
    for (start, end, pol) in CHRONS:
        if end > age_max:
            end = age_max
        x_start = start * v_kmpMyr
        x_end = end * v_kmpMyr
        width = x_end - x_start
        color = COLORS["black"] if pol == "N" else "white"
        # Positive side
        ax_gpts.add_patch(Rectangle((x_start, bar_y), width, bar_h,
                                      facecolor=color, edgecolor=COLORS["black"],
                                      linewidth=0.4))
        # Negative side (mirror).
        ax_gpts.add_patch(Rectangle((-x_end, bar_y), width, bar_h,
                                      facecolor=color, edgecolor=COLORS["black"],
                                      linewidth=0.4))
    # Ridge axis line.
    ax_gpts.axvline(0, color=COLORS["orange"], lw=2.0, zorder=5)
    # Top axis labels (age in Myr).
    ax_gpts.set_title("(a)  Geomagnetic Polarity Timescale (last 5 Ma)",
                       loc="left", fontsize=12, fontweight="bold", pad=8)
    for t_ma in [0.78, 1.78, 2.58, 3.60]:
        ax_gpts.text(t_ma * v_kmpMyr, bar_y + bar_h + 0.05,
                      f"{t_ma:.2f} Ma", ha="center", va="bottom",
                      fontsize=8, color=COLORS["grey"])
    # Chron name labels.
    chron_labels = [
        ("Brunhes", 0.387 * v_kmpMyr),
        ("Matuyama", 1.685 * v_kmpMyr),
        ("Gauss", 3.10 * v_kmpMyr),
        ("Gilbert", 4.45 * v_kmpMyr),
    ]
    for name, x_pos in chron_labels:
        ax_gpts.text(x_pos, bar_y - 0.05, name, ha="center", va="top",
                      fontsize=9, color=COLORS["black"], style="italic")

    # ------- Middle: anomaly profile -------
    x_km = np.linspace(-200, 200, 4001)
    delta_F = forward_anomaly(x_km, v_kmpMyr=v_kmpMyr)
    # Add a touch of realistic noise to look like real data.
    np.random.seed(3)
    noise = 18 * np.random.randn(len(x_km))
    delta_F_noisy = delta_F + 0.5 * np.convolve(noise, np.ones(11) / 11, mode="same")

    ax_anom.plot(x_km, delta_F_noisy, color=COLORS["blue"], lw=1.2, alpha=0.55)
    ax_anom.plot(x_km, delta_F, color=COLORS["black"], lw=1.8)
    ax_anom.fill_between(x_km, 0, delta_F, where=delta_F > 0,
                          color=COLORS["blue"], alpha=0.18, interpolate=True)
    ax_anom.fill_between(x_km, 0, delta_F, where=delta_F < 0,
                          color=COLORS["vermilion"], alpha=0.18, interpolate=True)
    ax_anom.axhline(0, color=COLORS["grey"], lw=0.5)
    ax_anom.axvline(0, color=COLORS["orange"], lw=2.0)
    ax_anom.set_xlim(-200, 200)
    ax_anom.set_ylim(-500, 500)
    ax_anom.set_ylabel("$\\Delta F$  (nT)", fontsize=12)
    ax_anom.set_title("(b)  Total-field magnetic anomaly across the Juan de Fuca Ridge "
                       "(half-spreading rate 30 mm/yr)",
                       loc="left", fontsize=12, fontweight="bold", pad=6)
    ax_anom.grid(True, alpha=0.3)
    # Brunhes/Matuyama boundary annotation.
    ax_anom.annotate("B/M boundary\n(0.78 Ma)",
                      xy=(0.78 * v_kmpMyr, 250), xytext=(75, 380),
                      fontsize=9, color=COLORS["green"],
                      arrowprops=dict(arrowstyle="->", color=COLORS["green"], lw=1.0))
    ax_anom.text(0, 470, "ridge axis", ha="center", va="top",
                  color=COLORS["orange"], fontsize=10, fontweight="bold",
                  bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                            edgecolor=COLORS["orange"], lw=0.6))

    # ------- Bottom: cross-section -------
    ax_xs.set_xlim(-200, 200)
    ax_xs.set_ylim(-6, 0.5)
    ax_xs.set_xlabel("Distance from ridge axis  (km)", fontsize=12)
    ax_xs.set_ylabel("Depth\n(km b.s.l.)", fontsize=11)
    ax_xs.set_title("(c)  Schematic cross-section — magnetised seafloor "
                     "stripes (top of oceanic crust)",
                     loc="left", fontsize=12, fontweight="bold", pad=6)
    # Ocean.
    ax_xs.add_patch(Rectangle((-200, -3), 400, 3, facecolor=COLORS["skyblue"],
                                alpha=0.3, edgecolor="none"))
    ax_xs.text(-195, -0.3, "ocean", color=COLORS["blue"], fontsize=10,
                 style="italic")
    # Magnetised crust band (3-4 km b.s.l.), striped by polarity.
    for (start, end, pol) in CHRONS:
        if end > 5.0:
            continue
        x_start = start * v_kmpMyr
        x_end = end * v_kmpMyr
        width = x_end - x_start
        color = COLORS["blue"] if pol == "N" else COLORS["vermilion"]
        ax_xs.add_patch(Rectangle((x_start, -4.0), width, 1.0,
                                    facecolor=color, alpha=0.5,
                                    edgecolor=COLORS["grey"], linewidth=0.3))
        ax_xs.add_patch(Rectangle((-x_end, -4.0), width, 1.0,
                                    facecolor=color, alpha=0.5,
                                    edgecolor=COLORS["grey"], linewidth=0.3))
    # Lower lithosphere (gray).
    ax_xs.add_patch(Rectangle((-200, -6), 400, 2, facecolor="#D5D5D5",
                                edgecolor="none"))
    ax_xs.text(-195, -5.2, "lithosphere", color=COLORS["grey"], fontsize=10,
                 style="italic")

    # Ridge axis (magma injection).
    ax_xs.axvline(0, color=COLORS["orange"], lw=2.0)
    # Spreading arrows.
    ax_xs.annotate("", xy=(-150, -5.5), xytext=(-30, -5.5),
                    arrowprops=dict(arrowstyle="-|>", color=COLORS["black"],
                                    lw=1.5, mutation_scale=14))
    ax_xs.annotate("", xy=(150, -5.5), xytext=(30, -5.5),
                    arrowprops=dict(arrowstyle="-|>", color=COLORS["black"],
                                    lw=1.5, mutation_scale=14))
    ax_xs.text(-90, -5.3, "spreading", fontsize=9, color=COLORS["black"],
                 ha="center", va="bottom", style="italic")
    ax_xs.text(90, -5.3, "spreading", fontsize=9, color=COLORS["black"],
                 ha="center", va="bottom", style="italic")
    # Ridge label.
    ax_xs.text(0, 0.3, "ridge axis", ha="center", va="bottom",
                 color=COLORS["orange"], fontsize=10, fontweight="bold")
    ax_xs.invert_yaxis()
    ax_xs.grid(True, alpha=0.3)

    # Legend for polarity colours in cross-section.
    leg_x = -195
    leg_y = -4.5
    ax_xs.add_patch(Rectangle((leg_x, leg_y), 12, 0.3,
                                facecolor=COLORS["blue"], alpha=0.5))
    ax_xs.text(leg_x + 14, leg_y + 0.15, "normal", fontsize=9,
                 va="center", color=COLORS["blue"])
    ax_xs.add_patch(Rectangle((leg_x + 50, leg_y), 12, 0.3,
                                facecolor=COLORS["vermilion"], alpha=0.5))
    ax_xs.text(leg_x + 64, leg_y + 0.15, "reversed", fontsize=9,
                 va="center", color=COLORS["vermilion"])

    fig.suptitle("Juan de Fuca Ridge — magnetic stripes (forward-modelled)",
                  fontsize=14, fontweight="bold", y=0.99)
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir / "fig_jdf_real_profile.png")
    print("wrote", out_dir / "fig_jdf_real_profile.png")
