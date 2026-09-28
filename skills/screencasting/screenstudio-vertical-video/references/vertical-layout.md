# Vertical Layout Reference

## Canvas And Reusable Modes

Default social canvas:

- 1080×1920
- 30 FPS
- 9:16 square pixels

Create named modes for face-only, camera-over-screen, screen-only, and graphic scenes. Switch modes at meaningful phrase boundaries rather than animating every sentence.

## Privacy Crop Before Cover

Remove operating-system status bars, clocks, notifications, tabs, or account identifiers at the source-coordinate stage. A known project may require a fixed crop—for example, 33 source pixels from the top—but measure each recording rather than copying that value.

For a source with width `SW`, height `SH`, top crop `T`, and destination region `DW × DH`:

```ts
visibleSourceHeight = SH - T;
scale = Math.max(DW / SW, DH / visibleSourceHeight);
renderedWidth = SW * scale;
renderedHeight = SH * scale;
renderedTop = -T * scale;
```

Pan horizontally by converting the desired source-space left edge into rendered coordinates. Clamp the crop so it never reveals outside the source.

Use **cover**, not contain. A dark editor pane is valid source content; a blank strip caused by layout math is not.

## Camera Above Screen

For split layouts:

```ts
screenHeight = 1920 - cameraHeight;
```

Place the camera at the top and screen flush to its bottom edge. Adjust `cameraHeight` by scene when a terminal result needs more width or when the presenter's face would otherwise be lost. The two regions must always total the full canvas height.

Switch to screen-only when the active text remains too small after a sensible crop. Switch to face-only when the screen adds no evidence.

## Readability

- Crop to the active prompt, result, or code block rather than showing the whole desktop.
- Verify at likely phone display size, not only at 100% desktop preview.
- Keep the presenter's eyes and face inside the camera crop throughout the take.
- Use plain designed backgrounds and large borderless media where a concept scene replaces the screen.
- Bundle fonts locally so headless rendering does not depend on network access.
- Prefer official transparent logos and first-party illustrations.

## Captions

Treat caption placement as a platform-overlay problem. Keep captions clear of the bottom action/caption controls and right-side interaction rail, use no more than two lines, and keep the text box narrow enough that the right edge remains unobstructed.

Meta does not publish a fixed placement zone for burned-in captions on organic Reels. Its conservative first-party Reels-ad guidance recommends keeping the top 14%, bottom 35%, and 6% on each side free of important text or logos. At 1080×1920, the strict ad-safe caption rectangle is `x = 65…1015`, `y = 269…1248`, so a caption box anchored to its lower edge uses `bottom: 672px`.

For an organic Reel without a CTA, start with a practical lower-third inset around `bottom: 320px`, keep the full box inside 65 px side insets, and test it in the current app UI. Move to the conservative 672 px inset for paid placement or when the app preview shows additional bottom overlays. Label the chosen mode in the handoff; do not call the lower organic placement officially safe.

Store the inset as a named constant and apply it to the full box, including background and shadow. Verify against the current app before final export because controls vary by device, account, caption length, CTA, and app version.

Primary sources:

- [Instagram Help Center: Reel size and aspect ratios](https://www.facebook.com/help/instagram/1038071743007909)
- [Meta Ads Guide: Instagram Reels](https://www.facebook.com/business/ads-guide/update/video/instagram-reels)
- [Meta Business Help Center: text overlays and Safe Zone for Stories and Reels ads](https://www.facebook.com/business/help/980593475366490)

Recommended review stills:

1. widest caption over face-only
2. widest caption over camera-and-screen
3. smallest terminal text with caption present
4. first and last frame of each layout transition
5. every scene containing a privacy crop

The caption check passes only when every word is readable without competing with platform controls or important on-screen content.
