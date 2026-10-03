"""Prepare an offline clip workspace from the approved style and local asset cache."""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_resource(source, destination, expected=None, preserve_existing=False):
    if not source.is_file():
        raise FileNotFoundError(f'Missing cached resource: {source}')
    if expected and digest(source) != expected:
        raise ValueError(f'Cached resource checksum mismatch: {source}')
    if destination.exists():
        if preserve_existing or digest(source) == digest(destination):
            return
        raise ValueError(f'Refusing to overwrite a different resource: {destination}')
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True, type=Path)
    parser.add_argument('--images', nargs='*', help='Image IDs to copy; omit to copy the five cached illustrations')
    parser.add_argument('--no-runtime-link', action='store_true')
    parser.add_argument('--cache-root', type=Path, default=Path('~/.cache/clip-production'),
                        help='Private clip-production cache root')
    parser.add_argument('--sound', choices=['auto', 'required', 'skip'], default='auto',
                        help='Reuse cached sound; auto records a missing cache without downloading')
    args = parser.parse_args()
    skill = Path(__file__).resolve().parents[1]
    workspace = args.workspace.expanduser().resolve()
    if workspace == skill or skill in workspace.parents:
        raise ValueError('The production workspace must be outside the skill folder')
    manifest = json.loads((skill/'assets/library/manifest.json').read_text())
    cache_root = args.cache_root.expanduser().resolve()
    for section in ['privateSound', 'runtime']:
        for key, value in manifest[section].items():
            prefix = '~/.cache/clip-production/'
            if isinstance(value, str) and value.startswith(prefix):
                manifest[section][key] = str(cache_root/value[len(prefix):])
    ids = {i['id'] for i in manifest['images']}
    if args.images is not None and set(args.images)-ids:
        raise ValueError(f'Unknown image IDs: {sorted(set(args.images)-ids)}')
    for name in ['source','transcript','scripts','clips','covers','review','remotion/public']:
        (workspace/name).mkdir(parents=True, exist_ok=True)
    template = skill/'assets/remotion'
    for source in template.rglob('*'):
        if source.is_file():
            copy_resource(source, workspace/'remotion'/source.relative_to(template), preserve_existing=True)
    for source in (skill/'scripts').glob('*.py'):
        if source.name != Path(__file__).name:
            copy_resource(source, workspace/'scripts'/source.name, preserve_existing=True)
    copied = []
    for resource in manifest['images']:
        if args.images is not None and resource['id'] not in args.images:
            continue
        source = skill/resource['path']
        copy_resource(source, workspace/'remotion/public'/source.name, resource['sha256'])
        copied.append(resource['id'])
    sound = manifest['privateSound']
    sound_sources = [(Path(sound['path']).expanduser(), 'opening-swipe.wav', sound['sha256']),
                     (Path(sound['sourcePath']).expanduser(), 'mixkit-fast-swipe-zoom-2627.wav', None),
                     (Path(sound['licensePath']).expanduser(), 'mixkit-license.html', None)]
    available = all(source.is_file() for source, _, _ in sound_sources)
    if args.sound == 'required' and not available:
        raise FileNotFoundError('Private swipe cache is missing; see references/resource-reuse.md')
    reused_sound = args.sound != 'skip' and available
    if reused_sound:
        for source, name, checksum in sound_sources:
            copy_resource(source, workspace/'remotion/public/sfx'/name, checksum)
    font = manifest['font']
    assert digest(workspace/'remotion/public/SpaceGrotesk-Variable.ttf') == font['sha256']
    runtime = manifest['runtime']
    modules = Path(runtime['nodeModules']).expanduser()
    lock = Path(runtime['packageLock']).expanduser()
    destination = workspace/'remotion/node_modules'
    linked = destination.is_symlink() and modules.is_dir() and destination.resolve() == modules.resolve()
    if not args.no_runtime_link and not destination.exists() and not destination.is_symlink() and modules.is_dir() and lock.is_file():
        if digest(lock) == digest(workspace/'remotion/package-lock.json'):
            destination.symlink_to(modules, target_is_directory=True)
            linked = True
    clips = workspace/'remotion/clips.json'
    if not clips.exists():
        clips.write_text('[]\n')
    copy_resource(skill/'references/requirements.txt', workspace/'requirements.txt', preserve_existing=True)
    (workspace/'review/resource-reuse.json').write_text(json.dumps({
        'skill':str(skill),'images':copied,'sound':'private local cache' if reused_sound else 'not copied; setup needed before final export',
        'runtimeLinked':linked,'python':sys.executable,
        'whisperCache':runtime['whisperCache'],'networkRequests':0
    }, indent=2)+'\n')
    print(json.dumps({'workspace':str(workspace),'images':copied,'privateSoundReused':reused_sound,
                      'runtimeLinked':linked,'networkRequests':0}))


if __name__ == '__main__':
    main()
