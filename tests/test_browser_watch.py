"""Check browser session handoff when a challenge reloads before the player appears."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/content-production/youtube-remotion-clips/scripts'))
import browser_watch


class BrowserHandoff(unittest.TestCase):
    def test_transient_challenge_and_advertised_backend_keep_own_cookies(self):
        calls=[]
        bodies=iter(['module[runtime] has already been instantiated',
                     '<a href="/switchbackend?companion_id=4">backend</a>'])
        def command(args,**kwargs):
            calls.append(args)
            tail=args[3:]
            if tail==['eval','navigator.userAgent']:
                output=json.dumps('Mozilla HeadlessChrome/150.0.0.0')
            elif tail==['get','html','body']:
                output=next(bodies)
            elif tail==['get','url']:
                output='https://mirror.example/watch?v=abcdefghijk'
            elif tail[0]=='eval':
                output=json.dumps(json.dumps(dict(url='https://mirror.example/watch?v=abcdefghijk',status=200,html='<source src="https://media.example/signed.mpd?fresh=1">')))
            elif tail==['cookies','--json']:
                output=json.dumps(dict(success=True,data=dict(cookies=[dict(name='anonymous',value='own',domain='mirror.example',path='/')])))
            else:
                output=''
            return subprocess.CompletedProcess(args,0,output,'')
        with tempfile.TemporaryDirectory() as temp,patch.object(browser_watch.subprocess,'run',side_effect=command):
            result=browser_watch.capture('https://mirror.example/watch?v=abcdefghijk',temp,executable='agent-browser')
            self.assertEqual(result['userAgent'],'Mozilla Chrome/150.0.0.0')
            self.assertEqual(result['cookies'][0]['value'],'own')
            self.assertIn('https://mirror.example/switchbackend?companion_id=4',result['pages'])
            self.assertTrue(result['html'].exists())
            self.assertEqual(len({args[2] for args in calls}),1)
            self.assertEqual(calls[-1][3:],['close'])
            self.assertTrue(any(args[3:]==['open','https://mirror.example/watch?v=abcdefghijk'] for args in calls))


if __name__=='__main__':
    unittest.main()
