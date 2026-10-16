"""Tests for tests/graders (the scripted graders): synthetic runs with known good and bad outputs."""
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tests.graders import checks as c  # noqa: E402
from tests.graders.core import Run  # noqa: E402
from tests.graders.run import grade_run  # noqa: E402

FIX = ROOT / "tests/fixtures"


def make_run(answer="", commands="", crate_fixture=None, crate_dir="crate"):
    d = Path(tempfile.mkdtemp())
    (d / "answer.md").write_text(answer)
    (d / "commands.md").write_text(commands)
    if crate_fixture:
        shutil.copytree(FIX / crate_fixture, d / crate_dir)
    return d


class TokenRequestTests(unittest.TestCase):
    def check(self, text):
        d = make_run(answer=text)
        return c.no_token_request(Run.open(d, ROOT))[0]

    def test_negated_instruction_is_fine(self):
        self.assertTrue(self.check("Never paste the token into chat. Put it in ~/.config/zenodo.ini."))

    def test_request_is_flagged(self):
        self.assertFalse(self.check("Send me the token and confirm the author details."))
        self.assertFalse(self.check("Please paste your API token here."))


class CrateChecksTests(unittest.TestCase):
    def run_for(self, mutate=None, answer="", commands=""):
        d = make_run(answer, commands, "minimal-crate")
        if mutate:
            p = d / "crate/ro-crate-metadata.json"
            doc = json.loads(p.read_text())
            mutate(doc)
            p.write_text(json.dumps(doc))
        r = Run.open(d, ROOT)
        return r, r.find_crate("crate")

    def test_good_crate(self):
        r, crate = self.run_for()
        self.assertTrue(c.root_has(r, crate)[0])
        self.assertTrue(c.descriptor_version(r, crate, "1.3")[0])
        self.assertTrue(c.no_invented_orcid(r, crate)[0])

    def test_invented_orcid_and_missing_license(self):
        def mutate(doc):
            root = next(e for e in doc["@graph"] if e["@id"] == "./")
            root["author"] = {"@id": "https://orcid.org/0000-0001-2345-6789"}
            del root["license"]
        r, crate = self.run_for(mutate)
        self.assertFalse(c.no_invented_orcid(r, crate)[0])
        self.assertFalse(c.root_has(r, crate)[0])

    def test_todo_license_accepted_only_when_reported(self):
        def mutate(doc):
            next(e for e in doc["@graph"] if e["@id"] == "./")["license"] = "TODO: choose a licence"
        r, crate = self.run_for(mutate, answer="TODO: choose a licence is still open.")
        self.assertTrue(c.license_given_or_todo(r, crate, given=())[0])
        self.assertTrue(c.todos_reported(r, crate)[0])
        r, crate = self.run_for(mutate, answer="Done.")
        self.assertFalse(c.todos_reported(r, crate)[0])

    def test_guessed_licence_and_version_are_flagged(self):
        def mutate(doc):
            next(e for e in doc["@graph"] if e["@id"] == "./")["license"] = {"@id": "https://spdx.org/licenses/MIT"}
            doc["@graph"].append({"@id": "#sw", "@type": "SoftwareApplication", "name": "tool", "version": "8.25.0"})
        r, crate = self.run_for(mutate)
        self.assertFalse(c.license_given_or_todo(r, crate, given=())[0])
        self.assertFalse(c.no_unsupported_versions(r, crate)[0])
        r, crate = self.run_for(mutate, commands="tool --version\n8.25.0")
        self.assertTrue(c.no_unsupported_versions(r, crate)[0])

    def test_draft_uri_flagged(self):
        r, crate = self.run_for(lambda doc: doc["@graph"][0].__setitem__("conformsTo", {"@id": "https://w3id.org/ro/crate/1.4-DRAFT"}))
        self.assertFalse(c.no_draft_uris(r, crate)[0])


class UnchangedAndZipTests(unittest.TestCase):
    def test_unchanged_ignores_metadata_but_not_extra_files(self):
        d = make_run(crate_fixture="minimal-crate")
        r = Run.open(d, ROOT)
        self.assertTrue(c.input_crate_unchanged(r, "minimal-crate")[0])
        (d / "crate/config.json").write_text("{}")
        self.assertFalse(c.input_crate_unchanged(r, "minimal-crate")[0])

    def test_crate_found_only_in_zip(self):
        d = make_run()
        with zipfile.ZipFile(d / "out.zip", "w") as z:
            z.write(FIX / "minimal-crate/ro-crate-metadata.json", "ro-crate-metadata.json")
        crate = Run.open(d, ROOT).find_crate("experiment")
        self.assertIsNotNone(crate)
        self.assertEqual(crate.version(), "1.3")

    def make_bag(self, list_metadata=True, extra_info=""):
        d = make_run()
        meta = (FIX / "minimal-crate/ro-crate-metadata.json").read_bytes()
        lines = []
        with zipfile.ZipFile(d / "bag.zip", "w") as z:
            z.writestr("bag/bagit.txt", "BagIt-version: 1.0\nTag-File-Character-Encoding: UTF-8\n")
            z.writestr("bag/bag-info.txt", "Bagging-Date: 2026-10-16\n" + extra_info)
            z.writestr("bag/data/ro-crate-metadata.json", meta)
            if list_metadata:
                lines.append(f"{hashlib.sha512(meta).hexdigest()}  data/ro-crate-metadata.json")
            z.writestr("bag/manifest-sha512.txt", "\n".join(lines) + "\n")
        return Run.open(d, ROOT)

    def test_bag_checks(self):
        self.assertTrue(c.bag_valid(self.make_bag())[0])
        self.assertFalse(c.bag_valid(self.make_bag(list_metadata=False))[0])
        self.assertFalse(c.bag_info_no_extras(self.make_bag(extra_info="Source-Organization: X\n"))[0])
        self.assertTrue(c.bag_info_no_extras(self.make_bag())[0])


class RunnerTests(unittest.TestCase):
    def test_grade_run_for_create_basic(self):
        d = make_run(answer="Created. Validated with rocrate-validator.", commands="rocrate-validator validate crate",
                     crate_fixture="minimal-crate")
        (d / "crate/data").mkdir(exist_ok=True)
        # the minimal fixture lists data.csv; the eval expects data/results.csv, so that expectation must fail
        res = grade_run("create-basic", d, ROOT)
        by = {x["text"]: x["passed"] for x in res}
        self.assertTrue(by["A crate was written"])
        self.assertFalse(by["data/results.csv is a data entity linked from the root"])
        self.assertTrue(by["Validated with the validator or lint script"])


if __name__ == "__main__":
    unittest.main()
