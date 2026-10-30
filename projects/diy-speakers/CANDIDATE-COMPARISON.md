# First Component Comparison — Nearfield 2.1

Date: 2026-10-30. Status: **research shortlist, no selected or ordered components**.

## Fixed owner requirements

- Two nearfield satellites used at 60–80 cm on a monitor-crowded desk in a variable room of about 19 m².
- Excellent middle frequencies, clean highs, low amplifier hiss and well-controlled stereo imaging.
- Separate subwoofer permitted and preferred as a way to deliver deep, physically impactful bass without forcing a large main woofer onto the desk.
- Real-wood or attractive composite finish; aesthetic and durability count, but not a predetermined wood species.
- 50–100k RUB initial staged ambition, potentially approaching 200k RUB over iterative improvement.
- Heard reference: **ADAM T5V**. Comparative benchmark: **ADAM T8V**.
- No costly parts until a source-linked feasibility model can justify them.

## Scope and methodology

Vendor Fs, Qts and Vas are suitable for an initial **small-signal low-frequency sealed-box** ranking. They cannot rank midrange transparency, tweeter quality, directivity, crossover, distortion at listening SPL, or true room response.

The executable [compare_candidates.py](simulation/compare_candidates.py) reads [candidates.json](simulation/candidates.json). It calls the shared simple sealed-box model and reports Fc/Qtc/F3 for **hypothetical volumes** and (where Xmax is specified comparably) Sd × Xmax. These values are not enclosure designs, and no dynamic bass capacity is inferred from a small-signal F3 alone.

### Midwoofers — manufacturer data

| Model | Nominal diameter | Fs, Hz | Qts | Vas, L | First-trial sealed net volume, L | Why compare |
|---|---:|---:|---:|---:|---:|---|
| [SB Acoustics SB15MFC30-8](https://sbacoustics.com/product/5in-sb15mfc30-8/) | 5 in | 39 | .37 | 17.7 | 8 | 5-inch compact desk candidate; polypropylene |
| [SB Acoustics SB17MFC35-8](https://sbacoustics.com/product/6in-sb17mfc35-8/) | 6 in | 33 | .37 | 39 | 12 | 6-inch soft cone, more diaphragm area |
| [SB Acoustics SB17NRX2C35-8](https://sbacoustics.com/product/6in-sb17nrx2c35-8-norex/) | 6 in | 36.5 | .42 | 27 | 12 | Natural-fiber 6-inch candidate; interesting closed-box fit |
| [HiVi M6N-B](https://www.parts-express.com/pedocs/specs/297-488--hivi-m6n-b-spec-sheet.pdf) | 6 in | 46 | .39 | 21.9 | 12 | Chinese manufactured option; compare fairly on actual measurements |
| [Dayton RS180-8](https://daytonaudio.com/product/101/rs180-8-7-reference-woofer-8-ohm) | 7 in | 35.7 | .31 | 24.4 | 12 | Larger metal cone; physical fit and high-frequency break-up need evaluation |

**Lifecycle warning:** SB15NRXC30-8 and SB17NRXC35-8 are flagged by SB Acoustics as discontinued-from-standard-range/OEM only. Do not base the long-term design on these without a verified supply/replacement strategy.

First **mechanical/acoustic trade-off**, not a winner announcement:
- 5-inch: more desk-friendly and potentially easier 2-way midwoofer-to-tweeter integration; less piston area than a 6-inch cone.
- 6-inch: more area/headroom but more baffle/desk occupation; crossover directivity must be treated as central design constraint.
- 7-inch: possible acoustic power advantage, but room on the desk and 60–80-cm tweeter/midwoofer geometry become more critical.

The chosen sub crossover must be **acoustic**, not merely an ideal electrical LR4 switch, and may be explored initially at 70, 80, 90, 100 and 110 Hz. The real roll-off/phase of each speaker will modify the crossover. Crossover-to-tweeter frequency likewise requires actual FRD/ZMA and polar data, not Fs alone.

### Tweeters — manufacturer data

| Model | Type | Fs | 2.83V / 1m sensitivity | Research issue |
|---|---|---:|---:|---|
| [SB26STCN-C000-4](https://sbacoustics.com/product/sb26stcn-c000-4/) | compact neodymium fabric dome | 960 Hz | 92.5 dB | Space saving, waveguide/baffle integration still TBD |
| [SB26ADC-C000-4](https://sbacoustics.com/product/sb26adc-c000-4/) | aluminum dome | 680 Hz | 90 dB | Well-documented, used in manufacturer published kits |
| [SB26STWGC-4](https://sbacoustics.com/product/sb26stwgc-4-fabric/) | fabric dome with waveguide | 780 Hz | 93 dB | Controlled directivity candidate; waveguide geometry affects baffle |

Do not rank tweeters based on the Fs or sensitivity column alone. Per-driver response and harmonic distortion at intended SPL and crossover frequency are required. We should also benchmark an affordable non-SB tweeter option when manufacturer off-axis and distortion data are available.

### Subwoofer drivers — manufacturer data

| Model | Diameter | Fs, Hz | Qts | Vas, L | Xmax, mm | Vd if comparable, cm³ | Research issue |
|---|---:|---:|---:|---:|---:|---:|---|
| [Dayton DCS255-4](https://daytonaudio.com/product/38/dcs255-4-10-classic-subwoofer-4-ohm) | 10 in | 37.7 | .46 | 32.1 | 8.3 | 287.5 | Affordable baseline; deep 25–30 Hz output must be evaluated at target SPL |
| [Dayton RSS265HO-4](https://daytonaudio.com/product/120/rss265ho-4-10-reference-ho-subwoofer-4-ohm) | 10 in | 26.9 | .35 | 29.4 | 12.3 | 430.1 | High-output 10-inch reference for compact/equalized cabinets |
| [SB29SWNRX-S75-6](https://sbacoustics.com/product/10in-sb29swnrx-s75-6-norex/) | 10 in | 20 | .29 | 66 | not specified comparably | — | Low Fs, more complex box/EQ decision |
| [Dayton RSS315HF-4](https://daytonaudio.com/product/121/rss315hf-4-12-reference-hf-subwoofer-4-ohm) | 12 in | 24.2 | .39 | 84.1 | 14.3 | 736.0 | Strong displacement benchmark; bigger cabinet |
| [SB34SWNRX-S75-6](https://sbacoustics.com/product/12in-sb34swnrx-s75-6-norex/) | 12 in | 19 | .32 | 164 | not specified comparably | — | Low Fs but large Vas / box volume uncertainty |

Vd is a useful **potential displacement** metric, not a complete SPL/THD predictor. Across vendors, Xmax definition must be verified before a strict like-for-like ranking. Do not calculate Vd from SB's *linear coil travel peak-to-peak* as if it were a published one-way Xmax.

**Important insight:** A high-output 10-inch with proper enclosure/DSP may be a better practical fit than an inferior 12-inch; a well-engineered 12-inch can still offer substantially more low-bass volume displacement. Choose after comparative **sealed / vented / passive-radiator** enclosure designs plus excursion/current/thermal/SPL calculations at 25, 30, 40 and 60 Hz.

## Cost sanity checks (not comparable supplier quotes)

A few **observed listings**, not a current turnkey Russian price list:
- [SB15MFC30-8](https://wallegro.ru/item/12691592144/Dinamik-SB-Acoustics-SBMFC-.html) listed around **8,412 RUB** by an import reseller; product title incorrectly mentions 6 inches, while official specification is 5 inches. Confirm correct model and final fees.
- [Dayton DCS255-4](https://shopozz.ru/brand/dayton-audio/page/3) showed around **18,990 RUB** on an importer listing. That does not establish value for a 25-Hz high-SPL goal.
- [SB26ADC-C000-4](https://www.audiohobby.eu/ru/dinamiki/10725-sb-acoustics-1-metal-dome-chmbr-tweeter-sb26adc-c000-4.html) EU retailer listed **€36 before VAT**, **not** a delivered Russia price.
- [SB29SWNRX-S75-6](https://www.audiohobby.eu/ru/dinamiki/12848-sb-acoustics-10-subwoofer-75mm-vc-nrx-sb29swnrx-s75-6.html) EU listing **€135 before VAT**, not directly comparable to other markets.

All availability, import compliance, final delivery/taxes and return terms must be rechecked at purchase time. Do not make a full-system BOM by adding MSRP from different markets. Build a quote ledger for **two woofer + two tweeter + amp/DSP + power + woodworking + cabling + instrument / returns**, and then a separate optional **sub + amp + cabinet** ledger.

## Model expectations

Our current *hypothetical* net sealed boxes produce, in a small-signal idealized model:
- SB15MFC30-8 at 8 L: ~75 Hz F3;
- SB17NRX2C35-8 at 12 L: ~62 Hz F3;
- DCS255-4 at 35 L: ~59 Hz F3;
- RSS265HO-4 at 35 L: ~61 Hz F3;
- RSS315HF-4 at 60 L: ~45 Hz F3.

These figures **do not** mean the RSS265HO can be swapped into a DCS enclosure at unchanged power/EQ and sound identical; different Qtc and LF gain/phase substantially alter the integration. They also say nothing about target *25 Hz SPL* and possible excursion/limiter losses. For serious bass, modeling vented alignments, Linkwitz/low-shelf EQ and real driver displacement constraints is mandatory.

## Provisional candidate bundles for testing — NOT shopping selections

1. **Compact:** SB15MFC30-8 + SB26STCN-C000-4 × 2, active 2-way or passive crossovers; sub separate.
2. **Mid-focused:** SB17NRX2C35-8 + SB26ADC-C000-4 × 2; slightly larger satellites, crossover/directivity measurement gate.
3. **Price/China challenger:** HiVi M6N-B + vetted tweeter, with identical sound, polar, enclosure and total-cost test to SB designs.
4. **Sub options:** DCS255 as a *price* floor, RSS265HO as high-output 10-inch, SB29SWNRX as low-Fs comparison, RSS315HF as 12-inch displacement reference.

Any candidate may fail when measured. Final choice requires current unit pricing, physical fit and quality evidence.

## Decision gate

Do not purchase all five types. First narrow to **two satellite midwoofers, two tweeter options and two subs** for full measured/simulated evaluation; buy **one prototype speaker's** drivers only after the data has been assembled. Do not equate a long T/S table with 'midrange sound quality'.
