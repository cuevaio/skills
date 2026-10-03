"""Resume a direct media representation using checked, atomic byte ranges."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
import requests


def download(url, output, *, cookies=None, resource_key=None, workers=4, timeout=20):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, headers={'Range':'bytes=0-0'}, cookies=cookies,
                      timeout=timeout, stream=True) as response:
        response.raise_for_status()
        match = re.fullmatch(r'bytes 0-0/(\d+)', response.headers.get('Content-Range',''))
        if response.status_code != 206 or not match or next(response.iter_content(1),b'') == b'':
            raise ValueError('Server does not support checked byte ranges')
        size = int(match[1])
    chunk_size = 1024*1024
    parts = output.with_suffix(output.suffix+'.parts')
    parts.mkdir(exist_ok=True)
    identity = dict(resource=resource_key or hashlib.sha256(url.encode()).hexdigest(), size=size)
    metadata = parts/'identity.json'
    if metadata.exists() and json.loads(metadata.read_text()) != identity:
        raise ValueError('Partial download belongs to a different representation or size')
    metadata.write_text(json.dumps(identity)+'\n')

    def get(index):
        start = index*chunk_size
        end = min(size,start+chunk_size)-1
        destination = parts/f'{index:06}'
        if destination.is_file() and destination.stat().st_size == end-start+1:
            return
        for attempt in range(3):
            try:
                response = requests.get(url, headers={'Range':f'bytes={start}-{end}'},
                                        cookies=cookies, timeout=timeout)
                response.raise_for_status()
                expected_range = f'bytes {start}-{end}/{size}'
                if (response.status_code != 206 or response.headers.get('Content-Range') != expected_range
                        or len(response.content) != end-start+1):
                    raise ValueError('Server returned a different byte range')
                temporary = destination.with_suffix('.partial')
                temporary.write_bytes(response.content)
                temporary.replace(destination)
                return
            except (requests.RequestException, ValueError):
                if attempt == 2:
                    raise

    count = (size+chunk_size-1)//chunk_size
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(get, range(count)))
    temporary = output.with_suffix(output.suffix+'.assembling')
    with temporary.open('wb') as stream:
        for index in range(count):
            with (parts/f'{index:06}').open('rb') as part:
                while block := part.read(chunk_size):
                    stream.write(block)
    if temporary.stat().st_size != size:
        raise ValueError('Final media size mismatch')
    temporary.replace(output)
    return size


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest')
    parser.add_argument('base_url')
    parser.add_argument('representation')
    parser.add_argument('output')
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    ns = {'m':'urn:mpeg:dash:schema:mpd:2011'}
    root = ET.parse(args.manifest)
    representation = next(e for e in root.findall('.//m:Representation',ns)
                          if e.attrib.get('id') == args.representation)
    base = representation.find('m:BaseURL',ns)
    if base is None or not base.text:
        raise ValueError('Representation has no direct BaseURL; use yt-dlp for segmented DASH')
    size = download(urljoin(args.base_url,base.text),args.output,workers=args.workers)
    print(json.dumps(dict(output=args.output,bytes=size)))


if __name__ == '__main__':
    main()
