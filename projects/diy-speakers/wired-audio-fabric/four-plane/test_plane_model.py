import unittest
from dataclasses import replace

from plane_model import (
    DeterministicScheduler, EndpointTelemetry, Plane, aggregate, assess_endpoint,
    demo, fiber_propagation_difference_ns, oscillator_drift_samples,
)


def healthy(name="left"):
    return EndpointTelemetry(
        name=name, received_ms=1000, identity_authenticated=True,
        firmware_measurement_accepted=True, rail_ok=True,
        amplifier_ok=True, clock_locked=True, available_buffer_ms=80,
    )


class PlaneModelTests(unittest.TestCase):
    def test_healthy_three_endpoints_only_qualified_ready(self):
        result = aggregate([healthy("left"), healthy("right"), healthy("sub")], 1050)
        self.assertEqual(result["state"], "READY")

    def test_expired_heartbeat_is_unknown(self):
        self.assertEqual(assess_endpoint(healthy(), 1400)["state"], "UNKNOWN")

    def test_missing_attestation_blocks_ready(self):
        h = replace(healthy(), identity_authenticated=False)
        self.assertEqual(assess_endpoint(h, 1050)["state"], "UNKNOWN")

    def test_rejected_firmware_measurement_blocks_ready(self):
        h = replace(healthy(), firmware_measurement_accepted=False)
        self.assertEqual(assess_endpoint(h, 1050)["state"], "UNKNOWN")

    def test_power_fault_overrides_nominal_heartbeat(self):
        h = replace(healthy(), rail_ok=False, local_hardware_trip=True)
        self.assertEqual(assess_endpoint(h, 1050)["state"], "FAULT")

    def test_local_fault_has_priority_over_unknown_stale(self):
        h = replace(healthy(), received_ms=0, local_hardware_trip=True)
        self.assertEqual(assess_endpoint(h, 1000)["state"], "FAULT")

    def test_clock_unlock_forces_muted(self):
        h = replace(healthy(), clock_locked=False)
        self.assertEqual(assess_endpoint(h, 1050)["state"], "MUTED")

    def test_low_buffer_is_degraded_not_ready(self):
        h = replace(healthy(), available_buffer_ms=9)
        self.assertEqual(assess_endpoint(h, 1050)["state"], "DEGRADED")

    def test_fan_absence_only_fault_if_fan_is_required(self):
        no_fan = replace(healthy(), fan_ok=False, fan_required=False)
        self.assertEqual(assess_endpoint(no_fan, 1050)["state"], "READY")
        required = replace(healthy(), fan_ok=False, fan_required=True)
        self.assertEqual(assess_endpoint(required, 1050)["state"], "DEGRADED")

    def test_aggregate_fault_surfaces_sub_endpoint(self):
        reports = [healthy("left"), healthy("right"),
                   replace(healthy("sub"), amplifier_ok=False)]
        self.assertEqual(aggregate(reports, 1050)["state"], "FAULT")

    def test_priority_preemption_before_audio(self):
        sched = DeterministicScheduler()
        sched.push(Plane.AUDIO, "media")
        sched.push(Plane.ATTESTATION_HEALTH, "health")
        sched.push(Plane.CONTROL, "pause")
        sched.push(Plane.TIME, "time")
        sched.push(Plane.SAFETY_LOCAL, "trip")
        self.assertEqual([sched.pop().label for _ in range(5)],
                         ["trip", "time", "pause", "health", "media"])

    def test_equal_priority_is_fifo(self):
        sched = DeterministicScheduler()
        sched.push(Plane.AUDIO, "one")
        sched.push(Plane.AUDIO, "two")
        self.assertEqual([sched.pop().label, sched.pop().label], ["one", "two"])

    def test_fiber_length_is_nonzero_not_impossible(self):
        self.assertAlmostEqual(fiber_propagation_difference_ns(5), 25.0)
        self.assertAlmostEqual(fiber_propagation_difference_ns(0), 0.0)

    def test_free_running_oscillators_drift(self):
        self.assertAlmostEqual(oscillator_drift_samples(96000, 50, 1), 4.8)

    def test_empty_report_cannot_say_ready(self):
        self.assertEqual(aggregate([], 1000)["state"], "UNKNOWN")

    def test_no_crypto_or_phy_claims(self):
        d = demo()
        self.assertFalse(d["cryptography_implemented"])
        self.assertFalse(d["physical_clock_sync_implemented"])
        self.assertFalse(d["measured_bounds"])
        self.assertEqual(d["sub_power_fault"]["state"], "FAULT")


if __name__ == "__main__":
    unittest.main()
