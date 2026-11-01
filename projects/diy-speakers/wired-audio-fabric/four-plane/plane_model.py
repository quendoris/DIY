#!/usr/bin/env python3
"""Deterministic four-plane AUDIT MODEL. No crypto, real clock servo, or PHY.

Failure and control-plane contract testbed. A simulated auth verdict is an
input, NOT evidence that cryptographic attestation was implemented.
"""
from __future__ import annotations

import heapq
import itertools
import json
from dataclasses import dataclass, field
from enum import IntEnum


class Plane(IntEnum):
    SAFETY_LOCAL = 0
    TIME = 1
    CONTROL = 2
    ATTESTATION_HEALTH = 3
    AUDIO = 4


class Status(IntEnum):
    READY = 0
    DEGRADED = 1
    MUTED = 2
    UNKNOWN = 3
    FAULT = 4


@dataclass(frozen=True)
class EndpointTelemetry:
    name: str
    received_ms: int
    identity_authenticated: bool
    firmware_measurement_accepted: bool
    rail_ok: bool
    amplifier_ok: bool
    clock_locked: bool
    available_buffer_ms: float
    fan_ok: bool = True
    fan_required: bool = False
    local_hardware_trip: bool = False


def assess_endpoint(
    report: EndpointTelemetry,
    now_ms: int,
    max_telemetry_age_ms: int = 300,
    min_buffer_ms: float = 20.0,
) -> dict:
    if now_ms < 0 or max_telemetry_age_ms <= 0 or min_buffer_ms < 0:
        raise ValueError("Invalid inspection contract")
    if report.received_ms < 0 or report.received_ms > now_ms:
        raise ValueError("future/invalid report time")
    reasons = []
    if report.local_hardware_trip or not report.rail_ok or not report.amplifier_ok:
        reasons.append("LOCAL_HARDWARE_OR_RAIL_FAULT")
        status = Status.FAULT
    elif now_ms - report.received_ms > max_telemetry_age_ms:
        reasons.append("STALE_TELEMETRY")
        status = Status.UNKNOWN
    elif not report.identity_authenticated or not report.firmware_measurement_accepted:
        reasons.append("UNVERIFIED_DEVICE_OR_FIRMWARE")
        status = Status.UNKNOWN
    elif not report.clock_locked:
        reasons.append("CLOCK_UNLOCKED")
        status = Status.MUTED
    elif report.fan_required and not report.fan_ok:
        reasons.append("REQUIRED_FAN_FAULT")
        status = Status.DEGRADED
    elif report.available_buffer_ms < min_buffer_ms:
        reasons.append("LOW_BUFFER_MARGIN")
        status = Status.DEGRADED
    else:
        status = Status.READY
    return {
        "name": report.name,
        "state": status.name,
        "reasons": reasons,
        "report_age_ms": now_ms - report.received_ms,
        "note": "Telemetry assertions are supplied by a test oracle, not independent hardware proof",
    }


def aggregate(reports: list[EndpointTelemetry], now_ms: int) -> dict:
    if not reports:
        return {"state": Status.UNKNOWN.name, "endpoints": [], "reasons": ["NO_ENDPOINTS"]}
    if len({e.name for e in reports}) != len(reports):
        raise ValueError("duplicate endpoint names")
    results = [assess_endpoint(r, now_ms) for r in reports]
    state = max(Status[e["state"]] for e in results)
    return {
        "state": state.name,
        "endpoints": results,
        "report_age_max_ms": max(e["report_age_ms"] for e in results),
        "scope": "Only the included required endpoints and the modeled evidence were checked",
    }


@dataclass(order=True)
class QueuedEvent:
    priority: int
    insertion_order: int
    plane: Plane = field(compare=False)
    label: str = field(compare=False)


class DeterministicScheduler:
    def __init__(self):
        self._items: list[QueuedEvent] = []
        self._counter = itertools.count()

    def push(self, plane: Plane, label: str) -> None:
        if not label or not isinstance(plane, Plane):
            raise ValueError("invalid event")
        heapq.heappush(self._items, QueuedEvent(int(plane), next(self._counter), plane, label))

    def pop(self) -> QueuedEvent | None:
        return heapq.heappop(self._items) if self._items else None


def fiber_propagation_difference_ns(extra_meters: float, speed_m_per_s=2e8) -> float:
    if extra_meters < 0 or speed_m_per_s <= 0:
        raise ValueError("invalid path parameters")
    return extra_meters * 1e9 / speed_m_per_s


def oscillator_drift_samples(sample_rate_hz: int, relative_ppm: float, seconds: float) -> float:
    if sample_rate_hz <= 0 or seconds < 0:
        raise ValueError("invalid clock estimate")
    return sample_rate_hz * relative_ppm * seconds * 1e-6


def demo() -> dict:
    initial = [
        EndpointTelemetry(name=n, received_ms=1000, identity_authenticated=True,
                          firmware_measurement_accepted=True, rail_ok=True,
                          amplifier_ok=True, clock_locked=True, available_buffer_ms=80)
        for n in ("left", "right", "sub")
    ]
    scheduler = DeterministicScheduler()
    for plane, name in [(Plane.AUDIO, "audio_block_20"),
                        (Plane.ATTESTATION_HEALTH, "health_heartbeat"),
                        (Plane.TIME, "clock_update"),
                        (Plane.CONTROL, "pause"),
                        (Plane.SAFETY_LOCAL, "local_hw_trip_notification")]:
        scheduler.push(plane, name)
    order = []
    while (event := scheduler.pop()) is not None:
        order.append(event.label)
    faulty = initial.copy()
    faulty[2] = EndpointTelemetry(
        name="sub", received_ms=1000, identity_authenticated=True,
        firmware_measurement_accepted=True, rail_ok=False, amplifier_ok=True,
        clock_locked=True, available_buffer_ms=80, local_hardware_trip=True,
    )
    return {
        "four_logical_planes": ["attestation_health", "control", "audio", "sync_time"],
        "safety_local_is_independent_of_optical_control": True,
        "nominal": aggregate(initial, 1050),
        "sub_power_fault": aggregate(faulty, 1050),
        "deterministic_priority_order": order,
        "extra_5m_fiber_delay_ns_estimate": fiber_propagation_difference_ns(5),
        "50ppm_96khz_drift_over_1s_samples": oscillator_drift_samples(96000, 50, 1),
        "cryptography_implemented": False,
        "physical_clock_sync_implemented": False,
        "measured_bounds": False,
    }


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, sort_keys=True))
