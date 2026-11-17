---
name: talking-video-prompt
description: Write a ready-to-paste prompt for an AI video generator that makes a short talking-presenter clip: a person in a scene looks at the camera and speaks a short script, with lip sync, timed pauses, gestures tied to specific words, and a call to action. Typically a teaser of 8–15 seconds that promotes a blog post, article, feature or launch on social media. It writes the script from the source (hook, one-line answer, call to action), times it to fit the target length, ties gestures to props or panels in the starting image, and adds the motion, stability and style lines that keep the clip clean. Use when someone asks for a "video prompt", "video generation script", "talking head prompt", "a prompt like this one for my other post", "make it under 10 seconds", or wants a short spoken promo clip described for a video model. Not for producing the video itself, screen-recorded demos (use demo-video), narrated walkthrough scripts (use demo-script), or podcasts (use demo-podcast).
---

# Talking video prompt

A short promo clip has about ten seconds to do three things: make someone stop scrolling, say
what the post is about in one breath, and point at the link. A video model will do all of that
well only if the prompt tells it exactly what to say, when to pause, where to look and what to
leave alone. This skill writes that prompt.

## What to gather first

- **The source.** The post or feature the clip promotes. Read it, and take the hook and the
  one-line answer from its own framing and terms (its tagline, its "think of it as" lines, its
  running example).
- **The presenter and scene.** Usually a starting image the user already has, such as a cover
  photo. Describe the presenter by what's visible ("the man in the blue shirt"), never by a real
  person's name. Only use a person the user has the rights to show, and never script a real,
  identifiable person saying things they didn't say.
- **Props.** Anything in the image the presenter can gesture at: panels on a whiteboard, objects
  in each hand, a screen.
- **Target length.** Default to under 10 seconds unless the user says otherwise.
- **Image-to-video or text-to-video.** If the scene contains writing (a whiteboard, a slide, a
  sign), recommend image-to-video with the user's image as the first frame. Video models redraw
  text badly, so the words should come from the image.

## The script formula

Three or four short lines:

1. **Hook:** a question the target reader is already asking, built from the post's own terms.
   "Semantic model, ontology, knowledge graph. Same thing?" /
   "Your AI agent has access to tools, but does it know how to use them efficiently?"
2. **Answer:** the post's core idea in one sentence, ideally a list of three that matches what's
   on screen. "No. Math, meaning and facts: three different jobs."
3. **Bridge** (optional, longer clips only): "Want to see how it works?"
4. **Call to action:** "Check out the link below." or just "Link below."

Write for the ear: short words, no acronyms the listener can't decode, no claims the post
doesn't make.

## Timing

Speech runs about **2.5 words per second** at a natural, unhurried pace. Add every pause.

| Target | Budget | Shape |
|---|---|---|
| Under 10 s | ~15 words, two 1 s pauses | Hook, answer, "Link below." |
| 10–15 s | ~25 words, 1–1.5 s pauses | Hook, answer, bridge, CTA |
| 15–20 s | ~35 words, 1.5 s pauses | As above, with a fuller answer sentence |

Always state the estimated duration and how you got it ("about 6 seconds of speech plus two
1-second pauses"). If a line won't fit, shorten the line; don't shorten the pauses below 1 second.

## The prompt template

```
[Presenter description] [position in the scene], turns to the camera and speaks the following script in a natural, clear, and engaging tone[, with a pause of 1–2 seconds after each sentence]:

"[Hook]"

Pause for [N] second(s).

"[Answer]"

Pause for [N] second(s).

"[Bridge — optional]"

Pause for [N] second(s).

"[Call to action]"

His/Her/Their lips move in perfect sync with the dialogue, respecting the pauses between sentences. [Gesture line: tie each named item to one prop, in order, on a specific word.] [He/She/They] maintain(s) natural facial expressions and subtle head movements during the pauses. [Prop motion: how each prop moves, gently.] [Stability line, if there's text in the scene: "The whiteboard stays steady and in focus, and its drawings do not change."] [Background: one short phrase.] Cinematic lighting, smooth motion, realistic gestures, and natural speech timing. Do not rush the dialogue; ensure clear sentence breaks and deliberate pauses.
```

Use the pronoun that matches the presenter as the user described them; if unsure, use "they" or
repeat the description.

## Rules that keep the clip clean

- **One gesture per named item, on a specific word.** "As he says 'math', 'meaning' and 'facts',
  he gestures towards the left, middle and right panels in turn." Gestures tied to single words
  sync better than gestures tied to whole sentences.
- **Keep props moving gently.** Use words like "gently rotate", "slowly spins", "pulses with
  light". Big motion pulls attention from the face and breaks lip sync.
- **Pin anything with text.** Add the stability line whenever the scene has writing, and suggest a
  wider starting frame if the text still shimmers.
- **Spell out the pauses.** Write each pause as its own line ("Pause for 1 second."), not as a
  parenthesis inside the dialogue.
- **End with the anti-rush line.** Models tend to compress speech; "Do not rush the dialogue"
  helps.

## What to hand back

1. The prompt in a single fenced code block, ready to paste.
2. The estimated duration, with the arithmetic.
3. Two or three short notes: image-to-video vs text-to-video, a shorter fallback line if the tool
   caps length, and what to drop if the gestures misfire.

When the user asks for a change ("shorter", "under 10 seconds", "different hook"), return the
full revised prompt again, plus one line on what changed.

## Check before you send

1. Does every spoken line use the source's own terms, with no claim the source doesn't make?
2. Does the duration estimate, pauses included, fit the target?
3. Is every gesture tied to a prop that is actually in the starting image?
4. If the scene has text, is there a stability line and an image-to-video recommendation?
5. Is the presenter described by appearance, not by a real person's name?
