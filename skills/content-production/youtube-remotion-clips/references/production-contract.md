# Production contract

Run helpers from the production workspace, not from the skill directory. Use a compatible Python environment with `requirements.txt`; use the saved package lock for `npm ci` only when the shared runtime is unavailable. The Python requirements record the versions used in the original production, not an assertion that they are the latest releases.

## Inputs

`source/video.mp4` is the canonical recording. `transcript/transcript.json` comes from the word-timestamped Whisper helper. `edit-plan.json` is an array; each selected clip needs:

```json
[
  {
    "id": "clip-one",
    "title": "a clear, source-backed title",
    "start": 10.0,
    "end": 35.0,
    "color": "#9fe7d0",
    "portraitCrop": "crop=540:960:690:0",
    "splitCrop": "crop=960:960:480:0",
    "coverTime": 1.0,
    "reason": "one complete idea and why it is useful"
  }
]
```

Those crop values are illustrative for a 1920-pixel-wide source. Inspect dimensions, speaker location and overlays before specifying yours. `coverTime` is in the final tightened clip's seconds; select it after inspecting that timeline. You can update it in `remotion/clips.json` before running `prepare_covers.py`. Clip ids must be filename-safe and valid Remotion composition ids. Keep source attribution and source URL in `provenance.json`.

`prepare_clips.py` creates local captions and source slices. `tighten_clips.py` reads its archived original plan on reruns so it does not tighten twice. If changing source ranges, words or crops, create a new production version rather than silently reusing an old archive. It writes the shared retained segments and revised SRTs. `prepare_split_media.py --force` rebuilds a stale wide-camera variant after timeline changes.

## Visual plan

Generate topic images from `image-prompts.md` into `remotion/public/` and record their prompts and provenance. Filenames below refer to generated production outputs, not bundled resources. After tightening, write `visual-plan.json` with exactly one entry per current clip. Choose image holds by spoken meaning, using final output timestamps. For example:

```json
[
  {
    "id": "clip-one",
    "highlightColor": "#9fe7d0",
    "cutaways": [
      {
        "at": 5.0,
        "duration": 4.0,
        "layout": "full",
        "image": "kitchen.png",
        "objectPosition": "48% 50%",
        "visualStart": 5.0,
        "visualEnd": 15.0,
        "reason": "the speaker explains the kitchen analogy"
      },
      {
        "at": 9.0,
        "duration": 6.0,
        "layout": "split",
        "image": "kitchen.png",
        "objectPosition": "48% 50%",
        "visualStart": 5.0,
        "visualEnd": 15.0,
        "reason": "hold the illustration through the rest of the explanation"
      }
    ]
  }
]
```

The example requires a clip longer than 15 seconds. The planner checks ids, available files, timeline bounds and non-overlapping passages before saving metadata. `prepare_covers.py` extracts the camera at `coverTime` from the synchronized split media and pairs it with the first related illustration. Choose a different cover image in metadata if appropriate.

`configure_sound.py` measures the opening voice, adds a soundEffect entry to each clip, and records provenance before Remotion rendering. Missing private sound is a setup issue, not permission to silently omit the requested effect. Use `--disable` only when the task calls for no sound.

## Outputs and phase ownership

- source selection: `content-repurpose`, with source ranges and complete ideas in `edit-plan.json`.
- rendering: `youtube-remotion-clips`, with `remotion/clips.json`, `review/`, `clips/*.mp4`, `clips/*.srt`, `covers/*.png` and `provenance.json`.
- accompanying copy: `social-post`, using clip ids, speaker/interviewer names, source URL, actual claims and creator-confirmed takeaways. save platform variants in `social-copy.json`, covering Instagram, LinkedIn, X, YouTube Shorts, Threads, TikTok and any additional available Buffer accounts. Preserve channel IDs for multiple accounts on the same service and record blocked destinations.
- prepare/publish: `content-publish`, consuming those finished assets and carrying forward existing authorization.

Keep raw full transcripts unchanged. Refined excerpt transcripts go into `transcript/<clip-id>/transcript.json`. Images are conceptual unless they depict independently verified evidence. A source's personal story remains their own in all derivatives.
