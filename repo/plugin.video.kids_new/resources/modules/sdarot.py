# -*- coding: utf-8 -*-
import socket,ssl,os,io
from resources.modules import log
import time,xbmc,xbmcaddon
Addon = xbmcaddon.Addon()
from  resources.modules import cache

import xbmcvfs
from urllib.parse import parse_qsl
xbmc_tranlate_path=xbmcvfs.translatePath
global global_var,stop_all#global
global progress
progress=''
global_var=[]
stop_all=0
import hashlib
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
if KODI_VERSION<=18:
    import urllib2
    import urlparse
    import httplib
    url_r=urllib2
else:
    import urllib
    import urllib.parse as urlparse
    import http.client as httplib
    import urllib.request
    url_r=urllib.request
import urllib,logging,base64,json
if KODI_VERSION<=18:
    que=urllib.quote_plus
    que_n=urllib.quote
    url_encode=urllib.urlencode
else:
    que_n=urllib.parse.quote
    que=urllib.parse.quote_plus
    url_encode=urllib.parse.urlencode

if KODI_VERSION<=18:
    xbmc_tranlate_path=xbmc_tranlate_path
else:
    import xbmcvfs
    xbmc_tranlate_path=xbmcvfs.translatePath
if Addon.getSetting("regex_mode")=='1':
    import regex  as re
else:
    import re

type=['tv','non_rd']


from  resources.modules.client import get_html

HEADERS={
    'User-agent': 'Sdarot AndroidTV 4,1.2.0p; Android: 23,6.0.1',
    'pkg': 'com.phone.sdarottv',
    
    'Content-Type': 'application/x-www-form-urlencoded',


    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'utf-8',

    }
local=False
try:
  import xbmcgui,xbmcaddon,xbmc
  CACHE_FILE = os.path.join(xbmc_tranlate_path(xbmcaddon.Addon().getAddonInfo('profile')).decode('utf-8'), 'cache.json')
except:
  local=True
  dataPath=os.path.dirname(os.path.realpath(__file__))
  CACHE_FILE=os.path.join(dataPath,'cache_f')
  

from resources import API
POSTER_PREFIX = base64.b64decode('aHR0cHM6Ly9zdGF0aWMuc2Rhcm90LndvcmxkL3Nlcmllcy8=').decode('utf-8')

user_dataDir_pre = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
user_dataDir_img=os.path.join(user_dataDir_pre,'images')
if not os.path.exists(user_dataDir_img):
    os.makedirs(user_dataDir_img)

t_path = xbmc_tranlate_path(xbmcaddon.Addon().getAddonInfo('path'))
try:
    import dns.resolver
except:
    import shutil
    d= os.path.join(t_path,'dns')
    if os.path.exists(d):
        shutil.rmtree(d)
    if KODI_VERSION<=18:
        dns_path=os.path.join(t_path,'dns_17')
    else:
        dns_path=os.path.join(t_path,'dns_19')
    
    shutil.copytree(dns_path, d, False, None)
    import dns.resolver
def get_ip(address):
    headers=HEADERS
    a_key=urlparse.urlparse(address).netloc
    req = ('https://dns.google.com/resolve?name='+a_key)
    log.warning(req)
    data=get_html(req,headers=headers).json()
    log.warning(data)
    return data['Answer'][0]['data']


def cache_ip(address):
    try:
        if not os.path.isfile(CACHE_FILE):
            a_list = {}
        else:
            with open(CACHE_FILE, 'r') as handle:
                a_list = json.load(handle)
        a_key = base64.b64encode(urlparse.urlparse(address).netloc.encode("utf-8"))
        if not a_list.get(a_key):
            a_list[a_key] = {'a': 0, 'b': ''}
        now = int(time.time())
        if now - a_list[a_key]['a'] > 86400:
            a_list[a_key]['b'] =  base64.b64decode(get_ip(base64.b64decode(a_key)))
            a_list[a_key]['a'] =  now
            with io.open(CACHE_FILE, 'w', encoding='utf-8') as handle:
                handle.write((json.dumps(a_list, ensure_ascii=False)))
        return base64.b64decode(a_list[a_key]['b']).decode('utf-8')
    except Exception as e:
        import linecache,sys
        sources_searching=False
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        log.warning('ERROR IN cache_ip:'+str(lineno))
        log.warning('inline:'+line)
        log.warning('Error:'+str(e))
        
        return None
def MyResolver(host):
  dns_value=Addon.getSetting('dns')
  dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
  dns.resolver.default_resolver.nameservers=[dns_value]
  answer = dns.resolver.query(host)
  #resolver = dns.resolver.Resolver()
  
 
  #resolver.nameservers = [dns_value]
  #answer = resolver.query(host,'A')
 
  
  
    
  return answer[0].address
class MyHTTPConnection(httplib.HTTPConnection):
  def connect(self):
    self.sock = socket.create_connection((MyResolver(self.host),self.port),self.timeout)
class MyHTTPSConnection(httplib.HTTPSConnection):
  def connect(self):
    sock = socket.create_connection((MyResolver(self.host), self.port), self.timeout)
    self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file)

class MyHTTPHandler(url_r.HTTPHandler):
  def http_open(self,req):
    return self.do_open(MyHTTPConnection,req)

class MyHTTPSHandler(url_r.HTTPSHandler):
  def https_open(self,req):
    return self.do_open(MyHTTPSConnection,req)
    
    
    
    
def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature
def get_auth(string_to_encode):

    a=encrypt_string(string_to_encode+'Sdarot AndroidTV 4,1.2.0p; Android: 23,6.0.1')
    
    b=encrypt_string(a+'KvtIUb//NH;$6U^]DP\'Uc33}Q5YMM-i?')
    return b
class resolve_dns():
    
    def __init__(self,url,headers=HEADERS,cookies={},data={}):
        self.url=url
        headers['auth']=get_auth(url.replace(API,''))
        
        self.headers=headers
        self.cookies=cookies
        self.data=data
    def download_image(self):
        try:
            import cookielib
        except:
            import http.cookiejar
            cookielib = http.cookiejar
        if Addon.getSetting('dns_solver')=='1':
            new_ip=cache.get(self.get_ip,24, table='cookies')
            
            
            
            self.url=self.url.replace(API,'https://'+new_ip)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
        handlers = [MyHTTPHandler,MyHTTPSHandler]
        cookjar = cookielib.CookieJar()
        handlers += [url_r.HTTPHandler(), url_r.HTTPSHandler(), url_r.HTTPCookieProcessor(cookjar)]
        if Addon.getSetting('dns_solver')=='1':
            handlers = [url_r.HTTPHandler(), url_r.HTTPSHandler(context=ctx), url_r.HTTPCookieProcessor(cookjar)]
        opener = url_r.build_opener(*handlers)
        #opener.addheaders.append(('Set-Cookie', url_encode(self.cookies)))
    
        if 'Sdarot' in self.cookies:

          self.headers['Cookie']='Sdarot={0}'.format((self.cookies.get('Sdarot')))
        elif 'Sratim' in self.cookies:
            self.headers['Cookie']='Sratim={0}'.format((self.cookies.get('Sratim')))
        
        request = url_r.Request(self.url.replace(' ','%20'),  headers=self.headers,data=url_encode(self.data).encode("utf-8"))
        log.warning('self.url:'+str(self.url))
        request.get_method = lambda: 'GET'
        html = opener.open(request).read()
        img_n=self.url.split('/')
        f_img=img_n[len(img_n)-1].replace('/','')
        f_save=os.path.join(user_dataDir_img,f_img)
        
        with open( f_save, "wb" ) as f:
          f.write( html )
    def get_ip(self):
        
        
        req = (base64.b64decode('aHR0cHM6Ly9kbnMuZ29vZ2xlLmNvbS9yZXNvbHZlP25hbWU9').decode('utf-8')+API.replace('https://',''))
        data=get_html(req,headers=self.headers).json()

        return data['Answer'][0]['data']
    def get(self):
        
        
        try:
            import cookielib
        except:
            import http.cookiejar
            cookielib = http.cookiejar
        
        if Addon.getSetting('dns_solver')=='1':
            new_ip=cache.get(self.get_ip,24, table='cookies')
            
            
            
            self.url=self.url.replace(API,'https://'+new_ip)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
        handlers = [MyHTTPHandler,MyHTTPSHandler]
        cookjar = cookielib.CookieJar()
        handlers += [url_r.HTTPHandler(), url_r.HTTPSHandler(), url_r.HTTPCookieProcessor(cookjar)]
        if Addon.getSetting('dns_solver')=='1':
            handlers = [url_r.HTTPHandler(), url_r.HTTPSHandler(context=ctx), url_r.HTTPCookieProcessor(cookjar)]
        opener = url_r.build_opener(*handlers)
        #opener.addheaders.append(('Set-Cookie', url_encode(self.cookies)))
    
        if 'Sdarot' in self.cookies:

          self.headers['Cookie']='Sdarot={0}'.format((self.cookies.get('Sdarot')))
        elif 'Sratim' in self.cookies:
            self.headers['Cookie']='Sratim={0}'.format((self.cookies.get('Sratim')))
            log.warning(self.cookies)
            log.warning(self.headers['Cookie'])
        request = url_r.Request(self.url.replace(' ','%20'),  headers=self.headers,data=url_encode(self.data).encode("utf-8"))
        log.warning('self.url:'+str(self.url))
        request.get_method = lambda: 'GET'
        html = opener.open(request).read()
        
        cookie_new={}
        for cook in cookjar:
          cookie_new[cook.name]=cook.value
        return html,cookie_new

    def post(self):
        try:
            import cookielib
        except:
            import http.cookiejar
            cookielib = http.cookiejar
        
        if Addon.getSetting('dns_solver')=='1':
            new_ip=cache.get(self.get_ip,24, table='cookies')
            
            
            
            
            self.url=self.url.replace(API,'https://'+new_ip)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        handlers = [MyHTTPHandler,MyHTTPSHandler]
        cookjar = cookielib.CookieJar()
        handlers += [url_r.HTTPHandler(), url_r.HTTPSHandler(), url_r.HTTPCookieProcessor(cookjar)]
        if Addon.getSetting('dns_solver')=='1':
            handlers = [url_r.HTTPHandler(), url_r.HTTPSHandler(context=ctx), url_r.HTTPCookieProcessor(cookjar)]
        opener = url_r.build_opener(*handlers)
        #opener.addheaders.append(('Set-Cookie', url_encode(self.cookies)))

        
        if 'Sdarot' in self.cookies:

          self.headers['Cookie']='Sdarot={0}'.format((self.cookies.get('Sdarot')))

        request = url_r.Request(self.url,  headers=self.headers,data=url_encode(self.data).encode("utf-8"))

        request.get_method = lambda: 'POST'
      

        html = opener.open(request).read()
        cookie_new={}
        for cook in cookjar:
          cookie_new[cook.name]=cook.value
        return html,cookie_new
    def image(self):
        try:
            import cookielib
        except:
            import http.cookiejar
            cookielib = http.cookiejar
        

        handlers = [MyHTTPHandler,MyHTTPSHandler]
        cookjar = cookielib.CookieJar()
        handlers += [url_r.HTTPHandler(), url_r.HTTPSHandler(), url_r.HTTPCookieProcessor(cookjar)]
        
        opener = url_r.build_opener(*handlers)
        #opener.addheaders.append(('Set-Cookie', url_encode(self.cookies)))

        
        if 'Sdarot' in self.cookies:

          self.headers['Cookie']='Sdarot={0}'.format((self.cookies.get('Sdarot')))

        request = url_r.Request(self.url,  headers=self.headers,data=url_encode(self.data))

        request.get_method = lambda: 'POST'
      

        html = opener.open(request)
        localFile = open('desktop.jpg', 'wb')
        localFile.write(html.read())
        localFile.close()
    
    
def get_user_cookie_sratim(cookie_pre=''):
    username = Addon.getSetting('username')
    password = Addon.getSetting('Password_sdr')
    
    if username and password:

        data = {
            'username': username,
            'password': password
        }
        
        #req = requests.post(API + '/login', data=data, headers=HEADERS)
        req,cookie_new=resolve_dns('http://api.sratim.tv/user/login', data=data, headers=HEADERS).post()
        
        res = json.loads(req)
        
        if 'errors' in res:
            #if res['success']==False:
                
            #    xbmc.executebuiltin(u'Notification(%s,%s)' % ('Sdarot', ' Sratim.TV'+ ', '.join(res['errors'])))
            return cookie_pre
            
        if res['success']:
            
            return cookie_new

        else:
            #xbmcgui.Dialog().ok('בדוק שם משתמש וסיסמא של סדרות טיוי', ', '.join(res['errors']).encode('utf-8'))
            
            if u'\u05d0\u05ea\u05d4 \u05db\u05d1\u05e8 \u05de\u05d7\u05d5\u05d1\u05e8 \u05dc\u05de\u05e2\u05e8\u05db\u05ea!' in res['errors']:
                
                
                return {}
            
            #Addon.setSetting('password', '')
    #else:
    #    xbmcgui.Dialog().ok('שגיאה', 'בדוק שם משתמש וסיסמא של סדרות טיוי')
    return {}
def get_user_cookie(cookie_pre=''):
    username = Addon.getSetting('username')
    password = Addon.getSetting('Password_sdr')
    
    if username and password:

        data = {
            'username': username,
            'password': password
        }
        
        #req = requests.post(API + '/login', data=data, headers=HEADERS)
        req,cookie_new=resolve_dns(API + '/user/login', data=data, headers=HEADERS).post()
        
        res = json.loads(req)
        
        if 'errors' in res:
            if res['success']==False:
              if KODI_VERSION<=18:
                c_str='כבר מחובר'.decode('utf-8')
              else:
                c_str='כבר מחובר'
              
              if c_str not in ', '.join(res['errors']):
                xbmc.executebuiltin(u'Notification(%s,%s)' % ('Mando', ' SDAROT.TV'+ ', '.join(res['errors'])))
            return cookie_pre
            
        if res['success']:
            
            return cookie_new

        else:
            #xbmcgui.Dialog().ok('בדוק שם משתמש וסיסמא של סדרות טיוי', ', '.join(res['errors']).encode('utf-8'))
            
            if u'\u05d0\u05ea\u05d4 \u05db\u05d1\u05e8 \u05de\u05d7\u05d5\u05d1\u05e8 \u05dc\u05de\u05e2\u05e8\u05db\u05ea!' in res['errors']:
                
                
                return {}
            
            #Addon.setSetting('password', '')
    #else:
    #    xbmcgui.Dialog().ok('שגיאה', 'בדוק שם משתמש וסיסמא של סדרות טיוי')
    return {}
def get_ip_url(url):
    base = urlparse.urlparse(url)
    #watch = cache_ip(url)
    watch=cache.get(get_ip,24,url, table='cookies')
    return url.replace(base.netloc, watch)
def build_final_url(url, cookie):

    try:
        f_k=que_n(cookie.get('Sdarot'), safe='')
        return 'http:{0}|Cookie=Sdarot={1}&User-Agent={2}'.format(get_ip_url(url), f_k, HEADERS.get('User-agent'))
    except:
        f_k=que_n(HEADERS.get('Cookie'), safe='')
        return 'http:{0}|Cookie={1}&User-Agent={2}'.format(get_ip_url(url), f_k, HEADERS.get('User-agent'))
    
def get_final_video_and_cookie(sid, season, episode, choose_quality=False, download=False):
    token,cookie=cache.get(get_sdarot_ck,0,sid,season,episode, table='cookies')

    log.warning('Donor test:'+token)
    if token == 'donor':
        vid = get_video_url(sid, season, episode, token, cookie, choose_quality)

    else:
        if download:
            #plugin.notify('התחבר כמנוי כדי להוריד פרק זה', image=ICON)
            return None, None
        else:
            vid = get_video_url(sid, season, episode, token, cookie, choose_quality)
            log.warning(vid)
            if 'errors' in vid:
                msg=vid['errors'][0]
            else:
                msg="אנא המתן 30 שניות"
            if 1:
                dp = xbmcgui.DialogProgress()
                dp.create("לצפייה באיכות HD וללא המתנה ניתן לרכוש מנוי", msg+'\n'+ ''+'\n'+
                          "[COLOR orange][B]לרכישת מנוי להיכנס בדפדפן - www.sdarot.tv/donate[/B][/COLOR]")
                dp.update(0)
            
            tm=30
   
            if not 'errors' in vid:
             tm=0
             return vid, cookie
            else:
              tm=re.findall(r' \d+ ', vid['errors'][0])
              tm=int (tm[0].strip())
            if tm>28:
              
              token,cookie=cache.get(get_sdarot_ck,0,sid,season,episode, table='cookies')
            
            
            
            

            for s in range(tm, -1, -1):
                time.sleep(1)
                if 1:
                    dp.update(int((tm - s) / (tm+1) * 100.0), msg+'\n'+ 'עוד {0} שניות'.format(s)+'\n'+ "[COLOR orange][B]לרכישת מנוי להיכנס בדפדפן - www.sdarot.tv/donate[/B][/COLOR]")
                    if dp.iscanceled():
                        dp.close()
                        return None, None
                

        vid = get_video_url(sid, season, episode, token, cookie, choose_quality)
        
    if vid:
            return vid, cookie
def get_video_url(sid, season, episode, token, cookie, choose_quality):

    #req = requests.post(API + '/episode/watch/sid/{0}/se/{1}/ep/{2}'.format(sid, season, episode),
    #                    data={'token': token}, cookies=cookie, headers=HEADERS).json()
    req,cookie_new=resolve_dns(API + '/episode/watch/sid/{0}/se/{1}/ep/{2}'.format(sid, season, episode),
                        data={'token': token}, cookies=cookie, headers=HEADERS).post()
    req=json.loads(req)
    if req['success']:
        qualities = req['watch']
        if choose_quality:
            return qualities
        else:
            qualities_list = qualities.keys()
            log.warning('qualities_list:')
            log.warning(qualities_list)
            max_quality = int(Addon.getSetting('max_quality'))
            quality = '480'

            if max_quality >= 720:
                quality = '1080' if '1080' in qualities_list and max_quality == 1080 else '720'
                if quality == '720' and '720' not in qualities_list:
                    quality = '480'
            log.warning(qualities[quality])
            return build_final_url(qualities[quality], cookie)
    
    return req
def get_sdarot_ck(sid,season,episode,cookie={}):
            #cookie=cache.get(get_user_cookie,1, table='user_cookies')
            
            cookie = get_user_cookie()
       
       
            d={'SID': sid, 'season': season, 'episode': episode}
            req,cookie_new=resolve_dns(API + '/episode/preWatch', data={'SID': sid, 'season': season, 'episode': episode},
                                cookies=cookie, headers=HEADERS).post()
     
            
            #req = requests.post(API + '/episode/preWatch', data={'SID': sid, 'season': season, 'episode': episode},
            #                    cookies=cookie, headers=HEADERS)
            #token = req.text
            
            token=(req).decode('utf-8')
          
            if not cookie:
              cookie = cookie_new
            return token,cookie
def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
            
            global global_var,stop_all,progress
            progress='Start'
            f_links='NO LINK'
            tmdbKey='653bb8af90162bd98fc7ee32bcbbfb3d'
            if tv_movie=='tv':
          
               url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&append_to_response=external_ids&language=he'%(id,tmdbKey)
               n_value='name'
            else:
               
               url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&append_to_response=external_ids&language=he'%(id,tmdbKey)
               n_value='title'
            
            try:
                
                name=get_html(url2,timeout=10).json()[n_value]
            except:
                name=original_title
       
            start_time=time.time()
            da=[]
            sd_link=''
            da.append((tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))

            progress='Requests'
            if KODI_VERSION<=18:
                
                req,cookie_new=resolve_dns(API + '/series/search/{0}/page/{1}/perPage/100'.format(que(name.replace('%','%25').encode('utf-8')), '0')).get()
             
            else:
                req,cookie_new=resolve_dns(API + '/series/search/{0}/page/{1}/perPage/100'.format(que(name.replace('%','%25')), '0')).get()
            
            '''
            s = requests.Session()
            req = requests.Request(method='GET', url=API, headers=HEADERS)
            prep = req.prepare()
            prep.url = API + '/series/search/{0}/page/{1}/perPage/100'.format(name, '1')
            
            req = s.send(prep)
            '''
            
            all_links=[]
            results = json.loads(req)['series']

            if not results:
                progress='Requests2'
                req,cookie_new=resolve_dns(API + '/series/search/{0}/page/{1}/perPage/100'.format(original_title, '0')).get()
               
                results = json.loads(req)['series']
           
            if results:
                
                items = []
                for s in results:
                    progress='Requests3'
                    req ,cookie_new= resolve_dns(API + '/series/info/{0}'.format(s['id']), headers=HEADERS).get()
                    req=json.loads(req)
     
                    #req = requests.get(API + '/series/info/{0}'.format(s['id']), headers=HEADERS).json()
                    serie = req['serie']
                    ep_found=0
                    se_found=0
                    episodes = serie['episodes']
                    
                    if episodes!=None:
                        for sen in episodes:
                          
                          if sen==season:
                            se_found=1
                        
                        if se_found==1:
                           
                            if (len(episodes)>=int(season)):
                              for items_in in episodes[season]:
                                ep=items_in['episode']
                         
                                if episode==ep:
                                  ep_found=1
                                  break
                           
                            if ep_found==1:
                                sd_link=json.dumps((s['id'], season, episode))
                                #f_links=get_final_video_and_cookie(s['id'], season, episode, False, False)
                                if not episodes:
                                    return []
                                break
                                
                                #all_links.append((s['heb'],sd_link,'Sdarot','480'))
                                #links_sdarot=all_links
            progress='Token'
            x=0
            tick_x=0
            
            token,cookie=cache.get(get_sdarot_ck,0,s['id'],(season),(episode), table='cookies')
            progress='Done Token'
            
  
            if token == 'donor':
                res='1080'
            else:
                res='480'
            if sd_link!='':
                all_links.append((original_title+'.S%sE%s'%(season_n,episode_n),'Direct_link$$$'+sd_link,'0',res))
                
                global_var=all_links
                elapsed_time = time.time() - start_time
                progress=' Done '+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                while x<10:
                    if tick_x==0:
                        progress='Done'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                        tick_x=1
                    else:
                        progress='Done_'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                        tick_x=0
                    x+=1
                    time.sleep(0.1)
                
            #get_sdarot_ck(s['id'],(season),(episode))
            
            
            return all_links
            