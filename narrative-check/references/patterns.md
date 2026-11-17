# Narrative check: worked cases

Real cases from a beginner-level blog post that explains semantic models, ontologies and knowledge
graphs through one running example, an online shop with customers, orders and t-shirts.

## Case 1: loop-back and buried hook (a "Semantic Model" section)

**The map the author was shown:**

1. Tables have quirks (`invoice_amount`, `is_test`, cancelled rows). *Problem.*
2. A semantic model is a menu, plus a diagram. *Solution.*
3. The SQL recipe, "without one… with one…". *Solution, with a small replay of the problem.*
4. Bullets: tables vs semantic models. *An aside.*
5. "Everyone gets the same number." *Payoff.*
6. Who builds it. *An aside.*
7. A VP of Sales asks an AI agent for net revenue; the chart doesn't match the finance report.
   *Problem again, told as a story.*
8. "The agent failed because it didn't understand your business." *Diagnosis.*
9. "Connect your agents to those semantic models." *Solution again, payoff again.*
10. Think of it as. *Closer.*

**Patterns found:** loop-back (7–9 replay 1–5), buried hook (the VP story is the strongest opener),
setup gap (the story blames a staging table that the quirk list never mentions), duplicate claim
(5 and 9), duplicate list (4 also appears in a later section).

**Target outline:** VP story → why it happened (merge 1 and 8, add the staging table to the quirks)
→ menu and diagram → recipe, with one sentence saying it reads the finished table and leaves out the
bad rows → one payoff paragraph (merge 5 and 9, refer back to the VP's agent) → who builds it →
closer. Drop the bullets here.

## Case 2: late answer and shifting inventory (an "Ontology" section)

**Hook:** sales, marketing and finance each define "active customer" differently, so the agent
guesses.

**Problem:** the answer (a shared written definition) came in subsection five, after taxonomy,
relationships, rules and an optional code box, none of which address the hook. The section said an
ontology "adds *two* things", later that it "*also*" writes definitions, and the optional box listed
four parts. It ended with "Think of it as", then ran two more subsections, the last of which
introduced a new platform.

**Fix:** name all four parts in the definition sentence → answer the hook immediately (shared
definition and its evidence) → bridge: *"Look closely at that definition, though: 'a customer who
placed a paid order'. It only makes sense if the agent already knows what a customer and an order
are, and how one connects to the other."* → taxonomy → relationships and rules → "one map, two
readers" → optional box, which now refers only backwards → comparison subsection absorbing the
platform point → one closer.

The bridge sentence turns the definition itself into the question that motivates the next three
subsections. Look for that move: the answer to one question, read closely, raises the next one.

## Case 3: a section that mostly worked ("Knowledge Graph")

**Verdict given first:** "This section holds together much better than the other two." Then the
smaller problems:

- **Missing motivating question.** It never asks why copy records into a graph when the database
  already has them. Added a paragraph: records live in different systems under different IDs; in
  tables every hop is a join someone must write; in a graph the links are stored.
- **Vocabulary drift.** The ontology defined *places* and *lists*; the graph diagram said PLACED and
  CONTAINS. Renamed CONTAINS to LISTS in the diagram, the alt text and the comparison table.
- **Example drift.** The graph used a laptop (P20) with IDs C102/O501; the final section used
  C215/O733 and a t-shirt. Switched to C215 → O733 → P31, a t-shirt, everywhere, then grepped for
  the old IDs.
- **Overlapping claim.** Both the ontology and the graph claimed "the agent doesn't have to guess
  the joins". Rewritten so each says what it adds: the ontology says a path exists; the graph holds
  the records on it.

## Clarity rewrites

| Original | What's unclear | Rewrite |
|---|---|---|
| "A semantic model gets the math right, but only once everyone agrees on what's being counted." | Both halves sound like the same idea; the limit is never stated. | "A semantic model makes sure a number is always calculated the same way. What it can't do is decide what belongs in the count. Say you want the number of active customers…" |
| "…pulled from a staging table, a rough working copy of the data that nobody had checked yet." | Vague metaphor; doesn't say why reading it gives a wrong number. | "…read its numbers from a staging table instead of the finished one. A staging table is where new data lands first, before anyone has cleaned or checked it, so it can still hold duplicates and half-loaded rows." |
| "This matters more than it might seem." | Promises a claim, doesn't make it. | "Writing a definition down doesn't just tidy things up. It changes the answers an agent gives." |
| "In one hands-on test…" / "the presenter's conclusion" | Who? | Name the person (and link them if asked). |
| "…a revenue question came back wrong about one time in three" | Hidden setup: the same question was asked many times, and the question isn't given. | "He asked its agent the same question many times: how much revenue one product earned in Pennsylvania. About one time in three, the answer changed…" |
| "The word was different, but the problem was the same." | Different from what? | "It's the active customer problem again, with a different word: nobody had written down what 'revenue' meant, so the agent guessed." |
| "Adding a single human-written note…" | What note, where? | "…one human-written example, a saved query with a plain note saying that revenue means the price of each item sold." |
| "…the shop's real records, drawn as dots and lines." | Wrong verb: they're stored, not drawn. | "…stored as a network of connected points… We can picture each node as a dot and each relationship as a line." |

## Checking a claim before adding it

**Author's request:** "Say that for complex customer queries semantic models are hard to define,
and the knowledge graph can reason through complex questions."

**Verdict:** mostly right, but "complex" needs narrowing.

- Holds: semantic models struggle with questions that follow a *chain of connections* ("What else
  did customers who bought the logo t-shirt also buy?" is four joins that loop back through the same
  tables). You can't predefine a route for every chain; a graph just follows stored links.
- Goes too far: "complex" also covers *calculations*, which are the semantic model's strength and a
  graph's weakness. It isn't that semantic models are "hard to define"; it's that every chain would
  need its own predefined join path. "Reason" overstates the graph alone; inferring unstated facts
  needs the ontology's rules too.

The author chose their own wording. It went in verbatim, followed by one short note on what it left
out (that the graph isn't better at the math) and a one-sentence optional addition.
