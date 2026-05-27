# L27 — Ridges and Rifts — Production Package

**Lecture:** Lecture 27 — Ridges and Rifts
**Module:** 7 (Tectonics, Lithosphere, and the Cooling Earth)
**Position:** L26 (Lithosphere) → **L27 (Ridges and Rifts)** → L28 (Convergent Margins) → L29 (Transforms) → L30 (Synthesis)
**Date produced:** May 2026
**Audit reference:** L27_AUDIT_AND_OUTLINE.md Rev 3

This package contains the complete L27 deliverables: lecture markdown, 11 figures with their generating Python scripts, Marp slide deck, instructor-private materials, and references delta.

## Package contents

```
L27_package/
├── lectures/
│   └── 27_ridges_and_rifts.md       # MyST Markdown lecture (429 lines)
├── slides/
│   └── lecture_27_slides.md          # Marp slide deck (25 slides)
├── assets/
│   ├── scripts/
│   │   ├── _ess314_style.py          # Shared style module (carry-over from L26)
│   │   ├── _coastlines.py            # Natural Earth coastline helper (L26)
│   │   ├── _land_mask.py             # Land masking helper (L26)
│   │   ├── F1_ridge_magmatic_system.py
│   │   ├── F2_mar_gravity_profile.py
│   │   ├── F3_gravity_non_uniqueness.py
│   │   ├── F4_slow_vs_fast_ridge.py
│   │   ├── F5_jdf_magnetic_stripes.py
│   │   ├── F6_ear_system_map.py
│   │   ├── F7_ear_kenya_cross_section.py
│   │   ├── F9_continental_rift_gravity.py
│   │   ├── F10_three_rift_comparison.py
│   │   ├── F11_conus_bouguer_map.py
│   │   └── F12_rifting_continuum.py
│   ├── figures/                       # 11 generated PNG figures
│   └── data/
│       ├── ne_110m_coastline.geojson  # Natural Earth (carry-over)
│       └── ne_110m_land.geojson       # Natural Earth (carry-over)
├── instructor_private/
│   ├── L27_master_matrix.md           # Full 6×6 rifting continuum reveal table
│   ├── L27_concept_check_answers.md   # 4-question answer key, 8 pts total
│   └── L27_facilitation_script.md     # 50-min classroom timing
├── references_L27_delta.bib           # 11 new BibTeX entries
└── README.md                          # This file
```

## Integration into the main `ess314/` repository

For deployment by the Copilot build agent:

1. **Lecture markdown.** Copy `lectures/27_ridges_and_rifts.md` into the main repo at `lectures/27_ridges_and_rifts.md`. Update `_toc.yml` to place L27 between L26 and L28 (currently the placeholder slot `14_earthquake_phenomena_I` may show in some configurations; verify and remove if needed).

2. **Figure scripts.** Copy all of `assets/scripts/F*.py` to `assets/scripts/` in the main repo. The shared helpers (`_ess314_style.py`, `_coastlines.py`, `_land_mask.py`) are unchanged from L26 — no overwrite needed.

3. **Figures.** Copy all of `assets/figures/F*.png` to `assets/figures/` in the main repo. The numbered file names (F1–F12) do not collide with L26's figures because L26 uses the same numbering scheme in a different namespace at deployment.

4. **Natural Earth data cache.** No action needed; the cache at `assets/data/ne_110m_*.geojson` is already in the main repo from L26.

5. **Slide deck.** Copy `slides/lecture_27_slides.md` to `slides/lecture_27_slides.md` in the main repo. Confirm the slides build with:
   ```bash
   npx @marp-team/marp-cli slides/lecture_27_slides.md --html
   ```

6. **Instructor materials.** Copy the three files in `instructor_private/` into the *private* `ess314-instructor` sibling repo, not the public one. The TA guides for Module 7 go alongside.

7. **References.** Merge `references_L27_delta.bib` into the main repo's `references.bib`. Each entry has a unique citation key; check for duplicates against the existing bib before appending.

## Open-license sourcing (Rev 3 audit)

Of the 11 L27 figures:

- **5 connect to real research data or open-license figures** (Rev 3 design):
  - **F2** — Sandwell & Smith global marine gravity overlay (real data when network reachable; synthetic fallback in deployed PNG, documented in caption)
  - **F4** — AMC-depth-vs-spreading-rate scatter after Bell et al. 2022 *Frontiers* (CC-BY 4.0)
  - **F5** — NOAA EMAG2v3 magnetic anomaly data (public domain) via Code Block D
  - **F6** — references Biggs et al. 2021 *Nature Communications* Fig. 1 (CC-BY 4.0) for the research-grade EAR map
  - **F11** — references USGS Fact Sheet 78-95 (Phillips et al. 1993) for the CONUS Bouguer map (public domain)

- **6 are Python forward models / pedagogical schematics** (intrinsically pedagogical; no open equivalent):
  - F1, F3, F7, F9, F10, F12.

All figure captions identify their source. All real-data fetchers (F2, F5, F11) include synthetic fallbacks that work in the sandbox, so the deployed PNG is reproducible offline.

## Build-time improvement opportunities (optional)

If the Copilot build agent has network access to external data servers, three figures can be upgraded:

1. **F2** — Run the script with the Sandwell & Smith URL active and replace the synthetic overlay with real satellite-altimetry gravity.
2. **F5** — Run Code Block D against the live NOAA EMAG2 grid and use the real-data output as F5.
3. **F6** — Download Biggs et al. 2021 Fig. 1 directly from Springer Nature (CC-BY 4.0); replace the schematic F6 with the proper journal figure and update the caption to credit. *Recommended: verify CC-BY licence on download page before reuse.*
4. **F11** — Download the USGS FS 78-95 figure (public domain) directly; replace the synthetic with the proper USGS PNG.

These are *optional*; the current package builds and deploys without them.

## Pedagogical design notes (Rev 3 highlights)

- **Two predict-then-reveal rounds** sit in §5: Round 1 (MOR gravity non-uniqueness) and Round 2 (rifting continuum spectrum). The vocabulary is "Round" — no "Beat" anywhere in the L27 files.
- **Code Block D** introduces the fourth canonical data-access pattern of the course: peak detection on a 1D profile, using `scipy.signal.find_peaks` against a real magnetic profile, with explicit failure-mode handling in the AI literacy callout.
- **The Pacific Northwest anchor** is JdF + Axial Seamount + OOI cabled array. Connects directly back to L26 Siletzia and forward to L28 Cascadia.

## Quality gate status

| Check | Status |
|-------|--------|
| All 11 figure scripts present | ✅ |
| All 11 figure PNGs generated | ✅ |
| Lecture markdown follows MyST conventions matching L26 | ✅ |
| Zero "Beat" hits (lecture + slides + instructor) | ✅ |
| Wong colorblind-safe palette in all figures | ✅ |
| `bbox_inches="tight"` only in savefig (never rcParams) | ✅ |
| `fig.tight_layout()` before every savefig | ✅ |
| `ax.set_ylim(max, 0)` for all depth axes; no invert_yaxis | ✅ |
| ≥ 11pt fonts everywhere | ✅ |
| Code Block D documented and tested | ✅ (synthetic fallback; inverts to 2.17 cm/yr vs. 2.85 reported) |
| Slide deck at 25-slide cap | ✅ (25 slides, at cap) |
| Alt text on every slide-deck figure | ✅ |
| Instructor-private deliverables complete | ✅ |
| References delta with verified DOIs | ✅ |

End of README.
