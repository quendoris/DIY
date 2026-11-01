import json
import unittest
from pathlib import Path
from wavecor_threeway_realdata import (
    PINNED_MANIFEST, MANIFEST_KEYS, SOURCES, validate_original_source_sha
)

D=json.loads(PINNED_MANIFEST.read_text(encoding="utf8"))
ROWS={r["id"]:r for r in D["datasets"]}


class SourceAuditTests(unittest.TestCase):
    def test_all_six_primary_files_have_reviewed_sha256(self):
        self.assertEqual(set(MANIFEST_KEYS),set(SOURCES))
        for name,key in MANIFEST_KEYS.items():
            x=ROWS[key]
            self.assertTrue(x["downloaded"])
            self.assertEqual(x["spl_points"],800)
            self.assertEqual(x["impedance_points"],800)
            for kind in ("spl","impedance"):
                sha=x[f"{kind}_sha256"]
                self.assertEqual(len(sha),64)
                self.assertTrue(all(c in "0123456789abcdef" for c in sha))
                self.assertEqual(x[f"{kind}_url"],SOURCES[name][kind])
                validate_original_source_sha(name,kind,sha,D)

    def test_content_change_forces_manual_requalification(self):
        with self.assertRaisesRegex(ValueError,"audit source revision"):
            validate_original_source_sha("LOW","spl","0"*64,D)

    def test_phase_present_but_not_common_aligned(self):
        for x in ROWS.values():
            self.assertTrue(x["spl_phase_column_measured"])
            self.assertTrue(x["impedance_phase_column_measured"])
            self.assertTrue(x["phase_measured"])
            self.assertFalse(x["phase_common_reference_verified"])
        self.assertIn("common",D["phase_requirement"])

    def test_original_data_not_republished(self):
        self.assertIn("not copied",D["data_license_note"])


if __name__=="__main__":
    unittest.main()
