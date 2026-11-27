"""Tests for the trigger-test harness (stream parsing, pass rules, prompt-set sanity). No model calls."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests/triggers"))
import run  # noqa: E402

STREAM = "\n".join(json.dumps(x) for x in [
    {"type": "system", "subtype": "init"},
    {"type": "assistant", "message": {"content": [{"type": "text", "text": "ok"},
        {"type": "tool_use", "name": "Skill", "input": {"skill": "ro-crate-skills:ro-crate-consume"}},
        {"type": "tool_use", "name": "Bash", "input": {"command": "ls"}}]}},
    {"type": "result", "subtype": "error_max_turns", "total_cost_usd": 0.05},
]) + "\nnot json\n"


class HarnessTests(unittest.TestCase):
    def test_parse_stream(self):
        self.assertEqual(run.parse_stream(STREAM), ("ro-crate-consume", "Skill", 0.05))
        self.assertEqual(run.parse_stream('{"type":"assistant","message":{"content":[{"type":"text","text":"hi"}]}}'),
                         (None, None, 0.0))

    def test_pass_rules(self):
        pos = {"kind": "positive", "accept": ["ro-crate-create", "ro-crate-py"]}
        neg = {"kind": "negative", "accept": []}
        self.assertTrue(run.passed(pos, "ro-crate-py"))
        self.assertFalse(run.passed(pos, "ro-crate-consume"))
        self.assertFalse(run.passed(pos, None))
        self.assertTrue(run.passed(neg, None))
        self.assertTrue(run.passed(neg, "dataviz"))
        self.assertFalse(run.passed(neg, "ro-crate-spec"))

    def test_prompt_set(self):
        items = json.loads((ROOT / "tests/triggers/triggers.json").read_text())
        skills = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(len({i["id"] for i in items}), len(items))
        for i in items:
            self.assertIn(i["split"], ("dev", "test"))
            if i["kind"] == "positive":
                self.assertIn(i["skill"], skills)
                self.assertTrue(set(i["accept"]) <= skills and i["skill"] in i["accept"], i["id"])
        for s in skills:  # every skill has dev and test positives
            splits = {i["split"] for i in items if i["skill"] == s}
            self.assertEqual(splits, {"dev", "test"}, s)


if __name__ == "__main__":
    unittest.main()
