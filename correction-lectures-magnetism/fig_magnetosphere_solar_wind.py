"""fig_magnetosphere_solar_wind.py — schematic of Earth's magnetosphere.

Sun on the LEFT. Solar wind streams from left to right. Dayside magnetopause
faces LEFT (sunward, negative x); magnetotail extends to the RIGHT
(antisunward, positive x). Inside the magnetopause: Earth at centre,
compressed dayside / elongated nightside dipole field, two Van Allen belts.

ESS 314, Lecture 23 §6.1 (Earth Magnetism — Magnetosphere and Space Weather).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

from _style import COLORS, apply_style

# All distances in Earth radii (R_E).
R_E = 1.0
MAGPAUSE_SUNWARD = -10.0      # dayside stand-off (negative x = sunward = LEFT)
MAGPAUSE_NIGHT = 30.0         # antisunward tail truncation (RIGHT)
BOWSHOCK_SUNWARD = -14.0


def magnetopause_shape(theta: np.ndarray, r0: float = 10.0) -> np.ndarray:
    """Shue 1997-style magnetopause: r = r0 * (2 / (1 + cos theta))^alpha.
    theta measured from the SUNWARD direction.
    """
    alpha = 0.58
    r = r0 * (2.0 / (1.0 + np.cos(theta))) ** alpha
    return r


def bow_shock_shape(theta: np.ndarray, r0: float = 14.0) -> np.ndarray:
    alpha = 0.65
    r = r0 * (2.0 / (1.0 + np.cos(theta))) ** alpha
    return r


def main(out: Path) -> None:
    apply_style()

    fig, ax = plt.subplots(figsize=(13.5, 6.5))
    ax.set_aspect("equal")
    ax.set_xlim(-22, 35)
    ax.set_ylim(-18, 18)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_facecolor("#FAFAFA")

    # Sun on the LEFT (negative x).
    sun_x = -20
    sun = Circle((sun_x, 0), 1.6, facecolor="#FFE066", edgecolor="#E69F00",
                 lw=1.5, zorder=2)
    ax.add_patch(sun)
    ax.text(sun_x, -3.0, "Sun", ha="center", va="top", fontsize=12,
            fontweight="bold", color="#E69F00")

    # Solar wind streamlines flowing left -> right. Deflect around the magnetopause.
    n_lines = 8
    y_lines = np.linspace(-15, 15, n_lines)
    # Drop streamlines that would pass through Earth.
    y_lines = y_lines[np.abs(y_lines) > 2.0]
    for y in y_lines:
        x_full = np.linspace(sun_x + 2.0, 33, 120)
        y_full = np.empty_like(x_full)
        for i, xi in enumerate(x_full):
            # Magnetopause y at this x — use parametric form (sunward at -10).
            theta_grid = np.linspace(0.001, np.pi - 0.001, 400)
            r_grid = magnetopause_shape(theta_grid)
            # In standard convention, sunward (LEFT) corresponds to x = -r cos theta.
            xm = -r_grid * np.cos(theta_grid)
            ym = r_grid * np.sin(theta_grid)
            if xi >= xm.min() and xi <= xm.max():
                idx = np.argmin(np.abs(xm - xi))
                y_mag = ym[idx]
            else:
                y_mag = np.inf
            clearance = 1.5
            target_y = (np.sign(y) * max(abs(y), abs(y_mag) + clearance)
                        if y_mag != np.inf else y)
            # Centred bend near the magnetopause stand-off region.
            weight = np.exp(-((xi - (-5.0)) / 10.0) ** 2)
            y_full[i] = (1 - weight) * y + weight * target_y
        ax.plot(x_full, y_full, color=COLORS["vermilion"], lw=1.2,
                alpha=0.7, zorder=3)
        # Arrowhead in the middle of the line, indicating flow direction.
        mid = 80
        ax.annotate("", xy=(x_full[mid + 2], y_full[mid + 2]),
                    xytext=(x_full[mid - 2], y_full[mid - 2]),
                    arrowprops=dict(arrowstyle="-|>", color=COLORS["vermilion"],
                                    lw=0, mutation_scale=12),
                    zorder=3)

    # "solar wind" label.
    ax.annotate("", xy=(-13, 16), xytext=(-18, 16),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["vermilion"],
                                lw=2.0, mutation_scale=14))
    ax.text(-15.5, 17, "solar wind", ha="center", va="bottom",
            fontsize=11, color=COLORS["vermilion"], fontweight="bold")

    # Bow shock — full curve.
    theta_arc = np.linspace(0.001, np.pi - 0.001, 200)
    r_bs = bow_shock_shape(theta_arc)
    xbs = -r_bs * np.cos(theta_arc)   # x = -r cos theta (sunward on left)
    ybs = r_bs * np.sin(theta_arc)
    mask = xbs < MAGPAUSE_NIGHT
    ax.plot(xbs[mask], ybs[mask], color=COLORS["orange"], lw=2.0,
            linestyle="--", zorder=4)
    ax.plot(xbs[mask], -ybs[mask], color=COLORS["orange"], lw=2.0,
            linestyle="--", zorder=4)
    ax.text(BOWSHOCK_SUNWARD - 0.8, 8, "bow\nshock", color=COLORS["orange"],
            fontsize=11, fontweight="bold", ha="center", va="center", zorder=10)

    # Magnetopause.
    r_mp = magnetopause_shape(theta_arc)
    xmp = -r_mp * np.cos(theta_arc)
    ymp = r_mp * np.sin(theta_arc)
    mask_mp = xmp < MAGPAUSE_NIGHT
    ax.plot(xmp[mask_mp], ymp[mask_mp], color=COLORS["blue"], lw=2.4, zorder=5)
    ax.plot(xmp[mask_mp], -ymp[mask_mp], color=COLORS["blue"], lw=2.4, zorder=5)
    # Magnetotail truncation at +30 R_E.
    if len(ymp[mask_mp]):
        ymp_at_night = ymp[mask_mp][-1]
        ax.plot([MAGPAUSE_NIGHT, MAGPAUSE_NIGHT], [-ymp_at_night, ymp_at_night],
                color=COLORS["blue"], lw=1.0, linestyle=":", zorder=5)
    ax.text(MAGPAUSE_SUNWARD - 0.5, -1.0, "magnetopause", color=COLORS["blue"],
            fontsize=11, fontweight="bold", ha="right", va="top", zorder=10)
    ax.text(MAGPAUSE_NIGHT + 0.8, 0, "magnetotail", color=COLORS["blue"],
            fontsize=11, fontweight="bold", ha="left", va="center", zorder=10)

    # Earth at origin.
    earth = Circle((0, 0), R_E, facecolor=COLORS["skyblue"],
                   edgecolor=COLORS["black"], lw=1.0, zorder=20)
    ax.add_patch(earth)
    ax.text(-1.7, 0, "Earth", ha="right", va="center", fontsize=10,
            color=COLORS["black"], fontweight="bold", zorder=20)

    # Internal dipole field lines — schematic.
    # Closed dayside loops.
    for L_shell in [1.4, 2.2, 3.5]:
        # Parametric closed dipole field line in (x, y).
        t = np.linspace(-np.pi/2 + 0.05, np.pi/2 - 0.05, 200)
        r = L_shell * np.cos(t) ** 2
        # Compress sunward (x < 0), stretch antisunward (x > 0).
        x_line = r * np.sin(t)
        y_line = r * np.cos(t)
        # Apply mild compression on dayside.
        x_line_dayside = np.where(x_line < 0, x_line * 0.85, x_line * 1.2)
        # On the dayside (x < 0) keep loop closed. On nightside, allow opening for outer L.
        if L_shell < 3.0:
            ax.plot(x_line_dayside, y_line, color=COLORS["black"], lw=0.7,
                    zorder=15)
            ax.plot(x_line_dayside, -y_line, color=COLORS["black"], lw=0.7,
                    zorder=15)
        else:
            # Outer L-shell: nightside stretches into the tail.
            ax.plot(x_line_dayside[x_line <= 0], y_line[x_line <= 0],
                    color=COLORS["black"], lw=0.7, zorder=15)
            ax.plot(x_line_dayside[x_line <= 0], -y_line[x_line <= 0],
                    color=COLORS["black"], lw=0.7, zorder=15)

    # Nightside tail field lines — stretched, near-horizontal in the tail.
    for y_target in [3.5, 6.0, 8.0]:
        xs_tail = np.linspace(0, MAGPAUSE_NIGHT - 1, 80)
        ys_tail = y_target * (1 - np.exp(-xs_tail / 6.0))
        # Connect to Earth's poles via a curved segment.
        xs_close = np.linspace(-0.1, 0, 20)
        ys_close = 1.0 + np.linspace(0, 0, 20)
        # Plot both top and bottom branches.
        ax.plot(xs_tail, ys_tail, color=COLORS["black"], lw=0.7, zorder=15)
        ax.plot(xs_tail, -ys_tail, color=COLORS["black"], lw=0.7, zorder=15)

    # Van Allen belts.
    for L in [1.5, 4.0]:
        t = np.linspace(-np.pi/2 + 0.2, np.pi/2 - 0.2, 40)
        for offset in np.linspace(-0.18, 0.18, 5):
            rrad = L + offset
            xx = rrad * np.cos(t)
            yy = rrad * np.sin(t)
            ax.plot(xx, yy, color=COLORS["pink"], lw=1.2, alpha=0.6,
                    zorder=18)
            ax.plot(-xx, yy, color=COLORS["pink"], lw=1.2, alpha=0.6,
                    zorder=18)
    ax.text(5.8, 5.0, "Van Allen\nbelts",
            color=COLORS["pink"], fontsize=10, fontweight="bold",
            ha="left", va="bottom", zorder=20)

    # Scale bar (Earth radii).
    ax.plot([28, 30], [-15, -15], color=COLORS["black"], lw=1.5)
    ax.text(29, -15.5, "$2\\,R_E$", ha="center", va="top", fontsize=10)

    ax.set_title("Earth's magnetosphere — meridional section "
                 "(Sun on left, magnetotail on right)",
                 fontsize=14, fontweight="bold", pad=10)

    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir / "fig_magnetosphere_solar_wind.png")
    print("wrote", out_dir / "fig_magnetosphere_solar_wind.png")
