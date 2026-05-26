"""F9 — Continental crustal Vp profile (synthetic, gradational).

Idealised upper / middle / lower crust + Moho + mantle for a stable
continental interior, with gradient rather than sharp steps (compare
to oceanic F7). Values from Christensen & Mooney 1995 global average.

Writes assets/figures/F9_continental_vp_profile.png.
"""
from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from _style import COLORS, apply_style  # noqa: E402

apply_style()

OUT = Path(__file__).resolve().parent.parent / "figures" / "F9_continental_vp_profile.png"


def main() -> None:
    depth = np.array([0.0, 2.0, 10.0, 20.0, 30.0, 38.0, 40.0, 60.0])
    vp    = np.array([5.6, 6.1, 6.3,  6.5,  6.9,  7.1,  8.1,  8.15])

    # Densify with linear interpolation for smooth gradient look
    d_fine = np.linspace(depth.min(), depth.max(), 400)
    v_fine = np.interp(d_fine, depth, vp)

    fig, ax = plt.subplots(figsize=(5.2, 6.2))
    ax.plot(v_fine, d_fine, color=COLORS["green"], lw=2.4)
    ax.fill_betweenx(d_fine, 0, v_fine, color=COLORS["green"], alpha=0.18)

    labels = [
        (1.0,  "Upper crust\n(granitoid)"),
        (15.0, "Middle crust"),
        (28.0, "Lower crust\n(more mafic)"),
        (45.0, "Mantle (peridotite)"),
    ]
    for d, lbl in labels:
        ax.text(5.7, d, lbl, fontsize=10, va="center")

    # Moho marker
    ax.axhline(39.0, color=COLORS["vermilion"], lw=1.2, ls="--")
    ax.text(8.4, 38.6, "Moho ~40 km", color=COLORS["vermilion"], fontsize=11,
            va="bottom", ha="right")

    ax.set_xlabel(r"$V_P$ (km s$^{-1}$)")
    ax.set_ylabel("Depth (km)")
    ax.set_xlim(5.0, 8.5)
    ax.set_ylim(60, 0)
    ax.set_title("Continental crustal Vp profile (stable interior)", loc="left")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    print(f"[F9] wrote {OUT}")


if __name__ == "__main__":
    main()
