---
name: screencast
description: Guide a screencast from idea through publication.
disable-model-invocation: true
---

# Screencast

Move a screencast through five **gates**. Load and follow the matching phase skill rather than improvising a second workflow.

## Route

| Current state | Load | Gate reached |
| --- | --- | --- |
| An idea, topic, or source material | `screencast-plan` | A recordable production brief exists |
| A production brief, but no tested capture setup | `screencast-setup` | A test recording has passed |
| A tested setup, but no usable footage | `screencast-record` | The current batch has verified takes |
| Raw footage or a rough timeline | `screencast-edit` | Feedback is returned or the final timeline is approved |
| An approved timeline or finished master | `screencast-publish` | The published video works for its audience |

If the user names a phase or already has its input, start there. For an end-to-end request, run the phases in order and carry each phase's handoff into the next.

For a series, use a **batch loop** rather than recording everything first:

1. Record a few short lessons with `screencast-record`.
2. Run a feedback rough cut with `screencast-edit`.
3. Apply discoveries to the plan, setup, or recording method.
4. Record the next batch.
5. Run the final editing pass when the latest feedback edit found no unresolved production-wide change and the ledger shows verified takes for every planned lesson in the release.

## Intake

Inspect any supplied topic, footage metadata, project files, platform requirements, or existing production documents before asking questions. Establish only what is needed to route:

- intended viewer and outcome
- single video or series
- current phase and existing artifacts
- target platform or delivery context
- deadline and meaningful constraints

Ask only for facts that cannot be discovered and that block the next gate. When a preference is missing but reversible, state a sensible default and proceed.

For a series or multi-session production, maintain a durable production ledger in the user's chosen location. If no format exists, use one row per video with `Planned`, `Setup tested`, `Recorded`, `Rough cut`, `Final`, and `Published` status plus links to its brief, media, timeline, and canonical URL.

Perform media and platform actions directly when the available tools support them. Otherwise, give the user one focused action block, request the resulting file, screenshot, metadata, or confirmation, and evaluate that evidence before continuing. A gate remains open until either direct observation or explicit user confirmation proves it passed.

## Operating Principle

Optimize for **high quality, quickly**: protect clarity, intelligibility, and viewer focus; simplify everything else. Recommend gear, effects, or process only when it solves an observed problem. A shipped, useful screencast is the objective.

At every gate, summarize:

- what is complete
- decisions carried forward
- unresolved risks
- the exact input ready for the next phase
