"""Read a mirror player through an isolated browser and return its own session cookies."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import uuid
from urllib.parse import urljoin
from discover_download import WatchPage


class BrowserError(Exception):
    pass


def capture(watch_url, directory, timeout=30, executable=None, max_backends=8):
    executable=executable or shutil.which('agent-browser')
    if not executable:
        raise BrowserError('agent-browser is not installed')
    directory=Path(directory)
    directory.mkdir(parents=True,exist_ok=True)
    session='clip-source-'+uuid.uuid4().hex[:12]
    common=[executable,'--session',session]
    launch=['--args','--no-sandbox'] if sys.platform.startswith('linux') else []

    def run(args):
        try:
            result=subprocess.run(common+args,capture_output=True,text=True,timeout=timeout)
        except (OSError,subprocess.TimeoutExpired) as exc:
            raise BrowserError(type(exc).__name__) from exc
        if result.returncode and args==['get','html','body'] and 'Element not found' in result.stderr:
            return ''
        if result.returncode:
            log=directory/'browser-error.log'
            log.write_text(result.stderr,encoding='utf-8');log.chmod(0o600)
            raise BrowserError('Browser command failed; see browser-error.log')
        return result.stdout

    try:
        # Use the installed browser's version rather than a hardcoded, stale Chrome version.
        run(launch+['open','about:blank'])
        agent=json.loads(run(['eval','navigator.userAgent']).strip()).replace('HeadlessChrome/','Chrome/')
        run(['close'])
        run(launch+['--user-agent',agent,'open',watch_url])
        deadline=time.monotonic()+timeout
        refreshed=False
        while True:
            html=run(['get','html','body'])
            parser=WatchPage();parser.feed(html)
            if parser.sources or parser.backends:
                break
            if 'has already been instantiated' in html and not refreshed:
                # The challenge occasionally reloads while its WASM module is still live.
                # A fresh navigation resets that page runtime without losing session cookies.
                refreshed=True
                run(['open',watch_url])
                continue
            if 'access denied' in html.lower() or time.monotonic()>=deadline:
                path=directory/'browser-watch.html'
                path.write_text(html,encoding='utf-8');path.chmod(0o600)
                raise BrowserError('Browser did not expose a playback source or advertised backend')
            time.sleep(.5)
        path=directory/'browser-watch.html'
        path.write_text(html,encoding='utf-8');path.chmod(0o600)
        resolved=run(['get','url']).strip()
        pages={}
        for index,href in enumerate(parser.backends[:max_backends]):
            url=urljoin(resolved,href)
            script='(async()=>{const r=await fetch('+json.dumps(url)+');return JSON.stringify({url:r.url,status:r.status,html:await r.text()})})()'
            try:
                result=json.loads(run(['eval',script]))
                if isinstance(result,str):result=json.loads(result)
            except (BrowserError,ValueError):
                pages[url]=dict(html='',url=url,status=599)
                continue
            saved_page=directory/f'browser-backend-{index}.html'
            saved_page.write_text(result['html'],encoding='utf-8');saved_page.chmod(0o600)
            pages[url]=dict(html=result['html'],url=result['url'],status=result['status'])
        cookies=json.loads(run(['cookies','--json']))
        if not cookies.get('success'):
            raise BrowserError('Could not retrieve this browser session cookies')
        values=cookies['data']['cookies']
        saved=directory/'browser-cookies.json'
        saved.write_text(json.dumps(values,indent=2)+'\n',encoding='utf-8');saved.chmod(0o600)
        return dict(html=path,url=resolved,cookies=values,userAgent=agent,pages=pages)
    finally:
        try:
            run(['close'])
        except BrowserError:
            pass
