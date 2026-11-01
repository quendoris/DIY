# D0 — Start Designing the Desktop 2.1 System

2026-11-01. Status: first design gate, **no final parts or PCB selected**.

## Engineering decision

**Start with an acoustic specification and an evidence-based comparison of drivers and enclosures.** This establishes the electrical power, DAC, DSP and thermal requirements instead of building those subsystems to an imaginary load. The **first physical DIY project remains a protected low-voltage power module**, developed with a certified external AC/DC supply. The separate optical four-plane fabric continues in software.

## Confirmed owner requirements

- Two satellites on/near a multi-monitor desktop; **60–80 cm** from listener; room around **19 m²**, subject to later changes.
- Excellent intelligible, natural midrange; clean highs; very deep physically impactful bass using a separate 10–12-inch subwoofer if worthwhile.
- Real-wood visual identity; high repairability and independently replaceable modules.
- 50–100k RUB first-stage target; progressive improvements could reach ~200k RUB.
- Heard reference **ADAM Audio T5V**, aspirational comparison **T8V**.
- Long-term distributed audio controller + fiber links + local DAC, with four logical trust/health, control, audio and clock planes; not a prerequisite for early mechanical prototypes.

## Starting scenarios — not imposed on the owner

Numerical simulations will compare at 0.7 m listening distance: representative normal levels 75 and 85 dB SPL with short 95 dB peaks, and subwoofer response/limits at 25, 30, 40, 60, 80 Hz. These are **design sweeps**, not promised measured performance or recommended continuous loudness levels. Examine crossover to sub around 70–110 Hz, then decide using measured **acoustic** transfer, phase and delay. A stand-alone 2.0 design should remain listenable before the sub arrives.

## Satellite shortlist

| Candidate | Manufacturer T/S | Sd / sensitivity | Hypothesis |
|---|---|---|---|
| SB Acoustics SB15MFC30-8 (5-inch) | Fs=39 Hz, Qts=.37, Vas=17.7 L | 82 cm²; 87 dB/2.83 V/1 m | compact enclosure, modest vertical centre spacing |
| SB Acoustics SB17NRX2C35-8 (6-inch) | Fs=36.5 Hz, Qts=.42, Vas=27 L | 118 cm²; 87 dB/2.83 V/1 m | more radiating area and potential LF-mid headroom |
| HiVi M6N-B (6-inch) | Fs=46 Hz, Qts=.39, Vas=21.9 L | 133 cm²; 89 dB/2.83 V/1 m; Xmax 4.3 mm | affordable Chinese contender, with real measured response needed |

Primary/supporting sources:
- https://sbacoustics.com/product/5in-sb15mfc30-8/
- https://sbacoustics.com/product/6in-sb17nrx2c35-8-norex/
- https://www.parts-express.com/HiVi-M6N-B-6-Damped-Aluminum-Magnesium-Cone-Woofer-297-488

**Not yet evaluated:** true midrange nonlinear distortion, baffle directivity, measured polar frequency response, high-frequency breakup, driver centre offsets, availability/landed local price. T/S numbers alone **cannot** rank subjective midrange fidelity.

## Initial tweeter comparison

| Driver | Manufacturer Fs / sensitivity | Purpose |
|---|---|---|
| SB26STWGC-4 fabric with integrated aluminum waveguide | 780 Hz; 93 dB/2.83V/1m | waveguide-controlled polar response |
| SB26ADC-C000-4 aluminum dome | 680 Hz; 90 dB/2.83V/1m | alternative radiation, front baffle and filter profile |

Sources:
- https://sbacoustics.com/product/sb26stwgc-4-fabric/
- https://sbacoustics.com/product/sb26adc-c000-4/

A lower tweeter Fs does not permit an arbitrary low crossover without knowing frequency-dependent response, distortion and thermal excursion. Do not buy a beryllium driver by reputation.

## Subwoofer shortlist

| Candidate | Fs/Qts/Vas | Sd/Xmax/Vd | Why model |
|---|---|---|---|
| Dayton RSS265HO-4, 10-inch | 26.9 Hz/.35/29.4 L | 349.7 cm²/12.3 mm/430.1 cm³ | higher-output compact candidate |
| Dayton RSS315HF-4, 12-inch | 24.2 Hz/.39/84.1 L | 514.7 cm²/14.3 mm/736.0 cm³ | ~1.71x nominal volume displacement vs 10-inch HO, not a measured SPL ratio |
| Dayton DCS255-4, 10-inch | 37.7 Hz/.46/32.1 L | 346.4 cm²/8.3 mm/287.5 cm³ | low-cost comparison, may fail deep-bass SPL goal |

Sources:
- https://www.daytonaudio.com/product/120/rss265ho-4-10-reference-ho-subwoofer-4-ohm
- https://www.daytonaudio.com/product/121/rss315hf-4-12-reference-hf-subwoofer-4-ohm
- https://daytonaudio.com/product/38/dcs255-4-10-classic-subwoofer-4-ohm

**Data conflict:** the Dayton RSS315HF-4 product page lists BL=1 Tm, whereas the manufacturer's PDF spec reports 13.99 Tm. Treat motor BL as **CONFLICT / DO NOT USE** until source revision is resolved. Source PDF: https://www.daytonaudio.com/images/resources/295-464-dayton-audio-rss315hf-4-specifications-46174.pdf.

## Required comparisons and decision gates

**D0: audit all source data and unknowns.** Confirm physical dimensions, response/impedance curves, source measurement conditions, T/S, availability, taxes/shipping and revision. Add unknowns instead of guessing.

**D1: LF model.** For each 5/6-inch satellite and each 10/12-inch sub compare sealed, vented and optionally passive-radiator alignment, box dimensions/net volume, F3/F6, phase/group delay, electrical power, excursion and port air velocity at specified SPL. Include T/S tolerances. This is the **next executable work package**.

**D2: nearfield crossover/directivity.** Compare two tweeters and 5/6-inch midwoofer in real front baffles; import measured FRD/ZMA and angles, study 0.6–0.8m listening and desktop reflection. A mathematically flat ideal electrical LR4 sum is not an actual speaker frequency response.

**D3: electronics requirements.** Derive amplifier rail/current/headroom, DAC/noise limits, cooling and independent hardware protection from D1/D2. Pass qualified requirements to [shared-power](../shared-power/README.md).

**D4: first physical steps.** DC-only protected PSU/supervisor experiment using a certified mains-isolated adapter, and one inexpensive satellite test enclosure with replaceable baffle after modeling.

**D5: complete system.** Matching satellites, separate active sub, crossover and timing calibration, per-speaker DAC, optical four-plane audio/control/clock/trust evaluation.

### Required outputs before purchase

For every tested candidate: source and units; exact model revision; envelope of model predictions with assumptions; missing/contradictory manufacturer facts; comparable current delivered Russian prices; a `MEASURED` / `SIMULATED` / `NOT_TESTED` evidence flag; tests and reason codes for rejected choices. It is acceptable to have **no chosen driver** until the predicted acoustic performance and price both check out.

## Construction order clarification — 2026-11-01

The final cabinet is explicitly **last**: the owner wants exceptional industrial/futuristic styling with detailed acoustic/mechanical and aesthetic modeling, possibly real wood/resin/composite, not a finalized plywood box.

A **temporary, practical plywood measurement enclosure** and interchangeable baffle are approved intermediate research tooling. An **open-frame test** is suitable only for low-power mechanical/impedance/T/S experiments; unrestricted free-air LF playback can produce excess excursion, and rear cancellation invalidates cabinet-response conclusions.

Three direct AliExpress candidates, with exact listing/SKU references, are now recorded in [ALIEXPRESS-CANDIDATES.md](ALIEXPRESS-CANDIDATES.md). Vendor and model identities remain **unverified**, despite the owner's observation that each selected unit costs less than 10,000 RUB. Purchase consideration is conditional on a clear model identity or explicit acceptance of measurement-only uncertainty.

## Immediate prototype configurations

1. SB15MFC30-8 + SB26STWGC-4, matched against SB15MFC30-8 + SB26ADC-C000-4.
2. SB17NRX2C35-8 + SB26STWGC-4 to examine 6-inch midband/crossover tradeoffs.
3. HiVi M6N-B + one evaluated tweeter as the value challenger.
4. In parallel: RSS265HO-4 vs RSS315HF-4 vs cheaper DCS255-4 under identical sub requirements.

Do **not** choose drivers solely by Fs, Vas, Xmax, paper/metal cones or brand.


## Final-intent competition extension

The owner clarified that budget Chinese units are **possible final-design drivers**, not merely temporary prototypes. The expanded [cross-manufacturer competition](FINAL-INTENT-MIDWOOFER-COMPETITION.md) now includes Wavecor 6/6.5inch 8Ω drivers with **Russian same-market observations** (WF168WA06 8,600 RUB, WF168WA02 9,200 RUB, WF152BD14 14,000 RUB), 4Ω SB17NBAC independent-measurement baseline, Scan-Speak and upper-bound PURIFI. The goal is a real equal-acoustic-SPL, matching-filter, same-baffle and off-axis comparison, plus replacement availability and total system cost; no driver can graduate from 'prototype' to 'prestige' based solely on country of origin.
