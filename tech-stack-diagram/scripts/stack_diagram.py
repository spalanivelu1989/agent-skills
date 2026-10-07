#!/usr/bin/env python3
"""Render a tech-stack ("layer cake") diagram from a small JSON spec.

    python3 stack_diagram.py spec.json out.svg            # write the SVG, print a fit report
    python3 stack_diagram.py spec.json out.svg --strict   # exit 1 if any text overflows

The spec lists layers top to bottom; each layer has a name, a one-line purpose and
2-3 capability cards (title = capability, sub = chosen technology). There are no
coordinates and no box-to-box links: the layout is computed here, and one arrow
between consecutive layers means "builds on / feeds the next layer".

    {"title": "Product — Application stack", "width": 1400, "per_row": 3,
     "layers": [{"name": "Experience", "desc": "Where analysts and admins work",
                 "tone": "terracotta", "arrow": "optional label",
                 "items": [{"title": "Web UI", "sub": "React + Vite"},
                           {"title": "LLM", "sub": "Claude Opus 5", "style": "dark"}]}],
     "legend": {"lines": ["optional footnote"]}}
"""
import html
import json
import sys

FONT = "-apple-system, Segoe UI, Helvetica, Arial, sans-serif"
INK, MUTED, LINE = "#1E2530", "#4A5563", "#56606E"
CARD = {"fill": "#FAFAF8", "stroke": "#D9D6D0"}
DARK = {"fill": "#2F2F33", "stroke": "#111111", "title": "#FFFFFF", "sub": "#D6D6DA"}

# Pale layer fill, layer border, title colour, purpose-line colour.
TONES = {
    "terracotta": ("#F8ECE8", "#B5735A", "#7A3418", "#9A4A2A"),
    "indigo":     ("#EEEDFB", "#8B84D6", "#3B348F", "#5650B5"),
    "teal":       ("#E5F3EE", "#5FA58A", "#1E5E47", "#2E7A5E"),
    "stone":      ("#F1EEE8", "#A39C90", "#3F3A33", "#5E574D"),
    "blue":       ("#E8F0FB", "#6E95CF", "#1F4A86", "#2F5FA3"),
    "amber":      ("#FBF3E2", "#C99A3E", "#6E4A0E", "#8A6018"),
    "rose":       ("#FBEAF0", "#C9708F", "#7A2343", "#9A3A5C"),
    "slate":      ("#EEF1F5", "#8A97A8", "#2A3646", "#4A5668"),
}
TONE_ORDER = ["terracotta", "indigo", "teal", "amber", "stone", "blue", "rose", "slate"]

# Geometry (px). Proven on the reference diagrams; change only with a reason.
MARGIN, PAD, GAP, ROW_GAP = 60, 52, 44, 24      # page margin, layer padding, gap between cards/layers, between card rows
TITLE_SIZE, SUB_SIZE = 26, 21                   # card title / subtitle
LAYER_TITLE, LAYER_DESC = 27, 21                # layer name / purpose line
esc = lambda t: html.escape(str(t), quote=False)


def layout(spec):
    """Compute every layer, card and arrow position. Shared by the SVG and PPTX writers."""
    W = spec.get("width", 1400)
    per_row = spec.get("per_row", 3)
    card_h = spec.get("card_h", 120)
    bw = W - 2 * MARGIN
    y = 100 if spec.get("title") else 48
    layers, cards, arrows = [], [], []
    n = len(spec["layers"])
    for li, L in enumerate(spec["layers"]):
        items = L.get("items", [])
        rows = [items[i:i + per_row] for i in range(0, len(items), per_row)] or [[]]
        head = 112 if L.get("desc") else 80
        h = head + len(rows) * card_h + (len(rows) - 1) * ROW_GAP + 26
        tone = L.get("tone", TONE_ORDER[li % len(TONE_ORDER)])
        fill, stroke, tcol, dcol = TONES[tone]
        layers.append({"name": L["name"], "desc": L.get("desc", ""), "x": MARGIN, "y": y, "w": bw, "h": h,
                       "fill": fill, "stroke": stroke, "title_color": tcol, "desc_color": dcol})
        for ri, row in enumerate(rows):
            cw = (bw - 2 * PAD - (len(row) - 1) * GAP) / max(len(row), 1)
            cy = y + head + ri * (card_h + ROW_GAP) + card_h / 2
            for ci, it in enumerate(row):
                dark = it.get("style") == "dark"
                cards.append({"title": it["title"], "sub": it.get("sub", ""), "dark": dark,
                              "x": MARGIN + PAD + ci * (cw + GAP), "y": cy - card_h / 2, "w": cw, "h": card_h,
                              "layer": L["name"]})
        if li < n - 1:
            arrows.append({"x": W / 2, "y0": y + h + 4, "y1": y + h + GAP - 4, "label": L.get("arrow")})
        y += h + GAP
    H = y - GAP + 48
    legend = None
    if spec.get("legend", {}).get("lines"):
        lines = spec["legend"]["lines"]
        legend = {"x": MARGIN, "y": y - GAP + 24, "w": bw, "h": 22 + 18 * len(lines), "lines": lines}
        H = legend["y"] + legend["h"] + 40
    return {"W": W, "H": H, "title": spec.get("title", ""), "layers": layers, "cards": cards,
            "arrows": arrows, "legend": legend}


def text_width(text, size, bold=False):
    """Rendered width, calibrated on the reference PNGs: ~0.43 em per character (0.51 bold), plus margin."""
    return len(text) * size * (0.54 if bold else 0.46)


def check(lay):
    problems = []
    for c in lay["cards"]:
        room = c["w"] - 28
        for t, size, bold in [(c["title"], TITLE_SIZE, True)] + [(s, SUB_SIZE, False) for s in c["sub"].split("\n") if s]:
            if text_width(t, size, bold) > room:
                problems.append(f'"{t}" may overflow its card in "{c["layer"]}" '
                                f'(~{text_width(t, size, bold):.0f}px for {room:.0f}px) — shorten it or lower per_row')
        if len([s for s in c["sub"].split("\n") if s]) > 2:
            problems.append(f'"{c["title"]}": more than two subtitle lines — the card is a label, not a paragraph')
    return problems


def render(lay):
    W, H = lay["W"], lay["H"]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">',
         f'<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{LINE}"/></marker></defs>',
         f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>']
    if lay["title"]:
        o.append(f'<text x="{W/2}" y="38" text-anchor="middle" font-size="24" font-weight="700" fill="{INK}">{esc(lay["title"])}</text>')
    for L in lay["layers"]:
        o.append(f'<rect x="{L["x"]}" y="{L["y"]}" width="{L["w"]}" height="{L["h"]}" rx="26" fill="{L["fill"]}" stroke="{L["stroke"]}" stroke-width="1.3"/>')
        o.append(f'<text x="{L["x"]+52}" y="{L["y"]+50}" font-size="{LAYER_TITLE}" font-weight="600" fill="{L["title_color"]}">{esc(L["name"])}</text>')
        if L["desc"]:
            o.append(f'<text x="{L["x"]+52}" y="{L["y"]+86}" font-size="{LAYER_DESC}" fill="{L["desc_color"]}">{esc(L["desc"])}</text>')
    for a in lay["arrows"]:
        o.append(f'<path d="M{a["x"]},{a["y0"]} L{a["x"]},{a["y1"]}" stroke="{LINE}" stroke-width="1.7" marker-end="url(#arr)"/>')
        if a["label"]:
            o.append(f'<text x="{a["x"]+12}" y="{(a["y0"]+a["y1"])/2+5}" font-size="14" fill="#37424F">{esc(a["label"])}</text>')
    for c in lay["cards"]:
        st = DARK if c["dark"] else {**CARD, "title": INK, "sub": MUTED}
        o.append(f'<rect x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{c["h"]}" rx="14" fill="{st["fill"]}" stroke="{st["stroke"]}" stroke-width="1.5"/>')
        cx, cy = c["x"] + c["w"] / 2, c["y"] + c["h"] / 2
        subs = [s for s in c["sub"].split("\n") if s]
        step = SUB_SIZE * 1.36
        ty = cy - len(subs) * step / 2 + TITLE_SIZE / 3
        o.append(f'<text x="{cx}" y="{ty}" text-anchor="middle" font-size="{TITLE_SIZE}" font-weight="700" fill="{st["title"]}">{esc(c["title"])}</text>')
        for i, s in enumerate(subs):
            o.append(f'<text x="{cx}" y="{ty + step*(i+1)}" text-anchor="middle" font-size="{SUB_SIZE}" fill="{st["sub"]}">{esc(s)}</text>')
    lg = lay["legend"]
    if lg:
        o.append(f'<rect x="{lg["x"]}" y="{lg["y"]}" width="{lg["w"]}" height="{lg["h"]}" rx="10" fill="#F8FAFC" stroke="#D5DCE4"/>')
        for i, t in enumerate(lg["lines"]):
            o.append(f'<text x="{lg["x"]+20}" y="{lg["y"]+23+i*18}" font-size="14" fill="{MUTED}">{esc(t)}</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    spec = json.load(open(sys.argv[1]))
    lay = layout(spec)
    open(sys.argv[2], "w").write(render(lay))
    problems = check(lay)
    print(f"wrote {sys.argv[2]} — {len(lay['layers'])} layers, {len(lay['cards'])} cards, {lay['W']}×{lay['H']:.0f}")
    print(f"problems: {len(problems)}")
    for p in problems:
        print("  -", p)
    if problems and "--strict" in sys.argv:
        sys.exit(1)
