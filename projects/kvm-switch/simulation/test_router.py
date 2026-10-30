import unittest
from dataclasses import replace
from router import Uplink, assess, demo, square_matrix


class RouterTests(unittest.TestCase):
    def test_square_2_3_5(self):
        self.assertEqual([square_matrix(n)["permutation_count"] for n in (2, 3, 5)],
                         [2, 6, 120])

    def test_three_hosts_four_displays(self):
        result = assess(demo())
        self.assertTrue(result["feasible"], result)
        self.assertEqual(result["routes"]["M1"]["host"], "laptop")
        self.assertEqual(result["routes"]["M2"]["host"], "laptop")
        self.assertEqual(result["uplinks"]["laptop_dp_mst"]["streams_used"], 2)

    def test_single_hdmi_not_two_independent_monitors(self):
        s = demo()
        single = Uplink("laptop_hdmi", "laptop", "HDMI_SST", 1, 100.0)
        s = replace(s, uplinks=(single,) + tuple(
            u for u in s.uplinks if u.host != "laptop"))
        self.assertEqual(assess(s)["reason"], "uplink_stream_or_payload_capacity")

    def test_mst_link_must_have_sufficient_capacity(self):
        s = demo()
        s = replace(s, uplinks=tuple(
            replace(u, payload_gbps=8.0) if u.id == "laptop_dp_mst" else u
            for u in s.uplinks))
        self.assertFalse(assess(s)["feasible"])

    def test_host_display_count(self):
        s = demo()
        s = replace(s, hosts=tuple(
            replace(h, max_displays=1) if h.id == "laptop" else h
            for h in s.hosts))
        self.assertEqual(assess(s)["reason"], "host_display_limit")

    def test_reassign_to_third_computer(self):
        s = demo()
        s = replace(s, assignments={**s.assignments, "M4": "backup"})
        self.assertEqual(assess(s)["routes"]["M4"]["host"], "backup")

    def test_invalid_host_rejected(self):
        s = demo()
        with self.assertRaises(ValueError):
            assess(replace(s, assignments={"M1": "unknown"}))


if __name__ == "__main__":
    unittest.main()
