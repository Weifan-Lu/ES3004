"""
fig_l30_group1_mars.py

Companion to fig_l30_group1_earth.py: the SAME ray physics, scaled down to Mars.
A schematic Mars model has a thick silicate mantle over a large, low-velocity
LIQUID core (radius ~1830 km, more than half the planetary radius). Snell's law
in a sphere (p = r sin i / v conserved) is integrated as the kinematic ray
system, so the geometry emerges directly:

  - Direct P (right, blue) and direct S (left, orange) leave a surface marsquake,
    curve concave toward the surface, and TURN within the mantle.
  - A steeper ray reaches the core-mantle boundary and REFLECTS as a
    core-reflected phase (PcP / ScS analog) - the arrival that sizes the core.
  - Beyond the geometric reach of the turning rays, a wedge opposite the source
    is the core shadow.

The scientific point for the Studio: NASA's InSight mission sized the Martian
liquid core to ~1830 km from a single seismic station using exactly these
travel-time and reflected-phase relations - the same method as on Earth, scaled
to one instrument.

Schematic model (original code); Martian core radius after Stahler et al. (2021),
Science 373, 443-448, and Khan et al. (2021), Science 373, 434-438.

Output: assets/figures/fig_l30_group1_mars.png
License: CC-BY 4.0 (this script)
"""
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge
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
C_P, C_S, C_REFL = COLORS[0], COLORS[1], COLORS[4]

# --- schematic Mars ---
R = 3390.0        # planetary radius (km)
R_CMB = 1830.0    # large liquid core (radius from InSight, Stahler et al. 2021)
W = 25.0          # boundary smoothing (km)


def vp(r):
    """P velocity: mantle rises with depth, drops sharply into the liquid core."""
    f = np.clip((R - r) / (R - R_CMB), 0, 1)
    vm = 7.5 + (9.2 - 7.5) * f ** 0.6     # silicate mantle
    vcore = 5.5                            # liquid Fe-S core (low velocity)
    s = 0.5 * (1 + np.tanh((r - R_CMB) / W))
    return s * vm + (1 - s) * vcore


def vs(r):
    """S velocity: mantle only (no shear waves in the liquid core)."""
    f = np.clip((R - r) / (R - R_CMB), 0, 1)
    return 4.0 + (5.0 - 4.0) * f ** 0.6


def deriv(s, Y, vfunc):
    x, y, px, py = Y
    r = np.hypot(x, y)
    vv = vfunc(r)
    dvdr = (vfunc(r + 1.0) - vfunc(r - 1.0)) / 2.0
    g = -dvdr / (vv * vv * r)
    return [vv * px, vv * py, g * x, g * y]


def _events(stop_core):
    def surf(s, Y):
        return np.hypot(Y[0], Y[1]) - R
    surf.terminal = True
    surf.direction = +1
    evs = [surf]
    if stop_core:
        def core(s, Y):
            return np.hypot(Y[0], Y[1]) - R_CMB
        core.terminal = True
        core.direction = -1
        evs.append(core)
    return evs


def trace(a_deg, vfunc, stop_core, smax=30000):
    a = np.radians(a_deg)
    u0 = 1.0 / vfunc(R)
    Y0 = [0.0, R, np.sin(a) * u0, -np.cos(a) * u0]
    sol = solve_ivp(lambda s, Y: deriv(s, Y, vfunc), [0, smax], Y0,
                    events=_events(stop_core), max_step=6, rtol=1e-9, atol=1e-7)
    return sol


def trace_reflect(a_deg, vfunc, smax=30000):
    """Down to the CMB, reflect about the radial normal, back up to the surface."""
    a = np.radians(a_deg)
    u0 = 1.0 / vfunc(R)
    Y0 = [0.0, R, np.sin(a) * u0, -np.cos(a) * u0]
    sol1 = solve_ivp(lambda s, Y: deriv(s, Y, vfunc), [0, smax], Y0,
                     events=_events(True), max_step=6, rtol=1e-9, atol=1e-7)
    if not sol1.y_events[1].size:
        return None  # never reached the core
    xh, yh, pxh, pyh = sol1.y_events[1][0]
    r = np.hypot(xh, yh)
    nx, ny = xh / r, yh / r                       # outward radial unit vector
    dot = pxh * nx + pyh * ny
    pxr, pyr = pxh - 2 * dot * nx, pyh - 2 * dot * ny   # reflect slowness
    Y1 = [xh, yh, pxr, pyr]
    sol2 = solve_ivp(lambda s, Y: deriv(s, Y, vfunc), [0, smax], Y1,
                     events=_events(False), max_step=6, rtol=1e-9, atol=1e-7)
    x = np.concatenate([sol1.y[0], sol2.y[0]])
    y = np.concatenate([sol1.y[1], sol2.y[1]])
    return x, y


def main():
    fig, ax = plt.subplots(figsize=(8.2, 8.8))

    # ---- Mars layers ----
    ax.add_patch(Circle((0, 0), R, facecolor="#F2E2D2", edgecolor=COLORS[6],
                        lw=1.6, zorder=1))
    ax.add_patch(Circle((0, 0), R_CMB, facecolor="#E9A06A", edgecolor=COLORS[6],
                        lw=1.3, zorder=2))
    ax.text(0, -R_CMB * 0.4, "liquid core\n(~1830 km)", ha="center",
            va="center", fontsize=11)
    ax.text(0, (R + R_CMB) / 2 * 0.92, "mantle", ha="center", va="center",
            fontsize=12)

    # ---- core shadow wedge: mantle shell opposite the source ----
    ax.add_patch(Wedge((0, 0), R, 255, 285, width=R - R_CMB,
                       facecolor="#9E9E9E", edgecolor="none", alpha=0.45,
                       zorder=3))

    # ---- marsquake source ----
    ax.plot(0, R, marker="*", ms=20, color=COLORS[6], zorder=6)
    ax.annotate("marsquake", (0, R), (-1400, R + 130), fontsize=12, ha="right",
                arrowprops=dict(arrowstyle="->", color=COLORS[6]))

    # ---- RIGHT: direct P turning in the mantle ----
    for a in (62, 50, 40):
        sol = trace(a, vp, stop_core=True)
        ax.plot(sol.y[0], sol.y[1], color=C_P, lw=2.0, zorder=5)

    # ---- LEFT: direct S turning in the mantle (mirrored) ----
    for a in (60, 48, 38):
        sol = trace(a, vs, stop_core=True)
        ax.plot(-sol.y[0], sol.y[1], color=C_S, lw=2.0, ls=(0, (5, 2)), zorder=5)

    # ---- core-reflected phase (PcP / ScS analog) ----
    refl = trace_reflect(20, vp)
    if refl is not None:
        ax.plot(refl[0], refl[1], color=C_REFL, lw=2.2, zorder=5)
    refl2 = trace_reflect(12, vp)
    if refl2 is not None:
        ax.plot(refl2[0], refl2[1], color=C_REFL, lw=2.2, zorder=5)

    # ---- labels ----
    ax.text(R * 0.60, R * 0.66, "direct P", color=C_P, fontsize=12)
    ax.text(-R * 0.78, R * 0.66, "direct S", color=C_S, fontsize=12)
    ax.text(R * 0.30, -R * 0.30, "core-reflected\n(PcP / ScS)", color=C_REFL,
            fontsize=11, ha="left")
    ax.annotate("core shadow", (0, -R * 0.96), (0, -R - 850), fontsize=11,
                ha="center", color="#555555",
                arrowprops=dict(arrowstyle="->", color="#555555"))

    handles = [
        Line2D([0], [0], color=C_P, lw=2.4, label="P (turns in mantle)"),
        Line2D([0], [0], color=C_S, lw=2.4, ls=(0, (5, 2)),
               label="S (turns in mantle; none in core)"),
        Line2D([0], [0], color=C_REFL, lw=2.4,
               label="core-reflected phase (sizes the core)"),
    ]
    ax.legend(handles=handles, loc="lower center", ncol=1,
              bbox_to_anchor=(0.5, -0.20), frameon=True, fontsize=11)

    ax.text(0, -R - 1700,
            "The same ray physics, scaled to Mars: a single station (NASA InSight) sized the\n"
            "liquid core to ~1830 km from turning P/S and core-reflected travel times.",
            ha="center", va="top", fontsize=11)

    ax.set_title("Group 1 companion - the same method on Mars:\n"
                 "sizing a liquid core with one seismometer", fontsize=15, pad=12)
    lim = R + 400
    ax.set_xlim(-lim - 500, lim + 500)
    ax.set_ylim(-lim - 2200, lim + 500)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.tight_layout()
    figdir = os.path.join(os.path.dirname(__file__), "..", "figures")
    out = os.path.join(figdir, "fig_l30_group1_mars.png")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    print("wrote", out)


if __name__ == "__main__":
    main()
