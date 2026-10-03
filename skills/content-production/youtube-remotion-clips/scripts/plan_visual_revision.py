"""Apply a source-specific visual plan to the tightened timeline."""
import argparse
import json
import math
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
            kind = visual.get('kind')
            if kind not in {None, 'screenshot', 'portraits'}:
                raise ValueError('Unknown visual kind')
            if kind == 'screenshot':
                size = visual.get('imageSize', [])
                if len(size) != 2 or any(not isinstance(v, (int, float)) or not math.isfinite(v) or v <= 0 for v in size):
                    raise ValueError('Screenshot imageSize must contain positive dimensions')
                for field in ['cropRect'] + (['splitCropRect'] if 'splitCropRect' in visual else []):
                    crop = visual.get(field, [])
                    if len(crop) != 4 or any(not isinstance(v, (int, float)) or not math.isfinite(v) for v in crop):
                        raise ValueError('Screenshot crop must contain four finite numbers')
                    x, y, width, height = crop
                    if x < 0 or y < 0 or width <= 0 or height <= 0 or x+width > size[0] or y+height > size[1]:
                        raise ValueError('Screenshot crop must fit inside imageSize')
            if kind == 'portraits':
                portraits = visual.get('portraits', [])
                if not 1 <= len(portraits) <= 2:
                    raise ValueError('Use one or two portrait images per passage')
                for portrait in portraits:
                    if not (Path('remotion/public')/portrait['image']).is_file():
                        raise FileNotFoundError(portrait['image'])
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
