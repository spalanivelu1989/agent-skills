# Saved reference voices

Use one in `podcast.json` as `"reference": "@<name>"` on a host with `"engine": "chatterbox"`.

| Name | Made from | Sound | Chosen for |
|---|---|---|---|
| `heart_expressive` | Kokoro `af_heart`, 10.8 s, rendered with the line below | Warm US female; under Chatterbox it is energetic and human | Default listener's-stand-in host (MAYA). A user picked it by ear from seven options after rejecting Kokoro-only female voices as dull. |

`heart_expressive` was rendered with:
> Honestly, I love this part of the job. You walk onto a plant floor, you ask one simple question,
> and suddenly everyone has an opinion. That is where the real story is.

Settings that went with it (podcast.json host `"emotions"`): neutral exaggeration 0.75 / cfg_weight
0.35, excited 0.9 / 0.3, calm 0.55 / 0.42, seed 11.

To add a voice: render a 10–12 s conversational line with a Kokoro voice (`_kokoro_worker.py` "ref"
mode, or set `"kokoro_voice"` on the host and `render` makes `refs/<host>.wav`), try it in a sampler,
and copy the clip here once a user approves it. Synthetic voices only: never a real person's recording.
