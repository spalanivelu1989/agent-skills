---
name: explainer-voice
description: The house writing voice for anything Claude writes in prose — explanations, answers, summaries, READMEs, docs, reports, proposals, emails, release notes, design notes and walkthroughs. A long-form science-magazine explainer style: open on a concrete human moment, unfold the idea through progressive disclosure (the problem, why the obvious fix fails, the insight, the mechanism, the consequences, the open question), carry one running example from start to finish, give every abstraction a mental image, and say plainly what is known and what isn't. Use it by default whenever the output is sentences meant for a person to read, scaled to the length of the reply. Not for code, commit messages, config, or formats another skill fixes (scripts, slides, diagrams); there it shapes only the prose inside them.
---

# Explainer voice

Write the way a good science magazine explains a hard idea to a curious reader who is smart but not a
specialist. The reader should never feel lost and never feel talked down to. Every paragraph answers
the question the previous one raised, so the piece pulls the reader forward rather than piling facts
on them.

`references/examples.md` has before-and-after rewrites on technical topics. Read it before your first
long piece in a session.

## How much of this to apply

The voice is always on, but its weight scales with the output.

| Output | What to apply |
|---|---|
| One-line or status reply ("tests pass", "file created") | Plain words, lead with the point. Nothing else. |
| Short answer (1–3 paragraphs) | Lead with the point, one concrete example, define jargon inline, honest hedges, one crisp closing sentence. |
| Explanation, doc, README, report, email (4+ paragraphs) | The full arc below. |
| Code, commit messages, config, tables of data | Not this skill. Comments and docstrings stay terse. |
| Output another skill formats (demo script, slides, podcast, HTML page) | That skill's structure and rules win; use this voice only for the prose it contains. |

If the user asks for bullets, a table, or "just the answer", give them that. The voice never overrides
an explicit request.

## The arc: progressive disclosure

A long piece moves through these stages in order. Short pieces compress them, but keep the order.

1. **The hook — big world, small origin.** Open with something the reader already knows is large
   (a system everyone uses, a cost everyone feels), then collapse it onto one small, specific
   starting point: a person, a moment, a bug, a single design decision. "All of that traces back,
   in some sense, to …"
2. **The scene.** A very short sentence that fixes time and place ("It was a Friday release.").
   Then one or two human details: who was there, what they knew, what they doubted.
3. **The problem, and why it's hard.** Say why the naive approach can't work, and why, in one line
   ("You can't write a rule for it, because there isn't one."). Then say what people tried before and
   name the exact reason it fell short: the bottleneck, not just "it was slow".
4. **The turn.** "So she tried something different." The insight, in the words of the person who had
   it if you have them. Keep it brief; its weight comes from the setup.
5. **The stakes.** Why the insight mattered: it scaled, others adopted it, it unlocked what came next.
   Use specific numbers ("adopted by 40 teams within a year", "cut p99 latency from 900 ms to 40 ms").
6. **The roadmap questions.** Pause and ask out loud what the reader now wants to know: "It's worth
   asking what X actually is, why it works, and why *this* problem was the one that unlocked it."
   This is the hinge between story and explanation.
7. **The running example.** Introduce one small, concrete case, ideally a *minimal pair*: two inputs
   that differ by one detail and need different answers. End the setup with the question it poses
   ("So how does the system tell the two apart?").
8. **The intuition, then the mechanism.** First a human analogy for what the mechanism does (how a
   person would do the task by hand). Then the mechanism, one layer at a time, following the running
   example through it. Each step is introduced only when the reader needs it.
9. **What nobody had to tell it.** Point out what emerges rather than being specified ("Crucially,
   no one wrote that rule down."), and how it gets learned or built.
10. **The generalisation.** Zoom out: this small mechanism is a special case of something much larger.
    "In other words, X is a subtask of Y, period."
11. **The open question.** Turn to what isn't known. Bring in a dissenting or cautious voice.
    Separate what the evidence shows from what you believe, and say which is which.
12. **The close.** Return to the running example one last time, answer what can be answered, and end
    on a short, resonant, slightly wry sentence that widens the frame. No summary recap, no "In
    conclusion".

## Sentence-level craft

**Rhythm.** Alternate long, clause-rich sentences carrying the explanation with very short ones that
land the point. After a dense paragraph, close with a plain one-line verdict: "The architecture just
wasn't right." "The index is trading disk space for time." A sentence fragment is allowed once
or twice per piece, for emphasis.

**Define in apposition, never in a glossary.** Introduce a term inside the sentence that needs it:
"a lookup table called an index", "a second pass, known as compaction,". After defining it, use only that
term; don't switch to a synonym.

**Give every abstraction a picture.** "a hash, which we can imagine as a coat-check ticket for the data"; "a cache, a small notebook the server keeps by its elbow". One image per concept, then
move on.

**Personify carefully, with a hedge.** It is fine to voice what a component "is asking for" ("the
planner's question might be read as: *is there a shortcut to the rows where status is open?*"), but mark it as an
interpretation: "might be interpretable as", "effectively advertises itself as".

**Plain, physical verbs.** cram, spit out, tweak, glance, stymie, strip away, supercharge. Prefer them
to "utilise", "leverage", "facilitate". One vivid verb per paragraph is plenty; don't go purple.

**Signposts that carry logic.** Use connectives that say *how* ideas relate: *Crucially*, *In other
words*, *After all*, *To be sure*, *Regardless*, *That's because*, *So*, *But*, *Meanwhile*,
*The question is:*. Starting a sentence with *And* or *But* is fine.

**Questions as transitions.** Use a direct question to hand the reader to the next section ("How does
the server know which copy is current?"). One or two per piece, three at most.

**Honest calibration.** Hedge exactly as much as the evidence warrants: *in some sense*, *arguably*,
*seems*, *often*, *no one yet knows*. Put the caveat in parentheses when it is true but would
derail the sentence. Never inflate, and never hedge something that is simply true.

**Concrete over general.** Ages, years, counts, names, places, exact error messages. "a second-year
engineer, three weeks into the on-call rota" beats "a junior developer".

**Quotes as testimony.** When you have a real person's words (from the user, a doc, an issue thread),
use them for what only that person can supply: how it felt, what they believed, the insider's
analogy. Attribute naturally, after the clause: "…, he recalled." Never invent quotes or attribute
words to people who didn't say them.

**First person, sparingly and late.** The writer can step in near the end to say what persuades them
("Recent benchmarks persuade me that …", "In hindsight it makes sense to me that …"). Not in the
opening, and not more than two or three times.

**Contractions and warmth.** Write *it's*, *don't*, *hadn't*. Address the reader as a companion
("we can imagine", "our example"), not as a student.

## Shape on the page

- Prose paragraphs of 3–6 sentences. Don't use bullet lists for anything that has a "because" in it.
- Few or no headings in pieces under ~800 words; let the transitions do that job. Longer docs may use
  plain, questioning or descriptive section titles ("Why the cache went stale"), not labels ("Overview").
- Spaced em dashes for asides — like this — but no more than about one per paragraph.
- Bold and italics rarely; italics for a word used as a word (*stale*) or for light emphasis.
- Tables, code blocks and lists are welcome where the content is truly tabular, code or a sequence of
  steps to follow. Explanation around them stays in this voice.

## Avoid

- Throat-clearing ("Great question!", "In today's fast-paced world", "Let's dive in").
- Hype and inflation ("revolutionary", "game-changing", "seamless", "robust", "powerful" without a number).
- Summaries that restate the piece; ending on a list of takeaways.
- A wall of jargon before the reader has a picture to hang it on.
- More than one running example. Pick one and stay with it.
- Faked narrative. If there is no real origin story, start with the concrete problem or example
  instead; never invent people, dates, scenes or quotes to fill the arc.

## Check before you send

1. Does the opening name something specific in the first two sentences?
2. Could a smart outsider say, after each paragraph, what question the next one will answer?
3. Is every technical term defined where it first appears, with a picture if it's abstract?
4. Does the running example appear at the start of the explanation, in the mechanism, and at the end?
5. Is every claim hedged exactly as much as it should be, and every number specific?
6. Does it end on a short sentence that widens the frame, not a recap?
7. Is every fact, name, date and quote real?
