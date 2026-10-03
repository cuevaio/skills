# Acquisition and Whisper transcription

Use a project-local Python environment with `yt-dlp[default]`, `faster-whisper`, `imageio-ffmpeg`, and a compatible PyAV version. The observed working versions are in [lessons.md](lessons.md). Use Node as yt-dlp's JavaScript runtime. Keep video and audio downloads separate so transcription can start first.

If YouTube rejects the server with HTTP 429 or a bot check, verify once with a normal browser and try documented client or proof-of-origin options. Repeating the same blocked request is not progress. An open-source Invidious instance may provide a working companion DASH manifest. Consult the maintained instance list, check media responses rather than trusting HTTP 200, and distinguish browser CORS failures from actual server failures. Do not treat credentials or a different network as already available.

Download a working manifest with yt-dlp's generic extractor. Resolve relative `BaseURL` entries against the companion host. If a continuous stream is very slow but small ranges work, use [download_ranges.py](../scripts/download_ranges.py). It checks response size and resumes complete chunks. Signed stream references expire; do not bake them into the skill.

Use [transcribe.py](../scripts/transcribe.py) for word-timestamped Whisper JSON, TXT, and SRT. On a CPU, an efficient full-video model plus a larger model for the selected excerpts can reduce turnaround. Preserve the raw full transcript. Review names, technical terms, low-confidence words, and apparent hallucinations in the actual selected audio. A larger model can make the same mistake.


The CLI now defaults to multilingual `small` and detects language. `--language en --model small.en` is appropriate for a confirmed English recording. `--local-files-only` requires the chosen model to exist in the local cache.
