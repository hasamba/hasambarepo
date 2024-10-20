# -*- coding: utf-8 -*-
from resources.modules import log
import logging,re,os,sys,urllib,json,xbmcplugin,requests,xbmc
import  threading,xbmcaddon,xbmcgui
from resources.modules.addall import addLink,addDir3,addNolink
Addon = xbmcaddon.Addon()
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database
__BASENICKJADD__= 'https://nickjr.walla.co.il/'
__BASE_URL_NICK__ = 'https://nick.walla.co.il/'
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
import xbmc
import xbmcvfs
from urllib.parse import parse_qsl
xbmc_tranlate_path=xbmcvfs.translatePath
user_dataDir_pre = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
global all_data_you
all_data_you=[]
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
if KODI_VERSION<=18:
    que=urllib.quote_plus
    url_encode=urllib.urlencode
else:
    que=urllib.parse.quote_plus
    url_encode=urllib.parse.urlencode
if KODI_VERSION>=17:
 
  domain_s='https://'
elif KODI_VERSION<17:
  domain_s='http://'
dir_path = os.path.dirname(os.path.realpath(__file__))
mypath=os.path.join(dir_path,'..\solvers')
sys.path.append(mypath)
mypath=os.path.join(dir_path,'..\done')
sys.path.append(mypath)
from resources.modules.addall import addDir3,addLink
user_dataDir=os.path.join(user_dataDir_pre,'cache_f','ghost')
user_dataDir2=os.path.join(user_dataDir_pre,'cache_f','avegner')
user_dataDir3=os.path.join(user_dataDir_pre,'cache_f','ghk')
if not os.path.exists(user_dataDir):
    os.makedirs(user_dataDir)
if not os.path.exists(user_dataDir2):
    os.makedirs(user_dataDir2)
def download_file(url,path):
    local_filename =os.path.join(path, "fixed_list.txt")
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

def unzip(file,dest):
    
    from zipfile import ZipFile
    
    
    zip_file = file
    ptp = 'Masterpenpass'
    zf=ZipFile(zip_file)
    #zf.setpassword(bytes(ptp))
    #with ZipFile(zip_file) as zf:
    zf.extractall(dest)

def renew_data(path,l_list):


    download_file(l_list,path)

    unzip(os.path.join(path, "fixed_list.txt"),path)

    return 'ok'
def gdecom(url):

    import StringIO ,gzip
    compressedFile = StringIO.StringIO()
    compressedFile.write(url.decode('base64'))
    # # Set the file's current position to the beginning
    # of the file so that gzip.GzipFile can read
    # its contents from the top.
    # 
    compressedFile.seek(0)
    return  gzip.GzipFile(fileobj=compressedFile, mode='rb').read()
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

global all_dub,all_dub2,all_dub3,all_dub4,all_dub5,all_dub6,all_dub7
all_dub=[]
all_dub2=[]
all_dub3=[]
all_dub4=[]
all_dub5=[]
all_dub6=[]
all_dub7=[]
try:
    import xbmc
    addonInfo = xbmcaddon.Addon().getAddonInfo
    dataPath = xbmc_tranlate_path(addonInfo('profile')).decode('utf-8')
except:
  
    dataPath = os.path.dirname(os.path.realpath(__file__))
images_file = os.path.join(dataPath, 'images_file_nick.txt')
def getData(url):
 headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'TE': 'Trailers',
 }
 try:
        
            x=requests.get(url,headers=headers).content
           
            
            

            return 'true', x
 except Exception as e:
    xbmc.sleep(100)
    
    x=requests.get(url,headers=headers).content
           
            
            
    log.warning(str(e))
    return 'true', x
    

    
    
    
def clean(contentType, name):
    return name
    try:
         
        if isinstance(name, str):
         
            if contentType.lower().find('utf-8') == -1: 
            
                name = name.decode('windows-1255', 'replace')
                name = name.encode('utf-8')
        elif isinstance(name, unicode):
            name = name.encode('utf-8')    
 
    except Exception as e:
        
         raise e
#     if (name):
#         cleanName = name.replace("&quot;", "\"").replace("&#39;", "'").replace("&nbsp;", " ")
#         return  cleanName
    return name
def ghk_new():
    global all_dub
    log.warning('get GhostK')
    import cache
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    
    l_list='https://raw.githubusercontent.com/moshep15/back/master/onlykids.txt'
    #l_list=Addon.getSetting("ghaddr").decode('base64')
    cacheFile=os.path.join(user_dataDir3,'localfile.txt')
    if not os.path.exists(cacheFile):
       
        download_file(l_list,user_dataDir3)

        unzip(os.path.join(user_dataDir3, "fixed_list.txt"),user_dataDir3)

    else:

        all_img=cache.get(renew_data,1,user_dataDir3,l_list, table='posters')
    
    


    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM MyTable where REPLACE(father,' ','')=REPLACE('[B][COLOR orange]ילדים[/B][/COLOR][B]סדרות לילדים מדובבים[/B]',' ','') or  REPLACE(father,' ','')=REPLACE('[B][COLOR orange]ילדים[/B][/COLOR][B]סדרות נוסטלגיה לילדים[/B]',' ','')")
    match = dbcur.fetchall()
    

    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        data=data.replace('%27',"'")
        try:
            f_link=gdecom(f_link)
        except:
           pass
    
            
        all_dub.append((name,f_link,icon,fanart,plot,'[[GhostK]]'))
    return all_dub
def NickJr():
 
    global all_dub
    #tv_mode=__settings__.getSetting(id = 'deviceId')
    all_dub=[]
    list=[]
    url='http://nickjr.walla.co.il/'
    #r = requests.get(url)
    contentType, page = getData(url+'tvshows')
    matches1 = re.compile('desktop&quot;:5(.*?)</section>',re.DOTALL).findall(page)

    match=re.compile('<a href="/(.*?)".*?<img src="(.*?)".*?cd-title>(.*?)<').findall(matches1[0])

            
    for link,image,name in match:

      if __BASENICKJADD__ not in link:
       link=__BASENICKJADD__+link
      #contentType, page = getData(link)
      #matche = re.compile('<div class="top_stripe_div".+?<img src="(.+?)">').findall(page)
      #if (len(matche)>0):
      # image=matche[0]
      #else:

      if '///' in image:
       image_fixed='http:' +image
      else:
       image_fixed='http:/' +image

      list.append((link,name))
      
      all_dub.append((clean(contentType,name),link,image_fixed,image_fixed,clean(contentType,name),'[[nickjr]]'))
    return all_dub
def getMatches(url, pattern):

 try:
        contentType, page = getData(url)
        matches = re.compile(pattern).findall(page)
        return contentType, matches 
 except Exception as e:
   
   log.warning(str(e))
 
   pass
def GetlistMatch():
    
    list=[]

    contentType,block = getMatches(__BASE_URL_NICK__+'tvshows','desktop&quot;:5(.*?)</section>')
    page = re.compile('<a href="/(.*?)".*?<img src="(.*?)".*?cd-title>(.*?)<').findall(block[0])

    for path in page:
                
                summary = ''
                url=__BASE_URL_NICK__ + path[0]
            
                iconImage='http:' + path[1]
                title=path[2]
               
                list.append((clean(contentType,title),__BASE_URL_NICK__ + path[0],iconImage))
                
    return list
def nicolodiaon():
            global all_dub2
            list2=[]
            names=[]
            all_dub2=[]
  
           
            matches_list=GetlistMatch()
     
    
            for items in matches_list:
               list2.append(items[1])
               names.append(items[0])
              
               all_dub2.append((items[0], items[1], items[2], items[2], '','[[Nicolodian]]'))
            
            return all_dub2
def html_decode(s):
   
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('-','&#8211;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s
def get_youtube_data(link_url,xxx):
   global all_data_you
   contentType, page = getData(link_url)

   matche = re.compile('yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix(.+?)</div></div></div>',re.DOTALL).findall(page)
   for links in matche:
    link=re.compile('<a href="(.+?)"').findall(links)
    name=re.compile('title="(.+?)"').findall(links)
    
    

    link[0]=link[0][9:]

    name_final=name[0]
    if "Watch Later" in name[0]:
       name_final=name[1]
    if "Queue" in name[1]:
       name_final=name[2]


    image=re.compile('<img.+?"https:(.+?)"',re.DOTALL).findall(links)
    all_data_you.append((name_final,link[0],image[0],xxx))
    
def results_Youtube(link_url,pages=False):
   import time,xbmcgui
   global all_data_you
   start_time=time.time()
   if Addon.getSetting("dp")=='true':
                dp = xbmcgui.DialogProgress()
                dp.create("טוען סרטים", "אנא המתן", '')
                dp.update(0)
   all_data_you=[]
   #tv_mode=__settings__.getSetting(id = 'deviceId')
  

   thread=[]
   x=0
   regex='page=(.+?)$'
   page_no=int(re.compile(regex).findall(link_url)[0])
   xxx=0
   for page in range(page_no,page_no+2):
        link=(link_url.split('page=')[0])+'page='+str(page)
        get_youtube_data(link,xxx)
        #thread.append(Thread(get_youtube_data,link_url,xxx))
        #thread[len(thread)-1].setName('עמוד ' + str(page))
        xxx+=1
   '''
   for td in thread:
        td.start()

        if Addon.getSetting("dp")=='true':
                elapsed_time = time.time() - start_time
                dp.update(0, ' מפעיל '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),td.name)
        #if len(thread)>38:
        xbmc.sleep(25)
   while 1:
          
          still_alive=0
          all_alive=[]
          for yy in range(0,len(thread)):
            
            if  thread[yy].is_alive():
              all_alive.append(thread[yy].name)
              still_alive=1
          if Addon.getSetting("dp")=='true':
                elapsed_time = time.time() - start_time
                dp.update(0, ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),','.join(all_alive))
          if still_alive==0:
            break
          xbmc.sleep(100)

   '''
   all_data_you=sorted(all_data_you, key=lambda x: x[3], reverse=False)
   for name_final,link,image,xxx in all_data_you:
       video_data={}
       video_data['title']=html_decode(name_final)
       video_data['icon']='https:'+image
       video_data['fanart']='https:'+image
       video_data['plot']=html_decode(name_final)+'-HebDub-'
       nm=html_decode(name_final)
       addLink(nm,'https://www.youtube.com/watch?v='+link,5,False,'https:'+image,'https:'+image,html_decode(name_final),video_info=json.dumps(video_data),original_title=nm)
   if pages:
        regex='page=(.+?)$'
        match=re.compile(regex).findall(link_url)
        link=link_url.split('page=')[0]
        
        addDir3('[COLOR aqua][I]עוד תוצאות[/I][/COLOR]'.decode('utf8'),link+'page='+str(int(match[0])+2),117,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTNmz-ZpsUi0yrgtmpDEj4_UpJ1XKGEt3f_xYXC-kgFMM-zZujsg','https://cdn4.iconfinder.com/data/icons/arrows-1-6/48/1-512.png','עוד תוצאות'.decode('utf8'))
def Trailer_Youtube(link_url,now,sys_arg_1_data=""):
  
   import datetime
   
   #tv_mode=__settings__.getSetting(id = 'deviceId')
   list=[]
   names=[]
   
   x=0
   all_d=[]
   
   contentType, page = getData(link_url)

   matche = re.compile('ytInitialData = (.+?)};',re.DOTALL).findall(page.decode('utf-8'))
  
   all_j=json.loads(matche[0]+'}')
   for items in all_j['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']:
    if 'videoRenderer' not in items:
        continue
    name=items['videoRenderer']['title']['runs'][0]['text']
    link=items['videoRenderer']['videoId']
    image=items['videoRenderer']['thumbnail']['thumbnails'][0]['url']
    
    
    x=x+1

    name_final=name

    
    list.append(link)
    names.append(html_decode(name_final))
    
    video_data={}
    video_data['title']=html_decode(name_final)
    video_data['icon']='https:'+image
    video_data['fanart']='https:'+image
    video_data['plot']=html_decode(name_final)+'-HebDub-'
  
    all_d.append(addLink(html_decode(name_final),'https://www.youtube.com/watch?v='+link,5,False,image,image,html_decode(name_final),video_info=json.dumps(video_data)))
   
   log.warning('all_d:'+str(len(all_d)))
   xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_d,len(all_d))
def channel_Youtube_videos(link_url,icon,image,next_page,sys_arg_1_data=""):
    o_image=image
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://youtubemultidownloader.net',
        'Connection': 'keep-alive',
        'Referer': 'https://youtubemultidownloader.net/channel.html',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    params = (
        ('url', link_url+'/videos'),
        ('nextPageToken', next_page),
    )
    log.warning(link_url+'/videos')
    log.warning(next_page)
    r = requests.get('https://api.youtubemultidownloader.com/playlist', headers=headers, params=params).json()
    all_d=[]
    for itt in r['items']:
        image=itt['thumbnails']
        video_data={}
        video_data['title']=itt['title']  
        video_data['icon']=image
        video_data['fanart']=image
        video_data['plot']=itt['title']+'-HebDub-'
        link=itt['url']
        all_d.append(addLink(itt['title'].encode('utf-8',errors='ignore'),link,5,False,image,image,itt['title'].encode('utf-8',errors='ignore'),video_info=json.dumps(video_data)))
   
    all_d.append(addDir3('[COLOR lightblue][I][B]עמוד הבא[/B][/I][/COLOR]',link_url,53,icon,o_image,'YOUTUBE',next_page=r['nextPageToken']))
    xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_d,len(all_d))
def channel_Youtube_videos_autoplay(link_url,icon,image,next_page):
    import random
    o_image=image
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://youtubemultidownloader.net',
        'Connection': 'keep-alive',
        'Referer': 'https://youtubemultidownloader.net/channel.html',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    num_pages=int(Addon.getSetting("number_of_pages"))
    for i in range(0,3):
        params = (
            ('url', link_url+'/videos'),
            ('nextPageToken', next_page),
        )
        
        r = requests.get('https://api.youtubemultidownloader.com/playlist', headers=headers, params=params).json()
        all_d=[]
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        counter=0
        all_lists=[]
        for itt in r['items']:
            image=itt['thumbnails']
            video_data={}
            video_data['title']=itt['title']  
            video_data['icon']=image
            video_data['fanart']=image
            video_data['plot']=itt['title']+'-HebDub-'
            link=itt['url']
            #all_d.append(addLink(itt['title'].encode('utf-8',errors='ignore'),link,5,False,image,image,itt['title'].encode('utf-8',errors='ignore'),video_info=json.dumps(video_data)))
            link='plugin://plugin.video.kids_new/?mode=5&description=%s&url=%s&iconimage=%s&fanart=%s&video_info={"fanart": "%s", "plot": "%s", "icon": "%s", "title": "%s"}&mode=5&id= &name=%s'%(' ',que(link),image,image,image,' ',image,itt['title'].replace("'",'%27'),itt['title'].replace("'",'%27'))
            listItem = xbmcgui.ListItem(itt['title'], path=link) 
            listItem.setInfo(type='Video', infoLabels=video_data)
            playlist.add(url=link,listitem=listItem)
            all_lists.append(link)
            
            counter+=1
        next_page=r['nextPageToken']
        
        playlist.shuffle()
    #rand=random.randint(0,len(all_lists)-1)
    #all_lists_fix=all_lists[rand]
    #listItem = xbmcgui.ListItem('Playlist', path=all_lists_fix) 
    #listItem.setInfo(type='Video', infoLabels=video_data)
    #ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=all_lists_fix)
def channel_Youtube(link_url,icon,image,sys_arg_1_data=""):
  
   import datetime
   
   #tv_mode=__settings__.getSetting(id = 'deviceId')
   list=[]
   names=[]
   
   x=0
   all_d=[]
   all_d.append(addDir3('[COLOR khaki][B]כל הסרטונים[/B][/COLOR]',link_url,53,icon,image,'YOUTUBE'))
   all_d.append(addLink('[COLOR khaki][B]נגן אקראי[/B][/COLOR]',link_url,55,False,icon,image,'YOUTUBE'))
   xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_d,len(all_d))
   contentType, page = getData(link_url)
   if KODI_VERSION<19:
       matche = re.compile('ytInitialData = (.+?)};',re.DOTALL).findall(page)
   else:
       matche = re.compile('ytInitialData = (.+?)};',re.DOTALL).findall(page.decode('utf-8'))
  
   all_j=json.loads(matche[0]+'}')
   
   for items in all_j['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents']:
    if 'itemSectionRenderer' not in items:
        continue
    if 'shelfRenderer' not in items['itemSectionRenderer']['contents'][0]:
        continue
    if KODI_VERSION<19:
        name=items['itemSectionRenderer']['contents'][0]['shelfRenderer']['title']['runs'][0]['text'].encode('utf8')
    else:
        name=items['itemSectionRenderer']['contents'][0]['shelfRenderer']['title']['runs'][0]['text']
    addNolink( '[COLOR lightblue][I]'+name+'[/I][/COLOR]', 'www',999,False, iconimage=icon,fan=image)
    
    
    
    all_d=[]
    if 'horizontalListRenderer' not in (items['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']):
        continue
    for itt in items['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['horizontalListRenderer']['items']:
        if 'gridVideoRenderer' not in itt:
            continue
        it2=itt['gridVideoRenderer']
        if KODI_VERSION<19:
            name_final=it2['title']['simpleText'].encode('utf8')
        else:
            name_final=it2['title']['simpleText']
        #image=it2['richThumbnail']['movingThumbnailRenderer']['movingThumbnailDetails']['thumbnails'][0]['url']
        image=it2['thumbnail']['thumbnails'][0]['url']
        all_img=it2['thumbnail']['thumbnails']
        max_res=0
        for itt_img in all_img:
            if itt_img['width']>max_res:
                image=itt_img['url']
        #log.warning(image)
        link=it2['videoId']
        
       
        
        
    

        

        
        list.append(link)
        names.append(html_decode(name_final))
        
        video_data={}
        video_data['title']=html_decode(name_final)
        video_data['icon']=image
        video_data['fanart']=image
        video_data['plot']=html_decode(name_final)+'-HebDub-'
        if KODI_VERSION<19:
            all_d.append(addLink(html_decode(name_final).encode('utf-8',errors='ignore'),'https://www.youtube.com/watch?v='+link,5,False,image,image,html_decode(name_final),video_info=json.dumps(video_data)))
        else:
            all_d.append(addLink(html_decode(name_final),'https://www.youtube.com/watch?v='+link,5,False,image,image,html_decode(name_final),video_info=json.dumps(video_data)))
    
    xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_d,len(all_d))
  
def get_youtube_lists_little():
  global all_dub3
  list=[]
  list2=[]
  names=[]
  names2=[]
  all_dub3=[]
  Addon = xbmcaddon.Addon()

  addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
  tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
  tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
  dbcon = database.connect(tmdb_cacheFile)
  dbcur = dbcon.cursor()
  dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT,""fanart TEXT,""plot TEXT);"% 'youtbe_little')

  try:
        dbcur.execute("VACUUM 'AllData';")
        dbcur.execute("PRAGMA auto_vacuum;")
        dbcur.execute("PRAGMA JOURNAL_MODE=MEMORY ;")
        dbcur.execute("PRAGMA temp_store=MEMORY ;")
  except:
   pass
  dbcon.commit()
    
  #tv_mode=__settings__.getSetting(id = 'deviceId')

  
  f_path=os.path.join(dir_path,'youtube_playlist_little.html')
  playlists= open(f_path,'r').read()
 
  
  youtube_playlists = re.compile('List"(.+?)"EndList').findall(playlists)
  
 
  x=0
  for link in  youtube_playlists:

    dbcur.execute("SELECT * FROM youtbe_little WHERE link = '%s'"%(link))

    match = dbcur.fetchone()
    if match==None:
      
      
        try:
          
          contentType, page = getData(link)
        
          matche = re.compile('<div class="playlist-info">.+?<ul class="playlist-details">',re.DOTALL).findall(page)
         
          matches = re.compile('data-sessionlink="ei=(.+?)" >(.+?)</a>').findall(matche[0])
          
          matches3 = re.compile('data-thumbnail-url="(.+?).:?(jpg|png)').findall(page)
          names.append(html_decode(matches[0][1]))
        
          list.append(link)
          dbcur.execute("INSERT INTO youtbe_little Values ('%s', '%s', '%s', '%s','%s');" %  (html_decode(matches[0][1]).replace("'"," "),link,matches3[0][0]+"."+matches3[0][1],matches3[0][0]+"."+matches3[0][1],html_decode(matches[0][1]).replace("'"," ")))
          dbcon.commit()
          video_data={}
          video_data['title']=html_decode(matches[0][1])
          video_data['icon']=matches3[0][0]+"."+matches3[0][1]
          video_data['fanart']=matches3[0][0]+"."+matches3[0][1]
          video_data['plot']=html_decode(matches[0][1])
         
          addDir3(html_decode(matches[0][1]),'[[youtube]]'+link,46,matches3[0][0]+"."+matches3[0][1],matches3[0][0]+"."+matches3[0][1],html_decode(matches[0][1]),video_info=video_data)
          
          
          
        except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            
            log.warning('ERROR IN KIDSTV play:'+str(lineno))
            log.warning('inline:'+line)
            log.warning(e)
            log.warning(link)
           
    else:
      name,link,icon,image,plot=match
     
      video_data={}
      video_data['title']=name
      video_data['icon']=icon
      video_data['fanart']=image
      video_data['plot']=plot
     
      addDir3(name,'[[youtube]]'+link,46,icon,image,plot,video_info=video_data)
  dbcur.close()
  dbcon.close()
  return all_dub3
def get_youtube_lists():
  log.warning('get_youtube_lists')
  global all_dub3
  list=[]
  list2=[]
  names=[]
  names2=[]
  all_dub3=[]
  Addon = xbmcaddon.Addon()
  try:
    from sqlite3 import dbapi2 as database
  except:
    from pysqlite2 import dbapi2 as database
  addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
  tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
  tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
  dbcon = database.connect(tmdb_cacheFile)
  dbcur = dbcon.cursor()
  dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT,""fanart TEXT,""plot TEXT);"% 'youtbe')

  try:
        dbcur.execute("VACUUM 'AllData';")
        dbcur.execute("PRAGMA auto_vacuum;")
        dbcur.execute("PRAGMA JOURNAL_MODE=MEMORY ;")
        dbcur.execute("PRAGMA temp_store=MEMORY ;")
  except:
   pass
  dbcon.commit()
    
  #tv_mode=__settings__.getSetting(id = 'deviceId')

  
  f_path=os.path.join(dir_path,'youtube_playlist.html')
  playlists= open(f_path,'r').read()
 
  
  youtube_playlists = re.compile('List"(.+?)"EndList').findall(playlists)
  
 
  x=0
  for link in  youtube_playlists:

    dbcur.execute("SELECT * FROM youtbe WHERE link = '%s'"%(link))

    match = dbcur.fetchone()
    if match==None:
      
      
        try:
          log.warning('Youtube:'+link)
          contentType, page = getData(link)
        
          matche = re.compile('<div class="playlist-info">.+?<ul class="playlist-details">',re.DOTALL).findall(page)
         
          matches = re.compile('data-sessionlink="ei=(.+?)" >(.+?)</a>').findall(matche[0])
          
          matches3 = re.compile('data-thumbnail-url="(.+?).:?(jpg|png)').findall(page)
          names.append(html_decode(matches[0][1]))
        
          list.append(link)
          dbcur.execute("INSERT INTO youtbe Values ('%s', '%s', '%s', '%s','%s');" %  (html_decode(matches[0][1]).replace("'"," "),link,matches3[0][0]+"."+matches3[0][1],matches3[0][0]+"."+matches3[0][1],html_decode(matches[0][1]).replace("'"," ")))
          dbcon.commit()
          all_dub3.append((html_decode(matches[0][1]),link,matches3[0][0]+"."+matches3[0][1],matches3[0][0]+"."+matches3[0][1],html_decode(matches[0][1]),'[[youtube]]'))
          
        except Exception as e:
          log.warning( 'ERROR ' + link)
          log.warning( e)
    else:
      name,link,icon,image,plot=match
      all_dub3.append((name,link,icon,image,plot,'[[youtube]]'))
  dbcur.close()
  dbcon.close()
  return all_dub3

def Sdarot_Tv():
    from resources.modules.sdarot import resolve_dns
    global all_dub4
    all_dub4=[]
    all_names=[]
    import requests
    from resources import API
    POSTER_PREFIX='https://static.sdarot.website/series/'
    
    all_generes=['38','7','44','75']
    all_ge_name=['ילדים','אנימציה','נוער','מדובב']
    for items in all_generes:
        counter=0
        while(counter<10):
            
            try:
                req,cookie_new = resolve_dns(API + '/series/list/{0}/page/0/perPage/100'.format(items)).get()
                break
            except Exception as e:
                log.warning('Error from Sdarot:'+str(e))
                xbmc.sleep(100)
                log.warning(API + '/series/list/{0}/page/0/perPage/100'.format(items))
            counter+=1
            
        
        req=json.loads(req)
        
        #log.warning(a)
        if req['series']==None:
            log.warning('Error in Series:'+API + '/series/list/{0}/page/0/perPage/100'.format(items))
            continue
        #log.warning(req)
        log.warning(len(req['series']))
        for s in req['series']:
                if KODI_VERSION<19:
                    label = (s['heb'].encode('utf-8'))
                else:
                    label = s['heb']
                if  'מדובב' in label:
                    add_dis='[COLOR yellow] מדובב[/COLOR]\n'
                else:
                    add_dis=''
                
                all_dub4.append((label,s['id'],POSTER_PREFIX + s['poster'],POSTER_PREFIX + s['poster'],add_dis+s['description'],'[[Sdarot]]'))
                all_names.append(s['id'])
        for pages in range(1,int(req['pages']['totalPages'])):
            counter=0
            while(counter<10):
                
                try:
                    req,cookie_new = resolve_dns(API + '/series/list/{0}/page/{1}/perPage/100'.format(items, str(pages))).get()
                    break
                except Exception as e:
                    log.warning('Error from Sdarot pages:'+str(e))
                    xbmc.sleep(100)
                    log.warning(API + '/series/list/{0}/page/{1}/perPage/100'.format(items, str(pages)))
                counter+=1
            
            req=json.loads(req)
            if 'series' not in req:
                continue
            if req['series']==None:
                continue
            for s in req['series']:
                if KODI_VERSION<19:
                    label = (s['heb'].encode('utf-8'))
                else:
                    label = s['heb']
            
            
                
                if  'מדובב' in label:
                    add_dis='[COLOR yellow] מדובב[/COLOR]\n'
                else:
                    add_dis=''
                
                all_dub4.append((label,s['id'],POSTER_PREFIX + s['poster'],POSTER_PREFIX + s['poster'],add_dis+s['description'],'[[Sdarot]]'))
                all_names.append(s['id'])
              
    
    return all_dub4
def get_aven():
    global all_dub7
    
    import cache
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    

   
    l_list='https://raw.githubusercontent.com/kodimen/Steve-Rogers/master/%D7%94%D7%A0%D7%95%D7%A7%D7%9D%20%D7%94%D7%A8%D7%90%D7%A9%D7%95%D7%9F.txt'
    cacheFile=os.path.join(user_dataDir2,'localfile.txt')
    if not os.path.exists(cacheFile):
       
        download_file(l_list,user_dataDir2)

        unzip(os.path.join(user_dataDir2, "fixed_list.txt"),user_dataDir2)

    else:

        all_img=cache.get(renew_data,1,user_dataDir2,l_list, table='posters')
    
    


    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM MyTable where REPLACE(father,' ','')=REPLACE('[B][COLOR deepskyblue] הנוקם הראשון סדרות בתרגום מובנה [/COLOR][/B]סדרות מדובבות לילדים',' ','')")
    match = dbcur.fetchall()

    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        data=data.replace('%27',"'")
        try:
            f_link=gdecom(f_link)
        except:
           pass
    
            
        all_dub7.append((name,f_link,icon,fanart,plot,'[[Aven]]'))
    return all_dub7
def get_ghost():
    global all_dub6

    import cache
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    
    #l_list='https://files.fm/pa/moshep1977/upload/1.txt'
    l_list=Addon.getSetting("ghaddr").decode('base64')
    cacheFile=os.path.join(user_dataDir,'localfile.txt')
    if not os.path.exists(cacheFile):
       
        download_file(l_list,user_dataDir)

        unzip(os.path.join(user_dataDir, "fixed_list.txt"),user_dataDir)

    else:

        all_img=cache.get(renew_data,1,user_dataDir,l_list, table='posters')
    
    


    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM MyTable where REPLACE(father,' ','')=REPLACE('[B][COLOR orange]ילדים[/B][/COLOR][B]סדרות לילדים מדובבים[/B]',' ','')")
    match = dbcur.fetchall()

    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        data=data.replace('%27',"'")
        try:
            f_link=gdecom(f_link)
        except:
           pass
    
            
        all_dub6.append((name,f_link,icon,fanart,plot,'[[Ghost]]'))
    return all_dub6
def get_small():
    global all_dub5
    import requests
    all_dub5=[]
    headers= {
                                
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language': 'en-US,en;q=0.5',
                                'Connection': 'keep-alive',
                                'Upgrade-Insecure-Requests': '1',
                            }
    html=requests.get('https://hatzerim.wordpress.com/',headers=headers).content.decode('utf-8')
    regex='<li id="menu-item-.+?" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-.+?"><a href="(.+?)">(.+?)<|<li id="menu-item-.+?" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-.+?"><a href="(.+?)">(.+?)<'
    match=re.compile(regex).findall(html)
    image_all={}
    from resources.modules.image_small import images_all
    for topic_link,topic_name,link,name in match:
      if len (topic_link)>0:
        topic_name=topic_name
      else:
          image=''
          if 0:
            x=0
            html2=requests.get(link).content
            regex2='<meta property="og:image" content="(.+?)"'
            match2=re.compile(regex2).findall(html2)
            image=match2[0]
            
            image_all[name.encode('utf8')]=image
          if name in images_all:
            image=images_all[name]
          if KODI_VERSION<19:
            name=html_decode(name.decode('utf-8')).encode('utf-8')
          all_dub5.append((name,link,image,image,name,'[[Small]]'))
    return all_dub5
def get_anime(link_o,search_entered=''):
    try:
      link_o=int(link_o)
    except:
       link_o=0

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.anime-spin.net/%D7%A6%D7%A4%D7%99%D7%99%D7%94/',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Accept-Encoding':'utf-8',

        'Cache-Control': 'no-cache',
    }
    
    x=requests.get('https://www.anime-spin.net/%D7%A6%D7%A4%D7%99%D7%99%D7%94/',headers=headers)
    regex='name="csrf-token" content="(.+?)"'
    match=re.compile(regex).findall(x.content)
    cook=(x.cookies)
    if search_entered!='':
        data = [
          ('token', match[0]),
          ('text', search_entered),
          
        ]

        response = requests.post('https://www.anime-spin.net/ajax/search', headers=headers, data=data,cookies=cook).text
        r=response.decode('unicode_escape').replace('\/','/')
        
        regex='a href="(.+?)".+?img src="(.+?)".+?<span class="data">(.+?)<'
        match=re.compile(regex,re.DOTALL).findall(r)

     
        for link,image,name in match:
            video_data={}
            video_data['title']=name
            video_data['icon']=image
            video_data['fanart']=image
            video_data['plot']=name
            
            addDir3(name,'[[anime]]'+link.encode('utf8'),46,image,image,name,video_info=video_data)
    else:
        data = [
          ('token', match[0]),
          ('type', 'popular'),
          ('from', link_o),
          ('limit', '18'),
        ]

        response = requests.post('https://www.anime-spin.net/ajax/watchFilters', headers=headers, data=data,cookies=cook).text
        r=response.decode('unicode_escape').replace('\/','/')#.replace('\u003C','<').replace('\u003E','>').replace('/\\','/').replace('\/','/').replace('\\"','"')
        regex_pre='<div class="item"(.+?)</div>'
        match_pre=re.compile(regex_pre,re.DOTALL).findall(r)
   
        for items in match_pre:
            
            regex='img src="(.+?)".+?a href="(.+?)".+?<h3>(.+?)</h3>.+?<h4>(.+?)</h4>'
            match=re.compile(regex,re.DOTALL).findall(items)

          
            for image,link,name,plot in match:
                video_data={}
                video_data['title']=name
                video_data['icon']=image
                video_data['fanart']=image
                video_data['plot']=plot
                
                addDir3(name,'[[anime]]'+link.encode('utf8'),46,image,image,plot,video_info=video_data)
        addDir3('[COLOR aqua][I]עמוד הבא[/I][/COLOR]',str(int(link_o)+18),52,' ',' ',' ')
def update_now_tv(progress=False):

    import time
    from time import gmtime, strftime
    import datetime
    import _strptime
    from datetime import datetime
    
    
    
    
    
    if (progress):
        import xbmcgui
        dp = xbmcgui . DialogProgress ( )
        if KODI_VERSION<19:
            dp.create('אנא המתן','מעדכן סדרות', '','')
            dp.update(0, 'אנא המתן','מעדכן סדרות', '' )
        else:
            dp.create('אנא המתן','מעדכן סדרות'+'\n'+ ''+'\n'+'')
            dp.update(0, 'אנא המתן'+'\n'+'מעדכן סדרות'+'\n'+ '' )
    global all_dub,all_dub2,all_dub3,all_dub4,all_dub5,all_dub6,all_dub7
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    start_time=time.time()

    
    

    thread=[]
    search_entered=''
    if search_entered=='youtube only':
        thread.append(Thread(get_youtube_lists))
    else:
        #thread.append(Thread(NickJr))
        #thread.append(Thread(nicolodiaon))
        #thread.append(Thread(get_youtube_lists))
        #thread[len(thread)-1].setName('youtube')
        thread.append(Thread(Sdarot_Tv))
        thread[len(thread)-1].setName('Sdarot')
        thread.append(Thread(get_small))
        thread[len(thread)-1].setName('small')
        #thread.append(Thread(get_ghost))
        #thread.append(Thread(get_aven))

   
    for td in thread:
          td.start()
    if (progress):
        elapsed_time = time.time() - start_time
        if KODI_VERSION<19:
            dp.update(0, 'אנא המתן','מעדכן סדרות',time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+ '\nמתחיל סריקה' )
        else:
            dp.update(0, 'אנא המתן'+'\n'+'מעדכן סדרות'+'\n'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+ '\nמתחיל סריקה' )
    while 1:

        
        for threads in thread:
       
            still_alive=0
            all_alive=[]
            all_d=0
            for yy in range(0,len(thread)):
                    if thread[yy].is_alive():
                      all_alive.append(thread[yy].getName())
                      still_alive=1
                    else:
                        all_d+=1
        if still_alive==0:
          break
        if (progress):
            elapsed_time = time.time() - start_time
            if KODI_VERSION<19:
                dp.update(int(((all_d* 100.0)/(len(thread))) ), 'אנא המתן',time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), ','.join(all_alive))
            else:
                dp.update(int(((all_d* 100.0)/(len(thread))) ), 'אנא המתן'+'\n'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+ ','.join(all_alive))
        xbmc.sleep(1000)
    if (progress):
            dp.close()
    log.warning('all_dub:'+str(len(all_dub)))
    log.warning('all_dub2:'+str(len(all_dub2)))
    log.warning('all_dub3:'+str(len(all_dub3)))
    log.warning('all_dub4:'+str(len(all_dub4)))
    log.warning('all_dub5:'+str(len(all_dub5)))
    log.warning('all_dub6:'+str(len(all_dub6)))
    log.warning('all_dub7:'+str(len(all_dub7)))
    all_data_tog=all_dub+all_dub2+all_dub3+all_dub4+all_dub5+all_dub6+all_dub7
    
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT, ""image TEXT,""plot TEXT,""origin TEXT);"% 'kids_show')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""date TEXT,""type TEXT);" % 'updated')
    dbcur.execute("DELETE FROM kids_show")
    dbcon.commit()
    for name1,link,icon,image,plot,origin in all_data_tog:
       if KODI_VERSION<19:
           dbcur.execute("INSERT INTO %s Values (?,?,?,?,?,?)" % 'kids_show', (name1.decode('utf8'),link.decode('utf8'),icon.decode('utf8'),image.decode('utf8'),plot.decode('utf8'),origin.decode('utf8')))
       else:
           dbcur.execute("INSERT INTO %s Values (?,?,?,?,?,?)" % 'kids_show', (name1,link,icon,image,plot,origin))
    dbcur.execute("DELETE FROM updated  where type='tv'")
    
    
    # datetime object containing current date and time
    now = datetime.now()
    a = now.strftime('%H:%M:%S %d/%m/%Y')
    dbcur.execute("INSERT INTO updated Values ('%s','%s')"%(str(a),'tv'))
    
    dbcon.commit()
    
    
    
    
    all_links={}
    all_names=[]
    count=0
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    
    
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT,""fanart TEXT,""plot TEXT,""video_data TEXT);"% 'kids_show_orginized')
    
    
    dbcur.execute("DELETE FROM kids_show_orginized")
    dbcon.commit()
    dbcur.execute("SELECT * FROM kids_show ")

    match = dbcur.fetchall()
    xx=0
    for name1,link,icon,image,plot,origin in match:
          if (progress):
              if KODI_VERSION<19:
                  dp.update(int(((xx* 100.0)/(len(match))) ), 'אנא המתן','אוסף', name1 )
              else:
                  dp.update(int(((xx* 100.0)/(len(match))) ), 'אנא המתן'+'\n'+'אוסף'+'\n'+ name1 )
              xx+=1
          check=True
          if search_entered=='youtube only':
             check=False
             if origin=='[[youtube]]':
               check=True
          add_l=''
          if KODI_VERSION<19:
              if 'מדובב'.decode('utf-8') in name1 and 'Sdarot' in origin:
                add_l='מדובב'
              name1=html_decode(name1.replace('מדובב','').replace('*','').replace(':','').replace('-','').strip()).decode('utf-8')#.replace('מדובב','').replace('*','').replace(':','').replace('-','')
          else:
              if 'מדובב' in name1 and 'Sdarot' in origin:
                add_l='מדובב'
              name1=html_decode(name1.replace('מדובב','').replace('*','').replace(':','').replace('-','').strip())#.replace('מדובב','').replace('*','').replace(':','').replace('-','')
          origin_n=origin.replace('[','').replace(']','')
          if name1 not in all_links:
   
             all_names.append(name1)
             all_links[name1]={}
             all_links[name1]['icon']=icon
             all_links[name1]['image']=image
             all_links[name1]['plot']=plot
  
             all_links[name1]['link']=origin+link+add_l
             all_links[name1]['origin']=origin_n
          else:
               if link not in all_links[name1]['link']:
                 if '$$$' in link:
                      links=link.split('$$$')
                      for link in links:
                        all_links[name1]['link']=all_links[name1]['link']+'$$$'+origin+link+add_l
                 else:
                   all_links[name1]['link']=all_links[name1]['link']+'$$$'+origin+link+add_l
                 all_links[name1]['origin']=all_links[name1]['origin']+','+origin_n
    xx=0
    all_l=[]
    for items in all_links:
        if (progress):
              if KODI_VERSION<19:
                dp.update(int(((xx* 100.0)/(len(match))) ), 'אנא המתן','אוסף2', items )
              else:
                  dp.update(int(((xx* 100.0)/(len(match))) ), 'אנא המתן'+'\n'+'אוסף2'+'\n'+ items )
              xx+=1
        link=all_links[items]['link']
        icon=all_links[items]['icon']
        image=all_links[items]['image']
        plot=all_links[items]['plot']
        origin=all_links[items]['origin']
        video_data={}
        video_data['title']=items
        video_data['icon']=icon
        video_data['fanart']=image
        video_data['plot']='--[COLOR lightblue]'+origin+'[/COLOR]-- \n '+plot
        video_data['fast']=1
        dbcur.execute("INSERT INTO %s Values (?,?,?,?,?,?)" % 'kids_show_orginized', (items,link,icon,image,'--[COLOR lightblue]'+origin+'[/COLOR]--\n '+plot,json.dumps(video_data)))
        #all_l.append(addDir3(items,link,46,icon,image,'--[COLOR lightblue]'+origin+'[/COLOR]--\n '+plot,video_info=video_data))
        
    dbcon.commit()
    dbcur.close()
    dbcon.close()
    #update_library()
    log.warning('Done Updating')
    if progress:
        xbmc.executebuiltin('Container.Refresh')
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kids new', 'הכל עודכן')))
def get_background_data():
    log.warning('background')
    global all_dub,all_dub2,all_dub3,all_dub4,all_dub5,all_dub6,all_dub7
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    
    log.warning('Waiting for play')
    
    while 1:
        if  xbmc.Player().isPlaying() :
            if  xbmc.Player().getTime()>10:
                break
        xbmc.sleep(100)
    log.warning('Done Waiting')
    thread=[]
    search_entered=''
    if search_entered=='youtube only':
        thread.append(Thread(get_youtube_lists))
    else:
        #thread.append(Thread(NickJr))
        #thread.append(Thread(nicolodiaon))
        thread.append(Thread(get_youtube_lists))
        thread.append(Thread(Sdarot_Tv))
        thread.append(Thread(get_small))
        #thread.append(Thread(get_ghost))
        #thread.append(Thread(get_aven))

   
    for td in thread:
          td.start()
    
    while 1:

    
        for threads in thread:
       
            still_alive=0
            for yy in range(0,len(thread)):
                    if thread[yy].is_alive():
                      
                      still_alive=1
        if still_alive==0:
          break
        xbmc.sleep(1000)
    log.warning('all_dub:'+str(len(all_dub)))
    log.warning('all_dub2:'+str(len(all_dub2)))
    log.warning('all_dub3:'+str(len(all_dub3)))
    log.warning('all_dub4:'+str(len(all_dub4)))
    log.warning('all_dub5:'+str(len(all_dub5)))
    log.warning('all_dub6:'+str(len(all_dub6)))
    log.warning('all_dub7:'+str(len(all_dub7)))
    all_data_tog=all_dub+all_dub2+all_dub3+all_dub4+all_dub5+all_dub6+all_dub7
    
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT, ""image TEXT,""plot TEXT,""origin TEXT);"% 'kids_show')
    dbcur.execute("DELETE FROM kids_show")
    for name1,link,icon,image,plot,origin in all_data_tog:
       dbcur.execute("INSERT INTO %s Values (?,?,?,?,?,?)" % 'kids_show', (name1.decode('utf8'),link.decode('utf8'),icon.decode('utf8'),image.decode('utf8'),plot.decode('utf8'),origin.decode('utf8')))
    dbcur.execute("DELETE FROM updated  where type='tv'")
    from time import gmtime, strftime
    a=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    dbcur.execute("INSERT INTO updated Values ('%s','%s')"%(str(a),'tv'))
    dbcon.commit()
    dbcur.close()
    dbcon.close()
    log.warning('Done Updating')
def get_background_data_tr_tv():
        log.warning('Starting Thread Update TV')
        thread=[]
        thread.append(Thread(get_background_data))
        thread[0].start()
        return 'OK'
def update_library():
    import datetime
    
    user_path=xbmc_tranlate_path(Addon.getSetting('library.movie'))
    base_tv_path=os.path.join(user_path,'strm','tv')
    log.warning('base_tv_path:'+base_tv_path)
     

    strm='plugin://plugin.video.kids_new/?mode=46&name=%s&url=%s&iconimage=%s&fanart=%s&description=%s&id=%s&video_info=%s'
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database

    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    
    dbcur.execute("SELECT * FROM kids_show_orginized ORDER BY name ASC")
    match = dbcur.fetchall()
    
    dbcur.close()
    dbcon.close()
    new_items=[]
    
                
    count=0
    import codecs
    tmdbid="0" 


    # datetime object containing current date and time
    now = datetime.datetime.now()
    date_added=now.strftime("%Y-%m-%d %H:%M:%S")
    for name ,link,icon, image,plot,data in match:
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
                tv_path=os.path.join(base_tv_path,c_title)
                if not os.path.exists(tv_path):
                    os.makedirs(tv_path)
     
                path=tv_path
                strm_path=os.path.join(tv_path,c_title)
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
                file = codecs.open(os.path.join(tv_path, c_title+'.nfo'), "w", "utf-8")

                file.write(final)
                file.close()
    
                file = open(strm_path+'.strm', "w")

                file.write(new_strm)
                file.close()
                
                
    xbmc.executebuiltin('UpdateLibrary(video)')
    
    
def get_links(search_entered='',sys_arg_1_data=""):
    import xbmcgui,cache
    log.warning('start')
    if Addon.getSetting("kids_dp")=='true':
            dp = xbmcgui . DialogProgress ( )
            dp.create('אנא המתן','טוען', '','')
            dp.update(0, 'אנא המתן','טוען', '' )
    thread=[]
    #thread.append(Thread(get_background_data))
    #thread[0].start()
    
   
    #get_background_data()
    all_links={}
    all_names=[]
    count=0
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT,""fanart TEXT,""plot TEXT,""origin TEXT);"% 'kids_show')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""date TEXT,""type TEXT);" % 'updated')
    try:
            dbcur.execute("VACUUM 'kids_show';")
            dbcur.execute("PRAGMA auto_vacuum;")
            dbcur.execute("PRAGMA JOURNAL_MODE=MEMORY ;")
            dbcur.execute("PRAGMA temp_store=MEMORY ;")
    except:
       pass
    dbcon.commit()
    dbcur.execute("SELECT * FROM kids_show ")

    match = dbcur.fetchall()
    xx=0
    for name1,link,icon,image,plot,origin in match:
          if Addon.getSetting("kids_dp")=='true':
              dp.update(int(((xx* 100.0)/(len(match))) ), 'אנא המתן','אוסף', name1 )
              xx+=1
          check=True
          if search_entered=='youtube only':
             check=False
             if origin=='[[youtube]]':
               check=True
          add_l=''
          if 'מדובב' in name1 and 'Sdarot' in origin:
            add_l='מדובב'
            
          name1=html_decode(name1.replace('מדובב','').replace('*','').replace(':','').replace('-','').strip()).decode('utf-8')#.replace('מדובב','').replace('*','').replace(':','').replace('-','')
          origin_n=origin.replace('[','').replace(']','')
          if name1 not in all_links:
   
             all_names.append(name1)
             all_links[name1]={}
             all_links[name1]['icon']=icon
             all_links[name1]['image']=image
             all_links[name1]['plot']=plot
  
             all_links[name1]['link']=origin+link+add_l
             all_links[name1]['origin']=origin_n
          else:
               if link not in all_links[name1]['link']:
                 if '$$$' in link:
                      links=link.split('$$$')
                      for link in links:
                        all_links[name1]['link']=all_links[name1]['link']+'$$$'+origin+link+add_l
                 else:
                   all_links[name1]['link']=all_links[name1]['link']+'$$$'+origin+link+add_l
                 all_links[name1]['origin']=all_links[name1]['origin']+','+origin_n
    xx=0
    all_l=[]
    for items in all_links:
        if Addon.getSetting("kids_dp")=='true':
              dp.update(int(((xx* 100.0)/(len(match))) ), 'אנא המתן','אוסף2', items )
              xx+=1
        link=all_links[items]['link']
        icon=all_links[items]['icon']
        image=all_links[items]['image']
        plot=all_links[items]['plot']
        origin=all_links[items]['origin']
        video_data={}
        video_data['title']=items
        video_data['icon']=icon
        video_data['fanart']=image
        video_data['plot']='--[COLOR lightblue]'+origin+'[/COLOR]-- \n '+plot
        video_data['fast']=1
        if search_entered=='' or search_entered=='youtube only':
          all_l.append(addDir3(items,link,46,icon,image,'--[COLOR lightblue]'+origin+'[/COLOR]--\n '+plot,video_info=video_data))
        else:
          if search_entered in items:
            all_l.append(addDir3(items,link,46,icon,image,'--[COLOR lightblue]'+origin+'[/COLOR]--\n '+plot,video_info=video_data))
    if Addon.getSetting("kids_dp")=='true':
        dp.close()





    xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_l,len(all_l))
    xbmcplugin.addSortMethod(int(sys_arg_1_data), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
    xbmcplugin.addSortMethod(int(sys_arg_1_data), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    xbmcplugin.addSortMethod(int(sys_arg_1_data), xbmcplugin.SORT_METHOD_DATEADDED)
    xbmcplugin.addSortMethod(int(sys_arg_1_data), xbmcplugin.SORT_METHOD_VIDEO_RATING)
    xbmcplugin.setContent(int(sys_arg_1_data), 'movies')
    xbmcplugin.endOfDirectory(int(sys_arg_1_data))
    dbcur.close()
    dbcon.close()
    all_img=cache.get(get_background_data_tr_tv,24, table='posters')

    
  
    