# Premium DIY Loudspeakers — Research Concept

Status: **owner constraints captured / stereo 2.1 preferred research baseline; parts and manufacturing not frozen**.

## New wired digital transport concept — 2026-11-01

The owner proposed a **wired-only, optical** distributed audio system: PC→digital controller over USB-C, separate duplex optical links to independently powered satellites and subwoofer, deep receiver buffering with independent high-priority commands, sample-clock synchronization, authenticated device identities and rigorous model-level contracts. The correct digital-audio interpretation places local DACs *after the fiber* in the active speakers, unless a separately modeled analog-optical link is deliberately chosen.

This is a **research direction**, not a fixed PHY or complete cryptographic architecture. The portable player+earbud radio design is a separate scope. Documents and first executable contract: [wired-audio-fabric/](wired-audio-fabric/README.md).

## Owner clarification — 2026-10-30

- Room approximately 19 m², with future room changes possible.
- Main loudspeakers **on/near the desk with several computer monitors**, listener approximately **0.60–0.80 m** from the speaker; physical dimensions secondary to acoustics and total cost.
- **Deep, physically perceptible bass is mandatory**, but the midrange must retain clarity and headroom. A dedicated **10-inch subwoofer** in a third enclosure is welcome; 12-inch and dual-sub alternatives remain worth comparing.
- Real wood appearance is preferred; pear is not mandatory. Composite, resin and carbon-like details are optional aesthetic experiments, not assumed acoustic necessities.
- **50–100k RUB** is a practical initial spending target, with incremental development perhaps **up to 200k RUB** over time. Modularity and buying subsystems independently are non-negotiable priorities.
- Listening benchmark: **ADAM Audio T5V** was heard, **ADAM Audio T8V** is the comparison target. Both are now explicitly confirmed; do not confuse them with KRK ROKIT.
- Initial hypothesis: two high-quality near-field two-way satellites + one independent active 10–12-inch subwoofer. No product or wattage freeze.

Design starting point: **[DESIGN-KICKOFF-D0.md](DESIGN-KICKOFF-D0.md)** — manufacturer-audited satellite/sub/tweeter alternatives, quantitative scenarios and a decision-gated roadmap.

Full architecture: [STEREO-2.1-ARCHITECTURE.md](STEREO-2.1-ARCHITECTURE.md).

New source-linked comparison: [CANDIDATE-COMPARISON.md](CANDIDATE-COMPARISON.md); phased spending and verification plan: [ATOMIC-ROADMAP.md](ATOMIC-ROADMAP.md). All mathematical models and test data: [simulation/](simulation/README.md).

## User intent

Build a pair of loudspeakers that a serious music enthusiast would enjoy, with excellent measurable and perceived quality, durable construction, repairability, and an attractive real-wood finish. Integrate with the ongoing digital sound-engine work and the independent local audio system when useful.

Important user constraints:
- avoid prestige-only upgrades and six-figure or million-ruble assumptions;
- take advantage of accessible well-engineered components and inexpensive Chinese amplifier / DSP manufacturing when measurements justify them;
- do not assume an anechoic chamber or extensive wall coverings are prerequisites for satisfying high-fidelity listening;
- simulate and compare alternatives before buying parts;
- pearwood is a visual/material interest from the discussed concept, not a validated cabinet construction;
- no fixed two-/three-/four-way count, tower/bookshelf size, power, cost or final driver selection has been approved.

The attached Qwen proposal offers useful concepts (directivity, damping, driver nonlinearities, DSP and controlled measurements) but its $8,400 and $16,000 systems are examples **not grounded in user budget and room requirements**.

## Candidates to compare

### A. Two-way stereo, compact / stand-mount
- one high-quality 5–7-inch midwoofer and one controlled-directivity tweeter per side;
- sealed vs vented enclosure determined by bass requirement and electroacoustic models;
- passive crossover + stereo Class D amplifier, or active DSP with four amplifier channels;
- optional later independent subwoofer.

**Likely best first experiment** because cost, alignment, physical size and number of unknowns are manageable. Not a promise it will meet a deep-bass/high-SPL specification.

### B. 2.5- or three-way stereo
- separate midrange/bass radiation to ease directivity and excursion demands;
- potentially better headroom and stronger bass but more drivers/amplifiers/crossover work and enclosure complexity;
- compare only after the listening distance, room and target SPL/bass floor are specified.

### C. Multiway experimental reference
- 4+ active channels per side, motional feedback, nonlinear system identification and active enclosure vibration suppression;
- preserve as optional research branches with independent evidence and **incremental** measured improvements.
- no obligation to include any of these in the first complete enjoyable system.

## Candidate value engineering

- Start with manufacturer-measured driver data and published angular responses. Possible reference families include SB Acoustics and Dayton Audio Reference; do not treat them as selected parts.
- A carefully implemented TI TPA3255-class amplifier is a legitimate price/performance candidate; compare measured board-level noise, gain, PSU, output LC filter, load dependence, protection and heat.
- Prefer a known open-source DSP such as CamillaDSP for proof-of-processing before writing a replacement from scratch; use reproducible IIR/FIR/crossover configurations.
- Consider fully passive 2-way as a cheaper competing baseline. An active speaker is not automatically acoustically superior without correct calibration.
- Protect meaningful expenditure on transducers, safe amplifier power and calibrated measurements before decorative extras.

## Actual acceptance metrics — to define

- On-axis and off-axis response, listening-window smoothness and directivity through crossover.
- Bass extension at a **defined** maximum SPL and listening distance, not only a 20-Hz small-signal plot.
- THD/IMD / compression / driver excursion and port noise where applicable.
- Stereo pair matching, response to placement and meaningful room correction.
- Self-noise/hiss, amp hum, thermal/protection behavior and latency.
- Cabinet panel vibration, build repeatability, safe acoustic output and long-term serviceability.
- Subjective listening against a chosen reference under level-matched conditions.

## Build and research sequence

1. Gather room/placement, dimensions, budget, SPL and bass targets.
2. Compare 2-way/3-way/2.1 architectures from actual driver T/S and polar data.
3. Run sealed/vented simulations, diffraction, crossover and driver-excursion budgets.
4. Prototype DSP pipelines virtually and calculate cost/BOM bounds.
5. Obtain one representative low-cost driver+cabinet prototype, make near-field/gated measurements and revise assumptions.
6. Commit full stereo implementation only after directivity, bass, loudness, quality and budget gates pass.
7. Experimental feedback and nonlinearity correction *later*, only where they can improve the measured system.

See [AUDIT-QWEN.md](AUDIT-QWEN.md) and [TOOLS-AND-TEST-GATES.md](TOOLS-AND-TEST-GATES.md).

## Remaining questions — not yet answered

1. Physical placement possibilities around multiple monitors: can small stands/arms position the speakers at ear height, and is a separate sub floor position available?
2. Comfortable and maximum intended listening levels; target bass SPL at the listening seat.
3. First digital input path: PC sound-engine/DAC or a separate standalone digital receiver.

The 2.1 design is a preferred starting hypothesis, not a completed specification. No irreversible mechanical or electrical decision is made before the modeled requirements and component data support it.
