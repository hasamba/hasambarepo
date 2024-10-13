# -*- coding: utf-8 -*-
#!/usr/bin/python
import os,time,re
import sys,urllib2
import mimetypes
import xbmc,xbmcgui,xbmcaddon
import threading
from  resources.modules.client import get_html
global _shutdown
global _process
global progress_tor,break_window_tor
from resources.modules import log
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
if KODI_VERSION<=18:
    xbmc_tranlate_path=xbmc.translatePath
else:
    import xbmcvfs
    xbmc_tranlate_path=xbmcvfs.translatePath
progress_tor=''
break_window_tor=False
_process=None
_shutdown=False
Addon = xbmcaddon.Addon('plugin.video.thorrent')
__addon__=Addon
QUEUED_FOR_CHECKING     = 0
CHECKING_FILES          = 1
DOWNLOADING_METADATA    = 2
DOWNLOADING             = 3
FINISHED                = 4
SEEDING                 = 5
ALLOCATING              = 6
CHECKING_RESUME_DATA    = 7
NO_CONNECTION           = 8
state_arr=['QUEUED_FOR_CHECKING','CHECKING_FILES','DOWNLOADING_METADATA','DOWNLOADING','FINISHED','SEEDING','ALLOCATING','CHECKING_RESUME_DATA','NO_CONNECTION']
    
PUBLIC_TRACKERS = [
    "udp://tracker.openbittorrent.com:80/announce",
    "udp://open.demonii.com:1337/announce",
    'udp://tracker.leechers-paradise.org:6969/announce',
    "udp://tracker.istole.it:80/announce",
    "udp://tracker.coppersurfer.tk:6969/announce",
    "udp://tracker.publicbt.com:80/announce",
    "udp://exodus.desync.com:6969/announce",
    "udp://exodus.desync.com:80/announce",
    "udp://tracker.yify-torrents.com:80/announce",
    'http://tracker.openbittorrent.kg:2710/announce',
    'http://tracker.leechers-paradise.org:6969/announce',
    "http://tracker.istole.it:80/announce",
    "http://tracker.coppersurfer.tk:6969/announce",
    "http://tracker.publicbt.com:80/announce",
    "http://exodus.desync.com:6969/announce",
    "http://exodus.desync.com:80/announce",
    "http://tracker.yify-torrents.com:80/announce"
]
def get_seed(url):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
        'DNT': '1',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://checker.openwebtorrent.com/',
        
    }

    params = (
        ('magnet',url),
    )

    x = get_html('https://checker.openwebtorrent.com/check', headers=headers, params=params).json()
    log.warning(x)
    if 'seeds' not in x:
        return 0
    seeds=x['seeds']
    for items in x['extra']:
        if 'seeds' in items and items['seeds']>seeds:
            seeds=items['seeds']
    return seeds
            

def ensure_android_binary_location(binary_path, android_binary_path):
    
    if not os.path.exists(os.path.dirname(android_binary_path)):
        os.makedirs(os.path.dirname(android_binary_path))
    if not os.path.exists(android_binary_path) or int(os.path.getmtime(android_binary_path)) < int(os.path.getmtime(binary_path)):
        shutil.copy2(binary_path, android_binary_path)
    return android_binary_path
def _torrent_options(tv_movie,url_n,port):
        
        debug = Addon.getSetting('debug')
        log.warning('DEGUG:'+debug)
        binary_path=(os.path.join(xbmc_tranlate_path(Addon.getAddonInfo('profile')), 'resources', 'bin',"%s_%s" %(Platform.system, Platform.arch))).encode('utf-8')
        binary = "torrent2http"
        
        if Platform.system == 'windows':
            binary = "torrent2http.exe"
            torrent_file=os.path.join(xbmc_tranlate_path(Addon.getAddonInfo('profile')), 'resources', 'bin', "%s_%s" %(Platform.system, Platform.arch), binary).encode('utf-8')
        elif Platform.system == "android":
           
            binary_path = ensure_android_binary_location(binary_path, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(xbmc_tranlate_path('special://xbmc')))), "files", __addon__.getAddonInfo('id'), binary).encode('utf-8'))
            torrent_file=binary_path
            
        
    
    
        fsencoding = sys.getfilesystemencoding() or 'utf-8'
        _path = xbmc_tranlate_path("special://profile/addon_data/%s/cache" % __addon__.getAddonInfo('id'))
        if not os.path.exists(_path):
                os.makedirs(_path)
                if not os.path.exists(_path):
                    raise Error("Unable to create cache directory %s" % _path, 30322)
        cache_path = _path.encode(fsencoding)
            
        _path = os.path.join(cache_path, tv_movie)
        if not os.path.exists(_path):
            os.makedirs(_path)
            if not os.path.exists(_path):
                raise Error("Unable to create cache directory %s" % _path, 30322)
        media_cache_path = _path
        
        _path = xbmc_tranlate_path(__addon__.getSetting("%s_download_path"  %tv_movie))
        if _path:
            if _path.lower().startswith("smb://"):
                if Platform.system != "windows":
                    raise Notify("Downloading to an unmounted network share is not supported (%s)" % _path, 30319, 0)
                _path.replace("smb:", "").replace("/", "\\")

            if not os.path.isdir(_path):
                raise Notify('Download path does not exist (%s)' % _path, 30310, 1)
            
            user_download_path = _path.encode(fsencoding)
        else:
            user_download_path = None
        download_path = user_download_path or media_cache_path
        
        download_kbps = int(__addon__.getSetting("download_kbps"))
        if download_kbps <= 0:
            download_kbps = -1
        download_kbps = download_kbps
        
        upload_kbps = int(__addon__.getSetting("upload_kbps"))
        if upload_kbps <= 0:
            upload_kbps = -1
        elif upload_kbps < 15:
            raise Notify('Max Upload Rate must be above 15 Kilobytes per second.', 30324, 1)
            upload_kbps = 15
        upload_kbps = upload_kbps
        
        if not __addon__.getSetting("%s_keep_incomplete" %tv_movie) == 'false' and __addon__.getSetting("%s_keep_complete" %tv_movie) == 'true':
            keep_complete = True
        else:
            keep_complete = False
        
        
        if __addon__.getSetting("%s_keep_incomplete" %tv_movie) == 'true' and __addon__.getSetting("%s_keep_complete" %tv_movie) == 'false':
            keep_incomplete = True
        else:
            keep_incomplete = False
        
        if __addon__.getSetting("%s_keep_files" %tv_movie) == 'true' and not keep_complete and not keep_incomplete:
            keep_files = True
        else:
            keep_files = False
            
        if keep_files or keep_complete or keep_incomplete:
            delete_files = False
        else:
            delete_files = True
            
        trackers = __addon__.getSetting('trackers')
        if trackers:
            trackers = ",".join(trackers.split(',')+PUBLIC_TRACKERS)
        else:
            trackers = ",".join(PUBLIC_TRACKERS)
        trackers = trackers
        debug='false'
        kwargs = {
            # '--file-index':             0,
            '--dl-path':                download_path,
            '--connections-limit':      int(__addon__.getSetting('connections_limit')),
            '--dl-rate':                download_kbps,
            '--ul-rate':                upload_kbps,
            '--enable-dht':             __addon__.getSetting('enable_dht'),
            '--enable-lsd':             __addon__.getSetting('enable_lsd'),
            '--enable-natpmp':          __addon__.getSetting('enable_natpmp'),
            '--enable-upnp':            __addon__.getSetting('enable_upnp'),
            '--enable-scrape':          __addon__.getSetting('enable_scrape'),
            '--encryption':             int(__addon__.getSetting('encryption')),
            '--show-stats':             debug,
            '--files-progress':         debug,
            '--overall-progress':       debug,
            '--pieces-progress':        debug,
            '--listen-port':            int(__addon__.getSetting('listen_port')),
            '--random-port':            __addon__.getSetting('use_random_port'),
            '--keep-complete':          str(keep_complete).lower(),
            '--keep-incomplete':        str(keep_incomplete).lower(),
            '--keep-files':             str(keep_files).lower(),
            '--max-idle':               300,
            '--no-sparse':              'false',
            #'--resume-file':            None,
            '--user-agent':             'torrent2http/1.0.1 libtorrent/1.0.3.0 kodipopcorntime/%s' %__addon__.getAddonInfo('version'),
            #'--state-file':             None,
            '--enable-utp':             __addon__.getSetting('enable_utp'),
            '--enable-tcp':             __addon__.getSetting('enable_tcp'),
            '--debug-alerts':           debug,
            '--torrent-connect-boost':  int(__addon__.getSetting('torrent_connect_boost')),
            '--connection-speed':       int(__addon__.getSetting('connection_speed')),
            '--peer-connect-timeout':   int(__addon__.getSetting('peer_connect_timeout')),
            '--request-timeout':        20,
            '--min-reconnect-time':     int(__addon__.getSetting('min_reconnect_time')),
            '--max-failcount':          int(__addon__.getSetting('max_failcount')),
            '--dht-routers':            __addon__.getSetting('dht_routers') or None,
            '--trackers':               trackers,
            
        }

        args = [torrent_file]
        for k, v in kwargs.iteritems():
            if v == 'true':
                args.append(k)
            elif v == 'false':
                args.append("%s=false" % k)
            elif v is not None:
                args.append(k)
                if isinstance(v, str):
                    args.append(v.decode('utf-8').encode(fsencoding))
                else:
                    args.append(str(v))

        torrent_options = args
        args = ['--uri', url_n, '--bind', '127.0.0.1:%s' %port]
        for i in xrange(4):
            if isinstance(args[i], str):
                args[i] = args[i].decode('utf-8')
            args[i] = args[i].encode(fsencoding)
        return torrent_options+args
        
class Thread(threading.Thread):
    LOCAL = threading.local()

    def __init__(self, target=None):
        self._target   = target or self.run
        self._exc_info = []

        super(Thread, self).__init__(target=self.___run)
        self.daemon = False
        self.stop = threading.Event()
        self.start()

    def __enter__(self):
        return self

    def ___run(self):
        try:
            Thread.LOCAL.tName = self.getName()
            self._target()
        except:
            self._exc_info = sys.exc_info()
            sys.exc_clear()
            self.stop.set()

    def checkError(self):
        return len(self._exc_info) > 0

    def raiseAnyError(self):
        if self._exc_info: 
            raise self._exc_info[0], self._exc_info[1], self._exc_info[2]

    def cleanError(self):
        self._exc_info = []

    def getError(self):
        return self._exc_info

    def __exit__(self, *exc_info):
        self.close()
        return not exc_info[0] and not len(self._exc_info) > 0

    def __del__(self):
        self.close()

    def close(self):
        if hasattr(self, 'stop') and not self.stop.is_set():
            self.stop.set()
        self.raiseAnyError()
def get_torrent_file(silent_mode=False):
    import shutil
    global progress_tor,break_window_tor
    path1=xbmc_tranlate_path('special://home/addons/script.module.requests/lib')
    sys.path.append( path1)
    path1=xbmc_tranlate_path('special://home/addons/script.module.urllib3/lib')
    sys.path.append( path1)
    path1=xbmc_tranlate_path('special://home/addons/script.module.chardet/lib')
    sys.path.append( path1)
    path1=xbmc_tranlate_path('special://home/addons/script.module.certifi/lib')
    sys.path.append( path1)
    path1=xbmc_tranlate_path('special://home/addons/script.module.idna/lib')
    sys.path.append( path1)
    path1=xbmc_tranlate_path('special://home/addons/script.module.futures/lib')
    sys.path.append( path1)
    
    ok=False
    if Addon.getSetting('new_play_window')=='false':
        dp = xbmcgui . DialogProgress ( )
        dp.create('אנא המתן','בודק אם נגן קיים', '','')
        dp.update(0, 'אנא המתן','בודק אם נגן קיים', '' )
    progress_tor='בודק נגן'
    def download_file(url,path):
        import requests
        local_filename =os.path.join(path, "1.zip")
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True)
        total_length = r.headers.get('content-length')

        if total_length is None: # no content length header
            total_length=1
        with open(local_filename, 'wb') as f:
            dl = 0
            total_length = int(total_length)
            for chunk in r.iter_content(chunk_size=1024): 
                dl += len(chunk)
                done = int(100 * dl / total_length)
                if Addon.getSetting('new_play_window')=='false':
                    dp.update(done, 'אנא המתן','מוריד נגן', '' )
                progress_tor=' מוריד נגן '+str(done)
                
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush() commented by recommendation from J.F.Sebastian
        return local_filename

    def unzip(file,path):
        global progress_tor,break_window_tor
        if Addon.getSetting('new_play_window')=='false':
            dp.update(100, 'אנא המתן','מחלץ', '' )
        progress_tor=' מחלץ '
        from zipfile import ZipFile
        
        
        zip_file = file
        ptp = 'Masterpenpass'
        #xbmc.executebuiltin("XBMC.Extract({0}, {1})".format(zip_file, path), True)
        
        zf=ZipFile(zip_file)
        #zf.setpassword(bytes(ptp))
        #with ZipFile(zip_file) as zf:
        zf.extractall(path)
        
    
    binary = "torrent2http"
    bin_dataDir=(os.path.join(xbmc_tranlate_path(Addon.getAddonInfo('profile')), 'resources', 'bin',"%s_%s" %(Platform.system, Platform.arch))).encode('utf-8')
    if Platform.system == 'windows':
        binary = "torrent2http.exe"
        url='https://github.com/DiMartinoXBMC/script.module.torrent2http/raw/master/bin/windows_x86/torrent2http.exe.zip'
        file=os.path.join(bin_dataDir,'1.zip')
    elif Platform.system == "android":
        url='https://github.com/DiMartinoXBMC/script.module.torrent2http/raw/master/bin/android_arm/torrent2http.zip'
        file=os.path.join(bin_dataDir,'1.zip')
    else:
        url='https://github.com/DiMartinoXBMC/script.module.torrent2http/raw/master/bin/linux_arm/torrent2http.zip'
        file=os.path.join(bin_dataDir,'1.zip')
    torrent_file=os.path.join(xbmc_tranlate_path(Addon.getAddonInfo('profile')), 'resources', 'bin', "%s_%s" %(Platform.system, Platform.arch), binary).encode('utf-8')
    
    
    if not os.path.exists(bin_dataDir) or not os.path.isfile(torrent_file):
        if os.path.exists(bin_dataDir):
           
            shutil.rmtree(bin_dataDir)
        
        os.makedirs(bin_dataDir)
        
        download_file(url,bin_dataDir)
        unzip(file,bin_dataDir)
        os.remove(file)
    else:
        if silent_mode==False:
       
            ok=xbmcgui.Dialog().yesno(("נגן קיים"),('להוריד בכל זאת?'))
            if ok:
                shutil.rmtree(bin_dataDir)
                os.makedirs(bin_dataDir)
        
                download_file(url,bin_dataDir)
                unzip(file,bin_dataDir)
                os.remove(file)
    if Addon.getSetting('new_play_window')=='false':
        dp.close()
    if silent_mode==False:
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('הורדה', '[COLOR aqua][I] הורד בהצלחה תהנה [/I][/COLOR]')))
        #xbmcgui.Dialog().ok('הורדה','[COLOR aqua][I] הורד בהצלחה תהנה [/I][/COLOR]')
        ok=True
    return ok
def get_free_port(port=5001):
    import socket
    """
    Check we can bind to localhost with a specified port
    On failer find a new TCP port that can be used for binding
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', port))
        s.close()
    except socket.error:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('127.0.0.1', 0))
            port = s.getsockname()[1]
            s.close()
        except socket.error:
            raise Error("Can not find a TCP port to bind torrent2http", 30300)
    return port
class Platform(object):
    class __metaclass__(type):
        def __getattr__(cls, name):
            getattr(cls, "_%s" % name)()
            return getattr(cls, name)

        def _arch(cls):
            if sys.platform.lower().startswith('linux') and (os.uname()[4].lower().startswith('arm') or os.uname()[4].lower().startswith('aarch')):
                cls.arch = 'arm'
            elif sys.maxsize > 2**32 or sys.platform.lower().startswith('linux') and os.uname()[4].lower().startswith('x86_64'):
                cls.arch = 'x64'
            else:
                cls.arch = 'x86'

        def _system(cls):
            if sys.platform.lower().startswith('linux'):
                cls.system = 'linux'
                if 'ANDROID_DATA' in os.environ:
                    cls.system = 'android'
            elif sys.platform.lower().startswith('win'):
                cls.system = 'windows'
            elif sys.platform.lower().startswith('darwin'):
                cls.system = 'darwin'
            else:
                cls.system = None
def isAlive():
        global _process
        return _process and _process.poll() is None
class JSONDecodeError(ValueError):
    """Subclass of ValueError with the following additional properties:

    msg: The unformatted error message
    doc: The JSON document being parsed
    pos: The start index of doc where parsing failed
    end: The end index of doc where parsing failed (may be None)
    lineno: The line corresponding to pos
    colno: The column corresponding to pos
    endlineno: The line corresponding to end (may be None)
    endcolno: The column corresponding to end (may be None)

    """
    # Note that this exception is used from _speedups
    def __init__(self, msg, doc, pos, end=None):
        ValueError.__init__(self, errmsg(msg, doc, pos, end=end))
        self.msg = msg
        self.doc = doc
        self.pos = pos
        self.end = end
        self.lineno, self.colno = linecol(doc, pos)
        if end is not None:
            self.endlineno, self.endcolno = linecol(doc, end)
        else:
            self.endlineno, self.endcolno = None, None

    def __reduce__(self):
        return self.__class__, (self.msg, self.doc, self.pos, self.end)

def status( port,timeout=30):
        global _shutdown
        _last_status_pre   = {"name":"","state":NO_CONNECTION,"state_str":"no_connection","error":"","progress":0,"download_rate":0, "upload_rate":0,"total_download":0,"total_upload":0,"num_peers":0,"num_seeds":0,"total_seeds":-1,"total_peers":-1}
        if not _shutdown:
            _url = "http://127.0.0.1:%s/" %port
            
            if not isAlive():
                raise TorrentError("torrent2http are not running")
            _last_status = get_html(_url+ "/status", timeout=5).json() or _last_status
            if _last_status.get('error'):
                raise TorrentError("torrent2http error: %s" %_last_status['error'])
            if 'error_code' in _last_status:
                log.warning('(Torrent) %s: %s' %('Status', _last_status))
                sys.exc_clear()
                _last_status=_last_status_pre
        return _last_status
class LogPipe(Thread):
    def __init__(self, logger):
        self._logger = logger
        self._read_fd, self._write_fd = os.pipe()
        super(LogPipe, self).__init__(target=self.run)

    def fileno(self):
        return self._write_fd

    def run(self):
        self._logger("Logging started")
        with os.fdopen(self._read_fd) as f:
            for line in iter(f.readline, ""):
                line = re.sub(r'^\d+/\d+/\d+ \d+:\d+:\d+ ', '', line)
                self._logger(line.strip())
                if self.stop.is_set():
                    break
        self._logger("Logging finished")        
def _debug( message):
        log.warning("(Torrent) (torrent2http) %s" % message)
class Error(Exception):
    def __init__(self, tracebackStr, messageID):
        # An English explanation for use in traceback
        self.tracebackstr = tracebackStr

        # Message identifier which can be translated into a local language message to the user
        self.messageID = messageID

    def __str__(self):
        return self.tracebackstr
class TorrentError(Error):
    def __init__(self, tracebackStr, messageID=None):
        # An English explanation for use in traceback
        self.tracebackstr = tracebackStr

        # Message identifier which can be translated into a local language message to the user
        self.messageID = messageID or 30313
def isAlive():
        global _process
        return _process and _process.poll() is None

        
def preload(port):
    global _process
    global progress_tor,break_window_tor
    log.warning('S1:')
    if Addon.getSetting('new_play_window')=='false':
        dp = xbmcgui . DialogProgress ( )
        dp.create('אנא המתן','מפעיל', '','')
        dp.update(0, 'אנא המתן','מפעיל', '' )
    progress_tor='מפעיל'
    log.warning('(Loader) Pre-Loading media')


    progress = 0
    _url = "http://127.0.0.1:%s/" %port
    start_time=time.time()
    duration=0
    #start
    log.warning('Start:')
    while not _shutdown:
        xbmc.sleep(100)
        if (time.time() - start_time) > 5 or not isAlive():
                    raise TorrentError("Can't start torrent2http")
                    
        status =  get_html(_url+ "/status", timeout=5).json() 
        if not status['state'] == NO_CONNECTION:
            break
    #get file
    log.warning('get file:')
    if not isAlive():
       raise TorrentError("torrent2http are not running")
    _last_files = get_html(_url+"/ls", timeout=5).json()['files']
    #_checkData
    log.warning('_checkData:')
    while not _shutdown:
            status =  get_html(_url+ "/status", timeout=5).json() 
            elapsed_time = time.time() - start_time
            progress_tor='Seed: %s, Peers:%s, State:%s, Down:%s'%(str(status['total_seeds']),str(status['total_peers']),status['state_str'],str(status['download_rate']))
            if Addon.getSetting('new_play_window')=='false':
                dp.update(int(status['progress']),'אנא המתן','Seed: %s, Peers:%s, State:%s, Down:%s'%(str(status['total_seeds']),str(status['total_peers']),status['state_str'],str(status['download_rate'])),time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
                
                if dp.iscanceled():
                    dp.close()
                    _process.kill()
                    return 'Stop'
                    break
            else:
                        
                if break_window_tor:
                    _process.kill()
                    return 'Stop'
            if status['state'] in [FINISHED, SEEDING, DOWNLOADING]:
                break
    #Preload
    log.warning('Preload:')
    start_time=time.time()
    min_magnet_rate=int(Addon.getSetting('min_magnet_rate'))
    timeout_magnet=int(Addon.getSetting('timeout_magnet'))
    while not _shutdown:
        time.sleep(0.100)

        status =  get_html(_url+ "/status", timeout=5).json() 
        elapsed_time = time.time() - start_time
        if Addon.getSetting('new_play_window')=='false':
            dp.update(int(status['progress']*1.0),'אנא המתן','Seed: %s, Peers:%s, State:%s, Down:%s'%(str(status['total_seeds']),str(status['total_peers']),status['state_str'],str(status['download_rate'])),time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        progress_tor='Seed: %s, Peers:%s, State:%s, Down:%s'%(str(status['total_seeds']),str(status['total_peers']),status['state_str'],str(status['download_rate']))
        if elapsed_time>timeout_magnet:
            if status['download_rate']<min_magnet_rate:
                return None
        if Addon.getSetting('new_play_window')=='false':
            if dp.iscanceled():
                dp.close()
                _process.kill()
                return 'Stop'
                break
        else:
                if break_window_tor:
                    _process.kill()
                    return 'Stop'
        if status['download_rate'] <= 0:
            continue
        break
    #filestatus = _TEngine.playFile()
    files=get_html(_url+ "ls", timeout=5).json()['files']
    log.warning('files:')
    log.warning(files)
    size = 0
    f_url=None
    for i, f in enumerate(files):
        
        #mimeType = mimetypes.guess_type(f['name'])
        log.warning('(Torrent) File name: %s, MIME info: %s' %(f['name'], ''))
        # if mimeType[0] and mimeType[0][:5] == 'video' and f['size'] > size:
        # if 'video' in str(mimeType) and f['size'] > size:
        if(re.match('.*\.avi|.*\.mp4|.*\.mkv',f['name'])):
            _file_id = i
            log.warning(f['url'])
            f_url=f['url']
            try:
            
              urllib2.urlopen(f['url'], timeout=5)

            except:
              pass
    try:
        filestatus=files[_file_id]
    except (KeyError, TypeError):
        raise TorrentError("Can not find a file to play")
    start_time=time.time()
    min_download_rate=int(Addon.getSetting('min_download_rate'))
    
    while not _shutdown:
        xbmc.sleep(100)
        files=get_html(_url+ "ls", timeout=5).json()['files']
        status =  get_html(_url+ "/status", timeout=5).json()
        filestatus=files[_file_id]
        bytSeconds = status['download_rate']*0.8*1024 # Download rate is reduced by 20 percent to make sure against fluctuations.
        needSizeInProcent = 0.0025 # Fix cache size
        needSizeInProcent = float(__addon__.getSetting("buffer_pre"))/10000
        
        if duration > 0:
            # How long does it take to download the entire movie in seconds.
            seconds = filestatus['size']/bytSeconds
            elapsed_time = time.time() - start_time
            if Addon.getSetting('new_play_window')=='false':
                dp.update(int(progress*1.0),'אנא המתן',str(seconds),str(needSizeInProcent),time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
            progress_tor=str(seconds)+','+str(needSizeInProcent)
            # Does it take longer time than to play the movie? Otherwise we only
            # need a buffer to protect against fluctuations (0.02)
            if seconds > duration:
                # If a movie has a playback time of 2 hours and we take 3 hours to download the movie,
                # we can only reach to download 2/3 of the movie. We therefore need to cache 1/3 of the movie before playback.
                # (Or the user need a new connection)
                needSizeInProcent = 1-(duration/seconds)
            else:
                needSizeInProcent = 1-(duration/(duration+60.0)) # 60 seconds cache

        needCacheSize = filestatus['size']*needSizeInProcent
        progressValue=0
        try:
            progressValue = (100/(((needCacheSize)/bytSeconds)*1000))*100
        except:
            pass
        
        progress = progress+progressValue
        
        data=status
        if 'state_str' in data and 'download_rate' in data:
            stri=str(data['state_str'])+' '+str(round(data['download_rate'],2))+'Kb/s'
        if 'num_seeds' in data and 'num_peers' in data:
            stri2=' S-'+str(data['num_seeds'])+'/P-'+str(data['num_peers'])
        if 'error' in data and len(data['error'])>1:
            log.warning('Error in data:'+str(data['error']))
            err=data['error']
            stri2=err
        prog=0
        try:
            prog=int(((filestatus['download']*0.45))/needCacheSize)
        except Exception as e:
            log.warning('Buffer err:'+str(e))
            pass
        elapsed_time = time.time() - start_time
        if elapsed_time>timeout_magnet:
            if data['download_rate']<min_download_rate:
                return None
        if Addon.getSetting('new_play_window')=='false':
            dp.update(int(progress), stri, stri2,time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
                        
        progress_tor=str(int(progress))+'%,'+stri+','+stri2
        if Addon.getSetting('new_play_window')=='false':
            if dp.iscanceled():
                    dp.close()
                    _process.kill()
                    return 'Stop'
                    break
        else:
                if break_window_tor:
                    _process.kill()
                    return 'Stop'
        if progress >= 100 or (filestatus['download']*0.45) >= needCacheSize: # We are caching about 65% (filestatus['download']*0.45) more end need (needCacheSize).
            
            log.warning('(Loader) Finished with pre-loading media')
            if Addon.getSetting('new_play_window')=='false':
                dp.close()
            return f_url
        
    try:
        dp.close()
    except:
        pass
    return f_url
def get_torrent_link(url_n,tv_movie):
    global _shutdown,_process
    import subprocess
    
    if not _shutdown:
        log.warning('(Torrent) Find free port')
        port = get_free_port()

        log.warning('(Torrent) Starting torrent2http')
        startupinfo = None
        if Platform.system == "windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= 1
            startupinfo.wShowWindow = 0

        
        _logpipe = LogPipe(_debug)

        torrent_options =_torrent_options(tv_movie,url_n,port)

        try:
            _process = subprocess.Popen(torrent_options, stderr=_logpipe, stdout=_logpipe, startupinfo=startupinfo)
        except Exception as e:
           
            raise TorrentError("Can't start torrent2http: %s" % str(sys.exc_info()[1]))
        _url = "http://127.0.0.1:%s/" %port
        log.warning('_url::'+_url)
        start = time.time()
        progress_tor='מפעיל נגן'
        while not _shutdown:
            if (time.time() - start) > 5 or not isAlive():
                raise TorrentError("Can't start torrent2http")
            now_state=status(port,1)
            log.warning('now_state:')
            log.warning(now_state)
            if not now_state['state'] == NO_CONNECTION:
                log.warning("(Torrent) torrent2http successfully started")
                break
    url=preload(port)
    return url