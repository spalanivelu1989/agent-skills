#!/usr/bin/env python3
"""Get a transcript for a video URL: existing captions first, then local Whisper.

Writes to --out: metadata.json, segments.json, transcript.txt and compact.txt.
Prints a JSON summary as its last line. Needs uvx (yt-dlp, Whisper) and ffmpeg.

    python3 -I transcribe.py URL --out DIR [--mode auto|captions|whisper]
    python3 -I transcribe.py --segments FILE --out DIR   # format existing segments
"""

from __future__ import annotations

import argparse
import html
import json
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

TIMING = re.compile(r"(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})\s+-->")
TAG = re.compile(r"<[^>]+>")


def run(command, cwd):
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True)


def yt_dlp(*args):
    # Without a JS runtime yt-dlp warns and may miss formats, so pass node if present.
    runtime = ["--js-runtimes", "node"] if shutil.which("node") else []
    return ["uvx", "yt-dlp", *runtime, "--no-playlist", "--no-progress", *args]


def parse_vtt(text):
    """Caption files repeat lines as they scroll, so keep only each cue's new lines."""
    segments, previous = [], []
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n")):
        lines = block.strip().split("\n")
        index = next((i for i, line in enumerate(lines) if TIMING.search(line)), None)
        if index is None:
            continue
        hours, minutes, seconds, millis = TIMING.search(lines[index]).groups()
        start = int(hours or 0) * 3600 + int(minutes) * 60 + int(seconds) + int(millis) / 1000
        cue = [html.unescape(TAG.sub("", line)).strip() for line in lines[index + 1 :]]
        cue = [line for line in cue if line]
        new = [line for line in cue if line not in previous]
        if new:
            segments.append({"start": start, "text": " ".join(new)})
        if cue:
            previous = cue
    return segments


def load_segments(path):
    """Accept Whisper JSON, a plain list, or a Supadata reply (offset in milliseconds)."""
    # strict=False tolerates raw line breaks inside text, which saved replies can contain.
    data = json.loads(Path(path).read_text(), strict=False)
    if isinstance(data, dict):
        data = data.get("segments") or data.get("content") or []
    if not isinstance(data, list):
        raise SystemExit(f"No timestamped segments found in {path}")
    segments = []
    for item in data:
        start = item["start"] if "start" in item else item.get("offset", 0) / 1000
        segments.append({"start": float(start), "text": item["text"].strip()})
    return segments


def clean(segments):
    """Collapse exact repeats: Whisper invents lines like 'Thank you.' over silence."""
    cleaned = []
    for segment in segments:
        text = re.sub(r"\s+", " ", segment["text"]).strip()
        if text and not (cleaned and cleaned[-1]["text"] == text):
            cleaned.append({"start": segment["start"], "text": text})
    return cleaned


def stamp(seconds):
    whole = int(seconds)
    return f"{whole // 3600}:{whole % 3600 // 60:02}:{whole % 60:02}"


def write_outputs(segments, out, block_seconds):
    (out / "segments.json").write_text(json.dumps(segments, indent=1, ensure_ascii=False))
    (out / "transcript.txt").write_text(" ".join(s["text"] for s in segments) + "\n")
    lines, current, block_start = [], [], 0.0
    for segment in segments:
        # Close the block before adding, so a line never sits under an earlier timestamp.
        if current and segment["start"] - block_start >= block_seconds:
            lines.append(f"[{stamp(block_start)}] " + " ".join(current))
            current = []
        if not current:
            block_start = segment["start"]
        current.append(segment["text"])
    if current:
        lines.append(f"[{stamp(block_start)}] " + " ".join(current))
    (out / "compact.txt").write_text("\n".join(lines) + "\n")
    return len(lines)


def fetch_metadata(url, out):
    result = run(yt_dlp("--dump-single-json", "--skip-download", url), out)
    if result.returncode != 0:
        return {"url": url, "error": result.stderr.strip()[-400:]}
    info = json.loads(result.stdout)
    fields = ("id", "title", "channel", "uploader", "upload_date", "duration", "webpage_url")
    metadata = {key: info.get(key) for key in fields}
    metadata["url"] = url
    metadata["manual_caption_languages"] = sorted(info.get("subtitles") or {})
    metadata["auto_caption_languages"] = len(info.get("automatic_captions") or {})
    return metadata


def fetch_captions(url, language, out):
    """Prefer captions written by people; fall back to YouTube's automatic ones."""
    folder = out / "captions"
    folder.mkdir(exist_ok=True)
    wanted = f"{language}.*,{language}" if language else "en.*,en"
    base = ["--skip-download", "--sub-langs", wanted, "--sub-format", "vtt/best"]
    for kind, flag in (("manual captions", "--write-subs"), ("automatic captions", "--write-auto-subs")):
        command = yt_dlp(*base, flag, "-o", str(folder / "caption.%(ext)s"), url)
        run(command, out)
        # Shortest name first, so "caption.en.vtt" beats variants like "caption.en-orig.vtt".
        files = sorted(folder.glob("*.vtt"), key=lambda path: len(path.name))
        if files:
            segments = parse_vtt(files[0].read_text(errors="replace"))
            if segments:
                return segments, kind
    return None, None


def whisper_command(audio, out, language, prompt, model):
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        command = [
            "uvx", "--from", "mlx-whisper", "mlx_whisper", str(audio),
            "--model", model or "mlx-community/whisper-large-v3-turbo",
            "--output-format", "json", "--output-dir", str(out),
            "--condition-on-previous-text", "False", "--verbose", "False",
        ]
        if language:
            command += ["--language", language]
        if prompt:
            command += ["--initial-prompt", prompt]
        return command
    command = [
        "uvx", "--from", "openai-whisper", "whisper", str(audio),
        "--model", model or "turbo",
        "--output_format", "json", "--output_dir", str(out),
        "--condition_on_previous_text", "False", "--verbose", "False",
    ]
    if language:
        command += ["--language", language]
    if prompt:
        command += ["--initial_prompt", prompt]
    return command


def transcribe_audio(url, out, language, prompt, model):
    # Keep downloads in their own folder, away from the scripts that read them.
    folder = out / "audio"
    folder.mkdir(exist_ok=True)
    existing = sorted(path for path in folder.glob("audio.*") if path.suffix != ".part")
    if not existing:
        # Low-bitrate audio is plenty for speech and much faster to download.
        command = yt_dlp(
            "-f", "bestaudio[abr<=80]/worstaudio/bestaudio",
            "-o", str(folder / "audio.%(ext)s"), url,
        )
        result = run(command, out)
        if result.returncode != 0:
            raise SystemExit(f"Audio download failed:\n{result.stderr.strip()[-800:]}")
        existing = sorted(path for path in folder.glob("audio.*") if path.suffix != ".part")
    audio = existing[0]
    result = run(whisper_command(audio, out, language, prompt, model), out)
    produced = out / f"{audio.stem}.json"
    if result.returncode != 0 or not produced.exists():
        raise SystemExit(f"Whisper failed:\n{result.stderr.strip()[-800:]}")
    return load_segments(produced)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", nargs="?")
    parser.add_argument("--out", required=True)
    parser.add_argument("--mode", choices=["auto", "captions", "whisper"], default="auto")
    parser.add_argument("--segments", help="Format an existing segments file instead of fetching")
    parser.add_argument("--language", help="ISO code such as en; Whisper detects it if omitted")
    parser.add_argument("--prompt", help="Names and terms that help Whisper spell things correctly")
    parser.add_argument("--model", help="Override the Whisper model")
    parser.add_argument("--block-seconds", type=int, default=45)
    args = parser.parse_args()
    if not args.url and not args.segments:
        parser.error("give a URL or --segments")

    out = Path(args.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    metadata = {}
    if args.segments:
        segments, source = load_segments(args.segments), "supplied segments"
    else:
        metadata = fetch_metadata(args.url, out)
        (out / "metadata.json").write_text(json.dumps(metadata, indent=1, ensure_ascii=False))
        segments, source = None, None
        if args.mode in ("auto", "captions"):
            segments, source = fetch_captions(args.url, args.language, out)
        if segments is None:
            if args.mode == "captions":
                raise SystemExit("No captions available for this video.")
            segments = transcribe_audio(args.url, out, args.language, args.prompt, args.model)
            source = "local Whisper"

    segments = clean(segments)
    if not segments:
        raise SystemExit("The transcript came back empty.")
    blocks = write_outputs(segments, out, args.block_seconds)
    print(
        json.dumps(
            {
                "source": source,
                "title": metadata.get("title"),
                "duration_seconds": metadata.get("duration"),
                "segments": len(segments),
                "compact_blocks": blocks,
                "compact_characters": (out / "compact.txt").stat().st_size,
                "out": str(out),
            }
        )
    )


if __name__ == "__main__":
    sys.exit(main())
