# Prompt: generate a system-architecture.md from a codebase

Copy the prompt below into a Claude session opened at the root of the codebase. It produces a
`system-architecture.md` containing exactly the information the ArchFlow skill's Steps 1-5 consume —
components, groupings, connection mechanisms, the key-connection callout, and one concrete
end-to-end scenario.

---

Explore this codebase thoroughly and write a `system-architecture.md` at the repository root that captures the system's architecture completely and unambiguously. This document will be the single input for generating architecture diagrams, a UML workflow sequence diagram, and an animated demo of one request flowing through the system — so every component, connection, and scenario step you write will literally become a box, an arrow, or an animation step. Be concrete; leave nothing for a reader to infer.

Ground every claim in code you actually read: entry points, route/handler definitions, service clients and SDK usage, queue/topic declarations, database schemas and connection strings, docker-compose/Kubernetes manifests, CI configs, and environment variables. Never invent a component or connection you cannot point to in the code. If something is genuinely undeterminable from the code (e.g. an auth mechanism configured outside the repo), still include it but mark it `(inferred)`.

Do not include a Mermaid or PlantUML diagram in the document — prose and tables only. (A diagram, if present, would be treated as the source of truth by downstream tooling, so an incomplete one does harm.)

Structure the document exactly like this:

## `# <System Name> — System Architecture`

2-3 sentences: what the system does and who uses it. Give the system a short product-style name — it is used to derive code identifiers, so prefer "OrderHub" over "the order processing and fulfilment platform".

## `## Components`

One `###` subsection per internal component (a deployable or independently-reasonable unit: frontend app, backend/API service, background worker, database, cache, queue broker, gateway, CLI). For each:

- **Name**: 3 words maximum, title case — this becomes a diagram box title and a card label, so "Report Worker", not "the asynchronous report generation worker process".
- **Type**: frontend / backend API service / worker / database / cache / queue / gateway / CLI.
- **Layer**: which of 2-4 named layers it belongs to (e.g. Frontend, Core Services, Data, Integration). Use the same layer names consistently — they become the diagram's groupings.
- **Responsibility**: 1-2 sentences, written to stand alone — this text is shown verbatim as the component's description in an interactive inspector.
- **Tech**: framework/language/runtime, one line.

Aim for 6-14 components. If the codebase has more moving parts than that, fold helpers into the component that owns them (a service's internal modules are one box) and say in the Responsibility line what was folded in. Mark any component that is optional (only runs when configured) as **Optional** and say what enables it.

## `## External dependencies`

Every system this codebase depends on but does not own: third-party APIs, SaaS products, LLM providers, legacy systems, identity providers. For each: name, what it provides, **Required or Optional/fallback**, and one line on what happens when it is unavailable. These render differently from internal components in every diagram, so the internal/external split must be exact — when in doubt, "do we deploy and operate it?" decides.

## `## Connections`

A table with one row per communication edge. This is the section diagrams are drawn from, so precision here matters most:

| From | To  | Protocol | Auth | Pattern | What flows |
| ---- | --- | -------- | ---- | ------- | ---------- |

- **Protocol**: REST/JSON, gRPC, GraphQL, WebSocket, AMQP, direct SQL, file share, etc.
- **Auth**: JWT, OAuth2 client-credentials, API key, mTLS, none — per edge, not per system.
- **Pattern**: exactly one of — `request/response` (synchronous call, answer comes back on the same connection), `fire-and-forget` (no reply expected), `queue/pub-sub` (name the queue or topic), `polling` (state explicitly who polls whom and how often — this changes how the flow is animated), `webhook/callback`, `scheduled` (cron — state the schedule).
- **What flows**: 2-5 words naming the payload ("order events", "rendered PDF", "embeddings").

Never write "A integrates with B" — name the mechanism. If two components talk over two different channels for two different purposes, write two rows. If a connection's direction is surprising (the "server" initiates, or replies arrive via a separate callback), spell that out in the What-flows cell.

## `## The key connection`

2-4 sentences on the single most important or most easily misunderstood connection in the architecture — almost always "how does this system actually reach its key external dependency". Write the paragraph a new engineer needs to not get this wrong: is it one connection or two different mechanisms for different purposes, who initiates, what the auth handshake is. This paragraph is repeated across every generated artifact as the one thing a viewer should remember.

## `## Primary end-to-end scenario`

Pick **one** realistic scenario that a real user actually triggers and that touches as many components as possible — this single scenario becomes the workflow sequence diagram and the animated demo, so choose the system's signature flow, not a health check. Write it as a numbered walkthrough of 10-20 steps:

- Start with the user's triggering action, quoted ("user drops an invoice PDF into the upload folder").
- Every step names: the acting component, what it sends/asks/does, the receiving component, over which connection (must match a row in the Connections table), and what comes back if anything.
- Name every intermediate artifact in **bold** the moment it is produced (**Test Plan**, **Invoice Record**, **Signed URL**) and refer to it by that name afterwards.
- Group the steps under 3-6 phase headings written as a story a non-engineer can follow ("Explore the site, then write a plan" — not "Discoverer phase").
- If a step is a synchronous ask-and-answer, write it as one step ("asks the DB for X, gets X back"), not two.
- End with the concrete deliverable returned to the user.

## `## Side paths and scheduled flows` _(only if any exist)_

Audit logging, metrics, retry/fallback paths, nightly jobs — each in 1-2 sentences, explicitly flagged as optional or scheduled, so downstream diagrams know they may be dropped from simplified views and are not part of the main request chain.

## `## Deployment constraints` _(only if any exist)_

Anything a simplified diagram must not abstract away because it is a real operational fact: components that must share a host or volume, a broker that is the _only_ path between two services, ordering/startup dependencies.

Before you finish, verify the document against this checklist and fix any failure:

1. Every component named in the scenario appears in Components; every hop in the scenario matches a row in Connections; every From/To in Connections appears in Components or External dependencies. No orphans in any direction.
2. Every Connections row has a concrete Pattern — no row says "integrates", "talks to", or "uses".
3. The scenario touches at least ~80% of the internal components; if it can't, say which components are off the main path and why.
4. Someone could draw this system accurately without opening the code. Any sentence that requires the code to disambiguate is not finished.
5. Only what the code does today — no roadmap items, no aspirational features, no marketing language.
