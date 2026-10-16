"""Helpers: load a run directory, find and parse a crate, simple text checks. Standard library only."""
import hashlib
import json
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

# The fictional example ORCID used in the repository (Josiah Carberry); any other ORCID
# found in a produced crate is treated as invented unless the eval allows it.
EXAMPLE_ORCIDS = {"0000-0002-1825-0097"}
ORCID_RE = re.compile(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]")
TODO_RE = re.compile(r"^\s*TODO\b", re.I)


def aslist(v):
    return v if isinstance(v, list) else ([] if v is None else [v])


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


@dataclass
class Crate:
    """A parsed ro-crate-metadata.json: a plain JSON graph plus lookups, no RO-Crate library."""
    root_dir: Path
    path: Path
    doc: dict
    graph: list = field(default_factory=list)
    emap: dict = field(default_factory=dict)
    descriptor: dict | None = None
    root: dict | None = None
    text: str = ""

    @classmethod
    def load(cls, metadata_path, text=None):
        """Load from a file, or from `text` (e.g. read out of a zip) with metadata_path naming where it came from."""
        p = Path(metadata_path)
        text = read(p) if text is None else text
        doc = json.loads(text)
        graph = doc.get("@graph", []) if isinstance(doc, dict) else []
        emap = {e["@id"]: e for e in graph if isinstance(e, dict) and isinstance(e.get("@id"), str)}
        desc = emap.get("ro-crate-metadata.json") or emap.get("ro-crate-metadata.jsonld")
        root = None
        if desc and isinstance(desc.get("about"), dict):
            root = emap.get(desc["about"].get("@id"))
        return cls(p.parent, p, doc, graph, emap, desc, root, text)

    def conforms_to(self, entity=None):
        e = entity if entity is not None else self.descriptor
        return [x.get("@id") for x in aslist((e or {}).get("conformsTo")) if isinstance(x, dict)]

    def version(self):
        for c in self.conforms_to():
            m = re.match(r"https://w3id\.org/ro/crate/(\d+\.\d+)$", c or "")
            if m:
                return m.group(1)
        return None

    def types(self, e):
        return set(aslist(e.get("@type")))

    def all_strings(self):
        def walk(v):
            if isinstance(v, str):
                yield v
            elif isinstance(v, list):
                for x in v:
                    yield from walk(x)
            elif isinstance(v, dict):
                for x in v.values():
                    yield from walk(x)
        yield from walk(self.graph)


@dataclass
class Run:
    """One run's outputs directory with answer, commands and any crates the agent wrote."""
    outputs: Path
    repo: Path
    answer: str = ""
    commands: str = ""

    @classmethod
    def open(cls, outputs, repo):
        o = Path(outputs)
        return cls(o, Path(repo), read(o / "answer.md"), read(o / "commands.md"))

    def find_crate(self, hint=None):
        """Locate the crate: hint is a subdirectory (relative to outputs) or None for the shallowest match."""
        if hint and hint.startswith("zip:"):
            return self._crate_from_zip(hint[4:])
        roots = [self.outputs / hint] if hint else [self.outputs]
        cands = []
        for r in roots:
            for pat in ("ro-crate-metadata.json", "*ro-crate-metadata.json", "ro-crate-metadata.jsonld"):
                cands += [p for p in r.rglob(pat) if "node_modules" not in p.parts and "sfbin" not in p.parts]
        if not cands:
            return self._crate_from_zip(hint)
        cands.sort(key=lambda p: (len(p.parts), str(p)))
        try:
            return Crate.load(cands[0])
        except ValueError:
            return None

    def _crate_from_zip(self, hint=None):
        """A crate that only exists inside a zip written by the agent (metadata at the zip root or in one folder)."""
        zips = [self.outputs / hint] if hint and (self.outputs / hint).suffix == ".zip" else sorted(self.outputs.rglob("*.zip"))
        for z in zips:
            try:
                with zipfile.ZipFile(z) as zf:
                    names = zf.namelist()
                    meta = [n for n in names if re.fullmatch(r"([^/]+/)?(data/)?ro-crate-metadata\.json", n)]
                    if meta:
                        return Crate.load(z, text=zf.read(sorted(meta, key=len)[0]).decode("utf-8", "replace"))
            except (OSError, zipfile.BadZipFile, ValueError):
                continue
        return None


# --- generic result type ------------------------------------------------------------------
def ok(evidence=""):
    return True, evidence


def fail(evidence=""):
    return False, evidence


# --- text checks ----------------------------------------------------------------------------
def mentions(text, *patterns, all_=True):
    hits = [bool(re.search(p, text, re.I | re.S)) for p in patterns]
    good = all(hits) if all_ else any(hits)
    return (good, f"patterns {patterns} -> {hits}")


def not_mentions(text, *patterns):
    hits = [p for p in patterns if re.search(p, text, re.I | re.S)]
    return (not hits, f"unexpected matches: {hits}" if hits else "none of the unwanted patterns present")


def file_sha(path, algo="sha512"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_digest(directory, ignore=()):
    """Digest of relative paths and contents of a directory, to check that an input crate was not modified."""
    h = hashlib.sha256()
    d = Path(directory)
    for p in sorted(x for x in d.rglob("*") if x.is_file() and not any(i in x.parts for i in ignore)):
        h.update(str(p.relative_to(d)).encode())
        h.update(file_sha(p, "sha256").encode())
    return h.hexdigest()


def zip_members(path):
    try:
        with zipfile.ZipFile(path) as z:
            return z.namelist()
    except (OSError, zipfile.BadZipFile):
        return None
