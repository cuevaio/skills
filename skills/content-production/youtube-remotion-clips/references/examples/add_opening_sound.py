"""Mix a brief licensed swipe into exports while copying the encoded video intact."""
import array
import hashlib
import json
import math
import shutil
import subprocess
from pathlib import Path
import imageio_ffmpeg

ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
archive=Path('versions/pre-opening-sound')
archive.mkdir(parents=True,exist_ok=True)
if not (archive/'clips.json').exists():
    shutil.copy2('remotion/clips.json',archive/'clips.json')
    shutil.copytree('clips',archive/'clips',dirs_exist_ok=True)
    shutil.copy2('remotion/src/index.jsx',archive/'index.jsx')
    shutil.copy2('clips.zip',archive/'clips.zip')
asset=Path('remotion/public/sfx/opening-swipe.wav')
if not asset.exists():
    subprocess.run([ffmpeg,'-v','error','-y','-i','remotion/public/sfx/mixkit-fast-swipe-zoom-2627.wav',
        '-af','atrim=start=0.04:end=0.673333333,asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st=0.593333333:d=0.04',
        '-ar','48000','-c:a','pcm_s16le',str(asset)],check=True)

def pcm(path,seconds):
    raw=subprocess.check_output([ffmpeg,'-v','error','-i',str(path),'-t',str(seconds),'-ar','48000',
                                  '-ac','2','-f','f32le','-'])
    values=array.array('f');values.frombytes(raw)
    return values

def rms(values):
    return math.sqrt(sum(v*v for v in values)/len(values))

sfx=pcm(asset,19/30)
clips=json.loads(Path('remotion/clips.json').read_text())
report=[]
for clip in clips:
    original=archive/'clips'/(clip['id']+'.mp4')
    speech=pcm(original,19/30)
    # Keep the effect approximately 8 dB below the opening dialogue, capped at 30% gain.
    gain=round(min(.30, .4*rms(speech)/rms(sfx)),4)
    peak=max(abs(v+gain*s) for v,s in zip(speech,sfx))
    if peak > .88:
        gain=round(gain*.88/peak,4)
    clip['soundEffect']=dict(media='sfx/opening-swipe.wav',volume=gain,startFrame=0,durationFrames=19)
    output=Path('clips')/(clip['id']+'.mp4')
    subprocess.run([ffmpeg,'-v','error','-y','-i',str(original),'-i',str(asset),
        '-filter_complex',f'[1:a]volume={gain}[swipe];[0:a][swipe]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]',
        '-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k',
        '-movflags','+faststart',str(output)],check=True)
    def video_hash(path):
        return hashlib.sha256(subprocess.check_output([ffmpeg,'-v','error','-i',str(path),
            '-map','0:v:0','-c','copy','-bsf:v','h264_mp4toannexb','-f','h264','-'])).hexdigest()
    assert video_hash(original)==video_hash(output),clip['id']
    report.append(dict(id=clip['id'],gain=gain,sfxDuration=19/30,
                       estimatedOpeningSpeechRmsDb=20*math.log10(rms(speech)),
                       effectRmsDb=20*math.log10(rms(sfx)*gain),videoBitstream='unchanged'))
    print(f"{clip['id']}: opening swipe at {gain:.3f} gain; video bitstream unchanged",flush=True)
Path('remotion/clips.json').write_text(json.dumps(clips,indent=2))
Path('review/sound-verification.json').write_text(json.dumps(report,indent=2))
p=Path('provenance.json');data=json.loads(p.read_text())
data['opening_sound']={
    'name':'Fast swipe zoom','provider':'Mixkit','item_id':2627,
    'source_page':'https://mixkit.co/free-sound-effects/woosh/',
    'download_url':'https://assets.mixkit.co/active_storage/sfx/2627/2627.wav',
    'license_url':'https://mixkit.co/license/#sfxFree',
    'license_snapshot':'remotion/public/sfx/mixkit-license.html',
    'duration_seconds':19/30,'start_seconds':0,
    'mix':'Effect approximately 8 dB below the opening voice, up to 30% linear gain; original speech gain retained',
    'verification':'review/sound-verification.json',
    'notes':'Sound incorporated in final videos. Do not redistribute the standalone asset in templates or download bundles.'
}
p.write_text(json.dumps(data,indent=2)+'\n')
