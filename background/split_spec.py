#!/usr/bin/env python3
"""Split an all-in-one RO-Crate specification Markdown file into one file per chapter.

The released all-in-one Markdown (ro-crate-1.2.0.md, ro-crate-1.3.0.md on Zenodo) is larger than
the 256 KiB per file that Anthropic's plugin directory accepts without review, and is hard to read
in one go. This script cuts it at each top-level heading into the file names that the
specification uses on GitHub (docs/_specification/<version>/), and rewrites `](#anchor)` links
whose target is in another chapter to `](<chapter>.md#anchor)`. Nothing else is changed: line N
of a chapter file is line (start + N - 1) of the all-in-one file.

With a third argument, the RO-Crate quick reference (ro-crate-quick-reference-1.2-1.3.md) is also
written to the output folder as quick-reference.md, with its links to the specification web pages
pointing at the chapter files instead, so it can serve as an index of requirements.

Usage: python split_spec.py ro-crate-1.3.0.md ro-crate-1.3/ [ro-crate-quick-reference-1.2-1.3.md]
"""
import re
import sys
from pathlib import Path

# Chapter file for each top-level heading, by explicit {#id} or by heading text.
CHAPTERS = {
    "introduction": "introduction.md",
    "terminology": "terminology.md",
    "structure": "structure.md",
    "metadata": "metadata.md",
    "root data entity": "root-data-entity.md",
    "data-entities": "data-entities.md",
    "contextual-entities": "contextual-entities.md",
    "crate-focus": "crate-focus.md",
    "provenance": "provenance.md",
    "profiles": "profiles.md",
    "workflows": "workflows.md",
    "appendix": "appendix/index.md",
    "implementation-notes": "appendix/implementation-notes.md",
    "jsonld": "appendix/jsonld.md",
    "relative-uris": "appendix/relative-uris.md",
    "changelog": "appendix/changelog.md",
    "references": "references.md",
}
FRONT_MATTER = "index.md"

EXPLICIT_ID = re.compile(r"\{#([^}\s]+)[^}]*\}\s*$")
ATX = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LINK = re.compile(r"\]\(#([^)\s]+)\)")


def pandoc_id(text):
    """Pandoc auto_identifiers: drop formatting and punctuation, spaces to hyphens, lowercase."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*]", "", text)
    text = "".join(c for c in text.lower() if c.isalnum() or c in " _-.")
    text = re.sub(r"\s+", "-", text.strip())
    return re.sub(r"^[^a-z]+", "", text) or "section"


def github_id(text):
    """GitHub/Jekyll-style ids, as used on the specification web pages: each space is a hyphen, no dots."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = "".join(c for c in text.lower() if c.isalnum() or c in " _-")
    return text.strip().replace(" ", "-")


def headings(lines):
    """Yield (index, level, text) for ATX and Setext headings outside fenced code blocks."""
    fence = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        m = re.match(r"^(`{3,}|~{3,})", stripped)
        if m:
            if fence is None:
                fence = m.group(1)[0] * len(m.group(1))
            elif stripped.startswith(fence) and stripped.strip(fence[0]) == "":
                fence = None
            continue
        if fence:
            continue
        m = ATX.match(line)
        if m:
            yield i, len(m.group(1)), m.group(2)
        elif i > 0 and lines[i - 1].strip() and not lines[i - 1].startswith(("|", " ", "-", "*", ">")):
            if re.fullmatch(r"=+", stripped):
                yield i - 1, 1, lines[i - 1].strip()
            elif re.fullmatch(r"-{3,}", stripped):
                yield i - 1, 2, lines[i - 1].strip()


def split(src, outdir):
    lines = Path(src).read_text(encoding="utf-8").splitlines(keepends=True)
    starts = [(0, FRONT_MATTER)]
    anchors = {}  # anchor in the all-in-one file -> chapter file
    pages = {}  # chapter file -> anchors on its web page, where each chapter is a page of its own
    current = FRONT_MATTER
    seen = {}
    for i, level, text in headings(lines):
        m = EXPLICIT_ID.search(text)
        title = EXPLICIT_ID.sub("", text).strip()
        anchor = m.group(1) if m else pandoc_id(title)
        if level == 1 and i > 0:
            key = anchor if anchor in CHAPTERS else title.lower()
            if key not in CHAPTERS:
                sys.exit(f"{src}:{i + 1}: no chapter file for top-level heading {text!r}")
            current = CHAPTERS[key]
            starts.append((i, current))
        if not m:  # pandoc numbers duplicate auto ids: x, x-1, x-2
            n = seen.get(anchor, 0)
            seen[anchor] = n + 1
            if n:
                anchor = f"{anchor}-{n}"
        anchors.setdefault(anchor, current)
        anchors.setdefault(github_id(title), current)
        pages.setdefault(current, set()).update({m.group(1)} if m else {pandoc_id(title), github_id(title)})

    outdir = Path(outdir)
    unresolved = set()
    for n, (start, name) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
        here = Path(name).parent

        def relink(m):
            target = anchors.get(m.group(1))
            if target is None:
                unresolved.add(m.group(1))
                return m.group(0)
            if target == name:
                return m.group(0)
            rel = Path(*([".."] * len(here.parts)), target).as_posix()
            return f"]({rel}#{m.group(1)})"

        path = outdir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(LINK.sub(relink, line) for line in lines[start:end]), encoding="utf-8")
        print(f"{path}\t{start + 1}-{end}\t{path.stat().st_size}")
    for anchor in sorted(unresolved):
        print(f"warning: no heading for link #{anchor}", file=sys.stderr)
    return pages


SPEC_PAGE = re.compile(
    r"\]\(https://www\.researchobject\.org/ro-crate/specification/[0-9.]+(?:-DRAFT)?/"
    r"([a-z/-]+?)(?:\.html)?(?:\?[^)#]*)?(?:#([^)\s]+))?\)")


def quick_reference(src, outdir, pages):
    """Copy the quick reference with links to specification pages pointing at the chapter files."""
    files = {Path(f).with_suffix("").as_posix(): f for f in CHAPTERS.values()}

    def relink(m):
        page, anchor = m.group(1), m.group(2)
        target = files.get(page) or files.get(f"{page}/index")
        if target is None:
            print(f"warning: no chapter file for {m.group(0)}", file=sys.stderr)
            return m.group(0)
        if anchor and anchor not in pages.get(target, ()):
            print(f"warning: #{anchor} is not a heading in {target}", file=sys.stderr)
        return f"]({target}#{anchor})" if anchor else f"]({target})"

    text = Path(src).read_text(encoding="utf-8")
    text = SPEC_PAGE.sub(relink, text)
    text = text.replace("](community#contact-us)", "](https://www.researchobject.org/ro-crate/community#contact-us)")
    note = ("<!-- Links to specification pages rewritten by split_spec.py to the chapter files in this folder. -->\n")
    path = Path(outdir) / "quick-reference.md"
    path.write_text(note + text, encoding="utf-8")
    print(f"{path}\t\t{path.stat().st_size}")


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__.strip().splitlines()[-1])
    pages = split(sys.argv[1], sys.argv[2])
    if len(sys.argv) == 4:
        quick_reference(sys.argv[3], sys.argv[2], pages)
