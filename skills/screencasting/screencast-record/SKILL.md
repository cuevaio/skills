---
name: screencast-record
description: Guide a screencast recording session and produce usable takes efficiently. Use for rehearsal, intros and outros, recording in chunks, synchronizing screen and voice, handling mistakes, demonstrating software, or recovering momentum during capture.
---

# Record A Screencast

Record **chunks**, not a perfect performance. A chunk is one complete thought or screen action with clean handles on both sides.

Operate the recorder directly when tools permit it. Otherwise, act as the session producer: give the presenter one chunk and its reset instructions at a time, collect their take log and playback observations, and evaluate supplied clips or evidence. Never claim a take is verified without direct playback evidence or the presenter's explicit confirmation.

## Process

### 1. Open The Session

Require a minimal record card before capture: intended viewer outcome, current batch of beats, delivery prompts or script, demo start/reset state, required sources, and privacy risks. If no production brief exists, establish those fields now or load `screencast-plan`.

Require a passed capture test and checklist. At minimum confirm the intended screen or region, microphone, camera and system audio when used, readable screen layout, notifications, private data, storage, and record/stop controls. If these are not known, establish and test them now or load `screencast-setup`. Repeat the short test whenever the room, device, application, or source configuration changed.

Prepare a take log containing the lesson or beat, take number, status, and any note for editing. Confirm the recorder is actively capturing all required sources before delivering content.

### 2. Rehearse The Next Chunk

Work one beat ahead, not one video ahead:

1. Identify the thought or action to land.
2. Rehearse it aloud once or twice.
3. Set the screen to the chunk's documented starting state.
4. Return the presenter and cursor to a consistent resting position.

For on-camera openings, relax the face and begin with a natural, welcoming expression. Open directly, or bridge briefly from what the viewer already learned. For serialized lessons, avoid repetitive ceremony. Close by landing the takeaway; a summary and natural downward cadence are usually enough.

### 3. Capture Screen And Voice Together

Perform and explain the screen action at the same time unless a deliberately polished voice-over is part of the brief. Simultaneous capture preserves real reactions, makes timing legible, and reduces synchronization work.

Keep the viewer oriented:

- say what matters before or as attention should move there
- keep the cursor still when it is not communicating
- narrate decisions and reasoning, not every mechanical click
- voice the viewer's likely objection when it builds trust or creates the next transition
- let personal experience clarify a recommendation after the facts are clear

### 4. End Cleanly And Choose The Take

At a natural end-of-thought or visual transition:

1. Finish the sentence.
2. Return to the resting position.
3. Leave a few seconds of silence and a stable screen.
4. Mark the take as preferred, alternate, or reject.

The silence and stable frames are **handles** the editor can cut, crossfade, or freeze.

### 5. Handle Mistakes By Size

| Mistake | Response |
| --- | --- |
| Harmless typo or small misspeak | Correct it naturally and continue when the correction helps the viewer |
| Broken delivery or confusing screen state | Pause, reset to the chunk's start, and retake the chunk |
| Uncertain fact, unexplained result, or unsafe action | Stop, verify, repair the demo state, then retake |
| Missing source or failed capture | Preserve what is usable, fix preflight, and record again |

Use an intentional mistake only when it mirrors a likely learner attempt and its failure teaches the correction. Never fabricate uncertainty or leave a misleading result unresolved.

### 6. Review In Small Batches

After a few chunks or one short lesson, stop and verify playback before recording a large batch. Check source presence, sync, audio quality, screen readability, continuity, and factual correctness. Send a small series batch through a feedback rough cut in `screencast-edit`; apply what it reveals before capturing the next batch.

Save a restorable snapshot of the demonstrated state after each lesson when future revisions may require it: a duplicated document, fixture, seed, project archive, or clean version-control commit when appropriate. Do not disturb unrelated work to create a snapshot.

The recording gate passes when every beat in the current batch has a preferred verified take, the take log identifies it, source and demo snapshots needed for revisions exist, and no known factual, privacy, capture, or continuity failure is deferred to editing without a specific repair.

Return or save this handoff:

```markdown
## Recording Handoff
- Batch and lessons:
- Media locations:
- Preferred takes and alternates:
- Demo/source snapshots:
- Pickups still required: none / <list>
- Edit notes and known repairs:
- Playback evidence and result:
```
