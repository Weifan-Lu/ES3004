"""F7 — Oceanic crustal Vp profile (synthetic textbook stepped profile).

Layer 1 (sediments), 2A/2B (extrusives/dikes), Layer 3 (gabbros), Moho,
upper mantle. Values from White, Detrick et al. compilations summarised
in Fowler 2005 §9.

Writes assets/figures/F7_oceanic_vp_profile.png.
"""
from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from _style import COLORS, apply_style  # noqa: E402

apply_style()

OUT = Path(__file__).resolve().parent.parent / "figures" / "F7_oceanic_vp_profile.png"


def main() -> None:
    # (depth_top_km, vp_km_s, label)
    layers = [
        (0.0,  1.7, "Layer 1 — sediments"),
        (0.4,  3.5, "Layer 2A — pillow basalts"),
        (1.0,  5.2, "Layer 2B — sheeted dikes"),
        (1.8,  6.8, "Layer 3 — gabbros"),
        (7.0,  8.1, "Upper mantle (peridotite)"),
        (12.0, 8.1, None),
    ]
    depths = []
    vp = []
    for i in range(len(layers) - 1):
        d0, v, _ = layers[i]
        d1, _,  _ = layers[i + 1]
        depths.extend([d0, d1])
        vp.extend([v, v])

    fig, ax = plt.subplots(figsize=(5.2, 6.2))
    ax.plot(vp, depths, color=COLORS["blue"], lw=2.4)
    ax.fill_betweenx(depths, 0, vp, color=COLORS["skyblue"], alpha=0.25)

    # Layer annotations
    for d0, v, lbl in layers[:-1]:
        if lbl:
            ax.text(v + 0.15, d0 + 0.15, lbl, fontsize=10, color=COLORS["black"], va="top")

    # Moho marker
    ax.axhline(7.0, color=COLORS["vermilion"], lw=1.2, ls="--")
    ax.text(2.0, 6.85, "Moho", color=COLORS["vermilion"], fontsize=11, va="bottom")

    ax.set_xlabel(r"$V_P$ (km s$^{-1}$)")
    ax.set_ylabel("Depth below seafloor (km)")
    ax.set_xlim(1, 9)
    ax.set_ylim(12, 0)
    ax.set_title("Oceanic crustal Vp profile (idealised)", loc="left")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    print(f"[F7] wrote {OUT}")


if __name__ == "__main__":
    main()
