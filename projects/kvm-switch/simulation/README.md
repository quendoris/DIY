# N-host/M-display Routing Model (Stage K0)

The first simulator is **logical**: it allocates independently rendered monitor streams to upstream links and ensures that stream-count, effective payload and host display-count budgets are not exceeded. It uses Python's standard library, no purchased hardware and no proprietary SDK.

It **does not simulate** HDMI FRL, DisplayPort MST protocol packets, USB4 tunnels, DSC compression, VRR/HDCP, EDID/HPD state machines, electrical crossbars, real S-parameters or PHY link training. Passing its tests does not prove the proposed hardware can be built.

## Run

From this directory:

    python3 -m unittest -v
    python3 router.py
    python3 router.py --square 2
    python3 router.py --square 3
    python3 router.py --square 5

## First results

- 2×2: 2 full one-to-one route permutations.
- 3×3: 6 full one-to-one route permutations.
- 5×5: 120 full one-to-one route permutations.
- 3 hosts / 4 monitors: two independent 2560×1440@60 8-bit RGB active-picture demands allocated over **one hypothetical DP MST uplink** from the laptop; two 1920×1080@60 8-bit RGB demands allocated to two HDMI links from the desktop. The third host remains available for reassignment.

The bandwidth numbers are **illustrative input assumptions**: active-picture data alone is not the same as required transport bit rate. The hypothetical upstream budgets (15 and 8 Gbit/s) are neither claims about a specific product nor certification of HDMI/DP capability. Real links must include timing, blanking, link encoding, protocol overhead, DSC behavior if present, and source/sink limits.

The negative tests intentionally reject:
- two independent screens claimed from one ordinary HDMI SST input, even with an unlimited bit-rate assumption;
- an MST link with insufficient bandwidth;
- a laptop configured to produce fewer independent screens than requested.

## Next stages

1. Separate computers, physical ports, **independent rendered streams** and output monitors into explicit topology/ownership entities.
2. Implement VRR/HDR/DSC capability negotiation and a reliable versioned EDID/HPD/MST lifecycle model.
3. Add atomic route-plan validation (transactional control-plane commit, not physically instantaneous switching).
4. Add modeled failures, power resets, host disconnects, cable changes and unauthorized attempts.
5. Verify state invariants with exhaustive tests and TLA+/Apalache or TLC.
6. Then run full-rate HDMI/DP SI/PI models with datasheet/S-parameter evidence.

Reference: https://www.displayport.org/cables/driving-multiple-displays-from-a-single-displayport-output/
