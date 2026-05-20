"""fig_gpts.py — Geomagnetic Polarity Timescale, 0-10 Ma.

Horizontal ribbon showing alternating normal (black) and reversed (white)
polarity chrons for the past 10 million years, with the four named chrons
of the past 5 Myr (Brunhes, Matuyama, Gauss, Gilbert) labelled and the
Olduvai and Jaramillo normal subchrons within the Matuyama highlighted.

Chron boundaries follow the Geologic Time Scale 2020 (Ogg, in Gradstein
et al. 2020, Elsevier) and Cande & Kent (1995) for older intervals.

ESS 314, Lecture 24 §6 (Rock Magnetism — Geomagnetic Polarity Timescale).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

from _style import COLORS, apply_style


# Polarity chrons (start_age, end_age) in Ma; polarity in {"N", "R"}.
# Following Ogg (2020) and Cande & Kent (1995).
CHRONS = [
    # Brunhes (normal)
    (0.000, 0.773, "N", "Brunhes"),
    # Matuyama (reversed) with Jaramillo and Olduvai normal subchrons inside
    (0.773, 0.990, "R", None),
    (0.990, 1.070, "N", "Jaramillo"),  # subchron
    (1.070, 1.775, "R", None),
    (1.775, 1.934, "N", "Olduvai"),    # subchron
    (1.934, 2.595, "R", "Matuyama"),
    # Gauss (normal) with Kaena and Mammoth reversed subchrons (very short, omitted)
    (2.595, 3.596, "N", "Gauss"),
    # Gilbert (reversed)
    (3.596, 4.187, "R", None),
    (4.187, 4.300, "N", None),  # Cochiti
    (4.300, 4.493, "R", None),
    (4.493, 4.631, "N", None),  # Nunivak
    (4.631, 4.799, "R", None),
    (4.799, 4.896, "N", None),  # Sidufjall
    (4.896, 4.997, "R", None),
    (4.997, 5.235, "N", None),  # Thvera
    (5.235, 5.330, "R", "Gilbert"),
    # C3n / C3An / C3Br / C4n area — approximate from CK95
    (5.330, 6.033, "N", None),  # C3n
    (6.033, 6.252, "R", None),
    (6.252, 6.436, "N", None),
    (6.436, 6.733, "R", None),
    (6.733, 7.140, "N", None),
    (7.140, 7.212, "R", None),
    (7.212, 7.251, "N", None),
    (7.251, 7.554, "R", None),
    (7.554, 7.642, "N", None),
    (7.642, 8.072, "R", None),
    (8.072, 8.225, "N", None),  # C4n
    (8.225, 8.257, "R", None),
    (8.257, 8.605, "N", None),
    (8.605, 9.025, "R", None),
    (9.025, 9.230, "N", None),  # C4An
    (9.230, 9.308, "R", None),
    (9.308, 9.580, "N", None),
    (9.580, 9.642, "R", None),
    (9.642, 9.740, "N", None),
    (9.740, 9.880, "R", None),
    (9.880, 9.920, "N", None),
    (9.920, 10.000, "R", None),
]


def main(out: Path) -> None:
    apply_style()

    fig, ax = plt.subplots(figsize=(13, 3.0))

    bar_y = 0.0
    bar_h = 0.8

    for (start, end, pol, name) in CHRONS:
        color = COLORS["black"] if pol == "N" else "white"
        edge = COLORS["black"]
        rect = Rectangle((start, bar_y), end - start, bar_h,
                         facecolor=color, edgecolor=edge, linewidth=0.5)
        ax.add_patch(rect)
        # Add main chron name labels above.
        if name in {"Brunhes", "Matuyama", "Gauss", "Gilbert"}:
            mid = (start + end) / 2
            # Where is the mid of the *whole* named chron, not just this segment?
            # For Matuyama use composite 0.773-2.595; for Gilbert use 3.596-5.330.
            if name == "Matuyama":
                mid = (0.773 + 2.595) / 2
            elif name == "Gilbert":
                mid = (3.596 + 5.330) / 2
            ax.text(mid, bar_y + bar_h + 0.12, name,
                    ha="center", va="bottom", fontsize=12,
                    fontweight="bold", color=COLORS["black"])
        # Subchron labels below.
        if name in {"Jaramillo", "Olduvai"}:
            mid = (start + end) / 2
            ax.text(mid, bar_y - 0.10, name,
                    ha="center", va="top", fontsize=10,
                    color=COLORS["vermilion"], style="italic")
            # Small upward marker.
            ax.plot([mid, mid], [bar_y - 0.02, bar_y - 0.08],
                    color=COLORS["vermilion"], lw=0.8)

    # Axis cosmetics.
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.7, bar_h + 0.6)
    ax.set_xlabel("Age (Ma)", fontsize=12)
    ax.set_yticks([])
    # x-ticks every 1 Myr, minor every 0.5.
    ax.set_xticks(np.arange(0, 11, 1))
    ax.set_xticks(np.arange(0, 11, 0.5), minor=True)
    ax.tick_params(axis="x", which="major", length=5)
    ax.tick_params(axis="x", which="minor", length=3)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)

    # Legend (drawn manually).
    leg_x = 7.6
    leg_y = bar_y + bar_h + 0.30
    ax.add_patch(Rectangle((leg_x, leg_y), 0.25, 0.18,
                            facecolor=COLORS["black"], edgecolor=COLORS["black"]))
    ax.text(leg_x + 0.32, leg_y + 0.09, "normal polarity",
            va="center", ha="left", fontsize=10)
    ax.add_patch(Rectangle((leg_x + 1.7, leg_y), 0.25, 0.18,
                            facecolor="white", edgecolor=COLORS["black"]))
    ax.text(leg_x + 2.02, leg_y + 0.09, "reversed polarity",
            va="center", ha="left", fontsize=10)

    ax.set_title("Geomagnetic Polarity Timescale  (last 10 Ma)",
                 fontsize=14, fontweight="bold", pad=12)

    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir / "fig_gpts.png")
    print("wrote", out_dir / "fig_gpts.png")
