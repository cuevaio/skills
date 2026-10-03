"""Exercise portable scaffolding and source-specific planning through their CLIs."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ADAPTER = Path(__file__).resolve().parents[1]/'skills/content-production/youtube-remotion-clips'


class ProductionHelpers(unittest.TestCase):
    def test_missing_cache_scaffolds_offline_and_preserves_edits(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            workspace = base/'production'
            command = [sys.executable, str(ADAPTER/'scripts/bootstrap_project.py'),
                       '--workspace', str(workspace), '--cache-root', str(base/'empty-cache')]
            first = subprocess.run(command, check=True, capture_output=True, text=True)
            state = json.loads(first.stdout)
            self.assertFalse(state['privateSoundReused'])
            self.assertFalse(state['runtimeLinked'])
            self.assertEqual(state['networkRequests'], 0)
            self.assertTrue((workspace/'remotion/public/kitchen.png').is_file())
            renderer = workspace/'remotion/src/index.jsx'
            renderer.write_text('creator edited this renderer\n')
            subprocess.run(command, check=True, capture_output=True)
            self.assertEqual(renderer.read_text(), 'creator edited this renderer\n')
            required = subprocess.run(command+['--sound','required'], capture_output=True)
            self.assertNotEqual(required.returncode, 0)
            self.assertIn(b'Private swipe cache is missing', required.stderr)

    def test_visual_plan_accepts_new_ids_and_rejects_invalid_ranges_without_mutation(self):
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            public = workspace/'remotion/public'
            public.mkdir(parents=True)
            (public/'topic.png').write_bytes(b'fixture: existence check only')
            (workspace/'remotion/style.json').write_text(json.dumps({'canvas':{'fps':30}}))
            metadata = workspace/'remotion/clips.json'
            metadata.write_text(json.dumps([{'id':'new-interview', 'duration':20, 'color':'#a9d5ff'}]))
            plan = workspace/'visual-plan.json'
            entries = [{'id':'new-interview','cutaways':[{'at':3,'duration':5,'layout':'full','image':'topic.png'}]}]
            plan.write_text(json.dumps(entries))
            command = [sys.executable, str(ADAPTER/'scripts/plan_visual_revision.py'),'--plan',str(plan)]
            subprocess.run(command, cwd=workspace, check=True, capture_output=True)
            current = json.loads(metadata.read_text())[0]
            self.assertEqual(current['cutaways'][0]['duration'], 5)
            self.assertEqual(current['splitMedia'], 'new-interview-split.mp4')
            approved = metadata.read_bytes()
            entries[0]['cutaways'][0]['duration'] = 25
            plan.write_text(json.dumps(entries))
            result = subprocess.run(command, cwd=workspace, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(metadata.read_bytes(), approved)


if __name__ == '__main__':
    unittest.main()
