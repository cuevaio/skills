"""Check destination payloads through the scheduler's plan interface."""
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/content-production/buffer-scheduling/scripts/schedule.py'
spec = importlib.util.spec_from_file_location('buffer_schedule', SCRIPT)
scheduler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scheduler)


class BufferSchedule(unittest.TestCase):
    def validate(self, posts):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            master = root / 'clip.mp4'
            master.write_bytes(b'local master fixture')
            for post in posts:
                post.update(mode='addToQueue', clip={'path': str(master)})
            plan = root / 'plan.json'
            plan.write_text(json.dumps({'organizationId': 'organization', 'posts': posts}))
            ledger = root / 'ledger.jsonl'
            calls = []
            def dry_run(args, payload):
                self.assertIn('--dry-run', args)
                calls.append(payload)
                return {}
            with patch.object(sys, 'argv', ['schedule.py', '--plan', str(plan), '--ledger', str(ledger)]), patch.object(scheduler, 'cli', side_effect=dry_run), contextlib.redirect_stdout(io.StringIO()) as output:
                scheduler.main()
            self.assertFalse(ledger.exists())
            self.assertEqual(json.loads(output.getvalue())['created'], 0)
            return calls

    def test_six_services_and_second_account_keep_distinct_destinations(self):
        services = ['instagram', 'linkedin', 'twitter', 'youtube', 'threads', 'tiktok', 'instagram']
        posts = [dict(key=f'clip:{i}', channelId=f'account-{i}', service=service, text='the useful idea') for i, service in enumerate(services)]
        posts[3]['metadata'] = {'youtube': {'title': 'the useful idea', 'categoryId': '28', 'privacy': 'public'}}
        posts[5].update(metadata={'tiktok': {'isAiGenerated': True}}, videoMetadata={'thumbnailOffset': 0}, schedulingType='notification')
        payloads = self.validate(posts)
        self.assertEqual([p['channelId'] for p in payloads], [f'account-{i}' for i in range(7)])
        self.assertEqual(payloads[0]['metadata'], {'instagram': {'type': 'reel', 'shouldShareToFeed': True}})
        self.assertEqual(payloads[3]['metadata'], {'youtube': {'title': 'the useful idea', 'categoryId': '28', 'privacy': 'public'}})
        self.assertEqual(payloads[5]['metadata'], {'tiktok': {'isAiGenerated': True}})
        self.assertEqual(payloads[5]['schedulingType'], 'notification')
        self.assertEqual(payloads[5]['assets'][0]['video']['metadata'], {'thumbnailOffset': 0})
        self.assertTrue(all('dueAt' not in p for p in payloads))

    def test_youtube_incomplete_package_is_rejected_before_creation(self):
        for missing in ['title', 'categoryId', 'privacy']:
            youtube = {'title': 'the useful idea', 'categoryId': '28', 'privacy': 'public'}
            del youtube[missing]
            with self.subTest(missing=missing), self.assertRaisesRegex(RuntimeError, 'YouTube requires'):
                self.validate([dict(key='clip:youtube', channelId='youtube-account', service='youtube', text='description', metadata={'youtube': youtube})])

    def test_instagram_explicit_settings_are_preserved(self):
        payloads = self.validate([dict(key='clip:instagram', channelId='instagram-account', service='instagram', text='caption', metadata={'instagram': {'type': 'reel', 'shouldShareToFeed': False}}, videoMetadata={'thumbnailOffset': 2})])
        self.assertFalse(payloads[0]['metadata']['instagram']['shouldShareToFeed'])
        self.assertEqual(payloads[0]['assets'][0]['video']['metadata'], {'thumbnailOffset': 2})


if __name__ == '__main__':
    unittest.main()
