"""Extract selected source ranges and generate clip-local word captions."""
import json
from pathlib import Path
import subprocess
import imageio_ffmpeg
from transcribe import timestamp


def groups(words):
    result, current = [], []
    for word in words:
        count = sum(len(w["word"].strip()) + 1 for w in current)
        if current and (count + len(word["word"].strip()) > 28
                        or len(current) >= 5
                        or word["start"] - current[0]["start"] > 1.7):
            result.append({"start": current[0]["start"], "end": current[-1]["end"], "words": current})
            current = []
        current.append(word)
        if word["word"].rstrip().endswith((".", "?", "!")):
            result.append({"start": current[0]["start"], "end": current[-1]["end"], "words": current})
            current = []
    if current:
        result.append({"start": current[0]["start"], "end": current[-1]["end"], "words": current})
    for i, group in enumerate(result):
        next_start = result[i + 1]["start"] if i + 1 < len(result) else group["end"] + .12
        group["end"] = min(next_start, group["end"] + .15)
    return result


def main():
    clips = json.loads(Path("edit-plan.json").read_text())
    transcript = json.loads(Path("transcript/transcript.json").read_text())
    all_words = [word for segment in transcript["segments"] for word in segment["words"]]
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    for clip in clips:
        start, end = clip["start"], clip["end"]
        clip["duration"] = round(end - start, 3)
        clip["media"] = clip["id"] + "-source.mp4"
        output = Path("remotion/public") / clip["media"]
        if not output.exists():
            subprocess.run([ffmpeg, "-hide_banner", "-y", "-ss", str(start), "-i", "source/video.mp4",
                            "-t", str(clip["duration"]), "-vf", "fps=30", "-c:v", "libx264",
                            "-preset", "fast", "-crf", "18", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(output)], check=True)
        refined = Path("transcript") / clip["id"] / "transcript.json"
        reviewed = refined.with_name("reviewed.json")
        if reviewed.exists():
            refined = reviewed
        if refined.exists():
            local = json.loads(refined.read_text())
            clip_words = [word for segment in local["segments"] for word in segment["words"]]
            offset = 0
        else:
            clip_words = [w for w in all_words if w["end"] > start and w["start"] < end]
            offset = start
        words = [{"word": w["word"], "start": max(0, w["start"] - offset),
                  "end": min(end - start, w["end"] - offset)} for w in clip_words]
        for word in words:
            word["word"] = clip.get("corrections", {}).get(word["word"].strip(), word["word"])
        words = [word for word in words if word["word"].strip()]
        # Whisper sometimes gives a spoken word zero duration; retain it using a
        # small share of the following word's interval rather than dropping it.
        for i, word in enumerate(words):
            if word["end"] > word["start"]:
                continue
            if i + 1 < len(words) and words[i + 1]["end"] > word["start"]:
                following = words[i + 1]
                word["end"] = min(word["start"] + .04, following["end"] - .01)
                following["start"] = max(following["start"], word["end"])
            elif i and words[i - 1]["end"] - words[i - 1]["start"] > .06:
                word["end"] = word["start"]
                word["start"] = max(words[i - 1]["start"] + .01, word["start"] - .04)
                words[i - 1]["end"] = min(words[i - 1]["end"], word["start"])
        words = [word for word in words if word["end"] > word["start"]]
        merged = []
        for word in words:
            if merged and (word["word"].startswith("-")
                           or (word["word"].startswith(".") and word["word"].strip()[1:].isdigit())):
                merged[-1]["word"] += word["word"].strip()
                merged[-1]["end"] = word["end"]
            else:
                merged.append(word)
        words = merged
        clip["captions"] = groups(words)
        with (Path("clips") / (clip["id"] + ".srt")).open("w") as srt:
            for index, group in enumerate(clip["captions"], 1):
                text = " ".join(w["word"].strip() for w in group["words"])
                srt.write(f"{index}\n{timestamp(group['start'])} --> {timestamp(group['end'])}\n{text}\n\n")
    Path("remotion/clips.json").write_text(json.dumps(clips, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
