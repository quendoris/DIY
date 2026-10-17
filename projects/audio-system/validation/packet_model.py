#!/usr/bin/env python3
"""Deterministic packet-level audio-link model; standard library only.

This is an early scheduling/budget model, not a waveform or standards-compliant
RF simulator. See README.md for assumptions and interpretation.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import asdict, dataclass
from typing import Sequence


@dataclass(frozen=True)
class Config:
    duration_seconds: float = 60.0
    packet_interval_ms: float = 10.0
    payload_bytes: int = 5760
    phy_rate_mbps: float = 4.0
    link_efficiency: float = 0.75
    overhead_bytes: int = 32
    base_latency_ms: float = 1.0
    jitter_sigma_ms: float = 0.5
    loss_probability: float = 0.001
    max_retries: int = 2
    retry_backoff_ms: float = 1.0
    playout_buffer_ms: float = 40.0
    seed: int = 1


def percentile(values: Sequence[float], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[max(0, min(len(ordered) - 1, math.ceil(p * len(ordered)) - 1))]


def simulate(config: Config, payload_trace_bytes: Sequence[int] | None = None) -> dict:
    if config.duration_seconds <= 0 or config.packet_interval_ms <= 0:
        raise ValueError("duration and packet interval must be positive")
    if config.payload_bytes < 0 or config.overhead_bytes < 0:
        raise ValueError("payload and overhead sizes cannot be negative")
    if config.phy_rate_mbps <= 0 or not (0 < config.link_efficiency <= 1):
        raise ValueError("PHY rate must be positive and efficiency must be in (0, 1]")
    if not (0 <= config.loss_probability < 1):
        raise ValueError("loss probability must be in [0, 1)")
    if config.max_retries < 0 or config.retry_backoff_ms < 0:
        raise ValueError("retry count and backoff cannot be negative")
    if config.jitter_sigma_ms < 0 or config.base_latency_ms < 0 or config.playout_buffer_ms < 0:
        raise ValueError("latency, jitter and buffer cannot be negative")
    if payload_trace_bytes is not None and (
        not payload_trace_bytes or any(size < 0 for size in payload_trace_bytes)
    ):
        raise ValueError("payload trace must be non-empty and contain non-negative sizes")

    rng = random.Random(config.seed)
    packet_count = math.ceil(config.duration_seconds * 1000 / config.packet_interval_ms)
    tx_available_ms = 0.0
    arrivals: list[float] = []
    first_queue_delays: list[float] = []
    attempt_queue_delays: list[float] = []
    payload_sizes: list[int] = []
    on_time_bytes = 0
    misses = 0
    attempts_total = 0
    retries_total = 0
    generated_bytes = 0

    effective_rate_mbps = config.phy_rate_mbps * config.link_efficiency

    for i in range(packet_count):
        generated_ms = i * config.packet_interval_ms
        payload = (
            payload_trace_bytes[i % len(payload_trace_bytes)]
            if payload_trace_bytes is not None
            else config.payload_bytes
        )
        payload_sizes.append(payload)
        generated_bytes += payload
        arrival_ms: float | None = None

        for attempt in range(config.max_retries + 1):
            start_ms = max(generated_ms, tx_available_ms)
            attempt_queue_delays.append(start_ms - generated_ms)
            if attempt == 0:
                first_queue_delays.append(start_ms - generated_ms)
            wire_bytes = payload + config.overhead_bytes
            airtime_ms = (wire_bytes * 8) / (effective_rate_mbps * 1000)
            tx_available_ms = start_ms + airtime_ms
            attempts_total += 1

            if rng.random() >= config.loss_probability:
                propagation_ms = max(
                    0.0, rng.gauss(config.base_latency_ms, config.jitter_sigma_ms)
                )
                arrival_ms = tx_available_ms + propagation_ms
                break

            if attempt < config.max_retries:
                retries_total += 1
                tx_available_ms += config.retry_backoff_ms

        deadline_ms = generated_ms + config.playout_buffer_ms
        if arrival_ms is None or arrival_ms > deadline_ms:
            misses += 1
        else:
            on_time_bytes += payload
            arrivals.append(arrival_ms - generated_ms)

    duration_ms = packet_count * config.packet_interval_ms
    return {
        "model": "single-radio FIFO with immediate per-packet retry; packet-level only",
        "config": asdict(config),
        "payload_trace_bytes": list(payload_trace_bytes) if payload_trace_bytes is not None else None,
        "packets_generated": packet_count,
        "packets_missed_deadline": misses,
        "deadline_miss_rate": misses / packet_count if packet_count else 0.0,
        "generated_payload_bytes": generated_bytes,
        "on_time_payload_bytes": on_time_bytes,
        "source_payload_rate_mbps": generated_bytes * 8 / (duration_ms * 1000),
        "on_time_goodput_mbps": on_time_bytes * 8 / (duration_ms * 1000),
        "attempts_total": attempts_total,
        "retries_total": retries_total,
        "mean_queue_delay_ms": sum(first_queue_delays) / len(first_queue_delays) if first_queue_delays else 0.0,
        "p95_queue_delay_ms": percentile(first_queue_delays, 0.95),
        "mean_attempt_queue_delay_ms": sum(attempt_queue_delays) / len(attempt_queue_delays) if attempt_queue_delays else 0.0,
        "mean_on_time_latency_ms": sum(arrivals) / len(arrivals) if arrivals else None,
        "p95_on_time_latency_ms": percentile(arrivals, 0.95),
        "note": "A deadline miss means the packet was unavailable at its playout deadline; it is not a psychoacoustic audibility prediction.",
    }


def parse_trace(text: str | None) -> list[int] | None:
    if text is None:
        return None
    try:
        values = [int(part.strip()) for part in text.split(",") if part.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("trace must be comma-separated integer byte counts") from exc
    if not values:
        raise argparse.ArgumentTypeError("trace must contain at least one byte count")
    return values


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration-seconds", type=float, default=60.0)
    parser.add_argument("--packet-interval-ms", type=float, default=10.0)
    parser.add_argument("--payload-bytes", type=int, default=5760)
    parser.add_argument("--payload-trace-bytes", type=str, default=None,
                        help="comma-separated packet payload sizes; repeated cyclically")
    parser.add_argument("--phy-rate-mbps", type=float, default=4.0)
    parser.add_argument("--link-efficiency", type=float, default=0.75)
    parser.add_argument("--overhead-bytes", type=int, default=32)
    parser.add_argument("--base-latency-ms", type=float, default=1.0)
    parser.add_argument("--jitter-sigma-ms", type=float, default=0.5)
    parser.add_argument("--loss-probability", type=float, default=0.001)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--retry-backoff-ms", type=float, default=1.0)
    parser.add_argument("--playout-buffer-ms", type=float, default=40.0)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    config = Config(
        duration_seconds=args.duration_seconds,
        packet_interval_ms=args.packet_interval_ms,
        payload_bytes=args.payload_bytes,
        phy_rate_mbps=args.phy_rate_mbps,
        link_efficiency=args.link_efficiency,
        overhead_bytes=args.overhead_bytes,
        base_latency_ms=args.base_latency_ms,
        jitter_sigma_ms=args.jitter_sigma_ms,
        loss_probability=args.loss_probability,
        max_retries=args.max_retries,
        retry_backoff_ms=args.retry_backoff_ms,
        playout_buffer_ms=args.playout_buffer_ms,
        seed=args.seed,
    )
    trace = parse_trace(args.payload_trace_bytes)
    print(json.dumps(simulate(config, trace), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
