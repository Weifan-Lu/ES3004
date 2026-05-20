"""fig_dipole_big.py — single big-panel meridional dipole field.

Replaces the cramped 3-panel ``fig_dipole_field_geometry`` from the
prior L23 build. Shows analytical dipole streamlines around a centred
sphere, with an inset that decomposes the field at one surface point
into B_r and B_theta components.

ESS 314, Lecture 23 §2.3 (Earth Magnetism — Fundamentals).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch

from _style import COLORS, apply_style


def dipole_field(x: np.ndarray, y: np.ndarray, m_unit: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    """Analytical 2-D dipole field on a meridional plane.

    Dipole at origin, moment along +y. Returns (Bx, By) in arbitrary
    units. The dipole singularity at r=0 is masked.
    """
    r2 = x * x + y * y
    r = np.sqrt(r2)
    # Avoid division by zero at the origin.
    mask = r2 < 0.04
    r2 = np.where(mask, np.nan, r2)
    r = np.where(mask, np.nan, r)
    # m = (0, m_unit); m . r = m_unit * y
    m_dot_r = m_unit * y
    bx = 3.0 * m_dot_r * x / r ** 5
    by = (3.0 * m_dot_r * y - m_unit * r2) / r ** 5
    return bx, by


def main(out: Path) -> None:
    apply_style()

    fig, ax = plt.subplots(figsize=(8.5, 7.0))
    ax.set_aspect("equal")

    # Meshgrid in dipole-radius units (sphere radius = 1).
    extent = 3.0
    n = 600
    xg = np.linspace(-extent, extent, n)
    yg = np.linspace(-extent, extent, n)
    X, Y = np.meshgrid(xg, yg)
    # Earth's geomagnetic dipole points from geographic N (magnetic S) to
    # geographic S (magnetic N), so the moment vector m is in the -y
    # direction here.
    Bx, By = dipole_field(X, Y, m_unit=-1.0)

    # Mask the field inside the sphere so streamlines don't pass through it.
    inside = (X * X + Y * Y) < 1.0
    Bx = np.where(inside, np.nan, Bx)
    By = np.where(inside, np.nan, By)

    # Seed streamlines from a vertical fan above the north pole and below
    # the south pole — exploits dipole symmetry to fill space with smooth,
    # evenly-spaced field lines. Each line is integrated both forward and
    # backward so it loops naturally.
    seed_y_top = np.array([0.05, 0.15, 0.30, 0.50, 0.75, 1.05, 1.4, 1.8, 2.3])
    seed_x_pos = np.array([1.05, 1.15, 1.3, 1.5, 1.75, 2.05, 2.4, 2.8])
    seeds_top_pos = np.column_stack([seed_y_top, np.full_like(seed_y_top, 2.6)])
    seeds_top_neg = np.column_stack([-seed_y_top, np.full_like(seed_y_top, 2.6)])
    seeds_bot_pos = np.column_stack([seed_y_top, np.full_like(seed_y_top, -2.6)])
    seeds_bot_neg = np.column_stack([-seed_y_top, np.full_like(seed_y_top, -2.6)])
    seeds_eq_pos = np.column_stack([seed_x_pos, np.zeros_like(seed_x_pos)])
    seeds_eq_neg = np.column_stack([-seed_x_pos, np.zeros_like(seed_x_pos)])
    seeds = np.vstack([
        seeds_top_pos, seeds_top_neg,
        seeds_bot_pos, seeds_bot_neg,
        seeds_eq_pos, seeds_eq_neg,
    ])

    ax.streamplot(
        X, Y, Bx, By,
        start_points=seeds,
        density=20,
        color=COLORS["black"],
        linewidth=0.8,
        arrowsize=1.1,
        arrowstyle="-|>",
        broken_streamlines=False,
    )

    # The sphere.
    sphere = Circle((0, 0), 1.0, facecolor="white", edgecolor=COLORS["black"],
                    linewidth=1.4, zorder=10)
    ax.add_patch(sphere)
    # Equator dashed line.
    ax.plot([-1, 1], [0, 0], color=COLORS["grey"], linewidth=0.8,
            linestyle="--", zorder=11)

    # Pole labels: geographic north (top) hosts the *magnetic south* pole,
    # geographic south (bottom) hosts the *magnetic north* pole. This is
    # why the north end of a compass needle is attracted toward the
    # geographic North.
    ax.text(0, 1.25, "geographic N\n(magnetic S)", ha="center", va="bottom",
            fontsize=12, fontweight="bold", color=COLORS["black"], zorder=12)
    ax.text(0, -1.25, "geographic S\n(magnetic N)", ha="center", va="top",
            fontsize=12, fontweight="bold", color=COLORS["black"], zorder=12)

    # Dipole moment arrow inside the sphere — points from magnetic S (top)
    # to magnetic N (bottom), i.e. downward.
    ax.annotate(
        "", xy=(0, -0.7), xytext=(0, 0.7),
        arrowprops=dict(arrowstyle="-|>", color=COLORS["vermilion"],
                        lw=2.4, mutation_scale=18),
        zorder=11,
    )
    ax.text(0.15, 0.0, r"$\mathbf{m}$", fontsize=15, fontweight="bold",
            color=COLORS["vermilion"], zorder=12)

    # B_r / B_theta decomposition inset at one surface point.
    # Pick a point at colatitude theta = 45 deg measured from the magnetic
    # north pole (which is at the geographic south, i.e. -y here). The
    # point therefore sits in the lower-right quadrant; with the flipped
    # dipole, B_r points outward and B_theta points tangentially toward
    # the magnetic equator, keeping both components positive.
    theta_pt = np.radians(45.0)
    r_pt = 1.0
    px = r_pt * np.sin(theta_pt)
    py = -r_pt * np.cos(theta_pt)
    # Compute field magnitudes at that point (in dipole units).
    # B_r = (mu m / 4 pi r^3) * 2 cos theta ; B_theta = ... * sin theta.
    # In arbitrary units take the prefactor = 1.
    Br_mag = 2.0 * np.cos(theta_pt)
    Bt_mag = np.sin(theta_pt)
    arrow_scale = 0.55  # visual scale of the decomposition arrows

    # Radial unit vector at the point (pointing away from origin) and a
    # tangential unit vector pointing from the point toward the magnetic
    # equator (which is the geographic equator, y = 0).
    r_hat = np.array([np.sin(theta_pt), -np.cos(theta_pt)])
    t_hat = np.array([np.cos(theta_pt), np.sin(theta_pt)])

    # Draw decomposition.
    ax.annotate(
        "", xy=(px + Br_mag * arrow_scale * r_hat[0], py + Br_mag * arrow_scale * r_hat[1]),
        xytext=(px, py),
        arrowprops=dict(arrowstyle="-|>", color=COLORS["blue"],
                        lw=2.2, mutation_scale=14),
        zorder=14,
    )
    ax.annotate(
        "", xy=(px + Bt_mag * arrow_scale * t_hat[0], py + Bt_mag * arrow_scale * t_hat[1]),
        xytext=(px, py),
        arrowprops=dict(arrowstyle="-|>", color=COLORS["orange"],
                        lw=2.2, mutation_scale=14),
        zorder=14,
    )
    # Point marker.
    ax.plot(px, py, "o", color=COLORS["black"], markersize=5, zorder=15)

    # Labels for the two components, placed clear of the arrows.
    ax.text(
        px + Br_mag * arrow_scale * r_hat[0] + 0.15,
        py + Br_mag * arrow_scale * r_hat[1] + 0.05,
        r"$B_r$", fontsize=14, color=COLORS["blue"], fontweight="bold",
        zorder=15,
    )
    ax.text(
        px + Bt_mag * arrow_scale * t_hat[0] + 0.05,
        py + Bt_mag * arrow_scale * t_hat[1] + 0.05,
        r"$B_\theta$", fontsize=14, color=COLORS["orange"], fontweight="bold",
        zorder=15,
    )

    # Equation inset (bottom-right).
    eqn_text = (
        r"$B_r = \dfrac{\mu_0 m}{4\pi r^3}\, 2\cos\theta$"
        "\n"
        r"$B_\theta = \dfrac{\mu_0 m}{4\pi r^3}\, \sin\theta$"
    )
    ax.text(
        0.97, 0.04, eqn_text,
        transform=ax.transAxes, ha="right", va="bottom",
        fontsize=12,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                  edgecolor=COLORS["grey"], linewidth=0.8),
        zorder=20,
    )

    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title("The dipole field — meridional cross-section",
                 fontsize=15, pad=10)

    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir / "fig_dipole_big.png")
    print("wrote", out_dir / "fig_dipole_big.png")
