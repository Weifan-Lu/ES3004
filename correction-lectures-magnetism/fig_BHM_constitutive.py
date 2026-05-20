"""fig_BHM_constitutive.py — diamagnet vs paramagnet, with the linear
constitutive relation B = mu_0 (1 + chi) H derivation.

Visual idiom is directly from Marine Denolle's handwritten lecture note
(uploaded session 4): two side-by-side rock blobs containing a grid of
small atomic dipoles, with the applied field H above each blob and the
net magnetisation M below. Diamagnet (chi < 0): dipoles align opposite
to H. Paramagnet (chi > 0): dipoles align with H.

ESS 314, Lecture 23 §2.4 (Earth Magnetism — Fundamentals).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, FancyArrowPatch

from _style import COLORS, apply_style


def draw_dipole(ax, cx: float, cy: float, direction: str, color: str,
                width: float = 0.10, height: float = 0.22) -> None:
    """Draw a small atomic dipole as a vertical rod with + and - ends."""
    if direction == "up":
        plus_y, minus_y = cy + height / 2, cy - height / 2
    elif direction == "down":
        plus_y, minus_y = cy - height / 2, cy + height / 2
    else:
        raise ValueError(direction)
    # Rod (rectangle).
    rod = plt.Rectangle((cx - width / 2, cy - height / 2), width, height,
                        facecolor="white", edgecolor=color, linewidth=1.2)
    ax.add_patch(rod)
    # + and - labels.
    ax.text(cx, plus_y + 0.04, "+", ha="center", va="center",
            fontsize=10, color=color, fontweight="bold")
    ax.text(cx, minus_y - 0.04, "-", ha="center", va="center",
            fontsize=10, color=color, fontweight="bold")


def draw_blob(ax, cx: float, cy: float, w: float = 1.5, h: float = 1.1,
              face: str = "#F5F5F0") -> None:
    """Draw an irregular rock-outline blob."""
    n = 40
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    # Irregular but smooth radius variation.
    np.random.seed(42)
    r_jitter = 1.0 + 0.06 * np.random.randn(n)
    rx = (w / 2) * r_jitter * np.cos(angles)
    ry = (h / 2) * r_jitter * np.sin(angles)
    pts = np.column_stack([cx + rx, cy + ry])
    blob = Polygon(pts, closed=True, facecolor=face,
                   edgecolor=COLORS["grey"], linewidth=1.2)
    ax.add_patch(blob)


def draw_panel(ax, kind: str) -> None:
    """Draw one (diamagnet | paramagnet) panel."""
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-2.0, 2.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    if kind == "diamagnet":
        title = "Diamagnet  ($\\chi < 0$)"
        m_color = COLORS["vermilion"]
        dipole_dir = "down"  # induced dipoles align against H
        m_dir = "down"       # net M points opposite to H
    else:
        title = "Paramagnet  ($\\chi > 0$)"
        m_color = COLORS["blue"]
        dipole_dir = "up"
        m_dir = "up"

    ax.set_title(title, fontsize=14, pad=4)

    # Applied field H — arrow above the blob, always pointing UP.
    ax.annotate(
        "", xy=(-1.15, 1.95), xytext=(-1.15, 1.05),
        arrowprops=dict(arrowstyle="-|>", color=COLORS["black"],
                        lw=2.0, mutation_scale=14),
    )
    ax.text(-1.05, 1.55, r"$\mathbf{H}$", fontsize=15, fontweight="bold",
            color=COLORS["black"], va="center")

    # The rock blob.
    draw_blob(ax, cx=0.15, cy=0.3, w=1.7, h=1.5)

    # Grid of atomic dipoles inside the blob (3 rows x 3 cols).
    grid_x = np.array([-0.45, 0.15, 0.75])
    grid_y = np.array([-0.20, 0.30, 0.80])
    for xi in grid_x:
        for yj in grid_y:
            draw_dipole(ax, xi, yj, direction=dipole_dir, color=m_color)

    # Net magnetisation M — arrow below the blob.
    if m_dir == "up":
        ax.annotate(
            "", xy=(0.15, -0.85), xytext=(0.15, -1.55),
            arrowprops=dict(arrowstyle="-|>", color=m_color,
                            lw=2.2, mutation_scale=14),
        )
    else:
        ax.annotate(
            "", xy=(0.15, -1.55), xytext=(0.15, -0.85),
            arrowprops=dict(arrowstyle="-|>", color=m_color,
                            lw=2.2, mutation_scale=14),
        )
    ax.text(0.42, -1.18, r"$\mathbf{M}$", fontsize=15, fontweight="bold",
            color=m_color, va="center")

    # Annotation: dipole alignment direction.
    align_text = ("dipoles align\nopposite to $\\mathbf{H}$"
                  if kind == "diamagnet"
                  else "dipoles align\nwith $\\mathbf{H}$")
    ax.text(0.15, -1.85, align_text, ha="center", va="top",
            fontsize=11, color=COLORS["grey"])


def main(out: Path) -> None:
    apply_style()

    fig = plt.figure(figsize=(11, 7.5))
    gs = fig.add_gridspec(2, 2, height_ratios=[3.0, 1.0],
                          hspace=0.10, wspace=0.15,
                          left=0.04, right=0.97, top=0.93, bottom=0.05)

    ax_dia = fig.add_subplot(gs[0, 0])
    ax_para = fig.add_subplot(gs[0, 1])
    ax_eqn = fig.add_subplot(gs[1, :])

    draw_panel(ax_dia, "diamagnet")
    draw_panel(ax_para, "paramagnet")

    # Derivation strip across the bottom.
    ax_eqn.set_xticks([])
    ax_eqn.set_yticks([])
    for spine in ax_eqn.spines.values():
        spine.set_visible(False)
    ax_eqn.set_xlim(0, 1)
    ax_eqn.set_ylim(0, 1)

    derivation_lines = [
        r"$\mathbf{B} \;=\; \mu_0 (\mathbf{H} + \mathbf{M})$"
        r"$\;\;=\;\; \mu_0 (\mathbf{H} + \chi\mathbf{H})$"
        r"$\;\;=\;\; \mu_0 (1 + \chi)\,\mathbf{H}$"
        r"$\;\;=\;\; \mu\,\mathbf{H}$",
    ]
    ax_eqn.text(0.5, 0.65, derivation_lines[0],
                ha="center", va="center", fontsize=16, color=COLORS["black"])

    # Two captions below the derivation: applied vs response.
    ax_eqn.text(0.16, 0.10,
                "applied\nfield",
                ha="center", va="center", fontsize=10,
                color=COLORS["black"], fontstyle="italic")
    ax_eqn.annotate("", xy=(0.32, 0.55), xytext=(0.20, 0.20),
                    arrowprops=dict(arrowstyle="-", color=COLORS["black"],
                                    lw=0.6, linestyle="--"))

    ax_eqn.text(0.42, 0.10,
                "material\nresponse",
                ha="center", va="center", fontsize=10,
                color=COLORS["black"], fontstyle="italic")
    ax_eqn.annotate("", xy=(0.42, 0.55), xytext=(0.42, 0.22),
                    arrowprops=dict(arrowstyle="-", color=COLORS["black"],
                                    lw=0.6, linestyle="--"))

    ax_eqn.text(0.93, 0.10,
                "magnetic\npermeability $\\mu \\equiv \\mu_0(1+\\chi)$",
                ha="center", va="center", fontsize=10,
                color=COLORS["black"], fontstyle="italic")

    fig.suptitle(r"Linear-media constitutive relation",
                 fontsize=15, y=0.985, fontweight="bold")

    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir / "fig_BHM_constitutive.png")
    print("wrote", out_dir / "fig_BHM_constitutive.png")
