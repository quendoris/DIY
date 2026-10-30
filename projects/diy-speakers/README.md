# Premium DIY Loudspeakers — Research Concept

Status: **exploratory / requirements not frozen; no purchasing or manufacturing commitment**.

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

## Preliminary questions — not answered yet

1. Placement: desktop / stands / floor; listening distance and rough room size?
2. Physical envelope: max height/width and preference for bookshelf vs floorstanding?
3. Realistic total **pair** budget, including amplification and essential measurement equipment?
4. Deep bass and volume target: acceptable ~45–50 Hz at reasonable level, or ~25–35 Hz and high SPL without a separate subwoofer?
5. Material: pearwood mandatory for visible surfaces, or one of several candidates?
6. External PC/audio engine vs fully autonomous active loudspeakers, and what inputs are required?

No irreversible architectural decision is made until these are known.
