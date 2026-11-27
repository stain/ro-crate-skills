#!/usr/bin/env python3
"""Convert the rules of an RO-Crate MASP profile crate to a rocrate-validator SHACL profile.

Usage: masp_to_shacl.py <masp-crate/ro-crate-metadata.json> <out-dir> [--token NAME]
                        [--version X.Y] [--base 1.3] [--context ro-crate-context.jsonld]

Writes <out-dir>/<token>/<version>/profile.ttl and must/0_masp_rules.ttl, a profile folder for
  rocrate-validator validate --extra-profiles-path <out-dir> -p <token>-<version> <crate>
The profile declares prof:isProfileOf the RO-Crate version (--base, default from the MASP root's
isProfileOf), so rocrate-validator runs the RO-Crate checks first; its rule that finds the root
(the descriptor's about) types it as RootDataEntity, which the root's shapes target.

Mapping: class rule -> sh:NodeShape (sh:targetClass, or a SPARQL target when it needs several
types); property rule -> property shape (sh:path from prov:specializationOf, else rdfs:label via
the --context file or the crate's own @context; sh:minCount/sh:maxCount); rangeIncludes -> sh:or of
sh:class (class rules), datatypes/node kinds (Text, Number, Boolean, Date, URL), sh:hasValue
(PropertyValue literal or @id), sh:pattern + sh:flags (PropertyValue /regex/flags) and sh:in
(ItemList); class-rule counts -> SPARQL constraints on the root. The descriptor's own rules are
left to the RO-Crate profile. Every entity of a class is checked (as wpsld does), which is
stricter than masp-validate (see the skill). Prints what it could not convert. Standard library only.
"""
import json
import os
import re
import sys

SH = "http://www.w3.org/ns/shacl#"
XSD = "http://www.w3.org/2001/XMLSchema#"
SCHEMA = "http://schema.org/"
SCHEMA_ROLE = "http://www.w3.org/ns/dx/prof/role/schema"
INDICATORS_ROLE = "https://w3id.org/ro/conformance-indicators"
ROOT_CLASSES = {"1.2": ["https://github.com/crs4/rocrate-validator/profiles/ro-crate-1.2/RootDataEntity"],
                "1.3": ["https://github.com/crs4/rocrate-validator/profiles/ro-crate-1.2/RootDataEntity",
                        "https://github.com/crs4/rocrate-validator/profiles/ro-crate-1.3/RootDataEntity"]}
# rocrate-validator's 1.3 profile reuses the 1.2 checks, so both must be listed (as Workflow Run Crate 0.6 does)
TRANSITIVE = {"1.3": ["1.3", "1.2"], "1.2": ["1.2"]}
PREFIXES = {"schema": SCHEMA, "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#", "xsd": XSD, "sh": SH,
            "dct": "http://purl.org/dc/terms/", "prov": "http://www.w3.org/ns/prov#",
            "prof": "http://www.w3.org/ns/dx/prof/", "pcdm": "http://pcdm.org/models#",
            "bioschemas": "https://bioschemas.org/terms/"}
NUMBERS = ("integer", "decimal", "double", "float", "long", "int")


def ids(value):
    values = value if isinstance(value, list) else [value]
    return [v["@id"] if isinstance(v, dict) else v for v in values if v not in (None, "", [])]


def first(value):
    for v in value if isinstance(value, list) else [value]:
        v = v.get("@value", v.get("@id")) if isinstance(v, dict) else v
        if v not in (None, ""):
            return str(v)
    return None


def as_int(value):
    try:
        return int(first(value))
    except (TypeError, ValueError):
        return None


def iri(t):
    return "<" + t.replace(">", "%3E").replace(" ", "%20") + ">"


def lit(s):
    return '"""' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"""'


class Context:
    def __init__(self, *contexts):
        self.terms = dict(PREFIXES)
        self.vocab = SCHEMA
        for c in contexts:
            for part in c if isinstance(c, list) else [c]:
                if isinstance(part, dict):
                    for k, v in part.items():
                        if k == "@vocab":
                            self.vocab = v
                        elif not k.startswith("@"):
                            v = v.get("@id") if isinstance(v, dict) else v
                            if isinstance(v, str):
                                self.terms[k] = v

    def expand(self, term, vocab=True):
        if term is None:
            return None
        term = term.replace("https://schema.org/", SCHEMA)
        if term in self.terms and term not in PREFIXES:
            return self.expand(self.terms[term]) if ":" in self.terms[term] else self.terms[term]
        if ":" in term:
            prefix, rest = term.split(":", 1)
            if rest.startswith("//"):
                return term
            if prefix in self.terms:
                return self.terms[prefix] + rest
            return None
        return self.vocab + term if vocab else None


def range_kind(r, ctx):
    """A constraint for a datatype-like range, or None."""
    name = r.split("/")[-1].split("#")[-1].split(":")[-1]
    if name in ("Text", "string", "CssSelectorType", "XPathType", "PronounceableText"):
        return "[ sh:nodeKind sh:Literal ]"
    if name in ("Number", "Integer", "Float", "Quantity", "decimal", "double", "integer"):
        return "[ sh:or ( " + " ".join(f"[ sh:datatype xsd:{t} ]" for t in NUMBERS) + " ) ]"
    if name in ("Boolean", "boolean"):
        return "[ sh:datatype xsd:boolean ]"
    if name in ("Date", "DateTime", "Time", "date", "dateTime"):
        return "[ sh:nodeKind sh:Literal ]"
    if name in ("URL", "anyURI"):
        return "[ sh:nodeKind sh:IRIOrLiteral ]"
    return None


def main(argv):
    opts = {"--token": None, "--version": None, "--base": None, "--context": None}
    args = []
    it = iter(argv)
    for a in it:
        if a in opts:
            opts[a] = next(it, None)
        else:
            args.append(a)
    if len(args) != 2:
        sys.exit(__doc__)
    doc = json.load(open(args[0], encoding="utf-8"))
    extra = json.load(open(opts["--context"], encoding="utf-8")).get("@context", {}) if opts["--context"] else {}
    ctx = Context(extra, doc.get("@context"))
    nodes = {n["@id"]: n for n in doc["@graph"] if isinstance(n, dict) and "@id" in n}
    root_id = first(nodes["ro-crate-metadata.json"].get("about"))
    root = nodes[root_id]
    schema = [nodes.get(r, {}) for r in ids(root.get("hasResource")) if SCHEMA_ROLE in ids(nodes.get(r, {}).get("hasRole"))]
    rules = [nodes[r] for s in schema for r in ids(s.get("hasPart")) if r in nodes]
    if not rules:
        sys.exit("No MASP rules: no schema ResourceDescriptor with hasPart in the root's hasResource")
    classes = {n["@id"]: n for n in rules if "rdfs:Class" in ids(n.get("@type"))}
    alternatives = []
    props = [n for n in rules if "rdf:Property" in ids(n.get("@type"))]
    notes = []

    # The descriptor rule (rdfs:label "@id" = ro-crate-metadata.json) and the root rule it is about
    descriptor_rule, root_rules = None, set()
    for p in props:
        if first(p.get("rdfs:label")) == "@id":
            for r in ids(p.get("rangeIncludes")):
                if first(nodes.get(r, {}).get("value")) == "ro-crate-metadata.json":
                    descriptor_rule = (ids(p.get("domainIncludes")) or [None])[0]
    for p in props:
        if descriptor_rule in ids(p.get("domainIncludes")) and (first(p.get("rdfs:label")) or first(p.get("name"))) == "about":
            root_rules.update(r for r in ids(p.get("rangeIncludes")) if r in classes)

    def class_types(cid):
        c = classes[cid]
        types = [ctx.expand(t) for t in ids(c.get("prov:specializationOf"))] or [ctx.expand(cid, vocab=False)]
        if None in types:
            notes.append(f"{cid}: cannot expand its types {ids(c.get('prov:specializationOf')) or cid}; left out")
            return []
        return types

    base = opts["--base"] or next((b.rsplit("/", 1)[-1] for b in ids(root.get("isProfileOf")) if "w3id.org/ro/crate/" in b), "1.3")
    root_classes = ROOT_CLASSES.get(base, ROOT_CLASSES["1.3"])
    token = opts["--token"] or re.sub(r"[^a-z0-9]+", "-", (first(root.get("name")) or "masp-profile").lower()).strip("-")
    indicators = [e for r in ids(root.get("hasResource")) if INDICATORS_ROLE in ids(nodes.get(r, {}).get("hasRole"))
                  for a in ids(nodes[r].get("hasArtifact")) for e in ids(nodes.get(a, {}).get("itemListElement"))]
    # the IRI crates name in conformsTo: a conformance indicator, else the root's absolute @id
    profile_iri = (indicators + ([root_id] if re.match(r"^[a-z][a-z0-9+.-]*:", root_id) else []) + [f"urn:masp:{token}"])[0]
    # rocrate-validator requires the folder's version to match a version in the profile IRI
    iri_version = re.search(r"/(\d+(?:\.\d+)+)/?(?:#.*)?$", profile_iri)
    version = opts["--version"] or (iri_version.group(1) if iri_version else ".".join((first(root.get("version")) or "0.1").split(".")[:2]))
    ns = f"urn:masp-shacl:{token}:"

    out = ["@prefix sh: <http://www.w3.org/ns/shacl#> .", "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
           "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .", "",
           f"# Generated by masp_to_shacl.py from {args[0]} ({first(root.get('name'))} {first(root.get('version')) or ''})", ""]
    counts = []
    for cid, c in classes.items():
        if cid == descriptor_rule:
            continue
        label = first(c.get("name")) or first(c.get("rdfs:label")) or cid
        types = class_types(cid)
        if not types:
            continue
        lo, hi = as_int(c.get("sh:minCount")), as_int(c.get("sh:maxCount"))
        if cid not in root_rules and (lo or hi is not None):
            counts.append((label, types, lo, hi))
        shapes, id_filters = [], []
        for p in props:
            if cid not in ids(p.get("domainIncludes")):
                continue
            plabel = first(p.get("rdfs:label")) or first(p.get("name"))
            if plabel == "@id":  # MASP selects entities by name: becomes part of the target
                for r in ids(p.get("rangeIncludes")):
                    v = first(nodes.get(r, {}).get("value"))
                    m = re.match(r"^/\^?(.*?)\$?/([a-z]*)$", v or "", re.S)
                    last = 'REPLACE(STR(?this), "^.*/([^/]+)/?$", "$1")'
                    if m:  # matched against the last path segment, as the IRI is absolute once parsed
                        flags = "".join(f for f in m.group(2) if f in "imsx")
                        id_filters.append(f"REGEX({last}, {json.dumps('^' + m.group(1) + '$')}, {json.dumps(flags)})")
                    elif v:
                        id_filters.append(f"{last} = {json.dumps(v.rstrip('/'))}")
                continue
            path = next((ctx.expand(s) for s in ids(p.get("prov:specializationOf"))), None) or ctx.expand(plabel)
            if not path or (not ids(p.get("prov:specializationOf")) and plabel not in ctx.terms):
                if not path or not opts["--context"]:
                    notes.append(f"{p['@id']}: no prov:specializationOf; {plabel!r} mapped to {path} (give --context to map RO-Crate terms)")
            if not path:
                continue
            lines = [f"sh:path {iri(path)}", f"sh:name {lit(f'{label}: {plabel}')}"]
            if first(p.get("rdfs:comment")) or first(p.get("description")):
                lines.append(f"sh:description {lit(first(p.get('rdfs:comment')) or first(p.get('description')))}")
            pmin, pmax = as_int(p.get("sh:minCount")), as_int(p.get("sh:maxCount"))
            if pmin:
                lines.append(f"sh:minCount {pmin}")
            if pmax is not None:
                lines.append(f"sh:maxCount {pmax}")
            options, ranges = [], ids(p.get("rangeIncludes"))
            for r in ranges:
                target = nodes.get(r, {})
                rtypes = ids(target.get("@type"))
                if r in classes:
                    options += [f"[ sh:class {iri(t)} ]" for t in class_types(r)[:1]]
                elif "PropertyValue" in rtypes:
                    value = target.get("value")
                    v = first(value)
                    m = re.match(r"^/(.*)/([a-z]*)$", v or "", re.S)
                    if isinstance(value, dict) and "@id" in value:
                        options.append(f"[ sh:hasValue {iri(ctx.expand(value['@id'], vocab=False) or value['@id'])} ]")
                    elif m:
                        flags = "".join(f for f in m.group(2) if f in "imsx")
                        options.append(f"[ sh:pattern {lit(m.group(1))}" + (f" ; sh:flags {lit(flags)}" if flags else "") + " ]")
                    elif v is not None:
                        options.append(f"[ sh:hasValue {lit(v)} ]")
                elif "ItemList" in rtypes:
                    members = [ctx.expand(e, vocab=False) or e for e in ids(target.get("itemListElement"))]
                    options.append("[ sh:in ( " + " ".join(iri(e) for e in members) + " ) ]")
                elif range_kind(r, ctx):
                    options.append(range_kind(r, ctx))
                elif ctx.expand(r):
                    options.append(f"[ sh:class {iri(ctx.expand(r))} ]")
                else:
                    notes.append(f"{p['@id']}: range {r} not converted")
            if options and len(options) == len(ranges):
                lines.append("sh:or ( " + " ".join(options) + " )" if len(options) > 1 else options[0][2:-2])
            elif options:
                notes.append(f"{p['@id']}: some ranges not converted, so its range is not checked")
            message = f"{label}: {plabel} (MASP rule {p['@id']})"
            lines.append(f"sh:message {lit(message)}")
            shapes.append("    sh:property [\n        " + " ;\n        ".join(lines) + " ;\n    ]")
        if not shapes:
            continue
        sid = iri(ns + re.sub(r"[^A-Za-z0-9_-]+", "_", cid.strip("#")))
        if cid in root_rules and len(root_rules) > 1:
            # one of several kinds of root: no target of its own, the root must conform to one of them
            alternatives.append(sid)
            target = " ;\n    ".join(f"sh:class {iri(t)}" for t in types)
        elif cid in root_rules:
            target = " ;\n    ".join(f"sh:targetClass {iri(t)}" for t in root_classes)
        elif len(types) == 1 and not id_filters:
            target = f"sh:targetClass {iri(types[0])}"
        else:
            where = " ".join(f"?this a {iri(t)} ." for t in types)
            where += "".join(f" FILTER({f})" for f in id_filters[:1])
            target = f"sh:target [ a sh:SPARQLTarget ; sh:select {lit(f'SELECT ?this WHERE {{ {where} }}')} ]"
        out.append(f"{sid} a sh:NodeShape ;\n    sh:name {lit(label)} ;\n    {target} ;\n" + " ;\n".join(shapes) + " .\n")

    if alternatives:
        targets = " ;\n    ".join(f"sh:targetClass {iri(t)}" for t in root_classes)
        names = ", ".join(first(classes[c].get("name")) or c for c in root_rules)
        out.append(f"{iri(ns + 'root-alternatives')} a sh:NodeShape ;\n    sh:name {lit('Kind of root data entity')} ;\n"
                   f"    {targets} ;\n    sh:or ( {' '.join(alternatives)} ) ;\n"
                   f"    sh:message {lit('The root data entity must conform to one of: ' + names)} .\n")

    if counts:  # how many entities of a type the whole crate has, checked once from the root
        # ($this must occur in the pattern: pySHACL 0.40 reports nothing for a query that only has a subquery)
        sparql = []
        for label, types, lo, hi in counts:
            where = " ".join(f"?x a {iri(t)} ." for t in types)
            cond = " || ".join(c for c in ([f"?n < {lo}"] if lo else []) + ([f"?n > {hi}"] if hi is not None else []))
            msg = f"The crate must have {lo or 0} to {hi if hi is not None else 'any number of'} {label} entities"
            sparql.append(f"    sh:sparql [ a sh:SPARQLConstraint ; sh:message {lit(msg)} ;\n        sh:select "
                          + lit(f"SELECT $this WHERE {{ $this a ?rootType . {{ SELECT (COUNT(DISTINCT ?x) AS ?n) WHERE {{ {where} }} }} FILTER({cond}) }}") + " ]")
        targets = " ;\n    ".join(f"sh:targetClass {iri(t)}" for t in root_classes)
        out.append(f"{iri(ns + 'class-counts')} a sh:NodeShape ;\n    sh:name {lit('Number of entities of each type')} ;\n    {targets} ;\n"
                   + " ;\n".join(sparql) + " .\n")

    folder = f"{args[1].rstrip('/')}/{token}/{version}"
    os.makedirs(folder + "/must", exist_ok=True)
    with open(folder + "/must/0_masp_rules.ttl", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    with open(folder + "/profile.ttl", "w", encoding="utf-8") as f:
        f.write("@prefix prof: <http://www.w3.org/ns/dx/prof/> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n"
                f"{iri(profile_iri)} a prof:Profile ;\n    rdfs:label {lit(first(root.get('name')) or token)} ;\n"
                + (f"    rdfs:comment {lit(first(root.get('description')))} ;\n" if first(root.get("description")) else "")
                + f"    prof:isProfileOf <https://w3id.org/ro/crate/{base}> ;\n"
                "    prof:isTransitiveProfileOf " + " , ".join(f"<https://w3id.org/ro/crate/{v}>" for v in TRANSITIVE.get(base, [base])) + " ;\n"
                f"    prof:hasToken {lit(token)} .\n")
    print(f"Wrote {folder}/profile.ttl and must/0_masp_rules.ttl (profile {profile_iri}, based on RO-Crate {base})")
    print(f"Run: rocrate-validator validate --extra-profiles-path {args[1]} -p {token}-{version} <crate>")
    for n in notes:
        print("Not converted:", n)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
