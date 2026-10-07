#!/usr/bin/env python3
"""Time a demo script from its narration, so the numbers come from words, not guesses.

    python3 timing.py script.md            # print each row's time and the total
    python3 timing.py script.md --write    # also rewrite the (m:ss–m:ss) times in the table
    python3 timing.py script.md --wpm 140 --action 2

Reads the first Markdown table whose header has a "Narration" column. Each row takes:
  words in its narration ÷ wpm  +  --action seconds (on-screen moves around the words)
A row whose narration is "—" or empty is a pause or silent action: it takes the seconds given in its
label, e.g. "*Pause* (2s)", or --pause seconds. Times are rounded to whole seconds.
"""
import argparse
import re
import sys
from pathlib import Path

TIME = re.compile(r"\((?:\s*\d+:\d{2}\s*[–-]\s*\d+:\d{2}\s*|…|\.\.\.)\)")


def words(text):
    text = re.sub(r"[*_`\"“”]", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return len(re.findall(r"[A-Za-z0-9][\w'’./-]*", text))


def mmss(s):
    s = int(round(s))
    return f"{s // 60}:{s % 60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--wpm", type=float, default=150)
    ap.add_argument("--action", type=float, default=1.5, help="seconds of screen action per spoken row")
    ap.add_argument("--pause", type=float, default=2.0, help="seconds for a silent row with no stated length")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    path = Path(a.script)
    lines = path.read_text().splitlines()
    head = next((i for i, l in enumerate(lines)
                 if l.lstrip().startswith("|") and "narration" in l.lower()), None)
    if head is None:
        sys.exit("no table with a Narration column found")
    cols = [c.strip().lower() for c in lines[head].strip().strip("|").split("|")]
    narr = next(i for i, c in enumerate(cols) if "narration" in c)

    t, rows = 0.0, []
    for i in range(head + 2, len(lines)):
        line = lines[i]
        if not line.lstrip().startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) <= narr:
            continue
        label, spoken = cells[0], cells[narr]
        n = words(spoken) if spoken not in ("", "—", "-") else 0
        if n:
            dur = n / a.wpm * 60 + a.action
        else:
            m = re.search(r"(\d+(?:\.\d+)?)\s*s\b", label)
            dur = float(m.group(1)) if m else a.pause
        start, t = t, t + dur
        rows.append((re.sub(r"[*]", "", TIME.sub("", label)).strip(), n, start, t))
        if a.write:
            stamp = f"({mmss(start)}–{mmss(t)})"
            first = line.split("|")[1]
            new_first = TIME.sub(stamp, first) if TIME.search(first) else first.rstrip() + f" {stamp} "
            lines[i] = line.replace(first, new_first, 1)

    for label, n, s, e in rows:
        print(f"  {label:<40} {n:>4} words  {mmss(s)}–{mmss(e)}")
    print(f"total {mmss(t)}  ({sum(r[1] for r in rows)} words at {a.wpm:g} wpm, +{a.action:g}s per spoken row)")
    if a.write:
        path.write_text("\n".join(lines) + "\n")
        print(f"times written to {path}")


if __name__ == "__main__":
    main()
