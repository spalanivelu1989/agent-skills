# Writing a two-host episode

## Shape
A 30-minute episode that worked (examples/infor-summit): ten chapters of roughly three minutes.
The energetic v2 (examples/infor-summit-v2) used twelve chapters of about two and a half minutes.

| # | Chapter | Job |
|---|---|---|
| 1 | Welcome | Who the hosts are, the AI-voice disclosure, the source date, the map of the episode, one striking sourced result as a hook |
| 2 | The problem, in the audience's words | The blockers people actually say, then which answer fits each |
| 3 | A simple model | One framework (a journey, three steps) the rest of the episode hangs on |
| 4 | One map | Every offering or concept in exactly one box; repeat the one-sentence version back |
| 5–6 | How it works | Walk the boxes in order, with one end-to-end example each; one illustrative scenario, labelled |
| 7 | For you specifically | Industry by industry, role by role, or segment by segment |
| 8 | Trust and objections | Safety, control, "what if it's wrong", the two or three objections buyers raise |
| 9 | Proof and next steps | Published results; a readiness check; how to pick a first step |
| 10 | Wrap-up | Each host's thirty-second summary, one caution, one question for the listener |

Scale it: a 10-minute episode keeps 1, 2, 4, one "how it works", 9 and 10, at the same pace.

## Energetic discovery style (what users asked for)
A calm Q&A was called "dull and robotic". What fixed it:
- **Discovery, not lecture:** the stand-in figures things out aloud ("Wait, so the agent drafts it
  and I approve it?"), connects to her own experience ("I've said all three of those. Out loud.
  In meetings."), and pushes back ("Okay, let me play the sceptic.").
- **Reactions with content:** "Three thousand hours. That's people's time back." Laughter as "Ha!".
- **Delivery tags:** `NAME (excited): …` for hooks and big numbers, `NAME (calm): …` for the AI
  disclosure and governance; about one turn in four tagged.
- **`[overlap]`** before a quick interjection (a few per episode) so turns don't queue politely.
- **Short chapters with a cold open:** start the welcome on the most striking sourced result.
- Example: `examples/infor-summit-v2/podcast-script.md` (12 chapters, 263 turns, 30.4 min).

## Lines the voices stumble on
| Line | Problem | Write instead |
|---|---|---|
| "Been there." / "And?" / "Any more?" / "Ninety-five!" (Chatterbox host) | Repeats, fillers or garbling | "Oh, I have been there." / "And then what?" / "Got any more?" / "Wow. Ninety-five percent faster!" |
| "And fashion?" / "And box four?" (Kokoro) | The leading "And" is swallowed ("In fashion?") | "What about fashion?" / "And... box four?" |

## Hosts
- **The listener's stand-in** (e.g. MAYA) asks short, concrete questions in the audience's words, plays
  the sceptic for objections, repeats things back ("Let me repeat it back…"), and lands the takeaways.
- **The specialist** (e.g. SAM) answers in one to four sentences, uses the source's own phrasing for
  claims, and says "that's on the roadmap" or "let's confirm it for your product" when that is the truth.
- In the example episode the specialist carried 78 % of the words and it still worked, because the
  stand-in asked a question every one to three turns. For a more balanced feel, aim for 60–70 %. Neither
  host monologues: split anything longer than five sentences with a question, a reaction or a repeat-back.

## Turns that sound like people
- Open chapters with a question, not a heading read aloud.
- Use reactions sparingly and only when they carry meaning: "Three thousand hours. That's people's time back."
- Concrete beats abstract: name the customer, the process, the number, the time it took.
- Signpost: "Box one is…", "Second…", "Here's an illustration, not a real screenshot."
- Repeat-backs are the best memory aid: one per big idea.
- End each chapter on a takeaway line, then `[pause 1.0]`.

## Writing for the ear
- **Numbers in words:** "three thousand", "ninety-eight percent", "one point three percent",
  "twenty twenty-six", "under sixty days". Digits get read unpredictably, and transcripts check better.
- **Acronyms:** hyphenate letter-by-letter ones in the script ("R-P-A", "C-F-O") or add a rule; leave
  ones said as words alone ("ION" → eye-on).
- **Product codes and versions:** say them as people do: "Infor M three", "the April twenty twenty-six release".
- **No visual-only content:** no tables, URLs, parentheses or footnotes. Sources go in the script's
  header and in your delivery message, not in the audio.
- **Short sentences.** Kokoro handles commas well, semicolons less so.

## Facts
- Use the project's verified facts. A client-facing episode uses only what the listener could check.
- Attribute positioning claims to the company; hedge dated statuses ("in limited availability as of…").
- Label every illustration ("Here's an illustration, not a real screenshot").
- Say a customer's real sector (a distributor is not a manufacturer).
- Keep internal-only material out: partner pricing, training-only figures, unverified counts.
