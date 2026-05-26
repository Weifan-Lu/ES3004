# L26 — Lithosphere: Oceanic vs. Continental
## Production Package

**Course:** ESS 314 — Introduction to Geophysics
**Module:** 7 — Tectonics, Lithosphere, and the Cooling Earth
**Lecture:** 26 (first lecture of Module 7 per the revised roadmap)
**Status:** Production-ready · awaiting integration into the `ess314` repository

---

## Package Contents

```
L26_package/
├── README.md                                       (this file)
├── lectures/
│   └── 26_lithosphere_oceanic_continental.md       (full 9-section MyST markdown,
│                                                    602 lines including 3 inline
│                                                    Python data-access blocks)
├── assets/
│   ├── scripts/
│   │   ├── _ess314_style.py                        (shared palette + rcParams)
│   │   ├── _coastlines.py                          (Natural Earth GeoJSON loader)
│   │   ├── _land_mask.py                           (1-deg land mask cache)
│   │   └── F1–F13_*.py                             (13 figure scripts)
│   ├── figures/
│   │   └── F1–F13_*.png                            (13 generated figures, 200 dpi)
│   └── data/
│       └── ne_110m_{coastline,land}.geojson        (cached Natural Earth)
├── slides/
│   └── lecture_26_slides.md                        (Marp deck, exactly 25 slides)
├── instructor_private/
│   ├── L26_master_matrix.md                        (full 11-attribute answer key)
│   ├── L26_concept_check_answers.md                (4-question key)
│   └── L26_facilitation_script.md                  (40-min beat-by-beat guide)
└── references_L26_delta.bib                        (15 BibTeX entries to append)
```

---

## Key Pedagogical Design Choices

**Framing question:** *What do we mean by "the lithosphere," and why does the answer change depending on which observable we use?*

**Data-access pedagogy (§4).** Three runnable Python code blocks with full provenance:
- Code Block A — Müller/Seton 2020 seafloor age via `xarray` from EarthByte webDAV
- Code Block B — CRUST1.0 Moho XYZ from UCSD
- Code Block C — ETOPO1 bathymetric transect via PyGMT's `grdtrack`

Each block teaches a distinct workflow (cloud netCDF / local XYZ / virtual GMT dataset). Students see the working geophysicist's first 30 minutes with a new question.

**Survey come-back through controlled active learning (§6).** The eleven-attribute comparison matrix covers composition, layering, density, thickness, seismic structure, heat flow, gravity, magnetics, age, and geodynamic role. Delivered in three predict-then-reveal beats. Students *predict* before each reveal and fill in their own matrix — survey content earned through prediction rather than transcribed.

**Two key conceptual figures:**
- **F6** (Boundary Layers — Key Figure). Oceanic boundary layers thickening with √age (panel a) alongside an old craton column showing four "lithosphere bases" — elastic Te (80 km), mechanical/yield (150 km), seismic LAB (220 km), thermal LAB (280 km) — *all different*. This is the lecture's thesis.
- **F11** (Oceanic vs. Continental Vp). Side-by-side velocity profiles showing sharp shallow oceanic Moho with strong LVZ, vs. deep gradational continental Moho with weak or absent LVZ.

**PNW anchor (§9):** Siletzia — the Eocene oceanic plateau accreted to Cascadia. Anderson et al. 2024 (open access via USGS) provides the reproducibility hook.

**AI literacy:** "AI as a Reasoning Partner" — students prompt an AI to derive the HSC model and grade the response against a four-criterion physical-correctness rubric.

---

## Quality Gate Status

| Check | Status |
|-------|--------|
| `invert_yaxis` count (must be 0) | ✅ 0 |
| `bbox_inches` only in savefig (must be 0 in rcParams) | ✅ 0 |
| Minimum font size 11pt | ✅ 11pt |
| Slide count ≤ 25 | ✅ 25 |
| All 13 figures generated | ✅ 13 |
| 9 lecture sections + LOs + AI literacy + Further Reading | ✅ |
| Three §4 code blocks | ✅ 3 |
| Three §6 predict-then-reveal beats | ✅ 3 |
| PNW anchor (Siletzia §9) | ✅ |
| AI-literacy callout with rubric | ✅ |
| Open-access references in §8 | ✅ Richards 2018, Holdt 2025, Levin 2023, Long 2024, Anderson 2024 |

**Anti-survey checklist:**
- ✅ Predict-then-reveal active-learning beats (3)
- ✅ Non-uniqueness / two-models-same-data (HSC vs. plate, §3.5/F5)
- ✅ Multi-method synthesis (F6 combines elastic + thermal + seismic + heat flow)
- ✅ Open research question with 2022–2025 paper
- ✅ AI-literacy critique beat
- ✅ PNW anchor

---

## Important Note on Figure Generation

**The sandbox network is restricted** (per `<network_configuration>`: only github.com, npmjs, pypi, etc. are reachable — not EarthByte, UCSD, or IRIS). Three of the figures (F1 seafloor age, F2 Atlantic transect, F12 CRUST1.0 Moho) are therefore generated from **realistic synthetic data** that faithfully mimics the real datasets, not from the real data itself.

The three Code Blocks in §4 of the lecture are designed to run on **the student's machine**, where these data servers are reachable. Each script that mimics a real-data figure carries:

- A docstring explaining the real-data workflow
- A title noting "real-data version produced by Code Block X in §4"

Students who run the code blocks on their laptops will get the *actual* data figures. This is honest and reproducible. If you regenerate these three figures on the deployment server (which presumably has full internet access), you can either:

1. Modify F1/F2/F12 to pull the real data with `xarray.open_dataset(URL)` — the same calls shown in the lecture body.
2. Keep the synthetic versions, since they match the visual patterns and serve the pedagogical role.

I recommend option (1) for the deployed book.

---

## Integration Notes for `ess314` Repository

When integrating into the live `uw-geophysics-edu.github.io/ess314` JupyterBook:

1. **Move files** into the existing repo structure:
   - `lectures/26_lithosphere_oceanic_continental.md` → `lectures/`
   - `assets/scripts/*.py` → existing `assets/scripts/`
   - `assets/figures/*.png` → existing `assets/figures/`
   - `slides/lecture_26_slides.md` → existing `slides/`
2. **Append** `references_L26_delta.bib` entries to the course-wide `references.bib`.
3. **Update `_toc.yml`** to insert L26 into Module 7 and remove the old `25_heat_geodynamics` placeholder.
4. **Compile slides** with Marp CLI:
   `npx @marp-team/marp-cli slides/lecture_26_slides.md -o slides/lecture_26.html`
5. **Update `references.bib`** by appending the entries from `references_L26_delta.bib`.
6. **Instructor-private** files should go to the private `ess314-instructor` repo, not the public book.

---

*End of L26 package README.*
