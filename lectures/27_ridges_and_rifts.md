---
title: "Lecture 27 — Ridges and Rifts"
short_title: "L27 Ridges and Rifts"
authors:
  - Marine Denolle
  - ESS 314 ESS Faculty
date: 2026
module: 7
lecture: 27
keywords: [mid-ocean ridge, continental rift, East African Rift, magnetic stripes, Vine-Matthews, McKenzie stretching, Juan de Fuca, Axial Seamount, rifting continuum, non-uniqueness]
---

# Ridges and Rifts

:::{seealso}
📊 **Lecture slides** — <a href="https://uw-geophysics-edu.github.io/ess314/slides/lecture_27_slides.html" target="_blank">open in new tab ↗</a>
:::

```{admonition} Learning Objectives
:class: tip dropdown

By the end of this lecture, students will be able to:

- **[LO-1, LO-2]** Articulate the rifting continuum from stable continental craton through mature rift, magmatic break-up, and seafloor spreading, identifying the diagnostic geophysical signature of each stage.
- **[LO-2, LO-3]** Derive the half-spreading rate from a magnetic-stripe profile using the Geomagnetic Polarity Time Scale, and decompose a continental-rift Bouguer anomaly into its topography, Moho, and lithosphere–asthenosphere boundary contributions.
- **[LO-3, LO-4]** Demonstrate the non-uniqueness of gravity-only density modeling at a mid-ocean ridge, and identify the additional observables that disambiguate between shallow-narrow and deep-broad density structures.
- **[LO-5, LO-7]** Use `scipy.signal.find_peaks` to invert spreading rate from a real magnetic-anomaly grid, and critically evaluate the failure modes of autonomous stripe picking.

**Prerequisites:** Half-space cooling and the lithosphere as a thing (L26); gravity anomalies and the isostatic decomposition (L19–L21); magnetic anomalies and the geodynamo (L23–L25). Familiarity with `numpy`, `matplotlib`, `xarray`, and `scipy.signal` is assumed for §4.
```

---

## 1. The Geoscientific Question

A mid-ocean ridge is a 60,000-km-long submarine mountain chain that produces dense basaltic oceanic crust at a remarkably steady rate. A continental rift is a topographic depression filled with terrestrial sediments, normal-faulted continental crust, and patchy alkaline volcanism. The two look nothing alike — different elevations, different rocks, different volcanism, different gravity, different seismicity. And yet they are connected by a single physical process: extension of the lithosphere.

```{figure} ../assets/figures/F1_seafloor_age_map.png
:name: f27-global-ridges
:alt: Global map of seafloor age. Bright yellow bands trace every active mid-ocean ridge on Earth — the Mid-Atlantic Ridge running pole-to-pole, the East Pacific Rise, the Southwest Indian Ridge, the Juan de Fuca system off the Pacific Northwest. Dark purple-black patches in the northwest Pacific are the oldest oceanic crust at roughly 180 Ma. The width of each colour band records the spreading rate.
:width: 100%

**Every active mid-ocean ridge on Earth, in one map.** Seafloor age from the Müller/Seton 2020 grid {cite:p}`Seton2020`: ridges appear as the bright yellow zero-age axes. Slow ridges (Mid-Atlantic, Southwest Indian) generate narrow age bands; fast ridges (East Pacific Rise) generate wide bands. Compare the linear ridge geometry here with the broad, fragmented continental-rift systems shown next — same physical process (lithospheric extension), very different surface expression.
```

The East African Rift system today shows us every stage of that connection. In southern Tanzania the lithosphere is in the earliest stages of rifting. In the Main Ethiopian Rift the crust has thinned to about 25 km and magmatic segments have begun to organize. At Afar the rift floor has subsided below sea level and dykes are accommodating most of the extension. In the Red Sea and Gulf of Aden the process has run to completion — there is oceanic crust on the floor and the spreading is a magnetic-stripe record of the past few million years. The same rift system, sampled along its length, contains the whole story from stable continent to mature ridge.

```{figure} ../assets/figures/F6_ear_system_map.png
:name: f6-ear-system
:alt: Map of the East African Rift system showing the Nubian, Somalian, and Arabian plates, the Eastern (Kenya/Ethiopia/Afar) and Western (Tanganyika/Malawi) rift branches, plate motion arrows, and major volcanic centres including Erta Ale, Dabbahu, Aluto, Nyiragongo, Oldoinyo Lengai, and Kilimanjaro. Green circles mark sampling points along the rifting-continuum spectrum from incipient rifting in Malawi to full seafloor spreading in the Gulf of Aden.
:width: 80%

The East African Rift system. Each green circle marks a snapshot along the rifting continuum: incipient at Malawi, mature at Kenya, magmatic break-up at Afar, full spreading at the Gulf of Aden. For the research-grade reference map see Biggs et al. 2021 (*Nature Communications* 12:6881, Fig. 1, CC-BY 4.0).
```

The framing question for the rest of the lecture is:
> *Mid-ocean ridges and continental rifts both extend the lithosphere. Why do they look so different in gravity, heat flow, and magnetics — and how do we know they are connected by a single physical process?*

The answer requires every method developed in earlier modules. Gravity and isostasy (L19–L21) decompose the rift signature into contributions from topography, Moho relief, and the lithosphere–asthenosphere boundary. Magnetics (L23–L25) records spreading rates through Vine–Matthews stripes. Seismic refraction (L08) gives the velocity structure of new oceanic crust and the thinned continental crust beneath rifts. L26's thermal-cooling framework, recast as a stretching factor, predicts the subsidence history of continental rifts and their post-rift passive margins.

---

## 2. Governing Physics

### 2.1 Extension as the unifying process

The starting point is mechanical: under sufficient horizontal extensional stress, the lithosphere stretches. If the extension is *passive* — driven by far-field plate-boundary forces — the lithosphere thins gradually, the surface subsides, and decompression of the underlying asthenosphere may produce melt. If the extension is *active* — driven by mantle plume buoyancy and the resulting thermal upwelling — magmatism dominates the process from the start, and extension is accommodated by dyke injection rather than fault slip.

In practice, real rifts combine both end-members. The East African Rift began as passive extension along inherited Proterozoic lithospheric weaknesses, then transitioned to magmatism-dominated extension once the Afar plume began to interact with the rift axis around 30 Ma. Mid-ocean ridges are the limit case in which magmatism has fully outpaced faulting: extension is taken up by new crust generated at the axis, not by faulting of pre-existing crust.

The unifying physical variable is the *stretching factor*:

$$
\beta = \frac{L_0}{L_{\text{thinned}}},
$$ (eq:stretching-factor)

where $L_0$ is the original lithosphere thickness and $L_{\text{thinned}}$ is the thickness after rifting. Stable craton has $\beta = 1$. A mature continental rift has $\beta = 2$–3. Magmatic break-up has $\beta = 4$–6. A mid-ocean ridge has $\beta \to \infty$ — the original continental lithosphere has been entirely replaced by new oceanic material.

### 2.2 At ridges: decompression melting and the magmatic conveyor

A mid-ocean ridge is in steady state. Hot mantle rises beneath the axis to fill the gap left by diverging plates. As it rises, the pressure on it drops while the temperature stays nearly constant. The decompression carries the rising mantle across the dry peridotite solidus and partial melt is generated. The melt is buoyant, rises faster than the surrounding mantle, and accumulates beneath the ridge in a layered magmatic system: an axial melt lens at 1.5–3 km below the seafloor, a broader crystal mush zone underneath, and a transition into solid gabbro and mantle peridotite below the Moho.

```{figure} ../assets/figures/F1_ridge_magmatic_system.png
:name: f1-ridge-magmatic
:alt: Schematic cross-section of a mid-ocean ridge showing four crustal layers (Layer 2A pillow basalts, Layer 2B/2C sheeted dykes, Layer 3 gabbro, then mantle peridotite below the Moho at about 5.8 km depth), with a thin axial magma lens at 1.8 km depth in vermilion, a broad orange crystal mush zone surrounding and underlying the lens, and three vertical orange arrows showing mantle upwelling from below the Moho. Plate-motion arrows at the top point outward from the ridge axis.
:width: 90%

The mid-ocean ridge magmatic system. The axial magma lens (AML) is a thin, high-melt-fraction body imaged seismically at 1.5–3 km below the seafloor on intermediate- and fast-spreading ridges. It is surrounded by a much larger crystal mush zone with melt fractions typically below 15%. Cooling and crystallisation of the mush feed the layered crustal stack outward — pillow basalts (Layer 2A), sheeted dykes (Layer 2B/2C), and cumulate gabbro (Layer 3) — that is observable today in obducted ophiolites on land.
```

The dyke-injection mechanism matters at every stage of the rifting continuum. At a mid-ocean ridge dykes propagate laterally from the axial magma lens to feed the sheeted dyke complex and the overlying pillow basalts. At a magmatic continental rift like Afar, the *same* dyke geometry is observed: 60-km-long dyke intrusion events accommodate metres of extension per dyke, and the surface deformation pattern measured by InSAR matches the ridge model precisely (Wright et al. 2006, *Nature*).

### 2.3 At rifts: stretching, subsidence, and the McKenzie model

The canonical model for continental rifting is McKenzie 1978. The lithosphere of original thickness $a$ is stretched uniformly by factor $\beta$ in a single instantaneous event. Immediately afterward, the crust is thinner (by factor $\beta$) and the mantle lithosphere is thinner (by the same factor), and the rest of the column is hot asthenosphere risen to maintain the original column height.

The thinned column is denser than its un-rifted neighbour in the upper part (crust replaced by mantle is replaced by lower-density asthenosphere effects), so isostatic balance requires subsidence. Immediately after rifting the surface drops by the *initial syn-rift subsidence* $S_i$. As the asthenospheric heat dissipates over the next 50–100 Myr by conduction, the column re-thickens and the surface drops further by *post-rift thermal subsidence* $S_T(t)$. The total subsidence approaches an asymptote scaled by $\beta$.

The signatures evolve through three observable phases:

1. **Syn-rift** (active extension, ~0–10 Myr). Elevated heat flow, normal-faulted graben at the surface, magmatic intrusion if $\beta$ is large or a plume is present.
2. **Post-rift thermal subsidence** (~10–100 Myr). Surface cools and subsides on a $\sqrt{t}$ schedule reminiscent of the half-space cooling model from L26.
3. **Passive margin or failed rift** (>100 Myr). If extension continued and broke the lithosphere, the rift evolved into a mid-ocean ridge and the original rift basin is now a sediment-loaded passive margin. If extension stopped, the rift is preserved as a *failed rift* like the Midcontinent (Keweenawan) Rift in North America.

```{admonition} The Wilson cycle
:class: note

The rifting continuum is the *beginning* of the Wilson cycle — the long-period oscillation of continental break-up, ocean basin growth, ocean closure, and continent–continent collision that has run multiple times in Earth history. L27 captures the first two stages. Convergent margins (L28), transforms (L29), and the geodynamic synthesis (L30) capture the rest of the cycle.
```

---

## 3. Mathematical Framework

### 3.1 Notation

```{admonition} Notation
:class: important dropdown

| Symbol | Meaning | Typical value |
|--------|---------|---------------|
| $r$ | Half-spreading rate | $0.7$–$8\ \mathrm{cm/yr}$ |
| $d_n$ | Distance from ridge axis to $n^{\text{th}}$ reversal stripe | km |
| $t_n$ | Age of $n^{\text{th}}$ polarity reversal (from GPTS) | Ma |
| $\beta$ | Lithospheric stretching factor | $1$–$\infty$ |
| $a$ | Original lithosphere thickness | $\sim 125$ km |
| $S_i$ | Syn-rift (initial) subsidence | $0.5$–$3$ km |
| $S_T(t)$ | Post-rift thermal subsidence | $0.5$–$4$ km |
| $T_e$ | Effective elastic thickness | $5$–$80$ km |
| $\rho_m$ | Mantle density | $3300\ \mathrm{kg\,m^{-3}}$ |
| $\rho_s$ | Sediment density (rift fill) | $2200$–$2400\ \mathrm{kg\,m^{-3}}$ |
| $\rho_g$ | Gabbroic-intrusion density (failed rift) | $\sim 3080\ \mathrm{kg\,m^{-3}}$ |
| $\Delta\rho$ | Density contrast across an interface | g/cm³ |
| $\alpha$ | Thermal expansion coefficient | $3 \times 10^{-5}\ \mathrm{K^{-1}}$ |
```

### 3.2 Magnetic stripes and spreading rate

The cornerstone observation of plate tectonics is the symmetric pattern of magnetic anomalies on either side of a mid-ocean ridge. As new oceanic crust crystallises at the ridge axis, it cools through its Curie temperature and acquires a thermoremanent magnetisation aligned with the Earth's field at that moment. The field reverses polarity at irregular intervals — the *Geomagnetic Polarity Time Scale* (GPTS) records these reversals back to ~180 Ma. Successive bands of crust therefore record alternating polarity, producing positive and negative anomalies that mirror across the ridge axis.

The relationship between distance and age is linear if the spreading rate is constant. For a half-spreading rate $r$ (cm/yr) and a reversal at age $t_n$ (Ma), the corresponding stripe sits at distance

$$
d_n = r \cdot t_n
$$ (eq:stripe-distance)

from the ridge axis (where $r$ is converted from cm/yr to km/Myr by multiplying by 10). The inverse problem is one line:

$$
r = \frac{d_n - d_m}{t_n - t_m}.
$$ (eq:spreading-rate-inverse)

Given the location of any two reversal stripes and the GPTS ages of those reversals, the half-spreading rate is determined. In practice we use four or five stripes and a least-squares fit to reduce uncertainty.

### 3.3 Ridge gravity and the role of the mantle root

A mid-ocean ridge is isostatically compensated. The free-air anomaly is therefore small and oscillates around zero. The Bouguer anomaly, however, is strongly *negative* over the ridge axis — the opposite of what naive intuition would predict for a topographic high.

The reason is the density contrast that the Bouguer correction has *not* removed. The Bouguer reduction strips out the gravitational effect of the topography itself (water and crust above the reference level) but leaves intact the effect of *subsurface* density variations. Beneath the ridge axis there is a broad zone of partially molten and thermally expanded mantle — the mantle root, several hundred kilometres wide and tens of kilometres thick. Its density deficit (about $-0.04$ g/cm³) produces a large negative gravity contribution. The Bouguer anomaly across the ridge is dominated by this mantle root, not by the surface bathymetry.

```{figure} ../assets/figures/F2_mar_gravity_profile.png
:name: f2-mar-gravity
:alt: Three-panel cross-section across the Mid-Atlantic Ridge at 40 degrees south. Panel a shows bathymetry that rises smoothly from about 5 km depth at the flanks to about 2 km at a narrow axial valley at the ridge axis. Panel b shows the gravity anomalies — the Bouguer anomaly drops from about 330 mGal at the flanks to about 90 mGal at the axis (a 250 mGal negative anomaly), while the free-air anomaly oscillates around zero with a small positive bump at the axis. Panel c shows the density model with oceanic crust at 2.9 g/cm cubed, fertile mantle at 3.30, and a broad orange-shaded low-density mantle root with a 0.04 g/cm cubed contrast centred under the ridge and extending from about 11 km to 45 km depth and from minus 280 to plus 280 km horizontal distance.
:width: 90%

Bathymetry, gravity anomalies, and density model across the Mid-Atlantic Ridge at 40°S. The free-air anomaly stays close to zero (ridge is in approximate isostatic equilibrium), but the Bouguer anomaly drops by ~250 mGal over the ridge axis because of the low-density mantle root beneath. The shape and amplitude reproduce the Lowrie & Fichtner (2020) §8.5 model. Gravity data plotted on this figure use Sandwell & Smith (2014) global marine gravity (open license) when run with network access; the figure shown is the deployed-version forward-model overlay.
```

### 3.4 The McKenzie 1978 stretching subsidence

Following McKenzie's instantaneous-stretching model, the syn-rift subsidence is

$$
S_i = a \, \frac{\rho_m \alpha T_m \left(1 - 1/\beta\right)}{\rho_m - \rho_s},
$$ (eq:mckenzie-syn-rift)

and the subsequent thermal subsidence follows

$$
S_T(t) = S_T^{\infty} \left[1 - \frac{8}{\pi^2} \sum_{n=0}^{\infty} \frac{1}{(2n+1)^2} \exp\left(-\frac{(2n+1)^2 t}{\tau}\right)\right],
$$ (eq:mckenzie-thermal)

with thermal time-scale $\tau = a^2 / (\pi^2 \kappa) \approx 62$ Myr for $a = 125$ km. The infinite-time asymptote $S_T^{\infty}$ depends on $\beta$ and gives the depth of the post-rift basin floor. The closed-form expressions are useful but not the point — the point is that *the heat-equation framework from L26 applies to continental rifting as well, with $\beta$ replacing the seafloor-age variable*. Both are statements of the same underlying physics: cooling of a thermally perturbed lithospheric column.

The "Steer's head" geometry that all passive margins display follows from this: a narrow syn-rift basin (large $\beta$ near the rift axis) overlain by a much broader post-rift thermal-subsidence basin (decreasing $\beta$ with distance from the failed rift centre).

### 3.5 Continental-rift gravity and the same decomposition

The continental-rift counterpart of the ridge gravity decomposition has three contributions, one to each major lithospheric interface, exactly mirroring the structural elements introduced by stretching.

```{figure} ../assets/figures/F9_continental_rift_gravity.png
:name: f9-rift-gravity
:alt: Two-panel decomposition of the continental rift Bouguer anomaly. Top panel shows three contributions plotted as a function of distance from rift axis: an orange dashed narrow positive contribution from topography (rift shoulders and axial graben), a green dash-dotted intermediate positive contribution from Moho relief (raising from 32 km off-axis to 22 km at the axis), a blue dotted broad negative contribution from lithosphere-asthenosphere boundary thinning (LAB shallowing from 150 to 120 km), and a thick black total curve that is the sum. The total Bouguer anomaly drops to about minus 150 mGal at the axis. Bottom panel shows the corresponding density cross-section with thinned crust, asthenospheric upwelling (vermilion shading), and structural-element annotations.
:width: 88%

Continental-rift Bouguer anomaly decomposed into three additive contributions, each tied to a structural element. The broad LAB-thinning negative contribution dominates; the Moho-relief positive contribution partially cancels it; the topographic contribution modulates near the axis. (After Lowrie & Fichtner 2020, Fig. 8.42.)
```

The same three-element decomposition applies to every continental rift. The proportions shift with the rifting stage — at incipient rifting the LAB-thinning signal is small; at magmatic break-up the Moho-relief term is dominated by a magmatic intrusion of dense gabbroic underplating; at a failed rift the topographic contribution flips sign as post-rift sediments fill the basin.

### 3.6 EAR Kenya: a worked instance

The East African Rift in Kenya is the textbook example of a mature continental rift, and the three-panel cross-section through the southern Kenya segment shows the full structural story.

```{figure} ../assets/figures/F7_ear_kenya_cross_section.png
:name: f7-ear-kenya
:alt: Three-panel cross-section of the East African Rift in Kenya. Panel a shows a Bouguer gravity anomaly that drops to a broad minus 250 mGal low across a 100-km wide rift zone, with a small central positive of about plus 25 mGal directly over the axis from shallow magmatic intrusion. Panel b shows topography with broad uplift to about 1700 metres at the rift shoulders and an axial graben dropping to 900 metres at the axis. Panel c shows the density and Vp cross-section to 80 km depth: upper crust at 2.7 g per cubic cm extends from the surface to about 16 km depth, lower crust at 2.9 from 16 to 22 km at the axis (rising sharply from 32 km off-axis), and a low-velocity Vp 7.4 km/s and low-density mantle dome with delta-rho minus 0.04 occupying the upper mantle from 22 to 80 km depth across the central 200 km of the rift. A narrow vermilion-coloured rectangle in the upper crust at the axis marks the dyke injection zone.
:width: 88%

Geophysical cross-section through the Kenya Rift at ~0–1°N (geometry after Mechie et al. 1997). The signature is the canonical mature-rift one: broad Bouguer low (~−250 mGal) with central magmatic high, broad uplift with axial graben, thinned crust (Moho rising from 32 to 22 km), and a low-velocity / low-density mantle dome — the "Kenya dome".
```

The Bouguer low here is deeper than the Basin & Range (~−100 mGal) because Kenya has had longer to develop and the magmatic root has had more time to accumulate. The central magmatic high (positive feature on top of the regional low) is the gravity signature of dyke injection — exactly the physics introduced in §2.2.

---

## 4. Working With Real Data

Three short data-access workflows continue the L26 series. The first three lectures of Module 7 (L26 and now L27) introduce one new data-fetching pattern apiece; by L30 the student has a portfolio of reproducible open-data workflows for every major geophysical observable.

### 4.1 Code Block D — Spreading rate from magnetic stripes

This is the fourth canonical data-access block of the course. The earlier three appeared in L26: seafloor age (xarray + EarthByte), CRUST1.0 Moho (ASCII XYZ), and ETOPO1 bathymetric transect (PyGMT). Code Block D introduces *peak detection on a 1D profile* — a workflow that recurs throughout geophysics, from teleseismic phase picking to gravity anomaly mapping.

```python
# Pick spreading rate from the EMAG2 global magnetic anomaly grid.
# Provenance: Meyer, B., Saltus, R., and Chulliat, A. (2017). EMAG2v3: Earth
#   Magnetic Anomaly Grid (2-arc-minute resolution), Version 3. NOAA NCEI.
#   DOI: 10.7289/V5H70CVX. Public domain — US federal data.

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Load EMAG2v3 (the netCDF distribution from NOAA NCEI)
url = "https://www.ngdc.noaa.gov/geomag/EMAG2/EMAG2_V3_20170530.nc"
emag = xr.open_dataset(url)

# Extract a profile perpendicular to the Juan de Fuca Ridge axis at 47°N
profile = emag["z"].sel(lat=47.0, method="nearest").sel(lon=slice(-132, -126))
# Approximate distance (km) east of −129°E along 47°N
distances_km = (profile.lon.values - (-129.0)) * 111 * np.cos(np.radians(47))

# Find peaks (positive anomalies = normal polarity bands)
peaks, _ = find_peaks(profile.values, prominence=80, distance=20)
peak_distances = distances_km[peaks]

# Compare to GPTS (Cande & Kent 1995):
# C1n (Brunhes)  centre ≈ 0.39 Ma
# C2An (Gauss)   centre ≈ 3.09 Ma
# C3n (Thvera)   centre ≈ 5.12 Ma
# C3An_2          centre ≈ 6.58 Ma
gpts_centres = np.array([0.39, 3.09, 5.12, 6.58])

# Match the first few positive-side peaks to GPTS chrons
positive_peaks = np.sort(peak_distances[peak_distances > 5])
n = min(len(positive_peaks), len(gpts_centres))

# Linear fit through origin: distance_km = (half_rate_cm_per_yr * 10) * age_Ma
slope = np.sum(gpts_centres[:n] * positive_peaks[:n]) / np.sum(gpts_centres[:n] ** 2)
half_rate_cm_per_yr = slope / 10.0
print(f"Inverted half-spreading rate: {half_rate_cm_per_yr:.2f} cm/yr")
print(f"Reported JdF (Nuvel-1A): 2.85 cm/yr")
```

The output of this workflow on the deployed sandbox synthetic, and a sample of what students should obtain when run on a real EMAG2 fetch, is in Figure F5.

```{figure} ../assets/figures/F5_jdf_magnetic_stripes.png
:name: f5-jdf-stripes
:alt: Two-panel figure. Top panel shows the predicted polarity-reversal stripes from the Cande and Kent 1995 GPTS, symmetric about the ridge axis at zero. Black bars mark normal-polarity intervals; white gaps mark reversed-polarity intervals. The pattern is roughly symmetric. Bottom panel shows a magnetic anomaly profile along a 600-km swath across the Juan de Fuca Ridge axis at 47 degrees north. The anomaly oscillates between approximately plus 250 and minus 150 nT, with prominent positive peaks at the axis and at roughly plus/minus 90 km, plus/minus 145 km, and plus/minus 220 km. Pink triangle markers from scipy.signal.find_peaks show automatic peak detections at major positive anomalies. An inset box reports the inverted half-spreading rate as 2.17 cm/yr against the reported Juan de Fuca rate of 2.85 cm/yr.
:width: 90%

Magnetic anomaly across the Juan de Fuca Ridge. (a) Predicted polarity stripes from the Cande & Kent 1995 GPTS at 2.85 cm/yr half-rate. (b) The magnetic anomaly profile with `find_peaks()` detections; the inverted half-rate from the first four matched chrons is 2.17 cm/yr against the reported 2.85 cm/yr — a 25% underestimate driven by the peak-detection threshold catching the Brunhes chron centre near the axis and pairing it with the C2An Gauss peak. A real-EMAG2 run with tuned prominence usually recovers the spreading rate to better than 10%. Stripe data: NOAA EMAG2v3 (Meyer et al. 2017; public domain) when network access is available; the deployed figure uses a synthetic Cande & Kent 1995 stripe sequence as fallback.
```

Two teaching points carry through.

1. **Inverse problems can be one-liners.** Spreading rate from stripes is essentially a single linear regression with a known ordinate (GPTS age) and a measured abscissa (peak distance from axis). The geological complexity hides in the *identification* of which peak corresponds to which polarity chron.
2. **Peak detection is geometry, not magic.** `scipy.signal.find_peaks` picks local maxima above a prominence threshold. The choice of threshold trades false positives against missed real peaks, and the right threshold depends on the data's signal-to-noise ratio. The AI-literacy callout at the end of this lecture returns to the failure modes.

---

## 5. Two Predict-Then-Reveal Rounds

The middle of this lecture is two structured rounds. In each, the class predicts an outcome before the answer is revealed. The pedagogical value of the predict-first step is irreducible: students who write down their predictions before seeing the answer build *their own* model of the phenomenon. Students who skip the prediction simply add the answer to the pile of facts they have heard.

### 5.1 Round 1 — The MOR gravity non-uniqueness exercise

```{admonition} Predict
:class: tip

You are handed the Bouguer gravity profile across a mid-ocean ridge. The profile shows a clean, broad negative anomaly centred on the ridge axis, with an amplitude of about $-250$ mGal and a half-width of roughly 200 km. Working in pairs, sketch a 2D density-anomaly cross-section that could explain this anomaly.

You may freely choose: the *depth* of the anomalous mass, its *horizontal width*, and its *density contrast* against the background. You may not assume access to any other measurement.

Take 4 minutes. Sketch your model on paper.
```

The reveal is two models that fit the observed Bouguer anomaly equally well within typical data uncertainty.

```{figure} ../assets/figures/F3_gravity_non_uniqueness.png
:name: f3-non-uniqueness
:alt: Three-panel figure. The top panel shows a scatter of observed Bouguer anomaly versus distance from ridge axis. Two model curves overlay the data: a solid blue curve labelled Model A which is shallow and narrow (top 10 km, base 50 km, half-width 80 km, density contrast minus 0.040 g/cm cubed), and a dashed vermilion curve labelled Model B which is deep and broad (top 30 km, base 220 km, half-width 220 km, density contrast minus 0.020 g/cm cubed). Both curves fit the data within scatter. The bottom-left panel shows Model A as a small rectangle within the upper mantle at 10 to 50 km depth and minus 80 to plus 80 km width. The bottom-right panel shows Model B as a much larger rectangle from 30 to 220 km depth and minus 220 to plus 220 km width.
:width: 92%

The MOR gravity non-uniqueness exercise. Both density models — shallow + narrow + large density contrast, versus deep + broad + small density contrast — fit the same Bouguer anomaly within data uncertainty. The amplitude near the axis is tightly constrained; the spatial extent is not. The two models make very different geological predictions, and gravity *alone* cannot distinguish them.
```

```{admonition} Discuss
:class: tip

Both models above fit the observed gravity to within typical data scatter. Yet they imply geologically very different rift cross-sections. Working in pairs:

1. What is the geological interpretation of each model? (Hint: think about partial melt fractions, depth of melt storage, and what "low-density mantle" means.)
2. Which *additional observable* would discriminate between the two? List as many as you can in two minutes.

Take 4 minutes. Be specific.
```

The pedagogical point lands in the discussion. Gravity alone is constitutively non-unique — Sten Vebæk Vestesen (1955) and Mark Talwani (1962) showed this is a fundamental property of the potential-field inverse problem, not a defect of any particular measurement. The Bouguer profile constrains the *amplitude* of the anomalous mass excess (well) and the *long-wavelength* horizontal extent (loosely), but it cannot independently resolve depth, width, and density contrast.

The fix is the multi-method synthesis principle from L26. Seismic Vp tomography would distinguish between the two models above: Model A predicts a shallow, narrow Vp anomaly localised at the axis; Model B predicts a deeper, broader Vp deficit extending well below the Moho. Surface heat flow would also discriminate — Model A's shallow melt should produce a focused thermal high; Model B's broad zone implies a broader heat-flow signature. Mantle Bouguer anomaly (with the bathymetric correction) further sharpens the constraint. Any single observable is non-unique; the *combination* is what makes a geophysical inversion well-posed.

### 5.2 Round 2 — The rifting continuum spectrum

```{admonition} Predict
:class: tip

The six stages of the rifting continuum are: (1) stable craton, (2) incipient rifting, (3) mature continental rift, (4) magmatic break-up (rift-to-spread transition), (5) slow-spreading mid-ocean ridge, (6) fast-spreading mid-ocean ridge.

For each stage, predict the *sign and rough magnitude* of:
- Bouguer gravity anomaly over the rift/ridge axis
- Surface heat flow elevation
- Topographic expression (elevation or depth)
- Stretching factor $\beta$
- Dominant magmatic style (none, alkaline, bimodal, dyke-dominated, episodic, continuous)
- Dominant seismicity style (rare, brittle, dyke swarms, etc.)

Take 5 minutes. Write down your six-row, six-column matrix.
```

The reveal is the rifting continuum figure plus a populated attribute table.

```{figure} ../assets/figures/F12_rifting_continuum.png
:name: f12-rifting-continuum
:alt: A six-panel figure showing the rifting continuum from left to right. Each panel has a colored header bar with a stage label and example region underneath, a vertical cross-section sketch in the middle showing crust as brown above the Moho as a thick black line, mantle lithosphere as tan, and asthenosphere as orange below the LAB shown as a dashed line, with depth from 0 to 300 km on the left axis of the first panel. Stage 1 stable craton (Canadian Shield) shows uniformly thick crust around 45 km and LAB at 250 km. Stage 2 incipient rifting (Rio Grande) shows mild crustal thinning to 35 km at the axis and LAB shallowed to 130 km. Stage 3 mature rift (EAR Kenya) shows crust thinned to 22 km with broad uplift and an axial graben. Stage 4 rift-to-spread (Afar/Red Sea) shows crust thinned to 12 km with strong magmatic break-up and a small dyke indicated at the axis. Stage 5 slow MOR (MAR) has new oceanic crust around 7 km thick with a deep axial valley. Stage 6 fast MOR (EPR) shows even thinner ocean crust at 6 km with an axial high and a small horizontal axial magma lens at 2 km depth. Below each cross-section is a six-row attribute table with rows Bouguer, Heat flow, Topo, beta, Magma, Seis.
:width: 100%

The rifting continuum. Each column is one stage; each cross-section sketch shows the diagnostic structural elements (Moho relief, LAB depth, axial valley or high, magmatic features); the attribute table below each panel gives the six standard geophysical observables. The East African Rift system *spatially* preserves stages 2 through 4 along its length, while the Red Sea / Gulf of Aden represent stage 5–6 transition. The Pacific is dominated by stage 6.
```

The lesson is structural. The same six observables produce qualitatively different signatures at each stage of the continuum, and the same physical process — extension — produces all of them. A geophysicist handed an unknown rift can locate it on the continuum by reading off these six attributes. A geodynamicist asked "is this rift going to become an ocean?" has, in principle, the answer: it depends on whether $\beta$ continues to grow or stabilises.

For three concrete instances — one active and well-developed, one active and immature, one that failed billions of years ago — the gravity signature evolves dramatically:

```{figure} ../assets/figures/F10_three_rift_comparison.png
:name: f10-three-rifts
:alt: Three-panel comparison of three different rifts. Panel a Basin and Range Province (Cenozoic active extension) shows a broad Bouguer gravity low of about minus 100 mGal across 600 km, with a cross-section below showing thinned crust around 28 km thick and asthenospheric upwelling under the LAB at about 60 km depth. Panel b East African Rift Kenya shows a much deeper Bouguer low of about minus 250 mGal with a central magmatic high, broad rift uplift with axial graben, sharp Moho rise from 35 to 22 km at the axis, and a strong low-density Kenya dome in the mantle. Panel c Keweenawan Midcontinent Rift (1.1 Ga failed) shows a central Bouguer high of about plus 50 mGal flanked by two negative sedimentary basins at about minus 40 mGal each, with cross-section showing a narrow dense gabbroic intrusion (rho about 3.08) extending from near surface to the Moho at 38 km, flanked by sedimentary basins.
:width: 95%

Three rifts at three different stages of the continuum. (a) Basin & Range Province — Cenozoic active extension, broad regional low. (b) East African Rift in Kenya — mature continental rift with central magmatic high and pronounced mantle root. (c) Keweenawan (Midcontinent) Rift — 1.1 Gyr-old *failed* rift, where dense gabbroic underplating produces a positive central anomaly that exceeds the regional baseline, flanked by sedimentary-basin lows on either side. The Keweenawan case is the structural endpoint for failed rifts: extension stopped, the lithosphere thickened back, and the dense magmatic intrusion is now the dominant gravity contribution.
```

---

## 6. Forward and Inverse Problems

The forward problem at a mid-ocean ridge is to predict observables from a structural model. Given a half-spreading rate $r$, the half-space cooling model from L26 predicts the bathymetric profile $d(t) = d_0 + 350\sqrt{t}$ (with age $t$ converted from distance via $t = x / (10r)$). Given the same $r$ and the GPTS, the magnetic-stripe pattern is predicted exactly. Given a layered density structure (crust + mantle root), the gravity anomaly follows from a 2D forward-modelling calculation.

The inverse problem is harder and is where Round 1 lives. Given an observed Bouguer profile, what is the density structure? Non-unique (Round 1). Given a magnetic profile, what is the spreading rate? Non-unique unless we know the GPTS *and* the symmetry. Given heat flow plus gravity plus seismicity, can we identify the rifting stage uniquely? Approximately yes (Round 2) — the *combination* breaks the non-uniqueness of any single observable.

The takeaway from this section returns to the L26 principle: geophysics is the multi-method science. Single-method inversions are constitutively non-unique. Multi-method synthesis produces the well-posed inverse problem.

---

## 7. Course Connections

```{admonition} Where this lecture connects
:class: seealso

- **L19–L21 (Gravity & Isostasy):** Bouguer anomaly decomposition into topographic, Moho, and lithosphere–asthenosphere contributions. F9 of this lecture *is* the rift-specific version of the isostatic decomposition you built in L21.
- **L23–L25 (Magnetics):** The Vine–Matthews–Morley framework applies directly here. The L25 magnetic-anomaly toolkit (regional removal, IGRF correction, reduction-to-the-pole) is what you would apply before running Code Block D on a real-world dataset.
- **L26 (Lithosphere):** Every attribute from the L26 oceanic-vs-continental matrix is *modified* at ridges and rifts. The lithosphere now has a process attached: extension and the rifting continuum.
- **L28 (Convergent Margins):** Closes the conveyor. Oceanic lithosphere born at ridges is recycled at subduction zones.
- **L29 (Transforms & Intraplate):** Plate boundaries are not just spreading and converging; the third kind connects them.
- **L30 (Synthesis):** Ridge push and slab pull as the dominant plate-driving forces. The Wilson cycle integrates rifts and ridges into the long-period history of the lithosphere.
```

---

## 8. Research Horizon

Three open-access pointers for students who want to take the lecture further.

1. **Paulatto et al. 2022** (*Frontiers in Earth Science* 10:970131, CC-BY 4.0). A modern review of seismic imaging of magma and crystal mush systems at mid-ocean ridges, hotspots, and continental rift volcanoes, with a database of 277 imaging studies. The headline result is that *most* mid-ocean ridge magma is in crystal-mush state at melt fractions below 15%; only a small fraction is in mobile axial melt lenses at any given time. This reshaped the mid-2010s textbook picture of mid-ocean ridge magmatism.
2. **Biggs et al. 2021** (*Nature Communications* 12:6881, CC-BY 4.0). A comprehensive review of volcanic activity and hazard in the East African Rift, written explicitly as a synthesis for both researchers and African geoscience capacity-building. The supplementary material includes a complete inventory of every confirmed volcanic centre in the EAR with deformation episodes back to 2002. Figure 1 of this paper is the canonical EAR system map referenced as F6 of this lecture.
3. **La Rosa et al. 2025** (*Solid Earth* 16:929–945, CC-BY 4.0). Cross-scale strain analysis in the Afar rift combining automatic fault mapping from digital elevation models with geodetic surface displacement. Provides the current best-constrained estimates of how strain partitions between faulting and dyke intrusion in the most magmatically active segment of the EAR.

```{admonition} Open research question
:class: note

Earlier figures and the McKenzie 1978 stretching framework assume that continental rifting *can* run to full break-up. In practice, the majority of continental rifts in Earth history have *failed* — they extended for some millions of years, then froze. The Midcontinent (Keweenawan) Rift in North America (F10c) is the textbook example: 1.1 Gyr old, dense gabbroic underplating, no seafloor spreading.

**Why do some rifts break to spreading and others fail?** Hypotheses include plume location, far-field plate-boundary force budget, and inherited lithospheric weakness orientation. The East African Rift is the modern laboratory for distinguishing these — the eastern branch (Afar) is breaking through; the western branch (Tanganyika–Malawi) is, by some measures, failing. Watching the next 10 Myr (or running the models forward) is the active research frontier here.
```

---

## 9. Societal Relevance: Juan de Fuca Ridge and Axial Seamount

The Juan de Fuca Ridge sits 250 km off the Washington and Oregon coasts. It is the spreading centre that creates the plate that subducts beneath Cascadia — the *same* plate that students saw accreted as Siletzia in L26 (Section 9), and the *same* plate that subducts to drive the Cascadia megathrust earthquake that will reappear in L28.

```{figure} ../assets/figures/F4_slow_vs_fast_ridge.png
:name: f4-slow-vs-fast
:alt: Two-panel figure. Panel a is a scatter plot of depth to AMC reflector versus full spreading rate from 0 to 170 mm per year. Slow-spreading ridges (blue circles, MAR and SWIR) have AMC depths from 2.5 to 6.5 km below seafloor at spreading rates of 10-40 mm per year. Intermediate ridges (green squares, JdF and GSC) cluster at 1.5 to 4 km depth at 40-80 mm per year. Fast ridges (vermilion triangles, EPR and Pacific–Antarctic) have shallow AMCs at 0.8 to 2.6 km depth at 80-160 mm per year. A trend line shows AMC depth declining exponentially with spreading rate. The Juan de Fuca Ridge is highlighted with a pink circle at 57 mm per year and 2.3 km depth. Panel b shows axial P-wave velocity profiles for a slow ridge (blue solid line, 25 mm per year) and a fast ridge (vermilion dashed line, 110 mm per year), each with a velocity inversion marking the AMC at 3 km and 1.7 km depth respectively.
:width: 92%

Axial magma chamber depth as a function of spreading rate. Slow-spreading ridges have deep, episodic magma bodies (when they have any); fast-spreading ridges have shallow, continuous axial melt lenses. The Juan de Fuca Ridge (highlighted) is intermediate-spreading and falls between the two end-members, with the additional complication that the Cobb hotspot interacts with the ridge axis at Axial Seamount. Trend after Paulatto et al. 2022 (*Frontiers in Earth Science* 10:970131, CC-BY 4.0).
```

The Juan de Fuca Ridge is also globally distinctive for a different reason: Axial Seamount, the hotspot-influenced volcano at the ridge axis at 45.95°N, is the only fully cabled mid-ocean ridge observatory in the world. The Ocean Observatories Initiative (OOI) Regional Cabled Array has continuously monitored Axial Seamount since 2014, with real-time bottom-pressure sensors, hydrophones, broadband seismometers, and chemical sensors at the volcanic summit. Axial erupted in 2015 — the *only* mid-ocean ridge eruption ever recorded in real time by a cabled geophysical network in advance, during, and after the event. The pressure data showed the volcano inflating in the months before the eruption and deflating during it; the seismometers recorded thousands of small earthquakes accompanying dyke propagation; the hydrothermal vent chemistry shifted as the magmatic plumbing changed. None of this would have been possible without the cabled array.

The point for ESS 314 is concrete: Cascadia is a complete plate-tectonic system in driving distance from Seattle. The ridge that creates the Juan de Fuca Plate is 250 km offshore. The trench that destroys it is 100 km offshore. The volcanic arc that records slab dehydration runs through Mount Rainier and Mount Baker just east of campus. L27 takes the student to the ridge end of that system. L28 will take them to the trench. By the time students reach L30, they will have studied every part of the Cascadia plate-tectonic engine in detail — and they will have done so largely by analysing real geophysical data from open sources.

The continental-scale gravity field puts the Pacific Northwest in tectonic context. The conterminous United States Bouguer anomaly shows the Cascadia margin sitting between two extremes — a strong Basin & Range gravity low to the south, a positive Siletzia anomaly along the coast — with the Midcontinent (Keweenawan) failed-rift high visible in the upper Midwest and the broad Appalachian orogenic low along the east coast.

```{figure} ../assets/figures/F11_conus_bouguer_map.png
:name: f11-conus-bouguer
:alt: Bouguer gravity anomaly map of the conterminous United States from −130 to −65 degrees longitude and 22 to 52 degrees latitude. The Basin and Range and Rocky Mountains show strong negative anomalies down to about minus 250 mGal across the western interior. A positive anomaly labelled Siletzia / Cascadia sits along the Washington and Oregon coast. The interior craton shows mild positive values. A localised positive anomaly labelled Midcontinent Rift sits in the upper Midwest. The Appalachians show a moderate negative anomaly along the east coast. Strong positive anomalies appear offshore in the Gulf of Mexico and Atlantic.
:width: 92%

Bouguer gravity anomaly of the conterminous United States. The western interior is dominated by the active extensional Basin & Range and the over-thickened Rocky Mountain crust (both strong negatives). The Midcontinent Rift is visible as a localised positive (failed rift, stage 4 → endpoint). Siletzia along the Pacific NW coast appears as a positive against the Cordilleran low — directly relevant to L26 §9 and the Cascadia anchor here. For the research-grade open-license map see Phillips et al. (1993; public domain). DOI: 10.3133/ds9.
```

---

## AI Literacy: AI as a Tool — autonomous stripe picking

```{admonition} AI as a Tool — autonomous stripe picking
:class: important

Code Block D used `scipy.signal.find_peaks` to identify magnetic-anomaly peaks as polarity-reversal stripes. This is a representative example of *autonomous picking* — a workflow that recurs throughout modern geophysics in much more sophisticated forms, including deep-learning models for seismic phase arrivals, dyke intrusion events, and earthquake clusters.

Where does `find_peaks` succeed? In the *data-rich middle* of the parameter space: clean profiles, strong signal, smoothly varying noise, no missing data, reasonable distance and prominence thresholds. The middle of the JdF profile in F5(b) is exactly such a case — the peaks are obvious, both visually and algorithmically, and the inversion recovers the spreading rate to within ~25%.

Where does it fail?

1. **Near the magnetic equator.** When the inducing field is near horizontal, the induced magnetisation of oceanic crust is much weaker than at high latitudes. Peak amplitudes drop, the signal-to-noise ratio degrades, and `find_peaks` returns false positives in the noise floor.
2. **At slow-spreading ridges with rough crustal topography.** Slow ridges (the MAR, the SWIR) have thicker, more block-faulted Layer 2A. The basement topography itself produces magnetic anomalies of similar wavelength to the polarity stripes. Disambiguating the two requires either bathymetric correction or independent age constraint.
3. **Near the magnetic poles.** Polar regions produce strong induced magnetisation in non-stripe geological features (continental shelf sediments, ice-sheet base, basement geology). The stripe signal is buried in background.
4. **With sediment cover.** Sediment overlying the oceanic crust attenuates the high-frequency magnetic signal by acting as a low-pass filter. Old crust (>50 Ma) with thick pelagic sediment cover has reduced stripe amplitude.

A deep-learning model trained on a global database of magnetic profiles (Galloway et al. 2024 is one recent example) does better than `find_peaks` on noisy data but inherits the same physical failure modes — it cannot recover information that the magnetic data fundamentally does not contain.

The pattern recurs throughout the course. AI tools succeed in the data-rich middle of parameter space and fail in the geophysically interesting edge cases. *The student must know enough geophysics to recognize when the tool will lie.* This is the third stage of the course's AI literacy arc (passive use → AI as writing coach → designing rubric-driven agents), and you will see it again in L29's autonomous focal-mechanism solutions and L30's data-driven plate-motion reconstructions.
```

---

## Concept checks

```{admonition} Concept-check exercises
:class: tip

Try these before the next class meeting; we will go over them in discussion.

1. **Spreading-rate calculation.** A magnetic-anomaly profile across the South Pacific shows the C5 chron (10.95 Ma reversal centre) at 410 km from the axis. What is the half-spreading rate at this location? Is this slow, intermediate, or fast?
2. **Non-uniqueness disambiguation.** You have the Bouguer profile of Round 1 and access to *one* additional measurement. You may choose between (i) seafloor surface heat flow at 30 stations along the transect, (ii) seismic Vp tomography to 50 km depth, or (iii) a magnetic stripe sequence. Which would you choose and why? Justify in 100 words or fewer.
3. **Rifting continuum.** The Rio Grande Rift in New Mexico shows surface heat flow ~80 mW/m², modest Bouguer low (~−100 mGal), bimodal alkaline volcanism, $\beta \approx 1.2$, and shallow extensional seismicity. Which stage of the rifting continuum is it? Justify in two sentences. (Hint: refer to F12.)
4. **AI failure mode.** A student runs Code Block D on a magnetic profile across the slow-spreading Reykjanes Ridge at 30°W. The `find_peaks` output shows ~12 peaks per side of the axis, but only ~4 polarity reversals are expected in the corresponding 8-Myr-old crust. Describe two plausible failure modes and how you would diagnose each.
```

---

## Further Reading

Open-access references are preferred and prioritised:

- **Paulatto, M., Hooft, E. E. E., Chrapkiewicz, K., Heath, B., Toomey, D. R., and Morgan, J. V.** (2022). Advances in seismic imaging of magma and crystal mush. *Frontiers in Earth Science* 10, 970131. DOI: [10.3389/feart.2022.970131](https://doi.org/10.3389/feart.2022.970131). **CC-BY 4.0.**
- **Biggs, J., Ayele, A., Fischer, T. P., et al.** (2021). Volcanic activity and hazard in the East African Rift Zone. *Nature Communications* 12, 6881. DOI: [10.1038/s41467-021-27166-y](https://doi.org/10.1038/s41467-021-27166-y). **CC-BY 4.0.**
- **La Rosa, A., Gayrin, P., Brune, S., et al.** (2025). Cross-scale strain analysis in the Afar rift (East Africa) from automatic fault mapping and geodesy. *Solid Earth* 16, 929–945. DOI: [10.5194/se-16-929-2025](https://doi.org/10.5194/se-16-929-2025). **CC-BY 4.0.**
- **Wright, T. J., Ebinger, C., Biggs, J., et al.** (2006). Magma-maintained rift segmentation at continental rupture in the 2005 Afar dyking episode. *Nature* 442, 291–294. DOI: [10.1038/nature04978](https://doi.org/10.1038/nature04978). (Cite-only; foundational.)
- **McKenzie, D.** (1978). Some remarks on the development of sedimentary basins. *Earth and Planetary Science Letters* 40, 25–32. DOI: [10.1016/0012-821X(78)90071-7](https://doi.org/10.1016/0012-821X(78)90071-7). (Cite-only; foundational.)
- **Vine, F. J. and Matthews, D. H.** (1963). Magnetic anomalies over oceanic ridges. *Nature* 199, 947–949. DOI: [10.1038/199947a0](https://doi.org/10.1038/199947a0). (Cite-only; foundational.)
- **Cande, S. C. and Kent, D. V.** (1995). Revised calibration of the geomagnetic polarity timescale for the Late Cretaceous and Cenozoic. *Journal of Geophysical Research* 100(B4), 6093–6095. DOI: [10.1029/94JB03098](https://doi.org/10.1029/94JB03098). Source of the GPTS used in Code Block D.
- **Maus, S.** (2009). EMAG2: Earth Magnetic Anomaly Grid (2-arc-minute resolution), Version 2. NOAA NCEI. DOI: [10.7289/V5MW2F2P](https://doi.org/10.7289/V5MW2F2P). Public domain — v2 lineage reference.
- **Meyer, B., Saltus, R., and Chulliat, A.** (2017). EMAG2v3: Earth Magnetic Anomaly Grid (2-arc-minute resolution), Version 3. NOAA NCEI. DOI: [10.7289/V5H70CVX](https://doi.org/10.7289/V5H70CVX). Public domain — source dataset for Code Block D (the v3 grid the code fetches).
- **Sandwell, D. T., Müller, R. D., Smith, W. H. F., Garcia, E., and Francis, R.** (2014). New global marine gravity model from CryoSat-2 and Jason-1 reveals buried tectonic structure. *Science* 346, 65–67. DOI: [10.1126/science.1258213](https://doi.org/10.1126/science.1258213). Source dataset for the F2 gravity profile overlay; freely distributed at https://topex.ucsd.edu/marine_grav/.
- **Phillips, J. D., Duval, J. S., and Ambroziak, R. A.** (1993). National geophysical data grids; gamma-ray, gravity, magnetic, and topographic data for the conterminous United States. *U.S. Geological Survey Digital Data Series DDS-9*. DOI: [10.3133/ds9](https://doi.org/10.3133/ds9). Public domain — source map for F11.
