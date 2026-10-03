# Download and transcribe a source

Use an existing compatible environment before installing packages. It needs `yt-dlp[default]`, `faster-whisper`, `imageio-ffmpeg`, `requests` and compatible PyAV. Recorded versions are in [requirements.txt](requirements.txt). Node supplies yt-dlp's JavaScript runtime; imageio-ffmpeg can supply FFmpeg when it is absent from PATH. Keep logs and the attempt record in the production's source directory.

## 1. Direct download

Run from the production workspace using that environment's Python and FFmpeg. Download audio first so Whisper can start while the picture downloads. These commands preserve original audio and select source video up to 1080p:

```bash
python -m yt_dlp --js-runtimes node --socket-timeout 20 --retries 2 --extractor-retries 1 --fragment-retries 2 --write-info-json -f ba -o 'source/audio.%(ext)s' 'YOUTUBE_URL'
python -m yt_dlp --js-runtimes node --socket-timeout 20 --retries 2 --extractor-retries 1 --fragment-retries 2 --ffmpeg-location 'FFMPEG_EXECUTABLE' --merge-output-format mp4 -f 'bv[height<=1080]+ba/b[height<=1080]' -o 'source/video.%(ext)s' 'YOUTUBE_URL'
```

Get `FFMPEG_EXECUTABLE` from `imageio_ffmpeg.get_ffmpeg_exe()` when necessary. Check the actual saved audio extension before calling Whisper. If the downloaded video's container differs, remux it to `source/video.mp4`; do not rename a container blindly.

Capture the error and classify it. A missing runtime, unsupported option, format choice or expired URL is a setup/request problem. HTTP 429 or `LOGIN_REQUIRED` is an access problem. A successful title, thumbnail or oEmbed response does not establish playable media. Validate the saved media by probing and decoding it before proceeding.

## 2. When direct access is blocked

Confirm playback once in a normal browser, following the browser skill's actual CLI and launch diagnostics. Inspect player status, not just the title. A browser may render the page while the player reports a bot check. If both browser and downloader show the same access block, repeating identical requests or switching arbitrary client names is not progress.

Check the [current yt-dlp extractor guidance](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#youtube) and [PO-token guide](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide). Try a different documented client/token route only when its actual prerequisites are available. Do not pretend that a token provider, authenticated browser, proxy or another network exists. Never copy credentials from an unrelated profile.

For a public mirror fallback, consult the [maintained Invidious list](https://api.invidious.io/) at execution time and test a small set of current instances. Save status codes and actual response types. Dead instances and a blocked public API do not prove that every playback route fails.

## 3. Discover playback routes instead of guessing them

Open a current mirror's watch page for the target video. Inspect its actual HTML `source` elements, manifest URLs and backend-switch links. Use `local=true` only when that instance supports it. Preserve the complete fresh URL, including query parameters and any routing/signature fields. Do not construct companion endpoints from a remembered host or video id. A hand-built endpoint returning 400 has not tested the route advertised by the player.

The companion software handles stream retrieval, but public instances can have different configuration and access requirements. Discover their routes from the current page rather than assuming a particular hostname, backend number or API shape.

Use the helper on a current public mirror watch URL:

```bash
python scripts/discover_download.py 'CURRENT_MIRROR_WATCH_URL' --output source/download-routes.json
```

It follows source elements and advertised backend links, validates DASH XML, resolves relative media URLs against the response host, and checks small audio/video byte ranges. It tests at most three advertised alternate backends by default. It records failures and returns exit code 2 if no route was verified. It does not guarantee that a mirror is available or authenticate to a protected service.

If the watch page is accessible only in the browser, save its HTML in the production workspace and pass `--html source/watch.html` with the browser's actual current URL. A browser CORS error fetching a companion manifest is distinct from an HTTP failure: test the exact advertised URL using a normal HTTP client. HTML or bot-check text returned with HTTP 200 is not a manifest. A valid MPD without working media URLs is not a downloaded source.

The report contains fresh signed URLs. Keep it private, never put it in the skill/repo, and print only route counts or status summaries. Download promptly; expired URLs require rediscovery.

## 4. Download a verified manifest

Read the verified manifest URL from `source/download-routes.json` and pass it to yt-dlp with the generic extractor. Use `subprocess.run` with an argument list instead of embedding a signed URL in a shell command. Select the current audio/video representation ids from the report or yt-dlp's format list, not ids from an old video. Save original audio separately and mux picture plus audio into `source/video.mp4` using FFmpeg.

If a continuous stream is slow but checked ranges work, use [download_ranges.py](../scripts/download_ranges.py):

```bash
python scripts/download_ranges.py source/download-manifest-0.mpd 'ACTUAL_MANIFEST_URL' 'CURRENT_REPRESENTATION_ID' source/video-track.mp4
```

This helper expects a direct representation BaseURL with `clen` in its URL. Use it only for that compatible manifest shape; other DASH layouts belong in yt-dlp's downloader. A remote-IP-bound Googlevideo URL may fail directly while the mirror's advertised proxy route works. Do not replace a verified proxy URL with an origin URL.

Probe both streams, mux and decode the result. Record video id, original URL, selected route, format ids, duration and acquisition status in provenance. Keep expired references out of reusable instructions.

## 5. Stop with specific evidence when access is unavailable

Maintain a short attempt ledger: method, changed condition, result and next action. After a direct attempt, one browser confirmation and a bounded set of advertised fallback routes, stop repeating blocked methods. Report whether the blocker needs source footage, valid authentication or an available network route. Do not claim successful acquisition until actual media is saved and decoded. A skill cannot guarantee access to a platform or a third-party mirror.

## Whisper

Use [transcribe.py](../scripts/transcribe.py) for word-timestamped JSON, TXT and SRT. An efficient full-video model plus a larger model for selected excerpts can reduce CPU turnaround. Preserve the raw full transcript, and review technical names, low-confidence words and hallucinations against the audio.

The CLI defaults to multilingual `small` and detects language. `--language en --model small.en` fits confirmed English audio. `--local-files-only` requires the chosen model to exist in cache. A larger model can repeat the same mistake; verification remains necessary.
