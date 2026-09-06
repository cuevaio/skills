---
name: screencast-edit
description: Turn raw screencast footage into a clear, approved timeline efficiently. Use for feedback edits, rough cuts, repairing jump cuts or screen discontinuities, improving audio, using crop, B-roll, freeze frames or punch-ins, applying presets, captions, and final quality control.
---

# Edit A Screencast

Edit in distinct passes. The **rough cut** decides what the video says; the **fine cut** decides how smoothly the viewer receives it.

Choose the mode before editing:

- **Feedback edit:** rough-cut a small early batch, report changes needed in planning, setup, or recording, and return to `screencast-record` before more capture.
- **Final edit:** complete every pass and hand an approved timeline to `screencast-publish` for export.

Operate the editor directly when tools permit it. Otherwise, provide exact editor-neutral operations, inspect exported review clips, timeline screenshots, transcripts, or metadata, and request the user's playback confirmation. Keep the relevant gate open until the evidence supports it.

## Process

### 1. Protect And Organize

Keep original recordings intact and confirm they are backed up before destructive media operations. Import and synchronize screen, microphone, camera, and system audio. Use the take log when available to identify preferred takes.

Create or confirm the final canvas, aspect ratio, frame rate, and audio layout before detailed work. Keep edits non-destructive where the editor supports it.

### 2. Make A Fast Rough Cut

Move quickly through the whole recording:

1. Assemble preferred chunks in teaching order.
2. Remove false starts, abandoned takes, long waits, and content outside the promise.
3. Ripple-close gaps rather than manually dragging the remaining timeline.
4. Keep small human corrections that improve trust and comprehension.
5. Flag factual uncertainty, missing visuals, privacy leaks, or required pickups immediately.

Use silence and waveform gaps to locate chunk boundaries, but verify meaning by listening. The rough cut is complete when only content intended for the viewer remains and the lesson is factually coherent from start to finish.

### 3. Repair In Viewer-First Order

For each distracting cut, use the lightest repair that keeps the viewer oriented:

1. Cut on a natural pause or completed screen action.
2. Trim or crossfade detached audio to remove clicks and room-tone jumps.
3. Hold the screen while audio crosses the cut.
4. Cover a talking-head cut with relevant screen detail or B-roll.
5. Crop or duplicate the screen recording to isolate the window being discussed.
6. Use a freeze frame to mask a transient popup or preserve screen continuity.
7. Use a restrained punch-in on the presenter, aligning the eyes across the scale change.
8. Record a pickup when an edit would obscure meaning or misrepresent what happened.

Effects are repairs or teaching cues, not decoration. Keep motion, zooms, rounded corners, annotation, and transitions consistent. Avoid covering a mistake in a way that changes the truth of the demonstration.

### 4. Fine-Tune Attention

- Give important content enough screen area to be readable; use a full talking head only when the presenter is the content.
- Remove irrelevant interface rather than asking the viewer to ignore it.
- Use on-screen drawing or highlights only when they direct attention more clearly than narration and cursor movement.
- Keep gaze direction and inset placement visually coherent with the demonstrated screen.
- Apply named presets or copied properties for recurring layouts instead of recreating styling clip by clip.
- Balance speech first, then system audio and music. Preserve consistent loudness and natural room tone.
- Add accurate captions and verify technical terms, names, and code independently of automatic transcription.

### 5. Quality-Control The Timeline

For a final edit, watch the complete timeline at normal speed with headphones and at the likely playback size. Also scan it for gaps, disabled clips, accidental black frames, and source dropouts. A feedback edit stops after the rough cut once it has concrete changes to feed into the next recording batch.

The final-edit quality check passes when:

- the opening establishes value promptly and the ending lands the promised outcome
- speech is intelligible and consistent without clipping, clicks, or abrupt ambience changes
- screen text and actions remain readable and temporally aligned with narration
- cuts preserve visual context rather than making the viewer reconstruct state
- facts, commands, results, names, captions, and private information have been checked
- styling is consistent and every effect has a teaching or repair purpose
- the final timeline, caption file, and intended export specification are identified for publishing

Return or save this handoff:

```markdown
## Editing Handoff
- Mode: feedback / final
- Timeline or project path and version:
- Lessons reviewed:
- Recording/setup changes for next batch: none / <list>
- Pickups required: none / <list>
- Caption file:
- Export specification and destination:
- QC evidence and result:
```

The feedback gate passes when the rough cut identifies any pickups and states whether planning, setup, or recording needs a production-wide change. The final gate passes only when all final-edit quality-control criteria above hold and the approved timeline is ready for publishing without unresolved edit decisions.
