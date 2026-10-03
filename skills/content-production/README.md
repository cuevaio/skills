# Content production

Start from the artifact you already have. An existing interview does not need a new script or recording session.

## Default for clips, reels and shorts

A plain request such as "create 5 clips from this YouTube video" activates the approved visual preset automatically. The same default applies to other hosted videos, local recordings, podcasts and screen recordings. The creator does not need to name a previous production, specify "my style" or mention Remotion. Use the bundled preset if no local profile exists; change the style only for explicit creator or project instructions.

## Routes

```text
idea → content-plan → content-research → content-script → video-setup → video-record
                                                                         ↓
                                                                  video-edit
                                                                         ↓
source recording → content-repurpose → youtube-remotion-clips → social-post
                              ↓                    ↓                 ↓
                       written derivatives   encoded clips    content-publish

.screenstudio project → screenstudio-edit, using video-edit's editorial guidance
```

`content` routes the full request and continues through the requested outputs. `content-repurpose` owns choosing complete ideas and preserving source context. `video-edit` owns editorial judgment. The Remotion and Screen Studio adapters own their respective mechanics. `social-post` owns accompanying platform copy. `content-publish` validates delivery and performs publication only when authorized.

## Install

```bash
npx skills@latest add cuevaio/skills
```

For the YouTube-to-clips-and-copy workflow, install its cooperating skills:

```bash
npx skills@latest add cuevaio/skills --skill content content-voice content-repurpose video-edit youtube-remotion-clips social-post content-publish
```

For Screen Studio:

```bash
npx skills@latest add cuevaio/skills --skill video-edit screenstudio-edit
```

For independent social copy:

```bash
npx skills@latest add cuevaio/skills --skill content-voice social-post
```

Sibling skills are discovered by name when installed. Read only the phase needed. Optional cross-skill references can be unavailable in a partial installation; report the missing capability or use the documented artifact contract instead of treating a sibling path as a bundled dependency. Install the whole collection for every router destination. Choose either the skills installer or the plugin for an agent to avoid duplicate installed copies.

## Creator defaults and production state

[content-voice](content-voice/SKILL.md) maintains the shared, explicitly approved [Anthony profile](content-voice/references/creator-style.md), including natural interview recommendations, lowercase friendly copy, relevant instagram hashtags and source-specific personal-claim boundaries. A local `CONTENT_STYLE.md` records project-specific choices and overrides shared defaults. For another creator, learn their style.

The Remotion adapter owns the [visual preset](youtube-remotion-clips/assets/remotion/style.json), reusable font, image prompt references and renderer. Private sound and runtime caches are reused locally and set up separately on another machine. Generated images, active productions, recordings, transcripts, source URLs and review results stay in a production workspace. The bundled interview examples demonstrate decisions; their ids, timestamps and speaker names are never new-production defaults.

## Catalog

| Skill | Invocation | Owns |
| --- | --- | --- |
| [content](content/SKILL.md) | User | Routing and production ledger |
| [content-voice](content-voice/SKILL.md) | Model or user | Creator profile and approved examples |
| [content-plan](content-plan/SKILL.md) | Model or user | Audience, useful promise and brief |
| [content-research](content-research/SKILL.md) | Model or user | Source-backed facts and caveats |
| [content-script](content-script/SKILL.md) | Model or user | Spoken delivery assets |
| [video-setup](video-setup/SKILL.md) | Model or user | Tested capture environment |
| [video-record](video-record/SKILL.md) | Model or user | Verified takes |
| [video-edit](video-edit/SKILL.md) | Model or user | Editorial decisions and master QC |
| [screenstudio-edit](screenstudio-edit/SKILL.md) | Model or user | Screen Studio implementation |
| [content-repurpose](content-repurpose/SKILL.md) | Model or user | Complete derivative ideas and source ranges |
| [youtube-remotion-clips](youtube-remotion-clips/SKILL.md) | Model or user | Acquisition, Whisper, Remotion rendering and clip assets |
| [social-post](social-post/SKILL.md) | Model or user | Native platform copy |
| [content-publish](content-publish/SKILL.md) | Model or user | Export/delivery checks and authorized publication |
