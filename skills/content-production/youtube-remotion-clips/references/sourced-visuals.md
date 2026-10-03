# Real images and screenshots

For named products, search their official site, repository and demos for screenshots. For named people, verify identity from their public profile or an authoritative speaker page before downloading photos. Use generated illustrations for abstract concepts where useful. Do not use generated faces as documentary photos.

Save source URL, publisher, retrieval date, local asset path, and what the visual depicts in `review/visual-sources.json`. Record demo extraction times and screenshot crops. Current product screens illustrate the product; they do not prove a historical statistic, customer purchase or speed claim. Keep source credits in this ledger, not over the video. Downloaded media belongs in the production workspace, never the skill repository.

Every image fills its entire region. Keep captions and the one-frame preview title, but add no headings, person labels, credits, cards, borders, padding or decorative backgrounds. Preview full and split crops at phone size. If filling the region removes the important content, choose a better source image or a separately framed crop.

The bundled renderer supports ordinary `image` cutaways plus two optional kinds:

- `kind: "screenshot"`, `imageSize: [width, height]`, `cropRect: [x, y, width, height]`, optional `splitCropRect`. The crop fills the region without stretching the source pixels; any aspect mismatch is cropped further. Inspect the visible result.
- `kind: "portraits"`, `image` referencing the first photo, `portraits: [{image, objectPosition}]`. Multiple photos stack in full-screen mode and appear side by side within the bottom region in split mode. Use one or two photos at a time. Identity notes remain in the ledger.

Both kinds retain the existing `at`, `duration`, `layout`, `visualStart` and `visualEnd` timing fields. Use `plan_visual_revision.py` to apply them, then preview with `node render.mjs --stills-only`. Hold each visual through the relevant explanation for several seconds.
