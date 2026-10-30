#!/usr/bin/env python3
"""Logical N-host/M-monitor routing. No actual HDMI, DP, USB4 or RF simulation."""
from __future__ import annotations
from dataclasses import dataclass, replace
from itertools import permutations
import argparse
import json


@dataclass(frozen=True)
class Host:
    id: str
    max_displays: int


@dataclass(frozen=True)
class Uplink:
    id: str
    host: str
    kind: str
    streams: int
    payload_gbps: float


@dataclass(frozen=True)
class Monitor:
    id: str
    payload_gbps: float


@dataclass(frozen=True)
class Scenario:
    hosts: tuple[Host, ...]
    uplinks: tuple[Uplink, ...]
    monitors: tuple[Monitor, ...]
    assignments: dict[str, str]


def assess(s: Scenario) -> dict:
    """Backtrack a distinct upstream video stream for each assigned monitor."""
    hosts = {h.id: h for h in s.hosts}
    monitors = {m.id: m for m in s.monitors}
    if len(hosts) != len(s.hosts) or len(monitors) != len(s.monitors):
        raise ValueError("duplicate host or monitor ID")
    if len({u.id for u in s.uplinks}) != len(s.uplinks):
        raise ValueError("duplicate uplink ID")
    if any(u.host not in hosts or u.streams < 0 or u.payload_gbps < 0 for u in s.uplinks):
        raise ValueError("invalid uplink")
    if any(h.max_displays < 0 for h in s.hosts) or any(m.payload_gbps < 0 for m in s.monitors):
        raise ValueError("negative capacity or demand")
    if any(m not in monitors or h not in hosts for m, h in s.assignments.items()):
        raise ValueError("unknown host or monitor")

    for host in s.hosts:
        requested = sum(h == host.id for h in s.assignments.values())
        if requested > host.max_displays:
            return {"feasible": False, "reason": "host_display_limit",
                    "host": host.id, "requested": requested, "maximum": host.max_displays}

    remaining = sorted(s.assignments, key=lambda m: (-monitors[m].payload_gbps, m))
    count = {u.id: 0 for u in s.uplinks}
    bandwidth = {u.id: 0.0 for u in s.uplinks}
    routes = {}

    def search(i: int) -> bool:
        if i == len(remaining):
            return True
        m = remaining[i]
        for u in sorted(s.uplinks, key=lambda u: u.id):
            if u.host != s.assignments[m] or count[u.id] >= u.streams:
                continue
            if bandwidth[u.id] + monitors[m].payload_gbps > u.payload_gbps + 1e-9:
                continue
            count[u.id] += 1
            bandwidth[u.id] += monitors[m].payload_gbps
            routes[m] = u.id
            if search(i + 1):
                return True
            count[u.id] -= 1
            bandwidth[u.id] -= monitors[m].payload_gbps
            del routes[m]
        return False

    if not search(0):
        return {"feasible": False, "reason": "uplink_stream_or_payload_capacity"}
    return {
        "feasible": True,
        "routes": {m: {"host": s.assignments[m], "uplink": routes[m],
                       "active_picture_gbps": monitors[m].payload_gbps}
                   for m in sorted(routes)},
        "uplinks": {u.id: {"streams_used": count[u.id], "stream_limit": u.streams,
                           "demand_gbps": round(bandwidth[u.id], 6),
                           "budget_gbps": u.payload_gbps}
                    for u in s.uplinks},
        "warning": "Logical resource allocation only; budgets are input assumptions. "
                   "No PHY, MST protocol, DSC, EDID, HDCP, or USB4 negotiation modeled."
    }


def demo() -> Scenario:
    """3 computers/4 screens: a laptop DP-MST uplink + two desktop HDMI links.
    Example capacity numbers are hypothetical effective budgets, NOT certified PHY speeds.
    """
    return Scenario(
        hosts=(Host("laptop", 2), Host("desktop", 3), Host("backup", 1)),
        uplinks=(
            Uplink("laptop_dp_mst", "laptop", "DP_MST_CANDIDATE", 2, 15.0),
            Uplink("desktop_hdmi_a", "desktop", "HDMI_SST", 1, 8.0),
            Uplink("desktop_hdmi_b", "desktop", "HDMI_SST", 1, 8.0),
            Uplink("backup_hdmi", "backup", "HDMI_SST", 1, 8.0),
        ),
        monitors=(Monitor("M1", 5.308416), Monitor("M2", 5.308416),
                  Monitor("M3", 2.985984), Monitor("M4", 2.985984)),
        assignments={"M1": "laptop", "M2": "laptop",
                     "M3": "desktop", "M4": "desktop"},
    )


def square_matrix(n: int) -> dict:
    """Exhaustively enumerate purely logical one-to-one assignments."""
    if not 1 <= n <= 7:
        raise ValueError("n must be 1..7")
    hosts = tuple(Host(f"H{i}", 1) for i in range(n))
    links = tuple(Uplink(f"U{i}", f"H{i}", "HDMI_SST", 1, 2.0) for i in range(n))
    displays = tuple(Monitor(f"M{i}", 1.0) for i in range(n))
    count = sum(assess(Scenario(hosts, links, displays,
                 {f"M{i}": f"H{order[i]}" for i in range(n)}))["feasible"]
                for order in permutations(range(n)))
    return {"matrix": f"{n}x{n}", "permutation_count": count,
            "scope": "Logical one-to-one assignments; no crossbar PCB modeled"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--square", type=int, default=None)
    args = parser.parse_args()
    print(json.dumps(square_matrix(args.square) if args.square else assess(demo()),
                     ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
