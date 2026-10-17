# Local Audio Player — Concept

Status: **concept only; architecture and requirements not frozen**.

Shared player/earbud constraints and validation gates: [Audio System Architecture](../audio-system/README.md).

## Intended experience

A physically small but satisfyingly heavy premium portable music player, designed as an independent instrument rather than a smartphone substitute.

Owner priorities:

- Local playback only; no internet services, Wi-Fi or Bluetooth stacks.
- No conventional external ports; ideally no exposed electrical contacts.
- Touchscreen; at most one sealed physical/Hall-based power/control button.
- Metal (titanium-focused) chassis and durable surface.
- Good water resistance, no case or daily protective accessories.
- Wireless charging, ideally through a shared rear dielectric insert.
- Local high-capacity storage for FLAC/ALAC and possibly DSD.
- Fully owner-controlled embedded firmware; preference for bare-metal/RTOS STM32-style platform.
- Configurable battery conservation such as a 30–90% operating window.
- Dedicated digital 2.4 GHz connection to companion earbuds, with no analog headphone jack.
- High reliability, diagnostics, recoverable firmware updates and careful power design.

A 2.4–2.8-inch AMOLED was **discussed**, not selected. Sapphire cover glass, 1 TB storage and an STM32H747-class dual-core design are candidates, not final commitments.

## High-level architecture

```text
sealed metal housing + RF/charging dielectric window
  ├── touchscreen + sealed input
  ├── MCU/SoC + RAM + firmware storage
  ├── audio file storage + verified metadata/library
  ├── deterministic reader/packetizer
  ├── dedicated 2.4 GHz radio + antenna
  ├── battery monitor / charge controller / protection
  ├── wireless power receiver
  └── safe recovery/service path (design TBD)
                    │
                    ▼
       custom digital radio protocol
                    │
                    ▼
          dedicated companion earbuds
```

If the player only transmits **digital** audio and has no analog output, it need not include a conventional headphone DAC/amplifier; those remain in the earbuds.

## Architecture decisions not yet made

1. **Data transfer vs truly portless design.** The preference is wireless/contactless transfer through a dock/insert. The earlier proposal of pogo-pin contacts is an engineering fallback, **not an accepted requirement**.
2. **Fast import throughput.** A Qi power-control channel is not a high-speed 1 TB data interface. Bulk transfer needs a separately validated data PHY (contactless near-field / RF / optical or an accepted physical dock).
3. **Ingress protection vs repairability.** Permanent potting and fully sealed enclosures may prevent battery replacement, storage repair or safe thermal expansion; investigate service strategy first.
4. **Display/MCU/storage.** Validate actual interface support, lifetime availability and memory/throughput, not just marketing specifications.
5. **Charging profile.** 30–90% is a longevity-oriented user policy, not a guarantee of a particular multi-year cycle life.

## What counts as success

- Verifiable offline operation with minimal attack surface;
- repeatable and reliable audio read-to-radio path;
- no unexplained dropouts;
- measured battery life and temperature;
- physical water-resistance testing;
- a tested, recoverable firmware and library import procedure.

See [ENGINEERING-NOTES.md](ENGINEERING-NOTES.md) and [ROADMAP.md](ROADMAP.md).
