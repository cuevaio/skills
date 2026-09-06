# Screencasting

A complete, editor-neutral workflow for making useful screencasts with high quality and minimal production drag.

## Workflow

1. [`screencast-plan`](screencast-plan/SKILL.md) defines the viewer, promise, lesson structure, and delivery material.
2. [`screencast-setup`](screencast-setup/SKILL.md) creates a repeatable setup and proves it with a test recording.
3. [`screencast-record`](screencast-record/SKILL.md) captures verified takes in short, editable chunks.
4. [`screencast-edit`](screencast-edit/SKILL.md) rough-cuts early batches, returns feedback, and produces the final timeline.
5. [`screencast-publish`](screencast-publish/SKILL.md) protects, exports, checks, hosts, and launches the finished video.

Run [`screencast`](screencast/SKILL.md) when you want one orchestrator to route the whole production. Install all six skills when using the orchestrator. Each phase skill can also be installed and used independently.

For a series, alternate recording and feedback editing in small batches. Move to final editing only after the latest feedback cut finds no unresolved production-wide issue and every planned lesson has a verified take.

## Installation

Install the collection and choose the screencasting skills when prompted:

```bash
npx skills@latest add cuevaio/skills
```

Or install a single phase directly:

```bash
npx skills@latest add cuevaio/skills --skill screencast-plan
```

## Skills

| Skill | Invocation | Output |
| --- | --- | --- |
| `screencast` | User | The correct route and durable phase handoffs |
| `screencast-plan` | Model or user | A recordable production brief |
| `screencast-setup` | Model or user | A tested setup and reusable preflight checklist |
| `screencast-record` | Model or user | Verified takes, a take log, and edit notes |
| `screencast-edit` | Model or user | Batch feedback or an approved final timeline |
| `screencast-publish` | Model or user | A validated publication and optional promotion plan |
