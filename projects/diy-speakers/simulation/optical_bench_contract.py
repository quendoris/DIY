#!/usr/bin/env python3
"""Reproducible optical-bench sizing & reporting contract.

Physical optics, latency, source authenticity, cryptography and clock sync
are NOT simulated or certified. Rates are idealized estimates with explicit
assumptions, not measured throughput.
"""
from __future__ import annotations
import json
import math
from dataclasses import dataclass, asdict

CHANNELS = {"left":3,"right":3,"sub":1}
LAYERS = ("attestation_health", "control", "audio", "time_sync")
FIBER_LENGTHS_M = (1,2,5)

@dataclass(frozen=True)
class PcmConfig:
    hz: int
    bits: int
    samples_per_block: int = 128
    def validate(self) -> None:
        if self.hz <= 0 or self.bits <= 0 or self.bits % 8 or self.samples_per_block <= 0:
            raise ValueError("invalid PCM/block parameters")

def payload_bps(hz: int, bits: int, channels: int) -> int:
    if min(hz, bits, channels) <= 0:
        raise ValueError("invalid PCM")
    return hz * bits * channels

def udp_payload_bytes(cfg: PcmConfig, channels: int) -> int:
    cfg.validate()
    if channels <= 0:
        raise ValueError("invalid channel count")
    return cfg.samples_per_block * channels * (cfg.bits // 8)

def ethernet_wire_fraction(application_payload_bytes: int, extra_protocol_header_bytes: int = 28) -> float:
    """IPv4/UDP/Ethernet no VLAN, no IP fragmentation, one packet.

    8 preamble+SFD + 12 IFG + 14 Ethernet header + 4 FCS
    + 20 IPv4 + 8 UDP + custom 28-byte protocol header.
    For realistic traffic use a separate accounting for ARQ, redundant
    frames, PTP, acknowledgments and retransmissions.
    """
    if application_payload_bytes <= 0 or extra_protocol_header_bytes < 0:
        raise ValueError("invalid packet")
    if application_payload_bytes + extra_protocol_header_bytes > 1472:
        raise ValueError("packet needs fragmentation or smaller block with standard IPv4 MTU 1500")
    # 66 bytes total standard link/ip overhead, plus custom application header
    total=application_payload_bytes + 66 + extra_protocol_header_bytes
    return application_payload_bytes / total

def optical_serialization_budget(cfg: PcmConfig, channels: int, available_line_bps: int, line_code_efficiency: float) -> dict:
    if available_line_bps <= 0 or not 0 < line_code_efficiency <= 1:
        raise ValueError("invalid physical link budget")
    bps = payload_bps(cfg.hz,cfg.bits,channels)
    available = available_line_bps*line_code_efficiency
    return {
        "required_pcm_mbps": round(bps/1_000_000,6),
        "available_max_payload_mbps_before_framing": round(available/1_000_000,6),
        "fits_before_framing": bps <= available,
        "reserve_fraction_before_framing": round((available-bps)/available,6),
    }

def propagation_ns(length_m: float, assumed_light_speed_m_s: float=2e8) -> float:
    if length_m < 0 or assumed_light_speed_m_s <= 0:
        raise ValueError("invalid optical speed/distance")
    return 1e9*length_m/assumed_light_speed_m_s

def zero_failure_upper_bound(failure_free_count: int, confidence: float=0.95) -> float:
    """One-sided exact Bernoulli upper bound if zero independent failures observed.

    Nonstationary burst errors violate the iid assumption. This bounds
    *packet* failure probability if count is packets; not physical BER.
    """
    if failure_free_count <= 0 or not 0 < confidence < 1:
        raise ValueError("invalid confidence test")
    return -math.expm1(math.log1p(-confidence)/failure_free_count)

def matrix() -> dict:
    rows=[]
    for hz,bits in ((96000,24),(192000,24),(192000,32)):
        cfg=PcmConfig(hz,bits)
        sizes={name:udp_payload_bytes(cfg,count) for name,count in CHANNELS.items()}
        packetized={name:ethernet_wire_fraction(size) if size + 28 <= 1472 else None
                    for name,size in sizes.items()}
        rows.append({
            "rate_hz":hz,"bits_per_sample":bits,
            "seven_output_pcm_mbps":round(payload_bps(hz,bits,7)/1e6,6),
            "per_unit_pcm_mbps":{k:round(payload_bps(hz,bits,v)/1e6,6)
                                for k,v in CHANNELS.items()},
            "pcm_128_sample_packet_bytes":sizes,
            "fits_default_ipv4_udp_mtu_with_28b_header":
                {k:(v+28<=1472) for k,v in sizes.items()},
            "wire_goodput_fraction_if_1packet_per_block":packetized,
            "packet_period_ms":round(cfg.samples_per_block/hz*1000,6),
            "per_satellite_50ms_buffer_bytes":int(3*hz*(bits//8)*.05),
        })
    return {
      "scope":"model estimates only; PHY/USB/clock performance not measured",
      "board_expected":"NUCLEO-H7S3L8 STM32H7S3L8H6 (marketplace typo must be checked)",
      "physical_build_status":"NOT TESTED",
      "fiber_lengths_m":list(FIBER_LENGTHS_M),
      "optical_propagation_ns_silica_assumption":
         {str(m):propagation_ns(m) for m in FIBER_LENGTHS_M},
      "silica_one_to_five_m_delta_ns":propagation_ns(5)-propagation_ns(1),
      "audio_formats":rows,
      "subsystem_names":list(LAYERS),
      "fiber_eth_max_nominal_mbps":100,
      "fiber_eth_udp_gross_budget_note":"100Mbit/s line and approximate MAC overhead only; application goodput must be measured",
      "broadcom_50Mbaud_8b10b_line_example":optical_serialization_budget(PcmConfig(192000,24),7,50_000_000,.8),
      "toshiba_15Mbps_nrzi_full_system_example":optical_serialization_budget(PcmConfig(96000,24),7,15_000_000,1),
      "one_million_error_free_packets_95pct_failure_probability_upper_bound":
         zero_failure_upper_bound(1_000_000,.95),
      "limits":[
          "A packet loss bound is not raw optical BER",
          "A network RTT cannot resolve 5ns per meter fiber propagation",
          "No statistical independence or stationary error rate established in the lab",
          "No IEEE 1588 or synchronized independent receiver clocks proven",
          "No guaranteed priorities inferred from four logical queues",
          "No acoustic DAC, link device or mains electrical certification",
      ]
    }

if __name__=="__main__":
    print(json.dumps(matrix(),indent=2,ensure_ascii=False,sort_keys=True))
