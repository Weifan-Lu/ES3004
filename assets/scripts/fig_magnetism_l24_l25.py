"""Generate all missing figures for Lectures 24 (rock magnetism) and 25 (anomalies).

Author: ESS 314 build pipeline.  All figures are synthetic / schematic and
serve as the open-source replacements for proprietary textbook images.
Run from repo root or from this directory; figures land in
``assets/figures/``.  Photographs are rendered as placeholder panels that
flag the need to swap in a CC-licensed image.
"""
from __future__ import annotations

import os
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrow, FancyBboxPatch, Polygon, Rectangle

# ---------------------------------------------------------------------------
# Global style
# ---------------------------------------------------------------------------
COLORS = [
    "#0072B2",  # blue
    "#E69F00",  # orange
    "#56B4E9",  # sky
    "#009E73",  # green
    "#D55E00",  # vermilion
    "#CC79A7",  # pink
    "#000000",  # black
]

mpl.rcParams.update(
    {
        "font.size": 13,
        "axes.titlesize": 15,
        "axes.labelsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 12,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)

HERE = Path(__file__).resolve().parent
OUT = (HERE.parent / "figures").resolve()
OUT.mkdir(parents=True, exist_ok=True)


def save(fig: plt.Figure, name: str) -> None:
    path = OUT / name
    fig.savefig(path)
    plt.close(fig)
    print(f"  wrote {path.relative_to(HERE.parent.parent)}")


# ---------------------------------------------------------------------------
# 1. fig_gpts: 0-10 Ma geomagnetic polarity timescale ribbon
# ---------------------------------------------------------------------------
def fig_gpts() -> None:
    # Chron boundaries (Ma), from Cande & Kent 1995 (rounded for teaching).
    # Pairs of (start, end, polarity) where polarity = 1 (normal) or 0 (reversed)
    chrons = [
        (0.000, 0.781, 1, "Brunhes"),
        (0.781, 0.988, 0, ""),
        (0.988, 1.072, 1, "Jaramillo"),
        (1.072, 1.778, 0, "Matuyama"),
        (1.778, 1.945, 1, "Olduvai"),
        (1.945, 2.581, 0, ""),
        (2.581, 3.032, 1, "Gauss"),
        (3.032, 3.116, 0, ""),
        (3.116, 3.207, 1, ""),
        (3.207, 3.330, 0, ""),
        (3.330, 3.596, 1, ""),
        (3.596, 4.187, 0, "Gilbert"),
        (4.187, 4.300, 1, ""),
        (4.300, 4.493, 0, ""),
        (4.493, 4.631, 1, ""),
        (4.631, 4.799, 0, ""),
        (4.799, 5.000, 1, ""),
        (5.000, 5.235, 0, ""),
        (5.235, 6.033, 1, "C3n"),
        (6.033, 6.252, 0, ""),
        (6.252, 6.436, 1, ""),
        (6.436, 6.733, 0, ""),
        (6.733, 7.140, 1, ""),
        (7.140, 7.212, 0, ""),
        (7.212, 7.251, 1, ""),
        (7.251, 7.554, 0, ""),
        (7.554, 7.642, 1, ""),
        (7.642, 8.072, 0, ""),
        (8.072, 8.225, 1, ""),
        (8.225, 8.257, 0, ""),
        (8.257, 8.699, 1, "C4n"),
        (8.699, 9.025, 0, ""),
        (9.025, 9.230, 1, ""),
        (9.230, 9.308, 0, ""),
        (9.308, 9.580, 1, ""),
        (9.580, 9.642, 0, ""),
        (9.642, 9.740, 1, ""),
        (9.740, 9.880, 0, ""),
        (9.880, 10.000, 1, ""),
    ]
    fig, ax = plt.subplots(figsize=(12, 3.2))
    for start, end, pol, label in chrons:
        color = "black" if pol == 1 else "white"
        ax.add_patch(
            Rectangle((start, 0), end - start, 1, facecolor=color, edgecolor="black", linewidth=0.5)
        )
        if label:
            ax.annotate(
                label,
                xy=(0.5 * (start + end), 1.05),
                xytext=(0.5 * (start + end), 1.6),
                ha="center",
                va="bottom",
                fontsize=11,
                arrowprops=dict(arrowstyle="-", lw=0.7, color="gray"),
            )
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.2, 2.2)
    ax.set_yticks([])
    ax.set_xlabel("Age (Ma)")
    ax.set_title("Geomagnetic polarity timescale (0–10 Ma) — black = normal, white = reversed",
                 pad=18)
    ax.set_xticks(np.arange(0, 11, 1))
    ax.spines["left"].set_visible(False)
    save(fig, "fig_gpts.png")


# ---------------------------------------------------------------------------
# 2. fig_jdf_real_profile: 3-panel JdF magnetic profile
# ---------------------------------------------------------------------------
def fig_jdf_real_profile() -> None:
    half_rate_km_per_myr = 30.0  # ~30 mm/yr each side of axis
    # Polarity intervals (Ma): Brunhes 0-0.781N, then Matuyama mixed, etc.
    chrons = [
        (0.000, 0.781, 1),
        (0.781, 0.988, 0),
        (0.988, 1.072, 1),
        (1.072, 1.778, 0),
        (1.778, 1.945, 1),
        (1.945, 2.581, 0),
        (2.581, 3.032, 1),
        (3.032, 3.330, 0),
        (3.330, 3.596, 1),
        (3.596, 4.187, 0),
        (4.187, 4.300, 1),
        (4.300, 4.493, 0),
        (4.493, 4.631, 1),
        (4.631, 4.799, 0),
        (4.799, 5.000, 1),
    ]
    max_age = 5.0
    max_dist = max_age * half_rate_km_per_myr  # 150 km
    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True,
                             gridspec_kw=dict(height_ratios=[0.6, 1.6, 1.4]))

    # ---- Panel (a): polarity bar mirrored about ridge axis ----
    ax = axes[0]
    for start, end, pol in chrons:
        x0 = start * half_rate_km_per_myr
        x1 = end * half_rate_km_per_myr
        color = "black" if pol == 1 else "white"
        ax.add_patch(Rectangle((x0, 0), x1 - x0, 1, facecolor=color,
                               edgecolor="black", linewidth=0.4))
        ax.add_patch(Rectangle((-x1, 0), x1 - x0, 1, facecolor=color,
                               edgecolor="black", linewidth=0.4))
    ax.set_xlim(-max_dist, max_dist)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_title("(a) Polarity timescale projected to distance (half-rate 30 mm/yr)")
    ax.axvline(0, color=COLORS[1], lw=2)

    # ---- Panel (b): synthetic anomaly profile ----
    ax = axes[1]
    x = np.linspace(-max_dist, max_dist, 4001)
    # Map x to age, sign of magnetisation from chrons.
    def polarity_at(d):
        age = abs(d) / half_rate_km_per_myr
        for s, e, p in chrons:
            if s <= age < e:
                return 1.0 if p == 1 else -1.0
        return 0.0

    m = np.array([polarity_at(xi) for xi in x])
    # Convert to anomaly via 1-D convolution that smears by ~6 km (FWHM).
    sigma_km = 3.0
    dx = x[1] - x[0]
    ker_x = np.arange(-30, 30 + dx, dx)
    kernel = np.exp(-0.5 * (ker_x / sigma_km) ** 2)
    kernel /= kernel.sum()
    delta_F = np.convolve(m, kernel, mode="same") * 350.0  # peak ~350 nT
    rng = np.random.default_rng(20240601)
    delta_F += rng.normal(0, 12.0, size=delta_F.shape)
    ax.fill_between(x, 0, delta_F, where=delta_F > 0, color=COLORS[0], alpha=0.85)
    ax.fill_between(x, 0, delta_F, where=delta_F < 0, color=COLORS[4], alpha=0.85)
    ax.plot(x, delta_F, color="black", lw=0.6)
    ax.axhline(0, color="gray", lw=0.5)
    ax.axvline(0, color=COLORS[1], lw=2, label="Ridge axis")
    ax.set_ylabel(r"$\Delta F$ (nT)")
    ax.set_title("(b) Sea-surface magnetic anomaly profile (synthetic, smoothed)")
    ax.set_ylim(-450, 450)
    ax.legend(loc="upper right")

    # ---- Panel (c): cross-section of magnetised crust ----
    ax = axes[2]
    # Seafloor at z=0, crust 2 km thick.
    for start, end, pol in chrons:
        x0 = start * half_rate_km_per_myr
        x1 = end * half_rate_km_per_myr
        color = COLORS[0] if pol == 1 else COLORS[4]
        ax.add_patch(Rectangle((x0, -2), x1 - x0, 2, facecolor=color, alpha=0.85,
                               edgecolor="white", linewidth=0.3))
        ax.add_patch(Rectangle((-x1, -2), x1 - x0, 2, facecolor=color, alpha=0.85,
                               edgecolor="white", linewidth=0.3))
    # Water column
    ax.add_patch(Rectangle((-max_dist, 0), 2 * max_dist, 2.5,
                           facecolor="#cfe4f3", alpha=0.6, edgecolor="none"))
    ax.axvline(0, color=COLORS[1], lw=2)
    ax.text(0, 2.7, "Spreading ridge", ha="center", color=COLORS[1], fontsize=12)
    ax.text(-max_dist + 5, -1, "Magnetised oceanic crust\n(2 km thick)",
            color="white", fontsize=11, va="center")
    ax.set_xlim(-max_dist, max_dist)
    ax.set_ylim(-3.5, 3.5)
    ax.set_ylabel("Depth (km)")
    ax.set_xlabel("Distance from ridge axis (km)")
    ax.set_title("(c) Cross-section: blue = normal polarity block, red = reversed")
    ax.invert_yaxis()
    fig.suptitle("Juan de Fuca Ridge magnetic stripes — synthetic forward model",
                 y=1.02, fontsize=15)
    save(fig, "fig_jdf_real_profile.png")


# ---------------------------------------------------------------------------
# 3. fig_drm_acquisition: depositional remanent magnetisation schematic
# ---------------------------------------------------------------------------
def fig_drm_acquisition() -> None:
    fig, ax = plt.subplots(figsize=(10, 7))
    # Water column
    ax.add_patch(Rectangle((0, 0), 10, 7, facecolor="#cfe4f3", alpha=0.5))
    # Sediment bed
    ax.add_patch(Rectangle((0, 0), 10, 1.2, facecolor="#a37c52"))
    ax.text(5, 0.6, "Compacted sediment (locked-in magnetisation)",
            ha="center", color="white", fontsize=12)
    # Ambient field direction (inclined down-right)
    field_dx, field_dy = 0.6, -0.45
    for x0, y0 in [(0.5, 6.5), (9.5, 6.5)]:
        ax.add_patch(FancyArrow(x0, y0, field_dx, field_dy, width=0.05,
                                head_width=0.25, color=COLORS[6]))
    ax.text(0.55, 6.85, r"Ambient field $\mathbf{B}$ (inclination $\sim 60^\circ$)",
            color=COLORS[6], fontsize=12)

    # Settling grains, increasingly aligned as they near the bed.
    rng = np.random.default_rng(42)
    for _ in range(40):
        x = rng.uniform(0.5, 9.5)
        y = rng.uniform(1.4, 6.0)
        # Bias the grain dipole angle toward field direction as y decreases
        theta_field = np.arctan2(field_dy, field_dx)
        spread = 0.9 * (y - 1.2) / 4.8  # rad, narrows as y -> 1.2
        theta = rng.normal(theta_field, spread)
        L = 0.35
        ax.plot(
            [x - 0.5 * L * np.cos(theta), x + 0.5 * L * np.cos(theta)],
            [y - 0.5 * L * np.sin(theta), y + 0.5 * L * np.sin(theta)],
            color=COLORS[0], lw=1.6, solid_capstyle="round",
        )
        ax.plot(x + 0.5 * L * np.cos(theta), y + 0.5 * L * np.sin(theta),
                marker="o", color=COLORS[4], markersize=4)

    # Labels
    ax.annotate("Suspended grains rotate freely",
                xy=(5, 5.5), xytext=(5, 6.5), ha="center",
                color="black", fontsize=12,
                arrowprops=dict(arrowstyle="->", color="gray"))
    ax.annotate("Near the bed, hydrodynamic torque\naligns grains with $\\mathbf{B}$",
                xy=(5, 1.6), xytext=(5, 3.0), ha="center",
                color="black", fontsize=12,
                arrowprops=dict(arrowstyle="->", color="gray"))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Depositional remanent magnetisation (DRM)\nsettling magnetic grains align with the ambient field",
                 fontsize=14)
    save(fig, "fig_drm_acquisition.png")


# ---------------------------------------------------------------------------
# 4. fig_anomaly_decomposition: stacked traces F_obs/F_IGRF/F_lith/F_ext/dF
# ---------------------------------------------------------------------------
def fig_anomaly_decomposition() -> None:
    x = np.linspace(0, 200, 2001)  # km
    rng = np.random.default_rng(7)
    # Lithospheric anomaly = sum of dipole-like Gaussians
    def gauss(c, w, a):
        return a * np.exp(-0.5 * ((x - c) / w) ** 2)
    F_lith = (gauss(60, 8, 350) - gauss(75, 6, -220) + gauss(120, 12, -180)
              + gauss(150, 5, 240))
    # IGRF main field — broad regional trend
    F_IGRF = 53000.0 - 7.0 * x + 0.005 * (x - 100) ** 2
    # External (daily variation + storm)
    F_ext = 30 * np.sin(2 * np.pi * x / 80) + 15 * np.sin(2 * np.pi * x / 23)
    # Observed
    F_obs = F_IGRF + F_lith + F_ext + rng.normal(0, 8, size=x.shape)
    # Residual anomaly
    dF = F_obs - F_IGRF - F_ext

    fig, axes = plt.subplots(5, 1, figsize=(12, 10), sharex=True)
    series = [
        (r"$F_{\rm obs}$ — total field measured", F_obs, COLORS[6], False),
        (r"$F_{\rm IGRF}$ — main field model", F_IGRF, COLORS[0], False),
        (r"$F_{\rm ext}$ — external (ionosphere/storms)", F_ext, COLORS[3], False),
        (r"$F_{\rm lith}$ — lithospheric (true target)", F_lith, COLORS[4], False),
        (r"$\Delta F = F_{\rm obs} - F_{\rm IGRF} - F_{\rm ext}$ — residual anomaly",
         dF, COLORS[1], True),
    ]
    for ax, (lbl, y, c, fill) in zip(axes, series):
        ax.plot(x, y, color=c, lw=1.8)
        if fill:
            ax.fill_between(x, 0, y, where=y > 0, color=COLORS[0], alpha=0.5)
            ax.fill_between(x, 0, y, where=y < 0, color=COLORS[4], alpha=0.5)
            ax.axhline(0, color="gray", lw=0.5)
        ax.set_ylabel("nT")
        ax.set_title(lbl, loc="left", fontsize=13, pad=4)
    axes[-1].set_xlabel("Distance along flight line (km)")
    fig.suptitle("Decomposition of a magnetic survey signal",
                 y=1.00, fontsize=15)
    save(fig, "fig_anomaly_decomposition.png")


# ---------------------------------------------------------------------------
# 5. fig_emag2_global: synthetic global lithospheric anomaly grid
# ---------------------------------------------------------------------------
def fig_emag2_global() -> None:
    # Plain matplotlib pseudo-global map (no cartopy dependency).
    rng = np.random.default_rng(2024)
    lon = np.linspace(-180, 180, 720)
    lat = np.linspace(-85, 85, 340)
    LON, LAT = np.meshgrid(lon, lat)
    # Build correlated noise field via summed sinusoids -> mid-ocean ridge stripes
    field = np.zeros_like(LON)
    # Background spatial noise
    for k in range(40):
        kx = rng.uniform(0.02, 0.25)
        ky = rng.uniform(0.02, 0.20)
        phix = rng.uniform(0, 2 * np.pi)
        phiy = rng.uniform(0, 2 * np.pi)
        amp = rng.normal(0, 80)
        field += amp * np.sin(kx * LON + phix) * np.sin(ky * LAT + phiy)
    # Smooth via gaussian-like kernel (separable)
    from scipy.ndimage import gaussian_filter  # available with scipy
    field = gaussian_filter(field, sigma=2.0)
    # Land/ocean mask: leave as is (we are schematic)
    fig, ax = plt.subplots(figsize=(13, 6.5))
    pcm = ax.pcolormesh(LON, LAT, field, cmap="RdBu_r", vmin=-250, vmax=250,
                        shading="auto")
    ax.set_xlim(-180, 180)
    ax.set_ylim(-85, 85)
    ax.set_xlabel("Longitude (°)")
    ax.set_ylabel("Latitude (°)")
    ax.set_title("Synthetic global lithospheric magnetic anomaly field\n"
                 "(EMAG2-style schematic — true data: Meyer et al. 2017, NCEI public domain)",
                 fontsize=14)
    cb = fig.colorbar(pcm, ax=ax, shrink=0.85, pad=0.02, label="ΔF (nT)")
    cb.ax.tick_params(labelsize=11)
    save(fig, "fig_emag2_global.png")


# ---------------------------------------------------------------------------
# 6. fig_usgs_nam_anomaly: schematic North America magnetic anomaly map
# ---------------------------------------------------------------------------
def fig_usgs_nam_anomaly() -> None:
    from scipy.ndimage import gaussian_filter
    rng = np.random.default_rng(11)
    x = np.linspace(-130, -65, 520)  # lon
    y = np.linspace(25, 55, 240)     # lat
    X, Y = np.meshgrid(x, y)
    field = rng.normal(0, 60, size=X.shape)
    # Add a few major features
    def blob(cx, cy, wx, wy, a):
        return a * np.exp(-0.5 * (((X - cx) / wx) ** 2 + ((Y - cy) / wy) ** 2))
    # Mid-continent rift (Lake Superior)
    field += blob(-90, 47, 4, 1.0, 600)
    # Appalachian magnetic high
    field += blob(-78, 38, 5, 1.5, -200)
    # Rocky Mountain Front
    field += blob(-105, 42, 2.5, 4, 350)
    # Pacific NW Coast Ranges (Siletzia)
    field += blob(-123, 46, 1.5, 2, 450)
    # Basin and Range low
    field += blob(-117, 39, 4, 3, -180)
    field = gaussian_filter(field, sigma=3.0)

    fig, ax = plt.subplots(figsize=(12, 7))
    pcm = ax.pcolormesh(X, Y, field, cmap="RdBu_r", vmin=-400, vmax=400,
                        shading="auto")
    # Schematic coastline / borders (very rough)
    ax.plot([-125, -117, -114, -103, -97, -82, -67],
            [49, 33, 32, 29, 26, 25, 45], color="black", lw=1.0)
    ax.annotate("Mid-continent rift", xy=(-90, 47), xytext=(-92, 53),
                arrowprops=dict(arrowstyle="->"), fontsize=11)
    ax.annotate("Siletzia (PNW)", xy=(-123, 46), xytext=(-130, 51),
                arrowprops=dict(arrowstyle="->"), fontsize=11)
    ax.annotate("Appalachian belt", xy=(-78, 38), xytext=(-74, 32),
                arrowprops=dict(arrowstyle="->"), fontsize=11)
    ax.set_xlim(-130, -65)
    ax.set_ylim(25, 55)
    ax.set_xlabel("Longitude (°)")
    ax.set_ylabel("Latitude (°)")
    ax.set_title("Magnetic anomaly map of North America (schematic)\n"
                 "True compilation: Bankey et al. 2002 (USGS Open-File 02-414)",
                 fontsize=14)
    fig.colorbar(pcm, ax=ax, shrink=0.85, pad=0.02, label="ΔF (nT)")
    save(fig, "fig_usgs_nam_anomaly.png")


# ---------------------------------------------------------------------------
# 7. fig_seattle_fault_aeromag: schematic Seattle Fault Zone
# ---------------------------------------------------------------------------
def fig_seattle_fault_aeromag() -> None:
    from scipy.ndimage import gaussian_filter
    rng = np.random.default_rng(99)
    x = np.linspace(-122.6, -122.0, 360)
    y = np.linspace(47.45, 47.75, 220)
    X, Y = np.meshgrid(x, y)
    field = rng.normal(0, 25, size=X.shape)
    # Seattle Fault Zone runs ~E-W near 47.58 N; north block (Eocene volcanics) is high
    fault_lat = 47.58
    north_mask = Y > fault_lat
    field[north_mask] += 200.0 * np.exp(-((Y[north_mask] - fault_lat) / 0.05) ** 2)
    south_mask = ~north_mask
    field[south_mask] -= 80.0 * np.exp(-((Y[south_mask] - fault_lat) / 0.08) ** 2)
    # Local intrusive high
    field += 250 * np.exp(-(((X - (-122.30)) / 0.04) ** 2
                            + ((Y - 47.66) / 0.03) ** 2))
    field = gaussian_filter(field, sigma=2.5)

    fig, ax = plt.subplots(figsize=(11, 7))
    pcm = ax.pcolormesh(X, Y, field, cmap="RdBu_r", vmin=-200, vmax=300,
                        shading="auto")
    # Fault trace
    ax.plot([-122.55, -122.05], [fault_lat, fault_lat - 0.01],
            color="black", lw=2.5, label="Seattle Fault Zone (mapped)")
    ax.plot([-122.55, -122.05], [fault_lat, fault_lat - 0.01],
            color="black", lw=2.5, marker="^", markevery=5, ms=8)
    # City
    ax.plot(-122.33, 47.61, marker="*", color="yellow", markersize=18,
            markeredgecolor="black")
    ax.annotate("Seattle", xy=(-122.33, 47.61), xytext=(-122.45, 47.70),
                fontsize=12, fontweight="bold")
    ax.set_xlabel("Longitude (°)")
    ax.set_ylabel("Latitude (°)")
    ax.set_title("Seattle Fault Zone aeromagnetic schematic\n"
                 "(after Blakely et al. 2002 — north block: Eocene Crescent Fm. high; south: low)",
                 fontsize=13)
    ax.legend(loc="lower left")
    fig.colorbar(pcm, ax=ax, shrink=0.85, pad=0.02, label="ΔF (nT)")
    save(fig, "fig_seattle_fault_aeromag.png")


# ---------------------------------------------------------------------------
# 8-11. Photograph placeholders
# ---------------------------------------------------------------------------
def _placeholder(name: str, mineral: str, tint: str,
                 attribution: str, notes: str) -> None:
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.add_patch(Rectangle((0, 0), 1, 1, transform=ax.transAxes,
                           facecolor=tint, alpha=0.35))
    ax.text(0.5, 0.70, mineral, transform=ax.transAxes, ha="center",
            fontsize=34, fontweight="bold", color="black")
    ax.text(0.5, 0.55, "[ photograph placeholder ]", transform=ax.transAxes,
            ha="center", fontsize=18, color="#444")
    ax.text(0.5, 0.40, notes, transform=ax.transAxes, ha="center",
            fontsize=15, color="#222", wrap=True)
    ax.text(0.5, 0.18, "Replace with: " + attribution, transform=ax.transAxes,
            ha="center", fontsize=12, style="italic", color="#555")
    ax.text(0.5, 0.08, "(CC-BY or CC-BY-SA from Wikimedia Commons)",
            transform=ax.transAxes, ha="center", fontsize=11, color="#777")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    save(fig, name)


def fig_specimens() -> None:
    _placeholder(
        "fig_magnetite_specimen.png", "Magnetite (Fe$_3$O$_4$)",
        tint="#222244",
        attribution="Rob Lavinsky / iRocks.com — Wikimedia Commons",
        notes="Ferrimagnetic; Curie 580 °C; carrier of TRM in basalt",
    )
    _placeholder(
        "fig_hematite_specimen.png", "Hematite ($\\alpha$-Fe$_2$O$_3$)",
        tint="#8B2A2A",
        attribution="DanielCD — Wikimedia Commons",
        notes="Canted antiferromagnet; Curie 680 °C; CRM carrier in red beds",
    )
    _placeholder(
        "fig_pyrrhotite_specimen.png", "Pyrrhotite (Fe$_{1-x}$S)",
        tint="#6B5A3E",
        attribution="Rob Lavinsky / iRocks.com — Wikimedia Commons",
        notes="Ferrimagnetic; Curie 320 °C; common in sediments & meteorites",
    )
    _placeholder(
        "fig_pillow_basalt.png", "Pillow basalt (oceanic crust)",
        tint="#2E4A3B",
        attribution="James St. John — Wikimedia Commons (CC BY 2.0)",
        notes="Cooled below Curie at the ridge; locks in seafloor TRM",
    )


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> None:
    print(f"Output dir: {OUT}")
    fig_gpts()
    fig_jdf_real_profile()
    fig_drm_acquisition()
    fig_anomaly_decomposition()
    fig_emag2_global()
    fig_usgs_nam_anomaly()
    fig_seattle_fault_aeromag()
    fig_specimens()
    print("Done.")


if __name__ == "__main__":
    main()
