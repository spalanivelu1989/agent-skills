#!/usr/bin/env python3
"""Render a research-paper HTML file to PDF, check it, and build page previews.

Usage:
    python3 -I render.py paper.html -o paper.pdf [--preview-dir DIR] [--cols 6]

Steps:
  1. Lint the HTML: leftover {{placeholders}}, citations that point at no
     reference, references never cited, Table/Figure numbering gaps or
     duplicates, captions not followed by their table, Contents vs headings.
  2. Print to PDF with headless Chrome (A4 comes from the page's @page rule).
  3. Report the page count, and pages whose last line looks like a stranded
     heading.
  4. Render every page as a thumbnail (pdftoppm) and stitch them into one
     contact sheet with headless Chrome, so the whole paper can be inspected
     as a single image. No Python imaging library is needed.

Exit code 1 if the lint finds errors (the PDF is still written).
Standard library only; needs Chrome and poppler (pdfinfo, pdftotext, pdftoppm).
"""
import argparse
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "chromium", "chromium-browser",
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        if os.path.isabs(c) and os.path.exists(c):
            return c
        if not os.path.isabs(c) and shutil.which(c):
            return shutil.which(c)
    sys.exit("Chrome or Chromium not found; install it or edit CHROME_CANDIDATES.")


def text_of(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def expand_cites(inner):
    nums = set()
    for part in re.split(r"[,;]", inner):
        part = part.strip()
        m = re.fullmatch(r"(\d+)\s*[–-]\s*(\d+)", part)
        if m:
            nums.update(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit():
            nums.add(int(part))
    return nums


def lint(src):
    errors, warnings = [], []
    src = re.sub(r"<!--.*?-->", "", src, flags=re.S)  # the template's component notes aren't content

    left = sorted(set(re.findall(r"\{\{[^}]*\}\}", src)))
    if left:
        errors.append(f"{len(left)} unfilled placeholder(s), e.g. {left[:3]}")

    # References: <ol start=N> blocks inside <div class="refs">
    refs_at = src.find('class="refs"')
    ref_nums = set()
    if refs_at == -1:
        errors.append('no <div class="refs"> references section')
    else:
        refs = src[refs_at:]
        end = refs.find("</div>")
        refs = refs[:end] if end != -1 else refs
        expected = 1
        for m in re.finditer(r"<ol(?:\s+start=\"(\d+)\")?[^>]*>(.*?)</ol>", refs, re.S):
            start = int(m.group(1) or 1)
            if start != expected:
                errors.append(f"reference list restarts at {start}, expected {expected}")
            n = len(re.findall(r"<li\b", m.group(2)))
            ref_nums.update(range(start, start + n))
            expected = start + n
        for li in re.findall(r"<li\b.*?</li>", refs, re.S):
            if 'class="u"' not in li and "http" not in li:
                warnings.append(f"reference without a URL: {text_of(li)[:70]}")

    body = src[:refs_at] if refs_at != -1 else src
    cited = set()
    for inner in re.findall(r'<span class="cite">\[([^\]]+)\]</span>', body):
        cited |= expand_cites(inner)
    missing = sorted(cited - ref_nums)
    if missing:
        errors.append(f"cited but not in References: {missing}")
    uncited = sorted(ref_nums - cited)
    if uncited:
        warnings.append(f"in References but never cited: {uncited}")

    # Table and figure numbering
    for kind in ("Table", "Figure"):
        nums = [int(n) for n in re.findall(rf'<p class="cap"><b>{kind} (\d+)\.</b>', src)]
        if nums and nums != list(range(1, len(nums) + 1)):
            errors.append(f"{kind} numbers out of sequence: {nums}")
        for n in set(nums):
            refs_in_text = len(re.findall(rf"\b{kind} {n}\b", text_of(src)))
            if refs_in_text < 2:  # the caption itself counts once
                warnings.append(f"{kind} {n} is never referred to in the text")
    for m in re.finditer(r'<p class="cap"><b>Table \d+\.</b>.*?</p>\s*(<\w+)', src, re.S):
        if m.group(1) != "<table":
            warnings.append(f"a Table caption is not directly above a <table>: {text_of(m.group(0))[:60]}")

    # Contents vs numbered headings
    toc = re.search(r'<div class="toc">(.*?)</div>\s*</div>|<div class="toc">(.*?)\n</div>', src, re.S)
    if toc:
        toc_nums = set(re.findall(r"<div>(\d+)\s", toc.group(0)))
        h2_nums = set(re.findall(r"<h2[^>]*>(\d+)\s", src))
        if toc_nums != h2_nums:
            errors.append(f"Contents and section headings differ: only in Contents {sorted(toc_nums - h2_nums, key=int)}, only in body {sorted(h2_nums - toc_nums, key=int)}")

    grades = re.findall(r'class="ev ([vacse])"', body)
    return errors, warnings, len(cited), len(ref_nums), len(grades)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def stranded_headings(pdf, pages):
    """Pages whose last text line is short and title-like (a heading left at the foot)."""
    hits = []
    for p in range(1, pages + 1):
        out = run(["pdftotext", "-f", str(p), "-l", str(p), "-layout", str(pdf), "-"]).stdout
        lines = [l.strip() for l in out.splitlines() if l.strip()]
        if len(lines) < 3:
            continue
        last = lines[-2] if lines[-1].isdigit() else lines[-1]  # skip the page number
        if "·" not in last and re.match(r"^(\d+(\.\d+)*\s+|Appendix |Table \d+\.|Figure \d+\.)", last) and len(last) < 90 and not last.endswith("."):
            hits.append((p, last))
    return hits


def contact_sheet(chrome, pdf, outdir, cols):
    outdir.mkdir(parents=True, exist_ok=True)
    for f in outdir.glob("p-*.png"):
        f.unlink()
    run(["pdftoppm", "-r", "30", "-png", str(pdf), str(outdir / "p")])
    thumbs = sorted(outdir.glob("p-*.png"))
    if not thumbs:
        return None
    # A4 at 30 dpi is about 248 x 351 px
    w, h, gap = 248, 351, 6
    rows = (len(thumbs) + cols - 1) // cols
    cells = "".join(
        f'<figure><img src="{t.name}"><figcaption>{i + 1}</figcaption></figure>'
        for i, t in enumerate(thumbs))
    page = (f"<!doctype html><style>body{{margin:0;background:#888;display:grid;"
            f"grid-template-columns:repeat({cols},{w}px);gap:{gap}px;padding:{gap}px}}"
            f"figure{{margin:0;position:relative}}img{{width:{w}px;height:{h}px;display:block;background:#fff}}"
            f"figcaption{{position:absolute;top:2px;left:4px;font:bold 14px sans-serif;color:#c00}}</style>{cells}")
    sheet_html = outdir / "sheet.html"
    sheet_html.write_text(page)
    sheet_png = outdir / "sheet.png"
    width = cols * (w + gap) + gap
    height = rows * (h + gap + 4) + gap
    run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         f"--window-size={width},{height}", f"--screenshot={sheet_png}", sheet_html.resolve().as_uri()])
    return sheet_png if sheet_png.exists() else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("-o", "--out", required=True, help="output PDF path")
    ap.add_argument("--preview-dir", help="where thumbnails and sheet.png go (default: <out>_preview)")
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--page", type=int, nargs="*", default=[],
                    help="also render these pages at 70 dpi for close inspection")
    a = ap.parse_args()

    src_path, pdf = Path(a.html).resolve(), Path(a.out).resolve()
    src = src_path.read_text(encoding="utf-8")
    errors, warnings, n_cited, n_refs, n_grades = lint(src)

    chrome = find_chrome()
    r = run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={pdf}", src_path.as_uri()])
    if not pdf.exists():
        sys.exit(f"PDF not written. Chrome said:\n{r.stderr[-2000:]}")

    info = run(["pdfinfo", str(pdf)]).stdout
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    words = len(run(["pdftotext", str(pdf), "-"]).stdout.split())

    print(f"PDF        {pdf}")
    print(f"Pages      {pages}   Words ≈ {words:,}")
    print(f"Citations  {n_cited} distinct reference numbers cited; {n_refs} references listed; {n_grades} evidence-grade tags")

    for p, line in stranded_headings(pdf, pages):
        warnings.append(f"page {p} may end on a stranded heading or caption: {line!r}")

    preview = Path(a.preview_dir) if a.preview_dir else pdf.with_name(pdf.stem + "_preview")
    sheet = contact_sheet(chrome, pdf, preview, a.cols)
    if sheet:
        print(f"Contact    {sheet}   (Read this image to inspect every page)")
    for p in a.page:
        run(["pdftoppm", "-r", "70", "-png", "-f", str(p), "-l", str(p), str(pdf), str(preview / "hi")])
    if a.page:
        print(f"Close-ups  {preview}/hi-*.png")

    for e in errors:
        print(f"ERROR      {e}")
    for w in warnings:
        print(f"WARN       {w}")
    if not errors and not warnings:
        print("Lint       clean")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
