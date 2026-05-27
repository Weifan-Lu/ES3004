# L27 — Concept Check Answer Key
## Instructor-private grading reference

Four concept-check questions from the lecture markdown §Concept checks. Each is worth 2 points unless otherwise noted; total = 8 points. Use the rubric below as a guide; partial credit is generous when the geophysical reasoning is sound even if the numerical answer is off.

---

## Q1 — Spreading-rate calculation (2 points)

> *A magnetic-anomaly profile across the South Pacific shows the C5 chron (10.95 Ma reversal centre) at 410 km from the axis. What is the half-spreading rate at this location? Is this slow, intermediate, or fast?*

### Answer

Apply equation (eq:stripe-distance):
$$
r = \frac{d_n}{t_n} = \frac{410 \text{ km}}{10.95 \text{ Ma}} = 37.4 \text{ km/Myr} = 3.74 \text{ cm/yr}.
$$

This is an **intermediate-spreading** half-rate (full rate ≈ 7.5 cm/yr). The classification thresholds (from §2.2 and Fig. F4):
- Slow: < 4 cm/yr full rate (< 2 cm/yr half-rate)
- Intermediate: 4–8 cm/yr full rate (2–4 cm/yr half-rate)
- Fast: > 8 cm/yr full rate (> 4 cm/yr half-rate)

The Pacific has several intermediate-spreading ridges (East Pacific Rise southern segments, Juan de Fuca, Galapagos Spreading Centre).

### Rubric

- 1.5 pt for the correct numerical half-rate (3.74 cm/yr; accept 3.5–4 cm/yr).
- 0.5 pt for the correct classification (intermediate).
- Half credit (1 pt) if the student got a half rate but used full-rate classification thresholds.
- Zero if no unit handling — common error is reporting "37 cm/yr" because they forgot km → cm.

---

## Q2 — Non-uniqueness disambiguation (2 points)

> *You have the Bouguer profile of Round 1 and access to one additional measurement. You may choose between (i) seafloor surface heat flow at 30 stations along the transect, (ii) seismic Vp tomography to 50 km depth, or (iii) a magnetic stripe sequence. Which would you choose and why? Justify in 100 words or fewer.*

### Answer

The best single additional observable is **(ii) seismic Vp tomography to 50 km depth**. Reasoning:

- Model A (shallow + narrow + Δρ = −0.040) has its low-density anomaly at 10–50 km — squarely within the tomographic resolution. A Vp anomaly localised in that depth range would confirm Model A.
- Model B (deep + broad + Δρ = −0.020) has its anomaly extending to 220 km — much of it *below* the tomographic window. Crucially, even the upper part of Model B should show a broader, weaker Vp anomaly than Model A. The signature is distinguishable.
- Heat flow (i) is in principle useful but harder to interpret — both models predict elevated axial heat flow with similar magnitudes; the spatial gradient is the distinguishing feature, but it is contaminated by hydrothermal advection.
- Magnetic stripes (iii) constrain *spreading rate*, not density structure. They don't help with this specific ambiguity.

### Rubric

- 2 pt for choosing (ii) with a good justification that distinguishes "depth + amplitude resolution".
- 1.5 pt for choosing (ii) with a vaguer justification ("seismic gives velocity structure").
- 1 pt for choosing (i) with a sound justification (the spatial gradient of heat flow does discriminate, just less powerfully).
- 0 pt for choosing (iii) — this answer reveals a misunderstanding of what magnetics constrains.

---

## Q3 — Rifting continuum stage (2 points)

> *The Rio Grande Rift in New Mexico shows surface heat flow ~80 mW/m², modest Bouguer low (~−100 mGal), bimodal alkaline volcanism, β ≈ 1.2, and shallow extensional seismicity. Which stage of the rifting continuum is it? Justify in two sentences.*

### Answer

The Rio Grande Rift is at the boundary between **stage 2 (incipient rifting)** and **stage 3 (mature continental rift)**, leaning toward stage 2.

Justification: β ≈ 1.2 places it cleanly in the lower part of the stage 2 range (1.1–1.3) and below the stage 3 range (1.5–2.5). Heat flow at 80 mW/m² is on the boundary (stage 2: 60–70; stage 3: 80–120). The bimodal alkaline volcanism is characteristic of stage 3, but the modest Bouguer low at −100 mGal (vs. stage 3's typical −150 to −250 mGal) suggests less mantle-lithosphere thinning than a fully mature rift like Kenya. The Rio Grande Rift is geologically intermediate between Baikal-style incipient extension and the canonical East African Rift mature segments.

### Rubric

- 2 pt for stage 2 or "between 2 and 3" with at least one referenced attribute supporting the classification.
- 1.5 pt for stage 3 with a justification referencing the bimodal volcanism (an honest reading; the system is on the boundary and reasonable people disagree).
- 1 pt for an unambiguous wrong answer (stage 1 or 4+).
- Half credit (1 pt) for the right stage but no specific attribute justification.

Note: the Rio Grande Rift is genuinely a boundary case. Some references classify it as stage 2 (Baldridge et al. 1995); others as stage 3 (Wilson & Aster 2003). Either answer is defensible with appropriate justification.

---

## Q4 — AI failure mode diagnosis (2 points)

> *A student runs Code Block D on a magnetic profile across the slow-spreading Reykjanes Ridge at 30°W. The `find_peaks` output shows ~12 peaks per side of the axis, but only ~4 polarity reversals are expected in the corresponding 8-Myr-old crust. Describe two plausible failure modes and how you would diagnose each.*

### Answer

Two plausible failure modes, in order of likelihood:

1. **Prominence threshold too low.** The `find_peaks(prominence=80)` call in Code Block D was tuned for the JdF profile in F5. The Reykjanes Ridge magnetic signal has a different overall amplitude (Reykjanes is at high latitude, where induced magnetisation is strong; basement topography is rough; ridge geometry is oblique). A prominence threshold appropriate for JdF may include local maxima from basement topography or noise that don't correspond to polarity reversals.
   - **Diagnosis**: visually inspect the profile + peak markers. If "peaks" are clearly within a single Brunhes-aged region with no expected reversal, the prominence is too low. Tune up.

2. **Basement topography aliases as anomaly peaks.** The Reykjanes Ridge has thick Layer 2A and pronounced block-faulting from slow-spreading detachment-style accretion. The basement topography itself produces magnetic anomalies of similar wavelength to the polarity stripes. `find_peaks` cannot distinguish a real polarity reversal from a topographic high in the same wavelength band.
   - **Diagnosis**: cross-correlate the profile against the GPTS at multiple spreading rates. If no consistent best-fit rate emerges, the data are likely contaminated. Alternatively, use bathymetric correction or independent age constraint to remove the topographic signal.

Less likely but defensible additional answers:

3. *Reduction-to-the-pole correction has not been applied*. The Reykjanes Ridge is at high latitude where induced magnetisation is nearly vertical, so the reduction is small; but the procedure normalises peak shape across the profile.
4. *Distance from axis was computed using a fixed latitude (47°N) when the actual profile is at 64°N*. Distance scaling is then 17% too small. Less likely to add false peaks but does shift the inversion.

### Rubric

- 2 pt for any two reasonable failure modes with diagnostic strategies.
- 1.5 pt for two failure modes with diagnostic strategies that are vague.
- 1 pt for one good failure mode + diagnostic.
- 0.5 pt for any failure mode without a diagnostic strategy.

The key teaching point this question lands: AI/algorithm tools require *physical* understanding to diagnose their failures. A student who answers "it's a noise issue, you should re-tune" without explaining *what* noise is from misses the geophysical content.

---

## Total: 8 points

Expected mean: 6.0/8 (75%).
Difficulty floor: Q1 should be near-universal credit.
Difficulty ceiling: Q4 separates students who have internalised the AI-as-Tool framing from those who treat it as a discrete add-on.
