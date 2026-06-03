"""
fig_28_parameter_space.py  -> SF3_parameter_space.png

Scientific content (the CENTERPIECE figure of L28):
The four-panel correlation analysis that anchors Wirth et al. (2022). Subduction
segments that have hosted great (Mw >= 8.5) earthquakes are plotted against four
parameters, with maximum observed Mw on the y-axis:
  TOP ROW  - the "dispelled" recipe: subducting-plate AGE (Wirth r = 0.05) and
             trench-normal CONVERGENCE RATE (r = 0.19). Flat scatter; the
             Ruff & Kanamori (1980) hypothesis that old + fast slabs host the
             largest earthquakes is not supported.
  BOTTOM ROW - the geometric controls the data actually favour: seismogenic-zone
             WIDTH (r = 0.44, the strongest single parameter) and downdip
             CURVATURE (|r| = 0.42; flatter megathrusts rupture larger,
             Bletery et al. 2016). Width panel marks the empirical thresholds:
             every recorded M>=8.5 has width > 75 km; every M>=9.2 has
             width > 150 km.
Giant (Mw >= 9) events are drawn as vermillion stars; M 8.5-8.9 as blue circles.

DATA: verbatim from Table 1 of Wirth et al. (2022) - the 14 instrumentally
recorded M >= 8.5 margin segments (plus Cascadia 1700 from palaeoseismology).
Convergence rate is TRENCH-NORMAL in the HS3-NUVEL1A ABSOLUTE reference frame
(Gripp & Gordon 2002), which is why Sumatra-Andaman reads 3 mm/yr. Downdip
curvature is from Bletery et al. (2016). The annotated r and statistical-power
values are Wirth's published Figure 3 values (computed over the full
instrumental + historical M>=8.5 set, so they differ slightly from the
correlation of these 14 points alone). Sediment thickness "<0.5" -> 0.4; "-" ->
NaN.

Reproduces the scientific content of (original figures NOT used):
  Wirth, E. A., Sahakian, V. J., Wallace, L. M. & Melnick, D. (2022). The
    occurrence and hazards of great subduction zone earthquakes. Nat. Rev. Earth
    Environ. 3, 125-140, doi:10.1038/s43017-021-00245-w. (Table 1, Fig. 3.)
  Bletery, Q. et al. (2016). Mega-earthquakes rupture flat megathrusts.
    Science 354, 1027-1031, doi:10.1126/science.aag0482.
  Ruff, L. & Kanamori, H. (1980). Phys. Earth Planet. Inter. 23, 240-252.

Output: assets/figures/SF3_parameter_space.png
License: CC-BY 4.0 (this script)
"""
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams.update({
    "font.size": 12.5, "axes.titlesize": 14, "axes.labelsize": 12.5,
    "xtick.labelsize": 11.5, "ytick.labelsize": 11.5, "legend.fontsize": 11,
    "figure.dpi": 150, "savefig.dpi": 300,
})

BLUE, ORANGE, SKY, GREEN, VERM, PINK, BLACK = (
    "#0072B2", "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7", "#000000")

# --- Wirth et al. (2022) Table 1 (verbatim) ---------------------------------
# name, Mw, age_Ma, conv_mm_yr(trench-normal HS3 absolute), sed_km,
#   dip_deg, width_km, curvature, label
NAN = np.nan
rows = [
    ("Tohoku 2011",        9.1, 132, 96, 0.4, 18, 161, 1.39, "Tohoku"),
    ("Cascadia 1700",      9.0,   7, 32, 4.0, 11, 127, 0.94, "Cascadia"),
    ("Maule 2010",         8.8,  34, 62, 2.0, 22, 105, 2.04, None),
    ("Valdivia 1960",      9.5,  23, 75, 1.0, 14, 190, 1.86, "Valdivia"),
    ("Atacama 1922",       8.5,  45, 75, 0.4, 22, 105, 1.77, None),
    ("Rat Is. 1965",       8.7,  49, 36, NAN, 31,  72, 3.63, None),
    ("Alaska 1964",        9.2,  43, 52, 2.0, 15, 180, 0.60, "Alaska"),
    ("Alaska 1957",        8.6,  55, 61, 2.0, 35,  75, 2.50, None),
    ("Unimak 1946",        8.6,  57, 62, NAN, 33,  72, 2.41, None),
    ("Nias 2005",          8.6,  43, 28, 4.0, 11, 174, 2.01, None),
    ("Sumatra-Andaman 2004", 9.1, 73,  3, 3.0,  9, 243, 2.26, "Sumatra"),
    ("Kuril 1963",         8.5, 117, 71, 0.4, 22, 102, 3.31, None),
    ("Kamchatka 1952",     9.0, 105, 77, 0.4, 27, 110, 2.45, None),
    ("Ecuador-Colombia 1906", 8.8, 12, 55, 3.0, 20, 101, 2.78, None),
]
name = [r[0] for r in rows]
Mw   = np.array([r[1] for r in rows], float)
age  = np.array([r[2] for r in rows], float)
conv = np.array([r[3] for r in rows], float)
dip  = np.array([r[5] for r in rows], float)
width= np.array([r[6] for r in rows], float)
curv = np.array([r[7] for r in rows], float)
lab  = [r[8] for r in rows]
giant = Mw >= 8.95

fig, axes = plt.subplots(2, 2, figsize=(13.0, 9.4))

def panel(ax, x, xlabel, r_text, verdict, vcolor, labels=False,
          thresholds=None, xlim=None, verdict_xy=(0.03, 0.93)):
    ax.scatter(x[~giant], Mw[~giant], s=70, c=BLUE, edgecolor=BLACK, lw=0.6,
               alpha=0.85, zorder=3)
    ax.scatter(x[giant], Mw[giant], s=190, marker="*", c=VERM,
               edgecolor=BLACK, lw=0.8, zorder=4)
    if thresholds:
        for xv, txt in thresholds:
            ax.axvline(xv, color="#888888", ls="--", lw=1.2, zorder=1)
            ax.text(xv, 9.62, txt, rotation=90, va="top", ha="right",
                    fontsize=9, color="#555555")
    if labels:
        for xi, mi, li in zip(x, Mw, lab):
            if li is not None and not np.isnan(xi):
                ax.annotate(li, xy=(xi, mi), xytext=(xi, mi + 0.07),
                            fontsize=8.5, ha="center", fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("maximum observed $M_w$")
    ax.set_ylim(8.4, 9.7)
    if xlim:
        ax.set_xlim(*xlim)
    ax.grid(alpha=0.22)
    # r annotation
    ax.text(0.97, 0.05, r_text, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=11, color=BLACK,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#cccccc"))
    # verdict banner
    vx, vy = verdict_xy
    va = "bottom" if vy < 0.3 else "top"
    ax.text(vx, vy, verdict, transform=ax.transAxes, ha="left", va=va,
            fontsize=11.5, color=vcolor, fontweight="bold")

# TOP ROW: the dispelled recipe (weak correlations)
panel(axes[0, 0], age, "subducting-plate age (Ma)",
      "Wirth $r=0.05$\npower $=0.05$", "DISPELLED", "#777777",
      labels=True, xlim=(0, 175), verdict_xy=(0.55, 0.10))
panel(axes[0, 1], conv, "trench-normal convergence rate (mm/yr)\n(HS3-NUVEL1A absolute frame)",
      "Wirth $r=0.19$\npower $=0.11$", "DISPELLED", "#777777",
      labels=True, xlim=(0, 105))

# BOTTOM ROW: the geometric controls (stronger correlations)
panel(axes[1, 0], width, "seismogenic-zone width (km)",
      "Wirth $r=0.44$\npower $=0.37$", "CONTROL", GREEN,
      labels=True, thresholds=[(75, "M$\\geq$8.5: width > 75 km"),
                               (150, "M$\\geq$9.2: width > 150 km")],
      xlim=(50, 260))
panel(axes[1, 1], curv, "downdip curvature  $K_s$  ($10^{-8}\\,$m$^{-1}$)",
      "Wirth $|r|=0.42$\npower $=0.34$", "CONTROL", GREEN,
      labels=True, xlim=(0, 4))
axes[1, 1].annotate("flatter $\\rightarrow$ larger\n(Bletery 2016)",
                    xy=(0.94, 9.0), xytext=(2.4, 9.45), fontsize=9.5,
                    color=GREEN, ha="center",
                    arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.4))

# legend (figure-level)
import matplotlib.lines as mlines
giant_h = mlines.Line2D([], [], marker="*", color=VERM, ls="none", ms=15,
                        markeredgecolor=BLACK, label="giant ($M_w \\geq 9$)")
big_h = mlines.Line2D([], [], marker="o", color=BLUE, ls="none", ms=9,
                      markeredgecolor=BLACK, label="great ($M_w$ 8.5-8.9)")
fig.legend(handles=[giant_h, big_h], loc="upper center", ncol=2,
           bbox_to_anchor=(0.5, 0.055), frameon=False)

fig.suptitle("What controls the maximum subduction earthquake? "
             "(Wirth et al. 2022, Table 1 & Fig. 3)", fontsize=15.5, y=0.995)
fig.text(0.5, 0.945,
         "Top: age and convergence rate \u2014 the recipe the data dispelled.   "
         "Bottom: seismogenic width and flatness \u2014 the geometric controls that hold.",
         ha="center", fontsize=11.5, color="#444444")
fig.tight_layout(rect=[0, 0.07, 1, 0.93])
out = "../figures/SF3_parameter_space.png"
fig.savefig(out, bbox_inches="tight")
print(f"Saved {out}")

# console check
for x, nm in [(age, "age"), (conv, "conv"), (width, "width"), (curv, "curv")]:
    m = ~np.isnan(x)
    r = np.corrcoef(x[m], Mw[m])[0, 1]
    print(f"  subset corr(Mw, {nm:5s}) = {r:+.2f}")
print(f"giants (Mw>=9): width {width[giant].min():.0f}-{width[giant].max():.0f} km, "
      f"age {age[giant].min():.0f}-{age[giant].max():.0f} Ma, "
      f"conv {conv[giant].min():.0f}-{conv[giant].max():.0f} mm/yr")
