"""Measure opening speech and configure one swipe in the Remotion timeline."""
import argparse
import array
import json
import math
import subprocess
from pathlib import Path
import imageio_ffmpeg


def pcm(ffmpeg, path, seconds):
    raw = subprocess.check_output([ffmpeg, '-v', 'error', '-i', str(path), '-t', str(seconds),
                                   '-ar', '48000', '-ac', '2', '-f', 'f32le', '-'])
    values = array.array('f')
    values.frombytes(raw)
    if not values:
        raise ValueError(f'No opening audio: {path}')
    return values


def rms(values):
    return math.sqrt(sum(value*value for value in values)/len(values))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--disable', action='store_true', help='Explicitly omit the opening sound')
    args = parser.parse_args()
    path = Path('remotion/clips.json')
    clips = json.loads(path.read_text())
    style = json.loads(Path('remotion/style.json').read_text())
    settings = style['openingSound']
    report = []
    if args.disable or not settings['enabled']:
        for clip in clips:
            clip.pop('soundEffect', None)
        report.append({'sound': 'disabled explicitly'})
    else:
        asset = Path('remotion/public')/settings['asset']
        if not asset.is_file():
            raise FileNotFoundError('Opening swipe missing; see resource-reuse.md for private cache setup')
        seconds = settings['durationFrames']/style['canvas']['fps']
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        effect = pcm(ffmpeg, asset, seconds)
        effect_rms = rms(effect)
        if effect_rms == 0:
            raise ValueError('Opening swipe contains no audible sound')
        for clip in clips:
            speech = pcm(ffmpeg, Path('remotion/public')/clip['media'], seconds)
            gain = min(settings['maximumGain'], settings['rmsRatioToSpeech']*rms(speech)/effect_rms)
            # Reduce only the effect if its mix exceeds the desired sample headroom.
            for _ in range(12):
                peak = max(abs(voice+gain*sfx) for voice,sfx in zip(speech,effect))
                if peak <= .88:
                    break
                gain *= .8
            gain = round(gain, 4)
            clip['soundEffect'] = dict(media=settings['asset'], volume=gain, startFrame=0,
                                       durationFrames=settings['durationFrames'])
            report.append(dict(id=clip['id'], gain=gain, durationSeconds=seconds,
                               speechRms=rms(speech), effectRms=effect_rms*gain))
    path.write_text(json.dumps(clips, indent=2)+'\n')
    Path('review').mkdir(exist_ok=True)
    Path('review/sound-plan.json').write_text(json.dumps(report, indent=2)+'\n')
    provenance = Path('provenance.json')
    data = json.loads(provenance.read_text()) if provenance.exists() else {}
    data['openingSound'] = {'plan': 'review/sound-plan.json', 'asset': settings['asset'],
                            'disabled': args.disable or not settings['enabled'],
                            'license': 'private asset; do not redistribute standalone sound'}
    provenance.write_text(json.dumps(data, indent=2)+'\n')
    print(f'Configured opening audio for {len(clips)} clips')


if __name__ == '__main__':
    main()
