"""Acquire and validate a recording with one reproducible, resumable command."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

# The installed skill directory is shared; keep runtime bytecode out of its bundle.
sys.dont_write_bytecode = True
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit
import av
import imageio_ffmpeg
import requests
from discover_download import discover, select_audio
from browser_watch import capture, BrowserError
from download_ranges import download as download_ranges


class AcquisitionError(Exception):
    pass


class SetupError(AcquisitionError):
    pass


def write_json(path, data):
    temporary = path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(data,indent=2)+'\n')
    temporary.chmod(0o600)
    temporary.replace(path)


def sha256(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        while block := stream.read(1024*1024):
            result.update(block)
    return result.hexdigest()


def inspect_media(path):
    with av.open(str(path)) as media:
        return dict(video=any(s.type=='video' for s in media.streams),
                    audio=any(s.type=='audio' for s in media.streams),
                    duration=media.duration/av.time_base if media.duration else None)


def identity(source):
    parsed = urlsplit(source)
    host = (parsed.hostname or '').lower()
    video_id = None
    if host == 'youtu.be':
        video_id = parsed.path.strip('/').split('/')[0]
    elif host in {'youtube.com','www.youtube.com','m.youtube.com','music.youtube.com'}:
        video_id = parse_qs(parsed.query).get('v',[None])[0]
        if not video_id and parsed.path.startswith(('/live/','/shorts/','/embed/')):
            video_id = parsed.path.split('/')[2]
    if video_id and re.fullmatch(r'[A-Za-z0-9_-]{11}',video_id):
        return 'youtube:'+video_id,video_id
    if parsed.scheme in {'http','https'}:
        return 'url:'+hashlib.sha256(source.encode()).hexdigest(),None
    path = Path(source).expanduser().resolve()
    if not path.is_file():
        raise AcquisitionError('Source is not a supported URL or an existing local file')
    return 'file:'+str(path)+':'+sha256(path),None


def classify(text):
    low = text.lower()
    if any(value in low for value in ['not a bot','login_required','http error 429','http error 403','sign in']):
        return 'access-blocked'
    if any(value in low for value in ['ffmpeg not found','no module named','unrecognized arguments','unsupported option']):
        return 'setup-error'
    if 'timed out' in low or 'timeout' in low:
        return 'network-timeout'
    return 'download-failed'


class Downloader:
    def __init__(self,args):
        self.args = args
        self.workspace = args.workspace.expanduser().resolve()
        self.root = self.workspace/'source'
        self.root.mkdir(parents=True,exist_ok=True)
        self.report_path = self.root/'acquisition.json'
        self.ffmpeg = args.ffmpeg or shutil.which('ffmpeg') or imageio_ffmpeg.get_ffmpeg_exe()
        self.key,self.video_id = identity(args.source)
        self.report = dict(sourceKey=self.key,source=args.source,status='running',attempts=[],audio=None,video=None)
        self.lock = self.root/'.acquisition.lock'

    def record(self,method,result,**details):
        self.report['attempts'].append(dict(method=method,result=result,**details))
        write_json(self.report_path,self.report)
        print(json.dumps(dict(stage=method,result=result)),flush=True)

    def command(self,argv,label):
        result = subprocess.run(argv,capture_output=True,text=True)
        log = self.root/(label+'.log')
        log.write_text(result.stdout+'\n'+result.stderr)
        log.chmod(0o600)
        if result.returncode:
            category = classify(result.stderr)
            self.record(label,category,log=log.name)
            raise (SetupError if category=='setup-error' else AcquisitionError)(category)

    def validated(self,kind):
        item = self.report.get(kind)
        if not item:
            return False
        path = self.root/item['file']
        return path.is_file() and sha256(path)==item['sha256']

    def validate(self,path,video=False):
        metadata = inspect_media(path)
        if not metadata['audio'] or (video and not metadata['video']):
            raise AcquisitionError('Saved source lacks required audio/video streams')
        self.command([self.ffmpeg,'-v','error','-xerror','-i',str(path),'-f','null','-'],
                     'validate-video' if video else 'validate-audio')
        return dict(file=path.name,bytes=path.stat().st_size,sha256=sha256(path),**metadata)

    def finalize(self,video_path=None,audio_path=None):
        if not self.validated('audio'):
            audio = self.root/'audio.mka'
            temporary = self.root/'audio.new.mka'
            self.command([self.ffmpeg,'-v','error','-y','-i',str(audio_path or video_path),
                          '-map','0:a:0','-vn','-c:a','copy',str(temporary)],'extract-audio')
            item = self.validate(temporary)
            temporary.replace(audio);item['file']=audio.name
            self.report['audio']=item
            write_json(self.report_path,self.report)
        if video_path and not self.args.audio_only:
            temporary = self.root/'video.new.mp4'
            command = [self.ffmpeg,'-v','error','-y','-i',str(video_path)]
            if audio_path:
                command += ['-i',str(audio_path),'-map','0:v:0','-map','1:a:0']
            else:
                command += ['-map','0:v:0','-map','0:a:0']
            self.command(command+['-c','copy','-movflags','+faststart',str(temporary)],'mux-video')
            item = self.validate(temporary,video=True)
            video = self.root/'video.mp4'
            temporary.replace(video);item['file']=video.name
            self.report['video']=item
        write_json(self.report_path,self.report)

    def ytdlp(self,url,template,format_selector):
        command = [sys.executable,'-m','yt_dlp','--no-playlist','--js-runtimes','node',
                   '--socket-timeout',str(self.args.timeout),'--retries','2','--extractor-retries','1',
                   '--fragment-retries','2','--ffmpeg-location',self.ffmpeg,'--no-progress',
                   '--no-simulate','--print','after_move:filepath','-f',format_selector,'-o',str(template)]
        if self.args.cookies:
            command += ['--cookies',str(self.args.cookies)]
        command += [url]
        result = subprocess.run(command,capture_output=True,text=True)
        label='yt-dlp-audio' if 'audio' in template.name else 'yt-dlp-video'
        log=self.root/(label+'.log');log.write_text(result.stdout+'\n'+result.stderr);log.chmod(0o600)
        if result.returncode:
            category=classify(result.stderr)
            self.record(label,category,log=log.name)
            raise (SetupError if category=='setup-error' else AcquisitionError)(category)
        for line in reversed(result.stdout.splitlines()):
            path=Path(line.strip())
            if path.is_file():
                return path
        raise AcquisitionError('yt-dlp returned no saved media path')

    def direct(self):
        parsed=urlsplit(self.args.source)
        if parsed.scheme not in {'https','http'}:
            self.finalize(video_path=Path(self.args.source).expanduser().resolve())
            self.record('local-source','verified')
            return
        if self.validated('audio'):
            raw_audio=self.root/self.report['audio']['file']
        else:
            raw_audio=self.ytdlp(self.args.source,self.root/'download-audio.%(ext)s',
                                 f'ba/b[height<=?{self.args.max_height}]')
            self.finalize(audio_path=raw_audio)
            self.record('direct-audio','verified')
        if self.args.audio_only:
            return
        if inspect_media(raw_audio)['video']:
            self.finalize(video_path=raw_audio)
        else:
            picture=self.ytdlp(self.args.source,self.root/'download-video.%(ext)s',
                               f'bv[height<=?{self.args.max_height}]/b[height<=?{self.args.max_height}]')
            self.finalize(video_path=picture,audio_path=raw_audio)
        self.record('direct-video','verified')

    def mirror_urls(self):
        if self.args.mirror:
            return self.args.mirror[:self.args.max_mirrors]
        response=requests.get(self.args.instances_url,timeout=self.args.timeout)
        response.raise_for_status()
        listing=response.json()
        candidates=[]
        skipped=[]
        for host,settings in listing:
            monitor=settings.get('monitor') or {}
            url=settings.get('uri','https://'+host)
            if (settings.get('type')!='https' or urlsplit(url).scheme!='https'
                    or not monitor or monitor.get('down') or monitor.get('enabled') is False):
                skipped.append(dict(host=host,reason='not a monitored available public HTTPS instance'))
                continue
            playback=(settings.get('stats') or {}).get('playback') or {}
            ratio=playback.get('ratio')
            # Prefer recent playback success, then unknown playback, then known failures.
            group=2 if ratio is not None and ratio>0 else (1 if ratio is None else 0)
            candidates.append((group,ratio or 0,monitor.get('uptime') or 0,url))
        candidates.sort(key=lambda item:(-item[0],-item[1],-item[2],item[3]))
        hosts=list(dict.fromkeys(item[3] for item in candidates))
        selected=hosts[:self.args.max_mirrors]
        write_json(self.root/'instance-selection.json',dict(selected=selected,eligible=hosts,skipped=skipped))
        return selected

    def mirrors(self):
        if not self.video_id or not self.args.max_mirrors:
            return False
        try:
            urls=self.mirror_urls()
        except (requests.RequestException,ValueError,TypeError) as exc:
            self.record('instance-list','unavailable',error=type(exc).__name__)
            return False
        for index,instance in enumerate(urls):
            parsed=urlsplit(instance)
            watch=(instance if parsed.path and parsed.path!='/' else
                   urlunsplit((parsed.scheme,parsed.netloc,'/watch',urlencode({'v':self.video_id,'local':'true'}),'')))
            session=requests.Session()
            try:
                routes=discover(watch,self.root/f'mirror-{index}/routes.json',
                                html_path=self.args.watch_html if index==0 else None,
                                max_backends=self.args.max_backends,session=session,timeout=self.args.timeout)
                if (not routes['routes'] and getattr(self.args,'browser','auto')!='off'
                        and any(a.get('result') in {'browser-challenge-or-access-denied','http-access-blocked'} for a in routes['attempts'])):
                    try:
                        browser=capture(watch,self.root/f'mirror-{index}',timeout=max(15,self.args.timeout),max_backends=self.args.max_backends)
                        session.headers['User-Agent']=browser['userAgent']
                        for cookie in browser['cookies']:
                            session.cookies.set(cookie['name'],cookie['value'],domain=cookie['domain'],path=cookie.get('path','/'))
                        routes=discover(browser['url'],self.root/f'mirror-{index}/browser-routes.json',
                                        html_path=browser['html'],max_backends=self.args.max_backends,
                                        session=session,timeout=self.args.timeout,page_snapshots=browser['pages'])
                        self.record('browser-watch','player-discovered',host=parsed.hostname)
                    except BrowserError as exc:
                        self.record('browser-watch','unavailable',host=parsed.hostname,reason=str(exc))
                if not routes['routes']:
                    self.record('mirror','no-verified-route',host=parsed.hostname,report=f'mirror-{index}/routes.json',
                                failures=routes['attempts'])
                    continue
                for route in routes['routes']:
                    audio=[s for s in route['streams'] if s['mimeType'].startswith('audio/')]
                    video=[s for s in route['streams'] if s['mimeType'].startswith('video/') and s['height']<=self.args.max_height]
                    if not audio or (not self.args.audio_only and not video):
                        continue
                    selected_audio=select_audio(audio)
                    audio_path=self.root/('mirror-audio-'+hashlib.sha256((route['manifestUrl'].split('?')[0]+selected_audio['id']).encode()).hexdigest()[:12]+'.track')
                    if not self.validated('audio'):
                        download_ranges(selected_audio['url'],audio_path,cookies=session.cookies,
                                        resource_key=self.key+':'+selected_audio['id'],timeout=self.args.timeout)
                        self.finalize(audio_path=audio_path)
                    else:
                        audio_path=self.root/self.report['audio']['file']
                    if not self.args.audio_only:
                        selected_video=max(video,key=lambda s:(s['height'],s['bandwidth']))
                        video_path=self.root/('mirror-video-'+hashlib.sha256((route['manifestUrl'].split('?')[0]+selected_video['id']).encode()).hexdigest()[:12]+'.track')
                        download_ranges(selected_video['url'],video_path,cookies=session.cookies,
                                        resource_key=self.key+':'+selected_video['id'],timeout=self.args.timeout)
                        self.finalize(video_path=video_path,audio_path=audio_path)
                    self.record('mirror','verified',host=parsed.hostname,audioRepresentation=selected_audio['id'],
                                audioLanguage=selected_audio.get('language'),videoRepresentation=selected_video['id'] if not self.args.audio_only else None)
                    return True
            except (requests.RequestException,AcquisitionError,ValueError,av.FFmpegError) as exc:
                self.record('mirror','failed',host=parsed.hostname,error=type(exc).__name__)
        return False

    def run(self):
        # OS file locking releases automatically after exit or a crash.
        with self.lock.open('a+b') as lock:
            try:
                if sys.platform == 'win32':
                    import msvcrt
                    lock.write(b'0');lock.flush();lock.seek(0)
                    msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
                else:
                    import fcntl
                    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except (BlockingIOError,OSError):
                raise AcquisitionError('Another download is using this workspace')
            if self.report_path.exists():
                previous=json.loads(self.report_path.read_text())
                if previous['sourceKey'] != self.key:
                    raise AcquisitionError('Workspace contains another source; choose a new workspace')
                self.report=previous
                self.report['status']='running'
            if self.validated('audio') and (self.args.audio_only or self.validated('video')):
                self.record('resume','verified-media-reused')
            else:
                try:
                    self.direct()
                except SetupError as exc:
                    self.report['status']='error'
                    self.record('setup','error',reason=str(exc))
                    return 1
                except (AcquisitionError,av.FFmpegError) as exc:
                    self.record('direct','failed',error=type(exc).__name__)
                    if not self.mirrors():
                        self.report['status']='blocked'
                        self.report['nextAction']='Inspect the recorded HTTP/player failures and confirm browser playback for the reported public hosts. If playback is also denied, acquisition needs a working network route, explicitly supplied authentication, or a local source file.'
                        write_json(self.report_path,self.report)
                        print(json.dumps(dict(status='blocked',report=str(self.report_path),nextAction=self.report['nextAction'])),flush=True)
                        return 2
            self.report['status']='ready'
            self.report.pop('nextAction',None)
            write_json(self.report_path,self.report)
            provenance=self.workspace/'provenance.json'
            data=json.loads(provenance.read_text()) if provenance.exists() else {}
            data['sourceAcquisition']=dict(sourceKey=self.key,report='source/acquisition.json',
                                           audio=self.report['audio'],video=self.report.get('video'))
            write_json(provenance,data)
            print(json.dumps(dict(status='ready',audio=str(self.root/self.report['audio']['file']),
                                  video=str(self.root/self.report['video']['file']) if self.report.get('video') else None,
                                  report=str(self.report_path))),flush=True)
            return 0


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',help='YouTube URL, another yt-dlp-supported URL, or a local recording')
    parser.add_argument('--workspace',type=Path,required=True)
    parser.add_argument('--audio-only',action='store_true')
    parser.add_argument('--max-height',type=int,default=1080)
    parser.add_argument('--max-mirrors',type=int,default=5)
    parser.add_argument('--max-backends',type=int,default=8)
    parser.add_argument('--browser',choices=['auto','off'],default='auto',help='Use an isolated agent-browser session for mirror challenges when available')
    parser.add_argument('--timeout',type=int,default=20)
    parser.add_argument('--mirror',action='append',help='Explicit mirror origin or current watch URL; replaces registry discovery')
    parser.add_argument('--watch-html',type=Path,help='Saved browser HTML for the first explicitly provided mirror')
    parser.add_argument('--instances-url',default='https://api.invidious.io/instances.json')
    parser.add_argument('--cookies',type=Path,help='Explicitly supplied yt-dlp cookie file; never discovered automatically')
    parser.add_argument('--ffmpeg',help='Use this FFmpeg executable')
    args=parser.parse_args()
    if not 0<=args.max_mirrors<=8 or not 0<=args.max_backends<=8 or args.timeout<1 or args.max_height<1:
        parser.error('Limits must be positive; mirror/backend counts must be between 0 and 8')
    if args.watch_html and not args.mirror:
        parser.error('--watch-html requires an explicitly supplied --mirror watch URL')
    if args.cookies and not args.cookies.is_file():
        parser.error('--cookies file does not exist')
    try:
        raise SystemExit(Downloader(args).run())
    except (AcquisitionError,OSError,ValueError,av.FFmpegError) as exc:
        print(json.dumps(dict(status='error',reason=str(exc))),file=sys.stderr)
        raise SystemExit(1)


if __name__=='__main__':
    main()
