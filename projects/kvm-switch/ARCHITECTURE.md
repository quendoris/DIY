# Architecture and Open Questions

Status: early proposed architecture. No device part is selected for production.

## 1. Routing topology must be explicit

**Revised baseline:** scalable multi-host / multi-display routing with independently counted host computers, physical video uplinks, logical independent video streams and output monitors. Test 2×2, 3×3, 5×5 logical permutations and the owner's 3-host/4-display scenario. A full 5×5 SST fabric remains one important special case, not the top-level system limit. Upstream DP MST/USB4 display transport can carry more than one independent stream if the host, link, conversion/router and target modes support it. Standard HDMI SST cannot be made a two-display extended-desktop source by a passive splitter. Full details: [SCALABLE-ROUTING.md](SCALABLE-ROUTING.md).

Three functional modes to separate:
- `SINGLE`: one selected host/sink, basic KVM;
- `PERMUTATION`: independent routes for five sources to five monitors without duplicating a single source;
- `MULTICAST`: one source image cloned to multiple sinks — separate and possibly expensive path;
- `MULTI_HOST_EXTEND`: multiple hosts own different monitors simultaneously, with multiple independent streams per host where available — **core use case**.

Do not assume that a tree of four-lane 2:1 muxes will automatically become a functional multi-output HDMI matrix. Inspect per-lane routing, termination, redriving, mux insertion loss, cable lengths and management channels.

## 2. Video board

Physical video datapath: 4 differential FRL lanes per HDMI 2.1 full-rate link at up to 12 Gbit/s/lane, in addition to low-speed control/auxiliary signals. The requested 3840×2160 240 Hz RGB/4:4:4 mode usually needs DSC within the 48-Gbit/s HDMI 2.1 bandwidth; exact 8/10-bit, HDR and timing compatibility must be source/sink-specific.

At 3840×2160×240:
- 8-bit RGB active-picture information: **47.775744 Gbit/s** before blanking/transport.
- 10-bit RGB active-picture information: **59.71968 Gbit/s** before blanking/transport.
- HDMI 2.1 FRL 48 Gbit/s is a *raw link* figure, with usable payload below it.

Source / monitor capability records must capture EDID, max FRL rate, DSC, VRR, HDR, color format, timing, and actual behavior under retraining.

**Verified candidate silicon (not yet chosen):** Diodes PI3WVR14412: 4-channel 2:1/1:2 analog video mux/demux with up to 20 Gbit/s per high-speed channel, and DDC/HPD switching. It is not by itself a complete 5×5 matrix, EDID engine, HDCP repeater or retimer.

Consider both transparent physical routing and active repeater/topology; these are not equivalent architectures and have different costs, protocol duties and licensing constraints.

### EDID/HPD/FRL semantics

EDID caching can avoid unnecessary monitor disappearance from the desktop. But keeping HPD asserted **does not by itself** maintain FRL link training, SCDC state, video frame continuity, HDCP authentication or VRR. A source with a permanently presented virtual sink may still be transmitting a real high-speed link that requires sink electrical termination and valid protocol behavior.

Do not promise sub-millisecond black-frame-free switching until complete source/sink side states, retraining deadlines and signal integrity have been modeled and measured.

HDCP 2.3 is not a blanket requirement for all HDMI 2.1 signals. Protected content must be handled compliantly and transparently, or explicitly declared unsupported. Do not attempt to extract keys or bypass content protection.

## 3. USB board: divide by function

Never equate USB-C (connector), USB 2.0/3.2 (legacy device links), USB4 (router/tunneling fabric) and USB Power Delivery (power-role protocol).

- **USB 2.0 HID control:** could be duplicated through separate logical device interfaces per PC, with explicit policy for ownership and no cross-host data bridging. This can provide smoother keyboard/mouse switching at the cost of firmware and security work.
- **USB 3.x hub switching:** switching one upstream host ordinarily causes device-disconnect/re-enumeration; preserve operation as a normal compliant USB device rather than promising a seamless illusion.
- **USB4:** protocol domains are organized under a host connection manager. PHY-speed muxes alone are not a multi-host USB4 router. Choosing a host requires correct USB-C CC/PD negotiation, role/orientation, USB4 entry, link reset/training and tunnel restoration. Evaluate actual router/hub architectures and whether multi-host switching at the requested speed is implementable with distributable devices/docs.
- **Power delivery:** design independent source/sink/DRP roles for each port. STUSB4500 is sink-only and cannot independently implement every power role. Provide VBUS overcurrent, reverse-current prevention, inrush protection, discharge and failure isolation.

Verified silicon distinctions:
- ASMedia ASM2464PD is a USB4-to-PCIe/NVMe **endpoint/device controller**, not a generic USB4 multi-host hub.
- VIA VL830 is a USB4 **endpoint** with an integrated USB 3.2 hub and DP function, not a general multi-host fabric router.
- TI TUSB546-DCI is USB 3.1 Gen1 (5 Gbit/s) + DP Alt Mode mux/redriver, **not USB4 40/80 Gbit/s**.

## 4. Management board

An STM32H5-class MCU is a sensible baseline; select exact variant from measured GPIO, I2C/SPI, flash, debugging, and isolated-power needs. Higher-end STM32H7 is allowed if it solves an actual measured requirement. RTOS choice follows testable timing/reliability needs rather than branding.

Management responsibilities:
- route topology and ownership authorization;
- per-port identity/versioned EDID state;
- HPD, DDC, SCDC, FRL link state tracking/telemetry;
- USB host/peripheral presence and link state tracking;
- USB-C role/PD and VBUS policy;
- board discovery/health/temperature/voltages;
- transactional route updates and fault recovery;
- cryptographically authenticated management actions;
- signed updates, rollback and safe recovery.

Recommended operation model:
```text
IDLE → AUTHORIZED → PRECHECK → QUIESCE → ROUTE → LINK_TRAIN
                                      ↓               ↓
                                  ROLLBACK ← FAULT / TIMEOUT
                                                      ↓
                                                 VERIFY → COMMIT
```

This is **logical transactional consistency**, not impossible physical atomicy of HDMI and USB links. Keep host isolation and the previous valid route where safe. Fail closed for unauthorized switching, but safe and deterministic for power failures.

## 5. Hardware token and security

Treat the token as authentication of management operations, not proof of an impenetrable device:
- challenge-response via a secure element with unique non-exportable private key;
- ephemeral session, nonce, replay counter, authorization policy, expiry, rate limit;
- safe enrollment/revocation/recovery;
- physical tamper/forced unplug scenario;
- write-restricted management interface;
- firmware verification and debug-lock policy.

Avoid unsupported claims such as 'bank HSM level' from choosing ATECC608 alone. FIDO2 token integration is a distinct USB Host + authenticator-protocol project.

Critical protection: never inadvertently bridge data between two PCs through the KVM controller. HID virtualization, hub switching, and management transport are separate trust domains.

## 6. Backplane and PCB

Every high-speed PCB or daughterboard connector introduces an RF discontinuity. Keep FRL and USB4 high-speed paths localized on dedicated boards if possible. If they cross mezzanine interfaces, use qualified high-speed connectors/cables and account for the complete channel loss budget.

Select material and geometry **by measured insertion/return loss and eye-opening**, not a blanket rule that FR4 is impossible. Use impedance control, continuous reference planes, via-stub analysis and backdrilling where required by the specific geometry. Arbitrary universal length matching such as 5 mil for every pair is not a valid substitute for channel simulation.

Dedicated always-on auxiliary power should feed the MCU and safe management/EDID state. Per-port high-current USB power is a separately budgeted and independently protected subsystem.

## References (primary)

- HDMI overview and optional feature policy: https://www.hdmi.org/blog/detail/139
- HDMI 2.2 newer maximum-link bandwidth: https://www.hdmi.org/blog/detail/189
- Diodes PI3WVR14412: https://www.diodes.com/part/view/PI3WVR14412
- USB4 system topology: https://www.usb.org/sites/default/files/D1T1-3%20-%20USB4%20System%20Overview.pdf
- USB4 2.0 specs: https://www.usb.org/document-library/usb4r-specification-v20
- ASMedia ASM2464PD: https://www.asmedia.com.tw/product/802zX91Yw3tsFgm4/C64ZX59yu4sY1GW5.html
- VIA VL830: https://www.via-labs.com/product_show.php?id=114
- TI TUSB546: https://www.ti.com/product/TUSB546-DCI
- STUSB4500 sink-only: https://www.st.com/en/interfaces-and-transceivers/stusb4500.html
