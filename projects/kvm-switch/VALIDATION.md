# Verification and Development Gates

All gates are to be backed by scripts or repeatable measurements. Open-source artifacts should separate original public specifications from assumptions, inferred behavior, vendor-only details and tests.

## K0 — topology and acceptance definition

Record exact input/output counts and meaning of ten HDMI ports, permitted simultaneous routes, source duplication requirements, number of independent USB upstream computers, USB-C power roles, required keyboard/mouse persistence and protected-content support.

Define acceptance cases at minimum:
- 4K240 8-bit and 10-bit RGB full chroma, with explicit DSC support assumptions;
- lower-rate fallback to 4K120/144 and 1440p240;
- HDR, VRR, stereo/audio behavior as needed;
- 5×5 permutation routing with illegal source/sink conflicts rejected;
- USB2/3/USB4 host disconnect/re-enumeration as a **measured separate property**.

## K1 — math and protocol models

Compute:
- HDMI active pixel/bit rate and FRL mode/payload overhead vs 4K240 profiles;
- video route count, high-speed lane count and mux/crosspoint fanout requirements;
- USB4 router/domain constraints and CC/PD role states;
- end-to-end connection state machine and timeouts;
- hardware token challenge-response and authorization expiry;
- power-supply sequence/current limits for 10 HDMI ports plus USB.

## K2 — data-driven part selection

For every prospective component collect exact datasheet, availability, pinout, voltage, per-lane rate, insertion loss, return loss, power, package, interface, evaluation hardware and price/availability quotes. Distinguish endpoint, hub, host, router, mux, linear redriver and retimer.

No chip gets into the BOM because its family name sounds compatible with USB4 or HDMI.

## K3 — SI/PI/EMC simulation

Use a PCB/channel simulator supporting transmission lines, connectors, S-parameters and eye/bathtub/BER analysis; include source cable, sink cable, connectors, board traces and any mezzanine links.

Analyze differential impedance, insertion/return loss, skew, reflections, crosstalk, via stubs, retiming/equalization and BER margins at relevant FRL/USB4 rates. Model power-integrity, startup, fault and transient loads separately.

An optical board renderer or KiCad geometry check alone does not validate a 12-Gbit/s differential link.

## K4 — firmware reference model

Build an independent state-machine simulator with ports, auth, route requests, HPD/EDID states, FLR/FRL (use FRL in implementation), PD states, USB enumeration and faults.

Safety properties:
- no route mutation without authorization;
- no two ports shorted/back-powered;
- no cross-host management or HID data leakage;
- no partially committed route reported as successful;
- recover safely after MCU reset, token loss, monitor unplug or PD fault;
- stale EDID version and monitor replacement handled explicitly.

## K5 — isolated representative benches

First build representative **one HDMI source ↔ one HDMI sink via a selected mux path**, and separately a USB2 HID multi-host virtualization bench / USB3 switched-upstream bench. USB4 protocol-level bench only after an appropriate router/hub development kit and documentation are identified.

Before full 5×5 assembly validate the exact signal-integrity budget on the chosen physical channel. Physical results are used to calibrate and challenge the models, not treated as substitute for modeling.

## K6 — integration and production

Only after K0–K5: fab high-speed Video board, USB board and Main board; run repeated switch/retrain cycles, errors, power/EMI/thermal tests, OS interoperability and authorization fault injection. Retain raw evidence, tool versions and independent reviews.

## Budget methodology

No trusted turnkey target price yet. Qwen's $600–$2,000 estimates lacked verified full topological BOM and fab/assembly quotes.

Build **three independent cost envelopes**:
1. management + low-speed control bench;
2. independent full-rate HDMI proof-of-channel;
3. independent USB4-compatible proof-of-channel.

Then add multiport scaling, mezzanine/cable cost, assembly yield and revision count. Instrumentation/access to lab equipment must be explicit, not silently priced at zero.

## Design freeze rule

No 10-port routing PCB, board-to-board high-speed connector or completed 5×5 switch architecture until the required paths, cable loss budget and verified available devices are demonstrated in a complete channel calculation.
