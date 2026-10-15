#!/usr/bin/env bash
# One-time setup of Chatterbox TTS (Resemble AI, MIT licence) for the "hybrid" and "chatterbox"
# engines. Chatterbox clones a voice from a short reference clip and takes an emotion
# "exaggeration" per turn, so it sounds more human and more energetic than Kokoro, at about
# 4.5x real time on Apple Silicon (MPS).
#
#   bash setup_chatterbox.sh     # creates ~/.cache/demo-podcast-chatterbox (about 4 GB with models)
#
# Safe to re-run. Needs uv and Python 3.11. Kokoro (setup_tts.sh) is still needed: it voices the
# Kokoro hosts, makes reference clips and runs the Whisper checks.
set -euo pipefail

ENV="${CHATTERBOX_ENV:-$HOME/.cache/demo-podcast-chatterbox}"
command -v uv >/dev/null || { echo "Need uv: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }

[ -x "$ENV/bin/python" ] || uv venv "$ENV" --python 3.11 -q
export VIRTUAL_ENV="$ENV"
# setuptools<81: Resemble's Perth watermarker still imports pkg_resources.
uv pip install -q chatterbox-tts praat-parselmouth soundfile librosa "setuptools<81"

# Warm the model download so the first render starts quickly.
"$ENV/bin/python" - <<'EOF'
import warnings; warnings.filterwarnings("ignore")
import torch
from chatterbox.tts import ChatterboxTTS
dev = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
ChatterboxTTS.from_pretrained(device=dev)
print(f"Chatterbox ready on {dev}: $ENV")
EOF
