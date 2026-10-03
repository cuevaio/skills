# Skill organization decision

## Decision

Keep `skills/content-production/<skill>/SKILL.md` and add `youtube-remotion-clips` as a peer adapter. Keep `content` as a routing entrypoint. One skill owns each decision: voice in content-voice, selection in content-repurpose, editing discipline in video-edit, rendering mechanics in the adapter, social copy in social-post. Use skill-local references, scripts and assets for details.

This preserves existing install names and the category structure. Adding nested video or writing categories now would move paths and plugin entries without creating a useful new boundary. Splitting download and transcription into more skills would create mandatory handoffs for small implementation steps. They stay inside the adapter until there is an independent use case. Putting everything into content would load rendering details for planning or copy-only tasks and duplicate phase ownership.

## Research

The [Agent Skills specification](https://agentskills.io/specification) defines a skill directory with SKILL.md plus optional scripts, references and assets, and recommends progressively loading detail. The [skills installer](https://github.com/vercel-labs/skills) supports discovery and selected installation; skill identity must survive installer flattening. Consequently, category folders organize the repository while each skill name remains unique. Cross-skill links resolve after full installation into sibling directories; subset installations need explicit companion guidance.

## Defaults and portability

Keep Anthony's explicitly requested writing defaults in one content-voice reference with reusable writing patterns. Other creators and explicit project preferences override those defaults. Keep the clip style in the adapter's actual renderer preset. Examples are evidence, not fixed source ids, crops or personal claims.

Portable templates, fonts and image prompts travel with the skill. Image files are production outputs, not distributed skill assets. Copyrighted sound, dependency installations and Whisper model weights remain caches outside it. Bootstrap must make no network calls and work as a scaffold when optional caches are absent, while clearly reporting setup needed before final delivery. Source-specific crops, cover timestamps and visual beats are production metadata, not helper constants.

## Validation

Check skill frontmatter and unique names, plugin coverage, local references, font hashes and absence of bundled images, and Python syntax. Exercise bootstrap with an empty home and an existing cache, rerun without overwriting edited files, use arbitrary clip ids in the visual/cover helpers, and render a fresh composition to inspect its cover and highlighted captions. Installer discovery should list all thirteen skills. These checks supplement, rather than replace, review of the actual instruction boundaries.
