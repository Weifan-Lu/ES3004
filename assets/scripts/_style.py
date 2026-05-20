"""Shared style for ESS 314 figures (Module 6 — magnetism).

Imports the WCAG AA colorblind-safe palette and a standard matplotlib
rcParams block. Use::

    from _style import COLORS, apply_style
    apply_style()
"""
from __future__ import annotations

import matplotlib as mpl

# WCAG AA colorblind-safe palette (Wong 2011) — the project standard.
COLORS = {
    "blue":    "#0072B2",  # primary
    "orange":  "#E69F00",
    "skyblue": "#56B4E9",
    "green":   "#009E73",
    "vermilion": "#D55E00",
    "pink":    "#CC79A7",
    "black":   "#000000",
    "grey":    "#5C5C5C",
    "lightgrey": "#CCCCCC",
}

# Standard project rcParams. Note: bbox_inches="tight" is invalid in
# matplotlib rcParams (skill rule); always pass it to savefig() instead.
_RCPARAMS = {
    "font.family": "DejaVu Sans",
    "font.size": 13,
    "axes.labelsize": 13,
    "axes.titlesize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
    "figure.titlesize": 15,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "axes.linewidth": 0.8,
    "lines.linewidth": 1.6,
    "savefig.dpi": 300,
    "figure.dpi": 100,
}


def apply_style() -> None:
    """Apply the project-standard rcParams to the current matplotlib session."""
    mpl.rcParams.update(_RCPARAMS)
