---
title: "Session 10 (Activity) - One Earth, Many Observables"
---

# Session 10 (Activity): One Earth, Many Observables

*The Synthesis Studio - a 20-minute capstone review for Lecture 30.*

::::{dropdown} Learning Objectives
:color: primary
:icon: goal
:open:

By the end of this session, students will be able to:

- **[LO-OUT-F]** Decide which geophysical method fits a given Earth question and spatial scale.
- **[LO-OUT-D / LO-OUT-E]** State a joint inverse problem and explain what each method cannot constrain on its own.
- **[LO-1]** Explain why no single observable fixes Earth structure uniquely.
- **[LO-OUT-H / LO-7]** Flag the hidden assumption in a claim built on a single method.

::::

::::{dropdown} Syllabus Alignment
:color: secondary
:icon: checklist

| | |
|---|---|
| **Course LOs addressed** | LO-1, LO-3, LO-4, LO-7 |
| **Learning outcomes practiced** | LO-OUT-D, LO-OUT-E, LO-OUT-F, LO-OUT-H |
| **Companion lecture** | L30 - *Putting It Together: Geophysics as a Tool for Earth Structure* |
| **Lab connection** | Lab AI - *AI as a Geophysics Collaborator* (rubric-driven evaluation) |
| **Format** | Six-group jigsaw + report-out, enacting the joint-inversion logic of L30 Fig. 161 |

::::

## How the studio works

The course built one idea above all others: a single Earth model produces many observables, and requiring a model to fit all of them at once reduces the non-uniqueness that any one method carries alone. This session turns that idea from a figure into an activity. The class divides into six groups; each takes one Earth target at one scale and reconstructs how a geophysicist would constrain it. The report-out then assembles every group's observables onto a single diagram, so the class rebuilds the central figure of the final lecture from six independent starting points.

The session follows the discussion arc used all quarter - **observe, hypothesize, connect, reflect**: groups *observe* the figure for their target, *hypothesize* which methods bear on it, *connect* the methods into a joint inverse problem, and *reflect* on what a single method would miss.

| Phase | Time | Activity |
|---|---|---|
| Setup | 2 min | Assign six groups; review the Synthesis Card and the one rule. |
| Group work | 10 min | Fill the Synthesis Card for your target. |
| Report-out | ~6 min | Each group reports in 60 seconds; the facilitator assembles the master diagram. |
| Closing | ~2 min | Scale invariance: every group filled in one corner of the same figure. |

**The one rule:** name at least two methods, and one ambiguity their combination resolves.

## The Synthesis Card

Each group fills the same six rows. A printable worksheet and cut-apart station cards are provided as a companion handout, and a print-ready PDF is linked at the foot of this page.

1. **Methods** - the two to four course methods you would deploy.
2. **Observable to property** - for each method: what you measure, and what Earth property it senses.
3. **The null space** - what one method, alone, cannot tell you.
4. **The joint move** - method A plus method B removes which ambiguity? (one sentence)
5. **One number** - an order-of-magnitude estimate you can produce.
6. **The one-method trap** - the hidden assumption in a single-method headline.

---

## The six stations

Each station has a figure to reason from. The figure does not give the answer; it gives the target and a few footholds.

### Station 1 - The Whole Planet

```{figure} ../assets/figures/fig_l30_group1_earth.png
:name: fig-l30-g1
:alt: Cross-section of Earth showing mantle, liquid outer core, and solid inner core. Direct P rays (right) turn in the mantle and reach about 100 degrees; steeper rays refract through the low-velocity outer core and re-emerge beyond about 143 degrees as PKP, while one ray crosses the inner core as PKIKP. The gap between is the P-wave shadow zone. On the left, S rays turn in the mantle but cannot cross the liquid outer core, so no direct S exists beyond about 103 degrees - the S-wave shadow.
:width: 80%

Ray-traced shadow zones (Snell's law, p = r sin i / v constant). The velocity drop at the core-mantle boundary refracts P into the core as PKP and opens the shadow zone; S has no path through the liquid outer core and simply disappears beyond about 103 degrees - the evidence that the outer core has no shear strength.
```

```{figure} ../assets/figures/fig_l30_group1_mars.png
:name: fig-l30-g1-mars
:alt: Cross-section of Mars with a large liquid core of radius about 1830 km. A surface marsquake sends P and S rays that curve concave toward the surface and turn within the mantle by Snell's law; a steeper ray reflects off the core-mantle boundary as a core-reflected phase, and a wedge opposite the source marks the core shadow.
:width: 62%

Companion case: the same ray physics on Mars. A single station (NASA InSight) sized the liquid core to about 1830 km from core-reflected phases - the scaling-down of the same method.
```

**Question.** How do we know Earth's outer core is liquid iron - and how would you find the core of Mars with a single seismometer?
**Footholds:** teleseismic body waves and the S-wave shadow; normal modes and PKIKP; mean density and moment of inertia; the geodynamo.
**Notice:** which property does each method sense - state, radius, density, or the existence of a convecting conductor?

````{admonition} Extension - design two observing networks
:class: tip

Your team is now asked to design **two complementary networks** to pin Earth's core radius, density, and liquid/solid state - and to argue why you would want both.

```{figure} ../assets/figures/fig_l30_group1_networks.png
:name: fig-l30-g1-networks
:alt: Two side-by-side designs. Design A, satellite-led: a GRACE-FO pair measuring gravity and monthly mass change, a magnetic-survey satellite sensing the outer-core geodynamo, and rotation and precession giving the moment of inertia; it senses global integrated fields with weak vertical resolution. Design B, ground-led: a ring of seismometers recording body-wave travel times and the PKP shadow plus the planet's normal modes; it resolves sharp boundaries such as the core-mantle and inner-core boundaries but needs earthquakes and has sparse ocean coverage.
:width: 100%

Two designs for the same target. The satellite-led network fixes the global mass and field budget; the ground-led network fixes the sharp boundaries and state.
```

- **Design A - satellite-led.** What is mostly in orbit? Likely elements: time-variable **gravity** (a GRACE-FO-style pair for mass and moment of inertia), the **magnetic field** (a Swarm-style survey that senses the outer-core geodynamo), and **rotation, precession, nutation** (space geodesy) that constrain the moment of inertia. These give **bulk** quantities - core size, mean density, core dynamics - with global coverage but weak resolution of *where* at depth.
- **Design B - ground-led.** What is mostly on the ground? A global **seismometer** network recording **body-wave travel times** (the PKP shadow itself) and the planet's **free oscillations** (normal modes). These resolve **sharp radial structure** - the depths of the core-mantle and inner-core boundaries, the velocity jumps, and whether a layer is solid or liquid - but need earthquakes and have uneven coverage over oceans.
- **The joint move (the point of the task).** Neither design alone fixes everything: satellites constrain *how much mass and what bulk field* without sharp depth control; ground sensors constrain *exactly where the boundaries are and their state* but cannot weigh the whole planet from sparse stations. Used together, they pin core radius, density, and state with the null space of each filled by the other. State, in one sentence, which ambiguity each network removes from the other.
````

### Station 2 - Ocean Geophysics: The Spreading Seafloor

```{figure} ../assets/figures/fig_l30_group2_spreading_seafloor.png
:name: fig-l30-g2
:alt: Three stacked panels versus seafloor age. Top, a barcode of magnetic reversal stripes giving age. Middle, seafloor depth deepening as the square root of age on a downward depth axis. Bottom, heat flow falling as the inverse square root of age, with a measured curve below the half-space prediction over young crust marking a hydrothermal deficit; a worked point is marked at fifty million years.
:width: 88%

One thermal model, three independent observables: magnetics for age, bathymetry for depth, a heat-flow probe for flux.
```

**Question.** For one patch of seafloor - how old is it, how deep should it be, and how much heat should it give off?
**Footholds:** magnetic reversal stripes (age); bathymetry and gravity (depth, isostasy); a heat-flow probe with the half-space cooling model.
**Notice:** the heat-flow deficit over young crust is only visible because age and depth confirm the model independently.

### Station 3 - Cascadia Earthquake and Tsunami Hazard

```{figure} ../assets/figures/fig_l30_group3_cascadia_hazard.png
:name: fig-l30-g3
:alt: Cross-section of the Cascadia subduction zone from trench to arc volcano, depth increasing downward. A subducting slab dips beneath the continent; a thick locked megathrust segment carries a star. Four labeled observing systems point to the model: seismic imaging of slab geometry, waveform and paleoseismic estimate of seismic moment, GPS and InSAR locking, and forward ground-motion and tsunami prediction. A box gives the seismic moment and a magnitude near nine.
:width: 92%

One fault model must satisfy four independent observing systems at once.
```

**Question.** What will the next Cascadia megathrust do to Seattle and the coast?
**Footholds:** seismic imaging of slab geometry and width; waveform and paleoseismic moment; geodetic locking; ground-motion and tsunami forward models.
**Notice:** whether shallow slip reaches the trench - a question of wedge structure - governs the tsunami height.

### Station 4 - Mountains, Basins, and the Continents

```{figure} ../assets/figures/fig_l30_group4_mountains_isostasy.png
:name: fig-l30-g4
:alt: Top, an Airy isostasy cross-section: low-density crust supports topography with a deep crustal root that follows a curved seismic Moho, with mantle below; depth increases downward. Bottom, the gravity signature: a free-air anomaly near zero over compensated topography and a strongly negative Bouguer anomaly over the thick low-density root.
:width: 88%

Gravity alone is non-unique; a seismically imaged Moho fixes the depth and removes the ambiguity.
```

**Question.** Why is the Tibetan Plateau (or the Cascades) high - and what holds it up?
**Footholds:** free-air versus Bouguer gravity; Airy and Pratt isostasy; crustal refraction and wide-angle reflection for Moho depth; the Nafe-Drake velocity-density bridge.
**Notice:** the same surface anomaly is consistent with infinitely many depth-density pairs until a seismic interface pins the depth.

### Station 5 - The Cryosphere and Climate-Solid Earth Coupling

```{figure} ../assets/figures/fig_l30_group5_cryosphere.png
:name: fig-l30-g5
:alt: Left, an ice sheet on the lithosphere with a satellite overhead measuring total mass change; an arrow shows present-day melt removing mass and an upward arrow shows glacial isostatic rebound from past ice. Right, a waterfall chart: the observed mass trend, the removal of the glacial isostatic adjustment signal, and the resulting true ice loss, with a note that an independent viscosity or uplift constraint is needed to separate them.
:width: 96%

A satellite-gravity trend conflates present-day melt with the solid Earth still rebounding from past ice.
```

**Question.** How do we weigh an ice sheet and watch it melt - and why does the solid Earth bounce back?
**Footholds:** time-lapse and satellite gravity (mass change); glacial isostatic adjustment (rebound, mantle viscosity); cryoseismology; distributed acoustic sensing on ice.
**Notice:** to isolate the melt you must subtract the rebound signal, which itself carries a viscosity null space.

### Station 6 - The Reconstructed Past: Plate Kinematics

```{figure} ../assets/figures/fig_l30_group6_plate_kinematics.png
:name: fig-l30-g6
:alt: Left, a latitude-longitude grid with a continent fixed on a paleolatitude line recovered from magnetic inclination, its orientation set by declination, but free to slide east-west because longitude is undetermined. Right, an age-progressive hotspot track with a bend near forty-seven million years, ages labeled along two arms, and a note that the age-distance gradient gives plate speed and absolute motion.
:width: 96%

Paleomagnetism gives latitude and orientation but not longitude; hotspot tracks supply the missing absolute motion.
```

**Question.** How do we rewind the plates 100 million years - and why isn't the hotspot frame fixed?
**Footholds:** paleomagnetism (paleolatitude, apparent polar wander); seafloor magnetic isochrons; hotspot tracks; plate reconstructions.
**Notice:** the hotspot reference frame is only approximately fixed, because plumes are bent by large-scale mantle flow.

---

## Report-out: build the master diagram

As each group reports, place its observables onto one shared diagram on the board: each method becomes an arrow from a single Earth model, and each "joint move" becomes a link that removes an ambiguity. By the sixth group, six independent targets have rebuilt the same figure. The closing point is the one to carry out of the course: the workflow - deploy sources and receivers, measure a field at the surface, invert for the property contrast at depth, then test against an independent observable - is identical in form at every scale. The synthesis principle is scale-invariant.

```{seealso}
The facilitator's run-of-show, timing, board choreography, and a per-group answer key live in the instructor materials (private repository), not on this public page.
```

## AI literacy variant (LO-7)

For the terminal stage of the course's AI-literacy arc, each group also receives an AI-generated answer to its question and grades it against three rubric items before accepting any of it: is the mechanism stated correctly; is an independent observable acknowledged; are limits and uncertainty present? Any failure is recorded in the AI error log from the AI Literacy lab. The standard is not whether the AI sounds authoritative - it is whether the argument survives the scrutiny you would apply to a classmate's reasoning.

## Exit card (Geophysical Reasoning Portfolio)

Before leaving, each group submits its completed Synthesis Card as the final entry in the Geophysical Reasoning Portfolio. The single most revealing line is the "one-method trap": a clear statement of the hidden assumption behind a single-method claim is the cleanest evidence of the synthesis habit the course set out to build.

```{note}
**Printable materials.** A print-ready, self-contained **HTML** of the six station cards — each figure paired with its prompt and a blank Synthesis Card — is available as {download}`station cards (HTML) <../assets/handouts/lecture_30_synthesis_station_cards.html>`. Open it in any browser and use *Print* (one card per page; the figures are embedded, so nothing else is needed). A {download}`PDF version <../assets/handouts/lecture_30_synthesis_station_cards.pdf>` and the {download}`blank worksheet <../assets/handouts/lecture_30_synthesis_cards.md>` are alongside it. Print one card per table and one worksheet per student.
```
