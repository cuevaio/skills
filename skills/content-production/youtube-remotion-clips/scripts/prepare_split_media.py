"""Keep the original speaker width for the half-screen camera layout."""
import json
import subprocess
import sys
from pathlib import Path
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
for clip in json.loads(Path('remotion/clips.json').read_text()):
    output = Path('remotion/public')/clip['splitMedia']
    if output.exists() and '--force' not in sys.argv:
        continue
    segments = clip['segments']
    if not clip.get('splitCrop'):
        raise ValueError(f"{clip['id']}: supply splitCrop for this source")
    filters = ['[0:v]' + clip['splitCrop'] + ',split=' + str(len(segments))
               + ''.join(f'[v{i}]' for i in range(len(segments)))]
    for i,s in enumerate(segments):
        filters.append(f'[v{i}]trim=start={s["sourceStart"]}:end={s["sourceEnd"]},'
            f'setpts=(PTS-STARTPTS)/{s["rate"]},fps=30,'
            f'tpad=stop_mode=clone:stop_duration=0.1,trim=end_frame={s["frames"]},setsar=1[o{i}]')
    filters.append(''.join(f'[o{i}]' for i in range(len(segments)))
                   + f'concat=n={len(segments)}:v=1:a=0[out]')
    graph = Path('review')/(clip['id']+'-split.ffgraph')
    graph.write_text(';\n'.join(filters))
    subprocess.run([ffmpeg,'-v','error','-y','-i',
        'remotion/public/'+clip['id']+'-source.mp4','-filter_complex_script',str(graph),
        '-map','[out]','-an','-c:v','libx264','-preset','fast','-crf','18',
        '-pix_fmt','yuv420p','-movflags','+faststart',str(output)],check=True)
    print(f"Prepared {clip['id']} wide camera",flush=True)
