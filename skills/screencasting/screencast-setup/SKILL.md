---
name: screencast-setup
description: Prepare and test a reliable screencast recording setup. Use when choosing recording gear or software, improving audio, camera, lighting, room acoustics, screen readability, privacy, source capture, or creating a preflight checklist.
---

# Set Up A Screencast

Build the smallest setup that passes a playback test. Upgrade only to solve a problem the test exposes.

Perform setup and playback actions directly when the available tools can control and inspect the recording environment. Otherwise, prepare the checklist for the user, ask them to run one test, and assess the returned clip, screenshots, metadata, or explicit observations. Keep the gate open until that evidence passes.

## Process

### 1. Establish The Capture

Read the production brief when one exists. Determine which sources the video actually needs:

- screen
- microphone
- system or application audio
- camera
- secondary camera or device

Prefer one recorder that captures required sources simultaneously on separate tracks. If sources must be recorded separately, establish a visible and audible sync mark at the start of each take.

Decide whether camera adds useful human connection. A brief on-camera introduction followed by screen-only teaching is a valid middle ground. Screen-only is valid when privacy, comfort, or editability matters more.

### 2. Fix Quality In Priority Order

Work from impact, not price:

1. **Speech:** place the microphone close to the speaker, set conservative input levels, and remove hum, clipping, plosives, and desk vibration.
2. **Room:** reduce echo with a smaller space and soft surfaces such as curtains, rugs, blankets, or acoustic treatment.
3. **Screen:** make the demonstrated content readable at the viewer's likely playback size.
4. **Light:** if on camera, use a soft, controllable key light; add separation or background light only if needed.
5. **Camera:** use the camera already available until it creates a specific limitation.

Stable framing and controlled light matter more than an expensive camera. Stable, intelligible audio matters more than perfect visuals.

### 3. Prepare The Environment

Load [references/preflight.md](references/preflight.md) as the source of truth for operational checks. Remove irrelevant items and add production-specific checks. Work through it to create a private, distraction-free, readable screen and a quiet, repeatable room and presenter state.

For a series, record exact device names and the chosen layout, level, zoom, resolution, brightness, framing, and position values so another session can reproduce them.

### 4. Configure The Recorder

Confirm each source by name rather than trusting defaults. Record the full intended display or an explicit region, whichever removes more capture risk.

Avoid committing to a specific application, resolution, or frame rate unless the delivery platform or demonstrated motion requires it.

### 5. Run Preflight

Record 20 to 30 seconds containing:

- normal and emphatic speech
- representative typing and mouse movement
- system audio when needed
- the presenter in their normal camera position when used
- a representative app, terminal, or code sample at final layout size

Play the test back with headphones and view it at the likely delivery size. The setup gate passes only when speech is clean and intelligible, every required source is present and synchronized, screen text is readable, framing and lighting are stable, and no private or distracting material is visible.

Return or save this handoff:

```markdown
## Setup Handoff
- Checklist: <path or inline checklist>
- Tested on: <date and environment>
- Sources and exact device names:
- Project/capture settings:
- Repeatable room, screen, and presenter settings:
- Test evidence and result:
- Open risks: none / <list>
```
