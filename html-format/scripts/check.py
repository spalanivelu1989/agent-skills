#!/usr/bin/env python3
"""Lint a document built from the html-format template.

    python3 ~/.claude/skills/html-format/scripts/check.py page.html [more.html …]

Catches the failures that recur and that can be seen without a browser:
scaffold text left in, sections the sidebar cannot link to, chips that state a
duration, a lone sidenote paying for a whole gutter, language names the
highlighter does not know, hand-written markup the scripts generate, capture
boxes sharing a storage bucket, new CSS, a coloured leading edge on a tinted
box, and theme blocks that have drifted apart. Exit status is 1 if any ERROR was reported, else 0. WARN lines are
judgement calls — read them, then decide.

Standard library only.
"""

import re
import sys
from html.parser import HTMLParser

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}

# Text that only exists in the template scaffold. Any of it surviving into a
# finished page means a placeholder was never replaced.
PLACEHOLDERS = [
    "DOCUMENT TITLE",
    "DOCUMENT DESCRIPTION",
    "OPTIONAL KICKER",
    "One or two sentences stating what this document is",
    "who this is written for",
    "what to have in hand",
    "who maintains it",
    "Part 1 · Label",
    "Part 2 · Label",
    "First section",
    "Second section",
    "Body copy goes here",
    "An aside the reader can take or leave",
    "Provenance, related links, or maintenance notes",
]

# Used when the document does not carry the highlighter (it was deleted), so
# there is nothing to read the list from.
FALLBACK_LANGS = {
    "python", "javascript", "typescript", "java", "kotlin", "go", "rust",
    "cpp", "csharp", "php", "ruby", "swift", "sql", "bash", "json", "yaml",
    "markup", "html", "xml", "css", "abap", "plaintext", "text", "txt",
    "none", "log", "console", "output", "diff",
}

LAYOUT_TOKENS = {"--measure", "--card-pad", "--sidenote-w", "--sidenote-gap"}

THEME_BLOCKS = {
    "light (:root)": r":root\s*\{",
    "dark (OS preference)": r"@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*:root\s*\{",
    'dark (data-theme="dark")': r':root\[data-theme="dark"\]\s*\{',
    'light (data-theme="light")': r':root\[data-theme="light"\]\s*\{',
    'paper (data-theme="paper")': r':root\[data-theme="paper"\]\s*\{',
    "print": r"@media\s+print\s*\{\s*:root,\s*:root\[data-theme\]\s*\{",
}


class Node:
    def __init__(self, tag, attrs, parent, line):
        self.tag = tag
        self.attrs = dict(attrs)
        self.parent = parent
        self.children = []
        self.text = []
        self.line = line

    @property
    def classes(self):
        return (self.attrs.get("class") or "").split()

    def has(self, cls):
        return cls in self.classes

    def all_text(self):
        out = list(self.text)
        for c in self.children:
            out.append(c.all_text())
        return " ".join(t for t in out if t).strip()

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()

    def ancestors(self):
        p = self.parent
        while p is not None:
            yield p
            p = p.parent

    def inside(self, pred):
        return any(pred(a) for a in self.ancestors())


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", [], None, 0)
        self.cur = self.root
        self.raw = {"style": [], "script": []}
        self._raw_tag = None

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.cur, self.getpos()[0])
        self.cur.children.append(node)
        if tag in VOID:
            return
        self.cur = node
        if tag in self.raw:
            self._raw_tag = tag
            self.raw[tag].append("")

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        self._raw_tag = None
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        if self._raw_tag:
            self.raw[self._raw_tag][-1] += data
        elif data.strip():
            self.cur.text.append(data.strip())


def block_tokens(css, pattern):
    """Return {token: value} for the first rule body matching pattern."""
    m = re.search(pattern, css)
    if not m:
        return None
    body = css[m.end(): css.index("}", m.end())]
    body = re.sub(r"/\*.*?\*/", "", body, flags=re.S)
    # Layout tokens live on bare :root only; the palette is what must agree.
    return {
        k.strip(): v.strip().lower()
        for k, v in re.findall(r"(--[\w-]+|color-scheme)\s*:\s*([^;]+);", body)
        if k.strip() not in LAYOUT_TOKENS
    }


def check(path):
    src = open(path, encoding="utf-8").read()
    t = Tree()
    t.feed(src)
    nodes = list(t.root.walk())
    errors, warns = [], []

    def err(line, msg):
        errors.append((line, msg))

    def warn(line, msg):
        warns.append((line, msg))

    html = next((n for n in nodes if n.tag == "html"), None)
    hattrs = html.attrs if html else {}
    nav_mode = hattrs.get("data-nav", "tabbed")
    if nav_mode not in ("tabbed", "scroll"):
        err(html.line, f'data-nav="{nav_mode}" — must be "tabbed" or "scroll"')

    # --- Scaffold left behind -------------------------------------------
    body_start = src.find("<body")
    for ph in PLACEHOLDERS:
        for m in re.finditer(re.escape(ph), src):
            # The template's own comments quote some of these; only flag text
            # outside comments.
            before = src[: m.start()]
            if before.rfind("<!--") > before.rfind("-->"):
                continue
            err(before.count("\n") + 1, f'placeholder text left in: "{ph}"')
    meta_desc = next(
        (n for n in nodes if n.tag == "meta" and n.attrs.get("name") == "description"),
        None,
    )
    if meta_desc is None or not (meta_desc.attrs.get("content") or "").strip():
        warn(1, 'no <meta name="description"> — shared links show no summary')

    # --- Headings --------------------------------------------------------
    h1s = [n for n in nodes if n.tag == "h1"]
    if len(h1s) != 1:
        err(h1s[1].line if len(h1s) > 1 else 1, f"expected exactly one <h1>, found {len(h1s)}")

    # --- Sections and navigation ----------------------------------------
    ids = {}
    for n in nodes:
        i = n.attrs.get("id")
        if i:
            if i in ids:
                err(n.line, f'duplicate id="{i}" (first on line {ids[i]})')
            else:
                ids[i] = n.line

    phases = [n for n in nodes if n.tag == "section" and n.has("phase")]
    for s in phases:
        if not s.attrs.get("id"):
            err(s.line, "section.phase has no id — it will be missing from the sidebar")
        if not any(c.tag == "h2" for c in s.children):
            warn(s.line, "section.phase has no direct <h2> — the sidebar falls back to its id as the label")
        label = s.attrs.get("data-nav-label")
        h2 = next((c for c in s.children if c.tag == "h2"), None)
        shown = label or (h2.all_text() if h2 else "")
        if len(shown) > 60:
            warn(s.line, f"sidebar label is {len(shown)} chars — add a shorter data-nav-label")

    sidebar = next((n for n in nodes if n.tag == "nav" and n.has("sidebar")), None)
    if sidebar and any(n.tag == "a" and n.has("tab") for n in sidebar.walk()):
        err(sidebar.line, "hand-written a.tab links in the sidebar — they are generated from section ids; delete them")

    pager = next((n for n in nodes if n.has("pager")), None)
    if nav_mode == "scroll" and pager:
        warn(pager.line, "scroll mode with a .pager left in — it is dead markup; delete it")
    if nav_mode == "tabbed" and phases and len(phases) < 4:
        warn(html.line, f"tabbed mode with only {len(phases)} sections — scroll mode usually suits fewer than 4")
    if nav_mode == "tabbed" and phases and not pager:
        warn(html.line, "tabbed mode but no .pager — readers get no prev/next buttons")

    # --- Chips and meta-strip -------------------------------------------
    for n in nodes:
        if n.has("chip"):
            txt = n.all_text()
            if re.match(r"\s*(Time|Writes|Read)\s*[—-]", txt):
                err(n.line, f'chip states a duration/path/reading time: "{txt}" — remove it')
        if n.has("phase-meta") and not any(c.has("chip") for c in n.children):
            err(n.line, "empty .phase-meta row — delete it")
        if n.has("meta-strip"):
            for c in n.children:
                if re.match(r"\s*Time\b", c.all_text()):
                    err(c.line, 'meta-strip has a "Time — …" entry — durations go stale; remove it')

    # --- Callout labels ---------------------------------------------------
    for n in nodes:
        if n.has("label") and n.parent is not None and (
            n.parent.has("win") or n.parent.has("why") or n.parent.has("warn") or n.parent.has("sidenote")
        ):
            if n.all_text().strip().lower() in ("note", "info", "tip", "warning", "aside", "important"):
                warn(n.line, f'generic callout label "{n.all_text()}" — make it say something')

    # --- Sidenotes ----------------------------------------------------------
    notes = [n for n in nodes if n.tag == "aside" and n.has("sidenote")]
    if 0 < len(notes) < 3:
        warn(
            notes[0].line,
            f"{len(notes)} sidenote(s) — each makes every section reserve 14rem above 1440px; "
            "below ~3, use .why callouts instead",
        )

    # --- Code -----------------------------------------------------------
    scripts = "\n".join(t.raw["script"])
    langs = set()
    for m in re.finditer(r'\bdef\(\s*"([^"]+)"', scripts):
        langs.update(m.group(1).split())
    am = re.search(r"var ALIAS = \{(.*?)\};", scripts, re.S)
    if am:
        langs.update(k.strip('"') for k in re.findall(r'^\s*("?[\w+#.-]+"?)\s*:', am.group(1), re.M))
    highlighter = bool(langs)
    if not highlighter:
        langs = FALLBACK_LANGS
    for n in nodes:
        if n.tag in ("pre", "code"):
            m = re.search(r"(?:^|\s)(?:language|lang)-([\w+#.-]+)", n.attrs.get("class") or "")
            if m and m.group(1).lower() not in langs:
                err(n.line, f'unknown language "{m.group(1)}" — the block will render grey; fix the name or drop the class')
        if n.has("codewrap") or n.has("copy-btn"):
            err(n.line, f".{n.classes[0]} written by hand — the script adds it; a hand-wrapped block gets no copy button")
        if any(c.startswith("doc-search") or c == "doc-topbar" for c in n.classes):
            err(n.line, f".{n.classes[0]} written by hand — the search box is built by the script; delete this markup (data-search=\"off\" on <html> turns search off)")

    # --- Tables, figures, disclosures ------------------------------------
    for n in nodes:
        if n.tag == "table" and not n.inside(lambda a: a.has("tablewrap")):
            warn(n.line, "table not inside .tablewrap — narrow screens will scroll the page, not the table")
        if n.tag == "img":
            alt = n.attrs.get("alt")
            if alt is None or not alt.strip():
                err(n.line, "img without alt text")
            else:
                fig = n.parent
                cap = next((c for c in fig.children if c.tag == "figcaption"), None) if fig else None
                if cap and cap.all_text().strip() == alt.strip():
                    warn(n.line, "alt text identical to the figcaption — they serve different readers")
        if n.tag == "details" and n.has("disclose"):
            for c in n.children:
                if c.tag != "summary" and not c.has("disclose-body"):
                    err(c.line, "details.disclose child outside .disclose-body — it will render flush to the edges")
                if c.tag == "summary" and c.attrs.get("class"):
                    warn(c.line, "summary in .disclose takes no class")

    # --- Output capture -------------------------------------------------
    caps = [n for n in nodes if n.has("capture") and n.attrs.get("data-capture")]
    seen = {}
    for c in caps:
        k = c.attrs["data-capture"]
        if k in seen:
            err(c.line, f'duplicate data-capture="{k}" (first on line {seen[k]}) — they will overwrite each other')
        seen[k] = c.line
        if not any(x.tag == "textarea" for x in c.walk()):
            err(c.line, f'capture "{k}" has no <textarea>')
    if caps and not hattrs.get("data-capture-store"):
        err(html.line, "capture boxes present but no data-capture-store on <html> — shares the default bucket with other pages")
    collectors = [n for n in nodes if n.has("capture") and n.attrs.get("data-collect")]
    if len(collectors) > 1:
        err(collectors[1].line, "more than one collector — at most one per document")
    for c in collectors:
        for need in ("collectBox", "collectBtn"):
            if need not in ids:
                err(c.line, f'collector missing id="{need}"')

    # --- No new CSS, no new dependencies ---------------------------------
    for n in nodes:
        if "style" in n.attrs and n.tag not in ("html",):
            err(n.line, f'style= attribute on <{n.tag}> — use a component instead of new CSS')
    styles = [n for n in nodes if n.tag == "style"]
    if len(styles) > 1:
        err(styles[1].line, f"{len(styles)} <style> blocks — the template has one; do not add CSS")
    for n in nodes:
        if n.tag == "script" and n.attrs.get("src"):
            err(n.line, f'external script {n.attrs["src"]} — the document must be self-contained')
        if n.tag == "link" and "stylesheet" in (n.attrs.get("rel") or ""):
            href = n.attrs.get("href") or ""
            if not href.startswith("https://fonts.googleapis.com/"):
                err(n.line, f"external stylesheet {href} — only the Google Fonts link is allowed")
    body_html = src[body_start:] if body_start >= 0 else ""
    body_html = re.sub(r"<script\b.*?</script>", "", body_html, flags=re.S)
    # Colour attributes (inline SVG is the usual source); style= is caught above.
    for m in re.finditer(
        r"\b(?:fill|stroke|color|bgcolor|stop-color)\s*=\s*[\"']?(#[0-9a-fA-F]{3,8})\b", body_html
    ):
        line = src[: body_start + m.start()].count("\n") + 1
        warn(line, f"raw colour {m.group(1)} in the body — use var(--token) / currentColor")

    # --- No coloured leading edge on a tinted box ------------------------
    # House rule: a box with a background is identified by its tint and its
    # label, not by a coloured bar down its left side.
    css = "\n".join(t.raw["style"])
    flat = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", flat):
        selector, body = m.group(1).strip(), m.group(2)
        edge = re.search(r"border-left\s*:\s*([^;]+)", body)
        shadow = re.search(r"box-shadow\s*:\s*inset\s+\d+(?:\.\d+)?(?:px|rem)\s+0\s+0\s+", body)
        tinted = re.search(r"background(?:-color)?\s*:\s*(?!none|transparent)", body)
        if tinted and ((edge and not re.match(r"\s*(none|0)\b", edge.group(1))) or shadow):
            last = selector.splitlines()[-1].strip()
            hit = re.search(re.escape(last) + r"\s*\{[^}]*?(?:border-left|box-shadow)", src)
            line = hit.start() if hit else -1
            err(src[: line].count("\n") + 1 if line >= 0 else 1,
                f"{selector.splitlines()[-1].strip()} has a background and a coloured leading edge"
                " — tinted boxes carry no left bar; drop the border-left")

    # --- Theme blocks agree ----------------------------------------------
    blocks = {name: block_tokens(css, pat) for name, pat in THEME_BLOCKS.items()}
    for name, toks in blocks.items():
        if toks is None:
            err(1, f"theme block missing: {name}")
    present = {k: v for k, v in blocks.items() if v}
    if present:
        names = set().union(*[set(v) for v in present.values()])
        for name, toks in present.items():
            missing = sorted(names - set(toks))
            if missing:
                err(1, f"theme block {name} is missing: {', '.join(missing)}")
    pairs = [
        ("dark (OS preference)", 'dark (data-theme="dark")'),
        ("light (:root)", 'light (data-theme="light")'),
        ('light (data-theme="light")', "print"),
    ]
    for a, b in pairs:
        if blocks.get(a) and blocks.get(b):
            diff = sorted(
                k for k in set(blocks[a]) & set(blocks[b]) if blocks[a][k] != blocks[b][k]
            )
            if diff:
                err(1, f"theme blocks {a} and {b} disagree on: {', '.join(diff)} — change all of them together")

    return errors, warns


def main(argv):
    if not argv:
        print(__doc__.strip().splitlines()[2].strip())
        return 2
    failed = False
    for path in argv:
        errors, warns = check(path)
        print(f"{path}: {len(errors)} error(s), {len(warns)} warning(s)")
        for line, msg in sorted(errors):
            print(f"  ERROR {path}:{line}  {msg}")
        for line, msg in sorted(warns):
            print(f"  WARN  {path}:{line}  {msg}")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
