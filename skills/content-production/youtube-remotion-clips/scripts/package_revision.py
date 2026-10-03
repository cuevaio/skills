"""Bundle current deliverables, excluding standalone sound and source recordings."""
import json
from pathlib import Path
import zipfile

clips = json.loads(Path('remotion/clips.json').read_text())
if not clips:
    raise ValueError('No clips to package')
paths = [Path(folder)/(clip['id']+suffix) for clip in clips
         for folder,suffix in [('clips','.mp4'), ('clips','.srt'), ('covers','.png')]]
paths += [Path('edit-plan.json'), Path('provenance.json'), Path('remotion/clips.json')]
paths += list(Path('review').glob('*verification.json'))
paths += [Path(name) for name in ['social-copy.json','CONTENT_STYLE.md'] if Path(name).is_file()]
for path in paths:
    if not path.is_file():
        raise FileNotFoundError(path)
with zipfile.ZipFile('clips.zip.tmp', 'w', compression=zipfile.ZIP_STORED) as bundle:
    for path in paths:
        bundle.write(path, str(path))
with zipfile.ZipFile('clips.zip.tmp') as bundle:
    assert bundle.testzip() is None
Path('clips.zip.tmp').replace('clips.zip')
print(f'Bundled {len(clips)} clips with subtitles, covers and provenance')
