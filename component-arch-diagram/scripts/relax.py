"""Give a hand-placed spec more breathing room without re-routing it.

    python3 relax.py in.spec.json out.spec.json [--sx 1.4] [--sy 1.6]

Boxes keep their size; only the space *between* them grows. Two piecewise-linear
maps (one for x, one for y) have slope 1 across every standard-size box and slope
sx / sy everywhere else, so:
  - a link that ends on a box edge still ends on that edge,
  - horizontal / vertical segments stay horizontal / vertical (no new diagonals),
  - column alignment is kept, because the maps are global.
Bands, groups, legend, actors, labels and junctions move with the same maps; boxes
wider or taller than the spec's default box (e.g. a shared runtime spanning three
columns) stretch with the gaps they cover. Stack-mode specs lay themselves out and
are refused (they belong to tech-stack-diagram).
"""
import argparse
import json


def build_map(intervals, k):
    """Return f(v): slope 1 inside the merged rigid intervals, slope k outside."""
    iv = sorted(intervals)
    merged = []
    for a, b in iv:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])

    def f(v):
        out, prev = 0.0, 0.0
        for a, b in merged:
            if v <= a:
                return out + (v - prev) * k
            out += (a - prev) * k
            if v <= b:
                return out + (v - a)
            out += b - a
            prev = b
        return out + (v - prev) * k
    return f


def relax(spec, sx, sy):
    if spec.get("mode") == "stack":
        raise SystemExit("relax.py: tech-stack specs are drawn by the tech-stack-diagram skill, which spaces its own layout")
    bw, bh = spec.get("box", {}).get("w", 200), spec.get("box", {}).get("h", 78)
    xs, ys = [], []
    for n in spec["nodes"]:
        w, h = n.get("w", bw), n.get("h", bh)
        if w <= bw:
            xs.append((n["cx"] - w / 2, n["cx"] + w / 2))
        if h <= bh:
            ys.append((n["cy"] - h / 2, n["cy"] + h / 2))
    fx, fy = build_map(xs, sx), build_map(ys, sy)
    P = lambda p: [round(fx(p[0]), 1), round(fy(p[1]), 1)]

    def rect(r, wkey="w", hkey="h"):
        x0, y0 = r["x"], r["y"]
        r["x"], r["y"] = round(fx(x0), 1), round(fy(y0), 1)
        if wkey in r:
            r[wkey] = round(fx(x0 + r[wkey]) - r["x"], 1)
        if hkey in r:
            r[hkey] = round(fy(y0 + r[hkey]) - r["y"], 1)

    # Canvas: stretch up to the last frame, then keep the original outer margin (the
    # legend's height is drawn by the renderer, so it must not be stretched either).
    c = spec["canvas"]
    frames = spec.get("bands", []) + spec.get("groups", []) + ([spec["legend"]["box"]] if spec.get("legend", {}).get("box") else [])
    right = max((f["x"] + f.get("w", 0) for f in frames), default=c["width"])
    lg0 = spec.get("legend", {}).get("box")
    bottom = lg0["y"] if lg0 else max((f["y"] + f.get("h", 0) for f in frames), default=c["height"])
    c["width"] = round(fx(right) + (c["width"] - right))
    tail = c["height"] - bottom
    if lg0:   # legend height as the renderer draws it, plus a 30 px margin below it
        lg = spec["legend"]
        tail = max(tail, 22 + 18 * len(lg.get("lines", [])) + (30 if lg.get("swatches") else 0) + 30)
    c["height"] = round(fy(bottom) + tail)
    for b in spec.get("bands", []) + spec.get("groups", []):
        rect(b)
    for n in spec["nodes"]:
        w, h = n.get("w", bw), n.get("h", bh)
        x0, x1 = fx(n["cx"] - w / 2), fx(n["cx"] + w / 2)
        y0, y1 = fy(n["cy"] - h / 2), fy(n["cy"] + h / 2)
        n["cx"], n["cy"] = round((x0 + x1) / 2, 1), round((y0 + y1) / 2, 1)
        if w > bw or "w" in n:
            n["w"] = round(x1 - x0, 1)
        if h > bh or "h" in n:
            n["h"] = round(y1 - y0, 1)
    for a in spec.get("actors", []):
        a["cx"], a["cy"] = P([a["cx"], a["cy"]])
    for lk in spec.get("links", []):
        lk["pts"] = [P(p) for p in lk["pts"]]
        if "label_at" in lk:
            lk["label_at"] = P(lk["label_at"])
    spec["junctions"] = [P(j) for j in spec.get("junctions", [])]
    for lb in spec.get("labels", []):
        lb["at"] = P(lb["at"])
    lg = spec.get("legend", {}).get("box")
    if lg:
        rect(lg)
    return spec


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--sx", type=float, default=1.4, help="gap stretch, horizontal")
    ap.add_argument("--sy", type=float, default=1.6, help="gap stretch, vertical")
    a = ap.parse_args()
    spec = relax(json.load(open(a.src)), a.sx, a.sy)
    json.dump(spec, open(a.dst, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {a.dst} — canvas {spec['canvas']['width']}×{spec['canvas']['height']}")
