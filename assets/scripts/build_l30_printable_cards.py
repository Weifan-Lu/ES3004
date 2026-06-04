"""
build_l30_printable_cards.py

Assembles a print-ready PDF of the six Lecture 30 synthesis station cards.
Each page (US Letter, portrait) pairs one group figure with its prompt and a
blank Synthesis Card for students to complete at the table.

Output: slides/week10/lecture_30_synthesis_station_cards.pdf
License: CC-BY 4.0
"""
import os
import textwrap
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import image as mpimg

mpl.rcParams.update({
    "font.size": 11,
    "savefig.dpi": 300,
})

COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]

HERE = os.path.dirname(__file__)
FIGDIR = os.path.join(HERE, "..", "figures")
OUTDIR = os.path.join(HERE, "..", "handouts")

CARD_FIELDS = [
    "1. Methods (2-4 course methods)",
    "2. Observable -> property (what you measure; what it senses)",
    "3. The null space (what one method alone cannot tell you)",
    "4. The joint move (method A + B removes which ambiguity?)",
    "5. One number (an order-of-magnitude estimate)",
    "6. The one-method trap (the hidden single-method assumption)",
]

GROUPS = [
    dict(
        fig="fig_l30_group1_whole_planet.png",
        title="Group 1 - The Whole Planet",
        scale="planetary interior  |  ~10,000 km",
        question=("How do we know Earth's outer core is liquid iron - and how "
                  "would you find the core of Mars with a single seismometer?"),
        methods=("S-wave shadow and teleseismic body waves; normal modes and "
                 "PKIKP; mean density and moment of inertia; the geodynamo."),
    ),
    dict(
        fig="fig_l30_group2_spreading_seafloor.png",
        title="Group 2 - Ocean Geophysics: The Spreading Seafloor",
        scale="ridge to abyssal plain  |  ~1,000 km",
        question=("For one patch of seafloor - how old is it, how deep should "
                  "it be, and how much heat should it give off?"),
        methods=("Magnetic reversal stripes (age); bathymetry and gravity "
                 "(depth); heat-flow probe with the half-space cooling model."),
    ),
    dict(
        fig="fig_l30_group3_cascadia_hazard.png",
        title="Group 3 - Cascadia Earthquake & Tsunami Hazard",
        scale="subduction margin  |  regional",
        question=("What will the next Cascadia megathrust do to Seattle and "
                  "the coast?"),
        methods=("Seismic imaging of slab geometry and width W; waveform and "
                 "paleoseismic moment M0; geodetic (GPS/InSAR) locking; "
                 "ground-motion and tsunami forward models."),
    ),
    dict(
        fig="fig_l30_group4_mountains_isostasy.png",
        title="Group 4 - Mountains, Basins & the Continents",
        scale="lithosphere  |  10-500 km",
        question=("Why is the Tibetan Plateau (or the Cascades) high - and "
                  "what holds it up?"),
        methods=("Free-air versus Bouguer gravity; Airy and Pratt isostasy; "
                 "crustal refraction for Moho depth; the Nafe-Drake bridge."),
    ),
    dict(
        fig="fig_l30_group5_cryosphere.png",
        title="Group 5 - The Cryosphere & Climate-Solid Earth Coupling",
        scale="ice sheet to mantle  |  regional-global",
        question=("How do we weigh an ice sheet and watch it melt - and why "
                  "does the solid Earth bounce back?"),
        methods=("Time-lapse and satellite gravity (mass change); glacial "
                 "isostatic adjustment (rebound, mantle viscosity); "
                 "cryoseismology; distributed acoustic sensing on ice."),
    ),
    dict(
        fig="fig_l30_group6_plate_kinematics.png",
        title="Group 6 - The Reconstructed Past: Plate Kinematics",
        scale="whole planet  |  deep time",
        question=("How do we rewind the plates 100 million years - and why "
                  "isn't the hotspot frame fixed?"),
        methods=("Paleomagnetism (paleolatitude, apparent polar wander); "
                 "seafloor magnetic isochrons; hotspot tracks; "
                 "plate reconstructions."),
    ),
]


def draw_page(pdf, g):
    fig = plt.figure(figsize=(8.5, 11.0))   # US Letter portrait

    # ---- header band ----
    fig.text(0.06, 0.965, "ESS 314  -  Lecture 30 Synthesis Studio",
             fontsize=10, color=COLORS[6], alpha=0.7)
    fig.text(0.06, 0.940, g["title"], fontsize=16, fontweight="bold",
             color=COLORS[0])
    fig.text(0.06, 0.918, g["scale"], fontsize=11, style="italic",
             color=COLORS[6])

    # ---- figure ----
    img = mpimg.imread(os.path.join(FIGDIR, g["fig"]))
    ax = fig.add_axes([0.06, 0.50, 0.88, 0.40])
    ax.imshow(img)
    ax.axis("off")

    # ---- prompt ----
    y = 0.475
    fig.text(0.06, y, "Question", fontsize=12, fontweight="bold",
             color=COLORS[4])
    y -= 0.022
    for line in textwrap.wrap(g["question"], width=92):
        fig.text(0.06, y, line, fontsize=11)
        y -= 0.020
    y -= 0.008
    fig.text(0.06, y, "Methods on the table", fontsize=12, fontweight="bold",
             color=COLORS[4])
    y -= 0.022
    for line in textwrap.wrap(g["methods"], width=92):
        fig.text(0.06, y, line, fontsize=11)
        y -= 0.020

    # ---- blank Synthesis Card ----
    y -= 0.012
    fig.text(0.06, y, "Synthesis Card", fontsize=13, fontweight="bold",
             color=COLORS[0])
    y -= 0.006
    fig.add_artist(mpl.lines.Line2D([0.06, 0.94], [y, y], color=COLORS[0],
                                    lw=1.2))
    y -= 0.026
    for field in CARD_FIELDS:
        fig.text(0.06, y, field, fontsize=10.5, color=COLORS[6])
        y -= 0.024
        # write-on rule
        fig.add_artist(mpl.lines.Line2D([0.08, 0.94], [y, y],
                                        color="#BBBBBB", lw=0.8))
        y -= 0.022

    fig.text(0.06, 0.035,
             "The one rule: name at least two methods, and one ambiguity their "
             "combination resolves.",
             fontsize=9.5, style="italic", color=COLORS[6])

    pdf.savefig(fig)
    plt.close(fig)


def main():
    out = os.path.join(OUTDIR, "lecture_30_synthesis_station_cards.pdf")
    with PdfPages(out) as pdf:
        for g in GROUPS:
            draw_page(pdf, g)
        d = pdf.infodict()
        d["Title"] = "ESS 314 L30 Synthesis Studio - Station Cards"
        d["Subject"] = "Six-group synthesis activity for Lecture 30"
    print("wrote", out)


if __name__ == "__main__":
    main()
