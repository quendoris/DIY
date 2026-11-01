# D2 — Three-Way Acoustic Integration and Measured-Data Readiness

Date: 2026-11-01. **Active development branch**. The owner selected TWO 3-way active satellites PLUS one separate active sub (ADR-001). This is not a reconsideration of 2-way architecture. For the final design, the cabinet is LAST; early simple plywood fixtures are disposable test instruments.

## System candidates, chosen as test configurations not purchases

**Reference 3-way chain A** — one satellite:
- LOW **Wavecor WF168WA06**, 6.5-inch / 8Ω; manufacturer Fs 41 Hz, Qts 0.50, Sd 131cm², ±3mm theoretical linear excursion, sensitivity **88dB/2.83V/1m** averaged 400-3000Hz.
- Dedicated MID **Wavecor MR120BD02**, 4.75-inch / 8Ω; manufacturer 200–4000Hz recommended region, 86dB/2.83V/1m averaged 300-2000Hz, Sd 50cm², Fs 73Hz **before burn-in**, Qts 0.56 before (0.55 after), ±1.5mm theoretical linear excursion. Its own isolated **2L test chamber** is a good FIRST FIXTURE since Wavecor used a 2L enclosure in published harmonic-distortion tests; the final sealed chamber volume is NOT yet decided.
- HIGH **Wavecor TW030WA22**, 30mm / 8Ω; Wavecor's current graphene-reinforced Tetoron dome; manufacturer Fs 780Hz, sensitivity 91dB/2.83V/1m (averaged 2–20kHz), recommended band 2–25kHz; 8Ω current part **TW030WA22-01**.
- Deep SUB: **Wavecor SW312WA05 12.25-inch** or **Dayton RSS315HF-4** pending equal 25/30Hz power/excursion/thermal measurement envelope, physical availability and final true cost. This independent cabinet has its own DAC/amp and timing discipline.

**Lower-band comparison B**: Replace WF168WA06 with the owner's **HiVi M6N 8Ω** (89dB/2.83V/1m, user quoted 6,439 RUB) or **HiVi D6G 8Ω** (~85dB/2.83V/1m; T/S partly secondary sourced), keeping identical dedicated MID, HF, target electrical crossover input and comparable physical baffle dimensions. These remain **final-design contenders**, not a cheap rehearsal stage. In a three-way topology the more expensive Wavecor WF152BD14 may not justify its midband capabilities if only LF-to-400/600Hz is used; require evidence.

**Do not assign one nominal dB to whole speaker:** sensitivity averages differ between drivers, full baffle-step, power compression, delay and acoustic equalization change actual gain. Independent channel amps/digital trims can compensate *within safe voltage/excursion bounds*. 4Ω sensitivity at 2.83V must not be confused with the same electrical wattage as 8Ω.

## Material primary data now found

The **manufacturer itself** publishes numerical SPL and impedance text response downloads for ALL three reference chain drivers:

1. https://www.wavecor.com/html/wf168wa05_06.html — `WF168WA06 SPL response`, `WF168WA06 impedance response`. Factory **infinite-baffle** SPL and free-air impedance. Factory sample measured 2.83V/1m, 1/6-oct smoothing; room response not present.
2. https://www.wavecor.com/html/mr120bd01_02_03_04.html — `MR120BD02/04 SPL response`, `MR120BD02/04 impedance response`. Factory **infinite-baffle** SPL 2.83V/1m, 1/6 octave; free-air impedance. Measured harmonic distortion: **2L sealed** enclosure, 0.5m, 5.1V RMS input to MR120BD02/04, 1/12 octave smoothing. The plotted THD curves need careful numerical extraction or own testing; do not claim universal level.
3. https://www.wavecor.com/html/tw030wa21_22.html — `TW030WA22 on-axis SPL response`, `TW030WA22 impedance response`. Factory infinite-baffle, 2.83V/1m, 1/6 octave; free-air impedance. Distortion test: **0.5m, 2.83V** for TW030WA22. Note same manufacturer's old PDF has stale chart labels naming preceding TW030WA10; current HTML is authoritative for selected part and manufacture date.

**PRIMARY MEASUREMENT UPDATE (2026-11-01):** All six original Wavecor numerical files are now retrieved, parsed and SHA-256 pinned: each LF/MID/HF unit has 800 frequency/dB/phase points AND 800 frequency/impedance/phase points. The actual unresolved property is COMMON acoustic time reference between independently measured drivers, not a missing phase column. See [D2-REAL-01](D2-REAL-01-WAVECOR-PHASE.md) and [source manifest](simulation/threeway_acoustic_sources.json). The source data were recorded in an infinite baffle, not our final enclosure. We do not claim measured total-speaker crossover coherence.



## Independent real-world reference

`WaveCenter SOTA` by Bernd Timmermanns (Hobby HiFi 1/2025) is a real three-way kit using **2× MR120BD02 mids**, two WF182BD13 woofers and Audaphon AMT-1i HF, manufacturer-independent designer published crossover values **330Hz and 2800Hz**, with measurement discussion. https://lautsprecher-shop.de/hifi/wavecenter_sota_en.htm

**Not interchangeable with our one-MID-per-satellite design**: baffle width/centres, MID count, HF type, room and passive crossover all differ. Its 330/2800Hz settings are evidence a serious implementation exists, not ready-made values to copy.

## Initial crossover sweeps (hypotheses, not finished design)

- SUB → satellite LF: start **70–110Hz**, then derive from in-room acoustic transfer, placement, power and LF behavior;
- satellite LF → dedicated MID: start **350–600Hz**, then consider lower/higher values if MID excursion or LF cone distortion supports;
- dedicated MID → HF: start **2.0–3.0kHz**, then consider waveguide/vertical angles and the TW030WA22 frequency-dependent distortion.

An ideal equal-phase **Linkwitz–Riley 4th-order electrical** crossover is a useful formula reference, not a promise about the actual acoustical sum. At 2500Hz, ideal LP and HP branches have **0.5 amplitude each**; a **relative time error of 100 microseconds** rotates one by 90° and the crossing sum drops by about **3.0103dB**, even with perfectly flat ideal drivers. 100 microseconds = **9.6 samples at 96kHz**. The exact acoustic result requires phase responses, driver acoustic centres and measured gain; this is only a sensitivity illustration. [threeway_acoustic_geometry.py](simulation/threeway_acoustic_geometry.py) implements the exact ideal complex arithmetic and nearfield path-length calculation.

For a *hypothetical* 115mm MID↔HF centre separation, a listener 0.7m away shifting vertically 0.1m changes differential geometric path by roughly **48 microseconds** (assuming 343m/s sound speed). This is large enough to justify measuring the 0.6–0.8m listening window, not only a single on-axis point. The **115mm spacing is illustrative** and not an actual fit calculation; baffle geometry and driver flange dimensions require the actual drawings.

## Non-negotiable pre-production acoustic gates

**D2-01 data & identity:**
- **DONE:** download original manufacturer numerical curves, pin source URLs and SHA-256 digests, refuse unreviewed changes.
- **DONE:** per-driver manufacturer acoustic phase measured and parsed. **OPEN:** all drivers measured on same actual baffle with a common timing reference; require this before an actual acoustic crossover claim.
- Mark differences in T/S before/after burn-in, and seller data conflicts for M6N/D6G/F6N and WF168WA06.

**D2-02 disposable fixtures:**
- Choose adjustable vertical centres and replaceable baffle cutouts only after factory drawings confirmed.
- Dedicated MID chamber mechanically/air-tight isolated from woofer; preliminary 2L test volume for MR120BD02 is an evidence-backed fixture starting point, not final enclosure.
- Track woofer box **net** volume, leakage, baffle step, damping and driver inset. Do not assume unbaffled frequency response represents cabinet performance.

**D2-03 hardware-safe acoustic measurements:**
- Install safe high-pass and independent amplifier protection before increasing input levels.
- Actual acoustic FRD at identical microphone/phase origin: at centre, ±0.05 and ±0.10m seated head position, realistic 0.6/0.7/0.8m distance; off-axis polars horizontally and vertically.
- 300–600Hz and 2–3kHz band-limit distortion/IMD at matched acoustic SPL, not mixed RMS input. Reference per-driver voltage and impedance.
- Measure max safe continuous/short-term output **per channel**, shutdown, tweeter pop-free startup and frequency-dependent limiter without guessing final amplifier watts.
- Align LF/MID/HF delay using *measured group delay*, and later align SUB via room/location/acoustic time-of-flight; keep sample-timestamp vs physical timing separate.

**D2-04 honest conclusion:**
- A measured chosen driver with its own `FRD/ZMA` and re-test after mechanical change; no magical 'HiFi' statement from paper/metal/cone alone.
- Pass/fail on output, distortion, vertical response, phase, repeatability, true supply and cost. The chosen drivers are **real production candidates**, not destined for replacement because they cost less.

## Parallel STM32 research branch without blocking the acoustic work

The owner explicitly says an upcoming marketplace `NUCLEO-H7S3L8 / STM32H7R3L9` may differ from ST reference. **This is acceptable as a RESEARCH BOARD**, provided safe power and wiring are established; deviations become informative test cases, not a claim of authenticity or standard behavior. No acoustic test is blocked on its arrival. For a future bespoke **PRODUCTION PCB**, exact component/revision selection, traceable firmware, per-device programming, current-limited pre-power validation, full unit acceptance/retest and independent safety are required. See **[ADR-003](ADR-003-RESEARCH-HARDWARE-QUALIFICATION.md)**.

## Current outputs

- [Three-way architecture](ADR-001-ACTIVE-THREE-WAY-SUB.md)
- [Combined component data](THREE-WAY-PLUS-SUB-RESEARCH.md)
- [Ideal complex crossover + nearfield geometry model](simulation/threeway_acoustic_geometry.py)
- [Reviewed original manufacturer URLs, source hashes and phase data](simulation/threeway_acoustic_sources.json)
- [First real source crossovers and phase bridge results](D2-REAL-01-WAVECOR-PHASE.md)
- [Real phase and impedance importer](simulation/wavecor_threeway_realdata.py)
- [Conditional delay and head-position study](simulation/wavecor_phase_sensitivity.py)

**No actual speaker crossover/physical SPL/THD is yet measured.** The numerical model is useful to identify constraints and design tests, not to certify sound quality.
