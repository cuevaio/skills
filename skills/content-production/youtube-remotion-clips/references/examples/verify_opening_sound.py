"""Prove the encoded opening contains the requested swipe, with normal speech afterward."""
import array
import json
import math
import subprocess
from pathlib import Path
import imageio_ffmpeg

ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
def pcm(path,start,duration):
    data=subprocess.check_output([ffmpeg,'-v','error','-ss',str(start),'-i',str(path),
        '-t',str(duration),'-ar','48000','-ac','2','-f','f32le','-'])
    result=array.array('f');result.frombytes(data);return result

def rms(values):
    return math.sqrt(sum(v*v for v in values)/len(values))

sfx=pcm('remotion/public/sfx/opening-swipe.wav',0,19/30)
report=json.loads(Path('review/sound-verification.json').read_text())
clips=json.loads(Path('remotion/clips.json').read_text())
for clip,item in zip(clips,report):
    previous=Path('versions/pre-opening-sound/clips')/(clip['id']+'.mp4')
    output=Path('clips')/(clip['id']+'.mp4')
    old=pcm(previous,0,19/30)
    new=pcm(output,0,19/30)
    actual=[b-a for a,b in zip(old,new)]
    expected=[v*clip['soundEffect']['volume'] for v in sfx]
    correlation=sum(a*b for a,b in zip(actual,expected))/math.sqrt(
        sum(a*a for a in actual)*sum(b*b for b in expected))
    assert correlation > .95,(clip['id'],correlation)
    later_old=pcm(previous,2,2);later_new=pcm(output,2,2)
    error=rms([b-a for a,b in zip(later_old,later_new)])/rms(later_old)
    assert error < .10,(clip['id'],error)
    item.update(encodedEffectCorrelation=correlation,
                laterSpeechRelativeEncodingError=error,encodedAudio='swipe present; later speech preserved')
    print(clip['id']+': encoded opening swipe confirmed',flush=True)
Path('review/sound-verification.json').write_text(json.dumps(report,indent=2))
