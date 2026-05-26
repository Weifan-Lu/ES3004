---
title: "Lecture 26 — Lithosphere: Oceanic vs. Continental"
short_title: "L26 Lithosphere"
authors:
  - Marine Denolle
  - ESS 314 ESS Faculty
date: 2026
module: 7
lecture: 26
keywords: [lithosphere, oceanic, continental, half-space cooling, plate model, LAB, Moho, Siletzia, Cascadia]
---

# Lithosphere: Oceanic vs. Continental

```{admonition} Learning Objectives
:class: tip

By the end of this lecture, students will be able to:

- **[LO-1, LO-2]** Derive the half-space cooling (HSC) model of oceanic lithosphere from the 1D heat equation and apply it to predict bathymetry and surface heat flow as a function of seafloor age.
- **[LO-2, LO-3]** Identify the five distinct definitions of the lithosphere base — mechanical, thermal, seismic, elastic, and chemical — and explain why they disagree, particularly beneath old continental cratons.
- **[LO-3]** Download, plot, and interpret three open geophysical datasets (Müller/Seton seafloor age, ETOPO1 bathymetry, CRUST1.0 Moho) using a reproducible Python workflow.
- **[LO-4]** Construct a side-by-side comparison of oceanic and continental lithosphere across eleven attributes (composition, layering, density, thickness, seismic structure, heat flow, gravity, magnetics, age, geodynamic role) and use the comparison to argue for or against the rigidity assumption of plate tectonics.

**Prerequisites:** Stress, strain, and the equation of motion (L03); seismic refraction (L08); gravity and isostasy (L19–L21); magnetics (L23–L25). Familiarity with `numpy`, `matplotlib`, and `xarray` is assumed for the data-access blocks; students who have completed Lab 7 (AI as Collaborator) will recognize the open-data workflow.
```

---

## 1. The Geoscientific Question

We have used the word *lithosphere* freely in earlier modules. It described where earthquakes nucleate, where elastic flexure occurs, where the geomagnetic field is recorded, where gravity anomalies originate. In every one of those contexts the lithosphere was treated as a single well-defined object: a rigid outer shell of the Earth that we can imagine, draw, and reason about as a thing.

The lecture ahead will challenge that picture in one particular way. Ask a seismologist where the lithosphere ends and you will get one answer. Ask a flexural modeler and you will get a different one. Ask someone who studies heat flow, or surface waves, or postglacial rebound, and you will get three more. Under oceans these answers mostly agree. Under old continental cratons they can be 50 km apart.

Module 7 is the synthesis module of the course. Rather than introducing a new method, this lecture *uses* every method developed so far — refraction, reflection, surface-wave tomography, receiver functions, gravity, magnetics, heat flow, geodesy — and asks which combinations let us interpret the lithosphere as a real geophysical object, and where those interpretations fail. The framing question for the rest of the lecture is:

> *What do we mean by "the lithosphere," and why does the answer change depending on which observable we use?*

Oceanic and continental lithosphere are the two case studies, and the comparison between them is where the rest of the lecture lives.

---

## 2. Governing Physics

### 2.1 Conductive cooling of a half-space

The simplest physical model of the oceanic lithosphere starts at a mid-ocean ridge, where hot mantle material is brought to the surface and immediately begins to lose heat to the overlying ocean. As that material moves laterally away from the ridge it continues to cool by conduction, growing a cold rigid layer at the top. The thickness of that cold layer at any point depends only on how long it has been cooling — which is how long it has been since the material was created at the ridge — and on a single thermal diffusivity $\kappa$.

This *half-space cooling* (HSC) model treats the mantle below the ridge axis as a semi-infinite half-space at uniform initial temperature $T_m$, with a fixed cold surface temperature $T_s$ imposed at $z = 0$ from time $t = 0$ onward. The cold layer that grows downward over time is the *thermal boundary layer*. The portion of that layer that is also cold and stiff enough to behave mechanically as part of a rigid plate is the *mechanical boundary layer*. They are not the same thing.

### 2.2 Mechanical vs. thermal boundary layers

Here is the conceptual hinge of the lecture. Conduction transports heat continuously from the hot mantle to the surface, but rocks do not transition from "fluid" to "solid" at a single temperature. They transition gradually, governed by rheology. Roughly:

- Below about $600\,^\circ\mathrm{C}$, mantle rocks are too cold to creep on tectonic timescales. They are part of the rigid plate. This isotherm sets the **mechanical boundary layer**.
- Below about $1300\,^\circ\mathrm{C}$, conduction is still the dominant heat-transport mechanism, but the rocks can flow on geological timescales. This isotherm sets the **thermal boundary layer**.
- Between the two isotherms there is a region that conducts heat like a solid but creeps like a fluid. This region is part of the lithosphere if you are a heat-flow geophysicist but part of the asthenosphere if you are a flexural modeler.

This is not a definitional quibble. It is a real physical reflection of the fact that the lithosphere is defined by *behavior*, and the behavior of rocks depends on which timescale and which physical process you ask about. We will return to this in Beat B of §6.

```{admonition} A brief word on rheology
:class: note

The transition from elastic to viscous behavior is the subject of an expanded version of Lecture 3 (Stress, Strain, and Rheology). For the present lecture, you only need the conclusion: a rock that is elastic on a one-second timescale (a seismic wave) can be viscous on a one-million-year timescale (mantle convection). The Maxwell time $\tau_M = \eta / \mu$ — the viscosity divided by the shear modulus — separates the two regimes. For the asthenosphere, $\tau_M$ is roughly a few thousand years.
```

---

## 3. Mathematical Framework

### 3.1 Notation

```{admonition} Notation
:class: important

| Symbol | Meaning | Typical value (oceanic) |
|--------|---------|-------------------------|
| $t$ | Lithospheric age | $0$–$180$ Ma |
| $z$ | Depth below seafloor | $0$–$200$ km |
| $T(z, t)$ | Temperature | scalar function |
| $T_m$ | Mantle potential temperature | $\sim 1350\,^\circ\mathrm{C}$ |
| $T_s$ | Surface (seafloor) temperature | $\sim 0\,^\circ\mathrm{C}$ |
| $\kappa$ | Thermal diffusivity | $\sim 10^{-6}\ \mathrm{m^2\,s^{-1}}$ |
| $k$ | Thermal conductivity | $\sim 3.1\ \mathrm{W\,m^{-1}\,K^{-1}}$ |
| $\rho_m, \rho_w$ | Mantle, seawater density | $3300, 1030\ \mathrm{kg\,m^{-3}}$ |
| $\alpha$ | Thermal expansion coefficient | $\sim 3 \times 10^{-5}\ \mathrm{K^{-1}}$ |
| $d(t)$ | Ocean depth at age $t$ | $2.5$–$6$ km |
| $q(t)$ | Surface heat flow at age $t$ | $50$–$250\ \mathrm{mW\,m^{-2}}$ |
| $L_p$ | Plate-model basal thickness | $\sim 95$ km |
```

### 3.2 Half-space cooling temperature

For a semi-infinite half-space initially at uniform temperature $T_m$, with its surface at $z = 0$ held at $T_s$ from $t = 0$, the 1D heat equation

$$
\frac{\partial T}{\partial t} = \kappa\, \frac{\partial^2 T}{\partial z^2}
$$ (eq:diffusion)

has the well-known error-function solution

$$
T(z, t) = T_s + (T_m - T_s)\, \operatorname{erf}\!\left( \frac{z}{2\sqrt{\kappa t}} \right).
$$ (eq:hsc-temperature)

The thermal boundary layer thickness grows as $\sqrt{\kappa t}$: at $t = 50$ Ma, with $\kappa = 10^{-6}\ \mathrm{m^2\,s^{-1}}$, the layer is about 90 km thick.

### 3.3 Bathymetry from isostasy

The cold lithosphere is denser than the hot asthenosphere it replaced, so a column of older lithosphere sits lower than a column of younger lithosphere. By Airy isostasy, the seafloor depth $d(t)$ relative to the ridge crest $d_0$ is

$$
d(t) - d_0 = \frac{2\, \rho_m\, \alpha\, (T_m - T_s)}{\rho_m - \rho_w} \sqrt{\frac{\kappa t}{\pi}}.
$$ (eq:hsc-bathymetry)

Plugging in standard values gives a numerically convenient form:

$$
d(t) \approx 2500 + 350\sqrt{t} \quad \text{(meters, $t$ in Ma)}.
$$ (eq:hsc-numerical)

This is the celebrated $\sqrt{t}$ depth–age relation. It is one of the strongest empirical confirmations of the plate-tectonic conveyor model: bathymetry, surface heat flow, and oceanic crustal age combine into a single coherent prediction.

### 3.4 Surface heat flow

Heat flow at the surface follows from Fourier's law applied to the HSC temperature field:

$$
q(t) = \frac{k\, (T_m - T_s)}{\sqrt{\pi \kappa t}}.
$$ (eq:hsc-heatflow)

Like bathymetry, heat flow has a $1/\sqrt{t}$ dependence on age — declining from a sharp peak at the ridge axis to a low background value at the oldest oceanic crust.

### 3.5 The plate model

The HSC model has one critical flaw: it predicts that oceanic lithosphere should keep thickening, and the seafloor should keep deepening, indefinitely. Observation contradicts this past about 70 Ma — beyond that age, both depth and heat flow flatten out. The **plate model** fixes this by imposing a fixed lithospheric thickness $L_p \approx 95$ km, with a constant basal isotherm $T_m$ at $z = L_p$. The depth of the seafloor under the plate model approaches a maximum value:

$$
d(t) = d_{\max} - (d_{\max} - d_0)\, \exp\!\left(-\frac{t}{\tau}\right),
$$ (eq:plate-depth)

with $d_{\max} \approx 6.4$ km and $\tau \approx 62$ Myr. For $t \ll \tau$ the plate model reduces to the HSC $\sqrt{t}$ relation; for $t \gg \tau$ it asymptotes to a flat plate.

```{figure} ../assets/figures/F4_plate_vs_hsc_schematic.png
:name: F4_schematic
:alt: Two-panel schematic showing the plate model (constant-thickness lithosphere) on the left and the half-space cooling model (lithosphere thickening as sqrt of age) on the right. Both panels show a ridge axis in the center with arrows indicating plate motion and mantle upwelling.
:width: 100%

The two thermal models of oceanic lithosphere. **(a)** Plate model: lithosphere has fixed maximum thickness ($\sim 95$ km) with a constant basal isotherm. **(b)** Half-space cooling: lithosphere thickens as $\sqrt{t}$ indefinitely.
```

The two models can be compared directly against the global compilation of seafloor depth and heat flow.

```{figure} ../assets/figures/F5_model_comparison_3panel.png
:name: F5_model_comparison
:alt: Three-panel comparison of HSC and plate models. Panel a shows depth versus age with binned data falling between the two curves and converging on the plate model at old ages. Panel b shows heat flow versus age with similar behavior. Panel c shows depth versus square-root-of-age, where the HSC model is linear and the plate model is curved.
:width: 100%

HSC vs. plate-model fits to binned global data. **(a)** Depth vs. age: HSC overpredicts subsidence past $\sim 70$ Ma. **(b)** Heat flow vs. age: HSC underpredicts heat flow at old ages. **(c)** Depth vs. $\sqrt{t}$: the HSC model is *linear by construction* here, which made it easy to fit by hand in the 1970s. The plate model curves at the right, reflecting the basal-isotherm boundary condition.
```

---

## 4. Working With Real Data

A short tangent — and the most important practical section of this lecture. Every figure above can in principle be regenerated by you from open data, on your own laptop, in minutes. This is not how geophysicists worked even twenty years ago; today it is the entry point to every research project. We work through three short code blocks here, each demonstrating a different data-access pattern that will recur throughout your geoscience career.

### 4.1 Code Block A — Downloading and plotting the seafloor age grid

The Müller/Seton 2020 age grid is the canonical open data product for the age of every patch of oceanic crust on Earth. It is distributed as a netCDF file via the University of Sydney EarthByte webDAV server, and is readable directly from a URL with `xarray`:

```python
# Müller/Seton 2020 seafloor age grid via xarray
# Provenance: Seton, M. et al. (2020), G-Cubed,
#   doi:10.1029/2020GC009214 — open license, cite when used.

import xarray as xr
import matplotlib.pyplot as plt

# Direct netCDF via xarray (cloud-style: no local download needed)
url = ("https://www.earthbyte.org/webdav/ftp/Data_Collections/"
       "Muller_etal_2019_Tectonics/Muller_etal_2019_Agegrids/"
       "Muller_etal_2019_Tectonics_v2.0_netCDF/"
       "Muller_etal_2019_Tectonics_v2.0_AgeGrid-0.nc")
ds = xr.open_dataset(url)
print(ds)              # ALWAYS inspect first — variable names, units, scaling
age = ds["z"]          # age in Myr (per dataset README)

fig, ax = plt.subplots(figsize=(10, 5))
age.plot(ax=ax, cmap="magma_r", vmin=0, vmax=180)
ax.set_title("Seafloor age (Ma) — Müller et al. 2019 / Seton et al. 2020")
plt.tight_layout()
plt.savefig("oceanic_age_map.png", dpi=200, bbox_inches="tight")
```

```{figure} ../assets/figures/F1_seafloor_age_map.png
:name: F1_age_map
:alt: Global map showing seafloor age in millions of years. Bright yellow bands mark mid-ocean ridges where new crust forms; dark purple-black areas in the northwest Pacific mark the oldest oceanic crust around 180 Ma. The pattern is symmetric about each ridge, with the Atlantic showing narrow age stripes from slow spreading and the Pacific showing wider stripes from fast spreading.
:width: 100%

Global seafloor age. The brightest bands are mid-ocean ridge axes (age $\approx 0$); the darkest areas are the oldest oceanic crust (NW Pacific, $\sim 180$ Ma) — older crust has already been subducted. The width of each color band encodes the spreading rate: narrow bands in the slow-spreading Atlantic, wide bands in the fast-spreading Pacific.
```

Three teaching points carry across every dataset you will ever touch.

1. **`xarray` is the standard tool for gridded geophysical data.** It handles netCDF, HDF5, GRIB, and Zarr formats uniformly, lazily reads only the parts of a dataset you actually use, and integrates with `numpy` and `matplotlib`.
2. **Always print the dataset before plotting.** Datasets carry units, scaling factors, coordinate metadata, and missing-value flags. Plotting blindly before inspecting the metadata is the single most common source of "my map looks weird" bugs.
3. **Cite the data, not just the figure.** Every paper that uses these data cites Seton et al. 2020. So should you.

### 4.2 Code Block B — Downloading and plotting CRUST1.0 Moho depth

The CRUST1.0 model (Laske et al. 2013) is a 1°-by-1° global model of crustal structure, distributed as a small bundle of ASCII XYZ files. Unlike the Müller grid, it is small enough to read entirely into memory in a few lines:

```python
# CRUST1.0 Moho depth from Laske et al. (2013)
# Source: https://igppweb.ucsd.edu/~gabi/crust1.html
# Download crust1.0.tar.gz, unpack, find xyzcoords.moho.txt inside.

import numpy as np
import matplotlib.pyplot as plt

# CRUST1.0 distributes Moho depth as a simple 3-column XYZ file
# on a 1° grid: lon, lat, moho_depth (km, positive = below sea level)
moho_xyz = np.loadtxt("xyzcoords.moho.txt")
lon, lat, moho_km = moho_xyz[:, 0], moho_xyz[:, 1], moho_xyz[:, 2]

# Reshape to 1° grid: 180 lat rows × 360 lon columns
moho_grid = moho_km.reshape((180, 360))

fig, ax = plt.subplots(figsize=(10, 5))
im = ax.imshow(moho_grid, extent=[-180, 180, -90, 90],
               cmap="viridis", vmin=5, vmax=60, origin="upper")
plt.colorbar(im, label="Moho depth (km)")
ax.set_title("CRUST1.0 Moho depth (Laske et al. 2013)")
plt.tight_layout()
plt.savefig("crust10_moho.png", dpi=200, bbox_inches="tight")
```

```{figure} ../assets/figures/F12_north_america_moho.png
:name: F12_moho_NA
:alt: Map of North American crustal thickness color-coded from about 10 km (deep blue, oceanic crust offshore) to about 55 km (yellow, beneath the Rocky Mountains). Labeled features include the Canadian Shield with crust around 45 km, the Rockies at maximum thickness, the Basin and Range with thinned crust, and the Appalachians with moderate thickness.
:width: 100%

North American Moho thickness from CRUST1.0 (regional crop). Oceans show the canonical $\sim 10$ km oceanic Moho; the Canadian Shield craton sits at $\sim 45$ km; the Rockies (with their tectonic root) reach $\sim 50$+ km; the Basin and Range, extended by Cenozoic rifting, has been thinned to $\sim 28$–$30$ km.
```

Two teaching points specific to this dataset:

1. **Discrete grids are small enough to inspect by hand.** The full CRUST1.0 grid is $360 \times 180 = 64{,}800$ cells. You could in principle print it. Don't, but knowing the size matters for picking the right tools.
2. **Continental crustal thickness varies by a factor of two across one continent.** Oceanic crust does not. This will be Beat B of our active-learning comparison in §6.

### 4.3 Code Block C — A bathymetric transect across the Mid-Atlantic Ridge

ETOPO1 is the global bathymetry-and-topography product maintained by NOAA NGDC. The PyGMT library provides one-line remote access to a cached version through GMT's virtual datasets, including a `grdtrack` function that extracts a profile along an arbitrary track:

```python
# ETOPO1 bathymetric transect via PyGMT
# Source: Amante, C. & Eakins, B.W. (2009). ETOPO1 1 Arc-Minute Global Relief.
# NOAA NGDC, doi:10.7289/V5C8276M. Open access.

import pygmt
import numpy as np
import matplotlib.pyplot as plt

# Track from Cape Hatteras (~-76°E) to West Africa (~-10°E) at 30°N
points = np.column_stack([
    np.linspace(-75, -10, 500),       # longitudes
    np.full(500, 30.0),               # latitude 30°N
])
track = pygmt.grdtrack(points=points, grid="@earth_relief_05m",
                       newcolname="depth_m")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(track.iloc[:, 0], track["depth_m"] / 1000.0, color="black", lw=1)
ax.set_ylim(6, -1)        # depth axis: 6 km bottom, +1 km top, NO invert_yaxis
ax.set_xlabel("Longitude (°E)")
ax.set_ylabel("Depth (km below sea level)")
ax.set_title("Mid-Atlantic transect at 30°N (ETOPO1 / earth_relief)")
plt.tight_layout()
plt.savefig("matlantic_transect.png", dpi=200, bbox_inches="tight")
```

```{figure} ../assets/figures/F2_matlantic_transect.png
:name: F2_transect
:alt: Cross-sectional view of the Atlantic seafloor at 30 degrees north latitude. The seafloor rises smoothly from continental shelves at both edges to a peak at the Mid-Atlantic Ridge in the middle, where depth shoals to about 3 km. The profile is symmetric about the ridge, showing how the ridge sits as a long, broad mountain in the middle of the ocean basin.
:width: 100%

The Mid-Atlantic Ridge as a bathymetric transect at 30°N. Symmetric subsidence on both sides reproduces the HSC prediction; abyssal plains flatten at $\sim 5.5$ km, consistent with the plate-model asymptote (§3.5). Continental shelves at the margins are the boundaries of the oceanic lithosphere itself.
```

The point of these three blocks is not Python. It is the rhythm of the working geophysicist's first thirty minutes with a new question: identify the dataset, find its public access path, read it directly into memory, inspect metadata, plot, interpret. Real geophysical data is one `xarray` call away. *The provenance and license matter.* Always inspect before plotting. Never use a figure whose data path you cannot reproduce.

---

## 5. Forward and Inverse Problems

### 5.1 The forward problem

Given an age $t$ and the standard thermal parameters, predict the bathymetry and heat flow. We did this once already in Equation {eq}`eq:hsc-numerical`. A numerical example:

> **Question.** What ocean depth does the HSC model predict at $t = 80$ Ma?
>
> **HSC:** $d = 2500 + 350 \sqrt{80} = 2500 + 3130 \approx 5630$ m.
> **Plate model:** $d_{\max} - (d_{\max} - d_0)\, e^{-80/62} \approx 5340$ m.
> **Observation:** $\sim 5500$ m.

The plate model is a few hundred meters too shallow; HSC is a few hundred meters too deep. The disagreement is the residual that drives ongoing research (Richards et al. 2018; Holdt et al. 2025).

### 5.2 The inverse problem

The harder direction is to infer lithospheric structure from a combination of geophysical observations. The HSC equations are easy to invert — given a measured bathymetry and a known ridge depth $d_0$, you can solve for the age $t$ — but the *real* inverse problem is more interesting: given **bathymetry + heat flow + GPS strain rates + receiver functions** at a single location, what is the *full* lithospheric structure?

Two specific subproblems we will see in this and later lectures:

1. **Inferring the lithosphere–asthenosphere boundary (LAB) from receiver functions.** A receiver function isolates the P-to-S converted phases generated at impedance contrasts beneath a seismometer. Sharp positive contrasts pick out the Moho; negative contrasts at $\sim 80$–$120$ km depth under oceans pick out the LAB (Rychert & Shearer 2009). Under cratons, the same technique often fails to find a sharp LAB at all (Levin et al. 2023) — a result that becomes the central evidence for the "lithosphere is not one thing" thesis below.
2. **Inferring continental Moho from CRUST1.0 and refraction.** The CRUST1.0 map shown in Code Block B is itself the *output* of an inversion — depths are 1° averages of receiver-function and active-source refraction estimates, with gravity constraints filling gaps.

---

## 6. Comparison Matrix and Active-Learning Beats

This is the core of the lecture. We are going to build a side-by-side comparison of oceanic and continental lithosphere across eleven attributes. You will predict each row before we reveal it. Predict first; copy the answer afterward. The comparison is delivered in three beats.

### 6.1 Beat A — Composition, density, and the consequences for subduction

```{admonition} Predict
:class: tip

Before we go any further, predict the following:

1. What is the dominant rock type of oceanic crust? Of continental crust?
2. Which lithosphere is denser? Why?
3. Given (2), which lithosphere subducts at convergent margins, and which does not?
4. Sketch a density profile for each lithosphere from the surface down to 250 km.

Take five minutes. Write your answers down. We will compare them.
```

Now the reveal.

```{figure} ../assets/figures/F7_oceanic_vp_profile.png
:name: F7_oceanic_vp
:alt: P-wave velocity profile of oceanic crust shown on the left as a stepped line plot from about 1.7 km/s in the thin sediment layer near the surface, jumping to 3 km/s in pillow basalts, then 5 km/s in sheeted dykes, then 6.7 km/s in gabbro, then jumping to 8.1 km/s in mantle peridotite at the 7 km Moho. A lithology column on the right labels each layer.
:width: 90%

Oceanic crustal velocity profile from seafloor seismic refraction. Layer 1: pelagic sediments. Layer 2A: pillow basalts. Layer 2B: sheeted dykes. Layer 2C/3: cumulate gabbro. The Moho at $\sim 7$ km is sharp. Below it, $V_p \approx 8.1$ km/s peridotite — the bulk composition is uniformly mafic.
```

```{figure} ../assets/figures/F9_continental_vp_profile.png
:name: F9_continental_vp
:alt: P-wave velocity profile of continental crust on the left, gradually increasing from 1.8 km/s in surface sediments through 5.8 km/s in the upper granitic crust, then more gradually through 6.7 km/s in the middle crust and 7.2 km/s in the lower mafic crust, then jumping to 8.0 km/s in the upper mantle at the 40 km Moho. A lithology column on the right labels each layer.
:width: 90%

Continental crustal velocity profile from refraction and receiver-function synthesis. Layered but gradational: granitic upper crust, amphibolite-grade middle crust, mafic granulite lower crust, $\sim 40$ km Moho. The bulk composition is felsic-to-intermediate (andesitic average) — fundamentally different from the oceanic stack.
```

The composition difference drives every other contrast we will see. Oceanic crust is mafic basalt and gabbro all the way down. Continental crust is granitic at the top, intermediate in the middle, mafic at the base — and only mafic at the bottom because the felsic upper crust *floats* on a mafic root. Density follows mineralogy: oceanic crust averages about $2.9$ g/cm³, continental crust about $2.7$ g/cm³. Mantle lithosphere underneath is peridotite in both cases, around $3.3$ g/cm³.

Now the subtle and important point. **The mantle lithosphere beneath old continental cratons is *chemically depleted* relative to oceanic mantle lithosphere.** Repeated episodes of melt extraction over billions of years have removed iron-rich basaltic components, leaving a residual harzburgite that is slightly less dense than the underlying fertile asthenospheric mantle. This is the *Jordan tectosphere* hypothesis: cratonic mantle lithosphere is buoyant enough to resist sinking even when it is colder and older than the surrounding mantle. It is also the reason cratons are stable for billions of years and oceanic plates are recycled in 200 million.

Subduction is therefore not just a thermal-buoyancy story. It is a *thermal-and-chemical* buoyancy story. Oceanic lithosphere is dense enough to subduct because its mantle component is fertile and its crust is mafic; continental lithosphere is buoyant enough to resist subduction because its mantle component is depleted and its crust is felsic. This is the answer to the prediction question. Write it down.

### 6.2 Beat B — Thickness, seismic structure, and "what is the lithosphere?"

```{admonition} Predict
:class: tip

Predict the seismic $V_p$ profile, the depth to Moho, and the total lithospheric thickness for each of the following locations:

1. Pacific seafloor, 100 Ma old, far from any ridge or subduction zone.
2. Canadian Shield craton, Archean rocks at the surface.
3. East African Rift, active continental rifting today.

Take five minutes. Sketch a depth–velocity panel for each.
```

The reveal is the second key conceptual figure of the lecture.

```{figure} ../assets/figures/F11_continental_vs_oceanic_vp.png
:name: F11_vp_comparison
:alt: Two side-by-side panels showing P-wave velocity versus depth for continental crust on the left and oceanic crust on the right, both spanning 0 to 200 km depth. The continental panel shows a thick crust extending to 40 km, then a long lithospheric mantle, with only a weak velocity drop at the LAB. The oceanic panel shows water at the surface, a thin crust to 11 km, then a strong velocity drop at 60 km marking the LAB and the Gutenberg low-velocity zone.
:width: 100%

Continental vs. oceanic $V_p$ profiles, side by side. Oceanic Moho is sharp and shallow ($\sim 11$ km below sea level), and the asthenospheric LVZ ($\sim 60$ km) is unambiguous. Continental Moho is deeper ($\sim 40$ km) and often gradational. The continental LVZ is much weaker, and often absent entirely beneath cratons.
```

And then the figure that anchors the whole lecture.

```{figure} ../assets/figures/F6_boundary_layers_key.png
:name: F6_boundary_layers
:alt: Two-panel figure. Left panel shows oceanic lithosphere thickening with age — the mechanical boundary layer based on the 600 degree isotherm and the thermal boundary layer based on the 1300 degree isotherm both thicken as the square root of age and flatten beyond 70 Ma at the plate-model maximum. Right panel shows an old continental craton column from the surface to 350 km depth. Four different lithosphere bases are marked at different depths: elastic Te at 80 km, mechanical yield at 150 km, seismic LAB at 220 km, and thermal LAB at 280 km. All four are different.
:width: 100%

**The thesis of the lecture.** Under oceans (a), the mechanical and thermal boundary layers track each other closely as the lithosphere thickens with age, and the plate model imposes a maximum thickness of $\sim 125$ km. Under old cratons (b), four different definitions of the "lithosphere base" disagree by 200 km. *They should agree. They don't.* The lithosphere is not one thing.
```

Look at panel (b) carefully. The Moho is at 45 km — that is the crust–mantle boundary, set by composition. Above the Moho is felsic-to-mafic crust; below it is peridotite mantle. There is no ambiguity about *that* boundary.

But where does the *lithosphere* end?

- A geodynamicist who looks at how the cratonic crust supports a load uses **effective elastic thickness $T_e$** — the depth above which the rocks behave elastically over geological time. Under the Canadian Shield, $T_e \approx 80$ km.
- A rheologist who looks at the yield-strength envelope finds that the lithospheric mantle is mechanically strong down to where the temperature reaches about $\sim 700\,^\circ\mathrm{C}$ — call it the **mechanical lithosphere base** at $\sim 150$ km.
- A seismologist using S-to-P receiver functions and surface waves finds the **seismic LAB** — a region where shear velocity decreases — at $\sim 220$ km.
- A heat-flow analyst using the surface heat flow plus xenolith pressure-temperature estimates finds the conductive geotherm intersects the mantle adiabat at $\sim 280$ km, defining the **thermal LAB**.

These are not measurement errors. They are *real, observed disagreements* that have driven a generation of research. Recent papers (Levin et al. 2023) have argued that under cratons, the LAB is not a sharp boundary at all but a gradient — a zone with *frozen-in structures* left over from billions of years of tectonic accretion and modification. The lithosphere base, in this view, is not a surface in the mantle. It is a description of the rheological behavior of the rocks, and the depth at which that behavior changes depends on which physical process you ask about.

Under oceans, why do these definitions mostly agree? Because oceanic lithosphere is young, simple, and globally homogeneous. The thermal field has not had time to equilibrate into something that decouples from the mechanical behavior, and there is no buoyant chemical layer at the bottom that could outlast the thermal cooling. The lithosphere base under oceans is essentially the thermal boundary layer, full stop. Under continents — especially old continents — the lithosphere base is a four-way disagreement.

This is the answer to Beat B. Write it in your matrix.

### 6.3 Beat C — Heat flow, gravity, magnetics, age structure

```{admonition} Predict
:class: tip

Predict the following measurements:

1. Surface heat flow at 100 Ma seafloor in the central Pacific.
2. Surface heat flow on the Canadian Shield.
3. Bouguer gravity anomaly over a 5-km-deep ocean basin.
4. Bouguer gravity anomaly over the Himalayas.
5. The dominant magnetic-anomaly pattern over the Juan de Fuca Plate.
6. The dominant magnetic-anomaly pattern over the North American craton.

Three minutes. Numbers if you can; signs if you can't.
```

The reveals come quickly here. Heat flow at 100 Ma seafloor, from Equation {eq}`eq:hsc-heatflow`, is about $48\ \mathrm{mW\,m^{-2}}$. On the Canadian Shield it is $30$–$45\ \mathrm{mW\,m^{-2}}$ — *lower* than the old oceanic value, despite the much thicker crust. Why? Because cratons have low radiogenic heat production: the bulk of their continental crust is too far from the surface to contribute much, and the cratonic root has been depleted in heat-producing elements over billions of years.

Bouguer gravity over a 5-km ocean basin is strongly *positive* — about $+200$–$300$ mGal — because we have removed the gravitational effect of seawater density between the survey and the dense oceanic crust below. Bouguer gravity over the Himalayas is strongly *negative* — about $-500$ mGal — because the crustal root extends to 65–70 km depth and the dense mantle that would normally be there is replaced by lighter crust.

Magnetic signatures: the Juan de Fuca Plate shows the textbook Vine–Matthews–Morley striped pattern, with sub-parallel positive and negative anomalies recording every reversal of the Earth's field over the past 10 Ma. The North American craton shows a complex aeromagnetic pattern tied to basement terranes, batholiths, and ancient deformation — a *map of geologic structure*, not a *record of time*.

These results synthesize naturally into a coherent comparison.

```{list-table} Oceanic vs. continental lithosphere — eleven-attribute comparison
:header-rows: 1
:name: comparison_matrix

* - Attribute
  - Oceanic
  - Continental
* - 1. Composition (bulk)
  - Mafic — basalt + gabbro
  - Felsic-to-intermediate (andesitic average)
* - 2. Crustal layering
  - Layer 1 sediment, 2 basalt + dykes, 3 gabbro
  - Upper (granitic), middle (TTG / amphibolite), lower (granulite)
* - 3. Density (crust / mantle lith.)
  - $\rho_c \sim 2.9$ g/cm³, $\rho_m \sim 3.3$ g/cm³
  - $\rho_c \sim 2.7$ g/cm³, $\rho_m \sim 3.2$–$3.3$ (chemically depleted)
* - 4. Crustal thickness
  - $\sim 7$ km (almost uniform)
  - $30$–$70$ km (cratons $\sim 45$, rifts $< 30$, orogens $> 50$)
* - 5. Total lithospheric thickness
  - $0$–$125$ km, thickens as $\sqrt{t}$
  - $100$–$300$+ km; cratons $> 250$ km
* - 6. Seismic $V_p$ profile
  - Sharp jumps $2 \to 5 \to 6.7 \to 8.1$ km/s
  - Gradual $6.0 \to 6.5 \to 6.9 \to 8.0$ km/s
* - 7. Heat flow
  - Ridges $\sim 250$ mW/m², decays as $1/\sqrt{t}$ to $\sim 50$ at old ages
  - $50$–$80$ mW/m² (cratons $30$–$45$, rifts $80$–$120$); $\sim 40\%$ radiogenic
* - 8. Gravity signature
  - Bouguer strongly positive over basins; free-air $\sim 0$ over ridges
  - Bouguer strongly negative over orogens; long-wavelength cratonic geoid anomaly
* - 9. Magnetic signature
  - Vine–Matthews stripes; Layer 2A is primary source of remanence
  - Terrane-mapped anomalies tied to basement structure
* - 10. Age range / structure
  - $0$–$180$ Ma; age $\propto$ distance from ridge $\div$ rate
  - $0$–$4000$ Ma; cratonic cores $2.5$–$4$ Ga + Phanerozoic mobile belts
* - 11. Geodynamic role
  - Conveyor belt: born at ridges, recycled at trenches
  - Stable rafts; resists subduction; reservoir of continental crust growth
```

```{figure} ../assets/figures/F10_ophiolite_distribution.png
:name: F10_ophiolites
:alt: World map showing major ophiolite belts — fossil oceanic lithosphere now exposed on land — as red line segments. Belts are concentrated along the Cordilleran margin of western North America, the Appalachian–Caledonian–Uralian system, the Tethyan belt from the Alps through Cyprus to Oman and the Himalayas, and the western Pacific from Japan through the Philippines to New Guinea.
:width: 100%

Global distribution of ophiolite belts. Every red trace marks a place where a piece of oceanic lithosphere — pillow basalts, sheeted dykes, gabbros, and mantle peridotite, exactly as predicted by the Layer 1–3 stack — has been emplaced onto a continent during a continent–continent or continent–arc collision. Ophiolites are the petrological proof that the layered oceanic structure of Figure F7 is real.
```

The completed comparison matrix tells a coherent two-sentence story:

> *Oceanic lithosphere is globally homogeneous and young — its attributes are predictable from a single thermal-cooling parameter. Continental lithosphere is heterogeneous and preserves Earth history — its attributes record four billion years of accretion, deformation, and chemical evolution.*

The geodynamic role of each follows mechanically from these attribute differences. Oceanic lithosphere is dense enough, thin enough, and young enough to be recycled at trenches. Continental lithosphere is buoyant enough, thick enough, and chemically distinct enough to outlast multiple supercontinent cycles. This is the closing point of the lecture, and it sets up Module 7's remaining lectures: ridges and rifts (L27) where lithosphere is born, transforms (L28) where it slides past itself, subduction zones (L29) where it dies, and geodynamics (L30) where we put the whole conveyor in a global heat budget.

---

## 7. Course Connections

```{admonition} Where this lecture connects
:class: seealso

- **L03 (Stress, Strain, and Rheology, expanded version):** Yield-strength envelopes determine the mechanical lithosphere thickness shown in Figure F6.
- **L08–L09 (Refraction):** Source of the oceanic $V_p$ profile in Figure F7 and the synthetic record section in Figure F8.
- **L11–L12 (Whole Earth & Tomography):** Source of the seismic LAB depth estimates used in Figure F6.
- **L19–L21 (Gravity & Isostasy):** Source of the effective elastic thickness $T_e$ used in Figure F6.
- **L23–L25 (Magnetics):** Vine–Matthews stripes on the Juan de Fuca Plate; Layer 2A is the primary magnetic source.
- **L27 (Ridges and Rifts):** Picks up the oceanic-lithosphere story at $t = 0$; we will follow up with the geophysical signatures of mid-ocean ridges and continental rifts.
- **L28 (Transforms):** Sliding interfaces between lithospheric plates.
- **L29 (Subduction Zones):** Where oceanic lithosphere is recycled.
- **L30 (Plate Tectonics and Geodynamics):** Course capstone — the whole-Earth heat budget that makes all of this work.
```

---

## 8. Research Horizon

The thermal-cooling models that anchored this lecture were established between 1967 and 1977 (Davis & Lister; McKenzie; Parsons & Sclater). They have not been replaced in fifty years; they have been refined. Three recent papers are useful entry points if you want to take this lecture further:

1. **Richards et al. 2018**, *JGR Solid Earth* — re-fits the oceanic-thermal models against a globally improved compilation of basement depths and heat flow. Concludes that the plate model with a basal temperature of $\sim 1330\,^\circ\mathrm{C}$ and plate thickness $\sim 130$ km fits the global data within uncertainty, but that residual variability is still large enough to require additional mechanisms (small-scale convection, deep mantle plumes) in many regions.

2. **Holdt et al. 2025**, *JGR Solid Earth* — the most recent global re-fit, exploiting modern bathymetric and heat-flow databases. Provides the current best-fit plate-cooling parameters and a useful framework for which data sets actually constrain which model parameters.

3. **Levin et al. 2023**, *JGR Solid Earth* — reframes the LAB-under-cratons problem from "what is the depth?" to "what kind of boundary is it?" Argues that the seismic LAB beneath cratons is best understood not as a sharp interface but as a *layer of abundant frozen-in scattering structures* — the rheological transition is gradational, and the boundary inferred from seismic methods is a property of how seismic waves scatter, not where any single physical property changes abruptly.

```{admonition} Open research question
:class: note

*If the LAB beneath cratons is a gradient rather than a sharp boundary, what does that imply for the rigid-plate assumption of plate tectonics?* This is one of the open questions in current geodynamics. We will return to it explicitly in L30, the Module 7 capstone.
```

---

## 9. Societal Relevance: Siletzia and Cascadia

Every student in this room is sitting on lithosphere of a particular and unusual kind. Beneath Seattle and Portland, the continental basement is not the Proterozoic-and-younger North American craton. It is **Siletzia** — an Eocene oceanic plateau that was accreted to the North American margin around 50 Ma and now forms the basement of the entire Cascadia forearc from southern Vancouver Island to southern Oregon.

```{figure} ../assets/figures/F13_siletzia_potential_fields.png
:name: F13_siletzia
:alt: Two side-by-side maps of the Pacific Northwest showing geophysical anomalies attributed to Siletzia. Panel a shows a Bouguer gravity high (peach band) running roughly north–south along the forearc from southern British Columbia to southern Oregon. Panel b shows the corresponding aeromagnetic anomaly, with a central positive band along the Siletzia axis flanked by negative anomalies on both sides, characteristic of a magnetically stratified accreted oceanic block.
:width: 100%

The geophysical signature of Siletzia in the Pacific Northwest forearc (schematic, after Anderson et al. 2024, *Tectonics*). **(a)** A regional Bouguer gravity high marks the high-density basaltic basement. **(b)** The aeromagnetic anomaly is dipolar — a central positive flanked by negative lows — reflecting the magnetically stratified internal structure of the accreted plateau.
```

Why does this matter for a Seattle resident in 2026? Two reasons.

1. **The Siletzia–North America boundary is a tectonic suture.** Active faults like the Seattle Fault Zone reactivate weaknesses inherited from the original Eocene accretion. The seismic hazard of the Puget Lowland is not just a Cascadia-megathrust problem; it includes upper-plate faults that exist because Siletzia is welded onto a different kind of continental basement.

2. **You can see Siletzia from your laptop.** The figure above is a schematic, but Anderson et al. (2024) is open-access through the USGS Publications Warehouse and uses the same tools that you have just learned to use in §4. The Bouguer gravity map of the Puget Lowland is *downloadable*. So is the aeromagnetic grid. Every result in that paper is reproducible by a student with `xarray`, `numpy`, `matplotlib`, and an afternoon.

The lithosphere lecture is what lets you ask the right questions when you read a paper like that. Every attribute in our comparison matrix has a clear and concrete meaning over Siletzia: composition (mafic), density (high → gravity high), thickness ($\sim 30$ km in the forearc), seismic structure ($V_p \approx 6.5$ km/s consistent with basaltic basement), magnetics (dipolar pattern from stratified extrusives), age (Eocene, $\sim 50$ Ma), geodynamic role (accreted plateau, not subducted). The framework you build here is the framework you use to read the next paper.

---

## AI Literacy: AI as a Reasoning Partner

```{admonition} AI Prompt Lab — derive the half-space cooling model
:class: tip

A prompt to try with an AI assistant:

> *Derive the half-space cooling model of seafloor bathymetry from the 1D heat equation. Show all steps from the diffusion equation to the final $d(t) = d_0 + a\sqrt{t}$ form. Use Airy isostasy to convert the temperature field to bathymetry. Show the numerical prefactor.*

**Your task: grade the AI's response against the rubric below.**

| Criterion | Pass | Fail |
|-----------|------|------|
| Sets up the diffusion equation correctly with the right boundary conditions ($T(0,t) = T_s$, $T(\infty, t) = T_m$, $T(z, 0) = T_m$). | error-function solution emerges naturally | uses unphysical boundary conditions or skips the derivation |
| Correctly applies Airy isostasy: column with cold lithosphere must support the same pressure at compensation depth as a column without. | thermal contraction integral appears | conflates thermal expansion with density |
| Derives the numerical prefactor $a$ consistent with $\rho_m, \alpha, T_m, \kappa$. | gets $\sim 350$ m·Ma$^{-1/2}$ | drops factors of $\pi$, factors of 2, etc. |
| Acknowledges that the HSC model is wrong for $t > 70$ Ma. | mentions the plate model | claims HSC is exact at all ages |

If the AI produces a *plausible* derivation that is wrong on any of these criteria, that is the point. An AI assistant is a *reasoning partner*, not an oracle. Your job as a working geophysicist is to know enough physics to catch the failures.
```

This is the second time in the course you are using an AI critically as a co-derivation tool. The same pattern — write the prompt clearly, evaluate the response against a rubric of physical correctness, identify the failure modes — will reappear in L29 and L30. By the end of Module 7 you will have built your own rubric for AI-generated geodynamic claims.

---

## Further Reading

Open-access references — all linkable; we recommend at least one of each:

- **Richards, F. D., Hoggard, M. J., White, N., & Ghelichkhan, S.** (2018). Reassessing the thermal structure of oceanic lithosphere with revised global inventories of basement depths and heat flow measurements. *JGR Solid Earth* 123, 9136–9161. DOI: [10.1029/2018JB015998](https://doi.org/10.1029/2018JB015998).
- **Holdt, M. J. W., White, N., Hoggard, M. J., & Watson, A. J.** (2025). Revised oceanic plate cooling models. *JGR Solid Earth*. DOI: [10.1029/2024JB029890](https://doi.org/10.1029/2024JB029890).
- **Levin, V., Long, M. D., Servali, A., & Crawford, T.** (2023). Defining continental lithosphere as a layer with abundant frozen-in structures that scatter seismic waves. *JGR Solid Earth* 128. DOI: [10.1029/2022JB026309](https://doi.org/10.1029/2022JB026309).
- **Anderson, M. L., Wells, R. E., Frankel, A. D. et al.** (2024). Deep structure of Siletzia in the Puget Lowland: Imaging an obducted plateau and accretionary thrust belt with potential fields. *Tectonics* 43. DOI: [10.1029/2022TC007720](https://doi.org/10.1029/2022TC007720). Open access via USGS Pubs Warehouse.
- **Van der Hilst, R.** (2004). MIT OCW 12.201 *Essentials of Geophysics*, Chapter 5 (Geodynamics): half-space cooling, plate model, isostasy. [Open-access lecture notes](https://ocw.mit.edu/courses/12-201-essentials-of-geophysics-fall-2004/).
- **Seton, M. et al.** (2020). A global dataset of present-day oceanic crustal age and seafloor spreading parameters. *G-Cubed* 21. DOI: [10.1029/2020GC009214](https://doi.org/10.1029/2020GC009214) — the source dataset for Code Block A.
- **Laske, G., Masters, G., Ma, Z. & Pasyanos, M.** (2013). Update on CRUST1.0 — a 1-degree global model of Earth's crust. EGU Abstract 2658. [Data and documentation](https://igppweb.ucsd.edu/~gabi/crust1.html) — the source dataset for Code Block B.

---

```{admonition} Concept checks for §6
:class: note

Try these before the next class meeting; we will go over them in discussion.

1. **HSC numerical practice.** Compute the predicted ocean depth at $t = 25$ Ma using the HSC numerical form (Eq. {eq}`eq:hsc-numerical`). What is the predicted surface heat flow at the same age?
2. **Plate-model asymptote.** Show analytically that the plate-model depth (Eq. {eq}`eq:plate-depth`) reduces to the HSC form for $t \ll \tau$. (Hint: Taylor-expand the exponential.)
3. **The lithosphere is not one thing.** A geophysicist measuring effective elastic thickness $T_e$ in a continental craton finds $T_e = 90$ km. A seismologist using S-to-P receiver functions at the same location finds a LAB at $\sim 200$ km. A heat-flow analyst, using surface heat flow and a xenolith-constrained geotherm, infers the thermal LAB at $\sim 270$ km. Are these three measurements *inconsistent*? Explain in two sentences.
4. **Siletzia.** Using only the comparison matrix from §6.3, predict the gravity signature, the magnetic signature, and the heat flow over Siletzia *before* you look at a published figure. Then compare to Anderson et al. 2024. Where did your predictions match? Where did they fail?
```
