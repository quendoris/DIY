# Engineering Notes — Player

## Important corrections to inherited discussion

The imported conversation contains hypotheses, design preferences and several numerical overclaims. None of the following should be treated as an already validated performance figure.

### Bulk transfer

At **30 Mbit/s of sustained application payload**, one decimal 1 TB of data requires about **74 hours** (before overhead). It does **not** take 8 hours.

To transfer decimal 1 TB in **two hours**, the actual payload throughput must average about **1.11 Gbit/s**. This cannot be assumed for Qi negotiation/data signaling or a generic low-rate inductive channel.

A USB 2.0 connection using four signal/power contacts does not become USB 3.x SuperSpeed by changing firmware. USB 3.x requires additional high-speed differential signal paths, suitable controlled-impedance interconnects and qualified docking geometry.

Thus the current desired priorities are:

1. Portless exterior;
2. Qi-compatible wireless charging when technically appropriate;
3. Independent bulk-data transfer design, with real throughput testing;
4. Pogo-contact dock only as a clearly labelled fallback/tradeoff.

### Wireless charging and housing

Use a dielectric charging/RF window and characterize metal proximity, ferrites, coil alignment, losses, eddy-current heating and battery temperature.

### Battery

Charging in an intentionally reduced SoC band can reduce some degradation modes; exact lifetime depends on cell chemistry, temperature, calendar ageing, charge rate, usable capacity and environmental stress.

Do not promise 8–15 years of battery service or schedule forced 0–100% cycles without a demonstrated fuel-gauge requirement.

Use approved protection, thermistor measurement and charge-controller safety features. Firmware policy supplements but never substitutes independent electrical safety.

### Embedded design

The earlier STM32H747 dual-core split (M7 UI, M4 audio/network) is a **candidate**. Validate:

- sustained file-system and storage throughput;
- selected AMOLED electrical interface;
- DMA, SRAM and UI framebuffer memory;
- digital audio framing/transcoding assumptions;
- RF transport buffering and clock synchronization;
- watchdog and signed-update/failsafe design.

A high-quality player need not use a powerful application processor if its tasks genuinely fit the MCU, but performance should be demonstrated rather than asserted.

### Physical durability

IP67/IP68 or any other ingress-protection claim must be demonstrated with the final assembled device.

Full potting can degrade repairability and create thermal/mechanical stresses. Waterproofing is not automatic from use of resin.

## Reference constraints

- USB Type-C / SuperSpeed wiring: https://www.usb.org/sites/default/files/USB%20Type-C%20Spec%20R2.0%20-%20August%202019.pdf
- Wireless Power Consortium Qi: https://www.wirelesspowerconsortium.com/standards/qi-wireless-charging/
- FLAC format: https://www.rfc-editor.org/rfc/rfc9639.html

## Practical prototype principle

Start with a reusable external development rig: storage, display, processor and audio radio outside the final titanium enclosure. Physical miniaturization, hermetic sealing and expensive metal machining should be later gates.
