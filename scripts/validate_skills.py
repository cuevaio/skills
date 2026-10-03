"""Validate the collection's discovery, references, resources and helper syntax."""
import ast
import hashlib
import json
import re
from pathlib import Path
import yaml


def main():
    root = Path(__file__).resolve().parents[1]
    skills = sorted((root/'skills').glob('**/SKILL.md'))
    names = set()
    for skill in skills:
        text = skill.read_text()
        assert text.startswith('---\n'), f'Missing frontmatter: {skill}'
        frontmatter = yaml.safe_load(text.split('---', 2)[1])
        name = frontmatter['name']
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) and len(name) <= 64, name
        assert name == skill.parent.name and name not in names, name
        assert 0 < len(frontmatter['description']) <= 1024, name
        assert len(text.splitlines()) < 500, f'Consider moving detail out of {skill}'
        names.add(name)
    for file in root.rglob('*.md'):
        if '.git' in file.parts:
            continue
        for target in re.findall(r'\]\(([^)\s]+)\)', file.read_text()):
            if '://' in target or target.startswith('#'):
                continue
            target = target.split('#', 1)[0]
            assert not target.startswith('/'), f'Machine-specific reference: {file}: {target}'
            assert (file.parent/target).exists(), f'Broken link: {file}: {target}'
    plugin = json.loads((root/'.claude-plugin/plugin.json').read_text())
    manifest_skills = {str((root/path/'SKILL.md').resolve()) for path in plugin['skills']}
    assert len(plugin['skills']) == len(manifest_skills), 'Duplicate plugin entries'
    assert manifest_skills == {str(skill.resolve()) for skill in skills}, 'Plugin catalog differs from discovered skills'
    adapter = root/'skills/content-production/youtube-remotion-clips'
    catalog = json.loads((adapter/'assets/resource-manifest.json').read_text())
    for resource in [catalog['font']]:
        path = adapter/resource['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == resource['sha256'], path
    assert (adapter/catalog['font']['license']).exists()
    image_formats = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.avif', '.svg'}
    assert not any(p.suffix.lower() in image_formats for p in adapter.rglob('*')), 'Bundle image prompts, not image files'
    assert (adapter/'references/image-prompts.md').is_file()
    for file in root.rglob('*.py'):
        if '.git' not in file.parts:
            ast.parse(file.read_text(), filename=str(file))
    prohibited = {'.wav', '.mp3', '.mp4', '.pyc'}
    for file in (root/'skills').rglob('*'):
        assert file.suffix not in prohibited, f'Unbundled media/cache required: {file}'
    print(f'Validated {len(skills)} skills, plugin discovery, local links, asset hashes and Python syntax')


if __name__ == '__main__':
    main()
