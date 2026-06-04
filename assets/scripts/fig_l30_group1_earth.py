"""
fig_l30_group1_earth.py

Scientific content: the seismic shadow that proves Earth's outer core is liquid,
built by ray tracing (no hand shading). A PREM-like model has P velocity rising
with depth through the mantle (concave gradient) and DROPPING sharply at the
core-mantle boundary, then rising again through the outer core. Snell's law in a
sphere (p = r sin i / v conserved) is integrated as the kinematic ray system in
arc length, so the geometry emerges directly:

  - Direct P (right, blue) turns in the mantle and is observed out to ~100-103 deg.
  - Steeper rays refract through the low-velocity outer core and re-emerge as PKP
    (red) only beyond ~143 deg; the gap between is the P-wave shadow zone.
  - A ray that crosses the inner core (solid) is PKIKP.
  - S (left, orange) turns in the mantle but cannot cross the liquid outer core,
    so there is no direct S beyond ~103 deg: the S-wave shadow. That absence is
    the evidence that the outer core has no shear strength.

Reproduces the scientific content of (schematic PREM-like model, original code):
  Spherical ray theory and Earth's shadow zones after Lowrie & Fichtner (2020),
  Fundamentals of Geophysics, 3rd ed., Cambridge Univ. Press, Ch. 3; the P-wave
  shadow zone after Gutenberg (1913).

Output: assets/figures/fig_l30_group1_earth.png
License: CC-BY 4.0 (this script)
"""
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.lines import Line2D
from scipy.integrate import solve_ivp

mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 16,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]
C_P, C_S, C_PKP = COLORS[0], COLORS[1], COLORS[4]

R = 6371.0
R_CMB = 3480.0
R_ICB = 1220.0
W = 40.0

FIGDIR = os.path.join(os.path.dirname(__file__), "..", "figures")


def vp(r):
    f = np.clip((R - r) / (R - R_CMB), 0, 1)
    vm = 8.0 + (13.7 - 8.0) * f ** 0.55                       # mantle
    voc = 8.0 + (10.3 - 8.0) * ((R_CMB - r) / (R_CMB - R_ICB))  # outer core
    s_cmb = 0.5 * (1 + np.tanh((r - R_CMB) / W))
    s_icb = 0.5 * (1 + np.tanh((r - R_ICB) / W))
    return s_cmb * vm + (1 - s_cmb) * (s_icb * voc + (1 - s_icb) * 11.0)


def vs(r):
    f = np.clip((R - r) / (R - R_CMB), 0, 1)
    return 4.5 + (7.3 - 4.5) * f ** 0.55   # mantle only (no S in liquid core)


def trace(a_deg, vfunc, stop_core, smax=45000):
    def deriv(s, Y):
        x, y, px, py = Y
        r = np.hypot(x, y)
        vv = vfunc(r)
        dvdr = (vfunc(r + 1.0) - vfunc(r - 1.0)) / 2.0
        g = -dvdr / (vv * vv * r)
        return [vv * px, vv * py, g * x, g * y]
    a = np.radians(a_deg)
    u0 = 1.0 / vfunc(R)
    Y0 = [0.0, R, np.sin(a) * u0, -np.cos(a) * u0]

    def surf(s, Y):
        return np.hypot(Y[0], Y[1]) - R
    surf.terminal = True
    surf.direction = +1
    events = [surf]
    if stop_core:
        def core(s, Y):
            return np.hypot(Y[0], Y[1]) - R_CMB
        core.terminal = True
        core.direction = -1
        events.append(core)
    sol = solve_ivp(deriv, [0, smax], Y0, events=events, max_step=8,
                    rtol=1e-9, atol=1e-7)
    return sol.y[0], sol.y[1]


def rim(theta_deg):
    t = np.radians(theta_deg)
    return R * np.sin(t), R * np.cos(t)


def main():
    fig, ax = plt.subplots(figsize=(9.0, 9.4))

    # ---- Earth layers ----
    ax.add_patch(Circle((0, 0), R, facecolor="#EAF2F8", edgecolor=COLORS[6],
                         lw=1.6, zorder=0))
    ax.add_patch(Circle((0, 0), R_CMB, facecolor="#FBE3C8", edgecolor=COLORS[6],
                         lw=1.3, zorder=1))
    ax.add_patch(Circle((0, 0), R_ICB, facecolor="#F1C27A", edgecolor=COLORS[6],
                         lw=1.1, zorder=2))
    ax.text(0, 0, "inner core\n(solid)", ha="center", va="center", fontsize=10.5)
    ax.text(0, -(R_CMB + R_ICB) / 2, "outer core\n(liquid)", ha="center",
            va="center", fontsize=11)
    ax.text(2750, 3950, "mantle", ha="center", va="center", fontsize=12)

    # ---- source ----
    ax.plot(0, R, marker="*", ms=22, color=COLORS[6], zorder=6)
    ax.annotate("earthquake", (0, R), (-2300, R + 300), fontsize=12, ha="right",
                arrowprops=dict(arrowstyle="->", color=COLORS[6]))

    # ---- RIGHT: direct P (mantle) + core phases (PKP / PKIKP) ----
    for a in (52, 38, 27, 19.6):
        x, y = trace(a, vp, stop_core=False)
        ax.plot(x, y, color=C_P, lw=2.0, zorder=5)
    for a in (15, 9):
        x, y = trace(a, vp, stop_core=False)
        ax.plot(x, y, color=C_PKP, lw=2.2, zorder=5)
    x, y = trace(6, vp, stop_core=False)   # PKIKP through the inner core
    ax.plot(x, y, color=C_PKP, lw=2.2, ls=(0, (1, 1)), zorder=5)

    # ---- LEFT: direct S (mantle); mirror to x<0 ----
    for a in (50, 34, 24):
        x, y = trace(a, vs, stop_core=True)
        ax.plot(-x, y, color=C_S, lw=2.0, ls=(0, (5, 2)), zorder=5)

    # ---- shadow-zone annotation on the right rim (emergent gap) ----
    for ang in (103, 143):
        rx, ry = rim(ang)
        ax.plot([0.96 * rx, 1.04 * rx], [0.96 * ry, 1.04 * ry],
                color=COLORS[6], lw=1.4, zorder=6)
    midx, midy = rim(123)
    ax.annotate("P-wave shadow\n~103-143 deg", (midx, midy), (R + 1500, -1900),
                fontsize=11, ha="center", color=COLORS[6],
                arrowprops=dict(arrowstyle="->", color=COLORS[6]))
    ax.text(R * 0.62, R * 0.78, "direct P", color=C_P, fontsize=12)
    ax.text(R * 0.42, -R * 0.86, "PKP", color=C_PKP, fontsize=12)
    ax.text(R * 0.14, -R * 0.55, "PKIKP", color=C_PKP, fontsize=10)

    # ---- S-shadow annotation on the left ----
    ax.text(-R * 0.66, R * 0.78, "direct S", color=C_S, fontsize=12)
    ax.text(-R - 250, -R * 0.55,
            "S-wave shadow\n(beyond ~103 deg):\nno direct S, so the\nouter core is liquid",
            color=C_S, fontsize=11, ha="left", va="center")

    # ---- legend ----
    handles = [
        Line2D([0], [0], color=C_P, lw=2.4, label="P (turns in mantle)"),
        Line2D([0], [0], color=C_PKP, lw=2.4, label="PKP (through outer core)"),
        Line2D([0], [0], color=C_PKP, lw=2.4, ls=(0, (1, 1)),
               label="PKIKP (through inner core)"),
        Line2D([0], [0], color=C_S, lw=2.4, ls=(0, (5, 2)),
               label="S (cannot cross liquid core)"),
    ]
    ax.legend(handles=handles, loc="lower center", ncol=2,
              bbox_to_anchor=(0.5, -0.165), frameon=True, fontsize=11)

    ax.text(0, -R - 1500,
            "Rays bend by Snell's law (p = r sin i / v constant). The velocity drop at the\n"
            "core-mantle boundary refracts P into the core (PKP) and opens the shadow zone;\n"
            "S has no path through the liquid outer core, so it simply disappears beyond ~103 deg.",
            ha="center", va="top", fontsize=11)

    ax.set_title("Group 1 - The Whole Planet:\nthe seismic shadow that proves Earth's outer core is liquid",
                 fontsize=16, pad=14)
    lim = R + 500
    ax.set_xlim(-lim - 700, lim + 700)
    ax.set_ylim(-lim - 2200, lim + 600)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.tight_layout()
    out = os.path.join(FIGDIR, "fig_l30_group1_earth.png")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    print("wrote", out)


if __name__ == "__main__":
    main()
