import unittest

from packet_model import Config, simulate


class PacketModelTests(unittest.TestCase):
    def test_high_capacity_link_meets_deadlines(self):
        cfg = Config(
            duration_seconds=1,
            packet_interval_ms=10,
            payload_bytes=400,
            phy_rate_mbps=20,
            link_efficiency=0.9,
            overhead_bytes=24,
            base_latency_ms=1,
            jitter_sigma_ms=0,
            loss_probability=0,
            max_retries=0,
            playout_buffer_ms=40,
        )
        result = simulate(cfg)
        self.assertEqual(result["packets_missed_deadline"], 0)
        self.assertAlmostEqual(result["deadline_miss_rate"], 0.0)

    def test_insufficient_capacity_misses_deadlines(self):
        cfg = Config(
            duration_seconds=1,
            packet_interval_ms=10,
            payload_bytes=5760,
            phy_rate_mbps=4,
            link_efficiency=0.75,
            overhead_bytes=32,
            base_latency_ms=1,
            jitter_sigma_ms=0,
            loss_probability=0,
            max_retries=0,
            playout_buffer_ms=40,
        )
        result = simulate(cfg)
        self.assertGreater(result["packets_missed_deadline"], 0)
        self.assertGreater(result["mean_queue_delay_ms"], 0)

    def test_payload_trace_is_applied_cyclically(self):
        cfg = Config(
            duration_seconds=0.04,
            packet_interval_ms=10,
            phy_rate_mbps=100,
            link_efficiency=1,
            overhead_bytes=0,
            base_latency_ms=0,
            jitter_sigma_ms=0,
            loss_probability=0,
            max_retries=0,
            playout_buffer_ms=40,
        )
        result = simulate(cfg, [100, 200])
        self.assertEqual(result["generated_payload_bytes"], 600)
        self.assertEqual(result["packets_generated"], 4)

    def test_seed_makes_run_reproducible(self):
        cfg = Config(duration_seconds=1, loss_probability=0.2, seed=42)
        self.assertEqual(simulate(cfg), simulate(cfg))

    def test_trace_rejects_invalid_values(self):
        cfg = Config(duration_seconds=1)
        with self.assertRaises(ValueError):
            simulate(cfg, [])
        with self.assertRaises(ValueError):
            simulate(cfg, [100, -1])


if __name__ == "__main__":
    unittest.main()
