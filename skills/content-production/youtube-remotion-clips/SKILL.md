---
name: youtube-remotion-clips
description: Create clips, reels or shorts from any YouTube URL or recording in the creator's default style automatically. Use for requests like "create 5 clips from this video" without requiring a style reference or a Remotion mention. Download with yt-dlp, transcribe with Whisper, and render tight camera cuts, highlighted captions, fresh images, split covers and an opening swipe.
compatibility: Requires Python, Node.js, FFmpeg and a Remotion-compatible browser. Downloads, uncached Whisper models and new images may require network access.
---

# Produce Remotion clips

This is the rendering adapter in the content-production collection, alongside `screenstudio-edit`. Keep tool-specific acquisition, timing, layout and exports here. Use `content-repurpose` for selecting complete source ideas, `video-edit` for editorial judgment, `social-post` for platform copy, and `content-publish` for delivery checks or authorized publication. Read sibling skills only when their phase is needed; if a dependency is not installed, follow the handoff below and report the missing capability instead of assuming it exists.

## Default for every clip request

Apply this collection's approved clip preset automatically whenever the creator asks for clips, reels or shorts. A request such as "create 5 clips from this YouTube video" is sufficient: download, transcribe, select five complete ideas, generate relevant images, render and verify the finished clips in the saved style. Do not ask which style to use or require the creator to mention a previous project, "my usual style", Remotion or this skill.

The visual style is a permanent creator preference, independent of source origin, speaker, subject and language. It applies to YouTube interviews, other hosted videos, local recordings, podcasts and screen recordings. Adapt source acquisition, transcription language, speaker crops and illustrative content to the new recording while retaining the preset. Source-specific interview names, timestamps, images and personal claims are not defaults.

Override the visual treatment only when the current request or an explicit project preference calls for another style. If no local `CONTENT_STYLE.md` exists, use the bundled preset directly; its absence is not a reason to ask again or choose a generic style. When the recording has no speaker camera, use the relevant source screen or footage in the camera region, keeping the same typography, timing, image treatment and audio defaults. Do not manufacture a speaker portrait.

## Style and resources

The default is already approved for Anthony. Use the approved [creator profile](../content-voice/references/creator-style.md) when installed and the bundled [style preset](assets/remotion/style.json). A project `CONTENT_STYLE.md` and current instructions override those defaults. For another creator, adapt the preset to their preferences. Social-copy lowercase does not change source quotations or subtitle spelling.

The usual treatment is 1080×1920 at 30 fps, full-bleed speaker camera, hard cuts with modest punch-ins, measured pause removal and pitch-preserving 1.15× speech. Adjust speed and silence thresholds for the actual voice. Keep completed ideas, necessary caveats and ending words.

Space Grotesk captions use 64 px, weight 620, white on translucent black, centered 320 px above the bottom with 65 px side insets. Highlight the active word in the clip accent. Hold related images through their explanation, using both full-screen and camera-top/image-bottom layouts. The accepted examples hold images for several seconds; do not repeat sub-second flashes. At frame zero, show a camera/image split with the title for exactly one frame, export a matching PNG, then resume without shifting audio. Mix a classic short opening swipe below the voice.

Bootstrap from this skill's actual location, rather than an assumed home path:

```bash
python3 <skill-dir>/scripts/bootstrap_project.py --workspace /path/to/production
```

The offline bootstrap copies the template, licensed font, image prompt references and production helpers, preserves existing editable files, and reuses matching local runtime and sound caches. The skill ships no images. Read [the image prompts](references/image-prompts.md), adapt a scene to the current spoken idea, and generate fresh illustrations into the production workspace. Record the actual prompt and generation provenance there. These are conceptual illustrations, not factual evidence. Use camera portraits from the current recording. Font and cache metadata are in [the resource manifest](assets/resource-manifest.json). Read [resource reuse](references/resource-reuse.md) for missing caches or another machine. `--sound required` checks the private swipe cache; `auto` records missing setup without downloading; `skip` omits it. The opening swipe is part of the default, even when not separately requested. Final delivery needs it unless the creator explicitly omits it; a missing cache is a setup issue to resolve or disclose, not a stylistic choice.

## Acquire and transcribe

Keep the full recording as `source/video.mp4`. Use open-source yt-dlp for YouTube, or copy the supplied local recording. Reuse available Python environments, Whisper models and the pinned Remotion runtime before installing anything. Read and follow [acquisition and transcription](references/acquire-transcribe.md) before the first download. Use its bundled `download_source.py SOURCE --workspace WORKSPACE` CLI as the default, rather than writing acquisition code. It handles yt-dlp, advertised-route fallback, resumable downloads, muxing, verification and the attempt report. Exit 0 means verified media; exit 2 means blocked acquisition; exit 1 means a setup/input error. Never guess companion URLs or treat page metadata as successful acquisition. Preserve raw transcripts and source provenance.

```bash
python scripts/transcribe.py source/video.mp4 --model small --output transcript
```

The CLI detects language unless `--language` is supplied. Choose a multilingual model for non-English audio. Use `--local-files-only` when the chosen model is cached. Refine selected excerpts with a larger model when useful and listen to names, technical words and low-confidence text. Full timestamps are absolute; excerpt timestamps begin at zero.

## Select and assemble

Read the transcript and choose complete, distinct ideas. `content-repurpose` owns the candidate ledger: source range, central idea, supporting explanation and selection reason. Write the chosen clips into `edit-plan.json`; inspect the current source to set portrait and wide-camera crops. Choose camera crops from the current recording.

Read [the production contract](references/production-contract.md) for fields, commands and handoffs. Run from the production workspace:

```bash
python scripts/prepare_clips.py
python scripts/tighten_clips.py
python scripts/plan_visual_revision.py --plan visual-plan.json
python scripts/prepare_split_media.py
python scripts/prepare_covers.py
python scripts/configure_sound.py
cd remotion
node render.mjs --stills-only
node render.mjs
```

Use one frame-aligned retained-segment timeline for video, audio, captions and visual beats. Inspect preview crops, captions, image focal points, covers and endings before full exports. The split camera is muted; continuous audio comes from the tightened source. Load local fonts with Remotion's rendering delay. Keep runtime symlinks immutable and copy media into `public/`.

Read [timing and crop guidance](references/full-camera-style.md) and [sustained visual guidance](references/sustained-visuals.md) when adjusting those parts. Do not mix the swipe again into an export already rendered with it.

## Verify and hand off

Check encoded MP4s, not just the editor. Run `scripts/verify_exports.py`, inspect playback at phone size, and compare the first encoded frame to its cover PNG. Check pause removal, completed speech, active word highlighting, full/split holds, caption safety, voice level and opening sound. Automated checks do not replace listening or factual review; record which actually ran.

Use `scripts/create_review.py` for an offline review page and `scripts/package_revision.py` for the current clip count. Preserve editable metadata, raw transcripts, source ranges, provenance, MP4s, SRTs and covers. Exclude standalone licensed sound, source recordings, runtime packages and model weights from delivery bundles.

Hand off clip id, complete idea, source range, speaker/interviewer context, final files and caveats to `social-post`. It owns naturally framed platform captions; do not duplicate its voice rules here. For clips-and-copy requests, continue through the requested outputs without stopping at the render phase. Public posting requires existing authorization for that action.
