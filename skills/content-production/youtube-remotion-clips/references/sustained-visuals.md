# Sustained visuals and highlighted captions

The user rejected the second clip's repeated 850 ms illustration flashes. Their preferred choices are full-screen images and a half-height camera above an AI image, with both held long enough to understand. They also requested the original active-word highlighting with the newer Space Grotesk caption style.

Plan a complete visual passage around the actual spoken topic. In the kitchen example, the image starts when the speaker explains being a chef at 4.67 s. It stays full-screen until 8.93 s, then remains in the lower half while camera fills the top until 21.57 s. This is one continuous 16.9 s visual section, not two disconnected flashes. Other clips have 8–12 s visual passages. Durations are editorial examples, not fixed requirements.

Use object-fit: cover inside both full-screen and split regions. Contain on a landscape image previously left large white bars. Choose an image-specific focal position and inspect faces and important objects. A focal point that suits a wide region may cut off a human face in a tall crop. The trust image needed 20% horizontal positioning and the sleeping image 12%.

The split layout uses y=0..960 for camera and y=960..1920 for the image. The already tightened portrait camera cannot restore the shoulders lost to its crop. Generate a second camera variant from the original source with exactly the same retained segments, rates and frame counts. For this source, crop 952×960 at x=968, y=0; the 8 px horizontal offset excludes the interview's divider. The wide variant is muted and overlays the existing camera. Audio continues from the original tightened media, including during image-only shots.

Retain captions at bottom inset 320 px in both layouts. Highlight each word only between its remapped start and end. Keep inactive text white and use the existing per-clip pastel accent. Space Grotesk 64 px, weight 620, white text, translucent black box and its padding remain unchanged. Suppress inserted spaces before punctuation so Whisper tokens like `2` plus `,500` read as `2,500`.

Hold image motion to a slow 3.5% push across the entire visual passage. Use shared visualStart and visualEnd across both layouts so the motion does not reset at the switch. Preview each layout and transition, then inspect the final encoded frames. Preserve previous exports before replacement.
