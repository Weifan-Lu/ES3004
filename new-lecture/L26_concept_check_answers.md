# L26 Instructor-Private: Concept-Check Answer Key

For the four concept checks at the end of the lecture markdown.

---

## Q1. HSC numerical practice

> *Compute the predicted ocean depth at $t = 25$ Ma using the HSC numerical form $d(t) = 2500 + 350\sqrt{t}$ m. What is the predicted surface heat flow at the same age?*

**Bathymetry:**
$d(25) = 2500 + 350 \sqrt{25} = 2500 + 350 \times 5 = 2500 + 1750 = 4250 \ \text{m}$.

**Heat flow:** Using $q(t) = k(T_m - T_s)/\sqrt{\pi \kappa t}$ with $k = 3.1$ W/m/K, $T_m - T_s = 1350$ K, $\kappa = 10^{-6}$ m²/s, $t = 25 \times 3.15 \times 10^{13}$ s:

$$q = \frac{3.1 \times 1350}{\sqrt{\pi \times 10^{-6} \times 7.88 \times 10^{14}}} \ \text{W/m}^2$$
$$\approx \frac{4185}{\sqrt{2.47 \times 10^9}} \approx \frac{4185}{49700} \approx 0.084 \ \text{W/m}^2 = 84 \ \text{mW/m}^2.$$

Acceptable answers: $80$–$90$ mW/m². Students who use $\sqrt{t}$ in Ma without unit conversion will get a result off by ~$\sqrt{3 \times 10^{13}}$. Common mistake.

**Grading:** Full credit for both numbers and units; half credit if depth is right but heat flow has unit-conversion errors.

---

## Q2. Plate-model asymptote

> *Show analytically that the plate-model depth reduces to the HSC form for $t \ll \tau$.*

The plate-model depth (Eq. {eq}`eq:plate-depth`):
$$d(t) = d_{\max} - (d_{\max} - d_0)\, \exp(-t/\tau).$$

Taylor-expand the exponential for $t/\tau \ll 1$:
$$\exp(-t/\tau) \approx 1 - t/\tau + \tfrac{1}{2}(t/\tau)^2 - \cdots.$$

To leading order:
$$d(t) \approx d_{\max} - (d_{\max} - d_0)(1 - t/\tau) = d_0 + (d_{\max} - d_0)\, \frac{t}{\tau}.$$

This gives a *linear* dependence on $t$, **not** a $\sqrt{t}$ dependence. The leading-order Taylor expansion is not the right comparison.

**The actual argument** is that for $t \ll \tau$, the plate-model temperature field has not yet "felt" the basal boundary condition at $z = L_p$. The error-function profile of HSC and the plate-model profile match in this limit. The correct way to show the equivalence is through the temperature solution: both models satisfy the same heat equation with the same upper boundary condition $T(0,t) = T_s$, and differ only in whether they impose a basal condition at $z = L_p$. For times short compared to the diffusion time across $L_p$ (i.e., $t \ll \tau = L_p^2 / (\pi^2 \kappa) \approx 62$ Myr), the thermal field has not yet diffused down to $L_p$, so the two models produce identical temperature profiles and therefore identical bathymetry.

**Grading:** Students who Taylor-expand the closed-form bathymetry will get a linear-in-$t$ answer, which is wrong as a derivation but right as a "the two models agree at small $t$" insight. Give partial credit and use this question in discussion to surface the deeper point about diffusion timescales.

---

## Q3. The lithosphere is not one thing

> *A geophysicist measuring effective elastic thickness $T_e$ in a continental craton finds $T_e = 90$ km. A seismologist using S-to-P receiver functions at the same location finds a LAB at $\sim 200$ km. A heat-flow analyst, using surface heat flow and a xenolith-constrained geotherm, infers the thermal LAB at $\sim 270$ km. Are these three measurements *inconsistent*? Explain in two sentences.*

**Model answer:**
These measurements are not inconsistent because they measure different physical properties: $T_e$ measures the *elastic-flexural* response of the lithosphere on geological timescales, the seismic LAB measures the depth at which shear-wave velocity drops sharply due to a change in seismic properties, and the thermal LAB measures the depth at which the conductive geotherm intersects the mantle adiabat. Each definition captures a different aspect of how lithosphere transitions to asthenosphere, and under old continental cratons — where the lithosphere has had billions of years to develop chemical depletion, thermal equilibration, and rheological gradation — these definitions can disagree by 100+ km without contradiction.

**Look for:** any acknowledgement that the definitions probe different physics. Common error: students who say "the seismic LAB is the *true* LAB and the others are approximations." Mark this down — it misses the lecture's central thesis.

---

## Q4. Siletzia

> *Using only the comparison matrix from §6.3, predict the gravity signature, the magnetic signature, and the heat flow over Siletzia before you look at a published figure. Then compare to Anderson et al. 2024. Where did your predictions match? Where did they fail?*

**Predictions from matrix:**

| Attribute | Matrix prediction for Siletzia (oceanic plateau) | Observation |
|-----------|--------------------------------------------------|-------------|
| Gravity | Bouguer high (high-density basaltic basement, like oceanic crust) | ✅ Bouguer high observed (Anderson 2024 Fig. 1, 5) |
| Magnetics | Vine–Matthews stripes *or* high remanent magnetization (Layer 2A character) | ⚠️ Partial — Siletzia shows strong magnetic anomalies, but pattern is *not* striped because the plateau formed off-axis (probably plume-related) and has been subsequently deformed by accretion |
| Heat flow | Should be intermediate — old oceanic ($\sim 50$ Ma) is "old enough" to have cooled, so ~55 mW/m² | ⚠️ Higher than predicted ($60$–$80$ mW/m² in the Cascadia forearc) due to forearc thermal complications (subducting Juan de Fuca slab brings cold material, but radioactive sediments and forearc circulation complicate the simple HSC prediction) |

**The valuable failure**: the heat-flow prediction fails because the matrix entries assume *steady-state* oceanic lithosphere far from a plate boundary. Siletzia is at a *convergent* margin — a totally different thermal regime. Students who notice this are doing real geophysics.

**Grading:** full credit if all three predictions are made and at least one is critiqued against the data. Bonus credit for noticing that the matrix is a *simplified* tool that fails in tectonically complex settings.
