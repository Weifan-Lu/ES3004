"""Shared style helper for ESS 314 figures (L26/L27 carry-over).

Provides:
  - PALETTE: WCAG-AA colorblind-safe palette (Wong 2011) with project keys.
  - apply_style(): sets standard matplotlib rcParams.
  - save(fig, path): savefig with project defaults (300 dpi, bbox tight).
"""
from __future__ import annotations

import os
import matplotlib as mpl


PALETTE = {
    "blue":    "#0072B2",
    "orange":  "#E69F00",
    "skyblue": "#56B4E9",
    "green":   "#009E73",
    "verm":    "#D55E00",  # vermilion
    "pink":    "#CC79A7",
    "yellow":  "#F0E442",
    "black":   "#000000",
    "grey":    "#5C5C5C",
    "lightgrey": "#CCCCCC",
    "white":   "#FFFFFF",
}


_RCPARAMS = {
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "legend.frameon": False,
    "figure.dpi": 110,
    "savefig.dpi": 300,
}


def apply_style() -> None:
    """Apply the standard ESS 314 matplotlib rcParams."""
    mpl.rcParams.update(_RCPARAMS)


def save(fig, path: str) -> None:
    """Save a figure with project defaults (tight bbox, 300 dpi)."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fig.savefig(path, dpi=300, bbox_inches="tight")
