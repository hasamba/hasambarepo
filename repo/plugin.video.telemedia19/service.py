# -*- coding: utf-8 -*-
#
# Copyright Aliaksei Levin (levlam@telegram.org), Arseny Smirnov (arseny30@gmail.com),
# Pellegrino Prevete (pellegrinoprevete@gmail.com)  2014-2019
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#
import os,time
from ctypes.util import find_library
from ctypes import *
import json,re,xbmcvfs
import sys,logging
from shutil import copyfile
import platform
from threading import Thread
import  os
from packaging import version

try:
    import xbmc,xbmcaddon,xbmcgui,xbmcvfs
    Addon = xbmcaddon.Addon()
    on_xbmc=True
except:
    on_xbmc=False

global complete_size,event,data_to_send,ready_data,stop_listen,create_dp_new,server,client,file_path,size,in_tans
global last_link,post_box,send_login,stop_now,in_install
global pending_install,all_folders
all_folders={}
pending_install={}
in_install=0
stop_now=False
last_link='empty'
send_login=0
complete_size=0
global total_size,ready_size,ready_size_pre,global_id,global_offset,global_end,global_path,global_size,wait_for_download,wait_for_download_photo,wait_for_download_complete,file_size,downn_path,global_f
global_f=None
downn_path={}
file_size={}
ready_size=0
total_size=0
ready_size_pre=0
wait_for_download_photo=0
global_id=0
global_offset=0
global_end=0
global_path=0
global_size=0
wait_for_download=0
wait_for_download_complete=0
post_box={}
in_tans=0
server=0
size=0
file_path=''
client=0
create_dp_new=0
if on_xbmc:
    if Addon.getSetting("autologin")=='true':
        stop_listen=0
    else:
        stop_listen=2
else:
    stop_listen=0
ready_data=''
data_to_send=''
event=''
import socket
from contextlib import closing

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

    
    
        
from http.server  import BaseHTTPRequestHandler,HTTPServer
free_port=find_free_port()
if on_xbmc:
    if free_port!=int(Addon.getSetting("port")): 
        Addon.setSetting("port",str(free_port))
        xbmc.executebuiltin('Container.Refresh')
else:
    #print 'Port:'+str(free_port)
    file = open('port.txt', 'w') 
    file.write(str(free_port))
    file.close()
PORT_NUMBER =free_port
logging.warning('Port:'+str(free_port))
import socketserver 
import http.server as BaseHTTPServer

import os
import posixpath

import urllib
import cgi,random
import shutil
import mimetypes





__version__ = "0.1"
def check_login(event):

    if 'message' in event:
        
        if 'content' in event['message']:
            if 'text' in event['message']['content']:
                if 'Login code' in event['message']['content']['text']['text']:
                    msg=event['message']['content']['text']['text'].split('.')
                    xbmcgui.Dialog().ok('Telemedia Code',str(msg[0]))
def check_name(id):
        global post_box
 
        
        num=random.randint(0,60000)
        td_send({'@type': 'getChat','chat_id':id, '@extra':num})
        
        
  
        event=wait_response_now(num,timeout=2)
        
        if event['notification_settings']['mute_for']>0 or event['notification_settings']['use_default_mute_for']==True:
            return 'off','off'
        
        chat_name='UNK'
        f_name=str(event['id'])+'_small.jpg'
        icon=os.path.join(logo_path,f_name)
        if event:
            
            chat_name=event['title']
            
            if 'photo' in event:
                if 'small' in event['photo']:
                    icon_id=event['photo']['small']['id']
                    f_name=str(event['id'])+'_small.jpg'
                    icon=os.path.join(logo_path,f_name)
            
        
        return chat_name,icon
def update_addon():

    try:
        global in_install,pending_install
        logging.warning('Waiting to update')
        while xbmc.Player().isPlaying() or in_install==1:
            time.sleep(0.1)
        in_install=1
        counter_ten=10
        from default import install_addon
        
        while(counter_ten)>0:
            counter_ten-=1
            time.sleep(1)
        for items in pending_install:
            f_name=pending_install[items]['f_name']
            
            link_data=pending_install[items]['link_data']
            c_f_name=pending_install[items]['c_f_name']
            ver=pending_install[items]['version']
            logging.warning('Done,Updating')
            
            logging.warning(c_f_name+',ver:'+ver)
            install_addon(f_name,json.dumps(link_data),silent=True)
            if on_xbmc:
                xbmc.executebuiltin('Notification(%s, %s, %d)'%('[COLOR yellow]Update Ok[/COLOR]',f_name, 5000))
            logging.warning('Update Done')
        pending_install={}
        in_install=0
    
    except Exception as e:
            import linecache,sys
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            logging.warning('ERROR IN Auto Install:'+str(lineno))
            logging.warning('inline:'+str(line))
            logging.warning(str(e))
            in_install=0
            pending_install={}
    
def has_addon(name):
    ex=False
    logging.warning('1')
    if xbmc.getCondVisibility("System.HasAddon(%s)" % name):
        logging.warning('2')
        ex=True
    else:
        addon_path=os.path.join(xbmcvfs.translatePath("special://home"),'addons/')
        logging.warning(addon_path)
        logging.warning(os.listdir(os.path.dirname(addon_path)))
        all_dirs=[]
        for items in os.listdir(os.path.dirname(addon_path)):
            all_dirs.append(items.lower())
        if name.lower() in all_dirs:
            
            ex=True
    ver=''
    if ex:
        ver=((xbmc.getInfoLabel('System.AddonVersion(%s)'%name)))
        
        if len(ver)==0:
            addon_path=os.path.join(xbmcvfs.translatePath("special://home"),'addons/')
            cur_folder=os.path.join(addon_path,name)
            logging.warning(os.path.join(cur_folder, 'addon.xml'))
            file = open(os.path.join(cur_folder, 'addon.xml'), 'r') 
            file_data= file.read()
            file.close()
            regex='name=.+?version=(?:"|\')(.+?)(?:"|\')'
            ver=re.compile(regex,re.DOTALL).findall(file_data)[0]
        
    return ex,ver
def check_update (event):
    global pending_install,in_install
    if 'message' in event:
        if 'chat_id' in event['message']:
            if ',' in Addon.getSetting("update_chat_id"):
                all_ids=Addon.getSetting("update_chat_id").split(',')
            else:
                all_ids=[Addon.getSetting("update_chat_id")]
            if str(event['message']['chat_id']) in all_ids:
                logging.warning('correct chatid')
                if 'content' in event['message']:
                    items=event['message']
                    if 'document' in event['message']['content']:
                        logging.warning('correct doc')
                        if 'file_name' in event['message']['content']['document']:
                            f_name=event['message']['content']['document']['file_name']
                            if '.zip' not in f_name:
                                return 0
                            c_f_name=f_name.split('-')
                            if len(c_f_name)==0:
                                return 0
                            c_f_name=c_f_name[0]
                            if '-' not in f_name:
                                return 0
                            new_addon_ver=f_name.split('-')[1].replace('.zip','')
                            logging.warning(f_name)
                            if c_f_name in pending_install:
                                ex=True
                                cur_version=pending_install[c_f_name]['version']
                            else:
                                ex,cur_version=has_addon(c_f_name)
                            if ex:
                               logging.warning('has addon')
                               
                               logging.warning(cur_version)
                               logging.warning(new_addon_ver)
                               logging.warning(version.parse(cur_version) < version.parse(new_addon_ver))
                               if version.parse(cur_version) < version.parse(new_addon_ver):
                                logging.warning('ver higher')
                                if on_xbmc:
                                    xbmc.executebuiltin('Notification(%s, %s, %d)'%('[COLOR yellow]New Update[/COLOR] Ver:%s'%new_addon_ver,c_f_name, 500))
                                link_data={}
                                link_data['id']=str(items['content']['document']['document']['id'])
                                link_data['m_id']=items['id']
                                link_data['c_id']=items['chat_id']
                                
                                logging.warning('install_addon')
                                pending_install[c_f_name]={'version':new_addon_ver,'f_name':f_name,'link_data':link_data,'c_f_name':c_f_name}
                                logging.warning('New Addon to update:'+f_name)
                                if in_install==0:
                                    thread=[]
                                    thread.append(Thread(update_addon))

                                    thread[0].start()
                                
                                
                                
                    
def check_notify(event):
    
    if 'message' in event:
        
        if 'content' in event['message']:
        
            if 'document' in event['message']['content']:
                if 'file_name' in event['message']['content']['document']:
                    #logging.warning('Found send file')
                    chat_source=event['message']['chat_id']
                    chat_name,icon=check_name(chat_source)
                    if chat_name!='off':
                            
                        
                        nm=event['message']['content']['document']['file_name']
                        __icon__=icon
                        if on_xbmc:
                            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('[COLOR yellow]'+chat_name+'[/COLOR]',nm, 5000, __icon__))
                    
def get_file_size(id):
    global post_box
    import random
    num=random.randint(0,60000)
    post_box[num]={'@type':'td_send','data':{'@type': 'getFile','file_id':int(id), '@extra': num},'status':'pending','responce':None}
                
    
    #print 'waiting_get_file'
    event=wait_response(num)
    
   
    return  event['size'],event['local']['path'],event['local']['downloaded_prefix_size']

def download_buffer(id,offset,limit):
            global post_box
            #print 'Download Buffer'
            path=''
            size=''
            #print 'Start:'+str(offset)
            #print 'End:'+str(limit)
            num=random.randint(0,60000)
            post_box[num]={'@type':'td_send','data':{'@type': 'downloadFile','file_id':int(id), 'priority':1,'offset':offset,'limit':limit, '@extra': num},'status':'pending','responce':None}
            
            #print {'@type': 'downloadFile','file_id':int(id), 'priority':1,'offset':offset,'limit':limit, '@extra': num}
            event=wait_response(num)
            
            #logging.warning('Downloading id:'+str(id))
           
            
            time.sleep(5)
            '''
            while True:
                
                event = td_receive()
                
                
                #print 'Buffer:'+str(event)
                
                
                if event:
                    #print event
                    if event.get('@type') =='error':
                        if on_xbmc:
                            xbmcgui.Dialog().ok('Telemedia Error',str(event.get('message')))
                        else:
                            #print str(event.get('message'))
                        
                        break
                    
                        
                    
                    if 'updateFile' in event['@type']:
                        
                        #print "downloaded_size:"+str(event['file']['local']['downloaded_size'])
                        if event['file']['local']['downloaded_prefix_size']>=(limit-offset):
                            path=event['file']['local']['path']
                            size=event['file']['size']
                            
                            break
                time.sleep(0.1)
            
            return path,size
            '''




def wait_download_file_complete(id,start_range,end_range):
    global global_id,global_offset,global_end,global_path,global_size,wait_for_download_complete
    global_path=''
    global_size=''
    global_id=id
    global_offset=start_range
    global_end=end_range 
    wait_for_download_complete=1
    while(wait_for_download_complete>0):
        time.sleep(0.001)
    return global_path
    
def wait_download_file_photo(id,start_range,end_range):
    global global_id,global_offset,global_end,global_path,global_size,wait_for_download_photo
    global_path=''
    global_size=''
    global_id=id
    global_offset=start_range
    global_end=end_range 
    wait_for_download_photo=1
    dp = xbmcgui.DialogProgressBG()

    dp.create('[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]Login[/COLOR][/B]')
    time_out=0
    while(wait_for_download_photo>0):
        try:
            dp.update(int((ready_size*100.0)/(complete_size+1)),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Downloading  [/COLOR][/B]')
        except:
            pass
        time_out+=1
        if (time_out>50000):
            break
        time.sleep(0.001)
    dp.close()
    return global_path
def wait_download_file(id,start_range,end_range):
    global global_id,global_offset,global_end,global_path,global_size,wait_for_download
    global_path=''
    global_size=''
    global_id=id
    global_offset=start_range
    global_end=end_range 
    wait_for_download=1
    while(wait_for_download>0):
        time.sleep(0.001)
    return global_path,global_size
def download_photo(id,offset,end,event):
    
    file_path=''
    
    if event:
       
        j_enent=(event)
       
        file='None'
        
                    
        
        
        if 'id' in j_enent :
            
            if j_enent['id']==id:
                file_path=j_enent['local']['path']
        elif "@type" in j_enent:
                    if 'updateFile' in j_enent['@type']:
                        if "file"  in j_enent:
                            if j_enent["file"]['id']==int(id):
                                if j_enent["file"]['local']['is_downloading_completed']==True:
                                    file_path=j_enent["file"]['local']['path']
        if 'expected_size' in event :

                    if len(event['local']['path'])>0 and (event['local']['is_downloading_completed']==True):
                        
                        path=event['local']['path']
                      
                        file_path=path
    
    return file_path
def download_file_complete(id,offset,end,event):
            global file_path
            path=''
            size=''
            
            
    
            if 1:

                
 
                if event:
                    
                    
                   
                    
                    
                    if 'updateFile' in event['@type']:
                        
                        
                        if len(event['file']['local']['path'])>0 :
                            path=event['file']['local']['path']
                            size=event['file']['size']
                            file_path=path
                    if 'expected_size' in event :
                        
                            
                            if len(event['local']['path'])>0  :
                                #logging.warning('Found Complete in buffer')
                                path=event['local']['path']
                                size=event['size']
                                file_path=path
                
            return path,size
def download_file_out(id,offset,end,event):
            global file_path
            path=''
            size=''
            
            if (end-offset)>10000000:
                buf=int(Addon.getSetting("buffer_size"))
            else:
                #buf=0x500
                buf=end-offset
    
            if 1:

                
 
                if event:
                    
                    
                   
                    
                    
                    if 'updateFile' in event['@type']:
                        
                        
                        if len(event['file']['local']['path'])>0 and (event['file']['local']['downloaded_prefix_size']>=buf):
                            path=event['file']['local']['path']
                            size=event['file']['size']
                            file_path=path
                    if 'expected_size' in event :
                        
                            
                            if len(event['local']['path'])>0 and ((event['local']['downloaded_prefix_size']>=buf) or (event['local']['is_downloading_completed']==True)):
                                #logging.warning('Found Complete in buffer')
                                path=event['local']['path']
                                size=event['size']
                                file_path=path
                
            return path,size
class RangeHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    """Simple HTTP request handler with GET and HEAD commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method.

    The GET and HEAD requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    server_version = "RangeHTTP/" + __version__
    def check_if_buffer_needed(self):
        global ready_size,total_size
        try:
            g_timer=xbmc.Player().getTime()
            g_item_total_time=xbmc.Player().getTotalTime()
        except:
            g_timer=0
            g_item_total_time=0
        try:
          if g_item_total_time>0:
            needed_size=g_timer*(total_size/(g_item_total_time))
            slep=False
           
            if (ready_size<(needed_size+10000)):
                slep=True
                if on_xbmc:
                  xbmc.Player().pause()
            while (ready_size<(needed_size+10000)):
                #logging.warning('Paused:')
                
                
                #logging.warning('ready_size:'+str(ready_size))
                #logging.warning('needed_size:'+str(needed_size))
                
                time.sleep(1)
                
            if slep:
                #logging.warning('Done ready_size:'+str(ready_size))
                if on_xbmc:
                    xbmc.Player().pause()
            return 'ok'
        except Exception as e:
            logging.warning('Check buffer err:'+str(e))
    def do_GET(self):
        global in_tans
        if stop_listen!=1:
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            
            
           
            self.wfile.write(bytes('Not Logged In',"utf-8"))
            return 0
        """Serve a GET request."""
        #print 'GOTTTT REQUESTS'
        time_buffer=int(Addon.getSetting("time_buffer"))
        f, start_range, end_range = self.send_head()
        if f:
            logging.warning ("do_GET: Got (%d,%d)" % (start_range,end_range))
            #time.sleep(1)
            f.seek(start_range, 0)
            #time.sleep(5)
            chunk =int(Addon.getSetting("chunk_size_new2")) *1024
            total = 0
            all_chunk=0
            self.stop_now=0
            adv_buffer=Addon.getSetting("advance_buffer")=='true'
            while chunk > 0:
                
            
                if (start_range + chunk) > (end_range):
                    
                    chunk = end_range - start_range
                #if adv_buffer:
                #    self.check_if_buffer_needed()
                
                try:
                    a=f.read(chunk)
                except Exception as e:
                    logging.warning( 'ERRRRRRRRRRRR333333:'+str(e))
                    pass
                try:
                    
                    
                    self.wfile.write(a)
                except Exception as e:
                    logging.warning( 'ERRRRRRRRRRRRRRRRRRRRRRR:'+str(e))
                    break
                    '''
                    time.sleep(0.1)
                    try:
                        self.wfile.write(a)
                    except Exception as e:
                        #logging.warning( 'ERRRRRRRRRRRRR2222222:'+str(e))
                        break
                    '''
                total += chunk
                #time.sleep(0.001)
                start_range += chunk
            f.close()
            logging.warning('Close This')
            logging.warning( total)
        
        
    def do_POST(self):
        global event,data_to_send,ready_data,stop_listen,create_dp_new,client,in_tans
        global post_box,file_size,downn_path,send_login,ready_size,total_size
        global last_link,stop_now
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = json.loads(self.rfile.read(content_length)) # <--- Gets the data itself
        logging.warning(str(post_data))
        logging.warning(str(stop_listen))
        if stop_listen==0 or stop_listen==2:
            
            if stop_listen==2:
                
                if post_data['type']=='login':
                    
                    
                    
                    create_dp_new=0
                    
                    #td_json_client_destroy(client)
                    client = td_json_client_create()
                    td_send({'@type': 'getAuthorizationState', '@extra': 1.01234})
                    stop_listen=0
                        
                    ready_data={'status':'Not logged in'}
                else:
                    if stop_listen==0:
                        dt='Wait for loggin'
                    else:
                        dt='Needs to log from setting'
                    ready_data={'status':dt,'stop':stop_listen}
            else:
                    #print('Still on login')
                    ready_data={'status':'Still on login'}
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            
            
           
            self.wfile.write(bytes(json.dumps(ready_data),"utf-8"))
        elif stop_listen==1:
            if post_data['type']=='login':
                td_send({'@type': 'getAuthorizationState', '@extra': 1.91234})
                ready_data={'status':'Logged in'}
            
            ready_data=''
            if post_data['type']=='td_send':
                #data_to_send=post_data['info']
                
                post_box[json.loads(post_data['info'])['@extra']]={'@type':'td_send','data':json.loads(post_data['info']),'status':'pending','responce':None}
                #logging.warning('TD Send Post')
                
                #td_send(json.loads(post_data['info']))
                
                ready_data=wait_response(json.loads(post_data['info'])['@extra'])
            elif post_data['type']=='stop_now':
                stop_now=True
                ready_data='ok'
            elif post_data['type']=='get_file_size':
                if post_data['info'] not in file_size:
                    #logging.warning('Not in file size')
                    file_size[post_data['info']]=0
                    downn_path[post_data['info']]=''
                ready_data={'path':downn_path[post_data['info']],'file_size':file_size[post_data['info']],'downloaded':ready_size,'total_size':total_size}
            elif post_data['type']=='kill_file_size':
                try:
                    if post_data['info']  in file_size:
                        del file_size[post_data['info']]
                        del downn_path[post_data['info']]
                except:
                    pass
                ready_data={'status':'OK'}
            elif post_data['type']=='download_complete':
                num=random.randint(0,60000)
                post_box[num]={'@type':'td_send','data':{'@type': 'downloadFile','file_id': post_data['info'], 'priority':1,'offset':0,'limit':0, '@extra': num},'status':'pending','responce':None}
                
                path=wait_download_file_complete(post_data['info'],0,0)
                
                ready_data=path
                del post_box[num]
                
                
                
            elif post_data['type']=='download_photo':
                num=random.randint(0,60000)
                post_box[num]={'@type':'td_send','data':{'@type': 'downloadFile','file_id': post_data['info'], 'priority':1,'offset':0,'limit':0, '@extra': num},'status':'pending','responce':None}
                
                path=wait_download_file_photo(post_data['info'],0,0)
                
                ready_data=path
                del post_box[num]
            elif post_data['type']=='clean_last_link':
                
                last_link='empty'
                ready_data='ok'
            elif post_data['type']=='get_last_link':
                ready_data=last_link
                last_link='empty'
            elif post_data['type']=='listen':
            
                post_box['get_status']={'status':'listen','responce':None}
                counter_wait=0
                while post_box['get_status']['responce']==None and counter_wait<10:
                    counter_wait+=1
                    time.sleep(0.1)
                ready_data = post_box['get_status']['responce']
            elif post_data['type']=='listen2':
                post_box['updateFile_local']={'status':'listen','responce':None}
                
                ready_data = post_box['updateFile_local']['responce']#td_receive()
            elif post_data['type']=='login':
                
                #print ('Already Logged in')
                ready_data={'status':'Logging'}
            elif post_data['type']=='logout':
                post_box[555.999]={'@type':'td_send','data':{'@type': 'logOut', '@extra': 555.999},'status':'pending','responce':None}
                
                #td_send({'@type': 'logOut', '@extra': 555.999})
                ready_data=wait_response(555.999)
                
                
                ready_data={'status':'Logedout'}
                
                stop_listen=2
                time.sleep(1)
                
                td_json_client_destroy(client)
                if on_xbmc:
                    xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', 'Loged Out ok'))
            elif post_data['type']=='checklogin':
                ready_data={'status':stop_listen}
            elif post_data['type']=='getfolders':
                ready_data={'status':all_folders}
            
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(ready_data),"utf-8"))
        
    def do_HEAD(self):
        
        """Serve a HEAD request."""
        
        f, start_range, end_range = self.send_head()
        if f:
            f.close()
       
    def send_head(self):
        global size,global_f,ready_size_pre,total_size,stop_now
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        
        
        id=self.path.replace('/','')
        start_range=0
        if "Range" in self.headers:
            s, e = self.headers['range'][6:].split('-', 1)
            sl = len(s)
            el = len(e)
            if sl > 0:
                start_range = int(s)
        
        
        #print 'Download file'
        if 1:#size==0:
            size,path,prefix=get_file_size(id)
            
            #download_buffer(id,(size-40000),size)
            #p,b=download_buffer(id,0,40000)
        #size=1525952019
        #

        #    
        
        ##print ("HTTP: path: %s" % self.path)
        #path = "e:\\aa.avi"#self.translate_path(self.path)
        
        
        
        if stop_now:
            stop_now=False
            self.send_response(404)
        else:
            if "Range" in self.headers:
                self.send_response(206)
            else:
                self.send_response(200)

        self.send_header("Content-type", 'video/mp4')
      
        start_range = 0
        end_range = size
        self.send_header("Accept-Ranges", "bytes")

        if "Range" in self.headers:
            s, e = self.headers['range'][6:].split('-', 1)
            sl = len(s)
            el = len(e)
            if sl > 0:
                start_range = int(s)
                if el > 0:
                    end_range = int(e) + 1
            elif el > 0:
                ei = int(e)
                if ei < size:
                    start_range = size - ei

        f = None
        num=random.randint(0,60000)
        post_box[num]={'@type':'td_send','data':{'@type': 'downloadFile','file_id':int(id), 'priority':1,'offset':start_range,'limit':end_range, '@extra': num},'status':'pending','responce':None}
                
        
        #print {'@type': 'downloadFile','file_id':int(id), 'priority':1,'offset':start_range,'limit':end_range, '@extra': num}
        #logging.warning('start_range:'+str(start_range))
        do_buffer=True
        if 1:#start_range==0:
            event=wait_response(num)
        
            if 'expected_size' in event :
                
                if len(event['local']['path'])>0 and (event['local']['is_downloading_completed']==True):
                    do_buffer=False
                    #logging.warning('Found Complete')
                    path=event['local']['path']
                    size=event['size']
        if do_buffer:
            path,size=wait_download_file(id,start_range,end_range)
        
        ready_size_pre=start_range
        total_size=size
        s_buffersize=int(Addon.getSetting("chunk_size_file")) *1024
        try:
            f = open(path, 'rb',buffering=s_buffersize)
            global_f=f
        except Exception as e:
            f=global_f
            logging.warning('File Error:'+str(e))
            self.send_error(404, "File not found")
            return (None, 0, 0)
        
        
        self.send_header("Content-Range",
                         'bytes ' + str(start_range) + '-' +
                         str(end_range - 1) + '/' + str(size))
    
        self.send_header("Content-Length", str(end_range-start_range))
        #self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()

        ##print ("Sending Bytes %d to %d" % (start_range, end_range))
        return (f, start_range, end_range)


    def translate_path(self, opath):
        path = urllib.unquote(opath)
        for p in self.uprclpathmap.itervalues():
            if path.startswith(p):
                return path
        #print ("HTTP: translate_path: %s not found in path map" % opath)
        return None

    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.mp4': 'video/mp4',
        '.ogg': 'video/ogg',
        })



#This class will handles any incoming request from
#the browser 
'''
class myHandler(BaseHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        #logging.warning("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        
        # Send the html message
        self.wfile.write(str(event))
        return
    def do_POST(self):
        global event,data_to_send,ready_data,stop_listen,create_dp_new,client
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = json.loads(self.rfile.read(content_length)) # <--- Gets the data itself
        #logging.warning(str(post_data))
        if stop_listen==0 or stop_listen==2:
            
            if stop_listen==2:
                
                if post_data['type']=='login':
                    
                    if stop_listen>0:
                    
                        create_dp_new=0
                        stop_listen=0
                        td_json_client_destroy(client)
                        client = td_json_client_create()
                    ready_data={'status':'Logging'}
                else:
                    if stop_listen==0:
                        dt='Wait for loggin'
                    else:
                        dt='Needs to log from setting'
                    ready_data={'status':dt,'stop':stop_listen}
            else:
                    #print('Still on login')
                    ready_data={'status':'Logging'}
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            
            
           
            self.wfile.write(json.dumps(ready_data))
        elif stop_listen==1:
        
            
            ready_data=''
            if post_data['type']=='td_send':
                #data_to_send=post_data['info']
                td_send(json.loads(post_data['info']))
                ready_data=wait_response(json.loads(post_data['info'])['@extra'])
            elif post_data['type']=='listen':
                ready_data = td_receive()
            elif post_data['type']=='login':
                
                #print ('Already Logged in')
                ready_data={'status':'Logging'}
            elif post_data['type']=='logout':
                td_send({'@type': 'logOut', '@extra': 555.999})
                ready_data=wait_response(555.999)
                #print ('Logout '+str(ready_data))
                ready_data={'status':'Logedout'}
            
            
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(json.dumps(ready_data))
'''
class ThreadingSimpleServer(socketserver.ThreadingMixIn,
                            BaseHTTPServer.HTTPServer):
    pass
def start_server():
    global server
    logging.warning('Start server')
    #print 'Start1'
    # Set pathmap as request handler class variable
    RangeHTTPRequestHandler.uprclpathmap = {}
    #print 'Start3'
    server = ThreadingSimpleServer(('', PORT_NUMBER), RangeHTTPRequestHandler)
    #print 'Start'
    
    server.serve_forever()
t = Thread(target=start_server, args=())
t.start()


#logging.warning('Server is Up')
if on_xbmc:

    
    user_dataDir = xbmcvfs.translatePath(Addon.getAddonInfo("profile"))
else:
    cur=os.path.dirname(os.path.abspath(__file__))
    user_dataDir = cur
logo_path=os.path.join(user_dataDir, 'logo')
files_path=os.path.join(user_dataDir, 'files')
db_path=os.path.join(user_dataDir, 'database')
log_path=os.path.join(user_dataDir, 'log')
try:
    if not os.path.exists(user_dataDir):
         os.makedirs(user_dataDir)

    if not os.path.exists(logo_path):
         os.makedirs(logo_path)

    if not os.path.exists(files_path):
         os.makedirs(files_path)

    if not os.path.exists(db_path):
         os.makedirs(db_path)

    if not os.path.exists(log_path):
         os.makedirs(log_path)
except:
    pass
    
machine= (platform.machine())
platform= (platform.architecture())
logging.warning(platform)

cur=os.path.dirname(os.path.abspath(__file__))
cur=os.path.join(cur,'resources','lib')
if platform[0]=='32bit':
        logging.warning('32bit')




if sys.platform.lower().startswith('linux'):
    plat = 'linux'
    if 'ANDROID_DATA' in os.environ:
        plat = 'android'
elif sys.platform.lower().startswith('win'):
    plat = 'windows'
elif sys.platform.lower().startswith('darwin'):
    plat = 'darwin'
else:
    plat = None
logging.warning('Platform:'+plat)
if plat == 'android':
    if platform[0]=='32bit':
        logging.warning('32bit')
        f_name='libtdjsonjava32'
    else:
        f_name='libtdjsonjava64'


    loc1=os.path.join(xbmcvfs.translatePath('special://xbmc'),'libtdjsonjava.so')
    
  

    loc4=os.path.join(xbmcvfs.translatePath('special://xbmc'),'libtdjson.so')

  
    copyfile(os.path.join(cur,'%s.so'%f_name),loc1)

    #all_option=[loc1,loc2,loc3]#,os.path.join(cur,'lib','libtdjni.so'),os.path.join(cur,'lib','libtdjsonjava_armv7.so'),os.path.join(cur,'lib','libtdjsonjava_arm64.so'),os.path.join(cur,'lib','libtdjsonjava_and_x86.so'),os.path.join(cur,'lib','libtdjsonjava_and_64.so')]
    #all_option2=[loc4,loc5,loc6]
  
    if 1:#for items in all_option:
        try:
            logging.warning('CDLL:'+loc1)
            tdjson=CDLL(loc1)
         
          
            #cwd=xbmcvfs.translatePath('special://xbmc')
            #logging.warning('Imp:'+loc1)
            
            #fo, p, d = imp.find_module('libtdjsonjava', [cwd])
            #logging.warning('tdjson:'+cwd)
            #tdjson = imp.load_module('libtdjsonjava', fo, p, d)
    
            #break
        except Exception as e:
            logging.warning(e)
            pass 
    td_json_client_create = tdjson._td_json_client_create
    td_json_client_create.restype = c_void_p
    td_json_client_create.argtypes = []

    td_json_client_receive = tdjson._td_json_client_receive
    td_json_client_receive.restype = c_char_p
    td_json_client_receive.argtypes = [c_void_p, c_double]

    td_json_client_send = tdjson._td_json_client_send
    td_json_client_send.restype = None
    td_json_client_send.argtypes = [c_void_p, c_char_p]

    td_json_client_execute = tdjson._td_json_client_execute
    td_json_client_execute.restype = c_char_p
    td_json_client_execute.argtypes = [c_void_p, c_char_p]

    td_json_client_destroy = tdjson._td_json_client_destroy
    td_json_client_destroy.restype = None
    td_json_client_destroy.argtypes = [c_void_p]
    #logging.warning('Done Define')
    
if plat == 'linux':
    if machine.lower().startswith('arm') or machine.lower().startswith('st'):
       logging.warning('arm')
       f_name= 'libtdjson_armv7.so'
    else:
       logging.warning('linux')
       f_name= 'libtdjson_x86.so'
    ph=os.path.join(cur,f_name)          
    logging.warning ("cur:"+ph)
    tdjson = CDLL(ph)

    # tdjson = CDLL(tdjson_path)

    td_json_client_create = tdjson.td_json_client_create
    td_json_client_create.restype = c_void_p
    td_json_client_create.argtypes = []

    td_json_client_receive = tdjson.td_json_client_receive
    td_json_client_receive.restype = c_char_p
    td_json_client_receive.argtypes = [c_void_p, c_double]

    td_json_client_send = tdjson.td_json_client_send
    td_json_client_send.restype = None
    td_json_client_send.argtypes = [c_void_p, c_char_p]

    td_json_client_execute = tdjson.td_json_client_execute
    td_json_client_execute.restype = c_char_p
    td_json_client_execute.argtypes = [c_void_p, c_char_p]

    td_json_client_destroy = tdjson.td_json_client_destroy
    td_json_client_destroy.restype = None
    td_json_client_destroy.argtypes = [c_void_p]
    logging.warning('Done Define')        
 
if plat == 'windows':
    if platform[0]=='64bit':

        cur=os.path.join(cur,'x64')
        crypt_name='libcrypto-1_1-x64.dll'
        ssl_name='libssl-1_1-x64.dll'
    else:
        crypt_name='libcrypto-1_1.dll'
        ssl_name='libssl-1_1.dll'
    
    #ph=os.path.join(cur,'libeay32.dll')
    ph=os.path.join(cur,crypt_name)
    logging.warning(ph)
    CDLL(ph)


    #ph=os.path.join(cur,'ssleay32.dll')
    ph=os.path.join(cur,ssl_name)
    logging.warning(ph)
    CDLL(ph)


    ph=os.path.join(cur,'zlib1.dll')


    CDLL(ph)

    ph=os.path.join(cur,'tdjson.dll')
    logging.warning (ph)
    tdjson = CDLL(ph)

    # tdjson = CDLL(tdjson_path)

    td_json_client_create = tdjson.td_json_client_create
    td_json_client_create.restype = c_void_p
    td_json_client_create.argtypes = []

    td_json_client_receive = tdjson.td_json_client_receive
    td_json_client_receive.restype = c_char_p
    td_json_client_receive.argtypes = [c_void_p, c_double]

    td_json_client_send = tdjson.td_json_client_send
    td_json_client_send.restype = None
    td_json_client_send.argtypes = [c_void_p, c_char_p]

    td_json_client_execute = tdjson.td_json_client_execute
    td_json_client_execute.restype = c_char_p
    td_json_client_execute.argtypes = [c_void_p, c_char_p]

    td_json_client_destroy = tdjson.td_json_client_destroy
    td_json_client_destroy.restype = None
    td_json_client_destroy.argtypes = [c_void_p]
    
    td_set_log_file_path = tdjson.td_set_log_file_path
    td_set_log_file_path.restype = c_int
    td_set_log_file_path.argtypes = [c_char_p]

    td_set_log_max_file_size = tdjson.td_set_log_max_file_size
    td_set_log_max_file_size.restype = None
    td_set_log_max_file_size.argtypes = [c_longlong]

    td_set_log_verbosity_level = tdjson.td_set_log_verbosity_level
    td_set_log_verbosity_level.restype = None
    td_set_log_verbosity_level.argtypes = [c_int]

    fatal_error_callback_type = CFUNCTYPE(None, c_char_p)

    td_set_log_fatal_error_callback = tdjson.td_set_log_fatal_error_callback
    td_set_log_fatal_error_callback.restype = None
    td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]
    td_set_log_verbosity_level(0)
    def on_fatal_error_callback(error_message):
        logging.warning('TDLib fatal error: '+ error_message)
    c_on_fatal_error_callback = fatal_error_callback_type(on_fatal_error_callback)
    td_set_log_fatal_error_callback(c_on_fatal_error_callback)



 

def td_execute(query):
    query = json.dumps(query).encode('utf-8')
    result = td_json_client_execute(None, query)
    if result:
        result = json.loads(result.decode('utf-8'))
    return result



# setting TDLib log verbosity level to 1 (errors)
##logging.warning(td_execute({'@type': 'setLogVerbosityLevel', 'new_verbosity_level': 1, '@extra': 1.01234}))

##logging.warning(td_execute({'@type': 'setLogStream', 'log_stream': {'@type':'logStreamFile','path':log_f,'max_file_size':1000000000}, '@extra': 1.01234}))
#exit()
#a=a+1

# create client
if stop_listen==0:
    client = td_json_client_create()

# simple wrappers for client usage
def td_send(query):
    query = json.dumps(query).encode('utf-8')
    td_json_client_send(client, query)

def td_receive():
    try:
        result = td_json_client_receive(client, 0.01)
        if result:
            result = json.loads(result.decode('utf-8'))
        return result
    except Exception as e:
        logging.warning('Rec err:'+str(e))
        return ''

# another test for TDLib execute method
##logging.warning(td_execute({'@type': 'getTextEntities', 'text': '@telegram /test_command https://telegram.org telegram.me', '@extra': ['5', 7.0]}))
def wait_response_now(id,dp='',timeout=10):
    global post_box
    ret_value=''
    counter=0
    
    while True:
        event = td_receive()
        if event:
            if '@extra' in event :
                if event['@extra']==int(id):
                    break
        
        
            
        
            #    #print post_box[id]['status']
        time.sleep(0.001)
    return (event)
    
def wait_response(id,dp='',timeout=10):
    global post_box
    ret_value=''
    counter=0
    logging.warning('Wait res')
    while True:
        
        
        
        
            
        counter+=1
        if timeout>0:
            if counter>(timeout*1000):
                logging.warning('Wait res Timeout')
                del post_box[id]
                return None
        if id in post_box:
            
            if post_box[id]['status']=='recived':
                #print 'found ret'
                ret_value=post_box[id]['responce']
                del post_box[id]
                break
            #else:
            #    #print post_box[id]['status']
        time.sleep(0.001)
   
    return (ret_value)
# testing TDLib send method
if stop_listen==0:
    td_send({'@type': 'getAuthorizationState', '@extra': 1.01234})

# main events cycle
#logging.warning('Start Telemedia 2.0 service on port:'+str(free_port))
if on_xbmc:
  
    cond=xbmc.Monitor().abortRequested()
else:
    cond=0


event=None
while not cond:
    if send_login==1:
        send_login=0
        td_send({'@type': 'getAuthorizationState', '@extra': 99.991234})
        
        
    if 0:#on_xbmc:
        if monitor.waitForAbort(1):
                # Abort was requested while waiting. We should exit
                break
    
    
    if stop_listen==0:
        if create_dp_new==0:
            #logging.warning('create_dp_new')
            if on_xbmc:
                dp = xbmcgui.DialogProgressBG()

                dp.create('[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]Login[/COLOR][/B]')
            create_dp_new=1
        
        
        
        if event:
            '''
            if 'scope' in event:
                if ['@type']=='notificationSettingsScopeChannelChats':
                    if on_xbmc:
                        dp.update(0,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]notificationSettingsScopeChannelChats  [/COLOR][/B]')
                    #logging.warning('wating td_send')
                    td_send({'@type': 'getChats','offset_order':9223372036854775807, 'limit': '500', '@extra': 1.01234})
                    event=wait_response(1.01234)
                    #logging.warning('wating event')
                    #logging.warning(event)
            '''
            #logging.warning(event)
            if event.get('@type') =='error':
                    if on_xbmc:
                       
                        
                        xbmcgui.Dialog().ok('Telemedia Error',str(event.get('message')))
                        
                        if str(event.get('message'))=='PHONE_NUMBER_INVALID':
                            phone_number = xbmcgui.Dialog().input(Addon.getLocalizedString(32036).encode('ascii', 'ignore').decode('ascii'), '', xbmcgui.INPUT_NUMERIC)#
                            
                            td_send({'@type': 'setAuthenticationPhoneNumber', 'phone_number': str(phone_number)})
                            
                        if str(event.get('message'))=='PASSWORD_HASH_INVALID':
                            password = xbmcgui.Dialog().input(Addon.getLocalizedString(32038).encode('ascii', 'ignore').decode('ascii'), '', xbmcgui.INPUT_ALPHANUM)
                            if password=='':
                                xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia','Login Canceled'))
                                dp.close()
                                stop_listen=2
                            else:
                                td_send({'@type': 'checkAuthenticationPassword', 'password': str(password)})
                        if str(event.get('message'))=='PHONE_CODE_INVALID':
                            code = xbmcgui.Dialog().input(Addon.getLocalizedString(32037).encode('ascii', 'ignore').decode('ascii'), '', xbmcgui.INPUT_NUMERIC)
                            if code=='':
                                xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia','Login Canceled'))
                                dp.close()
                                stop_listen=2
                            else:
                                td_send({'@type': 'checkAuthenticationCode', 'code': str(code)})
            # process authorization states
            if event['@type'] == 'updateAuthorizationState':
                if on_xbmc:
                    dp.update(20,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]updateAuthorizationState  [/COLOR][/B]')
                auth_state = event['authorization_state']
                
                # if client is closed, we need to destroy it and create new client
                if auth_state['@type'] == 'authorizationStateClosed':
                    if on_xbmc:
                        dp.close()
                    stop_listen=2

                # set TDLib parameters
                # you MUST obtain your own api_id and api_hash at https://my.telegram.org
                # and use them in the setTdlibParameters call
                
                if auth_state['@type'] == 'authorizationStateWaitTdlibParameters':
                    td_send({'@type': 'setTdlibParameters', 'parameters': {
                                                           'database_directory': db_path,
                                                           'files_directory': files_path,
                                                           'use_message_database': True,
                                                           'use_secret_chats': True,
                                                           'api_id': 94575,
                                                           'api_hash': 'a3406de8d171bb422bb6ddf3bbd800e2',
                                                           'system_language_code': 'en',
                                                           'device_model': 'Desktop',
                                                           'system_version': 'Linux',
                                                           'application_version': '1.0',
                                                           'enable_storage_optimizer': True}})

                # set an encryption key for database to let know TDLib how to open the database
                elif auth_state['@type'] == 'authorizationStateWaitEncryptionKey':
                    if on_xbmc:
                        dp.update(40,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]authorizationStateWaitEncryptionKey  [/COLOR][/B]')
                    td_send({'@type': 'checkDatabaseEncryptionKey', 'key': 'my_key'})

                # enter phone number to log in
                elif auth_state['@type'] == 'authorizationStateWaitPhoneNumber':
                    if on_xbmc:
                        dp.update(60,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]authorizationStateWaitPhoneNumber  [/COLOR][/B]')
                        
                        #Enter phone number (Without the +):
                        phone_number = xbmcgui.Dialog().input(Addon.getLocalizedString(32036).encode('ascii', 'ignore').decode('ascii'), '', xbmcgui.INPUT_NUMERIC)#
                        
                            
                    else:
                        phone_number = input('Please enter your phone number: ')
                    if phone_number=='':
                                xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia','Login Canceled'))
                                dp.close()
                                stop_listen=2
                                td_json_client_destroy(client)
                    else:
                        td_send({'@type': 'setAuthenticationPhoneNumber', 'phone_number': str(phone_number)})

                # wait for authorization code
                elif auth_state['@type'] == 'authorizationStateWaitCode':
                    if on_xbmc:
                        #logging.warning('1')
                        dp.update(70,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]authorizationStateWaitCode  [/COLOR][/B]')
                        #'Enter code:'
                        #logging.warning('2')
                        code = xbmcgui.Dialog().input(Addon.getLocalizedString(32037).encode('ascii', 'ignore').decode('ascii'), '', xbmcgui.INPUT_NUMERIC)
                    else:
                        code = input('Please enter the authentication code you received: ')
                    if code=='':
                                xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia','Login Canceled'))
                                dp.close()
                                stop_listen=2
                                td_json_client_destroy(client)
                    else:
                        td_send({'@type': 'checkAuthenticationCode', 'code': str(code)})

                # wait for first and last name for new users
                elif auth_state['@type'] == 'authorizationStateWaitRegistration':
                    first_name = input('Please enter your first name: ')
                    last_name = input('Please enter your last name: ')
                    td_send({'@type': 'registerUser', 'first_name': first_name, 'last_name': last_name})

                # wait for password if present
                elif auth_state['@type'] == 'authorizationStateWaitPassword':
                    
                    
                    if on_xbmc:
                        dp.update(90,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]authorizationStateWaitPassword  [/COLOR][/B]')
                        #'Password:'
                        password = xbmcgui.Dialog().input(Addon.getLocalizedString(32038).encode('ascii', 'ignore').decode('ascii'), '', xbmcgui.INPUT_ALPHANUM)
                    else:
                        password = raw_input('Please enter your password: ')
                    if password=='':
                                xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia','Login Canceled'))
                                dp.close()
                                stop_listen=2
                                td_json_client_destroy(client)
                    else:
                        td_send({'@type': 'checkAuthenticationPassword', 'password': str(password)})
                elif auth_state['@type'] == "authorizationStateReady":
                    #logging.warning('In end')
                    stop_listen=1
                    if on_xbmc:
                        dp.close()
                        #'Login Complete'
                        
                        e=(Addon.getLocalizedString(32039)).encode('ascii','replace').decode('ascii')
                        xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia',e))
                        
                        xbmc.executebuiltin('Container.Refresh')
            # handle an incoming update or an answer to a previously sent request
                
            sys.stdout.flush()
    elif stop_listen==1:
        
        if wait_for_download_photo==1:
            global_path=download_photo(global_id,global_offset,global_end,event)
            if global_path!='':
                wait_for_download_photo=0
        if wait_for_download==1:
            
            global_path,global_size=download_file_out(global_id,global_offset,global_end,event)
            if global_path!='':
                wait_for_download=0
        if wait_for_download_complete==1:
            global_path,global_size=download_file_complete(global_id,global_offset,global_end,event)
            if global_path!='':
                wait_for_download_complete=0
        try:
            
            for items in post_box:
                    
                    if post_box[items]['status']=='pending':
                        
                        td_send(post_box[items]['data'])
                        post_box[items]['status']='send'
        except Exception as e:
            logging.warning('Err in pending:'+str(e))
            pass
        if event:
            
            try:
                if "@type" in event:
                    if 'updateFile' in event['@type']:
                        
                        for items in file_size:
                            if "file"  in event:
                                
                                if event["file"]['id']==int(items):
                                    file_size[items]=event['file']['local']['downloaded_size']
                                    downn_path[items]=event['file']['local']['path']
                    
            except Exception as e:
                logging.warning('Err in filesize:'+str(e))
                pass
            if event.get('@type') =='error':
                    if on_xbmc:
                        #dp.close()
                        xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia',str(event.get('message'))))
                        '''
                        if 'USER_ALREADY_PARTICIPANT' in str(event.get('message')) or 'Too Many Requests: retry after' in str(event.get('message')):
                            xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia',str(event.get('message'))))
                        else:
                            xbmcgui.Dialog().ok('Telemedia Error',str(event.get('message')))
                        '''
                    
            try:
                
                for items in post_box:
                       
                       
                        if post_box[items]['status']=='send':
                            if '@extra' in event :
                                #logging.warning('TD RECIVING NOW')
                                if event['@extra']==(items):
                                    #logging.warning('TD RECIVING DONE')
                                    post_box[items]['responce']=event
                                    post_box[items]['status']='recived'
                        if post_box[items]['status']=='listen':
                            if "@type" in event:
                                if 'updateFile' in event['@type']:
                                    post_box[items]['responce']=event
                                    
                        if items=='updateFile_local':
                            if "@type" in event:
                                if 'updateFile' in event['@type']:
                                    if "file"  in event:
                                        
                                        file=event["file"]['local']['path']
                                        if xbmcvfs.exists(file) and event["file"]['id']==post_box[items]['id']:
                                        
                                            
                                            post_box[items]['responce']=file
                                            
            except Exception as e:
                    logging.warning('Err post:'+str(e))
    if stop_listen!=2:
        try:
            if on_xbmc:
                
                if 0:
                    logging.warning('Break')
                    break
                event = td_receive()
                #logging.warning(event)
            else:
                try:
                    event = td_receive()
                except Exception as e:
                    logging.warning('Error td_recive:'+str(e))
                    break
            if event:
                
                if "@extra" in event:
                    if event["@extra"]==1.91234:
                        xbmc.executebuiltin('Notification(%s, %s, %d)'%('[COLOR yellow]Connection[/COLOR]',event["@type"], 5000))
                
                if 'chat_filters' in event:
                    for ite in event['chat_filters']:
                        all_folders[ite['id']]=ite['title']
            
            if stop_listen==1:
                if event:
                    
                    if on_xbmc:
                        if Addon.getSetting("full_debug")=='true':
                            logging.warning(json.dumps(event))
                    
                      
                      
                    if 'updateFile' in event['@type']:
                    
                    
                    
                      ready_size=ready_size_pre+event['file']['local']['downloaded_prefix_size']
                      
                    if 'expected_size' in event :
                    
                      ready_size=ready_size_pre+event['local']['downloaded_prefix_size']
                    if on_xbmc:
                        if 'size' in event:
                            complete_size=event['size']
                        if Addon.getSetting("auto_update")=='true' and len(Addon.getSetting("update_chat_id"))>0:
                            check_update(event)
                        #if Addon.getSetting("get_notify")=='true':
                        #   check_notify(event)
                        if Addon.getSetting("show_login")=='true':
                        
                           check_login(event)
                    if 'message' in event:
                       if 'chat_id' in event['message']:
                        if str(event['message']['chat_id'])=='772555074':
                            if 'text' in event['message']['content']:
                                if 'text' in event['message']['content']['text']:
                                    txt=event['message']['content']['text']['text']
                                    
                                    last_link_pre=re.compile('Here is the link to your file\n\n(.+?)\n\n').findall(txt)
                                    last_link='Found'
                                    if len(last_link_pre)>0:
                                       
                                        last_link=last_link_pre[0]
                                
        except Exception as e:
            import linecache,sys
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            logging.warning('ERROR IN service:'+str(lineno))
            logging.warning('inline:'+str(line))
            logging.warning(str(e))
            
            
            if not on_xbmc:
                break
    else:
        try:
            time.sleep(0.1)
        except:
            break
# destroy client when it is closed and isn't needed anymore
#logging.warning('Destroy Client')

td_json_client_destroy(client)
try:
    os.remove(file_path)
except:
    pass
server.shutdown()

#logging.warning('Done Destroy Client')
