# AliExpress Midwoofer Candidates — Pending Exact Identification

Date: 2026-11-01. Status: **user-provided leads; target listings not yet resolved, NO model/price/spec verified**.

The owner asked whether low-cost Chinese loudspeaker drivers available through these AliExpress affiliate redirects can replace the costly imported reference midwoofers:

- Candidate A: https://ali.click/2nf7p1i
- Candidate B: https://ali.click/8jf7p1e

Automated retrieval of these shortened redirect destinations was unsuccessful. **Do not assign a manufacturer, nominal size, impedance, speaker type, price or T/S measurements to these links until the final product page is independently visible.** For inspection request direct `aliexpress.com/item/<id>.html` links or a screenshot of each listing including selected variant, exact model, price, shipping and any specification image.

## The main distinction: midrange vs midwoofer

Our present desktop baseline is a **two-way satellite** (one 5–6.5-inch midwoofer + one tweeter) backed by a separate 10–12-inch subwoofer. This midwoofer must handle the important ~80–2000+ Hz region (final crossover depends on measured response/directivity), not merely operate as a 300–3000 Hz dedicated midrange. A listing for a **pure midrange** driver might suit a future three-way satellite, but it is **not automatically a replacement** for SB15MFC30-8 / SB17NRX2C35-8.

The subwoofer relaxes the satellite's deep-bass requirement, making a well-documented, fairly priced Chinese 5/6-inch driver a credible and attractive first experiment.

## Purchase gate for a low-cost candidate

| Field | Evidence to save | Stop/continue guidance |
|---|---|---|
| Exact model/selected option | complete product title, seller model, brand, 4/8-ohm and diameter variant, photos | model ambiguity => do not buy as a finalized pair |
| Units and seller | whether sold individually or pair; shipping, returns, seller reputation | ambiguous number of units => ask seller first |
| Geometry | outer diameter, cutout, mounting depth, holes, centre dimensions | needed before front baffle machining; removable baffle if unknown |
| Electrical | nominal impedance **and measured curve if available**, DC resistance, rated voltage/power | nominal wattage alone not enough |
| T/S | Fs, Qts, Vas, Re, Le, Sd, Xmax and their measurement conditions where available | missing T/S can still be accepted as explicitly **experimental**, not prevalidated |
| Acoustic | on-axis/off-axis response, bandwidth with smooth crossover region, harmonic distortion vs SPL | absent data => bench will have to measure before final crossover |
| Logistics/cost | two identical units from same revision/lot, total *delivered* RUB price | compare same-market *per pair* cost, not sticker alone |
| Return/repair | possibility of reordering replacement with same revisions | long-term serviceability |

## Buying *before* electronics design is complete

If the actual listing turns out to be a suitable **5–6.5-inch midwoofer** with credible seller/manufacturer identity and a sufficiently low total delivered price, buying **two identical units** can be a rational early experiment. Explicitly label it a **measurement/research purchase**, not a final selection. Buying a single unit first can minimize exposure when listing identity or quality is uncertain.

Prepare these independently while shipping:
1. versioned 5/6-inch replaceable-baffle test box designs with net volume alternatives; do **not** irreversibly cut front holes until exact mechanical drawings/measurements are confirmed;
2. speaker impedance sweep fixture and calibrated software to estimate T/S (added-mass or known-volume measurements);
3. microphone measurement protocol: gated response at 60–80 cm, nearfield LF, multiple angles, matched excitation and repeatable gain, THD/IMD at documented levels;
4. Class-D amplifier prototype with independent current-limited low-voltage supply and safe max-output protection;
5. exploratory two-way crossover in DSP without assuming ideal LR4 electrical transfer matches true acoustic transfer;
6. stereo pair matching criteria and production acceptance recording (coil DC resistance, Fs, curves, polarity).

A manufacturer's published `100 W`, `Hi-Fi`, `Kevlar`, `neodymium`, `carbon`, `N52` or `wide frequency response` claim **does not establish midrange clarity or production consistency**.

## Known Chinese-engineered benchmark, *not* either unidentified link

HiVi M6N-B 6-inch midwoofer: 8 ohm, Fs 46 Hz, Qts .39, Vas 21.9 L, sensitivity 89 dB (2.83V/1m), Xmax 4.3 mm, stated max normal 45 W, mounted diameter ~179 mm / cutout ~142 mm. The official published spec can be used to benchmark data completeness:
https://www.parts-express.com/pedocs/specs/297-488--hivi-m6n-b-spec-sheet.pdf

Verified retailer page showing this model in stock and a European retail amount (not a price delivered to the owner): https://www.soundimports.eu/en/hivi-m6n-b.html

Reference imported models for comparison: [CANDIDATE-COMPARISON.md](CANDIDATE-COMPARISON.md), and engineering kickoff: [DESIGN-KICKOFF-D0.md](DESIGN-KICKOFF-D0.md).

## Decision discipline

Until the final listing is visible, both user links are recorded as **UNRESOLVED**. No false comparison can be made. The correct next action is to inspect selected variants, source primary specs if possible, and then compare against HiVi and SB in the same math-and-measurement workflow.
