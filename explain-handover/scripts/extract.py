#!/usr/bin/env python3
"""Dump everything a reader could miss in a handed-over file, as plain text.

Stdlib only for .xlsx/.xlsm/.docx/.pptx/.md/.txt/code. PDF uses pypdf if it
imports, else the pdftotext/pdfinfo command-line tools.

Every content line carries a locator (cell, paragraph, slide, page, line) so
findings can be cited. The report opens with a UNITS index (sheets, headings,
slides, pages, types) for the coverage check, and ends with LOOSE ENDS:
placeholders, TODOs, question marks and "to be clarified" notes.

Usage: python3 -I extract.py FILE [FILE ...] [-o OUT] [--max-rows N] [--max-lines N]
"""
import argparse
import datetime
import hashlib
import os
import posixpath
import re
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

R_ID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
LOOSE = re.compile(
    r"\bTODO\b|\bFIXME\b|\bHACK\b|\bXXX\b|\bTBD\b|\bTBC\b|to be (?:clarified|confirmed|decided|agreed)"
    r"|\bplaceholder\b|lorem ipsum|\[insert|<insert|\?\s*\?|\s\?\s|will be updated|when agreed",
    re.I,
)
APP_KEYS = {"Application", "Company", "Manager", "Template", "Pages", "Slides", "HiddenSlides", "Notes"}
# In code, "??" and " ? " are operators (null-coalescing, ternary), not open questions.
LOOSE_CODE = re.compile(r"\bTODO\b|\bFIXME\b|\bHACK\b|\bXXX\b|\bTBD\b|\bplaceholder\b|lorem ipsum", re.I)
CODE_EXT = {".cs", ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".kt", ".go", ".rs", ".cpp", ".c",
            ".h", ".hpp", ".php", ".rb", ".swift", ".sql", ".sh", ".ps1", ".vb", ".abap", ".scala"}
OUTLINE = re.compile(
    r"^\s*(?:\[[^\]]+\]\s*)*(?:(?:public|private|protected|internal|static|sealed|abstract|partial|async|"
    r"override|virtual|export|default|final|open|data|pub|readonly)\s+)*"
    r"(?:namespace|class|interface|struct|enum|record|module|trait|impl|def|function|func|fn|CLASS|METHOD|FORM)\b"
    r"|^\s*(?:public|private|protected|internal)\s[^=;]*\w+\s*\([^;]*$"
)


def local(tag):
    return tag.rsplit("}", 1)[-1]


def kids(el, name):
    return [c for c in el if local(c.tag) == name]


def find_all(el, name):
    return [c for c in el.iter() if local(c.tag) == name]


def first(el, name):
    for c in el.iter():
        if local(c.tag) == name:
            return c
    return None


def attr(el, name):
    for k, v in el.attrib.items():
        if local(k) == name:
            return v
    return None


def texts(el, name="t"):
    return "".join(t.text or "" for t in el.iter() if local(t.tag) == name)


def col_letter(n):
    n, out = int(n), ""
    while n:
        n, r = divmod(n - 1, 26)
        out = chr(65 + r) + out
    return out


def one_line(s):
    return re.sub(r"\s*\n\s*", " / ", (s or "").strip())


class Pkg:
    """An OOXML zip: parts, relationships and core properties."""

    def __init__(self, path):
        self.z = zipfile.ZipFile(path)
        self.names = set(self.z.namelist())

    def xml(self, part):
        part = part.lstrip("/")
        return ET.fromstring(self.z.read(part)) if part in self.names else None

    def rels(self, part):
        d, b = posixpath.split(part.lstrip("/"))
        root = self.xml(posixpath.join(d, "_rels", b + ".rels"))
        out = {}
        if root is None:
            return out
        for r in root:
            tgt, mode = r.get("Target"), r.get("TargetMode")
            if mode != "External":
                tgt = tgt.lstrip("/") if tgt.startswith("/") else posixpath.normpath(posixpath.join(d, tgt))
            out[r.get("Id")] = (r.get("Type", "").rsplit("/", 1)[-1], tgt, mode == "External")
        return out

    def rel_of_type(self, part, kind):
        return [t for (k, t, ext) in self.rels(part).values() if k == kind and not ext]

    def core(self, emit):
        emit("== METADATA")
        for part in ("docProps/core.xml", "docProps/app.xml"):
            root = self.xml(part)
            if root is None:
                continue
            for c in root:
                keep = part.endswith("core.xml") or local(c.tag) in APP_KEYS
                if keep and (c.text or "").strip():
                    emit(f"  {local(c.tag)}: {c.text.strip()}")


# ---------------------------------------------------------------- xlsx
def do_xlsx(path, emit, units, a):
    p = Pkg(path)
    p.core(emit)
    wb = p.xml("xl/workbook.xml")
    wrels = p.rels("xl/workbook.xml")
    ss = []
    sroot = p.xml("xl/sharedStrings.xml")
    if sroot is not None:
        ss = [texts(si) for si in kids(sroot, "si")]
    dn = first(wb, "definedNames")
    if dn is not None:
        emit("== DEFINED NAMES")
        for d in dn:
            emit(f"  {d.get('name')}: {d.text}" + (" [hidden]" if d.get("hidden") == "1" else ""))
    ext_links = [t for (k, t, e) in wrels.values() if k == "externalLink"]
    if ext_links:
        emit(f"== EXTERNAL LINKS: {len(ext_links)} linked workbook(s) - values may come from other files")
    sheets = find_all(first(wb, "sheets"), "sheet")
    for sh in sheets:
        name, state = sh.get("name"), sh.get("state", "visible")
        kind, part, _ = wrels[sh.get(R_ID)]
        units.append(f"sheet: {name}" + ("" if state == "visible" else f" [{state.upper()}]"))
        emit("")
        emit(f"######## SHEET: {name}   state={state}   part={part}")
        root = p.xml(part)
        if root is None or kind != "worksheet":
            emit(f"  ({kind}; not a worksheet - charts or macros sheet)")
            continue
        srels = p.rels(part)
        dim = first(root, "dimension")
        if dim is not None:
            emit(f"  dimension: {dim.get('ref')}")
        if first(root, "sheetProtection") is not None:
            emit("  PROTECTED: sheet protection is on")
        hc = [col_letter(c.get("min")) + ("" if c.get("min") == c.get("max") else "-" + col_letter(c.get("max")))
              for c in find_all(root, "col") if c.get("hidden") == "1"]
        if hc:
            emit("  HIDDEN COLUMNS: " + ", ".join(hc))
        hr = [r.get("r") for r in find_all(root, "row") if r.get("hidden") == "1"]
        if hr:
            emit("  HIDDEN ROWS: " + ", ".join(hr[:60]) + (" ..." if len(hr) > 60 else ""))
        mc = [m.get("ref") for m in find_all(root, "mergeCell")]
        if mc:
            emit(f"  merged ranges: {len(mc)}")
        # comments, legacy and threaded
        notes = {}
        for cpart in p.rel_of_type(part, "comments"):
            croot = p.xml(cpart)
            authors = [one_line(x.text) for x in find_all(croot, "author")]
            for cm in find_all(croot, "comment"):
                aid = cm.get("authorId")
                who = authors[int(aid)] if aid and aid.isdigit() and int(aid) < len(authors) else ""
                notes[cm.get("ref")] = (who, texts(first(cm, "text")))
        for tpart in p.rel_of_type(part, "threadedComment"):
            for cm in find_all(p.xml(tpart), "threadedComment"):
                prev = notes.get(cm.get("ref"), ("", ""))
                notes[cm.get("ref")] = (prev[0] or "threaded", (prev[1] + " || " if prev[1] else "") + texts(cm, "text"))
        for dv in find_all(root, "dataValidation"):
            f1 = first(dv, "formula1")
            ref = dv.get("sqref") or texts(dv, "sqref")
            emit(f"  DROP-DOWN/VALIDATION {ref}: type={dv.get('type')} allowed={texts(f1, 'f') or (f1.text if f1 is not None else '')}"
                 + (f" prompt={one_line(dv.get('prompt'))}" if dv.get("prompt") else ""))
        for cf in find_all(root, "conditionalFormatting"):
            ref = cf.get("sqref") or texts(cf, "sqref")
            for rule in find_all(cf, "cfRule"):
                fs = [f.text for f in rule if local(f.tag) in ("formula", "f") and f.text]
                emit(f"  COLOUR RULE {ref}: {rule.get('type')} {rule.get('operator') or ''} {' ; '.join(fs)}".rstrip())
        for hl in find_all(root, "hyperlink"):
            tgt = srels.get(hl.get(R_ID), ("", hl.get("location") or "", False))[1]
            emit(f"  LINK {hl.get('ref')}: {tgt or hl.get('location')}")
        shown, total = 0, 0
        for row in find_all(root, "row"):
            total += 1
            if a.max_rows and total > a.max_rows:
                continue
            for c in kids(row, "c"):
                ref, t = c.get("r"), c.get("t")
                f, v, is_ = first(c, "f"), first(c, "v"), first(c, "is")
                val = v.text if v is not None else None
                if t == "s" and val is not None:
                    val = ss[int(val)]
                elif t == "inlineStr" and is_ is not None:
                    val = texts(is_)
                elif t == "b" and val is not None:
                    val = "TRUE" if val == "1" else "FALSE"
                line = None
                if f is not None and (f.text or f.get("t") == "shared"):
                    line = f"{ref}: ={f.text or '(shared formula)'}   -> computed: {val}"
                elif val not in (None, ""):
                    line = f"{ref}: {one_line(str(val))}"
                if ref in notes:
                    who, txt = notes.pop(ref)
                    line = (line or f"{ref}: (empty)") + f"   [COMMENT{' by ' + who if who else ''}: {one_line(txt)}]"
                if line:
                    emit("  " + line)
                    shown += 1
        if a.max_rows and total > a.max_rows:
            emit(f"  ... {total - a.max_rows} more rows not shown (re-run with --max-rows 0 for all)")
        for ref, (who, txt) in notes.items():
            emit(f"  {ref}: (no cell value)   [COMMENT{' by ' + who if who else ''}: {one_line(txt)}]")


# ---------------------------------------------------------------- docx
def para_text(p):
    out = []
    for el in p.iter():
        n = local(el.tag)
        if n == "t" and el.text:
            out.append(el.text)
        elif n == "delText" and el.text:
            out.append(f"[DELETED: {el.text}]")
        elif n == "tab":
            out.append("\t")
        elif n in ("br", "cr"):
            out.append(" / ")
        elif n == "commentReference":
            out.append(f"[C{attr(el, 'id')}]")
        elif n in ("footnoteReference", "endnoteReference"):
            out.append(f"[^{attr(el, 'id')}]")
    s = "".join(out)
    hidden = [texts(r) for r in find_all(p, "r") if first(r, "vanish") is not None and texts(r)]
    ins = [texts(i) for i in find_all(p, "ins") if texts(i)]
    if hidden:
        s += "   [HIDDEN TEXT: " + " | ".join(hidden) + "]"
    if ins:
        s += "   [TRACKED INSERTION: " + " | ".join(ins) + "]"
    return s


def do_docx(path, emit, units, a):
    p = Pkg(path)
    p.core(emit)
    styles = {}
    sroot = p.xml("word/styles.xml")
    if sroot is not None:
        for s in find_all(sroot, "style"):
            nm = first(s, "name")
            styles[attr(s, "styleId")] = attr(nm, "val") if nm is not None else attr(s, "styleId")
    body = first(p.xml("word/document.xml"), "body")
    emit("")
    emit("######## BODY")
    n = 0

    def walk(container, prefix=""):
        nonlocal n
        for el in container:
            tag = local(el.tag)
            if tag == "p":
                n += 1
                ps = first(el, "pStyle")
                style = styles.get(attr(ps, "val"), attr(ps, "val")) if ps is not None else ""
                txt = para_text(el)
                if not txt.strip():
                    continue
                m = re.match(r"(?i)heading\s*(\d)|title$", style or "")
                if m:
                    lvl = int(m.group(1)) if m.group(1) else 0
                    units.append(f"{'  ' * max(lvl - 1, 0)}heading: {txt.strip()}  (P{n})")
                    emit(f"P{n} {'#' * (lvl or 1)} {txt.strip()}   [style: {style}]")
                else:
                    bullet = "• " if first(el, "numPr") is not None else ""
                    emit(f"{prefix}P{n}: {bullet}{txt}" + (f"   [style: {style}]" if style and style != "Normal" else ""))
            elif tag == "tbl":
                emit(f"{prefix}TABLE (after P{n}):")
                for ri, tr in enumerate(kids(el, "tr"), 1):
                    cells = [one_line(" ".join(para_text(q) for q in find_all(tc, "p"))) for tc in kids(tr, "tc")]
                    emit(f"{prefix}  row {ri}: " + " | ".join(cells))
            elif tag == "sdt":
                pr = first(el, "sdtPr")
                label = attr(first(pr, "alias"), "val") or attr(first(pr, "tag"), "val") or "" if pr is not None else ""
                dd = [attr(li, "displayText") or attr(li, "value") for li in find_all(pr, "listItem")] if pr is not None else []
                cb = first(pr, "checked") if pr is not None else None
                desc = f"[FORM FIELD{' ' + label if label else ''}"
                if dd:
                    desc += f"; options: {', '.join(dd)}"
                if cb is not None:
                    desc += f"; checkbox checked={attr(cb, 'val')}"
                emit(f"{prefix}{desc}]")
                content = first(el, "sdtContent")
                if content is not None:
                    walk(content, prefix + "  ")

    walk(body)
    cm = p.xml("word/comments.xml")
    if cm is not None:
        emit("")
        emit("######## COMMENTS")
        for c in kids(cm, "comment"):
            emit(f"  C{attr(c, 'id')} by {attr(c, 'author')} {attr(c, 'date') or ''}: {one_line(' '.join(para_text(q) for q in find_all(c, 'p')))}")
    for kind in ("footnotes", "endnotes"):
        root = p.xml(f"word/{kind}.xml")
        if root is not None:
            items = [(attr(f, "id"), one_line(" ".join(para_text(q) for q in find_all(f, "p")))) for f in root]
            items = [(i, t) for i, t in items if t and i and int(i) > 0]
            if items:
                emit("")
                emit(f"######## {kind.upper()}")
                for i, t in items:
                    emit(f"  ^{i}: {t}")
    for part in sorted(x for x in p.names if re.match(r"word/(header|footer)\d*\.xml", x)):
        t = one_line(" ".join(para_text(q) for q in find_all(p.xml(part), "p")))
        if t:
            emit(f"{posixpath.basename(part)}: {t}")
    for (k, t, ext) in p.rels("word/document.xml").values():
        if ext and k == "hyperlink":
            emit(f"LINK: {t}")


# ---------------------------------------------------------------- pptx
def shape_lines(tree):
    out = []
    for el in tree:
        tag = local(el.tag)
        if tag == "grpSp":
            out += shape_lines(el)
        elif tag == "sp":
            nv = first(el, "cNvPr")
            ph = first(el, "ph")
            role = (ph.get("type") or "body") if ph is not None else "shape"
            if role in ("sldNum", "dt", "ftr"):
                continue
            paras = [texts(q) for q in find_all(el, "p") if local(q.tag) == "p"]
            paras = [x for x in paras if x.strip()]
            if paras:
                out.append(f"[{role}] {' / '.join(paras)}")
            elif nv is not None and nv.get("descr"):
                out.append(f"[{role} alt-text] {nv.get('descr')}")
        elif tag == "pic":
            nv = first(el, "cNvPr")
            out.append(f"[picture] {nv.get('name')}" + (f" alt-text: {nv.get('descr')}" if nv.get("descr") else " (no alt text)"))
        elif tag == "graphicFrame":
            tbl = first(el, "tbl")
            if tbl is not None:
                out.append("[table]")
                for ri, tr in enumerate(kids(tbl, "tr"), 1):
                    out.append(f"   row {ri}: " + " | ".join(one_line(texts(tc)) for tc in kids(tr, "tc")))
            elif first(el, "chart") is not None:
                out.append(f"[chart] {first(el, 'cNvPr').get('name')}")
            else:
                out.append(f"[object] {first(el, 'cNvPr').get('name')}")
    return out


def do_pptx(path, emit, units, a):
    p = Pkg(path)
    p.core(emit)
    pres = p.xml("ppt/presentation.xml")
    prels = p.rels("ppt/presentation.xml")
    ids = [(s.get("id"), prels[s.get(R_ID)][1]) for s in find_all(first(pres, "sldIdLst"), "sldId")]
    sections = {}
    for sec in find_all(pres, "section"):
        for sid in find_all(sec, "sldId"):
            sections[sid.get("id")] = sec.get("name")
    authors = {}
    ar = p.xml("ppt/commentAuthors.xml")
    if ar is not None:
        authors = {c.get("id"): c.get("name") for c in find_all(ar, "cmAuthor")}
    last_sec = None
    for i, (sid, part) in enumerate(ids, 1):
        root = p.xml(part)
        hidden = root.get("show") == "0"
        sec = sections.get(sid)
        if sec and sec != last_sec:
            emit("")
            emit(f"==== SECTION: {sec}")
            units.append(f"section: {sec}")
            last_sec = sec
        lines = shape_lines(first(root, "spTree"))
        title = next((l.split("] ", 1)[1] for l in lines if l.startswith(("[title]", "[ctrTitle]"))), "(no title)")
        units.append(f"  slide {i}: {title}" + (" [HIDDEN]" if hidden else ""))
        emit("")
        emit(f"######## SLIDE {i}{' [HIDDEN SLIDE]' if hidden else ''}")
        for l in lines:
            emit(f"  S{i} {l}")
        for npart in p.rel_of_type(part, "notesSlide"):
            nl = [l for l in shape_lines(first(p.xml(npart), "spTree")) if not l.startswith("[sldImg")]
            nl = [l.split("] ", 1)[1] for l in nl if l.startswith("[body]")]
            if nl:
                emit(f"  S{i} SPEAKER NOTES: {' / '.join(nl)}")
        for kind in ("comments", "comment", "modernComment"):
            for cpart in p.rel_of_type(part, kind):
                for c in find_all(p.xml(cpart), "cm"):
                    who = authors.get(c.get("authorId"), c.get("authorId") or "")
                    body = texts(c, "text") or texts(c)
                    emit(f"  S{i} COMMENT by {who}: {one_line(body)}")


# ---------------------------------------------------------------- pdf
def do_pdf(path, emit, units, a):
    try:
        from pypdf import PdfReader  # noqa: PLC0415
    except ImportError:
        PdfReader = None
    if PdfReader is None:
        if not shutil.which("pdftotext"):
            emit("!! Cannot read PDF: install pypdf in a venv (pip install pypdf) or poppler (pdftotext), "
                 "or use the pdf skill. Re-run with that venv's python.")
            return
        if shutil.which("pdfinfo"):
            emit("== METADATA")
            for l in subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout.splitlines():
                emit("  " + l)
        raw = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
        pages = raw.split("\f")
        emit("  (pdftotext fallback: annotations, form fields and bookmarks not read; install pypdf for those)")
        for i, pg in enumerate(pages, 1):
            if i == len(pages) and not pg.strip():
                break
            pdf_page(i, pg, emit, units, a)
        return
    r = PdfReader(path)
    emit("== METADATA")
    for k, v in (r.metadata or {}).items():
        emit(f"  {k.lstrip('/')}: {v}")
    emit(f"  pages: {len(r.pages)}   encrypted: {r.is_encrypted}")

    def outline(items, depth=0):
        for it in items:
            if isinstance(it, list):
                outline(it, depth + 1)
            else:
                try:
                    pg = r.get_destination_page_number(it) + 1
                except Exception:
                    pg = "?"
                units.append(f"{'  ' * depth}bookmark: {it.title}  (page {pg})")
    try:
        outline(r.outline)
    except Exception:
        pass
    fields = r.get_fields() or {}
    if fields:
        emit("== FORM FIELDS")
        for k, f in fields.items():
            emit(f"  {k}: value={f.get('/V')} type={f.get('/FT')}" + (f" options={f.get('/Opt')}" if f.get("/Opt") else ""))
    for i, page in enumerate(r.pages, 1):
        pdf_page(i, page.extract_text() or "", emit, units, a)
        for an in page.get("/Annots") or []:
            an = an.get_object()
            st, ct = an.get("/Subtype"), an.get("/Contents")
            if ct or st in ("/Text", "/FreeText", "/Highlight"):
                emit(f"  p{i} ANNOTATION {st}{' by ' + str(an.get('/T')) if an.get('/T') else ''}: {one_line(str(ct or ''))}")
            uri = (an.get("/A") or {}).get("/URI") if st == "/Link" else None
            if uri:
                emit(f"  p{i} LINK: {uri}")


def pdf_page(i, txt, emit, units, a):
    emit("")
    emit(f"######## PAGE {i}")
    lines = [l.rstrip() for l in txt.splitlines() if l.strip()]
    if not lines:
        emit(f"  p{i}: (no extractable text - likely a scanned image; OCR it with the pdf skill)")
    if not any(u.lstrip().startswith("bookmark") for u in units):
        units.append(f"page {i}: {lines[0].strip()[:80] if lines else '(image only)'}")
    for l in lines:
        emit(f"  p{i}: {l}")


# ---------------------------------------------------------------- text, markdown, code
def do_text(path, emit, units, a):
    ext = os.path.splitext(path)[1].lower()
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    emit(f"  lines: {len(lines)}")
    if ext in (".md", ".markdown"):
        if lines and lines[0].strip() == "---":
            end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
            if end:
                emit("== FRONT MATTER: " + " | ".join(lines[1:end]))
        fence = False
        for i, l in enumerate(lines, 1):
            if l.lstrip().startswith(("```", "~~~")):
                fence = not fence
            m = re.match(r"(#{1,6})\s+(.*)", l)
            if m and not fence:
                units.append(f"{'  ' * (len(m.group(1)) - 1)}heading: {m.group(2).strip()}  (L{i})")
        body = "\n".join(lines)
        for m in re.finditer(r"<!--(.*?)-->", body, re.S):
            ln = body[: m.start()].count("\n") + 1
            emit(f"  HIDDEN HTML COMMENT at L{ln}: {one_line(m.group(1))}")
        for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", body):
            emit(f"  LINK: {m.group(1)} -> {m.group(2)}")
    elif ext in CODE_EXT:
        imports = [f"L{i}: {l.strip()}" for i, l in enumerate(lines, 1)
                   if re.match(r"\s*(using\s+[\w.]+\s*;|import\s|from\s+\S+\s+import|#include|require\(|package\s)", l)]
        if imports:
            emit("== DEPENDENCIES (imports/usings)")
            for x in imports:
                emit("  " + x)
        for i, l in enumerate(lines, 1):
            if OUTLINE.match(l) and not l.strip().startswith(("//", "#", "*", "return", "if", "else")):
                units.append(f"L{i}: {l.strip()[:110]}")
    elif ext in (".csv", ".tsv"):
        sep = "\t" if ext == ".tsv" else ","
        if lines:
            units.append(f"table: {len(lines) - 1} data rows, columns: {lines[0][:200]}")
            emit(f"  columns ({lines[0].count(sep) + 1}): {lines[0]}")
    limit = a.max_lines or len(lines)
    emit("")
    emit("######## CONTENT")
    for i, l in enumerate(lines[:limit], 1):
        emit(f"L{i}: {l}")
    if len(lines) > limit:
        emit(f"... {len(lines) - limit} more lines not shown (re-run with --max-lines 0 for all)")


HANDLERS = {".xlsx": do_xlsx, ".xlsm": do_xlsx, ".docx": do_docx, ".docm": do_docx,
            ".pptx": do_pptx, ".pptm": do_pptx, ".pdf": do_pdf}
LEGACY = {".xls", ".doc", ".ppt", ".rtf", ".odt", ".ods", ".odp"}


def extract(path, a):
    out, units = [], []
    emit = out.append
    ext = os.path.splitext(path)[1].lower()
    st = os.stat(path)
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    head = [f"################ FILE: {os.path.abspath(path)}",
            f"type: {ext or '(none)'}   size: {st.st_size} bytes   modified: "
            f"{datetime.datetime.fromtimestamp(st.st_mtime):%Y-%m-%d %H:%M}",
            f"sha256: {sha}   (re-run at the end; it must not change)"]
    if ext in LEGACY:
        emit(f"!! Legacy format {ext}: convert a COPY first, e.g. "
             f"soffice --headless --convert-to {'xlsx' if ext in ('.xls', '.ods') else 'pptx' if ext in ('.ppt', '.odp') else 'docx'} "
             f"--outdir <scratch> '{path}' - then run this script on the converted copy.")
    else:
        try:
            HANDLERS.get(ext, do_text)(path, emit, units, a)
        except zipfile.BadZipFile:
            emit("!! Not a valid Office zip (encrypted / password-protected, or mislabelled). Ask for an unprotected copy.")
    pattern = LOOSE_CODE if ext in CODE_EXT else LOOSE
    loose = [l.strip() for l in out if pattern.search(l)]
    tail = ["", "######## LOOSE ENDS (placeholders, TODOs, open questions)"] + (
        ["  " + l[:300] for l in loose] or ["  (none found by pattern - still read for them)"])
    return head + ["", "######## UNITS (cover every one of these)"] + ["  " + u for u in units] + [""] + out + tail


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("-o", "--out", help="write the report here instead of stdout")
    ap.add_argument("--max-rows", type=int, default=400, help="rows per sheet (0 = all)")
    ap.add_argument("--max-lines", type=int, default=4000, help="lines per text file (0 = all)")
    a = ap.parse_args()
    report = []
    for f in a.files:
        report += extract(f, a) + ["", ""]
    text = "\n".join(report)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {a.out}: {len(report)} lines")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
