"""Shared spec loading for component-arch-diagram: band "tone"s (the tinted look).

Tech-stack ("layer cake") specs with "mode": "stack" are no longer drawn here; they
belong to the tech-stack-diagram skill (~/.claude/skills/tech-stack-diagram).
"""
import json
import sys

# Pale band fill, band border, title colour, subtitle colour.
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

def apply_tone(band):
    """Fill in a band's colours from its "tone"; explicit colours still win."""
    t = band.get("tone")
    if t:
        fill, stroke, title, desc = TONES[t]
        band.setdefault("fill", fill); band.setdefault("stroke", stroke)
        band.setdefault("title_color", title); band.setdefault("desc_color", desc)
        band.setdefault("tinted", not band.get("caps"))
    return band



def load_spec(path):
    spec = json.load(open(path))
    if spec.get("mode") == "stack":
        sys.exit(f"{path} is a tech-stack (\"mode\": \"stack\") spec. Draw it with the tech-stack-diagram skill:\n"
                 f"  python3 ~/.claude/skills/tech-stack-diagram/scripts/stack_diagram.py {path} out.svg")
    for b in spec.get("bands", []):
        apply_tone(b)
    return spec
