"""
fig_mantle_convection_engine.py

Scientific content: A schematic cross-section of the cooling, convecting mantle,
from the surface to the core-mantle boundary (CMB). It ties together the
whole-Earth thermal budget and the surface expressions of mantle convection:
  - a mid-ocean ridge (shallow, passive divergent upwelling),
  - a subducting slab (cold, dense downwelling) sinking toward the lower mantle,
  - a narrow, hot mantle plume rising from the CMB thermal boundary layer to a
    hotspot at the surface, DEFLECTED near the top by large-scale horizontal
    mantle flow ("mantle wind") -- so hotspots are not perfectly fixed,
  - the global heat budget (surface heat loss, radiogenic heating, core heat),
  - the Rayleigh-number criterion that the mantle convects rather than conducts.
Carries no data; original schematic.

Concepts follow standard geodynamics (Turcotte & Schubert, 2014, Geodynamics
3rd ed., Ch. 4-6) and the plume review of Koppers et al. (2021), Nat. Rev.
Earth Environ. 2, 382-401 (deep CMB origin, deflection by mantle flow).
Heat-budget value ~46 TW after Davies & Davies (2010), Solid Earth 1, 5-24.

Output: assets/figures/fig_mantle_convection_engine.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Polygon, FancyArrowPatch, Rectangle, Circle

mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 15,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

HOT   = "#D55E00"   # vermilion: hot upwelling / plume / D''
COLD  = "#0072B2"   # blue: cold downwelling / slab
CORE  = "#E69F00"   # orange: outer core
MANT  = "#F4EEE7"   # light mantle background
WIND  = "#009E73"   # green: mantle-wind flow
BLACK = "#000000"

CMB = 2890.0        # km

fig, ax = plt.subplots(figsize=(11.8, 7.6))

# Mantle background and core ---------------------------------------------
ax.add_patch(Rectangle((0, 0), 10, CMB, facecolor=MANT, edgecolor="none",
                        zorder=0))
ax.add_patch(Rectangle((0, CMB), 10, 280, facecolor=CORE, edgecolor=BLACK,
                        lw=1.2, hatch="..", zorder=1))
ax.text(5.0, CMB + 140, "outer core  (liquid iron)", ha="center", va="center",
        fontsize=11.5, color=BLACK, weight="bold")
ax.plot([0, 10], [CMB, CMB], color=BLACK, lw=2.2, zorder=3)
ax.text(9.85, CMB - 95, "core-mantle boundary (2890 km)", ha="right",
        va="center", fontsize=10.5, color=BLACK)
# D'' hot boundary layer (plume source)
for cx in (3.5, 4.1, 4.7):
    ax.add_patch(Circle((cx, CMB - 75), 0.42, facecolor=HOT, alpha=0.55,
                        edgecolor="none", zorder=2))
ax.text(0.9, CMB - 70, "D'' layer\n(plume source)", ha="left", va="center",
        fontsize=10, color=HOT, style="italic")

# Lithosphere band --------------------------------------------------------
ax.add_patch(Rectangle((0, 0), 10, 130, facecolor="#C9C2B8",
                        edgecolor=BLACK, lw=1.3, zorder=3))

# Mid-ocean ridge (passive shallow upwelling) -----------------------------
xr = 2.0
ax.add_patch(FancyArrowPatch((xr, 120), (xr - 0.9, 25), arrowstyle="-|>",
             mutation_scale=15, color=BLACK, lw=1.6, zorder=6))
ax.add_patch(FancyArrowPatch((xr, 120), (xr + 0.9, 25), arrowstyle="-|>",
             mutation_scale=15, color=BLACK, lw=1.6, zorder=6))
ax.add_patch(Polygon([(xr - 0.45, 520), (xr + 0.45, 520), (xr, 150)],
                     closed=True, facecolor=HOT, alpha=0.28,
                     edgecolor="none", zorder=2))
ax.annotate("mid-ocean ridge\n(shallow, passive upwelling)",
            xy=(xr, 12), xytext=(0.15, -330),
            fontsize=10.5, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=BLACK, lw=1.0))

# Subducting slab (cold downwelling) -------------------------------------
xs = 7.9
ax.add_patch(Polygon([(xs + 0.55, 130), (xs - 0.15, 130),
                      (6.0, 2700), (6.6, 2700)],
                     closed=True, facecolor=COLD, edgecolor=BLACK, lw=1.2,
                     alpha=0.85, zorder=4))
for f in (0.20, 0.48, 0.74):
    y0 = 130 + f * 2560
    x0 = xs + 0.2 - f * 1.55
    ax.add_patch(FancyArrowPatch((x0, y0), (x0 - 0.10, y0 + 250),
                 arrowstyle="-|>", mutation_scale=13, color="white", lw=1.7,
                 zorder=5))
ax.annotate("subducting slab\n(cold, dense downwelling)",
            xy=(6.9, 1550), xytext=(8.0, 1300),
            fontsize=10.5, ha="left", va="center", color=COLD,
            arrowprops=dict(arrowstyle="->", color=COLD, lw=1.1))

# Mantle plume from the CMB, deflected to the RIGHT near the top ----------
py = np.linspace(CMB - 80, 150, 60)
px = 4.0 + 1.3 * np.clip((900 - py) / 900.0, 0, 1) ** 1.3   # bends above 900 km
half = 0.16 + 0.12 * (py - 150) / (CMB - 150)
xL, xR = px - half, px + half
verts = list(zip(xL, py)) + list(zip(xR[::-1], py[::-1]))
ax.add_patch(Polygon(verts, closed=True, facecolor=HOT, edgecolor="none",
                     alpha=0.92, zorder=4))
ax.add_patch(Circle((px[-1], 235), 0.42, facecolor=HOT, alpha=0.85,
                    edgecolor="none", zorder=4))
xv = px[-1]
ax.add_patch(Polygon([(xv - 0.32, 130), (xv + 0.32, 130), (xv, -45)],
                     closed=True, facecolor=HOT, edgecolor=BLACK, lw=1.0,
                     zorder=6))
ax.annotate("hotspot volcano",
            xy=(xv, -35), xytext=(xv + 0.7, -330),
            fontsize=10.5, ha="left", va="center", color=HOT,
            arrowprops=dict(arrowstyle="->", color=HOT, lw=1.1))
ax.text(2.35, 1950, "plume rising\nfrom the CMB", ha="left", va="center",
        fontsize=10.5, color=HOT, weight="bold")

# Mantle wind: horizontal flow deflecting the plume top -------------------
ax.add_patch(FancyArrowPatch((3.3, 470), (6.4, 470), arrowstyle="-|>",
             mutation_scale=18, color=WIND, lw=2.4, zorder=5))
ax.text(4.85, 300, "mantle wind", ha="center", va="center",
        fontsize=11, color=WIND, weight="bold")

# A subtle convective return limb (left) ---------------------------------
ax.add_patch(FancyArrowPatch((0.8, 2250), (1.7, 620),
             connectionstyle="arc3,rad=-0.30", arrowstyle="-|>",
             mutation_scale=14, color="#9A9A9A", lw=1.5, zorder=2))

# Heat-budget annotations -------------------------------------------------
for hx in (0.7, 9.3):
    ax.add_patch(FancyArrowPatch((hx, 40), (hx, -150), arrowstyle="-|>",
                 mutation_scale=15, color=HOT, lw=2.0, zorder=6))
ax.text(5.0, -370, "surface heat loss  $\\approx$  46 TW",
        ha="center", va="center", fontsize=12, color=BLACK, weight="bold")
ax.text(0.9, 2230, "radiogenic heating\n+ secular cooling\nof the mantle",
        ha="left", va="center", fontsize=10, color="#5A5A5A", style="italic")
ax.annotate("heat from core\n$\\approx$ 5-15 TW",
            xy=(5.6, CMB - 55), xytext=(7.2, 2520),
            fontsize=10.5, ha="left", va="center", color=HOT,
            arrowprops=dict(arrowstyle="->", color=HOT, lw=1.0))

# Rayleigh-number box -----------------------------------------------------
ax.text(0.18, 1080,
        "$Ra = \\dfrac{\\rho g \\alpha \\Delta T D^{3}}{\\kappa \\eta}$"
        "\n\n$Ra \\sim 10^{6}$-$10^{8} \\gg Ra_{\\rm crit}\\,(\\sim 10^{3})$"
        "\n\n$\\Rightarrow$ the mantle convects:\nheat moves by flow,\nnot conduction",
        ha="left", va="center", fontsize=11,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                  edgecolor=BLACK, lw=1.2), zorder=7)

# Axes cosmetics ----------------------------------------------------------
ax.set_xlim(-0.2, 10.2)
ax.set_ylim(CMB + 320, -460)
ax.set_yticks([0, 660, 1500, 2890])
ax.set_yticklabels(["0", "660", "1500", "2890"])
ax.set_ylabel("depth (km)")
ax.set_xticks([])
for spine in ("top", "right", "bottom"):
    ax.spines[spine].set_visible(False)
ax.set_title("The cooling, convecting Earth: plate tectonics and hotspots "
             "as surface expressions", fontsize=14.5, pad=12)
fig.tight_layout()
fig.savefig("assets/figures/fig_mantle_convection_engine.png",
            bbox_inches="tight")
print("wrote assets/figures/fig_mantle_convection_engine.png")
