# Screen Studio Project Reconstruction

Use this branch when native editing or export cannot produce the required result.

## Package Discovery

A `.screenstudio` project is a package directory. Observed useful files include:

- `project.json`: metadata and edit slices; some versions wrap the payload under `.json`
- `recording/channel-2-display-0.mp4`: display capture
- `recording/channel-4-webcam-0.mp4`: webcam capture
- `recording/enhanced/channel-3-microphone-0-enhanced.m4a`: enhanced microphone
- `recording/channel-1-system-audio-0.m4a`: system audio
- `transcripts/microphone-session-0.json`: word timestamps
- `recording/mousemoves-0.json`: cursor samples

These names are observations, not a stable public interface. Inventory each package and inspect media metadata before use. If native export fails on an unsupported layout or camera shape, reconstruct rather than rewriting the original package in place.

Slices have commonly exposed:

```ts
type SourceSlice = {
  sourceStartMs: number;
  sourceEndMs: number;
  timeScale: number;
  volume: number;
  systemAudioVolume?: number;
};
```

Confirm the meaning of `timeScale` with a known clip before processing the full timeline.

## Segment Mapping

For global speed `SPEED`, an observed Screen Studio mapping is:

```ts
outputDurationMs =
  ((sourceEndMs - sourceStartMs) * timeScale) / SPEED;

outputTimeMs =
  outputStartMs +
  ((sourceTimeMs - sourceStartMs) * timeScale) / SPEED;
```

Video filter shape:

```text
trim=start=SOURCE_START:end=SOURCE_END,
setpts=(PTS-STARTPTS)*(timeScale/SPEED),
fps=TARGET_FPS
```

Audio filter shape:

```text
atrim=start=SOURCE_START:end=SOURCE_END,
asetpts=PTS-STARTPTS,
atempo=(SPEED/timeScale),
aresample=48000
```

Chain `atempo` factors when necessary. Concatenate identical intervals in identical order for display, camera, and audio. Add tiny audio fades when joins click.

## Silence Tightening

A useful starting policy—not a fixed rule—is:

- consider microphone silence longer than 400 ms
- preserve about 60 ms at speech edges
- keep retained fragments at least 180 ms
- cap intentionally muted loading beats near 300 ms instead of deleting all visual context

Decide removals within existing edited slices and represent retained muted beats as explicit silent audio so stream durations remain equal. Verify every aggressive join by listening.

## Transcript, Cursor, And Cues

Map each transcript word through the segment containing its midpoint. Drop removed words and clamp retained boundaries. Build caption groups after mapping.

Map cursor samples through the same function and downsample afterward. Derive scene cues from mapped transcript phrases with fallback times; phrase cues survive timeline changes better than unexplained frame numbers.

## Audio Rule

Choose one dialogue track. Enhanced microphone plus camera or screen audio commonly creates echo. Keep video components muted and add dialogue once. Mix system audio separately only when it communicates useful information.

Prove matching durations with `ffprobe`, then inspect sync around cuts near the beginning, middle, and end.
