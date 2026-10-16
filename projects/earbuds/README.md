# Modular Wireless Earbuds — Concept

Status: **concept; common audio/radio validation required**.

## User goals

- Small earbud form factor, broadly inspired by AirPods Pro-like geometry.
- Removable **cylindrical rechargeable cell** in a screw-off lower stem; selection, actual size/capacity and availability not yet validated.
- Touch/gesture sensor on the bottom/end of the stem.
- High-grip exterior that remains secure in rain or wet ears; optional ear hooks/fins and multiple tip sizes.
- Metal components in titanium or magnesium alloy where practical, with protected RF antenna region.
- Strong, adjustable hybrid active noise cancellation and separately controllable ambient transparency.
- High-quality music playback that does not have its processing interrupted by ANC.
- Owner-controlled firmware and modular/serviceable design.
- Preferred dedicated **2.4 GHz proprietary digital radio** from the companion local player, physically without Bluetooth capability.

## Subsystems

```text
dedicated 2.4 GHz receiver + antenna
                ↓
        jitter/reorder buffer
                ↓
       audio decoder / DSP
                ↓
         DAC + amplifier
                ↓
           transducers

feedforward / feedback microphones
                ↓
     low-latency ANC DSP/control
                ↓
  controlled summation at audio output

replaceable cell + independent protection + fuel gauge
sealed screw cap / gasket + ergonomic touch region
```

The music and ANC paths should have **independent scheduling and DSP resources** where justified, but their electrical/acoustic outputs inevitably interact. Acoustic design and measured stability are critical.

## Risks

- Very small **safe removable batteries**: verified charging compatibility, connector life, short-circuit prevention and battery mechanical protection.
- Water resistance around repeatedly opened threaded battery caps.
- Antenna detuning/shielding by metal, wet skin and head proximity.
- Actual RF throughput after packet overhead, interference and retransmits.
- Decoder compute and energy consumption in each earbud.
- ANC instability, noise amplification, microphone placement and safe transparency gain.
- Mechanical fit, ear retention, sound quality and thermal comfort.

## Audio-quality claims

Custom proprietary 2.4 GHz is a **design preference**, not proof that Bluetooth is inherently low quality. Contemporary Bluetooth systems can also deliver lossless audio in supported conditions.

Do not guarantee 24-bit/96-kHz lossless from a nominal 4-Mbit/s PHY. The raw stereo PCM rate is 4.608 Mbit/s, FLAC compression is content-dependent, and useful RF payload throughput is below the advertised raw PHY bit rate.

A zero-error digital audio transport must be established through data integrity measurements, buffering and RF tests; 'bit-perfect' is an acceptance criterion, not an architectural assumption.

See [ENGINEERING-NOTES.md](ENGINEERING-NOTES.md) and [ROADMAP.md](ROADMAP.md).
