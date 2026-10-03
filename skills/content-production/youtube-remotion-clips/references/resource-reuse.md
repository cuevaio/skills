# Resource reuse and another machine

The approved preset is `assets/remotion/style.json`. The skill ships the Remotion template and lockfile, Space Grotesk with its SIL OFL license, and [image prompt references](image-prompts.md). It contains no image files. Adapt the prompts to the current explanation and generate images in the production workspace; save the actual prompts, image provenance and inspected focal points there. Do not reuse camera portraits from a previous recording. The repository's MIT license covers authored instructions and helpers; the bundled font keeps its own license. No standalone Mixkit sound is distributed here.

## Offline bootstrap

`bootstrap_project.py --workspace /path/to/production` copies actual files into Remotion public, checks cached font/sound hashes, and preserves editable project files. It makes no network calls. `--cache-root /path/to/cache` selects a different private cache without changing the catalog. It copies `image-prompts.md` into the workspace for adaptation; it does not generate, download or copy images. It records reused and missing resources in `review/resource-reuse.json`.

A matching cached Remotion runtime at `~/.cache/clip-production/runtime/remotion-4.0.532/` can provide immutable node_modules. It is linked only when package-lock hashes match. `--no-runtime-link` opts out. If dependencies must change, remove only the workspace symlink and install locally; never mutate the shared cache. If the runtime is missing, run `npm ci` in the workspace's remotion directory using its saved lockfile.

Use an existing compatible Python environment, or create a production-local one from `requirements.txt`. The helper records the Python executable actually used. Whisper can reuse `~/.cache/huggingface/hub`; do not package models or force English because an English model is cached.

## Private opening swipe

The optional sound cache is `~/.cache/clip-production/sfx/mixkit-2627/`, containing:

- `mixkit-fast-swipe-zoom-2627.wav`, the original
- `opening-swipe.wav`, the trimmed version
- `mixkit-license.html`, a license snapshot

The manifest supplies source and license URLs and the trimmed hash. On a new machine, obtain the original asset once from its recorded source, review its current license, save the snapshot, and prepare the trimmed WAV with FFmpeg:

```bash
ffmpeg -i mixkit-fast-swipe-zoom-2627.wav -af 'atrim=start=0.04:end=0.673333333,asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st=0.593333333:d=0.04' -ar 48000 -c:a pcm_s16le opening-swipe.wav
```

Encoder changes can produce a different file hash. Verify a recovered sound before deliberately updating the local catalog hash. Do not bypass integrity checks or automatically redownload every production. Mixkit's recorded license allows incorporation in finished videos but excludes distributing the standalone sound in stock packs, tools or templates. Keep it private and out of this repository and shared ZIPs.

`--sound auto` reuses a complete cache or records pending setup. `--sound required` fails for a missing cache. `--sound skip` omits the copy. A fresh scaffold can work without sound, but the final usual-style clip needs the swipe unless the current task explicitly omits it.

Media files must be copied into public: the observed Remotion bundler skipped symlinked media. Runtime node_modules may be linked. The original preset was checked in a fresh offline workspace and produced a pixel-identical approved kitchen cover; that is historical evidence, not a guarantee that a new machine or edited source has passed verification.
