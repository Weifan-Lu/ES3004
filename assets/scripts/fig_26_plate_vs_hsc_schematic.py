"""F4 — Plate vs. half-space cooling schematic (synthetic; pedagogical).

Two-panel cartoon contrasting the two end-member thermal models for
oceanic lithosphere: a constant-thickness plate (left) versus a
half-space whose thermal boundary thickens as sqrt(t) (right). No data
fetched — this is a teaching schematic.

Writes assets/figures/F4_plate_vs_hsc_schematic.png.
"""
from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from _style import COLORS, apply_style  # noqa: E402

apply_style()

OUT = Path(__file__).resolve().parent.parent / "figures" / "F4_plate_vs_hsc_schematic.png"


def main() -> None:
    age = np.linspace(0.01, 150, 400)  # Ma
    # Plate model: constant asymptotic thickness, smooth approach
    plate_thick = 95.0 * (1 - np.exp(-age / 36.0))
    # HSC: thickness ∝ sqrt(t); use 9.4 km / sqrt(Ma) for the 1300 °C isotherm
    hsc_thick = 9.4 * np.sqrt(age)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)

    # Panel A — Plate
    ax = axes[0]
    ax.fill_between(age, 0, plate_thick, color=COLORS["skyblue"], alpha=0.45, label="cold plate")
    ax.plot(age, plate_thick, color=COLORS["blue"], lw=2.2)
    ax.axhline(95, color=COLORS["grey"], lw=1, ls="--")
    ax.text(140, 92, "asymptotic\nplate thickness", ha="right", va="bottom",
            color=COLORS["grey"], fontsize=10)
    ax.set_title("(a) Plate model — constant thickness at old age", loc="left")
    ax.set_xlabel("Seafloor age (Ma)")
    ax.set_ylabel("Depth to 1300 °C isotherm (km)")
    ax.set_ylim(140, 0)  # depth-down without invert_yaxis
    ax.set_xlim(0, 150)

    # Panel B — HSC
    ax = axes[1]
    ax.fill_between(age, 0, hsc_thick, color=COLORS["orange"], alpha=0.45, label="cold plate")
    ax.plot(age, hsc_thick, color=COLORS["vermilion"], lw=2.2)
    # Annotate sqrt(t)
    ax.text(110, 70, r"$z_T \propto \sqrt{\kappa\,t}$", color=COLORS["vermilion"],
            fontsize=14, ha="center")
    ax.set_title("(b) Half-space cooling — thickens as " r"$\sqrt{t}$", loc="left")
    ax.set_xlabel("Seafloor age (Ma)")
    ax.set_xlim(0, 150)

    for ax in axes:
        ax.grid(alpha=0.25)

    fig.suptitle("Oceanic lithosphere: two end-member thermal models",
                 y=1.02, fontsize=14)
    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    print(f"[F4] wrote {OUT}")


if __name__ == "__main__":
    main()
