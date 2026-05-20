"""fig_anomaly_decomposition.py — schematic of the magnetic-anomaly decomposition.

Shows F_observed = F_core (IGRF) + F_lith (static anomaly) + F_ext (diurnal),
then the residual ΔF = F_obs - F_IGRF - F_diurnal that survives both
corrections and is the geophysical signal of interest.

The x-axis represents distance along a survey track (or time, equivalently
for a constant-speed survey).

ESS 314, Lecture 25 §2 (Magnetic Anomalies — What is an anomaly?).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from _style import COLORS, apply_style


def synthesize_signals(x: np.ndarray) -> dict:
    """Build synthetic component traces for the decomposition figure."""
    # Core field: ~52,800 nT with a small linear regional gradient.
    F_core = 52800 + 0.4 * (x - x.mean())

    # Lithospheric anomaly: a localized Gaussian "bump" centred mid-survey.
    centre = x.mean()
    width = 8.0
    amp = 130
    F_lith = amp * np.exp(-((x - centre) / width) ** 2)

    # External (diurnal) variation: a slow ~30 nT sinusoid + noise.
    np.random.seed(11)
    F_ext = 25 * np.sin(2 * np.pi * x / 80) + 2.0 * np.random.randn(len(x))

    F_obs = F_core + F_lith + F_ext
    delta_F = F_obs - F_core - F_ext  # = F_lith, by construction
    return dict(F_obs=F_obs, F_core=F_core, F_lith=F_lith,
                F_ext=F_ext, delta_F=delta_F)


def main(out: Path) -> None:
    apply_style()

    x = np.linspace(0, 60, 600)  # km along survey track
    sig = synthesize_signals(x)

    fig, axes = plt.subplots(5, 1, figsize=(12, 9.5), sharex=True,
                              gridspec_kw=dict(hspace=0.32))

    # 1. Observed total field.
    ax = axes[0]
    ax.plot(x, sig["F_obs"], color=COLORS["black"], lw=1.6)
    ax.set_ylabel("$F_\\mathrm{obs}$\n(nT)", fontsize=11)
    ax.set_title("(a)  Measured total field along survey track",
                 loc="left", fontsize=12, fontweight="bold", pad=3)
    ax.set_ylim(sig["F_obs"].min() - 40, sig["F_obs"].max() + 40)
    ax.grid(True, alpha=0.3)
    ax.text(0.985, 0.92,
            "$F_\\mathrm{obs} = F_\\mathrm{core} + F_\\mathrm{lith} + F_\\mathrm{ext}$",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=12, color=COLORS["black"],
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor=COLORS["grey"], lw=0.6))

    # 2. Core field (IGRF).
    ax = axes[1]
    ax.plot(x, sig["F_core"], color=COLORS["blue"], lw=1.6)
    ax.set_ylabel("$F_\\mathrm{core}$\n(IGRF, nT)", fontsize=11)
    ax.set_title("(b)  Core field model (IGRF) — long-wavelength, slowly drifting",
                 loc="left", fontsize=12, fontweight="bold", pad=3,
                 color=COLORS["blue"])
    ax.set_ylim(sig["F_core"].min() - 20, sig["F_core"].max() + 20)
    ax.grid(True, alpha=0.3)

    # 3. Lithospheric anomaly.
    ax = axes[2]
    ax.plot(x, sig["F_lith"], color=COLORS["green"], lw=1.6)
    ax.fill_between(x, 0, sig["F_lith"], where=sig["F_lith"] > 0,
                     color=COLORS["green"], alpha=0.18)
    ax.axhline(0, color=COLORS["grey"], lw=0.5)
    ax.set_ylabel("$F_\\mathrm{lith}$\n(nT)", fontsize=11)
    ax.set_title("(c)  Lithospheric anomaly — static, the signal of interest",
                 loc="left", fontsize=12, fontweight="bold", pad=3,
                 color=COLORS["green"])
    ax.set_ylim(-30, 180)
    ax.grid(True, alpha=0.3)
    ax.annotate("buried magnetised body",
                xy=(x.mean(), 130), xytext=(x.mean() + 18, 100),
                fontsize=10, color=COLORS["green"], style="italic",
                arrowprops=dict(arrowstyle="->", color=COLORS["green"], lw=1.0))

    # 4. External (diurnal) variation.
    ax = axes[3]
    ax.plot(x, sig["F_ext"], color=COLORS["orange"], lw=1.4)
    ax.axhline(0, color=COLORS["grey"], lw=0.5)
    ax.set_ylabel("$F_\\mathrm{ext}$\n(nT)", fontsize=11)
    ax.set_title("(d)  External field (diurnal, ionospheric) — time-varying",
                 loc="left", fontsize=12, fontweight="bold", pad=3,
                 color=COLORS["orange"])
    ax.set_ylim(-40, 40)
    ax.grid(True, alpha=0.3)
    ax.text(0.985, 0.92,
            "removed by base-station correction",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=10, color=COLORS["orange"], style="italic")

    # 5. Recovered anomaly Delta F (the residual after correction).
    ax = axes[4]
    ax.plot(x, sig["delta_F"], color=COLORS["vermilion"], lw=2.0)
    ax.fill_between(x, 0, sig["delta_F"], where=sig["delta_F"] > 0,
                     color=COLORS["vermilion"], alpha=0.18)
    ax.axhline(0, color=COLORS["grey"], lw=0.5)
    ax.set_ylabel("$\\Delta F$\n(nT)", fontsize=11)
    ax.set_xlabel("Distance along survey track (km)", fontsize=12)
    ax.set_title("(e)  Recovered anomaly  "
                 r"$\Delta F = F_\mathrm{obs} - F_\mathrm{IGRF} - F_\mathrm{diurnal}$",
                 loc="left", fontsize=12, fontweight="bold", pad=3,
                 color=COLORS["vermilion"])
    ax.set_ylim(-30, 180)
    ax.grid(True, alpha=0.3)

    fig.suptitle("From measurement to anomaly — the three corrections",
                 fontsize=14, fontweight="bold", y=0.995)

    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir / "fig_anomaly_decomposition.png")
    print("wrote", out_dir / "fig_anomaly_decomposition.png")
