"""Compare the encoded opening frame with the cover, and frame one with the prior cut."""
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageChops, ImageStat
import imageio_ffmpeg

ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
report=[]
for clip in json.loads(Path('remotion/clips.json').read_text()):
    cover=Image.open(f"covers/{clip['id']}.png").convert('RGB')
    assert cover.size == (1080,1920)
    assert clip['cover']['frames'] == 1
    paths=[]
    for name,media,time in [
        ('cover-encoded',f"clips/{clip['id']}.mp4",0),
        ('after-cover',f"clips/{clip['id']}.mp4",1/30),
        ('previous-opening',f"versions/pre-covers/clips/{clip['id']}.mp4",1/30),
    ]:
        path=Path('review')/f"{clip['id']}-{name}.png"
        subprocess.run([ffmpeg,'-v','error','-y','-ss',str(time),'-i',media,
                        '-frames:v','1',str(path)],check=True)
        paths.append(path)
    encoded=Image.open(paths[0]).convert('RGB')
    cover_error=sum(ImageStat.Stat(ImageChops.difference(cover,encoded)).mean)/3
    assert cover_error < 6, (clip['id'],cover_error)
    following=Image.open(paths[1]).convert('RGB')
    previous=Image.open(paths[2]).convert('RGB')
    next_error=sum(ImageStat.Stat(ImageChops.difference(following,previous)).mean)/3
    assert next_error < 6, (clip['id'],next_error)
    report.append(dict(id=clip['id'],cover=f"covers/{clip['id']}.png",dimensions='1080x1920',
                       encodedFirstFrameMeanError=cover_error,
                       nextFrameComparedWithPreviousExportMeanError=next_error,
                       firstFrame='cover matches',secondFrame='original cut resumes'))
    print(clip['id']+': encoded cover and immediate return to existing cut passed',flush=True)
Path('review/cover-verification.json').write_text(json.dumps(report,indent=2))
