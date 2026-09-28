# Screen Studio Composition

## Reusable Layouts

Build named face-only, screen-only, camera-and-screen, and graphic modes. Vertical layouts commonly place camera above screen; horizontal layouts commonly use screen-dominant picture-in-picture or side-by-side. Choose based on proof readability, not convention alone.

## Privacy Crop Before Cover

Remove status bars, clocks, notifications, tabs, and account identifiers in source coordinates. A previous project needed 33 source pixels removed from the top; measure each recording instead of copying that value.

For source `SW × SH`, top crop `T`, and destination `DW × DH`:

```ts
visibleSourceHeight = SH - T;
scale = Math.max(DW / SW, DH / visibleSourceHeight);
renderedWidth = SW * scale;
renderedHeight = SH * scale;
renderedTop = -T * scale;
```

Pan by converting a desired source-space edge into rendered coordinates and clamp so the crop never reveals outside the source. Use cover, not contain: a dark editor pane may be source content; an empty strip caused by layout math is not.

## Vertical

- Default canvas: 1080×1920 at 30 FPS.
- In split layouts, camera and screen heights must sum to 1920 and touch exactly.
- Change camera height by scene when a terminal result needs more width while keeping the face visible.
- Switch to screen-only when proof remains too small.
- Reserve current platform safe zones for captions and interaction controls.

## Horizontal

- Default canvas: 1920×1080 at source frame rate or 30 FPS.
- Give proof most of the width; keep camera placement stable across adjacent actions.
- Use screen-only for dense code or terminal results.
- Avoid permanent overlays when the master will feed vertical derivatives.

## Deterministic Assets

Bundle fonts locally, use official assets with appropriate transparency, and make graphic-scene backgrounds explicit. Render review stills for widest captions, smallest proof, each privacy crop, and the first and last frame of layout transitions.
