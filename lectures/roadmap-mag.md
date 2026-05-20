Your sequencing is right. Content-first, figures-second, slides-last is the natural dependency order — prose stabilizes the conceptual structure, figures formalize what the prose claims, and slides crystallize the in-class delivery. I'll add one structural refinement (a downstream cleanup pass that Copilot owns) and tighten the granularity inside each phase.

## Roadmap at a glance

| Phase | Goal | Agent | Sessions | Output |
|---|---|---|---|---|
| **1. Prose** | Three deployment-ready MyST lecture files with figure briefs in place of figures | Claude | 3 (L23 → L24 → L25) | `lectures/23_earth_magnetism.md`, `lectures/24_rock_magnetism.md`, `lectures/25_magnetic_anomalies.md` |
| **1.5. Renumber** | One-commit cleanup: rename L26–L30, update TOC, syllabus, cross-references | Copilot (you in VS Code) | 1 commit | Renamed files, updated `_toc.yml`, `syllabus.md`, `references.bib` if needed |
| **2. Figures** | All Python scripts, rendered PNGs, rock photos with attribution; lecture files wired up | Claude | 3 batches (shared → data → photos) | `assets/scripts/*.py`, `assets/figures/*.png`, lecture files updated in place |
| **3. Slides** | Three Marp decks aligned to lecture files | Marine (you), Claude provides scaffolds | 3 (1 per deck) | `slides/lecture_23_slides.md`, `lecture_24_slides.md`, `lecture_25_slides.md` |

Total: 10 working sessions end-to-end. We're not on a clock, so this can stretch across as many weeks as you want.

## Phase 1 — Prose (3 sessions, one per lecture)

For each lecture I'll follow the standard skill workflow: audit your source material, do Phase-2 open-access source research, then produce the complete MyST lecture file with **figure briefs** (description + script filename + caption) as placeholders for the `{figure}` directives. No figures are rendered yet — the lecture is fully readable as prose with bracketed figure descriptions where images will land.

**What I need from you per lecture, before the session:**

| Lecture | Source material I need from you | What I already have |
|---|---|---|
| L23 | Nothing extra — current L23 markdown is the substrate; I'll restructure and rewrite | Current `23_earth_magnetism.md`, your three reference images, your handwritten B/H/M derivation |
| L24 | Any original lecture notes / past slide decks / paper handouts on rock magnetism and the Vine–Matthews–Morley framework — even if rough or from prior years | Wikimedia rock-photo curation list, your seafloor-stripe Image 3 |
| L25 | Any original lecture notes on magnetic anomalies, surveys, or anomaly maps; ideally one prior worked example you've taught (e.g. a PNW survey) | Open knowledge of EMAG2, USGS NAm map — but your teaching examples will make it sing |

If you have legacy slide decks for L24 and L25 from prior years, drop them as PDFs in the project — even ZIP-of-JPEGs format (the format the skill expects) is fine. If you don't have anything for L24/L25, I'll work from open-access sources and the standard textbook chapter, but session output will be conceptually generic rather than carrying your teaching voice.

**Gate after each lecture:** you review the prose draft and either approve or send short directive corrections. I incorporate, then move to the next lecture.

## Phase 1.5 — Renumber (Copilot owns; one commit)

The moment all three lecture-file prose drafts are approved, you drive Copilot through this consolidated cleanup in VS Code:

```
git mv lectures/24_magnetic_field_tectonics.md lectures/24_rock_magnetism.md
git mv lectures/25_heat_geodynamics.md          lectures/26_heat_geodynamics.md
git mv lectures/26_divergent_margins.md          lectures/27_divergent_margins.md
git mv lectures/27_convergent_margins.md         lectures/28_convergent_margins.md
git mv lectures/28_transform_intraplate.md       lectures/29_transform_intraplate.md
git mv lectures/29_synthesis.md                  lectures/30_synthesis.md
```

Plus: `_toc.yml` entries, `syllabus.md` schedule rows (class numbers 41–49 → 42–50), any "Lecture 25 takes…" prose in current L25–L29 that forward-references the next lecture, and the Lab 8 lecture-anchor (currently → L23/L24; now → L25). I'll provide a one-page diff guide before this commit so Copilot has every search/replace target spelled out.

## Phase 2 — Figures (3 sessions, batched by dependency)

Figures are batched by dependency rather than by lecture, because several figures appear in more than one lecture (the dipole, the B/H/M constitutive figure) and we want them built once.

**Session 2a — Foundational figures.** Built first because L24 and L25 reference them.
- `fig_dipole_big.py` — the big single-panel dipole drawing
- `fig_field_potential_gravity_analogy.py` — gravity↔magnetics parallel
- `fig_BHM_constitutive.py` — your handwritten note, made into a Python figure
- `fig_DIF_at_station.py` — local (D, I, F) decomposition

**Session 2b — Data figures.** Built from open-access archives; requires network/data work.
- `fig_declination_world_map.py` — WMM 2025 grid, Python pull from NOAA
- `fig_three_sources_cross_section.py`, `fig_field_power_spectrum.py`, `fig_seattle_secular_variation.py`, `fig_paleolatitude_from_inclination.py` — port/refresh from current L23
- `fig_juan_de_fuca_profile.py` — NOAA NCEI trackline data
- `fig_gpts.py` — Ogg 2020 polarity timescale
- `fig_emag2_global.py` and `fig_usgs_nam_anomaly.py` — public-domain map extracts
- `fig_anomaly_sphere_forward.py`, `fig_inclination_asymmetry.py` — forward-model figures for L25

**Session 2c — Photographs, schematics, finishing.**
- Download + verify Wikimedia rock photos (magnetite, hematite, pyrrhotite, pillow basalt), commit with attribution captions in `assets/figures/` 
- `fig_magnetosphere_solar_wind.py`, `fig_space_weather_timeline.py` — schematics
- `fig_drm_acquisition.py`, `fig_crm_growth.py`, `fig_ridge_stripes.py`, `fig_apwp_siletzia.py`, `fig_anomaly_decomposition.py` — remaining schematics
- Wire every figure into the three lecture files; replace each figure brief with the rendered `{figure}` directive

**Gate after each batch:** you spot-check rendered PNGs. Mis-rendered or pedagogically off figures get redirected before the next batch.

## Phase 3 — Slides (you lead; Claude scaffolds)

You said you'll do the slides at the end. The right division of labour is:

**Claude (me) — per deck, in one session:**
- Marp scaffold matching the lecture's section structure (≤ 25 slides per deck)
- Pre-filled title slide, learning-objectives slide, section-divider slides, figure-image references pointing to the rendered PNGs in `assets/figures/`, the concept-check slide, the summary slide
- A draft of bullets per slide (skeletal — you'll rewrite for in-class voice)

**You — per deck:**
- In-class voice and pacing
- Animations, builds, transitions
- The intangible "what to say while clicking" layer that doesn't belong in the markdown
- Final aesthetic pass against the shared `ess314.css` theme

If you want me to do more or less of this division, say so when we get to Phase 3.

## Recommended immediate next action

To unblock Phase 1, **session 1 — L23**, I need one input from you:

> Take any L24/L25 source material you have — old lecture notes, slide PDFs (any format), handouts, problem sets, anything — and drop them in the project. If you have nothing for L24/L25 beyond standard textbook coverage, say so and I'll work from open-access sources alone. For L23, I have what I need.

Once that's in (or you confirm you have nothing extra to add), I'll produce **new L23** end-to-end in the next session: audit → Phase-2 source verification → full MyST lecture file with figure briefs → quality-gate pass → handoff for your review. After your L23 review, we move to L24, then L25, then the Copilot renumbering commit closes Phase 1.