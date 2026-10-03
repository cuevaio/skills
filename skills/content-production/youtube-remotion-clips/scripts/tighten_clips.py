"""Build one frame-aligned timeline for media, captions, cuts and cutaways."""
import json
import re
import shutil
import subprocess
from pathlib import Path
import imageio_ffmpeg
from prepare_clips import groups
from transcribe import timestamp

FPS = 30
SPEED = 1.15
HANDLE = .06

def main():
    archive = Path('versions/pre-full-camera')
    archive.mkdir(parents=True, exist_ok=True)
    original = archive / 'clips.json'
    if not original.exists():
        shutil.copy2('remotion/clips.json', original)
        shutil.copytree('clips', archive / 'clips', dirs_exist_ok=True)
        shutil.copy2('remotion/src/index.jsx', archive / 'index.jsx')
    clips = json.loads(original.read_text())
    style = json.loads(Path('remotion/style.json').read_text())
    global FPS, SPEED, HANDLE
    FPS = style['canvas']['fps']
    SPEED = style['editing']['speed']
    HANDLE = style['editing']['handleSeconds']
    silence_db = style['editing']['silenceDb']
    silence_seconds = style['editing']['minimumSilenceSeconds']
    for clip in clips:
        if not clip.get('portraitCrop'):
            raise ValueError(f"{clip['id']}: supply portraitCrop in edit-plan.json after inspecting the source")
        if not clip.get('captions'):
            raise ValueError(f"{clip['id']}: word captions are required before tightening")
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    report = []
    for clip in clips:
        source = Path('remotion/public') / (clip['id'] + '-source.mp4')
        scan = subprocess.run([ffmpeg, '-hide_banner', '-i', str(source), '-af',
            f'silencedetect=noise={silence_db}dB:d={silence_seconds}', '-vn', '-f', 'null', '-'], capture_output=True, text=True, check=True)
        silences, pending = [], None
        for line in scan.stderr.splitlines():
            match = re.search(r'silence_start: ([\d.]+)', line)
            if match:
                pending = float(match[1])
            match = re.search(r'silence_end: ([\d.]+)', line)
            if match and pending is not None:
                silences.append((pending, float(match[1])))
                pending = None
        if pending is not None:
            silences.append((pending, clip['duration']))
        # Cut only measured silence. Keep breath handles and align source cuts to frames.
        remove = [(round((a + HANDLE) * FPS) / FPS,
                   round((b - HANDLE) * FPS) / FPS) for a, b in silences if b-a >= silence_seconds]
        words = [w for c in clip['captions'] for w in c['words']]
        lead = max(0, words[0]['start'] - HANDLE)
        tail = min(clip['duration'], words[-1]['end'] + HANDLE)
        ranges, cursor = [], round(lead*FPS)/FPS
        for a, b in remove:
            a, b = max(cursor, a), min(tail, b)
            if b <= a:
                continue
            if a-cursor >= 1/FPS:
                ranges.append((cursor, a))
            cursor = b
        if tail-cursor >= 1/FPS:
            ranges.append((cursor, round(tail*FPS)/FPS))
        segments, out = [], 0
        for a, b in ranges:
            frames = max(1, round((b-a)/SPEED*FPS))
            duration = frames/FPS
            segments.append(dict(sourceStart=a, sourceEnd=b, outputStart=out,
                                 outputEnd=out+duration, frames=frames, rate=(b-a)/duration))
            out += duration
        def remap(t):
            for s in segments:
                if t <= s['sourceEnd']:
                    return s['outputStart'] + max(0, t-s['sourceStart'])/s['rate']
            return out
        mapped = []
        for w in words:
            a, b = remap(w['start']), remap(w['end'])
            if b > a:
                mapped.append(dict(word=w['word'], start=round(a,6), end=round(b,6)))
        clip['captions'] = groups(mapped)
        for c in clip['captions']:
            c['end'] = min(out, c['end'])
        clip['duration'] = out
        clip['segments'] = segments
        clip['videoShots'] = [dict(at=s['outputStart'], focus='speaker') for s in segments]
        # Plan sustained visual beats after tightening, against the remapped spoken phrases.
        clip['cutaways'] = []
        clip['media'] = clip['id'] + '-tight.mp4'
        output = Path('remotion/public') / clip['media']
        filters = []
        count = len(segments)
        filters.append('[0:v]' + clip['portraitCrop'] + ',split=' + str(count) + ''.join(f'[v{i}]' for i in range(count)))
        filters.append('[0:a]asplit=' + str(count) + ''.join(f'[a{i}]' for i in range(count)))
        for i, s in enumerate(segments):
            a,b,d,r = s['sourceStart'],s['sourceEnd'],s['frames']/FPS,s['rate']
            filters.append(f'[v{i}]trim=start={a}:end={b},setpts=(PTS-STARTPTS)/{r},fps=30,tpad=stop_mode=clone:stop_duration=0.1,trim=end_frame={s["frames"]},setsar=1[vo{i}]')
            filters.append(f'[a{i}]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,atempo={r},apad,atrim=duration={d},afade=t=in:d=0.004,afade=t=out:st={max(0,d-.004)}:d=0.004[ao{i}]')
        filters.append(''.join(f'[vo{i}][ao{i}]' for i in range(count)) + f'concat=n={count}:v=1:a=1[vout][acat]')
        filters.append('[acat]loudnorm=I=-16:TP=-1.5:LRA=11[aout]')
        graph = Path('review') / (clip['id']+'-tighten.ffgraph')
        graph.write_text(';\n'.join(filters))
        subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(source),
                        '-filter_complex_script',str(graph),'-map','[vout]','-map','[aout]',
                        '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',
                        '-c:a','aac','-b:a','192k','-movflags','+faststart',str(output)],check=True)
        with (Path('clips')/(clip['id']+'.srt')).open('w') as f:
            for i,c in enumerate(clip['captions'],1):
                text = re.sub(r'\s+([,.;!?])', r'\1', ' '.join(w['word'].strip() for w in c['words']))
                f.write(f"{i}\n{timestamp(c['start'])} --> {timestamp(c['end'])}\n{text}\n\n")
        item = dict(id=clip['id'], originalDuration=clip['end']-clip['start'],
                    duration=out, removedSilence=sum(b-a for a,b in remove),
                    measuredSilences=silences, segments=segments, speed=SPEED)
        report.append(item)
        print(f"{clip['id']}: {item['originalDuration']:.2f}s → {out:.2f}s, {count} shots",flush=True)
    Path('remotion/clips.json').write_text(json.dumps(clips,indent=2))
    Path('review/tightening.json').write_text(json.dumps(report,indent=2))

if __name__ == '__main__':
    main()
