Analyze this codebase thoroughly and write a `system-architecture.md` file at the repository root. Base all claims strictly on the code you read (routes, handlers, services, schemas, configurations, and manifests). Do not invent components. Do not include Mermaid or PlantUML diagrams—use prose and tables only.

Structure the document exactly as follows:

## # <System Name> — System Architecture
Provide a 2-3 sentence description of what the system does and who uses it. Use a short product-style name (e.g., "OrderHub").

## Components
List each internal deployable component (aim for 6-14). For each, provide:
* **Name**: Max 3 words, title case.
* **Type**: Frontend, backend API, worker, database, cache, queue, gateway, or CLI.
* **Layer**: Grouping layer (e.g., Data, Core Services, Integration).
* **Responsibility**: 1-2 standalone sentences describing its purpose.
* **Tech**: Framework/language/runtime (one line).
*(Note: Mark as **Optional** if it only runs under specific configurations).*

## External dependencies
List all third-party systems, APIs, or SaaS products. Include: Name, what it provides, whether it is **Required** or **Optional/fallback**, and one line describing the fallback behavior if it is unavailable.

## Connections
Create a markdown table of all communication edges. Be precise; do not use vague terms like "integrates".
| From | To | Protocol | Auth | Pattern | What flows |
|---|---|---|---|---|---|
*(Note: Pattern must be exactly one of: request/response, fire-and-forget, queue/pub-sub [name it], polling [state who/how often], webhook/callback, or scheduled [state cron schedule].)*

## The key connection
Explain the single most critical or complex external integration in 2-4 sentences. Detail who initiates it, the auth handshake, and the mechanism.

## Primary end-to-end scenario
Provide one realistic, primary user scenario that touches the most components. Break it down into 10-20 numbered steps, grouped under 3-6 narrative phase headings (e.g., "Analyze the input").
* Specify the acting component, the receiving component, and the connection used (must perfectly match a row in the Connections table).
* Name any generated artifacts in **bold** (e.g., **Invoice Record**) the moment they are produced, and refer to them by that name afterward.
* If a step is a synchronous ask-and-answer, write it as one step.

## Side paths and scheduled flows
List any audit logs, metrics, retries, or scheduled jobs in 1-2 sentences. Flag them explicitly as optional or scheduled. (Only include if they exist).

## Deployment constraints
List any strict operational requirements, such as shared volumes, mandatory broker paths, or startup sequence dependencies. (Only include if they exist).

**Validation Checklist (Fix any failures before completing your response):**
1. Every component and connection mentioned in the scenario appears precisely in the Components and Connections sections.
2. There are zero orphaned connections in any direction.
3. Every Connections row has a concrete Pattern.
4. The document reflects only what the code does today—no roadmap or aspirational features.