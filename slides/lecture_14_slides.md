---
marp: true
theme: es3004
paginate: true
header: "ES3004 — Lecture 14"
footer: "Earthquake Phenomena I — Records, Phases, and Location"
math: katex
---

<!-- _class: title -->

# Earthquake Phenomena I
## Records, Phases, and Location

ES3004 — Introduction to Geophysics

Weifan Lu

---

## Learning Objectives

By the end of this lecture, you will be able to:

- **[LO-1]** Identify P, S, and surface waves on a seismogram and explain *why* they arrive in that order
- **[LO-2]** Convert an $S$-minus-$P$ time into a hypocentral distance using a known velocity model
- **[LO-3]** Frame earthquake location as a forward / inverse problem in $(x_0, y_0, z_0, t_0)$
- **[LO-5]** Explain the geometric origin of location uncertainty
- **[LO-7]** Critique an AI-picked phase or relocated catalog

---

## 1. The framing question

Southeast Asia sits adjacent to the highly active **Sundaland margin & Sumatra subduction zone**.

- Great megathrust event: $M_w \sim 9.1$, on **26 December 2004**
- Frequent intermediate and shallow earthquakes recorded across regional networks
- Every earthquake is hidden underground — the focus is never directly observed during rupture
- Yet, from surface records, we routinely infer **where, when, how big, and what kind**

This lecture: *where* and *when*.

*Read more → [Lecture 14 §1](../lectures/14_earthquake_phenomena_I.html#1-the-framing-question-where-did-the-earthquake-happen-and-how-do-we-know)*

---

## What the source geometry looks like

![w:880 alt:Block diagram showing fault, focus, epicenter, focal depth, and concentric wavefronts](../assets/figures/fig_eq_terminology.png)

**Focus** (hypocenter): point where rupture initiates
**Epicenter**: vertical projection of focus to surface
**Focal depth** $h$: vertical distance between them

---

## 2. Three pieces of physics combine

1. **Two body-wave modes.** P and S waves leave the source together; $V_P/V_S = \sqrt{3}$ in a Poisson solid

2. **Spherical wavefronts.** Geometric spreading reduces amplitudes, but *arrival times* are governed by the integral of slowness along the ray

3. **The free surface.** Converts body-wave energy into surface waves and produces the depth phases (pP) used for teleseismic depth determination

*Read more → [Lecture 14 §2](../lectures/14_earthquake_phenomena_I.html#2-the-physics-a-seismogram-records-p-s-and-surface-waves-in-time-order)*

---

## Wave propagation in time

![w:1000 alt:Cross-section showing P, S, and surface wavefronts radiating from a focus at 8 km depth, with a record section below showing arrivals at four stations at increasing distance](../assets/figures/fig_record_section_animation_final.png)

The three wavefronts spread at distinct speeds → arrivals always in **P → S → surface** order at every station.

---

## 3. The seismogram, anatomized

![w:1100 alt:Synthetic teleseismic seismogram with shaded windows for pre-event noise, P alone, P+S, and P+S+surface, with phase-onset markers and an annotation showing T_S minus T_P approximately equal to 7.5 minutes](../assets/figures/fig_three_phase_seismogram.png)

The interval $T_S - T_P$ is the **diagnostic measurement** for distance.

*Read more → [Lecture 14 §3](../lectures/14_earthquake_phenomena_I.html#3-the-mathematical-framework-travel-times-as-a-forward-operator)*

---

## The S-minus-P relation

Subtract the P arrival time from the S arrival time at one station:

$$T_S - T_P \;=\; D \left( \frac{1}{V_S} - \frac{1}{V_P} \right)$$

Solving for hypocentral distance:

$$\boxed{\;D \;=\; \frac{V_P\, V_S}{V_P - V_S}\,(T_S - T_P)\;}$$

For average crust ($V_P = 6.0$, $V_S = 3.46$ km/s):

$$D \;\approx\; 8.2 \times (T_S - T_P)$$

— the textbook **rule of eight**.

---

## S-P time as a function of distance

![w:880 alt:S-minus-P time versus hypocentral distance for three crustal velocity scenarios, showing that slower velocity contrasts produce steeper slopes](../assets/figures/fig_sp_time_distance.png)

Slower velocity contrast → steeper slope → small velocity-model errors → large distance errors.

---

## Single-station back-azimuth

![w:1100 alt:Three-component first-motion seismogram and a compass rose showing how the horizontal particle-motion vector points toward the source](../assets/figures/fig_polarization_baz.png)

$$\mathrm{AZI} \;=\; \arctan(A_E / A_N)$$

Vertical-component polarity resolves the $180°$ ambiguity.

---

## 3d. Triangulation: the multi-station epicenter

![w:1100 alt:Two map-view panels showing three stations and circles of constant hypocentral distance intersecting at the epicenter — perfectly in panel (a) and bounding a small residual region in panel (b)](../assets/figures/fig_triangulation.png)

- **3 stations** → epicenter (3 unknowns: $x_0, y_0, t_0$)
- **4 stations** → epicenter + depth (4 unknowns)

---

## 3e. Resolving focal depth

![w:1100 alt:Two-panel figure: left, a right triangle in cross-section showing h equals the square root of D squared minus Delta squared; right, a teleseismic schematic showing the direct P ray and the depth phase pP that reflects at the free surface above the source, separated in time by t_pP minus t_P](../assets/figures/fig_focal_depth_methods.png)

- **Local distance**: right triangle, $h = \sqrt{D^2 - \Delta^2}$
- **Teleseismic distance**: depth phase, $t_{pP} - t_P$ → focal depth

*Read more → [Lecture 14 §3e](../lectures/14_earthquake_phenomena_I.html#3e-resolving-focal-depth)*

---

## 4. The forward problem

Given a candidate hypocenter $\mathbf{m} = (x_0, y_0, z_0, t_0)$, predict the P arrival time at every station:

$$T_P^{(i)\,\mathrm{pred}} \;=\; t_0 \;+\; \frac{1}{V_P}\,\sqrt{(x_i - x_0)^2 + (y_i - y_0)^2 + (z_i - z_0)^2}$$

Two key properties:

- **Linear in $t_0$** — origin time enters as an additive constant
- **Non-linear in $(x_0, y_0, z_0)$** — distance enters through a square root

This decomposition is what Geiger's 1912 algorithm exploits.

*Read more → [Lecture 14 §4](../lectures/14_earthquake_phenomena_I.html#4-the-forward-problem-predicting-arrivals-at-every-station)*

---

## 5. The inverse problem

Define the residual at observation $i$:

$$r_i(\mathbf{m}) \;=\; d_i^{\,\mathrm{obs}} - G_i(\mathbf{m})$$

Minimize the misfit:

$$\Phi_2(\mathbf{m}) = \sum_i \left( \frac{r_i}{\sigma_i} \right)^{\!2} \quad\text{(L$\_2$, Gaussian errors)}$$

$$\Phi_1(\mathbf{m}) = \sum_i \left\vert{} \frac{r_i}{\sigma_i} \right\vert{} \quad\text{(L$\_1$, robust to outliers)}$$

Iterative: linearize about $\mathbf{m}_k$, take a least-squares step, repeat.

*Read more → [Lecture 14 §5](../lectures/14_earthquake_phenomena_I.html#5-the-inverse-problem-from-picks-to-a-hypocenter)*

---

## Why location uncertainty is geometric

![w:1100 alt:Two panels showing how station distribution affects location uncertainty: a clustered network gives an error ellipse elongated radially toward the network, and a teleseismic-only configuration produces a depth-origin time trade-off](../assets/figures/fig_error_ellipse.png)

- Clustered network → ellipse points radially *away*
- Distant stations only → depth and $t_0$ trade off

---

## Relative location: HypoDD

When two earthquakes are close together, the *difference* of their arrival times depends only on the *difference* of their coordinates — velocity-model errors cancel.

- {cite:t}`Waldhauser2000` — double-difference algorithm
- Routinely achieves **tens of metres** relative precision
- Resolves fault-plane structures invisible in absolute catalogs
- Applied globally for fault geometry and volcanic/seismic swarm imaging

---

## 6. Worked example — Regional Intra-slab Event

A regional station at $\Delta = 50$ km records $T_P = 14.2$ s, $T_S = 21.1$ s, with $A_N = 0.74$, $A_E = 0.32$, $A_Z = +0.92$.

- **Distance**: $D = 8.2 \times 6.9 \approx 56$ km
- **Back-azimuth**: $\mathrm{AZI} = \arctan(0.32/0.74) \approx 23°$
- **Depth**: $h = \sqrt{56^2 - 50^2} \approx 25$ km

A 25 km focal depth is consistent with a subducting slab intra-slab event in a active subduction setting.

> Practical seismic processing relies on converting these exact vector components and differential times into stable hypocenters.

*Read more → [Lecture 14 §6](../lectures/14_earthquake_phenomena_I.html#6-a-worked-example-locating-a-small-puget-lowland-earthquake)*

---

## 7. Course connections

- **Lecture 12 (Tomography)**: same forward/inverse framework, different unknown
- **Lecture 15 (next)**: takes location as known, asks *how big* — magnitude, $M_0$
- **Lectures 18, 23**: gravity and magnetic inverse problems — the same non-uniqueness reappears
- **Lab section**: phase picking and location with `ObsPy` and real seismic station data

*Read more → [Lecture 14 §11](../lectures/14_earthquake_phenomena_I.html#11-connections)*

---

## 8. Research horizon — ML phase picking

- **PhaseNet** {cite:p}`Zhu2019PhaseNet`: U-Net architecture; high precision on P-phase picking
- **EQTransformer** {cite:p}`Mousavi2020EQT`: hierarchical attention; microearthquakes detected across regional networks
- **PhaseNO** {cite:p}`Sun2023PhaseNO`: multi-station Fourier neural operator
- **Modern ML Catalogs**: re-processing decades of continuous waveform data
- Not a replacement for the physics — a fast front-end that supplies the $(T_P, T_S)$ that the inverse problem consumes

---

## 8. Research horizon — Distributed Acoustic Sensing

- A single fibre-optic cable, interrogated by laser pulses, becomes a dense seismic array of thousands of channels
- **Subsea & Offshore Fibres**: detect offshore earthquakes invisible to sparse land networks
- Crucial for **early warning of offshore megathrust ruptures**
- Active research area: semi-supervised picking on DAS strain-rate data {cite:p}`Zhu2023DAS`

*Read more → [Lecture 14 §8](../lectures/14_earthquake_phenomena_I.html#8-research-horizon)*

---

## 9. AI Literacy — when to trust an ML phase pick

ML pickers achieve ~95% precision on **data that look like their training data**.

- **Recall drops across unfamiliar tectonic regions** {cite:p}`Munchmeyer2022`
- Performance decreases on ocean-bottom, borehole, DAS, or noisy tropical data
- **Three habits**:
  1. Know the training distribution
  2. Verify a sample by eye
  3. Carry the velocity-model assumption forward — a pick is not a location

*Read more → [Lecture 14 §9](../lectures/14_earthquake_phenomena_I.html#9-ai-literacy-when-to-trust-an-automated-phase-pick)*

---

## 10. Concept check

1. If the velocity model used $V_P = 5.5$ instead of $V_P = 6.0$ km/s (same $V_P/V_S$), how would the calculated $D$ change?

2. For an event $\Delta = 5$ km from the closest station, do you trust the single-station $D$ more, or the multi-station triangulated epicenter?

3. With only teleseismic stations, which of $(x_0, y_0, z_0, t_0)$ is best constrained, and which is most degenerate?

*Read more → [Lecture 14 §10](../lectures/14_earthquake_phenomena_I.html#10-concept-checks)*

---

## Beyond Earth — locating *marsquakes*

NASA's **InSight** lander (2018–2022) carried a single three-component seismometer (SEIS) to Elysium Planitia.

- **One station, no triangulation possible.**
- Distance came from $T_S - T_P$ — equation $D = \dfrac{V_P V_S}{V_P - V_S}(T_S - T_P)$, with a *Mars* velocity model.
- Back-azimuth came from P-wave polarization.
- Depth was nearly unconstrained — a planetary-scale version of the depth–origin-time trade-off.

> The same fundamental physics locates both local tectonic earthquakes and distant planetary events like the [InSight S1222a marsquake](https://www.seis-insight.eu/en/public-2/martian-science/marsquake-service) ($M_w \sim 4.7$, May 2022).

---

## If you're newer to Python — what to focus on this week

You don't need to write a phase picker from scratch. The lab uses ObsPy, a high-level Python library where one line gets you a seismogram:

```python
from obspy.clients.fdsn import Client
st = Client("IRIS").get_waveforms("IU", "ANK", "*", "BHZ",
                                 t1, t1 + 600)
