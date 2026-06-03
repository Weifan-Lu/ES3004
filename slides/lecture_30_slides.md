---
marp: true
theme: ess314
paginate: true
math: katex
header: "ESS 314 — Lecture 30"
---

<!-- _class: title -->

# Putting It Together
## Geophysics as a Tool for Earth Structure

**ESS 314 — Geophysics · University of Washington**
Module 7 · L30 · 4 June 2026

*Read more → [Full lecture notes](../lectures/29_synthesis.html)*

---

## By the end of this lecture

- **[LO-1]** Explain why no single observable determines Earth structure uniquely
- **[LO-2]** Use the Rayleigh number to explain why the mantle convects
- **[LO-3]** State the joint inverse problem linking one model to many data types
- **[LO-4]** Identify the present frontiers of geophysics and why each advances now
- **[LO-7]** Evaluate an AI-generated multi-method argument against a rubric

---

## Ten weeks, one toolkit

- Seismic refraction, reflection, tomography
- Earthquakes, ground motion, tsunami
- Gravity and isostasy; magnetics and plate kinematics; the cooling lithosphere

**Each method is powerful. Each is also individually ambiguous.**

*Which method fits a given Earth question — and how are several reconciled?*

---

## 1. The Geoscientific Question

Different methods do **not** measure different Earths.

They measure different **properties** of the **same** Earth:
seismic velocity, density, temperature, magnetization.

> A model that fits the seismic data but predicts the wrong gravity
> is not a valid model.

*Read more → [Lecture 30 §1](../lectures/29_synthesis.html#1-the-geoscientific-question)*

---

## 2. Governing Physics — one model, many observables

![w:980 A flow diagram: one Earth model box on the left fans through five forward-operator boxes (elastic wave equation, gravity, magnetics, heat conduction, flexure and geodesy) to five observable boxes on the right; a dashed return arrow labels the joint inverse problem that reduces non-uniqueness.](../../assets/figures/fig_synthesis_forward_operators.png)

*Read more → [Lecture 30 §2](../lectures/29_synthesis.html#2-governing-physics)*

---

## 3a. The joint inverse problem

Each data type comes from the same model through its own physics:

$$ d_i = G_i(m) + e_i, \qquad i = 1,\dots,N $$

Find the model that fits **all** data at once:

$$ \chi^2(m) = \sum_{i=1}^{N} \frac{\lVert d_i - G_i(m)\rVert^2}{\sigma_i^2} $$

*Read more → [Lecture 30 §3a](../lectures/29_synthesis.html#a-the-joint-inverse-problem)*

---

## Why combining helps

- Each data type alone leaves a **null space** — changes it cannot detect
- Where two null spaces differ, requiring **both** removes models either would allow
- Combining independent observables **shrinks the null space**

**Joint interpretation reduces non-uniqueness — it does not just average it.**

---

## 3b. A concrete case: the cooling seafloor

Half-space conductive cooling sets the temperature field:

$$ T(z,t) = T_s + (T_m - T_s)\,\mathrm{erf}\!\left(\frac{z}{2\sqrt{\kappa t}}\right) $$

This single thermal model predicts **two independent observables.**

*Read more → [Lecture 30 §3b](../lectures/29_synthesis.html#b-a-concrete-case-one-thermal-model-two-observables)*

---

## Two observables, one model

Heat flow (a thermal measurement):

$$ q(t) = \frac{k\,(T_m-T_s)}{\sqrt{\pi \kappa t}} \;\propto\; t^{-1/2} $$

Seafloor depth (bathymetry + gravity, via isostasy):

$$ d(t) = d_r + \frac{2\rho_m \alpha (T_m-T_s)}{\rho_m-\rho_w}\sqrt{\frac{\kappa t}{\pi}} \;\propto\; t^{1/2} $$

---

## Forward predictions

![w:1000 Two panels versus seafloor age: heat flow falling as age to the minus one-half on the left, and seafloor depth deepening as the square root of age on the right, with old seafloor lifting above the half-space curve.](../../assets/figures/fig_plate_cooling_joint.png)

---

## The inverse problem: breaking trade-offs

- Heat flow alone constrains $k(T_m-T_s)/\sqrt{\kappa}$
- Depth alone constrains $\alpha(T_m-T_s)\sqrt{\kappa}$
- The two depend on $\kappa$ **oppositely** → fitting both separates $\kappa$ and $T_m$

**The joint fit breaks a degeneracy neither dataset could break alone.**

---

## Read the misfit, don't erase it

- Beyond ~70 Ma, seafloor is **shallower** than the half-space predicts
- This residual is **not noise** — it is a missing ingredient
- A finite-thickness **plate** (basal heat supply) removes it

*Interpreting a systematic residual as a statement about the model is the core habit of inference.*

---

## Worked example — 50 Ma seafloor

$$ q = \frac{510}{\sqrt{50}} \approx 72~\mathrm{mW\,m^{-2}} $$

$$ d = 2500 + 350\sqrt{50} \approx 4975~\mathrm{m} $$

**Both from one model.** A mismatch in either demands revision.

---

## This is the whole course

- Forward operators = Modules 1–7
- Non-uniqueness: refraction hidden layer → potential-field ambiguity → tomography
- Plate cooling ties **thermal model + isostasy + seafloor age** in one model

---

## 3c. From a cooling plate to a cooling planet

- The planet loses **~46 TW** at the surface — roughly half radiogenic, half secular cooling
- Heat escapes by **convection, not conduction**, when the Rayleigh number is large

$$ Ra = \frac{\rho g \alpha \Delta T D^{3}}{\kappa \eta} \sim 10^{6}\text{–}10^{8} \;\gg\; Ra_{\rm crit}\,(\sim 10^{3}) $$

*The cold lithosphere is just the conducting top boundary layer.*

*Read more → [Lecture 30 §3c](../lectures/29_synthesis.html#c-from-a-cooling-plate-to-a-cooling-planet)*

---

## 7. Plate tectonics & hotspots: two limbs of convection

![w:1000 Cross-section of the convecting mantle from surface to core-mantle boundary: a mid-ocean ridge and a hotspot volcano at the surface, a blue subducting slab descending as a cold downwelling, and a vermilion plume rising from the core-mantle boundary bent sideways by a green mantle-wind arrow; a boxed Rayleigh number shows the mantle convects, with surface heat loss of about 46 terawatts.](../../assets/figures/fig_mantle_convection_engine.png)

*Read more → [Lecture 30 §7](../lectures/29_synthesis.html#7-connecting-to-cascadia-from-local-cooling-to-the-global-engine)*

---

## Hotspots break the rigid-plate picture

- **Where:** volcanic chains in plate *interiors* — no plate-boundary mechanism
- **Fixity:** plumes are bent by a "mantle wind" → hotspots **migrate**; the frame is only ~fixed
- **Meaning:** wandering, tilting upwellings = a **convecting, turbulent** mantle

*Plate tectonics shows the cold downwellings; hotspots reveal the hot upwellings.*

---

## 8a. Machine learning

- Took off ~**2018**: CNNs detect & locate earthquakes from waveforms
- Enablers arriving together: **GPUs** + **large labelled seismic datasets**
- A tool, not an oracle — transfer and training bias are open problems

*Read more → [Lecture 30 §8a](../lectures/29_synthesis.html#a-machine-learning)*

---

## 8b. Sensing technology

- **Distributed acoustic sensing (DAS)**: a fibre-optic cable → thousands of strain sensors
- Records the wavefield every few metres over tens of km, at low cost
- Dark fibre under cities, seafloor, and glaciers becomes instrumentation

*Read more → [Lecture 30 §8b](../lectures/29_synthesis.html#b-sensing-technology)*

---

## 8c. Cryosphere & environment

- Glaciers and ice sheets radiate seismic signals: fracture, basal slip, calving
- Monitored continuously, modelled physically — and now with fibre on ice
- Same near-surface methods: groundwater, permafrost, contaminants

*Read more → [Lecture 30 §8c](../lectures/29_synthesis.html#c-the-cryosphere-and-the-environment)*

---

## 8d. Planetary interiors

![w:1000 Earth, Mars, and the Moon drawn to a common scale, each with a blue mantle and orange core; core radius is 55, 54, and 19 percent of planetary radius; imaged from thousands, one, and four seismic stations respectively.](../../assets/figures/fig_planetary_interiors.png)

*Read more → [Lecture 30 §8d](../lectures/29_synthesis.html#d-planetary-interiors)*

---

## Societal relevance — the Pacific Northwest

- **Cascadia**: megathrust geometry + locking + forearc gravity → one hazard picture
- **Puget Sound fibre**: urban telecom cables read as seismic arrays
- **Cascade glaciers & ice sheets**: seismic + geodetic monitoring of sea-level drivers

*Entry point: Pacific Northwest Seismic Network — pnsn.org*

---

## AI literacy — judge the synthesis

Prompt an AI: *"How do we know the outer core is liquid?"* Grade against a rubric:

- **Mechanism?** S-wave shadow — a fluid has no shear strength
- **Independent check?** The geodynamo needs a convecting conductor
- **Limits?** Liquid outer vs. solid inner core (PKIKP, normal modes)

**AI output is measured against your standard — not deferred to.**

---

<!-- _class: concept-check -->

## Concept Check

1. Old seafloor reads higher heat flow than the half-space predicts — which observable best distinguishes hydrothermal cooling from a finite plate, and why?
2. Gravity and refraction both target a basement interface. Name one property each senses, and why running both beats running either twice.
3. Mars's core is 54% of its radius; the Moon's is 19% — both found seismologically. What does the contrast imply about retained iron?
