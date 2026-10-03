"""Extract inspected camera portraits for one-frame split covers."""
import json
import subprocess
from pathlib import Path
import imageio_ffmpeg


def main():
    clips = json.loads(Path('remotion/clips.json').read_text())
    for clip in clips:
        if 'coverTime' not in clip or not 0 <= clip['coverTime'] < clip['duration']:
            raise ValueError(f"{clip['id']}: supply coverTime from an inspected tightened frame")
        if not clip.get('cutaways'):
            raise ValueError(f"{clip['id']}: supply a related image before preparing the cover")
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    Path('covers').mkdir(exist_ok=True)
    for clip in clips:
        camera = clip['id']+'-cover-camera.jpg'
        subprocess.run([ffmpeg, '-v', 'error', '-y', '-ss', str(clip['coverTime']),
                        '-i', 'remotion/public/'+clip['splitMedia'], '-frames:v', '1',
                        '-q:v', '2', 'remotion/public/'+camera], check=True)
        visual = clip['cutaways'][0]
        clip['cover'] = dict(camera=camera, image=visual['image'],
                            objectPosition=visual['objectPosition'], frames=1)
    Path('remotion/clips.json').write_text(json.dumps(clips, indent=2)+'\n')
    print(f'Prepared {len(clips)} cover portraits')


if __name__ == '__main__':
    main()
