"""Discover current public mirror sources and validate DASH routes without guessing endpoints."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET
import requests


class WatchPage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []
        self.backends = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'source' and attrs.get('src'):
            self.sources.append(attrs['src'])
        href = attrs.get('href', '')
        if tag == 'a' and 'switchbackend' in urlsplit(href).path:
            self.backends.append(href)


def representations(root, base):
    found = []

    def walk(node, current, mime):
        mime = node.attrib.get('mimeType', mime)
        local = next((child.text for child in node if child.tag.split('}')[-1] == 'BaseURL'), None)
        if local:
            current = urljoin(current, local.strip())
        if node.tag.split('}')[-1] == 'Representation' and local:
            found.append(dict(id=node.attrib.get('id'), mimeType=mime, url=current))
        for child in node:
            walk(child, current, mime)

    walk(root, base, '')
    return found


def discover(watch_url, output, html_path=None, max_backends=3):
    output.parent.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    attempts, valid, visited = [], [], set()
    pages = [watch_url]
    for index in range(max_backends+1):
        if index >= len(pages):
            break
        page_url = pages[index]
        try:
            if index == 0 and html_path:
                html, resolved = html_path.read_text(), page_url
            else:
                page = session.get(page_url, timeout=15)
                page.raise_for_status()
                html, resolved = page.text, page.url
            parser = WatchPage()
            parser.feed(html)
            if index == 0:
                for href in parser.backends:
                    candidate = urljoin(resolved, href)
                    if candidate not in pages:
                        pages.append(candidate)
            if not parser.sources:
                attempts.append(dict(stage='watch', status='no source element'))
            for src in parser.sources:
                url = urljoin(resolved, src)
                if url in visited:
                    continue
                visited.add(url)
                try:
                    response = session.get(url, timeout=15)
                    response.raise_for_status()
                    root = ET.fromstring(response.content)
                    if root.tag.split('}')[-1] != 'MPD':
                        raise ValueError('Response is not a DASH manifest')
                    streams = representations(root, response.url)
                    if not streams:
                        raise ValueError('DASH contains no direct representation URLs')
                    probes = []
                    for kind in ['audio/', 'video/']:
                        stream = next((s for s in streams if s['mimeType'].startswith(kind)), None)
                        if not stream:
                            continue
                        with session.get(stream['url'], headers={'Range':'bytes=0-1023'},
                                         timeout=15, stream=True) as media:
                            content_type = media.headers.get('Content-Type','').lower()
                            body = next(media.iter_content(1024), b'')
                            success = (media.status_code == 206 and len(body) == 1024
                                       and 'text/html' not in content_type
                                       and not body.lstrip().lower().startswith((b'<!doctype',b'<html')))
                            probes.append(dict(id=stream['id'], kind=kind[:-1],
                                               status=media.status_code, bytes=len(body), passed=success))
                    if not probes or not all(p['passed'] for p in probes):
                        raise ValueError('Media range probe failed')
                    path = output.parent/f'download-manifest-{len(valid)}.mpd'
                    path.write_bytes(response.content)
                    valid.append(dict(manifestUrl=response.url, manifest=str(path),
                                      streams=streams, probes=probes))
                except (requests.RequestException, ET.ParseError, ValueError) as exc:
                    attempts.append(dict(stage='manifest', error=type(exc).__name__,
                                         status=getattr(getattr(exc,'response',None),'status_code',None)))
        except (requests.RequestException, OSError) as exc:
            attempts.append(dict(stage='watch', error=type(exc).__name__,
                                 status=getattr(getattr(exc,'response',None),'status_code',None)))
        if valid:
            break
    # Signed URLs stay in this private production file; stdout prints no tokens.
    report = dict(routes=valid, attempts=attempts)
    output.write_text(json.dumps(report, indent=2)+'\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('watch_url', help='Current public mirror watch URL')
    parser.add_argument('--html', type=Path, help='HTML saved from a working browser; use its actual URL above')
    parser.add_argument('--output', type=Path, default=Path('source/download-routes.json'))
    parser.add_argument('--max-backends', type=int, default=3)
    args = parser.parse_args()
    if not 0 <= args.max_backends <= 8:
        parser.error('--max-backends must be between 0 and 8')
    report = discover(args.watch_url, args.output, args.html, args.max_backends)
    print(json.dumps(dict(verifiedRoutes=len(report['routes']), attempts=len(report['attempts']),
                          report=str(args.output))))
    raise SystemExit(0 if report['routes'] else 2)


if __name__ == '__main__':
    main()
