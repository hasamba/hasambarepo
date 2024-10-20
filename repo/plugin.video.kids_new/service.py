# -*- coding: utf-8 -*-
import xbmc,time,logging,datetime,xbmcaddon

from resources.modules.hebdub_movies import update_now
from resources.modules.kidstv import update_now_tv
Addon = xbmcaddon.Addon()
from resources.modules import log
log.warning('Kids Service Started')

import socketserver 
import xbmc,json
import http.server as BaseHTTPServer
#from kids import refresh_list
import socket
from contextlib import closing
import threading

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
global server
server=0
free_port=find_free_port()

PORT_NUMBER =free_port


__version__ = "0.1"
import xbmcaddon
Addon = xbmcaddon.Addon()
if free_port!=int(Addon.getSetting("port")): 
        Addon.setSetting("port",str(free_port))
        xbmc.executebuiltin('Container.Refresh')
        
START=True

    
class RangeHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    """Simple HTTP request handler with GET and HEAD commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method.

    The GET and HEAD requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    server_version = "RangeHTTP/" + __version__
    
    def do_GET(self):
        
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        print(self.path)
        self.wfile.write("Get".encode())
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = json.loads(self.rfile.read(content_length)) # <--- Gets the data itself
        log.warning(post_data)
        #if post_data['u']=="":
        #    post_data['u']=None
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        refresh_list(post_data['u'],post_data['sys'])
        
        
        self.wfile.write("Post".encode())



socket_server=socketserver.ThreadingMixIn
class ThreadingSimpleServer(socket_server,
                            BaseHTTPServer.HTTPServer):
    pass
def start_server():
    global server
    print(' Start Server')
    #print 'Start1'
    # Set pathmap as request handler class variable
    RangeHTTPRequestHandler.uprclpathmap = {}
    #print 'Start3'
    server = ThreadingSimpleServer(('', PORT_NUMBER), RangeHTTPRequestHandler)
    #print 'Start'
    log.warning('Start Kids On')  
    server.serve_forever()
    


t = threading.Thread(target=start_server, args=())
#t.start()
try:
    cond=xbmc.Monitor().abortRequested()
except:
    cond=xbmc.abortRequested
log.warning('Server Mando On')  



monitor = xbmc.Monitor()


log.warning('!!!!!!!!!!!!!!!!!!Start Kids_new service!!!!!!!!!!!!!!!!!!')

strings = time.strftime("%Y,%m,%d,%H,%M,%S")
t = strings.split(',')
numbers = [ int(x) for x in t ]
pre_date=numbers[2]
while not cond:
 
    if monitor.waitForAbort(1):
            # Abort was requested while waiting. We should exit
            break
    
   
    
 
    START=False
    strings = time.strftime("%Y,%m,%d,%H,%M,%S")
    t = strings.split(',')
    numbers = [ int(x) for x in t ]
   
    if numbers[3]==int(Addon.getSetting("update_kids")) and numbers[2]!=pre_date:
        log.warning('Updating now Hebdub')
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kids New', 'מעדכן מדובבים')))
        pre_date=numbers[2]
        update_now()
        update_now_tv()
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kids New', 'הכל מעודכן')))

       
    xbmc.sleep(1000)
del monitor
    
#server.shutdown()
                             