import math
import unittest
from optical_bench_contract import (
  CHANNELS, PcmConfig, ethernet_wire_fraction, matrix, optical_serialization_budget,
  payload_bps, propagation_ns, udp_payload_bytes, zero_failure_upper_bound
)


class OpticalLabContractTests(unittest.TestCase):
    def test_three_plus_three_plus_one(self):
        self.assertEqual(CHANNELS,{"left":3,"right":3,"sub":1})
        self.assertEqual(sum(CHANNELS.values()),7)

    def test_channel_rates_96k_24bit(self):
        self.assertEqual(payload_bps(96000,24,7),16_128_000)
        self.assertEqual(payload_bps(96000,24,3),6_912_000)
        self.assertEqual(payload_bps(96000,24,1),2_304_000)

    def test_channel_rates_192k_32bit(self):
        self.assertEqual(payload_bps(192000,32,7),43_008_000)
        self.assertEqual(payload_bps(192000,32,3),18_432_000)

    def test_packet_128_samples_96k_24bit(self):
        cfg=PcmConfig(96000,24)
        self.assertEqual(udp_payload_bytes(cfg,3),1152)
        self.assertLessEqual(udp_payload_bytes(cfg,3)+28,1472)
        self.assertAlmostEqual(cfg.samples_per_block/cfg.hz*1000,4/3)

    def test_packet_128_samples_192k_32bit_exceeds_mtu(self):
        cfg=PcmConfig(192000,32)
        self.assertEqual(udp_payload_bytes(cfg,3),1536)
        with self.assertRaises(ValueError):
            ethernet_wire_fraction(udp_payload_bytes(cfg,3))
        shorter=PcmConfig(192000,32,120)
        self.assertEqual(udp_payload_bytes(shorter,3),1440)
        self.assertLessEqual(udp_payload_bytes(shorter,3)+28,1472)

    def test_nominal_manchester_vs_high_rate(self):
        full=optical_serialization_budget(PcmConfig(192000,24),7,50_000_000,.5)
        self.assertFalse(full["fits_before_framing"])
        one_sat=optical_serialization_budget(PcmConfig(192000,24),3,50_000_000,.5)
        self.assertTrue(one_sat["fits_before_framing"])

    def test_toshiba_15mbps_cannot_carry_seven_96k24(self):
        self.assertFalse(optical_serialization_budget(
            PcmConfig(96000,24),7,15_000_000,1)["fits_before_framing"])

    def test_silica_propagation_only_assumption(self):
        self.assertEqual([propagation_ns(x) for x in (1,2,5)],[5,10,25])
        self.assertEqual(propagation_ns(5)-propagation_ns(1),20)

    def test_packet_failure_bound_95pct(self):
        v=zero_failure_upper_bound(1_000_000)
        self.assertAlmostEqual(v,2.995732e-6,delta=1e-10)
        self.assertGreater(zero_failure_upper_bound(10),v)

    def test_max_packet_goodput_fraction_is_below_one(self):
        v=ethernet_wire_fraction(1152)
        self.assertGreater(v,.90)
        self.assertLess(v,1.)

    def test_no_fake_test_claims(self):
        rep=matrix()
        self.assertEqual(rep["physical_build_status"],"NOT TESTED")
        self.assertIn("not measured",rep["scope"])
        self.assertEqual(rep["audio_formats"][0]["seven_output_pcm_mbps"],16.128)
        self.assertFalse(rep["audio_formats"][-1]["fits_default_ipv4_udp_mtu_with_28b_header"]["left"])

    def test_invalid_input_rejected(self):
        with self.assertRaises(ValueError): PcmConfig(96000,23).validate()
        with self.assertRaises(ValueError): propagation_ns(-1)
        with self.assertRaises(ValueError): zero_failure_upper_bound(0)
        with self.assertRaises(ValueError): ethernet_wire_fraction(0)


if __name__ == "__main__":
    unittest.main()
