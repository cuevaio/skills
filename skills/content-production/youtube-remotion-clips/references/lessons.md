# Initial-run acquisition and transcription lessons

Source: YouTube `MN9dGgmLyso`, Matt Pocock interviewing Lauren Tan. Original production completed on 2026-10-03.

## Observed failures and repairs

- Direct yt-dlp requests received HTTP 429 or `LOGIN_REQUIRED` from multiple clients, on both IPv4 and IPv6. A browser confirmed the same bot-check result. A proof-of-origin provider did not fix this server's requests.
- YouTube oEmbed returned a valid title even while playback was blocked. Metadata success did not establish media access.
- An Invidious API returned full metadata and signed Googlevideo URLs. Direct download of those remote-IP-bound URLs failed. The instance's companion service and relative media URLs were required.
- A browser fetch of a companion manifest failed with CORS while a Python requests fetch of the same URL returned a valid DASH manifest. Several other companion backends returned HTTP 500. Inspect response bodies and content types.
- HTTP 200 from a mirror sometimes contained a bot-check HTML page. Media headers and a successful byte-range read established actual access.
- A continuous audio download ran at about 32 KiB/s. Checked 1 MiB ranges with four workers downloaded the 64,819,204-byte audio much faster. The 866,279,097-byte video used the same resumable method. Byte counts matched the manifest's `clen` values.
- `faster-whisper==1.2.1` with `av==19.0.1` failed because `av.open()` no longer accepted `metadata_errors`. Pinning `av==16.1.0` restored decoding. Recheck compatibility on later upgrades.
- Whisper `small.en` transcribed the entire 4,005-second recording with word timestamps. `medium.en` refined each selected excerpt. Both models invented an `Arctic` fragment before `Cursor`; the clip caption omitted that artifact rather than manufacturing a replacement phrase. Another zero-confidence `Sure.` artifact was removed. Raw transcripts remain available.
- Initial draft end times would have cut off several final sentences. Checking word-end times extended the excerpts to preserve the completed thought.
- Wide image panels cropped the chef's hat and part of a robot's head. Moving image focus above center improved the crop. Inspect each actual generated image at its target aspect ratio.
- Generated-image tool results contain large base64 fields. Store the result and print only the saved path or small metadata. Never print the whole result to inspect a path.

## Reusable editorial decisions

Each clip explains a different part of the interview: clear intent, human responsibility in an AI kitchen, verification, context and coordination, and overnight merging with morning review. The final excerpt retains the warning that earning this trust takes time.

Captions use clip-local word timing and compact groups rather than full transcript sentences. Color marks the currently spoken word. That initial layout was superseded by the creator-approved full-camera style, sustained full-image/split-image holds, first-frame covers and opening swipe. Follow SKILL.md and style.json for current defaults. Original AI-generated illustrations show the topic while remaining visibly conceptual.

Source slices are normalized to approximately -16 LUFS before Remotion renders. Local fonts avoid network-dependent typography. Frame counts derive from the same duration used by media extraction and caption preparation.

The skill includes the implementation and verification helpers. All five final exports decoded successfully, had their expected frame counts, and had no sustained black frames. Integrated loudness ranged from -17.15 to -16.48 LUFS, with true peaks below zero dBTP. Original measurements and hashes remain in the private production workspace. All five videos loaded in Chromium with 1080×1920 metadata, and playback advanced without a media error. Encoded contact sheets showed the openings, both speaker layouts, widest captions, and completed endings. These checks do not establish a complete listening pass or creator approval.

Final export verification also remains in the project under `review/verification.json`. The pinned Python dependencies are in [requirements.txt](requirements.txt). Consult the current run's measurements rather than treating this example as proof of a later run.
