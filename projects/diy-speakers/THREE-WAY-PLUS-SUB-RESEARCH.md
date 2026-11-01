# Stereo Three-Way Satellites + Independent Subwoofer — Full Driver-System Research

> **DATA ACQUISITION UPDATE:** Six original Wavecor SPL/phase and complex impedance files for WF168WA06+MR120BD02+TW030WA22 were downloaded and verified by hash (800 rows per curve). The phase column is real, but cross-driver acoustic origin is not validated. A hypothetical 3-way LR4 cascade also required a phase allpass bridge in the LF path to sum ideal flat sources without error. Full evidence: [D2-REAL-01](D2-REAL-01-WAVECOR-PHASE.md). No final crossover or speaker component is approved from this result alone.

> **CURRENT DESIGN WORK:** [D2-THREE-WAY-ACOUSTIC-INTEGRATION.md](D2-THREE-WAY-ACOUSTIC-INTEGRATION.md) is now active: Wavecor WF168WA06 + MR120BD02 + TW030WA22 with HiVi M6N/D6G lower-band alternatives and separate deep SUB. Manufacturer text-response downloads exist, but acoustic **phase and actual cabinet data are missing**; ideal LR4+head-motion tests explicitly remain `MODEL_ONLY`. STM research-board policy is frozen in [ADR-003](ADR-003-RESEARCH-HARDWARE-QUALIFICATION.md).

> **ARCHITECTURE DECISION — 2026-11-01:** The owner chose **full active 3-way satellites plus an independent powered sub**. The 2-way controls and previous comments about 'earning' the 3-way topology are **historical research questions only**. We shall use 2-way or commercial references for **external performance comparison**, not to reconsider our own topology. See [ADR-001](ADR-001-ACTIVE-THREE-WAY-SUB.md). Final system budget and schedule are flexible and the final cabinet comes last.

Date: 2026-11-01. Status: **components sourced, electrical/physics hypotheses; NO proven optimal crossover, no purchase, no measured response**.

## Owner requirements and architecture

- **Two independently powered nearfield desktop satellites** at 0.6–0.8 m, on a multiple-monitor desk in a roughly 19 m² room. Critical: uncolored, low-distortion midrange and highs; separately physically impressive deep bass.
- **Final futuristic real-wood/composite enclosure built LAST**. Temporary test baffles and sealed plywood boxes are separate measurement apparatus.
- Explicitly investigate a *true* three-way satellite: LF midwoofer 6–7in + dedicated 3–4.75in midrange + tweeter. Each satellite therefore has two acoustic crossover regions. If a separate powered subwoofer is used, the total system is an acoustically **four-band** chain (sub, satellite LF, satellite mid, satellite HF), though conventional channel topology is still stereo 2.1.
- Candidate **7 independent DAC/amp output channels** if fully active: `L LF/MID/HF`, `R LF/MID/HF`, `SUB`. This does not mean seven digital program channels; normally inputs are stereo and crossover synthesis produces multiple output channels.
- Compare the original *two-way satellites plus sub* architecture directly, with **5** such output channels. At 0.7 m, extra large drivers/crossovers can worsen vertical response and timing without an offsetting midrange-distortion benefit.

## Two crucial truths

1. Each satellite **dedicated midrange** must have its own sealed, isolated rear chamber. It must not share the large woofer air volume: woofer pressure would modulate the mid cone and raise IMD. A tweeter may have a manufacturer-built rear chamber. Physical baffle distances and positions are integral to crossover simulation.
2. A 10–12in **dedicated subwoofer** is a separate LF duty, not a substitute for the midrange driver. Its positioning, DAC delay and acoustic time-of-flight need calibrated synchronization. The upper satellite LF woofer will be high-passed when a sub is connected.

## New dedicated MID drivers for 3-way trials

| Driver | Role / exact impedance | Band or manufacturer specs | Available Russian price/stock observation | Evaluation |
|---|---|---|---|---|
| **Wavecor MR120BD02** | 4.75in dedicated MID, **8Ω** | 200–4000 Hz recommended band; 86dB/2.83V/m; Fs~73Hz; Kevlar/carbon cone; Balanced Drive; copper cap, stabilization ring | **12,000 RUB each**, catalog says in stock | *Best matched serious Chinese MID for first tri-way study*. Separate air chamber, important baffle width and centre spacing |
| **Wavecor MR120BD01** | same MID family **4Ω** | same 200–4000 Hz band; **89dB/2.83V/m** (not 3dB more at equal electrical 1W) | **12,000 RUB each**, catalog in stock | Higher quoted voltage sensitivity; assess amplifiers/power; do not conflate 4Ω/8Ω |
| **Wavecor WF120BD04** | 4.75in **midwoofer** 8Ω | balanced motor and copper cap; 86dB/2.83V/m; vendor recommended max upper 4kHz | **12,100 RUB each**, catalog in stock | Alternative, not exclusively optimized for MID; only meaningful if distortion and crossover outperform dedicated MR |
| **Wavecor WF118WA02** | 4.5in midwoofer 8Ω | ferrite/paper cone, less expensive option; actual polar/THD still required | **7,700 RUB each**, catalog in stock | Price challenger, NOT presumed inferior or final by default |
| **SB Acoustics SB12MNRX2-25-4** | dedicated 4in MID, **4Ω** | shortened coil optimized for MID, copper ring, Fs63.5Hz, 90.5dB/2.83V/m, Sd50cm² | direct local price **not verified** | International reference; not the older `SB12MNRX25-4` already flagged OEM-only |
| **Scan-Speak 10F/8424G00** | 10cm 8Ω wideband used as MID | 86.5dB/2.83V/m, Fs90Hz, copper cap, compact neo motor | direct local price **not verified** | Compact reference; not manufactured as a special MID; high-pass distortion headroom to be proven |

Primary docs:
- Wavecor MR120 https://www.wavecor.com/html/mr120bd01_02_03_04.html
- Wavecor WF120BD04 https://www.wavecor.com/html/wf120bd03_04_07_08.html
- Wavecor WF118 https://www.wavecor.com/html/mid-woofers.html
- SB12MNRX2 https://sbacoustics.com/product/4-sb12mnrx2-25-4-norex/
- Scan-Speak 10F https://www.scan-speak.dk/product/10f-8424g00/
- Russian seller https://www.samodelka.ru/cats/10.htm?vendor=291

**Note:** Wavecor manufacturer MR120 spec band 200–4000Hz does **not** prove acceptable distortion at 200Hz with our target SPL, nor that a 4kHz crossover is optimal. Start study around **350–600Hz LF/MID** and **2.0–3.0kHz MID/HF**, then derive actual acoustic slopes from response, excursion, baffle and tweeter distortion tests.

## Tweeters: compare at real mid-to-HF acoustic crossover

| Driver | Spec facts | Russian observed RUB per piece | Why |
|---|---|---:|---|
| **Wavecor TW030WA22**, 8Ω | 30mm graphene-reinforced Tetoron textile, ~91dB/2.83V/1m, manufacturer recommended ≥2kHz, Fs~780Hz | **8,200**, listed stock | accessible, compatible nominal load with 8Ω mid + woofer; final-capable |
| **Wavecor TW030WA23**, 4Ω | 30mm graphene-reinforced Tetoron, ~94dB/2.83V/1m | **12,200**, listed stock | newer higher-tech motor/dome alternative, carefully normalize 4Ω |
| **Wavecor TW030WA24**, 8Ω | same improved diaphragm, ~91.5dB/2.83V/1m | **12,200**, currently order/expected supply, verify checkout | compatible 8Ω alternate, motor/thermal limits and directivity test |
| **Wavecor TW030WA11**, 4Ω | 30mm waveguide, Fs~410Hz, ~94dB/2.83V/1m, stated 1.5–25kHz range | **9,900**, mixed stock listings | lower possible crossover/favorable pattern; large 115mm waveguide may be awkward beside 4.75in MID at 0.7m |
| **SB Acoustics SB26STWGC-4**, 4Ω | fabric dome waveguide, Fs780Hz, 93dB/2.83V/1m | unknown Russian delivered | international reference with controlled pattern; manufacturer 120W 'rated' assumes 2600Hz 12dB HP; NOT raw wattage |

Manufacturer:
- TW030WA23/24 https://wavecor.com/html/tw030wa23_24_25_26.html (replacements for TW030WA13/14, which are being phased out).
- TW030WA11 https://wavecor.com/html/tw030wa11_12.html
- TW030WA21/22 manufacturer https://www.wavecor.com/html/tw030wa21_22.html ; updated graphene-reinforced Tetoron versions replacing TW030WA09/10, with published frequency response, impedance and THD measurements. An older retailer PDF has a resonance-frequency unit typo; manufacturer's live HTML clearly reports Fs 780 **Hz**.
- SB26STWGC https://sbacoustics.com/product/sb26stwgc-4-fabric/
- Russian price/availability snapshots https://www.samodelka.ru/cats/2.htm?vendor=291

Final tweeter selection is determined by the **measured 2–3kHz transfer function, distortion and 0/15/30/45/60deg polars on our actual baffle**, not by the manufacturer's Fs, Watts or exotic diaphragm words.

## Satellite LF/midwoofer

- **HiVi M6N 8Ω, 6.5in, owner 6,439 RUB each** — affordable serious candidate, ~89dB nominal 2.83V, 4.3mm reported Xmax; not necessarily inferior to other parts.
- **HiVi D6G 8Ω, 6.5in, owner 7,762 RUB each** — powerful 76mm voice coil, but ~85dB 2.83V sensitivity; no proof of lower midrange IMD at equal acoustic SPL.
- **Wavecor WF168WA06 8Ω, 6.5in, Russian 8,600 RUB each** — available Chinese alternative; manufacturer/seller conflict on Fs and sensitivity remains to be resolved.
- **Wavecor WF152BD14 8Ω, 6in, Russian 14,000 RUB each** — compact premium Chinese Balanced Drive option; may be redundant if only carrying 80–450Hz and a dedicated MR120 handles the rest. This is precisely why evaluating the full system saves money.

## Deep bass — separate SUB

Here `Vd=Sd*Xmax` when Sd in cm² and one-way Xmax in mm, converted to cm³ using `/10`. Xmax criteria may differ between vendors, so Vd is a **geometry-derived screening number, NOT delivered SPL or THD at 25Hz**.

| Exact driver | Diameter | Fs | Sd x Xmax | Vd (cm³) | Russian observed RUB unit | Evaluation |
|---|---|---:|---:|---:|---:|---|
| **Wavecor SW280WA01** | 11in shallow | 26Hz | 335cm² × 6mm | **201** | **16,450**, listed stock, discounted | Interesting shallow low-distortion design, but lower displacement; 25Hz high-output duty likely limiting, must simulate |
| **Wavecor SW259WA01** | 10.25in 4Ω | 29Hz | 312 × 11.5 | **358.8** | **32,000**, listed stock | Serious 10in Chinese speaker; updated direct replacement for discontinued SW263WA03 |
| **Wavecor SW270WA01** | 10.5in 4Ω | 28Hz | 312 × 11 | **343.2** | **19,800**, retailer says awaiting stock | Attractive price and Balanced Drive if truly available |
| **Wavecor SW312WA05** | 12.25in 4Ω | 28Hz | 488 × 11.5 | **561.2** | **34,700**, listed stock | Strong 12-inch black-cone contender, interesting for clean deep bass |
| **Dayton RSS265HO-4** | 10in 4Ω | 26.9Hz | 349.7 × 12.3 | **430.1** | unknown landed RUB | higher output 10in comparison control |
| **Dayton RSS315HF-4** | 12in 4Ω | 24.2Hz | 514.7 × 14.3 | **736** | unknown landed RUB | high-displacement 12in benchmark |

Manufacturer sources:
- SW280 https://www.wavecor.com/html/sw280wa01.html
- SW259 https://www.wavecor.com/html/sw259wa01_02.html
- SW270 https://wavecor.com/html/sw270wa01.html
- SW312 https://wavecor.com/html/sw312wa03_04_05_06.html
- Dayton 10 https://daytonaudio.com/product/120/rss265ho-4-10-reference-ho-subwoofer-4-ohm
- Dayton 12 https://daytonaudio.com/product/121/rss315hf-4-12-reference-hf-subwoofer-4-ohm
- Russian prices and reported inventory https://www.samodelka.ru/cats/11.htm

**Critical lifecycle warning:** Wavecor **SW310WA02 is discontinued**, replaced by SW312WA03/04. Wavecor SW263WA01/03 were discontinued and replaced by SW259WA01/02. Do not base future-serviceable enclosure CAD on old drivers solely because a marketplace has discounted old stock.

## Practical combined sets — WITHOUT buying commitment

Each set assumes **two satellites with one driver per LF/MID/HF** and one independent sub.

| Prototype concept | Per-satellite LF + MID + HF | Sub | Driver-only RUB total | Full active output channels |
|---|---|---|---:|---:|
| **H** (owner value) | HiVi M6N (6,439) + Wavecor MR120BD02 (12,000) + Wavecor TW030WA22 (8,200) | SW312WA05 (34,700) | **87,978** | 7 |
| **W** (all Chinese Wavecor) | Wavecor WF168WA06 (8,600) + Wavecor MR120BD02 (12,000) + Wavecor TW030WA22 (8,200) | SW312WA05 (34,700) | **92,300** | 7 |
| **2-way baseline** | HiVi M6N (6,439) + Wavecor TW030WA22 (8,200) | SW312WA05 (34,700) | **63,978** | 5 |

Calculation: `2*(LF+MID+HF) + one sub`. **Drivers only**: no PCB, 7 amp channels, multichannel DAC, PSU, fiber/controller, heat-sink/fan, cabinet, shipping or tools. So a full 3-way+sub is very likely to exceed the user's initial **50–100k RUB** spending stage; incremental up to ~200k RUB may be realistic but requires full budget/invoice. The third way adds **24,000 RUB for two dedicated mids alone**, plus extra amplifier/DAC channels, filtering and time-align calibration.

A low-cost 3-way route uses WF118WA02 (7,700) instead of MR120BD02 (12,000), but no claimed quality equality follows from lower price.

## Acoustic crossover starting envelopes, NOT finished settings

- **SUB ↔ satellite LF:** initial 70–100Hz study.
- **Satellite LF ↔ dedicated MID:** 350–600Hz initial test envelope; final only from measured mid excursion/distortion and directivity.
- **MID ↔ HF tweeter:** 2.0–3.0kHz study; final depends on waveguide, mid breakup, off-axis polars and true acoustic filter overlap.

**Nearfield and spacing**: at 0.6–0.8m with three vertically separated drivers, acoustic centre distances, vertical tilt/rotation, time alignment and desk reflection matter greatly. An electrical flat frequency-response plot on one axis does not prove a coherent measured sound field. Compare total listening-window response and seated head-movement range.

**Low-frequency sub design obligation**: model 25/30/40Hz output at specified SPL, enclosure alignment sealed/reflex/PR, required voltage and amplifier headroom, peak excursion, port velocity, THD, limiter and mechanical/thermal stress. The relationship `Vd` does not replace this.

## First next design action

Perform an actual combined acoustic crossover simulation using **manufacturer FRD/ZMA curves with original measurement provenance** for Wavecor MR120BD02, TW030WA22 and candidate HiVi/Wavecor lower woofer, rather than only T/S/F3. Wavecor offers downloadable numeric frequency/impedance data for many current models. For HiVi, source their exact measurements or measure own specimens; do not invent angular responses from only 2.83V sensitivity.

**Decision gate:** full three-way only earns its additional cost and DSP complexity if it demonstrably reduces midrange distortion or compression / improves polar response and headroom compared with a carefully optimized two-way+sub at the same target listening SPL. Do not assume either architecture is superior merely from parts count.


## D2-GEO-01 — acoustic-first arrangement, no fixed enclosure aesthetics

As directed by the owner, [geometry now follows actual driver drawings](D2-GEO-01-WAVECOR-BAFFLE.md), and the eventual futuristic enclosure will be shaped around whichever head-window measurement passes. OpenSCAD preview and reproducible model compare narrow vertical vs mirrored side-mounted LF, both potentially production-worthy layouts; model-only acoustic results do not certify either. Full 3-way plus SUB topology stays fixed.
