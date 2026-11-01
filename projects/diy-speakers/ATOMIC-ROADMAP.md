# Atomic Development Plan — Modular Stereo 2.1

Date: 2026-10-30. Status: **decision gates only; no unapproved purchases**.

## Owner objectives

- Near-field listener 0.60–0.80 m; room about 19 m² but not a permanent acoustic environment.
- Heard reference ADAM T5V; T8V is a comparison target, not a mandate to replicate a brand.
- Two manageable desktop satellites, separate deep-bass subwoofer. Retain a path to 2.2.
- Preserve transparent, expressive midrange and controlled highs while producing impactful low frequencies.
- Beautiful real-wood appearance; modular electronics, driver/cabinet serviceability and optional replaceable baffles.
- Initial staged outlay roughly 50–100k RUB, potentially up to 200k RUB over a longer development process; no expensive parts 'for prestige'.

## Proposed interface architecture

```text
PC / separate local player receiver / future selected input
                        |
            content / sound engine (bypassable)
                        |
         speaker DSP / calibrated crossover / limiter
                 |            |            |
          sat-L channels  sat-R channels  sub channel
              LF+HF          LF+HF          LF
                 |            |            |
           amp channels   amp channels   amp+protect
                 |            |            |
             satellite-L  satellite-R   sub enclosure
```

Choose one of two baseline electronics configurations by simulation and budget:

- **Passive satellites + active sub:** 2 main amplifier channels, 2 passive crossovers, sub amplifier/DSP. Lowest interconnect count and easier early stereo setup, but passive crossover is still a substantial acoustic and component design task.
- **Active two-way satellites + active sub:** 5 independent amplifier outputs and 5-channel DAC/DSP path (4 satellite driver channels + 1 sub). Enables per-driver delays, EQ and protection; extra electronics, cabling and careful gain/noise design. The four satellite amplifier channels need not all be high-power.

A single flexible processing API should support both, with **explicit profile versioning** so speaker calibration and user content processing cannot accidentally apply double EQ. External electronics may be preferable while the speaker enclosures are being iterated.

## Gates and deliverables

| Gate | Concrete deliverable | Acceptance condition | Buying requirement |
|---|---|---|---|
| G0 — goals | Audibility-neutral objective list and listening reference | Define main listening SPL/peak target, sub floor at defined SPL and allowed cabinet footprint | None |
| G1 — source corpus | Source-linked CSV/JSON for 5–7in mids, 3 tweeters, 10/12in subs | Valid Fs/Qts/Vas/Sd/Xmax, frequency/impedance curves, supply status and per-source provenance; mark missing | None |
| G2 — linear acoustic simulations | Sealed / vented / passive-radiator envelopes, driver excursion, port velocity, DSP boost, preliminary dimensions | At least 2 satellites × 2 sub candidates with explicit 25/30/40/80 Hz bounds, sensitivity to T/S tolerance | None |
| G3 — crossover and layout | Passive vs active two-way crossovers, polar/baffle/desk reflection model | Off-axis design, reasonable tweeter integration, phase/delay and low-noise amplifier budget | None |
| G4 — electronics testbench | Reproducible stereo+sub DSP settings, clipping and voltage/current thermal tests | Demonstrated gain/headroom, limiter stability, bypass path, power reserve and no unsafe failure state | Reuse PC/software and inexpensive development hardware if required |
| G5 — one satellite | Provisional plywood/MDF box with replaceable front panel; one midwoofer and one tweeter | Measured impedance, nearfield/gated response, off-axis curves, distortion, mechanical resonance and listening notes | First driver pair + prototype materials |
| G6 — stereo pair | Matched second satellite and placement fixtures for 60–80 cm | Response consistency, real room measurement and smooth listening transition | Second driver pair; amp/DAC if not yet present |
| G7 — subwoofer | Separate 10- vs 12-in modeled enclosure and purchased chosen driver with own amp | Measured extension at specified seat SPL with excursion/THD/thermal and protective limits | Chosen sub driver, enclosure, power |
| G8 — integration / 2.1 | Crossover to sub, corrected arrival times, profiles and bass placement | Controlled bass without audible hole/excess in 60–130 Hz crossover region; protection survives stress | Mostly software, microphone and fixtures |
| G9 — finish & expansion | Finished wooden/composite enclosures and possible second sub | Moisture/finish/durability, aesthetics and repeatability; second sub only if measured benefit | Later, optional |

## Cost allocations — planning envelopes, NOT current vendor quotes

**Phase I — first enjoyable stereo system** (rough planning target 50–100k RUB):
- Main driver pairs (2 × midwoofer, 2 × tweeter): ~20–35% of Phase-I budget.
- Amplification / DAC / DSP / safety: ~20–35%.
- Provisional and final cabinet materials / woodworking: ~15–25%.
- Measurement tooling / electrical accessories / replacements / delivery contingency: ~15–25%.

These percentages are not a full BOM and intentionally allow overlap/ranges. A fixed invoice requires current Russian landed quotes and the actual chosen topology. It is reasonable to spend early on a reusable individually calibrated microphone and a reference processing chain, but the same expense need not be repeated for the sub.

**Phase II — add strong subwoofer** (incremental):
- Driver: compare 10- and 12-in based on *total* enclosure/amp cost and bass at specified SPL, not bare unit price.
- Separate rated power supply, filtering/limiter, enclosure, vibration control and cabling.
- Evaluate whether cumulative cost may rise toward 200k RUB, with explicit allowance for revision/returns.

No commitment to spend the upper range. Each gate must preserve useful parts and allow terminating the project with a satisfying finished pair.

## Model fidelity / evidence discipline

### What the first model proves
The [existing baseline](simulation/acoustic_baseline.py) has verified small-signal sealed-box formulas and ideal LR4 electrical filter sums. The [candidate comparison](simulation/compare_candidates.py) computes first-order Fc/Qtc/F3 and displacement using manufacturer data, and never fills in absent Xmax values.

### What the first model does NOT prove
No live speaker has been measured; no 25-Hz at target SPL, no off-axis polar curve, no actual distortion comparison, no desk/room modes, no vent air velocity, no thermal compression, no validated dynamic amplifier gain/headroom. These are next proof obligations; do not convert the calculated F3 into a performance promise.

### Model progression
1. Complete T/S and dimension inputs with temperature/tolerance variation.
2. Sealed & ported bass + enclosure group delay and port area/velocity (including excursion as a function of input voltage).
3. Import actual frequency/phase and impedance datasets; model on/off-axis and baffle radiation.
4. Simulate closed-loop calibrated DSP crossover, driver delay and level-dependent limiting.
5. Match modeled vs measured data from a single inexpensive mechanical prototype; correct the model before final build.

## Design trade-off experiments (no purchases yet)

**Satellites:**
- 5-in SB15MFC30-8 vs 6-in SB17NRX2C35-8 in first trial net sealed 8 vs 12 L.
- HiVi M6N-B as cost/value challenger, using its own official data.
- One fabric-dome and one aluminum-dome tweeter, optionally with waveguide and interchangeable baffle.
- Optionally compare SB17MFC35-8 for an alternate soft-cone 6-in approach.

**Subwoofer:**
- 10-in Dayton DCS255-4 price floor vs Dayton RSS265HO-4 higher displacement; SB29SWNRX-S75-6 is a lower-Fs additional contender.
- Compare 12-in Dayton RSS315HF-4 for displacement and enclosure/floor area tradeoffs.
- Account for in-room LF modes; use sub placement separately from satellite desk placement.

## Measurements without a treated studio

- Get calibrated USB measurement mic, or rent one; use REW for measurements; note REW is freeware rather than open-source.
- Use repeatable gated mid/high measurements; small-signal nearfield/groundplane for bass with correct assumptions and merging.
- Check multiple angles and drive levels, stereo matching and output noise at 0.6–0.8 m.
- Aim for subjective level-matched comparisons rather than claims that a costly cone material inherently sounds superior.
- Room treatment is optional, but placement and room modes are **not** optional physical effects. No amount of DSP can universally invert deep cancellation nulls.

## Acceptance targets currently provisional

- Sub extension *candidate*: 25–30 Hz at a to-be-defined listening SPL and distortion ceiling.
- Sub crossover study: 70–110 Hz in 10-Hz increments; acoustic adjustment by measured arrival time/phase.
- Main two-way crossover: not yet selected; must follow polar and distortion measurements, not tweeter Fs alone.
- Need user preference for typical/max listening loudness and available floor position for sub; until known, run small/medium/loud design cases and label them assumptions.

## Deliverable discipline

Every numerical result receives source file URL, exact part revision, model commit, units, assumptions, scripts, automated assertions, known mismatches and source vs result separation. Avoid selecting a 200k-RUB BOM while the project is still at a free simulation gate.


## Cross-cutting research: wired optical audio fabric

[Wired Audio Fabric](wired-audio-fabric/README.md) adds separate digital data/control scheduling, local per-speaker DACs, receiver-side buffering, endpoint identities, clock discipline and wired optical link research. The [first executable contract](wired-audio-fabric/simulation/README.md) covers logical pause/stop/epoch/fault handling, not PHY, security hardware, clock synchronization or analog performance. Treat it as a reusable foundational module that can be prototyped in software **in parallel with** driver/acoustic planning, without purchasing a full enclosure or complete amplifiers.


## First physical foundation: reusable power modules

The owner selected power supply/protection development as the first physical foundation, reused by multiple DIY devices. The [shared-power module](../shared-power/README.md) compares certified external AC/DC adapters and serviceable low-voltage local regulators, hardware short/overtemperature protection, output-noise qualifications and fanless vs acoustically isolated fan-cooled electronics compartments. All unsafe mains and surge testing remains for appropriately qualified facilities. The independent four-plane logical audio system is described in [FOUR-PLANE-ARCHITECTURE.md](wired-audio-fabric/FOUR-PLANE-ARCHITECTURE.md).


## Design kickoff — 2026-11-01

We start with [DESIGN-KICKOFF-D0.md](DESIGN-KICKOFF-D0.md): compare SB15MFC30-8 (5in), SB17NRX2C35-8 (6in), HiVi M6N-B, two SB Acoustics tweeters, and three 10/12in Dayton sub drivers. First preliminary inverse-Qtc closed-box calculation is [simulation/design_sweep.py](simulation/design_sweep.py), with reproducible assertions. The **first physical build remains the independent safe low-voltage DC power module**; its detailed rail/power ratings will follow acoustic/electronics envelope calculations. No components have been ordered or mechanically frozen.


## Three-way / subwoofer combination extension — 2026-11-01

The user explicitly requested **missing bands of a true three-way satellite (LF+dedicated MID+HF)** plus a serious independent low-frequency sub. See [THREE-WAY-PLUS-SUB-RESEARCH.md](THREE-WAY-PLUS-SUB-RESEARCH.md) and [simulation/threeway_system_candidates_2026-11.json](simulation/threeway_system_candidates_2026-11.json) for full seven-channel/driver-only costs and same-market Chinese Wavecor candidates. Continue to compare a five-channel two-way+sub baseline at 0.6–0.8 m and never assume that adding a dedicated mid makes the speaker objectively better. The final aesthetic enclosure remains LAST.
