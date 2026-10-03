# Full-camera reference lessons

The user requested the style in ~/projects/atomic-video-01: full camera, aggressive cuts, no empty silences, its font and subtitle position. Inspect src/AtomicMemoryReel.tsx, scripts/tighten-media.ts, and actual final frames when the project is available. Those files informed the precise Space Grotesk caption settings in SKILL.md.

The reference removes silence of at least 400 ms with 60 ms handles and runs speech at 1.25×. The interview revision used measured silence at -35 dB lasting at least 300 ms, 60 ms handles, and pitch-preserving 1.15× speech. These are observed choices, not universal audio thresholds. Adjust for background noise and the actual voice. Detect on audio rather than treating every Whisper timestamp gap as silence.

Every retained segment has sourceStart, sourceEnd, outputStart, outputEnd, frame count, and effective rate. Round output durations to frames; apply that effective rate to video, audio and words. Bound each audio segment to its frame duration, use 4 ms fades to prevent clicks, and concatenate once. Rebuild SRT from the remapped words. Never pair a tightened video with the original subtitles.

For the 1920×1080 two-person source, Lauren is on the right. The final portrait crop is 540×960 at x=1184, y=0. These values are historical examples; the current helper requires explicit portraitCrop and splitCrop metadata. Cropping the full source height left a sliver of the blue interview name tag visible. Inspect base and punch crops, including the bottom edge. This crop is specific to this source, not a generic setting.

Use roughly 10% hard punch-ins. The initial revision used 850 ms image flashes; the creator rejected that pacing. Follow sustained-visuals.md for the current full-screen and camera-above-image layouts, held through the relevant explanation. Do not substitute frequent animations for actual removal of empty pauses.

The reusable tightening script expects the original prepared clips.json, source excerpt MP4s, and the existing project directory structure. It archives the original metadata and exports before applying edits, and reads that archive on reruns so the operation does not tighten a second time. Output review/tightening.json records all source intervals and duration changes. Preserve the archive when shipping the project.
