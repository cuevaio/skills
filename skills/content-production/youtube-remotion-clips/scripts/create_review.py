"""Create an offline review page and contact sheets from encoded exports."""
import html
import json
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg


def main():
    clips = json.loads(Path("remotion/clips.json").read_text())
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    font = ImageFont.truetype("remotion/public/SpaceGrotesk-Variable.ttf", 18)
    cards = []
    for clip in clips:
        widest = max(clip["captions"], key=lambda c: sum(len(w["word"]) for w in c["words"]))
        times = [0, clip["cutaways"][0]["at"] + 1 if clip["cutaways"] else clip["duration"] / 2,
                 clip["cutaways"][1]["at"] + 1 if len(clip["cutaways"]) > 1 else clip["duration"] / 2,
                 (widest["start"] + widest["end"]) / 2, clip["duration"] - .6]
        sheet = Image.new("RGB", (270 * len(times), 520), "#101418")
        draw = ImageDraw.Draw(sheet)
        for index, time in enumerate(times):
            time = max(0, min(time, clip["duration"]-1/30))
            dest = Path("review") / f"{clip['id']}-encoded-{index}.jpg"
            subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-ss", str(time),
                            "-i", f"clips/{clip['id']}.mp4", "-frames:v", "1", str(dest)], check=True)
            img = Image.open(dest).resize((270, 480), Image.Resampling.LANCZOS)
            sheet.paste(img, (index * 270, 0))
            draw.text((index * 270 + 12, 491), f"{time:.2f}s", fill="#ffffff", font=font)
        sheet.save(Path("review") / f"{clip['id']}-contact.jpg", quality=95)
        source = f"{int(clip['start']//60):02}:{clip['start']%60:05.2f}–{int(clip['end']//60):02}:{clip['end']%60:05.2f}"
        cards.append(f'''<article><h2>{html.escape(clip['title'])}</h2>
<p>{clip['duration']:.1f}s · Source {source}</p>
<video controls preload="metadata" poster="covers/{clip['id']}.png" src="clips/{clip['id']}.mp4"></video>
<p>{html.escape(clip['reason'])}</p>
<a href="clips/{clip['id']}.mp4" download>Download MP4</a> · <a href="clips/{clip['id']}.srt" download>Download subtitles</a> · <a href="covers/{clip['id']}.png" download>Download cover</a>
</article>''')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>clip review</title><style>
*{box-sizing:border-box}body{margin:0;background:#101418;color:#f4f1e8;font:17px system-ui,sans-serif;padding:40px 6vw;max-width:1500px;margin:auto}
h1{font-size:clamp(32px,5vw,60px);letter-spacing:-2px;margin-bottom:12px}h2{font-size:24px}p{color:#b6bfc5;line-height:1.55}a{color:#9fe7d0}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:28px;margin-top:40px}article{background:#191f25;padding:22px;border-radius:20px}video{display:block;width:100%;max-height:620px;aspect-ratio:9/16;background:#000;border-radius:12px}footer{margin:40px 0}
</style><h1>clip review</h1><p>Complete ideas from the source recording. 1080×1920 · 30 fps · Space Grotesk captions with word highlighting · Full-screen and split-screen visuals · Tight cuts.</p>
<p>Ready for creator review. Visuals may include sourced screenshots, public photos and conceptual illustrations. Check provenance for source and generation records.</p>
<p><a href="source/video.mp4">Full recording</a> · <a href="transcript/transcript.txt">Readable Whisper transcript</a> · <a href="transcript/transcript.srt">Full subtitles</a> · <a href="clips.zip">All clips and subtitles</a></p><main>'''
    page += "\n".join(cards)
    page += '''</main><footer><a href="edit-plan.json">Source ranges and edit decisions</a> · <a href="provenance.json">Assets and transcription notes</a> · <a href="review/verification.json">Export checks</a></footer></html>'''
    Path("index.html").write_text(page)


if __name__ == "__main__":
    main()
