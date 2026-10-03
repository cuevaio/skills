"""Exercise portable scaffolding and source-specific planning through their CLIs."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ADAPTER = Path(__file__).resolve().parents[1]/'skills/content-production/youtube-remotion-clips'


class ProductionHelpers(unittest.TestCase):
    def test_reviewed_captions_retain_zero_duration_words_and_join_model_tokens(self):
        with tempfile.TemporaryDirectory() as temp:
            workspace=Path(temp)
            (workspace/'transcript/clip').mkdir(parents=True)
            (workspace/'remotion/public').mkdir(parents=True)
            (workspace/'clips').mkdir()
            (workspace/'remotion/public/clip-source.mp4').write_bytes(b'existing prepared media')
            (workspace/'edit-plan.json').write_text(json.dumps([dict(id='clip',start=100,end=102)]))
            raw=json.dumps(dict(segments=[dict(words=[dict(word='wrong',start=0,end=1)])]))
            (workspace/'transcript/transcript.json').write_text(raw)
            (workspace/'transcript/clip/transcript.json').write_text(raw)
            words=[dict(word=word,start=start,end=end) for word,start,end in
                   [('and',0,0),(' hello',0,.3),(' GPT',.3,.5),('-5',.5,.7),(' 5',.7,.9),('.0',.9,1.1),(' okay',1.1,1.5),(' -20',1.5,1.8)]]
            (workspace/'transcript/clip/reviewed.json').write_text(json.dumps(dict(segments=[dict(words=words)])))
            subprocess.run([sys.executable,str(ADAPTER/'scripts/prepare_clips.py')],cwd=workspace,check=True,capture_output=True)
            captions=json.loads((workspace/'remotion/clips.json').read_text())[0]['captions']
            actual=[word for caption in captions for word in caption['words']]
            self.assertEqual([word['word'].strip() for word in actual],['and','hello','GPT-5','5.0','okay','-20'])
            self.assertTrue(all(0<=word['start']<word['end']<=2 for word in actual))
            self.assertLessEqual(actual[0]['end'],actual[1]['start'])
            self.assertEqual((workspace/'transcript/clip/transcript.json').read_text(),raw)
            self.assertIn('GPT-5 5.0',(workspace/'clips/clip.srt').read_text())

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
            self.assertTrue((workspace/'image-prompts.md').is_file())
            self.assertTrue((workspace/'remotion/public/SpaceGrotesk-Variable.ttf').is_file())
            self.assertFalse(any(p.suffix.lower() in {'.png','.jpg','.webp'} for p in workspace.rglob('*')))
            prompts = workspace/'image-prompts.md'
            prompts.write_text('creator adapted the prompts\n')
            renderer = workspace/'remotion/src/index.jsx'
            renderer.write_text('creator edited this renderer\n')
            subprocess.run(command, check=True, capture_output=True)
            self.assertEqual(renderer.read_text(), 'creator edited this renderer\n')
            self.assertEqual(prompts.read_text(), 'creator adapted the prompts\n')
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
