# Camera cuts and shared timing

Use the saved preset for pause thresholds, speech speed, caption typography and punch-ins. Adjust audio detection for background noise and the actual voice. Detect pauses from audio rather than treating every Whisper timestamp gap as silence. Preserve speech handles, completed ideas and the final words.

Every retained segment has sourceStart, sourceEnd, outputStart, outputEnd, frame count and effective rate. Round output durations to frames and apply that effective rate to video, audio and words. Bound each audio segment to its frame duration, use short fades to prevent clicks, and concatenate once. Rebuild SRT from the remapped words. Never pair tightened media with original subtitles.

Inspect the current source dimensions, speaker location and overlays before setting portraitCrop and splitCrop. Preview base and punch crops, including the bottom edge, to exclude dividers and unwanted labels without clipping faces or gestures. A speaker's side and crop are never inherited from a previous recording.

Use modest hard punch-ins at actual edits. Remove empty pauses rather than substituting decorative motion. Hold related imagery through its explanation using [sustained visual guidance](sustained-visuals.md).

The tightening helper archives the original prepared metadata and exports, then reads that archive on reruns so it does not tighten twice. Its review report records source intervals and duration changes. When changing source ranges, words or crops, create a new production version rather than silently reusing a stale archive.
