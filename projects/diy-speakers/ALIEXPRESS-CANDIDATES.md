# AliExpress Midwoofer Candidates — Pending Exact Identification

Date: 2026-11-01. Status: **three named HiVi models supplied by owner; user-observed prices; seller identity and exact item-to-variant mapping not externally verified**.

**Update:** owner identified models/descriptions/prices as HiVi F6N (6,729 RUB), HiVi D6G (7,762 RUB) and HiVi M6N (6,439 RUB). They are now compared against independently available specifications, including a serious F6N revision/source discrepancy, in [HIVI-F6N-D6G-M6N-REVIEW.md](HIVI-F6N-D6G-M6N-REVIEW.md). The unresolved SKU mapping and source separation in the table below remain valid.

The owner initially supplied two ali.click URLs and then provided **three direct AliExpress Russia item IDs with explicit selected SKUs**:

| Label | Listing | Selected SKU | Identity verified? |
|---|---|---|---|
| A | https://aliexpress.ru/item/1005012112593734.html?sku_id=12000057541009369 | 12000057541009369 | **No — storefront unavailable** |
| B | https://aliexpress.ru/item/1005010706311970.html?sku_id=12000053252107661 | 12000053252107661 | **No — storefront unavailable** |
| C | https://aliexpress.ru/item/1005013335483366.html?sku_id=12000060917810176 | 12000060917810176 | **No — storefront unavailable** |

Owner's observation: all selected listing options are **under 10,000 RUB per unit** as seen in their account; this is **user-reported**, not an independently verified quote. We cannot yet establish model, loudspeaker role, frequency range, material, exact unit count, impedance or any Thiele–Small parameters.

The old affiliate leads remain unresolved: https://ali.click/2nf7p1i and https://ali.click/8jf7p1e. Do not assume a one-to-one match with any of the three direct item IDs.

AliExpress Russia storefront returned an access/anti-bot failure through available browsing methods; searching exact product/selected SKU IDs found **no reliable metadata match**. **Never substitute information from a similar-looking but different ID.** To identify the three listings, request one screenshot of each product title + selected variant + visible technical specifications (ideally seller's datasheet/table). If dimensions/options differ by SKU, the selected SKU is authoritative for this comparison.

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


## Physical-development update: the real enclosure is the LAST step

The owner explicitly wants a difficult, futuristic, beautiful final cabinet — not an early plywood compromise. The owner has access to a small tool workshop and can build **temporary plywood test enclosures / replaceable baffles**.

The first electromechanical research fixture therefore uses:
- **free-air / open-frame driver mounting for low-level electrical and T/S measurements only**, with high-pass and conservative input to prevent excessive unbaffled LF excursion;
- a simple *temporary* measured-volume plywood or MDF test box for usable low-frequency, crossover and off-axis acoustic comparison; its volume, sealing, removable front panel and bracing must be documented;
- replaceable baffles that fit exact **measured** driver cutout/mounting dimensions; no machining of the aesthetic final wood/resin/composite enclosure;
- independent low-voltage amplifier/protected PSU and simple measurements with a calibrated microphone before any high-power testing.

**Why not assess sound quality on an unbaffled driver?** Rear acoustic radiation cancels front bass and changes response; no final bass extension, baffle-step/directivity or crossover integration can be inferred from free-air listening.

It can still make sense to purchase two of an affordable, correctly identified driver early as an **experiment** even with missing published T/S, provided exact model/impedance/geometry and quantity/cost are confirmed. The measurement bench can *produce* missing T/S before the final design.
