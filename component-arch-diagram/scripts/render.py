#!/usr/bin/env python3
"""Render a layered, hand-routed component architecture diagram from a JSON spec.

    python3 render.py spec.json out.svg          # write the SVG and print the layout report
    python3 render.py spec.json out.svg --strict # exit 1 if the report finds any problem

The spec places every box and routes every link by hand (see SKILL.md). This
script only draws what it is told and checks it:
  - every link segment is horizontal or vertical
  - no link passes through a box it does not start or end in
  - which links cross each other (outside boxes) — aim for zero, accept a few
  - no label sits on a box or on another label
"""
import json, sys, html
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stack import load_spec

DEFAULT_KINDS = {
    "ui":    {"fill": "#EEF4FF", "stroke": "#6B8BC9"},
    "api":   {"fill": "#F1F5F9", "stroke": "#64748B"},
    "agent": {"fill": "#FFF7E8", "stroke": "#C8913A"},
    "svc":   {"fill": "#F3EEFF", "stroke": "#8C6BC9"},
    "data":  {"fill": "#EAF4EC", "stroke": "#5B8F66"},
    "model": {"fill": "#EAF7F7", "stroke": "#3F9A9A"},
    "eval":  {"fill": "#FFF0F3", "stroke": "#C9546E"},
    "ops":   {"fill": "#FFF8E1", "stroke": "#B8962E"},
    "ext":   {"fill": "#2F2F33", "stroke": "#111111", "dark": True},
}
FONT = "-apple-system, Segoe UI, Helvetica, Arial, sans-serif"
LINE = "#56606E"
esc = lambda t: html.escape(str(t), quote=False)


def load(path):
    spec = load_spec(path)   # applies band "tone"s; refuses stack specs
    spec.setdefault("kinds", {})
    kinds = dict(DEFAULT_KINDS); kinds.update(spec["kinds"]); spec["kinds"] = kinds
    box = spec.get("box", {}); bw, bh = box.get("w", 200), box.get("h", 78)
    for n in spec["nodes"]:
        n.setdefault("w", bw); n.setdefault("h", bh); n.setdefault("shape", "rect"); n.setdefault("sub", "")
        n.setdefault("ts", box.get("title_size", 15)); n.setdefault("ss", box.get("sub_size", 12.5)); n.setdefault("rx", box.get("rx", 10))
    return spec


def rect_of(n):
    return (n["cx"] - n["w"] / 2, n["cy"] - n["h"] / 2, n["cx"] + n["w"] / 2, n["cy"] + n["h"] / 2)


def inside(pt, r, pad=0):
    return r[0] - pad < pt[0] < r[2] + pad and r[1] - pad < pt[1] < r[3] + pad


def label_rect(lb):
    """Approximate a label's box from its text (12px font ≈ 6.4px per character)."""
    x, y = lb["at"]; w = 6.4 * len(lb["text"]) + 4; a = lb.get("anchor", "start")
    x0 = x - (w / 2 if a == "middle" else w if a == "end" else 0)
    return (x0, y - 11, x0 + w, y + 3)


# ---------------------------------------------------------------- drawing
def draw_box(out, n, kinds):
    k = kinds[n["kind"]]; x0, y0, x1, y1 = rect_of(n); w, h = n["w"], n["h"]
    shape = n["shape"]; dark = k.get("dark") or shape == "cloud"
    fill, stroke = ("#2F2F33", "#111111") if shape == "cloud" else (k["fill"], k["stroke"])
    ty = n["cy"]
    if shape == "cyl":
        e = 9
        out.append(f'<path d="M{x0},{y0+e} A{w/2},{e} 0 0 1 {x1},{y0+e} V{y1-e} A{w/2},{e} 0 0 1 {x0},{y1-e} Z" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        out.append(f'<path d="M{x0},{y0+e} A{w/2},{e} 0 0 0 {x1},{y0+e}" fill="none" stroke="{stroke}" stroke-width="1.5"/>')
        ty += 2
    elif shape == "folder":
        out.append(f'<path d="M{x0},{y0+10} V{y0+4} Q{x0},{y0} {x0+4},{y0} H{x0+60} L{x0+70},{y0+10} H{x1-6} Q{x1},{y0+10} {x1},{y0+16} V{y1-6} Q{x1},{y1} {x1-6},{y1} H{x0+6} Q{x0},{y1} {x0},{y1-6} Z" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        ty += 3
    elif shape == "hex":   # decision
        k0 = 20
        out.append(f'<path d="M{x0+k0},{y0} H{x1-k0} L{x1},{n["cy"]} L{x1-k0},{y1} H{x0+k0} L{x0},{n["cy"]} Z" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')
    else:
        rx = 30 if shape == "cloud" else n["rx"]
        out.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    tc, sc = ("#FFFFFF", "#D6D6DA") if dark else ("#1E2530", "#4A5563")
    lines = [l for l in n["sub"].split("\n") if l] if n["sub"] else []
    ts, ss = n["ts"], n["ss"]; step = ss * 1.36
    y = ty - len(lines) * step / 2 + ts / 3
    out.append(f'<text x="{n["cx"]}" y="{y}" text-anchor="middle" font-size="{ts}" font-weight="700" fill="{tc}">{esc(n["title"])}</text>')
    for i, l in enumerate(lines):
        out.append(f'<text x="{n["cx"]}" y="{y + step*(i+1)}" text-anchor="middle" font-size="{ss}" fill="{sc}">{esc(l)}</text>')


# Optional spec "link_style": {"color": "#A3AAB4", "head": "open", "corners": "square", "width": 1.5}
# — open chevron arrowheads, sharp right-angle corners. Omitted: filled heads, rounded corners.
STYLE = {}


def draw_link(out, lk):
    pts = lk["pts"]; r = 0 if STYLE.get("corners") == "square" else 10
    d = f"M{pts[0][0]},{pts[0][1]}"
    for i in range(1, len(pts) - 1):
        (x0, y0), (x1, y1), (x2, y2) = pts[i-1], pts[i], pts[i+1]
        def toward(ax, ay, bx, by):
            L = max(abs(bx-ax), abs(by-ay)) or 1; dd = min(r, L/2)
            return ax + (bx-ax)/L*dd, ay + (by-ay)/L*dd
        if r == 0:
            d += f" L{x1},{y1}"
            continue
        a = toward(x1, y1, x0, y0); b = toward(x1, y1, x2, y2)
        d += f" L{a[0]:g},{a[1]:g} Q{x1},{y1} {b[0]:g},{b[1]:g}"
    d += f" L{pts[-1][0]},{pts[-1][1]}"
    color = lk.get("color", STYLE.get("color", LINE))
    marker = f' marker-end="url(#arr{color.lstrip("#")})"' if lk.get("arrow", True) else ""
    dash = ' stroke-dasharray="6 5"' if lk.get("dashed") else ""
    join = ' stroke-linejoin="miter"' if r == 0 else ""
    out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{STYLE.get("width", 1.7)}"{join}{marker}{dash}/>')


def draw_label(out, lb):
    x, y = lb["at"]
    out.append(f'<text x="{x}" y="{y}" text-anchor="{lb.get("anchor", "start")}" font-size="12" fill="{lb.get("color", "#37424F")}" class="lbl">{esc(lb["text"])}</text>')


def render(spec):
    W, H = spec["canvas"]["width"], spec["canvas"]["height"]; out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
    STYLE.clear(); STYLE.update(spec.get("link_style", {}))
    base = STYLE.get("color", LINE)
    colors = sorted({lk.get("color", base) for lk in spec["links"]} | {base})
    if STYLE.get("head") == "open":   # open chevron, drawn with the line's own stroke
        markers = "".join(f'<marker id="arr{c.lstrip("#")}" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M1,1 L11,6 L1,11" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>' for c in colors)
    else:
        markers = "".join(f'<marker id="arr{c.lstrip("#")}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for c in colors)
    out.append(f'<defs>{markers}<style>.lbl{{paint-order:stroke;stroke:#FFFFFF;stroke-width:5px;stroke-linejoin:round}}</style></defs>')
    out.append(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')
    if spec.get("title"):
        out.append(f'<text x="{W/2}" y="38" text-anchor="middle" font-size="24" font-weight="700" fill="#1E2530">{esc(spec["title"])}</text>')
    for b in spec.get("bands", []):
        fill, stroke = b.get("fill", "#FBFCFE"), b.get("stroke", "#C9D1DB")
        out.append(f'<rect x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" rx="{b.get("rx", 14)}" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>')
        if b.get("caps"):   # stacked-layer style: spaced caps title across the top, optional one-line summary
            out.append(f'<text x="{b["x"]+28}" y="{b["y"]+36}" font-size="19" font-weight="800" letter-spacing="3.5" fill="{b.get("title_color", "#1E2530")}">{esc(b["name"].upper())}</text>')
            if b.get("desc"):
                out.append(f'<text x="{b["x"]+28}" y="{b["y"]+60}" font-size="14" fill="{b.get("desc_color", "#4A5563")}">{esc(b["desc"])}</text>')
            continue
        if b.get("tinted"):   # tinted-band style: sentence-case title and purpose line in the band's own colour
            out.append(f'<text x="{b["x"]+52}" y="{b["y"]+50}" font-size="27" font-weight="600" fill="{b.get("title_color", "#1E2530")}">{esc(b["name"])}</text>')
            if b.get("desc"):
                out.append(f'<text x="{b["x"]+52}" y="{b["y"]+86}" font-size="21" fill="{b.get("desc_color", "#4A5563")}">{esc(b["desc"])}</text>')
            continue
        out.append(f'<text x="{b["x"]+20}" y="{b["y"]+30}" font-size="13" font-weight="700" fill="#5B6B7F">{esc(b["n"])}</text>')
        for i, part in enumerate(b["name"].split("\n")):
            out.append(f'<text x="{b["x"]+20}" y="{b["y"]+50+i*18}" font-size="15" font-weight="700" fill="#1E2530">{esc(part)}</text>')
    for g in spec.get("groups", []):
        out.append(f'<rect x="{g["x"]}" y="{g["y"]}" width="{g["w"]}" height="{g["h"]}" rx="14" fill="#FBFCFE" stroke="#C9D1DB" stroke-width="1.3"/>')
        out.append(f'<text x="{g["x"]+16}" y="{g["y"]+26}" font-size="15" font-weight="700" fill="#1E2530"><tspan fill="#5B6B7F" font-size="13">{esc(g["n"])}  </tspan>{esc(g["name"])}</text>')
    for lk in spec["links"]:
        draw_link(out, lk)
    for j in spec.get("junctions", []):
        out.append(f'<circle cx="{j[0]}" cy="{j[1]}" r="3.5" fill="{base}"/>')
    for lk in spec["links"]:
        if lk.get("label"):
            draw_label(out, {"text": lk["label"], "at": lk["label_at"], "anchor": lk.get("anchor", "start"),
                             "color": lk.get("color", "#37424F") if lk.get("color") else "#37424F"})
    for lb in spec.get("labels", []):
        draw_label(out, lb)
    for a in spec.get("actors", []):
        x, y = a["cx"], a["cy"] - 25
        if a.get("style") == "bust":   # user icon: head and shoulders only
            c = a.get("color", "#3B4A5E")
            out.append(f'<circle cx="{x}" cy="{y+4}" r="12" fill="{c}"/>'
                       f'<path d="M{x-22},{y+44} C{x-22},{y+26} {x-12},{y+19} {x},{y+19} C{x+12},{y+19} {x+22},{y+26} {x+22},{y+44} Z" fill="{c}"/>')
        else:
            out.append(f'<circle cx="{x}" cy="{y}" r="11" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.6"/>'
                       f'<path d="M{x},{y+11} V{y+35} M{x-18},{y+20} H{x+18} M{x},{y+35} L{x-14},{y+54} M{x},{y+35} L{x+14},{y+54}" stroke="{LINE}" stroke-width="1.6" fill="none"/>')
        for i, part in enumerate(a["label"].split("\n")):
            out.append(f'<text x="{x+35}" y="{y+22+i*17}" font-size="14" font-weight="700" fill="#1E2530">{esc(part)}</text>')
    for n in spec["nodes"]:
        draw_box(out, n, spec["kinds"])
    lg = spec.get("legend")
    if lg:
        b = lg["box"]; lines = lg.get("lines", []); sw = lg.get("swatches", [])
        hgt = 22 + 18 * len(lines) + (26 if sw else 0)
        out.append(f'<rect x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{hgt}" rx="10" fill="#F8FAFC" stroke="#D5DCE4"/>')
        x, y = b["x"] + 20, b["y"] + 12
        if sw:   # colour key: one chip per kind, e.g. the role that owns a process step
            for s_ in sw:
                k = spec["kinds"][s_["kind"]]
                out.append(f'<rect x="{x}" y="{y}" width="22" height="14" rx="4" fill="{k["fill"]}" stroke="{k["stroke"]}" stroke-width="1.4"/>')
                out.append(f'<text x="{x+28}" y="{y+11}" font-size="12.5" fill="#1E2530">{esc(s_["text"])}</text>')
                x += 28 + 7 * len(s_["text"]) + 22
            y += 26
        for i, t in enumerate(lines):
            out.append(f'<text x="{b["x"]+20}" y="{y+11+i*18}" font-size="12.5" fill="#4A5563">{esc(t)}</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------------------------------------------------------------- checks
def check(spec):
    nodes = {n["id"]: rect_of(n) for n in spec["nodes"]}
    W, H = spec["canvas"]["width"], spec["canvas"]["height"]
    problems = []
    def owners(pt, pad=0):
        return {i for i, r in nodes.items() if inside(pt, r, pad)}
    for li, lk in enumerate(spec["links"]):
        name = lk.get("name") or lk.get("label") or f"link #{li}"
        pts = lk["pts"]; ends = owners(pts[0], 8) | owners(pts[-1], 8)   # links may start/end on a box edge
        for p, q in zip(pts, pts[1:]):
            if p[0] != q[0] and p[1] != q[1]:
                problems.append(f"diagonal segment in '{name}': {p} -> {q}")
            for i, r in nodes.items():
                if i in ends: continue
                if any(inside((p[0] + (q[0]-p[0])*t/40, p[1] + (q[1]-p[1])*t/40), r, 6) for t in range(41)):
                    problems.append(f"'{name}' runs through box {i}")
        for p in pts:
            if not (0 <= p[0] <= W and 0 <= p[1] <= H):
                problems.append(f"'{name}' leaves the canvas at {p}")
    crossings = []
    segs = [(li, s) for li, lk in enumerate(spec["links"]) for s in zip(lk["pts"], lk["pts"][1:])]
    for a in range(len(segs)):
        for b in range(a + 1, len(segs)):
            (la, (p, q)), (lb, (u, v)) = segs[a], segs[b]
            if la == lb: continue
            h1, h2 = p[1] == q[1], u[1] == v[1]
            if h1 == h2: continue
            (hp, hq), (vp, vq) = ((p, q), (u, v)) if h1 else ((u, v), (p, q))
            x, y = vp[0], hp[1]
            if min(hp[0], hq[0]) + 1 < x < max(hp[0], hq[0]) - 1 and min(vp[1], vq[1]) + 1 < y < max(vp[1], vq[1]) - 1:
                if not owners((x, y)):
                    crossings.append((x, y))
    labels = [(lk["label"], label_rect({"text": lk["label"], "at": lk["label_at"], "anchor": lk.get("anchor", "start")}))
              for lk in spec["links"] if lk.get("label")] + [(lb["text"], label_rect(lb)) for lb in spec.get("labels", [])]
    for t, r in labels:
        for i, nr in nodes.items():
            if r[0] < nr[2] and r[2] > nr[0] and r[1] < nr[3] and r[3] > nr[1]:
                problems.append(f"label '{t}' overlaps box {i}")
    for a in range(len(labels)):
        for b in range(a + 1, len(labels)):
            r, s = labels[a][1], labels[b][1]
            if r[0] < s[2] and r[2] > s[0] and r[1] < s[3] and r[3] > s[1]:
                problems.append(f"labels '{labels[a][0]}' and '{labels[b][0]}' overlap")
    return problems, sorted(set(crossings))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    spec = load(sys.argv[1])
    open(sys.argv[2], "w").write(render(spec))
    problems, crossings = check(spec)
    print(f"wrote {sys.argv[2]} — {len(spec['nodes'])} boxes, {len(spec['links'])} links")
    print(f"problems: {len(problems)}"); [print("  -", p) for p in problems]
    print(f"crossings (outside boxes): {len(crossings)}"); [print("  -", c) for c in crossings]
    if "--strict" in sys.argv and problems:
        sys.exit(1)
