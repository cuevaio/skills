# Anthony's Skills

Small, composable Agent Skills for producing useful content with AI agents. They are written to work across models, editors, platforms, and operating systems.

## Installation

```bash
npx skills@latest add cuevaio/skills
```

Choose the skills and agents you want when prompted. The installer copies ordinary files into your project so you can inspect and adapt them.

## Skill Catalog

Skills are grouped by domain under `skills/<category>/<skill>/SKILL.md`.

### Content Production

Move an idea through research, scripting, recording, editing, repurposing, platform writing, and publication while preserving the creator's voice.

**User-invoked**

- [`content`](skills/content-production/content/SKILL.md): route an end-to-end production through the right phase

**Model-invoked**

- [`content-voice`](skills/content-production/content-voice/SKILL.md): learn and maintain a creator-approved writing and speaking profile
- [`content-plan`](skills/content-production/content-plan/SKILL.md): choose the audience, angle, promise, format, channel, and CTA
- [`content-research`](skills/content-production/content-research/SKILL.md): build a source-backed fact and evidence pack
- [`content-script`](skills/content-production/content-script/SKILL.md): write hooks, outlines, talking points, and spoken scripts
- [`video-setup`](skills/content-production/video-setup/SKILL.md): build and test a reliable capture setup
- [`video-record`](skills/content-production/video-record/SKILL.md): record usable takes in efficient chunks
- [`video-edit`](skills/content-production/video-edit/SKILL.md): rough-cut and polish vertical or horizontal videos
- [`youtube-remotion-clips`](skills/content-production/youtube-remotion-clips/SKILL.md): download, transcribe and render complete subtitled clips with reusable Remotion assets
- [`screenstudio-edit`](skills/content-production/screenstudio-edit/SKILL.md): edit or reconstruct Screen Studio projects programmatically
- [`content-repurpose`](skills/content-production/content-repurpose/SKILL.md): derive useful clips and posts from a canonical source
- [`social-post`](skills/content-production/social-post/SKILL.md): write native X, LinkedIn, and Instagram packages
- [`content-publish`](skills/content-production/content-publish/SKILL.md): validate, post, and verify finished content
- [`buffer-scheduling`](skills/content-production/buffer-scheduling/SKILL.md): queue clips through Buffer with verified attribution, duplicate prevention, and fewer API requests

See the [content-production collection](skills/content-production/README.md) for the workflow and individual installation guidance.

## Default clip style

Ask "create 5 clips from [video URL]". The installed clip skill automatically uses Anthony's approved style for any source: full camera, tight cuts, Space Grotesk captions with word highlighting, sustained full/split images, a one-frame split cover and an opening swipe. No previous-production reference, style name or Remotion mention is needed. Explicit style changes override the preset; images are generated fresh from prompt references.

## Organization and maintenance

Keep domain categories under `skills/`, with one independently discoverable `SKILL.md` per capability. `content` is a small router; phase skills own editorial decisions; tool adapters own implementation. Detailed procedures, scripts, fonts and image prompt references live inside the skill that uses them. Generate images in each production workspace; no images are bundled. The YouTube/Remotion adapter is a sibling of the Screen Studio adapter, so you can install either without loading both workflows.

Anthony's explicitly approved [creator defaults](skills/content-production/content-voice/references/creator-style.md) and reusable writing patterns are included. Another creator's local `CONTENT_STYLE.md` overrides them. Production footage, model weights, runtimes and the licensed opening sound stay outside the repository.

Run repository checks with a Python environment containing PyYAML:

```bash
python scripts/validate_skills.py
```

See [the content collection](skills/content-production/README.md) for installation combinations and [the organization decision](docs/skill-organization.md) for the rationale and sources.

## Philosophy

- Keep skills focused and composable.
- Give each process a checkable completion gate.
- Prefer fast feedback over large batches of unverified work.
- Use the tools already available until a real limitation appears.
- Keep human decisions with the human and automate the legwork around them.

## License

[MIT](LICENSE)
