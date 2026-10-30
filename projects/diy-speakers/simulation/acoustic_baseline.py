#!/usr/bin/env python3
"""First-order research bench for a near-field stereo 2.1 design.

Models only:
  (1) small-signal second-order SEALED-box LF response from Fs/Qts/Vas/Vb;
  (2) ideal fourth-order Linkwitz-Riley ELECTRICAL crossover.
No nonlinear excursion/SPL, ports, room modes, directivity or delay are modeled.
"""
from __future__ import annotations

import argparse
import cmath
import json
import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SealedBox:
    fs_hz: float
    qts: float
    vas_l: float
    net_volume_l: float

    def validate(self) -> None:
        if min(self.fs_hz, self.qts, self.vas_l, self.net_volume_l) <= 0:
            raise ValueError("Fs, Qts, Vas and net box volume must be positive")

    @property
    def compliance_ratio(self) -> float:
        self.validate()
        return 1 + self.vas_l / self.net_volume_l

    @property
    def fc_hz(self) -> float:
        return self.fs_hz * math.sqrt(self.compliance_ratio)

    @property
    def qtc(self) -> float:
        return self.qts * math.sqrt(self.compliance_ratio)

    def response(self, freq_hz: float) -> complex:
        """Sealed-box normalized high-pass transfer; ideal lumped-parameter model."""
        if freq_hz < 0:
            raise ValueError("Frequency cannot be negative")
        if freq_hz == 0:
            return 0j
        ratio = freq_hz / self.fc_hz
        s = 1j * ratio
        return (s * s) / (s * s + s / self.qtc + 1)

    def f3_hz(self) -> float:
        """Low-frequency -3 dB crossing relative to high-frequency unity gain."""
        target = 1 / math.sqrt(2)
        lo, hi = 0.0, 100 * self.fc_hz
        for _ in range(90):
            mid = (lo + hi) / 2
            if abs(self.response(mid)) < target:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2


def lr4(freq_hz: float, crossover_hz: float) -> tuple[complex, complex]:
    """Ideal, aligned LR4 electrical LP and HP complex transfer functions.

    These are each two cascaded 2nd-order Butterworth sections. A real driver,
    enclosure and acoustic delay do NOT generally have complementary LR4 curves.
    """
    if crossover_hz <= 0 or freq_hz < 0:
        raise ValueError("Crossover frequency must be >0, measurement frequency >=0")
    s = 1j * freq_hz / crossover_hz
    denom = s * s + math.sqrt(2) * s + 1
    low = 1 / (denom * denom)
    high = (s * s / denom) ** 2
    return low, high


def gain_db(value: complex) -> float | None:
    magnitude = abs(value)
    return 20 * math.log10(magnitude) if magnitude > 0 else None


def report(
    box: SealedBox,
    sub_crossover_hz: float = 80,
    sweep_hz: tuple[float, ...] = (20, 30, 40, 60, 80, 100, 160, 300),
) -> dict:
    box.validate()
    result = []
    for f in sweep_hz:
        lp, hp = lr4(f, sub_crossover_hz)
        result.append({
            "frequency_hz": f,
            "sealed_box_gain_db": gain_db(box.response(f)),
            "ideal_sub_electrical_gain_db": gain_db(lp),
            "ideal_satellite_electrical_gain_db": gain_db(hp),
            "ideal_aligned_sum_gain_db": gain_db(lp + hp),
        })
    return {
        "model": "small-signal sealed second-order + ideal aligned LR4 electrical split",
        "speaker_distance_m": {"min": 0.60, "max": 0.80},
        "reference": "ADAM T5V heard; ADAM T8V target comparison",
        "box": asdict(box),
        "sealed_fc_hz": box.fc_hz,
        "sealed_qtc": box.qtc,
        "sealed_f3_hz": box.f3_hz(),
        "sub_crossover_hz": sub_crossover_hz,
        "sweep": result,
        "caveats": [
            "Sealed model is small-signal free-field only, not a specific real driver",
            "Sample box Thiele-Small parameters are illustrative, not selected parts",
            "Electrical LR4 unity sum assumes identical acoustic arrival and ideal transducers",
            "Does not calculate SPL, Xmax, thermal load, distortion, room modes, desk bounce or diffraction",
            "Requires actual impedance, measured FRD/ZMA and driver positions before crossover freeze",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fs", type=float, default=42.0)
    parser.add_argument("--qts", type=float, default=0.38)
    parser.add_argument("--vas", type=float, default=18.0)
    parser.add_argument("--volume", type=float, default=12.0)
    parser.add_argument("--crossover", type=float, default=80.0)
    a = parser.parse_args()
    result = report(SealedBox(a.fs, a.qts, a.vas, a.volume), a.crossover)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
