# Image prompts for clip illustrations

Adapt these references to the current spoken idea. They describe a visual direction, not a fixed image to recreate. Generate fresh images in the production workspace, never inside the skill or repository. Save the final prompt, output filename, generation provenance and inspected focal point in the production's asset record.

## Shared visual direction

Use a warm cinematic 3d illustration with expressive human and robot characters, rounded shapes, believable materials, soft light and restrained teal/amber accents. Make the main action readable at phone size. The image should explain the spoken idea without written labels, code, logos or text. Treat it as a conceptual illustration, not a photograph of a real person or proof of an actual event.

A useful starting prompt:

> a cinematic 3d illustration of [subject doing one clear action that explains the spoken idea]. [setting and one useful visual detail]. warm soft lighting, subtle teal accents, clear separation between subject and background, expressive characters, uncluttered composition, believable materials. keep the important action near the center with room around it for both a vertical full-screen crop and a wide split-screen crop. no text, letters, logos or watermarks.

Change the setting, characters and visual metaphor when the topic changes. Do not force robots or these five motifs into every video.

## Topic references

**Clear intent and domain knowledge.** Show a person communicating a concrete destination or plan to an assistant, with that goal visible in the scene. Example prompt extension: a human and a small robot studying a simple physical model of the thing they want to build, the human pointing to a meaningful part of the model. Avoid implying that an indistinct futuristic glow is the goal.

**Responsibility and the kitchen analogy.** Show a chef coordinating robot sous-chefs in a working kitchen and checking the dish being prepared. Keep the chef's gesture and the shared task readable. Example prompt extension: an attentive chef guiding two robot sous-chefs as they prepare one meal, with a clear work surface and soft kitchen light. Show collaboration rather than an unattended machine producing a perfect result.

**Verification and agent tools.** Show an assistant interacting with an application or inspecting a tangible result. Example prompt extension: a robot using a simple screen and controls to check whether a small mechanism works, watching its visible response, with tools nearby. Use readable physical action rather than tiny fake code or decorative checkmarks as evidence.

**Context and coordination.** Show a coordinator helping several assistants work on distinct parts of one task. Example prompt extension: a coordinator robot at a central workspace, guiding other robots toward different parts of a shared construction, with each worker's role visually distinct. Keep the scene sparse enough to understand without labels.

**Overnight work and earned trust.** Show background work happening while a person rests, with a visible record waiting for later review. Example prompt extension: a sleeping engineer in a quiet room while robot assistants work at a nearby desk, with an orderly stack of completed work ready to inspect in the morning. This illustrates the speaker's story, not a promise of unattended correctness.

## Compose for the actual layouts

- For full-screen 9:16, keep faces and important objects inside the central vertical crop. Add headroom and avoid cutting off gestures.
- For the camera-top/image-bottom split, the image occupies a roughly square region. Keep the action readable in that crop too, or generate a separate composition when one image cannot serve both.
- For the first-frame cover, pair the current speaker's real camera frame with the related illustration. Leave space near the split for the Remotion title; do not bake the title into the generated image.
- Inspect the actual output in both layouts and set its focal point in the visual plan. Prompt wording does not guarantee safe crops.
- Hold the image through the relevant explanation with a slow push. Choose duration from the speech, not from the availability of a visual.
