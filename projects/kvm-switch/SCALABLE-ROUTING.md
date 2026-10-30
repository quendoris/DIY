# Scalable N-Host × M-Display Routing (2026-10-30)

Status: **revised user-approved direction, before electrical architecture freeze**.

## Replace the arbitrary ten-port limit

Do not freeze the device at ten HDMI sockets. Treat 2×2, 3×3 and 5×5 as *test-case sizes*, not maximum sizes. Define separate independent limits for:
- number of host computers H;
- physical upstream connectors U;
- independent source video streams S;
- monitor/output connectors M;
- physical switch fabric bandwidth, fanout and power;
- the number of logical displays a particular host GPU/OS can actually drive;
- headroom reserved for future daughterboards and protocols.

The number of computers is **not necessarily** the number of source ports. One computer may use multiple independent HDMI inputs; one DP MST or suitable USB4 uplink may carry multiple video streams. A standard HDMI SST source link does not produce two independent extended desktops.

## Concrete owner scenario: 3 PCs, 4 monitors

Desired assignment:
- Laptop → monitors 1 and 2, distinct independently extended displays;
- desktop PC → monitors 3 and 4;
- third PC remains available for reassignment.

Feasible *in principle* if the laptop has a DP MST-capable GPU/OS/output or suitable USB4 display transport, each monitor mode fits in the available link data budget, the actual hub/router/switch topology exposes independent sinks and the display-count limitations are met.

One ordinary HDMI source port by itself cannot provide this independent two-monitor experience. A passive HDMI splitter can generally mirror the same output; it does not create a second independent desktop.

The physical design may use HDMI **downstream outputs** while accepting DP/USB-C/USB4 upstream sources and actively converting/branching formats. This does not require a host-side HDMI input per monitor.

## Three layer model

**Layer A — desired user ownership:** Host H owns monitors M1 and M2, host P owns M3 and M4. When ownership changes, the routing controller calculates a new target state.

**Layer B — resource feasibility:** Assign each monitor an independent source video stream on one of that host's physical uplinks; check GPU display count, stream count per uplink, effective payload rate, mode/DSC/VRR/HDR and whether simultaneous routing is available.

**Layer C — protocol and hardware execution:** Allocate MST/DP/USB4 tunnels as applicable, maintain correct EDID/HPD/source/sink state, drive crossbars/converters, manage retraining, authorization and rollback.

A pass in layer B says nothing about SI, PHY, FRL, HDCP or possible hotplug behavior in layer C.

## Independent playback modes

- **EXTEND**: independent operating-system monitor identities, each consuming a distinct generated source stream. This is the main requirement.
- **MIRROR**: identical source image cloned to multiple sinks, with different electrical/source semantics. Do not silently substitute for EXTEND.
- **REASSIGN**: monitor changes ownership between hosts; source OS may detect a hotplug, remove/add a display, or renegotiate timing. No zero-flicker guarantee.
- **MULTI_HOST**: display assignment from several hosts simultaneously on distinct sinks. This is core.
- **MULTICAST / PROCESSED VIDEO**: true fan-out, compositing, arbitrary extraction of independently encoded streams from a non-MST HDMI transport. Separate research modes, not a baseline.

## Layer A/B math

At the logical level, each monitor has at most one assigned host, while a host can own multiple monitors if GPU/streams/bandwidth permit. The one-to-one N×N scenario has N! full permutations; this is a useful exhaustive state-model test but **does not prove any particular physical matrix exists**.

For H hosts and M independently assigned displays, ignoring physical capacity, the number of total assignments to hosts or an unassigned state is (H+1)^M. Additional restrictions reduce the physically valid states.

A logical router must compute a valid assignment and reject unsupported requests with a machine-readable reason, not silently switch to lower quality or clone mode.

## Open-source modeling stack

The first zero-cost executable example lives in [simulation/](simulation/README.md):
- pure Python deterministic stream/host/payload-capacity planner;
- 2×2, 3×3, 5×5 permutations;
- 3-host/4-monitor scenario and deliberate negative tests.

Next independent gates:
- **TLA+/TLC or Apalache** to check route/authorization/invariants;
- **Linux DRM MST kernel interfaces** as a primary reference for DP MST topology and hotplug semantics;
- **ngspice** for power and low-speed circuits;
- **scikit-rf / PyBERT** for high-speed channel/S-parameter and eye/BER investigations, only with realistic device/channel input;
- **openEMS** for EM analysis of geometry where appropriate;
- actual video link training/HDCP/USB4 compliance require later device-level verification and may not have complete open-source simulators.

All results must include assumptions, mode lists, unknown properties, source data and reproducible commands. Avoid claims that software predicts every unknown real-world electrical behavior.

## Low-budget sequencing

K0: mathematical resource allocation and counterexamples — free.
K1: versioned state machine and authorization model — free.
K2: capability discovery, protocol specification study and interface feasibility — mostly free.
K3: SI/PI/channel modeling using real S-parameters or bounded assumptions — mostly software effort.
K4: only then buy a minimal independent HDMI/DP/USB development path, not a full 5×5 board.
K5: scale tested building blocks and revise materials/stackups as channel budgets require.

User preference: many exploratory project ideas are welcome; do not spend money or freeze a final housing now.
