import unittest

from fabric import (Block, Command, Receiver, demo, ideal_mds_erasure_recovery,
                    nominal_clock_drift_samples, pcm_payload_mbps)


class FabricModelTests(unittest.TestCase):
    def setUp(self):
        self.r = Receiver(channels=2, samples_per_block=128, bytes_per_sample=3)
        self.r.bind_session("L", True)
        self.pcm = bytes([i % 251 for i in range(768)])

    def frame(self, seq=0, epoch=0, session="L"):
        return Block.construct(session, epoch, seq, self.pcm)

    def cmd(self, action="PLAY", counter=1, epoch=0, verified=True, session="L"):
        return Command(session, epoch, counter, action, verified)

    def test_five_channel_bandwidth(self):
        self.assertAlmostEqual(pcm_payload_mbps(5, 96000, 24), 11.52)
        self.assertAlmostEqual(pcm_payload_mbps(5, 192000, 24), 23.04)
        self.assertAlmostEqual(pcm_payload_mbps(5, 96000, 32), 15.36)

    def test_block_duration_and_drift(self):
        self.assertAlmostEqual(128 * 1000 / 96000, 4/3)
        self.assertAlmostEqual(nominal_clock_drift_samples(96000, 50, 60), 288)

    def test_exact_buffered_bytes(self):
        self.r.push(self.frame())
        self.r.command(self.cmd())
        self.assertEqual(self.r.next_audio(), self.pcm)

    def test_pause_preempts_full_buffer_and_keeps_remaining(self):
        for i in range(4):
            self.r.push(self.frame(i))
        self.r.command(self.cmd("PLAY", 1))
        self.assertEqual(self.r.next_audio(), self.pcm)
        self.r.command(self.cmd("PAUSE", 2))
        self.assertIsNone(self.r.next_audio())
        self.assertEqual(self.r.next_playout_seq, 1)
        self.assertEqual(len(self.r.blocks), 3)
        self.r.command(self.cmd("PLAY", 3))
        self.assertEqual(self.r.next_audio(), self.pcm)

    def test_reject_unauthenticated_session(self):
        r = Receiver(1, 128, 3)
        with self.assertRaises(PermissionError):
            r.bind_session("X", False)

    def test_reject_unauthenticated_command(self):
        with self.assertRaises(PermissionError):
            self.r.command(self.cmd(verified=False))
        self.assertTrue(self.r.paused)

    def test_reject_command_replay(self):
        self.r.command(self.cmd("PLAY", 1))
        with self.assertRaises(ValueError):
            self.r.command(self.cmd("PAUSE", 1))
        self.assertFalse(self.r.paused)

    def test_reject_wrong_session_and_stale_epoch(self):
        with self.assertRaises(PermissionError):
            self.r.push(self.frame(session="R"))
        with self.assertRaises(ValueError):
            self.r.push(self.frame(epoch=2))

    def test_reject_crc_corruption(self):
        corrupted = Block("L", 0, 0, self.pcm[:-1] + b"x", self.frame().crc32)
        with self.assertRaises(ValueError):
            self.r.push(corrupted)

    def test_reject_duplicate_and_late_blocks(self):
        self.r.push(self.frame())
        with self.assertRaises(ValueError):
            self.r.push(self.frame())
        self.r.command(self.cmd("PLAY", 1))
        self.r.next_audio()
        with self.assertRaises(ValueError):
            self.r.push(self.frame())

    def test_reject_wrong_block_size(self):
        with self.assertRaises(ValueError):
            self.r.push(Block.construct("L", 0, 0, b"short"))

    def test_stop_invalidates_old_buffer_epoch(self):
        self.r.push(self.frame())
        self.r.command(self.cmd("STOP", 1))
        self.assertTrue(self.r.paused)
        self.assertEqual(self.r.blocks, {})
        self.assertEqual(self.r.epoch, 1)
        with self.assertRaises(ValueError):
            self.r.push(self.frame())
        with self.assertRaises(ValueError):
            self.r.command(self.cmd("PLAY", 2, epoch=0))
        self.r.push(self.frame(epoch=1))
        self.r.command(self.cmd("PLAY", 2, epoch=1))
        self.assertEqual(self.r.next_audio(), self.pcm)

    def test_underrun_does_not_play_unverified_data(self):
        self.r.command(self.cmd("PLAY", 1))
        self.assertIsNone(self.r.next_audio())
        self.assertEqual(self.r.underruns, 1)
        with self.assertRaises(ValueError):
            self.r.push(self.frame(0))

    def test_ideal_fec_parity_is_not_magic(self):
        self.assertTrue(ideal_mds_erasure_recovery(4, 4, 4))
        self.assertFalse(ideal_mds_erasure_recovery(4, 4, 5))
        self.assertFalse(ideal_mds_erasure_recovery(4, 2, 3))

    def test_demo_reports_scoped_limitations(self):
        d = demo()
        self.assertTrue(d["first_block_bit_identical"])
        self.assertTrue(d["buffered_audio_suppressed_on_pause"])
        self.assertTrue(d["resume_block_bit_identical"])
        self.assertTrue(d["stop_incremented_epoch"])
        self.assertFalse(d["actual_crypto_implemented"])
        self.assertFalse(d["actual_fiber_or_dac_implemented"])


if __name__ == "__main__":
    unittest.main()
