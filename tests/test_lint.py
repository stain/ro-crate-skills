"""Tests for skills/ro-crate-validator/scripts/lint_crate.py using the fixtures."""
import json, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINT = ROOT / "skills/ro-crate-validator/scripts/lint_crate.py"
FIX = ROOT / "tests/fixtures"


def run(target, *extra):
    p = subprocess.run([sys.executable, str(LINT), str(target), "--json", *extra], capture_output=True, text=True)
    return p.returncode, json.loads(p.stdout)


class LintTests(unittest.TestCase):
    def test_minimal_crate_passes(self):
        code, out = run(FIX / "minimal-crate")
        self.assertEqual((code, out["errors"], out["version"]), (0, 0, "1.3"))

    def test_invalid_crate_reports_required_properties_and_missing_file(self):
        code, out = run(FIX / "invalid-crate")
        msgs = " ".join(f["message"] for f in out["findings"])
        self.assertEqual(code, 1)
        for needle in ("lacks description", "lacks license", "lacks datePublished", "missing.txt"):
            self.assertIn(needle, msgs)

    def test_draft_uri_is_an_error(self):
        doc = json.loads((FIX / "minimal-crate/ro-crate-metadata.json").read_text())
        doc["@graph"][0]["conformsTo"] = {"@id": "https://w3id.org/ro/crate/1.4-DRAFT"}
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "ro-crate-metadata.json").write_text(json.dumps(doc))
            code, out = run(d)
        self.assertEqual(code, 1)
        self.assertTrue(any("DRAFT" in f["message"] for f in out["findings"]))

    def test_legacy_and_detached_fixtures(self):
        code, out = run(FIX / "crate-1.0")
        self.assertEqual((code, out["version"]), (0, "1.0"))
        self.assertTrue(any("legacy" in f["message"] for f in out["findings"]))
        code, out = run(FIX / "detached-crate")
        self.assertEqual((code, out["errors"]), (0, 0))

    def test_run_profile_and_injection_fixtures_are_structurally_valid(self):
        for name in ("process-run-crate", "profile-crate", "injection-crate", "crate-1.1"):
            with self.subTest(name):
                self.assertEqual(run(FIX / name)[0], 0)

    def test_todo_placeholder_is_warned(self):
        doc = json.loads((FIX / "minimal-crate/ro-crate-metadata.json").read_text())
        root = next(e for e in doc["@graph"] if e["@id"] == "./")
        root["license"] = "TODO: choose a licence"
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "ro-crate-metadata.json").write_text(json.dumps(doc))
            (Path(d) / "data.csv").write_text("a,b\n")
            code, out = run(d)
        self.assertEqual(code, 0)
        self.assertTrue(any("placeholder" in f["message"] and f["level"] == "WARN" for f in out["findings"]))


if __name__ == "__main__":
    unittest.main()
