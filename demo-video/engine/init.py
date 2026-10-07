"""Set up (or refresh) a demo-video folder in a project.

    python3 ~/.claude/skills/demo-video/engine/init.py docs/demo-video

Copies the engine into <dir>/tools/ (always — the engine is not meant to be
edited per project, so re-running this upgrades it), and the templates
scenes.json, scenes.py and README.md into <dir>/ only if they do not exist.
Adds a .gitignore for the heavy outputs (clips/, pass1/, *.mp4).
"""
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
ENGINE = ["demo.py", "record.py", "voice.py", "build.py", "check.py", "explore.py",
          "kokoro_say.py", "tts_inspect.py", "setup_tts.sh"]
TEMPLATES = ["scenes.json", "scenes.py", "README.md"]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    dest = Path(sys.argv[1]).resolve()
    tools = dest / "tools"
    tools.mkdir(parents=True, exist_ok=True)
    for f in ENGINE:
        shutil.copy2(SKILL / "engine" / f, tools / f)
    print(f"engine → {tools}  ({len(ENGINE)} files)")
    for f in TEMPLATES:
        target = dest / f
        if target.exists():
            print(f"kept   {target.name} (exists)")
        else:
            shutil.copy2(SKILL / "templates" / f, target)
            print(f"new    {target.name}")
    gi = dest / ".gitignore"
    want = ["clips/", "pass1/", "*.mp4", "__pycache__/"]
    have = gi.read_text().split() if gi.exists() else []
    if missing := [w for w in want if w not in have]:
        gi.write_text("\n".join(have + missing) + "\n")
        print(f"gitignore +{' '.join(missing)}")
    print(f"""
Next:
  bash {tools}/setup_tts.sh                       # once per machine: local Kokoro voice + Whisper
  edit {dest}/scenes.py  (BASE_URL, login)
  python3 {tools}/explore.py / --tabs             # first pass: stills + page text in pass1/
  edit {dest}/scenes.json (story, voice-over, cues) and scenes.py (one function per scene)
  python3 {tools}/voice.py && python3 {tools}/record.py && python3 {tools}/build.py && python3 {tools}/check.py""")


if __name__ == "__main__":
    main()
