"""Apply a source-specific visual plan to the tightened timeline."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', required=True, type=Path)
    args = parser.parse_args()
    clips = json.loads(Path('remotion/clips.json').read_text())
    plan = json.loads(args.plan.read_text())
    by_id = {item['id']: item for item in plan}
    if len(by_id) != len(plan) or set(by_id) != {clip['id'] for clip in clips}:
        raise ValueError('Visual plan must contain each current clip id exactly once')
    fps = json.loads(Path('remotion/style.json').read_text())['canvas']['fps']
    for clip in clips:
        item = by_id[clip['id']]
        cutaways = item['cutaways']
        for visual in cutaways:
            if visual['layout'] not in {'full', 'split'}:
                raise ValueError('Visual layout must be full or split')
            start = round(visual['at'] * fps) / fps
            duration = round(visual['duration'] * fps) / fps
            if start < 1/fps or duration <= 0 or start+duration > clip['duration']+1e-6:
                raise ValueError(f"{clip['id']}: visual falls outside the usable timeline")
            if not (Path('remotion/public')/visual['image']).is_file():
                raise FileNotFoundError(visual['image'])
            visual.update(at=start, duration=duration)
            visual.setdefault('objectPosition', '50% 50%')
            visual.setdefault('visualStart', start)
            visual.setdefault('visualEnd', start+duration)
        ordered = sorted(cutaways, key=lambda visual: visual['at'])
        if any(a['at']+a['duration'] > b['at']+1e-6 for a,b in zip(ordered, ordered[1:])):
            raise ValueError(f"{clip['id']}: illustrative passages overlap")
        clip['cutaways'] = ordered
        clip['color'] = item.get('highlightColor', clip['color'])
        clip['splitMedia'] = clip['id']+'-split.mp4'
    Path('review').mkdir(exist_ok=True)
    Path('remotion/clips.json').write_text(json.dumps(clips, indent=2)+'\n')
    Path('review/visual-plan.json').write_text(json.dumps(plan, indent=2)+'\n')
    print(f'Applied visual plan for {len(clips)} clips')


if __name__ == '__main__':
    main()
