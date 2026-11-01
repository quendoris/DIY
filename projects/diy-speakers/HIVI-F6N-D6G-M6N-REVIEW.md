# HiVi F6N vs D6G vs M6N — Owner Offers and Engineering Review

Date: 2026-11-01. Status: **preliminary technical comparison; no completed measurements, no committed purchase**.

## What was provided

The owner supplied substantial seller descriptions for three real HiVi/Swans driver models, with observed Russian-market **per-unit** prices (not independently rechecked, delivery/tax may vary):

| Unit | Owner-observed RUB each | RUB for two |
|---|---:|---:|
| F6N | 6,729 | 13,458 |
| D6G | 7,762 | 15,524 |
| M6N | 6,439 | 12,878 |

The owner previously gave three AliExpress links with exact SKUs; we do **not** confidently map all three item IDs to the three named models, as storefront verification remains blocked. Don't accidentally equate an unrelated F6 datasheet with F6N or the damped M6N-B version with M6N. Identify exact chosen SKU/lot and confirm the seller ships **one** or **two** drivers at the advertised price.

## Parameters and provenance

| Parameter | F6N SELLER description | F6N alternative source | D6G independent source | M6N SELLER description |
|---|---:|---:|---:|---:|
| Rated/max power (W) | 45 / 90 | 45 (RMS) / not checked | 60 / 120 | 45 / 90 |
| Nominal impedance (ohm) | 8 | 8 | 8 | 8 |
| Fs (Hz) | 44 | **48** | 44 | 46 |
| Qts | 0.34 | **0.43** | 0.38 | 0.39 |
| Vas (L) | 22.7 | **19.1** | **12.1** | 21.9 |
| Xmax (mm, one way reported) | 3.5 | **4.5** | 4.8 | 4.3 |
| 2.83V/1m sensitivity (dB) | 89 | 88.7 | **85** | 89 |
| BL (T·m) | 8.5 | 7.3 | 9.5 | 7.8 |
| Voice coil diameter (mm) | 25 | 25 | 76 | 25 |

**F6N source conflict is material, not rounding:** source scenarios would give different closed-box sizing and midwoofer sensitivity. The owner listing is internally reasonably consistent (Qts from Qms=2.01 and Qes=.41 is ~.341; stated excursion from (14.5−7.5)/2 = 3.5mm). But the alternative HiVi F6N directory reports Fs=48, Qts=.43, Vas=19.1L and Xmax=4.5mm. It links to a manufacturer-hosted PDF that the accessible fetch mechanism rejected. Do **not** combine the two scenarios or quietly use specifications for different **F6**.

- Alternative F6N source: https://bits.00aud.io/drivers/hivi/f6n-8ohm

**D6G source split:** The owner's card omits most T/S parameters, so Qts=.38 and Vas=12.1L here are **secondary-sourced** data, not claimed as owner data. Other sources corroborate Fs 44, 60W nominal, 120W maximum, 76-mm coil, Xmax 4.8mm and sensitivity 85 dB; manufacturer's own listing identifies the D6G and its coil/cone architecture. Some reseller descriptions disagree about the magnetic material (one says ferrite, another says neodymium), requiring vendor confirmation rather than a fabricated decision.

- Manufacturer: https://www.swanspeakers.com/commercial/product/view?id=479
- Data directory: https://bits.00aud.io/drivers/hivi/d6g-8ohm
- Detailed retailer specs: https://diyaudiocart.com/product/hivi-d6g-6-1-2-midrange-yellow-kevlar-cone-casting-aluminum-frame-8ohm-pair/

**M6N data are largely reproducible:** Fs 46, Qts .39, Vas 21.9, Xmax 4.3, 45W nominal, 89 dB sensitivity, Re 6.5 ohm. An example of poor machine translation in the owner description is “moving mass 13.9 L”: **mass cannot be measured in liters**, and other published tables give approximately 13.6 g. It is not valid to use the mistranslated figure as-is.

- https://www.rumoh.eu/speakers/hivi/woofer/1711/hivi-m6n
- https://radio63.narod.ru/page/download/M6N.pdf

## What the construction really tells us

- **M6N:** aluminum-magnesium cone; 89dB nominal sensitivity; best **first two-way midwoofer research baseline** on cost/data completeness. Investigate mid-to-tweeter crossover, high-frequency cone breakup and off-axis beaming. The sub makes extreme satellite LF extension unnecessary.
- **D6G:** Kevlar/paper composite cone with a very large 76mm coil; 60W nominal, 4.8mm Xmax but 85dB nominal sensitivity. Roughly 2.51× electrical input power is needed for the same level if comparing those published 2.83V sensitivity figures *under equivalent conditions*. This is not itself a quality defect; nonlinear distortion, directivity and actual acoustic power require measurements. Interesting advanced A/B candidate at only ~2.65k RUB extra per *pair* compared with M6N.
- **F6N:** potentially good 6.5-inch LF/mid driver, but the material T/S discrepancy should be resolved before treating it as equal-data comparison; it may reflect a different revision/test method or catalog error, not proof of counterfeit stock.

No actual **THD/IMD** or controlled comparison of midrange has been performed; do not claim a 'more musical', 'more accurate' or 'Hi-End' winner based on marketing.

## Small-signal common enclosed-box test

To avoid comparing one manufacturer's 14L vented F3 to another seller's 15L vented F3, the bundled [hivi_offer_sweep.py](simulation/hivi_offer_sweep.py) models **an 8-liter sealed reference fixture** for all four data scenarios. These values are *only illustration of box behavior*, not proof of actual sound quality or recommended final cabinet.

| Model + parameter scenario | 8L model Qtc | 8L model F3 (Hz) | Net sealed liters for hypothetical exact Butterworth Qtc=1/sqrt(2) |
|---|---:|---:|---:|
| F6N seller | 0.666 | ~91.8 | ~6.83 |
| F6N alternate | 0.791 | ~79.9 | ~11.21 |
| D6G secondary | 0.602 | ~83.9 | ~4.91 |
| M6N seller | 0.754 | ~83.7 | ~9.58 |

The model cannot conclude that D6G and M6N sound the same based on their similar small-signal F3 in this one reference box. It also cannot predict their midrange THD, crossover response or attainable 80–100Hz output at high drive.

## What to buy first?

**Engineering/measurement-first plan** (not an unconditional order):

1. If quickly making a stereo pair matters most: two identical **M6N** with the exact same vendor variant/lot, budget 12,878 RUB at owner-observed price before any missing fees.
2. If comparing the unknown motor/cone technology matters more than immediate stereo: one **M6N** and one **D6G**, budget 14,201 RUB at owner-observed prices, with no direct stereo pair until selected design has two matching units.
3. Hold F6N until source discrepancy/part revision resolved; a single test unit remains possible if the seller can confirm correct identity but not provide reliable T/S. We can derive T/S ourselves after arrival.

**Potential issue of desktop fit:** all three have nominal ~179mm-class frames (verify exact D6G cutout from its drawing). That is already close to the ADAM T5V's external 179mm cabinet width and may make a 6.5-inch midwoofer cabinet fairly wide. Compare a real 5-inch alternative before freezing final nearfield baffle geometry.

## Enclosure strategy is explicitly FIXED by the owner

The final futuristic aesthetically engineered wooden/composite/resin cabinet will be designed **last**, once the acoustics and electronics are mature. Until then:
- free-air fixture at conservative input only for basic impedance/suspension/T/S;
- simple plywood **temporary** sealed or vented boxes with removable baffle and measured actual internal net volume for acoustic tests;
- record baffle dimensions, grille, seals and driver inset to make measurements repeatable;
- no unrestricted LF power into a free-air driver; no claims of realistic bass response outside a proper acoustic test baffle.

During shipping we can build a safe low-voltage amplifier/impedance measurement jig, calibrated measurement setup and repeatable scripted sweeps. After arrival, measure true Re, Fs, Qts, Vas (known-volume or added mass), impedance vs frequency, off-axis response, level-dependent THD, thermal effects and L/R matching.

## Next decisions

Need exact selected SKU-to-model mapping, model revision and vendor shipping quantity; manufacturer published Le, Sd and response/impedance tables where available. A pair purchase is reasonable if one variant satisfies role, geometry and actual delivered price, but never guarantees better-than-ADAM subjective sound without assembled-speaker measurements.

The low-level electrical bench can proceed while the [protected DC foundation](../shared-power/README.md) is being developed; final wood aesthetic design remains a later independent project.
