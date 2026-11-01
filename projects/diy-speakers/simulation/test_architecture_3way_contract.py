"""Architectural contract checks for the user-selected active 3-way + sub.

This audit checks stored topology and stated limits, not the correctness of
electrical hardware, converter clocks, encryption, acoustics or safety.
"""
import json
import unittest
from pathlib import Path

SPEC = json.loads(Path(__file__).with_name("architecture_3way_contract.json").read_text(encoding="utf-8"))


class OwnerArchitectureDecisionTests(unittest.TestCase):
    def test_two_stereo_sources_and_seven_independent_outputs(self):
        self.assertEqual(SPEC["source_program_channels"], 2)
        satellite = [x for x in SPEC["speaker_units"] if x["role"] == "active_satellite"]
        sub = [x for x in SPEC["speaker_units"] if x["role"] == "active_subwoofer"]
        self.assertEqual(len(satellite), 2)
        self.assertEqual({x["id"] for x in satellite}, {"left", "right"})
        self.assertEqual(len(sub), 1)
        self.assertEqual(sum(x["dac_output_channels"] for x in SPEC["speaker_units"]), 7)
        self.assertEqual(sum(x["amplifier_output_channels"] for x in SPEC["speaker_units"]), 7)
        self.assertEqual(SPEC["output_channels_required"], 7)

    def test_three_acoustic_bands_and_isolated_mids_per_satellite(self):
        for x in SPEC["speaker_units"]:
            if x["role"] == "active_satellite":
                self.assertEqual(x["acoustic_bands"], ["low", "mid", "high"])
                self.assertTrue(x["midrange_independent_rear_volume"])
                self.assertEqual(x["dac_output_channels"], len(x["acoustic_bands"]))
            else:
                self.assertEqual(x["acoustic_bands"], ["low_sub"])

    def test_independent_power_and_local_clock_domains(self):
        units = SPEC["speaker_units"]
        self.assertEqual(len({x["power_domain"] for x in units}), 3)
        self.assertEqual(len({x["local_audio_clock_domain"] for x in units}), 3)
        self.assertTrue(SPEC["timing"]["common_playout_epoch_required"])
        self.assertEqual(SPEC["timing"]["inter_device_sample_alignment"], "NOT_TESTED")
        self.assertFalse(SPEC["timing"]["fiber_length_invariant_without_calibration"])

    def test_four_logical_planes_without_magic_security_claim(self):
        planes = {x["id"]:x for x in SPEC["audio_planes"]}
        self.assertEqual(set(planes), {"health_trust", "command", "media", "clock_sync"})
        for k in ("health_trust", "command", "clock_sync"):
            self.assertTrue(planes[k]["independent_from_media_buffer"])
        self.assertFalse(SPEC["digital_analog"]["command_authentication_implemented"])
        self.assertIn("CRC not MAC", SPEC["digital_analog"]["media_integrity_policy"])

    def test_per_driver_dac_channels_are_not_per_driver_dac_chips(self):
        self.assertTrue(SPEC["digital_analog"]["per_driver_conversion_channel_required"])
        self.assertFalse(SPEC["digital_analog"]["per_driver_discrete_dac_IC_required"])

    def test_raw_digital_payload_rate(self):
        channels = SPEC["output_channels_required"]
        self.assertEqual(channels*96000*24/1_000_000, 16.128)
        self.assertEqual(channels*192000*24/1_000_000, 32.256)

    def test_owner_has_one_fixed_architecture_without_forced_budget_upgrade(self):
        self.assertEqual(SPEC["decision_status"], "owner_selected_topology_frozen")
        self.assertEqual(SPEC["mechanical"]["finished_aesthetic_enclosure"], "LAST")
        self.assertFalse(SPEC["mechanical"]["driver_models_selected"])
        self.assertIn("two-way+sub is an alternative target topology", SPEC["prohibited_inferences"])

    def test_open_build_requirements_and_certification_limits(self):
        openness = SPEC["openness"]
        self.assertTrue(openness["public_complete_source_release_goal"])
        self.assertEqual(openness["licensing_status"], "TBD")
        self.assertEqual(openness["official_safety_certification_current_status"], "NOT_TESTED")
        self.assertIn("PCB_schematics_layouts", openness["planned_releasable_artifacts"])
        self.assertIn("raw_measurements_and_unit_tests", openness["planned_releasable_artifacts"])
        self.assertTrue(SPEC["digital_analog"]["protection_hardware_independent_from_network"])

    def test_initial_crossovers_remain_unfrozen(self):
        for key, bounds in SPEC["candidate_crossovers_hz"].items():
            if key != "note":
                lo, hi = bounds
                self.assertGreater(hi, lo)
        self.assertIn("NOT predetermined", SPEC["candidate_crossovers_hz"]["note"])


if __name__ == "__main__":
    unittest.main()
