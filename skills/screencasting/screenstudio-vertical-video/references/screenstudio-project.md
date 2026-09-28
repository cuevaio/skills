# Screen Studio Reconstruction Reference

Use this branch when Screen Studio cannot export the desired result or when a programmable vertical composition is required.

## Package Discovery

A `.screenstudio` project is a package directory. Common useful files include:

- `project.json`: project metadata and edit slices; some versions wrap the payload under `.json`
- `recording/channel-2-display-0.mp4`: display capture
- `recording/channel-4-webcam-0.mp4`: webcam capture
- `recording/enhanced/channel-3-microphone-0-enhanced.m4a`: enhanced microphone
- `recording/channel-1-system-audio-0.m4a`: system audio
- `transcripts/microphone-session-0.json`: word timestamps
- `recording/mousemoves-0.json`: cursor samples

These names are observations, not a stable public contract. Inventory every package and inspect media metadata before use.

The first scene's slices have commonly exposed:

```ts
type SourceSlice = {
  sourceStartMs: number;
  sourceEndMs: number;
  timeScale: number;
  volume: number;
  systemAudioVolume?: number;
};
```

Verify whether `timeScale` means output duration divided by source duration in the project being handled. Confirm with a known clip before processing the entire timeline.

## The Segment Map

For a chosen global speed `SPEED`, a retained interval maps as:

```ts
outputDurationMs =
  ((sourceEndMs - sourceStartMs) * timeScale) / SPEED;

outputTimeMs =
  outputStartMs +
  ((sourceTimeMs - sourceStartMs) * timeScale) / SPEED;
```

Video uses:

```text
trim=start=SOURCE_START:end=SOURCE_END,
setpts=(PTS-STARTPTS)*(timeScale/SPEED),
fps=30
```

Audio uses:

```text
atrim=start=SOURCE_START:end=SOURCE_END,
asetpts=PTS-STARTPTS,
atempo=(SPEED/timeScale),
aresample=48000
```

Chain `atempo` factors when the required value falls outside the filter's supported range.

Concatenate every screen segment, camera segment, and microphone segment in identical order. Add tiny audio fades at segment edges when needed to suppress clicks.

## Silence Tightening

Detect candidate silence on the chosen microphone track, but decide removals within each existing Screen Studio slice. A useful starting policy is:

- consider silence longer than 400 ms
- preserve roughly 60 ms at speech edges
- keep retained fragments at least 180 ms long
- cap intentionally muted loading beats near 300 ms rather than deleting all visual context

Treat these as tunable editorial defaults. Verify every aggressive join by listening; waveform silence alone cannot prove that a removal preserves meaning.

Represent muted beats as explicit silent audio segments so every stream keeps the same duration.

## Transcript, Cursor, And Scene Cues

Map each transcript word through the segment containing its midpoint. Drop words in removed or muted intervals and clamp retained word boundaries to the segment. Build readable caption groups only after mapping.

Map cursor samples with the same function and downsample only after mapping. This keeps cursor motion aligned through cuts and speed changes.

Find scene cues by tokenized transcript phrases with a fallback timestamp. Phrase-driven cues survive upstream cut changes better than unexplained frame numbers.

## Audio Source Rule

Choose one microphone track as dialogue. Enhanced microphone plus camera audio or screen audio commonly creates doubled speech. Keep all video components muted and add dialogue once at the composition root. Mix system audio separately and only for moments where it conveys useful information.

Before composition, prove that screen, camera, and dialogue outputs have matching durations with `ffprobe`, then inspect lip sync near the beginning, middle, and end.
