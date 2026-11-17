---
name: narrative-check
description: Audit existing prose (a blog section, article, doc, README, report or essay) for two kinds of problem, then fix them on request. Narrative order means concepts that drift, loop back, repeat, end twice or arrive in an order that doesn't build. Clarity means sentences and paragraphs that are ambiguous, vague or unclear. It maps what each paragraph does, names the drift patterns it finds, proposes a reordered outline that keeps the author's own sentences, flags unclear sentences with a rewrite for each, checks any new claim the author wants added before writing it, then applies the agreed fixes and updates everything coupled to them (diagrams, alt text, tables, table of contents, anchors). Use when someone says a section "drifts", "jumps around", "doesn't flow", "has no narrative", "doesn't follow a logical order", or that a sentence or paragraph is "ambiguous", "vague", "unclear" or "confusing", or asks to check, review, restructure or tighten the story of a piece of writing. It complements explainer-voice: that skill says how to write, this one audits what's already written. Not for proofreading spelling and grammar alone, or for code review.
---

# Narrative check

A reader can follow every paragraph and still feel lost, because the paragraphs come in the wrong
order: the problem gets solved, then raised again; the strongest story comes after the answer; the
section ends, then keeps going. And a sentence can be perfectly grammatical and still say nothing a
reader can picture. This skill finds both problems, explains them to the author in terms they can
check against their own text, and fixes them in a way that keeps the author's voice.

It works alongside **explainer-voice**. That skill is the house style for writing. This one is the
editor that reads a draft and asks: does each paragraph answer the question the last one raised? Load
explainer-voice too (once per session) before writing any replacement prose, so fixes match the house
style.

`references/patterns.md` has real before-and-after cases for every pattern below. Read it before the
first check in a session.

## The workflow

The author usually says something like "this section drifts, correct me if I'm wrong". That's two
requests: give an honest verdict, and don't change anything yet. So the default is **diagnose, then
ask, then fix**.

1. **Read the whole piece, not just the section.** Drift often comes from neighbours: a list that
   repeats one in another section, an example whose IDs differ from the final section, a claim the
   previous section already made. Read the surrounding sections and anything the section links to or
   cites (a related post in the same repo is often the source of its facts).
2. **Map the section.** Write one line per paragraph or block (diagram, panel, list, code, collapsible
   box) with its *role*: problem, story, definition, mechanism, example, evidence, payoff, aside,
   comparison, closer. Tag each with what it does to the story, in italics: *Problem.*, *Solution
   again.*, *An aside.* Laid out this way, a loop or a late hook shows on the page and the author can
   check the claim for themselves.
3. **Diagnose.** Name each pattern you find (from the catalogue below), in bold, with the exact
   paragraph it applies to and why it breaks the reader's path. Quote the author's words.
4. **Give an honest verdict.** If the author is right, say so in the first sentence. If the section
   mostly holds together, say *that* in the first sentence and list the smaller problems ("This
   section holds together much better than the other two"). Never invent drift to justify the check.
   If the author is wrong about something, say what and why.
5. **Propose the fix as a numbered target outline.** One line per step, saying where each existing
   paragraph goes, what merges, what's dropped and why, and the one or two new sentences (bridges)
   the reorder needs. Keep the author's sentences wherever they still fit; the edit changes the
   *joins*, not the voice. Say what else must change with it (table of contents, anchors, diagrams).
6. **Ask before rewriting.** End with one question: should I rewrite it in this order? Don't touch
   the file until they say yes. Exception: a single sentence the author has explicitly called
   unclear, with no other change requested. Fix that directly and show the before and after.
7. **Apply the fix** (see "Applying fixes" below), then report what changed, step by step, and flag
   every place you deviated from the agreed plan and why.

## Part 1: narrative order

The test is the one explainer-voice sets: after each paragraph, a reader should be able to say what
question the next one will answer. These patterns are the usual ways that breaks.

**Loop-back.** The section runs problem → solution → problem again → solution again. Typical cause:
a "Why it matters" story added after the explanation, which reads as a step backwards. Fix: move the
story to the top as the hook, merge the two problem statements, keep one solution.

**Buried hook.** The most concrete, human story (a VP's wrong chart, a failed test) sits halfway
down. The opening is abstract. Fix: open on the story.

**Late answer to the hook.** The section opens a question ("which definition of *active customer*?")
and answers it several subsections later, after detours that don't address it. Fix: answer the hook
right after the definition, then use a bridge sentence to raise the question the detours answer.

**Shifting inventory.** What the thing "contains" keeps changing: "it adds *two* things", then
later "it *also* does a third", while an optional box lists four. Fix: name every part once, early,
in one sentence, then take them in order.

**Duplicate claim.** The same definition, payoff or benefit is stated twice: a callout panel
repeating the sentence above it, two "everyone gets the same number" paragraphs, a bullet list that
also appears in another section. Fix: keep the stronger one, delete or merge the other. Check other
sections before deleting, since a list may now appear only once after an earlier fix.

**Multiple endings.** A closer ("Think of it as…", a summary panel) appears mid-section, then more
subsections follow. Fix: one closer, at the end.

**Late new idea.** A new concept, product or claim turns up in the last block (a platform name, a
new architecture). Fix: fold it into the subsection it belongs to, with one sentence of setup.

**Circular reference.** The main text leans on optional or collapsed content ("the box above shows
what that looks like") while the optional box points forward ("which we'll meet next"). Fix: the
main path must stand alone; optional content refers only backwards.

**Setup gap.** The story's causes aren't set up anywhere: the failure involves a staging table but
the list of quirks never mentions one, so the fix can't be seen to address it. Fix: name every
cause in the setup, and make the fix visibly handle each.

**Missing motivating question.** The obvious objection is never asked: "the database already has
these records, so why copy them into a graph?" Fix: ask it out loud and answer it in its own
paragraph. This is often the real reason the thing exists.

**Overlapping claims across sections.** Two sections claim the same benefit for different things
(both "the agent doesn't have to guess the joins"). Fix: say what each adds that the other doesn't.

**Example drift.** The running example changes mid-piece (t-shirts become a laptop) or its IDs
differ between sections. Fix: one example, the same IDs, start to finish. Update every diagram,
table row and alt text that mentions the old one.

**Vocabulary drift.** The same thing gets several names ("staging copy", "checked table", "real
one") or a later section uses a name the earlier one never defined (the graph says CONTAINS, the
ontology defined *lists*). Fix: pick one term per thing and use it everywhere. When one section is
the schema for another, the names must match exactly.

**Evidence that blurs a distinction.** A supporting example uses a different case, or belongs to
the neighbouring concept, right before a passage that separates the two. Fix: add one framing
sentence that ties the evidence to the case at hand ("It's the active customer problem again, with
a different word").

## Part 2: clarity

These are sentence- and paragraph-level. For each one, quote the original, say in one line what's
unclear, and give the rewrite.

**Empty opener.** "This matters more than it might seem." The sentence promises a claim without
making it. Fix: lead with the claim itself.

**Unnamed actor or source.** "One hands-on test", "the presenter", "some teams". Fix: name who,
and where it came from. Link the name if the author wants it.

**Hidden setup.** "Came back wrong one time in three", but the reader doesn't know the same
question was asked many times, or what the question was. Fix: state the setup before the result.

**Dangling comparison.** "The word was different, but the problem was the same." Different from
what? Fix: name both sides.

**Undefined artefact.** "A single human-written note." What kind of note, and where does it live?
Fix: say what it is and where it sits.

**Pair that sounds like one thing.** "It gets the math right, but only once everyone agrees on
what's being counted." Both halves sound like the same idea, so the limit is never stated. Fix: say
plainly what the thing *can't* do, then give a one-line example.

**Jargon defined by a metaphor.** "A staging table, a rough working copy of the data." The picture
is vague and doesn't say why using it causes the failure. Fix: define it by what it does, then say
why that matters here ("where new data lands first, before anyone has cleaned or checked it, so it
can still hold duplicates and half-loaded rows").

**Wrong verb for the mechanism.** "Records, drawn as dots and lines", when the records are *stored*
that way and the dots are only how we picture them. Fix: use the literal verb, and keep the picture
as a separate, clearly marked image.

**Overclaim.** "It can reason through complex questions." Fix: narrow to what's true ("follow
chains of connections") and say where the rest comes from.

## Part 3: claims the author wants added

When the author asks to add a claim ("say that X can't do this and Y can"), check it **before**
writing it.

- Say in the first sentence whether they're right, mostly right or wrong.
- Split the claim into the parts that hold and the parts that go too far. Common overreach:
  a word like "complex" that covers two different kinds of difficulty (complex *connections* versus
  complex *calculations*); a strong verb ("reason", "understand", "guarantee") for something that
  only does a narrower thing; a capability credited to one component that really needs two.
- Check facts against the sources in the repo (a related post, a reference, the code). Never add a
  fact, number, name or quote that isn't in a source.
- Offer the corrected paragraph, ready to paste, and ask whether to add it as written.
- If the author chooses their own wording, add it **verbatim**. Afterwards, mention once, briefly,
  anything the chosen wording leaves out, with a one-sentence addition they can take or leave. Don't
  push.

## Applying fixes

- **Keep the author's text.** Move paragraphs whole; rewrite only the joins and the sentences the
  diagnosis named. Don't take the chance to restyle everything else.
- **Update everything coupled to the change.** Table of contents entries and anchor ids (and grep
  the repo for links to any removed anchor), diagram labels, alt text and aria-labels, table rows,
  captions, and any later section that reuses the example. After renaming an example or a term, grep
  the file for the old one and confirm nothing is left.
- **Mind the markup around inline elements.** In JSX, a line break between text and an inline tag
  (`<a>`, `<mark>`, `<code>`) drops the space; add `{' '}`. In Markdown and HTML, check that links and
  emphasis still sit inside the sentence.
- **Use the project's existing styles** for highlights, callouts and links (look in the stylesheet
  first) instead of inline one-offs.
- **Verify.** If the project builds or has tests, run them after a structural rewrite and report the
  result. If you skip it for a one-word change, say so.
- **Report.** List the new order or the changes step by step, name everything dropped or merged and
  why, and call out each deviation from the agreed plan. Don't paste the whole rewritten section
  back.

## Check before you send the diagnosis

1. Does the first sentence give the verdict (right, partly right, or mostly fine)?
2. Is there a one-line-per-paragraph map, with each role tagged?
3. Does every named pattern point to a specific paragraph and quote the author's words?
4. Does the proposed outline keep the author's sentences, and say what's dropped and why?
5. Did you read the neighbouring sections for duplicates, example drift and vocabulary drift?
6. Does it end with a single question asking permission to rewrite?
