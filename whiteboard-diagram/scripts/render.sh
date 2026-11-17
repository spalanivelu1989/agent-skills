#!/usr/bin/env bash
# Render a whiteboard HTML/SVG file to PNG with headless Chrome.
# Usage: render.sh <board.html> <out.png> [scale]   (scale defaults to 2 -> 2752x1536)
set -euo pipefail

in="${1:?usage: render.sh <board.html> <out.png> [scale]}"
out="${2:?usage: render.sh <board.html> <out.png> [scale]}"
scale="${3:-2}"

chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [[ ! -x "$chrome" ]]; then
  chrome="$(command -v google-chrome || command -v chromium || command -v chromium-browser || true)"
fi
[[ -n "$chrome" ]] || { echo "Chrome or Chromium not found" >&2; exit 1; }

in_abs="$(cd "$(dirname "$in")" && pwd)/$(basename "$in")"
out_abs="$(cd "$(dirname "$out")" && pwd)/$(basename "$out")"

rm -f "$out_abs"
"$chrome" --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor="$scale" --window-size=1376,768 \
  --screenshot="$out_abs" "file://$in_abs" 2>/dev/null

[[ -s "$out_abs" ]] || { echo "Render failed: $out_abs was not written" >&2; exit 1; }
echo "Rendered $out_abs"
