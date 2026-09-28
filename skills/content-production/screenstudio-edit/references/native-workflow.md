# Native Screen Studio Workflow

Use this branch when Screen Studio can express the required edit and export reliably.

## Protect The Project

Duplicate or version the `.screenstudio` package before structural edits. Keep raw recordings and the last approved project version until the final encoded file passes review.

## Apply The Cut List

Use the cut list and review decisions from `video-edit`:

1. apply source ranges without detaching screen, camera, microphone, or system audio
2. preserve approved native speed changes
3. verify that ripple edits move all linked sources together
4. compare the implemented range against the approved transcript/timeline

## Implement Layouts

Apply the layout map from `video-edit`. Crop identified privacy regions, fill every assigned region, and implement the approved source-space pan toward active proof.

For multi-orientation delivery, create separate layout versions rather than forcing one compromise composition.

## Motion And Cursor

Use automatic or manual zoom only to direct attention. Repair a zoom that hides context, arrives after the action, or makes the pointer difficult to follow. Keep cursor movement intentional; remove idle circling and avoid decorative motion over dense text.

Use consistent camera shape, padding, crop behavior, transition timing, and zoom intensity across the project.

## Implement Audio And Captions

Select the approved dialogue and system-audio tracks once. Apply the caption file, style, and safe-zone position from `video-edit`. Inspect joins for detached or doubled audio and verify caption timing after every timeline change.

## Review And Export

Export short review ranges for the opening, densest demonstration, widest captions, complex transitions, and ending. After approval, export a local master and run the independent checks in `export-qc.md`.

The native implementation passes when the approved cut, layout, audio, caption, privacy, and orientation decisions match the exported review ranges.
