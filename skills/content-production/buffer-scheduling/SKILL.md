---
name: buffer-scheduling
description: Schedule videos and social posts through Buffer, identify relevant people in the source material, find and verify their profiles, add supported mentions, avoid duplicates, and verify scheduled results. Use when the user asks to queue or schedule content with Buffer.
---

# Schedule posts with Buffer

Use the user's requested accounts, content and cadence. A request to schedule content authorizes the scheduling work and routine caption adaptation within that scope. Ask for missing destination or timing only when it cannot be inferred; don't introduce a second approval gate when the user already authorized the action.

## Discover the account and existing content

Read the current [CLI guide](https://developers.buffer.com/guides/cli.md). Use `BUFFER_API_KEY` from the environment. Never print its value, source the whole shell configuration into output, or pass the key as a command argument. If a key exists only in a shell startup file, load only the required assignment securely.

For a new batch, fetch account identity, timezone and queue capacity together, then list channels once using the returned organization ID. Reuse these live results throughout that batch; refresh changed account or channel settings when the user reports an upgrade, new connection or schedule change. In CLI 1.2.2, the organization flag is required despite some examples omitting it:

```bash
buffer account --fields 'organizations.{id,name,limits.scheduledPosts},timezone'
buffer channels list --organization-id <org-id> --fields id,name,displayName,service,timezone,isDisconnected,isLocked,isQueuePaused,postingSchedule
```

Use the selected or unambiguous organization and name it before writes. Map X to service `twitter`. Inspect Instagram, LinkedIn and X separately. A video already posted to Instagram may still need LinkedIn, while X may already contain it. Do not deduplicate across platforms.

Read published history and the complete relevant queue for the target channels using one `posts list` query with `filter.channelIds`. Include all statuses for that scope when reconciling duplicates, rather than issuing one query per status. Avoid unrelated channels' history. `posts list` returns `{items,pageInfo}`. Follow `pageInfo.hasNextPage` and use the opaque `endCursor`. To fetch queue records, use JSON input with `filter.status` set to `scheduled`, `draft`, `needs_approval`, and `sending`. Inspect errors separately; they are not successful publications. Match source media and captions against the clip inventory, accounting for handles or punctuation in published copy.

## Resolve media before scheduling

The [Buffer API has no file-upload endpoint](https://developers.buffer.com/guides/hosting-media.md). Each video needs a direct public HTTPS URL that remains reachable through publication. Drive preview/share links, expiring social CDN links, signed URLs that expire early, temporary tunnels, and short-lived file hosts do not satisfy that requirement.

Use an existing authorized public media host. If none is available, ask for its name and the credential location without asking the user to paste secrets. Continue preparing the inventory, captions, calendar and validated payloads while that dependency is pending. A Buffer browser login can provide a native upload route when available; API authentication does not imply browser authentication.

Already published X video assets can expose stable `video.twimg.com` MP4 URLs without expiring query parameters. Inspect and verify these when crossposting those same clips. Prefer the local master on the user's own host for new videos. Record when a published transcode replaces a master.

Check public URL headers and retrieval without authentication. Confirm video MIME type and inspect duration, dimensions, H.264/AAC compatibility, audio and the intended cover. Reuse existing export verification when it matches the current master; don't re-render compatible files.

## Cloudflare R2 with saved Wrangler login

When Cloudflare is the chosen host, use the existing Wrangler login as the current user. `wrangler r2 bucket list` verifies access without exposing credentials. Prefer a dedicated public media bucket so private application buckets remain private.

For this creator, `cueva-social-videos` is the dedicated bucket. Its public base URL is `https://pub-b4ec68a0f4354377b0c004985853d68a.r2.dev`. Reuse it for authorized social media uploads. It contains public exports only. Use group, clip ID and a content-hash suffix in object names so revised exports cannot overwrite queued media.

```bash
wrangler r2 bucket dev-url get cueva-social-videos
wrangler r2 object put cueva-social-videos/clips/group/clip-hash.mp4 --file /absolute/clip.mp4 --remote --content-type video/mp4 --cache-control 'public, max-age=31536000, immutable'
```

For a new dedicated bucket, use `wrangler r2 bucket create <name>` and enable its public URL with `wrangler r2 bucket dev-url enable <name> --force` when public hosting is already authorized. Read back the URL. Always include `--remote`; local uploads cannot serve Buffer. Verify public MIME type, byte size and downloaded SHA-256 before recording the URL. Keep objects reachable through publication. The `r2.dev` endpoint is rate limited and intended for development traffic; use an R2 custom domain or production delivery route for sustained higher-volume hosting.

When changing already scheduled posts to Buffer-selected times, edit their existing IDs with `mode: "addToQueue"`, omit `dueAt`, and verify the resulting slots. Do not delete and recreate them. Replacing their video assets with hosted local masters can also avoid relying on social platform transcodes.

## Prepare the calendar and payloads

Keep a local plan with clip identity, absolute file path, SHA-256, channel, caption, timezone and due time. Identify relevant people and resolve platform mentions as described below before finalizing captions. Reuse approved captions and the creator's saved voice. Do not invent first-person experiences. When cadence is unspecified, choose a reasonable cadence and disclose it before scheduling. Convert times with the user's timezone, not the host's timezone.

Discover the current input fields with `buffer schema describe posts create`. Read `buffer context pitfalls` and `buffer context idempotency` before bulk mutations. Use `--input <file>` or stdin for nested assets and metadata. `--json` overrides other input flags.

For automatic publication at an explicit time:

```json
{
  "channelId": "<verified-channel-id>",
  "text": "<platform-caption>",
  "schedulingType": "automatic",
  "mode": "customScheduled",
  "dueAt": "2026-10-04T18:00:00-05:00",
  "assets": [{"video": {"url": "https://media.example.com/clip.mp4"}}]
}
```

Instagram reels require `metadata.instagram.type: "reel"` and `metadata.instagram.shouldShareToFeed: true`. Select the first-frame cover using `assets[0].video.metadata.thumbnailOffset: 0`. Do not set a custom video thumbnail URL; the API rejects it.

`addToQueue` lets Buffer assign the next available slots from the existing channel schedule, including multiple posts per day. When the user asks Buffer to choose times, omit `dueAt` and use this mode. This uses the configured schedule; it does not itself calculate new optimal times or change posting frequency. Use `customScheduled` only when the user wants a deliberate calendar. `schedulingType: notification` requires manual mobile publication.

Validate every payload with `--dry-run` before bulk creation. A dry run does not verify media reachability or reserve a slot. Check posting limits with `dailyPostingLimits list`; CLI 1.2.2 requires a full ISO DateTime for `--date`, even though its help shows a date-only example.

## Mention people on each platform

Finding relevant people and tagging them is part of every Buffer video scheduling task for this creator; do not wait for a separate request or a list of names. Review the clip, transcript, source title, description, credits, and existing production notes to identify speakers, interviewers, guests, and people explicitly discussed. Resolve aliases and role descriptions such as "poteto" or "the opencode founder" using source evidence. Record each person's relevance to the individual clip, so a guest from another segment is not tagged across an entire batch.

Verify who is speaking separately from identifying a company's founders or people named in the transcript. A founder's profile alone does not establish that they are the interviewee. For the OpenCode YC Lightcone batch, the interviewee is Jay V, founder and CEO, whose X handle is `@jayair` and LinkedIn profile is `https://www.linkedin.com/in/jayair/`. Dax Raad, `@thdxr`, is discussed in the coffee storefront clip; he is not the interviewee. Use Jay for speaker attribution and Dax only when the caption specifically discusses his work. This identity correction was supplied by the creator and corroborated by Jay's LinkedIn activity sharing the YC interview.

Find and verify each relevant person's LinkedIn, X, and Instagram profiles independently using the person's own site, the actual profile, or reliable corroborating evidence. Save their name, aliases, profile URLs, verification sources, and unresolved platforms in a reusable profile map. Reuse verified results within the batch and recheck them for later batches. Do not infer an Instagram handle from an X handle. Omit accounts that cannot be verified, as the creator requested, and continue scheduling the rest.

When a caption names or attributes an idea to an identified person, use their verified platform mention wherever supported. Include natural speaker or interviewer attribution when it helps explain or credit the clip, even if the initial caption only uses a role description. Keep the attribution faithful to the source and the creator's voice. Do not add unrelated people merely to increase reach. Check the final caption's length after inserting handles and record which mentions were applied or omitted on each platform.

Read Buffer's current [mention guide](https://support.buffer.com/en-us/articles/adding-mentions-tags-in-posts-ulm0tGb2Ej). X and Instagram accept exact `@handle` text in captions; Buffer does not autocomplete these handles, and they become links after publication. Instagram allows up to 20 caption mentions. Image tags are a separate feature.

LinkedIn native mentions require `metadata.linkedin.annotations`, not just an `@name` string. Inspect the current schema before writing. The October 2026 `AnnotationInputLinkedIn` required `id`, `entity`, `length`, `link`, `localizedName`, `start`, and `vanityName`. Use a resolved LinkedIn entity URN and offsets that match the displayed name in the final caption. Preserve the person's name capitalization. A profile slug or public `fs_miniProfile` URN is not a resolved member entity ID. The public Buffer API exposed no member lookup endpoint in this session. An authenticated Buffer composer can resolve eligible profiles; API credentials alone do not authenticate that browser session.

Buffer allows personal LinkedIn profiles to mention their connections, and company Pages to mention profiles that follow the Page. Other profile visibility and mention settings can also prevent tagging. When identity or eligibility cannot be resolved, retain plain names and report the limitation; do not claim a native mention was added.

For X and LinkedIn caption-only edits, use `posts edit` with only `id` and `text`, except when updating native LinkedIn annotations. Omit `mode` and `dueAt` to preserve the existing queue slot. Instagram rejected this minimal edit in October 2026 because it required media and a post type even for an existing reel. Resend the verified existing video URL and the existing Instagram metadata, including `type: "reel"` and `shouldShareToFeed`, without changing the source or cover settings. Validate the edits, reconcile current text before writing, record the previous and resulting captions, and verify every affected post's ID, status, channel, due time, and media source afterward. Update the local plan and calendar to match. The October 2026 verified profile map is `/home/cueva/content/scheduling/buffer/people-profiles.json`; recheck profiles for future batches.

## Create, reconcile and verify

There is no API idempotency key. Persist the intended payload before each `posts create` and save returned post IDs immediately. If a result is uncertain, inspect all relevant remote records before another create. Stop if the outcome remains ambiguous.

Request `post.id,post.text,post.status,post.dueAt,post.channelId,post.assets.source` in the create response, then verify the affected channels in one paginated `posts list` pass with all required fields, including `schedulingType` and any platform metadata being verified. This avoids spending one additional API call per post. Verify status, channel, text, media and due time against the plan. A successful request alone does not prove the post is scheduled. Preserve an attempt ledger, including partial success, and report exactly what was scheduled versus what remains blocked. Scheduled playback cannot be verified until publication.

The bundled [scheduler](scripts/schedule.py) accepts a JSON plan containing `organizationId` and `posts`. Each post contains `key`, `service`, `channelId`, `text`, and `clip.path`. Set `mode: "addToQueue"` to let Buffer choose the time. For a custom schedule, use `mode: "customScheduled"` and include `dueAt`. A separate JSON media map associates local absolute file paths with stable public video URLs. Run without `--execute` for local validation; omitted URLs use a validation-only placeholder and never create posts. It requires all URLs before execution, records attempts durably, reconciles matching remote posts, and stops on unresolved writes.

```bash
python scripts/schedule.py --plan /absolute/plan.json --ledger /absolute/ledger.jsonl
python scripts/schedule.py --plan /absolute/plan.json --media /absolute/media.json --ledger /absolute/ledger.jsonl --execute
```

## Minimize Buffer API requests

Optimize remote requests, not the number of local CLI commands. In installed CLI 1.2.2, `schema describe`, `context` and `posts create --dry-run` use bundled data; the dry-run returns before token lookup and the GraphQL request. Keep validating every payload locally. Public media checks and profile research do not consume the Buffer API quota. Recheck this behavior if the CLI implementation changes.

Before a bulk run, estimate requests as `new posts + discovery calls + before pages + after pages + limit checks`. One create per post is the baseline for the current scheduler. Do not assume parallel calls, narrower `--fields`, or several GraphQL operations in one HTTP request reduce quota usage. Use a supported bulk endpoint only after verifying its availability and quota accounting.

- Fetch account identity and capacity in one call, and all target channels in one call. Save results with organization ID and retrieval time. Reuse them within the active batch; a previous batch's settings are context, not proof of current access or capacity.
- Use `filter.channelIds` for every reconciliation and verification read. Request `--limit 100`, follow every returned cursor, and fetch all target channels together. Limit published-history dates only when the inventory or previous verified snapshot establishes a complete deduplication boundary. Never trim history merely to fit a request budget.
- Use one before snapshot for deduplication, queue occupancy and reconciliation. Do not repeat the same list inside multiple helpers. The bundled scheduler scopes its before read to the plan's channels. When calling `existing_posts` separately, pass the target channel IDs too.
- Prepare captions, mentions, media and platform metadata before creating posts. Avoid scheduling unfinished captions and then spending one edit per post to correct them. Combine all authorized changes to an existing post into one edit and skip entries already matching the desired result.
- Ask create/edit responses for all fields needed to validate that operation. Save IDs, returned times and payloads durably. Use one final list pass for the affected channels, including YouTube title/privacy and automatic publishing settings when relevant. Do not follow it with a separate metadata scan or a `posts get` per item.
- Check daily posting limits for all target channel IDs in one call per relevant date, only for dates where the planned volume could reach the limit. Do not query every date in a sparse, weeks-long queue. Reuse the discovery account response for scheduled-post capacity instead of fetching it again.
- On resume, stop any other writer, read the ledger, and reconcile only the batch's target channels. Create only unconfirmed entries. Use the local ledger for progress updates during execution; avoid polling Buffer after each post. Confirmed IDs remain evidence of the earlier create response, while the final snapshot establishes current remote state.
- Record request counts by remote operation and page, plus quota/reset information supplied by Buffer. Do not probe the quota endpoint repeatedly. On a daily-window rejection, persist progress and the reset deadline, then stop requests until reset with a small margin. Use a bounded continuation that disables itself on completion or unresolved outcomes. A plan upgrade and a key's API allowance are separate; verify access once when the user reports a change.

When the user replaces the key in `.bashrc`, load only that literal assignment into the worker's environment, replacing any stale inherited `BUFFER_API_KEY`. Never print, log or pass the secret as an argument. Rotating keys is not a request-saving strategy.

For 72 posts across three empty target queues, aim for roughly 77 remote requests: 72 creates, one account read, one channel read, one combined daily-limit check if needed, one before page and one after page. This is an estimate assuming each scoped read fits in 100 records. Existing history, required date checks and reconciliation can add pages. Do not sacrifice duplicate prevention or final verification to meet the estimate.

## Queue limits and plan changes

This creator prefers Buffer-selected posting times and multiple posts per day. Use `addToQueue` unless the current request specifies exact times. The connected schedules in October 2026 had two daily slots for Instagram and LinkedIn, and four for X.

Include the current organization limit in the discovery account read before planning around queue capacity. Use that saved response within the batch; fetch again only when settings change or a new batch starts:

```bash
buffer account --fields 'organizations.{id,name,limits.scheduledPosts}'
```

Do not hardcode the free-plan limit or keep an old restriction after an upgrade. On October 4, 2026, this creator's upgraded organization reported `limits.scheduledPosts: 5000`. That is enough to queue the full prepared batch directly. Treat marketing language such as "unlimited" separately from the numerical limit exposed by the API, and recheck live account data on later tasks. Daily posting limits, scheduled-post capacity and API request quotas are separate constraints.

When the user upgrades during a partially queued batch, stop any refill timer before another process writes the same ledger. Reconcile existing Buffer IDs, then schedule only the remaining entries. Verify the complete remote queue, refresh the calendar and report, and retire the refill job once the backlog reaches zero. Do not recreate already scheduled posts or change their queue order just because the account changed.

On the previous free plan, the API rejected an eleventh scheduled post on a channel. The CLI emitted the rejection on stderr with empty stdout. Capture both streams and inspect the exit code. A clear rejection establishes that no post was created; record that evidence before retrying when capacity changes. A timeout or empty stdout without that evidence remains uncertain and needs remote reconciliation.

Only use a finite queue refill when a verified current queue cap is smaller than the authorized batch. Read live capacity in the refill job rather than assuming ten slots. Keep stable media URLs and a durable ledger, add only the available number of posts, and disable the job once all posts have entered Buffer. Do not upgrade a paid plan without authorization. Explain the cap and refill schedule. Verify both selection when slots open and the completion stop condition.

The October 2026 content batch lives at `/home/cueva/content/scheduling/buffer`. Its `queue-plan.json` and `queue-ledger.jsonl` record the 57 new posts; the five original LinkedIn posts retain their existing IDs in `requeue-ledger.jsonl`. This batch's machine-local `buffer-content-refill.timer` was retired after the subscription upgrade. Do not reactivate it or reuse its plan for unrelated work. Record confirmed scheduled IDs separately from any local backlog; local entries are not scheduled in Buffer until they have verified remote records.

## Installation lesson

On October 3, 2026, npm package `@bufferapp/cli@1.2.2` failed to install because its published dependencies used unresolved `catalog:` versions. Check current packaging first. For that version, extracting its official npm tarball into a user-local directory, replacing the runtime `commander` dependency with `^14.0.0`, removing development dependencies and lifecycle scripts, and installing runtime dependencies produced a working CLI. Link its `built/index.mjs` into the user's local bin. Keep this workaround isolated; do not modify unrelated agent configuration through `buffer install codex` just to install this skill.
