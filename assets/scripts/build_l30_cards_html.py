"""
build_l30_cards_html.py

Render the six Lecture 30 "Synthesis Studio" station cards as a single,
self-contained, print-ready HTML file. Each group figure is embedded directly
in the document as a base64 data-URI, so the file can be opened in any browser
and printed (one card per page) with no external assets.

Companion to build_l30_printable_cards.py (which produces the PDF version).

Output: assets/handouts/lecture_30_synthesis_station_cards.html
License: CC-BY 4.0
"""
import base64
import html
import os

HERE = os.path.dirname(__file__)
FIGDIR = os.path.join(HERE, "..", "figures")
OUTDIR = os.path.join(HERE, "..", "handouts")
OUT = os.path.join(OUTDIR, "lecture_30_synthesis_station_cards.html")

CARD_FIELDS = [
    "1 · Methods (2–4 course methods you would deploy)",
    "2 · Observable → property (what you measure; what Earth property it senses)",
    "3 · The null space (what one method alone cannot tell you)",
    "4 · The joint move (method A + method B removes which ambiguity?)",
    "5 · One number (an order-of-magnitude estimate you can produce)",
    "6 · The one-method trap (the hidden single-method assumption)",
]

GROUPS = [
    dict(
        fig="fig_l30_group1_earth.png",
        title="Group 1 — The Whole Planet",
        scale="planetary interior  ·  ~10,000 km",
        question=("How do we know Earth's outer core is liquid iron — and how "
                  "would you find the core of Mars with a single seismometer?"),
        methods=("S-wave shadow and teleseismic body waves; normal modes and "
                 "PKIKP; mean density and moment of inertia; the geodynamo."),
    ),
    dict(
        fig="fig_l30_group2_spreading_seafloor.png",
        title="Group 2 — Ocean Geophysics: The Spreading Seafloor",
        scale="ridge to abyssal plain  ·  ~1,000 km",
        question=("For one patch of seafloor — how old is it, how deep should "
                  "it be, and how much heat should it give off?"),
        methods=("Magnetic reversal stripes (age); bathymetry and gravity "
                 "(depth); heat-flow probe with the half-space cooling model "
                 "(q = 510·t^(−1/2) mW m⁻², d = 2500 + 350·t^(1/2) m, t in Ma)."),
    ),
    dict(
        fig="fig_l30_group3_cascadia_hazard.png",
        title="Group 3 — Cascadia Earthquake & Tsunami Hazard",
        scale="subduction margin  ·  regional",
        question=("What will the next Cascadia megathrust do to Seattle and "
                  "the coast?"),
        methods=("Seismic imaging of slab geometry and width W; waveform and "
                 "paleoseismic moment M₀; geodetic (GPS/InSAR) locking; "
                 "ground-motion and tsunami forward models (M₀ = μ·D̄·L·W)."),
    ),
    dict(
        fig="fig_l30_group4_mountains_isostasy.png",
        title="Group 4 — Mountains, Basins & the Continents",
        scale="lithosphere  ·  10–500 km",
        question=("Why is the Tibetan Plateau (or the Cascades) high — and "
                  "what holds it up?"),
        methods=("Free-air versus Bouguer gravity; Airy and Pratt isostasy; "
                 "crustal refraction for Moho depth; the Nafe–Drake bridge "
                 "(Airy root r ≈ ρ_c·h / (ρ_m − ρ_c))."),
    ),
    dict(
        fig="fig_l30_group5_cryosphere.png",
        title="Group 5 — The Cryosphere & Climate–Solid Earth Coupling",
        scale="ice sheet to mantle  ·  regional–global",
        question=("How do we weigh an ice sheet and watch it melt — and why "
                  "does the solid Earth bounce back?"),
        methods=("Time-lapse and satellite gravity (mass change); glacial "
                 "isostatic adjustment (rebound, mantle viscosity); "
                 "cryoseismology; distributed acoustic sensing on ice."),
    ),
    dict(
        fig="fig_l30_group6_plate_kinematics.png",
        title="Group 6 — The Reconstructed Past: Plate Kinematics",
        scale="whole planet  ·  deep time",
        question=("How do we rewind the plates 100 million years — and why "
                  "isn't the hotspot frame fixed?"),
        methods=("Paleomagnetism (paleolatitude, apparent polar wander); "
                 "seafloor magnetic isochrons; hotspot tracks; "
                 "plate reconstructions."),
    ),
]


def data_uri(path: str) -> str:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{b64}"


CSS = """
:root {
  --ink: #111111; --blue: #0072B2; --verm: #D55E00; --grey: #555555;
  --rule: #BBBBBB;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: var(--ink); line-height: 1.45;
}
.card {
  width: 8.5in; min-height: 11in; padding: 0.6in 0.7in; margin: 0 auto;
  page-break-after: always; display: flex; flex-direction: column;
}
.card:last-child { page-break-after: auto; }
.eyebrow { font-size: 10pt; letter-spacing: 0.04em; color: var(--grey);
  text-transform: uppercase; }
h1 { font-size: 19pt; color: var(--blue); margin: 0.05in 0 0.02in; }
.scale { font-style: italic; color: var(--grey); font-size: 11pt; margin-bottom: 0.18in; }
.figwrap { text-align: center; margin: 0.05in 0 0.18in; }
.figwrap img { max-width: 100%; max-height: 3.7in; object-fit: contain; }
h2 { font-size: 12.5pt; color: var(--verm); margin: 0.12in 0 0.04in; }
.body { font-size: 11pt; margin: 0 0 0.06in; }
.synthtitle { font-size: 13pt; color: var(--blue); font-weight: 700;
  margin: 0.14in 0 0.02in; border-bottom: 1.5px solid var(--blue); padding-bottom: 0.04in; }
.field { font-size: 10.5pt; color: var(--ink); margin: 0.13in 0 0.02in; }
.rule { border: 0; border-top: 0.8px solid var(--rule); margin: 0.05in 0 0; height: 0; }
.rule.tall { margin-top: 0.30in; }
.footer { margin-top: auto; font-style: italic; font-size: 9.5pt; color: var(--grey);
  border-top: 0.8px solid var(--rule); padding-top: 0.08in; }
.toolbar {
  position: sticky; top: 0; background: #f4f6f8; border-bottom: 1px solid #d4dadf;
  padding: 8px 14px; font-size: 13px; color: #333; text-align: center;
}
.toolbar button {
  font: inherit; padding: 5px 14px; margin-left: 10px; cursor: pointer;
  background: var(--blue); color: white; border: 0; border-radius: 5px;
}
@media print {
  .toolbar { display: none; }
  .card { margin: 0; }
}
@page { size: Letter portrait; margin: 0; }
"""


def render_card(g: dict) -> str:
    fields = "\n".join(
        f'      <div class="field">{html.escape(f)}</div>\n'
        f'      <hr class="rule">\n      <hr class="rule tall">'
        for f in CARD_FIELDS
    )
    return f"""  <section class="card">
    <div class="eyebrow">ESS 314 · Lecture 30 Synthesis Studio</div>
    <h1>{html.escape(g['title'])}</h1>
    <div class="scale">{html.escape(g['scale'])}</div>
    <div class="figwrap"><img alt="{html.escape(g['title'])} figure" src="{data_uri(os.path.join(FIGDIR, g['fig']))}"></div>
    <h2>Question</h2>
    <div class="body">{html.escape(g['question'])}</div>
    <h2>Methods on the table</h2>
    <div class="body">{html.escape(g['methods'])}</div>
    <div class="synthtitle">Synthesis Card</div>
{fields}
    <div class="footer">The one rule: name at least two methods, and one ambiguity their combination resolves.</div>
  </section>"""


def main() -> None:
    os.makedirs(OUTDIR, exist_ok=True)
    cards = "\n".join(render_card(g) for g in GROUPS)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ESS 314 L30 — Synthesis Studio Station Cards</title>
<style>{CSS}</style>
</head>
<body>
  <div class="toolbar">
    Six station cards — print one per table (one card per page; figures are embedded).
    <button onclick="window.print()">Print</button>
  </div>
{cards}
</body>
</html>
"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    size_kb = os.path.getsize(OUT) / 1024
    print(f"wrote {OUT} ({size_kb:.0f} KB, {len(GROUPS)} cards)")


if __name__ == "__main__":
    main()
