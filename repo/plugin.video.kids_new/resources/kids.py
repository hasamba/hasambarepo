# -*- coding: utf-8 -*-
import xbmcaddon,os,xbmc,xbmcgui,urllib,re,xbmcplugin,sys,logging,json,time,threading
from resources.modules import cache
from resources.modules import log
from urllib.parse import parse_qsl
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
__addon__ = xbmcaddon.Addon()

    

Addon = xbmcaddon.Addon()
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
if KODI_VERSION<=18:#kodi18
    if Addon.getSetting('debug')=='false':
        reload (sys )#line:61
        sys .setdefaultencoding ('utf8')#line:62
else:#kodi19
    import importlib
    importlib.reload (sys )#line:61
    import xbmcvfs
    xbmc_tranlate_path=xbmcvfs.translatePath
    
user_dataDir = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)
user_dataDir_img=os.path.join(user_dataDir,'images')
if not os.path.exists(user_dataDir_img):
    os.makedirs(user_dataDir_img)
from resources.modules.addall import addLink,addDir3,addNolink
global sys_arg_1_data
sys_arg_1_data=""
if KODI_VERSION<=18:
    que=urllib.quote_plus
    url_encode=urllib.urlencode
else:
    que=urllib.parse.quote_plus
    url_encode=urllib.parse.urlencode
if KODI_VERSION<=18:
    unque=urllib.unquote_plus
else:
    unque=urllib.parse.unquote_plus
if KODI_VERSION>18:
    
    class Thread (threading.Thread):
       def __init__(self, target, *args):
        super().__init__(target=target, args=args)
       def run(self, *args):
          
          self._target(*self._args)
          return 0
else:
   
    class Thread(threading.Thread):
        def __init__(self, target, *args):
           
            self._target = target
            self._args = args
            
            
            threading.Thread.__init__(self)
            
        def run(self):
            
            self._target(*self._args)
        
def replaceHTMLCodes(txt):
    try:
        import HTMLParser
        html_parser = HTMLParser.HTMLParser()
       
    except:
        import html as html_parser
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = html_parser.unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    txt = txt.replace("&#8211", "-")
    txt = txt.replace("&#8217", "'")
    txt = txt.strip()
    return txt
def get_params(user_params=''):
        
        
        param = dict(parse_qsl(user_params.replace('?','')))
        return param     


def read_site_html(url_link):
    import requests

    html=requests.get(url_link)
    return html
#def get_amount():
    
def main_menu():
    
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    match=[('0')]
    match_tv=[('0')]
    try:
        dbcur.execute("SELECT * FROM updated where type='movies'")
        match = dbcur.fetchall()
        
        dbcur.execute("SELECT * FROM updated where type='tv'")
        match_tv = dbcur.fetchall()
    
    except:
        pass
    if len(match)==0:
        match=[('0')]
    if len(match_tv)==0:
        match_tv=[('0')]
   
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""con1 TEXT,""origin TEXT,""icon TEXT, ""image TEXT,""plot TEXT,""data TEXT);"% 'kids_movie')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""url TEXT,""video_info TEXT,""id TEXT,""icon TEXT,""fan TEXT,""free TEXT);"%'watched' )
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""con1 TEXT,""origin TEXT,""icon TEXT, ""image TEXT,""plot TEXT,""data TEXT);"% 'newones')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT, ""image TEXT,""plot TEXT,""origin TEXT);"% 'kids_show')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT, ""image TEXT,""plot TEXT,""data TEXT,""tmdbid TEXT,""date_added TEXT);"% 'kids_movie_ordered')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT,""fanart TEXT,""plot TEXT,""video_data TEXT);"% 'kids_show_orginized')
    
    dbcon.commit()
    dbcur.execute("SELECT * FROM kids_movie_ordered")

    match2 = dbcur.fetchall()
    dbcur.execute("SELECT * FROM watched ")
    match3 = dbcur.fetchall()
    all_names=[]
    count_m=0
    
    for name1,link,con1,origin,icon,image,plot,data in match2:
        if name1 not in all_names:
            all_names.append(name1)
            count_m+=1
    dbcur.execute("SELECT * FROM kids_show_orginized ")
    
    match2 = dbcur.fetchall()
    all_names=[]
    count_tv=0
    
    for name1,link,icon,image,plot,origin in match2:
        if name1 not in all_names:
            all_names.append(name1)
            count_tv+=1
    
    all_d=[]
    all_firebase=match3
    if len(Addon.getSetting("firebase"))>0:
        all_firebase=read_firebase('last_played_movie')
    
    #all_d.append(addDir3('סרטים אחרונים','0',59,'https://www.flatpanelshd.com/pictures/despicableme2-1l.jpg','http://4k.com/wp-content/uploads/2014/11/toystory3_img10_720-790x442.jpg','סרטים מדובבים',generes=match[0][0]))
    all_d.append(addDir3('(%s) סרטים מדובבים עמודים'%str(count_m),'0',10,'https://www.flatpanelshd.com/pictures/despicableme2-1l.jpg','http://4k.com/wp-content/uploads/2014/11/toystory3_img10_720-790x442.jpg','סרטים מדובבים',generes=match[0][0]))
    all_d.append(addDir3('(%s) סרטים מדובבים שנים'%str(count_m),'0',10,'https://www.flatpanelshd.com/pictures/despicableme2-1l.jpg','http://4k.com/wp-content/uploads/2014/11/toystory3_img10_720-790x442.jpg','לפי שנים',generes=match[0][0]))
    all_d.append(addDir3('(%s) סרטים מדובבים לפי א-ב'%str(count_m),'0',11,'https://www.flatpanelshd.com/pictures/despicableme2-1l.jpg','http://4k.com/wp-content/uploads/2014/11/toystory3_img10_720-790x442.jpg','סרטים מדובבים',generes=match[0][0]))
    all_d.append(addDir3('[COLOR lightblue](%s) סרטים שנצפו[/COLOR]'%str(len(all_firebase)),'0',10,'https://icons.iconarchive.com/icons/sirubico/movie-genre/256/Children-icon.png','https://i.ytimg.com/vi/9FQgg_h_lcQ/maxresdefault.jpg','נצפו'))
    
    
    
    
    #all_d.append(addDir3('(%s) סדרות'%str(count_tv),'www',2,'https://travelmamas.com/wp-content/uploads/2017/10/best_travel_movies_for_kids_frozen-837x1200.jpg','https://www.slashfilm.com/wp/wp-content/images/Astro-Boy.jpg','ילדים',generes=match_tv[0][0]))
    
    
    all_d.append(addLink( '[COLOR yellow][I]הגרל לי סרט[/I][/COLOR]',  'www',17,False,'https://icons.iconarchive.com/icons/softskin/series-folder/256/Folder-TV-Disney-icon.png','https://media.timeout.com/images/105360571/image.jpg','הגרל לי סרט'))
    
    
    all_d.append(addDir3('קדימונים לילדים','www',4,'https://imagesvc.timeincapp.com/v3/mm/image?url=https%3A%2F%2Fewedit.files.wordpress.com%2F2017%2F11%2Fanimationsplit.jpg%3Fw%3D2000&w=700&q=85','https://cdn1.thr.com/sites/default/files/imagecache/list_landscape_960x541/2017/08/coco_ferdinand_the_star_lego_ninjago_my_little_pony_-_split_-_publicity_-_h_2017_1.jpg','טרליירים'))
    all_d.append(addDir3('ערוצי YOUTUBE','www',52,'https://play-lh.googleusercontent.com/lMoItBgdPPVDJsNOVtP26EKHePkwBg-PkuY9NOrc-fumRtTFP4XhpUNk_22syN4Datc','https://play-lh.googleusercontent.com/96nxQxbB8Ug-vZjAk-3FSs6JN68iJ3JYQBpmJeA8wt9vnt6wUoxZBj61dWObvTH1DbI_','YOUTUBE'))
    all_d.append(addDir3('קטנטנים','www',54,'https://yt3.ggpht.com/a/AATXAJwz0u6V3D-IQ--LWl20eJqHEsD59-Sjzjh-jg=s900-c-k-c0xffffffff-no-rj-mo','https://i.pinimg.com/736x/40/8f/bb/408fbbbcff4fb06e395735425f17c364--little-babies-baby-kids.jpg','YOUTUBE'))
    

    
    
    
    
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""url TEXT,""video_info TEXT,""id TEXT,""icon TEXT,""fan TEXT,""free TEXT);"%'last_played_movie' )
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""url TEXT,""video_info TEXT,""id TEXT,""icon TEXT,""fan TEXT,""free TEXT);"%'last_played_tv' )
   
    dbcur.execute("SELECT * FROM last_played_movie")
    match = dbcur.fetchall()
    
    for name ,url ,video_info ,id ,icon ,fan ,free in match:
        all_d.append(addLink(name.replace('%27',"'"),url,5,False,icon,fan,free.replace('%27',"'"),video_info=unque(video_info),id=id))
    
    all_d.append(addDir3('חפש','www',49,'https://4tup.files.wordpress.com/2010/06/child-movie-theatre-860.jpg','https://media.timeout.com/images/105586169/image.jpg','חפש'))
    xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_d,len(all_d))
    
    addNolink( '[COLOR yellow][I]עדכן סרטים[/I][/COLOR]', 'movie',6,False, iconimage="https://i.ytimg.com/vi/6sRi1FvWe1Q/maxresdefault.jpg",fan='https://i.ytimg.com/vi/DZj9lWmqbus/hqdefault.jpg',sys_arg_1_data=sys_arg_1_data)
    
    
    addNolink( '[COLOR yellow][I]עדכן ספריה[/I][/COLOR]', 'tv',58,False, iconimage="https://i.ytimg.com/vi/6sRi1FvWe1Q/maxresdefault.jpg",fan='https://i.ytimg.com/vi/DZj9lWmqbus/hqdefault.jpg',sys_arg_1_data=sys_arg_1_data)
    
    dbcur.close()
    dbcon.close()
    
def ClearCache():
  
    
    cache.clear(['cookies', 'pages','posters'])
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kids', 'Cleared')))
def get_sdarot(url):
       from sdarot import MyResolver
       url_data=json.loads(url)

       url, cookie=get_final_video_and_cookie(url_data[0], url_data[1], url_data[2], False, False)
       '''
       regex='https://(.+?)/'
       match=re.compile(regex).findall(url)
       h=(MyResolver(match[0]))
       url=url.replace(match[0],h)
       '''
       return url
def get_final_video_and_cookie(sid, season, episode, choose_quality=False, download=False):
    from resources.modules.sdarot import get_sdarot_ck,get_sdarot_ck,get_video_url
    local=False
    #get_sdarot_ck(sid,season,episode)
    token,cookie=cache.get(get_sdarot_ck,3,sid,season,episode, table='cookies')

    
    #cookie={'Sdarot':'FOcYpGHLb'}
    if cookie=={} or token == 'donor':
       
        token,cookie=cache.get(get_sdarot_ck,0,sid,season,episode,cookie, table='cookies')
       
    else:
        vid = get_video_url(sid, season, episode, token, cookie, choose_quality)
        if 'errors' not in vid:
             return vid, cookie
        else:
            if KODI_VERSION<19:
                xbmc.executebuiltin((u'Notification(%s,%s)' % ('Victory', vid['errors'][0])).encode('utf-8'))
            else:
                xbmc.executebuiltin((u'Notification(%s,%s)' % ('Victory', vid['errors'][0])))
        if 'uid=|Co' in vid:
           
            token,cookie=cache.get(get_sdarot_ck,0,sid,season,episode, table='cookies')
          
        else:
           
 
           
           if 'errors' not in vid:
             return vid, cookie
    if token == 'donor':
        vid = get_video_url(sid, season, episode, token, cookie, choose_quality)

    else:
        if download:
            #plugin.notify('התחבר כמנוי כדי להוריד פרק זה', image=ICON)
            return None, None
        else:
            vid = get_video_url(sid, season, episode, token, cookie, choose_quality)
            if 'errors' in vid:
                msg="אנא המתן 30 שניות"#vid['errors'][0]
            else:
                msg="אנא המתן 30 שניות"
            if not local:
                
                dp = xbmcgui.DialogProgress()
                if KODI_VERSION<19:
                    dp.create("לצפייה באיכות HD וללא המתנה ניתן לרכוש מנוי", msg, vid['errors'][0],
                          "[COLOR orange][B]לרכישת מנוי להיכנס בדפדפן - www.sdarot.tv/donate[/B][/COLOR]")
                    
                else:
                    dp.create("לצפייה באיכות HD וללא המתנה ניתן לרכוש מנוי", msg+'\n'+ ''+'\n'+
                          "[COLOR orange][B]לרכישת מנוי להיכנס בדפדפן - www.sdarot.tv/donate[/B][/COLOR]")
                
                
                dp.update(0)
            tm=31
   
            if not 'errors' in vid:
             tm=0
         
             return vid, cookie
            else:
                
                tm=re.findall(r' \d+ ', vid['errors'][0])
                if len(tm)==0:
                    
                        xbmcgui.Dialog().ok('Sdaror TV',vid['errors'][0])
                        sys.exit()
                tm=int (tm[0].strip())
                if tm>28:
                    token,cookie=cache.get(get_sdarot_ck,0,sid,season,episode, table='cookies')
                    tm=30
            
            
            
            

            for s in range(tm, -1, -1):
                time.sleep(1)
                if  local:
                    sys.stdout.write("\r עוד {0} שניות".format(s))
                    sys.stdout.flush()
                else:
                    if KODI_VERSION<19:
                        dp.update(int((tm - s) / (tm+1) * 100.0), msg, 'עוד {0} שניות'.format(s), '')
                    else:
                        dp.update(int((tm - s) / (tm+1) * 100.0), msg+'\n'+ 'עוד {0} שניות'.format(s)+'\n'+ "[COLOR orange][B]לרכישת מנוי להיכנס בדפדפן - www.sdarot.tv/donate[/B][/COLOR]")
                    
                    if dp.iscanceled():
                        dp.close()
                        return None, None
        

        
        vid = get_video_url(sid, season, episode, token, cookie, choose_quality)
        
        if 'errors' in vid:
                    xbmcgui.Dialog().ok('Sdaror TV',vid['errors'][0])
                    sys.exit()
    if vid:
           
            return vid, cookie
def load_resolveurl_libs():
    path=xbmc_tranlate_path('special://home/addons/script.module.resolveurl/lib')
    sys.path.append( path)
    path=xbmc_tranlate_path('special://home/addons/script.module.six/lib')
    sys.path.append( path)
    path=xbmc_tranlate_path('special://home/addons/script.module.kodi-six/libs')
    sys.path.append( path)
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

def resolve_link(url,id,plot,name1):
    import requests
    if 'drive.google.com' in url:
        o_url=url
        load_resolveurl_libs()
        import resolveurl
        url =resolveurl .HostedMediaFile (url =url ).resolve ()#line:2687
        if not url:
            from resources.modules.google_solve import googledrive_resolve
            url,q=googledrive_resolve(o_url)
        
        
        
        
    if 'tv4kids' in url:
        url=unque(url).replace('t1dxi9ex4ypp.cdn.shift8web.com','tv4kids.tk').replace('[[OS]]','')
        
        headers = {
            'authority': 'tv4kids.tk',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            
        }

        response = requests.get(url, headers=headers,stream=True).url
        


        headers = {
            'authority': 'tv4kids.tk',
            'accept-encoding': 'identity;q=1, *;q=0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'no-cors',
            'referer':url.replace('[[OS]]',''),
            'accept-language': 'en-US,en;q=0.9',
           
        }
        
        head=url_encode(headers)
        url=url+"|"+head
        url=response
        
    if 'videopress.com' in url:
        url=unque(url).replace('[[OS]]','')
        ids=url.split('?')[0].split('/')
        id=ids[len(ids)-1]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://videopress.com/',
            'content-type': 'application/json',
            'Origin': 'https://videopress.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers',
        }

        response = requests.get('https://public-api.wordpress.com/rest/v1.1/videos/'+id, headers=headers).json()
        l_link=''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            
            'Origin': 'https://videopress.com',
            'Connection': 'keep-alive',
            'Referer': 'https://videopress.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers',
        }
        
        for items in response['files']:
            file_lk=response['files'][items]
            if 'mp4' in file_lk and 'hls' not in file_lk:
                l_link='https://videos.files.wordpress.com/%s/%s'%(id,file_lk['mp4'])
        url=l_link
        head=url_encode(headers)
        url=url+"|"+head
        
    if '%%%' in url:
        regex='\[\[(.+?)\]\]'
        match2=re.compile(regex).findall(url)
        if len(match2)>0:
           
            url=url.replace(match2[0],'').replace('[','').replace(']','').strip()
        url=url.split('%%%')[0]
        url_id=url
        if KODI_VERSION<19:
            url='plugin://plugin.video.telemedia/?url=%s&no_subs=%s&season=%s&episode=%s&mode=40&original_title=%s&id=%s&data=&fanart=&url=%s&iconimage=&file_name=%s&description=%s&resume=%s&name=%s&heb_name=%s'%(url_id,'1','%20','%20',name1.decode('utf-8','ignore').encode("utf-8"),id,url_id,name1.decode('utf-8','ignore').encode("utf-8"),plot,'',name1,name1)
        else:
            url='plugin://plugin.video.telemedia/?url=%s&no_subs=%s&season=%s&episode=%s&mode=40&original_title=%s&id=%s&data=&fanart=&url=%s&iconimage=&file_name=%s&description=%s&resume=%s&name=%s&heb_name=%s'%(url_id,'1','%20','%20',que(name1),id,url_id,que(name1),que(plot),'',que(name1),que(name1))
    if '[' in url and 'http' not in url:
       from resources.modules.sdarot import MyResolver
       url_data=json.loads(url)
       url, cookie=get_final_video_and_cookie(url_data[0], url_data[1], url_data[2], False, False)
    if 'f2h' in url:
        url=url.replace('nana10.co.il','io')
        headers = {
        'Pragma': 'no-cache',
        
        'Accept-Encoding': 'utf8',

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',


        
        }
        html=requests.get(url,headers=headers).content
        
        regex='<script.+?"(.+?)/ip.php'
        match=re.compile(regex).findall(html)

        for links in match:
         
         if 'f2h.co.il' in links:
           id=links

        regex2="<form name='myform' id='myform' method='post' action='.+?/thanks/(.+?)'"
        match2=re.compile(regex2).findall(html)

        url=id+'/files/'+match2[0].replace("|","%7C")
    if 'www.youtube.com' in url :
        vid=re.compile('\?(?:v|id)=(.+?)(?:$|&)').findall(url)[0]
        url='plugin://plugin.video.youtube/play/?video_id='+vid
    if 'dood.to' in url:
        
        headers = {
            'authority': 'dood.to',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'iframe',
            'referer': url,
            'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
           }
        url=url.replace('/d/','/e/')
        x=requests.get(url,headers=headers).content
        regex="'/pass_md5/(.+?)'"

        m=re.compile(regex,re.DOTALL).findall(x)
        x=requests.get('https://dood.to/pass_md5/'+m[0],headers=headers).content
        
        tokens=m[0].split('/')
        token=tokens[len(tokens)-1]
        expiry=int(time.time()*1000)
        
        a='?token=5trtb3h06c50mgjd5yih06se&expiry=1596976834003'
        a='S4w8nJVnR1?token=%s&expiry=%s'%(token,expiry)
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^88^\\^, ^\\^Google',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Dest': 'video',
            'Referer': url,
            'Accept-Language': 'en-US,en;q=0.9',
           
        }


        headers2 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
            'Accept-Language': 'en-US,en;q=0.5',
           
            'Connection': 'keep-alive',
            'Referer': url,
        }
        url= x+a+"|"+ url_encode(headers)
    return url
def read_firebase_c(table_name):
    

    from resources.modules.firebase import firebase
    log.warning('https://%s.firebaseio.com'%Addon.getSetting("firebase"))
    firebase = firebase.FirebaseApplication('https://%s.firebaseio.com'%Addon.getSetting("firebase"), None)
   
    result = firebase.get('/', None)
   
    if table_name in result:
        return result[table_name]
    else:
        return {}
def read_firebase(table_name,no_cache=False):
    if no_cache:
        result=read_firebase_c(table_name)
    else:
        result=cache.get(read_firebase_c,24,table_name, table='cookies')
    return result
def write_firebase(name,url,video_info,id,icon,fan,plot,table_name,seek_time,total_time):
    from resources.modules.firebase import firebase
    fb_app = firebase.FirebaseApplication('https://%s.firebaseio.com'%Addon.getSetting("firebase"), None)

    if KODI_VERSION<19:
        result = fb_app.post(table_name, {'name':name,'url':url,'video_info':video_info,'id':id,'icon':icon,'fan':fan,'plot':plot,'seek_time':seek_time,'total_time':total_time})
    else:
        d={'name':name,'url':url,'video_info':video_info,'id':id,'icon':icon,'fan':fan,'plot':plot,'seek_time':seek_time,'total_time':total_time}
        result = fb_app.post(table_name, {'name':name,'url':url,'video_info':video_info,'id':id,'icon':str(icon),'fan':str(fan),'plot':plot,'seek_time':seek_time,'total_time':total_time})
    return 'OK'
def delete_firebase(table_name,record):
    from resources.modules.firebase import firebase
    fb_app = firebase.FirebaseApplication('https://%s.firebaseio.com'%Addon.getSetting("firebase"), None)
    result = fb_app.delete(table_name, record)
    return 'OK'
def jump_seek(name,url,video_info,id,icon,fan,plot,table_name):
    global break_jump
    break_jump=1
    timeout=0
    while timeout<200:
        timeout+=1
        if break_jump==0:
            break
        if xbmc.Player().isPlaying():
            break
        xbmc.sleep(100)
    mark_once=0
    counter_stop=0
    g_timer=0
    while xbmc.Player().isPlaying():
        
        if break_jump==0:
            break
        try:
        
            vidtime = xbmc.Player().getTime()
        except Exception as e:
            vidtime=0
            pass
        
        if vidtime>0.2:
            try:
               g_timer=xbmc.Player().getTime()
               
                
                
               g_item_total_time=xbmc.Player().getTotalTime()
               time_left=xbmc.Player().getTotalTime()-xbmc.Player().getTime()
               
            except:
                pass
        xbmc.sleep(100)
    all_record=read_firebase(table_name+'_seek_time',no_cache=True)

    video_info=json.loads(unque(video_info))
    if table_name=='last_played_tv':
        f_name=video_info['original_title']+name
    else:
        f_name=video_info['title']
    for itt in all_record:
        
        if 'name' not in all_record[itt]:
            continue
        
        if all_record[itt]['name']==f_name:
                delete_firebase(table_name+'_seek_time',itt)
        
    if g_timer>30:
        if len(Addon.getSetting("firebase"))>0 and 'youtube' not in url:
            write_firebase(f_name,url,video_info,id,icon,fan,plot,table_name+'_seek_time',str(g_timer),str(g_item_total_time))
def get_youtube5(url):
    import json,requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://en.y2mate.guru',
        'Connection': 'keep-alive',
        'Referer': 'https://en.y2mate.guru/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers',
    }

    data = {'url':url}
    

    response = requests.post('https://api.y2mate.guru/api/convert', headers=headers, json=data).json()
    max_q=0
    final_url=''
    for items in response['url']:
        if items['no_audio']==False and items['name']=='MP4':
            if int(items['quality'])>max_q:
                final_url=items['url']
    return final_url
    
def play_link(name,url,video_info,id,icon,fan,plot):
    icon=str(icon)
    fan=str(fan)
    log.warning(url)
    #if 'הבולשת' in plot:
    #    url='https://www.youtube.com/watch?v=pz-X_5s1Ak0'
    url=url.replace('https://drive.google.com/open?id=','https://drive.google.com/file/d/')
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    
    if 'tv_title' in video_info:
        table_name='last_played_tv'
    else:
        table_name='last_played_movie'
    if len(Addon.getSetting("firebase"))>0 and 'youtube' not in url:
        all_firebase=read_firebase(table_name,no_cache=True)
        write_fire=True
        for items in all_firebase:
            if 'name' not in all_firebase[items]:
                continue
            
            if all_firebase[items]['name']==name:
                delete_firebase(table_name,items)
                #write_fire=False
                break
        if write_fire:
            write_firebase(name,url,que(video_info),id,icon,fan,plot,table_name,'0','0')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""url TEXT,""video_info TEXT,""id TEXT,""icon TEXT,""fan TEXT,""free TEXT);"%table_name )
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""url TEXT,""video_info TEXT,""id TEXT,""icon TEXT,""fan TEXT,""free TEXT);"%'watched' )
    
    dbcur.execute("DELETE FROM "+table_name)
    dbcur.execute("INSERT INTO %s Values ('%s','%s','%s','%s','%s','%s','%s')"%(table_name,name.replace("'","%27"),que(url),que(video_info),id,icon,fan,plot.replace("'","%27")))
    
    
    dbcur.execute("SELECT * FROM watched ")
    all_w=[]
    match = dbcur.fetchall()
    all_nw=[]
    for name_w ,link_w,data_w,tmdbid_w,icon_w, image_w,free_w in match:
        all_nw.append(name_w)
    if name.replace("'","%27") not in all_nw and name not in all_nw:
        dbcur.execute("INSERT INTO watched Values ('%s','%s','%s','%s','%s','%s','%s')"%(name.replace("'","%27"),que(url),que(video_info),id,icon,fan,plot.replace("'","%27")))
    
    dbcon.commit()
    dbcur.close()
    dbcon.close()
    try:
        all_data=json.loads(video_info)
    except:
        all_data={}
        all_data['title']=name
        all_data['plot']=plot
    all_f_name=[]
    if '$$$' in url:
       links=url.split('$$$')
       sour_pre=''
       sour=''
       all_s=[]
       for lk in links:
           f_name=''
           regex='\[\[(.+?)\]\]'
           match=re.compile(regex).findall(str(lk))
           if len(match)==0:
               if 'TEME' in lk:
                 ff_link=lk
                 f_name=lk.split('%%%')[1].split('_')[1]
                 
                 ff_link=fn.replace(match2[0],'').replace('[','').replace(']','')
                 match=[('TE',f_name)]
               else:
                    regex='//(.+?)/'
                     
                    match_ser=re.compile(regex).findall(str(lk))
            
                    if len(match_ser)>0:
                         match=[]
                         match.append((sour,match_ser[0]))
                    else:
                        match=[]
                        match.append((sour,'Direct'))
           else:
                if 'TEME' in lk:
                 ff_link=lk
                 f_name=lk.split('%%%')[1].split('_')[1]
                 
                 match=[('TE',f_name)]
                 
                else:
                    regex='\[\[(.+?)\]\].+?//(.+?)/'
                    match=re.compile(regex).findall(str(lk))
                if len(match)==0:
                    if 'TEME' in lk:
                     ff_link=lk
                     f_name=lk.split('%%%')[1].split('_')[1]
                     
                     match=[('TE',f_name)]
                     
                    else:
                        regex='\[\[(.+?)\]\]'
                        sour=re.compile(regex).findall(str(lk))[0]
                        match=[]
                        match.append((sour,'Direct'))
           
           for sour,ty in match:
                all_f_name.append(f_name)
                sour=sour.replace('openload','vummo')
                ty=ty.replace('tv4kids','streamango').replace('.tk','.com')
                if 'sratim' in ty:
                    ty='str'
                all_s.append('[COLOR lightblue][B]'+sour+'[/B][/COLOR] - [COLOR yellow][I]'+ty.replace('letsupload','avlts')+'[/I][/COLOR]')
                
       
       ret = xbmcgui.Dialog().select("בחר", all_s)
       if ret!=-1:
         ff_link=links[ret]
         
         regex='\[\[(.+?)\]\]'
         match2=re.compile(regex).findall(links[ret])
         log.warning(match2)
         if len(match2)>0:
           log.warning(all_s[ret])
           if 'TE' in all_s[ret]:
            
            
            ff_link=ff_link
           if 'http' in ff_link or 'TE' in all_s[ret]:
            ff_link=ff_link.replace(match2[0],'').replace('[','').replace(']','')
            log.warning(ff_link)
           else:
            ff_link=ff_link.replace(match2[0],'')
            log.warning(ff_link)
         else:
            try:
                if 'http' in ff_link:
                    ff_link=ff_link.replace(match2[0],'').replace('[','').replace(']','')
                    log.warning(ff_link)
                else:
                    ff_link=ff_link.replace(match2[0],'')
                    log.warning(ff_link)
            except:
                pass
         log.warning(all_s[ret])
         if 'TE' in all_s[ret]:
            
            
            heb_name=all_f_name[ret]
            saved_name=all_f_name[ret]
            original_title=all_f_name[ret]
            season='%20'
            
         url=ff_link.strip()
         log.warning(url)
       else:
         sys.exit()
    else:
        regex='\[\[(.+?)\]\]'
        match2=re.compile(regex).findall(url)
        if len(match2)>0:
           
            url=url.replace(match2[0],'').replace('[','').replace(']','').strip()
    o_url=url
    
    player=Addon.getSetting("alt_video_player")
    if 'youtube' in o_url and player=='true':
        url=get_youtube5(o_url)
    else:
        if '[' not in o_url and 't.me/' not in o_url:
            try:
                
                
                load_resolveurl_libs()
                import resolveurl
                log.warning('Resolve:'+url)
                url =resolveurl .HostedMediaFile (url =url ).resolve ()#line:2687
                
                log.warning('Resolt:'+str(url))
                if not url:
                    url=resolve_link(o_url,id,all_data['plot'],name)
            except Exception as e:
                log.warning('Erorr in resolve:'+str(e))
                xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kids', str(e))))
                url=resolve_link(o_url,id,all_data['plot'],name)
        else:
            url=resolve_link(o_url,id,all_data['plot'],name)
    listItem = xbmcgui.ListItem(all_data['title'], path=url) 
    listItem.setInfo(type='Video', infoLabels=all_data)


    listItem.setProperty('IsPlayable', 'true')
    ok=xbmcplugin.setResolvedUrl(handle=int(sys_arg_1_data), succeeded=True, listitem=listItem)
    thread=[]
    if 'youtube' not in o_url:
        thread.append(Thread(jump_seek,name,o_url,que(video_info),id,icon,fan,plot,table_name))
        
    
        thread[0].start()
    else:
       playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
       base_header = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': '*/*',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        
        'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
        }
       import requests,random
       if KODI_VERSION<19:
            x=requests.get(o_url,headers=base_header).content
       else:
           x=requests.get(o_url,headers=base_header).content.decode('utf-8')
       
       matche = re.compile('ytInitialData = (.+?)};',re.DOTALL).findall(x)
       all_j=json.loads(matche[0]+'}')
       rand=random.randint(0,len(all_j['playerOverlays']['playerOverlayRenderer']['endScreen']['watchNextEndScreenRenderer']['results'])-1)
       title=all_j['playerOverlays']['playerOverlayRenderer']['endScreen']['watchNextEndScreenRenderer']['results'][rand]['endScreenVideoRenderer']['title']['simpleText']
       link_id=all_j['playerOverlays']['playerOverlayRenderer']['endScreen']['watchNextEndScreenRenderer']['results'][rand]['endScreenVideoRenderer']['videoId']
       link='plugin://plugin.video.kids_new/?mode=5&description={0}&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D{1}&iconimage=&fanart=&video_info={2}&mode=5&id=&name={3}'.format('next',link_id,'',title)
       listItem = xbmcgui.ListItem(title, path=link) 
       playlist.add(url=link,listitem=listItem)
       
def save_fav(name,url,iconimage,fanart,description,video_info):
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""url TEXT,""iconimage TEXT,""fanart TEXT,""description TEXT,""free TEXT,""free2 TEXT);"%'Fav' )
    dbcur.execute("INSERT INTO Fav Values ('%s','%s','%s','%s','%s','%s','')"%(name.replace("'","%27"),url,iconimage,fanart,description.replace("'","%27"),video_info.replace("'","%27")))
    
    dbcon.commit()
    dbcur.close()
    dbcon.close()
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kids', 'נשמר')))
    all_firebase=read_firebase('kids_fav',no_cache=True)
    not_found=True
    for items in all_firebase:
        if 'name' not in all_firebase[items]:
            continue
        if all_firebase[items]['name']==name:
            not_found=False
            break
    if not_found:
        write_firebase(name,url,que(video_info),id,iconimage,fanart,description,"kids_fav",'0','0')
def show_fav():
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""url TEXT,""iconimage TEXT,""fanart TEXT,""description TEXT,""free TEXT,""free2 TEXT);"%'Fav' )

    dbcon.commit()
    
    dbcur.execute("SELECT * FROM Fav")
    match = dbcur.fetchall()
    all_d=[]
    thread=[]
    all_img=[]
    from resources.modules.kidstv_season import get_sdarot_season
    for name ,url ,icon ,fan ,plot,free,free2 in match:
        last=''
        if '[[Sdarot]]' in url:
            url_n=url.replace('מדובב','').replace('בבודמ','')
            id=url_n.replace('[[Sdarot]]','')
            all_ep=get_sdarot_season(id,icon,fan,plot)
            last='[I][B][COLOR lightblue] ['+(all_ep[len(all_ep)-1][0])+'] [/I][/B][/COLOR]'
        if 'sdarot' in icon:
            
            f_image=get_img_loc(icon)
            
            if not os.path.exists(os.path.join(f_image)):
                all_img.append(icon)
            icon=f_image
            image=f_image
        
       
        try:
            video_data=json.loads(free.replace("%27","'"))
        except: 
            video_data={}
            video_data['title']=name.replace("%27","'")
            video_data['icon']=icon
            video_data['fanart']=fan
            video_data['plot']=plot.replace("%27","'")
        video_data['title']=name.replace("%27","'")
        video_data['fast']=1
        
        all_d.append(addDir3(name.replace('%27',"'")+last,url,46,icon,fan,plot.replace('%27',"'"),video_info=video_data))
    thread.append(Thread(download_img,all_img))
  
    for td in thread:
          td.start()
          
    xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_d,len(all_d))
    dbcur.close()
    dbcon.close()
def remove_fav(name,url,iconimage,fanart,description,video_info):
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    nm=json.loads(video_info)['title']
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""url TEXT,""iconimage TEXT,""fanart TEXT,""description TEXT,""free TEXT,""free2 TEXT);"%'Fav' )
    
    dbcur.execute("DELETE FROM Fav Where name='%s'"%(nm.replace("'","%27")))
    
    dbcon.commit()
    dbcur.close()
    dbcon.close()
    
    all_firebase=read_firebase('kids_fav',no_cache=True)

    for items in all_firebase:
            
            if 'name' not in all_firebase[items]:
                continue
            
            if all_firebase[items]['name']==nm:
                
                delete_firebase('kids_fav',items)
               
                break
    xbmc.executebuiltin('Container.Refresh')
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kids', 'הוסר')))
def get_img_loc(image):
    img_n=image.split('/')
    f_img=img_n[len(img_n)-1].replace('/','')
   
    f_save=os.path.join(user_dataDir_img,f_img)
    return f_save
def download_img(urls):
    
    from resources.modules.sdarot import resolve_dns
    for items in urls:
        try:
            x=resolve_dns(items).download_image()
        except:
            pass
    return 0
def heb_tv_dub(url):
    page=int(url)
    
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT,""fanart TEXT,""plot TEXT,""video_data TEXT);"% 'kids_show_orginized')
    dbcur.execute("SELECT * FROM kids_show_orginized ORDER BY name ASC")
    all_l=[]
    match = dbcur.fetchall()
    x=page
    thread=[]
    all_img=[]
    for name ,link,icon, image,plot,data in match:
        
        if (x>=(page*100) and x<=((page+1)*100)):
            if 'sdarot' in image:
                f_image=get_img_loc(image)
                
                if not os.path.exists(os.path.join(f_image)):
                    all_img.append(image)
                icon=f_image
                image=f_image
            
                
            all_l.append(addDir3(name.replace('..','a'),link,46,icon, image,plot,video_info=json.loads(data)))
        
        x+=1
    thread.append(Thread(download_img,all_img))
  
    for td in thread:
          td.start()
    all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),13,'https://www.flatpanelshd.com/pictures/despicableme2-1l.jpg','http://4k.com/wp-content/uploads/2014/11/toystory3_img10_720-790x442.jpg','סרטים מדובבים'))
    xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_l,len(all_l))
    dbcur.close()
    dbcon.close()
def heb_tv_letter(iconimage,fanart):
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    
    
        
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT,""fanart TEXT,""plot TEXT,""video_data TEXT);"% 'kids_show_orginized')
    dbcur.execute("SELECT * FROM kids_show_orginized WHERE substr(name,1,1) NOT LIKE 'א%' and  substr(name,1,1) NOT LIKE 'ב%' and  substr(name,1,1) NOT LIKE 'ג%' and  substr(name,1,1) NOT LIKE 'ד%' and  substr(name,1,1) NOT LIKE 'ה%' and  substr(name,1,1) NOT LIKE 'ו%' and  substr(name,1,1) NOT LIKE 'ז%' and  substr(name,1,1) NOT LIKE 'ח%' and  substr(name,1,1) NOT LIKE 'ט%' and  substr(name,1,1) NOT LIKE 'י%' and  substr(name,1,1) NOT LIKE 'כ%' and  substr(name,1,1) NOT LIKE 'ל%' and  substr(name,1,1) NOT LIKE 'מ%' and  substr(name,1,1) NOT LIKE 'נ%' and  substr(name,1,1) NOT LIKE 'ס%' and  substr(name,1,1) NOT LIKE 'ע%' and  substr(name,1,1) NOT LIKE 'פ%' and  substr(name,1,1) NOT LIKE 'צ%' and  substr(name,1,1) NOT LIKE 'ק%' and  substr(name,1,1) NOT LIKE 'ר%' and  substr(name,1,1) NOT LIKE 'ש%' and  substr(name,1,1) NOT LIKE 'ת%'")
    match_num = dbcur.fetchall()
    
    
    all_l=[]
    exclude=[1503,1498,1509,1501,1507]
    all_l.append(addDir3('1-2'+ ' [COLOR lightblue](%s)[/COLOR] '%str(len(match_num)),'0',15,iconimage,fanart,'סרטים מדובבים'))
    for ch in range(1488,1515): 
        if ch in exclude:
            continue
        if KODI_VERSION<19:
            dbcur.execute('SELECT * FROM kids_show_orginized where name like "{0}%"'.format(unichr(ch)))
        else:
            dbcur.execute('SELECT * FROM kids_show_orginized where name like "{0}%"'.format(chr(ch)))
    
        match = dbcur.fetchall()
        if KODI_VERSION<19:
            all_l.append(addDir3(unichr(ch)+ ' [COLOR lightblue](%s)[/COLOR] '%str(len(match)),'0',15,iconimage,fanart,'סרטים מדובבים'))
        else:
            all_l.append(addDir3(chr(ch)+ ' [COLOR lightblue](%s)[/COLOR] '%str(len(match)),'0',15,iconimage,fanart,'סרטים מדובבים'))
    xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_l,len(all_l))
    dbcur.close()
    dbcon.close()
def heb_tv_dub_letter(name,url):
    o_name=name
    page=int(url)
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    name=name.split(' [')[0]
    if name=='1-2':
        exclude=[1503,1498,1509,1501,1507]
        all_s=[]
        for ch in range(1488,1515): 
            if ch in exclude:
                continue
            if KODI_VERSION<19:
                all_s.append("substr(name,1,1) NOT LIKE '{0}%' and ".format(unichr(ch)))
            else:
                all_s.append("substr(name,1,1) NOT LIKE '{0}%' and ".format(chr(ch)))
        dbcur.execute("SELECT * FROM kids_show_orginized WHERE substr(name,1,1) NOT LIKE 'א%' and  substr(name,1,1) NOT LIKE 'ב%' and  substr(name,1,1) NOT LIKE 'ג%' and  substr(name,1,1) NOT LIKE 'ד%' and  substr(name,1,1) NOT LIKE 'ה%' and  substr(name,1,1) NOT LIKE 'ו%' and  substr(name,1,1) NOT LIKE 'ז%' and  substr(name,1,1) NOT LIKE 'ח%' and  substr(name,1,1) NOT LIKE 'ט%' and  substr(name,1,1) NOT LIKE 'י%' and  substr(name,1,1) NOT LIKE 'כ%' and  substr(name,1,1) NOT LIKE 'ל%' and  substr(name,1,1) NOT LIKE 'מ%' and  substr(name,1,1) NOT LIKE 'נ%' and  substr(name,1,1) NOT LIKE 'ס%' and  substr(name,1,1) NOT LIKE 'ע%' and  substr(name,1,1) NOT LIKE 'פ%' and  substr(name,1,1) NOT LIKE 'צ%' and  substr(name,1,1) NOT LIKE 'ק%' and  substr(name,1,1) NOT LIKE 'ר%' and  substr(name,1,1) NOT LIKE 'ש%' and  substr(name,1,1) NOT LIKE 'ת%' ORDER BY name ASC")
    else:
        dbcur.execute('SELECT * FROM kids_show_orginized where name like "{0}%" ORDER BY name ASC'.format(name))
    all_l=[]
    match = dbcur.fetchall()
    x=page
    thread=[]
    all_img=[]
    for name ,link,icon, image,plot,data in match:
        if (x>=(page*100) and x<=((page+1)*100)):
            
            if 'sdarot' in image:
                f_image=get_img_loc(image)
                
                if not os.path.exists(os.path.join(f_image)):
                    all_img.append(image)
                icon=f_image
                image=f_image
                
            all_l.append(addDir3(name,link,46,icon,image,plot,video_info=json.loads(data)))
            
        x+=1




    
    thread.append(Thread(download_img,all_img))
  
    for td in thread:
          td.start()
    if (len(match)-((page+1)*100))>0:
        all_l.append(addDir3(o_name+' [COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),15,'https://www.flatpanelshd.com/pictures/despicableme2-1l.jpg','http://4k.com/wp-content/uploads/2014/11/toystory3_img10_720-790x442.jpg','סרטים מדובבים'))
    xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_l,len(all_l))
    dbcur.close()
    dbcon.close()
def heb_mov_dub(url,description):
    import datetime
    page=int(url)
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    all_w={}
    if len(Addon.getSetting("firebase"))>0:
            all_db=read_firebase('last_played_movie_seek_time',no_cache=False)
        
            for itt in all_db:
                if 'name' not in all_db[itt]:
                    continue
                items=all_db[itt]
                all_w[items['name']]={}
                all_w[items['name']]['seek_time']=items['seek_time']
                all_w[items['name']]['total_time']=items['total_time']
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    if 'נצפו' in description:
        
        if len(Addon.getSetting("firebase"))>0:
            all_db=read_firebase('last_played_movie')
            match=[]
            for itt in all_db:
                if 'name' not in all_db[itt]:
                    continue
                items=all_db[itt]
                
                match.append((items['name'],items['url'],items['video_info'],items['id'],items['icon'],items['fan'],''))
            
        else:
            dbcur.execute("SELECT * FROM watched ")
        
            match = dbcur.fetchall()
        all_l=[]
        x=page
        all_array=[]
        count=0
        for name ,link,data,tmdbid,icon, image,free in match:
            all_array.append((count,name ,link,data,tmdbid,icon, image,free))
            count+=1
        all_array=sorted(all_array, key=lambda x: x[0], reverse=True)
        for count,name ,link,data,tmdbid,icon, image,free in all_array:
            if (x>=(page*100) and x<=((page+1)*100)):
                all_l.append(addLink(replaceHTMLCodes(name.replace("%27","'")),link,5,False,icon,image,'',video_info=unque(data),id=tmdbid,all_w=all_w))
            x+=1
        all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),10,'https://www.flatpanelshd.com/pictures/despicableme2-1l.jpg','http://4k.com/wp-content/uploads/2014/11/toystory3_img10_720-790x442.jpg',description))
        
    elif 'שנים' in description:
        
        dbcur.execute("SELECT * FROM kids_movie_year ORDER BY year DESC")
        all_l=[]
        match = dbcur.fetchall()
        x=page
        for name ,link,icon, image,plot,data,tmdbid ,date_added,year in match:
            if (x>=(page*100) and x<=((page+1)*100)):
                all_l.append(addLink(replaceHTMLCodes(name),link,5,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w))
            x+=1
        all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),10,'https://www.flatpanelshd.com/pictures/despicableme2-1l.jpg','http://4k.com/wp-content/uploads/2014/11/toystory3_img10_720-790x442.jpg',description))
    else:
        
        dbcur.execute("SELECT * FROM kids_movie_ordered ORDER BY date_added DESC")
        all_l=[]
        match = dbcur.fetchall()
        x=page
        all_data_in=[]
        for name ,link,icon, image,plot,data,tmdbid ,date_added in match:
            try:
                try:
                                                                      
                      new_date=datetime.datetime.strptime(date_added, '%Y-%m-%d %H:%M:%S')
                except TypeError:
                      
                      new_date=datetime.datetime(*(time.strptime(date_added, "%Y-%m-%d %H:%M:%S")[0:6]))
                      
            except:
               try:
                try:
                                                                      
                      new_date=datetime.datetime.strptime(date_added, '%d/%m/%Y %H:%M:%S')
                except TypeError:
                      
                      new_date=datetime.datetime(*(time.strptime(date_added, "%d/%m/%Y %H:%M:%S")[0:6]))
               except:
                new_date=new_date
            all_data_in.append((name ,link,icon, image,plot,data,tmdbid ,new_date))
        all_data_in=sorted(all_data_in, key=lambda x: x[7], reverse=True)
        for name ,link,icon, image,plot,data,tmdbid ,date_added in all_data_in:
            if (x>=(page*100) and x<=((page+1)*100)):
                all_l.append(addLink((name),link,5,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w))
                
            x+=1
        all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),10,'https://www.flatpanelshd.com/pictures/despicableme2-1l.jpg','http://4k.com/wp-content/uploads/2014/11/toystory3_img10_720-790x442.jpg',description))
    xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_l,len(all_l))
    dbcur.close()
    dbcon.close()
def heb_mov_letter(iconimage,fanart):
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    
    
        
        
    dbcur.execute("SELECT * FROM kids_movie_ordered WHERE substr(name,1,1) NOT LIKE 'א%' and  substr(name,1,1) NOT LIKE 'ב%' and  substr(name,1,1) NOT LIKE 'ג%' and  substr(name,1,1) NOT LIKE 'ד%' and  substr(name,1,1) NOT LIKE 'ה%' and  substr(name,1,1) NOT LIKE 'ו%' and  substr(name,1,1) NOT LIKE 'ז%' and  substr(name,1,1) NOT LIKE 'ח%' and  substr(name,1,1) NOT LIKE 'ט%' and  substr(name,1,1) NOT LIKE 'י%' and  substr(name,1,1) NOT LIKE 'כ%' and  substr(name,1,1) NOT LIKE 'ל%' and  substr(name,1,1) NOT LIKE 'מ%' and  substr(name,1,1) NOT LIKE 'נ%' and  substr(name,1,1) NOT LIKE 'ס%' and  substr(name,1,1) NOT LIKE 'ע%' and  substr(name,1,1) NOT LIKE 'פ%' and  substr(name,1,1) NOT LIKE 'צ%' and  substr(name,1,1) NOT LIKE 'ק%' and  substr(name,1,1) NOT LIKE 'ר%' and  substr(name,1,1) NOT LIKE 'ש%' and  substr(name,1,1) NOT LIKE 'ת%'")
    match_num = dbcur.fetchall()
    
    
    all_l=[]
    exclude=[1503,1498,1509,1501,1507]
    all_l.append(addDir3('1-2'+ ' [COLOR lightblue](%s)[/COLOR] '%str(len(match_num)),'0',12,iconimage,fanart,'סרטים מדובבים'))
    for ch in range(1488,1515): 
        if ch in exclude:
            continue
        if KODI_VERSION<19:
            dbcur.execute('SELECT * FROM kids_movie_ordered where name like "{0}%"'.format(unichr(ch)))
        else:
            dbcur.execute('SELECT * FROM kids_movie_ordered where name like "{0}%"'.format(chr(ch)))
    
        match = dbcur.fetchall()
        if KODI_VERSION<19:
            all_l.append(addDir3(unichr(ch)+ ' [COLOR lightblue](%s)[/COLOR] '%str(len(match)),'0',12,iconimage,fanart,'סרטים מדובבים'))
        else:
            all_l.append(addDir3(chr(ch)+ ' [COLOR lightblue](%s)[/COLOR] '%str(len(match)),'0',12,iconimage,fanart,'סרטים מדובבים'))
    xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_l,len(all_l))
    dbcur.close()
    dbcon.close()
def heb_mov_dub_letter(name,url):
    o_name=name
    page=int(url)
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    name=name.split(' [')[0]
    if name=='1-2':
        exclude=[1503,1498,1509,1501,1507]
        all_s=[]
        for ch in range(1488,1515): 
            if ch in exclude:
                continue
            if KODI_VERSION<19:
                all_s.append("substr(name,1,1) NOT LIKE '{0}%' and ".format(unichr(ch)))
            else:
                all_s.append("substr(name,1,1) NOT LIKE '{0}%' and ".format(chr(ch)))
        dbcur.execute("SELECT * FROM kids_movie_ordered WHERE substr(name,1,1) NOT LIKE 'א%' and  substr(name,1,1) NOT LIKE 'ב%' and  substr(name,1,1) NOT LIKE 'ג%' and  substr(name,1,1) NOT LIKE 'ד%' and  substr(name,1,1) NOT LIKE 'ה%' and  substr(name,1,1) NOT LIKE 'ו%' and  substr(name,1,1) NOT LIKE 'ז%' and  substr(name,1,1) NOT LIKE 'ח%' and  substr(name,1,1) NOT LIKE 'ט%' and  substr(name,1,1) NOT LIKE 'י%' and  substr(name,1,1) NOT LIKE 'כ%' and  substr(name,1,1) NOT LIKE 'ל%' and  substr(name,1,1) NOT LIKE 'מ%' and  substr(name,1,1) NOT LIKE 'נ%' and  substr(name,1,1) NOT LIKE 'ס%' and  substr(name,1,1) NOT LIKE 'ע%' and  substr(name,1,1) NOT LIKE 'פ%' and  substr(name,1,1) NOT LIKE 'צ%' and  substr(name,1,1) NOT LIKE 'ק%' and  substr(name,1,1) NOT LIKE 'ר%' and  substr(name,1,1) NOT LIKE 'ש%' and  substr(name,1,1) NOT LIKE 'ת%' ORDER BY name ASC")
    else:
        dbcur.execute('SELECT * FROM kids_movie_ordered where name like "{0}%" ORDER BY name ASC'.format(name))
    all_l=[]
    match = dbcur.fetchall()
    x=page
    all_w={}
    if len(Addon.getSetting("firebase"))>0:
            all_db=read_firebase('last_played_movie_seek_time')
       
            for itt in all_db:
                if 'name' not in all_db[itt]:
                    continue
                items=all_db[itt]
                all_w[items['name']]={}
                all_w[items['name']]['seek_time']=items['seek_time']
                all_w[items['name']]['total_time']=items['total_time']
                
    for name ,link,icon, image,plot,data,tmdbid ,date_added in match:
        if (x>=(page*100) and x<=((page+1)*100)):
            all_l.append(addLink(replaceHTMLCodes(name),link,5,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w))
        x+=1

    if (len(match)-((page+1)*100))>0:
        all_l.append(addDir3(o_name+' [COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),12,'https://www.flatpanelshd.com/pictures/despicableme2-1l.jpg','http://4k.com/wp-content/uploads/2014/11/toystory3_img10_720-790x442.jpg','סרטים מדובבים'))
    xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_l,len(all_l))
    dbcur.close()
    dbcon.close()
def random_tv(sys_arg_1_data):
    import random
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT,""fanart TEXT,""plot TEXT,""video_data TEXT);"% 'kids_show_orginized')
    dbcur.execute("SELECT * FROM kids_show_orginized ORDER BY name ASC")
    all_l=[]
    match = dbcur.fetchall()
    dbcur.close()
    dbcon.close()
    x=0
    found=True
    count=0
    while found:
        rand=random.randint(0,len(match)-1)
        
        for name ,link,icon, image,plot,data in match:
            if x==rand and 'Sdarot' in link:
                found=False
                break

            x+=1
        count+=1
        if count>10:
            break
        xbmc.sleep(100)
    s_name=name
    from resources.modules.kidstv_season import get_seasons
    all_img=[]
    if 'sdarot' in image:
        f_image=get_img_loc(image)
        
        if not os.path.exists(os.path.join(f_image)):
            all_img.append(image)
        icon=f_image
        image=f_image
        thread=[]
        thread.append(Thread(download_img,all_img))
      
        for td in thread:
              td.start()
    name,link,icon,image,plot,video_data=get_seasons(name,link,icon,image,plot,1,rand=True,sys_arg_1_data=sys_arg_1_data)
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('נבחרה', s_name)))
    play_link(name,link,json.dumps(video_data),'0',icon,image,plot)
def random_movie():
    import random
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    

    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT,""image TEXT,""plot TEXT,""data TEXT,""tmdbid TEXT,""date_added TEXT);"% 'kids_movie_ordered')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""url TEXT,""video_info TEXT,""id TEXT,""icon TEXT,""fan TEXT,""free TEXT);"%'watched' )
    dbcur.execute("SELECT * FROM kids_movie_ordered ORDER BY name ASC")
    #get watched
    
    
    all_l=[]
    match = dbcur.fetchall()
    match_watched=[]
    if len(Addon.getSetting("firebase"))>0:
            all_db=read_firebase('last_played_movie')
            
            for itt in all_db:
                if 'name' not in all_db[itt]:
                    continue
                items=all_db[itt]
                
                match_watched.append((items['name'],items['url'],items['video_info'],items['id'],items['icon'],items['fan'],''))
    else:
        dbcur.execute("SELECT * FROM watched ORDER BY name ASC")
        match_watched = dbcur.fetchall()
    dbcur.close()
    dbcon.close()
    x=0
    found=True
    all_w=[]
    for name,url,video_info,id,icon,fan,free in match_watched:
        all_w.append(name)
    count=0
    rand_was=[]
    while found:
    
        rand=random.randint(0,len(match)-1)
       
        if rand not in rand_was:
           
            rand_was.append(rand)
            
            name ,link,icon, image,plot,data,tmdbid,date_added=match[rand]
           
            if name not in all_w:
                found=False
                
                break
     
        count+=1
        if count>len(match):
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('לא נמצא דבר', 'לא נמצא דבר')))
            break
        xbmc.sleep(100)
    if not found:
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('נבחרה', name)))
        play_link(name,link,data,tmdbid,icon,image,plot)
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
        xbmc.sleep(100)
def check_times(name,video_info):
    import datetime
    from datetime import date
    name=json.loads(video_info)['title']
    import requests
    today = date.today()

    d1 = today.strftime("%d/%m/%Y")

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': '*/*',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        
        'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('text', name),
        ('channel', '-1'),
        ('genre', '-1'),
        ('ageRating', '-1'),
        ('publishYear', '-1'),
        ('productionCountry', '-1'),
        ('startDate', (d1)+' 00:00:00'),
        ('endDate', (today+ datetime.timedelta(days=7)).strftime("%d/%m/%Y")+' 00:00:00'),
        ('startTime', str(d1)+' 07:30:00'),
        ('endTime', str(d1)+' 07:30:00'),
        ('currentPage', '1'),
        ('pageSize', '50'),
        ('isOrderByDate', 'true'),
        ('lcid', '1037'),
        ('pageIndex', '1'),
    )

    
    x = requests.get('https://www.hot.net.il/PageHandlers/LineUpAdvanceSearch.aspx', headers=headers, params=params).content
    
    regex='<tr(.+?)</tr'
    m=re.compile(regex,re.DOTALL).findall(x)
    if len(m)==0:
        xbmcgui.Dialog().ok('זמן שידור','לא ידוע')
        return 0
    all_d=[]
    all_itt=[]
    for items in m:
        regex="class='w122 nborder'>(.+?)<"
        m2=re.compile(regex,re.DOTALL).findall(items)
        counter=0
        b=True
        for itt in m2:
            if counter==0:
                temp_zero=itt
            elif counter==1:
                if itt in all_itt:
                    b=False
                    break
                else:
                    #all_d.append(temp_zero)
                    all_d.append('[COLOR red][B]'+itt+'[/B][/COLOR]')
                    all_itt.append(itt)
            
            elif counter==3:
                    all_d.append('[COLOR lightblue][B]'+itt+'[/B][/COLOR]')
            #else:
            #    all_d.append(itt)
            counter+=1
        if b:
            all_d.append('\n------------------------------------\n')
    showText('מתי משודר', '|'.join(all_d))
def  sync_firebase():
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM watched ")
    match = dbcur.fetchall()
    all_names={}
    dp = xbmcgui.DialogProgress()
    if KODI_VERSION<19:
        dp.create("Firebase", 'מעדכן', 'אנא המתן',"")
    else:
        dp.create("Firebase", 'מעדכן'+'\n'+ 'אנא המתן'+'\n'+"")
    dp.update(0)
                
    count_m=0
    for name_w ,link_w,data_w,tmdbid_w,icon_w, image_w,free_w in match:
        vid_info=unque(data_w)
        try:
            vid_info=json.loads(vid_info)
            all_names[vid_info['title'].replace("%27","'").replace("-"," ")]=[]
            all_names[vid_info['title'].replace("%27","'").replace("-"," ")].append((name_w.replace("%27","'").replace("-"," ") ,link_w,data_w,tmdbid_w,icon_w, image_w,free_w))
   
        except Exception as e:
            log.error('sync_firebase:'+str(e))
        
        
    all_record=read_firebase('last_played_movie',no_cache=True)
    all_fire_names=[]
    
    for itt in all_record:
        if 'name' not in all_record[itt]:
            continue
        all_fire_names.append(all_record[itt]['name'])
    count=0
    for items in all_names:
        if KODI_VERSION<19:
            dp.update(int((count) / (len(all_names)) * 100.0), 'אנא המתן', items, '')
        else:
            dp.update(int((count) / (len(all_names)) * 100.0), 'אנא המתן'+'\n'+ items+'\n'+ '')
        count+=1
        if dp.iscanceled():
            dp.close()
        if 'עונה ' in items:
            continue
        if items not in all_fire_names:
            
            f_name,url,video_info,id,icon,fan,plot=all_names[items][0]
            write_firebase(f_name,url,video_info,id,icon,fan,plot,'last_played_movie','0','0')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""url TEXT,""iconimage TEXT,""fanart TEXT,""description TEXT,""free TEXT,""free2 TEXT);"%'Fav' )

    dbcon.commit()
    
    dbcur.execute("SELECT * FROM Fav")
    match = dbcur.fetchall()
    all_d=[]
    thread=[]
    all_img=[]
    all_n=[]
    all_d=[]
    for name ,url ,icon ,fan ,plot,free,free2 in match:
        all_n.append(name)
        all_d.append((name ,url ,icon ,fan ,plot,free,free2))
    all_firebase=read_firebase('kids_fav',no_cache=True)
    all_f_n=[]
    all_f=[]
    for items in all_firebase:
        if 'name' not in all_firebase[items]:
            continue
        all_f_n.append(all_firebase[items]['name'])
        all_f.append(all_firebase[items])
    i=0
    for nm in all_f_n:
        if nm not in all_n:
            name=all_f[i]['name']
            url=all_f[i]['url']
            icon=all_f[i]['icon']
            fan=all_f[i]['fan']
            plot=all_f[i]['plot']
            video_info=all_f[i]['video_info']
            
            
            dbcur.execute("INSERT INTO Fav Values ('%s','%s','%s','%s','%s','%s','')"%(name.replace("'","%27"),url,icon,fan,plot.replace("'","%27"),video_info.replace("'","%27")))
        i+=1
    dbcon.commit()
    dp.close()
    xbmcgui.Dialog().ok('Firebase','הסתיים')
def search_result(search_entered,dubbed=False):
    dp = xbmcgui . DialogProgress ( )
    if KODI_VERSION>18:
        dp.create('Please wait','מחפש...')
    else:
        dp.create('Please wait','מחפש...', '','')
    if KODI_VERSION>18:
        dp.update(0, 'Please wait'+'\n'+'מחפש...'+'\n'+ '' )
    else:
        dp.update(0, 'Please wait','מחפש...', '' )
        
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    x=0
    if not dubbed:
        dbcur.execute("SELECT * FROM kids_movie_ordered where name like '%{0}%'".format(search_entered))
        match2 = dbcur.fetchall()
        
        all_w={}
        if len(Addon.getSetting("firebase"))>0:
                if KODI_VERSION>18:
                    dp.update(0, 'Please wait'+'\n'+'read_firebase...'+'\n'+ '' )
                else:
                    dp.update(0, 'Please wait','read_firebase...', '' )
                all_db=read_firebase('last_played_movie_seek_time',no_cache=True)
            
                for itt in all_db:
                    if 'name' not in all_db[itt]:
                        continue
                    items=all_db[itt]
                    all_w[items['name']]={}
                    all_w[items['name']]['seek_time']=items['seek_time']
                    all_w[items['name']]['total_time']=items['total_time']
        
        all_l=[]
        addNolink( '[COLOR yellow][I]סרטים[/I][/COLOR]', 'www',999,False, iconimage="https://i.ytimg.com/vi/6sRi1FvWe1Q/maxresdefault.jpg",fan='https://i.ytimg.com/vi/DZj9lWmqbus/hqdefault.jpg',sys_arg_1_data=sys_arg_1_data)
        if KODI_VERSION>18:
            dp.update(0, 'Please wait'+'\n'+'Done_firebase...'+'\n'+ '' )
        else:
            dp.update(0, 'Please wait','Done_firebase...', '' )
        for name ,link,icon, image,plot,data,tmdbid ,date_added in match2:
            if KODI_VERSION>18:
                dp.update(0, 'Please wait'+'\n'+'מחפש...'+'\n'+ name )
            else:
                dp.update(0, 'Please wait','מחפש...', name )
            all_l.append(addLink(replaceHTMLCodes(name),link,5,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w))
            x+=1
            
        xbmcplugin.addDirectoryItems(int(sys_arg_1_data),all_l,len(all_l))
        addNolink( '[COLOR yellow][I]סדרות[/I][/COLOR]', 'www',999,False, iconimage="https://i.ytimg.com/vi/6sRi1FvWe1Q/maxresdefault.jpg",fan='https://i.ytimg.com/vi/DZj9lWmqbus/hqdefault.jpg',sys_arg_1_data=sys_arg_1_data)
    if not dubbed:
        dbcur.execute("SELECT * FROM kids_show_orginized where name like '%{0}%'".format(search_entered))
    else:
        dbcur.execute("SELECT * FROM kids_show_orginized where name like '%{0}%' or plot like '%{0}%'".format(search_entered))
    all_l=[]
    match = dbcur.fetchall()

    thread=[]
    all_img=[]

    for name ,link,icon, image,plot,data in match:
            if KODI_VERSION>18:
                dp.update(0, 'Please wait'+'\n'+'מחפש...'+'\n'+ name )
            else:
                dp.update(0, 'Please wait','מחפש...', name )
            if 'sdarot' in image:
                f_image=get_img_loc(image)
                
                if not os.path.exists(os.path.join(f_image)):
                    all_img.append(image)
                icon=f_image
                image=f_image
                
            all_l.append(addDir3(name.replace('..','a'),link,46,icon, image,plot,video_info=json.loads(data)))
        
            x+=1
    if KODI_VERSION>18:
        dp.update(0, 'Please wait'+'\n'+'מוריד תמונות...'+'\n'+ '' )
    else:
        dp.update(0, 'Please wait','מוריד תמונות...', '' )
    thread.append(Thread(download_img,all_img))
  
    for td in thread:
          td.start()
    xbmcplugin.addDirectoryItems(int(sys_arg_1_data),all_l,len(all_l))
    dbcur.close()
    dbcon.close()
    dp.close()
def youtubemenu():
    all_d=[]
    all_d.append(addDir3('ערוץ TEEN','https://www.youtube.com/channel/UCcgf7Bokf_WzQLFDwaBEmSw',51,'https://upload.wikimedia.org/wikipedia/commons/9/98/TEENick_Splat_logo.png','https://i.ytimg.com/vi/zHeH_sDeZqE/maxresdefault.jpg','ערוץ TEEN'))
    all_d.append(addDir3('ערוץ YES','https://www.youtube.com/user/YesVOD',51,'https://images.globes.co.il/images/NewGlobes/big_image_800/2015/yes-800.20151202T113624.jpg','https://www.gadgety.co.il/wp-content/themes/main/thumbs/2018/05/Yes-logo-350x233.jpg','ערוץ YES'))
    all_d.append(addDir3('ערוץ HOT','https://www.youtube.com/user/HOTVODyoung',51,'https://www.gadgety.co.il/wp-content/themes/main/thumbs/2018/09/Hot-new-logo-350x233.jpg','https://www.ynet.co.il/PicServer5/2017/10/27/8114181/811417901000100640360no.jpg','ערוץ HOT'))
    all_d.append(addDir3('ערוץ ZOOM','https://www.youtube.com/user/ZOOMTVISRAEL',51,'https://www.digitalvibe.co.il/wp-content/uploads/2016/02/zoom.jpg','https://s3cdn.zoomtv.co.il/wp-content/uploads/2017/08/ZoomGt.jpg','ערוץ ZOOM'))
    all_d.append(addDir3('ערוץ BIGI','https://www.youtube.com/user/kidstvbme',51,'https://www.kamaze.co.il/Uploads/Images/reviews/BIGI.jpg','https://images1.calcalist.co.il/PicServer3/2020/10/27/1030838/1_lm.jpg','ערוץ BIGI'))
    
    all_d.append(addDir3('ערוץ כאן','https://www.youtube.com/user/23tv',51,'https://res.cloudinary.com/atzuma/image/upload/c_thumb,g_face:center,h_450,q_70,w_800/v1502878408/atzuma/bxszjmvitaufgvnlc1qh.jpg','https://i.ytimg.com/vi/SQ4eYiZ5foo/maxresdefault.jpg','ערוץ כאן'))
    all_d.append(addDir3('ערוץ קוין','https://www.youtube.com/channel/UCbNShN8GoHuxv92-dIn6Tow',51,'https://yt3.ggpht.com/ytc/AAUvwnhM9Z9P_TpXdEAyeJakmb0wdEkSvKf9AaKVJDC6=s900-c-k-c0x00ffffff-no-rj','https://eilat.city/images/events/eventItem/%D7%A7%D7%95%D7%95%D7%99%D7%9F-%D7%A8%D7%95%D7%91%D7%99%D7%9F.jpg','קוין'))
    all_d.append(addDir3('לימוד קסמים','https://www.youtube.com/channel/UCBIS-ugzEVCP5s-ARxFee-A',51,'https://www.popy.co.il/storage/content-images/chen-wizard-1-10.png','https://i.ytimg.com/vi/BdjoVz70dK8/maxresdefault.jpg','קוין'))
    all_d.append(addDir3('אי הזחלים','https://www.youtube.com/user/Larva2011ani',51,'https://ae01.alicdn.com/kf/HTB1atevtoR1BeNjy0Fmq6z0wVXaS/20cm-Cute-Funny-Insect-Slug-Creative-Larva-Plush-Toys-Stuffed-Doll-Movie-TV-Cartoon-Stuffed-Worm.jpg','https://i.ytimg.com/vi/wvLaOtygQQI/maxresdefault.jpg','הזחלים'))
    
    xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_d,len(all_d))
def small_kids():
    all_d=[]
    all_d.append(addDir3('נסטיה','https://www.youtube.com/channel/UCJplp5SjeGSdVdwsfb9Q7lQ',51,'https://upload.wikimedia.org/wikipedia/commons/9/98/TEENick_Splat_logo.png','https://i.ytimg.com/vi/UjgV6fDOEbg/maxresdefault.jpg','נסטיה'))
    all_d.append(addDir3('דיאנה','https://www.youtube.com/channel/UCk8GzjMOrta8yxDcKfylJYw',51,'https://yt3.ggpht.com/a/AGF-l7-hD4TMvKFh1QTzcExTsZc7Vkmu-ucEUnwjFw=s900-c-k-c0xffffffff-no-rj-mo','https://i.ytimg.com/vi/waE-c0Qj5gM/maxresdefault.jpg','דיאנה'))
    all_d.append(addDir3('סופיה','https://www.youtube.com/channel/UCCo2mpdEvV8SrC5FsgG-OKg',51,'https://yt3.ggpht.com/a/AATXAJwikdaZiczrVALY9If48Wh-Jo96OteLSTAL8g=s900-c-k-c0xffffffff-no-rj-mo','https://i.ytimg.com/vi/gOl6kfzltIQ/maxresdefault.jpg','סופיה'))
    all_d.append(addDir3('דיסני','https://www.youtube.com/user/disneyjuniorisrael/featured',51,'https://hospitality-on.com/sites/default/files/2017-09/Walt%20Disney%20Park%20%26%20Resorts.jpg','https://i.ytimg.com/vi/-oztKC-X_ww/maxresdefault.jpg','דיסני'))
    
    xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_d,len(all_d))

def clear_telemdia():
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath
    a=xbmcgui.Dialog().yesno('TELEMEDIA','אתה בטוח שאתה רוצה לנקות הכל?')
    if a:
        os.remove ( os.path.join(tmdb_data_dir, 'telehebdub.db'))
    xbmcgui.Dialog().ok('TELEMEDIA','Done')
def update_library():
    import datetime
    
    user_path=xbmc_tranlate_path(Addon.getSetting('library.movie'))
    base_movie_path=os.path.join(user_path,'strm','movies')
    
     

    strm='plugin://plugin.video.kids_new/?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&description=%s&id=%s&video_info=%s'
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database

    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    
    dbcur.execute("SELECT * FROM kids_movie_ordered ORDER BY date_added DESC")
    match = dbcur.fetchall()
    
    dbcur.close()
    dbcon.close()
    new_items=[]
    dp = xbmcgui.DialogProgress()
    if KODI_VERSION<19:
        dp.create("טוען", "")
        
    else:
        dp.create("טוען", "" )
                
                
    count=0
    import codecs
    for name ,link,icon, image,plot,data,tmdbid ,date_added in match:
            template='''\
<movie>
    <title>%s</title>
    <originaltitle>%s</originaltitle>
    <ratings>
        <rating name="themoviedb" max="10" default="true">
            <value>%s</value>
            <votes>%s</votes>
        </rating>
    </ratings>
    <plot>%s</plot>
    <runtime>%s</runtime>
    <path>%s</path>
    <filenameandpath>%s.strm</filenameandpath>
    <basepath>%s.strm</basepath>
    <uniqueid type="tmdb" default="true">%s</uniqueid>
    
    %s
    <year>%s</year>
    <trailer>plugin://plugin.video.youtube/?action=play_video&amp;videoid=%s</trailer>
    <thumb spoof="" cache="" aspect="poster" preview="">%s</thumb>
    <fanart>
      <thumb colors="" preview="%s">%s</thumb>
            
    </fanart>
    <dateadded>%s</dateadded>
</movie>
    '''
            if KODI_VERSION<19:
                dp.update(int((count) / (len(match)) * 100.0), name)
            else:
                dp.update(int((count) / (len(match)) * 100.0), name)
            
            if dp.iscanceled():
                dp.close()
                return None, None
            count+=1
            try:
                try:
                                                                      
                      new_date=datetime.datetime.strptime(date_added, '%Y-%m-%d %H:%M:%S')
                except TypeError:
                      
                      new_date=datetime.datetime(*(time.strptime(date_added, "%Y-%m-%d %H:%M:%S")[0:6]))
                      
            except:
               try:
                try:
                                                                      
                      new_date=datetime.datetime.strptime(date_added, '%d/%m/%Y %H:%M:%S')
                except TypeError:
                      
                      new_date=datetime.datetime(*(time.strptime(date_added, "%d/%m/%Y %H:%M:%S")[0:6]))
               except:
                new_date="1988-03-02 00:34:31"
                
            try:
                fixed_data=json.loads(data)
            except:
                fixed_data=None
            if fixed_data:
                
                title=fixed_data['title']
                c_title=title.replace('*',"_").replace(':',"_").replace("'","_").replace('\\','_').replace('/','_').replace("'",'_').replace('"','_').replace('!','_').replace('?','_').replace('.',"_")
                if 'OriginalTitle' in fixed_data:
                    original_title=fixed_data['OriginalTitle']
                else:
                    original_title=fixed_data.get('originaltitle',title)
                rating=fixed_data.get('rating',"")
                votes=fixed_data.get('votes',"")
                plot=fixed_data.get('plot',"")
                runtime=fixed_data.get('duration',"")
                movie_path=os.path.join(base_movie_path,c_title)
                if not os.path.exists(movie_path):
                    os.makedirs(movie_path)
     
                path=movie_path
                strm_path=os.path.join(movie_path,c_title)
                tmdb_id=fixed_data.get('tmdb',"")
                genere=[]
                if 'genre' in fixed_data:
                    for items in fixed_data['genre'].split('/'):
                        genere.append('<genre>%s</genre>'%items)
                generes='\n'.join(genere)
                year=fixed_data.get('year',"")
                trailer=fixed_data.get('trailer',"")
                icon=fixed_data.get('icon',"")
                if 'fanart' in fixed_data:
                    fanart=fixed_data['fanart']
                else:
                    
                    fanart=fixed_data.get('poster',"")
                dateadded=new_date
                new_items=(template%(title,original_title,rating,votes,plot,runtime,path,strm_path,strm_path,tmdb_id,generes,year,trailer,icon,fanart,fanart,dateadded))
                new_strm=strm%(que(title),que(link),que(icon),que(fanart)," ",tmdb_id,"ss")
                
                final='<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n'+new_items
                file = codecs.open(os.path.join(movie_path, c_title+'.nfo'), "w", "utf-8")

                file.write(final)
                file.close()
    
                file = open(strm_path+'.strm', "w")

                file.write(new_strm)
                file.close()
                
                
    
    dp.close()
    xbmc.executebuiltin('UpdateLibrary(video)')
def latest_movies():
    from resources.modules.hebdub_movies import get_dub_movies,get_dub_movies2,get_dub_movies4,get_dub_movies5,get_dub_movies6,get_dub_movies7
    from resources.modules.hebdub_movies import all_dub,all_dub7
    thread=[]
    
    thread.append(Thread(get_dub_movies))
    thread.append(Thread(get_dub_movies7))
    
    
    for td in thread:
          td.start()
    
    while 1:

    
        for threads in thread:
       
            still_alive=0
            for yy in range(0,len(thread)):
                    if thread[yy].is_alive():
                      
                      still_alive=1
            xbmc.sleep(300)
        if still_alive==0:
          break
        xbmc.sleep(100)
    log.warning('all_dub:'+str(len(all_dub)))
    log.warning('all_dub2:'+str(len(all_dub7)))
    all_dub7.append((name.replace(' [COLOR coral]מדובב [/COLOR]','').replace('[COLOR coral]מדובב [/COLOR]',''),f_link,5,'[[Dr]]',icon,fanart,plot,data.replace("OriginalTitle","originaltitle")))
 
def refresh_list(user_params,sys_arg_1):
    global sys_arg_1_data
    sys_arg_1_data=sys_arg_1
    params=get_params(user_params=user_params)

    url=None
    name='No name'
    mode=None
    iconimage='No icon'
    fanart='No fan'
    description='No plot'
    id='0'
    next_page='0'
    video_info={}
    try:
            url=unque(params["url"])
    except:
            pass
    try:
            name=unque(params["name"])
    except:
            pass
    try:
            iconimage=unque(params["iconimage"])
    except:
            pass
    try:        
            mode=int(params["mode"])
    except:
            pass
    try:        
            fanart=unque(params["fanart"])
    except:
            pass
    try:        
            description=unque(params["description"])
    except:
            pass
    try:
        video_info=unque(params["video_info"])
    except:
            pass
    try:
        id=(params["id"])
    except:
            pass
            
    try:
        next_page=unque(params["next_page"])
    except:
            pass
            
    log.warning('Mode:'+str(mode))

    if mode==None or url==None or len(url)<1:
            main_menu()
    elif mode==1:
        from resources.modules.hebdub_movies import get_dub
        get_dub(url,sys_arg_1_data=sys_arg_1_data)
        
    elif mode==2:
        from resources.modules.kidstv import get_links
        get_links(sys_arg_1_data=sys_arg_1_data)
        
    elif mode==4:
        import datetime
        from resources.modules.kidstv import Trailer_Youtube
        now = datetime.datetime.now()
        #link_url='https://www.youtube.com/results?sp=CAI%253D&q=%22%D7%98%D7%A8%D7%99%D7%99%D7%9C%D7%A8+%D7%9E%D7%93%D7%95%D7%91%D7%91%22+' + str(now.year)
        link_url='https://www.youtube.com/results?search_query={0}+%22%D7%98%D7%A8%D7%99%D7%99%D7%9C%D7%A8+%D7%9E%D7%93%D7%95%D7%91%D7%91%22&sp=CAI%253D'.format(str(now.year))
       
        Trailer_Youtube(link_url,now,sys_arg_1_data=sys_arg_1_data)
        
    elif mode==5:
        play_link(name,url,video_info,id,iconimage,fanart,description)
    elif mode==6:
        from resources.modules.hebdub_movies import update_now
        from resources.modules.kidstv import update_now_tv
        if url=='movie':
            update_now(progress=True)
        elif url=='tv':
            update_now_tv(progress=True)
        else:
            update_now(progress=True)
            update_now_tv(progress=True)
    elif mode==7:
        
        save_fav(name,url,iconimage,fanart,description,video_info)
    elif mode==8:
        show_fav()
    elif mode==9:
        remove_fav(name,url,iconimage,fanart,description,video_info)
    elif mode==10:
        heb_mov_dub(url,description)
    elif mode==11:
        heb_mov_letter(iconimage,fanart)
    elif mode==12:
        heb_mov_dub_letter(name,url)
    elif mode==13:
        heb_tv_dub(url)
        
    elif mode==14:
        heb_tv_letter(iconimage,fanart)
    elif mode==15:
        heb_tv_dub_letter(name,url)
    elif mode==16:
        random_tv(sys_arg_1_data)
    elif mode==17:
        random_movie()
    elif mode==35:
        ClearCache()
    elif mode==46:
        from resources.modules.kidstv_season import get_seasons
        get_seasons(name,url,iconimage,fanart,description,int(next_page),sys_arg_1_data=sys_arg_1_data)
    elif mode==47:
        check_times(name,video_info)
    elif mode==48:
        sync_firebase()
    elif mode==49:
        
        search_entered=''
        keyboard = xbmc.Keyboard(search_entered, 'Enter Search')
        keyboard.doModal()
        if keyboard.isConfirmed() :
               search_entered = (keyboard.getText().replace("'","%27"))
               if search_entered!='':
                  
                  search_result(search_entered)
        
    elif mode==50:
        import datetime
        from resources.modules.kidstv import Trailer_Youtube
        now = datetime.datetime.now()
        link_url='https://www.youtube.com/results?search_query={0}+פרק &sp=CAI%253D'.format(name)
        
        Trailer_Youtube(link_url,now)
    elif mode==51:
        
        from resources.modules.kidstv import channel_Youtube
        channel_Youtube(url,iconimage,fanart,sys_arg_1_data=sys_arg_1_data)
    elif mode==52:
        youtubemenu()
        
    elif mode==53:
        
        from resources.modules.kidstv import channel_Youtube_videos
        channel_Youtube_videos(url,iconimage,fanart,next_page,sys_arg_1_data=sys_arg_1_data)
        
    elif mode==54:
        small_kids()
    elif mode==55:
        from resources.modules.kidstv import channel_Youtube_videos_autoplay
        channel_Youtube_videos_autoplay(url,iconimage,fanart,next_page,sys_arg_1_data=sys_arg_1_data)
    elif mode==56:
        clear_telemdia()
    elif mode==57:
        search_result('מדובב',dubbed=True)
    elif mode==58:
        update_library()
    elif mode==59:
        latest_movies()
    xbmcplugin.setContent(int(sys_arg_1_data), 'movies')


    xbmcplugin.endOfDirectory(int(sys_arg_1_data),cacheToDisc=True)

