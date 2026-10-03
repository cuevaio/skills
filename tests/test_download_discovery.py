"""Verify discovery follows advertised URLs and rejects false-success responses."""
import importlib.util
import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

HELPER = Path(__file__).resolve().parents[1]/'skills/content-production/youtube-remotion-clips/scripts/discover_download.py'
spec = importlib.util.spec_from_file_location('download_discovery', HELPER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DownloadDiscovery(unittest.TestCase):
    def test_discovers_signed_player_route_and_uses_its_relative_streams(self):
        seen = []

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                seen.append(self.path)
                parsed = urlsplit(self.path)
                query = parse_qs(parsed.query)
                if parsed.path == '/watch':
                    self.send_response(200)
                    self.send_header('Set-Cookie', 'playback=issued; Path=/')
                    self.end_headers()
                    self.wfile.write(b'<source src="/manifest?route=stale"><a href="/switchbackend?companion_id=7">another backend</a>')
                elif parsed.path == '/switchbackend':
                    self.send_response(200); self.end_headers()
                    self.wfile.write(b'<source src="/manifest?route=fresh&amp;local=true">')
                elif parsed.path == '/manifest' and query.get('route') == ['fresh'] and 'playback=issued' in self.headers.get('Cookie',''):
                    self.send_response(200); self.end_headers()
                    self.wfile.write(b'<MPD xmlns="urn:mpeg:dash:schema:mpd:2011"><Period><AdaptationSet mimeType="audio/mp4"><Representation id="current-audio"><BaseURL>/stream?clen=2048&amp;route=fresh</BaseURL></Representation></AdaptationSet><AdaptationSet mimeType="video/mp4"><Representation id="current-video"><BaseURL>/stream?clen=2048&amp;route=fresh</BaseURL></Representation></AdaptationSet></Period></MPD>')
                elif parsed.path == '/stream' and self.headers.get('Range') == 'bytes=0-1023':
                    self.send_response(206); self.send_header('Content-Type','video/mp4'); self.end_headers()
                    self.wfile.write(b'fixture media bytes'.ljust(1024,b'0'))
                else:
                    self.send_response(400); self.end_headers()
                    self.wfile.write(b'Invalid route')

            def log_message(self, *_):
                pass

        server = ThreadingHTTPServer(('127.0.0.1',0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        try:
            with tempfile.TemporaryDirectory() as temp:
                url = f'http://127.0.0.1:{server.server_port}/watch'
                report = module.discover(url, Path(temp)/'routes.json')
                self.assertEqual(len(report['routes']),1)
                route = report['routes'][0]
                self.assertIn('route=fresh&local=true',route['manifestUrl'])
                self.assertEqual({p['kind'] for p in route['probes']},{'audio','video'})
                self.assertTrue(all(p['passed'] for p in route['probes']))
                self.assertIn('/switchbackend?companion_id=7',seen)
                self.assertTrue(Path(route['manifest']).is_file())
                self.assertEqual(report['attempts'][0]['status'],400)
        finally:
            server.shutdown(); server.server_close(); thread.join()

    def test_watch_challenges_record_status_and_reason(self):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(418 if self.path=='/denied' else 200);self.end_headers()
                self.wfile.write(b"<html><title>Making sure you're not a bot!</title></html>")
            def log_message(self,*_):
                pass
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            with tempfile.TemporaryDirectory() as temp:
                for path,status in [('/denied',418),('/challenge',200)]:
                    report=module.discover(f'http://127.0.0.1:{server.server_port}'+path,Path(temp)/'routes.json')
                    self.assertFalse(report['routes'])
                    self.assertEqual(report['attempts'][0]['status'],status)
                    self.assertEqual(report['attempts'][0]['result'],'browser-challenge-or-access-denied')
        finally:
            server.shutdown();server.server_close();thread.join()

    def test_http_200_html_is_not_a_verified_manifest(self):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200); self.end_headers()
                if self.path == '/watch':
                    self.wfile.write(b'<source src="/fake-manifest">')
                else:
                    self.wfile.write(b'<html><body>access blocked</body></html>')

            def log_message(self, *_):
                pass

        server = ThreadingHTTPServer(('127.0.0.1',0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        try:
            with tempfile.TemporaryDirectory() as temp:
                output = Path(temp)/'routes.json'
                report = module.discover(f'http://127.0.0.1:{server.server_port}/watch', output)
                self.assertFalse(report['routes'])
                self.assertEqual(json.loads(output.read_text())['attempts'][0]['error'],'ValueError')
        finally:
            server.shutdown(); server.server_close(); thread.join()


if __name__ == '__main__':
    unittest.main()
