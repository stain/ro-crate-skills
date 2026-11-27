#!/usr/bin/env python3
"""Summarise and check the rules of an RO-Crate MASP profile or schema crate.

Usage: masp_rules.py [--json] <masp-crate/ro-crate-metadata.json>

Reads the crate the way the MASP validator does: the ResourceDescriptor in the root's
hasResource with hasRole http://www.w3.org/ns/dx/prof/role/schema lists the rules in its
hasPart (rdfs:Class, rdf:Property, PropertyValue, ItemList, DefinedTermSet); nothing else
in the crate is a rule. Prints the profile's identifiers (root @id, conformance indicators),
then each class rule with its property rules, cardinalities and ranges, then problems:
  ERROR    the validator would ignore or misread the rule (exit status 1)
  WARNING  works with the JavaScript validator but is fragile or unusual
Does not validate a target crate against the profile: use masp-validate for that.
Standard library only.
"""
import json
import re
import sys

SCHEMA_ROLE = "http://www.w3.org/ns/dx/prof/role/schema"
INDICATORS_ROLE = "https://w3id.org/ro/conformance-indicators"
PRIMITIVES = {"Text", "Number", "Integer", "Float", "Boolean", "Date", "DateTime", "Time", "URL"}


def ids(value):
    values = value if isinstance(value, list) else [value]
    return [v["@id"] if isinstance(v, dict) else v for v in values if v not in (None, "")]


def first(value):
    values = value if isinstance(value, list) else [value]
    for v in values:
        if isinstance(v, dict):
            v = v.get("@value", v.get("@id"))
        if v not in (None, ""):
            return str(v)
    return None


def types(node):
    return set(ids(node.get("@type")))


def count(node, key, problems, rid):
    """sh:minCount / sh:maxCount as an int (strings such as "1" are accepted, as upstream)."""
    for k in (key, "http://www.w3.org/ns/shacl#" + key.split(":")[1]):
        if k in node:
            value = first(node[k])
            if value is None:
                continue  # empty list or "": no constraint
            if k != key:
                problems.append(("WARNING", rid, f"{k} written as a full IRI; the JavaScript validator only reads the key {key}"))
            try:
                return int(value)
            except (TypeError, ValueError):
                problems.append(("ERROR", rid, f"{key} is not an integer: {value!r}"))
    return None


def card(lo, hi):
    return f"{lo or 0}..{hi if hi is not None else '*'}"


def short(iri):
    for ns in ("http://schema.org/", "https://schema.org/"):
        if iri.startswith(ns):
            return iri[len(ns):]
    return iri


def main(argv):
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    if len(args) != 1:
        sys.exit(__doc__)
    doc = json.load(open(args[0], encoding="utf-8"))
    graph = doc.get("@graph")
    if not isinstance(graph, list):
        sys.exit("Not a flattened RO-Crate: no @graph array")
    nodes = {n.get("@id"): n for n in graph if isinstance(n, dict)}
    problems = []

    context = doc.get("@context")
    local = {}
    for c in context if isinstance(context, list) else [context]:
        if isinstance(c, dict):
            local.update(c)
    uses_sh = any(isinstance(k, str) and k.startswith("sh:") for n in graph for k in n)
    if uses_sh and "sh" not in local:
        problems.append(("WARNING", "@context", 'uses sh:minCount/sh:maxCount but does not define the prefix '
                         '"sh": "http://www.w3.org/ns/shacl#" (the validator still reads the keys as written)'))

    descriptor = nodes.get("ro-crate-metadata.json") or {}
    root_id = first(descriptor.get("about"))
    root = nodes.get(root_id) or {}
    if not root:
        problems.append(("ERROR", "ro-crate-metadata.json", "metadata descriptor or its about (root) not found"))

    resources = [nodes.get(r) or {} for r in ids(root.get("hasResource"))]
    schema = [r for r in resources if SCHEMA_ROLE in ids(r.get("hasRole"))]
    indicators = []
    for r in resources:
        if INDICATORS_ROLE in ids(r.get("hasRole")):
            for a in ids(r.get("hasArtifact")):
                indicators += ids((nodes.get(a) or {}).get("itemListElement"))
    if not schema:
        unlinked = [n.get("@id") for n in graph if SCHEMA_ROLE in ids(n.get("hasRole"))]
        problems.append(("ERROR", root_id, f"no ResourceDescriptor with hasRole {SCHEMA_ROLE} in the root's hasResource: no rules"
                         + (f" ({', '.join(unlinked)} has the role but is not in hasResource)" if unlinked else "")))
    rule_ids = [i for s in schema for i in ids(s.get("hasPart"))]
    if schema and not rule_ids:
        problems.append(("ERROR", first(schema[0].get("@id")), "schema ResourceDescriptor lists no rules in hasPart"))

    classes, props, others = {}, {}, {}
    for rid in rule_ids:
        node = nodes.get(rid)
        if node is None:
            problems.append(("ERROR", rid, "listed in hasPart of the schema descriptor but not in @graph"))
            continue
        t = types(node)
        if "rdfs:Class" in t or "http://www.w3.org/2000/01/rdf-schema#Class" in t:
            classes[rid] = node
        elif "rdf:Property" in t or "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property" in t:
            props[rid] = node
        else:
            others[rid] = node

    by_class = {c: [] for c in classes}
    root_rule = None
    for rid, p in props.items():
        label = first(p.get("rdfs:label")) or first(p.get("name"))
        if not first(p.get("rdfs:label")):
            problems.append(("WARNING" if label else "ERROR", rid, "property rule without rdfs:label (the JSON key it constrains)"))
        if "schema:domainIncludes" in p or "http://schema.org/domainIncludes" in p:
            problems.append(("ERROR", rid, "write domainIncludes, not schema:domainIncludes: the validator reads the plain key"))
        if "schema:rangeIncludes" in p or "http://schema.org/rangeIncludes" in p:
            problems.append(("ERROR", rid, "write rangeIncludes, not schema:rangeIncludes: the validator reads the plain key"))
        if "value" in p:
            problems.append(("ERROR", rid, "value on a property rule: put it on a PropertyValue referenced from rangeIncludes"))
        if label != "@id" and not ids(p.get("prov:specializationOf")):
            problems.append(("WARNING", rid, "property rule without prov:specializationOf (the vocabulary term it specialises)"))
        domain = ids(p.get("domainIncludes"))
        if not domain:
            problems.append(("ERROR", rid, "property rule without domainIncludes: applies to no class rule"))
        for d in domain:
            if d in by_class:
                by_class[d].append(rid)
            else:
                problems.append(("ERROR", rid, f"domainIncludes {d} is not a class rule listed in the schema descriptor"))
        lo, hi = count(p, "sh:minCount", problems, rid), count(p, "sh:maxCount", problems, rid)
        if lo is not None and hi is not None and lo > hi:
            problems.append(("ERROR", rid, f"sh:minCount {lo} > sh:maxCount {hi}"))
        for r in ids(p.get("rangeIncludes")):
            target = nodes.get(r)
            if r.startswith("#") and target is None:
                problems.append(("ERROR", rid, f"rangeIncludes {r} not found in @graph"))
            if target is not None and r not in rule_ids and "PropertyValue" not in types(target):
                problems.append(("WARNING", rid, f"rangeIncludes {r} is not listed in the schema descriptor's hasPart"))
            if target is not None and "PropertyValue" in types(target):
                value = first(target.get("value"))
                if label == "@id" and value == "ro-crate-metadata.json":
                    root_rule = domain
                if isinstance(value, str) and value.startswith("/") and not re.match(r"^/.*/[a-z]*$", value, re.S):
                    problems.append(("ERROR", r, f"value starts with / but is not a /regex/flags literal: {value!r}"))

    for rid, c in classes.items():
        if not ids(c.get("prov:specializationOf")) and rid.startswith("#"):
            problems.append(("ERROR", rid, "class rule with a local @id and no prov:specializationOf: matches no entities"))
        lo, hi = count(c, "sh:minCount", problems, rid), count(c, "sh:maxCount", problems, rid)
        if lo is not None and hi is not None and lo > hi:
            problems.append(("ERROR", rid, f"sh:minCount {lo} > sh:maxCount {hi}"))
        for s in ids(c.get("rdfs:subClassOf")):
            if s.startswith("#") and s not in classes:
                problems.append(("WARNING", rid, f"rdfs:subClassOf {s} is not a class rule listed in the schema descriptor"))
    if classes and not root_rule:
        problems.append(("WARNING", root_id, 'no root detection rule (property rule rdfs:label "@id" with rangeIncludes a '
                         'PropertyValue "ro-crate-metadata.json"): fine for a schema, needed for a profile of whole crates'))

    summary = {
        "root": root_id, "name": first(root.get("name")), "version": first(root.get("version")),
        "conformsTo": ids(root.get("conformsTo")), "isProfileOf": ids(root.get("isProfileOf")),
        "conformanceIndicators": indicators, "descriptorClassRule": root_rule[0] if root_rule else None,
        "classRules": {}, "otherRules": {r: sorted(types(n)) for r, n in others.items()},
        "problems": [{"level": lv, "rule": r, "message": m} for lv, r, m in problems],
    }
    for cid, c in classes.items():
        entry = {"label": first(c.get("rdfs:label")) or first(c.get("name")),
                 "specializationOf": ids(c.get("prov:specializationOf")),
                 "subClassOf": ids(c.get("rdfs:subClassOf")),
                 "instances": card(first(c.get("sh:minCount")), first(c.get("sh:maxCount"))), "properties": []}
        for pid in by_class[cid]:
            p = props[pid]
            entry["properties"].append({"rule": pid, "label": first(p.get("rdfs:label")) or first(p.get("name")),
                                        "values": card(first(p.get("sh:minCount")), first(p.get("sh:maxCount"))),
                                        "range": ids(p.get("rangeIncludes"))})
        summary["classRules"][cid] = entry

    if as_json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"{summary['name']} {summary['version'] or ''}".strip(), f"<{root_id}>")
        for key in ("conformsTo", "isProfileOf", "conformanceIndicators"):
            if summary[key]:
                print(f"  {key}: " + ", ".join(summary[key]))
        print(f"{len(classes)} class rules, {len(props)} property rules, {len(others)} other rules"
              + (f"; descriptor class rule {summary['descriptorClassRule']}" if root_rule else ""))
        for cid, e in summary["classRules"].items():
            spec = ", ".join(short(s) for s in e["specializationOf"]) or "(own @id)"
            print(f"\n{e['label'] or cid} [{cid}] = {spec}, instances {e['instances']}"
                  + (f", subClassOf {', '.join(e['subClassOf'])}" if e["subClassOf"] else ""))
            for p in sorted(e["properties"], key=lambda p: (not p["values"].startswith(("1", "2", "3")), p["label"] or "")):
                rng = ", ".join(short(r) for r in p["range"]) or "-"
                print(f"  {p['values']:>6}  {p['label']}  -> {rng}")
        if others:
            kinds = {}
            for t in summary["otherRules"].values():
                kinds["/".join(t)] = kinds.get("/".join(t), 0) + 1
            print("\nOther rules: " + ", ".join(f"{n} {k}" for k, n in sorted(kinds.items())) + " (--json lists them)")
        if problems:
            print()
            for level, rid, message in problems:
                print(f"{level}: {rid}: {message}")
    return 1 if any(level == "ERROR" for level, _, _ in problems) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
