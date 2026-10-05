---
name: content-publish
description: Validate, post, and verify finished content. Use when exporting video, backing up production assets, checking codecs or captions, uploading to social or video platforms, scheduling posts, configuring metadata and accessibility, testing published URLs, launching a piece, or recording publication and learning signals.
---

# Publish Content

Publishing is complete when the intended audience can reliably find, open, understand, and consume the piece—not when an export or upload finishes.

Choose the requested mode before acting:

- **Validate:** inspect a package, file, preview, or existing URL and stop with findings.
- **Prepare:** finish exports, metadata, accessibility, and scheduling fields, then stop at the approval gate.
- **Publish:** prepare, obtain explicit creator approval for the exact package and destination, post or schedule it, then verify the audience experience.

Perform reversible export and verification work directly when tools permit it. Public posting, scheduling, visibility changes, and notifications require explicit creator approval immediately before the action unless the user already approved that exact package, account, destination, and timing in the current request. Otherwise, give one focused human action and inspect the result.

## Creator defaults

For this creator's titles and social captions, read [the saved creator style](../content-voice/references/creator-style.md) alongside the local profile. Preserve the approved natural source context, lowercase copy and relevant instagram hashtags. Use the approved copy instead of reintroducing a mechanical attribution footer in the composer. Video subtitles follow the video preset, not the social-copy casing rule.

## Default clip destinations

For Anthony, prepare each finished clip for Instagram, LinkedIn, X, YouTube Shorts, Threads and TikTok, plus every other available account in the selected Buffer organization. Discover channels live for each new batch. Include every channel ID, including multiple accounts on the same platform; a platform list is a minimum, not an account allowlist. An explicit destination subset in the current request overrides this default.

Keep one delivery row per clip and channel ID, with native copy, required metadata, media, status and any blocker. Check video support and current destination requirements before scheduling. Report disconnected, locked, paused or unsupported channels and missing platforms instead of silently dropping them or reconnecting accounts. Newly connected channels join the next batch automatically. Rendering or copy-only requests prepare the packages; publishing requests carry forward the user's authorization and continue through Buffer scheduling and verification.

## 1. Protect The Production

Confirm independent copies of canonical sources, project files, research, script, assets, captions, masters, platform packages, and style profile as appropriate. Preserve enough project and source state to revise time-sensitive claims later.

## 2. Validate The Deliverable

Start from the destination's current requirements rather than a memorized preset.

For video:

- export a local master
- inspect duration, dimensions, aspect ratio, frame rate, codec, range/color tags, audio, sync, captions, opening, closing, and text-heavy motion
- play the encoded file outside the editor

For written/social packages:

- verify final copy against source claims and personal confirmations
- inspect truncation, line breaks, tags, links, media order, cover crop, alt text, and current platform preview

Reuse a validated master when compatible. Re-encode only when destination requirements or the timeline changed.

In **Validate** mode, stop here and report pass/fail evidence plus required repairs. Do not continue into publication.

## 3. Configure Publication

Set title, description/caption, thumbnail or cover, captions, transcript, alt text, links, collaborators/tags, visibility, scheduling, regional/age/access settings, and canonical destination. Use the approved platform package rather than rewriting inside the composer without carrying the change back.

Record the final package, every target account and channel ID, visibility, and publication time or Buffer queue mode. In **Prepare** mode, stop here. In **Publish** mode, continue when the user has authorized the work; request approval only for a missing decision that changes that scope. For Buffer, use `buffer-scheduling` and verify each clip/channel row independently. Scheduling completion needs verified remote IDs and queue slots; live playback remains pending until publication.

## 4. Publish And Verify

After posting, test the actual audience experience:

- open the canonical URL while signed out or from an audience-equivalent account when possible
- check mobile and desktop or the relevant native app
- verify playback, audio, captions, crops, links, permissions, tags, and accessibility
- compare the published transcode or formatting with the approved preview

Fix publication defects at the source when possible, then update the canonical package and ledger.

## 5. Record The Launch

Record publication time, canonical URL, derivative/source ID, platform, owner, and the signal that will answer whether the content did its job—such as qualified replies, completion, clicks, saves, leads, or course starts.

Separate observations from conclusions during review. Feed confirmed voice corrections to `content-voice`, planning lessons to `content-plan`, and format lessons to the relevant production skill.

The completion gate depends on mode:

- **Validate:** documented technical/editorial pass or fail evidence and required repairs.
- **Prepare:** protected sources plus a complete, validated package awaiting creator approval.
- **Publish:** protected sources, validated package, recorded creator approval, verified live or scheduled publication, working accessibility, canonical URL, and review signal.

```markdown
## Publication Report
- Source/derivative ID:
- Final package or master:
- Backup locations:
- Platform and canonical URL:
- Mode: validate / prepare / publish
- Creator approval evidence: not required / pending / <evidence>
- Publication time and owner:
- Visibility, tags, and access settings:
- Caption/transcript/alt-text locations:
- Mobile/desktop/app verification:
- Review signal and review date:
- Open risks: none / <list>
```
