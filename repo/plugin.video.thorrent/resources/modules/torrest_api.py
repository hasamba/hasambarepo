# -*- coding: utf-8 -*-
from collections import namedtuple

import sys,re,os,json,threading,time
import xbmc,xbmcgui,xbmcaddon
from xbmc import Monitor
from xbmcgui import ListItem, DialogProgress, Dialog
Addon = xbmcaddon.Addon('plugin.video.thorrent')
from resources.modules import log
from  resources.modules.client import get_html
global progress_torrest,break_window_tor,_process,break_window_torrest
_process=''
progress_torrest=''
break_window_tor=False
break_window_torrest=False

KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
if KODI_VERSION<=18:
    xbmc_tranlate_path=xbmc.translatePath
else:
    import xbmcvfs
    xbmc_tranlate_path=xbmcvfs.translatePath
user_dataDir = xbmc_tranlate_path(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)
     
base_header={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',

            'Pragma': 'no-cache',
            
           
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            }

TorrentStatus = namedtuple("TorrentStatus", [
    "active_time",  # type:int
    "all_time_download",  # type:int
    "all_time_upload",  # type:int
    "download_rate",  # type:int
    "finished_time",  # type:int
    "has_metadata",  # type:bool
    "paused",  # type:bool
    "peers",  # type:int
    "peers_total",  # type:int
    "progress",  # type:float
    "seeders",  # type:int
    "seeders_total",  # type:int
    "seeding_time",  # type:int
    "state",  # type:int
    "total",  # type:int
    "total_done",  # type:int
    "total_wanted",  # type:int
    "total_wanted_done",  # type:int
    "upload_rate",  # type:int
])

TorrentInfo = namedtuple("TorrentInfo", [
    "info_hash",  # type:str
    "name",  # type:str
    "size",  # type:int
])

Torrent = namedtuple("Torrent", list(TorrentInfo._fields) + [
    "status",  # type:TorrentStatus
])

FileStatus = namedtuple("FileStatus", [
    "total",  # type:int
    "total_done",  # type:int
    "buffering_total",  # type:int
    "buffering_progress",  # type:float
    "priority",  # type:int
    "progress",  # type:float
    "state",  # type:int
])

FileInfo = namedtuple("FileInfo", [
    "id",  # type:int
    "length",  # type:int
    "name",  # type:str
    "path",  # type:str
])

File = namedtuple("File", list(FileInfo._fields) + [
    "status",  # type:FileStatus
])
ADDON=Addon
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_ID = ADDON.getAddonInfo("id")
ADDON_PATH = (ADDON.getAddonInfo("path"))
ADDON_ICON = (ADDON.getAddonInfo("icon"))
ADDON_DATA = (xbmc_tranlate_path(ADDON.getAddonInfo("profile")))
class PlayError(Exception):
    pass
videos_extensions = (
    '.m4v', '.3g2', '.3gp', '.nsv', '.tp', '.ts', '.ty', '.strm', '.pls', '.rm', '.rmvb', '.mpd', '.m3u', '.m3u8',
    '.ifo', '.mov', '.qt', '.divx', '.xvid', '.bivx', '.vob', '.nrg', '.pva', '.wmv', '.asf', '.asx', '.ogm', '.m2v',
    '.avi', '.dat', '.mpg', '.mpeg', '.mp4', '.mkv', '.mk3d', '.avc', '.vp3', '.svq3', '.nuv', '.viv', '.dv', '.fli',
    '.flv', '.001', '.wpl', '.vdr', '.dvr-ms', '.xsp', '.mts', '.m2t', '.m2ts', '.evo', '.ogv', '.sdp', '.avs', '.rec',
    '.url', '.pxml', '.vc1', '.h264', '.rcv', '.rss', '.mpls', '.webm', '.bdmv', '.wtv', '.trp', '.f4v')
def notification(message, heading=ADDON_NAME, icon=ADDON_ICON, time=5000, sound=True):
    xbmcgui.Dialog().notification(heading, message, icon, time, sound)
def is_video(s):
    return s.lower().endswith(videos_extensions)

def ensure_android_binary_location(binary_path, android_binary_path):
    
    if not os.path.exists(os.path.dirname(android_binary_path)):
        os.makedirs(os.path.dirname(android_binary_path))
    if not os.path.exists(android_binary_path) or int(os.path.getmtime(android_binary_path)) < int(os.path.getmtime(binary_path)):
        shutil.copy2(binary_path, android_binary_path)
    return android_binary_path
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
def from_dict(data, clazz, **converters):
    if data is None:
        return None
    # data = dict(data)
    for k, converter in converters.items():
        data[k] = converter(data.get(k))
    return clazz(**data)


class TorrestError(Exception):
    pass
def build_setting_file(port,tv_movie):
    c_path = xbmc_tranlate_path("special://profile/addon_data/%s/cache" % Addon.getAddonInfo('id'))
    if not os.path.exists(c_path):
                os.makedirs(c_path)
                
    _path = xbmc_tranlate_path(Addon.getSetting("%s_download_path"  %tv_movie))
    f_path=c_path
    if _path:
        f_path=_path
        
    t_path=os.path.join(f_path,'Torrents')
    if not os.path.exists(t_path):
            os.makedirs(t_path)
    buffer_size=int(Addon.getSetting('buffer_pre'))*1024*1024
    file_d={
           #"listen_port": int(port),
           "listen_interfaces": "",
           "outgoing_interfaces": "",
           "disable_dht": False,
           "disable_upnp": False,
           "download_path": f_path,
           "torrents_path": t_path,
           "user_agent": 0,
           "session_save": 30,
           "tuned_storage": False,
           "connections_limit": 0,
           "limit_after_buffering": False,
           "max_download_rate": 0,
           "max_upload_rate": 0,
           "share_ratio_limit": 0,
           "seed_time_ratio_limit": 0,
           "seed_time_limit": 0,
           "encryption_policy": 0,
           "proxy": None,
           "buffer_size": buffer_size,
            "service_log_level": 4,
           "alerts_log_level": 0
    }
    file_d2={#"listen_port":int(port),
            "listen_interfaces":"",
            "outgoing_interfaces":"",
            "disable_dht":False,
            "disable_upnp":False,
            "download_path":"downloads",
            "torrents_path":"downloads\\Torrents",
            "user_agent":0,
            "session_save":30,
            "tuned_storage":False,
            "connections_limit":0,
            "limit_after_buffering":False,
            "max_download_rate":0,
            "max_upload_rate":0,
            "share_ratio_limit":0,
            "seed_time_ratio_limit":0,
            "seed_time_limit":0,
            "encryption_policy":0,
            "proxy":None,
            "buffer_size":20971520,
            "piece_wait_timeout":60,
            "service_log_level":4,
            "alerts_log_level":0}
    settings_file=os.path.join(user_dataDir,'settings.json')
   

        
    with open(settings_file, "w") as write_file:
        json.dump(file_d, write_file)
    return file_d
HANDLE_FLAG_INHERIT = 0x00000001

def windows_suppress_file_handles_inheritance(r=100):
    import stat
    from ctypes import windll, wintypes, byref
    from msvcrt import get_osfhandle

    handles = []
    for fd in range(r):
        try:
            # May raise OSError
            s = os.fstat(fd)
            if stat.S_ISREG(s.st_mode):
                # May raise IOError
                handle = get_osfhandle(fd)
                flags = wintypes.DWORD()
                windll.kernel32.GetHandleInformation(handle, byref(flags))
                if flags.value & HANDLE_FLAG_INHERIT:
                    if windll.kernel32.SetHandleInformation(handle, HANDLE_FLAG_INHERIT, 0):
                        handles.append(handle)
                    else:
                        logging.error("Error clearing inherit flag, disk file handle %x", handle)
        except (OSError, IOError):
            pass

    return handles
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
            raise TypeError( self._exc_info[0], self._exc_info[1], self._exc_info[2])

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
def windows_restore_file_handles_inheritance(handles):
    import ctypes

    for osf_handle in handles:
        try:
            ctypes.windll.kernel32.SetHandleInformation(osf_handle, HANDLE_FLAG_INHERIT, HANDLE_FLAG_INHERIT)
        except (ctypes.WinError, WindowsError, OSError):
            pass
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
def get_state_string(state):
    if 0 <= state <= 9:
        return ('Queued: ' + str(state))
    return ('Unknown')
def sizeof_fmt(num, suffix="B", divisor=1000.0):
    for unit in ("", "k", "M", "G", "T", "P", "E", "Z"):
        if abs(num) < divisor:
            return "{:.2f}{}{}".format(num, unit, suffix)
        num /= divisor
    return "{:.2f}{}{}".format(num, "Y", suffix)
def buffer_and_play(info_hash, file_id,api,url_n):
    global progress_torrest,break_window_torrest,_process
    
    api.download_file(info_hash, file_id, buffer=True)

    monitor = Monitor()
    if 1:#Addon.getSetting('new_play_window')=='false':
        progress = DialogProgress()
        progress.create(ADDON_NAME)
    buffer_size=int(Addon.getSetting('buffer_pre'))*1024*1024
    try:
        timeout = int(Addon.getSetting('buffer_timeout'))
        start_time = time.time()
        last_time = 0
        last_done = 0
        total_done=0
        to_value=0
        while True:
            current_time = time.time()
            status = api.file_status(info_hash, file_id)
            
            
            total_done = status.buffering_total * status.buffering_progress / 100
            
            if total_done >= buffer_size:
                break
            speed = float(total_done - last_done) / (current_time - last_time)
            last_time = current_time
            last_done = total_done
            status2 = api.torrent_status(info_hash)
            status3 = api.simple_status()
            
            #if status3['progress']>3:
            #    break
            if 1:#Addon.getSetting('new_play_window')=='false':
                progress.update(
                    int((total_done*100.0)/buffer_size),
                    "{} - {:.2f}%".format(get_state_string(status.state), (total_done*100)/buffer_size),
                    "{} {} {} - {}/s".format(
                        sizeof_fmt(total_done), 'of', sizeof_fmt(buffer_size), sizeof_fmt(speed)),'S:'+str(status2.seeders)+',P:'+str(round(status3['progress'],2))+',Timeout:'+str(to_value) )
            progress_torrest=str(round((total_done*100.0)/buffer_size,1))+",{} - {:.2f}%".format(get_state_string(status.state), (total_done*100)/buffer_size)
            close=False
            if 1:#Addon.getSetting('new_play_window')=='false':
                if progress.iscanceled():
                    close=True
            else:
                
                log.warning('break_window_torrest:')
                log.warning(break_window_torrest)
                if break_window_torrest==True:
                    close=True
            if close:
                api.stop_torrent( info_hash)
                _process.kill()
                import shutil
                _path = xbmc_tranlate_path("special://profile/addon_data/%s/cache" % Addon.getAddonInfo('id'))
      
                if os.path.exists(_path):
                    counter=0
                    while(counter<20):
                        try:
                            log.warning('Remove:')
                            shutil.rmtree(_path)
                            break
                        except:
                            try:
                                _process.kill()
                            except:
                                pass
                            xbmc.sleep(100)
                        counter+=1
                return 'stop'
                        
                raise PlayError("User canceled buffering")
            log.warning('speed:'+str(status3['download_rate']))
            log.warning('Time:'+str((current_time - start_time)))
            log.warning((timeout/3))
            to_value=0
            if (status3['download_rate'])<10:
                to_value=int((timeout/3)-(current_time - start_time))
            if (current_time - start_time) >(timeout/3) and (status3['download_rate'])<10:
                notification('Timeout reached')
                raise PlayError("Buffering timeout reached")
            
            if monitor.waitForAbort(1):
                raise PlayError("Abort requested")
    finally:
        if 1:#Addon.getSetting('new_play_window')=='false':
            progress.close()

    serve_url = api.serve_url(info_hash, file_id)
    log.warning(serve_url)
    return serve_url
def play_info_hash(info_hash,api,url_n, timeout=10, buffer=True):
    global progress_torrest,break_window_torrest,_process
    start_time = time.time()
    monitor = Monitor()
    if 1:#Addon.getSetting('new_play_window')=='false':
        progress = DialogProgress()
        progress.create('Thorrent ', "Waiting for metadata")

    try:
        while not api.torrent_status(info_hash).has_metadata:
            status = api.torrent_status(info_hash)
            
            if monitor.waitForAbort(0.5):
                raise PlayError("Abort requested")
            passed_time = time.time() - start_time
            if 0 < timeout < passed_time:
                notification("Timed out waiting for metadata")
                raise PlayError("No metadata after timeout")
            if 1:#Addon.getSetting('new_play_window')=='false':
                progress.update(int(100 * passed_time / timeout),'S:'+str(status.seeders_total)+',D:'+str(status.download_rate),str(status.progress))
            progress_torrest='Hash wait,S:'+str(status.seeders_total)+',D:'+str(status.download_rate)+',P:'+str(status.progress)
            close=False
            if 1:#Addon.getSetting('new_play_window')=='false':
                if progress.iscanceled():
                    close=True
            else:
                # global progress_torrest,break_window_torrest
                if break_window_torrest==True:
                    close=True
            if close:
                log.warning('Close1:')
                try:
                    api.stop_torrent( info_hash)
                except:
                    pass
                try:
                    _process.kill()
                except:
                    pass
                log.warning('Close3:')
                import shutil
                _path = xbmc_tranlate_path("special://profile/addon_data/%s/cache" % Addon.getAddonInfo('id'))
                log.warning('Close4:')
                if os.path.exists(_path):
                    counter=0
                    while(counter<20):
                        try:
                            log.warning('Remove:')
                            shutil.rmtree(_path)
                            break
                        except:
                            try:
                                _process.kill()
                            except:
                                pass
                            xbmc.sleep(100)
                        counter+=1
                return 'stop'
    finally:
        if 1:#Addon.getSetting('new_play_window')=='false':
            progress.close()
    '''
    start_time=time.time()
    progress = DialogProgress()
    progress.create('Thorrent ', "Waiting for metadata")
    
    while 1:
        status = api.simple_status()
        passed_time = time.time() - start_time
        if 0 < timeout < passed_time:
            notification("Timed out waiting for metadata")
            raise PlayError("No metadata after timeout")
        progress.update(int(100 * passed_time / timeout),'Wait:'+str(status['download_rate']))
        log.warning(status)
        if status['download_rate']==0:
            break
        xbmc.sleep(100)
    
    progress.close()
    '''
    files = api.files(info_hash, status=False)
    
    min_candidate_size = int(Addon.getSetting('min_candidate_size')) * 1024 * 1024
    candidate_files=[]
    for f in files:
        
        if is_video(f.path) and f.length >= min_candidate_size:
            
            candidate_files.append(f)

    if not candidate_files:
        notification("No candidate files found")
        raise PlayError("No candidate files found for {}".format(info_hash))
    elif len(candidate_files) == 1:
        chosen_file = candidate_files[0]
    else:
        #chosen_index = Dialog().select("Please choose what file to play", [f.name for f in candidate_files])
        #if chosen_index < 0:
        #    raise PlayError("User canceled dialog select")
        chosen_file = candidate_files[0]

    if buffer:
        serve_url=buffer_and_play(info_hash, chosen_file.id,api,url_n)
    else:
        play(info_hash, chosen_file.id)
    return serve_url
def android_get_current_app_id():
    with open("/proc/{:d}/cmdline".format(os.getpid())) as fp:
        return fp.read().rstrip("\0")
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
def get_torrent_link(url_n,tv_movie,free_port,file_loc,file_path,api):
    import subprocess
    global _process
    file_d=build_setting_file(free_port,tv_movie)
    
    
    settings_file=os.path.join(user_dataDir,'settings.json')
    cmd=[file_loc,'-port',str(free_port),'-settings',settings_file]
    _logpipe = LogPipe(_debug)
    kwargs={}
    if Platform.system == 'windows':
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
        kwargs.setdefault("startupinfo", si)
        handles = windows_suppress_file_handles_inheritance()
        kwargs.setdefault("stdout", subprocess.PIPE)
        kwargs.setdefault("stderr", subprocess.STDOUT)
        kwargs.setdefault("cwd", file_path)
        try:
            _process = subprocess.Popen(cmd, stderr=_logpipe, stdout=_logpipe, startupinfo=si)
        except Exception as e:
           
            raise TorrentError("Can't start torrest: %s" % str(sys.exc_info()[1]))
        finally:
            if Platform.system == 'windows':
                windows_restore_file_handles_inheritance(handles)
    else:
        si=None
        kwargs.setdefault("close_fds", True)
        # Make sure we update LD_LIBRARY_PATH, so libs are loaded
        env = kwargs.get("env", os.environ).copy()
        ld_path = env.get("LD_LIBRARY_PATH", "")
        if ld_path:
            ld_path += os.pathsep
        ld_path +=  os.path.join(os.sep, "data", "data", android_get_current_app_id(), "files", "torrest")
        env["LD_LIBRARY_PATH"] = ld_path
        kwargs["env"] = env
        handles = []
        kwargs.setdefault("stdout", subprocess.PIPE)
        kwargs.setdefault("stderr", subprocess.STDOUT)
        kwargs.setdefault("cwd", file_path)
    
        try:
            _process = subprocess.Popen(cmd,**kwargs)
        except Exception as e:
           
            raise TorrentError("Can't start torrest: %s" % str(sys.exc_info()[1]))
        
    log.warning(kwargs)
    
    
       
    #r = get_html( "http://{}:{}".format('127.0.0.1', free_port)+"/settings/set", json=file_d).content()
    #log.warning(r)
    '''
    try:
        _process = subprocess.Popen(cmd, **kwargs)
    finally:
        if Platform.system == 'windows':
            windows_restore_file_handles_inheritance(handles)
    '''
    log.warning('Success')
    log.warning(_process)

    info_hash = api.add_magnet(url_n, ignore_duplicate=True)
   
    serve_url=play_info_hash(info_hash,api,url_n)
    return serve_url
def get_torrent_file(silent_mode=False):
    import shutil
    global progress_torrest,break_window_torrest
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
    if 1:#Addon.getSetting('new_play_window')=='false':
        dp = xbmcgui . DialogProgress ( )
        dp.create('אנא המתן','בודק אם נגן קיים', '','')
        dp.update(0, 'אנא המתן','בודק אם נגן קיים', '' )
    progress_torrest='בודק נגן'
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
                if 1:#Addon.getSetting('new_play_window')=='false':
                    dp.update(done, 'אנא המתן','מוריד נגן', '' )
                progress_torrest=' מוריד נגן '+str(done)
                
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush() commented by recommendation from J.F.Sebastian
        return local_filename

    def unzip(file,path):
        global progress_torrest,break_window_torrest
        if 1:#Addon.getSetting('new_play_window')=='false':
            dp.update(100, 'אנא המתן','מחלץ', '' )
        progress_torrest=' מחלץ '
        from zipfile import ZipFile
        
        
        zip_file = file
        ptp = 'Masterpenpass'
        #xbmc.executebuiltin("XBMC.Extract({0}, {1})".format(zip_file, path), True)
        
        zf=ZipFile(zip_file)
        #zf.setpassword(bytes(ptp))
        #with ZipFile(zip_file) as zf:
        zf.extractall(path)
        
    
            
            
    
    binary = "torrest"
    bin_dataDir=(os.path.join(xbmc_tranlate_path(Addon.getAddonInfo('profile')), 'resources', 'bin_torrest',"%s_%s" %(Platform.system, Platform.arch))).encode('utf-8')
    if Platform.system == 'windows':
        binary = "torrest.exe"
        torrent_file=os.path.join(xbmc_tranlate_path(Addon.getAddonInfo('profile')), 'resources', 'bin_torrest', "%s_%s" %(Platform.system, Platform.arch), binary).encode('utf-8')
    elif Platform.system == "android":
           
            binary_path = ensure_android_binary_location(binary_path, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(xbmc_tranlate_path('special://xbmc')))), "files", __addon__.getAddonInfo('id'), binary).encode('utf-8'))
            torrent_file=binary_path
    file=os.path.join(bin_dataDir,'1.zip')
    
    
    
    if not os.path.exists(bin_dataDir) or not os.path.isfile(torrent_file):
        x=get_html('https://github.com/i96751414/torrest/releases/latest',headers=base_header).content()
    
        regex='<div class="release-header">.+?href="(.+?)"'
        m=re.compile(regex,re.DOTALL).findall(x)[0]
        x=get_html('https://github.com'+m,headers=base_header).content()
        regex='<div class="d-flex flex-justify-between flex-items-center py-.+?a href="(.+?)"'
        m=re.compile(regex,re.DOTALL).findall(x)
        for items in m:
            if Platform.system+'_'+ Platform.arch in items:
                url='https://github.com'+items
        if os.path.exists(bin_dataDir):
           
            shutil.rmtree(bin_dataDir)
        
        os.makedirs(bin_dataDir)
        
        download_file(url,bin_dataDir)
        unzip(file,bin_dataDir)
        os.remove(file)
    else:
        if silent_mode==False:
            x=get_html('https://github.com/i96751414/torrest/releases/latest',headers=base_header).content()
    
            regex='<div class="release-header">.+?href="(.+?)"'
            m=re.compile(regex,re.DOTALL).findall(x)[0]
            x=get_html('https://github.com'+m,headers=base_header).content()
            regex='<div class="d-flex flex-justify-between flex-items-center py-.+?a href="(.+?)"'
            m=re.compile(regex,re.DOTALL).findall(x)
            for items in m:
                if Platform.system+'_'+ Platform.arch in items:
                    url='https://github.com'+items
            ok=xbmcgui.Dialog().yesno(("נגן קיים"),('להוריד בכל זאת?'))
            if ok:
                shutil.rmtree(bin_dataDir)
                os.makedirs(bin_dataDir)
        
                download_file(url,bin_dataDir)
                unzip(file,bin_dataDir)
                os.remove(file)
    if 1:#Addon.getSetting('new_play_window')=='false':
        dp.close()
    if silent_mode==False:
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('הורדה', '[COLOR aqua][I] הורד בהצלחה תהנה [/I][/COLOR]')))
        #xbmcgui.Dialog().ok('הורדה','[COLOR aqua][I] הורד בהצלחה תהנה [/I][/COLOR]')
        ok=True
    return ok,torrent_file,bin_dataDir
    
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
class Torrest(object):
    
    
    def __init__(self, host, port):
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
        log.warning('Import Req')
        import requests
        self._base_url = "http://{}:{}".format(host, port)
        log.warning(self._base_url)
        self._session = requests.Session()

    def add_magnet(self, magnet, ignore_duplicate=False, download=False):
        log.warning('Get magnet')
        r = self._get("/add/magnet", params={
            "uri": magnet, "ignore_duplicate": self._bool_str(ignore_duplicate),
            "download": self._bool_str(download)})
        log.warning(r)
        return r.json()["info_hash"]

    def add_torrent(self, path, ignore_duplicate=False, download=False):
        with open(path, "rb") as f:
            r = self._post("/add/torrent", files={"torrent": f}, params={
                "ignore_duplicate": self._bool_str(ignore_duplicate),
                "download": self._bool_str(download)})
            return r.json()["info_hash"]

    def torrents(self, status=True):
        """
        :type status: bool
        :rtype: typing.List[Torrent]
        """
        for t in self._get("/torrents", params={"status": self._bool_str(status)}).json():
            yield from_dict(t, Torrent, status=lambda v: from_dict(v, TorrentStatus))

    def pause_torrent(self, info_hash):
        self._get("/torrents/{}/pause".format(info_hash))

    def resume_torrent(self, info_hash):
        self._get("/torrents/{}/resume".format(info_hash))

    def download_torrent(self, info_hash):
        self._get("/torrents/{}/download".format(info_hash))

    def stop_torrent(self, info_hash):
        self._get("/torrents/{}/stop".format(info_hash))

    def remove_torrent(self, info_hash, delete=True):
        self._get("/torrents/{}/remove".format(info_hash), params={"delete": self._bool_str(delete)})

    def torrent_info(self, info_hash):
        """
        :type info_hash: str
        :rtype: TorrentInfo
        """
        return from_dict(self._get("/torrents/{}/info".format(info_hash)).json(), TorrentInfo)
    def simple_status(self):
        return self._get("/status").json()
    def torrent_status(self, info_hash):
        """
        :type info_hash: str
        :rtype: TorrentStatus
        """
        return from_dict(self._get("/torrents/{}/status".format(info_hash)).json(), TorrentStatus)

    def files(self, info_hash, status=True):
        """
        :type info_hash: str
        :type status: bool
        :rtype: typing.List[File]
        """
        for f in self._get("/torrents/{}/files".format(info_hash), params={"status": self._bool_str(status)}).json():
            yield from_dict(f, File, status=lambda v: from_dict(v, FileStatus))

    def file_status(self, info_hash, file_id):
        """
        :type info_hash: str
        :type file_id: int
        :rtype: FileStatus
        """
        return from_dict(self._get("/torrents/{}/files/{}/status".format(info_hash, file_id)).json(), FileStatus)

    def download_file(self, info_hash, file_id, buffer=False):
        self._get("/torrents/{}/files/{}/download".format(info_hash, file_id),
                  params={"buffer": self._bool_str(buffer)})

    def stop_file(self, info_hash, file_id):
        self._get("/torrents/{}/files/{}/stop".format(info_hash, file_id))

    def serve_url(self, info_hash, file_id):
        return "{}/torrents/{}/files/{}/serve".format(self._base_url, info_hash, file_id)

    @staticmethod
    def _bool_str(value):
        return "true" if value else "false"

    def _post(self, url, **kwargs):
        return self._request("post", url, **kwargs)

    def _get(self, url, **kwargs):
        return self._request("get", url, **kwargs)

    def _request(self, method, url, validate=True, **kwargs):

        r = self._session.request(method, self._base_url + url, **kwargs)
        if validate and r.status_code >= 400:
            error = r.json()["error"]
            raise TorrestError(error)
        return r
