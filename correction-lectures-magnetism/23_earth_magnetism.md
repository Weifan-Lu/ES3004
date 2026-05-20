---
title: "Earth's Magnetic Field — Fundamentals, the Geodynamo, and Space Weather"
subtitle: "What the field is, where it comes from, and why it protects us"
short_title: "Earth Magnetism"
week: 9
lecture: 23
date: "2026-06-01"
topic: "Magnetism I — fundamentals, the geodynamo, and space weather"
course_lo: ["LO-1", "LO-2", "LO-4"]
learning_outcomes: ["LO-OUT-A", "LO-OUT-C"]
open_sources:
  - "Lowrie & Fichtner (2020), Fundamentals of Geophysics, 3rd ed., Ch. 5.1–5.3 (UW Libraries e-book)"
  - "IGRF-13 model and field calculator: NOAA NCEI / IAGA (public domain, https://www.ngdc.noaa.gov/IAGA/vmod/igrf.html)"
  - "NOAA World Magnetic Model 2025 (public domain, https://www.ncei.noaa.gov/products/world-magnetic-model)"
  - "NASA Space Weather Mission resources (public domain, https://svs.gsfc.nasa.gov/)"
  - "NOAA Space Weather Prediction Center (public domain, https://www.swpc.noaa.gov/)"
keywords: [geomagnetism, geodynamo, declination, inclination, IGRF, WMM, dipole, susceptibility, magnetosphere, space weather, geomagnetic storm, secular variation, paleolatitude]
---

# Earth's Magnetic Field: Fundamentals, the Geodynamo, and Space Weather

:::{seealso}
📊 **Lecture slides** — <a href="https://uw-geophysics-edu.github.io/ess314/slides/lecture_23_slides.html" target="_blank">open in new tab ↗</a>
:::

::::{dropdown} Learning Objectives
:color: primary
:icon: target
:open:

By the end of this lecture, students will be able to:

- **[LO-23.1]** Define the magnetic field $\mathbf{B}$, the magnetising field $\mathbf{H}$, the magnetisation $\mathbf{M}$, and the magnetic susceptibility $\chi$, and write the constitutive relation $\mathbf{B} = \mu_0(\mathbf{H} + \mathbf{M}) = \mu_0(1+\chi)\mathbf{H}$ for a linear medium.
- **[LO-23.2]** Draw the parallel between the gravitational and magnetic potentials in source-free regions ($\mathbf{g} = -\nabla\Phi$; $\mathbf{H} = -\nabla\Psi$) and explain why the magnetic dipole — not the monopole — is the simplest physical source of a magnetic field.
- **[LO-23.3]** Decompose the geomagnetic field vector at a station into declination $D$, inclination $I$, and total intensity $F$, and convert between $(D, I, F)$ and the local $(X, Y, Z)$ Cartesian components.
- **[LO-23.4]** Identify the three principal sources of the surface field — core (geodynamo), lithosphere, and ionosphere — locate them in their physical context, and assign each source a characteristic spatial wavelength range.
- **[LO-23.5]** Describe the secular variation of the field, including the drift of the north magnetic pole and the occurrence of geomagnetic jerks; explain in qualitative terms how the magnetosphere shields the Earth from solar-wind plasma and what happens during a geomagnetic storm.
- **[LO-23.6]** Apply the geocentric axial dipole equation $\tan I = 2 \tan \lambda$ as a forward problem (predict $I$ given $\lambda$) and as an inverse problem (estimate $\lambda$ with propagated uncertainty given a measured $I$).

::::

::::{dropdown} Syllabus Alignment
:color: secondary
:icon: list-task

| | |
|---|---|
| **Course LOs addressed** | LO-1 (observables ↔ Earth properties), LO-2 (forward model from source physics to surface field), LO-4 (method strengths, limitations, and uncertainty) |
| **Learning outcomes practiced** | LO-OUT-A (predict surface signature from a simple source model), LO-OUT-C (interpret a measurement as a constraint on subsurface structure with appropriate uncertainty) |
| **Prior lecture** | [L22 — Density and the Lithosphere](22_density_lithosphere.md) |
| **Next lecture** | [L24 — Rock Magnetism: How Rocks Remember the Field](24_rock_magnetism.md) |
| **Lab connection** | Companion notebook `magnetics_forward.ipynb` — (D, I, F) decomposition, IGRF/WMM evaluation at a station, GAD paleolatitude. Full anomaly inversion deferred to Lab 8 (covered in L25). |
| **Textbook** | Lowrie & Fichtner (2020), Ch. 5.1–5.3 |

::::

## Prerequisites

Students should be comfortable with the vector calculus introduced in the gravity module (Lectures 18–22) — in particular, the idea that a scalar potential generates a vector field by gradient ($\mathbf{g} = -\nabla\Phi$), and that surface measurements can be projected onto local Cartesian components. Familiarity with the inverse-square law and with the analytical structure of a forward problem (parameter → observable) from gravity will transfer directly. No prior exposure to electromagnetism beyond an introductory-physics treatment of a bar magnet is required.

---

## 1. The Geoscientific Question

```{epigraph}
A compass needle in Seattle today points 15.5° east of true north.
In 1955 it pointed 22.1° east. The asphalt of Seattle-Tacoma's main
runway was repainted in 2019 to keep its name, "16R", honest.
```

A pilot lining up on runway 16R at Seattle-Tacoma International Airport is flying along a heading numbered to match Earth's magnetic field. The number "16" means the runway points along magnetic bearing 160°. That number has to be repainted every decade or two, because the magnetic field at Seattle is not static: its declination — the horizontal angle between magnetic north and true (geographic) north — has decreased from about +22° in 1955 to about +15.5° in 2026. KSEA's main runway was renamed from 16L/34R to 16R/34L in 2019 to keep up with this drift. Anchorage, Fairbanks, and several other airports in the high latitudes have done the same.

The same drift, plotted globally rather than at one airport, makes the more general point ({numref}`fig-declination-world`). Declination varies smoothly across the planet, reaching values of +25° or more in eastern Russia and −20° in the eastern Pacific, and the entire pattern shifts measurably from one five-year IGRF epoch to the next. A planetary-scale physical quantity changes fast enough — on human timescales — to alter aviation infrastructure, navigation systems, and pipeline routing.

```{figure} ../assets/figures/fig_declination_world_map.png
:name: fig-declination-world
:alt: World map of magnetic declination for epoch 2025, Mercator projection, contours at 5-degree intervals, with positive declination (east of true north) and negative declination distinguished by colour and linestyle. Seattle, Anchorage, London, and Tokyo are marked with their current declination values.
:width: 100%

Magnetic declination for epoch 2025.0 from the NOAA World Magnetic Model (WMM-2025). Contours of declination are drawn at 5° intervals; positive declination (compass points east of true north) is shown as solid blue lines, negative declination (compass points west) as dashed vermilion lines, and the agonic line (zero declination) as a heavy black line. Four reference cities are annotated with their current declination. Data: NOAA NCEI / CIRES, US Government, public domain.
```

<!--
FIGURE BRIEF — fig_declination_world_map (Phase 2 build)
  Script: assets/scripts/fig_declination_world_map.py
  Data source: NOAA NCEI WMM-2025 declination grid (or compute on the fly with pyIGRF)
    URL: https://www.ncei.noaa.gov/products/world-magnetic-model
    license: public domain (US Government work)
  Stack: matplotlib + cartopy (PlateCarree projection truncated to ±70° lat) OR matplotlib + scipy
  Required:
    - Colours: solid blue (#0072B2) for D > 0, dashed vermilion (#D55E00) for D < 0, heavy black for D = 0
    - Contour interval 5°, label every 10°
    - Annotate Seattle (47.65°N, 122.30°W, D = +15.5°),
      Anchorage (61.22°N, 149.90°W, D = +16°),
      London (51.50°N, 0.13°W, D = +1°),
      Tokyo (35.68°N, 139.65°E, D = −8°)
    - mpl.rcParams: base font 13pt; savefig 300dpi
    - ADA: alt text describes the figure independently of colour
-->

Four observations frame this lecture:

1. The field has a dominantly **dipolar** geometry, with its axis tilted about 11° from the rotation axis. The dipole is the simplest geometry that any divergence-free vector field can take — a fundamental consequence of $\nabla \cdot \mathbf{B} = 0$.
2. The field has multiple **sources**, with very different spatial scales and very different physical mechanisms operating at depths from thousands of kilometres below the surface to hundreds of kilometres above it.
3. The field **drifts** — measurably, year by year — and occasionally reverses polarity altogether on the geologic timescale.
4. The field **shields** the planet. A web of currents in the ionosphere and magnetosphere — themselves powered by the dipole's interaction with the solar wind — deflects the bulk of incoming solar-particle radiation away from the atmosphere and the surface. Without this shield, Earth would be substantially more like Mars.

This lecture works through these four points in order: what the field *is* (§2), where it is *measured* and *comes from* (§3–§4), how it *drifts* (§5), how it *shields* (§6), and what it lets us *read backward* in geologic time (§7). The complementary story — how rocks acquire and record the field — is the subject of the next lecture.

## 2. What is magnetism? The fundamentals

Before locating sources or interpreting measurements, the basic vocabulary of magnetism needs to be in place: what the magnetic force law looks like, what we mean by "the magnetic field" at a point in space, and how the field inside a material differs from the field that drives it.

### 2.1 The magnetic force and the absence of monopoles

In Coulomb's electrostatics, two point charges separated by distance $r$ exert on one another a force of magnitude $F = q_1 q_2 / (4\pi\varepsilon_0 r^2)$, with charge an *intrinsic* property of matter. By analogy, the force between two magnetic poles of strengths $p_1$ and $p_2$ separated by $r$ can be written

```{math}
:label: eq-magnetic-coulomb
F = \frac{1}{4\pi\mu_0}\,\frac{p_1 p_2}{r^2},
```

with the constant $\mu_0 = 4\pi \times 10^{-7}\,\mathrm{T\,m\,A^{-1}}$ being the *permeability of free space*. (The reciprocal placement of $\mu_0$ relative to $\varepsilon_0$ is a convention of SI units; the inverse-square form is the physics.) Equation [](#eq-magnetic-coulomb) is useful for intuition and for some textbook derivations, but it has a fatal physical flaw: **isolated magnetic poles do not exist**. Every magnetic source ever observed is at least a *dipole* — a pair of equal and opposite poles inseparably bound together. Cut a bar magnet in half and you do not get a north pole and a south pole; you get two smaller bar magnets, each with both poles. Maxwell's second equation makes this exact: 

```{math}
:label: eq-no-monopole
\nabla \cdot \mathbf{B} = 0.
```

The magnetic field has no sources or sinks. Lines of $\mathbf{B}$ have no beginning and no end; they form closed loops. This is the most consequential single fact in magnetism, and it has a direct geometric consequence: the simplest possible magnetic field around a localised source is the field of a *dipole* — not, as for gravity, the field of a monopole. Earth's field is dipolar at first order because *every* magnetic field, far enough from its source, is dipolar.

### 2.2 Field and potential — the analogy with gravity

In a region containing no electric currents, the magnetic field $\mathbf{H}$ can be written as the gradient of a *magnetic scalar potential* $\Psi$:

```{math}
:label: eq-magnetic-potential
\mathbf{H} = -\nabla \Psi, \qquad \nabla^2 \Psi = 0 \quad (\text{in source-free region}).
```

This is structurally identical to the gravity case from Module 5, where the gravitational acceleration $\mathbf{g}$ is the gradient of a scalar potential $\Phi$ satisfying Laplace's equation outside the source distribution. {numref}`fig-field-potential-analogy` summarises the parallel.

```{figure} ../assets/figures/fig_field_potential_gravity_analogy.png
:name: fig-field-potential-analogy
:alt: Two-column visual comparison of gravity (left) and magnetism (right). The gravity column shows a point mass at depth, scalar gravitational potential isolines as concentric circles, gravitational acceleration vectors pointing radially inward, and the relations g = minus grad Phi, divergence of g equals minus 4 pi G rho, curl of g equals 0. The magnetism column shows a point magnetic dipole at depth, scalar magnetic potential isolines as the standard dipole pattern with two lobes, magnetic field vectors curving from north pole around to south pole, and the relations H = minus grad Psi (current-free regions), divergence of B equals 0, curl of H equals J (current density).
:width: 100%

The gravity–magnetism analogy in source-free regions. **Left:** gravity. A point mass at depth generates a scalar potential $\Phi$ whose isolines are concentric spheres; the gravitational acceleration $\mathbf{g} = -\nabla\Phi$ points radially inward toward the mass. Gravity has *sources* (positive mass) but no sinks; the divergence of $\mathbf{g}$ is non-zero where mass is present. **Right:** magnetism. A point magnetic dipole at depth generates a scalar potential $\Psi$ whose isolines trace the two-lobe dipole pattern; the magnetising field $\mathbf{H} = -\nabla\Psi$ curves from one pole around to the other. Because magnetic monopoles do not exist, $\nabla \cdot \mathbf{B} = 0$ everywhere — magnetic field lines form closed loops. Both potentials satisfy Laplace's equation in the source-free region above the source, which means the gravity-field machinery (continuation, harmonic analysis, half-width depth rules) transfers directly to magnetism.
```

<!--
FIGURE BRIEF — fig_field_potential_gravity_analogy (Phase 2 build)
  Script: assets/scripts/fig_field_potential_gravity_analogy.py
  Type: Python schematic (two-panel, matplotlib only — no data)
  Required:
    - Left panel: point mass marker, contour isolines for 1/r potential (concentric), 
      vector arrows g pointing radially inward, equations in text box at bottom
    - Right panel: dipole marker (small arrow), contour isolines for cos θ / r² potential
      (two-lobe pattern), vector arrows H tangent to lines of force, equations in text box
    - Colours: gravity uses single-colour scheme (sky blue #56B4E9); 
      magnetism uses dipole convention (red for north pole half, blue for south pole half)
    - Both panels same dimensions, common scale bar
    - Equations rendered with matplotlib mathtext or saved as separate SVG insert
  Pedagogical goal: students see at a glance that the two columns are structurally identical,
  except (i) gravity has monopoles and magnetism does not, and (ii) magnetism has a Maxwell
  fourth equation (curl H = J) with no gravity analog.
-->

The analogy is structural, not exact. Two differences matter:

- **Magnetism has a fourth equation**: Ampère's law in its static form, $\nabla \times \mathbf{H} = \mathbf{J}$, where $\mathbf{J}$ is the electric current density. In regions where currents flow — inside the outer core, in the ionosphere, in a wire carrying current — the magnetic field is *not* derivable from a scalar potential. Gravity has no such complication: the gravitational force has zero curl everywhere.
- **Magnetism has no monopoles**, as already noted. The simplest magnetic source is a dipole; the simplest gravitational source is a point mass.

In the source-free atmosphere and lithosphere above the dynamo and below the ionosphere — the *crustal magnetics window* — the scalar-potential framework holds. Everything we learned in the gravity module about how a buried source projects to the surface, how to continue measurements upward or downward, and how to bound source depth from the spatial wavelength of an anomaly, transfers wholesale into magnetics. The new ingredients are the dipole geometry of the source and the vector character of the response.

### 2.3 The dipole field

A magnetic dipole of moment $\mathbf{m}$ (units: A m²) located at the origin generates, in spherical coordinates $(r, \theta)$ with $\theta$ measured from the dipole axis, the field components

```{math}
:label: eq-dipole-field
B_r = \frac{\mu_0 m}{4\pi r^3}\,2\cos\theta,
\qquad
B_\theta = \frac{\mu_0 m}{4\pi r^3}\,\sin\theta.
```

Three features matter ({numref}`fig-dipole-big`):

1. The field strength falls off as $1/r^3$ — faster than the $1/r^2$ of a gravitational monopole. Magnetic anomalies are therefore *more localised* than gravity anomalies for sources of similar depth.
2. The radial component $B_r$ is *twice* the tangential component $B_\theta$ at the same colatitude. This factor of two is what produces the factor of two in the paleolatitude equation in §7.
3. The field is *axisymmetric* about the dipole axis. The full three-dimensional pattern is generated by rotating {numref}`fig-dipole-big` about the vertical axis.

```{figure} ../assets/figures/fig_dipole_big.png
:name: fig-dipole-big
:alt: Large single-panel meridional cross-section of a magnetic dipole. A small bar magnet sits at the centre of a sphere. Curved field lines emerge from the magnetic north pole (top), arch outward through space, and curve back to enter the magnetic south pole (bottom). Lines are densest near the poles, sparsest at the equatorial plane. Arrows on each field line show direction. A small inset diagram at the lower right shows the local breakdown of the field vector at one point on the surface into a radial component B_r equal to (mu_0 m / 4 pi r cubed) times 2 cos theta and a tangential component B_theta equal to (mu_0 m / 4 pi r cubed) times sin theta, with theta measured from the dipole axis.
:width: 90%

The magnetic field of a centred dipole in meridional cross-section. Field lines emerge from the north pole, arch through space, and re-enter at the south pole; they form closed loops because $\nabla \cdot \mathbf{B} = 0$. The field intensity falls off as $1/r^3$. At any point on the surface, the field has a radial component $B_r = (\mu_0 m / 4\pi r^3)\,2\cos\theta$ and a tangential component $B_\theta = (\mu_0 m / 4\pi r^3)\,\sin\theta$. Earth's surface field is dipolar to a first approximation, with the dipole axis tilted about 11° from the rotation axis.
```

<!--
FIGURE BRIEF — fig_dipole_big (Phase 2 build)
  Script: assets/scripts/fig_dipole_big.py
  Type: Python schematic, single big panel — replaces the cramped 3-panel fig_dipole_field_geometry
  Required:
    - Compute analytical dipole field on a meshgrid, plot streamlines via matplotlib streamplot
    - Sphere at centre with N/S poles labelled (geographic convention: N at top)
    - 12-16 field lines, arrowheads showing direction
    - Inset at lower right showing decomposition into B_r and B_θ at one example point on the sphere
    - Colours: field lines in primary black (#000000); inset arrows in blue (#0072B2) for B_r and orange (#E69F00) for B_θ
    - Panel dimensions ~ 8 × 6 inches; large enough to project clearly in lecture hall
    - Reference: visually analogous to user-provided Image 2, but cleaner, labelled, and ADA-compliant
    - mpl.rcParams: base font 13pt; savefig 300dpi
-->

The dipole moment $\mathbf{m}$ encapsulates everything about the source: its magnitude, its orientation, and its sign. Doubling $m$ doubles the field everywhere; reversing $m$ reverses the field everywhere. Earth's main field has $|m| \approx 8 \times 10^{22}$ A m² at present epoch; for context, a refrigerator magnet has $|m| \approx 10^{-2}$ A m².

### 2.4 Matter responds: M, χ, and the constitutive relation

So far, $\mathbf{H}$ has been treated as if it were the only magnetic field in play. In matter, two related but distinct fields coexist:

- $\mathbf{H}$ — the **magnetising field**, with units A m⁻¹. This is the *applied* field, the field that exists *because of* the external sources (currents in the geodynamo, the dipole moment of a buried body, etc.).
- $\mathbf{M}$ — the **magnetisation**, with units A m⁻¹. This is the *response* of the material to $\mathbf{H}$: the volumetric density of induced and intrinsic atomic dipole moments inside the material.
- $\mathbf{B}$ — the **magnetic flux density** (or simply, the "magnetic field" in modern usage), with units T (tesla; $1\,\mathrm{T} = 10^{-9}\,\mathrm{nT}^{-1}$ — geophysical fields are reported in nanoteslas). This is the field that *physically deflects a moving charge* and that *a magnetometer measures*. It includes both the applied field and the material response.

The three are tied together by the **constitutive relation**

```{math}
:label: eq-constitutive
\mathbf{B} = \mu_0(\mathbf{H} + \mathbf{M}).
```

For most rocks and minerals at Earth's ambient field strength, the response is *linear*: the magnetisation is proportional to the applied field, with a dimensionless proportionality constant called the **magnetic susceptibility** $\chi$:

```{math}
:label: eq-linear-response
\mathbf{M} = \chi \mathbf{H}.
```

Combining [](#eq-constitutive) and [](#eq-linear-response) gives the effective permeability relation,

```{math}
:label: eq-permeability
\mathbf{B} = \mu_0 (1 + \chi) \mathbf{H} = \mu \mathbf{H},
```

where $\mu \equiv \mu_0(1+\chi)$ is the material's permeability. {numref}`fig-BHM-constitutive` lays out the two basic regimes — diamagnetic ($\chi < 0$) and paramagnetic ($\chi > 0$) — and shows how the induced dipoles inside the material orient relative to the applied field in each case. A *third* regime, in which the material carries a permanent magnetisation even when $\mathbf{H} = 0$ (the *remanent* regime), is the subject of Lecture 24.

```{figure} ../assets/figures/fig_BHM_constitutive.png
:name: fig-BHM-constitutive
:alt: Two-panel figure illustrating the linear-media constitutive relation for magnetic materials. The left panel shows a diamagnet: an applied field H points upward, and inside the material small dipoles align downward (opposite to H), producing a magnetisation M that points opposite to H. A textbox shows chi less than zero. The right panel shows a paramagnet: an applied field H points upward, and small dipoles inside the material align upward (parallel to H), producing M parallel to H. A textbox shows chi greater than zero. Below both panels is the derivation B equals mu zero times the quantity H plus M, equals mu zero times the quantity one plus chi times H, equals mu times H.
:width: 100%

The linear-media constitutive relation $\mathbf{B} = \mu_0(\mathbf{H}+\mathbf{M}) = \mu_0(1+\chi)\mathbf{H}$ visualised at the atomic scale. **Left:** in a *diamagnet* (quartz, halite, calcite), the applied field $\mathbf{H}$ induces atomic dipoles oriented *opposite* to $\mathbf{H}$, so $\mathbf{M}$ is anti-parallel to $\mathbf{H}$ and $\chi < 0$ (typically of order $-10^{-5}$). The flux density inside the material is slightly *less* than $\mu_0 \mathbf{H}$. **Right:** in a *paramagnet* (olivine, biotite, pyroxene), the applied field aligns atomic dipoles *with* itself, so $\mathbf{M}$ is parallel to $\mathbf{H}$ and $\chi > 0$ (typically of order $+10^{-4}$). The flux density inside the material is slightly *greater* than $\mu_0 \mathbf{H}$. In both cases the magnitudes are small: $|\mathbf{M}| \ll |\mathbf{H}|$, and the rock is well within the linear regime. A third regime — *remanent* magnetisation, where $\mathbf{M} \neq 0$ even when $\mathbf{H} = 0$ — is the subject of Lecture 24.
```

<!--
FIGURE BRIEF — fig_BHM_constitutive (Phase 2 build)
  Script: assets/scripts/fig_BHM_constitutive.py
  Type: Python schematic — directly inspired by instructor's handwritten note (uploaded)
  Required:
    - Two side-by-side panels: diamagnet (left), paramagnet (right)
    - Each panel: irregular rock-outline blob containing a 3x3 grid of small dipole rectangles
      (with + and − ends drawn)
    - External H arrow above each blob pointing UP
    - Diamagnet: internal dipoles oriented DOWN (- on top, + on bottom); resulting M arrow pointing DOWN
    - Paramagnet: internal dipoles oriented UP (+ on top, - on bottom); resulting M arrow pointing UP
    - Below the two panels, a single equation block:
      B = mu_0 (H + M)
        = mu_0 (H + chi*H)
        = mu_0 (1 + chi) H
        = mu H
    - Annotation: "chi < 0" under diamagnet; "chi > 0" under paramagnet
    - Colours: H arrows in black; M arrows in primary blue (#0072B2) for paramagnet,
      vermilion (#D55E00) for diamagnet (consistent with COLORS palette and dual-encoded by direction)
    - Style note: follow Marine's handwritten layout — derivation reads top-to-bottom on the page
    - mpl.rcParams: base font 13pt; savefig 300dpi
-->

In rock magnetism, $\chi$ is almost always reported as the *volume susceptibility* (SI, dimensionless) of a bulk rock sample, and is a *property of the rock as a whole*, not of any individual mineral. A "magnetite-bearing" basalt with 1 vol% magnetite has $\chi \sim 10^{-2}$; a pure-quartz sandstone has $\chi \sim -10^{-5}$. The full classification of magnetic minerals and the deeper structure of $\chi$ — including why some minerals carry a permanent moment that survives the removal of the applied field — is the subject of L24.

For the rest of *this* lecture, two takeaways suffice:

- **The field that a magnetometer measures, $\mathbf{B}$, includes both the applied field and the material response.** When we model an anomaly above a buried body, the anomaly arises from $\mathbf{M}$ — the rock's response to the regional $\mathbf{H}$.
- **In Earth's ambient field, all common rocks behave linearly**: $|M| \ll |H|$, and the constitutive relation $\mathbf{B} \approx \mu_0 \mathbf{H}$ inside vacuum or air is an excellent approximation outside the rock. The relative permeability $1 + \chi$ of ordinary crustal rocks differs from 1 by at most a few percent.

## 3. The dipole field at a station: (D, I, F)

Section 2 established the field that a centred dipole produces in three-dimensional space. At any *one* point on the surface, this field is a single vector — three numbers' worth of information. Geophysicists report those three numbers in two equivalent conventions.

The vector form is **(X, Y, Z)** in a local Cartesian frame, with $X$ pointing to true (geographic) north, $Y$ pointing east, and $Z$ pointing *downward* — depth-positive in the geophysical convention. The "magnetic" form is **(D, I, F)**, where $D$ is the **declination** (the horizontal angle between magnetic north and true north, measured positive east), $I$ is the **inclination** (the angle of the total field below horizontal, measured positive into the lower hemisphere), and $F$ is the **total intensity** (the magnitude of the field vector, in nT). The two conventions are related by

```{math}
:label: eq-dif-to-xyz
X = F \cos I \cos D, \quad
Y = F \cos I \sin D, \quad
Z = F \sin I,
```

with the horizontal component $H = F\cos I$ (this scalar $H$ should not be confused with the magnetising field vector $\mathbf{H}$ of §2 — the geophysics convention reuses the symbol, regrettably). Surface field magnitudes range from about 25 000 nT near the magnetic equator to about 65 000 nT near the poles.

```{figure} ../assets/figures/fig_DIF_at_station.png
:name: fig-DIF-station
:alt: Two-panel figure showing the local decomposition of the geomagnetic field at a station. Panel a is a map view from above with true north on the X axis, east on the Y axis, and the horizontal magnetic field H rotated 15.5 degrees east of true north — the declination D. Panel b is a side view showing the local horizontal ground line, a Z axis pointing downward, the total-field vector F at inclination angle I equals 68.9 degrees below horizontal, decomposed into a horizontal component H = F cos I and a vertical component Z = F sin I.
:width: 90%

The local representation of the geomagnetic field at a surface station. **Panel (a)** map view: declination $D$ is the angle of the horizontal field component $H$, measured east of true (geographic) north. **Panel (b)** side view: inclination $I$ is the angle of the total field $F$ below horizontal; the field decomposes into $H = F\cos I$ horizontally and $Z = F\sin I$ vertically (downward positive). Values shown are for Seattle in 2026: $D = +15.5°$, $I = +68.9°$, $F = 52\,900$ nT, from IGRF-13 {cite}`alken2021igrf`.
```

<!--
FIGURE BRIEF — fig_DIF_at_station (Phase 2 build)
  Script: assets/scripts/fig_DIF_at_station.py
  Type: Python schematic — repurposed from panels b and c of the current fig_dipole_field_geometry.png
  Required:
    - Panel a (map view): X axis north, Y axis east; H vector rotated +15.5° from X; annotate D
    - Panel b (side view): horizontal ground line, Z axis down; F vector at 68.9° below horizontal;
      decomposition into H = F cos I (horizontal) and Z = F sin I (vertical)
    - Colours: F in vermilion (#D55E00), H in primary blue (#0072B2), Z in green (#009E73), 
      angles labelled with arc markers
    - mpl.rcParams: base font 13pt; savefig 300dpi
-->

::::{admonition} Worked example: Seattle 2026 station components
:class: tip

For Seattle (47.65° N, 122.30° W) in 2026, IGRF-13 gives $D = +15.5°$, $I = +68.9°$, $F = 52\,900$ nT. Applying [](#eq-dif-to-xyz):

- $X = 52\,900 \cdot \cos(68.9°)\cdot \cos(15.5°) = 18\,300$ nT (toward true north)
- $Y = 52\,900 \cdot \cos(68.9°)\cdot \sin(15.5°) = 5\,070$ nT (toward east)
- $Z = 52\,900 \cdot \sin(68.9°) = 49\,360$ nT (downward)

The horizontal component $H = F \cos I = 19\,000$ nT is small compared with the vertical $Z = 49\,400$ nT: at Seattle's latitude, the field is strongly inclined, and a compass needle — which responds only to the horizontal component — is correspondingly weak.

::::

## 4. The three sources of the surface field

The dipole geometry of §3 is the *shape* of the field seen at the surface. Where the field actually *comes from* is a different question, and the answer is that the surface field is the sum of three contributions produced by three different physical processes occurring at three different depths inside and above the Earth.

```{figure} ../assets/figures/fig_three_sources_cross_section.png
:name: fig-three-sources
:alt: A half-Earth cross-section showing the three principal sources of the geomagnetic field in their physical context. The deep interior is shown with a small bright orange inner core, a yellow-orange outer core containing curved arrows that represent turbulent convection (the geodynamo), a brown mantle, and a thin blue band at the top representing the magnetised lithosphere with small white arrows indicating remanent magnetisation directions. Above the surface a pale blue band represents the ionosphere, marked with curved horizontal arrows that depict electric currents. Three labelled callout boxes identify Source 1 (Core geodynamo, 2900 to 5150 km, wavelengths longer than 3000 km), Source 2 (Lithosphere, upper 30 km, wavelengths 400 to 3000 km), and Source 3 (Ionosphere or magnetosphere, 80 to 500 km altitude, time-varying).
:width: 100%

The three principal sources of Earth's magnetic field located in their physical context. **Source 1 — the core (geodynamo)** lies between 2 900 km and 5 150 km depth, where turbulent convection of liquid iron generates the *main field*. **Source 2 — the magnetised lithosphere** lies in the upper ~30 km of the crust, where rocks carrying a remanent magnetisation from their geologic past contribute a static, spatially heterogeneous signal. **Source 3 — the ionosphere and magnetosphere** sit above the surface (~80–500 km altitude), where currents flowing in the conducting upper atmosphere produce a time-varying contribution. The surface field measured at any station is the *sum* of all three.
```

### 4.1 Source 1 — the core (the geodynamo)

The dominant source of the surface field is the **geodynamo**: self-sustaining turbulent convection of electrically conducting liquid iron in the outer core, between approximately 2 900 km and 5 150 km depth. Heat escaping from the inner core and chemical buoyancy from the freezing-out of light elements at the inner-core boundary drive this flow, and the rotating, conducting fluid generates a magnetic field through the **magnetohydrodynamic dynamo** mechanism — physically analogous to, but vastly more complex than, the disc dynamo in an introductory physics textbook.

The field that emerges from the core-mantle boundary is filtered by depth on its way to the surface: short spatial wavelengths attenuate strongly, so the surface signature of the geodynamo is dominated by **long-wavelength** structure (wavelengths $\gtrsim 3\,000$ km, or spherical-harmonic degree $n \leq 13$). This long-wavelength character is why the dipole approximation works so well at the surface — short wavelengths simply do not survive propagation from $r = 3\,480$ km out to $r = 6\,371$ km. The core field also *drifts* on decadal timescales, the topic of §5.

### 4.2 Source 2 — the lithosphere (crust)

The second source is the **magnetised lithosphere**: rocks in the upper ~30 km of the crust carrying a *permanent* (remanent) magnetisation or responding by induction in the present-day core field. This source is much weaker than the core field on absolute scale — contributing typically 10–1 000 nT to the surface measurement against a core background of 30 000–60 000 nT — but it has its power concentrated at *shorter wavelengths* (spherical-harmonic degree $n \sim 16$ to $n \sim 100$, wavelengths from about 3 000 km down to 400 km), where the core field has fallen off.

The lithospheric field is *static* on human timescales: the rocks carrying it cool and re-magnetise only on geological timescales. It is the *signal* that magnetic surveys of the crust seek to map — the part of the surface measurement that carries information about subsurface structure. The physical mechanisms by which rocks acquire and carry magnetisation, and the way crustal anomalies project to the surface, are the subjects of L24 and L25 respectively.

### 4.3 Source 3 — the ionosphere and magnetosphere

The third source is the **time-varying external field** produced by electric currents flowing in the conducting upper atmosphere — the **ionosphere** (E and F regions, roughly 80–500 km altitude) and the **magnetosphere** beyond it. These currents are driven by solar ultraviolet ionisation (producing the *Sq* — solar quiet — daily variation, with diurnal amplitude of order 30–50 nT at mid-latitudes) and by the interaction of the solar wind with Earth's magnetic field (geomagnetic storms, substorms, magnetospheric ring currents). The ionospheric contribution varies on timescales from seconds to days and has a broad spatial spectrum.

This third source is what makes magnetic surveys operationally harder than gravity surveys. The gravity field at a station is essentially static; the magnetic field is not. Every measurement made at a moving platform (a ship, an aircraft, a satellite) includes a slowly drifting external contribution that must be removed by reference to a fixed *base station* before the static (core + crust) signal can be interpreted. The physics of the magnetosphere itself is the subject of §6.

### 4.4 The spectral fingerprint — separating the three sources

The three sources occupy different spatial-wavelength regimes, and they leave a distinct fingerprint on the field's power spectrum. The **Mauersberger–Lowes spectrum** ({numref}`fig-power-spectrum`) plots the power per spherical-harmonic degree $R_n$ against $n$. The steep drop-off from $n = 1$ to $n \sim 13$ is the dipole-dominated core field. The plateau from $n \sim 16$ outward is the crustal contribution. The faint floor at $R_n \sim$ a few nT² is the ionospheric residual at the time of the satellite mission used to build the model.

```{figure} ../assets/figures/fig_field_power_spectrum.png
:name: fig-power-spectrum
:alt: Log-log plot of magnetic-field power per spherical-harmonic degree R_n in units of nT-squared as a function of degree n from 1 to 110. A steeply decreasing solid blue line labelled Core falls from about 10 to the 10 at n equals 1 to below 10 to the minus 1 at n equals 45. A dashed orange line labelled Crust rises from near zero at n equals 14 to a plateau of about 50 nT-squared between n equals 20 and n equals 60. A dotted green horizontal line at about 4 nT-squared marks the ionospheric external floor. The top axis shows approximate horizontal wavelengths in kilometres.
:width: 100%

Power spectrum of Earth's magnetic field at the surface. The three principal sources occupy non-overlapping wavelength regimes — the core dominates $n \leq 13$, the crust dominates $n \gtrsim 16$, and the ionosphere contributes a roughly degree-independent floor. Reproduces the form of Fig. 1 in {cite}`maus2008powerspectrum`.
```

This separation in wavelength is what allows surveys at different scales to *target* different sources. A satellite mission averaging over hundreds of kilometres samples the core field. A continental-scale aeromagnetic compilation isolates the lithosphere. A high-resolution ground survey along a road traverse resolves individual crustal bodies whose horizontal sizes are tens to hundreds of metres. The choice of survey scale is, in effect, a choice of which source to keep and which to filter out.

## 5. The field drifts — secular variation

The core field is generated by fluid motions whose characteristic timescales are decades to millennia. It therefore *drifts*, and the drift — **secular variation** — is recorded at every magnetic observatory on Earth.

The recent history at Seattle ({numref}`fig-seattle-sv`) tells the story through three quantities: declination $D$ dropped from about +22° in 1955 to +15.5° in 2026; inclination $I$ dropped from 71° to 68.9°; total intensity $F$ fell by about 3 000 nT over the same seven decades.

```{figure} ../assets/figures/fig_seattle_secular_variation.png
:name: fig-seattle-sv
:alt: Three stacked line plots sharing an x-axis from 1955 to 2026 in years. The top plot is declination in degrees east of north, dropping from plus 22.1 degrees in 1955 to plus 15.5 degrees in 2026 with the endpoints annotated. The middle plot is inclination in degrees, dropping from 71 degrees to 68.9 degrees. The bottom plot is total intensity F in nanoteslas, dropping from about 56 000 nT to 52 900 nT.
:width: 90%

Secular variation of declination $D$, inclination $I$, and total intensity $F$ at Seattle (47.65° N, 122.30° W) for 1955–2026, derived from the IGRF/DGRF historical models {cite}`alken2021igrf`. The pace and direction of the drift are reasonably stable on the seven-decade scale but vary appreciably from one decade to the next, occasionally exhibiting an abrupt **geomagnetic jerk** — a rapid change in $\mathrm{d}B/\mathrm{d}t$ on a timescale of months.
```

Globally, the most dramatic recent manifestation of secular variation is the **rapid drift of the north magnetic pole**. Through the 19th and most of the 20th century, the pole moved across the Canadian Arctic at roughly 10 km per year. Beginning in the 1990s, the drift accelerated to 50–60 km per year, taking the pole across the Arctic Ocean toward Siberia. The acceleration is fast enough that the WMM, normally re-released on a five-year schedule for civil aviation and navigation, was issued an *out-of-cycle update* in 2019 to keep pace.

For lithospheric magnetic surveys, secular variation has an operational consequence: every measurement is corrected to a reference epoch (the current IGRF epoch) by subtracting the modelled core-field value at the time of observation. The signal that survives this subtraction is the lithospheric anomaly of L25.

For the scientific question of *why* the pole moves, secular variation is a direct constraint on the flow of liquid iron in the outer core — the very flow that generates the field. The Swarm mission (§8) extracts maps of this flow from the time-series of vector field measurements at satellite altitude.

## 6. The magnetosphere and space weather

The third source identified in §4 — the time-varying field from the ionosphere and magnetosphere — is more than a measurement nuisance. The same currents and plasma structures responsible for the daily ~30 nT wobble are what makes Earth's dipole field a *planetary shield*, deflecting solar-wind plasma and most cosmic rays into trajectories that miss the atmosphere. The shield has a name (the *magnetosphere*), a weather system (the *space weather* generated by solar activity), and a non-trivial historical impact on infrastructure that is well-documented and growing in importance as more of the modern economy moves into space.

### 6.1 The solar wind meets Earth's field

The Sun continuously emits a supersonic stream of charged plasma — predominantly protons and electrons — at speeds of 300–800 km s⁻¹. This **solar wind** carries with it a frozen-in *interplanetary magnetic field* (IMF) of order 5–10 nT at 1 AU. When the solar wind reaches Earth, it encounters the dipole field and is forced to flow around it.

The geometry of this interaction is sketched in {numref}`fig-magnetosphere`. On the dayside, the solar wind decelerates abruptly across a *bow shock* (analogous to the shock wave in front of a supersonic aircraft), then flows around the obstacle of Earth's field. The boundary at which the magnetic pressure of Earth's field balances the ram pressure of the solar wind is the **magnetopause**, located on average at ~10 Earth radii on the sunward side. Inside the magnetopause, Earth's field is compressed against the dayside and stretched into a long *magnetotail* on the nightside that extends hundreds of Earth radii downstream.

```{figure} ../assets/figures/fig_magnetosphere_solar_wind.png
:name: fig-magnetosphere
:alt: Schematic side view of Earth's magnetosphere with the Sun on the left. Streamlines representing the solar wind flow from the Sun and encounter a curved bow shock surface. Inside the bow shock the streamlines are deflected around a teardrop-shaped magnetopause boundary, which is compressed on the dayside and stretched into a long magnetotail on the nightside. Inside the magnetopause Earth is shown at the centre with dipole field lines that are compressed on the dayside and elongated on the nightside. The Van Allen radiation belts are indicated as two doughnut-shaped regions in the inner magnetosphere. Labels mark the bow shock, magnetopause, magnetotail, plasmasphere, and inner and outer Van Allen belts.
:width: 100%

Schematic of Earth's magnetosphere viewed from the dawn–dusk meridian, with the Sun to the left. The solar wind (streamlines) flows from the Sun, crosses the curved **bow shock**, and is deflected around the **magnetopause** — the surface at which the magnetic pressure of Earth's compressed dipole field balances the ram pressure of the solar wind. Inside the magnetopause, Earth's dipole field is squashed on the dayside (typical magnetopause stand-off distance ~10 Earth radii) and stretched into a long *magnetotail* on the nightside. The **Van Allen radiation belts** — two doughnut-shaped regions of charged particles trapped by the dipole — sit inside the inner magnetosphere. The geometry is the planetary shield: charged particles in the solar wind cannot easily cross magnetic field lines, and so most of the incoming plasma is deflected around the magnetopause rather than reaching the atmosphere.
```

<!--
FIGURE BRIEF — fig_magnetosphere_solar_wind (Phase 2 build)
  Script: assets/scripts/fig_magnetosphere_solar_wind.py
  Type: Python schematic (matplotlib only, no real data)
  Reference: NASA SVS public-domain magnetosphere visualizations (e.g., 
    https://svs.gsfc.nasa.gov/12747 — verify URL when building)
  Required:
    - Sun on far left (small circle); solar wind streamlines flowing right
    - Curved bow shock (light orange parabolic curve) ~14 Earth radii sunward
    - Magnetopause boundary (heavier blue curve) ~10 Earth radii sunward, 
      stretching into magnetotail on nightside
    - Earth at centre with simplified dipole field lines, compressed on dayside, elongated nightside
    - Two crescent-shaped Van Allen belts marked at ~1.5 and ~4 Earth radii
    - Labels for: bow shock, magnetopause, magnetotail, plasmasphere, inner/outer Van Allen belts
    - Colours: solar wind streamlines vermilion (#D55E00), bow shock orange (#E69F00),
      magnetopause blue (#0072B2), Earth field lines black, Van Allen belts pink (#CC79A7)
    - Distance markers in Earth radii on a scale bar
    - mpl.rcParams: base font 13pt; savefig 300dpi
-->

### 6.2 Why the field protects us

The shielding action of the magnetosphere has two distinct components, with consequences on very different timescales.

**Direct deflection of charged particles.** A charged particle moving in a magnetic field experiences a Lorentz force perpendicular to its velocity and to the field, with magnitude $F = qvB$. In Earth's field, the Larmor radius of a 1 MeV solar-wind proton is of order 100 km — much smaller than the magnetosphere. The particle therefore *spirals* around field lines rather than crossing them, and is deflected around the magnetopause rather than penetrating into the lower atmosphere. The leakage that does occur happens preferentially at the *polar cusps*, where field lines connect directly to interplanetary space; this is what produces the auroral ovals around the magnetic poles.

**Atmospheric retention.** Over geologic time, the magnetosphere prevents the solar wind from progressively stripping the upper atmosphere through *sputtering* — the same process that has thinned Mars's atmosphere over the past ~3.5 Gyr since its dynamo shut down. Mars and Earth received broadly similar atmospheres at formation; Mars's loss of its magnetic shield is consistent with the loss of most of its atmosphere over geologic time. The argument is not airtight (atmospheric escape depends on gravity, temperature, and chemistry too), but the correlation across the inner Solar System is striking: terrestrial planets with active dynamos retain substantial atmospheres; those without do not.

### 6.3 Geomagnetic storms

When the solar wind is disturbed — most commonly by a *coronal mass ejection* (CME), a fast-moving cloud of plasma launched from the solar corona — its ram pressure and IMF orientation change rapidly. If the IMF orientation has a southward component opposite to Earth's northward dipole, magnetic reconnection at the dayside magnetopause becomes efficient: solar-wind plasma is injected directly into the inner magnetosphere, the ring current intensifies, and the surface magnetic field decreases by tens to hundreds of nT over hours to days. This is a **geomagnetic storm**.

Three storms in the modern record illustrate the range:

- **The Carrington event (1–2 September 1859)** is the largest geomagnetic storm in instrumental history. Telegraph systems across North America and Europe sparked and caught fire; some continued to operate without power, drawing current from the geomagnetically induced electric field. Aurorae were visible at low latitudes including Hawai'i, Mexico, and Cuba. The peak disturbance, estimated from contemporaneous magnetograms, exceeded 1 600 nT in horizontal disturbance — about 3% of the ambient field.
- **The Quebec storm (13 March 1989)** caused the 9-hour collapse of the Hydro-Québec power grid, leaving six million people without electricity. Geomagnetically induced currents in long transmission lines drove transformers into saturation, tripping protective relays. The storm also disrupted satellite operations and HF radio communications across the northern hemisphere.
- **The Gannon storm (10–12 May 2024)** was the first G5-class (extreme) storm since 2003. Auroral displays were visible across the contiguous United States and as far south as Mexico. The storm caused a significant satellite-drag event — most consequentially for low-Earth-orbit constellations, where increased neutral density caused several SpaceX Starlink satellites launched during the storm to fail to reach their target orbits and decay. GPS positioning errors during the storm caused widespread disruption to precision agriculture across the central United States during the spring planting season.

### 6.4 Operational consequences

Modern infrastructure that is sensitive to geomagnetic activity includes:

- **Power grids.** Long high-voltage transmission lines act as antennas for the geomagnetically induced electric field. The induced quasi-DC currents (GICs) saturate transformer cores, distort the AC waveform, and in extreme cases cause transformer failure. The risk scales with grid extent and latitude; the Canadian and Scandinavian grids are the most exposed.
- **Satellites.** Increased neutral density in the upper atmosphere during storms causes orbital drag, particularly for low-Earth-orbit spacecraft. Single-event upsets from energetic-particle penetration cause computer faults in satellites at all altitudes. Cumulative radiation dose in the Van Allen belts is a design constraint for geostationary spacecraft.
- **GPS and other GNSS.** Total-electron-content variations in the ionosphere during storms cause position errors that can exceed metres in single-frequency receivers and centimetres even in dual-frequency receivers. Precision applications — surveying, autonomous machine control, aviation approach systems — are degraded.
- **HF radio communications.** The D-region of the ionosphere absorbs HF radio waves during storms, causing blackouts of long-distance shortwave links — including the over-the-pole routes used by transpolar airline flights, which routinely divert during storm conditions.
- **Pipelines.** Long buried pipelines, like power lines, accumulate geomagnetically induced potentials that accelerate corrosion at insulator joints.

Real-time monitoring of space weather is the responsibility of national agencies — the NOAA Space Weather Prediction Center in the United States, equivalent services in Europe, Japan, and Australia — that issue alerts based on observations from the *Swarm* constellation (§8), the *SOHO* and *DSCOVR* solar-monitoring missions, and a global network of ground magnetometers. The same data also feed the IGRF and WMM models on which navigation systems depend.

## 7. The forward and inverse problems — paleo-latitude from inclination

For a **geocentric axial dipole** (GAD) — the simplest model of the time-averaged field, in which the dipole axis is assumed to coincide with the rotation axis — the inclination $I$ at geographic latitude $\lambda$ is

```{math}
:label: eq-gad
\tan I = 2 \tan \lambda.
```

The factor of 2 comes directly from the dipole field expression [](#eq-dipole-field): at the surface, the radial component is twice as large as the tangential component at any latitude. Equation [](#eq-gad) is the **forward problem** of paleo-latitude: given a paleo-latitude $\lambda$ inferred from a plate reconstruction, predict the inclination that a magnetic mineral would record on cooling at that latitude.

The **inverse problem** is more useful in practice. A basalt that crystallised at unknown latitude carries a (thermo)remanent magnetisation whose inclination can be measured in the lab — the physics of *how* that remanence is locked in is the subject of L24. Inverting [](#eq-gad):

```{math}
:label: eq-gad-inverse
\lambda = \arctan\!\left(\frac{\tan I}{2}\right).
```

```{figure} ../assets/figures/fig_paleolatitude_from_inclination.png
:name: fig-paleolatitude
:alt: Two side-by-side plots. The left panel Forward I from lambda plots inclination I in degrees on the y axis from 0 to 90 against paleo-latitude lambda in degrees on the x axis from 0 to 90. The curve tan I = 2 tan lambda passes through the origin and reaches I = 90 degrees at lambda = 90 degrees, with circle markers at the equator (I = 0), 30 degrees (I = 49), Seattle (I = 65 degrees GAD prediction), and pole (I = 90). The right panel plots inferred paleo-latitude lambda against measured inclination I, both 0 to 90 degrees. The curve lambda = arctan of tan I over 2 is shown in blue with a light-blue uncertainty band that is widest near the equator and narrowest near the pole.
:width: 100%

(a) Forward problem: inclination predicted from paleo-latitude using the geocentric axial dipole equation [](#eq-gad). (b) Inverse problem: paleo-latitude recovered from a measured inclination, with the $\pm 1\sigma_\lambda$ uncertainty band that results from a $\sigma_I = 2°$ measurement error propagated through [](#eq-gad-inverse). The error is largest near the equator and shrinks toward the pole — a consequence of the slope of the forward curve.
```

Uncertainty propagation through [](#eq-gad-inverse) is direct: differentiating gives

```{math}
\frac{\mathrm{d}\lambda}{\mathrm{d}I} = \frac{1}{2}\,\frac{\sec^2 I}{1 + \tfrac{1}{4}\tan^2 I},
```

so $\sigma_\lambda \approx (\mathrm{d}\lambda/\mathrm{d}I)\,\sigma_I$ to first order. The slope $\mathrm{d}\lambda/\mathrm{d}I$ is large near $I = 0$ (equator) and small near $I = 90°$ (pole): a $\pm 2°$ measurement error in inclination becomes roughly $\pm 1°$ in paleo-latitude at the pole but $\pm 4°$ at the equator. Inverting a paleo-magnetic inclination is more reliable at high paleo-latitudes than at low ones.

::::{admonition} Limits of the GAD assumption
:class: warning

Equation [](#eq-gad) is exact only for a perfect dipole. The actual surface field deviates from a centred axial dipole both because the dipole axis itself is tilted (the 11° tilt that gives Seattle a 65.5° *GAD* inclination but a 68.9° *measured* inclination) and because higher-degree harmonics contribute about 10% of the surface power.

These deviations average out over time: when many lava flows spanning $\gtrsim 10\,000$ years are averaged at the same site, the mean inclination matches the GAD prediction to within a few degrees. But a *single* lava flow records a snapshot that may deviate by 5–10°. Paleomagnetic latitudes are therefore reliable only when based on many independent samples covering enough geologic time to average over secular variation. Lecture 24 returns to this issue when reconstructing plate motions from oceanic stripes.

::::

## 8. Research horizon — the Swarm satellites and geomagnetic jerks

The IGRF is built every five years from observatory data and from *satellite* measurements that map the field globally to spherical-harmonic degrees $n \lesssim 130$ {cite}`alken2021igrf`. The currently flying satellite constellation is **Swarm**, a three-spacecraft ESA mission launched in 2013 (operating beyond its design lifetime). Swarm measures the vector field at 460 km altitude with sub-nT precision, which is good enough to:

1. Track **westward drift** of the magnetic equator at a rate of about 0.2° per year — a signature of azimuthal flow at the top of the outer core, consistent with hydrodynamic models of the geodynamo.
2. Detect **geomagnetic jerks** — abrupt, year-scale changes in the rate of secular variation — which appear to originate in the bulk of the outer core but whose physical mechanism is debated.
3. Image the **lithospheric field** at degree $n \sim 130$, exposing features such as oceanic-spreading fabrics, large impact structures (e.g. Vredefort, Sudbury), and continental-margin gradient zones.

The geophysical question driving this work — *"What is happening in the outer core right now?"* — is central to long-range climate-grade geomagnetic reference models for civil aviation, satellite navigation, and military operations, and to ongoing efforts to understand whether the present declining dipole moment foreshadows a polarity reversal on the geologic timescale. (It probably does not, but the question is open.)

## 9. AI literacy — using a language model as a derivation partner

Equation [](#eq-gad) is one of the cleanest examples of a single-formula forward problem in geophysics. It is also short enough that a competent large language model (LLM) can be asked to *derive* it from the standard expression for the field of a magnetic dipole in polar coordinates [](#eq-dipole-field). This is a useful test of the model's mathematical reasoning, and of the student's ability to check the result.

::::{admonition} Reasoning Partner activity
:class: tip

**Step 1 — Ask the LLM to derive equation [](#eq-gad).** Prompt: *"Starting from the magnetic dipole field $B_r = (2m\cos\theta) / r^3$, $B_\theta = (m\sin\theta) / r^3$ in spherical polar coordinates with $\theta$ measured from the dipole axis, derive the relation between the inclination of the surface field and the magnetic colatitude. Show each step."*

**Step 2 — Verify, do not trust.** Three checks the student must perform:

1. Does the LLM correctly identify that *inclination* is the angle of the total field below horizontal, not below vertical? (A common mistake.)
2. Does the algebra go through cleanly, or does the LLM drop a factor of 2?
3. Is the final formula written in terms of *colatitude* (the angle from the pole) or *latitude* (the angle from the equator)? The two differ by $\pi/2$ and the difference matters: equation [](#eq-gad) is $\tan I = 2 \tan\lambda$ with $\lambda$ = latitude, but it becomes $\tan I = 2 \cot\theta$ if $\theta$ = colatitude.

**Step 3 — Disagree productively.** If the LLM's derivation has an error, write a one-sentence prompt that identifies the specific step and asks for a correction. Do *not* simply ask "is this right?" — that elicits agreement regardless of the actual answer. Effective prompts name the line or step that is in question.

The student deliverable is a one-page record showing: (i) the LLM's derivation, (ii) at least one identified error or unclear step, and (iii) the corrected derivation in the student's own notation, signed.

::::

## 10. Concept check

::::{admonition} Concept-check questions
:class: note

1. **(D, I, F) at Seattle in 1955.** Given the 1955 IGRF values $D = +22.1°$, $I = +71.0°$, $F = 55\,980$ nT, compute the local components $(X, Y, Z)$ at Seattle. Compare with the 2026 values quoted in §3. Which component has changed the most in *relative* terms? Which has changed the most in *absolute* (nT) terms?

2. **B versus H in a rock.** A basalt with bulk volume susceptibility $\chi = 5 \times 10^{-3}$ sits in Earth's field at Seattle ($H = F\cos I / \mu_0 \approx 1.5 \times 10^4$ A m⁻¹ for an ambient $F = 52\,900$ nT, $I = 68.9°$). Compute the magnetisation $M = \chi H$ inside the rock, the additional flux density $\mu_0 M$ this contributes, and the ratio $M/H$ and $\mu_0 M / B$. Comment on whether the approximation $\mathbf{B} \approx \mu_0 \mathbf{H}$ holds for this rock.

3. **Space weather budget.** During a moderate (G3) geomagnetic storm, the surface horizontal field at mid-latitudes is depressed by approximately 200 nT for about six hours, then recovers. Estimate the order of magnitude of the geomagnetically induced electric field at the surface using $|\mathcal{E}| \sim L\,|\mathrm{d}B/\mathrm{d}t|$ for a 1 000 km transmission line with $\mathrm{d}B/\mathrm{d}t$ inferred from the storm timescale. Compare with the operational threshold of ~10 V km⁻¹ above which transformer saturation becomes a concern.

4. **Paleo-latitude error budget.** A paleomagnetic study of a 50-Myr-old basalt yields a site-mean inclination of $I = 35° \pm 3°$. Compute the inferred paleo-latitude and its $1\sigma$ uncertainty using [](#eq-gad-inverse). The same study finds $I = 75° \pm 3°$ at a second site. Compare the two paleo-latitude uncertainties. Explain in one sentence why one is larger than the other.

::::

::::{admonition} Concept-check answers
:class: dropdown

*Answers and worked solutions are provided in the instructor materials (see `concept_check_lecture23.md` in the `ess314-instructor` repository).*

::::

## 11. Looking ahead

Lecture 24 takes the framework of this lecture — the dipole field, the constitutive relation, the lithospheric source as the geophysical *signal* — and asks the next question: *how does a rock come to carry a permanent magnetisation, and what does that magnetisation tell us about plate motion?* The answer covers the five categories of magnetic ordering at the mineral scale, the three mechanisms by which rocks lock in a remanent moment (TRM, DRM, CRM), the geomagnetic polarity timescale, and the Vine–Matthews–Morley reading of the seafloor stripe pattern as a tape recorder of plate spreading.

Lecture 25 then takes the next step: how a buried magnetised body — characterised by the mechanisms of L24 — produces a small but measurable anomaly at the surface, and how that anomaly is inverted to recover subsurface structure. This is the magnetic analog of the gravity-anomaly inversion of L20.

## 12. Further reading

Open-access references are preferred; paywalled works are cited for completeness but are not required for the lecture.

```{bibliography}
:filter: docname in docnames
:keyprefix: lec23-
```

::::{admonition} Companion notebook (next step)
:class: seealso

The accompanying Jupyter notebook **`magnetics_forward.ipynb`** (in the course `notebooks/` directory) implements the GAD equation, the (D, I, F) ↔ (X, Y, Z) transformation, and an IGRF-13 / WMM-2025 field calculator that students will use in the discussion section. The notebook also includes a short space-weather data-pulling exercise using the NOAA SWPC API.

::::

::::{admonition} Open data and tools
:class: seealso

- **NOAA Geomagnetism Calculator**: <https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml> — IGRF / WMM field model lookup at any point.
- **NOAA Space Weather Prediction Center**: <https://www.swpc.noaa.gov/> — real-time geomagnetic activity, Kp index, storm alerts.
- **ESA Swarm Virtual Research Environment**: <https://vires.services/> — Swarm vector field data and analysis tools.
- **WMM-2025 model files and documentation**: <https://www.ncei.noaa.gov/products/world-magnetic-model> — declination grids in CSV form (public domain).

::::
