"""Tests for skills/ro-crate-action-recorder/scripts/link_actions.py."""
import json, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills/ro-crate-action-recorder/scripts/link_actions.py"

CRATE = {"@context": "https://w3id.org/ro/crate/1.3/context", "@graph": [
    {"@id": "ro-crate-metadata.json", "@type": "CreativeWork", "about": {"@id": "./"},
     "conformsTo": {"@id": "https://w3id.org/ro/crate/1.3"}},
    {"@id": "./", "@type": "Dataset", "name": "n", "description": "d", "datePublished": "2025-01-01",
     "license": "x", "hasPart": [{"@id": "a.txt"}]},
    {"@id": "a.txt", "@type": "File"},
    {"@id": "tool@1", "@type": "SoftwareApplication", "name": "tool"},
    {"@id": "tool a.txt", "@type": "CreateAction", "instrument": {"@id": "tool@1"}, "object": {"@id": "a.txt"}},
]}


def run(d, *extra):
    return subprocess.run([sys.executable, str(SCRIPT), d, *extra], capture_output=True, text=True)


class LinkActionsTests(unittest.TestCase):
    def test_mentions_added_and_no_invented_url(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ro-crate-metadata.json"
            p.write_text(json.dumps(CRATE))
            out = run(d)
            doc = json.loads(p.read_text())
            root = next(e for e in doc["@graph"] if e["@id"] == "./")
            self.assertEqual(root["mentions"], [{"@id": "tool a.txt"}])
            self.assertIn("no url", out.stdout)
            self.assertFalse(any("url" in e for e in doc["@graph"] if e["@id"] == "tool@1"))

    def test_url_only_when_given_and_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ro-crate-metadata.json"
            p.write_text(json.dumps(CRATE))
            run(d, "--software-url", "tool@1=https://example.org/tool")
            run(d)
            doc = json.loads(p.read_text())
            root = next(e for e in doc["@graph"] if e["@id"] == "./")
            self.assertEqual(len(root["mentions"]), 1)
            self.assertEqual(next(e for e in doc["@graph"] if e["@id"] == "tool@1")["url"], "https://example.org/tool")


if __name__ == "__main__":
    unittest.main()
