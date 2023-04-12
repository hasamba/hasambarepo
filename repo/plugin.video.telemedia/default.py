# -*- coding: utf-8 -*-
import socket,xbmcaddon,os,xbmc,xbmcgui,urllib,urllib,re,xbmcplugin,sys,logging,shutil,time,xbmcvfs,json
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
__addon__ = xbmcaddon.Addon()
import xbmcvfs
from urllib.parse import parse_qsl
xbmc_tranlate_path=xbmcvfs.translatePath

__cwd__ = xbmc_tranlate_path(__addon__.getAddonInfo('path'))
Addon = xbmcaddon.Addon()
from resources.modules import log
from  resources.modules.client import get_html


from threading import Thread
from resources.modules.public import addNolink,addDir3,addLink,lang,user_dataDir
from resources.modules.general import clean_name,check_link,server_data,replaceHTMLCodes,domain_s,similar,cloudflare_request,fix_q,call_trakt,post_trakt,reset_trakt,cloudflare_request,base_header
logo_path=os.path.join(user_dataDir, 'logo')
if not xbmcvfs.exists(logo_path+'/'):
     os.makedirs(logo_path)
icons_path=os.path.join(user_dataDir, 'icons')
if not xbmcvfs.exists(icons_path+'/'):
     os.makedirs(icons_path)
fan_path=os.path.join(user_dataDir, 'fan')
if not xbmcvfs.exists(fan_path+'/'):
     os.makedirs(fan_path)
addon_path=os.path.join(user_dataDir, 'addons')
if not xbmcvfs.exists(addon_path+'/'):
     os.makedirs(addon_path)
addon_extract_path=os.path.join(user_dataDir, 'addons','temp')
if not xbmcvfs.exists(addon_extract_path+'/'):
     os.makedirs(addon_extract_path)
global id,playing_file,seek_time,exit_now
dir_path = os.path.dirname(os.path.realpath(__file__))
telemaia_icon=os.path.join(dir_path,'icon.png')
telemaia_fan=os.path.join(dir_path,'fanart.jpg')
exit_now=0
import random
if Addon.getSetting("debug")=='false':
    try:
        reload(sys)  
        sys.setdefaultencoding('utf8')
    except:
        pass
KIDS_CHAT_ID=-1001251653717
HEBREW_GROUP=-1001106800100
WORLD_GROUP=-1001000750206
id=0
listen_port=Addon.getSetting("port")
seek_time=0
playing_file=False
FMANAGER  = {0:'com.android.documentsui',1:'com.android.documentsui'}[0]
socket.setdefaulttimeout(40.0)
import xml.etree.ElementTree as ET
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
if KODI_VERSION<=18:
    que=urllib.quote_plus
    url_encode=urllib.urlencode
else:
    que=urllib.parse.quote_plus
    url_encode=urllib.parse.urlencode
if KODI_VERSION<=18:
    xbmc_tranlate_path=xbmc_tranlate_path
else:
    import xbmcvfs
    xbmc_tranlate_path=xbmcvfs.translatePath
class OverlayText:
    def __init__(self):
        log.warning('(Overlay) Initialize overlay text')
        x, y, w, h = self._calculate_the_size()

        self._shown       = False
        self._window     = xbmcgui.Window(12005)
        self._label      = xbmcgui.ControlLabel(x, y, w, h, '', alignment=0x00000002 | 0x00000004)
        media_path=os.path.join(xbmc_tranlate_path(Addon.getAddonInfo("path")),'resources','media')
        self._background = xbmcgui.ControlImage(x, y, w, h, os.path.join(media_path, "black.png"))

        self._background.setColorDiffuse("0xD0000000")

    def __enter__(self):
        return self

    def open(self):
        if not self._shown:
            self._window.addControls([self._background, self._label])
            self._shown = True

    def isShowing(self):
        return self._shown

    def setText(self, text):
        if self._shown:
            self._label.setLabel(text)

    def _calculate_the_size(self):
        # get skin resolution
        tree = ET.parse(os.path.join(xbmc_tranlate_path("special://skin/"), "addon.xml"))
        res = tree.findall("./extension/res")[0]
        viewport_w = int(res.attrib["width"])
        viewport_h = int(res.attrib["height"])
        # Adjust size based on viewport, we are using 1080p coordinates
        w = int(int(1920.0 * 0.7) * viewport_w / 1920.0)
        h = int(150 * viewport_h / 1088.0)
        x = int((viewport_w - w) / 2)
        y = int((viewport_h - h) / 2)
        return x, y, w, h

    def __exit__(self, *exc_info):
        self.close()
        return not exc_info[0]

    def __del__(self):
        self.close()

    def close(self):
        if hasattr(self, '_background') and self._shown:
            self._window.removeControls([self._background, self._label])
            self._shown = False



def selection_time_menu(title='',item=''):
    try:
     from  resources.modules import pyxbmct
     class selection_time(pyxbmct.AddonDialogWindow):
        
        def __init__(self, title='',item=''):
           
            super(selection_time, self).__init__(title)
            #'Play from beginning'
            self.item=[item,Addon.getLocalizedString(32043)]
            self.setGeometry(350, 150,1, 1,pos_x=700, pos_y=200)
            self.list_index=-1

            self.clicked=0
            
            self.set_active_controls()
            self.set_navigation()
            # Connect a key action (Backspace) to close the window.
            self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        def get_selection(self):
            """ get final selection """
            return self.list_index
        def click_list(self):
            self.clicked=1
            self.list_index=self.list.getSelectedPosition()
           
            self.close()
        
        def set_active_controls(self):
         
          
            # List
            self.list = pyxbmct.List()
            self.placeControl(self.list, 0,0,  rowspan=2, columnspan=1)
            # Add items to the list
            
           
            self.list.addItems(self.item)
            
            # Connect the list to a function to display which list item is selected.
            self.connect(self.list, self.click_list)
            
           

        def set_navigation(self):
            
            self.setFocus(self.list)

        

        

        def setAnimation(self, control):
            # Set fade animation for all add-on window controls
            control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=50',),
                                    ('WindowClose', 'effect=fade start=100 end=0 time=50',)])
     window = selection_time(title,item)
     window.doModal()
     selection = window.get_selection()
     clicked=window.clicked
     del window
     return selection,clicked
    except:
        pass

def clear_files():
    user_path=xbmc_tranlate_path(Addon.getSetting("files_folder"))
    log.warning(user_path)
    temp_path=os.path.join(user_path, 'files')
    if (user_dataDir!=user_path):
        
        all_folders=[temp_path,user_path]
    else:
        all_folders=[temp_path]
    try:
        for items in all_folders:
            db_path=os.path.join(items, 'temp')
            if os.path.exists(db_path):
                onlyfiles = [f for f in os.listdir(db_path) if os.path.isfile(os.path.join(db_path, f))]
                
                for fl in onlyfiles:
                    #dp.update(0, 'Please Wait...','Removing File', fl )
                    re_fl=os.path.join(db_path,fl)
                    
                    if os.path.exists(re_fl):
                      try:
                        os.remove(re_fl)
                      except Exception as e:
                        log.warning('Err:'+str(e))
                        pass
            
                        
            db_path=os.path.join(items, 'documents')
            if os.path.exists(db_path):
                onlyfiles = [f for f in os.listdir(db_path) if os.path.isfile(os.path.join(db_path, f))]
                for fl in onlyfiles:
                    #dp.update(0, 'Please Wait...','Removing File', fl )
                    re_fl=os.path.join(db_path,fl)
                    if os.path.exists(re_fl):
                      try:
                        os.remove(re_fl)
                      except:
                        pass
            
            db_path=os.path.join(items, 'videos')
            if os.path.exists(db_path):
                onlyfiles = [f for f in os.listdir(db_path) if os.path.isfile(os.path.join(db_path, f))]
                for fl in onlyfiles:
                    #dp.update(0, 'Please Wait...','Removing File', fl )
                    re_fl=os.path.join(db_path,fl)
                    if os.path.exists(re_fl):
                      try:
                        os.remove(re_fl)
                      except:
                        pass
            db_path=os.path.join(items, 'photos')
            if os.path.exists(db_path):
                onlyfiles = [f for f in os.listdir(db_path) if os.path.isfile(os.path.join(db_path, f))]
                for fl in onlyfiles:
                    #dp.update(0, 'Please Wait...','Removing File', fl )
                    re_fl=os.path.join(db_path,fl)
                    if os.path.exists(re_fl):
                      try:
                        os.remove(re_fl)
                      except:
                        pass
            db_path=os.path.join(items, 'music')
            if os.path.exists(db_path):
                onlyfiles = [f for f in os.listdir(db_path) if os.path.isfile(os.path.join(db_path, f))]
                for fl in onlyfiles:
                    #dp.update(0, 'Please Wait...','Removing File', fl )
                    re_fl=os.path.join(db_path,fl)
                    if os.path.exists(re_fl):
                      try:
                        os.remove(re_fl)
                      except:
                        pass
    except Exception as e:
        log.warning('Error removing files:'+str(e))

    
def is_hebrew(input_str):    
       try:
        import unicodedata
        input_str=input_str.replace(' ','').replace('\n','').replace('\r','').replace('\t','').replace(' ','')
        nfkd_form = unicodedata.normalize('NFKD', input_str.replace(' ','').replace('\n','').replace('\r','').replace('\t','').replace(' ',''))
        a=False
        for cha in input_str:
            
            a='HEBREW' in unicodedata.name(cha.strip())
            if a:
                break
        return a
       except:
            return True
        
class TelePlayer(xbmc.Player):
    def __init__(self, *args, **kwargs):
       
        self.g_timer=0
        self.g_item_total_time=0
        xbmc.Player.__init__(self)
        
    def onPlayBackStarted(self):
        global id,playing_file
        self.g_timer=0
        log.warning('(Tele Player) onPlayBackStarted')
        playing_file=True
    def onPlayBackResumed(self):
        global id,playing_file
        log.warning('(Tele Player) onPlayBackResumed')
        playing_file=True

    def onPlayBackPaused(self):
        global id,playing_file
        log.warning('(Tele Player) onPlayBackPaused')
        playing_file=True
    def onPlayBackEnded(self):
        global id,playing_file
        log.warning('(Tele Player) Ended playback')
        num=random.randint(0,60000)
        data={'type':'td_send',
             'info':json.dumps({'@type': 'cancelDownloadFile','file_id':int(id), '@extra': num})
             }
        event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
        
        
        playing_file=False
        
        log.warning('playing_file1')
    def update_db(self):
        log.warning('Self.TMDB:'+str(self.tmdb))
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        self.dbcon = database.connect(cacheFile)
        self.dbcur = self.dbcon.cursor()
        self.dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
        self.dbcon.commit()
        self.season=self.season.replace('%20','0').replace(' ','0')
        self.episode=self.episode.replace('%20','0').replace(' ','0')
        if len(str(self.tmdb))<2 and tmdb!='%20':
            only_name=True
            self.dbcur.execute("SELECT * FROM playback where name='%s' and season='%s' and episode='%s'"%(self.saved_name.replace("'","%27"),self.season,self.episode))
        else:
            only_name=False
            self.dbcur.execute("SELECT * FROM playback where tmdb='%s' and season='%s' and episode='%s'"%(self.tmdb,self.season,self.episode))
        match = self.dbcur.fetchall()
        
        
        if match==None:
          self.dbcur.execute("INSERT INTO playback Values ('%s','%s','%s','%s','%s','%s','%s');" %  (self.saved_name.replace("'","%27"),self.tmdb,self.season,self.episode,str(self.g_timer),str(self.g_item_total_time),' '))
          self.dbcon.commit()
        else:
           if len(match)>0:
            name,timdb,season,episode,playtime,totaltime,free=match[0]
            if str(self.g_timer)!=playtime:
                if only_name:
                    self.dbcur.execute("UPDATE playback SET playtime='%s' where name='%s' and  season='%s' and episode='%s'"%(str(self.g_timer),self.saved_name.replace("'","%27"),self.season,self.episode))
                else:
                    self.dbcur.execute("UPDATE playback SET playtime='%s' where tmdb='%s' and  season='%s' and episode='%s'"%(str(self.g_timer),self.tmdb,self.season,self.episode))
                self.dbcon.commit()
           else:
                self.dbcur.execute("INSERT INTO playback Values ('%s','%s','%s','%s','%s','%s','%s');" %  (self.saved_name.replace("'","%27"),self.tmdb,self.season,self.episode,str(self.g_timer),str(self.g_item_total_time),' '))
                self.dbcon.commit()
        self.dbcur.close()
        self.dbcon.close()
    def onPlayBackStopped(self):
        global id,playing_file
        log.warning('(Tele Player) Stop playback')
        num=random.randint(0,60000)
        data={'type':'td_send',
             'info':json.dumps({'@type': 'cancelDownloadFile','file_id':int(id), '@extra': num})
             }
        event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
        
        
        playing_file=False
        
        log.warning('playing_file2')
    '''
    def onPlayBackSeek(self, time, seekOffset):
        global id,playing_file
        log.warning('SEEK FOUND')
        self.pause()
       
        log.warning('vidtime:'+str(seekOffset))
        
        td_send({'@type': 'downloadFile','file_id':int(id), 'priority':1,'offset':seekOffset,'limit':0, '@extra': 777.999})
        event=wait_response(777.999)
        playing_file=True
        self.play()
    '''
    def download_buffer(self):
        try:
            buffer_size=long(Addon.getSetting("buffer_size_new"))*1000000
            global id,playing_file
            dp = xbmcgui.DialogProgress()
            
            dp.create('Telemedia', '[B][COLOR=yellow]%s[/COLOR][/B]'%Addon.getLocalizedString(32044))
            num=random.randint(0,60000)
            data={'type':'td_send',
             'info':json.dumps({'@type': 'downloadFile','file_id':int(id), 'priority':2,'offset':(994694350-(993165312)),'limit':994694350, '@extra': num})
             }
            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            
            j_enent_o=(event)
            
           
            
            j_enent_o=(event)
            once=True
            while True:
                data={'type':'listen',
                 'info':''
                 }
                event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
               
                #event = td_receive()
                
                if dp.iscanceled():
                    try:
                        self.path=event['file']['local']['path']
                    except: 
                        self.path=''
                        pass
                    break
                if self.stop==1:
                    break
                if event:
                    
                    if event.get('@type') =='error':
               
                        xbmcgui.Dialog().ok('Error occurred',str(event.get('message')))
                        break
                    
                        
                        
                    if 'updateFile' in event['@type']:
                        
                        dp.update(int((event['file']['local']['downloaded_prefix_size']*100.0)/buffer_size),'[B][COLOR=green]%s[/COLOR][/B]'%self.saved_name, '[B][COLOR=yellow]%s %s/%s[/COLOR][/B]'%(Addon.getLocalizedString(32045),str(event['file']['local']['downloaded_prefix_size']),str(buffer_size)))
                        if len(event['file']['local']['path'])>0 and event['file']['local']['downloaded_prefix_size']>(0x500):
                            size=event['file']['size']
                           
                            break
                xbmc.sleep(10)
            dp.close()
        except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            log.warning('ERROR IN Main:'+str(lineno))
            log.warning('inline:'+str(line))
            log.warning(str(e))
            xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
    def download_file(self,dp):
        try:
            buffer_size_d=int(Addon.getSetting("buffer_size_new"))*1000000
            buffer_size=buffer_size_d
            global id,playing_file
           
            dp.create('Telemedia', '[B][COLOR=yellow]%s[/COLOR][/B]'%Addon.getLocalizedString(32044))
            num=random.randint(0,60000)
            start = time.time()
            data={'type':'td_send',
             'info':json.dumps({'@type': 'downloadFile','file_id':int(id), 'priority':1,'offset':0,'limit':0, '@extra': num})
             }
            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            do_buffer=True
            if 'expected_size' in event :
                log.warning('Found Complete')
                if len(event['local']['path'])>0 and  (event['local']['is_downloading_completed']==True):
                    do_buffer=False
                    self.path='Done'
            if 'size' in event:
                if event['size']==0:
                    do_buffer=False
                    self.path='Stop'
                    
            log.warning('do_buffer'+str(do_buffer))
            if do_buffer:
                log.warning(json.dumps(event))
                if 'size' in event:
                
                    if buffer_size>=event['size']:
                            buffer_size=event['size']-1000
                            
                    j_enent_o=(event)
                    
                    
                    
                    j_enent_o=(event)
                    
                    while True:
                        data={'type':'get_file_size',
                         'info':id
                         }
                        event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
                        
                        if 'path' in event:
                            path=event['path']
                            file_size=event['file_size']
                            
                            if dp.iscanceled():
                                try:
                                    self.path='Done'
                                except: 
                                    self.path=''
                                    pass
                                break
                            
                            if file_size!=0:
                                
                               
                                    speed=int((file_size//(time.time() - start)))
                                    t_remiain=(buffer_size_d-file_size)/speed
                                    if KODI_VERSION<19:
                                        dp.update(int((file_size*100.0)/buffer_size),'[B][COLOR=green]%s[/COLOR][/B]'%self.saved_name, '[B][COLOR=yellow]%s %s/%s[/COLOR][/B]'%(Addon.getLocalizedString(32045),str(file_size),str(buffer_size)),str(round(speed/(1024),2))+' Kbps / '+str(t_remiain)+' sec')
                                    else:
                                        dp.update(int((file_size*100.0)/buffer_size),'[B][COLOR=green]%s[/COLOR][/B]'%self.saved_name+'\n'+ '[B][COLOR=yellow]%s %s/%s[/COLOR][/B]'%(Addon.getLocalizedString(32045),str(round(file_size,2)),str(round(buffer_size,2)))+'\n'+str(round(speed/(1024),2))+' Kbps / '+str(round(t_remiain,2))+' sec')
                                    if len(path)>0 and int(file_size)>=buffer_size:
                                        self.path=path
                                        break
                    xbmc.sleep(10)
                else:
                    self.path='Done'
                    xbmcgui.Dialog().ok('Error occurred',str(event))
                data={'type':'kill_file_size',
                     'info':id
                     }
                event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            #dp.close()
        except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            log.warning('ERROR IN Main:'+str(lineno))
            log.warning('inline:'+str(line))
            log.warning(str(e))
            xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
            self.path='Done'
    def get_resume(self):
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        self.dbcon = database.connect(cacheFile)
        self.dbcur = self.dbcon.cursor()
        self.dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
        self.dbcon.commit()
        if len(str(self.tmdb))>2 and self.tmdb!='%20':
            self.dbcur.execute("SELECT * FROM playback where tmdb='%s' and season='%s' and episode='%s'"%(self.tmdb,str(self.season).replace('%20','0').replace(' ','0'),str(self.episode).replace('%20','0').replace(' ','0')))
            
        else:
            self.dbcur.execute("SELECT * FROM playback where name='%s' and season='%s' and episode='%s'"%(self.saved_name.replace("'","%27"),str(self.season).replace('%20','0').replace(' ','0'),str(self.episode).replace('%20','0').replace(' ','0')))
       
        match_playtime = self.dbcur.fetchone()
        if match_playtime!=None:

            name_r,timdb_r,season_r,episode_r,playtime,totaltime,free=match_playtime
            res={}
            res['wflag']=False
            res['resumetime']=playtime
            res['totaltime']=totaltime
        else:
            res=False
            
        set_runtime=0
        if res:
            if not res['wflag']:

                if res['resumetime']!=None:

                    #'Resume From '
                    choose_time=Addon.getLocalizedString(32042)+time.strftime("%H:%M:%S", time.gmtime(float(res['resumetime'])))
                    log.warning('choose_time')
                    log.warning(choose_time)
                    if float(res['resumetime'])>=(0.98*(float(res['totaltime']))):
                        selection=1
                        clicked=1
                    else:
                        selection,clicked=selection_time_menu('Menu',choose_time)
                        #window = selection_time('Menu',choose_time)
                        #window.doModal()
                        #selection = window.get_selection()
                        #clicked=window.clicked
                        #del window
                    if clicked==0:
                        return -1
                    if selection==-1:
                       stop_auto_play=1
                       
                       return 0
                    if selection==0:
                        
                        set_runtime=float(res['resumetime'])
                        set_total=res['totaltime']
                        
                        
                    elif selection==1:
                        
                        
                        set_runtime=0
                        set_total=res['totaltime']
        self.dbcur.close()
        self.dbcon.close()
        return set_runtime
    def playTeleFile(self, id_pre,data,name,no_subs,tmdb,season,episode,original_title,description,resume,l_data,iconimage='',fanart='',r_art='',r_logo=''):
      try:
        dp = xbmcgui . DialogProgress ( )
        dp.create('Telemedia', '[B][COLOR=yellow]%s[/COLOR][/B]'%Addon.getLocalizedString(32044))
        try:
            cond=xbmc.Monitor().abortRequested()
        except:
            cond=xbmc.abortRequested
        self.tmdb=tmdb
        self.saved_name=name
        log.warning('self.saved_name:'+self.saved_name)
        self.season=season
        self.episode=episode
        global id,playing_file,seek_time
        try:
            dialog = xbmcgui.DialogBusy()
            dialog.create()
        except:
            pass
        id=id_pre
        self.stop=0
        self.path=''
        
        
        link=('http://127.0.0.1:%s/'%listen_port)+id
        if 1:#Addon.getSetting("pre_buffer")=='true':
            
            t = Thread(target=self.download_file, args=(dp,))
            t.start()


            count_timeout=0
            while self.path=='' :
                xbmc.sleep(10)
                count_timeout+=1
                if (count_timeout>1000):
                    break
            
        if self.path=='Stop':
            xbmcgui.Dialog().ok('Error occurred','קובץ לא תקין')
            return 'Not ok'
        listItem = xbmcgui.ListItem(name, path=link) 
        #listItem.setProperty('inputstreamaddon', 'inputstream.adaptive')
        #listItem.setProperty('inputstream.adaptive.manifest_type', 'hls')
        
        video_data={}
        log.warning('season:'+str(season))
        if season!=None and season!="%20" and season!="0":
           video_data['TVshowtitle']=original_title.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
           video_data['mediatype']='tvshow'
           
        else:
           video_data['mediatype']='movies'
        if season!=None and season!="%20" and season!="0":
           tv_movie='tv'
           url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&append_to_response=external_ids'%(tmdb,'653bb8af90162bd98fc7ee32bcbbfb3d')
        else:
           tv_movie='movie'
           
           url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&append_to_response=external_ids'%(tmdb,'653bb8af90162bd98fc7ee32bcbbfb3d')
        if 'tt' not in tmdb:
             try:
                
                
                imdb_id=get_html(url2).json()['external_ids']['imdb_id']
                
             except Exception as e:
                log.warning('IMDB err:'+str(e))
                imdb_id=" "
        else:
             imdb_id=tmdb
        

        
        if 'Music File' in description:
            types='music'
            video_data['title']=name
        else:
            types='Video'
            if '@' in name and '.' in name:
                nm=name.split('.')
                ind=0
                for items in nm:
                    if '@' in items:
                        nm.pop(ind)
                    ind+=1
                name='.'.join(nm)
            video_data['title']=name.replace('.mkv','').replace('.avi','').replace('.mp4','')
            log.warning('New Name:'+name)
            video_data['Writer']=tmdb
            video_data['season']=season
            video_data['episode']=episode
            video_data['plot']=description+'from_telemedia'
            video_data['imdb']=imdb_id
            video_data['code']=imdb_id

            video_data['imdbnumber']=imdb_id
            
            video_data['imdb_id']=imdb_id
            video_data['IMDBNumber']=imdb_id
            video_data['genre']=imdb_id
            video_data['OriginalTitle']=original_title.replace('.mkv','').replace('.avi','').replace('.mp4','')
            log.warning('New Name Hebrew:'+str(name))
           
            if no_subs=='1' or is_hebrew(str(name)):
                video_data[u'mpaa']=str('heb')
        
        listItem.setInfo(type=types, infoLabels=video_data)
        listItem.setArt({'clearlogo':r_logo,'clearart':r_art,'icon': iconimage, 'thumb': iconimage, 'poster': iconimage,'tvshow.poster': iconimage, 'season.poster': iconimage})
        if not resume:
            resume_time=self.get_resume()
        else:
            resume_time=resume
        broken_play=True
        resume_time=float(resume_time)
        if resume_time!=-1:
            
            self.play(link,listitem=listItem,windowed=False)
            
            #Waiting for play
            #Please Wait
            
            if KODI_VERSION<19:
                dp.create(self.saved_name+'...',Addon.getLocalizedString(32040), '' )
            else:
                dp.create(self.saved_name+'...',Addon.getLocalizedString(32040))
            
            w_time=int(Addon.getSetting("wait_size"))
            
            for _ in range(w_time):
                if KODI_VERSION<19:
                    dp.update(0,self.saved_name+'...',Addon.getLocalizedString(32040), str(_) )
                else:
                    dp.update(0,self.saved_name+'...'+'\n'+Addon.getLocalizedString(32040)+'\n'+ str(_) )
                try:
                    vidtime = self.getTime()
                except:
                    vidtime=0
                    pass
                if self.isPlaying() and vidtime>0:
                    broken_play=False
                    
                    break
                if dp.iscanceled():
                    dp.close()
                    broken_play=False
                   
                    break
                time.sleep(0.100)
            
            
            if not broken_play:
                try:
                    xbmcgui.DialogBusy().close() 
                except:
                    pass
                xbmc.executebuiltin("Dialog.Close(busydialog)")
            
                
            self.path=''
            
            if resume_time>0:
                try:
                    self.seekTime(int(float(resume_time)))
                except Exception as e:
                    log.warning('Seek Err:'+str(e))
                    pass
            dp.close()
            if not broken_play:
                
                with OverlayText() as self._overlay:
                  while (not cond) and (self.isPlaying()):
                     try:
                        vidtime = self.getTime()
                     except:
                        vidtime = 0
                     try:
                        self.g_timer=xbmc.Player().getTime()
                        self.g_item_total_time=xbmc.Player().getTotalTime()
                     except:
                        pass
                     
                     if  xbmc.getCondVisibility('Player.Seeking') or xbmc.getCondVisibility('Player.Caching'):
                        self._overlay.open()
                     else:
                        self._overlay.close()
                     if 0:#self._overlay.isShowing():
                            data={'type':'get_file_size',
                             'info':id
                             }
                            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
                            
                            
                            needed_size=self.g_timer*(int(event['total_size'])/(self.g_item_total_time))
                            
                            show_str='הורדה: '+str(event['downloaded'])+', גודל: '+str(event['total_size'])+', דרוש: '+str(needed_size)
                            ready_size=event['downloaded']
                            
                            
                            self._overlay.setText('אנא המתן לטעינה \n'+show_str)
                            
                                
                            time.sleep(0.100)
                            
                            continue
                     time.sleep(0.1)
            else:
                log.warning('Sending 404')
                data={'type':'stop_now',
                     'info':''
                     }
                event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
        #dp.create('Please Wait...','Closing File', '','')
        #dp.update(0, 'Please Wait...','Canceling File', '' )
        log.warning('(Tele Player) The playback has stop222')
        log.warning('(Tele Player) STOPED')
        self.stop=1
        num=random.randint(0,60000)
        data={'type':'td_send',
             'info':json.dumps({'@type': 'cancelDownloadFile','file_id':int(id), '@extra': num})
             }
        event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
        
        #dp.update(0, 'Please Wait...','Removing File', '' )
        if resume_time!=-1:
            self.update_db()
        time.sleep(1)
        clear_files()
        playing_file=True
        #dp.close()
        return broken_play,resume_time
      except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            log.warning('ERROR IN Main:'+str(lineno))
            log.warning('inline:'+str(line))
            log.warning(str(e))
            xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
       
            
        
        
def get_params():
        param=[]
        if len(sys.argv)>=2:
          paramstring=sys.argv[2]
          if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param     

def download_photo(id,counter,f_name,mv_name):
   try:
    
    log.warning('mv_name:'+mv_name)
    #if xbmcvfs.exists(mv_name):
    #    return mv_name
    log.warning('mv_name Not found:'+mv_name)
    data={'type':'download_photo',
             'info':id
             }
    log.warning('Sending')
    file=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    log.warning('file:'+file)
    xbmc.sleep(100)
    if xbmcvfs.exists(file):
        try:
            shutil.move(file,mv_name)
        except Exception as e:
            log.warning('File copy err:'+str(e))
            pass
        
    else :
        log.warning('File not found')
        return 'None'
    
    return mv_name
   except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        log.warning('ERROR IN Photo:'+str(lineno))
        log.warning('inline:'+str(line))
        log.warning(str(e))
        xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia ERR','Err:'+str(e)+'Line:'+str(lineno)))

        return ''


def infiniteReceiver(all_d,last_id,archive='chatListMain',chat_filter_id='0',next_page='0'):
   global exit_now
   try:
    log.warning('next_page:'+str(next_page))
    log.warning('sending')
    dp = xbmcgui . DialogProgress ( )
    if KODI_VERSION<19:
        dp.create('Please Wait...','Adding Groups', '','')
        dp.update(0, 'Please Wait...','Adding Groups', '' )
    else:
        dp.create('Please Wait...'+'\n'+ 'Adding Groups'+'\n'+ ''+'\n'+ '')
        dp.update(0, 'Please Wait...'+'\n'+ 'Adding Groups'+'\n'+  '' )
    num=random.randint(0,60000)
    order=last_id.split('$$$')[1]
    leid=last_id.split('$$$')[0]
    
    if chat_filter_id=='0':
        data={'type':'td_send',
             'info':json.dumps({'@type': 'getChats','offset_chat_id':leid,'offset_order':order, 'limit': '15000','chat_list':{'@type': archive}, '@extra': num})
             }
    else:
        data={'type':'td_send',
             'info':json.dumps({'@type': 'getChats','offset_chat_id':leid,'offset_order':order, 'limit': '15000','chat_list':{'@type': 'chatListFilter','chat_filter_id':int(chat_filter_id)}, '@extra': num})
             }
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    xbmc.sleep(1000)
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    exit_now=0
   
    if 'status' in event:
        xbmcgui.Dialog().ok('Error occurred',event['status'])
        exit_now=1
    if exit_now==0:
       

        
        
        counter=0
        counter_ph=10000
    
        j_enent_o=(event)
        zzz=0
        items=''
        next_page=int(next_page)
        start_value=next_page*100
        
        log.warning('start_value:'+str(start_value))
        next_page_exist=False
        len_size=len(j_enent_o['chat_ids'])
        if len_size>100:
            len_size=100
        for items in j_enent_o['chat_ids']:
            log.warning('counter:'+str(counter))
            counter+=1
            if (counter<start_value):
                continue
               
            if (counter>(start_value+100)):
                next_page_exist=True
                break
            
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'getChat','chat_id':items, '@extra':counter})
                 }
            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            log.warning(json.dumps(event))
            if 'status' in event:
                xbmcgui.Dialog().ok('Error occurred',event['status'])
                exit_now=1
                break
            
            order=''
            try:
                order=event['positions'][0]['order']
            except:
                pass
            
            if dp.iscanceled():
                          dp.close()
                         
                          break
            j_enent=(event)
            if KODI_VERSION<19:
                dp.update(int(((zzz* 100.0)/(len_size)) ), 'Please Wait...','Adding Groups', j_enent['@type'].encode('utf8') )
            else:
                dp.update(int(((zzz* 100.0)/(len_size)) ), 'Please Wait...'+'\n'+'Adding Groups'+'\n'+ j_enent['@type'] )
            if j_enent['@type']=='chat' and len(j_enent['title'])>1:
                
                icon_id=''
                fan_id=''
                fanart=''
                icon=''
                name=j_enent['title']
                log.warning(name+':'+str(items))
                
                color='white'
                if 'is_channel' in j_enent['type']:
                    if j_enent['type']['is_channel']==False:
                        
                        genere='Chat'
                        color='lightblue'
                    else:
                        genere='Channel'
                        color='khaki'
                else:
                     genere=j_enent['type']['@type']
                     color='lightgreen'
                if 'last_message' in j_enent:
                    plot=name
                    pre=j_enent['last_message']['content']
               
                    if 'caption' in pre:
                        plot=j_enent['last_message']['content']['caption']['text']
                    elif 'text' in pre:
                        if 'text' in pre['text']:
                            plot=j_enent['last_message']['content']['text']['text']
                    
                        
                else:
                    plot=name
                if KODI_VERSION<19:
                    dp.update(int(((zzz* 100.0)/(len_size)) ), 'Please Wait...','Adding Groups', name.encode('utf8') )
                else:
                    dp.update(int(((zzz* 100.0)/(len_size)) ), 'Please Wait...'+'\n'+ 'Adding Groups'+'\n'+ name)
                zzz+=1
             
                if 'photo' in j_enent:
                   
                   if 'small' in j_enent['photo']:
                     counter_ph+=1
                     icon_id=j_enent['photo']['small']['id']
                     f_name=str(j_enent['id'])+'_small.jpg'
                     mv_name=os.path.join(logo_path,f_name)
                     if os.path.exists(mv_name):
                        icon=mv_name
                     else:
                        icon=download_photo(icon_id,counter_ph,f_name,mv_name)
                   if 'big' in j_enent['photo']:
                     counter_ph+=1
                     fan_id=j_enent['photo']['big']['id']
                     f_name=str(j_enent['id'])+'_big.jpg'
                     mv_name=os.path.join(logo_path,f_name)
                     if os.path.exists(mv_name):
                        fanart=mv_name
                     else:
                        fanart=download_photo(fan_id,counter_ph,f_name,mv_name)
                mode=2
                last_id_fixed='0$$$0$$$0$$$0'
                
                if 'group links' in name.lower() or 'ערוץ קישורים' in name or 'קישורים לכל הקבוצות' in name:
                    mode=38
                    color='olive'
                    last_id_fixed='0'
                #log.warning(name)
                #log.warning(j_enent_o['chat_ids'])
                
                aa=addDir3('[COLOR %s]'%color+name+'[/COLOR]',str(items),mode,icon,fanart,plot+'\nfrom_plot',generes=genere,data='0',last_id=last_id_fixed,image_master=icon+'$$$'+fanart,menu_leave=True,original_title=name)
                all_d.append(aa)
            
    log.warning('close dp')
    if items!='' and next_page_exist:
        last_id=str(items)+'$$$'+str(order)
        log.warning('last_id:'+str(last_id))
        aa=addDir3('[COLOR blue]'+Addon.getLocalizedString(32026)+'[/COLOR]',archive,12,'https://sitechecker.pro/wp-content/uploads/2017/12/search-engines.png','https://www.komando.com/wp-content/uploads/2017/12/computer-search.jpg','Next',data='all',last_id=last_id,next_page=str(int(next_page+1)))
        all_d.append(aa)
    log.warning('close dp1')
    dp.close()
    return all_d
   except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        log.warning('ERROR IN Main:'+str(lineno))
        log.warning('inline:'+str(line))
        log.warning(str(e))
        xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
def my_groups(last_id,url,groups_id,next_page):
    log.warning('Start Main')
    if Addon.getSetting("first_time")=='true':
        num=random.randint(1,1001)
        data={'type':'td_send',
         'info':json.dumps({'@type': 'searchPublicChat', 'username': '@MyTelegraMediaGroups', '@extra': num})
         }
        event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
        data={'type':'td_send',
         'info':json.dumps({'@type': 'joinChat', 'chat_id': event['id'], '@extra': num})
         }
        event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
        invite_link='https://t.me/joinchat/AAAAAFbGe4DAnVWs3bsI3Q'
        num=random.randint(1,1001)
        data={'type':'td_send',
                     'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': invite_link, '@extra': num})
                     }
        event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
        Addon.setSetting('first_time','false')
        xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', 'Added groups OK'))
    try:
        
        all_d=[]
        aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32024)+'[/COLOR]',str(id),6,'https://sitechecker.pro/wp-content/uploads/2017/12/search-engines.png','https://www.komando.com/wp-content/uploads/2017/12/computer-search.jpg','Search All',last_id='0$$$0',data='all')
        all_d.append(aa)
        all_d=infiniteReceiver(all_d,last_id,archive=url,chat_filter_id=groups_id,next_page=next_page)
        log.warning('close dp2')
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
    except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        log.warning('ERROR IN Main:'+str(lineno))
        log.warning('inline:'+str(line))
        log.warning(str(e))
        xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
def main_menu():
    log.warning('Start Main')
    data={'type':'checklogin',
         'info':''
         }
    
    try:
        event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    except:
        xbmcgui.Dialog().ok(Addon.getLocalizedString(32052),'טלמדיה עדיין לא מחובר ... המתן קטנה')
        return ''
    log.warning(event)
    
    all_d=[]
    if 'status' not in event:
        xbmcgui.Dialog().ok(Addon.getLocalizedString(32052),'שגיאה\n'+str(event))
        return ''
    if event['status']==2 or event['status']=='Needs to log from setting':
        #Movies
        aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32020)+'[/COLOR]',str(id),10,'https://image.tmdb.org/t/p/w500_and_h282_face/jOzrELAzFxtMx2I4uDGHOotdfsS.jpg','https://image.tmdb.org/t/p/w500_and_h282_face/jOzrELAzFxtMx2I4uDGHOotdfsS.jpg','Movies')
        all_d.append(aa)
        #Tv Shows
        aa=addDir3('[COLOR blue]'+Addon.getLocalizedString(32021)+'[/COLOR]',str(id),11,'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQ48ZyMr013iwx2gXtSBm9iAcSkxv5ue5eJ16DEPXLCckXGcVRa','https://www.fanthatracks.com/wp-content/uploads/2019/08/themandalorian_disneyplus_SM_poster_cover.jpg','Tv Shows')
        all_d.append(aa)
        addNolink( '[COLOR lightgreen]%s[/COLOR]'%Addon.getLocalizedString(32001), 'www',5,False,fan="https://www.theseanamethod.com/wp-content/uploads/2017/01/login-570317_1280.jpg", iconimage="https://achieve.lausd.net/cms/lib/CA01000043/Centricity/domain/779/welligentbuttons/login.png")
        addNolink( '[COLOR red]%s[/COLOR]'%Addon.getLocalizedString(32019), 'www',21,False,fan="https://i.ytimg.com/vi/XlzVOc21PgM/maxresdefault.jpg", iconimage="https://pbs.twimg.com/profile_images/557854031930867712/cTa_aSs_.png")
        
        #xbmc.executebuiltin('Container.Refresh')
    else:
        if Addon.getSetting("autologin")=='false':
            Addon.setSetting('autologin','true')
            #search_updates()
        #addNolink( '[COLOR lightgreen]%s[/COLOR]'%Addon.getLocalizedString(32001), 'www',5,False,fan="https://www.theseanamethod.com/wp-content/uploads/2017/01/login-570317_1280.jpg", iconimage="https://achieve.lausd.net/cms/lib/CA01000043/Centricity/domain/779/welligentbuttons/login.png")
        #addNolink( '[COLOR lightgreen]Logout[/COLOR]', 'www',99,False,fan='https://miro.medium.com/max/800/1*peMgcGzIdn5O36ecjwrKxw.jpeg', iconimage="https://previews.123rf.com/images/faysalfarhan/faysalfarhan1711/faysalfarhan171154303/89754008-logout-isolated-on-elegant-brown-round-button-abstract-illustration.jpg")
        #Movies
        aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32020)+'[/COLOR]',str(id),10,'special://home/addons/plugin.video.telemedia/tele/movies.png','https://www.ubackground.com/_ph/22/269562231.jpg','Movies')
        all_d.append(aa)
        #Tv Shows
        aa=addDir3('[COLOR blue]'+Addon.getLocalizedString(32021)+'[/COLOR]',str(id),11,'special://home/addons/plugin.video.telemedia/tele/tvshows.png','https://static.highsnobiety.com/thumbor/R8JPAdy4hlfFhZj9_YqCQfcNsZ0=/fit-in/800x480/smart/static.highsnobiety.com/wp-content/uploads/2019/02/28155224/game-of-thrones-season-8-posters-001.jpg','Tv Shows')
        all_d.append(aa)
        aa=addDir3('[COLOR blue]'+Addon.getLocalizedString(32073)+'[/COLOR]','www',31,'special://home/addons/plugin.video.telemedia/tele/kids.png','https://insidethemagic-119e2.kxcdn.com/wp-content/uploads/2018/08/Expo19_11x16_Poster_KeyArt_72dpi-1-792x400.jpg',Addon.getLocalizedString(32073),data=KIDS_CHAT_ID)
        all_d.append(aa)
        #My Groups
        aa=addDir3('[COLOR blue]'+Addon.getLocalizedString(32022)+'[/COLOR]','chatListMain',12,'special://home/addons/plugin.video.telemedia/tele/mygroups.png','https://wallup.net/wp-content/uploads/2016/10/12/137743-jumping-silhouette-group_of_people-cat-sea-reflection.jpg','My Groups',last_id='0$$$9223372036854775807')
        all_d.append(aa)
        aa=addDir3('[COLOR blue]'+Addon.getLocalizedString(32138)+'[/COLOR]','chatListArchive',12,'special://home/addons/plugin.video.telemedia/tele/archive.png','https://hdwallpaperim.com/wp-content/uploads/2017/08/23/471244-Brandon_Sanderson-Stormlight_Archives.jpg','My Groups',last_id='0$$$9223372036854775807')
        all_d.append(aa)
        aa=addDir3('[COLOR blue]'+Addon.getLocalizedString(32141)+'[/COLOR]','chatListArchive',121,'special://home/addons/plugin.video.telemedia/tele/folder.png','https://www.fuzebranding.com/wp-content/uploads/2018/06/Fuze-Branding-Fun-Pastel-Desktop-Wallpapers-To-Help-You-Stay-Organized.jpg','My Folders')
        all_d.append(aa)
        aa=addDir3('[COLOR white]'+Addon.getLocalizedString(32027)+'[/COLOR]',str(id),113,'special://home/addons/plugin.video.telemedia/tele/search.png','https://seleritysas.com/wp-content/uploads/2019/12/shutterstock_606583169.jpg','Search All',last_id='0$$$0',data='all')
        all_d.append(aa)
        # #Search Groups
        # aa=addDir3('[COLOR white]'+Addon.getLocalizedString(32023)+'[/COLOR]',str(id),13,'https://pageloot.com/wp-content/uploads/elementor/thumbs/make-qr-codes-for-telegram-groups-o75hxtbe6pqtp9qokn9gy422mzjm9cdesi6lyghjjg.jpg','https://cdn.ilovefreesoftware.com/wp-content/uploads/2019/06/Search-Telegram-Channels.png','Search All',last_id='0$$$0',data='all')
        # all_d.append(aa)
        # #Search All
        # aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32024)+'[/COLOR]',str(id),6,'https://sitechecker.pro/wp-content/uploads/2017/12/search-engines.png','https://www.komando.com/wp-content/uploads/2017/12/computer-search.jpg','Search All',last_id='0$$$0',data='all')
        # all_d.append(aa)
        # #Search History
        # aa=addDir3('[COLOR lightgreen]'+Addon.getLocalizedString(32072)+'[/COLOR]',str(id),30,'https://sitechecker.pro/wp-content/uploads/2017/12/search-engines.png','https://www.komando.com/wp-content/uploads/2017/12/computer-search.jpg','Search All',last_id='0$$$0',data='all')
        # all_d.append(aa)
        
   
        #Add Local Tv shows
        # aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32046)+'[/COLOR]','https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language={0}&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language={1}&page=1'.format(lang,lang),26,'http://oakhillcapital.com/wp-content/uploads/2015/08/LocalTV.jpg','http://coldshotproductions.net/flachannelbanner.png',Addon.getLocalizedString(32046))
        # all_d.append(aa)
        

        if len(Addon.getSetting("update_chat_id"))>0:
            #my repo
            aa=addDir3('[COLOR blue]'+Addon.getLocalizedString(32127)+'[/COLOR]','www',46,'special://home/addons/plugin.video.telemedia/tele/addons.png','https://cdn.wallpapersafari.com/21/48/cRMEy3.jpg',Addon.getLocalizedString(32127))
            all_d.append(aa)
        
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""year TEXT, ""icon TEXT,""fan TEXT,""plot TEXT, ""free TEXT);" % 'custom_show')
        dbcon.commit()
        dbcur.execute("SELECT * FROM custom_show where tmdb='%s'"%(url))
        match = dbcur.fetchall()
        
        
        if len(match)==0:
          #My Local Tv shows
          aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32055)+'[/COLOR]','www',28,'http://oakhillcapital.com/wp-content/uploads/2015/08/LocalTV.jpg','http://coldshotproductions.net/flachannelbanner.png',Addon.getLocalizedString(32055))
          #all_d.append(aa)
        #Full data groups
        aa=addDir3('[COLOR gold]'+Addon.getLocalizedString(32079)+'[/COLOR]','www',33,'special://home/addons/plugin.video.telemedia/tele/info.png','https://img.wonderhowto.com/img/66/20/63525837196216/0/hack-like-pro-pivot-from-victim-system-own-every-computer-network.1280x600.jpg',Addon.getLocalizedString(32079))
        all_d.append(aa)
        #Kids World
        aa=addDir3('[COLOR blue]'+Addon.getLocalizedString(32073)+'[/COLOR]','www',31,'special://home/addons/plugin.video.telemedia/tele/kids.png','https://insidethemagic-119e2.kxcdn.com/wp-content/uploads/2018/08/Expo19_11x16_Poster_KeyArt_72dpi-1-792x400.jpg',Addon.getLocalizedString(32073),data=KIDS_CHAT_ID)
        #all_d.append(aa)

        
        dbcur.close()
        dbcon.close()
        
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
        #Addon updates
        
        addNolink( '[COLOR lightblue][B]%s[/B][/COLOR]'%Addon.getLocalizedString(32124), 'www',45,False,iconimage='special://home/addons/plugin.video.telemedia/tele/addons.png',fan='https://cdn.wallpapersafari.com/21/48/cRMEy3.jpg')
    addNolink( '[COLOR red][B]%s[/B][/COLOR]'%Addon.getLocalizedString(32140), 'www',120,False,fan="https://media-cdn.tripadvisor.com/media/photo-s/08/6f/12/05/beautiful-settings.jpg", iconimage="special://home/addons/plugin.video.telemedia/tele/setting.png")
def res_q(quality):
    f_q=' '
    if '4k' in quality.lower():
        quality='2160'
    if '2160' in quality:
      f_q='2160'
    elif '1080' in quality:
      f_q='1080'
    elif '720' in quality:
      f_q='720'
    elif '480' in quality:
      f_q='480'
    
    elif '360' in quality or 'sd' in quality.lower():
      f_q='360'
    elif '240' in quality:
      f_q='240'
    elif 'hd' in quality.lower() or 'hq' in quality.lower():
      f_q='720'
    return f_q
    
def fix_q_links(quality):
    f_q=100
    if '4k' in quality.lower():
        quality='2160'
    if '2160' in quality:
      f_q=1
    elif '1080' in quality:
      f_q=2
    elif '720' in quality:
      f_q=3
    elif '480' in quality:
      f_q=4
    
    elif '360' in quality or 'sd' in quality.lower():
      f_q=5
    elif '240' in quality:
      f_q=6
    elif 'hd' in quality.lower() or 'hq' in quality.lower():
      f_q=3
    return f_q
def get_q(name):
    q=res_q(name)
    loc=fix_q_links(q)
    '''
    log.warning('Q test:'+name)
    log.warning('Q s:'+q)
    log.warning('Q loc:'+str(loc))
    '''
    return q,loc
def search(tmdb,type,last_id_pre,search_entered_pre,icon_pre,fan_pre,season,episode,no_subs=0,original_title='',heb_name='',dont_return=True,manual=True):
    import random
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""free TEXT);" % 'search')
    dbcon.commit()
        
    dbcur.execute("SELECT * FROM search")
    match_search = dbcur.fetchall()
    all_pre_search=[]
    for nm,fr in match_search:
        all_pre_search.append(nm)
    last_id=last_id_pre.split('$$$')[0]
    last_id_msg=last_id_pre.split('$$$')[1]
   
    
    if search_entered_pre=='Search All':
        search_entered=''
        
        #Enter Search
        keyboard = xbmc.Keyboard(search_entered, Addon.getLocalizedString(32025))
        keyboard.doModal()
        if keyboard.isConfirmed():
                query = keyboard.getText()
        else:
            return 0
    else:
        query=search_entered_pre
    query=query.replace('%20',' ').replace('%27',"'").replace('%3a',":")
    if query not in all_pre_search and manual:
        dbcur.execute("INSERT INTO search Values ('%s','%s');" %  (query.replace("'","%27"),' '))
        dbcon.commit()
    dbcur.close()
    dbcon.close()
    num=random.randint(1,1001)
    all_links=[]
    filter_size=int(Addon.getSetting("filter_size"))*1024*1024
    log.warning(filter_size)
    if type=='all':
        data={'type':'td_send',
             'info':json.dumps({'@type': 'searchMessages', 'query': query,'offset_message_id':last_id,'offset_chat_id':last_id_msg,'limit':100, '@extra': num})
             }
        event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
        
        
        counter_ph=0
        for items in event['messages']:  
            #log.warning(items)
            
            if 'document' in items['content']:
                name=items['content']['document']['file_name']
                if '.mkv' not in name and '.mp4' not in name and '.avi' not in name:
                    continue
                size=items['content']['document']['document']['size']
                if size<filter_size:
                    continue
                f_size2=''
                if 'caption' in items['content']:
                    if 'text' in items['content']['caption']:
                        f_size2=items['content']['caption']['text']+'\n'
                f_size2=f_size2+str(round(float(size)/(1024*1024*1024), 2))+' GB'
                q,loc=get_q(name)
                link_data={}
                link_data['id']=str(items['content']['document']['document']['id'])
                link_data['m_id']=items['id']
                link_data['c_id']=items['chat_id']
                f_lk=json.dumps(link_data)
                all_links.append((name, f_lk,3,q,loc, icon_pre,fan_pre,f_size2,no_subs,tmdb,season,episode,original_title))
                #addLink( name, str(items['content']['document']['document']['id']),3,False, icon_pre,fan_pre,f_size2,data=data,no_subs=no_subs,tmdb=tmdb,season=season,episode=episode,original_title=original_title)
            if 'video' in items['content']:
                    name=items['content']['video']['file_name']
                    
                    size=items['content']['video']['video']['size']
                    if size<filter_size:
                        continue
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    log.warning('items')
                    q,loc=get_q(name)
                    link_data={}
                    link_data['id']=str(items['content']['video']['video']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    all_links.append(( name, f_lk,3,q,loc, icon_pre,fan_pre,f_size2,no_subs,tmdb,season,episode,original_title))
                    #addLink( name, str(items['content']['video']['video']['id']),3,False, icon_pre,fan_pre,f_size2,tmdb=tmdb,season=season,episode=episode,original_title=original_title)
            if 'caption' in items['content']:
                    txt_lines=items['content']['caption']['text'].split('\n')
                    all_l=[]
                    name=txt_lines[0]
                    rem_lines=[]
                    for lines in txt_lines:
                        if 'upfile' not in lines and 'drive.google' not in lines:
                          rem_lines.append(lines)
                          continue
                        
                            
                        all_l.append(lines)
                    if len(all_l)==0:
                        continue
                    icon=icon_pre
                    fan=fan_pre
                    if 'photo' in items['content']['caption']:
                        counter_ph+=1
                        icon_id=items['content']['photo']['sizes'][0]['photo']['id']
                        f_name=items['content']['photo']['sizes'][0]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(icons_path,f_name)
                        if os.path.exists(mv_name):
                            icon=mv_name
                        else:
                           icon=download_photo(icon_id,counter_ph,f_name,mv_name)
                        
                        counter_ph+=1
                        loc=items['content']['photo']['sizes']
                        icon_id=items['content']['photo']['sizes'][len(loc)-1]['photo']['id']
                        f_name=items['content']['photo']['sizes'][len(loc)-1]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(fan_path,f_name)
                        if os.path.exists(mv_name):
                            fan=mv_name
                        else:
                           fan=download_photo(icon_id,counter_ph,f_name,mv_name)
                           
                    q,loc=get_q(txt_lines[0])
                    all_links.append(('[COLOR lightgreen]'+ txt_lines[0]+'[/COLOR]' , '$$$'.join(all_l),9,q,loc, icon,fan,('\n'.join(rem_lines)).replace('\n\n','\n'),no_subs,tmdb,season,episode,original_title))
                    #addLink( '[COLOR lightgreen]'+ txt_lines[0]+'[/COLOR]' , '$$$'.join(all_l),9,False, icon,fan,('\n'.join(rem_lines)).replace('\n\n','\n'),no_subs=no_subs,tmdb=tmdb,season=season,episode=episode,original_title=original_title)
            elif 'web_page' in items['content']:
                name=items['content']['web_page']['title']
                link=items['content']['web_page']['url']
                plot=items['content']['web_page']['description']['text']
                if 'upfile' not in link and 'drive.google' not in link:
                      
                      continue
                icon=icon_pre
                fan=fan_pre
                if 'photo' in items['content']['web_page']:
                    counter_ph+=1
                    icon_id=items['content']['web_page']['photo']['sizes'][0]['photo']['id']
                    f_name=items['content']['web_page']['photo']['sizes'][0]['photo']['remote']['id']+'.jpg'
                    mv_name=os.path.join(icons_path,f_name)
                    if os.path.exists(mv_name):
                        icon=mv_name
                    else:
                       icon=download_photo(icon_id,counter_ph,f_name,mv_name)
                    
                    counter_ph+=1
                    loc=items['content']['web_page']['photo']['sizes']
                    icon_id=items['content']['web_page']['photo']['sizes'][len(loc)-1]['photo']['id']
                    f_name=items['content']['web_page']['photo']['sizes'][len(loc)-1]['photo']['remote']['id']+'.jpg'
                    mv_name=os.path.join(fan_path,f_name)
                    if os.path.exists(mv_name):
                        fan=mv_name
                    else:
                       fan=download_photo(icon_id,counter_ph,f_name,mv_name)
              
                q,loc=get_q(name)
                
                all_links.append(('[COLOR lightgreen]'+ name+'[/COLOR]', link,9,q,loc, icon,fan,plot.replace('\n\n','\n'),no_subs,tmdb,season,episode,original_title))
                #addLink( '[COLOR lightgreen]'+ name+'[/COLOR]', link,9,False, icon,fan,plot.replace('\n\n','\n'),no_subs=no_subs,tmdb=tmdb,season=season,episode=episode,original_title=original_title)
            f_id=items['chat_id']
    if dont_return:
        all_links=sorted(all_links, key=lambda x: x[4], reverse=False)
        filter_dup=Addon.getSetting("dup_links")=='true'
        all_t_links=[]
        for  name, link,mode,q,loc, icon,fan,plot,no_subs,tmdb,season,episode,original_title in all_links:
            
            if name not in all_t_links or filter_dup==False:
            
           
                all_t_links.append(name)
                addLink( name, link,mode,False, icon,fan,plot,no_subs=no_subs,tmdb=tmdb,season=season,episode=episode,original_title=original_title)
        try:
            last_id=str(items['id'])+'$$$'+str(f_id)
            
        except:
            #xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', 'No result for:'+query))
            pass
    return all_links
    
    #addDir3('[COLOR yellow]'+'Next Page'+'[/COLOR]',str(id),6,'https://www.5thtackle.com/wp-content/uploads/2017/04/next-page.jpg','https://www.mcgill.ca/continuingstudies/files/continuingstudies/next-page-magazine.png',query,data=type,last_id=last_id)
def utf8_simple(params):
    
    # problem: u.urlencode(params.items()) is not unicode-safe. Must encode all params strings as utf8 first.
    # UTF-8 encodes all the keys and values in params dictionary
    try:
        params = params
    except:
        params='ERROR'
            
    
    return params
def clean_name(name,original_title):
    name=name.replace('.mp4','').replace('.avi','').replace('.mkv','').replace(original_title,'')
    return name
def file_list(id,page,last_id_all,quary,icon_pre,fan_pre,image_master='',original_title=''):
   try:
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
        dbcon.commit()

        dbcur.execute("SELECT * FROM playback")
        match = dbcur.fetchall()
        all_w={}
        for n,tm,s,e,p,t,f in match:
            ee=clean_name(str(n),original_title)
            all_w[ee]={}
            all_w[ee]['resume']=str(p)
            all_w[ee]['totaltime']=str(t)
        link_types=['upfile','drive.google','youtube','youtu.be','.m3u8','twitch']
        from resources.modules.tmdb import get_html_g
        from resources.modules import cache
        html_g_tv,html_g_movie=cache.get(get_html_g,72, table='posters_n')
        all_d=[]
        icon_pre=telemaia_icon
        fan_pre=telemaia_fan
        if image_master!='':
            fan_pre=image_master.split('$$$')[1]
            icon_pre=image_master.split('$$$')[0]
        fan_o=fan_pre
        icon_o=icon_pre
        
        if 'from_plot' in quary:
            quary=' '
            dont_s_again=True
        else:
            dont_s_again=False
            search_entered=''
            #'Enter Search'
            keyboard = xbmc.Keyboard(search_entered, Addon.getLocalizedString(32025))
            keyboard.doModal()
            if keyboard.isConfirmed():
                    quary = keyboard.getText()
            else:
                return 0
        import random
      
        last_id_doc=last_id_all.split('$$$')[0]
        last_id=last_id_all.split('$$$')[1]
        last_id_link=last_id_all.split('$$$')[2]
        last_id_audio=last_id_all.split('$$$')[3]
        
        disp_files=Addon.getSetting("disp_f")=='true'
        disp_vid=Addon.getSetting("disp_v")=='true'
        disp_links=Addon.getSetting("disp_l")=='true'
        disp_audio=Addon.getSetting("disp_a2")=='true'
        
        disp_repo=Addon.getSetting("repo")=='true'
        
        download_full_files=Addon.getSetting("download_files")=='true'
        
        num=random.randint(1,1001)
        plat='windows'
        if sys.platform.lower().startswith('linux'):
        
            if 'ANDROID_DATA' in os.environ:
                plat = 'android'
        on_android=False
        if Addon.getSetting("install_apk")=='true':
            on_android=plat == 'android'
        if last_id_audio!='-99' and disp_audio:
            num=random.randint(1,1001)
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':(id), 'query': quary.strip(),'from_message_id':int(last_id_audio),'offset':0,'filter':{'@type': 'searchMessagesFilterAudio'},'limit':100, '@extra': num})
                 }
           
           
           
            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            
           
            counter_ph=1000
            for items in event['messages']:  
                    
                    
                    name=items['content']['audio']['title']
                    
                    size=items['content']['audio']['audio']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    icon=icon_pre
                    fan=fan_pre
                    if 'album_cover_thumbnail' in items['content']['audio']:
                        if 'photo' in items['content']['audio']['album_cover_thumbnail']:
                            counter_ph+=1
                            icon_id=items['content']['audio']['album_cover_thumbnail']['photo']['id']
                            f_name=items['content']['audio']['album_cover_thumbnail']['photo']['remote']['id']+'.jpg'
                            mv_name=os.path.join(icons_path,f_name)
                            if os.path.exists(mv_name):
                                icon=mv_name
                            else:
                               icon=download_photo(icon_id,counter_ph,f_name,mv_name)
                            
                            fan=icon
                    dur=items['content']['audio']['duration']
                    t=time.strftime("%H:%M:%S", time.gmtime(dur))
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                    name=clean_name(name,original_title)
                    link_data={}
                    link_data['id']=str(items['content']['audio']['audio']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    addLink( '[COLOR lime]'+name+'[/COLOR]',f_lk ,3,False, icon,fan,f_size2+'\n'+t+'\nMusic File',da=da,all_w=all_w,in_groups=True)
                    
                
            last_id_audio=-99
            try:
             last_id_audio=items['id']
             last_id_audio_found=1
            except:
             pass
     
        if last_id_doc!='-99' and disp_files:
           num=random.randint(1,1001)
           data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':(id), 'query': quary.strip(),'from_message_id':int(last_id_doc),'offset':0,'filter':{'@type': 'searchMessagesFilterDocument'},'limit':100, '@extra': num})
                 }
           
           
           #data={'type':'td_send',
           #      'info':json.dumps({'@type': 'getChatHistory','chat_id':long(id), 'from_message_id': 0,'offset':0,'limit':10, '@extra':num})
           #      }
           event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
           
           for items in event['messages']:  
               
                if 'document' not in items['content']:
                    continue
                ok_name=True
                file_name=items['content']['document']['file_name']
                if 'document' in items['content']:
                    if 'caption' in items['content']:
                        if 'text' in items['content']['caption']:
                            if len(items['content']['caption']['text'])>0:
                                name=items['content']['caption']['text']
                                ok_name=False
                    if ok_name:
                        name=file_name
                    if Addon.getSetting("files_display_type")=='0':
                        name=file_name
                    c_name=[]
                    if '\n' in name:
                        f_name=name.split('\n')
                        for it in f_name:
                            if '😎' not in it and it!='\n' and len(it)>1 and '💠' not in it:
                                c_name.append(it)
                        name='\n'.join(c_name)
                    
                        
                    if not(download_full_files and '_files_' in original_title.lower()):
                        
                        if on_android and 'apk' in original_title.lower():
                            if '.mkv' not in file_name and '.mp4' not in file_name and '.avi' not in file_name and '.zip' not in file_name and '.apk' not in file_name:
                                continue
                        elif disp_repo and 'repo' in original_title.lower():
                            
                            if '.mkv' not in file_name and '.mp4' not in file_name and '.avi' not in file_name and '.zip' not in file_name:
                                continue
                        else:
                            if '.mkv' not in file_name and '.mp4' not in file_name and '.avi' not in file_name:
                                continue
                    size=items['content']['document']['document']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    if Addon.getSetting("remove_title")=='true':
                        name=name.replace(original_title,'').replace('@'+original_title,'')
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                    regex='.*([1-3][0-9]{3})'
                    year_pre=re.compile(regex).findall(name)
                    year=0
                    if len(year_pre)>0:
                        year=year_pre[0]
                    mode=3
                    o_name=name
                    if '.zip'  in name:
                        name='[COLOR gold]'+name+'[/COLOR]'
                        mode=24
                    if '.apk'  in name:
                        name='[COLOR gold]'+name+'[/COLOR]'
                        mode=32
                    
                    if (download_full_files and '_files_' in original_title.lower()):
                        mode=36
                        name='[COLOR khaki]'+name+'[/COLOR]'
                        
                    name=clean_name(name,original_title)
                    link_data={}
                    link_data['id']=str(items['content']['document']['document']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    addLink( name,f_lk ,mode,False, icon_pre,fan_pre,f_size2,da=da,year=year,original_title=o_name,all_w=all_w,in_groups=True)
                
                
           last_id_doc=-99
           try:
            last_id_doc=items['id']
            last_id_doc_found=1
           except:
            pass
        else:
           last_id_doc=-99
           last_id_doc_found=0
        if last_id!='-99' and disp_vid:
            num=random.randint(1,1001)
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':(id), 'query': quary.strip(),'from_message_id':int(last_id),'offset':0,'filter':{'@type': 'searchMessagesFilterVideo'},'limit':100, '@extra': num})
                 }
            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            
            for items in event['messages']:  
                #log.warning(items)
                if 'video' in items['content']:
                    ok_name=True
                    if 'caption' in items['content']:
                        if 'text' in items['content']['caption']:
                            if len(items['content']['caption']['text'])>0:
                                name=items['content']['caption']['text']
                                ok_name=False
                    if ok_name:
                        name=items['content']['video']['file_name']
                    if Addon.getSetting("video_display_type")=='0':
                        name=items['content']['video']['file_name']
                    c_name=[]
                    if '\n' in name:
                        f_name=name.split('\n')
                        for it in f_name:
                            if '😎' not in it and it!='\n' and len(it)>1:
                                c_name.append(it)
                        name='\n'.join(c_name)
                    size=items['content']['video']['video']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    plot=''
                    
                    if 'caption' in items['content']:
                        plot=items['content']['caption']['text']
                        
                        if '\n' in plot and len(name)<3:
                                name=plot.split('\n')[0]
                    
                    if Addon.getSetting("remove_title")=='true':
                        name=name.replace(original_title,'').replace('@'+original_title,'')
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                    regex='.*([1-3][0-9]{3})'
                    year_pre=re.compile(regex).findall(name)
                    year=0
                    if len(year_pre)>0:
                        year=year_pre[0]
                    name=clean_name(name,original_title)
                    link_data={}
                    link_data['id']=str(items['content']['video']['video']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    addLink( name,f_lk,3,False, icon_pre,fan_pre,f_size2+'\n'+plot.replace('\n\n',' - '),da=da,year=year,all_w=all_w,in_groups=True)
                
                
               
            last_id=-99
            try:
                last_id=items['id']
            except:
                pass
                
            
        else:
            last_id=-99
        
        
        if last_id_link!='-99' and disp_links:
           num=random.randint(1,1001)
           data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':(id), 'query': quary,'from_message_id':int(last_id_link),'offset':0,'filter':{'@type': 'searchMessagesFilterUrl'},'limit':100, '@extra': num})
                 }
           
           
           #data={'type':'td_send',
           #      'info':json.dumps({'@type': 'getChatHistory','chat_id':long(id), 'from_message_id': 0,'offset':0,'limit':10, '@extra':num})
           #      }
           event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()

           
           counter_ph=0
           for items in event['messages']:  
                
                if 'web_page' in items['content']:
                    name=items['content']['web_page']['title']
                    link=items['content']['web_page']['url']
                    plot=items['content']['web_page']['description']['text']
                    all_l=[link]
                    ok=False
                    for items_in in link_types:
                        if items_in in link:
                            ok=True
                            break
                            
                    if not ok:
                          
                          continue
                        
                    
                    if 'text' in items['content']:
                        txt_lines=items['content']['text']['text'].split('\n')
                        
                        rem_lines=[]
                        
                        for lines in txt_lines:
                            ok=False
                            for items_in in link_types:
                                if items_in in lines:
                                    ok=True
                                    break
                                    
                            if not ok:
                                  
                                  continue
                            
                                
                            all_l.append(lines)
                    icon=icon_pre
                    fan=fan_pre
                    if 'photo' in items['content']['web_page']:
                        counter_ph+=1
                        icon_id=items['content']['web_page']['photo']['sizes'][0]['photo']['id']
                        f_name=items['content']['web_page']['photo']['sizes'][0]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(icons_path,f_name)
                        if os.path.exists(mv_name):
                            icon=mv_name
                        else:
                           icon=download_photo(icon_id,counter_ph,f_name,mv_name)
                        
                        counter_ph+=1
                        loc=items['content']['web_page']['photo']['sizes']
                        icon_id=items['content']['web_page']['photo']['sizes'][len(loc)-1]['photo']['id']
                        f_name=items['content']['web_page']['photo']['sizes'][len(loc)-1]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(fan_path,f_name)
                        if os.path.exists(mv_name):
                            fan=mv_name
                        else:
                           fan=download_photo(icon_id,counter_ph,f_name,mv_name)
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                    name=clean_name(name,original_title)
                    
                    addLink('[COLOR lightgreen]'+ name+'[/COLOR]', utf8_simple('$$$'.join(all_l)),9,False, icon,fan,plot.replace('\n\n','\n'),da=da,all_w=all_w,in_groups=True)
                elif 'caption' in items['content']:
                    txt_lines=items['content']['caption']['text'].split('\n')
                    all_l=[]
                    rem_lines=[]
                    
                    for lines in txt_lines:
                        ok=False
                        for items_in in link_types:
                            if items_in in lines:
                                ok=True
                                break
                                
                        if not ok:
                              rem_lines.append(lines)
                              continue
                        
                        
                            
                        all_l.append(lines)
                    if len(all_l)==0:
                        continue
                    icon=icon_pre
                    fan=fan_pre
                    if 'photo' in items['content']:
                        counter_ph+=1
                        
                        icon_id=items['content']['photo']['sizes'][0]['photo']['id']
                        f_name=items['content']['photo']['sizes'][0]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(icons_path,f_name)
                        if os.path.exists(mv_name):
                            icon=mv_name
                        else:
                           icon=download_photo(icon_id,counter_ph,f_name,mv_name)
                        
                        counter_ph+=1
                        loc=items['content']['photo']['sizes']
                        icon_id=items['content']['photo']['sizes'][len(loc)-1]['photo']['id']
                        f_name=items['content']['photo']['sizes'][len(loc)-1]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(fan_path,f_name)
                        if os.path.exists(mv_name):
                            fan=mv_name
                        else:
                           fan=download_photo(icon_id,counter_ph,f_name,mv_name)
                       
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                    
                    addLink( '[COLOR lightgreen]'+ txt_lines[0]+'[/COLOR]', utf8_simple('$$$'.join(all_l)),9,False, icon,fan,('\n'.join(rem_lines)).replace('\n\n','\n'),da=da,all_w=all_w,in_groups=True)
                
                elif 'text' in items['content']:
                    txt_lines=items['content']['text']['text'].split('\n')
                    all_l=[]
                    rem_lines=[]
                    
                    for lines in txt_lines:
                        ok=False
                        for items_in in link_types:
                            if items_in in lines:
                                ok=True
                                break
                                
                        if not ok:
                              rem_lines.append(lines)
                              continue
                        
                            
                        all_l.append(lines)
                    if len(all_l)==0:
                        continue
                    
                    icon=icon_pre
                    fan=fan_pre
                    if 'photo' in items['content']:
                        counter_ph+=1
                        icon_id=items['content']['photo']['sizes'][0]['photo']['id']
                        f_name=items['content']['photo']['sizes'][0]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(icons_path,f_name)
                        if os.path.exists(mv_name):
                            icon=mv_name
                        else:
                           icon=download_photo(icon_id,counter_ph,f_name,mv_name)
                        
                        
                        counter_ph+=1
                        
                        loc=items['content']['photo']['sizes']
                        icon_id=items['content']['photo']['sizes'][len(loc)-1]['photo']['id']
                        f_name=items['content']['photo']['sizes'][len(loc)-1]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(fan_path,f_name)
                        if os.path.exists(mv_name):
                            fan=mv_name
                        else:
                           fan=download_photo(icon_id,counter_ph,f_name,mv_name)
                       
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                   
                    addLink( '[COLOR lightgreen]'+ txt_lines[0]+'[/COLOR]', utf8_simple('$$$'.join(all_l)),9,False, icon,fan,('\n'.join(rem_lines)).replace('\n\n','\n'),da=da,all_w=all_w,in_groups=True)
                
                
                
           last_id_link=-99
           try:
            last_id_link=items['id']
            
           except:
            pass
        else:
           last_id_link=-99
          
           
        if last_id_doc==-99 and last_id==-99 and last_id_link==-99 and last_id_audio==-99:
            xbmcgui.Dialog().ok(Addon.getLocalizedString(32052),Addon.getLocalizedString(32059))
        f_last_id=str(last_id_doc)+'$$$'+str(last_id)+'$$$'+str(last_id_link)+'$$$'+str(last_id_audio)
        if quary==' ':
            quary='from_plot'
        #Next Page
        aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32026)+'[/COLOR]',str(id),2,'https://www.5thtackle.com/wp-content/uploads/2017/04/next-page.jpg','https://www.mcgill.ca/continuingstudies/files/continuingstudies/next-page-magazine.png',quary,data=str(int(page)+1),last_id=f_last_id,image_master=icon_o+'$$$'+fan_o)
        all_d.append(aa) 
        if dont_s_again:
            f_last_id='0$$$0$$$0$$$0'
            #'Search'
            aa=addDir3('[COLOR blue]'+Addon.getLocalizedString(32027)+'[/COLOR]',str(id),2,'https://sitechecker.pro/wp-content/uploads/2017/12/search-engines.png','https://www.komando.com/wp-content/uploads/2017/12/computer-search.jpg','search',data='0',last_id=f_last_id,image_master=image_master)
            all_d.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
   except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        log.warning('ERROR IN Main:'+str(lineno))
        log.warning('inline:'+str(line))
        log.warning(str(e))
        xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
def get_direct_bot_link(c_id,m_id):
   try:
    bot_id=Addon.getSetting("bot_id2")#'772555074'
    num=random.randint(0,60000)
    data={'type':'td_send',
         'info':json.dumps({'@type': 'forwardMessages','chat_id':(bot_id), 'from_chat_id': c_id,'message_ids':[m_id], '@extra': num})
         }

    log.warning('sending')
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
    new_link='empty'
    log.warning('Wait')
    counter_sh=0
    data={'type':'clean_last_link',
             'info':''
             }


    test=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
        
    while(new_link=='empty'):
        data={'type':'get_last_link',
             'info':''
             }


        new_link=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
        if new_link=='Found':
            log.warning( 'Limit')
            break
        time.sleep(0.1)
        counter_sh+=1
        if (counter_sh>100):
            log.warning('Timeout')
            break
    
    headers = {
      
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        }
    log.warning(new_link)
    f_link=re.compile('http:(.+?)\n',re.DOTALL).findall(str(new_link))[0]
    log.warning(f_link)
    
    return 'http:'+f_link
 
   except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        log.warning('ERROR IN bot:'+str(lineno))
        log.warning('inline:'+str(line))
        log.warning(str(e))
        #xbmcgui.Dialog().ok('Error occurred','Err in bot:'+str(e)+'Line:'+str(lineno))
        return "Error play"
def play_direct(final_link,data,name,no_subs,tmdb,season,episode,original_title,description,resume,resume_time):
        video_data={}
        if season!=None and season!="%20" and season!="0":
           video_data['TVshowtitle']=original_title.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
           video_data['mediatype']='tvshow'
           
        else:
           video_data['mediatype']='movies'
        if season!=None and season!="%20" and season!="0":
           tv_movie='tv'
           url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&append_to_response=external_ids'%(tmdb,'653bb8af90162bd98fc7ee32bcbbfb3d')
        else:
           tv_movie='movie'
           
           url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&append_to_response=external_ids'%(tmdb,'653bb8af90162bd98fc7ee32bcbbfb3d')
        if 'tt' not in tmdb:
             try:
                log.warning(url2)
                
                imdb_id=get_html(url2).json()['external_ids']['imdb_id']
                log.warning(imdb_id)
             except Exception as e:
                log.warning('IMDB err:'+str(e))
                imdb_id=" "
        else:
             imdb_id=tmdb
        video_data['title']=name.replace('.mp4','').replace('.avi','').replace('.mkv','').replace('-','').replace('Google Drive','').replace('[COLOR lightblue][B]','').replace('[/B][/COLOR]','').replace(' 360','').replace(' 480','').replace(' 720','').replace(' 1080','').strip()
        log.warning(video_data['title'])
        video_data['Writer']=tmdb
        video_data['season']=season
        video_data['episode']=episode
        video_data['plot']='from_telemedia'
        video_data['imdb']=imdb_id
        video_data['code']=imdb_id

        video_data['imdbnumber']=imdb_id
        
        video_data['imdb_id']=imdb_id
        video_data['IMDBNumber']=imdb_id
        video_data['genre']=imdb_id
        if no_subs=='1':
            video_data[u'mpaa']='heb'
        
        listItem = xbmcgui.ListItem(video_data['title'], path=final_link) 
        listItem.setInfo(type='Video', infoLabels=video_data)


        listItem.setProperty('IsPlayable', 'true')

       
        
        if resume_time==-1:
            return 0
        log.warning('resume_time:'+str(resume_time))
        ok=xbmc.Player().play(final_link,listitem=listItem)
def play(name,url,data,iconimage,fan,no_subs,tmdb,season,episode,original_title,description,resume,r_art='',r_logo=''):
    ok=check_free_space()
    try:
        cond=xbmc.Monitor().abortRequested()
    except:
        cond=xbmc.abortRequested
    if not ok:
        return 0
    '''
    link='http://127.0.0.1:%s/'%listen_port+url
    log.warning('Play Link:'+link)
    video_data={}
    video_data['title']=name
    video_data['poster']=fan

    video_data['icon']=iconimage
    
    listItem = xbmcgui.ListItem(video_data['title'], path=link) 
    listItem.setInfo(type='Video', infoLabels=video_data)


    listItem.setProperty('IsPlayable', 'true')

   
       
    ok=xbmc.Player().play(link,listitem=listItem)
    xbmc.executebuiltin("Dialog.Close(busydialog)")
    '''
    l_data=json.loads(url)

    if Addon.getSetting("test")=='998':
        log.warning('Check Resume')
        if not resume:
            resume_time=get_resume(tmdb,name,season,episode)
        else:
            resume_time=resume
        
        if resume_time==-1:
            return 0
        dialog = xbmcgui.DialogBusy()
        dialog.create()
        dp = xbmcgui.DialogProgress()
        dp.create('Please Wait...','Playing', '','')
        dp.update(0, 'Please Wait...','Playing', '' )
        c_id=l_data['c_id']
        m_id=l_data['m_id']
        log.warning('1')
        f_link=get_direct_bot_link(c_id,m_id)
       
        if f_link!='Found':
            
            play_direct(f_link,data,name,no_subs,tmdb,season,episode,original_title,description,resume,resume_time)
            log.warning('2')
            broken_play=True
            w_time=int(Addon.getSetting("wait_size"))
            log.warning('3')
            for _ in range(w_time):
                dp.update(0,'Playing...',Addon.getLocalizedString(32040)+' : '+str(_), '' )
                try:
                    vidtime = xbmc.Player().getTime()
                except:
                    vidtime=0
                    pass
                if xbmc.Player().isPlaying() and vidtime>0:
                    broken_play=False
                    dp.close()
                    break
                if dp.iscanceled():
                    dp.close()
                    broken_play=False
                    xbmc.Player().stop()
                    break
                time.sleep(0.100)
            log.warning('4')
            if resume_time>0:
                try:
                    xbmc.Player().seekTime(int(float(resume_time)))
                except Exception as e:
                    log.warning('Seek Err:'+str(e))
                    pass
            dp.close()
            g_timer=None
            while (not cond) and (xbmc.Player().isPlaying()):
                 try:
                    vidtime = xbmc.Player().getTime()
                 except:
                    vidtime = 0
                 try:
                    g_timer=xbmc.Player().getTime()
                    g_item_total_time=xbmc.Player().getTotalTime()
                 except:
                    pass
                 time.sleep(0.1)
            
            
            if resume_time!=-1 and g_timer:
                update_db_link(tmdb,name,season,episode,g_timer,g_item_total_time)
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            return 0
    
    try:
        url=l_data['id']
        if 0:
        
            free_space=xbmc.getInfoLabel('System.FreeSpace')
            log.warning('free_space:'+str(free_space))
            free_space_int=[int(s) for s in free_space.split() if s.isdigit()]
            log.warning('free_space:'+str(free_space_int))
            if 'MB' in free_space:
                total_free=int(free_space_int[0])
            elif 'GB' in free_space:
                total_free=int(free_space_int[0])*1024
            elif 'KB' in free_space:
                total_free=int(free_space_int[0])/1024
            else:
                total_free=0
           
            if (total_free<1600):
                ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32127),(Addon.getLocalizedString(32128)))
                if ok:
                    HOME= xbmc_tranlate_path('special://home/')
                    USERDATA= os.path.join(HOME,      'userdata')
                    ADDONS           = os.path.join(HOME,      'addons')
                    
                    THUMBS= os.path.join(USERDATA,  'Thumbnails')
                    TEMPDIR= xbmc_tranlate_path('special://temp')
                    PACKAGES= os.path.join(ADDONS,    'packages')
                    remove_all=[THUMBS,TEMPDIR,PACKAGES]
                    for items in remove_all:
                        shutil.rmtree(items,ignore_errors=True, onerror=None)
                    DATABASE         = os.path.join(USERDATA,  'Database')
                    arr = os.listdir(DATABASE)
                    for items in arr:
                        if 'Textures' in items:
                            try:
                                os.remove(os.path.join(DATABASE,items))
                            except:
                                pass
                free_space=xbmc.getInfoLabel('System.FreeSpace')
                log.warning('free_space:'+str(free_space))
                free_space_int=[int(s) for s in free_space.split() if s.isdigit()]
                log.warning('free_space:'+str(free_space_int))
                if 'MB' in free_space:
                    total_free=int(free_space_int[0])
                elif 'GB' in free_space:
                    total_free=int(free_space_int[0])*1024
                elif 'KB' in free_space:
                    total_free=int(free_space_int[0])/1024
                else:
                    total_free=0
                if (total_free<1600):
                    xbmcgui.Dialog().ok('Error occurred','Still not Enough space, free space:'+str(free_space))
                    #sys.exit()
        monitor=TelePlayer()
        try_next_player=Addon.getSetting("next_player_option")=='true'
        if Addon.getSetting("use_bot_player3")=='false':
             broken_play,resume_time=monitor.playTeleFile(url,data,name,no_subs,tmdb,season,episode,original_title,description,resume,l_data,iconimage=iconimage,fanart=fanart,r_art=r_art,r_logo=r_logo)
        else:
            broken_play=True
            if not resume:
                resume_time=get_resume(tmdb,name,season,episode)
            else:
                resume_time=resume
            log.warning('resume_time:')
            log.warning(resume_time)
        if resume_time==-1:
            return 0
        if broken_play and try_next_player:
            dp = xbmcgui.DialogProgress()
            if KODI_VERSION<19:
                dp.create('Please Wait...','Playing', '','')
                dp.update(0, 'Please Wait...','Playing', '' )
            else:
                dp.create('Please Wait...','Playing'+'\n'+ ''+'\n'+'')
                dp.update(0, 'Please Wait...'+'\n'+'Playing'+'\n'+ '' )
            #xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia ERR','Broken Play Trying another method'))
            c_id=l_data['c_id']
            m_id=l_data['m_id']
            
            f_link=get_direct_bot_link(c_id,m_id)
            if "Error play"==f_link:
                broken_play,resume_time=monitor.playTeleFile(url,data,name,no_subs,tmdb,season,episode,original_title,description,resume,l_data,iconimage=iconimage,fanart=fanart,r_art=r_art,r_logo=r_logo)
            else:
                log.warning(f_link)
                play_direct(f_link,data,name,no_subs,tmdb,season,episode,original_title,description,resume,resume_time)
                log.warning('2')
                broken_play=True
                w_time=int(Addon.getSetting("wait_size"))
                log.warning('3')
                count__ok=0
                for _ in range(1000):
                    if KODI_VERSION<19:
                        dp.update(0,'Playing...',Addon.getLocalizedString(32040)+' : '+str(_), '' )
                    else:
                        dp.update(0,'Playing...'+'\n'+Addon.getLocalizedString(32040)+' : '+str(_)+'\n'+ '' )
                    try:
                        vidtime = xbmc.Player().getTime()
                    except:
                        vidtime=0
                        pass
                    if  vidtime>0:
                        count__ok+=1
                    else:
                        count__ok=0
                    if xbmc.Player().isPlaying() and count__ok>3:
                        broken_play=False
                        
                        break
                    if dp.iscanceled():
                        dp.close()
                        broken_play=False
                        xbmc.Player().stop()
                        break
                    time.sleep(0.100)
            log.warning('4')

            if resume_time>0:
                try:
                    xbmc.Player().seekTime(int(float(resume_time)))
                except Exception as e:
                    log.warning('Seek Err:'+str(e))
                    pass
            dp.close()
            g_timer=None
            while (not cond) and (xbmc.Player().isPlaying()):
                 try:
                    vidtime = xbmc.Player().getTime()
                 except:
                    vidtime = 0
                 try:
                    g_timer=xbmc.Player().getTime()
                    g_item_total_time=xbmc.Player().getTotalTime()
                 except:
                    pass
                 time.sleep(0.1)
            
            
            if resume_time!=-1 and g_timer:
                update_db_link(tmdb,name,season,episode,g_timer,g_item_total_time)
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            return 0
    except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        log.warning('ERROR IN Main:'+str(lineno))
        log.warning('inline:'+str(line))
        log.warning(str(e))
        xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
    
def get_upfile_det(url):
    name=''
    log.warning(url)
    headers = {
  
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    
    'Content-Type': 'application/json;charset=utf-8',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    }
    html=get_html(url,headers=headers).content()
    
       
    regex='<title>(.+?)</title>.+?<input type="hidden" value="(.+?)" name="hash">'
    match=re.compile(regex,re.DOTALL).findall(html)
    if len(match)==0:
         xbmcgui.Dialog().ok('Error occurred','Link is down')
         return 0,0
    for name,link in match:
      id=url.split('/')[-1]
      id=id.replace('.html','').replace('.htm','')
      
      playlink='http://down.upfile.co.il/downloadnew/file/%s/%s'%(id,link)
    return playlink,name

def googledrive_download(id):
    #download('http://mirrors.kodi.tv/addons/jarvis/script.module.requests/script.module.requests-2.9.1.zip','script.module.requests')
    #dis_or_enable_addon('script.module.requests','auto')
    #import requests,time
    keys=[]
    #id_pre=id.split('=')
    #id=id_pre[len(id_pre)-1]
    
    def get_confirm_token(response):
        
        for cookie in response:
            log.warning('cookie.name')
            log.warning(cookie.name)
            backup_cookie= cookie.value
            if 'download_warning' in cookie.name:
                log.warning(cookie.value)
                log.warning('cookie.value')
                return cookie.value
            return backup_cookie

        return None

    
    URL = "https://docs.google.com/uc?export=download"

    #session = requests.Session()

    #response = session.get(URL, params = { 'id' : id }, stream = True)
    if KODI_VERSION<19:
        import urllib2
    else:
        import urllib
    try:
        import http.cookiejar as cookielib
    except:
        import cookielib

    from cookielib import CookieJar

    cj = CookieJar()
    if KODI_VERSION<19:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    else:
        opener = urllib.build_opener(urllib.HTTPCookieProcessor(cj))
    
    # input-type values from the html form
    formdata =  { 'id' : id }
    data_encoded = urllib.urlencode(formdata)
    log.warning(URL+'&'+ data_encoded)
    response = opener.open(URL+'&'+ data_encoded)
    content = response.read()
    cookies={}
    cook=[]
    
    for cookie in cj:
         cook.append(cookie.name+'='+cookie.value)
         cookies[cookie.name]=cookie.value
         log.warning( cookie)
    token = get_confirm_token(cj)
    log.warning(token)
    if token:
        params = { 'id' : id, 'confirm' : token }
        headers = {'Access-Control-Allow-Headers': 'Content-Length','Cookie':';'.join(cook)}
        
        data_encoded = urllib.urlencode(params)
        return (URL+'&'+ data_encoded+"|"+ urllib.urlencode(headers))
        #response = opener.open(URL+'&'+ data_encoded)
        #chunk_read(response, report_hook=chunk_report,dp=dp,destination=destination,filesize=filesize)
        

    #save_response_content(response, destination)
    return(keys)
def fix_q(quality):
    
    
    if '1080' in quality:
      f_q=0
    elif '720' in quality:
      f_q=1
    elif '480' in quality:
      f_q=2
   
    elif '360' in quality or 'sd' in quality.lower():
      f_q=3
   
    return f_q
def getPublicStream(url):
        try:
            import http.cookiejar as cookielib
        except:
            import cookielib
        import mediaurl,urllib

        pquality=-1
        pformat=-1
        acodec=-1
        fmtlist=[]
        mediaURLs = []
  
       
        cookies = cookielib.LWPCookieJar()
        try:
            handlers = [
                urllib.request.HTTPHandler(),
                urllib.request.HTTPSHandler(),
                urllib.request.HTTPCookieProcessor(cookies)
                ]
            opener = urllib.request.build_opener(*handlers)
            log.warning(url)
            req = urllib.request.Request(url)
        except Exception as e:
            log.warning(e)
            import urllib2
            handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(cookies)
            ]
            opener = urllib2.build_opener(*handlers)
            log.warning(url)
            req = urllib2.Request(url)
        req.add_header('User-agent',__USERAGENT__)
        result= opener.open(req)
        for cookie in cookies:
            if cookie.name=='DRIVE_STREAM':
              value=cookie.value

        #response = urllib.urlopen(req)
        
        response_data = result.read()
        #response.close()




        regex='<title>(.+?)</title>'
        name=re.compile(regex).findall(response_data)[0]
        for r in re.finditer('\"fmt_list\"\,\"([^\"]+)\"' ,
                             response_data, re.DOTALL):
            fmtlist = r.group(1)

        title = ''
        for r in re.finditer('\"title\"\,\"([^\"]+)\"' ,
                             response_data, re.DOTALL):
            title = r.group(1)


        if fmtlist==[]:
            return 'Download',None,name
        itagDB={}
        containerDB = {'x-flv':'flv', 'webm': 'WebM', 'mp4;+codecs="avc1.42001E,+mp4a.40.2"': 'MP4'}
        for r in re.finditer('(\d+)/(\d+)x(\d+)/(\d+/\d+/\d+)\&?\,?' ,
                               fmtlist, re.DOTALL):
              (itag,resolution1,resolution2,codec) = r.groups()

              if codec == '9/0/115':
                itagDB[itag] = {'resolution': resolution2, 'codec': 'h.264/aac'}
              elif codec == '99/0/0':
                itagDB[itag] = {'resolution': resolution2, 'codec': 'VP8/vorbis'}
              else:
                itagDB[itag] = {'resolution': resolution2}

        for r in re.finditer('\"url_encoded_fmt_stream_map\"\,\"([^\"]+)\"' ,
                             response_data, re.DOTALL):
            urls = r.group(1)


        
        urls = urllib.unquote(urllib.unquote(urllib.unquote(urllib.unquote(urllib.unquote(urls)))))
        urls = re.sub('\\\\u003d', '=', urls)
        urls = re.sub('\\\\u0026', '&', urls)


#        urls = re.sub('\d+\&url\='+self.PROTOCOL, '\@', urls)
        urls = re.sub('\&url\='+ 'https://', '\@', urls)

#        for r in re.finditer('\@([^\@]+)' ,urls):
#          videoURL = r.group(0)
#        videoURL1 = self.PROTOCOL + videoURL


        # fetch format type and quality for each stream
        count=0
        
        for r in re.finditer('\@([^\@]+)' ,urls):
                videoURL = r.group(1)
                for q in re.finditer('itag\=(\d+).*?type\=video\/([^\&]+)\&quality\=(\w+)' ,
                             videoURL, re.DOTALL):
                    (itag,container,quality) = q.groups()
                    count = count + 1
                    order=0
                    if pquality > -1 or pformat > -1 or acodec > -1:
                        if int(itagDB[itag]['resolution']) == 1080:
                            if pquality == 0:
                                order = order + 1000
                            elif pquality == 1:
                                order = order + 3000
                            elif pquality == 3:
                                order = order + 9000
                        elif int(itagDB[itag]['resolution']) == 720:
                            if pquality == 0:
                                order = order + 2000
                            elif pquality == 1:
                                order = order + 1000
                            elif pquality == 3:
                                order = order + 9000
                        elif int(itagDB[itag]['resolution']) == 480:
                            if pquality == 0:
                                order = order + 3000
                            elif pquality == 1:
                                order = order + 2000
                            elif pquality == 3:
                                order = order + 1000
                        elif int(itagDB[itag]['resolution']) < 480:
                            if pquality == 0:
                                order = order + 4000
                            elif pquality == 1:
                                order = order + 3000
                            elif pquality == 3:
                                order = order + 2000
                    try:
                        if itagDB[itag]['codec'] == 'VP8/vorbis':
                            if acodec == 1:
                                order = order + 90000
                            else:
                                order = order + 10000
                    except :
                        order = order + 30000

                    try:
                        if containerDB[container] == 'MP4':
                            if pformat == 0 or pformat == 1:
                                order = order + 100
                            elif pformat == 3 or pformat == 4:
                                order = order + 200
                            else:
                                order = order + 300
                        elif containerDB[container] == 'flv':
                            if pformat == 2 or pformat == 3:
                                order = order + 100
                            elif pformat == 1 or pformat == 5:
                                order = order + 200
                            else:
                                order = order + 300
                        elif containerDB[container] == 'WebM':
                            if pformat == 4 or pformat == 5:
                                order = order + 100
                            elif pformat == 0 or pformat == 1:
                                order = order + 200
                            else:
                                order = order + 300
                        else:
                            order = order + 100
                    except :
                        pass

                    try:
                        mediaURLs.append( mediaurl.mediaurl('https://' + videoURL, itagDB[itag]['resolution'] + ' - ' + containerDB[container] + ' - ' + itagDB[itag]['codec'], str(itagDB[itag]['resolution'])+ '_' + str(order+count), order+count, title=title))
                    except KeyError:
                        mediaURLs.append(mediaurl.mediaurl('https://'+ videoURL, itagDB[itag]['resolution'] + ' - ' + container, str(itagDB[itag]['resolution'])+ '_' + str(order+count), order+count, title=title))
        
        return mediaURLs,value,name
        
def googledrive_resolve(id,items):
    path=xbmc_tranlate_path('special://home/addons/script.module.resolveurl/lib')
    sys.path.append( path)
    path=xbmc_tranlate_path('special://home/addons/script.module.six/lib')
    sys.path.append( path)
    path=xbmc_tranlate_path('special://home/addons/script.module.kodi-six/libs')
    sys.path.append( path)
    import resolveurl
    try:
        f_link =resolveurl .HostedMediaFile (url =items ).resolve ()
    except:
        return 'Download',[]
    log.warning(id)
    global tv_mode
    links_data,cookie,name=getPublicStream('https://drive.google.com/file/d/'+id+'/view')
    if links_data=='Download':
        return 'Download',name
    mediaURLs = sorted(links_data)
    options = []
    all_mediaURLs=[]
    for mediaURL in mediaURLs:
        log.warning(mediaURL.qualityDesc)
        if '4k' in mediaURL.qualityDesc:
           
           options.append('4000')
        elif '1080' in mediaURL.qualityDesc:
           
           options.append('1080')
        elif '720' in mediaURL.qualityDesc:
           
           options.append('720')
        elif '480' in mediaURL.qualityDesc:
           
           options.append('480')
        elif '360' in mediaURL.qualityDesc:
           
           options.append('360')
        elif '240' in mediaURL.qualityDesc:
           
           options.append('240')
        else:
           
           options.append('0')
        all_mediaURLs.append((mediaURL.url,fix_q(mediaURL.qualityDesc)))
    qualities=options
    qualities=sorted(options, key=lambda x: x[0], reverse=False)
    all_mediaURLs=sorted(all_mediaURLs, key=lambda x: x[1], reverse=False)
    
    if Addon.getSetting("auto_q")=='true':
            all_n=[]
            playbackURL,qul = all_mediaURLs[0]
            playbackURL=playbackURL+'||Cookie=DRIVE_STREAM%3D'+cookie
            all_n.append(name+' - [COLOR lightblue][B]'+str(options[0])+'[/B][/COLOR]')
    else:
        #ret = xbmcgui.Dialog().select("Choose", options)
        #if ret==-1:
        #    sys.exit()
        all_l=[]
        all_n=[]
        count=0
        for items in mediaURLs:
            all_l.append(items.url+'||Cookie=DRIVE_STREAM%3D'+cookie)
            all_n.append(name+' - [COLOR lightblue][B]'+str(options[count])+'[/B][/COLOR]')
            count+=1
        playbackURL = '$$$'.join(all_l)#[ret].url


    if len(all_n)==1:
        all_n=all_n[0]
    return playbackURL ,all_n

def get_resume(tmdb,saved_name,season,episode):
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
        dbcon.commit()
        log.warning('TMDB:'+str(tmdb))
        if len(str(tmdb))>2:
            dbcur.execute("SELECT * FROM playback where tmdb='%s' and season='%s' and episode='%s'"%(tmdb,str(season).replace('%20','0').replace(' ','0'),str(episode).replace('%20','0').replace(' ','0')))
            log.warning("SELECT * FROM playback where tmdb='%s' and season='%s' and episode='%s'"%(tmdb,str(season).replace('%20','0').replace(' ','0'),str(episode).replace('%20','0').replace(' ','0')))
        else:
            dbcur.execute("SELECT * FROM playback where name='%s' and season='%s' and episode='%s'"%(saved_name.replace("'","%27"),str(season).replace('%20','0').replace(' ','0'),str(episode).replace('%20','0').replace(' ','0')))
        match_playtime = dbcur.fetchone()
        if match_playtime!=None:

            name_r,timdb_r,season_r,episode_r,playtime,totaltime,free=match_playtime
            res={}
            res['wflag']=False
            res['resumetime']=playtime
            res['totaltime']=totaltime
        else:
            res=False
            
        set_runtime=0
        if res:
            if not res['wflag']:

                if res['resumetime']!=None:

                    #Resume From 
                    choose_time=Addon.getLocalizedString(32042)+time.strftime("%H:%M:%S", time.gmtime(float(res['resumetime'])))
                    
                    if float(res['resumetime'])>=(0.98*(float(res['totaltime']))):
                        selection=1
                        clicked=1
                    else:
                        selection,clicked=selection_time_menu('Menu',choose_time)
                        #window = selection_time('Menu',choose_time)
                        #window.doModal()
                        #selection = window.get_selection()
                        #clicked=window.clicked
                        #del window
                    if clicked==0:
                        set_runtime=-1
                        return -1
                    if selection==-1:
                       stop_auto_play=1
                       resume_time=-1
                       return 0
                    if selection==0:
                        
                        set_runtime=float(res['resumetime'])
                        set_total=res['totaltime']
                        
                        
                    elif selection==1:
                        
                        
                        set_runtime=0
                        set_total=res['totaltime']
        dbcur.close()
        dbcon.close()
        return set_runtime
def update_db_link(tmdb,saved_name,season,episode,g_timer,g_item_total_time):
        log.warning('TMDB:'+str(saved_name))
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
        dbcon.commit()
        season=season.replace('%20','0').replace(' ','0')
        episode=episode.replace('%20','0').replace(' ','0')
        if len(str(tmdb))<2  and tmdb!='%20':
            only_name=True
            dbcur.execute("SELECT * FROM playback where name='%s' and season='%s' and episode='%s'"%(saved_name.replace("'","%27"),season,episode))
        else:
            only_name=False
            dbcur.execute("SELECT * FROM playback where tmdb='%s' and season='%s' and episode='%s'"%(tmdb,season,episode))
        match = dbcur.fetchall()
        log.warning(match)
        
        if match==None:
          dbcur.execute("INSERT INTO playback Values ('%s','%s','%s','%s','%s','%s','%s');" %  (saved_name.replace("'","%27"),tmdb,season,episode,str(g_timer),str(g_item_total_time),' '))
          dbcon.commit()
        else:
           if len(match)>0:
            name,timdb,season,episode,playtime,totaltime,free=match[0]
            if str(g_timer)!=playtime:
                if only_name:
                    dbcur.execute("UPDATE playback SET playtime='%s' where name='%s' and  season='%s' and episode='%s'"%(str(g_timer),saved_name.replace("'","%27"),season,episode))
                else:
                    dbcur.execute("UPDATE playback SET playtime='%s' where tmdb='%s' and  season='%s' and episode='%s'"%(str(g_timer),tmdb,season,episode))
                dbcon.commit()
           else:
                dbcur.execute("INSERT INTO playback Values ('%s','%s','%s','%s','%s','%s','%s');" %  (saved_name.replace("'","%27"),tmdb,season,episode,str(g_timer),str(g_item_total_time),' '))
                dbcon.commit()
        dbcur.close()
        dbcon.close()
def copy2clip(txt):
    import subprocess
    platform = sys.platform
    log.warning(platform)
    if platform == 'win32':
        try:
            cmd = 'echo ' + txt.strip() + '|clip'
            return subprocess.check_call(cmd, shell=True)
            pass
        except:
            pass
    elif platform == 'linux2':
        try:
            from subprocess import Popen, PIPE

            p = Popen(['xsel', '-pi'], stdin=PIPE)
            p.communicate(input=txt)
        except:
            pass
    else:
        pass
    pass
def play_link(name,url,icon,fan,no_subs,tmdb,season,episode,original_title):
    if 1:#try:
        
        try:
            cond=xbmc.Monitor().abortRequested()
        except:
            cond=xbmc.abortRequested
        xbmc.executebuiltin("Dialog.Open(busydialog)")
        all_n=[]
        log.warning('inlink:'+url)
        
        if '$$$' in url:
            final_links=[]
            all_urls=url.split('$$$')
            for ite in all_urls:
                if ite not in final_links:
                    final_links.append(ite)
            all_urls=final_links
        else:
            all_urls=[url]
            log.warning('NO DOLAR')
        log.warning(len(all_urls))
        log.warning('len(all_urls)')
        log.warning((all_urls))
        if len(all_urls)>1:
            for itt in all_urls:
                
                if 'upfile' in url:
                    f_link,name=get_upfile_det(itt)
                    if f_link==0:
                        return 0
                    
                    all_n.append(name)
                else:
                    all_n.append(re.compile('//(.+?)/').findall(itt)[0])
            ret = xbmcgui.Dialog().select("choose", all_n)
            if ret!=-1:
                if 'google' in all_urls[ret] and '?' in all_urls[ret] and 'google.com/open?' not in all_urls[ret]:
                    all_urls[ret]=all_urls[ret].split('?')[0]
                all_urls=[all_urls[ret]]
                
            else:
              return 0
        else:
            all_urls=[all_urls[0]]
        all_l=[]
        all_n=[]
        
        for items in all_urls:
            if 'upfile' in url:
                f_link,name=get_upfile_det(items)
                if f_link==0:
                    return 0
                all_l.append(f_link)
                all_n.append(name)
            if 'youtu' in items:
                if 'youtu.be' in items:
                    items=get_html(items).url
                log.warning(items)
                regex='v\=(.+?)$'
                video_id=re.compile(regex).findall(items)[0]
                if 'list=' in items:
                    video_id=items.split ('list=')[1 ]
                    playback_url = 'plugin://plugin.video.youtube/play/?playlist_id=%s&order=shuffle&play=1'%video_id
                else:
                    playback_url = 'plugin://plugin.video.youtube/play/?video_id=%s' % video_id
                xbmc.executebuiltin('RunPlugin(%s)'%playback_url)
                return 0
                log.warning(playback_url)
                all_l.append(playback_url)
                all_n.append(name)
            if 'drive.google' in items or 'docs.google' in items:
              
              if 'docs.googleusercontent.com' in items:
                log.warning('Returning')
                return 0
              
              if '=' in items and 'usp=' not in items:
                id=items.split('=')[-1]
            
              else:
               regex='/d/(.+?)/view'
               match=re.compile(regex).findall(items)
               if len(match)>0:
                 id=match[0]
               else:
                 regex='/d/(.+?)/preview'
                 match=re.compile(regex).findall(items)
                 if len(match)>0:
                    id=match[0]
                 else:
                    regex='/d/(.+?)$'
                    match=re.compile(regex).findall(items)
                    if len(match)>0:
                        id=match[0]
                    else:
                        regex='id=(.+?)$'
                        match=re.compile(regex).findall(items)
                        id=match[0]
              log.warning(items)
              f_link,name= googledrive_resolve(id,items)
              if f_link=='Download':
                   f_link= googledrive_download(id)
                   name='Download '+name
              count=0
              if '$$$' in f_link:
                for item in f_link.split('$$$'):
                    all_l.append(item)
                    all_n.append(name[count])
                    count+=1
              else:
                all_l.append(f_link)
                all_n.append(name)
        if len(all_l)==1:
            final_link=all_l[0]
            name=all_n[0]
        elif len(all_l)>0:
            #"choose"
            ret = xbmcgui.Dialog().select(Addon.getLocalizedString(32028), all_n)
            if ret!=-1:
                final_link=all_l[ret]
                name=all_n[ret]
            else:
              return 0
        else:
            final_link=all_urls[0]
        if 'twitch' in final_link:
            twitch_p=os.path.join(xbmc_tranlate_path("special://home/addons/"),'plugin.video.twitch')
            if os.path.exists(twitch_p):
            
                regex='https://www.twitch.tv/(.+?)(?:$| |\r|\n|\t)'
                #ids=final_link.split('/')
                f_id=re.compile(regex).findall(final_link)[0]
                
                
                xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.twitch/?content=streams&mode=search_results&query=%s",return)'%f_id)          
            else:
                copy2clip('https://github.com/MrSprigster/Twitch-on-Kodi/releases/download/2.4.8/plugin.video.twitch-2.4.8.zip')
                xbmcgui.Dialog().ok('Error occurred','You need Twich addon to play this link\n link was copied to clipboard')
                
            return 0
        log.warning('final_link:'+final_link)
        log.warning(name)
        video_data={}
        if season!=None and season!="%20" and season!="0":
           video_data['TVshowtitle']=original_title.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
           video_data['mediatype']='tvshow'
           
        else:
           video_data['mediatype']='movies'
        if season!=None and season!="%20" and season!="0":
           tv_movie='tv'
           url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&append_to_response=external_ids'%(tmdb,'653bb8af90162bd98fc7ee32bcbbfb3d')
        else:
           tv_movie='movie'
           
           url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&append_to_response=external_ids'%(tmdb,'653bb8af90162bd98fc7ee32bcbbfb3d')
        if 'tt' not in tmdb:
             try:
                log.warning(url2)
                
                imdb_id=get_html(url2).json()['external_ids']['imdb_id']
                log.warning(imdb_id)
             except Exception as e:
                log.warning('IMDB err:'+str(e))
                imdb_id=" "
        else:
             imdb_id=tmdb
        video_data['title']=name.replace('.mp4','').replace('.avi','').replace('.mkv','').replace('-','').replace('Google Drive','').replace('[COLOR lightblue][B]','').replace('[/B][/COLOR]','').replace(' 360','').replace(' 480','').replace(' 720','').replace(' 1080','').strip()
        log.warning(video_data['title'])
        video_data['Writer']=tmdb
        video_data['season']=season
        video_data['episode']=episode
        video_data['plot']='from_telemedia'
        video_data['imdb']=imdb_id
        video_data['code']=imdb_id

        video_data['imdbnumber']=imdb_id
        
        video_data['imdb_id']=imdb_id
        video_data['IMDBNumber']=imdb_id
        video_data['genre']=imdb_id
        if no_subs=='1':
            video_data[u'mpaa']='heb'
        
        listItem = xbmcgui.ListItem(video_data['title'], path=final_link) 
        listItem.setInfo(type='Video', infoLabels=video_data)


        listItem.setProperty('IsPlayable', 'true')

       
        resume_time=get_resume(tmdb,name,season,episode)
        if resume_time==-1:
            return 0
        log.warning('resume_time:'+str(resume_time))
        ok=xbmc.Player().play(final_link,listitem=listItem)
        w_time=int(Addon.getSetting("wait_size"))
        fail_play=True
        for _ in range(w_time):
            
            try:
                vidtime = xbmc.Player().getTime()
            except:
                vidtime=0
                pass
            if xbmc.Player().isPlaying() and vidtime>0:
                fail_play=False
                break
           
                
               
            time.sleep(0.100)
        
        
        
        
        
        if resume_time>0:
            try:
                xbmc.Player().seekTime(int(float(resume_time)))
            except Exception as e:
                log.warning('Seek Err:'+str(e))
                pass
        
        while (not cond) and (xbmc.Player().isPlaying()):
             try:
                vidtime = xbmc.Player().getTime()
             except:
                vidtime = 0
             try:
                g_timer=xbmc.Player().getTime()
                g_item_total_time=xbmc.Player().getTotalTime()
             except:
                pass
             time.sleep(0.1)
        
        #dp.create('Please Wait...','Closing File', '','')
        #dp.update(0, 'Please Wait...','Canceling File', '' )
        
        #dp.update(0, 'Please Wait...','Removing File', '' )
        if resume_time!=-1:
            update_db_link(tmdb,name,season,episode,g_timer,g_item_total_time)
        xbmc.executebuiltin("Dialog.Close(busydialog)")
    '''
    except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            log.warning('ERROR IN Play:'+str(lineno))
            log.warning('inline:'+str(line))
            log.warning(str(e))
            xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
            xbmc.executebuiltin("Dialog.Close(busydialog)")
    '''
def movies_menu():
    all_d=[]
    aa=addDir3(Addon.getLocalizedString(32131),'http://api.themoviedb.org/3/movie/now_playing?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%lang,14,'special://home/addons/plugin.video.telemedia/tele/Movies/cinema.png','https://images.cdn1.stockunlimited.net/preview1300/cinema-background-with-movie-objects_1823387.jpg','Tmdb')
    all_d.append(aa)
    'Popular Movies'
    aa=addDir3(Addon.getLocalizedString(32047),'http://api.themoviedb.org/3/movie/popular?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%lang,14,'special://home/addons/plugin.video.telemedia/tele/Movies/popular.png','https://www.newszii.com/wp-content/uploads/2018/08/Most-Popular-Action-Movies.png','Tmdb')
    all_d.append(aa)

    #Genre
    aa=addDir3(Addon.getLocalizedString(32048),'http://api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%lang,18,'special://home/addons/plugin.video.telemedia/tele/Movies/genre.png','https://s.studiobinder.com/wp-content/uploads/2019/09/Movie-Genres-Types-of-Movies-List-of-Genres-and-Categories-Header-StudioBinder.jpg','Tmdb')
    all_d.append(aa)
    #Years
    aa=addDir3(Addon.getLocalizedString(32049),'movie_years&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Movies/years.png','https://i.pinimg.com/originals/e4/03/91/e4039182cd17c48c8f9cead44cda7df3.jpg','Tmdb')
    all_d.append(aa)
    aa=addDir3(Addon.getLocalizedString(32132),'movie_years&page=1',112,'special://home/addons/plugin.video.telemedia/tele/Movies/studio.png','https://cdn-static.denofgeek.com/sites/denofgeek/files/styles/main_wide/public/2016/04/movlic_studios_1.jpg?itok=ih8Z7wOk','Tmdb')
    all_d.append(aa)
    #movie World
    aa=addDir3('[COLOR lime]'+Addon.getLocalizedString(32074)+'[/COLOR]','www',31,'special://home/addons/plugin.video.telemedia/tele/Movies/movie_world.png','https://cdn.hipwallpaper.com/i/14/59/G8mUMK.jpg',Addon.getLocalizedString(32074),data=-1001000750206)
    all_d.append(aa)
    
    #ISRAEL NOVIES
    aa=addDir3('[COLOR pink]'+Addon.getLocalizedString(32075)+'[/COLOR]','www',31,'special://home/addons/plugin.video.telemedia/tele/Movies/israel.png','https://i.ytimg.com/vi/Hq0CZUvuSDs/maxresdefault.jpg',Addon.getLocalizedString(32075),data=HEBREW_GROUP)
    all_d.append(aa)
    #Search movie
    aa=addDir3(Addon.getLocalizedString(32070),'http://api.themoviedb.org/3/search/movie?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&language=he&append_to_response=origin_country&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Movies/movie_search.png','http://www.videomotion.co.il/wp-content/uploads/whatwedo-Pic-small.jpg','Tmdb')
    all_d.append(aa)
    
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def search_menu():
    all_d=[]
    #Search All
    aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32024)+'[/COLOR]',str(id),6,'https://sitechecker.pro/wp-content/uploads/2017/12/search-engines.png','https://www.komando.com/wp-content/uploads/2017/12/computer-search.jpg','Search All',last_id='0$$$0',data='all')
    all_d.append(aa)
        #Search Groups
    aa=addDir3('[COLOR white]'+Addon.getLocalizedString(32023)+'[/COLOR]',str(id),13,'https://pageloot.com/wp-content/uploads/elementor/thumbs/make-qr-codes-for-telegram-groups-o75hxtbe6pqtp9qokn9gy422mzjm9cdesi6lyghjjg.jpg','https://cdn.ilovefreesoftware.com/wp-content/uploads/2019/06/Search-Telegram-Channels.png','Search All',last_id='0$$$0',data='all')
    all_d.append(aa)
    #Search History
    aa=addDir3('[COLOR lightgreen]'+Addon.getLocalizedString(32072)+'[/COLOR]',str(id),30,'https://sitechecker.pro/wp-content/uploads/2017/12/search-engines.png','https://www.komando.com/wp-content/uploads/2017/12/computer-search.jpg','Search All',last_id='0$$$0',data='all')
    all_d.append(aa)
    
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def main_trakt():
   all_d=[]
   aa=addDir3('רשימות','www',116,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','רשימות')
   all_d.append(aa)
   aa=addDir3('התקדמות','users/me/watched/shows?extended=full',115,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','התקדמות')
   all_d.append(aa)
   aa=addDir3('פרקים בצפייה','sync/watchlist/episodes?extended=full',115,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','התקדמות')
   all_d.append(aa)
   aa=addDir3('סדרות בצפייה','users/me/watchlist/episodes?extended=full',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','אוסף')
   all_d.append(aa)
   aa=addDir3('אוסף','users/me/collection/shows',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','אוסף')
   all_d.append(aa)
   aa=addDir3('רשימות צפייה סדרות','users/me/watchlist/shows',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','אוסף')
   all_d.append(aa)
   aa=addDir3('רשימות צפייה סרטים','users/me/watchlist/movies',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','אוסף')
   all_d.append(aa)
   aa=addDir3('סרטים שנצפו','users/me/watched/movies',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','אוסף')
   all_d.append(aa)
   aa=addDir3('סדרות שנצפו','users/me/watched/shows',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','אוסף')
   all_d.append(aa)
   aa=addDir3('Movies Collection','users/me/collection/movies',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','collection')
   all_d.append(aa)
   aa=addDir3('Liked lists','users/likes/lists',118,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Watched shows')
   all_d.append(aa)
   xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def get_trakt():
    
    trakt_lists=call_trakt("users/me/lists")
    #trakt_lists=call_trakt('users/me/collection/shows')
  
    my_lists = []
    
    for list in trakt_lists:
        my_lists.append({
            'name': list["name"],
            'user': list["user"]["username"],
            'slug': list["ids"]["slug"]
        })

    for item in my_lists:
        user = item['user']
        slug = item['slug']
        url=user+'$$$$$$$$$$$'+slug
        addDir3(item['name'],url,31,' ',' ',item['name'])
def progress_trakt(url):
        all_trk_data={}
        
        if  Addon.getSetting("fav_search_f_tv")=='true' and Addon.getSetting("fav_servers_en_tv")=='true' and len(Addon.getSetting("fav_servers_tv"))>0:
           fav_status='true'
        else:
            fav_status='false'
        if Addon.getSetting("dp")=='true':
                dp = xbmcgui.DialogProgress()
                dp.create("טוען פרקים", "אנא המתן", '')
                dp.update(0)
        import datetime
        start_time = time.time()
        xxx=0
        ddatetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        url_g=domain_s+'api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'
     
  
        html_g=get_html(url_g).json()
        #html_g=html_g_tv
        result = call_trakt(url)
     
        items = []
        

        new_name_array=[]
        
        for item in result:
            
            try:
                num_1 = 0
                if 'seasons' in item:
                    for i in range(0, len(item['seasons'])):
                        if item['seasons'][i]['number'] > 0: num_1 += len(item['seasons'][i]['episodes'])
                    num_2 = int(item['show']['aired_episodes'])
                    if num_1 >= num_2: raise Exception()

                    season = str(item['seasons'][-1]['number'])

                    episode = [x for x in item['seasons'][-1]['episodes'] if 'number' in x]
                    episode = sorted(episode, key=lambda x: x['number'])
                    episode = str(episode[-1]['number'])
                else:
                    season = str(item['episode']['season'])
                    episode=str(item['episode']['number'])
                

                tvshowtitle = item['show']['title']
                if tvshowtitle == None or tvshowtitle == '': raise Exception()
                tvshowtitle = replaceHTMLCodes(tvshowtitle)

                year = item['show']['year']
                year = re.sub('[^0-9]', '', str(year))
                if int(year) > int(ddatetime.strftime('%Y')): raise Exception()

                imdb = item['show']['ids']['imdb']
                if imdb == None or imdb == '': imdb = '0'

                tmdb = item['show']['ids']['tmdb']
                if tmdb == None or tmdb == '': raise Exception()
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                
               
                trakt = item['show']['ids']['trakt']
                if trakt == None or trakt == '': raise Exception()
                trakt = re.sub('[^0-9]', '', str(trakt))
                if 'last_watched_at' in item:
                    last_watched = item['last_watched_at']
                else:
                    last_watched = item['listed_at']
                if last_watched == None or last_watched == '': last_watched = '0'
                items.append({'imdb': imdb, 'tmdb': tmdb, 'tvshowtitle': tvshowtitle, 'year': year, 'snum': season, 'enum': episode, '_last_watched': last_watched})
            
            except Exception as e:
               log.warning(e)
            
            
        result = call_trakt('/users/hidden/progress_watched?limit=1000&type=show')
        result = [str(i['show']['ids']['tmdb']) for i in result]

        items_pre = [i for i in items if not i['tmdb'] in result]

      
        for items in items_pre:
          watched='no'
          not_yet=0
          gone=0
          season=items['snum']
          episode=items['enum']
    
          url='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=he&append_to_response=external_ids'%(items['tmdb'],'653bb8af90162bd98fc7ee32bcbbfb3d')
          #url='http://api.themoviedb.org/3/tv/%s/season/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'%(items['tmdb'],season)
          html=cache.get(get_movie_data,time_to_save,url, table='pages')
          plot=' '
          if 'The resource you requested could not be found' not in str(html):
             data=html
            
             if 'vote_average' in data:
               rating=data['vote_average']
             else:
              rating=0
             if 'first_air_date' in data:
               year=str(data['first_air_date'].split("-")[0])
             else:
                if 'release_date' in data:
                  year=str(data['release_date'].split("-")[0])
                else:
                    year=' '
             if data['overview']==None:
               plot=' '
             else:
               plot=data['overview']
             if 'title' not in data:
               new_name=data['name']
             else:
               new_name=data['title']
             f_subs=[]
             
             original_name=data['original_name']
             id=str(data['id'])
             mode=4
             if data['poster_path']==None:
              icon=' '
             else:
               icon=data['poster_path']
             if 'backdrop_path' in data:
                 if data['backdrop_path']==None:
                  fan=' '
                 else:
                  fan=data['backdrop_path']
             else:
                fan=html['backdrop_path']
             if plot==None:
               plot=' '
             if 'http' not in fan:
               fan=domain_s+'image.tmdb.org/t/p/original/'+fan
             if 'http' not in icon:
               icon=domain_s+'image.tmdb.org/t/p/original/'+icon
             genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                    if i['name'] is not None])
             try:genere = u' / '.join([genres_list[x['id']] for x in data['genres']])
             except:genere=''

   
            
             trailer = "plugin://plugin.video.allmoviesin?mode=25&url=www&id=%s" % id
             if new_name not in new_name_array:
              new_name_array.append(new_name)
              if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
                  if len(f_subs)>0:
                    color='white'
                  else:
                    color='red'
                    
              else:
                 color='white'
              elapsed_time = time.time() - start_time
              if Addon.getSetting("dp")=='true':
                dp.update(int(((xxx* 100.0)/(len(html))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'[COLOR'+color+']'+new_name+'[/COLOR]')
              xxx=xxx+1
              if int(data['last_episode_to_air']['season_number'])>=int(season):
                if int(data['last_episode_to_air']['episode_number'])>int(episode):
                
                  episode=str(int(episode)+1)
                else:
                 if int(data['last_episode_to_air']['season_number'])>int(season):
                   season=str(int(season)+1)
                   episode='1'
                 else:
                  if (data['next_episode_to_air'])!=None:
                    episode=str(int(episode)+1)
                   
                    not_yet='1'
                  else:
                    gone=1
              else:
                    if (data['next_episode_to_air'])!=None:
                        season=str(int(season)+1)
                        episode='1'
                        not_yet='1'
                    else:
                        gone=1
              video_data={}

              

              video_data['mediatype']='tvshow'
              video_data['OriginalTitle']=new_name
              video_data['title']=new_name



              video_data['year']=year
              video_data['season']=season
              video_data['episode']=episode
              video_data['genre']=genere
              
              if len(episode)==1:
                  episode_n="0"+episode
              else:
                   episode_n=episode
              if len(season)==1:
                  season_n="0"+season
              else:
                  season_n=season
              if Addon.getSetting("trac_trk")=='true':
                addon='\n'+' עונה'+season_n+'-פרק '+episode_n
              else:
                addon=''
              video_data['plot']=plot+addon
              try:
                max_ep=data['seasons'][int(season)-1]['episode_count']
              except Exception as e:
                max_ep=100
            
              if gone==0:
                  if not_yet==0:
                  
                    if episode_n=='01':
                      dates=json.dumps((0,'' ,''))
                    elif max_ep<=int(episode):
                        dates=json.dumps(('','' ,0))
                    else:
                      dates=json.dumps(('','' ,''))
                    all_trk_data[id]={}
                    all_trk_data[id]['icon']=icon
                    all_trk_data[id]['fan']=fan
                    all_trk_data[id]['plot']=plot+addon
                    all_trk_data[id]['year']=year
                    all_trk_data[id]['original_title']=original_name
                    all_trk_data[id]['title']=new_name
                    all_trk_data[id]['season']=season
                    all_trk_data[id]['episode']=episode
                    all_trk_data[id]['eng_name']=original_title
                    all_trk_data[id]['heb_name']=new_name
                    all_trk_data[id]['type']='tv'
                    
                    
                    log.warning('121')
                    addDir3('[COLOR '+color+']'+new_name+'[/COLOR]'+' S'+season_n+'E'+episode_n,url,mode,icon,fan,plot+addon,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer,watched=watched,season=season,episode=episode,eng_name=original_title,tmdbid=id,video_info=video_data,dates=dates,fav_status=fav_status)
                  else:
                   addNolink('[COLOR red][I]'+ new_name+'[/I][/COLOR]'+' S'+season_n+'E'+episode_n, 'www',999,False,iconimage=icon,fanart=fan)
          else:
            
            log.warning('323')
            responce=call_trakt("shows/{0}".format(items['trakt']), params={'extended': 'full'})
          
           
            addNolink('[COLOR red][I]'+ responce['title']+'[/I][/COLOR]', 'www',999,False)
        log.warning('424')
        if Addon.getSetting("dp")=='true':
          dp.close()
        log.warning('H7')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
        return all_trk_data
def get_trk_data(url):
        all_trk_data={}
        # time_to_save=int(Addon.getSetting("save_time"))
        xxx=0
        if Addon.getSetting("dp")=='true':
                    dp = xbmcgui.DialogProgress()
                    dp.create("טוען סרטים", "אנא המתן", '')
                    dp.update(0)
        url_g_m=domain_s+'api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'
                     
        
        url_g_tv=domain_s+'api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'
        #html_g_tv=get_html(url_g_tv).json()
        #html_g_m=get_html(url_g_m).json()
        #html_g_tv=html_g_tv
        html_g_m=html_g_movie
        start_time = time.time()
        src="tmdb" 
            
        i = (call_trakt('/users/me/watched/movies'))
        
        all_movie_w=[]
        for ids in i:
          all_movie_w.append(str(ids['movie']['ids']['tmdb']))
        '''
        i = (call_trakt('/users/me/watched/shows?extended=full'))
        all_tv_w={}
        for ids in i:
         all_tv_w[str(ids['show']['ids']['tmdb'])]=[]
         for seasons in ids['seasons']:
          for ep in seasons['episodes']:
            all_tv_w[str(ids['show']['ids']['tmdb'])].append(str(seasons['number'])+'x'+str(ep['number']))
        '''
         
        if '$$$$$$$$$$$' in url:
            data_in=url.split('$$$$$$$$$$$')
            user = data_in[0]
            slug = data_in[1]
            selected={'slug':data_in[1],'user':data_in[0]}

            responce=call_trakt("/users/{0}/lists/{1}/items".format(user, slug))
        else:
           responce=call_trakt(url)
        new_name_array=[]

        for items in responce:
          
          if 'show' in items:
             slug = 'tv'
             html_g=html_g_tv
          else:
            slug = 'movies'
            html_g=html_g_m
          if slug=='movies':
            url='http://api.themoviedb.org/3/movie/%s?api_key=%s&language=he&append_to_response=external_ids'%(items['movie']['ids']['tmdb'],'653bb8af90162bd98fc7ee32bcbbfb3d')
          else:
            url='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=he&append_to_response=external_ids'%(items['show']['ids']['tmdb'],'653bb8af90162bd98fc7ee32bcbbfb3d')
          
          html=cache.get(get_movie_data,72,url, table='pages')
          if 'The resource you requested could not be found' not in str(html):
             data=html
             if 'overview' not in data:
                continue
             if 'vote_average' in data:
               rating=data['vote_average']
             else:
              rating=0
             if 'first_air_date' in data :
               if data['first_air_date']==None:
                    year=' '
               else:
                   year=str(data['first_air_date'].split("-")[0])
             else:
                 if 'release_date' in data:
                    if data['release_date']==None:
                        year=' '
                    else:
                        year=str(data['release_date'].split("-")[0])
                 else:
                    year=' '
        
             if data['overview']==None:
               plot=' '
             else:
               plot=data['overview']
             if 'title' not in data:
               new_name=data['name']
             else:
               new_name=data['title']
             f_subs=[]
             if slug=='movies':
               original_name=data['original_title']
               mode=4
               
               id=str(data['id'])
               if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
                 f_subs=cache.get(get_subs,9999,'movie',original_name,'0','0',id,year,True, table='pages')
               
               
             else:
               original_name=data['original_name']
               id=str(data['id'])
               mode=7
             if data['poster_path']==None:
              icon=' '
             else:
               icon=data['poster_path']
             if 'backdrop_path' in data:
                 if data['backdrop_path']==None:
                  fan=' '
                 else:
                  fan=data['backdrop_path']
             else:
                fan=html['backdrop_path']
             if plot==None:
               plot=' '
             if 'http' not in fan:
               fan=domain_s+'image.tmdb.org/t/p/original/'+fan
             if 'http' not in icon:
               icon=domain_s+'image.tmdb.org/t/p/original/'+icon
             genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                    if i['name'] is not None])
             try:genere = u' / '.join([genres_list[x['id']] for x in data['genres']])
             except:genere=''

   
            
             trailer = "plugin://plugin.video.allmoviesin?mode=25&url=www&id=%s" % id
             if new_name not in new_name_array:
              new_name_array.append(new_name)
              if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
                  if len(f_subs)>0:
                    color='white'
                  else:
                    color='red'
                    
              else:
                 color='white'
              elapsed_time = time.time() - start_time
              if Addon.getSetting("dp")=='true':
                dp.update(int(((xxx* 100.0)/(len(html))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'[COLOR'+color+']'+new_name+'[/COLOR]')
              xxx=xxx+1
              watched='no'
              if id in all_movie_w:
                watched='yes'
              '''
              if id in all_tv_w:
                 if season+'x'+episode in all_tv_w[id]:
                  watched='yes'
              '''
              if slug=='movies':
                    fav_search_f=Addon.getSetting("fav_search_f")
                    fav_servers_en=Addon.getSetting("fav_servers_en")
                    fav_servers=Addon.getSetting("fav_servers")
                   
                    google_server= Addon.getSetting("google_server")
                    rapid_server=Addon.getSetting("rapid_server")
                    direct_server=Addon.getSetting("direct_server")
                    heb_server=Addon.getSetting("heb_server")
              else:
                    fav_search_f=Addon.getSetting("fav_search_f_tv")
                    fav_servers_en=Addon.getSetting("fav_servers_en_tv")
                    fav_servers=Addon.getSetting("fav_servers_tv")
                    google_server= Addon.getSetting("google_server_tv")
                    rapid_server=Addon.getSetting("rapid_server_tv")
                    direct_server=Addon.getSetting("direct_server_tv")
                    heb_server=Addon.getSetting("heb_server_tv")
        
   
              if  fav_search_f=='true' and fav_servers_en=='true' and (len(fav_servers)>0 or heb_server=='true' or google_server=='true' or rapid_server=='true' or direct_server=='true'):
                    fav_status='true'
              else:
                    fav_status='false'
             
              all_trk_data[id]={}
              all_trk_data[id]['icon']=icon
              all_trk_data[id]['fan']=fan
              all_trk_data[id]['plot']=plot
              all_trk_data[id]['year']=year
              all_trk_data[id]['original_title']=original_name
              all_trk_data[id]['title']=new_name
              all_trk_data[id]['season']='%20'
              all_trk_data[id]['episode']='%20'
              all_trk_data[id]['eng_name']=original_name
              all_trk_data[id]['heb_name']=new_name
              all_trk_data[id]['type']='movie'
              addDir3('[COLOR '+color+']'+new_name+'[/COLOR]',url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer,watched=watched,fav_status=fav_status)
          else:
            
            if slug=='movies':
                responce=call_trakt("movies/{0}".format(items['movie']['ids']['trakt']), params={'extended': 'full'})
            else:
                responce=call_trakt("shows/{0}".format(items['show']['ids']['trakt']), params={'extended': 'full'})
           
           
            addNolink('[COLOR red][I]'+ responce['title']+'[/I][/COLOR]', 'www',999,False)
            
        if Addon.getSetting("dp")=='true':
          dp.close()
        log.warning('H8')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
        return all_trk_data

def get_one_trk(color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image):
          global all_data_imdb
          import _strptime
          data_ep=''
          dates=' '
          fanart=image
          url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'%(id,season)
         
          html=get_html(url).json()
          next=''
          ep=0
          f_episode=0
          catch=0
          counter=0
          if 'episodes' in html:
              for items in html['episodes']:
                if 'air_date' in items:
                   try:
                       datea=items['air_date']+'\n'
                       
                       a=(time.strptime(items['air_date'], '%Y-%m-%d'))
                       b=time.strptime(str(time.strftime('%Y-%m-%d')), '%Y-%m-%d')
                      
                   
                       if a>b:
                         if catch==0:
                           f_episode=counter
                           
                           catch=1
                       counter=counter+1
                       
                   except:
                         ep=0
          else:
             ep=0
          episode_fixed=int(episode)-1
          try:
              plot=html['episodes'][int(episode_fixed)]['overview']
          
              ep=len(html['episodes'])
              if (html['episodes'][int(episode_fixed)]['still_path'])==None:
                fanart=image
              else:
                fanart=domain_s+'image.tmdb.org/t/p/original/'+html['episodes'][int(episode_fixed)]['still_path']
              if f_episode==0:
                f_episode=ep
              data_ep='[COLOR aqua]'+'עונה '+season+'-פרק '+episode+ '[/COLOR]\n[COLOR yellow] מתוך ' +str(f_episode)  +' פרקים לעונה זו [/COLOR]\n' 
              if int(episode)>1:
                
                prev_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)-1]['air_date'], '%Y-%m-%d'))) 
              else:
                prev_ep=0

          

                      
              if int(episode)<ep:

                if (int(episode)+1)>=f_episode:
                  color_ep='magenta'
                  next_ep='[COLOR %s]'%color_ep+time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) +'[/COLOR]'
                else:
                  
                  next_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) 
              else:
                next_ep=0
              dates=((prev_ep,time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)]['air_date'], '%Y-%m-%d'))) ,next_ep))
              if int(episode)<int(f_episode):
               color='yellow'
              else:
               color='white'
               h2=get_html('https://api.themoviedb.org/3/tv/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=en-US'%id).json()
               last_s_to_air=int(h2['last_episode_to_air']['season_number'])
               last_e_to_air=int(h2['last_episode_to_air']['episode_number'])
              
               if int(season)<last_s_to_air:
                 log.warning('bigger One')
                 color='lightblue'
            
               if h2['status']=='Ended' or h2['status']=='Canceled':
                color='peru'
               
               
               if h2['next_episode_to_air']!=None:
                 
                 if 'air_date' in h2['next_episode_to_air']:
                  
                  a=(time.strptime(h2['next_episode_to_air']['air_date'], '%Y-%m-%d'))
                  next=time.strftime( "%d-%m-%Y",a)
                  
               else:
                  next=''
                 
          except Exception as e:
              log.warning('Error :'+ heb_name)
              log.warning('Error :'+ str(e))
              plot=' '
              color='green'
              if f_episode==0:
                f_episode=ep
              data_ep='[COLOR aqua]'+'עונה '+season+'-פרק '+episode+ '[/COLOR]\n[COLOR yellow] מתוך ' +str(f_episode)  +' פרקים לעונה זו [/COLOR]\n' 
              dates=' '
              fanart=image
          try:
            f_name= urllib.parse.unquote_plus(heb_name)
     
          except:
            f_name=name
          if (heb_name)=='':
            f_name=name
          if color=='peru':
            add_p='[COLOR peru][B]סדרה זו הסתיימה או בוטלה[/B][/COLOR]'+'\n'
          else:
            add_p=''
          add_n=''
          if color=='white' and url_o=='tv' :
              if next !='':
                add_n='[COLOR tomato][I]פרק הבא ישודר ב ' +next+'[/I][/COLOR]\n'
              else:
                add_n='[COLOR tomato][I]פרק הבא ישודר ב ' +' לא ידוע עדיין '+'[/I][/COLOR]\n'
                next='???'
          
          added_txt=' [COLOR khaki][I]%sx%s[/I][/COLOR] '%(season,episode)
          all_data_imdb.append((color,f_name+' '+added_txt+' '+next,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx))
          return data_ep,dates,fanart,color,next
def get_Series_trk_data(url_o,match):
        import _strptime
        cacheFile_trk = os.path.join(user_dataDir, 'cache_play_trk.db')
        dbcon_trk2 = database.connect(cacheFile_trk)
        dbcur_trk2  = dbcon_trk2.cursor()
        dbcur_trk2.execute("CREATE TABLE IF NOT EXISTS %s ( ""data_ep TEXT, ""dates TEXT, ""fanart TEXT,""color TEXT,""id TEXT,""season TEXT,""episode TEXT, ""next TEXT,""plot TEXT);" % 'AllData4')
        dbcon_trk2.commit()
        dbcur_trk2.execute("DELETE FROM AllData4")
        log.warning('Updating sh')
        image=' '
        for item in match:
          next=''
          name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,tv_movie=item
          #name,id,season,episode=item
          data_ep=''
          dates=' '
          fanart=image
          url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'%(id,season)
         
          html=get_html(url).json()
          if 'status_message' in html:
            if html['status_message']!='The resource you requested could not be found.':
                xbmc.sleep(10000)
                html=get_html(url).json()
            
          ep=0
          f_episode=0
          catch=0
          counter=0
          if 'episodes' in html:
              for items in html['episodes']:
                if 'air_date' in items:
                   try:
                       datea=items['air_date']+'\n'
                       
                       a=(time.strptime(items['air_date'], '%Y-%m-%d'))
                       b=time.strptime(str(time.strftime('%Y-%m-%d')), '%Y-%m-%d')
                      
                   
                       if a>b:
                         if catch==0:
                           f_episode=counter
                           
                           catch=1
                       counter=counter+1
                       
                   except:
                         ep=0
          else:
             ep=0
          episode_fixed=int(episode)-1
          try:
              try:
                plot=html['episodes'][int(episode_fixed)]['overview']
              except:
                log.warning(name.decode('utf-8'))
                if 'episodes' not in html:
                    log.warning(html)
                    
                
                log.warning(episode_fixed)
                
                plot=''
                pass
              
          
              ep=len(html['episodes'])
              if (html['episodes'][int(episode_fixed)]['still_path'])==None:
                fanart=image
              else:
                fanart=domain_s+'image.tmdb.org/t/p/original/'+html['episodes'][int(episode_fixed)]['still_path']
              if f_episode==0:
                f_episode=ep
              data_ep='[COLOR aqua]'+'עונה '+season+'-פרק '+episode+ '[/COLOR]\n[COLOR yellow] מתוך ' +str(f_episode)  +' פרקים לעונה זו [/COLOR]\n' 
              if int(episode)>1:
                
                prev_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)-1]['air_date'], '%Y-%m-%d'))) 
              else:
                prev_ep=0

          

              try:
                  if int(episode)<ep:
                    
                    if (int(episode)+1)>=f_episode:
                      color_ep='magenta'
                      next_ep='[COLOR %s]'%color_ep+time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) +'[/COLOR]'
                    else:
                      
                      next_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) 
                  else:
                    next_ep=0
              except:
                next_ep=0
              dates=((prev_ep,time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)]['air_date'], '%Y-%m-%d'))) ,next_ep))
              if int(episode)<int(f_episode):
               color='yellow'
              else:
               color='white'
               h2=get_html('https://api.themoviedb.org/3/tv/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=en-US'%id).json()
               last_s_to_air=int(h2['last_episode_to_air']['season_number'])
               last_e_to_air=int(h2['last_episode_to_air']['episode_number'])
              
               if int(season)<last_s_to_air:
                 log.warning('bigger')
                 color='lightblue'
               if h2['status']=='Ended' or h2['status']=='Canceled':
                color='peru'
                
               if h2['next_episode_to_air']!=None:
                 if 'air_date' in h2['next_episode_to_air']:
                    a=(time.strptime(h2['next_episode_to_air']['air_date'], '%Y-%m-%d'))
                    next=time.strftime( "%d-%m-%Y",a)
               else:
                  next=''
          
          except Exception as e:
              import linecache
              exc_type, exc_obj, tb = sys.exc_info()
              f = tb.tb_frame
              lineno = tb.tb_lineno
              filename = f.f_code.co_filename
              linecache.checkcache(filename)
              line = linecache.getline(filename, lineno, f.f_globals)
              error='''\
              line no:%s,
              line:%s,
              error:%s,
              url:%s,
              ep_no:%s,
              '''%(str(lineno),line,str(e),url,episode_fixed)
              
              
              
              
              log.warning(error)
              log.warning('BAD Series Tracker')
              plot=' '
              color='green'
              if f_episode==0:
                f_episode=ep
              data_ep='[COLOR aqua]'+'עונה '+season+'-פרק '+episode+ '[/COLOR]\n[COLOR yellow] מתוך ' +str(f_episode)  +' פרקים לעונה זו [/COLOR]\n' 
              dates=' '
              fanart=image
          
          dbcon_trk2.execute("INSERT INTO AllData4 Values ('%s', '%s', '%s', '%s','%s', '%s', '%s','%s','%s');" % (data_ep.replace("'","%27"),json.dumps(dates),fanart.replace("'","%27"),color,id,season,episode,next,plot.replace("'","%27")))
        dbcon_trk2.commit()
        dbcon_trk2.close()
        log.warning('TRD SUCE')
        return 0
def ClearCache():
    from resources.modules import cache
    cache.clear(['cookies', 'pages','posters','posters_n'])
   

    

    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Telemedia', 'Cleaned')))
def trakt_liked(url,iconImage,fanart):
    responce=call_trakt(url)
   
            
    for items in responce:
        url=items['list']['user']['username']+'$$$$$$$$$$$'+items['list']['ids']['slug']
        addDir3(items['list']['name'],url,31,iconImage,fanart,items['list']['description'])
def get_genere(link):
   tv_images={u'\u05d0\u05e7\u05e9\u05df \u05d5\u05d4\u05e8\u05e4\u05ea\u05e7\u05d0\u05d5\u05ea': 'http://stavarts.com/wp-content/uploads/2017/10/%D7%A9%D7%99%D7%A9%D7%99-%D7%94%D7%A8%D7%A4%D7%AA%D7%A7%D7%90%D7%95%D7%AA-%D7%AA%D7%A9%D7%A2%D7%B4%D7%97-%D7%A8%D7%90%D7%92%D7%A0%D7%90%D7%A8%D7%95%D7%A7_Page_1.jpg', u'\u05de\u05e1\u05ea\u05d5\u05e8\u05d9\u05df': 'http://avi-goldberg.com/wp-content/uploads/5008202002.jpg', u'\u05d9\u05dc\u05d3\u05d9\u05dd': "https://"+'i.ytimg.com/vi/sN4xfdDwjHk/maxresdefault.jpg', u'\u05de\u05e2\u05e8\u05d1\u05d5\u05df': "https://"+'i.ytimg.com/vi/Jw1iuGaNuy0/hqdefault.jpg', u'\u05e4\u05e9\u05e2': 'http://www.mapah.co.il/wp-content/uploads/2012/09/DSC_1210.jpg', u'\u05e8\u05d9\u05d0\u05dc\u05d9\u05d8\u05d9': 'http://blog.tapuz.co.il/oferD/images/%7B2D0A8A8A-7F57-4C8F-9290-D5DB72F06509%7D.jpg', u'\u05de\u05e9\u05e4\u05d7\u05d4': 'http://kaye7.school.org.il/photos/family.jpg', u'\u05e1\u05d1\u05d5\u05df': 'http://www.myliberty.co.il/media/com_hikashop/upload/2-1.jpg', u'\u05d7\u05d3\u05e9\u05d5\u05ea': "https://"+'shaza10.files.wordpress.com/2010/11/d790d795d79cd7a4d79f-d797d793d7a9-d797d793d7a9d795d7aa-10-d7a6d799d79cd795d79d-d7aad795d79ed7a8-d7a4d795d79cd798d799d79f03.jpg', u'\u05e7\u05d5\u05de\u05d3\u05d9\u05d4': "https://"+'upload.wikimedia.org/wikipedia/he/e/ef/Le_Tout_Nouveau_Testament.jpg', u'\u05d0\u05e0\u05d9\u05de\u05e6\u05d9\u05d4': 'http://www.printime.co.il/image/users/16584/ftp/my_files/smileynumbers1we.jpg', u'\u05de\u05d3\u05e2 \u05d1\u05d3\u05d9\u05d5\u05e0\u05d9 \u05d5\u05e4\u05e0\u05d8\u05d6\u05d9\u05d4': "https://"+'media.getbooks.co.il/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/s/h/shemharuach_getbooks-copy.jpg', u'\u05d3\u05e8\u05de\u05d4': 'http://www.yorav.co.il/images/moshe+erela/2007/dram.JPG', u'\u05d3\u05d5\u05e7\u05d5\u05de\u05e0\u05d8\u05e8\u05d9': 'http://img.mako.co.il/2017/03/28/704104_I.jpg', u'\u05de\u05dc\u05d7\u05de\u05d4 \u05d5\u05e4\u05d5\u05dc\u05d9\u05d8\u05d9\u05e7\u05d4': "https://"+'dannyorbach.files.wordpress.com/2013/05/berlinsynagoge.jpg', u'\u05d3\u05d9\u05d1\u05d5\u05e8\u05d9\u05dd': 'http://www.news1.co.il/uploadimages/NEWS1-556713283061982.jpg'}
   movie_images={u'\u05de\u05d5\u05e1\u05d9\u05e7\u05d4': 'http://www.blich.ramat-gan.k12.il/sites/default/files/files/music.jpg', u'\u05e1\u05e8\u05d8 \u05d8\u05dc\u05d5\u05d9\u05d6\u05d9\u05d4': 'https://i.ytimg.com/vi/hFc1821MSoA/hqdefault.jpg', u'\u05d4\u05e8\u05e4\u05ea\u05e7\u05d0\u05d5\u05ea': "https://"+'upload.wikimedia.org/wikipedia/he/3/38/%D7%94%D7%A8%D7%A4%D7%AA%D7%A7%D7%90%D7%95%D7%AA_%D7%91%D7%A8%D7%A0%D7%A8%D7%93_%D7%95%D7%91%D7%99%D7%90%D7%A0%D7%A7%D7%94_%D7%9B%D7%A8%D7%96%D7%94_%D7%A2%D7%91%D7%A8%D7%99%D7%AA.png', u'\u05de\u05e1\u05ea\u05d5\u05e8\u05d9\u05df': 'http://avi-goldberg.com/wp-content/uploads/5008202002.jpg', u'\u05de\u05e2\u05e8\u05d1\u05d5\u05df': "https://"+'i.ytimg.com/vi/Jw1iuGaNuy0/hqdefault.jpg', u'\u05de\u05dc\u05d7\u05de\u05d4': 'http://images.nana10.co.il/upload/mediastock/img/16/0/208/208383.jpg', u'\u05e4\u05e9\u05e2': 'http://www.mapah.co.il/wp-content/uploads/2012/09/DSC_1210.jpg', u'\u05e4\u05e0\u05d8\u05d6\u05d9\u05d4': 'http://blog.tapuz.co.il/beinhashurot/images/1943392_142.jpg', u'\u05de\u05e9\u05e4\u05d7\u05d4': 'http://kaye7.school.org.il/photos/family.jpg', u'\u05e7\u05d5\u05de\u05d3\u05d9\u05d4': "https://"+'upload.wikimedia.org/wikipedia/he/e/ef/Le_Tout_Nouveau_Testament.jpg', u'\u05d0\u05e0\u05d9\u05de\u05e6\u05d9\u05d4': 'http://www.printime.co.il/image/users/16584/ftp/my_files/smileynumbers1we.jpg', u'\u05d3\u05e8\u05de\u05d4': 'http://www.yorav.co.il/images/moshe+erela/2007/dram.JPG', u'\u05d4\u05e1\u05d8\u05d5\u05e8\u05d9\u05d4': "https://"+'medicine.ekmd.huji.ac.il/schools/occupationaltherapy/He/about/PublishingImages/%d7%aa%d7%9e%d7%95%d7%a0%d7%94%207.jpg', u'\u05e8\u05d5\u05de\u05e0\u05d8\u05d9': "https://"+'i.ytimg.com/vi/oUon62EIInc/maxresdefault.jpg', u'\u05d3\u05d5\u05e7\u05d5\u05de\u05e0\u05d8\u05e8\u05d9': 'http://img.mako.co.il/2017/03/28/704104_I.jpg', u'\u05d0\u05d9\u05de\u05d4': 'http://up203.siz.co.il/up2/y12o20immdyw.jpg', u'\u05de\u05d5\u05ea\u05d7\u05df': 'http://www.brz.co.il/wp-content/uploads/2014/06/11-350x350.jpg', u'\u05de\u05d3\u05e2 \u05d1\u05d3\u05d9\u05d5\u05e0\u05d9': "https://"+'upload.wikimedia.org/wikipedia/commons/c/cc/4pen.jpg', u'\u05d0\u05e7\u05e9\u05df': "https://"+'www.renne.co.il/wp-content/uploads/2017/07/actionsign.jpg'}

   images={}
   html=get_html(link).json()
   aa=[]
   image='https://wordsfromjalynn.files.wordpress.com/2014/12/movie-genres-1.png'
   for data in html['genres']:
     if '/movie' in link:
       new_link='http://api.themoviedb.org/3/genre/%s/movies?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%(str(data['id']),lang)
     else:
       new_link='http://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&sort_by=popularity.desc&with_genres=%s&language=%s&page=1'%(str(data['id']),lang)
     if data['name'] in tv_images:
       image=tv_images[data['name']]
     elif data['name'] in movie_images:
       image=movie_images[data['name']]
     
     aa.append(addDir3(data['name'],new_link,14,image,image,data['name']))
   xbmcplugin .addDirectoryItems(int(sys.argv[1]),aa,len(aa))
def tv_show_menu():
    all=[]
    import datetime
    now = datetime.datetime.now()
    #Popular
    aa=addDir3(Addon.getLocalizedString(32057),'http://api.themoviedb.org/3/tv/popular?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%lang,14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/popular_tv.png','https://image.businessinsider.com/5d5ea69fcd97841fea3d3b36?width=1100&format=jpeg&auto=webp','TMDB')
    all.append(aa)
    aa=addDir3(Addon.getLocalizedString(32133),'https://api.themoviedb.org/3/tv/on_the_air?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%lang,14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/on_air.png','https://i.pinimg.com/236x/1c/49/8f/1c498f196ef8818d3d01223b72678fc4--divergent-movie-poster-divergent-.jpg','TMDB')
    all.append(aa)
    #Genre
    aa=addDir3(Addon.getLocalizedString(32048),'http://api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%lang,18,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/genre.png','https://consequenceofsound.net/wp-content/uploads/2019/11/CoS_2010sDecades-TVShows.jpg?quality=80','TMDB')
    all.append(aa)
	#New_Tv_Shows
    aa=addDir3(Addon.getLocalizedString(32139),'https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language=en-US&sort_by=popularity.desc&first_air_date_year='+str(now.year)+'&timezone=America%2FNew_York&include_null_first_air_ates=false&language=he&page=1',14,
	'special://home/addons/plugin.video.telemedia/tele/Tv_Show/new_tv.png',
	'https://lh5.ggpht.com/cr6L4oleXlecZQBbM1EfxtGggxpRK0Q1cQ8JBtLjJdeUrqDnXAeBHU30trRRnMUFfSo=w300','TMDB')
    all.append(aa)	
    #Years
    aa=addDir3(Addon.getLocalizedString(32049),'tv_years&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/years.png','https://d2yhzr6tx8qnba.cloudfront.net/images/db/9/b6/58e2db43d1b69.jpeg','TMDB')
    all.append(aa)
    aa=addDir3(Addon.getLocalizedString(32134),'tv_years&page=1',101,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/network.png','https://images.pond5.com/tv-networks-logos-loop-footage-042898083_prevstill.jpeg','TMDB')
    all.append(aa)
    aa=addDir3(Addon.getLocalizedString(32135),'https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language={0}&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language={1}&page=1'.format(lang,lang),14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/israel.png','http://coldshotproductions.net/flachannelbanner.png',Addon.getLocalizedString(32135))
    all.append(aa)
    #Add Turkish Tv shows
    aa=addDir3(Addon.getLocalizedString(32101),'https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language={0}&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language={1}&page=1'.format(lang,'tr'),14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/turkish.png','http://coldshotproductions.net/flachannelbanner.png',Addon.getLocalizedString(32046))
    all.append(aa)
    aa=addDir3(Addon.getLocalizedString(32136),'https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language={0}&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language={1}&page=1'.format(lang,'tr'),114,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/my_tv.png','http://mjdtech.net/content/images/2016/02/traktfeat.jpg',Addon.getLocalizedString(32046))
    #all.append(aa)
    aa=addDir3(Addon.getLocalizedString(32055),'www',28,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/my_tv.png','http://coldshotproductions.net/flachannelbanner.png',Addon.getLocalizedString(32055))
    all.append(aa)
    #Search tv
    aa=addDir3(Addon.getLocalizedString(32071),'http://api.themoviedb.org/3/search/tv?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&language=he&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/search.png','http://f.frogi.co.il/news/640x300/010170efc8f.jpg','TMDB')
    all.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all,len(all))
def search_movies(heb_name,original_title,data,iconimage,fanart,tmdb,season,episode,remote=False):
    log.warning('Searching now:'+heb_name)
    log.warning('Searching now:'+original_title)
    original_title=original_title.replace('%20',' ')
    all_links=search(tmdb,'all','0$$$0',heb_name,iconimage,fanart,season,episode,no_subs=1,original_title=original_title,dont_return=False,manual=False)
    all_links=all_links+search(tmdb,'all','0$$$0',original_title,iconimage,fanart,season,episode,original_title=original_title,dont_return=False,manual=False)
    all_links=sorted(all_links, key=lambda x: x[4], reverse=False)
    all_results=[]
    filter_dup=Addon.getSetting("dup_links")=='true'
    all_t_links=[]
    once=0
    d_save=[]
    for  name, link,mode,q,loc, icon,fan,plot,no_subs,tmdb,season,episode,original_title in all_links:
        if once==0:
            once=1
            d_save.append((name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,plot))
        if name not in all_t_links or filter_dup==False:
            
                all_t_links.append(name)
                all_results.append((name, link,mode,q,loc, icon,fan,plot,no_subs,tmdb,season,episode,original_title))
                if remote==False:
                    addLink( name, link,mode,False, icon,fan,plot,no_subs=no_subs,tmdb=tmdb,season=season,episode=episode,original_title=original_title)
    if Addon.getSetting("one_click")=='true' and remote==False:
        if len(d_save)==0:
            xbmcgui.Dialog().ok('Telemedia','Sorry no sources found')
        else:
            name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,plot=d_save[0]
            play(name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,plot,None)
    return all_results
def clear_color(name):
    new_name=name
    if '[COLOR' in name:
        regex='\](.+?)\['
        n_name=re.compile(regex).findall(name)
        if len(n_name)>0:
            new_name=n_name[0]
    return new_name
def search_tv(heb_name,original_title,data,iconimage,fanart,season,episode,tmdb,remote=False):
    
    heb_name=clear_color(heb_name)
    log.warning('heb_name:'+heb_name)
    log.warning('original_title:'+original_title)
    original_title=original_title.replace('%20',' ')
    if len(episode)==1:
      episode_n="0"+episode
    else:
       episode_n=episode
    if len(season)==1:
      season_n="0"+season
    else:
      season_n=season
    all_links=[]
    c_original=original_title.replace('%20','.').replace(' ','.').replace('%27',"'").replace("'","").replace('%3a',":")
    options=[heb_name+' ע%s פ%s'%(season,episode),heb_name+' ע%sפ%s'%(season,episode),heb_name+' עונה %s פרק %s'%(season,episode),c_original+'.S%sE%s'%(season_n,episode_n),c_original+'.S%sE%s'%(season,episode)]
    #if 'the' in original_title.lower():
    #    options.append(c_original.replace('The','').replace('the','')+'.S%sE%s'%(season_n,episode_n))
    options2=[' ע%s פ%s'%(season,episode),'ע%s.פ%s'%(season,episode),' ע%sפ%s'%(season,episode),' עונה %s פרק %s'%(season,episode),'.S%sE%s'%(season_n,episode_n),'.S%sE%s'%(season,episode)]
    for items in options:
        log.warning(items)
        all_links=all_links+search(tmdb,'all','0$$$0',items.replace(':',''),iconimage,fanart,season,episode,no_subs=1,original_title=original_title,heb_name=heb_name,dont_return=False,manual=False)

    if Addon.getSetting("order_by")=='0':
        
        all_links=sorted(all_links, key=lambda x: x[4], reverse=False)
    else:
        all_links=sorted(all_links, key=lambda x: x[1], reverse=False)
    exclude=[]
    filter_dup=Addon.getSetting("dup_links")=='true'
    log.warning(filter_dup)
    all_t_links=[]
    
        
    log.warning('Results:')
    once=0
    d_save=[]
    
    for  name, link,mode,q,loc, icon,fan,plot,no_subs,tmdb,season,episode,original_title in all_links:
        
        
        if name not in all_t_links or filter_dup==False:
            all_t_links.append(name)
            
            ok=False
            o_name=heb_name
            for items in options2:
                    t_items=items.replace('_','.').replace(' ','.').replace(':','').replace("'","").replace('-','.').replace('[','').replace(']','').replace('..','.').lower()
                    t_name=name.replace('_','.').replace('"',"").replace('  ',' ').lower().replace('-','.').replace(' ','.').replace('[','').replace(']','').replace('_','.').replace(':','').replace("'","").replace('..','.')
                    t_items2=c_original.replace('_','.').replace(' ','.').replace(':','').replace("'","").replace('-','.').replace('[','').replace(']','').replace('..','.').lower()
                    
                    if (t_items+'.'  in t_name+'.') or (t_items+' '  in t_name+' ') or (t_items+'_'  in t_name+'_') or (t_items.replace('.','_')+'_'  in t_name.replace('.','_')+'_') or (t_items.replace('.','-')+'_'  in t_name.replace('.','-')+'_'):
                       if (o_name in name) or (t_items2 in t_name):
                        ok=True
                        break
            
            if not ok:
                log.warning('Not Ok')
                
                exclude.append((name, link,mode,q,loc, icon,fan,plot,no_subs,tmdb,season,episode,original_title))
            else:
                  
                  if once==0:
                    once=1
                    d_save.append((name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,plot))
                  addLink( name, link,mode,False, icon,fan,plot,no_subs=no_subs,tmdb=tmdb,season=season,episode=episode,original_title=original_title)
    if Addon.getSetting("one_click")=='true' and remote==False:
        if len(d_save)==0:
            xbmcgui.Dialog().ok('Telemedia','Sorry no sources found')
        else:
            name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,plot=d_save[0]
            play(name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,plot,None)
    addNolink( '[COLOR lightblue][I]/////////////[/I][/COLOR]', 'www',99,False,iconimage=iconimage,fan=fanart)
    for  name, link,mode,q,loc, icon,fan,plot,no_subs,tmdb,season,episode,original_title in exclude:
        
            if remote==False:
                addLink( name, link,mode,False, icon,fan,plot,no_subs=no_subs,tmdb=tmdb,season=season,episode=episode,original_title=original_title)
    return all_links 
def clear_all():
    import shutil
    data={'type':'logout',
         'info':'quit'
         }
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    shutil.rmtree(user_dataDir)
    clear_files()
    xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', 'All is cleared now'))
def search_groups(icon_o,fan_o):
        all_d=[]
        search_entered=''
        #'Enter Search'
        keyboard = xbmc.Keyboard(search_entered, Addon.getLocalizedString(32025))
        keyboard.doModal()
        if keyboard.isConfirmed():
                query = keyboard.getText()
        else:
            return 0
        num=random.randint(0,60000)
        if KODI_VERSION<19:
            
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchPublicChats', 'query': query.decode('utf-8'), '@extra': num})
                 }
        else:
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchPublicChats', 'query': query, '@extra': num})
                 }
        event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
        
        dp = xbmcgui.DialogProgress()
        dp.create('Please Wait...'+'\nAdding Groups')
        dp.update(0, 'Please Wait...'+'\nAdding Groups')
    
        log.warning(json.dumps(event))
        counter=0
        counter_ph=10000
        zzz=0
        for items in event['chat_ids']:
            num=random.randint(0,60000)
            data={'type':'td_send',
                     'info':json.dumps({'@type': 'getChat','chat_id':items, '@extra':num})
                     }
            event_in=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            
            if dp.iscanceled():
                          dp.close()
                         
                          break
            j_enent=(event_in)
            if KODI_VERSION<19:
                dp.update(int(((zzz* 100.0)/(len(event['chat_ids']))) ), 'Please Wait...','Adding Groups', j_enent['@type'].encode('utf8') )
            else:
                dp.update(int(((zzz* 100.0)/(len(event['chat_ids']))) ), 'Please Wait...'+'\n'+'Adding Groups'+'\n'+ j_enent['@type'] )
            if j_enent['@type']=='chat' and len(j_enent['title'])>1:
                
                icon_id=''
                fan_id=''
                fanart=''
                icon=''
                name=j_enent['title']
             
                color='white'
                if 'is_channel' in j_enent['type']:
                    if j_enent['type']['is_channel']==False:
                        
                        genere='Chat'
                        color='lightblue'
                    else:
                        genere='Channel'
                        color='khaki'
                else:
                     genere=j_enent['type']['@type']
                     color='lightgreen'
                if 'last_message' in j_enent:
                    plot=name
                    pre=j_enent['last_message']['content']
               
                    if 'caption' in pre:
                        plot=j_enent['last_message']['content']['caption']['text']
                    elif 'text' in pre:
                        if 'text' in pre['text']:
                            plot=j_enent['last_message']['content']['text']['text']
                    
                        
                else:
                    plot=name
                if KODI_VERSION<19:
                    dp.update(int(((zzz* 100.0)/(len(event['chat_ids']))) ), 'Please Wait...','Adding Groups', name.encode('utf8') )
                else:
                    dp.update(int(((zzz* 100.0)/(len(event['chat_ids']))) ), 'Please Wait...'+'\n'+'Adding Groups'+'\n'+ name )
                zzz+=1
             
                if 'photo' in j_enent:
                   
                   if 'small' in j_enent['photo']:
                     counter_ph+=1
                     icon_id=j_enent['photo']['small']['id']
                     f_name=str(j_enent['id'])+'_small.jpg'
                     mv_name=os.path.join(logo_path,f_name)
                     if os.path.exists(mv_name):
                        icon=mv_name
                     else:
                        icon=download_photo(icon_id,counter_ph,f_name,mv_name)
                   if 'big' in j_enent['photo']:
                     counter_ph+=1
                     fan_id=j_enent['photo']['big']['id']
                     f_name=str(j_enent['id'])+'_big.jpg'
                     mv_name=os.path.join(logo_path,f_name)
                     if os.path.exists(mv_name):
                        fanart=mv_name
                     else:
                        fanart=download_photo(fan_id,counter_ph,f_name,mv_name)
                
                
                aa=addDir3('[COLOR %s]'%color+name+'[/COLOR]',str(items),2,icon,fanart,plot+'\nfrom_plot',generes=genere,data='0',last_id='0$$$0$$$0$$$0',image_master=icon+'$$$'+fanart,join_menu=True)
                all_d.append(aa)
            
            counter+=1
        if len(all_d)>0:
             
            addNolink( '[COLOR lightblue][I]%s[/I][/COLOR]'%Addon.getLocalizedString(32058), 'www',99,False,iconimage=icon_o,fan=fan_o)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
        dp.close()
               
def join_chan(url):
    num=random.randint(0,60000)
    data={'type':'td_send',
             'info':json.dumps({'@type': 'joinChat', 'chat_id': url, '@extra': num})
             }
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    log.warning(json.dumps(event))
    if event["@type"]=='ok':
        #Joined OK
        xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', Addon.getLocalizedString(32029)))
    else:
        #Error in join
        xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', Addon.getLocalizedString(32030)))

def leave_chan(name,url):
    num=random.randint(0,60000)
    #"Leave Channel"
    #Leave    
    ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32031),'?%s'%name+(Addon.getLocalizedString(32032)))
    if ok:
        data={'type':'td_send',
             'info':json.dumps({'@type': 'leaveChat', 'chat_id': url, '@extra': num})
             }
        event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
        log.warning(json.dumps(event))
        if event["@type"]=='ok':
            xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', Addon.getLocalizedString(32067)))
            xbmc.executebuiltin('Container.Refresh')
        else:
            xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', Addon.getLocalizedString(32068)))
def dis_or_enable_addon(addon_id, enable="true"):
    import json
    log.warning('ADDON ID:'+addon_id)
    addon = '"%s"' % addon_id
    if xbmc.getCondVisibility("System.HasAddon(%s)" % addon_id) and enable == "true":
        log.warning('already Enabled')
        return xbmc.log("### Skipped %s, reason = allready enabled" % addon_id)
    elif not xbmc.getCondVisibility("System.HasAddon(%s)" % addon_id) and enable == "false":
        log.warning('Not already Enabled')
        return xbmc.log("### Skipped %s, reason = not installed" % addon_id)
    else:
        do_json = {"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{"addonid":addon,"enabled":enable}} 
                   
        log.warning(do_json)
        query = xbmc.executeJSONRPC(json.dumps(do_json))
        response = json.loads(query)
        if enable == "true":
            log.warning("### Enabled %s, response = %s" % (addon_id, response))
        else:
            log.warning("### Disabled %s, response = %s" % (addon_id, response))
    return xbmc.executebuiltin('Container.Update(%s)' % xbmc.getInfoLabel('Container.FolderPath'))
def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass
def copyDirTree(root_src_dir,root_dst_dir):
    """
    Copy directory tree. Overwrites also read only files.
    :param root_src_dir: source directory
    :param root_dst_dir:  destination directory
    """
    not_copied=[]
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            
        
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                try:
                    os.remove(dst_file)
                except Exception as exc:
                    #os.chmod(dst_file, stat.S_IWUSR)
                    #os.remove(dst_file)
                    log.warning('Error del:'+dst_file)
                    log.warning(exc)
            try:
                shutil.copy(src_file, dst_dir)
            except:
              if '.dll' not in file_ and '.so' not in file_:
                not_copied.append(file_)
    return not_copied
def install_addon(name,url,silent=False,Delete=True):
    try:
            
        from zfile_18 import ZipFile
    except:
        from zipfile import ZipFile
    log.warning(name)
    log.warning(xbmc.getCondVisibility("System.HasAddon(%s)" % name.split('-')[0]))
    log.warning(url)
    log.warning(xbmc.getInfoLabel('System.AddonVersion(%s)'%name.split('-')[0]))
    
    num=random.randint(0,60000)
    #Install
    log.warning('url::'+url)
    url=json.loads(url)['id']
    if silent:
        ok=True
    else:
        ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32033),(Addon.getLocalizedString(32033)+' %s?'%name))
    if ok:
        if silent==False:
            dp = xbmcgui.DialogProgress()
            dp.create('Telemedia', '[B][COLOR=yellow]Installing[/COLOR][/B]','')
        if Delete:
            try:
                if os.path.exists(addon_path):
                    shutil.rmtree(addon_path)
            except Exception as e:
                log.warning('error removing folder:'+str(addon_path)+','+str(e))
            if not xbmcvfs.exists(addon_path+'/'):
                os.makedirs(addon_path)
        mv_name=os.path.join(addon_path,name)
        log.warning('Downloading addon')
        addon=download_photo(url,num,name,mv_name)
        
        if silent==False:
            dp.update(0,'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Extracting[/COLOR][/B]')
        zf = ZipFile(addon)

        uncompress_size = sum((file.file_size for file in zf.infolist()))

        extracted_size = 0

        for file in zf.infolist():
            extracted_size += file.file_size
            if silent==False:
                dp.update(int((extracted_size*100.0)/uncompress_size),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Extracting[/COLOR][/B]',file.filename)
            
            zf.extract(member=file, path=addon_extract_path)
        zf.close()
        f_o = os.listdir(addon_extract_path)
        
            
        #file = open(os.path.join(addon_extract_path,f_o[0], 'addon.xml'), 'r') 
        filename=os.path.join(addon_extract_path,f_o[0], 'addon.xml')
        if sys.version_info.major > 2:
            do_open = lambda filename: open(filename, encoding='utf-8')
        else:
            do_open = lambda filename: open(filename)

        with do_open(filename) as file:
            file_data= file.read()
            pass
        
        
        file.close()
        regex='id=(?:"|\')(.+?)(?:"|\')'
        nm=re.compile(regex).findall(file_data)[0]
        if not xbmc.getCondVisibility("System.HasAddon(%s)" % name.split('-')[0]):
            regex='import addon=(?:"|\')(.+?)(?:"|\')'
            dep=re.compile(regex).findall(file_data)
            missing=[]
            if silent==False:
                dp.update(90,'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Dependencies[/COLOR][/B]','')
            zzz=0
            for items in dep:
                if silent==False:
                    dp.update(int((extracted_size*100.0)/len(items)),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Dependencies[/COLOR][/B]',items)
                zzz+=1
                if not xbmc.getCondVisibility("System.HasAddon(%s)" % items):
                    missing.append(items)
            if len(missing)>0:
                showText('Missing Dependencies','\n'.join(missing))
                return 0
        addon_p=xbmc_tranlate_path("special://home/addons/")
        #dis_or_enable_addon(nm, enable="false")
        #xbmc.sleep(1000)
        
        files = os.listdir(addon_extract_path)
        log.warning(os.path.join(addon_p,f_o[0]))
        try:
            if os.path.exists(os.path.join(addon_p,f_o[0])):
                shutil.rmtree(os.path.join(addon_p,f_o[0]))
        except Exception as e:
         log.warning('Telemedia Error removing addon')
         pass
        log.warning('Copy')
        not_copied=copyDirTree(os.path.join(addon_extract_path,f_o[0]),os.path.join( addon_p,f_o[0]))
        if len(not_copied)>0:
            showText('File That was not copied', '\n'.join(not_copied))
        #shutil.move(os.path.join(addon_extract_path,f_o[0]), addon_p)
        x=xbmc.executebuiltin("UpdateLocalAddons")
        if silent==False:
            dp.update(100,'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Cleaning[/COLOR][/B]','')
        time.sleep(1)
        dis_or_enable_addon(nm)
        shutil.rmtree(addon_path)
        if silent==False:
            dp.close()
        #'Installed'
        #'Installation complete'
        if silent==False:
            xbmcgui.Dialog().ok(Addon.getLocalizedString(32034),Addon.getLocalizedString(32035))
def download_file_loc(id):
        try:
            
            path=''
            dp = xbmcgui.DialogProgress()
            dp.create('Telemedia', '[B][COLOR=yellow]Loading[/COLOR][/B]')
            num=random.randint(0,60000)
            data={'type':'td_send',
             'info':json.dumps({'@type': 'downloadFile','file_id':int(id), 'priority':1,'offset':0,'limit':0, '@extra': num})
             }
            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
           
            j_enent_o=(event)
            
           
            
            j_enent_o=(event)
            once=True
            while True:
                data={'type':'td_send',
                 'info':json.dumps({'@type': 'getFile','file_id':int(id), '@extra': num})
                 }
                event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
               
                
                #event = td_receive()
                
                if dp.iscanceled():
                    num=random.randint(0,60000)
                    data={'type':'td_send',
                         'info':json.dumps({'@type': 'cancelDownloadFile','file_id':int(id), '@extra': num})
                         }
                    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
                    path=''
                        
                    break
                
                if event:
                    if 'file' in event:
                        size=event['file']['size']
                    else:
                        size=event['size']
                    if event.get('@type') =='error':
               
                        xbmcgui.Dialog().ok('Error occurred',str(event.get('message')))
                        break
                    
                        
                    
                    if 'expected_size' in event:
                        
                        dp.update(int((event['local']['downloaded_size']*100.0)/size),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Downloading %s/%s[/COLOR][/B]'%(str(event['local']['downloaded_size']),str(size)))
                        
                        
                        if len(event['local']['path'])>0 and event['local']['is_downloading_completed']==True:
                            size=event['size']
                            path=event['local']['path']
                            break
                xbmc.sleep(100)
            dp.close()
            return path
        except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            log.warning('ERROR IN Main:'+str(lineno))
            log.warning('inline:'+str(line))
            log.warning(str(e))
            xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
def install_build(original_title,url):
    import shutil
    try:
            
        from zfile_18 import ZipFile
    except:
        from zipfile import ZipFile
    ok=xbmcgui.Dialog().yesno(("Install"),('Download and Install [COLOR lightblue][B] %s [/B][/COLOR]?'%original_title))
    if ok:
        path=download_file_loc(url)
        log.warning(path)
    dp = xbmcgui.DialogProgress()
    dp.create('Telemedia', '[B][COLOR=yellow]Cleaning Kodi[/COLOR][/B]')
    addon_p=xbmc_tranlate_path("special://home/addons/")
    f_list=os.listdir(addon_p)
    zz=0
    error_list=[]
    for items in f_list:
        if 'telemedia' not in items and 'requests' not in items and  'pyxbmct' not in items:
            n_f=os.path.join(addon_p,items)
            dp.update(int((zz)/len(f_list)),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Cleaning Kodi Addons[/COLOR][/B]',items)
            zz+=1
            try:
                os .unlink (n_f)
                shutil.rmtree(n_f)
            except:
                error_list.append('Removing:'+n_f)
                
    addon_p=xbmc_tranlate_path("special://home")
    zz=0
    for items in f_list:
        if 'addons' not in items:
            n_f=os.path.join(addon_p,items)
            dp.update(int((zz)/len(f_list)),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Cleaning Kodi user data[/COLOR][/B]',items)
            zz+=1
            try:
                os .unlink (n_f)
                shutil.rmtree(n_f)
            except:
                error_list.append('Removing:'+n_f)
    addon_p=xbmc_tranlate_path("special://home/")
    
    zz=0
    with zipfile.ZipFile(path) as zf:
     z_list=zf.infolist()
     for member in tqdm(z_list, desc='Extracting '):
         try:
            dp.update(int((zz)/len(z_list)),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Extracting[/COLOR][/B]',member)
            zz+=1
            if 'telemedia' not in member:
                zf.extract(member, addon_p)
         except zipfile.error as e:
             error_list.append(member)
             pass
    if len(error_list)>0:
        showText('Errors', '\n'.join(error_list))
    xbmcgui.Dialog().ok('All Done','Restart Kodi')
def add_tv_to_db(name,url,data,iconimage,fanart,description):
    #Add tv show
    #Add
    log.warning('id:'+url)
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""year TEXT, ""icon TEXT,""fan TEXT,""plot TEXT, ""free TEXT);" % 'custom_show')
    dbcon.commit()
    ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32050),(Addon.getLocalizedString(32051)+' ?%s'%name))
    if ok:
        dbcur.execute("SELECT * FROM custom_show where tmdb='%s'"%(url))
        match = dbcur.fetchall()
        log.warning(match)
        
        if len(match)==0:
          dbcur.execute("INSERT INTO custom_show Values ('%s','%s','%s','%s','%s','%s','%s');" %  (name.replace("'","%27"),url,data,iconimage,fanart,description.replace("'","%27"),''))
          dbcon.commit()
          #Added
          xbmcgui.Dialog().ok('Telemedia',name+' '+Addon.getLocalizedString(32054))
        else:
           #Error occurred
           #Already Listed
           xbmcgui.Dialog().ok(Addon.getLocalizedString(32052),Addon.getLocalizedString(32053))
    dbcur.close()
    dbcon.close()
def my_local_tv():
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""year TEXT, ""icon TEXT,""fan TEXT,""plot TEXT, ""free TEXT);" % 'custom_show')
    dbcon.commit()
    
    dbcur.execute("SELECT * FROM custom_show")
    match = dbcur.fetchall()
    all_d=[]
    for name,url,data,iconimage,fanart,description,free in match:
        
        aa=addDir3(name.replace("%27","'"),url,16,iconimage,fanart,description.replace("%27","'"),id=url,heb_name=name)
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
    dbcur.close()
    dbcon.close()
def remove_my_tv(name,url):
    #Remove
    ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32066),(Addon.getLocalizedString(32064)+' %s?'%name))
    if ok:
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""year TEXT, ""icon TEXT,""fan TEXT,""plot TEXT, ""free TEXT);" % 'custom_show')
        dbcon.commit()
        
        dbcur.execute("DELETE  FROM custom_show where tmdb='%s'"%url)
        dbcon.commit()
        
        
        xbmcgui.Dialog().ok('Telemedia',name + ' '+Addon.getLocalizedString(32065))
        xbmc.executebuiltin('Container.Refresh')
        
        dbcur.close()
        dbcon.close()
        
def pre_searches(url,data,last_id,description,iconimage,fanart):
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""free TEXT);" % 'search')
    dbcon.commit()
        
    dbcur.execute("SELECT * FROM search")
    match_search = dbcur.fetchall()
    all_d=[]
    for nm,fr in match_search:
        aa=addDir3(nm,url,6,iconimage,fanart,nm,last_id='0$$$0',data='all')
        all_d.append(aa)
        
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
    addNolink( '[COLOR lightgreen]%s[/COLOR]'%Addon.getLocalizedString(32093), 'www',37,False,fan="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/056c5ee1-35c4-4088-bd42-056e3d29a49f/d6r6rsf-a10be578-9677-4191-89f7-94421bec6656.jpg/v1/fill/w_1024,h_578,q_75,strp/gravity_clean_wallpaper_by_iiigerardoiii_d6r6rsf-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NTc4IiwicGF0aCI6IlwvZlwvMDU2YzVlZTEtMzVjNC00MDg4LWJkNDItMDU2ZTNkMjlhNDlmXC9kNnI2cnNmLWExMGJlNTc4LTk2NzctNDE5MS04OWY3LTk0NDIxYmVjNjY1Ni5qcGciLCJ3aWR0aCI6Ijw9MTAyNCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.6h7jn2BgO8JqvQjFL8g9xCNS3d4fWyaQgEVo0NUv794", iconimage="https://15logo.net/wp-content/uploads/2017/03/Clean-Home-800x800.jpg")
        
    dbcur.close()
    dbcon.close()
def clean_name2(name,original_title,html_g,icon_pre,fan_pre):
    #from resources.modules import PTN
    if '@' in name and '.' in name:
        nm=name.split('.')
        ind=0
        for items in nm:
            if '@' in items:
                nm.pop(ind)
            ind+=1
        name='.'.join(nm)
 

    name=name.replace(' ','.').replace('_','.').replace('-','.').replace('%20',' ').replace('5.1','').replace('AAC','').replace('2CH','').replace('.mp4','').replace('.avi','').replace('.mkv','').replace(original_title,'').replace('מדובב','').replace('גוזלן','').replace('BDRip','').replace('BRRip','')

    name=name.replace('1080p','').replace('720p','').replace('480p','').replace('360p','').replace('BluRay','').replace('ח1','').replace('ח2','').replace('נתי.מדיה','').replace('נ.מ.','').replace('..','.').replace('.',' ').replace('WEB-DL','').replace('WEB DL','').replace('נ מדיה','')

    name=name.replace('HDTV','').replace('DVDRip','').replace('WEBRip','')

    name=name.replace('דב סרטים','').replace('לולו סרטים','').replace('דב ס','').replace('()','').replace('חן סרטים','').replace('ק סרטים','').replace('חננאל סרטים','').replace('יוסי סרטים','').replace('נריה סרטים','').replace('HebDub','').replace('NF','').replace('HDCAM','').replace('@yosichen','')

    name=name.replace('BIuRay','').replace('x264','').replace('Hebdub','').replace('XviD','')

    name=name.replace('Silver007','').replace('Etamar','').replace('iSrael','').replace('DVDsot','').replace('אלי ה סרטים','').replace('PCD1','').replace('PCD2','').replace('CD1','').replace('CD2','').replace('CD3','').replace('Gramovies','').replace('BORip','').replace('200P','').replace('מס1','1').replace('מס2','2').replace('מס3','3').replace('מס4','4').replace('מס 3','3').replace('מס 2','2').replace('מס 1','1')

    name=name.replace('900p','').replace('PDTV','').replace('VHSRip','').replace('UPLOAD','').replace('TVRip','').replace('Heb Dub','').replace('MP3','').replace('AC3','').replace('SMG','').replace('Rip','').replace('6CH','').replace('XVID','')

    name=name.replace('HD','').replace('WEBDL','').replace('DVDrip','')

    #info=(PTN.parse(name))
    regex='.*([1-3][0-9]{3})'
    year_pre=re.compile(regex).findall(name)
    year=0
    if len(year_pre)>0:
        year=year_pre[0]
     
        name=name.replace(year,'')
    pre_year=year
    if year!=0:
        
        url2='http://api.themoviedb.org/3/search/movie?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&year=%s&language=he&append_to_response=origin_country&page=1'%(que(name),year)
    else:
        url2='http://api.themoviedb.org/3/search/movie?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&language=he&append_to_response=origin_country&page=1'%(que(name))
    log.warning(url2)
    y=get_html(url2).json()
    
    
    plot=''
    genere=''
    icon=icon_pre
    fan=fan_pre
    original_name=name
    rating=0
    tmdb=''
    if 'results' in y and len(y['results'])>0:
        res=y['results'][0]
        name=res['title']
        if 'release_date' in res:
           year=str(res['release_date'].split("-")[0])
        if year!=pre_year and len(y['results'])>1:
            for items_in in y['results']:
                if 'release_date' in items_in:
                    year=str(items_in['release_date'].split("-")[0])
                    if year==pre_year:
                        res=items_in
                        name=res['title']
        plot=res['overview']
        genres_list= dict([(i['id'], i['name']) for i in html_g['genres']  if i['name'] is not None])
        try:genere = u' / '.join([genres_list[x] for x in res['genre_ids']])
        except:genere=''
        
        if res['poster_path']==None:
          icon=' '
        else:
           icon='https://image.tmdb.org/t/p/original/'+res['poster_path']
        if 'backdrop_path' in res:
             if res['backdrop_path']==None:
              fan=' '
             else:
              fan='https://image.tmdb.org/t/p/original/'+res['backdrop_path']
        else:
            fan='https://image.tmdb.org/t/p/original/'+html['backdrop_path']
        original_name=res['original_title']
        rating=res['vote_average']
        tmdb=str(res['id'])
    return name,year,plot,genere,icon,fan,original_name,rating,tmdb
def tmdb_world(last_id,icon,fan,chan_id):
    from resources.modules.tmdb import get_html_g
    from resources.modules import cache
    html_g_tv,html_g_movie=cache.get(get_html_g,72, table='posters_n')
    icon_pre=icon
    fan_pre=fan
    if icon_pre==None:
        icon_pre=''
    if fan_pre==None:
        fan_pre='' 
    num=random.randint(1,1001)

    
    try:
        last_id=int(last_id)
    except:
        last_id=0
    data={'type':'td_send',
         'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': 'searchMessagesFilterDocument'},'limit':100, '@extra': num})
         }
   
   

    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    num=random.randint(1,1001)
    
    
    if 'message' in event:
   
        if int(chan_id)==KIDS_CHAT_ID:
            join_type=1
            #chant_id='@kidsworldglobal'
            invite_link='https://t.me/joinchat/AAAAAEqauFWJ4Zar9vPxsg'
        elif int(chan_id)==HEBREW_GROUP:
            invite_link="https://t.me/joinchat/AAAAAEH4beTG18SsVmQn0Q"
            join_type=1
            
        elif int(chan_id)==WORLD_GROUP:
            join_type=1
            invite_link="https://t.me/joinchat/AAAAADumPH7RARDHtG0SoA"
        num=random.randint(1,1001)
        if 1:#'Chat not found' in event['message']:
            if join_type==1:
                data={'type':'td_send',
                 'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': invite_link, '@extra': num})
                 }
            else:
                data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchPublicChat', 'username': '@kidsworldglobal', '@extra': num})
                 }
                event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
                data={'type':'td_send',
                 'info':json.dumps({'@type': 'joinChat', 'chat_id': event['id'], '@extra': num})
                 }
            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            num=random.randint(1,1001)
            
    
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': 'searchMessagesFilterVideo'},'limit':100, '@extra': num})
                 }
           
           

            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': 'searchMessagesFilterDocument '},'limit':100, '@extra': num})
                 }
           
           

            event=event.update(get_html('http://127.0.0.1:%s/'%listen_port,json=data).json())
            
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'addChatToList', 'chat_id': KIDS_CHAT_ID,'chat_list':{'@type':'chatListArchive'}, '@extra': num})
                 }
            event2=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
    dp = xbmcgui . DialogProgress ( )
    if KODI_VERSION<19:
        dp.create(Addon.getLocalizedString(32041)+'...',Addon.getLocalizedString(32040), '','')
    else:
        dp.create(Addon.getLocalizedString(32041)+'...',Addon.getLocalizedString(32040)+'\n'+ ''+'\n'+'')
    zzz=0
    for items in event['messages']:  
       
       
        if 'document' in items['content']:
            
            name=items['content']['document']['file_name']
            
            
            if '.mkv' not in name and '.mp4' not in name and '.avi' not in name:
                    continue
            #if 'מדובב' not in name and 'hebdub' not in name.lower() and chan_id==str(KIDS_CHAT_ID) :
            #    continue
            size=items['content']['document']['document']['size']
            f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
            
            if 'date' in items:
                da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
           
            mode=3
            
            if dp.iscanceled():
                break
            o_name=name
            icon=icon_pre
            fan=fan_pre
            name,year,plot,genere,icon,fan,original_name,rating,tmdb=cache.get(clean_name2,999,name,original_title,html_g_movie,icon_pre,fan_pre, table='posters_n')
            #name,year,plot,genere,icon,fan,original_name,rating,tmdb=clean_name2(name,original_title,html_g_movie,icon_pre,fan_pre)
            if KODI_VERSION<19:
                dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), Addon.getLocalizedString(32041)+'...','Adding', name )
            else:
                dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), Addon.getLocalizedString(32041)+'...'+'\n'+'Adding'+'\n'+ name )
            zzz+=1
            link_data={}
            link_data['id']=str(items['content']['document']['document']['id'])
            link_data['m_id']=items['id']
            link_data['c_id']=items['chat_id']
            f_lk=json.dumps(link_data)
            addLink( name,f_lk,3,False, icon,fan,'[COLOR blue]'+o_name+'[/COLOR]\n'+f_size2+'\n'+plot,da=da,year=year,original_title=original_name,generes=genere,rating=rating,tmdb=tmdb)
    all_d=[]
    last_id=str(items['id'])
    aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32026)+'[/COLOR]','www',31,icon_pre,fan_pre,Addon.getLocalizedString(32026),data=chan_id,last_id=last_id)
    all_d.append(aa) 
    f_last_id='0$$$0$$$0$$$0'
    #'Search'
    aa=addDir3('[COLOR blue]'+Addon.getLocalizedString(32027)+'[/COLOR]',str(chan_id),2,'https://sitechecker.pro/wp-content/uploads/2017/12/search-engines.png','https://www.komando.com/wp-content/uploads/2017/12/computer-search.jpg','search',data='0',last_id=f_last_id,image_master=icon_pre+'$$$'+fan_pre)
    all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def launch_command(command_launch):
    import subprocess
    try:
        log.warning('[%s] %s' % ('LAUNCHING SUBPROCESS:', command_launch))
        external_command = subprocess.call(command_launch, shell = True, executable = '/system/bin/sh')
    except Exception as e:
        try:
            log.warning('[%s] %s' % ('ERROR LAUNCHING COMMAND !!!', e.message, external_command))
            log.warning('[%s] %s' % ('LAUNCHING OS:', command_launch))
            external_command = os.system(command_launch)
        except:
            log.warning('[%s]' % ('ERROR LAUNCHING COMMAND !!!', external_command))

def selectDialog(label, items, pselect=-1, uDetails=False):
    select = xbmcgui.Dialog().select(label, items, preselect=pselect, useDetails=uDetails)
def install_apk(name,url):
    import xbmcvfs
    f_id=json.loads(url)['id']
    try:
        num=random.randint(0,60000)
        #Install
        
        ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32033),(Addon.getLocalizedString(32033)+' %s?'%name))
        if ok:
            mv_name=os.path.join(addon_path,name)
            log.warning('Downloading addon')
            addon=download_photo(url,num,name,mv_name)
            log.warning('addon')
            log.warning(addon)
            # We assume that you have already downloaded the apk you want in /sdcard/Download
            try:
                shutil.move(addon,'/sdcard/Download/application.apk')
            except Exception as e:
                log.warning('File copy err:'+str(e))
                pass

            #xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:'+addon+'")')
            
            
            
            CUSTOM = (Addon.getSetting("Custom_Manager") or 'com.android.documentsui')
            FMANAGER  = {0:'com.android.documentsui',1:CUSTOM}[0]
            
            xbmc.executebuiltin('StartAndroidActivity(%s,,,"content://%s")'%(FMANAGER,addon))
            
            xbmcgui.Dialog().ok('Done','Complete')
            
    except Exception as e:
        xbmcgui.Dialog().ok('Error occurred','Err:'+str(e))
#def full_data_groups():
def add_to_f_d_groups(url,name,data,iconimage,fanart,description):
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""id TEXT, ""icon TEXT,""fan TEXT,""plot TEXT, ""free TEXT);" % 'my_fd_groups')
        dbcon.commit()
        dbcur.execute("SELECT * FROM my_fd_groups where id='%s'"%(url))
        
        match = dbcur.fetchall()
        if len(match)==0:
            dbcur.execute("INSERT INTO my_fd_groups Values ('%s','%s','%s','%s','%s','%s');" %  (name.replace("'","%27"),url,iconimage,fanart,description.replace("'","%27"),' '))
            dbcon.commit()
        else:
            xbmcgui.Dialog().ok('Error occurred',Addon.getLocalizedString(32081))
        #Added
        xbmcgui.Dialog().ok('Telemedia',name+' '+Addon.getLocalizedString(32054))
        dbcur.close()
        dbcon.close()
def full_data_groups():
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""id TEXT, ""icon TEXT,""fan TEXT,""plot TEXT, ""free TEXT);" % 'my_fd_groups')
        dbcon.commit()
        dbcur.execute("SELECT * FROM my_fd_groups")
        
        match = dbcur.fetchall()
        all_d=[]
        for name,id,icon,fan,plot,free in match:
            aa=addDir3(name.replace('%27',"'"),id,31,icon,fan,plot.replace('%27',"'"),data=id,remove_from_fd_g=True)
            all_d.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
        dbcur.close()
        dbcon.close()
def remove_f_d_groups(url,name):
    ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32082),'?%s'%name+(Addon.getLocalizedString(32082)))
    if ok:
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""id TEXT, ""icon TEXT,""fan TEXT,""plot TEXT, ""free TEXT);" % 'my_fd_groups')
        dbcon.commit()
        dbcur.execute("DELETE  FROM my_fd_groups where id='%s'"%url)
        log.warning(url)
        dbcon.commit()
        
        
        xbmcgui.Dialog().ok('Telemedia',name + ' '+Addon.getLocalizedString(32065))
        xbmc.executebuiltin('Container.Refresh')
        
        dbcur.close()
        dbcon.close()
def download_files(name,url):

    try:
        num=random.randint(0,60000)
        #Install
        new_dest=xbmc_tranlate_path(Addon.getSetting("remote_path"))
        log.warning('new_dest:'+new_dest)
        if not os.path.exists(new_dest):
            xbmcgui.Dialog().ok('Error occurred',Addon.getLocalizedString(32089))
            Addon.openSettings()
            return 0
        ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32088),(Addon.getLocalizedString(32088)+' %s?'%name))
        if ok:
            mv_name=os.path.join(new_dest,name)
            log.warning('Downloading addon')
            addon=download_photo(url,num,name,mv_name)
            log.warning('addon')
            log.warning(addon)
            
        xbmcgui.Dialog().ok('Error occurred','Err:'+str(e))
    except Exception as e:
        xbmcgui.Dialog().ok(Addon.getLocalizedString(32090),Addon.getLocalizedString(32090))
def clear_search_h():
    ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32093),Addon.getLocalizedString(32094))
    if ok:
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""free TEXT);" % 'search')
        dbcon.commit()
            
        dbcur.execute("DELETE FROM search")
        dbcon.commit()
        xbmc.executebuiltin('Container.Refresh')
        dbcur.close()
        dbcon.close()
def groups_join(id,icon_pre,fan_pre):
    num=random.randint(0,60000)
    m_id=0
    count=0
    log.warning('Get All groups')
    all_d=[]
    all_l=[]
    complete_list={}
    complete_list['by_link']=[]
    complete_list['public']=[]
    while count<10:
        count+=1
        log.warning('m_id')
        log.warning(m_id)
        data={'type':'td_send',
             'info':json.dumps({'@type': 'getChatHistory','chat_id':id,'from_message_id':m_id,'offset':0,'limit':100,'only_local':False, '@extra':num})
             }
        event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
       
        
        counter_ph=num
        
        for msg in event['messages']:
            msg_in=msg['content']
            m_id=msg['id']
            icon=icon_pre
            fan=fan_pre
            if 'web_page' in msg_in:
                title=msg_in['web_page']['title']
                
                if 'photo' in msg_in['web_page']:
                    counter_ph+=1
                    icon_id=msg_in['web_page']['photo']['sizes'][0]['photo']['id']
                    f_name=msg_in['web_page']['photo']['sizes'][0]['photo']['remote']['id']+'.jpg'
                    mv_name=os.path.join(icons_path,f_name)
                    if os.path.exists(mv_name):
                        icon=mv_name
                    else:
                       icon=download_photo(icon_id,counter_ph,f_name,mv_name)
                    
                    counter_ph+=1
                    loc=msg_in['web_page']['photo']['sizes']
                    icon_id=msg_in['web_page']['photo']['sizes'][len(loc)-1]['photo']['id']
                    f_name=msg_in['web_page']['photo']['sizes'][len(loc)-1]['photo']['remote']['id']+'.jpg'
                    mv_name=os.path.join(fan_path,f_name)
                    if os.path.exists(mv_name):
                        fan=mv_name
                    else:
                       fan=download_photo(icon_id,counter_ph,f_name,mv_name)
                all_l=[]
                all_urls={}
                regex='https://t.me/joinchat/(.+?)\n'
                all_l=re.compile(regex,re.DOTALL).findall(msg_in['web_page']['description']['text'])
                if 'text' in msg_in:
                    all_l=all_l+re.compile(regex,re.DOTALL).findall(msg_in['text']['text'])
                
                
                if len(all_l)>0:
                    all_urls['by_link']='$$$'.join(all_l)
                
                complete_list['by_link']+=all_l
                all_l=[]
                regex='@(.+?)(?: |\n|-|$)'
                all_l=re.compile(regex,re.DOTALL).findall(msg_in['web_page']['description']['text'])
                if 'text' in msg_in:
                    all_l=all_l+re.compile(regex,re.DOTALL).findall(msg_in['text']['text'])
                    regex='https://t.me/(.+?)(?:/|\n)'
                
                    all_l=all_l+re.compile(regex,re.DOTALL).findall(msg_in['text']['text'])
                if len(all_l)>0:
                    all_urls['public']='$$$'.join(all_l)
                complete_list['public']+=all_l
                if not icon:
                    icon=''
                if not fan:
                    fan=''
                aa=addDir3(title,json.dumps(all_urls),39,icon,fan,msg_in['web_page']['description']['text'])
                all_d.append(aa)
            else:
                all_l=[]
                all_urls={}
                regex='https://t.me/joinchat/(.+?)\n'
                if 'text' in msg_in:
                    all_l=re.compile(regex,re.DOTALL).findall(msg_in['text']['text'])
                
                if 'text' in msg_in:
                    all_l=re.compile(regex,re.DOTALL).findall(msg_in['text']['text'])
                
                if len(all_l)>0:
                    all_urls['by_link']='$$$'.join(all_l)
                complete_list['by_link']+=all_l
                all_l=[]
                regex='@(.+?)(?: |\n|-|$)'
               
                if 'text' in msg_in:
                    all_l=re.compile(regex,re.DOTALL).findall(msg_in['text']['text'])
                    regex='https://t.me/(.+?)(?:/|\n)'
                    if 'text' in msg_in:
                        all_l=all_l+re.compile(regex,re.DOTALL).findall(msg_in['text']['text'])
                    
                    if len(all_l)>0:
                        all_urls['public']='$$$'.join(all_l)
                    else:
                        all_urls['public']=''.join(all_l)
                    complete_list['public']+=all_l
                    if not icon:
                        icon=''
                    if not fan:
                        fan=''
                   
                    
                    aa=addDir3(msg_in['text']['text'],json.dumps(all_urls),39,icon,fan,msg_in['text']['text'])
                    all_d.append(aa)
    if not icon:
        icon=''
    if not fan:
        fan=''
    aa=addDir3('[COLOR lightgreen]'+Addon.getLocalizedString(32105)+'[/COLOR]',json.dumps(complete_list),42,icon,fan,Addon.getLocalizedString(32106))
    all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def join_group(url):
    num=random.randint(0,60000)
    data={'type':'td_send',
             'info':json.dumps({'@type': 'getChats','offset_chat_id':0,'offset_order':9223372036854775807, 'limit': '100', '@extra': num})
             }
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
    j_urls=json.loads(url)
    all_j=[]
    dp = xbmcgui.DialogProgress()
            
    dp.create('Telemedia', '[B][COLOR=yellow]%s[/COLOR][/B]'%Addon.getLocalizedString(32062))
    if 'by_link' in j_urls:
      if len(j_urls['by_link'])>0:
       
        by_link_chats=j_urls['by_link']
        log.warning(by_link_chats)
        if '$$$' in url:
            all_urls=by_link_chats.split('$$$')
        else:
            all_urls=[by_link_chats]
        zzz=0
        for it in all_urls:
          if it!='joinchat':
            if it in all_j:
                continue
            all_j.append(it)
            dp.update(int((zzz*100.0)/len(j_urls)),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]%s[/COLOR][/B]'%it)
            zzz+=1
            num=random.randint(0,60000)
            data={'type':'td_send',
             'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': 'https://t.me/joinchat/'+it, '@extra': num})
             }
                   
            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            log.warning('now event')
            log.warning(event)
            if 'id' in event:
                num=random.randint(0,60000)
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'addChatToList', 'chat_id': event['id'],'chat_list':{'@type':'chatListArchive'}, '@extra': num})
                     }
                event2=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
                
            time.sleep(1)
        
            
    if 'public' in j_urls:
      if len(j_urls['public'])>0:
       
        if '$$$' in j_urls['public']:
            all_links=j_urls['public'].split('$$$')
        else:
            all_links=[j_urls['public']]
        zzz=0
        for items in all_links:
           if items!='joinchat':
            num=random.randint(0,60000)
            
            dp.update(int((zzz*100.0)/len(all_links)),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]%s[/COLOR][/B]'%items)
            zzz+=1
            data={'type':'td_send',
             'info':json.dumps({'@type': 'searchPublicChat','username':items, '@extra':num})
             }
            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            num=random.randint(0,60000)
            if event:
              if 'id' in event:
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'joinChat', 'chat_id': event['id'], '@extra': num})
                     }
                event3=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
                num=random.randint(0,60000)
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'addChatToList', 'chat_id': event['id'],'chat_list':{'@type':'chatListArchive'}, '@extra': num})
                     }
                event2=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    dp.close()
def check_free_space():
    if xbmc.getCondVisibility('system.platform.android'):
        from os import statvfs
        user_path=xbmc_tranlate_path(Addon.getSetting("files_folder"))
        
        st = statvfs(user_path)
        free_space = float(st.f_bavail * st.f_frsize)/ (1024*1024*1024) 
    
        
       
        log.warning('free:'+str(free_space))  
        
        if free_space<2:
            xbmcgui.Dialog().ok("שגיאה","מקום פנוי %s , נדרש 2 גיגה לפחות"%(str(round(free_space,2))+'Gb'))
            return False
        return True
        log.warning('free space:'+ str(free_space)+'Gb')
    elif xbmc.getCondVisibility('system.platform.windows'):
        import ctypes
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(user_dataDir), None, None, ctypes.pointer(free_bytes))
        free_space=free_bytes.value / 1024 / 1024/1024
        if free_space<2:
            xbmcgui.Dialog().ok("שגיאה","מקום פנוי %s , נדרש 2 גיגה לפחות"%str(free_space))
            return False
        return True
        log.warning('free space:'+ str(free_bytes.value / 1024 / 1024/1024)+'Gb')
    else:
        return True
def play_remote(url,season,episode,original_title,id,saved_name,description,resume,name,heb_name,c_id=None,m_id=None,r_art='',r_logo='',iconimage='',fanart=''):
    
    log.warning('TMDB2:'+id)
    heb_name=heb_name.replace('%20',' ')
    original_title=original_title.replace('%20',' ')
    '''
    if season=='0' or season=='%20':
        all_results=search_movies(heb_name,original_title,'','','',id,season,episode,remote=True)
    else:
        all_results=search_tv(heb_name,original_title,' ','','',season,episode,id,remote=True)
    '''
    found=False
    log.warning('In Play_remote')
    log.warning('remote id:'+url)
    url=url.replace('single','')
    name=name.replace('%20',' ')
    original_title=original_title.replace('%20',' ')
    saved_name=saved_name.replace('%20',' ')
    log.warning(name)
    log.warning(saved_name)
    log.warning(original_title)
    log.warning(heb_name)
    num=random.randint(0,60000)
    if 'https://t.me' in url:
        log.warning('Send')
        data={'type':'td_send',
                 'info':json.dumps({'@type': 'getMessageLinkInfo','url':url, '@extra':num})
                 }
    else:
        
        data={'type':'td_send',
                 'info':json.dumps({'@type': 'getRemoteFile','remote_file_id':url, '@extra':num})
                 }
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
   
    if 'id' in event:
        found=True
        link_o=str(event['id'])
        link_data={}
        link_data['id']=link_o
        link_data['m_id']=m_id
        link_data['c_id']=c_id
    elif 'https://t.me' in url:
        link_data={}
        log.warning(event)
        if 'restriction_reason' in event['message']:
            if len(event['message']['restriction_reason'])>0:
                xbmcgui.Dialog().ok('Error occurred','קישור הוסר, בחר אחר')
                return 0
        if 'document' in event['message']['content']:
            link_o=str(event['message']['content']['document']['document']['id'])
            
            link_data['id']=str(event['message']['content']['document']['document']['id'])
        else:
            link_o=str(event['message']['content']['video']['video']['id'])
            
            link_data['id']=str(event['message']['content']['video']['video']['id'])
        link_data['m_id']=event['message']['id']
        link_data['c_id']=event['message']['chat_id']
                    
        found=True
    
    if found:
        log.warning('TMDB2:'+id)
        log.warning('NAME:'+name)
        log.warning(link_data)
        play(name,json.dumps(link_data),'',iconimage,fanart,'0',id,season,episode,original_title,description,resume,r_art=r_art,r_logo=r_logo)
    return 0
def upload_log(backup=False):
   try:
    
    num=random.randint(0,60000)
    data={'type':'td_send',
             'info':json.dumps({'@type': 'getChats','offset_chat_id':0,'offset_order':9223372036854775807, 'limit': '100', '@extra': num})
             }
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    exit_now=0
   
    if 'status' in event:
        xbmcgui.Dialog().ok('Error occurred',event['status'])
        exit_now=1
    if exit_now==0:
       

        
        
        counter=0
        counter_ph=10000
    
        j_enent_o=(event)
        zzz=0
        items=''
        names=[]
        ids=[]
        for items in j_enent_o['chat_ids']:
            
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'getChat','chat_id':items, '@extra':counter})
                 }
            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            
            order=event['positions'][0]['order']
            
           
                         
                          
            j_enent=(event)
            
            
            if j_enent['@type']=='chat' and len(j_enent['title'])>1:
                
              
                names.append(j_enent['title'])
                ids.append(items)
    selected_group_id=-1
    if len(names)>0:
        ret = xbmcgui.Dialog().select("Choose", names)
        if ret==-1:
            sys.exit()
        else:
            selected_group_id=ids[ret]
        if selected_group_id!=-1:
            if backup:
                import  zfile as zipfile
                dp = xbmcgui.DialogProgress()
            
                dp.create('Telemedia', '[B][COLOR=yellow]Backingup[/COLOR][/B]','')
                zip_name = os.path.join(xbmc_tranlate_path("special://temp"), 'data.zip')
                directory_name = user_dataDir
                log.warning(zip_name)
                log.warning(user_dataDir)
                # Create 'path\to\zip_file.zip'
                zf = zipfile.ZipFile(zip_name, "w")
                zzz=0
                for dirname, subdirs, files in os.walk(directory_name): 
                    try:
                        dp.update(int((zzz*100.0)/len(files)),'[B][COLOR=green]Zipping[/COLOR][/B]', dirname)
                    except:
                        pass
                    zzz+=1
                    zf.write(dirname)
                    for filename in files:
                        try:
                            dp.update(int((zzz*100.0)/len(files)),'[B][COLOR=green]Zipping[/COLOR][/B]', filename)
                        except:
                            pass
                        try:
                            zf.write(os.path.join(dirname, filename))
                        except:
                            pass
                zf.close()
                logSelect=[zip_name]
                
                dp.close()
            else:
                db_bk_folder=xbmc_tranlate_path(Addon.getSetting("remote_path"))
                nameSelect=[]
                logSelect=[]
                import glob
                folder = xbmc_tranlate_path('special://logpath')
                
                for file in glob.glob(folder+'/*.log'):
                    try:nameSelect.append(file.rsplit('\\', 1)[1].upper())
                    except:nameSelect.append(file.rsplit('/', 1)[1].upper())
                    logSelect.append(file)
            count=0
            for fi in logSelect:
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'sendMessage','chat_id': selected_group_id,'input_message_content': {'@type':'inputMessageDocument','document': {'@type':'inputFileLocal','path': fi}},'@extra': 1 })
                     }
                event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            try:
                os.remove(zip_name)
            except:
                pass
    xbmcgui.Dialog().ok('Upload Log','Ok')
   except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            log.warning('ERROR IN Upload Log:'+str(lineno))
            log.warning('inline:'+str(line))
            log.warning(str(e))
            xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))


def join_all_groups(url):
    num=random.randint(0,60000)
    '''
    data={'type':'td_send',
             'info':json.dumps({'@type': 'getChats','offset_chat_id':0,'offset_order':9223372036854775807, 'limit': '100', '@extra': num})
             }
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
    my_groups_id=event['chat_ids']
    log.warning(my_groups_id)
    log.warning(len(my_groups_id))
    '''
    j_complete_list=json.loads(url)
    all_j=[]
    dp = xbmcgui.DialogProgress()
            
    dp.create('Telemedia', '[B][COLOR=yellow]%s[/COLOR][/B]'%Addon.getLocalizedString(32062))
    zzz=0
    for j_urls in j_complete_list['public']:
    
      if len(j_urls)>0:
       
        if '$$$' in j_urls:
            all_links=j_urls.split('$$$')
        else:
            all_links=[j_urls]
        if dp.iscanceled():
                    break
        for items in all_links:
            if items=='joinchat':
                continue
            num=random.randint(0,60000)
            if KODI_VERSION<19:
                dp.update(int((zzz*100.0)/len(j_complete_list['public'])),'[B][COLOR=green]%s[/COLOR][/B]'%Addon.getLocalizedString(32062), '[B][COLOR=yellow]%s[/COLOR][/B]'%items +' , %s/%s'%(str(zzz),str(len(j_complete_list['public']))))
            else:
                dp.update(int((zzz*100.0)/len(j_complete_list['public'])),'[B][COLOR=green]%s[/COLOR][/B]'%Addon.getLocalizedString(32062)+'\n'+ '[B][COLOR=yellow]%s[/COLOR][/B]'%items +' , %s/%s'%(str(zzz),str(len(j_complete_list['public']))))
            zzz+=1
            data={'type':'td_send',
             'info':json.dumps({'@type': 'searchPublicChat','username':items, '@extra':num})
             }
            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            if event:
              if 'id' in event :
                
                o_id=event['id']
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'joinChat', 'chat_id': event['id'], '@extra': num})
                     }
                event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
                if event:
                  if event.get('@type') =='error':
                    if 'Too Many Requests: retry after' in str(event.get('message')):
                        try:
                            time_to_wait=int(str(event.get('message')).split('Too Many Requests: retry after'))
                        except:
                            continue
                        while( time_to_wait>0):
                            if KODI_VERSION<19:
                                dp.update(int((zzz*100.0)/len(j_urls)),'[B][COLOR=green]%s[/COLOR][/B]'%Addon.getLocalizedString(32062), '[B][COLOR=yellow]Wait for %s sec[/COLOR][/B]'% str(time_to_wait))
                            else:
                                dp.update(int((zzz*100.0)/len(j_urls)),'[B][COLOR=green]%s[/COLOR][/B]'%Addon.getLocalizedString(32062)+'\n'+ '[B][COLOR=yellow]Wait for %s sec[/COLOR][/B]'% str(time_to_wait))
                            time_to_wait-=1
                            time.sleep(1)
                
                num=random.randint(0,60000)
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'addChatToList', 'chat_id': o_id,'chat_list':{'@type':'chatListArchive'}, '@extra': num})
                     }
                event2=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
                
                time.sleep(0.1)
               
                
            if dp.iscanceled():
                    break
    for j_urls in j_complete_list['by_link']:
    
    
      if len(j_urls)>0:
       
        by_link_chats=j_urls
        
        if '$$$' in url:
            all_urls=by_link_chats.split('$$$')
        else:
            all_urls=[by_link_chats]
        zzz=0
        for it in all_urls:
          if it!='joinchat':
            if it in all_j:
                continue
            all_j.append(it)
            if KODI_VERSION<19:
                dp.update(int((zzz*100.0)/len(j_complete_list['by_link'])),'[B][COLOR=green]%s[/COLOR][/B]'%Addon.getLocalizedString(32062), '[B][COLOR=yellow]%s[/COLOR][/B]'%it)
            else:
                dp.update(int((zzz*100.0)/len(j_complete_list['by_link'])),'[B][COLOR=green]%s[/COLOR][/B]'%Addon.getLocalizedString(32062)+'\n'+ '[B][COLOR=yellow]%s[/COLOR][/B]'%it)
            zzz+=1
            num=random.randint(0,60000)
            data={'type':'td_send',
             'info':json.dumps({'@type': 'checkChatInviteLink', 'invite_link': 'https://t.me/joinchat/'+it, '@extra': num})
             }
                   
            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            if not event:
                continue
            if 'chat_id' in event:
                continue
            else:
                log.warning('Joining:'+'https://t.me/joinchat/'+it)
            data={'type':'td_send',
             'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': 'https://t.me/joinchat/'+it, '@extra': num})
             }
                   
            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            if event.get('@type') =='error':
                if 'Too Many Requests: retry after' in str(event.get('message')):
                    time_to_wait=int(str(event.get('message')).split('Too Many Requests: retry after')[1])
                    while( time_to_wait>0):
                        if KODI_VERSION<19:
                            dp.update(int((zzz*100.0)/len(j_urls)),'[B][COLOR=green]%s[/COLOR][/B]'%Addon.getLocalizedString(32062), '[B][COLOR=yellow]Wait for %s[/COLOR][/B]'% str(time_to_wait))
                        else:
                            dp.update(int((zzz*100.0)/len(j_urls)),'[B][COLOR=green]%s[/COLOR][/B]'%Addon.getLocalizedString(32062)+'\n'+ '[B][COLOR=yellow]Wait for %s[/COLOR][/B]'% str(time_to_wait))
                        time_to_wait-=1
                        time.sleep(1)
                        if dp.iscanceled():
                            break
            
            if event and 'id' in event:
                num=random.randint(0,60000)
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'addChatToList', 'chat_id': event['id'],'chat_list':{'@type':'chatListArchive'}, '@extra': num})
                     }
                event2=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            time.sleep(1)
            if dp.iscanceled():
                    break
        if dp.iscanceled():
                    break

    dp.close()
    xbmcgui.Dialog().ok('Telemedia','All Done')
def set_bot_id(name):
   try:
    if name=='auto':
        ret_bot=1
        if len(Addon.getSetting("update_chat_id"))>0:
            dialog = xbmcgui.Dialog()
            ret_bot = dialog.select(Addon.getLocalizedString(32028), [Addon.getLocalizedString(32125), Addon.getLocalizedString(32126)])
    all_update_bot=[]
    if ',' in Addon.getSetting("update_chat_id"):
        all_update_bot=Addon.getSetting("update_chat_id").split(',')
    elif len(Addon.getSetting("update_chat_id"))>0:
        all_update_bot=[Addon.getSetting("update_chat_id")]
    num=random.randint(0,60000)
    data={'type':'td_send',
             'info':json.dumps({'@type': 'getChats','offset_chat_id':0,'offset_order':9223372036854775807, 'limit': '100', '@extra': num})
             }
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    exit_now=0
   
    if 'status' in event:
        xbmcgui.Dialog().ok('Error occurred',event['status'])
        exit_now=1
    if exit_now==0:
       

        
        
        counter=0
        counter_ph=10000
    
        j_enent_o=(event)
        zzz=0
        items=''
        names=[]
        ids=[]
        for items in j_enent_o['chat_ids']:
            
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'getChat','chat_id':items, '@extra':counter})
                 }
            event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
            
            order=event['positions'][0]['order']
            
           
                         
                          
            j_enent=(event)
            
            
            if j_enent['@type']=='chat' and len(j_enent['title'])>1:
                
              
                names.append(j_enent['title'])
                ids.append(items)
    selected_group_id=-1
    if len(names)>0:
        ret = xbmcgui.Dialog().select("Choose", names)
        if ret==-1:
            sys.exit()
        else:
            selected_group_id=ids[ret]
        if selected_group_id!=-1:
            if name=='backup':
                
                Addon.setSetting('bot_id2',str(ids[ret]))
                
            else:
                log.warning('ret_bot:'+str(ret_bot))
                log.warning(all_update_bot)
                log.warning(str(ids[ret]))
                if ret_bot==1:
                    Addon.setSetting('update_chat_id',str(ids[ret]))
                else:
                    if str(ids[ret]) not in all_update_bot:
                        Addon.setSetting('update_chat_id',Addon.getSetting("update_chat_id")+','+str(ids[ret]))
    xbmcgui.Dialog().ok('Update bot location','Ok')
   except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            log.warning('ERROR IN Upload Log:'+str(lineno))
            log.warning('inline:'+str(line))
            log.warning(str(e))
            xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
def has_addon(name):
    ex=False
    log.warning('1')
    if xbmc.getCondVisibility("System.HasAddon(%s)" % name):
        log.warning('2')
        ex=True
    else:
        addon_path=os.path.join(xbmc_tranlate_path("special://home"),'addons/')
        log.warning(addon_path)
        log.warning(os.listdir(os.path.dirname(addon_path)))
        all_dirs=[]
        for items in os.listdir(os.path.dirname(addon_path)):
            all_dirs.append(items.lower())
        if name.lower() in all_dirs:
            
            ex=True
    ver=''
    if ex:
        ver=((xbmc.getInfoLabel('System.AddonVersion(%s)'%name)))
        
        if 1:
        
            addon_path=os.path.join(xbmc_tranlate_path("special://home"),'addons/')
            cur_folder=os.path.join(addon_path,name)
            log.warning(os.path.join(cur_folder, 'addon.xml'))
            if KODI_VERSION<19:
                file = open(os.path.join(cur_folder, 'addon.xml'), 'r') 
            else:
                file = open(os.path.join(cur_folder, 'addon.xml'), 'r', encoding="utf8") 
            file_data= file.read()
            file.close()
            regex='name=.+?version=(?:"|\')(.+?)(?:"|\')'
            ver=re.compile(regex,re.DOTALL).findall(file_data)[0]
        
    return ex,ver
def search_updates():
    from packaging import version
    id=Addon.getSetting("update_chat_id")
    if (len(id)<3):
        xbmc.executebuiltin(u'Notification(%s,%s)' % ('עדכונים טלמדיה','לא הוגדר ערוץ עדכון'))
        return 0
    num=random.randint(0,60000)
    log.warning('send update')
    if ',' in Addon.getSetting("update_chat_id"):
        all_ids=Addon.getSetting("update_chat_id").split(',')
    else:
        all_ids=[Addon.getSetting("update_chat_id")]
    log.warning(all_ids)
    data={'type':'td_send',
             'info':json.dumps({'@type': 'getChats','offset_chat_id':0,'offset_order':0, 'limit': '100','chat_list':{'@type': 'chatListMain'}, '@extra': num})
             }
    
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    xbmc.sleep(1000)
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
    for in_ids in all_ids:
        
        log.warning(in_ids)
       
        data={'type':'td_send',
             'info':json.dumps({'@type': 'searchChatMessages','chat_id':(in_ids), 'query': '','from_message_id':0,'offset':0,'filter':{'@type': 'searchMessagesFilterDocument'},'limit':100, '@extra': num})
             }
       
       
       
        event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
        log.warning(json.dumps(event))
        if 'messages' not in event:
            xbmc.executebuiltin('Notification(%s, %s, %d)'%('[COLOR yellow]תקלה נסה שוב מאוחר יותר[/COLOR]',str(json.dumps(event)), 500))
            return ''
        for items_in in event['messages']:  
           
              
            
              if 'chat_id' in items_in:
                
                
                    log.warning('correct chatid')
                    if 'content' in items_in:
                        items=items_in
                        if 'document' in items_in['content']:
                            log.warning('correct doc')
                            if 'file_name' in items_in['content']['document']:
                                f_name=items_in['content']['document']['file_name']
                                
                                if '.zip' not in f_name:
                                    continue
                                log.warning(f_name)
                                
                                c_f_name=f_name.split('-')
                                if len(c_f_name)==0:
                                    continue
                                c_f_name=c_f_name[0]
                                if '-' not in f_name:
                                    continue
                                new_addon_ver=f_name.split('-')[1].replace('.zip','')
                                log.warning(f_name)
                                ex,cur_version=has_addon(c_f_name)
                                if ex:
                                   log.warning('has addon')
                                   
                                   log.warning(cur_version)
                                   log.warning(new_addon_ver)
                                   
                                   do_update=((version.parse(cur_version)) < (version.parse(new_addon_ver)))
                                   log.warning(do_update)
                                   if do_update:
                                    log.warning('ver higher')
                                    if 1:
                                        xbmc.executebuiltin('Notification(%s, %s, %d)'%('[COLOR yellow]New Update[/COLOR] Ver:%s'%new_addon_ver,c_f_name, 500))
                                    link_data={}
                                    link_data['id']=str(items['content']['document']['document']['id'])
                                    link_data['m_id']=items['id']
                                    link_data['c_id']=items['chat_id']
                                    
                                    log.warning('install_addon')
                                    
                                    install_addon(f_name,json.dumps(link_data),silent=True)
                                    if 1:
                                        xbmc.executebuiltin('Notification(%s, %s, %d)'%('[COLOR yellow]Update Ok[/COLOR]',c_f_name, 500))
    if 0:#not xbmc.Player().isPlaying():
        xbmc.executebuiltin("UpdateLocalAddons()")
        xbmc.executebuiltin("ReloadSkin()")
        
        xbmc.sleep(1000)
        xbmc.executebuiltin("Container.Refresh()")
                
    xbmc.executebuiltin(u'Notification(%s,%s)' % ('עדכונים','הסתיים'))
    #xbmcgui.Dialog().ok('עדכונים','הסתיים')
def my_repo():
    from packaging import version
    id=Addon.getSetting("update_chat_id")
    num=random.randint(0,60000)
    log.warning('send update')
    if ',' in Addon.getSetting("update_chat_id"):
        all_ids=Addon.getSetting("update_chat_id").split(',')
    else:
        all_ids=[Addon.getSetting("update_chat_id")]
    log.warning(all_ids)
    try:
        if os.path.exists(addon_path):
            shutil.rmtree(addon_path)
    except Exception as e:
        log.warning('error removing folder:'+str(addon_path)+','+str(e))
    if not xbmcvfs.exists(addon_path+'/'):
        os.makedirs(addon_path)
    all_addons={}
    all_repo_info=[]
    for in_ids in all_ids:
        
        log.warning(in_ids)
       
        data={'type':'td_send',
             'info':json.dumps({'@type': 'searchChatMessages','chat_id':(in_ids), 'query': '','from_message_id':0,'offset':0,'filter':{'@type': 'searchMessagesFilterDocument'},'limit':100, '@extra': num})
             }
       
       
       
        event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
        
        for items_in in event['messages']:  
           
              
            
              if 'chat_id' in items_in:
                
                
                    log.warning('correct chatid')
                    if 'content' in items_in:
                        items=items_in
                        if 'document' in items_in['content']:
                            log.warning('correct doc')
                            if 'file_name' in items_in['content']['document']:
                                f_name=items_in['content']['document']['file_name']
                                c_f_name=f_name.split('-')
                                if len(c_f_name)==0:
                                    continue
                                c_f_name=c_f_name[0]
                                if '.xml' in f_name:
                                    mv_name=os.path.join(addon_path,c_f_name)
                                    num=random.randint(0,60000)
                                    try:
                                        addon=download_photo(items_in['content']['document']['document']['id'],num,c_f_name,mv_name)
                                        file = open(addon, 'r') 
                                        file_data= file.read()
                                        file.close()
                                        all_repo_info.append(file_data)
                                    except:
                                        pass
                                if '.zip' not in f_name:
                                    continue
                                
                                log.warning(f_name)
                                
                                
                                if '-' not in f_name:
                                    continue
                                new_addon_ver=f_name.split('-')[1].replace('.zip','')
                               
                                size=items['content']['document']['document']['size']
                                
                                f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                                idd=str(items_in['content']['document']['document']['id'])
                                ex,cur_version=has_addon(c_f_name)
                                if c_f_name in all_addons:
                                    all_addons[c_f_name].append({'version':new_addon_ver,'ex':ex,'f_name':f_name,'id':idd,'m_id':items_in['id'],'c_id':items_in['id'],'size':str(f_size2)})
                                else:
                                    
                                    all_addons[c_f_name]=[]
                                    all_addons[c_f_name].append({'version':new_addon_ver,'ex':ex,'f_name':f_name,'id':idd,'m_id':items_in['id'],'c_id':items_in['id'],'size':str(f_size2)})
                                    
    log.warning('All M')
    m=[]
    for tt in all_repo_info:
        regex='setting f_name="(.+?)" "display_name"="(.+?)" icon="(.+?)" fanart="(.+?)" description="(.+?)"'
        m=m+re.compile(regex,re.DOTALL).findall(tt)
        log.warning(m)
    all_data_addon={}
    log.warning('All M')
    for f_name,disp_name,icon,fanart,plot in m:
        log.warning(plot)
        all_data_addon[f_name]={'disp_name':disp_name,'icon':icon,'fanart':fanart,'plot':plot}
    log.warning('All I')
    for items in all_addons:
        link_data={}
        name=items
       
        f_lk=json.dumps(all_addons[items])
        f_size2=all_addons[items][0]['size']
        color='white'
        if all_addons[items][0]['ex']==False:
            color='lightblue'
        title=name
        fan=' '
        icon=' '
        plot=' '
        log.warning(items)
        if items in all_data_addon:
            
            title=all_data_addon[items]['disp_name']
            icon=all_data_addon[items]['icon']
            fan=all_data_addon[items]['fanart']
            plot=all_data_addon[items]['plot']
        addNolink('[COLOR %s]'%color+ title+'[/COLOR]',f_lk ,47,False, iconimage=icon,fan=fan,generes=f_size2,plot=plot,original_title=json.dumps(all_addons))
def multi_install(name,url,original_title):
    try:
            
        from zfile_18 import ZipFile
    except:
        from zipfile import ZipFile
    
    all_data=json.loads(url)
   
    silent=False
  
    log.warning(original_title)
    try:
        all_avi_addond=json.loads( urllib.parse.unquote_plus(original_title))
    except:
        all_avi_addond=json.loads(urllib.unquote_plus(original_title))
    try:
        if os.path.exists(addon_path):
            shutil.rmtree(addon_path)
    except Exception as e:
        log.warning('error removing folder:'+str(addon_path)+','+str(e))
    if not xbmcvfs.exists(addon_path+'/'):
        os.makedirs(addon_path)
                
    all_ver=[]
    all_d=[]
    for items in all_data:
        all_ver.append(items['version'])
        all_d.append(items['f_name'])
    
    ret = xbmcgui.Dialog().select("Choose", all_ver)
    if ret==-1:
        sys.exit()
    else:
        url=all_data[ret]['id']
        name=all_d[ret]
        log.warning(name)
        log.warning(xbmc.getCondVisibility("System.HasAddon(%s)" % name.split('-')[0]))
        log.warning(url)
        log.warning(xbmc.getInfoLabel('System.AddonVersion(%s)'%name.split('-')[0]))
        
        num=random.randint(0,60000)
        #Install
        log.warning('url::'+url)
        
        if silent:
            ok=True
        else:
            ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32033),(Addon.getLocalizedString(32033)+' %s?'%name))
        if ok:
            if silent==False:
                dp = xbmcgui.DialogProgress()
                if KODI_VERSION<19:
                    dp.create('Telemedia', '[B][COLOR=yellow]Installing[/COLOR][/B]','')
                else:
                    dp.create('Telemedia', '[B][COLOR=yellow]Installing[/COLOR][/B]'+'\n'+'')
            
            mv_name=os.path.join(addon_path,name)
            log.warning('Downloading addon')
            addon=download_photo(url,num,name,mv_name)
            xbmc.sleep(1000)
            if silent==False:
                dp.update(0,'[B][COLOR=green]Telemedia[/COLOR][/B]'+'\n'+ '[B][COLOR=yellow]Extracting[/COLOR][/B]')
            zf = ZipFile(addon)

            uncompress_size = sum((file.file_size for file in zf.infolist()))

            extracted_size = 0

            for file in zf.infolist():
                extracted_size += file.file_size
                if silent==False:
                    if KODI_VERSION<19:
                        dp.update(int((extracted_size*100.0)/uncompress_size),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Extracting[/COLOR][/B]',file.filename)
                    else:
                        dp.update(int((extracted_size*100.0)/uncompress_size),'[B][COLOR=green]Telemedia[/COLOR][/B]'+'\n'+ '[B][COLOR=yellow]Extracting[/COLOR][/B]'+'\n'+file.filename)
                zf.extract(member=file, path=addon_extract_path)
            zf.close()
            f_o = os.listdir(addon_extract_path)
            
            filename=os.path.join(addon_extract_path,f_o[0], 'addon.xml')
            if sys.version_info.major > 2:
                do_open = lambda filename: open(filename, encoding='utf-8')
            else:
                do_open = lambda filename: open(filename)

            with do_open(filename) as file:
                file_data= file.read()
                pass

            
            file.close()
            regex='id=(?:"|\')(.+?)(?:"|\')'
            nm=re.compile(regex).findall(file_data)[0]
            if not xbmc.getCondVisibility("System.HasAddon(%s)" % name.split('-')[0]):
                regex='import addon=(?:"|\')(.+?)(?:"|\')'
                dep=re.compile(regex).findall(file_data)
                missing=[]
                if silent==False:
                    if KODI_VERSION<19:
                        dp.update(90,'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Dependencies[/COLOR][/B]','')
                    else:
                        dp.update(90,'[B][COLOR=green]Telemedia[/COLOR][/B]'+'\n'+ '[B][COLOR=yellow]Dependencies[/COLOR][/B]'+'\n'+'')
                zzz=0
                for items in dep:
                    if silent==False:
                        if KODI_VERSION>=19:
                            dp.update(int((extracted_size*100.0)/len(items)),'[B][COLOR=green]Telemedia[/COLOR][/B]'+'\n'+ '[B][COLOR=yellow]Dependencies[/COLOR][/B]'+'\n'+items)
                        else:
                            dp.update(int((extracted_size*100.0)/len(items)),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Dependencies[/COLOR][/B]',items)
                    zzz+=1
                    if not xbmc.getCondVisibility("System.HasAddon(%s)" % items):
                        missing.append(items)
                if len(missing)>0:
                    for itemm in missing:
                        if itemm in all_avi_addond:
                            install_addon(itemm,json.dumps(all_avi_addond[itemm][0]),silent=True,Delete=False)
                        else:
                            xbmc.executebuiltin('InstallAddon(%s)'%itemm)
                            zzx=0
                            while not xbmc.getCondVisibility("System.HasAddon(%s)" % itemm):
                                if KODI_VERSION>=19:
                                    dp.update(int((zzx*100.0)/100),'[B][COLOR=green]Telemedia[/COLOR][/B]'+'\n'+ '[B][COLOR=yellow]Waiting[/COLOR][/B]'+'\n'+itemm)
                                else:
                                    dp.update(int((zzx*100.0)/100),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Waiting[/COLOR][/B]',itemm)
                                zzx+=1
                                if xbmc .getCondVisibility ("Window.isVisible(yesnodialog)"):
                                        xbmc.executebuiltin('SendClick(11)')
                                if zzx>100:
                                    break
                                xbmc.sleep(1000)
                    #showText('Missing Dependencies','\n'.join(missing))
                    #return 0
            addon_p=xbmc_tranlate_path("special://home/addons/")
            #dis_or_enable_addon(nm, enable="false")
            #xbmc.sleep(1000)
            
            files = os.listdir(addon_extract_path)
            log.warning(os.path.join(addon_p,f_o[0]))
            #if os.path.exists(os.path.join(addon_p,f_o[0])):
            #    shutil.rmtree(os.path.join(addon_p,f_o[0]))
            log.warning('Copy')
            
            not_copied=copyDirTree(os.path.join(addon_extract_path,f_o[0]),os.path.join( addon_p,f_o[0]))
            if len(not_copied)>0:
                showText('File That was not copied', '\n'.join(not_copied))
            #shutil.move(os.path.join(addon_extract_path,f_o[0]), addon_p)
            xbmc.executebuiltin("UpdateLocalAddons")
            if silent==False:
                if KODI_VERSION<19:
                    dp.update(100,'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Cleaning[/COLOR][/B]','')
                else:
                    dp.update(100,'[B][COLOR=green]Telemedia[/COLOR][/B]'+'\n'+ '[B][COLOR=yellow]Cleaning[/COLOR][/B]'+'\n'+'')
                    
            time.sleep(1)
            dis_or_enable_addon(nm)
            try:
                shutil.rmtree(addon_path)
            except:
                pass
            if silent==False:
                dp.close()
            #'Installed'
            #'Installation complete'
            if silent==False:
                xbmcgui.Dialog().ok(Addon.getLocalizedString(32034),Addon.getLocalizedString(32035))
def movie_prodiction():
    all_d=[]
    if Addon.getSetting("order_networks")=='0':
        order_by='popularity.desc'
    elif Addon.getSetting("order_networks")=='2':
        order_by='vote_average.desc'
    elif Addon.getSetting("order_networks")=='1':
        order_by='first_air_date.desc'
   
    
    aa=addDir3('[COLOR red]Marvel[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=7505&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://yt3.ggpht.com/a-/AN66SAwQlZAow0EBMi2-tFht-HvmozkqAXlkejVc4A=s900-mo-c-c0xffffffff-rj-k-no','https://images-na.ssl-images-amazon.com/images/I/91YWN2-mI6L._SL1500_.jpg','Marvel')
    all_d.append(aa)
    aa=addDir3('[COLOR lightblue]DC Studios[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=9993&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://pmcvariety.files.wordpress.com/2013/09/dc-comics-logo.jpg?w=1000&h=563&crop=1','http://www.goldenspiralmedia.com/wp-content/uploads/2016/03/DC_Comics.jpg','DC Studios')
    all_d.append(aa)
    aa=addDir3('[COLOR lightgreen]Lucasfilm[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=1&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://fontmeme.com/images/lucasfilm-logo.png','https://i.ytimg.com/vi/wdYaG3o3bgE/maxresdefault.jpg','Lucasfilm')
    all_d.append(aa)
    aa=addDir3('[COLOR yellow]Warner Bros.[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=174&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'http://looking.la/wp-content/uploads/2017/10/warner-bros.png','https://cdn.arstechnica.net/wp-content/uploads/2016/09/warner.jpg','SyFy')
    all_d.append(aa)
    aa=addDir3('[COLOR blue]Walt Disney Pictures[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=2&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://i.ytimg.com/vi/9wDrIrdMh6o/hqdefault.jpg','https://vignette.wikia.nocookie.net/logopedia/images/7/78/Walt_Disney_Pictures_2008_logo.jpg/revision/latest?cb=20160720144950','Walt Disney Pictures')
    all_d.append(aa)
    aa=addDir3('[COLOR skyblue]Pixar[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=3&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://elestoque.org/wp-content/uploads/2017/12/Pixar-lamp.png','https://wallpapercave.com/wp/GysuwJ2.jpg','Pixar')
    all_d.append(aa)
    aa=addDir3('[COLOR deepskyblue]Paramount[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=4&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://upload.wikimedia.org/wikipedia/en/thumb/4/4d/Paramount_Pictures_2010.svg/1200px-Paramount_Pictures_2010.svg.png','https://vignette.wikia.nocookie.net/logopedia/images/a/a1/Paramount_Pictures_logo_with_new_Viacom_byline.jpg/revision/latest?cb=20120311200405&format=original','Paramount')
    all_d.append(aa)
    aa=addDir3('[COLOR burlywood]Columbia Pictures[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=5&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://static.tvtropes.org/pmwiki/pub/images/lady_columbia.jpg','https://vignette.wikia.nocookie.net/marveldatabase/images/1/1c/Columbia_Pictures_%28logo%29.jpg/revision/latest/scale-to-width-down/1000?cb=20141130063022','Columbia Pictures')
    all_d.append(aa)
    aa=addDir3('[COLOR powderblue]DreamWorks[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=7&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://www.dreamworksanimation.com/share.jpg','https://www.verdict.co.uk/wp-content/uploads/2017/11/DA-hero-final-final.jpg','DreamWorks')
    all_d.append(aa)
    aa=addDir3('[COLOR lightsaltegray]Miramax[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=14&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://vignette.wikia.nocookie.net/disney/images/8/8b/1000px-Miramax_1987_Print_Logo.png/revision/latest?cb=20140902041428','https://i.ytimg.com/vi/4keXxB94PJ0/maxresdefault.jpg','Miramax')
    all_d.append(aa)
    aa=addDir3('[COLOR gold]20th Century Fox[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=25&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://pmcdeadline2.files.wordpress.com/2017/03/20th-century-fox-cinemacon1.jpg?w=446&h=299&crop=1','https://vignette.wikia.nocookie.net/simpsons/images/8/80/TCFTV_logo_%282013-%3F%29.jpg/revision/latest?cb=20140730182820','20th Century Fox')
    all_d.append(aa)
    aa=addDir3('[COLOR bisque]Sony Pictures[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=34&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Sony_Pictures_Television_logo.svg/1200px-Sony_Pictures_Television_logo.svg.png','https://vignette.wikia.nocookie.net/logopedia/images/2/20/Sony_Pictures_Digital.png/revision/latest?cb=20140813002921','Sony Pictures')
    all_d.append(aa)
    aa=addDir3('[COLOR navy]Lions Gate Films[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=35&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'http://image.wikifoundry.com/image/1/QXHyOWmjvPRXhjC98B9Lpw53003/GW217H162','https://vignette.wikia.nocookie.net/fanon/images/f/fe/Lionsgate.jpg/revision/latest?cb=20141102103150','Lions Gate Films')
    all_d.append(aa)
    aa=addDir3('[COLOR beige]Orion Pictures[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=41&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://i.ytimg.com/vi/43OehM_rz8o/hqdefault.jpg','https://i.ytimg.com/vi/g58B0aSIB2Y/maxresdefault.jpg','Lions Gate Films')
    all_d.append(aa)
    aa=addDir3('[COLOR yellow]MGM[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=21&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://pbs.twimg.com/profile_images/958755066789294080/L9BklGz__400x400.jpg','https://assets.entrepreneur.com/content/3x2/2000/20150818171949-metro-goldwun-mayer-trade-mark.jpeg','MGM')
    all_d.append(aa)
    aa=addDir3('[COLOR gray]New Line Cinema[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=12&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://upload.wikimedia.org/wikipedia/en/thumb/0/04/New_Line_Cinema.svg/1200px-New_Line_Cinema.svg.png','https://vignette.wikia.nocookie.net/theideas/images/a/aa/New_Line_Cinema_logo.png/revision/latest?cb=20180210122847','New Line Cinema')
    all_d.append(aa)
    aa=addDir3('[COLOR darkblue]Gracie Films[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=18&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://i.ytimg.com/vi/q_slAJmZBeQ/hqdefault.jpg','https://i.ytimg.com/vi/yGofbuJTb4g/maxresdefault.jpg','Gracie Films')
    all_d.append(aa)
    aa=addDir3('[COLOR goldenrod]Imagine Entertainment[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=23&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://s3.amazonaws.com/fs.goanimate.com/files/thumbnails/movie/2813/1661813/9297975L.jpg','https://www.24spoilers.com/wp-content/uploads/2004/06/Imagine-Entertainment-logo.jpg','Imagine Entertainment')
    all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def tv_neworks():
    all_d=[]
    if Addon.getSetting("order_networks")=='0':
        order_by='popularity.desc'
    elif Addon.getSetting("order_networks")=='2':
        order_by='vote_average.desc'
    elif Addon.getSetting("order_networks")=='1':
        order_by='first_air_date.desc'
    aa=addDir3('[COLOR lightblue]Disney+[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=2739&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://lumiere-a.akamaihd.net/v1/images/image_308e48ed.png','https://allears.net/wp-content/uploads/2018/11/wonderful-world-of-animation-disneys-hollywood-studios.jpg','Disney')
    all_d.append(aa)
    aa=addDir3('[COLOR blue]Apple TV+[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=2552&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://ksassets.timeincuk.net/wp/uploads/sites/55/2019/03/Apple-TV-screengrab-920x584.png','https://www.apple.com/newsroom/videos/apple-tv-plus-/posters/Apple-TV-app_571x321.jpg.large.jpg','Apple')
    all_d.append(aa)
    aa=addDir3('[COLOR red]NetFlix[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=213&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://art.pixilart.com/705ba833f935409.png','https://i.ytimg.com/vi/fJ8WffxB2Pg/maxresdefault.jpg','NetFlix')
    all_d.append(aa)
    aa=addDir3('[COLOR gray]HBO[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=49&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://filmschoolrejects.com/wp-content/uploads/2018/01/hbo-logo.jpg','https://www.hbo.com/content/dam/hbodata/brand/hbo-static-1920.jpg','HBO')
    all_d.append(aa)
    aa=addDir3('[COLOR lightblue]CBS[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=16&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://cdn.freebiesupply.com/logos/large/2x/cbs-logo-png-transparent.png','https://tvseriesfinale.com/wp-content/uploads/2014/10/cbs40-590x221.jpg','HBO')
    all_d.append(aa)
    aa=addDir3('[COLOR purple]SyFy[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=77&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'http://cdn.collider.com/wp-content/uploads/syfy-logo1.jpg','https://imagesvc.timeincapp.com/v3/mm/image?url=https%3A%2F%2Fewedit.files.wordpress.com%2F2017%2F05%2Fdefault.jpg&w=1100&c=sc&poi=face&q=85','SyFy')
    all_d.append(aa)
    aa=addDir3('[COLOR lightgreen]The CW[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=71&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://www.broadcastingcable.com/.image/t_share/MTU0Njg3Mjc5MDY1OTk5MzQy/tv-network-logo-cw-resized-bc.jpg','https://i2.wp.com/nerdbastards.com/wp-content/uploads/2016/02/The-CW-Banner.jpg','The CW')
    all_d.append(aa)
    aa=addDir3('[COLOR silver]ABC[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=2&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'http://logok.org/wp-content/uploads/2014/03/abc-gold-logo-880x660.png','https://i.ytimg.com/vi/xSOp4HJTxH4/maxresdefault.jpg','ABC')
    all_d.append(aa)
    aa=addDir3('[COLOR yellow]NBC[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=6&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://designobserver.com/media/images/mondrian/39684-NBC_logo_m.jpg','https://www.nbcstore.com/media/catalog/product/cache/1/image/1000x/040ec09b1e35df139433887a97daa66f/n/b/nbc_logo_black_totebagrollover.jpg','NBC')
    all_d.append(aa)
    aa=addDir3('[COLOR gold]AMAZON[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=1024&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'http://g-ec2.images-amazon.com/images/G/01/social/api-share/amazon_logo_500500._V323939215_.png','https://cdn.images.express.co.uk/img/dynamic/59/590x/Amazon-Fire-TV-Amazon-Fire-TV-users-Amazon-Fire-TV-stream-Amazon-Fire-TV-Free-Dive-TV-channel-Amazon-Fire-TV-news-Amazon-1010042.jpg?r=1535541629130','AMAZON')
    all_d.append(aa)
    aa=addDir3('[COLOR green]hulu[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=453&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://i1.wp.com/thetalkinggeek.com/wp-content/uploads/2012/03/hulu_logo_spiced-up.png?resize=300%2C225&ssl=1','https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwi677r77IbeAhURNhoKHeXyB-AQjRx6BAgBEAU&url=https%3A%2F%2Fwww.hulu.com%2F&psig=AOvVaw0xW2rhsh4UPsbe8wPjrul1&ust=1539638077261645','hulu')
    all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def get_free_space():
    import subprocess
    if xbmc .getCondVisibility ('system.platform.android'):#line:1878
        import subprocess
        df = subprocess.Popen(['df', '/storage/emulated/'], stdout=subprocess.PIPE)
        output = df.communicate()
        log.warning(output)
        
        output=output[0]
        info = output.split('\n')[1].split()
        log.warning(info)
        size = float(info[1].replace('G', '').replace('M', '')) * 1000000000.0
        log.warning(size)
        size = size - (size % float(info[-1]))
        log.warning(size)
        available = float(info[3].replace('G', '').replace('M', '')) * 1000000000.0
        log.warning(available)
        available = available - (available % float(info[-1]))
        log.warning(available)
        space= int(round(available)), int(round(size))
         
    else:
        process = subprocess.Popen('cmd.exe /k ', shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=None)
        process.stdin.write("wmic logicaldisk get size,freespace,caption\n")
        space,e=process.communicate()
      
        process.stdin.close()
    log.warning(space)
    log.warning(user_dataDir)
    return space
def clean_space():
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    dp = xbmcgui.DialogProgress()
            
    dp.create('Telemedia', '[B][COLOR=yellow]Cleaning[/COLOR][/B]'+'')
    HOME= xbmc_tranlate_path('special://home/')
    USERDATA= os.path.join(HOME,      'userdata')
    ADDONS           = os.path.join(HOME,      'addons')
    
    THUMBS= os.path.join(USERDATA,  'Thumbnails')
    TEMPDIR= xbmc_tranlate_path('special://temp')
    PACKAGES= os.path.join(ADDONS,    'packages')
    remove_all=[THUMBS,TEMPDIR,PACKAGES]
    for items in remove_all:
        dp.update(0, 'Please Wait...'+'\n'+'Removing File'+'\n'+ items )
        shutil.rmtree(items,ignore_errors=True, onerror=None)
    DATABASE         = os.path.join(USERDATA,  'Database')
    try:
        os.mkdir(THUMBS)
    except:
        pass
    try:
        os.mkdir(TEMPDIR)
    except:
        pass
    try:
        os.mkdir(PACKAGES)
    except:
        pass
    arr = os.listdir(DATABASE)
    
    dp.update(0, 'Please Wait...'+'\n'+'Clean DB'+'\n'+ '' )
    for items in arr:
        if 'Textures' in items:
            try:
                found=(os.path.join(DATABASE,items))
            except:
                pass
    cacheFile=found
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("DELETE  FROM path")
    dbcur.execute("DELETE  FROM sizes")
    dbcur.execute("DELETE  FROM texture")
    dbcur.execute("DELETE  FROM version")
    dbcon.commit()
    dbcur.close()
    dbcon.close()
    dp.close()
    xbmcgui.Dialog().ok('Clean','Done.')
def get_version():
    num=random.randint(1,1001)
    data={'type':'td_send',
                 'info':json.dumps({'@type': 'getOption','name':'version', '@extra': num})
                 }
    event2=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
    data={'type':'td_send',
                 'info':json.dumps({'@type': 'getMe', '@extra': num})
                 }
    event4=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
    xbmcgui.Dialog().ok('Tdlib Version','Name:'+event4['first_name']+'\n'+'User name:'+event4['username']+'\n'+'Phone Number:'+event4['phone_number']+'\n'+event2['value'])
def get_folders(iconimage,fanart):
    data={'type':'getfolders',
         'info':''
         }
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    log.warning(json.dumps(event))
    all_d=[]
    for items in event['status']:
        aa=addDir3(event['status'][items],str(items),12,iconimage,fanart,event['status'][items],groups_id=items,last_id='0$$$9223372036854775807')
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def select_file_browser():

            items  = xbmcvfs.listdir('androidapp://sources/apps/')[1]
            select = selectDialog("Select File Explorer",items)
            Addon.setSetting('Custom_Manager',select)
            
params=get_params()

log.warning(params)
for items in params:
   params[items]=params[items].replace(" ","%20")
url=None
name=None
mode=None
iconimage=None
fanart=None
resume=None
c_id=None
m_id=None
description=' '
original_title=' '
fast_link=''
data=0
id=' '
saved_name=' '
prev_name=' '
isr=0
no_subs=0
season="%20"
episode="%20"
show_original_year=0
groups_id=0
heb_name=' '
tmdbid=' '
eng_name=' '
dates=' '
data1='[]'
file_name=''
fav_status='false'
only_torrent='no'
only_heb_servers='0'
new_windows_only=False
meliq='false'
tv_movie='movie'
last_id='0$$$0$$$0$$$0'
r_art=''
r_logo=''
tmdb=''
next_page='0'
try:
	urp= urllib.parse.unquote_plus
except:
	urp=urllib.unquote_plus
try:
        url= urp(params["url"])
       
except:
        
        pass
try:
        tv_movie=(params["tv_movie"])
except:
        pass
try:
        name= urp(params["name"])
except:
        pass
try:
        iconimage= urp(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart= urp(params["fanart"])
except:
        pass
try:        
        description= urp(params["description"])
except:
        pass
try:        
        data= urp(params["data"])
except:
        pass
try:        
        original_title=(params["original_title"])
except:
        pass
try:        
        tmdb=(params["id"])
except:
        pass
try:        
        season=(params["season"])
except:
        pass
try:        
        episode=(params["episode"])
except:
        pass
try:        
        tmdbid=(params["tmdbid"])
except:
        pass
try:        
        eng_name=(params["eng_name"])
except:
        pass
try:        
        show_original_year=(params["show_original_year"])
except:
        pass
try:        
        heb_name= urp(params["heb_name"])
except:
        pass
try:        
        isr=int(params["isr"])
except:
        pass
try:        
        saved_name=clean_name(params["saved_name"],1)
except:
        pass
try:        
        prev_name=(params["prev_name"])
except:
        pass
try:        
        dates=(params["dates"])
except:
        pass
try:        
        no_subs=(params["no_subs"])
except:
        pass
try:        
        image_master= urp(params["image_master"])
except:
        pass
try:        
        last_id= urp(params["last_id"])
except:
        pass
try:        
        resume=(params["resume"])
except:
        pass
try:
    file_name=(params["file_name"])
except:
        pass
try:
    c_id=(params["c_id"])
except:
        pass
try:
    m_id=(params["m_id"])
except:
        pass
try:
    groups_id=(params["groups_id"])
except:
        pass
try:
    r_art=(params["r_art"])
except:
        pass
try:
    r_logo=(params["r_logo"])
except:
        pass
try:
    next_page=(params["next_page"])
except:
    pass

log.warning(params)
episode=str(episode).replace('+','%20')
season=str(season).replace('+','%20')
if season=='0':
    season='%20'
if episode=='0':
    episode='%20'
log.warning('Mode:'+str(mode))
log.warning('url:'+str(url))
#strn=get_free_space()
#xbmcgui.Dialog().ok('Error occurred',strn)
if (mode==None or url==None or len(url)<1) and len(sys.argv)>1:
        
        main_menu()
elif mode==2:
  
    file_list(url,data,last_id,description,iconimage,fanart,image_master=image_master,original_title=original_title)
elif mode==3:
    
    play(name,url,data,iconimage,fanart,no_subs,tmdb,season,episode,original_title,description,resume)
elif mode==4:
    data={'type':'logout',
         'info':''
         }
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
elif mode==5:
    data={'type':'login',
         'info':''
         }
    event=get_html('http://127.0.0.1:%s/'%listen_port,json=data).json()
    log.warning(event)
elif mode==6:
    
    search(url,data,last_id,description,iconimage,fanart,'0','0',no_subs=0)
elif mode==9:
    play_link(name,url,iconimage,fanart,no_subs,tmdb,season,episode,original_title)

elif mode==10:
    movies_menu()
elif mode==11:
    tv_show_menu()
elif mode==12:
    my_groups(last_id,url,groups_id,next_page)
elif mode==13:
    search_groups(iconimage,fanart)
elif mode==14:
    from resources.modules.tmdb import get_movies
    get_movies(url)
elif mode==15:
    search_movies(heb_name,original_title,data,iconimage,fanart,tmdb,season,episode)
elif mode==16:
    from resources.modules.tmdb import get_seasons
    get_seasons(name,url,iconimage,fanart,description,data,original_title,tmdb,heb_name,isr)
elif mode==17:
    
    ClearCache()
elif mode==18:
    get_genere(url)
elif mode==19:
    from resources.modules.tmdb import get_episode
    get_episode(name,url,iconimage,fanart,description,data,original_title,tmdb,season,tmdbid,show_original_year,heb_name,isr)
elif mode==20:
    search_tv(heb_name,original_title,data,iconimage,fanart,season,episode,tmdb)
elif mode==21:
    clear_all()
elif mode==22:
    join_chan(url)
elif mode==23:
    leave_chan(name,url)
elif mode==24:
    install_addon(original_title,url)
elif mode==25:
    install_build(original_title,url)
elif mode==26:
    from resources.modules.tmdb import get_movies
    get_movies(url,local=True)
elif mode==27:
    add_tv_to_db(name,url,data,iconimage,fanart,description)
elif mode==28:
    my_local_tv()
elif mode==29:
    remove_my_tv(name,url)
elif mode==30:
    pre_searches(url,data,last_id,description,iconimage,fanart)
elif mode==31:
    tmdb_world(last_id,iconimage,fanart,data)
elif mode==32:
    install_apk(original_title,url)
elif mode==33:
    full_data_groups()
elif mode==34:
    add_to_f_d_groups(url,name,data,iconimage,fanart,description)
elif mode==35:
    remove_f_d_groups(url,name)
elif mode==36:
    download_files(original_title,url)
elif mode==37:
    clear_search_h()
elif mode==38:
    groups_join(url,iconimage,fanart)
elif mode==39:
    join_group(url)
elif mode==40:
    play_remote(url,season,episode,original_title,tmdb,file_name,description,resume,name,heb_name,c_id=c_id,m_id=m_id,r_art=r_art,r_logo=r_logo,iconimage=iconimage,fanart=fanart)
elif mode==41:
    upload_log()
elif mode==42:
    join_all_groups(url)
elif mode==43:
    upload_log(backup=True)
elif mode==44:
    set_bot_id(name)
elif mode==45:
    search_updates()
elif mode==46:
    my_repo()
elif mode==47:
    multi_install(name,url,original_title)
elif mode==48:
    clean_space()
elif mode==101:
    tv_neworks()
elif mode==112:
    movie_prodiction()
elif mode==113:
    search_menu()
elif mode==114:
      main_trakt()
elif mode==115:
    progress_trakt(url)
elif mode==116:
    get_trakt()
elif mode==117:
     get_trk_data(url)
elif mode==118:
    trakt_liked(url,iconimage,fanart)
elif mode==119:
    get_version()
elif mode==120:
    Addon.openSettings()
elif mode==121:
    get_folders(iconimage,fanart)
elif mode==122:
    select_file_browser()
log.warning('exit_now:'+str(exit_now))
log.warning(sys.argv)
if len(sys.argv)>1:# and exit_now==0:
    '''
    if mode!=None and mode!=15 and mode!=20:
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATEADDED)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    '''
    if mode==2 or mode==12 :
        xbmcplugin.setContent(int(sys.argv[1]), 'files')
    else:
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')

    
   
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
   
    #td_close()
    
        
