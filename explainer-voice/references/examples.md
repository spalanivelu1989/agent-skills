# Explainer voice: worked examples

Each example shows a flat "before" and the same content rewritten in the explainer voice. The facts
don't change; only the order, the framing and the sentences do. The scenarios are illustrative. In
real work, use only the facts, names and quotes you actually have.

---

## 1. Short answer (2 paragraphs): "Why is my query slow after the table grew?"

**Before**

> The query is slow because there is no index on `status`. PostgreSQL performs a sequential scan.
> Add an index with `CREATE INDEX ... ON orders(status)`. This will improve performance significantly.

**After**

> The table didn't get slower; it got bigger, and your query has been reading all of it every time.
> Without an index on `status`, PostgreSQL has no shortcut, so it does a *sequential scan*: it walks
> every row of `orders` and checks each one. At 10,000 rows that took a few milliseconds and nobody
> noticed. At 4 million, it's the 1.8 seconds you're seeing.
>
> An index is a sorted lookup table the database keeps beside the data, a bit like the index at the
> back of a book. With one on `status`, the planner can jump straight to the open orders instead of
> reading the whole book. `CREATE INDEX orders_status_idx ON orders(status);` should bring this back
> to milliseconds. (If almost every row is `open`, the planner may still choose to scan, because the
> shortcut doesn't skip much. In that case a partial index on the rare values is the better tool.)

What changed: the answer comes first in plain words. The jargon (*sequential scan*, *index*) is
defined where it appears, with a picture. Specific numbers replace "significantly". The honest caveat
goes in parentheses.

---

## 2. Long explanation: "How does our cache invalidation work?" (opening and mechanism)

**Before**

> ## Overview
> The cache layer uses Redis with TTL-based expiry and event-driven invalidation.
> ## Components
> - Write service publishes `entity.updated` events
> - Cache service subscribes and deletes keys
> - TTL fallback of 300s
> ## Known issues
> - Race condition between read-through and invalidation

**After**

> Every product page our customers load, every price in the basket, every "only 3 left" badge, is
> read from a cache, not the database. And almost every cache bug we've had traces back to one
> question: when the data changes, how does the cache find out?
>
> The obvious answer is to let entries expire. Give each one a time to live (TTL), say five
> minutes, and accept that a price might be stale for that long. For a long time that was the whole
> design. The trouble is that five minutes is both too long and too short. It's too long for a price
> change during a sale, and too short to protect the database on a busy morning.
>
> So the write service now announces its changes. Whenever it updates a product, it publishes a
> small message, `entity.updated`, saying which product changed. The cache service listens for these
> messages and deletes the matching key. The next read misses, goes to the database and refills the
> entry with the new value. The TTL stays as a safety net: if a message is ever lost, the stale
> entry still dies within five minutes.
>
> Consider two customers loading the same product a few milliseconds apart, just as its price
> changes. The first customer's read misses the cache and goes to the database, where it picks up
> the *old* price. Meanwhile the update lands and the invalidation message deletes the key, which is
> already empty. Then the first read finishes and writes the old price back into the cache. The
> second customer now sees a price that no longer exists, and will keep seeing it until the TTL
> runs out. Nothing failed, and every component did exactly what it was told. The bug is in the
> timing between them.

What changed: the headings and bullets became an arc. It opens with the big world (every page),
narrows to the one question, then gives the naive fix and why it falls short, the turn ("So …"), the
mechanism step by step, and a minimal running example (two near-simultaneous reads) that exposes the
race. A one-line verdict ends the paragraph.

---

## 3. Status-style reply: barely any change

**Before**

> I have successfully completed the requested task of updating the configuration file. The changes
> have been applied.

**After**

> Updated `config/app.yaml`: the timeout is now 30 s (it was 5 s). Nothing else changed.

At this size the voice is just plain words, the point first, and specifics. No arc and no imagery.

---

## 4. Closing paragraph of a design note

**Before**

> In conclusion, the new approach offers several benefits including improved latency, better
> scalability, and reduced cost. Future work includes evaluating alternative strategies.

**After**

> So we still don't know whether the queue will hold at ten times today's traffic. The load test
> says it will, but the load test also said that about the last design. What we do know is that the
> slow part is no longer the part we can't see. When the next bottleneck arrives, and it will, it
> will at least show up on a graph.

What changed: no recap. It says what is known and what isn't, and ends on a short line that widens
the frame.
