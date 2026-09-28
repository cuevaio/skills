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
- [`screenstudio-edit`](skills/content-production/screenstudio-edit/SKILL.md): edit or reconstruct Screen Studio projects programmatically
- [`content-repurpose`](skills/content-production/content-repurpose/SKILL.md): derive useful clips and posts from a canonical source
- [`social-post`](skills/content-production/social-post/SKILL.md): write native X, LinkedIn, and Instagram packages
- [`content-publish`](skills/content-production/content-publish/SKILL.md): validate, post, and verify finished content

See the [content-production collection](skills/content-production/README.md) for the workflow and individual installation guidance.

## Philosophy

- Keep skills focused and composable.
- Give each process a checkable completion gate.
- Prefer fast feedback over large batches of unverified work.
- Use the tools already available until a real limitation appears.
- Keep human decisions with the human and automate the legwork around them.

## License

[MIT](LICENSE)
