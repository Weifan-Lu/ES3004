"""
fig_planetary_interiors.py

Three planetary bodies (Earth, Mars, Moon) drawn to a common scale as
concentric circles, each labelled with its planetary radius, core radius,
core/planet ratio, and the number of seismic stations used to image it.

Core radii and station counts after:
  Earth:  Core radius 3480 km; thousands of FDSN stations.
  Mars:   Stähler et al. (2021), Science 373, 443-448. Core r ≈ 1830 km.
  Moon:   Apollo-era normal-mode + receiver-function analyses; core r ≈ 330 km.

Original schematic; carries no data.

Output: assets/figures/fig_planetary_interiors.png
License: CC-BY 4.0
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl

mpl.rcParams.update({
    "font.size": 12,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

# ── Planetary data ──────────────────────────────────────────────────────
planets = [
    dict(name="Earth",  R=6371, Rc=3480,  stations="thousands of stations\n(FDSN global network)",
         color_mantle="#6BAED6", color_core="#FD8D3C",
         xc=0.18),
    dict(name="Mars",   R=3390, Rc=1830,  stations="ONE station\n(InSight SEIS)",
         color_mantle="#74C476", color_core="#FD8D3C",
         xc=0.55),
    dict(name="Moon",   R=1737, Rc=330,   stations="four stations\n(Apollo network)",
         color_mantle="#9ECAE1", color_core="#FD8D3C",
         xc=0.83),
]

# Scale everything to Earth radius = 0.18 of figure width
SCALE = 0.175 / 6371   # display-units per km

FIG_W, FIG_H = 13, 6.0
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

BODY_Y = 0.55   # vertical centre of planets

for p in planets:
    xc = p["xc"]
    R_disp  = p["R"] * SCALE
    Rc_disp = p["Rc"] * SCALE

    # Mantle circle
    mantle = plt.Circle((xc, BODY_Y), R_disp,
                        facecolor=p["color_mantle"], edgecolor="#333333",
                        lw=1.8, zorder=2)
    ax.add_patch(mantle)

    # Core circle (hatched to indicate liquid outer core for Earth/Mars)
    core = plt.Circle((xc, BODY_Y), Rc_disp,
                      facecolor=p["color_core"], edgecolor="#333333",
                      lw=1.4, hatch="..", alpha=0.85, zorder=3)
    ax.add_patch(core)

    # For Earth: solid inner core (Ric ≈ 1220 km)
    if p["name"] == "Earth":
        Ric_disp = 1220 * SCALE
        inner = plt.Circle((xc, BODY_Y), Ric_disp,
                           facecolor="#E6550D", edgecolor="#333333",
                           lw=1.2, zorder=4)
        ax.add_patch(inner)
        ax.text(xc, BODY_Y, "solid\ninner\ncore",
                ha="center", va="center", fontsize=8,
                color="white", fontweight="bold", zorder=5)

    ratio = p["Rc"] / p["R"]

    # Planet name
    ax.text(xc, BODY_Y + R_disp + 0.055, p["name"],
            ha="center", va="bottom", fontsize=14, fontweight="bold",
            color="#222222")

    # Planet radius
    ax.text(xc, BODY_Y + R_disp + 0.025,
            f"R = {p['R']:,} km",
            ha="center", va="bottom", fontsize=9, color="#444444")

    # Core radius annotation
    ax.annotate("",
        xy=(xc + Rc_disp, BODY_Y),
        xytext=(xc, BODY_Y),
        arrowprops=dict(arrowstyle="<->", color="#333333", lw=1.4))
    ax.text(xc + Rc_disp / 2, BODY_Y - 0.035,
            f"$R_c$ = {p['Rc']:,} km\n({ratio:.0%} of $R$)",
            ha="center", va="top", fontsize=9, color="#333333")

    # Station count
    ax.text(xc, BODY_Y - R_disp - 0.06, p["stations"],
            ha="center", va="top", fontsize=9, color="#CC5500",
            style="italic")

# ── Legend ───────────────────────────────────────────────────────────────
leg_handles = [
    mpatches.Patch(facecolor="#6BAED6", edgecolor="#333333", label="Silicate mantle"),
    mpatches.Patch(facecolor="#FD8D3C", edgecolor="#333333", hatch="..", label="Liquid iron outer core"),
    mpatches.Patch(facecolor="#E6550D", edgecolor="#333333", label="Solid inner core (Earth only)"),
]
ax.legend(handles=leg_handles, loc="lower center", bbox_to_anchor=(0.5, 0.0),
          ncol=3, framealpha=0.9, fontsize=10)

ax.set_title(
    "Planetary interiors determined seismologically — drawn to common scale",
    fontsize=12, pad=6)

fig.tight_layout()
out = "assets/figures/fig_planetary_interiors.png"
fig.savefig(out, bbox_inches="tight")
print(f"Saved: {out}")
