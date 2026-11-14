# Writing guide: structure, language and evidence

These rules come from `example-paper.html`, the Tarento SAP GDPR paper the user singled out as the
model. When a rule here seems abstract, find the matching passage in that file and copy the move,
not the content.

## Contents

1. Structure: a chain of questions
2. The running example
3. Language
4. Evidence discipline
5. The business readers' guide
6. Typography (already in the template)
7. Final checklist

---

## 1. Structure: a chain of questions

The paper has three acts: **the problem** (Sections 1–4), **the solution it requires** (5–9) and
**how to take it forward** (10–14). Inside them, each section answers the question the previous one
leaves open. If you can't say what question a section answers, cut or merge it.

| Section | Answers | Leaves open |
|---|---|---|
| Title page, abstract, keywords, contents | What is this, and what does it conclude? | Why believe it? |
| Executive summary, ending in a boxed **Recommendation** | The whole argument on one page | What's the background? |
| 1 Introduction: context, problem statement, research questions, scope, structure | What exactly is being asked? | What must I know first? |
| 2 Background | The legal, technical or market terrain | How was evidence gathered? |
| 3 Method, evidence grades, limitations | How much to trust what follows | So what's wrong? |
| 4 The problem: running example, sources of difficulty, value chain, evidence it's current, boxed **Problem in one paragraph** | Why it's hard, and why now | Hasn't someone solved it? |
| 5 Existing approaches, comparison table, **The gap** | What exists and what doesn't | What do we have? |
| 6 Our current assets, assessed against requirements | How far our assets go | Will anyone pay? |
| 7 Demand, buyers, willingness to pay | Who buys, from which budget | How much is it worth? |
| 8 Market size: TAM top-down, SAM bottom-up, SOM | How big the prize is | What must we build? |
| 9 Solution requirements: framework figure, functional and non-functional requirements, governance, offering, investment | What a complete answer looks like | Where do we start? |
| 10 Segments and go-to-market | Which customers first, and how to reach them | What could go wrong? |
| 11 Risks (table with mitigations) | What could go wrong | What do we do on Monday? |
| 12 Roadmap, interview questions, pilot metrics, boxed **Decision rule** | What to do, and how to know whether to continue | What's uncertain? |
| 13 Discussion: what the evidence shows / what remains uncertain / a cautious view / the author's judgement | The honest state of knowledge | The verdict? |
| 14 Conclusions: five to seven numbered points, then the running example one last time | The verdict | — |
| References (grouped by source type), appendices (glossary plus topic-specific) | — | — |

**Adapting it.** This skeleton fits "should we pursue X?" papers: a market, a product, a capability.
For a different kind of question, keep the arc and swap the middle. A technology choice uses options,
evaluation criteria, comparison and a recommendation instead of demand and market size. A policy or
compliance question uses obligations, current state, gap analysis and a remediation plan. Always keep
these five: method and limitations before the analysis, a section on the gap, requirements, a
decision rule, and a discussion with a sceptic's view.

**Five moves to always make:**
- **Frame the problem as a trade-off when it is one.** In Section 4, state both sides in one sentence
  ("either X, or Y"). In Section 5, give the comparison table a column called "What it solves" and
  one called "The catch", so each existing approach is shown fixing one side and reopening the other.
  The gap then reads as the missing approach that removes the trade-off.
- Put **method before analysis**, so evidence grades are defined before the first graded claim.
- **End the comparison with "the gap"**, and say outright that a gap in public evidence is not proof
  that nobody does it.
- Give each act a **one-paragraph verdict box** (3–4 boxes in the whole paper). A reader who reads
  only the boxes should still get the argument.
- Write **a decision rule, not just a recommendation**: "Invest in phase 3 only if (a) … and
  (b) …. If …, stop." That's what makes the paper usable as ground truth.

## 2. The running example

Choose one concrete case, ideally a **minimal pair**: two inputs that differ by one fact and need
different answers. In the model paper, *Nordbutik AB* (a company) and *Anna Svensson* (a sole trader)
sit in the same SAP field with the same definition, and only Anna's row is personal data. That one
pair carries the whole technical problem.

Use it in at least four places: to **define the problem** (Section 4.1), to **define the gap** (5.3),
to **frame the requirement** (9), and in the **last paragraph** (14). The closing sentence states
the business test in its terms ("If we can do all three, we have a business; if we can only find
the field, we have a feature others give away"). Use only one example.

Never invent real-seeming people or firms without labelling them: write "(Both are hypothetical.)"

## 3. Language

The register is a serious consultancy white paper or journal preprint. It's formal but not stiff,
and it never sells. Use the explainer-voice skill for clarity, but within these limits:

- **Third person.** Write "this paper", "the author". First person appears only in "The author's
  judgement" paragraph of the Discussion. No scene-setting opening and no wry close. The ending is
  the running example and the business test. The one exception is the short narrative opening of
  the business readers' guide (§5); the formal body starts after it.
- **Define terms inside the sentence on first use**: "to block the data, which means hiding it from
  everyday use while keeping it for auditors". The glossary is a backup, not a crutch.
- **Leave nothing to look up.** A reader new to the field should finish the paper without searching
  for anything. Spell out every acronym on first use, both in the guide and again in the body. In
  Section 2, explain each prerequisite concept by what it does, step by step, before you name it.
  Follow every formal or legal term with a plain restatement ("In plain terms, …").
- **Turn mechanism back into consequence.** After a paragraph of technical or legal detail, add one
  sentence that starts "In practice, …" and says what changes for the organisation.
- **Make scale tangible with a sum.** Don't write "this grows costly at scale". Show the arithmetic
  and the assumption ("at 20 fields per table and 4,000 custom tables, that is 80,000 fields to
  classify") and tag it `ESTIMATE`.
- **Stretch one analogy to separate neighbouring concepts.** Where two or three terms are easy to
  confuse, put them in one analogy as successive stages and bold the word that differs. Use it
  once, in the guide or in Section 2.
- **Let each paragraph's first sentence carry its claim**, so a reader skimming first sentences
  still follows the argument.
- **Turn big ideas into short formulas**: *find, label, document, fix*. "Discovery is commoditised;
  classification and remediation are not." "A niche, not a moonshot."
- **Name the tensions**: "Two of these pull in opposite directions …", then carry that tension
  through the paper.
- **Follow a dense paragraph with a short verdict sentence**: "It is an execution engine, not a
  discovery tool."
- **Hedge exactly as much as the evidence allows**: "suggestive, not conclusive"; "could each be off
  by half"; "arguably". Give numbers as ranges with a central case (€70–450m, about €200m).
- **Give the sceptic a voice**: "A sceptic would argue that …", then say which evidence would settle it.
- **Avoid hype words**: no "revolutionary", "seamless", "robust" or "leverage". Use the spelling
  convention of the user's organisation (the model uses British English).
- **Lists only for genuine lists**: research questions, steps, numbered conclusions. Reasoning goes in
  paragraphs.

## 4. Evidence discipline

This is what lets the user treat the paper as ground truth.

- **Cite every factual claim** as `<span class="cite">[n]</span>`. Numbers follow the order of the
  References section. Group references by source type: law, regulators and courts, the vendor or
  platform, competitors, market data, internal, other. Give each one author or organisation, an
  italic title, a date and the **full URL** (it has to work on paper).
- **Grade the claims that carry weight** with the five tags defined in Section 3.3:
  `VERIFIED` (primary source read directly), `ANALYST`, `VENDOR`, `SURVEY`, and `ESTIMATE` (the
  paper's own reasoning, with assumptions shown). Aim for one tag per page, not one per sentence.
- **Never fabricate** a source, figure, quote, customer or price. If no public figure exists, say so
  and estimate bottom-up in a table, with each assumption beside the number it produces.
- **State limitations plainly** in Section 3.4: what wasn't run or tested, which sources returned
  errors (with the error), which figures were seen only second-hand (mark them "secondary"), and
  what primary research hasn't been done.
- **Show provenance on the title page**: the evidence base, the classification and a disclaimer.
  **Don't name an author.** Leave it out, or use a name the user gives you. Putting an invented
  expert's name on AI-assisted analysis misrepresents where it came from, even when the user asks
  for the paper to "look like" an expert wrote it. Meet that request through rigour, not a byline.
- **Internal files are read-only.** Read them in full, including hidden content, and never modify
  them. Record that in the method section ("read in full, unmodified").

## 5. The business readers' guide

The paper goes right after the title page, in `<div class="guide">`, and takes 2–3 pages. It retells
the argument for an MBA or board reader **with no jargon, codes or article numbers**.

It opens with a **short narrative**, one paragraph of 80–120 words, before the first heading. This
is the only place in the paper that uses the explainer-voice hook. Start with something the reader
already knows is large (a cost, a deadline, a system everyone relies on), then narrow it to one
concrete moment where the problem shows itself: the running example as it happens to someone. Use
the present tense, a specific role ("a payroll clerk in the Hamburg plant"), and one human detail:
what they see, what they have to decide, what they can't know. End on the question the paper
answers. Keep it short; the guide still has to fit on three pages.

The honesty rules still apply. A real case from the user's material is best. Otherwise make the
moment typical, not invented: a role, not a named person, and say so ("A typical case: …" or
"(The scenario is illustrative.)"). Never invent a quote, a date or an incident and present it as
real. If the topic gives no natural moment, open on the running example's minimal pair instead.

Then the sections:

1. The problem in one picture (the running example, told in full this time).
2. Why the organisation has to care, in plain words, with the scale of the risk.
3. Why now.
4. What a solution has to do, and which parts are already solved.
5. What we already have, with its strengths and limits.
6. How big the opportunity is, with each number and a one-line meaning.
7. Who pays, and from which budget.
8. The competition, one line each.
9. The recommendation.
10. Test before investing: a short When / Do / Learn table, and the decision rule.
11. How to read the rest: a table of which sections each kind of reader can skip.

Phrase the guide's headings as the reader's own questions ("Why does this matter to us?", "What would
a solution have to do?"). Point 1 is a good place for the stretched analogy from §3. Point 4 is a
good place for the trade-off in one sentence.

If it spills onto a fourth page, cut words before shrinking type. The guide already sits slightly
below body size.

## 6. Typography (already in the template)

Don't restyle. The template carries these choices:

- **Page:** A4, page numbers, a running header, and neither on the title page.
- **Text:** Charter serif body at 10.6pt, justified and hyphenated. Sans-serif navy headings.
- **Tables:** booktabs-style rules, header rows that repeat on each page, rows that never split.
  Captions sit *above* tables and *below* figures. Number tables and figures in order and refer to
  each one in the text.
- **Figures:** drawn in HTML and CSS (the `chain` and `layers` components), not as images, so they
  print sharply.
- **Colour:** one accent (navy `#10304a`). Everything must still read on a black-and-white printer.
- **Page breaks:** each act and each major section starts on a new page (`h2.newpage`). Short
  sections such as Risks and Discussion can run on.

## 7. Final checklist

1. Can every section's question be stated, and does the next section answer what it leaves open?
2. Does the running example appear in Sections 4, 5, 9 and the final paragraph?
3. Is every factual claim cited, every weighty claim graded, and every estimate shown with its assumptions?
4. Does Section 3.4 list everything that wasn't tested, couldn't be opened, or was seen only second-hand?
5. Is there a decision rule, and a "cautious view" that argues against the recommendation?
6. Does the business guide fit on three pages with no jargon, and does it open on one concrete
   moment that is real or labelled as illustrative?
7. Is `render.py` clean of errors, and has the contact sheet been inspected?
8. Is there no invented author, and is every name, number, date and quote real?
9. Could a newcomer read it without searching for anything? Is every acronym spelled out, and every
   prerequisite explained by what it does?
10. If the problem is a trade-off, does the comparison table show what each approach solves and its
    catch? Is each technical stretch followed by an "In practice" sentence?
