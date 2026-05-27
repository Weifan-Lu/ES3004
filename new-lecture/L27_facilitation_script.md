# L27 — Facilitation Script
## Instructor-private classroom timing and prompts

This is a 50-minute lecture (standard ESS 314 length). The plan below is *not* a script to read; it is a timing-and-emphasis framework. Italicised text is what to say aloud or write on the board; non-italicised text is what to do or prepare.

## Time budget

| Time | Block | Activity |
|------|-------|----------|
| 0–5 min | Open | Frame the rifting continuum question; show EAR map (F6) |
| 5–15 min | Physics | Stretching factor + ridge magmatic system + McKenzie subsidence |
| 15–22 min | Math | Magnetic stripe inversion + ridge gravity decomposition |
| 22–35 min | **Round 1** | Predict (4 min) → reveal F3 → discuss (5 min) |
| 35–43 min | **Round 2** | Predict the rifting continuum (5 min) → reveal F12 (3 min) |
| 43–46 min | PNW anchor | JdF + Axial Seamount + OOI cabled array |
| 46–50 min | Close | AI literacy callout + concept-check preview |

Total = 50 minutes. Each block has slack of 1–2 minutes. The two predict-then-reveal rounds together take 21 minutes — about 40% of the lecture, deliberately the largest single block.

## Pre-class setup

- [ ] Whiteboard or screen with the lecture markdown's framing question visible from the start.
- [ ] Marp slide deck cued at slide 1.
- [ ] If using clicker / Slido for Round 1 and Round 2 predictions, prepare the polls in advance.
- [ ] Print or share the Round 2 attribute table as an unfilled worksheet (six stages × six attributes = 36 empty cells). Students will fill cells during Round 2.

## Block 1 (0–5 min) — Open the rifting continuum

Show slide 3 (Geoscientific question) and slide 4 (EAR system map, F6).

Say aloud:
> *Mid-ocean ridges and continental rifts both extend the lithosphere. Why do they look so different in gravity, heat flow, and magnetics — and how do we know they are the same physical process?*

Walk the EAR map from south to north:
> *Down here in southern Tanzania the lithosphere is just beginning to crack. By the time we get to the Main Ethiopian Rift in the middle, the crust is already thinned to 25 km. At Afar the rift floor has dropped below sea level. By the Red Sea and Gulf of Aden, it's a real ocean spreading centre. The same rift system, end to end, contains the whole story.*

Frame the next 50 minutes:
> *Today we'll work through that continuum and see how each stage looks in gravity, magnetics, heat flow, and seismicity.*

## Block 2 (5–15 min) — Governing physics

Move through slides 5–7 efficiently. Three things to land:

1. **Stretching factor β** (slide 5). Make sure students see that β = 1 at the craton end and β → ∞ at the MOR end. The whole continuum is parametrised by this one variable.
2. **Ridge magmatic system** (slide 6, F1). Point out the axial melt lens, the broader mush zone underneath, the dyke injection from there to the surface. *Note*: the AML on slow-spreading ridges is small or absent. F4 will return to this.
3. **McKenzie 1978** (slide 13). Two timescales: syn-rift (fast, mechanical) and post-rift thermal (slow, $\sqrt{t}$). The Steer's-head basin is every passive margin on Earth.

Suggested transition phrase:
> *That's the physics. Now let's see how it shows up in the data.*

## Block 3 (15–22 min) — Math and Code Block D

Two equations and one code block:

1. Magnetic stripe inversion: $r = (d_n - d_m) / (t_n - t_m)$. Write on the board.
2. Ridge gravity decomposition (handwave the integral; emphasise the *negative* Bouguer over the *positive* topographic high — students often need to hear this twice).
3. **Code Block D** (slide 18). This is the fourth canonical block of the course. Run through the four lines: load EMAG2 → take a transect → `find_peaks` → fit. The pattern recurs throughout geophysics.

Show slide 19 (F5) briefly. Note the inverted half-rate (2.17 cm/yr) vs. the reported value (2.85 cm/yr). Hold the "why is it off" discussion for the AI literacy callout near the end.

## Block 4 (22–35 min) — ROUND 1: MOR gravity non-uniqueness

This is the first active-learning round. Slide 9 (predict).

Say:
> *I'm going to show you a clean Bouguer profile across a mid-ocean ridge. Amplitude is about minus 250 mGal at the axis, half-width is about 200 km. I want you to sketch the 2D density-anomaly cross-section that explains it. You choose depth, width, and density contrast. You have no other measurement.*

Students work for **4 minutes**. Walk the room; eavesdrop. Watch for groups who go straight to "shallow narrow" — that is the Model A answer and is correct but partial. Watch for groups who try "deep broad" — that is the Model B answer and is also correct. Confronting both groups during the reveal is the pedagogy.

After 4 minutes, ask **2–3 groups** to share their model. Pick groups with visibly different answers. Don't comment yet on which is right; just collect them.

Slide 10 (reveal, F3). Walk through:
> *Here are two models. Look at the top panel — both curves go right through the data. Now look at the bottom panels. Model A says the anomaly is shallow and narrow with a big density contrast. Model B says deep and broad with a small contrast. Both are completely consistent with the gravity profile.*

Pause. Let it sink in.

Slide 11 (discuss). Say:
> *Both interpretations are valid given gravity alone. Which additional measurement would let you decide between them?*

Take 2–3 student suggestions. Likely answers: heat flow (the focused shallow body should produce a hotter axial heat-flow anomaly than the broad deep one); seismic Vp (a tomographic image to 50 km depth would resolve the shallow body cleanly); mantle Bouguer anomaly (correcting for bathymetry separates topographic effects from mantle).

Pedagogical close on this block:
> *Single-method gravity is constitutively non-unique. The fix is the multi-method synthesis principle from L26 — the lithosphere is a vector of observables, not a single number. We'll see this pattern again in L29 and L30.*

## Block 5 (35–43 min) — ROUND 2: The rifting continuum

This is the second predict-then-reveal round. Slide 21 (predict).

Hand out the unfilled six-stage × six-attribute worksheet. Six stages along the top, six attributes down the side.

Say:
> *Here are the six stages. For each one, predict the sign and rough magnitude of: Bouguer anomaly, surface heat flow, topographic expression, stretching factor beta, dominant magmatism, dominant seismicity. Work in pairs. You have 5 minutes.*

Walk the room. Most groups will be confident on the endpoints (stage 1 craton, stage 6 fast MOR) and uncertain in the middle. Some will conflate stages 4 and 5 (the rift-to-spread transition vs. slow MOR). Some will try to use a single sign across the whole row, missing that several columns flip sign through the continuum.

After 5 minutes, reveal F12 (slide 22).

Don't try to walk through every cell. Instead, pick **3 cells** to discuss:

1. *Bouguer at stage 3 vs. stage 6*: −150 to −250 vs. just slightly negative. Why does the magnitude *decrease* as the rift becomes a mature ocean ridge? (Because at stage 6 the mantle root is broad and diffuse, not concentrated.)
2. *Topography at stage 4*: thin crust, just below sea level. The transition. Land this with a verbal pointer to Afar.
3. *Magma at stage 5 vs. stage 6*: episodic vs. continuous. Connects directly to F4 (the AMC depth scatter).

The full answer key is in `L27_master_matrix.md`.

## Block 6 (43–46 min) — PNW anchor

Slide 23 (JdF + Axial). Don't rush this; this is the lecture's "this is your home" moment. Talk about Axial Seamount as the only fully cabled MOR observatory in the world. Mention the 2015 eruption recorded in real time. Drop the "Cascadia is a complete plate-tectonic system in driving distance from Seattle" line.

If Emily Wilbur (TA) is present or has prepped material, hand off briefly — the PNSN catalog connection works well here.

## Block 7 (46–50 min) — AI literacy + close

Slide 24 (AI as Tool). Bring back the 2.17 cm/yr vs 2.85 cm/yr discrepancy from Code Block D.

Say:
> *Why was our inverted spreading rate 25% off? Because find-peaks doesn't know geophysics — it just picks local maxima. With a slightly higher prominence threshold, it would do better. With a deep-learning picker, it would also do better. But neither tool can recover information the data doesn't contain.*

Land the four failure modes from the lecture markdown (magnetic equator, slow-spreading roughness, polar regions, sediment cover) by reading the slide. Close with:
> *AI tools succeed in the data-rich middle of parameter space. They fail in the geophysically interesting edge cases. Your job is to know enough geophysics to recognise when the tool is lying.*

Slide 25 (concept checks + transition to L28). Preview L28 (Convergent Margins) in one sentence:
> *Today we built the plate at the ridge. Next time we'll watch it die at the trench.*

End class on time.

## Common in-class adjustments

- **Round 1 ran long.** Cut the McKenzie subsidence math in Block 2 to 2 minutes; defer to next class as a reading.
- **Round 2 ran long.** Truncate the PNW anchor to 1 minute; rely on slide 23 alone.
- **Students struggle with non-uniqueness in Round 1.** Spend an extra 2 minutes on the seismic Vp answer. This is more valuable than the rifting continuum table — the principle generalises further.
- **Students dominate Round 2 with right answers immediately.** Skip directly to F12 reveal and use the saved time to discuss why the EAR system spatially preserves the continuum.

## Connecting to other materials

- The concept checks at the end of the lecture markdown become the homework for next class.
- The Round 2 matrix returns explicitly in the Friday discussion (Session 7 — Inside the Planet) as the synthesis vehicle for the whole rifting concept.
- Code Block D is the entry point for a possible Lab on magnetic-stripe analysis if added later in the course.
