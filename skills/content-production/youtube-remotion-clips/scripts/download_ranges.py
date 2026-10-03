"""Download a manifest representation in checked byte ranges, with resume."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import time
import urllib.parse
import xml.etree.ElementTree as ET
import requests


def main():
    p = argparse.ArgumentParser()
    p.add_argument("manifest")
    p.add_argument("base_url")
    p.add_argument("itag")
    p.add_argument("output")
    p.add_argument("--workers", type=int, default=4)
    args = p.parse_args()
    ns = {"m": "urn:mpeg:dash:schema:mpd:2011"}
    tree = ET.parse(args.manifest)
    rep = next(e for e in tree.findall(".//m:Representation", ns) if e.attrib["id"] == args.itag)
    url = urllib.parse.urljoin(args.base_url, rep.find("m:BaseURL", ns).text)
    size = int(urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)["clen"][0])
    chunk = 1024 * 1024
    output = Path(args.output)
    parts = output.with_suffix(output.suffix + ".parts")
    parts.mkdir(parents=True, exist_ok=True)

    def get(index):
        start = index * chunk
        end = min(size, start + chunk) - 1
        dest = parts / f"{index:06}"
        if dest.exists() and dest.stat().st_size == end - start + 1:
            return
        for attempt in range(4):
            try:
                response = requests.get(url, headers={"Range": f"bytes={start}-{end}"}, timeout=45)
                response.raise_for_status()
                if response.status_code != 206 or len(response.content) != end - start + 1:
                    raise ValueError("Server did not return the requested byte range")
                dest.write_bytes(response.content)
                return
            except (requests.RequestException, ValueError):
                if attempt == 3:
                    raise
                time.sleep(1 + attempt)

    count = (size + chunk - 1) // chunk
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for done, _ in enumerate(pool.map(get, range(count)), 1):
            if done % 10 == 0 or done == count:
                print(f"{args.itag}: {done}/{count} MiB chunks", flush=True)
    temp = output.with_suffix(output.suffix + ".assembling")
    with temp.open("wb") as stream:
        for i in range(count):
            stream.write((parts / f"{i:06}").read_bytes())
    if temp.stat().st_size != size:
        raise ValueError("Final size mismatch")
    temp.replace(output)
    print(f"Saved {output}: {size} bytes", flush=True)


if __name__ == "__main__":
    main()
