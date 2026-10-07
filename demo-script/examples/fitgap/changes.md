# What changed, and why

## Round 1: verify and rewrite
**Labels: draft said → app says** (from the front-end code)
- "click submit" → the button is **Sign in**.
- "a source section" → **1. Sources**. The upload button is **Attach documents**, and *Attach as* sets the role (**Country As-Is**).
- "PDF, Word or a text format" → it also accepts Excel and PowerPoint (the `accept` list).
- "scope section … additional instructions" → **2. Scope**, with **Additional Instructions (optional)** inside it.
- "Run Analysis" → **Run analysis** (lowercase a). The log opens from **Logs** in the **Investigation** section.

**Behaviour**
- "compared against … SAP Best practices" is only true when a Best Practice source is attached or indexed; otherwise the score is "not assessable". Hedged at first ("where available"); the user later chose the plain wording, so it went into Before recording instead.
- "Once the document is uploaded, our pipeline will extract…" happens on attach, before Run, so it moved into the upload step.
- The Admin-only sidebar (Ask RAG, Agent) is hidden for a regular user, which keeps the screen clean.

**Added**
- An intro and a close, and a results step (Summary, Deviations, Workshop agenda): the draft stopped at "you can view the results".
- Typos fixed: "talk a look", "relatioships", "gloabal", "you will two tabs", "approximately around".

**Questions asked**
- Cypher and Quality views: too technical for business users? (Yes; cut.)
- What document will be uploaded? (The country document.)

## Round 2+: the user's edits (each applied exactly, length re-checked)
- The intro is about running a Fit-Gap analysis only → the close was flagged as mismatched; Spine kept as a quick look before the analysis.
- Removed "Your files are used only for this analysis…".
- "and, where available," → "and SAP Best Practices" (the condition went into Before recording).
- Removed "pick a specific Global Template process…" from Scope.
- Added: attach `India_Customer_Returns_As_Is.txt` from the Desktop, and show the processing.
- Added: Investigation → **Logs**; then **Stop**, **History**, a past run, **Load into page**. Load is disabled while a run is in progress, so Stop has to come first.
- Over 3:00 → proposed the one cut that fixed it (the Process/Model views in Spine).
- "the Solvay team shared" → "that Solvay shared with us". URL corrected to `…/demo`.

## After recording: re-sync
The video changed some steps, so the script was brought back in line:
- A `.txt` upload skips Docling, so only *chunking and embedding* → *extracting entities* appears.
- Additional Instructions left empty; a 2-second pause before Run; scroll up to History before clicking.
- The past run was named exactly (4.10.2 Process Returns, *GT 58.8%*).
- Times were taken from the recorded scene lengths (2:28).
