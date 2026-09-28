---
name: screenstudio-vertical-video
description: Create a polished vertical short or reel from an edited Screen Studio .screenstudio project. Use when preserving Screen Studio cuts while reframing screen, camera, microphone, captions, and cursor for 9:16; rebuilding from raw project sources after Screen Studio export fails; or producing synchronized H.264/AAC social-video exports with technical QC.
---

# Build A Vertical Video From Screen Studio

Treat the Screen Studio project as an edit decision list, not as a flattened source. Build every derivative from one **segment map** so screen, camera, dialogue, captions, cursor, and scene changes stay synchronized.

Choose the path:

- **Native export:** use Screen Studio when it can produce the required composition cleanly.
- **Reconstruction:** read the project non-destructively and rebuild from its raw sources when export is blocked, framing is too limited, or the vertical edit needs programmable layouts.

## 1. Protect And Inspect

Keep the original `.screenstudio` package unchanged. Work in a separate project and write generated media elsewhere.

Inventory the package before assuming channel names or schema. Locate:

- `project.json` and its edited slices
- display and webcam recordings
- enhanced microphone and system-audio tracks
- microphone transcript
- cursor samples

Screen Studio's package format is an implementation detail, so validate the discovered fields against actual clip durations and a few visible cut points. Read [the project reference](references/screenstudio-project.md) when reconstructing a package.

This step is complete when every source is identified, the preferred dialogue track is explicit, and at least three edit points match the Screen Studio timeline.

## 2. Build One Segment Map

Convert the edited slices into a monotonic list containing source start, source end, source time scale, mute state, output start, and output end. Apply any global speed-up and silence tightening here—once.

Derive all timing from this map:

- trim and concatenate display and webcam video with identical segments
- build dialogue from the same source intervals and tempo changes
- remap transcript words and cursor timestamps through the same function
- derive scene cues and transition sounds from mapped transcript phrases or mapped cuts

Use one dialogue source. Prefer the enhanced microphone; include system audio only when the demonstration needs it. A camera or screen file that also carries audio must remain muted in the composition, or it can create echo and doubled speech.

Read [the synchronization reference](references/screenstudio-project.md) for formulas, silence handling, and FFmpeg filter patterns.

The map passes when every output timestamp is monotonic, all generated streams have matching duration, and dialogue remains lip-synced at several points after cuts.

## 3. Reframe For 9:16

Create a 1080×1920, 30 FPS composition unless the destination requires another format. Use reusable layouts rather than clip-by-clip coordinates:

- face-only when the presenter is the content
- camera above screen for demonstrations
- screen-only when readability needs the full canvas
- designed graphic scenes for concepts, logos, or transitions

In camera-and-screen layouts, both regions must touch and fully occupy the frame. Crop the source status bar before scaling the screen to **cover** its assigned region. Pan the crop toward the active prompt or result; change camera height when that gives the screen enough readable width while keeping the face visible.

Use locally bundled fonts and transparent official assets. Keep recurring typography, crops, and spacing in named components. Read [the vertical layout reference](references/vertical-layout.md) for cover math, privacy crops, caption placement, and review frames.

The layout passes when no split frame contains letterboxing or a gap, no system status bar or private notification is visible, and the important screen text is readable at phone size.

## 4. Tighten The Story

Intercut screen evidence with face, diagrams, logos, and concise text so each visual answers what the narration is discussing. Keep graphic transitions brief and use sound effects as scene-change cues, not decoration.

Generate captions from the mapped transcript, then correct product names, code terms, and punctuation manually. Prefer short caption groups that can be read in one glance. Keep captions inside the current platform safe zone and review them with simulated Reels controls before export.

The edit passes when the opening establishes value quickly, every visual supports the current sentence, captions match speech, and the ending contains the intended invitation or next step.

## 5. Export And Prove The File

Render a high-quality H.264/AAC master, then normalize delivery metadata explicitly. Screen recordings often carry full-range pixels or an ICC profile; the social export should be yuv420p, limited-range BT.709 with primaries, transfer, and matrix all tagged.

Run the complete checks in [the export and QC reference](references/export-qc.md):

1. type-check or build the composition
2. render targeted stills for every reusable layout
3. render and finalize the full video
4. decode the entire video and audio streams
5. scan for black frames and source dropouts
6. inspect codec, dimensions, frame rate, range, and all color tags
7. measure integrated loudness and true peak
8. inspect a contact sheet and watch the final file at phone size with sound

## Completion Handoff

```markdown
## Vertical Video Handoff
- Source Screen Studio project:
- Reconstruction path and generated segment map:
- Master composition:
- Final export:
- Caption placement and safe-zone evidence:
- Dialogue/system-audio choice:
- Visual review frames:
- Decode, black-frame, color, and loudness QC:
- Original project unchanged: yes / no
```

The skill is complete only when the original project is intact, one segment map accounts for every synchronized stream, and the final delivery file passes both technical QC and normal-speed playback review.
