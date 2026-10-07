# From brief to story

Use this when the user gives meeting transcripts, notes or a brief, or when you have to propose the storyline yourself.

## 1. Synthesise the brief before touching the app

Read every transcript in full. Long `.vtt` files need condensing first:
- strip cue ids and timestamps;
- merge consecutive lines from the same speaker into turns;
- keep one timestamp per turn.

`.docx` converts with `textutil -convert txt -stdout file.docx` on macOS.

Write down, in this order:

| Question | Why it matters |
|---|---|
| **Who will watch, and what do they already know?** | It decides what to explain and what to skip. A steering committee that saw the concept last time needs results, not architecture. |
| **What does the person asking want them to believe at the end?** | It's usually one sentence. For example: "this condenses weeks of workshops into hours of decisions." |
| **What did they say must be shown, and in what order?** | It's often stated as a complaint about a previous attempt, e.g. "it has to be the gaps in the first view, not the workshop." |
| **Corrections made in the meeting** | Example: "that document is synthetic, we did not receive it". These are mandatory, because repeating the uncorrected version in front of the client is the worst outcome. |
| **Numbers that will be quoted** | Note how they were said, then verify them against the screen. A figure like "51% deviation" may really be 51.3% *alignment*, which is 48.7% divergence. Word them exactly as the tool computes them. |
| **Questions the audience asked or will ask** | Example: "is this AI-generated or computed?" Answer them in the story, not in Q&A. |
| **Claims that are estimates** | Examples: savings or time reductions. Mark them as estimates, or leave them out of the video. |

Show this synthesis to the user as a short brief and a proposed storyline before building anything.

## 2. A storyline that works for product output

1. **Hook (20–30 s).** Put the viewer in a situation, e.g. "Weeks before the rollout, you have one document…". State honestly what is real and what is synthetic.
2. **The verdict first (≈60 s).** Give the headline numbers from the summary screen. Show *how* they are computed: hover the formula, show the method. This answers the trust question early.
3. **The one-page view (≈30 s),** if the app has a brief or overview screen.
4. **One item end to end (60–90 s).** Choose the richest single record. Walk it top to bottom: comparison, impact, proposal, options, evidence, outcome. This is the heart of the video.
5. **The pattern across items (≈45 s).** Use one view that shows all items at once, then two contrasting examples. Pick the surprising one and the critical one.
6. **What happens next (≈45 s).** Show the workflow the output feeds, such as an agenda, a facilitator mode or an export. Hover action buttons; don't click them.
7. **Trust and traceability (≈20 s).** Sources, evidence and audit numbers.
8. **Close card (≈15 s).** Three or four takeaways. Use only claims you can stand behind.

Keep it to 6–8 minutes. If there is more, leave tabs out and say so in the README, so they can be shown live.

## 3. Writing the voice-over

- **Pacing:** write for about 150 words a minute. Kokoro speaks a little faster, and scenes stretch to fit the voice anyway.
- **Sentences:** short and declarative. One idea per sentence.
- **Cue phrases:** start each sentence that goes with a screen change with a distinctive phrase, e.g. "Hover the score…" or "Every claim is quoted…". That phrase becomes the cue.
- **Numbers:** say each number exactly as the screen shows it, and only numbers that are on screen in that scene.
- **Captions:** one per scene, under 90 characters. A caption is the claim, not a description of the screen.
- **Codes and acronyms:** write them for the eye, e.g. GAP-IN-RET-01 or SAP. Fix how they are said with `pronounce` rules in `scenes.json`, not in the text.
- **Honesty:** say "synthetic" when the data is, "estimate" when a figure is, and "in our dry run" for decisions that were not taken by the client.
