# Content Production

A composable workflow for turning ideas and source material into published videos and social posts without losing the creator's voice.

## Artifact Chain

```text
idea or source
→ content brief
→ research pack
→ script or delivery outline
→ verified takes
→ approved master
→ format variants
→ platform packages
→ publication report
```

The artifact chain is the interface between skills. Start from the artifact that already exists instead of replaying earlier phases.

## Workflow

1. [`content-voice`](content-voice/SKILL.md) creates or updates a private `CONTENT_STYLE.md` from approved examples and corrections.
2. [`content-plan`](content-plan/SKILL.md) defines the audience, promise, point of view, format, platform, and CTA.
3. [`content-research`](content-research/SKILL.md) gathers current facts, primary sources, examples, quotes, and visual evidence.
4. [`content-script`](content-script/SKILL.md) turns the brief and research into hooks, talking points, or a full spoken script.
5. [`video-setup`](video-setup/SKILL.md) proves the capture environment with a playback test.
6. [`video-record`](video-record/SKILL.md) captures verified takes in editable chunks.
7. [`video-edit`](video-edit/SKILL.md) builds an approved vertical or horizontal master. [`screenstudio-edit`](screenstudio-edit/SKILL.md) is the Screen Studio adapter.
8. [`content-repurpose`](content-repurpose/SKILL.md) derives independent clips and post candidates from the canonical source.
9. [`social-post`](social-post/SKILL.md) creates native X, LinkedIn, and Instagram packages.
10. [`content-publish`](content-publish/SKILL.md) validates, posts, verifies, and records the canonical URLs.

Run [`content`](content/SKILL.md) when you want one router to choose the next phase. Install all skills when using the router. Most phase skills work independently; `screenstudio-edit` is deliberately an adapter over `video-edit` and requires both.

## Installation

```bash
npx skills@latest add cuevaio/skills
```

Install one skill directly:

```bash
npx skills@latest add cuevaio/skills --skill social-post
```

Install the Screen Studio adapter with its editorial dependency:

```bash
npx skills@latest add cuevaio/skills --skill video-edit screenstudio-edit
```

## Private Creator State

The repository contains the method, not Anthony's private style profile. Store approved voice guidance in `CONTENT_STYLE.md` inside the private content workspace. Store active productions in a ledger that links each artifact in the chain.

## Skills

| Skill | Invocation | Output |
| --- | --- | --- |
| `content` | User | The correct route and phase handoffs |
| `content-voice` | Model or user | An approved `CONTENT_STYLE.md` |
| `content-plan` | Model or user | A production-ready content brief |
| `content-research` | Model or user | A cited research pack |
| `content-script` | Model or user | Hooks plus bullets, hybrid copy, or a full script |
| `video-setup` | Model or user | A tested recording setup |
| `video-record` | Model or user | Verified takes and a take log |
| `video-edit` | Model or user | An approved vertical or horizontal master |
| `screenstudio-edit` | Model or user | A validated Screen Studio edit or reconstruction |
| `content-repurpose` | Model or user | Traceable derivative candidates |
| `social-post` | Model or user | Native platform post packages |
| `content-publish` | Model or user | Verified publications and canonical URLs |
