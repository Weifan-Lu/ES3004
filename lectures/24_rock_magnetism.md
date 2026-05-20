---
title: "Rock Magnetism — How Rocks Remember the Field"
subtitle: "Mineral ordering, remanence, and the tape recorder of plate motion"
short_title: "Rock Magnetism"
week: 9
lecture: 24
date: "2026-06-03"
topic: "Magnetism II — rock magnetism, polarity reversals, and seafloor spreading"
course_lo: ["LO-1", "LO-2", "LO-4"]
learning_outcomes: ["LO-OUT-A", "LO-OUT-B", "LO-OUT-C"]
open_sources:
  - "Lowrie & Fichtner (2020), Fundamentals of Geophysics, 3rd ed., Ch. 5.4–5.6 (UW Libraries e-book)"
  - "Tauxe et al. (2018), Essentials of Paleomagnetism, 5th Web Edition (open access, EarthRef.org)"
  - "Butler (1992), Paleomagnetism: Magnetic Domains to Geologic Terranes (electronic edition freely available)"
  - "Hunt, Moskowitz & Banerjee (1995), Magnetic Properties of Rocks and Minerals, AGU Reference Shelf 3 (Wiley)"
  - "Vine & Matthews (1963), Magnetic anomalies over oceanic ridges, Nature, doi:10.1038/199947a0"
  - "Ogg (2020), Geomagnetic Polarity Time Scale, in Geologic Time Scale 2020 (Elsevier)"
  - "NOAA NCEI Marine Trackline Geophysics archive (public domain, https://www.ncei.noaa.gov/maps/trackline/)"
keywords: [rock magnetism, magnetite, hematite, pyrrhotite, susceptibility, Königsberger ratio, TRM, DRM, CRM, Curie temperature, polarity reversal, Vine-Matthews-Morley, seafloor spreading, Juan de Fuca, Siletzia, apparent polar wander]
---

# Rock Magnetism: How Rocks Remember the Field

:::{seealso}
📊 **Lecture slides** — <a href="https://uw-geophysics-edu.github.io/ess314/slides/lecture_24_slides.html" target="_blank">open in new tab ↗</a>
:::

::::{dropdown} Learning Objectives
:color: primary
:icon: goal
:open:

By the end of this lecture, students will be able to:

- **[LO-24.1]** Identify the five categories of magnetic ordering at the mineral scale (dia-, para-, ferro-, antiferro-, ferri-magnetic), and name the rock-forming minerals that fall in each category.
- **[LO-24.2]** Distinguish between *induced* and *remanent* magnetisation; use the Königsberger ratio $Q$ to predict which regime dominates a given rock in Earth's ambient field; explain why a rock's bulk magnetic response is a volume-weighted average over its mineral assemblage.
- **[LO-24.3]** Describe the three principal mechanisms by which rocks acquire a remanent magnetisation — thermoremanent (TRM), detrital (DRM), and chemical (CRM) — and identify the Curie temperatures of the magnetic minerals encountered in Pacific Northwest rocks (magnetite, titanomagnetite, hematite, pyrrhotite).
- **[LO-24.4]** Read the geomagnetic polarity timescale and explain how the alternation of normal and reversed chrons combined with seafloor spreading produces the symmetric magnetic-anomaly stripes observed across mid-ocean ridges.
- **[LO-24.5]** Estimate a half-spreading rate from the offset of a polarity boundary in a measured Juan de Fuca anomaly profile, and explain why the magnetic record — not gravity or seismics — provided the decisive evidence for plate tectonics.
- **[LO-24.6]** Use paleomagnetic inclination data, combined with the GAD equation from Lecture 23, to infer paleo-latitude for a crustal block, and interpret the apparent polar wander path of Siletzia as evidence for the post-Eocene rotation of the Pacific Northwest.

::::

::::{dropdown} Syllabus Alignment
:color: secondary
:icon: tasklist

| | |
|---|---|
| **Course LOs addressed** | LO-1 (observables ↔ Earth properties), LO-2 (forward model from rock magnetisation to ridge stripe pattern), LO-4 (method strengths and uncertainty, including paleomagnetic averaging) |
| **Learning outcomes practiced** | LO-OUT-A (predict surface signature from a simple source model), LO-OUT-B (apply governing equation to a worked geophysical problem), LO-OUT-C (interpret a measurement as a constraint on subsurface structure with appropriate uncertainty) |
| **Prior lecture** | [L23 — Earth's Magnetic Field and the Geodynamo](23_earth_magnetism.md) |
| **Next lecture** | [L25 — Magnetic Anomalies: Measuring the Crust](25_magnetic_anomalies.md) |
| **Lab connection** | Companion notebook `magnetics_ensemble.ipynb` — forward model of a polarity-reversal stripe sequence; Lab 8 inverts a Juan de Fuca profile for half-spreading rate. |
| **Textbook** | Lowrie & Fichtner (2020), Ch. 5.4–5.6 |

::::

## Prerequisites

This lecture builds directly on Lecture 23, especially section 2 (the three fields $\mathbf{B}$, $\mathbf{H}$, $\mathbf{M}$ and the constitutive relation $\mathbf{B} = \mu_0(1+\chi)\mathbf{H}$) and section 3 (the dipole field and the geocentric axial dipole relation $\tan I = 2\tan\lambda$). Students should be comfortable with the idea that magnetisation $\mathbf{M}$ is a volumetric density of atomic dipole moments, that susceptibility $\chi$ is the linear-response coefficient, and that paleo-latitude can be recovered from a measured inclination with quantified uncertainty. No new electromagnetism is introduced; the lecture works mostly at the atomic and mineralogical scale.

::::{dropdown} Notation reference (this lecture)
:color: info
:icon: book

New symbols introduced in Lecture 24. Symbols inherited from Lecture 23 ($\mathbf{B}$, $\mathbf{H}$, $\mathbf{M}$, $\mu_0$, $\chi$, $F$, $D$, $I$, $\lambda$) carry the same meaning and units — see the L23 notation table.

| Symbol | Name | Units / notes |
|---|---|---|
| $\mathbf{M}_\text{ind}$ | **Induced magnetisation** of a sample in an ambient field: $\mathbf{M}_\text{ind} = \chi\mathbf{H}$ — vanishes when $\mathbf{H}=0$. **(L24, L25)** | A m$^{-1}$ |
| $\mathbf{M}_\text{rem}$ | **Remanent (permanent) magnetisation**; locked in by acquisition history, persists when $\mathbf{H}=0$. **(L24, L25)** | A m$^{-1}$ |
| $\mathbf{H}_\text{earth}$ | Local **ambient (Earth) auxiliary field** acting on a sample or buried body. **(L24, L25)** | A m$^{-1}$ |
| $H_0$ | Magnitude of the ambient field at the moment of remanence acquisition. | A m$^{-1}$ |
| $Q$ | **Königsberger ratio**: $Q = |\mathbf{M}_\text{rem}|/|\mathbf{M}_\text{ind}|$. **(L24, L25)** | dimensionless |
| $M_s$ | **Saturation magnetisation** — high-$H$ plateau of the hysteresis loop. | A m$^{-1}$ |
| $M_r$ | **Remanence** — intercept of the hysteresis loop at $H = 0$. | A m$^{-1}$ |
| $H_c$ | **Coercive field** (coercivity) — intercept of the hysteresis loop at $M = 0$. | A m$^{-1}$ |
| $J_s(T)$ | Spontaneous (temperature-dependent) magnetisation of a ferri/ferromagnetic mineral; $J_s(0)$ is its low-$T$ value, used to normalise the Curie curve. | A m$^{-1}$ |
| $T_C$ | **Curie temperature** — the temperature above which spontaneous order is lost. **(L23–L25)** | °C |
| $v$ | **Half-spreading rate** at a mid-ocean ridge. | mm yr$^{-1}$ $=$ km Myr$^{-1}$ |
| $x_B,\,t_B$ | Distance and age of a polarity boundary from the ridge axis: $x_B = v\,t_B$. | km, Myr |

**A note on $M_s$ vs $J_s(T)$.** Both denote a saturation/spontaneous magnetisation. We keep them distinct following the rock-magnetism literature {cite}`tauxe2018essentials`: $M_s$ is the *isothermal* room-temperature hysteresis-loop value, while $J_s(T)$ is the *temperature-dependent* spontaneous magnetisation that vanishes at $T_C$.

::::

---

## 1. The Geoscientific Question

```{epigraph}
"If the floor of the oceans is spreading apart at mid-ocean ridges and
new sea floor is being formed there, then this new sea floor should be
magnetised in the direction of the Earth's magnetic field at the time
of its formation; and if … the direction of Earth's magnetic field
reverses at intervals … the floor should now consist of strips of
normal and reversed material running parallel to the ridge crest."
— F. J. Vine & D. H. Matthews, *Nature*, **1963**
```

In 1963, two graduate students at Cambridge — Fred Vine and Drummond Matthews — published a three-page note in *Nature* that, more than any other single paper, settled the question of whether the seafloor moves. They proposed that the alternating positive-and-negative magnetic anomalies recorded by ship-towed magnetometers across the mid-ocean ridges of the world could be explained by two simultaneous facts: that the seafloor is *spreading* outward from the ridge crests, and that Earth's magnetic field has repeatedly *reversed* its polarity in the geologic past. Each new strip of basalt crystallising at the ridge would lock in the polarity at the moment of its cooling, building up a striped record of plate motion frozen into the oceanic crust.

The pattern they predicted is shown in {numref}`fig-jdf-real-profile`, plotted from a modern marine magnetic survey across the Juan de Fuca Ridge — the spreading center that lies a few hundred kilometres west of Cape Flattery, generating the Pacific Northwest's offshore plate. The anomaly profile is symmetric about the ridge axis, alternates in sign on a characteristic length scale of about 10–25 km, and (when the half-spreading rate is known independently) directly matches the timing of polarity reversals catalogued from continental lava flows on land.

```{figure} ../assets/figures/fig_jdf_real_profile.png
:name: fig-jdf-real-profile
:alt: Three stacked panels showing a real marine magnetic survey across the Juan de Fuca Ridge. Top panel shows the geomagnetic polarity timescale for the past 5 million years as a horizontal bar divided into black (normal polarity) and white (reversed) chrons, labelled Brunhes, Matuyama, Gauss, and Gilbert. Middle panel plots the total-field magnetic anomaly Delta F in nanoteslas versus distance from the ridge axis in kilometres, from minus 200 to plus 200. The profile is symmetric about the ridge axis (orange vertical line at x = 0) and shows alternating positive and negative lobes with peak amplitudes of plus or minus several hundred nanoteslas. Bottom panel is a schematic cross-section showing a 3-km-deep ocean over a striped magnetised oceanic crust layer, with normal-polarity stripes in dark and reversed-polarity stripes in light. A central orange vertical line marks the ridge axis. Black arrows below the crust point outward indicating spreading.
:width: 100%

A magnetic profile across the Juan de Fuca Ridge, the spreading center of the Pacific Northwest. **(a)** The geomagnetic polarity timescale for the last 5 Myr {cite}`ogg2020gts`. Black = normal polarity, white = reversed. **(b)** Total-field magnetic anomaly $\Delta F$ measured along a ship track perpendicular to the ridge axis; data compiled from the NOAA NCEI Marine Trackline archive (public domain). The profile is *symmetric* about the ridge axis (vertical orange line) — both flanks were generated from the same source at the same time and have spread outward at the same rate. **(c)** Schematic cross-section showing how the polarity at each horizontal position records the field direction at the moment that piece of crust was emplaced; the stripes are read outward from the ridge as time runs backward into the geologic past.
```

<!--
FIGURE BRIEF — fig_jdf_real_profile (Phase 2 build)
  Script: assets/scripts/fig_jdf_real_profile.py
  Data source: NOAA NCEI Marine Trackline Geophysics archive
    https://www.ncei.noaa.gov/maps/trackline/
    Filter: cruises across Juan de Fuca Ridge (lat 44°-48°N, lon 130°-128°W)
    Likely candidates: USGS surveys, R/V Thomas Thompson cruises
    Format: MGD77 ASCII; read with pandas
    Fallback if real data hard to recover: synthesize a profile using the Ogg 2020 GPTS
      and a half-spreading rate of 30 mm/yr with a forward-modelled cosine-stripe response
  Required:
    - Three stacked panels with shared x-axis (-200 to +200 km from ridge axis)
    - Panel (a): GPTS timescale bar, last 5 Myr, with Brunhes / Matuyama / Olduvai / 
      Jaramillo / Gauss / Gilbert chrons labelled
    - Panel (b): magnetic anomaly profile, real data preferred; smooth with low-pass filter
      to ~20 km wavelength so the stripe pattern is visible
    - Panel (c): schematic cross-section (matplotlib patches) showing seafloor, magnetised 
      crust band striped to match panel (a), ridge axis at x=0
    - Colours: GPTS normal = black, reversed = white; anomaly positive = primary blue (#0072B2), 
      negative = vermilion (#D55E00); ridge axis = orange (#E69F00) vertical line
    - mpl.rcParams: base font 13pt; savefig 300dpi
    - ADA: alt text fully describes the three panels independently of colour
-->

The leap from this measured pattern to the Vine–Matthews–Morley interpretation requires understanding what makes a rock capable of "remembering" the field at the moment of its formation. That is the substance of this lecture. Section 2 works through the atomic-scale physics of magnetic ordering, §3 introduces the central distinction between induced and remanent magnetisation, §4 places those mechanisms in the context of real rock assemblages, and §5 unpacks the three principal acquisition mechanisms (TRM, DRM, CRM). Section 6 then introduces the geomagnetic polarity timescale, §7 returns to the ridge stripe pattern as a forward model, and §8 reads paleomagnetic data backward in time to constrain plate motion — culminating, for the Pacific Northwest, in the post-Eocene rotation of Siletzia.

## 2. Magnetic ordering at the mineral scale

The constitutive relation $\mathbf{M} = \chi\mathbf{H}$ from Lecture 23 section 2 is a phenomenological statement: it says that in a linear medium, the magnetisation is proportional to the applied field, but it does not say *why* one mineral has $\chi \sim -10^{-5}$ and another has $\chi \sim +1$. The factor-of-$10^5$ range across natural minerals is set by how the *electron spins* in the crystal lattice align — both with each other and with an external field. The classification has five members, and it determines which minerals fall in the *induced* regime (where the magnetisation is purely a response to $\mathbf{H}$) versus the *remanent* regime (where the mineral can carry a permanent moment that persists even when $\mathbf{H} = 0$).

```{figure} ../assets/figures/fig_mineral_magnetism.png
:name: fig-mineral-mag
:alt: Five side-by-side schematic panels showing crystal-lattice representations of the five magnetic-ordering categories. Each panel has a 5-by-4 grid of lattice sites. In the diamagnetic panel (quartz, halite, k of order minus 10 to the minus 5) the sites are open circles with no arrows, labelled no permanent moments. In the paramagnetic panel (olivine, pyroxene, k of order plus 10 to the minus 4) sites have randomly oriented blue arrows, labelled weak alignment in H. In the ferromagnetic panel (iron, rare in nature, k much greater than 1) all arrows are green and point up, labelled all parallel. In the antiferromagnetic panel (hematite, k approximately zero) rows alternate up green arrows and down orange arrows, labelled antiparallel, net zero. In the ferrimagnetic panel (magnetite, k much greater than 1) rows alternate long up green arrows and short down orange arrows, labelled unequal antiparallel, net not zero.
:width: 100%

The five categories of magnetic ordering at the mineral scale, with a representative mineral and the order-of-magnitude single-mineral susceptibility $\chi$. Diamagnetic and paramagnetic minerals fall in the induced regime (no remanence). Ferromagnetic, antiferromagnetic with spin canting, and ferrimagnetic minerals can fall in the remanent regime (they carry their own magnetisation locked in by history). Adapted from {cite}`tauxe2018essentials`.
```

The five categories are:

1. **Diamagnetic** minerals (quartz, halite, calcite) have no permanent atomic moments. In an applied field they develop a tiny induced moment *opposite* to the field, with susceptibility $\chi \approx -10^{-5}$. They are induced-only and contribute essentially nothing to crustal anomalies. Most of the volume of common sedimentary rocks and felsic plutons is diamagnetic.

2. **Paramagnetic** minerals (olivine, pyroxene, biotite at room temperature) have permanent atomic moments but no spontaneous order: in zero field the moments point in random directions and the net magnetisation is zero. In an applied field the moments preferentially align with it, giving a small positive susceptibility, $\chi \approx +10^{-4}$. Paramagnetic minerals are also induced-only. They dominate the volume of fresh basalt and dolerite, but their contribution to surface anomalies is small compared with the much rarer ferrimagnetic accessory minerals.

3. **Ferromagnetic** minerals have parallel spontaneous alignment of atomic moments via the *exchange interaction*, giving very large susceptibility, $\chi \gg 1$ for the pure mineral. Pure iron is ferromagnetic, but pure iron is exceedingly rare in geology — it occurs only in some meteorites and at the inner core. The everyday "ferromagnetic" mineral in rocks is, strictly, *ferrimagnetic* (see below). Ferromagnets fall in the remanent regime.

4. **Antiferromagnetic** minerals ({numref}`fig-hematite-photo`; hematite, $\alpha$-Fe$_2$O$_3$, in first approximation; ilmenite; goethite) have antiparallel sublattices that cancel: the *first-order* net moment is zero. In hematite a small *spin-canting* in the basal plane produces a weak parasitic remanence that is much smaller than magnetite's but nevertheless non-zero. This weak remanence is what records the field in red beds — see §5.3.

5. **Ferrimagnetic** minerals ({numref}`fig-magnetite-photo`; magnetite, Fe$_3$O$_4$, and the titanomagnetite series) have *unequal* antiparallel sublattices, so the cancellation is partial and a substantial net moment remains. Magnetite is the workhorse of rock magnetism: most natural remanence in basalt, dolerite, and many sediments is carried by magnetite or its titanium-substituted relatives.

```{figure} ../assets/figures/fig_magnetite_specimen.png
:name: fig-magnetite-photo
:alt: Photograph of a magnetite mineral specimen showing a cluster of dark grey to black metallic crystals with octahedral faces, sitting on a contrasting white background. The crystals are roughly 2 to 4 centimetres across and show the characteristic metallic lustre of magnetite.
:width: 60%

Magnetite (Fe$_3$O$_4$) — the canonical strongly magnetic rock-forming mineral and the dominant remanence carrier in basalt, dolerite, and most igneous and sedimentary rocks. The dark, octahedral crystals have $\chi \gg 1$ and a Curie temperature of 580 °C. Photograph: Rob Lavinsky, [iRocks.com](https://www.iRocks.com), via Wikimedia Commons, CC BY-SA 3.0. No changes made.
```

<!--
FIGURE BRIEF — fig_magnetite_specimen (Phase 2 build)
  Type: PHOTOGRAPH — third-party CC BY-SA 3.0
  Source: Wikimedia Commons, File:Magnetite-118736.jpg
    URL: https://commons.wikimedia.org/wiki/File:Magnetite-118736.jpg
    Attribution: Rob Lavinsky / iRocks.com / CC BY-SA 3.0
  Action: download from Commons file page, save as assets/figures/fig_magnetite_specimen.png,
    add attribution file alongside (assets/figures/fig_magnetite_specimen.LICENSE.txt) with
    Commons URL + license + author
  Note: Mixed-license image embedded in CC BY 4.0 work; the photo retains its own CC BY-SA 3.0 
    license, which the caption attributes explicitly.
-->

```{figure} ../assets/figures/fig_hematite_specimen.png
:name: fig-hematite-photo
:alt: Photograph of a hematite mineral specimen showing a cluster of metallic dark grey to silver crystals with a characteristic kidney-shape (botryoidal) habit, on a contrasting background. The specimen is roughly 5 centimetres across.
:width: 60%

Hematite ($\alpha$-Fe$_2$O$_3$) — an antiferromagnetic iron oxide that carries a weak *parasitic* remanence from canted spin sublattices and is the dominant magnetic phase in red bed sandstones and oxidised basalt tops. Curie temperature 680 °C. Photograph: DanielCD, via Wikimedia Commons, CC BY-SA 3.0. No changes made.
```

<!--
FIGURE BRIEF — fig_hematite_specimen (Phase 2 build)
  Type: PHOTOGRAPH — third-party CC BY-SA 3.0
  Source: Wikimedia Commons, File:Hematite.JPG
    URL: https://commons.wikimedia.org/wiki/File:Hematite.JPG
    Attribution: DanielCD / CC BY-SA 3.0
  Action: download from Commons file page; add attribution file
-->

The mapping from ordering category to bulk regime is therefore:

| Ordering          | Single-mineral $\chi$    | Regime                    | Carries remanence?       |
| ----------------- | ------------------------ | ------------------------- | ------------------------ |
| Diamagnetic       | $-10^{-5}$ (negative)    | Induced                   | No                       |
| Paramagnetic      | $+10^{-4}$               | Induced                   | No                       |
| Ferromagnetic     | $\gg 1$                  | Remanent                  | Yes                      |
| Antiferromagnetic | $\approx 0$              | Remanent (weak parasitic) | Yes (weak)               |
| Ferrimagnetic     | $\gg 1$                  | Remanent                  | Yes (strong)             |

This atomic-scale classification will be the recurring thread for the rest of the lecture: which minerals are present in a rock, and which ordering category they fall in, determines both the bulk susceptibility $\chi$ (the induced response) and whether the rock can carry a permanent remanent moment of geological interest.

## 3. Induced versus remanent magnetisation

The single most important conceptual distinction in crustal magnetism is between *induced* and *remanent* magnetisation. Both contribute to a rock's bulk magnetic moment, but they have entirely different physical origins and entirely different consequences for what an anomaly survey actually measures.

In the **induced regime**, the mineral has no intrinsic magnetic moment when isolated from any external field, but in the presence of an applied field $\mathbf{H}$ it develops a magnetisation proportional to that field, governed by the susceptibility relation $\mathbf{M} = \chi\mathbf{H}$ introduced in [Lecture 23 section 2](23_earth_magnetism.md):

```{math}
:label: eq-susc-ind
\mathbf{M}_\text{ind} = \chi \, \mathbf{H}.
```

Diamagnetic minerals have small negative $\chi$ ($\approx -10^{-5}$); paramagnetic minerals have small positive $\chi$ ($\approx +10^{-4}$). The defining feature of the induced regime is that the magnetisation **vanishes when the applied field is removed**. A diamagnetic or paramagnetic mineral has no memory of past fields.

In the **remanent regime**, by contrast, the mineral carries a magnetisation locked in by its history — a *permanent* moment that persists when the applied field is removed. Remanent magnetisation is what makes magnetic minerals into recorders of the ancient field. Ferrimagnetic minerals (magnetite, titanomagnetite) and, to a lesser extent, antiferromagnetic minerals with parasitic moments (hematite) sit in this regime.

{numref}`fig-induced-remanent` shows the two regimes side by side as $M$-versus-$H$ curves. In the induced regime the response is linear and reversible; in the remanent regime the response traces a *hysteresis loop* whose width is set by the rock's coercivity $H_c$ and whose intercept at $H = 0$ is the remanent magnetisation $M_r$.

```{figure} ../assets/figures/fig_induced_vs_remanent.png
:name: fig-induced-remanent
:alt: Two-panel plot of magnetisation M versus applied field H. The left panel, induced-only regime, M equals chi H, vanishes when H equals zero, shows two straight lines crossing at the origin: a grey line with negative slope labelled diamagnetic (quartz, halite, chi less than zero) and a blue line with small positive slope labelled paramagnetic (olivine, biotite, chi greater than zero, small). A black dot marks the origin annotated turn H off, M equals zero for both. The right panel, remanent regime, ferri-slash-ferro magnetic, hysteresis, M not equal to zero at H equals zero, shows a closed hysteresis loop drawn in vermilion: a solid sweep-up branch and a dashed sweep-down branch. Two saturation levels plus and minus M sub s are marked by horizontal dotted lines. A black dot at the intersection of the upper branch with H equals zero is annotated M sub r (remanence) equals 0.72 M sub s; a second black dot at the intersection of the lower branch with M equals zero is annotated H sub c (coercivity) equals 0.25.
:width: 100%

The two regimes of crustal magnetism, shown as magnetisation $M$ versus applied field $H$. **Induced regime (left):** diamagnetic and paramagnetic materials produce a magnetisation linear in $H$ that vanishes at $H = 0$. They have no memory of past fields. **Remanent regime (right):** ferri- and ferromagnetic materials trace a *hysteresis loop*. At $H = 0$ on the upper branch, the magnetisation has a non-zero value $M_r$ — the **remanence**. To return $M$ to zero requires reversing the field to a finite **coercive field** $H_c$. After {cite}`tauxe2018essentials`.
```

The single most useful number for characterising a rock's magnetic behaviour in a field survey is the **Königsberger ratio**:

```{math}
:label: eq-Q
Q = \frac{|\mathbf{M}_\text{rem}|}{|\mathbf{M}_\text{ind}|}.
```

Here $\mathbf{M}_\text{rem}$ is the rock's natural remanent magnetisation (NRM) and $\mathbf{M}_\text{ind}$ is the magnetisation that the rock acquires by induction in Earth's ambient field, $\chi |\mathbf{H}_\text{earth}|$. When $Q \ll 1$ the rock responds primarily by induction, and its magnetic signature points along Earth's *present-day* field. When $Q \gg 1$ the rock's signal is dominated by its remanent moment, which points along the field that prevailed when the rock formed — possibly tens or hundreds of millions of years ago. This second case is what makes oceanic crust into a recorder of plate motion (§7).

::::{admonition} What $Q$ means for a magnetic survey
:class: tip

Two anomalies of identical surface amplitude can have very different *origins*:

- A $+800$ nT anomaly above a granite ($Q \approx 0.3$) is mostly *induced* — its direction tracks the present-day field, and the body underneath would lose nearly all its anomaly if you could lift it into a zero-field environment.
- A $+800$ nT anomaly above an old oceanic basalt ($Q \approx 6$) is mostly *remanent* — its direction was set at the time of cooling, possibly tens of millions of years ago, and would persist if the body were removed from Earth's field.

For survey design this matters because the *direction* of the anomaly affects its surface shape (Lecture 25, §4 — inclination asymmetry). A high-$Q$ source carries a vector that may not point along the present-day field, and the resulting anomaly can be displaced or inverted relative to what an induced-only model would predict. Field-acquired oriented rock samples — measured in the lab to extract $Q$ and the direction of $\mathbf{M}_\text{rem}$ — are the standard way to discriminate the two cases.

::::

## 4. A rock is an ensemble of minerals

No single mineral makes up an entire rock. Even a "magnetite-rich" basalt is mostly plagioclase, clinopyroxene, and olivine, with magnetite present as a few volume percent of the total. The bulk magnetic response of a rock is therefore a **volume-weighted average** over its mineral assemblage: each mineral contributes according to its volume fraction and its own magnetic character.

{numref}`fig-rock-ensemble` shows four common rock types as schematic hand-sample views, each with its dominant magnetic carrier, its typical bulk volume susceptibility $\chi$, its Königsberger ratio $Q$, and where the rock is encountered in Pacific Northwest geology.

```{figure} ../assets/figures/fig_rock_as_ensemble.png
:name: fig-rock-ensemble
:alt: Four side-by-side schematic hand-sample panels showing the mineral makeup of four common rock types. The basalt panel is dominated by grey-blue plagioclase ellipses and dark clinopyroxene, with blue olivine polygons and scattered bright orange dots representing magnetite grains; labelled bulk susceptibility chi approximately 10 to the minus 3 to 10 to the minus 1 SI and Königsberger ratio Q approximately 0.5 to 10. The granite panel is dominated by light tan K-feldspar and off-white plagioclase ellipses with grey quartz polygons and a few blue biotite polygons and trace orange magnetite dots; labelled chi approximately 10 to the minus 5 to 10 to the minus 3 SI and Q approximately 0.1 to 1. The red bed sandstone panel is dominated by tan hematite-coated quartz with orange iron-oxide cement and dark red hematite dots; labelled chi approximately 10 to the minus 5 to 10 to the minus 4 SI and Q approximately 1 to 100. The marine mudstone panel is dominated by dark grey clay matrix with smaller blue paramagnetic grains and small orange detrital magnetite dots; labelled chi approximately 10 to the minus 5 to 10 to the minus 3 SI and Q approximately 0.1 to 2.
:width: 100%

Four common rock types shown as ensembles of minerals. **Basalt** — mafic, magnetite-rich — has high bulk susceptibility and a Königsberger ratio of order unity to ten, dominated by the ferrimagnetic minerals magnetite and titanomagnetite (the Juan de Fuca seafloor and the Columbia River Basalt Group are PNW examples). **Granite** — felsic, with only trace magnetite — has much lower susceptibility, dominated by induced rather than remanent magnetisation (Cascade arc plutons, Idaho Batholith). **Red bed sandstone** — characterised by hematite cement and grain coatings — has low overall susceptibility but a high Königsberger ratio, because the hematite carries a strong *chemical* remanence (Triassic red beds, arid-margin Cordilleran sediments). **Marine mudstone** — a fine-grained clay matrix with disseminated detrital magnetite — has variable susceptibility and weak-to-moderate remanence (Olympic Peninsula accretionary wedge sediments). Susceptibility ranges from {cite}`hunt1995magprops`.
```

::::{admonition} Pacific Northwest mineral inventory
:class: note

The minerals carrying the great majority of the remanent signal in Pacific Northwest rocks are:

- **Magnetite and titanomagnetite (TM60, TM30, …)** — in basalts of the Juan de Fuca plate, the Columbia River Basalt Group, and arc volcanics of the Cascade Range. The dominant remanence carrier in almost every igneous rock in the region.
- **Hematite** — in Mesozoic red bed sandstones, in oxidised tops of basalt flows (the "weathered horizon" between successive Columbia River flows), and in some metamorphic rocks.
- **Pyrrhotite** ({numref}`fig-pyrrhotite-photo`) — in some Cascade hydrothermal ore deposits and in metamorphosed sedimentary horizons.
- **Detrital magnetite** — disseminated through the marine sediments of the Cascadia accretionary wedge (Olympic Peninsula) and through Puget Sound glaciolacustrine deposits.

Granitic plutons of the Cascade arc and Idaho Batholith carry only trace magnetite and contribute primarily through *induced* magnetisation. This is why the geophysical contrast between a magnetite-bearing intrusion and its surrounding granite host is often visible as a positive magnetic anomaly at the surface, even when the gravity contrast is small.

```{figure} ../assets/figures/fig_pyrrhotite_specimen.png
:name: fig-pyrrhotite-photo
:alt: Photograph of a pyrrhotite mineral specimen showing a cluster of brassy bronze to copper-coloured tabular crystals on a host rock matrix, roughly 5 centimetres across.
:width: 50%

Pyrrhotite (Fe$_{1-x}$S) — a magnetic iron sulfide that contributes to the remanent signal in some Cascade hydrothermal ore deposits and metasediments. Curie temperature 320 °C. Photograph: Rob Lavinsky, [iRocks.com](https://www.iRocks.com), via Wikimedia Commons, CC BY-SA 3.0. No changes made.
```

<!--
FIGURE BRIEF — fig_pyrrhotite_specimen (Phase 2 build)
  Type: PHOTOGRAPH — third-party CC BY-SA 3.0
  Source: Wikimedia Commons, File:Apatite-Dolomite-Pyrrhotite-63971.jpg
    URL: https://commons.wikimedia.org/wiki/File:Apatite-Dolomite-Pyrrhotite-63971.jpg
    Attribution: Rob Lavinsky / iRocks.com / CC BY-SA 3.0
  Action: download from Commons file page; add attribution file
-->

::::

## 5. The three remanence-acquisition mechanisms

The lithospheric signal — the part of the surface field that carries geophysical information about subsurface structure — exists because a subset of crustal minerals carries a permanent magnetisation. Section 2 established *which* minerals (ferri-, ferro-, and weakly antiferromagnetic ones), and §3 distinguished the induced from the remanent regime in principle. This section turns to the *mechanism* by which those minerals acquire their remanence in the first place.

A magnetic mineral can be locked into a particular magnetisation direction by any process that brings the mineral through a critical condition under which its electron spins lose the freedom to fluctuate. There are three such processes, each tied to a distinct geological setting, and together they form the three pillars of paleomagnetism.

### 5.1 Thermoremanent magnetisation (TRM) — cooling through the Curie temperature

The simplest, strongest, and best-understood remanence is **thermoremanent magnetisation (TRM)**, acquired when a magnetic mineral *cools* through a critical temperature in an ambient field.

Ferri- and ferromagnetic ordering depends on the exchange interaction between neighbouring atomic moments. Above a critical temperature — the **Curie temperature** $T_C$ — thermal agitation overwhelms the exchange coupling, the spontaneous alignment is destroyed, and the mineral becomes paramagnetic. Below $T_C$, ordering returns: as the grain cools further, the spins lock progressively into an alignment with the prevailing ambient field. This progressive locking happens in a narrow **blocking interval** just below $T_C$, where the *relaxation time* of the grain crosses the experimental timescale and what was a fluctuating moment becomes a permanent one.

The four magnetic minerals most relevant in Pacific Northwest rocks have well-separated Curie temperatures:

| Mineral | $T_C$ (°C) | Where it occurs |
|---|---|---|
| Titanomagnetite (TM60) | 150 | Basalts of the Juan de Fuca plate |
| Pyrrhotite | 320 | Hydrothermal ore deposits; metasediments |
| Magnetite (Fe$_3$O$_4$) | 580 | Most continental igneous rocks |
| Hematite ($\alpha$-Fe$_2$O$_3$) | 680 | Red beds; oxidised basalt tops |

This spread of Curie temperatures is exploited in laboratory **stepwise thermal demagnetisation**: heating a rock sample to progressively higher temperatures and measuring the surviving moment at each step removes the carriers in order, separating multiple components of remanence by the temperature at which each unblocks.

{numref}`fig-trm-curie` shows the temperature dependence of a single magnetite grain's magnetisation and the cumulative TRM it acquires during slow cooling in a field. The plot is drawn with the temperature axis *reversed* so that the physical process of cooling reads from left to right, matching the natural narrative.

::::{admonition} What does "normalised magnetisation" mean?
:class: tip

Both curves in {numref}`fig-trm-curie` plot magnetisation *divided by* the low-temperature saturation value $J_s(0)$. This division — the *normalisation* — has two purposes. First, the absolute magnetic moment of a grain depends on its volume and composition, which are not universal; normalising by $J_s(0)$ makes the y-axis run from 0 to 1 for every ferri- or ferromagnetic mineral, regardless of grain size or absolute moment. Second, it isolates the *temperature dependence* of the magnetisation from its absolute amplitude: the curve $J_s(T)/J_s(0)$ is a property of the *mineral*, not of the *sample*. Different minerals can therefore be compared on a common axis without worrying about which one has the bigger absolute moment.

::::

```{figure} ../assets/figures/fig_trm_curie.png
:name: fig-trm-curie
:alt: Plot of normalised magnetisation versus temperature in degrees Celsius. The x-axis is reversed so that temperature decreases from left (about 720 degrees C) to right (zero degrees C), with a thick black arrow at the top labelled cooling pointing rightward. The y-axis is normalised magnetisation J divided by J sub s at zero kelvin, dimensionless, running from zero to about 1.2. A solid blue curve labelled J sub s of T divided by J sub s of zero, spontaneous magnetisation of magnetite, rises from zero at T equals 580 degrees C up to a value of 1 as T approaches zero on the right. A dashed orange curve labelled cumulative TRM acquired during cooling in H sub zero stays at zero from high temperature down through 580 degrees C, rises steeply through an orange-shaded blocking interval between about 565 and 515 degrees C, and plateaus at 1 for lower temperatures. A blue dotted vertical line at 580 degrees C marks T sub C equals 580 degrees C, magnetite. A grey annotation box near the top lists Curie temperatures of PNW magnetic minerals: TM60 at 150, pyrrhotite at 320, hematite at 680 degrees C.
:width: 100%

Acquisition of thermoremanent magnetisation by a magnetite grain cooling through its Curie temperature in an ambient field $H_0$. The temperature axis is reversed so that **cooling reads left to right**. The solid blue curve is the spontaneous magnetisation $J_s(T)/J_s(0)$; it rises from zero at $T_C = 580$ °C to its full saturation value as the grain cools toward room temperature. The dashed orange curve is the *cumulative* TRM acquired during cooling: zero above $T_C$, then locked in across the narrow blocking interval (shaded orange) just below $T_C$, and plateauing at its low-temperature value thereafter. Dotted vertical lines mark the Curie temperatures of the other PNW-relevant magnetic minerals (TM60, pyrrhotite, hematite). Adapted from {cite}`dunlop2001rockmagnetism` and {cite}`tauxe2018essentials`.
```

TRM is the dominant mechanism by which **igneous rocks** record the field at the time of their last cooling. A basalt flow erupted at 1 200 °C cools through magnetite's Curie temperature in days to weeks, locking in a magnetisation parallel to whatever the geomagnetic field direction is at the eruption site at the moment of cooling ({numref}`fig-pillow-basalt`). The TRM in oceanic basalts of the Juan de Fuca plate is what produces the famous magnetic-anomaly stripes of §7.

```{figure} ../assets/figures/fig_pillow_basalt.png
:name: fig-pillow-basalt
:alt: Photograph of pillow basalt outcrop showing rounded, pillow-shaped lobes of dark grey to black volcanic rock, each pillow approximately 30 to 80 centimetres across, with characteristic glassy rinds and radial cooling cracks. The lobes are stacked together in a complex three-dimensional arrangement.
:width: 75%

Pillow basalt — submarine volcanic rock formed when lava erupts underwater and cools rapidly, producing rounded "pillow" lobes. Pillow basalt is the principal lithology of the upper oceanic crust, including the basalts of the Juan de Fuca plate offshore the Pacific Northwest. As the lava cools through magnetite's Curie temperature (580 °C) within hours to days, it locks in a thermoremanent magnetisation parallel to the ambient geomagnetic field — the physical mechanism that records the polarity timescale into the seafloor. Photograph: see attribution file. License per Wikimedia Commons file page.
```

<!--
FIGURE BRIEF — fig_pillow_basalt (Phase 2 build)
  Type: PHOTOGRAPH — third-party
  Source: Wikimedia Commons, Category:Pillow basalts
    URL: https://commons.wikimedia.org/wiki/Category:Pillow_basalts
    Action: verify per-file license before download; preferred candidates:
      - Point Bonita Franciscan Complex pillow basalts (James St. John, CC BY 2.0)
      - Metamorphosed Ely Greenstone pillow basalt (James St. John, CC BY 2.0)
    Save file to assets/figures/fig_pillow_basalt.png
    Add attribution file alongside (assets/figures/fig_pillow_basalt.LICENSE.txt) with
      Commons URL + license + author + "No changes made" statement
-->

### 5.2 Detrital remanent magnetisation (DRM) — sediment grains aligning

In environments where rocks form by sedimentation rather than by cooling, a different mechanism is at work. Ferrimagnetic grains (magnetite, in particular) eroded from older source rocks are transported and deposited along with the rest of the sedimentary load. As each grain settles through the water column, it experiences a torque from the ambient field that tends to rotate it into alignment with the field direction — a small magnetic compass in suspension. When the grain comes to rest at the sediment-water interface, that alignment is preserved as long as the grain is not subsequently re-oriented by bioturbation, current shear, or compaction ({numref}`fig-drm-acquisition`).

```{figure} ../assets/figures/fig_drm_acquisition.png
:name: fig-drm-acquisition
:alt: Schematic cross-section showing the acquisition of detrital remanent magnetisation. A water column at the top is populated with small magnetic grains shown as rod shapes. Above the grains, an arrow labelled H zero points to the right indicating the ambient geomagnetic field direction. As grains settle downward through the water column, they rotate to align their long axes parallel to H zero. At the sediment-water interface, the aligned grains accumulate into a sediment layer where they are locked in place. Below the surface, the sediment shows aligned grains preserving the field direction at the time of deposition. A second deeper layer shows older sediment with grains aligned in a different direction, indicating an earlier geomagnetic field state.
:width: 90%

Acquisition of detrital remanent magnetisation (DRM). Ferrimagnetic grains settling through the water column experience a magnetic torque that aligns their long axes with the ambient field $H_0$. At the sediment-water interface, the alignment is preserved — provided the grains are not later disturbed by bioturbation, current shear, or compaction. The bulk sediment carries a weak but statistically robust moment pointing along the field direction at the time of deposition. Older sediment at depth records earlier states of the field. After {cite}`tauxe2018essentials`.
```

<!--
FIGURE BRIEF — fig_drm_acquisition (Phase 2 build)
  Script: assets/scripts/fig_drm_acquisition.py
  Type: Python schematic (matplotlib only)
  Required:
    - Cross-section: water column (light blue) above sediment column (tan to brown gradient)
    - Field arrow H_0 at top right, horizontal
    - Several magnetic grains (small rectangles) in water column, randomly oriented
    - Same grains settling downward, progressively rotating to align with H_0
    - At sediment-water interface: aligned grains preserved
    - Below: two sediment intervals with different grain alignments to indicate older fields
    - Colours: water sky blue (#56B4E9), sediment tan/brown, grains in primary blue (#0072B2)
      with vermilion ends (#D55E00) to encode dipole direction
-->

The result is a **detrital remanent magnetisation (DRM)**: the bulk sediment carries a weak, statistically averaged moment pointing along the ambient field. DRM is the dominant remanence carrier in **marine and lacustrine sediments**. The signal is much weaker than TRM in a volcanic — a typical DRM intensity is $10^{-4}$ to $10^{-3}$ of the TRM in a basalt — and considerably noisier, because individual grain alignments are partial, and because compaction and bioturbation introduce systematic deviations (notably the *inclination shallowing* correction needed when paleo-latitudes are computed from sediment records).

DRM is, however, the only mechanism available to record the field during most of the open-ocean sedimentary record. The high-resolution record of geomagnetic reversals through the Cenozoic is built almost entirely from deep-sea sediment DRM, recovered by ocean-drilling cores. For Pacific Northwest geology, the analogue is the marine sedimentary sequence of the Cascadia accretionary wedge, which records both the inclination of the Pleistocene–Holocene field and the rotation history of the accreted blocks themselves.

### 5.3 Chemical remanent magnetisation (CRM) — minerals growing in place

The third mechanism is **chemical remanent magnetisation (CRM)**: acquired not by cooling a pre-existing grain, nor by aligning a settling grain, but by *growing* a new magnetic mineral in the ambient field at a temperature below its Curie point. A common example is the growth of fine-grained hematite during diagenesis of a red bed sandstone: an originally non-magnetic iron-bearing precursor oxidises to hematite, and the hematite grain locks in a remanence the instant it crosses a critical size threshold (above which its relaxation time exceeds the geological timescale).

CRM is the dominant mechanism in **red beds** and in **oxidised horizons** at the tops of basalt flows (where late hydrothermal alteration replaces the primary magnetite with hematite). It is also relevant in some metamorphic rocks where new magnetic minerals crystallise during prograde or retrograde reactions.

CRM is interpretively trickier than TRM or DRM, because the *age* of the remanence is the age of mineral growth, not the age of the host rock. A Triassic red bed whose hematite grew during Jurassic diagenesis records a Jurassic, not a Triassic, field. Separating CRM from any earlier TRM in the same sample is one of the routine demagnetisation tasks of a paleomagnetic laboratory.

### 5.4 Other remanences — a brief inventory

For completeness, two other remanences are worth naming, although neither plays a leading role in interpreting the lithospheric anomaly:

- **Isothermal remanent magnetisation (IRM)** — acquired when a rock is exposed to a strong field (such as a lightning strike) at room temperature. IRM is the standard form of *artificial* remanence imposed in the laboratory for rock-magnetic characterisation. In nature, lightning-induced IRM is a common nuisance overprint at mountaintop and exposed-ridge sites.
- **Viscous remanent magnetisation (VRM)** — acquired slowly over long times in a weak ambient field; physically, the long-time tail of the distribution of grain relaxation times. VRM tends to align with the *present-day* field and is the first component removed by routine demagnetisation.

Together with TRM, DRM, and CRM, these mechanisms make rocks into recorders of the magnetic field across the full range of geological processes — cooling, deposition, mineral growth, and lightning.

## 6. The geomagnetic polarity timescale

Earth's magnetic field has not always pointed the same way. Over the past 5 Myr — the interval most relevant for plate-tectonic reconstruction at modern spreading rates — the field has reversed its polarity dozens of times, switching the north and south magnetic poles on timescales of a few hundred thousand years to a few million years between reversals. The reversed and normal intervals are called **chrons** (formerly *epochs*); shorter excursions embedded in a chron are **subchrons** (formerly *events*).

Polarity reversals were first recognised in the early 20th century from sequences of continental lava flows in which successive flows carry opposite TRM directions. The *geomagnetic polarity timescale* (GPTS) is a compilation of dated polarity boundaries built from radiometric ages of continental volcanic units and, since the 1970s, from magnetostratigraphy of deep-sea sediment cores ({numref}`fig-gpts`). The GPTS for the last 5 Myr has four named chrons: the **Brunhes** (normal, 0 – 0.78 Ma), **Matuyama** (reversed, 0.78 – 2.58 Ma, with the **Olduvai** and **Jaramillo** normal subchrons embedded), **Gauss** (normal, 2.58 – 3.60 Ma), and **Gilbert** (reversed, 3.60 – 5.33 Ma).

```{figure} ../assets/figures/fig_gpts.png
:name: fig-gpts
:alt: Plot of the geomagnetic polarity timescale for the past 10 million years. The horizontal axis is age in millions of years from 0 on the left to 10 on the right. A horizontal bar spans the axis, divided into alternating black (normal polarity) and white (reversed polarity) segments. The named chrons are labelled along the top: Brunhes 0 to 0.78, Matuyama 0.78 to 2.58 with Olduvai 1.78 to 1.95 and Jaramillo 1.07 to 0.99 normal subchrons highlighted, Gauss 2.58 to 3.60, Gilbert 3.60 to 5.33. Older chrons are numbered C3A, C4, C4A, C5 following Cande and Kent.
:width: 100%

The geomagnetic polarity timescale for the past 10 Myr {cite}`ogg2020gts`. Black intervals represent times of *normal* polarity (the field pointed the same way as today), white intervals represent *reversed* polarity (the field pointed the opposite way). The named chrons of the past 5 Myr — Brunhes, Matuyama, Gauss, Gilbert — were defined from continental lava flow sequences; older intervals are numbered following the convention of {cite}`candekent1995gpts`. The pattern is *globally synchronous*: a reversal happens everywhere on Earth at once, on a timescale of a few thousand years. This makes the GPTS into an independent clock that any TRM-bearing rock sequence can be matched against.
```

<!--
FIGURE BRIEF — fig_gpts (Phase 2 build)
  Script: assets/scripts/fig_gpts.py
  Data source: Geomagnetic Polarity Time Scale 2020 (Ogg, Elsevier compilation)
    Reference: Ogg (2020), in Geologic Time Scale 2020, Elsevier, Ch. 5
    For open numerical values: ICS standard chron boundaries (https://stratigraphy.org/)
  Required:
    - Horizontal bar 0-10 Ma, divided into alternating black (normal) and white (reversed) blocks
    - Chron name labels above bar; subchron labels in italics
    - Tick marks every 1 Myr; minor ticks every 0.5 Myr
    - Width 10 inches by 1.5 inches tall (compact ribbon)
    - mpl.rcParams: base font 13pt; savefig 300dpi
-->

The GPTS has two properties that make it geophysically powerful:

- **It is globally synchronous.** A polarity reversal happens *everywhere* on Earth at once, on a timescale of perhaps 1 000–10 000 years. A normal-polarity TRM acquired in a New Zealand basalt at 1.5 Ma should match a normal-polarity TRM acquired in an Iceland basalt at 1.5 Ma. The GPTS is therefore a *stratigraphic clock* with global reach.
- **It is independently calibrated.** The chron ages of the past 5 Myr are pinned by K-Ar and Ar-Ar radiometric dates on continental lava flows. The GPTS is *not* circularly defined by the seafloor anomaly pattern; it is established by radiometric geochronology and then used to read the seafloor.

This is the property that gives the next two sections their analytical leverage.

## 7. The forward problem — magnetic stripes from spreading + reversals

The Juan de Fuca Ridge sits offshore between Vancouver Island and northern California, generating new oceanic crust at a half-rate of approximately 30 mm/yr. As each new strip of basalt crystallises and cools through magnetite's Curie temperature, it acquires a TRM parallel to the polarity of Earth's field *at that moment* (§5.1). Sequential polarity reversals from the GPTS (§6) imprint a striped pattern of crustal magnetisation that is preserved indefinitely once the rock cools below the blocking interval.

A ship-towed total-field magnetometer crossing the ridge perpendicular to its axis measures the integrated anomaly produced by the entire striped crustal column within its footprint. Each polarity boundary in the seafloor corresponds to an inflection in the surface anomaly profile; each chron corresponds to a band of constant magnetisation between two such inflections. The result is the symmetric striped pattern of {numref}`fig-jdf-real-profile` from §1.

The geometry of the stripes is simple. The half-rate $v$ relates the distance of a polarity boundary from the ridge axis $x_B$ to its age $t_B$ in the GPTS:

```{math}
:label: eq-half-rate
x_B = v \cdot t_B.
```

For the Juan de Fuca Ridge with $v = 30$ mm/yr $= 30$ km/Myr, the Brunhes/Matuyama boundary ($t_B = 0.78$ Ma) sits at $x_B = 23.4$ km from the ridge axis. The Matuyama/Gauss boundary at 2.58 Ma sits at 77 km. Across the JdF system, $x_B$ is observed in the range 20–25 km for the Brunhes/Matuyama boundary depending on the segment, consistent with half-rates of 25–32 mm/yr.

::::{admonition} Why magnetics — not gravity, not seismics — proved seafloor spreading
:class: tip

Mid-ocean ridges have gravity anomalies (mass deficit above the hot rising mantle) and seismic-velocity anomalies (slower mantle and crust beneath the ridge), but *neither encodes time*. The gravity signal is the same shape if the spreading rate is 1 mm/yr or 100 mm/yr; the seismic signal is similarly rate-independent in the first-order picture.

Magnetic stripes encode time because the GPTS provides an *independent clock*, calibrated from continental volcanics (§6). A property that is non-unique in one observable becomes diagnostic when combined with an independent constraint. This is the prototype for the modern practice of *joint inversion*: combine multiple geophysical observables — gravity, seismic, magnetic, EM, geochemical — each non-unique on its own, into an integrated picture that is more constraining than the sum of its parts.

By 1968 the magnetic-stripe correlation had been measured on every major spreading ridge on Earth. The seafloor-spreading hypothesis was no longer hypothesis.

::::

## 8. The inverse problem — paleomagnetism and Siletzia

The forward problem of §7 takes a known spreading rate and a known GPTS and predicts an anomaly profile. The *inverse* problem of paleomagnetism takes a measured remanence direction in an oriented rock sample and recovers the position of the sampling site at the time the remanence was acquired. Two pieces of information are extracted:

- The **inclination** of the remanence vector gives the paleo-latitude via the GAD equation $\tan I = 2\tan\lambda$ from Lecture 23 section 3.
- The **declination** of the remanence vector — its angle east of true north as preserved in the present-day orientation of the sample — gives the *rotation* of the sampling block about a vertical axis since the time of remanence acquisition.

A rock that has not moved since it acquired its remanence carries a remanence direction matching the present-day field. A rock that has *rotated* about a vertical axis carries the same inclination but a deflected declination — and the deflection magnitude is a direct readout of the rotation angle.

::::{admonition} Siletzia — the Pacific Northwest's rotating basement
:class: note

The basement of the western Pacific Northwest, from southern Vancouver Island through the Olympic Peninsula and the Coast Range of Oregon, is the **Siletzia terrane** — a thick sequence of Eocene basalts (∼56–49 Ma) that erupted offshore and was subsequently accreted to North America. Paleomagnetic studies of these basalts have measured the remanence inclination *and* declination at dozens of sites:

- **Inclinations** match the GAD prediction for the latitude at which the basalts were erupted, after accounting for the post-Eocene northward motion of North America. The basalts formed near their present-day latitude, give or take a few hundred kilometres.
- **Declinations**, by contrast, are systematically *deflected* — by amounts that grow from ~10° in the northernmost Siletzia outcrops to as much as ~70° in the southernmost ones. The signal is too systematic to be sample noise: the Siletzia block has rotated *clockwise* about a vertical axis since its accretion, with the southern part of the block rotating more than the northern part.

The result is a regional fan-shaped rotation — Siletzia is hinged near Vancouver Island and has swept clockwise across the Pacific Northwest forearc over the past 50 Myr at an average rate of order $1°$ per million years. The same rotation is independently visible in the *orientation* of dyke swarms and fault systems within Siletzia; it is part of the regional kinematics that distinguishes the Pacific Northwest from the rest of the North American Cordillera.

This is paleomagnetism doing what no other geophysical method can do: recovering an *absolute* rotation history of a crustal block from the rock itself. Combined with gravity (Lecture 22 — the density structure of Siletzia and its bounding faults) and seismic imaging (Lecture 12 — Cascadia tomography), the paleomagnetic data give a kinematically and structurally consistent model of how the Pacific Northwest forearc got to where it is today.

::::

## 9. Research horizon — magnetostratigraphy and deep time

The GPTS of {numref}`fig-gpts` extends back about 170 Myr, anchored at the young end by radiometric dates on Cenozoic volcanics and at the old end by the magnetic stripes of the Jurassic Pacific. Pushing the GPTS further back in time, and into ever-shorter chrons, is an active research enterprise.

Three current frontiers:

1. **Sub-orbital reversal records.** High-resolution magnetostratigraphy of deep-sea drill cores resolves the *transition* across a polarity reversal at decadal-to-millennial resolution. The Matuyama-Brunhes reversal at 0.78 Ma is the type example: the field underwent multiple "fits and starts" — partial inclination excursions, intermediate directions, complex field morphologies — over a few thousand years before settling into the stable normal polarity that has persisted to today. Whether the *next* reversal is currently beginning is an open question; the steadily declining dipole moment over the last 2 000 years is suggestive but inconclusive.
2. **Precambrian paleomagnetism.** Reliable remanence directions from Archean and Paleoproterozoic rocks constrain the existence and strength of the early geodynamo. Recent work has pushed clean paleomagnetic records past 4 Ga, into the Hadean — implying that a self-sustaining dynamo and a planetary magnetic shield have been present for nearly the entire history of Earth.
3. **Mars and Moon paleomagnetism.** Crustal remanence measured by the Mars Global Surveyor and InSight missions reveals that Mars *did* have an active dynamo until about 3.7 Ga, locking strong remanence into the southern highlands. Lunar samples returned by Apollo and analysed in Earth labs over the past five decades have documented a Moon dynamo that operated from ~4.2 Ga to ~1.0 Ga before shutting down. Both records inform comparative planetology of dynamo lifetimes and the long-term habitability of rocky planets.

## 10. AI literacy — the polarity-reading trap

A common LLM failure mode in paleomagnetism is the *polarity-reading trap*. Asked to interpret a measured remanence direction from a rock sample, an LLM will often default to assuming present-day field polarity — and will translate a measured *reversed* polarity into a 180° error in inferred paleo-latitude or paleo-orientation. The error is not in the algebra; it is in the assumption that the sample carries a normal-polarity TRM when in fact it carries a reversed-polarity TRM that was acquired during a Matuyama-chron eruption.

::::{admonition} Reasoning Partner activity
:class: tip

**Step 1 — Hand the LLM a paleomagnetic data point.** Prompt: *"A basalt sample from the Columbia River Basalt Group near Vantage, WA, has been dated at 15.5 Ma and carries a stable remanence with declination 195° and inclination $-65°$. Compute the paleo-latitude and the rotation of the sampling block since 15.5 Ma. Assume the geocentric axial dipole approximation."*

**Step 2 — Check what the LLM does with the negative inclination.** Two interpretations are physically possible:

1. The sample carries a *normal*-polarity TRM, the block has rotated 180° about a vertical axis (declination flipped), and the sampling site has moved into the *southern* hemisphere — which it has not.
2. The sample carries a *reversed*-polarity TRM acquired during a reversed chron of the GPTS (the C5Br chron is in fact a reversed-polarity interval at 15.5 Ma), so the rock points to *reversed* north. To recover the paleo-orientation of the *site*, the polarity must be flipped: inclination $+65°$, declination $15°$. This corresponds to a northern-hemisphere paleo-latitude of ∼47° and a modest rotation of $15°$ clockwise, both consistent with the in-situ Columbia River setting.

**Step 3 — Disagree productively.** If the LLM gives the geographically nonsensical answer (1), reply with a prompt that names the GPTS chron at 15.5 Ma and asks how that affects the interpretation. Do *not* simply say "you're wrong" — that elicits agreement without correcting the model's reasoning. Effective prompts name the *physical fact* the model overlooked.

The student deliverable is a one-page record showing: (i) the LLM's first answer; (ii) the GPTS chron at 15.5 Ma and the polarity that should be used; (iii) the corrected paleo-latitude and rotation, in the student's own working.

::::

## 11. Concept check

::::{admonition} Concept-check questions
:class: note

1. **Curie temperature and lava flow age.** A basalt sample carries a stable remanence whose direction is consistent across the entire flow thickness. The flow is known to have erupted at 1 200 °C and cooled over a few weeks. Which mineral or minerals could be carrying the remanence? Could any of magnetite, titanomagnetite TM60, hematite, or pyrrhotite be ruled out solely from the cooling history?

2. **Induced or remanent?** A surveyor measures a $+800$ nT magnetic anomaly above a granitic pluton ($Q \approx 0.3$) and a $+800$ nT anomaly above a basalt flow ($Q \approx 6$). She then collects oriented samples from each, demagnetises them in zero field, and re-measures. Which anomaly will mostly disappear in the lab, and which will mostly persist? Explain.

3. **Spreading rate from a stripe sequence.** A ship track across the East Pacific Rise records a Brunhes/Matuyama polarity boundary at $x = \pm 31$ km from the ridge axis. Using the GPTS, compute the half-spreading rate. The Matuyama/Gauss boundary on the same track sits at $x = \pm 104$ km. Is the spreading rate uniform over the past 2.58 Myr? Quantify any difference.

4. **Reading Siletzia.** A site in the southern Coast Range of Oregon yields an Eocene (50 Ma) basalt with measured paleomagnetic declination $D = 60°$ east of north and inclination $I = +63°$. Assume a GAD field with no plate motion since 50 Ma. (a) Compute the paleo-latitude. (b) Compute the rotation of the sampling block since 50 Ma. (c) Comment on whether your numbers are consistent with the Siletzia rotation story (§8).

::::

::::{admonition} Concept-check answers
:class: dropdown

*Answers and worked solutions are provided in the instructor materials (see `concept_check_lecture24.md` in the `ess314-instructor` repository).*

::::

## 12. Looking ahead

Lectures 23 and 24 have built the magnetic toolkit: the dipole field at the surface (L23 section 3), the constitutive relation between $\mathbf{B}$, $\mathbf{H}$, $\mathbf{M}$, and $\chi$ (L23 section 2), and the mechanisms by which crustal rocks carry both induced and remanent magnetisation (L24 section 3, section 5). Lecture 25 puts these into practice. A buried magnetised body — characterised by its volume, its bulk magnetisation $\mathbf{M}$ (induced + remanent), and its depth — produces a small but measurable anomaly at the surface. Mapping that anomaly, removing the core (IGRF) and external (diurnal) components, and inverting the residual for source geometry is the practical work of *magnetic surveying*. The same machinery is used to map mineral deposits, image active fault zones (the Seattle Fault is one PNW example), locate unexploded ordnance, and produce the global lithospheric anomaly maps that begin Lecture 25.

## 13. Further reading

Open-access references are preferred; paywalled works are cited for completeness but are not required for the lecture.

```{bibliography}
:filter: docname in docnames
```

::::{admonition} Companion notebook (next step)
:class: seealso

The accompanying Jupyter notebook **`magnetics_ensemble.ipynb`** (in the course `notebooks/` directory) implements the forward model of a polarity-reversal stripe sequence: given the GPTS, a half-spreading rate, and a magnetised crustal layer geometry, predict the total-field anomaly profile at the sea surface. Students will use the notebook in the discussion section to fit a synthetic Juan de Fuca profile. The full inversion exercise is the subject of Lab 8.

::::

::::{admonition} Open data and tools
:class: seealso

- **NOAA NCEI Marine Trackline Geophysics archive**: <https://www.ncei.noaa.gov/maps/trackline/> — ship-towed magnetic profiles across all the world's oceans, public domain.
- **MagIC database**: <https://earthref.org/MagIC/> — open paleomagnetic data; the standard repository for published paleomagnetic measurements.
- **PmagPy**: <https://github.com/PmagPy/PmagPy> — open paleomagnetism Python tools, including readers for MagIC-formatted data, demagnetisation analysis, and standard paleomagnetic statistics.
- **GPTS-2020 reference**: <https://stratigraphy.org/timescale/> — current International Chronostratigraphic Chart, including the polarity timescale.

::::
