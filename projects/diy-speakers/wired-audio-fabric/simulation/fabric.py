#!/usr/bin/env python3
"""Versioned, deterministic receiver contract simulator. Standard library only.

No physical optical/USB link, true cryptography, clock servo, actual PCM DAC,
speaker output or measured low-latency behavior is implemented.
"""
from __future__ import annotations

import json
import zlib
from dataclasses import dataclass, field


def pcm_payload_mbps(channels: int, sample_rate_hz: int, bits_per_sample: int) -> float:
    if min(channels, sample_rate_hz, bits_per_sample) <= 0:
        raise ValueError("channels/rate/bits must be positive")
    return channels * sample_rate_hz * bits_per_sample / 1_000_000


def nominal_clock_drift_samples(sample_rate_hz: int, relative_ppm: float, seconds: float) -> float:
    if sample_rate_hz <= 0 or seconds < 0:
        raise ValueError("invalid clock drift inputs")
    return sample_rate_hz * relative_ppm * 1e-6 * seconds


def ideal_mds_erasure_recovery(data_blocks: int, parity_blocks: int, erased_blocks: int) -> bool:
    """Ideal MDS erasure-only capacity bound, not an implemented FEC codec."""
    if data_blocks <= 0 or parity_blocks < 0 or erased_blocks < 0:
        raise ValueError("invalid code dimensions")
    if erased_blocks > data_blocks + parity_blocks:
        raise ValueError("cannot erase more blocks than transmitted")
    return erased_blocks <= parity_blocks


@dataclass(frozen=True)
class Block:
    session: str
    epoch: int
    seq: int
    payload: bytes
    crc32: int

    @classmethod
    def construct(cls, session: str, epoch: int, seq: int, payload: bytes) -> "Block":
        return cls(session=session, epoch=epoch, seq=seq, payload=payload,
                   crc32=zlib.crc32(payload))


@dataclass(frozen=True)
class Command:
    session: str
    epoch: int
    counter: int
    action: str
    verified_by_auth_oracle: bool


@dataclass
class Receiver:
    """Minimal state machine; one media stream, one logical DAC output group."""

    channels: int
    samples_per_block: int
    bytes_per_sample: int
    session: str | None = None
    epoch: int = 0
    last_command_counter: int = 0
    next_playout_seq: int = 0
    paused: bool = True
    blocks: dict[int, bytes] = field(default_factory=dict)
    underruns: int = 0

    def __post_init__(self) -> None:
        if min(self.channels, self.samples_per_block, self.bytes_per_sample) <= 0:
            raise ValueError("invalid sample format")

    def bind_session(self, session: str, verified_by_auth_oracle: bool) -> None:
        """Authentication boolean is test-harness input; NOT a cryptographic proof."""
        if not verified_by_auth_oracle or not session:
            raise PermissionError("unauthenticated session")
        self.session = session
        self.epoch = 0
        self.last_command_counter = 0
        self.next_playout_seq = 0
        self.paused = True
        self.blocks.clear()
        self.underruns = 0

    def push(self, block: Block) -> None:
        if self.session is None or block.session != self.session:
            raise PermissionError("wrong session")
        if block.epoch != self.epoch:
            raise ValueError("stale or future epoch")
        if block.seq < self.next_playout_seq:
            raise ValueError("late packet")
        if block.seq in self.blocks:
            raise ValueError("duplicate block")
        if len(block.payload) != (
            self.channels * self.samples_per_block * self.bytes_per_sample
        ):
            raise ValueError("wrong frame size")
        if zlib.crc32(block.payload) != block.crc32:
            raise ValueError("CRC32 mismatch")
        self.blocks[block.seq] = block.payload

    def command(self, command: Command) -> None:
        if (not command.verified_by_auth_oracle or self.session is None
                or command.session != self.session):
            raise PermissionError("unauthenticated command")
        if command.counter <= self.last_command_counter:
            raise ValueError("replayed or reordered command")
        if command.epoch != self.epoch:
            raise ValueError("stale or future command epoch")
        if command.action not in ("PLAY", "PAUSE", "STOP", "FLUSH"):
            raise ValueError("unknown action")
        self.last_command_counter = command.counter
        if command.action == "PLAY":
            self.paused = False
        elif command.action == "PAUSE":
            self.paused = True
        else:
            self.paused = True
            self.blocks.clear()
            self.epoch += 1
            self.next_playout_seq = 0

    def next_audio(self) -> bytes | None:
        """The caller represents a fixed physical playout block boundary."""
        if self.paused:
            return None
        payload = self.blocks.pop(self.next_playout_seq, None)
        self.next_playout_seq += 1
        if payload is None:
            self.underruns += 1
        return payload


def demo() -> dict:
    """Synthetic bytes exercise contract, not an actual audio waveform."""
    r = Receiver(channels=2, samples_per_block=128, bytes_per_sample=3)
    r.bind_session("controller-to-left", verified_by_auth_oracle=True)
    payload = bytes([i % 251 for i in range(128 * 2 * 3)])
    for seq in range(4):
        r.push(Block.construct("controller-to-left", 0, seq, payload))
    r.command(Command("controller-to-left", 0, 1, "PLAY", True))
    first = r.next_audio()
    r.command(Command("controller-to-left", 0, 2, "PAUSE", True))
    muted_on_pause = r.next_audio() is None
    remaining_during_pause = len(r.blocks)
    r.command(Command("controller-to-left", 0, 3, "PLAY", True))
    next_block = r.next_audio()
    r.command(Command("controller-to-left", 0, 4, "STOP", True))
    return {
        "purpose": "illustrative deterministic state-machine contract, not real measured timing",
        "five_channel_24bit_96khz_mbps": pcm_payload_mbps(5, 96000, 24),
        "relative_clock_drift_50ppm_60s_samples": nominal_clock_drift_samples(
            96000, 50, 60
        ),
        "block_period_ms_at_96khz": 128 * 1000 / 96000,
        "four_block_buffer_ms_at_96khz": 4 * 128 * 1000 / 96000,
        "first_block_bit_identical": first == payload,
        "buffered_audio_suppressed_on_pause": muted_on_pause,
        "buffered_blocks_retained_on_pause": remaining_during_pause,
        "resume_block_bit_identical": next_block == payload,
        "stop_cleared_buffer": len(r.blocks) == 0,
        "stop_incremented_epoch": r.epoch == 1,
        "actual_crypto_implemented": False,
        "actual_fiber_or_dac_implemented": False,
    }


if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=False, indent=2, sort_keys=True))
