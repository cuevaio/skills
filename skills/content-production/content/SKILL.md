---
name: content
description: Route content from idea through publication.
disable-model-invocation: true
---

# Content Production

Move the production through artifact gates. Load and follow the matching phase skill rather than improvising a second workflow.

## Route

| Current state or request | Load | Gate reached |
| --- | --- | --- |
| “Write in my style,” style examples, or voice corrections | `content-voice` | A creator-approved style profile exists |
| An idea, goal, source, or loose topic | `content-plan` | A production-ready content brief exists |
| A brief with claims or examples that need evidence | `content-research` | A cited research pack exists |
| A brief or research pack that needs delivery language | `content-script` | The chosen script or outline exists |
| A script but no proven capture environment | `video-setup` | A playback test passes |
| A tested setup and material ready to perform | `video-record` | Preferred takes are verified |
| Raw footage, review notes, or a rough timeline | `video-edit` | A vertical or horizontal master is approved |
| A `.screenstudio` project or Screen Studio implementation problem | `screenstudio-edit` | The edit or reconstruction passes QC |
| A canonical source that should become clips or posts | `content-repurpose` | Derivative candidates are traceable and approved |
| A source that needs X, LinkedIn, or Instagram copy | `social-post` | Native platform packages are approved |
| A finished master or approved platform package | `content-publish` | The publication works and its URL is recorded |

If the user names a phase or already has its input artifact, start there. Use `CONTENT_STYLE.md` whenever it exists. Ask only for missing facts that cannot be discovered and that block the next gate.

## Production Ledger

For multi-asset work, maintain one row per canonical piece:

```markdown
| ID | Brief | Research | Script | Takes | Master | Variants | Platform packages | Published URLs | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

Derivatives point back to their canonical source ID. Platform copies are variants, not independent sources of truth.

## Operating Principle

Optimize for **useful and native**: one clear idea, expressed in the creator's voice, shaped for how the audience consumes it on that platform. Automate legwork while keeping point of view, personal claims, and final approval with the creator.

At every gate, report what is complete, decisions carried forward, unresolved risks, and the exact artifact ready for the next phase.
