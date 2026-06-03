---
title: "Lecture 28 — Convergent Plate Boundaries: Subduction Zones"
short_title: "L28 Convergent Margins"
authors:
  - Marine Denolle
  - ESS 314 ESS Faculty
date: 2026
module: 7
lecture: 28
keywords: [subduction, convergent margin, megathrust, slab, Wadati-Benioff, seismogenic zone, tsunami earthquake, Slab2, Cascadia, Chilean type, Mariana type, thermal parameter, great earthquake]
---

# Convergent Plate Boundaries: Subduction Zones

:::{seealso}
📊 **Lecture slides** — <a href="https://uw-geophysics-edu.github.io/ess314/slides/lecture_28_slides.html" target="_blank">open in new tab ↗</a>
:::

```{admonition} Learning Objectives
:class: tip

By the end of this lecture, students will be able to:

- **[LO-2, LO-4]** Describe the geometric anatomy of a subduction zone (trench, fore-arc, volcanic arc, back-arc; accretionary vs. erosive margin) and distinguish intra-oceanic from ocean–continent margins.
- **[LO-2]** Explain the dynamic classification of convergent margins along the Chilean-type ↔ Mariana-type continuum, and relate slab age, dip, and coupling to back-arc deformation.
- **[LO-1, LO-3]** Use three measurable parameters — incoming-plate age, convergence rate, and trench sediment thickness — to place a subduction zone in a quantitative classification space, and evaluate the historical hypothesis that age and rate control the maximum earthquake magnitude.
- **[LO-3, LO-4]** Interpret the depth-varying rupture behaviour of a megathrust (the seismicity, tsunami, and strong-motion domains) and connect each domain to a specific hazard.
- **[LO-4]** Characterize the Cascadia subduction zone in this framework and explain why a young, warm, slowly converging margin is nonetheless capable of an $M\,9$ earthquake.

**Prerequisites:** Lithosphere structure and plate-boundary kinematics (L26, especially §7 on relative motion, circuit closure, and subduction polarity); seismic-wave propagation and earthquake location (L04–L07); earthquake source and focal mechanisms (L13–L16); ground motions and tsunamis (L16–L17). Familiarity with the open-data workflow of L26 §4 is assumed for the companion notebook.
```

---

## 1. The Geoscientific Question

A convergent boundary is the one place in the plate-tectonic system where lithosphere is destroyed. Lecture 26 established the kinematic setting: where the relative-velocity vector points toward a boundary, lithosphere must be consumed, and the buoyancy contrast developed across the oceanic–continental comparison decides which plate descends. This lecture takes up what happens at that boundary — the structure of a subduction zone, the earthquakes it generates, and the question of how large those earthquakes can become.

That last question has a specific and instructive history. For roughly twenty-five years the field believed it had the answer. Following {cite:t}`RuffKanamori1980`, subduction zones were ordered along two parameters — the age of the incoming plate and the rate of convergence — and the largest earthquakes were expected where an old, dense plate converged rapidly with its overriding neighbour. Old and fast meant strongly coupled; strongly coupled meant great earthquakes. Young or slow margins were thought incapable of the very largest ruptures.

Two earthquakes dismantled that picture. The 2004 Sumatra–Andaman earthquake ($M\,9.1$) ruptured a margin of intermediate-to-old age converging relatively slowly and obliquely — not the predicted recipe. The 2011 Tōhoku earthquake ($M\,9.1$) struck a segment of the Japan Trench where the prevailing hazard models considered an event of that size essentially impossible. The synthesis that followed {cite:t}`Wirth2022` states the conclusion plainly: the hypotheses that plate age and convergence rate control the ability of a subduction zone to host great earthquakes have been dispelled.

```{figure} ../assets/figures/SF1_global_trenches.png
:name: SF1_global_trenches
:alt: Pacific-centred world map showing the major subduction trenches as toothed lines forming the Pacific Ring of Fire — Aleutian, Alaska, Cascadia, Middle America, Peru-Chile, Kuril-Kamchatka, Japan, Izu-Bonin-Mariana, Ryukyu, Philippine, Java-Sunda, Tonga-Kermadec, New Hebrides, Hikurangi — plus the Lesser Antilles, Sumatra, and Scotia arcs. Great earthquakes of the past century are plotted as stars sized by magnitude: Chile 1960 (M9.5), Alaska 1964 (M9.2), Sumatra 2004 (M9.1), Tohoku 2011 (M9.1), Kamchatka 1952 (M9.0), Cascadia 1700 (M9.0), scattered around the Pacific rim at zones of very different age and convergence rate.
:width: 100%

The world's subduction zones, with the great earthquakes ($M \geq 8.5$) of the past century. The trenches form the Pacific "Ring of Fire" together with the Sunda, Tethyan, and Caribbean–Scotia systems. Every $M\,9$ of the instrumental era occurred on a subduction megathrust — but those giants are spread across margins of widely differing plate age, convergence rate, and sediment supply, the first hint that the controlling parameters are not the obvious ones. Trench geometry after {cite:t}`Hayes2018` (Slab2); great-earthquake locations from the USGS/Global CMT catalogues as summarised by {cite:t}`Wirth2022`. Produced by ``assets/scripts/fig_28_global_trenches.py``.
```

The framing question for the lecture is therefore not "where do subduction earthquakes occur" — {numref}`SF1_global_trenches` answers that — but:

> *What physical properties of a subduction zone control how it deforms, how it fails, and how large an earthquake and tsunami it can produce — and why did the parameters everyone first reached for turn out to be the wrong ones?*

The answer organizes the rest of the lecture. The classification that failed is worth teaching precisely because it failed: it is a clean example of how a physically reasonable hypothesis is revised against data, and it leads directly to the controls the modern literature does favour.

---

## 2. Governing Physics

### 2.1 The slab as a cold, dense sinker

A subducting slab is oceanic lithosphere that has cooled and thickened away from its ridge (L26 §2). By the time it reaches a trench it is colder, and therefore denser, than the asthenosphere beneath it. That negative buoyancy is the engine of subduction: the weight of the sinking slab pulls the trailing plate along behind it. *Slab pull* is generally regarded as the dominant force in the plate-tectonic budget, larger than the *ridge push* that drives plates away from spreading centres.

The density contrast that drives the slab down has two parts, exactly as in the lithosphere comparison of L26 §6.1. The *thermal* contrast comes from the slab being colder than its surroundings; it grows with the age of the incoming plate, because older lithosphere is thicker and colder. The *compositional* contrast comes from the basalt-to-eclogite transition: as the basaltic oceanic crust descends and increases in pressure, it transforms to eclogite, a denser assemblage that adds to the slab's negative buoyancy. Both effects make an old slab a more vigorous sinker than a young one — which is exactly why the original Ruff–Kanamori reasoning was physically appealing.

### 2.2 Coupling on the megathrust

The boundary between the descending slab and the overriding plate is the *megathrust* — the largest fault surface on Earth, and the source of every great subduction earthquake. Its behaviour is governed by how strongly the two plates are mechanically locked, or *coupled*, across the interface.

Where the megathrust is strongly coupled, the plates lock during the interseismic period, strain accumulates in the overriding plate, and that strain is released suddenly in great earthquakes. Where the megathrust is weakly coupled, the plates slide past one another more aseismically, and little strain accumulates to be released seismically. The degree of coupling is not a fixed property of a margin; it varies with depth along the interface (developed in §4) and along strike, and it depends on temperature, fluid pressure, and the physical state of the material caught in the fault zone.

### 2.3 Two end-member modes

{cite:t}`UyedaKanamori1979` recognized that subduction zones occupy a continuum between two dynamic end-members, anchored by the contrast between the Chilean and Mariana margins ({numref}`SF2_chilean_mariana`).

```{figure} ../assets/figures/SF2_chilean_mariana.png
:name: SF2_chilean_mariana
:alt: Two cross-section schematics side by side. Left, Chilean type: a young buoyant slab subducts at a shallow ~25 degree angle, strongly coupled to the overriding plate, with the volcanic arc far from the trench, and orange arrows showing back-arc shortening; labeled strong coupling leading to M9. Right, Mariana type: an old dense slab sinks steeply at ~70 degrees, weakly coupled, with the arc close to the trench, and green arrows showing back-arc extension; labeled weak coupling leading to no great earthquakes.
:width: 100%

The two end-member modes of subduction {cite:p}`UyedaKanamori1979`. **(left) Chilean type:** a young, buoyant slab resists sinking and subducts at a shallow angle; it presses against the overriding plate (strong coupling), driving back-arc shortening and building a high mountain arc, and it hosts great ($M\,9$) earthquakes. **(right) Mariana type:** an old, dense slab sinks steeply and rolls back; coupling is weak, the trench retreats, and the back-arc is pulled into extension (active back-arc spreading). Mariana-type margins produce frequent small-to-moderate earthquakes but no recorded great events. Real margins lie on a continuum between these idealizations.
```

The Chilean end-member has a young, buoyant slab, a shallow dip, strong coupling, back-arc shortening (the Andes), and great earthquakes. The Mariana end-member has an old, dense slab, a steep dip, weak coupling, trench rollback, and back-arc extension (active spreading in the Mariana Trough). The continuum between them was the first physically grounded *dynamic* classification of convergent margins, and it remains a useful organizing idea. Its limitation — which the next two sections develop — is that the simple "old/dense/coupled → big earthquakes" expectation does not survive contact with the global earthquake record.

---

## 3. Mathematical Framework

### 3.1 Notation

```{admonition} Notation
:class: important

| Symbol | Meaning | Typical value / units |
|--------|---------|------------------------|
| $A$ | Age of incoming plate at the trench | $0$–$170$ Ma |
| $v_c$ | Convergence rate (trench-normal) | $0$–$240$ mm/yr |
| $\delta$ | Slab dip (deep) | $10$–$80^\circ$ |
| $\Phi$ | Thermal parameter | km (defined below) |
| $h_s$ | Trench sediment thickness | $0$–$4$ km |
| $W$ | Seismogenic-zone downdip width | $50$–$200$ km |
| $L$ | Along-strike rupture length | up to $\sim 1500$ km |
| $\bar{D}$ | Average coseismic slip | m |
| $\mu$ | Shear modulus of fault-zone rock | $\sim 30$–$50$ GPa |
| $M_0$ | Seismic moment | N·m |
| $M_w$ | Moment magnitude | dimensionless |
```

```{admonition} A note on convergence rate
:class: note
The subduction literature, and the classification figures of this lecture, report the *trench-normal* convergence rate in an *absolute* (hotspot, HS3-NUVEL1A) reference frame rather than the plate-pair *relative* rate defined kinematically in L26 §7.2. The two differ — sometimes greatly. The 2004 Sumatra–Andaman segment, for example, has a trench-normal absolute rate near $3$ mm/yr even though the Indian–Sunda plates approach at several centimetres per year, because much of that motion is oblique and the overriding plate is itself moving. The distinction matters when reading {numref}`SF3_parameter_space`.
```

### 3.2 The thermal parameter

The thermal state of a slab — how cold it remains as it descends — is what couples the three "classic" parameters into a single quantity. A slab stays colder if it is older when it arrives (more accumulated cooling), if it descends faster (less time to reabsorb heat at depth), and if it dips more steeply (it spends less horizontal distance warming up per unit depth). These combine into the *thermal parameter*

$$
\Phi = A \, v_c \, \sin\delta ,
$$ (eq:thermal-parameter)

with $A$ the incoming-plate age, $v_c$ the convergence rate, and $\delta$ the dip. A large $\Phi$ describes a cold slab that penetrates deep before warming; a small $\Phi$ describes a warm slab that equilibrates shallow. The thermal parameter sets the depth of the deepest earthquakes in a slab and the position of the basalt–eclogite transition, and — through temperature-dependent friction — it influences where on the interface the megathrust can store elastic strain.

The thermal parameter is the quantitative heart of the *classic* expectation: large $\Phi$ (old, fast, steep) was supposed to mean strong coupling and great earthquakes. Keep {eq}`eq:thermal-parameter` in mind through §5, where the observed maximum magnitudes are compared against it.

### 3.3 Seismic moment and the geometry of rupture

The size of an earthquake is its seismic moment,

$$
M_0 = \mu \, \bar{D} \, A_{\mathrm{rupture}} = \mu \, \bar{D} \, (L \, W),
$$ (eq:seismic-moment)

the product of the shear modulus, the average slip, and the ruptured fault area, written here as along-strike length $L$ times downdip width $W$. Moment magnitude follows from the moment by the standard relation

$$
M_w = \tfrac{2}{3} \log_{10} M_0 - 6.07 \quad (M_0 \text{ in N·m}).
$$ (eq:moment-magnitude)

Equation {eq}`eq:seismic-moment` reframes the central question in a more useful way. The maximum magnitude a margin can produce is controlled by the maximum fault *area* it can rupture coseismically, multiplied by the slip that area can store. The downdip width $W$ is set by the geometry of the seismogenic zone — the depth range over which the interface is locked and able to store elastic strain — and the along-strike length $L$ is set by how far a rupture can propagate before it runs into a barrier. Neither $L$ nor $W$ is a simple function of plate age or convergence rate. This is the mathematical reason the classic recipe fails: maximum magnitude scales with seismogenic *geometry*, not with the slab's thermal vigour.

```{admonition} Key Equation — what limits the largest earthquake
:class: important

The maximum moment of a subduction zone is set by the largest area it can rupture and the slip that area can hold:
$$
M_0^{\max} = \mu \, \bar{D}^{\max} \, L^{\max} \, W^{\max}.
$$
A wide, long, strongly locked seismogenic zone produces great earthquakes regardless of whether the incoming plate is young or old, fast or slow. The controls on $L^{\max}$ and $W^{\max}$ — interface dip, temperature, sediment, and roughness — are the parameters the modern literature actually uses.
```

---

## 4. The Forward Problem: Predicting Rupture Behaviour with Depth

The forward problem in subduction seismology is to predict, from the structure of a margin, how the megathrust will behave — where it locks, where it slips aseismically, and what kind of earthquake each part can produce. {cite:t}`Lay2012` synthesized the rupture behaviour of recent great earthquakes into a model of four depth-varying domains along the interface ({numref}`SF4_rupture_domains`), and this model organizes the connection between structure and hazard.

```{figure} ../assets/figures/SF4_rupture_domains.png
:name: SF4_rupture_domains
:alt: Cross-section of a subduction megathrust from the trench downdip, with the interface coloured into four domains by depth. Domain A from the trench to 15 km depth (green) is the near-trench domain of tsunami earthquakes and stable sliding, with a blue arrow at the trench showing seafloor uplift driving a tsunami. Domain B from 15 to 35 km (orange) is the central domain of large slip. Domain C from 35 to 55 km (vermillion) is the downdip domain of strong ground motion. Domain D (pink dashed) is a deeper transitional zone of slow slip, tremor, and low-frequency earthquakes.
:width: 100%

The four depth-varying rupture domains of a subduction megathrust {cite:p}`Lay2012`. **Domain A** (trench to $\sim 15$ km): the near-trench domain, where tsunami earthquakes, anelastic deformation, and stable sliding occur, and where the largest *seafloor* slip — and therefore the dominant tsunami source — is generated. **Domain B** ($\sim 15$–$35$ km): the central domain of large coseismic slip with modest short-period radiation; the core of great ruptures. **Domain C** ($\sim 35$–$55$ km): the downdip domain of isolated patches that radiate strong, coherent short-period energy, the dominant source of damaging strong ground motion. **Domain D**: a transitional domain, present mainly where a young, warm slab subducts at shallow dip, hosting slow-slip events, tremor, and low-frequency earthquakes. Produced by ``assets/scripts/fig_28_rupture_domains.py``.
```

The domains carry the lecture's central hazard message. The tsunami threat is largest from shallow slip in domain A, near the trench, where the seafloor is displaced directly upward; the strong-ground-motion threat is largest from domain C, downdip and closer to land. The shallow updip domain has its own distinctive hazard signature: because its weak, fluid-rich, low-rigidity materials radiate seismic energy inefficiently, an event confined to it can slip a great deal yet shake weakly — a *tsunami earthquake*, producing a tsunami far larger than its magnitude would suggest. The 2010 $M\,7.8$ Mentawai event, expected to generate a few metres of run-up, produced up to $16$ m {cite:p}`Wirth2022`. A margin's hazard profile therefore depends on which domains it has and how they are distributed, which in turn depends on its structure. A margin that locks all the way to the trench — so that domain A can rupture in a great earthquake rather than creeping — is a margin capable of a large, trench-breaching, strongly tsunamigenic event. The 2011 Tōhoku earthquake was exactly this: rupture propagated into the shallow domain A and produced tens of metres of slip near the trench, generating the devastating tsunami even though the deeper interface had been thought to set the magnitude ceiling.

The forward problem also explains the link between slab structure and the deeper, intermediate-depth seismicity. Earthquakes within the descending slab define the *Wadati–Benioff zone*, a dipping plane of seismicity that traces the slab to depths of several hundred kilometres in cold (large-$\Phi$) slabs and dies out shallow in warm (small-$\Phi$) slabs. The geometry of that zone — and of the locked seismogenic interface above it — is captured globally by the Slab2 model {cite:p}`Hayes2018`, which is the data product behind {numref}`SF1_global_trenches` and the cross-sections of this lecture.

---

## 5. The Inverse Problem: Inferring Maximum Magnitude — and Where It Fails

The inverse problem is the one the field cares about most and answers least well: given what can be measured about a margin, infer the largest earthquake it can produce. This is where the classic classification meets the data.

The classic framework reaches first for incoming-plate age and convergence rate. {cite:t}`Wirth2022` test that framework directly, correlating the maximum observed magnitude of the global set of $M \geq 8.5$ segments against eight subduction parameters. {numref}`SF3_parameter_space` reproduces the four most telling comparisons — the two parameters the recipe was built on, and the two that the data actually favour.

```{figure} ../assets/figures/SF3_parameter_space.png
:name: SF3_parameter_space
:alt: Four scatter panels of maximum moment magnitude versus a subduction parameter, after Wirth et al. 2022 Table 1 and Figure 3. Top row, the dispelled recipe: panel a, subducting-plate age, shows no correlation (Wirth r = 0.05) with the giant M ≥ 9 earthquakes (vermillion stars) scattered across all ages from Cascadia at 7 Ma to Tohoku at 132 Ma; panel b, trench-normal convergence rate in the HS3-NUVEL1A absolute frame, shows no correlation (r = 0.19) with Sumatra a giant at only 3 mm/yr. Bottom row, the geometric controls: panel c, seismogenic-zone width, shows the strongest correlation (r = 0.44) with every giant above 110 km width and dashed thresholds at 75 km (all M ≥ 8.5) and 150 km (all M ≥ 9.2); panel d, downdip curvature, shows the giants clustering at low curvature, the flatter-ruptures-larger result (|r| = 0.42, Bletery 2016).
:width: 100%

Which parameter controls the maximum earthquake? Maximum observed $M_w$ against four subduction parameters for the well-constrained margin segments of {cite:t}`Wirth2022`, Table 1. **Top row — the recipe the data dispelled. (a)** Plate age: no correlation ($r = 0.05$). The giant ($M \geq 9$) earthquakes (stars) span the full age range — young Cascadia ($7$ Ma), old Tōhoku ($132$ Ma). **(b)** Trench-normal convergence rate (HS3-NUVEL1A absolute frame): no correlation ($r = 0.19$). Sumatra–Andaman is a giant at a trench-normal rate of only $3$ mm/yr. **Bottom row — the geometric controls that hold. (c)** Seismogenic-zone width: the strongest single control ($r = 0.44$). Every giant has a width above $\sim 110$ km; recorded $M \geq 8.5$ events occur only where the width exceeds $75$ km, and $M \geq 9.2$ events only above $150$ km. **(d)** Downdip curvature: the giants cluster at low curvature — flatter megathrusts rupture larger ($|r| = 0.42$; {cite:t}`Bletery2016`). Correlation coefficients are Wirth et al.'s reported Figure 3 values over their full $M \geq 8.5$ data set; the plotted points are the Table 1 segments, so their bare correlation differs slightly. Age, rate, dip, width, and sediment are from the SubMap database ({cite:t}`HeuretLallemand2005`); downdip curvature from {cite:t}`Bletery2016`; $M_w$ from the USGS/Global CMT record. Produced by ``assets/scripts/fig_28_parameter_space.py``.
```

The figure is the inverse problem's verdict. If maximum magnitude were controlled by plate age or convergence rate, the giant earthquakes would track those parameters. They do not: the top row is flat, and the $M \geq 9$ events span the entire range of both — Chile 1960 (young), Cascadia 1700 (young, slow), Sumatra 2004 (old, near-zero trench-normal rate), Tōhoku 2011 (old, fast). The thermal parameter {eq}`eq:thermal-parameter` that combines age, rate, and dip does no better. What *does* order the magnitudes is the bottom row: the **seismogenic-zone width** (the strongest single control) and the **downdip curvature** of the interface. The conclusion is the one stated in §1 — age and convergence rate do not predict the maximum earthquake a margin can host {cite:p}`Wirth2022` — and it points directly at the controls that do.

What does the modern literature put in their place? The parameters that correlate most strongly with magnitude in {cite:t}`Wirth2022` are *geometric* — the ones that govern how far a rupture can propagate, consistent with the moment scaling of {eq}`eq:seismic-moment`:

1. **Seismogenic-zone width and dip — the strongest single control.** A wider, shallower-dipping locked zone offers a larger downdip rupture dimension $W$. The empirical thresholds are sharp: recorded $M \geq 8.5$ earthquakes occur only where the interface dips less than $\sim 35^\circ$ with a seismogenic width greater than $\sim 75$ km, and $M \geq 9.2$ events only where it dips less than $20^\circ$ with width greater than $150$ km — the widest, flattest megathrusts (the narrow, steeply dipping Aleutian arc being a noted exception). Convergence rate enters here *indirectly*: a faster-subducting slab stays colder to greater depth, pushing the downdip brittle–ductile limit farther from the trench and widening the seismogenic zone.
2. **Downdip curvature — planarity of the interface.** The largest earthquakes rupture nearly planar megathrusts; "mega-earthquakes rupture flat megathrusts" {cite:p}`Bletery2016`. Low curvature means the shear strength varies smoothly along dip, so the critical stress is exceeded across a broad, continuous area rather than being arrested at a geometric kink. Downdip curvature shows one of the highest correlations with magnitude in the global compilation.
3. **Secondary controls — sediment, roughness, fluids, upper-plate structure.** A thick, well-consolidated sediment section and a low incoming-plate roughness *smooth* the interface, removing the subducting seamounts and ridges that would otherwise arrest a rupture, and promote a large, homogeneous zone of interseismic coupling. The control is interface *smoothness*, not sediment volume in itself: the $M\,9.1$ Tōhoku margin is sediment-starved yet smooth. Pore-fluid pressure and consolidation state govern whether the shallow interface locks (and can rupture seismically to the trench) or creeps; at Cascadia, along-strike changes in sediment consolidation track along-strike changes in inferred locking {cite:p}`Han2017`.

One caveat accompanies every one of these correlations: the instrumental record (about a century) is far shorter than the earthquake cycle (centuries to millennia), so the statistical power of all of them is low {cite:p}`Wirth2022`. No single parameter is a reliable predictor on its own.

These second-order controls also organize the upper-plate deformation. The deep slab dip — itself related to slab age and buoyancy — governs whether the overriding plate shortens or extends ({numref}`SF5_slabdip_backarc`). That strain regime is in turn correlated with seismic behaviour: margins whose upper plates are *extensional* tend to host fewer great earthquakes, and erosive margins (typically extensional across the marine fore-arc) behave differently from accretionary ones. The correlation is suggestive rather than deterministic — the $M\,9.1$ Sumatra–Andaman rupture extended adjacent to the actively extending Andaman back-arc, a notable counterexample {cite:p}`Wirth2022`.

```{figure} ../assets/figures/SF5_slabdip_backarc.png
:name: SF5_slabdip_backarc
:alt: Scatter plot of deep slab dip (5-90 degrees, x-axis) against a back-arc strain index from shortening (negative) through neutral to extension (positive). Steeply dipping margins above about 50 degrees — Mariana, Tonga, Izu-Bonin, Kermadec — plot in the extension field (green). Shallowly dipping margins below about 30 degrees — Peru flat slab, central Chile, Nankai, Cascadia — plot in the shortening field (vermillion). Dashed vertical lines mark the 30 and 50 degree thresholds.
:width: 100%

Deep slab dip controls the deformation of the overriding plate {cite:p}`Lallemand2005`. Margins with steep deep dip ($> \sim 50^\circ$) tend toward back-arc extension and trench rollback (Mariana, Tonga, Izu–Bonin); margins with shallow deep dip ($< \sim 30^\circ$) tend toward upper-plate shortening (the Andes, the Peru flat slab). The back-arc strain index here is an ordinal teaching simplification; the threshold dips follow {cite:t}`Lallemand2005`. Produced by ``assets/scripts/fig_28_slabdip_backarc.py``.
```

The honest summary of the inverse problem is that there is no single observable that predicts maximum magnitude. The modern working assumption — and it is a sobering one for hazard assessment — is that essentially any mature subduction megathrust should be regarded as capable of a great, $M \sim 9$ earthquake until specific evidence shows otherwise {cite:p}`Wirth2022`. The 2004 and 2011 events were the proof of that principle, and the Pacific Northwest is the place where it matters most to the people reading this.

---

## 6. Worked Example: Classifying Three Margins

The companion notebook ``notebooks/subduction_parameter_space.ipynb`` carries out the full quantitative classification interactively, loading the per-zone table behind {numref}`SF3_parameter_space` and letting the reader reposition any margin and test the correlation. The qualitative version of that exercise, worked here, compares three margins that occupy very different parts of the parameter space yet have all produced — or are expected to produce — great earthquakes.

> **Chile (Maule segment).** Incoming plate $\sim 33$ Ma, converging fast ($\sim 68$ mm/yr) at a shallow dip; strongly coupled; back-arc shortening builds the Andes. This is the Chilean end-member of §2.3 — and it behaves as the classic recipe expects, hosting the 2010 $M\,8.8$ and the 1960 $M\,9.5$, the largest instrumentally recorded earthquake.
>
> **Mariana.** Incoming plate very old ($\sim 155$ Ma) but converging slowly ($\sim 35$ mm/yr) at a steep dip; weakly coupled; back-arc extension opens the Mariana Trough. The classic recipe, weighting old age heavily, would have flagged this as a great-earthquake candidate. It is not: no great earthquake has been recorded here. The steep dip and weak coupling give it a narrow seismogenic width $W$, and {eq}`eq:seismic-moment` limits the moment accordingly.
>
> **Cascadia.** Incoming plate young ($< 15$ Ma), converging slowly ($\sim 35$–$45$ mm/yr); warm slab; thick sediment; no bathymetric trench. By the classic recipe — young and slow — this is the *least* likely place for a great earthquake. Yet the paleoseismic record shows it produced an $M \sim 9$ in 1700, and it is the focus of §9.

The three margins make the lesson concrete: Chile fits the old recipe, Mariana breaks it in one direction (old but no great earthquakes), and Cascadia breaks it in the other (young but $M\,9$-capable). A classification scheme that cannot accommodate all three is not describing the controlling physics.

---

## 7. Course Connections

```{admonition} Where this lecture connects
:class: seealso

- **L26 §7 (Plate Boundaries and Relative Motion):** This lecture is the convergent case of the kinematic classification. The convergence rate $v_c$ used throughout is the relative-velocity magnitude defined there; the Mendocino triple junction worked in L26 §7.4 places the northern end of the Cascadia margin, and the subduction-polarity point made there is why §2.1 must invoke buoyancy, not kinematics, to say which plate descends.
- **L04–L07 (Seismic waves):** Wadati–Benioff seismicity (§4) is located by the travel-time methods developed there.
- **L13–L16 (Earthquake source):** The megathrust is a thrust fault; its focal mechanism, moment {eq}`eq:seismic-moment`, and magnitude {eq}`eq:moment-magnitude` are the source quantities introduced there.
- **L16–L17 (Ground motions and tsunamis):** The domain-A tsunami source and domain-C strong-motion source of {numref}`SF4_rupture_domains` are the inputs to the hazard methods of those lectures.
- **L27 (Ridges and Rifts):** The divergent counterpart — where the oceanic lithosphere that arrives at these trenches was born.
- **L29 (Transforms & Intraplate):** The third boundary class, and the breakdown of the rigid-plate assumption that circuit closure (L26 §7.4) depends on.
- **L30 (Plate Tectonics and Geodynamics):** Slab pull (§2.1) is the dominant term in the global force and heat budget assembled in the capstone.
```

---

## 8. Research Horizon

The study of great subduction earthquakes is in an unusually active phase, driven by the well-recorded giants of 2004, 2010, and 2011 and by new offshore instrumentation. Three open-access entry points:

1. **{cite:t}`Wirth2022`**, *Nature Reviews Earth & Environment* — the synthesis that frames this lecture. It documents the failure of the age/convergence-rate hypotheses and reviews the rupture characteristics (seaward and landward extent, strong-motion-generating areas, recurrence) that actually govern hazard. Open access through the USGS Publications Warehouse.

2. **{cite:t}`LayNishenko2022`**, *PNAS* — updates the concepts of seismic gaps and asperities along South America, where the long earthquake record makes it possible to ask how repeatable great ruptures are. A useful counterpoint to the "any margin can do it" conclusion: long-term plate-boundary strain budgets do impose a degree of cyclicity. Palaeoseismic archives — coral microatolls in Sumatra, turbidite sequences and drowned soils in Cascadia — reveal that recurrence is rarely simple: many margins show *supercycles*, clusters of differently sized ruptures separated by long quiet intervals, rather than clockwork repetition. The 2010 Maule earthquake filled a recognized seismic gap last ruptured in 1835. Open access.

3. **{cite:t}`Biemiller2024`**, *JGR Solid Earth* — examines how megathrust geometry (dip and seismogenic width) shapes maximum magnitude and recurrence, part of the modern shift toward geometry-based controls.

```{admonition} Open research question
:class: note

*If essentially any mature megathrust can host an $M\,9$, what observable — geometry, sediment, fluid pressure, or something not yet identified — most sharply distinguishes the segments that will from those that will not?* Offshore geodesy and seafloor seismology at Cascadia (§9) are being deployed to answer exactly this, and the answer will reshape hazard maps for the Pacific Northwest.
```

---

## 9. Societal Relevance: Cascadia, the M9-Capable "Exception"

The Cascadia subduction zone runs offshore from northern California to southern British Columbia, directly west of every student reading this. The Juan de Fuca plate — born at the ridge of L26, young and warm by the time it reaches the margin — descends beneath North America at $\sim 35$–$45$ mm/yr ({numref}`SF6_cascadia_section`).

```{figure} ../assets/figures/SF6_cascadia_section.png
:name: SF6_cascadia_section
:alt: West-to-east cross-section of the Cascadia subduction zone. The young, warm Juan de Fuca plate (blue) moves east at 35-45 mm/yr and descends beneath North America. A thick orange sediment layer rides on the incoming plate; there is a buried deformation front with no bathymetric trench and a large accretionary wedge. The megathrust interface is marked as a locked seismogenic zone (the 1700 M9 rupture) updip and an episodic-tremor-and-slip zone downdip, with the Cascade arc volcano to the east. A call-out box notes that Cascadia is young, slow, sediment-rich, and smooth — the opposite of the old big-earthquake recipe — yet is M9-capable.
:width: 100%

Cascadia subduction zone cross-section: the $M\,9$-capable "exception." The young ($< 15$ Ma), warm Juan de Fuca slab, the slow convergence, the thick incoming sediment, the buried deformation front with no bathymetric trench, and the unusually smooth interface are every ingredient the classic recipe says should produce only modest earthquakes. The paleoseismic record says otherwise: the megathrust is locked, and it produced an $M \sim 9$ in January 1700. Episodic tremor and slip (ETS) occupies the deep transition (domain D of {numref}`SF4_rupture_domains`). Schematic after {cite:t}`WangTrehu2016`; geometry consistent with Slab2 {cite:p}`Hayes2018`. Produced by ``assets/scripts/fig_28_cascadia_section.py``.
```

By the parameters of the classic recipe — young, slow — Cascadia is the *last* place one would expect a great earthquake. By the modern controls it is one of the most concerning margins on Earth. Its geometry alone places it firmly in great-earthquake territory: {cite:t}`Wirth2022` give it a seismogenic width of $127$ km and a shallow interface dip of $11^\circ$ — comfortably past the $>75$ km / $<35^\circ$ threshold for $M \geq 8.5$, and a smooth, near-planar megathrust. The thick, well-consolidated sediment smooths the interface further and may allow rupture to propagate the full $\sim 1000$ km length of the margin and breach the trench, the two ingredients (large $L$, shallow domain-A slip) that produce a long, strongly tsunamigenic rupture {cite:p}`WangTrehu2016, Han2017`. The evidence that this has happened is unambiguous: the January 1700 earthquake is dated to the night of 26 January 1700 by the tsunami it sent across the Pacific to Japan {cite:p}`Satake2003`, and recorded along the Cascadia margin by drowned forests and by the offshore turbidites it shook loose.

The practical message for a Pacific Northwest resident in 2026 is the lecture's thesis made local. The framework that says "old and fast means dangerous" would have rated Cascadia low. The framework built in this lecture — maximum magnitude set by seismogenic geometry and interface smoothness, not by slab age — rates it among the most hazardous, capable of an $M\,9$ megathrust earthquake and an accompanying near-field tsunami with little warning. The classification that data dispelled was not an academic curiosity; getting it wrong would mean preparing for the wrong earthquake.

---

## AI Literacy: Epistemics — Catching the Confident, Outdated Answer

```{admonition} AI Prompt Lab — what controls the maximum earthquake size?
:class: tip

A prompt to try with an AI assistant:

> *What controls the maximum earthquake magnitude a subduction zone can produce? Explain how plate age and convergence rate determine the largest possible earthquake.*

Notice that the prompt itself contains the obsolete assumption — that age and rate are the controls. A capable assistant may accept the premise and produce a fluent, confident explanation of the Ruff–Kanamori relationship, complete with the physical reasoning of §2.1, and never mention that the hypothesis was dispelled by the 2004 and 2011 earthquakes.

**Your task: grade the response against the rubric below.**

| Criterion | Pass | Fail |
|-----------|------|------|
| Does the response challenge the premise of the question? | flags that age/rate do not control $M_{\max}$ | accepts the premise uncritically |
| Does it cite the falsifying evidence? | names Sumatra 2004 and/or Tōhoku 2011 | presents the 1980 recipe as current |
| Does it give the modern controls? | seismogenic geometry, smoothness/sediment, fluids | offers only age and rate |
| Is it appropriately uncertain? | notes that any mature megathrust may be $M\,9$-capable | states a confident, deterministic rule |

This is the most important AI-literacy exercise in Module 7, because it is the failure mode you are *least* likely to catch: the answer is fluent, internally consistent, physically reasonable, and wrong only because the science moved. An assistant trained on decades of literature will have seen the dispelled hypothesis stated as fact thousands of times. The defence is not better prompting — it is domain knowledge. You catch this error because you read {numref}`SF3_parameter_space`, not because the AI flagged it. The lesson of the lecture and the lesson of the prompt lab are the same: a confident, well-formed explanation can encode a hypothesis the data have already overturned.
```

---

## Further Reading

Open-access references preferred; all linkable:

- **Wirth, E. A., Sahakian, V. J., Wallace, L. M. & Melnick, D.** (2022). The occurrence and hazards of great subduction zone earthquakes. *Nature Reviews Earth & Environment* 3, 125–140. DOI: [10.1038/s43017-021-00245-w](https://doi.org/10.1038/s43017-021-00245-w). Open access via the USGS Publications Warehouse.
- **Lay, T., Kanamori, H., Ammon, C. J., et al.** (2012). Depth-varying rupture properties of subduction zone megathrust faults. *JGR Solid Earth* 117, B04311. DOI: [10.1029/2011JB009133](https://doi.org/10.1029/2011JB009133).
- **Bletery, Q., Thomas, A. M., Rempel, A. W., et al.** (2016). Mega-earthquakes rupture flat megathrusts. *Science* 354, 1027–1031. DOI: [10.1126/science.aag0482](https://doi.org/10.1126/science.aag0482) — the controlling role of megathrust curvature.
- **Hayes, G. P., Moore, G. L., Portner, D. E., et al.** (2018). Slab2, a comprehensive subduction zone geometry model. *Science* 362, 58–61. DOI: [10.1126/science.aat4723](https://doi.org/10.1126/science.aat4723). Data release (public domain): [10.5066/F7PV6JNV](https://doi.org/10.5066/F7PV6JNV).
- **Lay, T. & Nishenko, S. P.** (2022). Updated concepts of seismic gaps and asperities to assess great earthquake hazard along South America. *PNAS* 119, e2216843119. DOI: [10.1073/pnas.2216843119](https://doi.org/10.1073/pnas.2216843119). Open access.
- **Straume, E. O., Gaina, C., Medvedev, S., et al.** (2019). GlobSed: Updated total sediment thickness in the world's oceans. *Geochem. Geophys. Geosyst.* 20, 1756–1772. DOI: [10.1029/2018GC008115](https://doi.org/10.1029/2018GC008115). Data via NOAA NCEI.
- **Wang, K. & Tréhu, A. M.** (2016). Invited review paper: Some outstanding issues in the study of great megathrust earthquakes — the Cascadia example. *Journal of Geodynamics* 98, 1–18. DOI: [10.1016/j.jog.2016.03.010](https://doi.org/10.1016/j.jog.2016.03.010).
- **Uyeda, S. & Kanamori, H.** (1979). Back-arc opening and the mode of subduction. *JGR Solid Earth* 84, 1049–1061. DOI: [10.1029/JB084iB03p01049](https://doi.org/10.1029/JB084iB03p01049).

---

```{admonition} Concept checks
:class: note

Try these before the next class meeting; we will go over them in discussion.

1. **Thermal parameter.** Compute $\Phi = A\,v_c\,\sin\delta$ for (a) Tōhoku ($A = 130$ Ma, $v_c = 83$ mm/yr, $\delta = 15^\circ$ shallow interface) and (b) Mariana ($A = 155$ Ma, $v_c = 35$ mm/yr, $\delta = 60^\circ$). Which slab is "colder" by this measure? Does the colder slab host the larger earthquakes? What does your answer say about $\Phi$ as a predictor of $M_{\max}$?
2. **Moment and area.** Using {eq}`eq:seismic-moment` and {eq}`eq:moment-magnitude` with $\mu = 40$ GPa, estimate the rupture area needed for an $M_w\,9.0$ earthquake assuming an average slip of $\bar{D} = 15$ m. If the seismogenic zone is $W = 100$ km wide, how long along strike must the rupture be? Compare to the length of the Cascadia margin.
3. **Reading the parameter space.** Using {numref}`SF3_parameter_space`, explain why seismogenic-zone width is a better predictor of $M_{\max}$ than plate age or convergence rate. State the two geometric thresholds (a dip and a width) that no recorded $M \geq 9.2$ earthquake has violated, and name the margin that is the noted exception to the width rule.
4. **Cascadia hazard.** Cascadia is young and slow. State, in two or three sentences, why it is nonetheless regarded as capable of an $M\,9$ earthquake, citing its seismogenic width and interface smoothness from §5 and §9.
5. **AI epistemics.** Run the AI Prompt Lab prompt above with an assistant of your choice. Did it accept the obsolete premise? Quote the sentence where it either challenged or accepted the age/rate assumption, and grade it against the rubric.
```

::::{admonition} A note on sensitive content
:class: warning
This lecture discusses earthquake and tsunami hazards that have caused large loss of life, including events within living memory. The intent is scientific and preparedness-oriented. Students in the Pacific Northwest who find the Cascadia hazard distressing may find it helpful to channel that concern into preparedness resources from the Washington Emergency Management Division and the Pacific Northwest Seismic Network.
::::
