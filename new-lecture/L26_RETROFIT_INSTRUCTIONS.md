# L26 Retrofit — Instructions for Copilot+Opus

**Repository:** `uw-geophysics-edu/ess314`
**Lecture URL (current state):** https://uw-geophysics-edu.github.io/ess314/lectures/26_lithosphere_oceanic_continental.html
**Files in scope:**
- `lectures/26_lithosphere_oceanic_continental.md` — main lecture markdown
- `slides/lecture_26_slides.md` — Marp slide deck
- `assets/figures/F1_seafloor_age_map.png` — to be regenerated from real data
- `assets/figures/F12_north_america_moho.png` — to be regenerated from real data
- `assets/figures/F13_siletzia_potential_fields.png` — to be replaced with the open-access Anderson 2024 figure
- `assets/scripts/F1_seafloor_age_map.py` — update or replace
- `assets/scripts/F12_north_america_moho.py` — update or replace
- `assets/scripts/F13_siletzia_potential_fields.py` — update or replace
- `references.bib` — add/update entries as needed

**Two independent tasks:**
1. **Vocabulary fix** — replace the word "Beat" everywhere it appears (it reads as AI-generated jargon).
2. **Figure retrofit** — replace three Python-synthetic figures (F1, F12, F13) with research-grade open-license sources.

---

## Task 1 — Replace the word "Beat"

The lecture uses "Beat A / Beat B / Beat C" to label the three predict-then-reveal segments inside §6. Replace with **Round 1 / Round 2 / Round 3**. ("Round" preserves the predict-reveal-discuss rhythm and reads naturally in a classroom context. If Marine prefers "Part" or "Stage" or "Pass" instead, do a global substitution with that term — the pattern is the same.)

### Find-and-replace table

Apply these substitutions to **`lectures/26_lithosphere_oceanic_continental.md`**, **`slides/lecture_26_slides.md`**, and any local instructor-private files (`instructor_private/L26_master_matrix.md`, `instructor_private/L26_facilitation_script.md`, `instructor_private/L26_concept_check_answers.md`) if those exist in the repo.

| Find (exact string) | Replace with |
|---------------------|--------------|
| `Comparison Matrix and Active-Learning Beats` | `Comparison Matrix and Three Predict-Then-Reveal Rounds` |
| `Beat A — Composition, density, and the consequences for subduction` | `Round 1 — Composition, density, and the consequences for subduction` |
| `Beat B — Thickness, seismic structure, and "what is the lithosphere?"` | `Round 2 — Thickness, seismic structure, and "what is the lithosphere?"` |
| `Beat B — Thickness, seismic structure, and “what is the lithosphere?”` | `Round 2 — Thickness, seismic structure, and “what is the lithosphere?”` |
| `Beat C — Heat flow, gravity, magnetics, age structure` | `Round 3 — Heat flow, gravity, magnetics, age structure` |
| `delivered in three beats` | `delivered in three rounds` |
| `This is the answer to Beat B.` | `This is the answer to Round 2.` |
| `We will return to this in Beat B of §6.` | `We will return to this in Round 2 of §6.` |
| `Beat B of our active-learning comparison in §6` | `Round 2 of our predict-then-reveal sequence in §6` |
| `Beat-by-Beat Reveal Order` | `Reveal order, round by round` |
| `Beat A` (any remaining occurrences) | `Round 1` |
| `Beat B` (any remaining occurrences) | `Round 2` |
| `Beat C` (any remaining occurrences) | `Round 3` |

### Slide deck — additional fixes

In `slides/lecture_26_slides.md`, the same substitutions apply. Specifically the following slide titles will need updating (the exact lines may vary slightly):

- `## Beat A — Composition, density, subduction (predict)` → `## Round 1 — Composition, density, subduction (predict)`
- `## Beat A — Reveal` → `## Round 1 — Reveal`
- `## Beat B — Thickness & seismic structure (predict)` → `## Round 2 — Thickness & seismic structure (predict)`
- `## Beat B — Reveal: oceanic vs. continental` $V_p$ → `## Round 2 — Reveal: oceanic vs. continental` $V_p$
- `## Beat B — The key figure` → `## Round 2 — The key figure`
- `## Beat C — Heat flow, gravity, magnetics, age (predict)` → `## Round 3 — Heat flow, gravity, magnetics, age (predict)`
- `## Beat C — Reveal` → `## Round 3 — Reveal`

### Verification for Task 1

After the substitution, run `grep -i "beat" lectures/26_lithosphere_oceanic_continental.md slides/lecture_26_slides.md instructor_private/L26_*.md 2>/dev/null` and confirm zero hits (or only hits that are clearly unrelated, like "heartbeat" or similar — there should be none in the L26 files).

---

## Task 2 — Retrofit three figures with real open-license data

The current L26 deployment uses Python-synthetic mimics for three figures because the sandbox where they were originally generated had no network access to the underlying data servers. The build server (with normal internet) can produce or fetch the real research-grade versions. Each retrofit replaces a synthetic figure with a properly attributed open-license source.

### 2A — F1 seafloor age map → real EarthByte/Seton data

**Current state:** `assets/figures/F1_seafloor_age_map.png` is a Python synthetic with idealized ridge geometries. Title reads "synthetic mimic of Müller/Seton 2020 grid."

**Target:** Real seafloor age map produced by running the existing Code Block A from §4.1 of the lecture markdown.

**Steps:**

1. Verify the EarthByte URL in Code Block A resolves. Open a Python shell and try:
   ```python
   import xarray as xr
   url = ("https://www.earthbyte.org/webdav/ftp/Data_Collections/"
          "Muller_etal_2019_Tectonics/Muller_etal_2019_Agegrids/"
          "Muller_etal_2019_Tectonics_v2.0_netCDF/"
          "Muller_etal_2019_Tectonics_v2.0_AgeGrid-0.nc")
   ds = xr.open_dataset(url)
   print(ds)
   ```
   If the URL fails (404 or permissions), try the equivalent file from the Seton et al. 2020 G-Cubed paper's archived dataset on the EarthByte FTP. The age grid is also mirrored at the Australian Research Data Commons. Search EarthByte's data portal at `https://www.earthbyte.org/category/agegrid/` for the current canonical URL and update Code Block A in the lecture markdown to match.

2. Replace the body of `assets/scripts/F1_seafloor_age_map.py` with a script that loads the real grid via `xarray`, applies the standard ESS 314 style (Wong palette, 11pt fonts, `bbox_inches="tight"` only in `savefig`, `fig.tight_layout()` before `savefig`), and renders to `assets/figures/F1_seafloor_age_map.png`. Use the same color map (`magma_r`, `vmin=0, vmax=180`) so the visual identity of the figure stays consistent. The land mask helper in `assets/scripts/_coastlines.py` and `assets/scripts/_land_mask.py` is already there from the original L26 production — reuse it for the continent overlay.

3. Update the lecture figure caption in `lectures/26_lithosphere_oceanic_continental.md`. The current title and caption mention "synthetic mimic" and "real-data version produced by Code Block A in §4 on your machine." Change to:

   **New caption:**
   ```
   Fig. 129 Global seafloor age from the Müller/Seton 2020 grid. The brightest bands are mid-ocean ridge axes (age ≈ 0); the darkest areas are the oldest oceanic crust (NW Pacific, ~180 Ma) — older crust has already been subducted. The width of each color band encodes the spreading rate: narrow bands in the slow-spreading Atlantic, wide bands in the fast-spreading Pacific. Data: Seton et al. 2020, *G-Cubed* 21, doi:10.1029/2020GC009214 (open license; cite when used). Produced by Code Block A in §4.
   ```

4. Also remove the title-line annotation in the figure ("synthetic mimic" / "real-data version produced by Code Block A in §4 on your machine") — make the title simply read **"Oceanic crust age — Müller/Seton 2020"**.

### 2B — F12 CRUST1.0 Moho map → real data

**Current state:** `assets/figures/F12_north_america_moho.png` is a Python synthetic mimicking the CRUST1.0 spatial pattern. Title reads "synthetic mimic of CRUST1.0."

**Target:** Real Moho thickness map of North America produced by loading the actual CRUST1.0 grid distributed by Scripps.

**Steps:**

1. Download the CRUST1.0 distribution from `https://igppweb.ucsd.edu/~gabi/crust1.html`. The file is `crust1.0.tar.gz`. Inside, find `crust1.bnds` (binary) or download the simpler XYZ versions if available — at minimum, the file with Moho depths on a 1° × 1° grid (or use the boundary depths file and compute Moho from there). The exact filename and format may differ from what Code Block B in §4.2 describes (which assumes a friendly XYZ named `xyzcoords.moho.txt`). Update Code Block B in the lecture markdown to match the actual current CRUST1.0 distribution format.

2. Replace `assets/scripts/F12_north_america_moho.py` with a script that:
   - Loads the real CRUST1.0 Moho grid
   - Crops to the North America bounding box (lon −130 to −60, lat 24 to 72)
   - Applies the same style (viridis colormap, vmin=10, vmax=55)
   - Overlays coastlines using `_coastlines.py` (already in repo)
   - Annotates the same regions (Canadian Shield, Rockies, Basin & Range, Cascadia, Appalachians, Gulf) at the same coordinates — these annotations are pedagogically important and the real data should show them clearly enough
   - Saves to `assets/figures/F12_north_america_moho.png`

3. Update the figure caption. Replace the current caption with:

   **New caption:**
   ```
   Fig. 130 North American Moho thickness from CRUST1.0 (Laske et al. 2013), regional crop. Oceans show the canonical ~10 km oceanic Moho; the Canadian Shield craton sits at ~45 km; the Rockies (with their tectonic root) reach ~50+ km; the Basin and Range, extended by Cenozoic rifting, has been thinned to ~28–30 km. Data: CRUST1.0 (Laske et al. 2013), https://igppweb.ucsd.edu/~gabi/crust1.html. Produced by Code Block B in §4.
   ```

4. Remove the "synthetic mimic" / "real-data version" annotation in the figure title — change to **"North American Moho thickness — CRUST1.0"**.

### 2C — F13 Siletzia gravity + aeromagnetic → Anderson et al. 2024 figure

**Current state:** `assets/figures/F13_siletzia_potential_fields.png` is a Python schematic mimicking the spatial pattern of Siletzia's gravity and aeromagnetic anomalies. Caption already cites Anderson et al. 2024 as the source.

**Target:** Use an actual figure from the Anderson et al. 2024 *Tectonics* paper, which is open-access via the USGS Publications Warehouse with US Geological Survey co-authors (Blakely, Wells).

**Steps:**

1. **Verify license status.** Fetch the paper landing page:
   - AGU/Wiley: `https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2022TC007720`
   - USGS Pubs Warehouse: `https://pubs.usgs.gov/publication/70251370`

   On the Wiley page, check whether the article is published under CC-BY 4.0 (look for the "Creative Commons" badge near the top of the abstract). The "Open Access Version: External Repository" link on the USGS page should confirm this.

   **If CC-BY confirmed:** Proceed to step 2 with full Wiley figures.
   **If CC-BY not confirmed but USGS Pubs Warehouse hosts a public-domain preprint version** (which it should, because Wells and Blakely are USGS employees and their work product is automatically public domain under US law): Use the preprint figure instead.
   **If neither route confirms reuse permission:** Skip the retrofit and instead update the existing synthetic figure's caption to be more explicit about its schematic nature (see fallback below).

2. **Download the figure.** Anderson et al. 2024 has several figures; the best single replacement for F13 is the one showing the side-by-side Bouguer gravity and aeromagnetic anomaly maps of the Puget Lowland (likely Figure 1 or Figure 4 in that paper — verify by looking at the paper). Save the figure to `assets/figures/F13_siletzia_potential_fields.png`, replacing the synthetic one.

3. **Update the figure script.** Replace `assets/scripts/F13_siletzia_potential_fields.py` with a short script that does nothing more than:
   - Document the source (Anderson et al. 2024, DOI, URL, license, retrieval date)
   - Optionally re-save with ESS 314 standard DPI (200) using PIL/Pillow if the downloaded image needs resizing

   This file documents provenance even though it doesn't generate the figure.

4. **Update the figure caption** in `lectures/26_lithosphere_oceanic_continental.md`:

   **New caption (if CC-BY confirmed):**
   ```
   Fig. 137 The geophysical signature of Siletzia in the Pacific Northwest forearc. (a) Bouguer gravity anomaly. (b) Aeromagnetic anomaly. Reproduced from Anderson, M. L., Blakely, R. J., Wells, R. E., & Dragovich, J. D. (2024). Deep structure of Siletzia in the Puget Lowland: Imaging an obducted plateau and accretionary thrust belt with potential fields. *Tectonics* 43, doi:10.1029/2022TC007720, under CC-BY 4.0.
   ```

   **New caption (if using USGS public-domain preprint version):**
   ```
   Fig. 137 The geophysical signature of Siletzia in the Pacific Northwest forearc. (a) Bouguer gravity anomaly. (b) Aeromagnetic anomaly. From Anderson, M. L., Blakely, R. J., Wells, R. E., & Dragovich, J. D. (2024). Deep structure of Siletzia in the Puget Lowland. *Tectonics* 43, doi:10.1029/2022TC007720. Reproduced from the USGS Publications Warehouse open-access version; figures by USGS authors are in the US public domain.
   ```

5. **Fallback** (if neither license route works): Keep the synthetic figure, but update its caption to be transparent:
   ```
   Fig. 137 Schematic geophysical signature of Siletzia in the Pacific Northwest forearc (illustrative; not a research figure). (a) Bouguer gravity high marking the high-density basaltic basement. (b) Dipolar aeromagnetic pattern from magnetically stratified extrusives. For the actual research-grade gravity and aeromagnetic maps of the Puget Lowland, see Anderson, M. L., Blakely, R. J., Wells, R. E., & Dragovich, J. D. (2024). Deep structure of Siletzia in the Puget Lowland: Imaging an obducted plateau and accretionary thrust belt with potential fields. *Tectonics* 43, doi:10.1029/2022TC007720, open access via USGS Pubs Warehouse.
   ```

### Verification for Task 2

For each of F1, F12, F13:

- [ ] The figure file at `assets/figures/F{1,12,13}_*.png` is no longer the Python synthetic. Open it visually and confirm it shows real data (or in F13's fallback case, that the caption is honest about being schematic).
- [ ] The figure title within the image does not say "synthetic mimic" or "real-data version produced by Code Block X in §4 on your machine" any more.
- [ ] The caption in `lectures/26_lithosphere_oceanic_continental.md` correctly attributes the source.
- [ ] The script in `assets/scripts/F{1,12,13}_*.py` either generates the figure from real data (F1, F12) or documents the provenance (F13).
- [ ] `references.bib` has a properly-formatted entry for Seton 2020 (F1), Laske 2013 (F12), and Anderson 2024 (F13). These entries already exist from the original L26 production — verify they are present, otherwise add them. BibTeX templates:

```bibtex
@article{Seton2020,
  author  = {Seton, M. and M{\"u}ller, R. D. and Zahirovic, S. and Williams, S. and Wright, N. M. and Cannon, J. and Whittaker, J. M. and Matthews, K. J. and McGirr, R.},
  title   = {A global dataset of present-day oceanic crustal age and seafloor spreading parameters},
  journal = {Geochemistry, Geophysics, Geosystems},
  volume  = {21},
  year    = {2020},
  doi     = {10.1029/2020GC009214}
}

@misc{Laske2013,
  author  = {Laske, G. and Masters, G. and Ma, Z. and Pasyanos, M.},
  title   = {Update on {CRUST1.0} - A 1-degree Global Model of {E}arth's Crust},
  howpublished = {Geophysical Research Abstracts 15, Abstract EGU2013-2658},
  year    = {2013},
  note    = {Data available at https://igppweb.ucsd.edu/{\textasciitilde}gabi/crust1.html}
}

@article{Anderson2024,
  author  = {Anderson, M. L. and Blakely, R. J. and Wells, R. E. and Dragovich, J. D.},
  title   = {Deep structure of {S}iletzia in the {P}uget {L}owland: Imaging an obducted plateau and accretionary thrust belt with potential fields},
  journal = {Tectonics},
  volume  = {43},
  year    = {2024},
  doi     = {10.1029/2022TC007720},
  note    = {Open access via USGS Publications Warehouse, doi:10.1029/2022TC007720}
}
```

---

## Sanity checks before committing

Run these from the repository root after both tasks are done:

```bash
# 1. No "Beat" anywhere in L26 files
grep -rn -i "beat" lectures/26_lithosphere_oceanic_continental.md \
                   slides/lecture_26_slides.md \
                   instructor_private/L26_*.md 2>/dev/null

# 2. Confirm the three figure files exist and were modified
ls -la assets/figures/F1_seafloor_age_map.png \
       assets/figures/F12_north_america_moho.png \
       assets/figures/F13_siletzia_potential_fields.png

# 3. Confirm the captions cite the real sources
grep -E "Seton et al\. 2020|doi:10.1029/2020GC009214" \
     lectures/26_lithosphere_oceanic_continental.md
grep -E "Laske et al\. 2013|CRUST1.0" \
     lectures/26_lithosphere_oceanic_continental.md
grep -E "Anderson.*2024|doi:10.1029/2022TC007720" \
     lectures/26_lithosphere_oceanic_continental.md

# 4. ESS 314 figure-style invariants (must still hold after retrofit)
grep -n "invert_yaxis" assets/scripts/F*.py | grep -v "NO invert_yaxis\|never invert_yaxis"
# (should be empty — invert_yaxis is forbidden; only allowed in comments warning against it)

grep -n "bbox_inches" assets/scripts/F*.py | grep -v "savefig"
# (should be empty — bbox_inches only allowed inside savefig calls, never in rcParams)
```

If any of these checks fail, fix before committing.

---

## Commit message template

```
L26 retrofit: Beat → Round; F1/F12/F13 use real open-license sources

- Replace "Beat A/B/C" with "Round 1/2/3" throughout §6 (lecture + slides + instructor-private)
- F1 seafloor age map: synthetic mimic → real Müller/Seton 2020 grid via Code Block A
- F12 CRUST1.0 Moho: synthetic mimic → real CRUST1.0 data via Code Block B
- F13 Siletzia: synthetic schematic → Anderson et al. 2024 figure (CC-BY / USGS public domain)
- Update captions with proper data-source attribution and DOIs
- references.bib: verify Seton 2020, Laske 2013, Anderson 2024 entries
```

---

## Notes for the agent

- **"Round" is the recommended substitution.** If Marine prefers "Part" or "Stage" or "Pass" instead, do a global substitution with that term — every find/replace pair in Task 1 follows the same pattern.
- **Do not change anything outside §6 of the lecture or the corresponding slides** except the four caption updates and the two cross-references in §2.2 and §4.2 to "Beat B." All other lecture content stays as-is.
- **Keep the visual identity of each figure stable** — same colormap, same value range, same coastline style, same annotation positions. The goal is to swap synthetic for real, not to redesign.
- **All ESS 314 figure-style rules apply** — Wong colorblind-safe palette, 11 pt minimum fonts, `bbox_inches="tight"` only in `savefig()` (never in rcParams), `fig.tight_layout()` before every `savefig()`, depth axes always `ax.set_ylim(max, 0)` (never `invert_yaxis`).
- **If a data URL is unreachable** (EarthByte server down, CRUST1.0 distribution moved, etc.), document the failure in the figure-script docstring and either find the current canonical URL or fall back to the existing synthetic version with a transparent caption — do not silently substitute another data source.
- **The deployed lecture is at** https://uw-geophysics-edu.github.io/ess314/lectures/26_lithosphere_oceanic_continental.html — useful to diff against the local copy if there are merge conflicts.

End of instructions.
