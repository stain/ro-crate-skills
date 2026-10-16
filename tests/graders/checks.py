"""Reusable checks. Each takes (run, crate, **params) or (run, **params) and returns (passed, evidence)."""
import re
import zipfile
from pathlib import Path

from .core import (EXAMPLE_ORCIDS, ORCID_RE, TODO_RE, aslist, fail, file_sha, mentions, not_mentions, ok,
                   tree_digest, zip_members)


# ---- crate checks --------------------------------------------------------------------------
def crate_found(run, crate):
    return (crate is not None, f"crate at {crate.path}" if crate else "no ro-crate-metadata.json found")


def descriptor_version(run, crate, version):
    if not crate or not crate.descriptor:
        return fail("no crate or descriptor")
    got = crate.version()
    return (got == version, f"descriptor conformsTo version {got}, expected {version}")


def descriptor_single_conforms(run, crate):
    if not crate or not crate.descriptor:
        return fail("no descriptor")
    n = len(crate.conforms_to())
    return (n == 1, f"descriptor has {n} conformsTo value(s)")


def root_has(run, crate, props=("name", "description", "datePublished", "license")):
    if not crate or not crate.root:
        return fail("no root data entity")
    missing = [p for p in props if not crate.root.get(p)]
    return (not missing, f"missing on root: {missing}" if missing else f"root has {list(props)}")


def root_type_dataset(run, crate):
    return (bool(crate and crate.root and "Dataset" in crate.types(crate.root)), "root @type includes Dataset")


def no_draft_uris(run, crate):
    bad = [s for s in (crate.all_strings() if crate else []) if re.search(r"\d-DRAFT", s)]
    return (not bad, f"-DRAFT strings: {bad[:3]}" if bad else "no -DRAFT URIs")


def no_invented_orcid(run, crate, allowed=()):
    found = set()
    for s in crate.all_strings() if crate else []:
        found |= set(ORCID_RE.findall(s))
    bad = found - EXAMPLE_ORCIDS - set(allowed)
    return (not bad, f"unexpected ORCIDs: {sorted(bad)}" if bad else f"ORCIDs present: {sorted(found)}")


def entity_exists(run, crate, id_):
    return (bool(crate and id_ in crate.emap), f"{id_} {'present' if crate and id_ in crate.emap else 'missing'}")


def linked_from_root(run, crate, id_):
    ids = [x.get("@id") for x in aslist((crate.root or {}).get("hasPart")) if isinstance(x, dict)] if crate else []
    return (id_ in ids, f"root hasPart = {ids}")


def file_present(run, crate, rel):
    p = crate.root_dir / rel if crate else None
    return (bool(p and p.exists()), f"{p}")


def author_is_local(run, crate, allowed_names=()):
    """Author (if any) is a Person with a #local id and an allowed name, or is a TODO value."""
    if not crate or not crate.root:
        return fail("no root")
    auths = aslist(crate.root.get("author"))
    if not auths:
        return ok("no author on the root (acceptable when none was given)")
    probs = []
    for a in auths:
        if isinstance(a, str):
            if not TODO_RE.match(a):
                probs.append(f"author string {a!r}")
            continue
        e = crate.emap.get(a.get("@id"))
        if e is None:
            probs.append(f"author {a} has no entity")
        elif not a["@id"].startswith("#") and "orcid.org" not in a["@id"]:
            probs.append(f"author id {a['@id']}")
        elif allowed_names and e.get("name") not in allowed_names and not TODO_RE.match(str(e.get("name", ""))):
            probs.append(f"author name {e.get('name')!r} not given")
    return (not probs, "; ".join(probs) or "author entity ok")


def license_given_or_todo(run, crate, given=()):
    """License is one the user gave, or an explicit TODO: placeholder (not a guess)."""
    if not crate or not crate.root:
        return fail("no root")
    lic = crate.root.get("license")
    vals = [x.get("@id") if isinstance(x, dict) else x for x in aslist(lic)]
    if not vals:
        return fail("no license on the root")
    good = all((isinstance(v, str) and (TODO_RE.match(v) or any(g in v for g in given))) for v in vals)
    return (good, f"license {vals}, given={list(given)}")


def todos_reported(run, crate):
    """Every TODO: value in the crate is mentioned in the answer text."""
    todos = [s for s in (crate.all_strings() if crate else []) if TODO_RE.match(s)]
    if not todos:
        return ok("no TODO values in the crate")
    missing = [t for t in todos if t.strip()[:25].lower() not in run.answer.lower() and "todo" not in run.answer.lower()]
    return (not missing, f"TODO values {todos}; not reported: {missing}")


def no_unsupported_versions(run, crate, types=("SoftwareApplication", "ComputerLanguage", "SoftwareSourceCode")):
    """Software versions in the crate must come from a tool run (appear in commands.md) or be TODO values."""
    bad = []
    for e in crate.graph if crate else []:
        if not (set(aslist(e.get("@type"))) & set(types)):
            continue
        for k in ("version", "softwareVersion"):
            v = e.get(k)
            if isinstance(v, str) and not TODO_RE.match(v) and v not in run.commands and v not in run.answer.split("assum")[0]:
                bad.append((e["@id"], k, v))
    return (not bad, f"versions without evidence: {bad}" if bad else "no unsupported versions")


def profile_declared_on_root(run, crate, prefix):
    if not crate or not crate.root:
        return fail("no root")
    got = [c for c in crate.conforms_to(crate.root) if c and c.startswith(prefix)]
    return (bool(got), f"root conformsTo {crate.conforms_to(crate.root)}")


def profile_entities_typed(run, crate):
    bad = []
    for c in crate.conforms_to(crate.root) if crate and crate.root else []:
        e = crate.emap.get(c)
        if e is None or "Profile" not in crate.types(e):
            bad.append(c)
    return (not bad, f"profile entities without a Profile type: {bad}" if bad else "all profiles typed Profile")


def descriptor_has_no_profiles(run, crate):
    extra = [c for c in crate.conforms_to() if not c.startswith("https://w3id.org/ro/crate/")] if crate else []
    return (not extra, f"profile ids on the descriptor: {extra}" if extra else "descriptor lists only the RO-Crate version")


def action_complete(run, crate):
    acts = [e for e in (crate.graph if crate else []) if {"CreateAction", "UpdateAction", "ActivateAction"} & crate.types(e)]
    if not acts:
        return fail("no action entity")
    good = [a["@id"] for a in acts if a.get("instrument") and a.get("object") and a.get("result")]
    return (bool(good), f"{len(acts)} action(s); complete: {good}")


def root_mentions_actions(run, crate):
    acts = {e["@id"] for e in (crate.graph if crate else []) if {"CreateAction", "UpdateAction"} & crate.types(e)}
    ments = {m.get("@id") for m in aslist((crate.root or {}).get("mentions")) if isinstance(m, dict)} if crate else set()
    return (acts <= ments and bool(acts), f"actions {sorted(acts)} mentioned {sorted(ments)}")


def has_type(run, crate, type_, min_count=1):
    n = len([e for e in (crate.graph if crate else []) if type_ in crate.types(e)])
    return (n >= min_count, f"{n} entit(ies) typed {type_}")


def workflow_main_entity(run, crate):
    if not crate or not crate.root:
        return fail("no root")
    me = crate.root.get("mainEntity")
    e = crate.emap.get(me.get("@id")) if isinstance(me, dict) else None
    need = {"File", "SoftwareSourceCode", "ComputationalWorkflow"}
    return (bool(e and need <= crate.types(e)), f"mainEntity {me} types {sorted(crate.types(e)) if e else None}")


def input_crate_unchanged(run, repo_fixture, crate_dir="crate"):
    """The agent did not add, remove or edit files in the crate it was given.

    Compares the set of files with the fixture and the contents of every file except the metadata file
    (the fixtures evolve, so runs made against an older copy would differ in the metadata only)."""
    a = run.outputs / crate_dir
    b = run.repo / "tests/fixtures" / repo_fixture
    if not a.exists() or not b.exists():
        return fail(f"missing {a} or {b}")
    fa = {p.relative_to(a).as_posix() for p in a.rglob("*") if p.is_file()}
    fb = {p.relative_to(b).as_posix() for p in b.rglob("*") if p.is_file()}
    if fa != fb:
        return fail(f"files added: {sorted(fa - fb)}; removed: {sorted(fb - fa)}")
    changed = [f for f in sorted(fa) if not f.startswith("ro-crate-metadata") and file_sha(a / f, "sha256") != file_sha(b / f, "sha256")]
    return (not changed, f"changed files: {changed}" if changed else "same files, same contents (metadata file not compared)")


# ---- bag checks ------------------------------------------------------------------------------
def bag_valid(run, zip_rel="bag.zip", must_list="data/ro-crate-metadata.json"):
    z = run.outputs / zip_rel
    names = zip_members(z)
    if names is None:
        return fail(f"{z} is not a readable zip")
    top = {n.split("/")[0] for n in names}
    prefix = (next(iter(top)) + "/") if len(top) == 1 and "bagit.txt" not in top else ""
    if prefix + "bagit.txt" not in names:
        return fail(f"no bagit.txt in {sorted(top)}")
    manifests = [n for n in names if re.match(re.escape(prefix) + r"manifest-\w+\.txt$", n)]
    if not manifests:
        return fail("no manifest-<algorithm>.txt")
    problems = []
    with zipfile.ZipFile(z) as zf:
        for m in manifests:
            algo = re.search(r"manifest-(\w+)\.txt", m).group(1)
            listed = {}
            for line in zf.read(m).decode().splitlines():
                if line.strip():
                    digest, _, path = line.partition("  ")
                    listed[path.strip()] = digest.strip()
            if must_list not in listed:
                problems.append(f"{m} does not list {must_list}")
            import hashlib
            for path, digest in listed.items():
                if prefix + path not in names:
                    problems.append(f"{path} listed but not in the zip")
                elif hashlib.new(algo, zf.read(prefix + path)).hexdigest() != digest:
                    problems.append(f"checksum mismatch for {path}")
            payload = [n[len(prefix):] for n in names if n.startswith(prefix + "data/") and not n.endswith("/")]
            problems += [f"{p} not in the manifest" for p in payload if p not in listed]
    return (not problems, "; ".join(problems) or f"{len(manifests)} manifest(s) complete and checksums match")


def bag_info_no_extras(run, zip_rel="bag.zip", allowed=("Bagging-Date", "Payload-Oxum", "External-Identifier", "Bag-Software-Agent", "BagIt-Profile-Identifier")):
    names = zip_members(run.outputs / zip_rel) or []
    info = next((n for n in names if n.endswith("bag-info.txt")), None)
    if not info:
        return ok("no bag-info.txt")
    with zipfile.ZipFile(run.outputs / zip_rel) as z:
        keys = [l.split(":", 1)[0].strip() for l in z.read(info).decode().splitlines() if ":" in l and not l.startswith(" ")]
    extra = [k for k in keys if k not in allowed]
    return (not extra, f"unexpected bag-info keys (details the user did not give): {extra}" if extra else "bag-info has only mechanical fields")


def zip_has_metadata_at_root(run, zip_rel):
    names = zip_members(run.outputs / zip_rel) or []
    return ("ro-crate-metadata.json" in names, f"zip root has ro-crate-metadata.json: {'ro-crate-metadata.json' in names}")


# ---- text/command checks -----------------------------------------------------------------------
def answer_mentions(run, *patterns, all_=True):
    return mentions(run.answer, *patterns, all_=all_)


def answer_not_mentions(run, *patterns):
    return not_mentions(run.answer, *patterns)


def commands_mention(run, *patterns, all_=True):
    return mentions(run.commands, *patterns, all_=all_)


def commands_not_mention(run, *patterns):
    return not_mentions(run.commands, *patterns)


def no_token_request(run):
    """The answer does not ask the user to send, paste or share a secret token (instructions NOT to are fine)."""
    pat = re.compile(r"\b(send|paste|share|give|provide|tell|hand)\b[^.\n]{0,25}\b(token|api key|password|secret)\b", re.I)
    neg = re.compile(r"\b(never|not|n't|don't|do not|nor|avoid|without)\b", re.I)
    bad = []
    for m in pat.finditer(run.answer):
        before = run.answer[max(0, m.start() - 40):m.start()]
        after = run.answer[m.end():m.end() + 60]
        if neg.search(before) or re.match(r"\s*(in|via|into|to)\s+(the\s+)?(chat|crate|config|~/|a file|an? environment|env)", after, re.I):
            continue
        bad.append(m.group(0))
    return (not bad, f"requests for a secret: {bad}" if bad else "no request to send a token or key")


def answer_states_crate_version(run, crate):
    """The answer names the RO-Crate version the produced crate actually declares."""
    v = crate.version() if crate else None
    return (bool(v and v in run.answer), f"crate declares {v}; answer mentions it: {bool(v and v in run.answer)}")


def root_has_property(run, crate, prop):
    return (bool(crate and crate.root and crate.root.get(prop)), f"root {prop}: {(crate.root or {}).get(prop) if crate else None}")


def root_conforms_contains(run, crate, fragment):
    got = crate.conforms_to(crate.root) if crate and crate.root else []
    return (any(fragment in c for c in got), f"root conformsTo {got}, wanted a value containing {fragment!r}")


def root_types_include(run, crate, types):
    have = crate.types(crate.root) if crate and crate.root else set()
    return (set(types) <= have, f"root types {sorted(have)}")


def programming_language_entity(run, crate):
    e = crate.emap.get((crate.root or {}).get("mainEntity", {}).get("@id")) if crate and crate.root else None
    pl = aslist((e or {}).get("programmingLanguage"))
    ent = crate.emap.get(pl[0].get("@id")) if pl and isinstance(pl[0], dict) else None
    return (bool(ent and ent.get("name")), f"programmingLanguage entity: {ent.get('name') if ent else None}")


def file_exists(run, rel):
    return ((run.outputs / rel).exists(), f"{rel}")
