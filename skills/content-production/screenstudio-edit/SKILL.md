---
name: screenstudio-edit
description: Edit or reconstruct a Screen Studio .screenstudio project for vertical or horizontal delivery. Use when applying feedback in Screen Studio, preserving its cuts while reframing screen and camera, rebuilding from raw package sources after export fails, synchronizing microphone, captions, cursor, and speed changes, or producing technically validated social-video exports.
---

# Edit With Screen Studio

Treat Screen Studio as both an editor and a source package. Choose the shallowest path that provides enough control while keeping the original recording recoverable.

This is an adapter for `video-edit`, which owns story, pacing, repair, captions, audio, orientation, and approval policy. Load `video-edit` first; this skill implements those decisions in Screen Studio or from its package sources.

## 1. Choose The Path

- **Native edit:** duplicate or version the project, edit and export in Screen Studio, then inspect the encoded file independently.
- **Reconstruction:** read the project non-destructively and rebuild from raw sources when export is blocked, programmable layouts are required, or native reframing cannot keep proof readable.

Keep the original `.screenstudio` package unchanged when reconstructing. Read [the project reference](references/screenstudio-project.md) before depending on internal files.

For a native project edit, read [the native workflow](references/native-workflow.md) and preserve a versioned copy before changing timeline structure.

## 2. Implement The Approved Edit

Take the rough/fine-cut decisions and review gates from `video-edit`. Inside Screen Studio or the reconstruction:

1. preserve synchronized source relationships while applying the cut list
2. retain approved native cuts and speed changes where they already satisfy the edit
3. implement the selected reusable layout for each scene
4. export short review ranges for timing or renderer risks

Version the project before large layout or timing changes.

## 3. Reconstruct From One Segment Map

When using raw package sources, convert edited slices into one monotonic segment map containing source interval, source time scale, mute state, output interval, and any additional silence removals.

Derive everything from it:

- screen and camera trims
- microphone and optional system audio
- transcript words and caption groups
- cursor samples
- scene cues and transition events

Use one dialogue source, normally the enhanced microphone. Keep screen and camera video muted in the final composition to prevent doubled speech.

Read [the synchronization reference](references/screenstudio-project.md) for formulas and FFmpeg patterns. The map passes when all streams share duration and lip sync holds after cuts near the beginning, middle, and end.

## 4. Compose The Destination

Use the applicable `video-edit` orientation branch. A vertical and horizontal version may share segment timing while using independent layout maps.

Crop private status areas before scaling. Use cover in assigned regions, pan toward active proof, and change split proportions when readability requires it. Read [the composition reference](references/composition.md) for source-space crop math and reusable layouts.

## 5. Export And Prove

Render representative stills for every layout, then the full master. Normalize delivery range and color tags only after measuring the source. At minimum, decode video and audio fully, inspect stream/color metadata, scan black frames, measure loudness and peak, inspect a contact sheet, and watch the final encoded file at target size. Use [the export reference](references/export-qc.md) for command details.

```markdown
## Screen Studio Editing Handoff
- Original project and preserved copy:
- Path: native / reconstruction
- Project version or segment-map path:
- Canonical orientation and variants:
- Dialogue/system-audio choice:
- Review stills or ranges:
- Master and final exports:
- Decode, black-frame, color, loudness, and playback QC:
- Creator approval: pending / <evidence>
```

The implementation gate passes when the original project is recoverable, every synchronized stream has one timing source of truth, layouts fill their intended regions without privacy leaks, and the final encoded file passes technical and visual review. The master is approved only when the `video-edit` creator-approval gate also passes.
