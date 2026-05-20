"""fig_field_potential_gravity_analogy.py — side-by-side schematic of
the gravitational and magnetic potentials in source-free regions.

Left: point mass at depth; scalar potential isolines (concentric circles);
gravity vectors pointing radially inward; the relations g = -grad Phi,
div g = -4 pi G rho, curl g = 0.

Right: point magnetic dipole at depth; scalar potential isolines (two-lobe
pattern); H field vectors curving from N to S; the relations H = -grad Psi,
div B = 0, curl H = J.

ESS 314, Lecture 23 §2.2 (Earth Magnetism — Fundamentals).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

from _style import COLORS, apply_style


def gravity_potential(X: np.ndarray, Y: np.ndarray, x0: float, y0: float) -> np.ndarray:
    """Gravitational potential of a point mass at (x0, y0) — proportional to -1/r."""
    r = np.sqrt((X - x0) ** 2 + (Y - y0) ** 2)
    r = np.where(r < 0.05, 0.05, r)
    return -1.0 / r


def dipole_potential(X: np.ndarray, Y: np.ndarray, x0: float, y0: float) -> np.ndarray:
    """Magnetic scalar potential of a dipole at (x0, y0) with moment +y.
    Psi = m_unit * (y - y0) / r^3 in 2D meridional plane (axisymmetric).
    """
    dx = X - x0
    dy = Y - y0
    r2 = dx * dx + dy * dy
    r2 = np.where(r2 < 0.0025, 0.0025, r2)
    r = np.sqrt(r2)
    return dy / r ** 3  # m_unit absorbed


def dipole_H(X: np.ndarray, Y: np.ndarray, x0: float, y0: float) -> tuple[np.ndarray, np.ndarray]:
    """2-D dipole field at every grid point — H = -grad Psi."""
    dx = X - x0
    dy = Y - y0
    r2 = dx * dx + dy * dy
    r2 = np.where(r2 < 0.05, np.nan, r2)
    r = np.sqrt(r2)
    m_dot_r = dy
    Hx = 3.0 * m_dot_r * dx / r ** 5
    Hy = (3.0 * m_dot_r * dy - r2) / r ** 5
    return Hx, Hy


def draw_ground(ax, color: str = "#C4A574") -> None:
    """Draw a thin band representing the ground surface."""
    ax.axhline(0, color=COLORS["black"], lw=1.0, zorder=2)


def draw_gravity_panel(ax) -> None:
    ax.set_title("Gravity  ($\\mathbf{g} = -\\nabla\\Phi$)",
                 fontsize=14, pad=10)
    ax.set_aspect("equal")
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 1.5)
    ax.set_xticks([])
    ax.set_yticks([])

    # Point mass at (0, -1.0) below surface.
    x0, y0 = 0.0, -1.0
    n = 250
    xg = np.linspace(-2.5, 2.5, n)
    yg = np.linspace(-2.5, 1.5, n)
    X, Y = np.meshgrid(xg, yg)
    Phi = gravity_potential(X, Y, x0, y0)

    # Equipotential contours.
    levels = sorted(-np.logspace(np.log10(0.5), np.log10(10), 8))
    ax.contour(X, Y, Phi, levels=levels,
               colors=COLORS["skyblue"], linewidths=1.0, linestyles="-",
               zorder=3)

    # Gravity vectors on a regular grid above the surface, all pointing
    # toward the buried mass.
    sample_x = np.linspace(-2.0, 2.0, 9)
    sample_y = np.array([0.3, 0.7, 1.1])
    for px in sample_x:
        for py in sample_y:
            dxv = x0 - px
            dyv = y0 - py
            mag = np.sqrt(dxv * dxv + dyv * dyv)
            scale = 0.30
            ax.annotate(
                "",
                xy=(px + scale * dxv / mag, py + scale * dyv / mag),
                xytext=(px, py),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["vermilion"],
                                lw=1.4, mutation_scale=10),
                zorder=5,
            )

    # Source marker.
    ax.plot(x0, y0, "o", color=COLORS["black"], markersize=10, zorder=6)
    ax.text(x0 + 0.15, y0 - 0.05, "point mass", fontsize=10,
            color=COLORS["black"], va="center")

    # Ground surface.
    ax.axhspan(-2.5, 0, color="#F2E6CC", alpha=0.5, zorder=1)
    draw_ground(ax)
    ax.text(2.3, 0.08, "surface", ha="right", va="bottom",
            fontsize=10, color=COLORS["grey"])

    # Equations box.
    eqn = (r"$\nabla \cdot \mathbf{g} = -4\pi G \rho$"
           "\n"
           r"$\nabla \times \mathbf{g} = 0$"
           "\n"
           r"$\nabla^2 \Phi = 0$  (outside source)")
    ax.text(0.03, 0.97, eqn,
            transform=ax.transAxes, ha="left", va="top",
            fontsize=10.5,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=COLORS["skyblue"], linewidth=0.8))

    # Legend strip.
    ax.text(0.03, 0.05,
            "isolines: $\\Phi$\nvectors: $\\mathbf{g}$ (toward mass)",
            transform=ax.transAxes, ha="left", va="bottom",
            fontsize=10, color=COLORS["grey"], style="italic")


def draw_magnetism_panel(ax) -> None:
    ax.set_title("Magnetism  ($\\mathbf{H} = -\\nabla\\Psi$, current-free)",
                 fontsize=14, pad=10)
    ax.set_aspect("equal")
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 1.5)
    ax.set_xticks([])
    ax.set_yticks([])

    # Dipole at (0, -1.0), moment +y.
    x0, y0 = 0.0, -1.0
    n = 350
    xg = np.linspace(-2.5, 2.5, n)
    yg = np.linspace(-2.5, 1.5, n)
    X, Y = np.meshgrid(xg, yg)
    Psi = dipole_potential(X, Y, x0, y0)

    # Equipotential contours of Psi — positive lobe red, negative lobe blue.
    levels_pos = np.array([0.05, 0.12, 0.25, 0.5, 1.0, 2.0])
    levels_neg = sorted(-levels_pos)
    ax.contour(X, Y, Psi, levels=levels_pos,
               colors=COLORS["vermilion"], linewidths=0.9, linestyles="-",
               zorder=3)
    ax.contour(X, Y, Psi, levels=levels_neg,
               colors=COLORS["blue"], linewidths=0.9, linestyles="--",
               zorder=3)

    # H field vectors at sample points.
    Hx, Hy = dipole_H(X, Y, x0, y0)
    skip = (slice(None, None, 35), slice(None, None, 35))
    Xs, Ys = X[skip], Y[skip]
    Hxs, Hys = Hx[skip], Hy[skip]
    # Only above surface.
    above = Ys > 0.05
    # Normalise so arrows have uniform length (direction matters, not magnitude).
    Hmag = np.sqrt(Hxs ** 2 + Hys ** 2)
    Hxn = np.where(above, Hxs / (Hmag + 1e-9), np.nan)
    Hyn = np.where(above, Hys / (Hmag + 1e-9), np.nan)
    ax.quiver(Xs, Ys, Hxn, Hyn,
              color=COLORS["green"], scale=12, width=0.005,
              pivot="middle", zorder=5)

    # Source marker — small dipole arrow.
    ax.annotate(
        "", xy=(x0, y0 + 0.18), xytext=(x0, y0 - 0.18),
        arrowprops=dict(arrowstyle="-|>", color=COLORS["black"],
                        lw=2.0, mutation_scale=12),
        zorder=6,
    )
    ax.text(x0 + 0.18, y0 - 0.05, "dipole", fontsize=10,
            color=COLORS["black"], va="center")

    # Ground surface.
    ax.axhspan(-2.5, 0, color="#F2E6CC", alpha=0.5, zorder=1)
    draw_ground(ax)
    ax.text(2.3, 0.08, "surface", ha="right", va="bottom",
            fontsize=10, color=COLORS["grey"])

    # Equations box.
    eqn = (r"$\nabla \cdot \mathbf{B} = 0$"
           "\n"
           r"$\nabla \times \mathbf{H} = \mathbf{J}$"
           "\n"
           r"$\nabla^2 \Psi = 0$  (current-free)")
    ax.text(0.03, 0.97, eqn,
            transform=ax.transAxes, ha="left", va="top",
            fontsize=10.5,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=COLORS["green"], linewidth=0.8))

    # Legend strip.
    ax.text(0.03, 0.05,
            "isolines: $\\Psi$ (red +, blue −)\nvectors: $\\mathbf{H}$",
            transform=ax.transAxes, ha="left", va="bottom",
            fontsize=10, color=COLORS["grey"], style="italic")


def main(out: Path) -> None:
    apply_style()

    fig, (ax_g, ax_m) = plt.subplots(1, 2, figsize=(13, 5.8))
    draw_gravity_panel(ax_g)
    draw_magnetism_panel(ax_m)

    fig.suptitle("Gravity and magnetism — the potential analogy",
                 fontsize=15, fontweight="bold", y=1.00)

    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir / "fig_field_potential_gravity_analogy.png")
    print("wrote", out_dir / "fig_field_potential_gravity_analogy.png")
