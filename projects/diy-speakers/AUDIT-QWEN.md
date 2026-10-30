# Audit of Attached Qwen Premium Speaker Proposal

Status: **engineering critique, not a verified vendor-by-vendor BOM**.

The original document proposes an expensive four-way active system and a roughly $8,400 three-way alternative, including pear-wood/MDF/CLD cabinet, Purifi woofer and amplifiers, premium beryllium/AMT tweeters, 4096-tap FIR DSP, motional feedback and optional active panel control. This is much more elaborate than the owner's current requirements justify.

Most claims in the pasted source contain bracket numbers such as [[42]] but their underlying bibliography/links were not supplied. Their exact specifications and prices cannot be accepted without first finding manufacturer datasheets and current supplier quotes.

## Claim audit

| Original claim | Correction / unresolved issue |
|---|---|
| Pear solid wood is categorically the worst cabinet material | Too absolute. Mass, stiffness, damping, dimensions, grain, joints and bracing matter. Pear has meaningful anisotropic moisture movement; choose with engineering design and test. |
| MDF is neutral while plywood gives an intrinsically 'dry sound' | 'Dry sound' cannot be deduced from the raw sheet material alone. Model and measure panel modes and radiation. |
| Every cabinet requires ~32–38 mm CLD composite | Not justified. Controlled-layer damping can help some modes but cabinet sizing and bracing may be cheaper and adequate. |
| 4–6 mm solid pear laminated against MDF will definitely never warp and pairs match exactly | Unproven. Moisture cycling, adhesive, grain, residual stress, sealing and assembly tolerances must be evaluated. |
| 'Wadding is a myth' and only point dampers work | Misleading. Porous acoustic absorption inside a cabinet treats internal standing waves; panel structural damping addresses different phenomena. Both may matter. |
| Best tweeter must be a $300–600 beryllium/AMT or a $1500 ribbon | Not established; compare polar/directivity, distortion, integration and value with affordable candidates. |
| Premium multi-hundred-watt amplifier for every tweeter | Usually unjustified without extraordinary SPL/load requirements. Amplifiers must be sized by power, headroom, impedance and noise; not prestige. |
| DSP FIR can fully linearize low-frequency phase/response | Cannot override excursion, power, air displacement, noise and room-response nulls. Low-frequency equalization costs headroom. |
| Raw FIR workload 4096 × 96000 × 8 = 3.145728 GMAC/s demands high-end x86 | Arithmetic applies to direct time-domain convolution, not fast partitioned FFT convolution used by real DSP engines. Use actual benchmark and latency requirement. |
| Current/voltage automatically yields exact cone velocity: v = (U - IR)/Ke | Incomplete: voltage across inductance, temperature-dependent resistance, flux/inductance nonlinearities, frequency and measurement error affect observability. Must identify the system and validate against an independent displacement/speed reference. |
| Servo feedback is absent from all commercial loudspeakers | False. Rythmik uses sensing-coil direct-servo subwoofer designs. |
| Any feedback automatically reduces THD by 10–20 dB | Unproven; stability, bandwidth, delay, model mismatch and driver physics control benefits. |
| Sealed box + EQ always gives excellent bass and needs no room-position consideration | Incorrect. Sealed trades output/efficiency for behavior and still couples to room boundaries/modes; EQ may exceed excursion limits. |
| A dedicated treated room or $50k NFS is required to measure decent DIY speakers | Overstatement. Calibrated microphones, gated far-field, near-field bass, repeatable angular measurements and public simulation tools allow serious development; note low-frequency/phase caveats. |
| UMIK-1 necessarily costs $250–400 | Wrong for the manufacturer direct price as of the cited source, which lists $79 before regional shipping/taxes. |
| Speaker pair must cost $8k–16k to be 'above ADAM' | Not a valid engineering inference. Specify which ADAM model, distance, level and metric, then use a budget-constrained objective comparison. |

## Important source examples

- TI TPA3255 datasheet and operating conditions: https://www.ti.com/product/TPA3255
- miniDSP manufacturer UMIK-1 price and calibration: https://www.minidsp.com/products/acoustic-measurement/UMIK-1
- SB Acoustics SB26ADC manufacturer specs: https://sbacoustics.com/product/sb26adc-c000-4/
- Dayton Audio RS180-8 manufacturer specs including vented/sealed F3: https://www.daytonaudio.com/product/101/rs180-8-7-reference-woofer-8-ohm
- Pear wood dimensional behavior: https://www.wood-database.com/pear/
- Real servo system from Rythmik: https://rythmikaudio.com/DirectServo.html
- Open-source CamillaDSP with real FFT convolution and benchmarks: https://github.com/HEnquist/camilladsp

## Decision

Do **not** freeze the source's proposed hardware, guaranteed performance/THD gain, cabinet wall thickness or $16k price. Model competing affordable architectures against specified owner use; reserve the more experimental ideas for optional later R&D.
