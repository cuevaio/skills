"""Exercise real media acquisition, reuse, fallback, and checked range resumption."""
import argparse
from contextlib import contextmanager
import json
import importlib.util
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import imageio_ffmpeg

SCRIPTS = Path(__file__).resolve().parents[1]/'skills/content-production/youtube-remotion-clips/scripts'
sys.path.insert(0,str(SCRIPTS))
import download_source as cli
import download_ranges


@contextmanager
def serving(handler):
    server = ThreadingHTTPServer(('127.0.0.1',0),handler)
    thread = threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}'
    finally:
        server.shutdown();server.server_close();thread.join()


class Acquisition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.fixture = Path(cls.temp.name)/'recording.mp4'
        cls.ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        subprocess.run([cls.ffmpeg,'-v','error','-f','lavfi','-i','color=c=blue:s=320x180:r=30',
                        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','1',
                        '-c:v','libx264','-c:a','aac','-y',str(cls.fixture)],check=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def args(self,source,workspace,**values):
        defaults = dict(source=str(source),workspace=Path(workspace),ffmpeg=self.ffmpeg,
                        audio_only=False,max_height=1080,max_mirrors=3,max_backends=3,
                        timeout=3,mirror=None,watch_html=None,cookies=None,
                        instances_url='https://api.invidious.io/instances.json')
        defaults.update(values)
        return argparse.Namespace(**defaults)

    def invoke(self,source,workspace,*extra):
        return subprocess.run([sys.executable,str(SCRIPTS/'download_source.py'),str(source),
                               '--workspace',str(workspace),'--ffmpeg',self.ffmpeg,*extra],
                              text=True,capture_output=True)

    def test_real_cli_local_audio_then_video_and_verified_rerun(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(self.invoke(self.fixture,temp,'--audio-only').returncode,0)
            self.assertFalse((Path(temp)/'source/video.mp4').exists())
            result = self.invoke(self.fixture,temp)
            self.assertEqual(result.returncode,0,result.stderr)
            root = Path(temp)/'source'
            self.assertTrue(cli.inspect_media(root/'video.mp4')['video'])
            self.assertTrue(cli.inspect_media(root/'audio.mka')['audio'])
            before = (root/'video.mp4').stat().st_mtime_ns
            result = self.invoke(self.fixture,temp)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('verified-media-reused',result.stdout)
            self.assertEqual((root/'video.mp4').stat().st_mtime_ns,before)
            report = json.loads((root/'acquisition.json').read_text())
            self.assertEqual(report['status'],'ready')
            self.assertEqual(report['video']['sha256'],cli.sha256(root/'video.mp4'))
            provenance = json.loads((Path(temp)/'provenance.json').read_text())
            self.assertEqual(provenance['sourceAcquisition']['audio']['file'],'audio.mka')
            other = Path(temp)/'other.mp4';other.write_bytes(self.fixture.read_bytes())
            self.assertEqual(self.invoke(other,temp).returncode,1)
            self.assertEqual((root/'video.mp4').stat().st_mtime_ns,before)

    @unittest.skipUnless(importlib.util.find_spec('yt_dlp'), 'yt-dlp unavailable in this environment')
    def test_real_ytdlp_direct_url_with_unknown_resolution(self):
        class Handler(SimpleHTTPRequestHandler):
            def log_message(self,*_):
                pass
        with serving(partial(Handler,directory=self.temp.name)) as origin,tempfile.TemporaryDirectory() as temp:
            result=self.invoke(origin+'/recording.mp4',temp,'--max-mirrors','0')
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertTrue(cli.inspect_media(Path(temp)/'source/video.mp4')['video'])

    def test_blocked_direct_uses_advertised_route_and_session_then_decodes(self):
        audio = Path(self.temp.name)/'audio.m4a'
        video = Path(self.temp.name)/'video.mp4'
        subprocess.run([self.ffmpeg,'-v','error','-y','-i',str(self.fixture),'-vn','-c:a','copy',str(audio)],check=True)
        subprocess.run([self.ffmpeg,'-v','error','-y','-i',str(self.fixture),'-an','-c:v','copy',str(video)],check=True)
        streams={'/audio':audio.read_bytes(),'/video':video.read_bytes()}
        seen=[]
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                seen.append(self.path)
                if self.path.startswith('/watch?'):
                    self.send_response(200);self.send_header('Set-Cookie','playback=yes; Path=/');self.end_headers()
                    self.wfile.write(b'<source src="/current-manifest?signature=issued">')
                elif self.path=='/current-manifest?signature=issued':
                    self.send_response(200);self.end_headers()
                    self.wfile.write(b'<MPD xmlns="urn:mpeg:dash:schema:mpd:2011"><Period><AdaptationSet mimeType="audio/mp4"><Representation id="a" bandwidth="128000"><BaseURL>/audio</BaseURL></Representation></AdaptationSet><AdaptationSet mimeType="video/mp4"><Representation id="v" height="180" bandwidth="100000"><BaseURL>/video</BaseURL></Representation></AdaptationSet></Period></MPD>')
                elif self.path in streams and 'playback=yes' in self.headers.get('Cookie',''):
                    payload=streams[self.path]
                    start,end=map(int,self.headers['Range'].removeprefix('bytes=').split('-'))
                    self.send_response(206);self.send_header('Content-Range',f'bytes {start}-{end}/{len(payload)}')
                    self.send_header('Content-Type','video/mp4');self.end_headers();self.wfile.write(payload[start:end+1])
                else:
                    self.send_response(403);self.end_headers()
            def log_message(self,*_):
                pass
        with serving(Handler) as origin,tempfile.TemporaryDirectory() as temp:
            downloader=cli.Downloader(self.args('https://youtube.com/watch?v=abcdefghijk',temp,mirror=[origin]))
            with patch.object(downloader,'ytdlp',side_effect=cli.AcquisitionError('access-blocked')):
                self.assertEqual(downloader.run(),0)
            self.assertTrue(cli.inspect_media(Path(temp)/'source/video.mp4')['audio'])
            self.assertEqual(downloader.report['attempts'][-1]['result'],'verified')
            self.assertIn('/current-manifest?signature=issued',seen)
            self.assertFalse(any('/companion/' in path for path in seen))

    def test_setup_error_does_not_try_mirrors(self):
        with tempfile.TemporaryDirectory() as temp:
            downloader=cli.Downloader(self.args('https://youtube.com/watch?v=abcdefghijk',temp))
            with patch.object(downloader,'ytdlp',side_effect=cli.SetupError('setup-error')),patch.object(downloader,'mirrors') as mirrors:
                self.assertEqual(downloader.run(),1)
                mirrors.assert_not_called()
            self.assertEqual(json.loads((Path(temp)/'source/acquisition.json').read_text())['status'],'error')

    def test_blocked_source_has_actionable_report(self):
        with tempfile.TemporaryDirectory() as temp:
            downloader=cli.Downloader(self.args('https://youtube.com/watch?v=abcdefghijk',temp,max_mirrors=0))
            with patch.object(downloader,'ytdlp',side_effect=cli.AcquisitionError('access-blocked')):
                self.assertEqual(downloader.run(),2)
            report=json.loads((Path(temp)/'source/acquisition.json').read_text())
            self.assertEqual(report['status'],'blocked')
            self.assertIn('accessible source',report['nextAction'])
            self.assertFalse((Path(temp)/'source/video.mp4').exists())

    def test_range_resume_reuses_checked_parts_and_rejects_wrong_response(self):
        payload=b'a'*(1024*1024)+b'b'*4096
        seen=[];wrong=[False]
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                start,end=map(int,self.headers['Range'].removeprefix('bytes=').split('-'))
                seen.append((start,end))
                self.send_response(206)
                self.send_header('Content-Range',f'bytes {start}-{end if not wrong[0] or end==0 else end+1}/{len(payload)}')
                self.end_headers();self.wfile.write(payload[start:end+1])
            def log_message(self,*_):
                pass
        with serving(Handler) as origin,tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'track'
            download_ranges.download(origin,output)
            self.assertEqual(output.read_bytes(),payload)
            output.unlink();seen.clear()
            download_ranges.download(origin,output)
            self.assertEqual(seen,[(0,0)])
            wrong[0]=True
            with self.assertRaises(ValueError):
                download_ranges.download(origin,Path(temp)/'bad')
            self.assertFalse((Path(temp)/'bad').exists())


if __name__=='__main__':
    unittest.main()
