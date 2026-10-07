# Verifying a script against the app

A demo script fails in front of a client when it names a button that doesn't exist or promises
behaviour the app doesn't have. Check both before rewriting a single sentence.

## 1. Find the UI
- **Code:** the front-end source (`src/`, `frontend/`, `app/`, templates). Search for the draft's
  labels: `grep -rn "Run Analysis" --include=*.tsx`. If nothing matches, look for the nearest
  wording; that is usually the real label, e.g. "Run analysis" with a lowercase a.
- **Live app (read-only):** open it in a headless browser, sign in, and dump each page's text
  (`page.inner_text("body")`) and a screenshot. Click tabs and links only, never save or submit.
  Dumps can include hidden menu text, so confirm what you see in the screenshot before saying
  something is visible.
- **Role:** find where the UI branches on role (`isAdmin`, `ADMIN_ONLY`, `role ===`). Check what the
  recording role sees: header tabs, sidebar entries, landing cards, admin buttons.

## 2. Labels to check (each one the draft names)
| Thing | Where it usually lives |
|---|---|
| Buttons | `<Button>…</Button>` text, the `label` prop, `aria-label` |
| Tabs | the tabs array (`{ label: "…" }`); counts are often appended, e.g. "Deviations (13)" |
| Section headings | `title="1. Sources"` props, `<SectionLabel>`, `<h2>` |
| Field names and placeholders | the `label=`, `placeholder=` and `htmlFor` text |
| Status messages | stage maps, e.g. `{ embedding: "chunking and embedding" }` |
| Sign-in | the login page's button text and the URL it lives at (`/demo`, `/login?next=…`) |

Write them in the script exactly as the screen shows them, in **bold**.

## 3. Claims to check (each one the draft makes)
- **Conditional behaviour:** "compared against X" may hold only when X is attached or indexed. Find
  the condition; hedge it in the narration or add it to Before recording.
- **Data handling:** "uploads are not stored" or "not added to the knowledge base": find the storage
  path and the expiry. Don't promise more than the code does. Some users will want the line removed
  anyway; that's their call.
- **Timing:** "takes about 10 minutes". Look for an estimate in the code, or a recorded run's
  duration ("Completed in 11m 12s").
- **Accepted inputs:** the real `accept=` list. It often includes more file types than the draft names.
- **Disabled states:** a button disabled while something runs (`disabled={running}`). This forces an
  order, e.g. Stop before Load.
- **Ordering:** when work actually happens. "Extracts the contents after upload" may really happen
  on attach, before Run.

## 4. Preconditions for recording
Collect these into Before recording:
- Records that must already exist: a finished run to load, a sample record, a saved filter.
- Files that must be on hand, and their roles or types.
- Fields to fill or leave empty.
- Personal data on screen: a username or e-mail in a pre-filled field. Suggest hiding it.
- Writes the walkthrough performs, and what each take leaves behind (a run in History, an upload).
- Slow steps and how long they take, so the narration can cover them.

## 5. Report
In "What I changed and why", list each correction as *draft said → app says*, with where it came
from (file:line or the live page). Keep label fixes, behaviour fixes and wording fixes separate.
