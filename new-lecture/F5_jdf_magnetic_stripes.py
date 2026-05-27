"""
F5_jdf_magnetic_stripes.py

Juan de Fuca Ridge magnetic stripes — Vine–Matthews polarity reversals
recorded in the oceanic crust.

This figure is intended to be a real extraction from the NOAA EMAG2v3
global magnetic anomaly grid (Maus 2009; NOAA NCEI; public domain).

Two execution paths are supported:

  (1) If the EMAG2 grid is reachable via the network on the user's machine,
      the script loads it directly with xarray and produces a real-data
      stripe profile.

  (2) If the grid is unreachable (sandbox / offline), the script falls back
      to a SYNTHETIC stripe sequence built from the canonical Cande & Kent
      1995 Geomagnetic Polarity Time Scale and a JdF half-spreading rate
      of 2.85 cm/yr. The synthetic version reproduces the qualitative
      pattern and the spreading-rate inversion workflow.

Reference:
  Maus, S. (2009). EMAG2: Earth Magnetic Anomaly Grid (2-arc-minute
  resolution). NOAA NCEI. doi:10.7289/V5MW2F2P. Public domain.
  Cande, S. C. and Kent, D. V. (1995). Revised calibration of the
  geomagnetic polarity timescale for the Late Cretaceous and Cenozoic.
  JGR 100(B4), 6093–6095. doi:10.1029/94JB03098.

Output: assets/figures/F5_jdf_magnetic_stripes.png
License: CC-BY 4.0 (this script)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _ess314_style import apply_style, PALETTE, save

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.signal import find_peaks


# Cande & Kent 1995 ages (Ma) for the major polarity reversals — Chrons C1n
# (Brunhes), C2n (Olduvai), C2An (Gauss), C3n, C3An, C4n, C5n (etc.)
# We use just the boundary ages of the major reversals for a 0–10 Ma window.
GPTS = {
    # name: (start_Ma, end_Ma) of NORMAL polarity epoch
    "C1n_Brunhes":   (0.000, 0.781),
    "C2n_Olduvai":   (1.778, 1.945),
    "C2An_Gauss":    (2.581, 3.596),
    "C3n_Cochiti":   (4.187, 4.300),
    "C3n_Nunivak":   (4.493, 4.631),
    "C3n_Sidufjall": (4.799, 4.896),
    "C3n_Thvera":    (4.997, 5.235),
    "C3An_1":        (6.033, 6.252),
    "C3An_2":        (6.436, 6.733),
    "C4n":           (7.140, 7.432),
    "C4n_2":         (7.562, 8.072),
    "C4An":          (8.769, 9.098),
}


def synthetic_stripe_profile(half_rate_cm_yr=2.85, x_km=None, noise_amp=18.0,
                              seed=7):
    """
    Synthesise a magnetic anomaly profile from the GPTS, given a constant
    spreading rate. Returns (x_km, anomaly_nT, true_peak_positions_km).
    """
    if x_km is None:
        x_km = np.linspace(-300, 300, 6001)

    # Convert each GPTS epoch to a spatial window on the seafloor
    # Distance (km) from ridge = age (Ma) * half-rate (cm/yr) * 10
    rate_km_per_Ma = half_rate_cm_yr * 10.0

    anomaly = np.zeros_like(x_km)

    true_peaks = []

    for name, (a1, a2) in GPTS.items():
        d1 = a1 * rate_km_per_Ma
        d2 = a2 * rate_km_per_Ma
        # Add normal-polarity stripe on both sides (symmetric about axis)
        for sign in (+1, -1):
            xa = sign * d1
            xb = sign * d2
            lo, hi = sorted([xa, xb])
            true_peaks.append(0.5 * (lo + hi))
            width = hi - lo
            # Gaussian centred on the band centre, scaled by width
            amp = 350.0 * (1.0 - np.exp(-width / 18.0))
            sigma = max(width / 2.5, 6.0)
            anomaly += amp * np.exp(-((x_km - 0.5 * (lo + hi)) ** 2)
                                      / sigma ** 2)

    # Subtract a long-wavelength regional field to centre the anomaly on 0
    anomaly -= np.mean(anomaly)

    # High-frequency oceanic noise (modest amplitude — real EMAG2 has SNR
    # adequate to recover the major chrons)
    rng = np.random.RandomState(seed)
    anomaly += rng.normal(0, noise_amp, size=x_km.shape)

    return x_km, anomaly, sorted(true_peaks)


def try_real_emag2(lat=47.0, lon_range=(-132, -126)):
    """
    Try to load EMAG2v3 from NOAA NCEI. Returns (x_km, anomaly_nT) or None.

    The canonical URL is the NetCDF distribution at NCEI. This requires
    network access to www.ngdc.noaa.gov.
    """
    try:
        import xarray as xr
        # NetCDF distribution path (subject to NCEI URL stability)
        url = ("https://www.ngdc.noaa.gov/geomag/EMAG2/"
               "EMAG2_V3_20170530.nc")
        ds = xr.open_dataset(url)
        prof = ds["z"].sel(lat=lat, method="nearest").sel(
            lon=slice(*lon_range))
        x_km = (prof.lon.values - np.mean(lon_range)) * 111.0 \
               * np.cos(np.radians(lat))
        return x_km, prof.values
    except Exception as e:
        print(f"  EMAG2 fetch failed ({type(e).__name__}: {e}); "
              f"using synthetic fallback.")
        return None


def make_figure():
    apply_style()

    # Try real data, fall back to synthetic
    real = try_real_emag2()
    if real is not None:
        x_km, anomaly = real
        source_label = "EMAG2v3 (NOAA NCEI; public domain)"
    else:
        x_km, anomaly, true_peaks = synthetic_stripe_profile()
        source_label = ("Synthetic from Cande & Kent 1995 GPTS "
                        "(half-rate 2.85 cm/yr)")

    # Find peaks (positive anomalies = normal polarity bands)
    # Tight prominence + minimum spacing of ~30 km to suppress noise picks
    peaks_idx, _ = find_peaks(anomaly, prominence=130, distance=120,
                               width=8)
    peaks_x = x_km[peaks_idx]
    peaks_y = anomaly[peaks_idx]

    # Convert peak positions to half-rate against GPTS
    # Map the first few positive-side peaks to their corresponding GPTS chrons.
    # On the positive (+x) side of the axis the major chrons are, in order:
    # C1n centre (≈ 0.39 Ma), C2An centre (≈ 3.09 Ma),
    # C3n combined centre (≈ 5.12 Ma using Thvera midpoint),
    # C3An_2 centre (≈ 6.58 Ma).
    pos_peaks = sorted(peaks_x[peaks_x > 5])
    gpts_centres = [
        0.5 * (GPTS["C1n_Brunhes"][0] + GPTS["C1n_Brunhes"][1]),
        0.5 * (GPTS["C2An_Gauss"][0]  + GPTS["C2An_Gauss"][1]),
        0.5 * (GPTS["C3n_Thvera"][0]  + GPTS["C3n_Thvera"][1]),
        0.5 * (GPTS["C3An_2"][0]      + GPTS["C3An_2"][1]),
        0.5 * (GPTS["C4n_2"][0]       + GPTS["C4n_2"][1]),
    ]
    n_use = min(len(pos_peaks), len(gpts_centres))
    if n_use >= 2:
        # Linear fit through origin: distance_km = (10*half_rate_cm_yr) * age_Ma
        ages_use = np.array(gpts_centres[:n_use])
        dist_use = np.array(pos_peaks[:n_use])
        # Least-squares slope (forced through origin)
        slope = np.sum(ages_use * dist_use) / np.sum(ages_use ** 2)
        half_rate_cm_yr = slope / 10.0
    else:
        half_rate_cm_yr = float("nan")

    # ── Build figure ──
    fig = plt.figure(figsize=(13, 6))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.6], hspace=0.30)

    ax_polarity = fig.add_subplot(gs[0])
    ax_anom = fig.add_subplot(gs[1], sharex=ax_polarity)

    # ── (a) Synthetic GPTS polarity bar (if synthetic mode) ──
    ax_polarity.set_xlim(-300, 300)
    ax_polarity.set_ylim(0, 1)
    rate_km_per_Ma = 2.85 * 10.0
    for name, (a1, a2) in GPTS.items():
        for sign in (+1, -1):
            lo, hi = sorted([sign * a1 * rate_km_per_Ma,
                             sign * a2 * rate_km_per_Ma])
            ax_polarity.add_patch(Rectangle((lo, 0.1), hi - lo, 0.8,
                                             facecolor="black",
                                             edgecolor="none"))
    ax_polarity.axvline(0, color=PALETTE["verm"], lw=1.5, ls="-",
                        alpha=0.9, zorder=5)
    ax_polarity.text(0, 1.05, "ridge axis", fontsize=9.5, ha="center",
                     color=PALETTE["verm"], style="italic")
    ax_polarity.set_yticks([])
    ax_polarity.set_title("(a) Predicted polarity stripes from GPTS "
                          "(black = normal polarity)",
                          loc="left", fontsize=11)
    ax_polarity.spines["left"].set_visible(False)

    # ── (b) Magnetic anomaly profile ──
    ax_anom.plot(x_km, anomaly, color=PALETTE["black"], lw=0.8)
    ax_anom.fill_between(x_km, 0, anomaly,
                          where=(anomaly > 0),
                          facecolor=PALETTE["blue"], alpha=0.55,
                          interpolate=True, label="Positive (normal polarity)")
    ax_anom.fill_between(x_km, 0, anomaly,
                          where=(anomaly < 0),
                          facecolor=PALETTE["verm"], alpha=0.40,
                          interpolate=True, label="Negative (reversed polarity)")
    ax_anom.axhline(0, color=PALETTE["black"], lw=0.5, alpha=0.5)
    ax_anom.scatter(peaks_x, peaks_y, marker="v", s=60, c=PALETTE["pink"],
                    edgecolor="black", lw=0.6, zorder=5,
                    label="find_peaks() detections")
    ax_anom.axvline(0, color=PALETTE["verm"], lw=1.5, alpha=0.9)
    ax_anom.set_xlim(-300, 300)
    ax_anom.set_xlabel("Distance from ridge axis (km)")
    ax_anom.set_ylabel("Magnetic anomaly (nT)")
    ax_anom.set_title(f"(b) Magnetic anomaly profile across the Juan de Fuca "
                       f"Ridge at 47°N — {source_label}",
                       loc="left", fontsize=11)
    ax_anom.legend(loc="lower right", framealpha=0.92, fontsize=9.5)
    ax_anom.grid(True, alpha=0.3)

    # Inversion result box
    if not np.isnan(half_rate_cm_yr):
        ax_anom.text(0.02, 0.96,
                      f"Inverted half-spreading rate: "
                      f"{half_rate_cm_yr:.2f} cm/yr\n"
                      f"(reported JdF: 2.85 cm/yr)",
                      transform=ax_anom.transAxes,
                      fontsize=10, va="top", ha="left",
                      bbox=dict(boxstyle="round,pad=0.25",
                                facecolor="white", edgecolor=PALETTE["black"],
                                alpha=0.92))

    return fig


if __name__ == "__main__":
    fig = make_figure()
    out = os.path.join(os.path.dirname(__file__), "..", "figures",
                       "F5_jdf_magnetic_stripes.png")
    save(fig, out)
    print(f"Wrote {out}")
