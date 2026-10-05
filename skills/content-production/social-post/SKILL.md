---
name: social-post
description: Write platform-native social posts from approved source material in the creator's voice. Use for X posts or threads, LinkedIn posts, Instagram captions or Reel packages, YouTube Shorts titles and descriptions, Threads posts, TikTok captions, cross-platform launch copy, hooks, CTAs, alt text, cover text, pinned comments, or adapting one source without pasting identical copy everywhere.
---

# Write Social Posts

Produce native platform packages from one factual source of truth. Read `CONTENT_STYLE.md`; when it is missing and “my style” matters, use `content-voice` before finalizing.

Check the selected platform's calibration status in the profile. An uncalibrated adaptation can produce a draft, but it cannot be labelled voice-approved until the creator reviews it.

## Creator defaults

For this creator, read [the saved creator style](../content-voice/references/creator-style.md) alongside any local `CONTENT_STYLE.md`. Use the approved lowercase, casual voice and native platform adaptations. For interview recommendations, integrate source context into the specific takeaway rather than attaching a fixed attribution footer. The profile distinguishes supported first-person learning from the speaker's experiences.

## Default clip destinations

For Anthony, prepare each finished clip for Instagram, LinkedIn, X, YouTube Shorts, Threads and TikTok, plus every other available account in the selected Buffer organization. Discover channels live for each new batch. Include every channel ID, including multiple accounts on the same platform; a platform list is a minimum, not an account allowlist. An explicit destination subset in the current request overrides this default.

Keep one delivery row per clip and channel ID, with native copy, required metadata, media, status and any blocker. Check video support and current destination requirements before scheduling. Report disconnected, locked, paused or unsupported channels and missing platforms instead of silently dropping them or reconnecting accounts. Newly connected channels join the next batch automatically. Rendering or copy-only requests prepare the packages; publishing requests carry forward the user's authorization and continue through Buffer scheduling and verification.

## 1. Establish The Post Job

Identify:

- source artifact and verified claims
- audience on this platform
- one job: teach, share a point of view, start conversation, announce, or convert
- one central idea
- desired action
- attached media and what it already communicates

Never invent a personal story, result, opinion, endorsement, or sense of urgency. Ask for confirmation or use a placeholder.

## 2. Choose The Platform Adapter

Read only the selected reference:

- [X](references/x.md)
- [LinkedIn](references/linkedin.md)
- [Instagram](references/instagram.md)
- [YouTube Shorts](references/youtube.md)
- [Threads](references/threads.md)
- [TikTok](references/tiktok.md)

For another connected Buffer service, adapt from the original source using that destination's current requirements and preview. Keep all target channel IDs in the handoff even when accounts share a platform. Keep new platform adaptations provisional where the voice profile lacks calibration; do not block an already authorized publishing task solely because the platform is new.

For a cross-platform request, create each package from the source artifact, not by editing one platform's post into the next.

## 3. Draft Around Meaning

Write three hooks that use meaningfully different angles, such as tension, observation, result, or useful disagreement. Select one based on the job and voice profile.

Build the body with the minimum context needed to understand the idea. Put evidence near claims. Let media carry details it already shows. End with a CTA proportionate to the relationship: a specific question, useful link, invitation to try, or no CTA when the idea is complete.

Avoid engagement bait, empty suspense, generic inspiration, fake vulnerability, and unverified algorithm folklore.

## 4. Package The Post

For a copy-only request, return the requested posts grouped by clip and platform. Keep alternate hooks and checks in the saved work; do not burden the answer with publishing metadata. When a complete publishing package is requested, return:

```markdown
## <Platform> Package
- Job and audience:
- Source artifact and claim IDs:
- Selected post:
- Alternate hooks:
- Media/cover text:
- Alt text:
- Link placement:
- CTA:
- Pinned comment or first reply: not needed / <copy>
- Personal claims awaiting confirmation: none / <list>
- Platform preview checks:
- Creator approval: pending / <evidence>
```

## 5. Review In Context

Check voice, factual traceability, first-screen readability, truncation, line breaks, link behavior, attached media, alt text, and the current platform preview. Compare cross-platform versions for native adaptation rather than cosmetic differences.

The draft gate passes when the post is recognizable as the creator, useful without hidden context, native to the selected platform, factually supported, and packaged with every asset needed to publish. A package is **approved** only after the creator accepts its exact copy, media, destination, and CTA; otherwise label it `ready for creator review`.
