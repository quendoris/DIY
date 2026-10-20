# LOMO Biolam S-11: PC-controlled microscope

**Status:** concept + dimension-unverified OpenSCAD assembly v0.1. This is not a factory reconstruction, printable mount, or safety-validated instrument.

## Owner requirements

- One PC application controls all normal operations over a local Ethernet connection to **Orange Pi Zero 3 (4 GB)**. No obligatory manual lighting or position controls.
- Two independently controlled lighting heads: transmitted light below specimen, reflected light above. Proposed white COB + eight-pixel RGB ring in each.
- Upper light: azimuth (approximately a quarter-circle of motion), a smaller vertical arc and independent head pitch. It must park outside the optical workspace, **physically latch**, and report sensor-confirmed park state.
- Two modes: transmitted for transparent preparations and high magnification; reflected for opaque surfaces and PCBs.
- Motorized coarse/fine Z focus and new X/Y stage. Accuracy, repeatability, quietness and fail-safe positioning take precedence over speed.
- Replaceable nonmetallic ESD-dissipative work surface for glass slides and PCBs. Powered boards need separate insulating supports.
- One external isolated fanless supply with individually protected rails; low electrical, thermal and mechanical noise.
- Programmable camera acquisition, focus stacks, XY mosaics and lighting series with metadata for every image.
- Independent hardwired E-STOP; no reliance on Linux/Ethernet for emergency stop, and no uncontrolled Z drop if actuator power is lost.

## Hardware confirmed or owned

- LOMO Biolam S-11, marked C11 and 838612. **Installed objectives:** 8x/0.20, 40x/0.65, 90x/1.25 MI (oil immersion).
- USB UVC camera: MC50-B, USB VID:PID 0ac8:3420. Linux driver uvcvideo.
- V4L2 advertises 2592x1944 MJPEG @15 fps and YUYV @2 fps. Actual achieved FPS, true sensor resolution and image quality remain unmeasured.
- Orange Pi Zero 3 4 GB, Raspberry Pi 3 Model B v1.2 (available for a separate test bench).
- MCP4725 single-channel DAC, MP1584EN buck module, WS2812 RGB ring with eight LEDs, white COBs advertised as 10 W, SG90 servos (not final precision actuator choice).
- Owner observed COB first visible output near 7.36 V and high brightness near 8 V. These **do not** establish continuous current rating. Listing 9–11 V / 300 mA / 10 W is internally inconsistent: select current-limited drivers only after bench characterization.

## Documentation

- [Architecture](ARCHITECTURE.md): system boundaries, modes, motion and safety.
- [Validation](VALIDATION.md): instrument measurement, electronics and motion acceptance gates.
- [Discussion evidence record](SOURCE-NOTES-2026-10-20.md): edited source notes, **not a raw chat export**.
- [Coordinate-based measurement worksheet](MEASUREMENT-PLAN.md): precise measurements for v0.2+ CAD.\n- [CAD notes](cad/README.md) and [OpenSCAD v0.1 assembly](cad/biolam-s11-envelope-v0.1.scad).

**CAD provenance:** published overall envelope 230x140x360 mm is a family maximum; exact optical offsets and mounts have **not** been measured. Current geometry uses deliberately labeled assumptions. Factory reference: https://www.biolam.su/files/biolam.pdf and https://www.zenit-npk.ru/fcatalog/info/49

## Private conversation archive

This public DIY repository holds technical design documents, **not plaintext conversations**. The [project archive policy](private-archive/README.md) refers to the [generalized QAR utility in quendoris/snippets](https://github.com/quendoris/snippets/tree/feat/qar-authenticated-archive/qar-authenticated-archive) for local Argon2id + AES-256-GCM encryption of an owner-provided complete transcript. **No complete encrypted transcript has been uploaded yet.**
