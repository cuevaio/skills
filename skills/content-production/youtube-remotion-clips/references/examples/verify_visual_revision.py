"""Verify real encoded layout samples and visible active-word color."""
import json
import subprocess
from pathlib import Path
from PIL import Image
import imageio_ffmpeg

ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
probe='remotion/node_modules/@remotion/compositor-linux-x64-gnu/ffprobe'
report=[]
for clip in json.loads(Path('remotion/clips.json').read_text()):
    visuals=clip['cutaways']
    assert [v['layout'] for v in visuals] == ['full','split']
    assert all(v['duration'] >= 3 and 0 <= v['at'] < v['at']+v['duration'] <= clip['duration'] for v in visuals)
    assert abs(visuals[0]['at']+visuals[0]['duration']-visuals[1]['at']) < 1e-6
    info=json.loads(subprocess.check_output([probe,'-v','error','-select_streams','v:0',
        '-show_entries','stream=nb_frames','-of','json','remotion/public/'+clip['splitMedia']]))
    assert int(info['streams'][0]['nb_frames']) == round(clip['duration']*30)
    words=[w for c in clip['captions'] for w in c['words']]
    samples=[]
    for visual in visuals:
        word=next(w for w in words if w['start']>visual['at']+.2
                  and w['end']<visual['at']+visual['duration']-.2 and w['end']-w['start']>.18)
        frame=round((word['start']+word['end'])/2*30)
        assert word['start'] < frame/30 < word['end']
        dest=Path('review')/f"{clip['id']}-highlight-{visual['layout']}.png"
        subprocess.run([ffmpeg,'-v','error','-y','-ss',str(frame/30),'-i',f"clips/{clip['id']}.mp4",
                        '-frames:v','1',str(dest)],check=True)
        image=Image.open(dest).convert('RGB')
        accent=tuple(int(clip['color'][i:i+2],16) for i in (1,3,5))
        area=image.crop((65,1390,1015,1600))
        pixels=sum(all(abs(p[i]-accent[i])<=16 for i in range(3)) for p in area.getdata())
        assert pixels > 50, (clip['id'],visual['layout'],word,pixels)
        samples.append(dict(layout=visual['layout'],seconds=frame/30,word=word['word'].strip(),
                            accent=clip['color'],accentPixels=pixels,frame=str(dest)))
    report.append(dict(id=clip['id'],fullSeconds=visuals[0]['duration'],
                       splitSeconds=visuals[1]['duration'],cameraFrames='aligned',samples=samples))
    print(clip['id']+': sustained layouts, synchronized camera and visible word highlight passed',flush=True)
Path('review/visual-verification.json').write_text(json.dumps(report,indent=2))
