# Anthony's Skills

Small, composable Agent Skills for doing creative work with AI agents. They are written to work across models, editors, and operating systems.

## Installation

```bash
npx skills@latest add cuevaio/skills
```

Choose the skills and agents you want when prompted. The installer copies ordinary files into your project so you can inspect and adapt them.

## Skill Catalog

Skills are grouped by domain under `skills/<category>/<skill>/SKILL.md`.

### Screencasting

Plan, set up, record, edit, and publish clear screencasts without turning equipment or post-production into a bottleneck.

**User-invoked**

- [`screencast`](skills/screencasting/screencast/SKILL.md): route an end-to-end production through the right phase

**Model-invoked**

- [`screencast-plan`](skills/screencasting/screencast-plan/SKILL.md): turn an idea into a recordable production brief
- [`screencast-setup`](skills/screencasting/screencast-setup/SKILL.md): build and test a reliable capture setup
- [`screencast-record`](skills/screencasting/screencast-record/SKILL.md): capture usable takes in editable chunks
- [`screencast-edit`](skills/screencasting/screencast-edit/SKILL.md): rough cut, repair, polish, caption, and quality-check
- [`screencast-publish`](skills/screencasting/screencast-publish/SKILL.md): back up, export, host, package, and launch

See the [screencasting collection](skills/screencasting/README.md) for the workflow and individual installation guidance.

## Philosophy

- Keep skills focused and composable.
- Give each process a checkable completion gate.
- Prefer fast feedback over large batches of unverified work.
- Use the tools already available until a real limitation appears.
- Keep human decisions with the human and automate the legwork around them.

## License

[MIT](LICENSE)
