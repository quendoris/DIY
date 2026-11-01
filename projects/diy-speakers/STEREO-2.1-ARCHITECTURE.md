# Stereo 2.1 — owner-approved direction and architectural options

Status: **requirements captured, design and component selection not frozen**.
Updated after the owner clarified placement, sound goals, aesthetics and incremental budget.

## Owner's requirements (2026-10-30)

- **Use:** serious music listening, including bass-heavy phonk, not exclusively mixing or a treated studio.
- **Environment:** room around **19 m²**, but future room/placement will vary.
- **Placement:** main loudspeakers on/near a desk used with multiple computer monitors, at a **listening distance of 60–80 cm**; exact dimensions are *secondary* to quality and sensible spending.
- **Music priority:** exceptionally clear, intelligible midrange; clean detailed treble; **very deep, physically impactful bass** is mandatory for the total system.
- **Subwoofer:** a separate third enclosure with a **10-inch** driver is acceptable, with **12 inches** open to comparison if extra output requires it.
- **Appearance:** visible attractive wood is a priority. Pear was a spontaneous example, *not* a mandatory species. Carbon composite, resin coating and other finishes may be explored if appearance, safety and cost warrant them. A plastic-looking or all-metal exterior is not the preferred visual identity.
- **Budget philosophy:** initial investment roughly **50,000–100,000 RUB**, possibly **up to 200,000 RUB** across years of incremental work. This is *not* a promise to buy the finished system all at once, and no component vendor/price is selected.
- **Modularity:** evaluate, buy, test and improve each module independently, while preserving future replacement/upgrade paths.
- **Listening reference:** user confirmed **ADAM Audio T5V** as heard reference and **ADAM Audio T8V** as target benchmark (not KRK ROKIT). Use real manufacturer specs and measurement data, but do not promise superior sound from nominal specs alone.
- **Integration:** should complement the user's content/sound engine and local audio system without double-EQ or conflating separate digital transfer requirements.

## Near-field reference dimensions

ADAM manufacturer data (not DIY design targets):

| Model | Size H × W × D | LF driver | Frequency extension (-6 dB) | Crossover |
|---|---|---|---|---|
| T5V | 298 × 179 × 297 mm | 5 in | 45 Hz | 3 kHz |
| T8V | 400 × 250 × 335 mm | 8 in | 33 Hz | 2.6 kHz |

Sources: [T5V](https://www.adam-audio.com/en/t-series/t5v/) · [T8V](https://www.adam-audio.com/en/t-series/t8v/).

At 60–80 cm, prioritize low idle hiss, listener-angle stability, tweeter-midwoofer vertical spacing, desk reflections and positioning alongside monitors. The sub should be independently positioned off-desk. A smaller near-field satellite plus sub is an *architectural hypothesis* for the user's goals, not a proven T8V-beating design.

## First executable calculation

[simulation/acoustic_baseline.py](simulation/acoustic_baseline.py) implements a deliberately small-signal sealed-enclosure model (Fs, Qts, Vas, Vb) and ideal Linkwitz–Riley 4 electrical crossover response with reproducible numerical tests. It has **no real measured driver**, no SPL/excursion prediction, no diffraction, desk, room or acoustic time alignment. The baseline is a math sanity test before comparing actual drivers and cabinets.

## Preferred starting hypothesis: 2.1

Two high-quality near-field **two-way** satellites for stereo imaging, mids and treble; one separate active subwoofer to carry deep bass.

```text
USB / local digital audio / optional future dedicated receiver
                 |
        content / music engine
        (optional, bypassable)
                 |
   speaker-specific DSP and protection
     |        |         |
   LEFT      RIGHT     SUB
  LF + HF   LF + HF   10-12" LF
   amps      amps     dedicated amp
```

A central flexible DSP with 5 independent output channels (woofer + tweeter × 2, sub × 1) is one candidate. Do not confuse this with 5.1 multichannel input. An alternate first build is two passive stereo loudspeakers with a stereo amplifier plus independently active subwoofer; fewer amplifier channels and less initial electronics, but passive filters have their own cost and tuning tradeoffs.

**Modularity caveat:** turning an existing two-way enclosure into a three-way design is not necessarily a plug-in upgrade: the acoustic baffle geometry, crossover, cavity and directivity change. Reserve the option for a new satellite/front-baffle module rather than pretending a third driver can always be added.

### Performance hypothesis — not yet an acceptance specification

- Model the satellites with around **5–7-inch** midwoofers and suitable tweeters.
- Explore controlled sub crossover around **70–100 Hz**, chosen from measured acoustic responses, not a hard rule. High-pass the satellites when sub is in use to reduce low-frequency excursion.
- Investigate useful in-room sub extension to around **25–30 Hz**, with a defined listening-seat SPL, distortion limit, excursion margin, amplifier headroom and thermal budget.
- Compare **10- and 12-inch** sub candidates. A 10-inch driver does not automatically deliver high SPL at 25 Hz; displacement, cabinet alignment and power determine that.
- Room response near 19 m² will be influenced by modes/boundaries, furniture and actual dimensions; the room area alone cannot fix modal frequencies. A second future sub may help position-to-position consistency more than another expensive tweeter.
- Prioritize low hiss in nearfield listening, matched satellites, smooth horizontal directivity and natural midrange over maximal headline watts.

## Placement

- Separate placement for the sub avoids forcing a large woofer onto a crowded desk.
- For the satellites test isolated desktop risers, compact stands behind/alongside displays or securely mounted brackets. Aim tweeters toward ear height and keep geometry roughly symmetric about the listening position.
- The desk surface can cause first-reflection response notches; measure and optimize distance/height/tilt. Mechanical isolation protects against rattles but is not an acoustic-room correction by itself.
- Do not mandate a fully treated room, but do acknowledge low-frequency modal peaks/nulls; use placement and appropriately limited EQ where effective.
- Avoid blocking display screens or forced close-to-wall port arrangements without testing.

## Cabinet aesthetic and longevity

Investigate:
1. braced birch plywood or MDF as a stable structural cabinet with a **beautiful real-wood veneer**, chamfered solid hardwood front/trim or replaceable outer panels;
2. carefully engineered solid-wood cabinet with moisture-movement joints and verification;
3. optional composite/carbon-fiber or carefully applied resin outer finish when its mass, cost, health safety and repairability are justified.

Wood species remains open. Grain, finish, UV behavior, humidity, seam construction, removable driver service and repeatability matter. Epoxy coating is a visual/durability choice, not guaranteed acoustic damping; cure emissions, dust and skin sensitization need safe procedures.

## Amplifier / DSP domains

- Keep sound-engine content transformation separate from speaker calibration (gain, crossover, delay, driver limits, EQ and protection).
- Provide a bypassable reference listening path and explicit gain/headroom tracking.
- Compare inexpensive documented Class D amplifier modules with premium benchmarks at the **same output voltage/current/noise/THD+N, load, thermal conditions and price**.
- One shared external controller/amplifier rack or serviceable modules inside satellites are both research options. External electronics make replacing a board easier and reduce heat in the small cabinet.
- The separate portless player does **not** automatically output USB/analog into these speakers: an independent compatible receiver, PC DSP input or future explicitly designed digital interface is required.

## Incremental gates (not purchase commitments)

**R0 — zero-cost requirements/model:** room geometry envelope, SPL & bass criterion, comparative 2.0 vs 2.1 vs 2.2; numerical box and driver model.

**R1 — one speaker module:** source one midwoofer and one tweeter only after datasheets, calculate sealed/vented reference box, simulate crossover and baffle, build low-cost cabinet coupon, measure.

**R2 — stereo pair:** match a second speaker and compare polar responses, pair balance, near-field hiss, desk reflection and listening tests. **50–100k RUB** is a *planning envelope* for the initial system, not a quote.

**R3 — subwoofer module:** simulate 10"/12", sealed/vented/passive radiator, maximum SPL/distortion/excursion and positioning; add independent amp, protection and adjustable crossover. This may extend cumulative spend beyond the initial envelope.

**R4 — integrated 2.1/2.2:** independently movable sub, delay/phase/crossover integration, measured room variations, protection, calibrated profiles.

**R5 — exceptional optional upgrades:** higher-grade driver or stronger DSP/amp if measured benefit exceeds the cost, second sub, experimental motional feedback. Keep **~200k RUB** as a loose total development ambition, not an entitlement to spend.

A cheap full stereo solution is not valuable if the desired deep bass, clean mids and durability are not met; conversely the most expensive tweeter is not justified by its price.

## Open items requiring owner input

1. Approximate ear-to-speaker listening distance and planned desktop/stand arrangement.
2. Typical listening level and whether very high sound pressure is intended, mindful of safe listening.
3. Would a subwoofer under/next to the desk be acceptable? Placement is not fixed at design stage.
4. Which exact model was heard: ADAM T5V/T8V, KRK ROKIT 5/8, or another?
5. First digital source for development: PC USB audio into external DAC/DSP, or a self-contained controller?


## Digital transport research branch

The owner also proposed a **strictly wired**, distributed optical network between a central digital controller and separately powered satellites/subwoofer. The audio link is digital, so a DAC sits locally after the fiber receiver. The PC connects to the controller via USB-C using a chosen compliant data protocol. Receiver-side buffering and independently authenticated control are to be verified, as are multi-device clock drift and synchronization. Read [wired-audio-fabric/README.md](wired-audio-fabric/README.md) and [CONTRACT.md](wired-audio-fabric/CONTRACT.md). This idea does **not** replace the separate wireless earbuds concept.
