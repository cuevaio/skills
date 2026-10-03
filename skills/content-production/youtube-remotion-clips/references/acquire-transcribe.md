# Download and transcribe a source

## Use the acquisition CLI

Use an existing compatible Python environment before installing packages. Dependencies are `yt-dlp[default]`, `requests`, `imageio-ffmpeg` and PyAV; Whisper additionally needs `faster-whisper`. Recorded versions are in [requirements.txt](requirements.txt). Node supplies yt-dlp's JavaScript runtime. The CLI finds FFmpeg on PATH or uses imageio-ffmpeg's bundled executable.

Run the bundled [download_source.py](../scripts/download_source.py) from the installed skill directory. Prefer this shared entry point so an old production workspace cannot keep stale acquisition helpers. If the skill is installed elsewhere, use its actual catalog path:

```bash
python ~/.agents/skills/youtube-remotion-clips/scripts/download_source.py 'VIDEO_URL_OR_LOCAL_FILE' --workspace .
```

This is the default acquisition path. Do not write another downloader, range fetcher, manifest parser or muxing script. The command handles source identity, direct yt-dlp attempts, bounded public-mirror discovery, advertised backend links, fresh signed manifests, session cookies, checked range downloads, audio extraction, muxing, media probing and full decode verification. It selects video up to 1080p. Mirror acquisition currently supports DASH representations with direct BaseURL media and checked byte-range access; unsupported layouts are reported rather than guessed.

Successful output is `source/video.mp4`, `source/audio.mka`, `source/acquisition.json` and an acquisition entry in `provenance.json`. The audio container preserves the original codec; do not assume an `.m4a` extension. Exit codes: `0` verified media, `2` acquisition blocked after the bounded attempts, `1` setup/input error. Read the JSON status and report before moving to transcription or rendering. Page titles, thumbnails, HTTP 200 HTML and an MPD without working media do not count as acquired footage.

Rerunning the same command verifies hashes and reuses completed files and checked partial ranges. A workspace belongs to one source; choose a new workspace for a different recording. A file lock prevents simultaneous acquisition in the same workspace. Keep all acquisition logs, signed URLs and partial downloads private in the production directory, never in this skill or repository.

To start transcription before acquiring the picture:

```bash
python ~/.agents/skills/youtube-remotion-clips/scripts/download_source.py 'VIDEO_URL' --workspace . --audio-only
python scripts/transcribe.py source/audio.mka --output transcript
python ~/.agents/skills/youtube-remotion-clips/scripts/download_source.py 'VIDEO_URL' --workspace .
```

Wait for the audio-only command to finish before starting the other commands. Transcription and picture acquisition can then run independently.

## Supply a concrete route when needed

By default the CLI discovers a bounded set of monitored public HTTPS instances from the current [Invidious registry](https://api.invidious.io/instances.json). `--max-mirrors` and `--max-backends` default to three each. `--max-mirrors 0` disables mirror fallback. Unmonitored network-specific aliases and unavailable instances are excluded even when their URI uses HTTPS. Recent playback successes are tried before unknown playback and known failures. Selection is saved in `source/instance-selection.json`. A live registry and the instances can be unavailable; read their actual attempt results.

An explicitly supplied current mirror origin or watch URL replaces registry discovery:

```bash
python ~/.agents/skills/youtube-remotion-clips/scripts/download_source.py 'VIDEO_URL' --workspace . --mirror 'CURRENT_MIRROR_OR_WATCH_URL'
```

If a mirror watch page works only in the browser, save its HTML and use its actual current URL:

```bash
python ~/.agents/skills/youtube-remotion-clips/scripts/download_source.py 'VIDEO_URL' --workspace . --mirror 'CURRENT_WATCH_URL' --watch-html source/watch.html
```

The CLI reads the page's source elements and advertised backend links, preserving complete query parameters. It never constructs companion endpoints from remembered hosts or video ids. Browser CORS failure and an HTTP playback failure are different: this HTTP client tests the exact advertised routes. Authentication required beyond anonymous page cookies must be explicitly provided; the CLI does not search browser profiles. An explicitly supplied Netscape cookie file can be passed as `--cookies /path/to/cookies.txt` for yt-dlp.

For setup errors, inspect the private log and the installed environment. Exit 2 starts diagnosis, rather than automatically asking for an upload. Read `source/acquisition.json`, including each mirror's HTTP status and failure reason. If it reports a browser challenge, confirm playback once in a normal browser for that exact public host, following the browser skill. A bot-check page returned with HTTP 200 is still blocked acquisition. If the browser also reports access denied, do not claim another local code change will grant access. Report the exact blocker and which concrete prerequisite is missing.

For access blocks, check the [current yt-dlp extractor guidance](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#youtube) and [PO-token guide](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide) only if a documented prerequisite is actually available. A browser confirmation can distinguish playback failure from downloader setup. Follow the browser skill for its launch arguments. Do not cycle through guessed clients, endpoints or nonexistent tokens after the report shows the same access block. Report the specific missing source, authentication or working network route.

The lower-level [discovery helper](../scripts/discover_download.py) and [range helper](../scripts/download_ranges.py) remain available for diagnosing a concrete route. The range helper derives the actual size from Content-Range, checks each response and resumes atomic 1 MiB chunks; it does not require a `clen` query parameter. The acquisition CLI already orchestrates these helpers; normal production should not invoke them separately.

## Whisper

Use [transcribe.py](../scripts/transcribe.py) for word-timestamped JSON, TXT and SRT. Its defaults are multilingual `small`, CPU int8 and language detection. `--language en --model small.en` fits confirmed English audio. `--local-files-only` requires the model in cache.

Preserve the raw full transcript. An efficient full-video model plus a larger model for selected excerpts can reduce CPU turnaround. Review technical names, low-confidence words and hallucinations against the audio; a larger model can repeat the same mistake.
