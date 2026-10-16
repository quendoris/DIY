# Acoustics and Near-Silent Key Design

Status: **highest-priority performance requirement**, ahead of RGB and premium CNC.

The owner explicitly wants the contrast of a **solid, premium metal touch surface** and **near-silent key travel and return**. No traditional click should be necessary to know a key has actuated. The tactile force transition must arise **passively, with the electromagnet fully off**; see [PASSIVE-MAGNETIC-TACTILITY.md](PASSIVE-MAGNETIC-TACTILITY.md).

Do not interpret Hall/TMR switching or magnetic return as sufficient proof of silence. The key and chassis are mechanical/acoustic structures; contactless electrical sensing only eliminates the electrical contact mechanism.

## Noise sources — separate them before optimizing

1. Bottom-out: key stem/keycap collides with hard travel limit.
2. Top-out: returning key hits its rest stop.
3. Side-load: rattling/rocking of stem against guides, plus stabilizer noise for large keys.
4. Resonance: thin-walled metal cap, stem, plate, metal frame and cavity ringing.
5. Force feedback: rapid magnetic snaps or active actuators can excite vibrations despite having no contact switch.
6. Electrical noise: coil drivers, inductor or magnetic assembly whine in the audible band.
7. External source: fingernail hitting metal, and transmission of vibration to desktop.

## Mechanical design hypotheses

### H1: magnetic return + quiet end-stops

Use permanent magnets for passive return and resting position. Include discrete, user-serviceable, compliant **bottom-out and top-out stops**; neither is a metal-to-metal impact.

Candidate stop materials: formulated silicone, urethane and similar engineering elastomers selected for compression set, aging, skin oils and temperature.

The stops should be deliberately separated from the Hall/TMR sensing path and should not determine actuation electrically.

### H2: rigid metal touch surface, controlled internal damping

A heavy metal chassis does not guarantee silence; it can radiate/transfer energy efficiently if excited.

Prototype cap interiors with:
- different wall thicknesses/rib positions;
- intentionally damped internal islands or liners;
- mass distribution variations that shift problematic resonances;
- isolated coupling of key module to structural plate.

Avoid relying only on foam under the PCB: measure cap-specific resonance and its coupling to the body.

### H3: avoid loose guides

Low-friction guided stems are still mechanically contacting parts unless a separate constrained bearing architecture is used.

Test precision clearance, dry polymer guides/bushings, preloading and stability over repeated cycles. Too-tight tolerances can cause binding and friction noise; low play alone is not proof of good typing feel.

### H4: optional active magnetic deceleration

With displacement plus a credible velocity estimate, a powered actuator **might** decelerate a fast keystroke before bottom-out and soften return near top-out. This is an experiment, not a safety mechanism.

Prove actuator force vs position/current, response time, power and latency, including worst-case rapid typing and multiple simultaneous keys.

Power-off, saturation, missed sensor sample or driver fault must still lead to harmless and reasonably quiet mechanical stops. Never assume firmware can eliminate all bottom-out events.

### H5: controlled decoupling

Test a removable key cartridge/plate isolation scheme that attenuates vibration without making the entire keyboard mushy. Soft mounts may conflict with positional precision and should be evaluated by measurement.

## Prototype matrix

Compare at minimum:

- metal cap vs light polymer control;
- hollow vs ribbed/damped metal cap;
- soft vs firm, replaceable top/bottom stops;
- passive magnet return vs active-assisted damping;
- isolated vs rigid cartridge/plate attachment;
- normal vs deliberately off-axis key presses;
- several typing velocities and repeated bottom-outs.

Use the **same key geometry and equivalent measurement setup** for controlled A/B comparisons.

## Acoustic protocol (draft)

Measure baseline ambient noise, then single actuation, repeated actuation and realistic typing.

Record:
- calibrated microphone and distance (initial draft: 0.25 m and 0.5 m);
- room ambient and device position;
- downstroke, release and long-key/stabilizer cases;
- peak level plus time-weighted A-weighted equivalent sound level, and spectra/transients;
- stroke force/travel, impact speed and keycap variant;
- audible tonal artifacts from PWM/current drivers;
- comparisons with a known quiet commercial keyboard.

The existing ~30 dBA idea is an **aspirational target pending measurement conditions**; a single decibel number without the ambient, time window and measuring geometry is not a meaningful specification. Do not present 30 dBA as proven.

A more robust acceptance plan records per-keystroke peak and integrated sound exposure above measured ambient, and compares variants under identical conditions. Real-room listening trials are also required.

## Comfort must survive silence optimization

Key should not feel sticky, sluggish or spongy. Track:

- full press force/displacement curve;
- rebound/return latency;
- hysteresis and repeatability;
- keycap wobble;
- bottom-out sensation;
- acoustic output.

A successful design feels **firm and precise under the finger** but sounds restrained, without sharp metallic knocks or ringing.

## Initial gate

Do not order a complete titanium cap set until at least **three metal-cap variations on a one-key rig** have been compared to a lighter control, using reproducible acoustic measurements.
