# Final-Intent Midwoofer Competition — Global 5–7-inch Benchmark

Date: 2026-11-01. Status: **cross-manufacturer research; all candidates are potentially FINAL components, not expendable stepping stones.**

## Decision change

The owner explicitly rejects the premise "try a cheap Chinese driver, then upgrade to serious Western drivers." We must instead find the **best measured transducer for the user’s intended real 2.1 loudspeaker**, regardless of its provenance. This is a *serious end-system candidate contest*, not an "entry level vs premium" ladder.

Confirmed context: 60–80cm nearfield, multiple desktop monitors, room near 19m², separate deep-bass 10–12-inch sub, exceptionally clean 80Hz–2.5kHz satellite region, design budget initially 50–100k RUB with longer staged expansion. Main wooden/resin/possibly composite aesthetic enclosure comes **last**; cheap temporary acoustic measurement box with removable baffle allowed.

## Research takeaway

An independently published, same-measurement protocol study of 6–7.5-inch drivers (AudioHorn: https://audiohorn.net/test/woofer/6-7inch/) compared a selection of SB, Satori, Scan-Speak, Sica and STX midwoofers with EQ matched at 95dB SPL. It reported **SB17NBAC** and premium **Satori MW19-TX** as two leaders, while more expensive MW16-TX and Scan-Speak 18W/4434G00 did not win on its selected criteria. This result is **study-specific**, not a universal proof or a direct test of HiVi.

**Exact variant caveat:** AudioHorn explicitly lists *SB17NBAC-4* (4Ω). The manufacturer-listed SB17NBAC35-8 has a different nominal impedance, sensitivity, Qts and drive winding. The 4Ω test conclusions must not be asserted for the 8Ω variant without checking.

Another independent finished-speaker measurement for HiVi L6-4R: https://ampslab-spk.com/2020/11/27/hawk-xt2/ documents breakup around 2.5kHz, a reason to consider a lower crossover; this is evidence that even reputable Chinese drivers have non-trivial system integration constraints, *not* a disqualification of Chinese products.

## Final-intent model shortlist, comparison status

| Candidate | Config | Fs/Qts/Vas | 2.83V/1m | What distinguishes it | Data limits |
|---|---|---|---|---|---|
| HiVi **M6N** | ~6.5in, 8Ω | 46Hz/.39/21.9L | 89 dB | owner sourced 6,439 RUB, alu-mag cone; economical, potential final driver | no common-method midrange THD / polar comparison against controls |
| HiVi **D6G** | 6.5in, 8Ω | 44Hz/.38/12.1L¹ | 85 dB¹ | owner 7,762 RUB, unusually large 76mm coil and composite cone | ¹secondary T/S/sensitivity; motor and revision validation outstanding |
| HiVi **F6N** | 6.5in, 8Ω | **SOURCE CONFLICT** | ~89 dB seller | owner 6,729 RUB | seller vs alternate: 44/.34/22.7 vs 48/.43/19.1; hold until source reconciled |
| Wavecor **WF152BD06** (or black WF152BD14) | 6in, 8Ω | 46/.35/11.5L *after burn-in* | 87 dB | **Chinese high-performance direct rival**, balanced motor, copper cap, downloadable measured response + impedance text files | local landed price TBD; no same-protocol HiVi measured comparison |
| Wavecor **WF168WA02** | 6.5in, 8Ω | 49/.52/24.6L | 89 dB | 139cm² paper cone, Russian retailer **9,200 RUB each**, described in stock | ±3mm excursion; bigger cone, higher Qts, no common-method HiVi distortion test |
| Wavecor **WF168WA06** | 6.5in, 8Ω | 41/.50/27.7L | 88 dB manufacturer | 131cm² glass-fiber cone, Russian retailer **8,600 RUB each**, described in stock | **seller quotes 86.5dB, Fs49; manufacturer 88dB, Fs41** — must resolve variant/mislabeled item |
| Wavecor **WF152BD14** | 6in, 8Ω | 46/.35/11.5L after burn-in | 87 dB | Black-coated balanced-drive motor, **152mm outer basket**; Russian retailer **14,000 RUB each** | Strong on documentation and nearfield footprint, but compare same-SPL THD before paying more |
| SB **SB17NBAC35-4** | 6in, 4Ω | 30/.29/42.6L | 90 dB | independent AudioHorn test frontrunner, copper sleeve and low Le | 4Ω, bigger Vas, fixture/tweeter integration required |
| SB **SB17NBAC35-8** | 6in, 8Ω | 31.5/.35/45L | 86.5 dB | same family in 8Ω; manufacturer full response/off-axis specification | independently measured -4 results not automatically transferable; EU shop ~€86.45 inc VAT, no Russia landed quote |
| SB **SB15NBAC30-8** | 5in, 8Ω | 35.5/.37/17L | 85.5 dB | compact reference for 60–80 cm + multi-monitor desktop | smaller diaphragm; must evaluate thermal SPL and midrange distortion |
| Scan-Speak Discovery **18W/4434G00** | 18cm, 4Ω | 47/.35/20.7L | 91.5 dB | Danish design, fiberglass cone, independent AudioHorn comparator; EU shop ~€89.95 inc VAT | 4Ω 2.83V corresponds ~2W; larger frame; study saw elevated distortion above 800/900Hz relative to finalists |
| SEAS **U18RNX/P** | 6.5in, 8Ω | data TBD | TBD | Curv cone and copper ring; a meaningful independent engineering comparison | manufacturer narrative verified, latest dimensional/T/S numerics not separately confirmed |
| PURIFI **PTT6.5X04-NFA-06** | 6.5in, 4Ω | 30/.29/25.9L | 88.6 dB | upper-bound distortion/excursion technology, ±9.8mm linear travel | **DKK 2725 ex VAT**, made-to-order ~16w; high-pass stereo+sub may not justify long-stroke premium |
| HiVi **L6-4R** | 6.5in, 4Ω | data TBD | TBD | actual complete DIY loudspeaker measurement exists | ~2.5kHz breakup challenges conventional high crossover |

Sources:
- HiVi values from user's seller cards; see [owner comparison](HIVI-F6N-D6G-M6N-REVIEW.md) and [JSON](simulation/hivi_offers_2026-11-01.json).
- Wavecor WF152BD06 (including **post-break-in** values) https://www.wavecor.com/html/wf152bd05_06_07_08.html ; black coating WF152BD14 https://wavecor.com/html/wf152bd13_14_15_16.html. WF168WA02 https://www.wavecor.com/html/wf168wa01_02.html ; WF168WA06 https://www.wavecor.com/html/wf168wa05_06.html ; Moscow/Russia storefront observed prices https://www.samodelka.ru/cats/10.htm?vendor=291 . Availability is a listing, not a verified transaction.
- SB NBAC -4 https://sbacoustics.com/product/6in-sb17nbac35-4/ ; -8 https://sbacoustics.com/product/6in-sb17nbac35-8/ ; compact 5in https://sbacoustics.com/product/5in-sb15nbac30-8/.
- Scan-Speak: https://www.scan-speak.dk/product/18w-4434g00/ and https://www.soundimports.eu/en/scan-speak-18w4434g00.html.
- SEAS: https://seas.no/index.php?Itemid=238&catid=44&id=102%3Ah1571-08-u18rnxp&option=com_content&view=article.
- PURIFI: https://ptt.purifi-audio.com/shop/ptt6-5x04-nfa-06-ptt6-5x04-nfa-06-1920.
- EU SB -8 offer: https://www.soundimports.eu/en/sb-acoustics-sb17nbac35-8.html.

**Important**: Model names and source quality matter. Never confuse M6N with M6N-B, F6N with F6, Wavecor WF152BD06 with 4Ω WF152BD05, or SB17NBAC35-4 with SB17NBAC35-8.

## New practical finding: genuinely buyable Chinese alternatives in Russia

Russian catalog https://www.samodelka.ru/cats/10.htm?vendor=291 shows:
- WF168WA06-01 at **8,600 RUB each**, posted in stock; manufacturer specifies Fs41Hz, sensitivity 88dB, Qts .50, 8Ω, glass fiber. Retailer claims Fs49Hz and sensitivity 86.5dB — **material discrepancy**.
- WF168WA02-01 at **9,200 RUB each**, posted in stock; Fs49Hz, 89dB, Qts .52, 8Ω, paper cone, ±3mm theoretical linear stroke.
- WF152BD06-01 and black-coated WF152BD14 at **14,000 RUB each**, posted in stock; compact 6-inch 8Ω balanced-drive motor. The black coating avoids manufacturer-recognized UV-induced cone fade in uncoated sibling.

These are meaningful same-market prices, versus owner-observed 6,439 RUB per HiVi M6N and 7,762 per HiVi D6G. Supplier checkout, model/variant, delivery, replacements and final invoice remain unconfirmed. This validates **high-performance Chinese competition is not merely an import substitute**.

## Normalization caveat — don't rank by marketing dB

For 8Ω, 2.83 V is approximately 1 W. For 4Ω, 2.83 V is approximately 2 W, so 2.83V/1m sensitivity must be reduced by ~3 dB to estimate an equal 1W/1m comparison (and precise result depends on actual impedance and manufacturer measuring conditions).

Example: Scan-Speak 18W/4434G00 advertised **91.5dB/2.83V/1m** at 4Ω is approximately **88.5dB/1W/1m** under nominal-load approximation; HiVi M6N advertised 89dB/2.83V/1m at 8Ω is about 89dB/1W/1m. That is not a statement their response, distortion or maximum acoustic output is equivalent.

PURIFI publishes both forms: PTT6.5X04-NFA-06 88.6dB/2.83V/1m and 85.8dB/1W/1m at its specified measured load.

Also 95dB/1m normalized testing is not an endorsement of sustained 95dB listening at 0.6–0.8m.

## Architecture consequence for our 60–80cm listening

- Main woofer should be high-passed once the subwoofer is present; motor stroke advantage below ~80Hz may contribute little to final midrange quality.
- Wide 6.5–7inch cone physically pushes tweeter centre farther from woofer centre and can produce directivity/lobing issues at 0.6–0.8m if crossover is placed too high. Compare a 5-inch reference and smaller **Wavecor 6in**; also study waveguides and phase.
- At 0.6–0.8m, the listening position is not automatically the acoustic far field of a multiway speaker. Measure vertical listening-window sensitivity and use a proper physical baffle before trusting its integration.
- Strong midrange motors/copper rings reduce potential nonlinear effects, but *specification alone is not a measured THD/IMD advantage*.
- A purely low-frequency closed-box F3 ranking is NOT a measure of realistic midrange fidelity.
- Final industrial wooden/epoxy/composite cabinet is deferred until the system and heat/power architecture are well understood; early temporary boxes still need a meaningful sealed volume and accurate mounting.

## Evidence rubric / apples-to-apples gate

Compare all final-intent candidates to the same **acoustic** targets, rather than equal amplifier voltage:

1. **Measured response on axis and at 15°, 30°, 45°, 60°** across the intended band, with same measurement distance/mounting geometry or documented corrections; baffle must permit repeatable centre placement. Retain raw data, smoothing and measurement microphone calibration. Do not derive final 100Hz anechoic response from short indoor gating alone.
2. **Same target acoustic level** at 1m reference (e.g. 85, 90, 95dB *short test intervals*) with flat target and identical bandwidth, then THD separated by H2/H3 and, if possible, multitone IMD and compression. Record applied electrical voltage/power separately.
3. **High-pass condition simulates real 2.1**: model around 80–110Hz and test midband full-level output, avoiding artificially penalizing a 5in for 25Hz extension it will never be asked to deliver.
4. **DSP and crossover**: 1–3kHz usable band, specific measured cone breakup, real acoustic phase, energy dispersion, chosen tweeter's ability to cross sufficiently low; include voice clarity and level-matched subjective comparison.
5. **Reliability and repetition**: test at least two real units of a would-be finalist, production variance Re/Fs, age/temperature effects, measured clamp/terminal/seal, availability and replacement supply.
6. **Cost**: landed 2-unit quote in **RUB** including shipping/returns, matched against total *system* cost and time. Do not compare user RUB listing with Euro manufacturer retail as if prices landed in the same market.
7. **Evidence discipline**: `PUBLISHED_MEASUREMENT`, `OWN_MEASUREMENT`, `MODEL_ONLY`, `UNKNOWN` and explicit manufacturer vs secondary source reliability. No invented third-harmonic curves from T/S data.
8. **No upgrade ladder**: once a candidate passes midrange purity, output, off-axis, reliability, availability and cost gates, it becomes the production candidate; never replace it merely to use a prestige brand.

## Proposed focused four-way measurement shortlist (not ordered yet)

- **HiVi M6N** — 6,439 RUB owner-observed, credible Chinese 8Ω final candidate.
- **Wavecor WF168WA02 / WF168WA06** — Russian-stock 9,200 / 8,600 RUB 8Ω midwoofers; different 6.5in cone/radiation and Qts than M6N, good matched-value challengers.
- **Wavecor WF152BD14** — 14,000 RUB, premium *Chinese* 6in 8Ω balanced-drive engineering competitor with actual numeric response/impedance data and narrower 152mm basket.
- **SB17NBAC35-4** — independent 95dB distortion winner *in tested 4Ω configuration*, high-performing international control.
- **HiVi D6G** — different cone/motor worth comparing if we want a fifth measured variant, but no evidence yet of superior THD.
- Keep **SB15NBAC30-8** as compact fifth candidate if desk width/directivity becomes decisive. Scan-Speak as independent external control with strong manufacturer documentation. PURIFI only as an ambitious upper-bound reference when actual distortion margin matters.

Not all specimens need to be bought simultaneously. A starter purchase could be **one HiVi M6N + one D6G** only if seller identification is verified, but it's preferable to have Wavecor and SB17NBAC source-based curves in the software first; the physical head-to-head must be run on actual comparable fixtures.

## New discovery: Wavecor downloadable numerical data

Wavecor provides **actual frequency/impedance response data in text format** for WF152BD14/16 black-coated variants on https://wavecor.com/html/wf152bd13_14_15_16.html (measured in infinite baffle). This makes them *very attractive for the first digital crossover simulation before parts purchase*. Manufacturer warns results differ in a real finite baffle. The black coating also addresses documented sunlight-related cone fading for uncoated WF152BD05/06/07/08.

## Next work product

- Identify currently buyable **HiVi, Wavecor and SB control** with unambiguous exact part and seller in Russia or deliverable to Russia; no unsupported price conversions.
- Download or obtain numeric FRD and impedance files for Wavecor and other alternatives; obtain actual angular datasets with provenance before scoring.
- Define nearfield/tweeter design cases and real test setup. Do not announce a 'winner' until all measured common-method gates pass; fair comparisons may produce an exciting final Chinese driver, but that result must be earned, not assumed.
