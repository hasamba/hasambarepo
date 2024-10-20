# -*- coding: utf-8 -*-
from resources.modules import log
import logging,re,os,sys,urllib,json,xbmcplugin,requests,xbmcgui
import  threading,xbmcaddon
from resources.modules.addall import addLink,addDir3
__BASENICKJADD__= 'https://nickjr.walla.co.il/'
__BASE_URL_NICK__ = 'https://nick.walla.co.il/'
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
import xbmc
import xbmcvfs
from urllib.parse import parse_qsl
xbmc_tranlate_path=xbmcvfs.translatePath

KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
if KODI_VERSION>=17:
 
  domain_s='https://'
elif KODI_VERSION<17:
  domain_s='http://'
from resources.modules.kidstv import html_decode
dir_path = os.path.dirname(os.path.realpath(__file__))
mypath=os.path.join(dir_path,'..\solvers')
sys.path.append(mypath)
mypath=os.path.join(dir_path,'..\done')
sys.path.append(mypath)

Addon = xbmcaddon.Addon()
user_dataDir_pre = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
#from pen_addons import download_file,unzip,gdecom
global all_ep
all_ep=[]
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
def read_firebase(table_name):
    from resources.modules.firebase import firebase
    firebase = firebase.FirebaseApplication('https://%s.firebaseio.com'%Addon.getSetting("firebase"), None)
    result = firebase.get('/', None)
    if table_name in result:
        return result[table_name]
    else:
        return {}
        
class Thread(threading.Thread):
    def __init__(self, target, *args):
       
        self._target = target
        self._args = args
        
        
        threading.Thread.__init__(self)
        
    def run(self):
        
        self._target(*self._args)

global all_season,all_season2,all_season3,all_season4,all_season5,all_season6
all_season=[]
all_season2=[]
all_season3=[]
all_season4=[]
all_season5=[]
all_season6=[]
try:
    import xbmc
    addonInfo = xbmcaddon.Addon().getAddonInfo
    dataPath = xbmc_tranlate_path(addonInfo('profile')).decode('utf-8')
except:
  
    dataPath = os.path.dirname(os.path.realpath(__file__))
images_file = os.path.join(dataPath, 'images_file_nick.txt')

user_dataDir=os.path.join(user_dataDir_pre,'cache_f','ghost')
user_dataDir2=os.path.join(user_dataDir_pre,'cache_f','avegner')

if not os.path.exists(user_dataDir):
    os.makedirs(user_dataDir)
if not os.path.exists(user_dataDir2):
    os.makedirs(user_dataDir2)
def get_sdarot_season(link,icon,image,plot_o,page=0):
    global all_ep
    from resources import API
    regex='--(.+?)--'
    m=re.compile(regex).findall(plot_o)
    if len(m)>0:
        plot_o=plot_o.replace(m[0],'')
    
    from resources.modules.sdarot import resolve_dns
    add_n=''
    log.warning('Sdarot:'+link)
    if 'מדובב' in link or 'בבודמ' in link:
        add_n='[COLOR lightblue][I] מדובב [/I][/COLOR]'
        link=link.replace('מדובב','').replace('בבודמ','')
    url=API+'/series/info/'+link
    req,cookie_new = resolve_dns(url).get()
    req=json.loads(req)

    if req['serie']['episodes']==None:
        return ''
    
    x=page*50
    max_x=x+50
    count=0
    log.warning('max_x:'+str(max_x))
    for se in (req['serie']['episodes']):
      season=se
      
      
      for ep in req['serie']['episodes'][se]:
            count+=1
            if count>=x:
                f_link=json.dumps([link,season,ep['episode']])
               
                all_season.append(('עונה %s פרק %s'%(season,ep['episode']),f_link))
                plot=plot_o+'-HebDub-'
                video_data={}
                video_data['title']=add_n+'עונה %s פרק %s'%(season,ep['episode'])
                video_data['icon']=icon
                video_data['fanart']=image
                video_data['plot']=plot+'-sdarot--KIDSSECTION-'
                all_ep.append((add_n+'עונה %s פרק %s'%(season,ep['episode']),f_link,icon,image,plot+'-sdarot--KIDSSECTION-',(video_data),'Sdarot',season,ep['episode']))
            
            
            
            if count>=max_x:
                 log.warning('Break count')
                 all_ep.append(('עמוד הבא',str(page+1),icon,image,plot+'-sdarot--KIDSSECTION-',(video_data),'Sdarot',season,ep['episode']))
                 break
      if count>=max_x:
        break
    return all_season
def get_small(link,icon,image,plot_o):
    global all_ep
    regex='--(.+?)--'
    m=re.compile(regex).findall(plot_o)
    if len(m)>0:
        plot_o=plot_o.replace(m[0],'')
    
    html=requests.get(link).content
    
    regex='<h.+?><.+?>(.+?)<.+?href="(.+?)"'
    match=re.compile(regex).findall(html)
    for name,link in match:
      name=html_decode(name.decode('utf-8')).encode('utf-8')
      name=name.replace('<span style="color:#99cc00;">','')
      
      plot=plot_o+'-HebDub-'
      video_data={}
      video_data['title']=name
      video_data['icon']=icon
      video_data['fanart']=image
      video_data['plot']=plot
      if '<ul>' not in name:
        all_ep.append((name,link, image,image,plot+'-KIDSSECTION-',(video_data),'Small','%20','%20'))
        #addLink( name, link,5,False, image,image,plot+'-KIDSSECTION-',video_info=json.dumps(video_data),dont_earse=True)
def getLink(inUrl):
       #try:
        import random
        from kidstv import getData
        
        servers = ['62.90.90.37', '31.168.228.117', '82.80.192.28', '31.168.228.126', '82.80.192.2', '31.168.228.113']
        
        contentType,mainPage = getData(inUrl)
        match = re.compile("data-player='(.*?)' data-adscontrol").findall(mainPage)
        result = json.loads(match[0])
        if result['vimmeId'] is None:
            id = result['id'][:-2].zfill(5)
            link = 'http://{0}/walla_vod/_definst_/mp4:media/0{1}/{2}/{3}-40.mp4/playlist.m3u8'.format(random.choice(servers), id[:2], id[2:], result['id'])
        else:
            link = 'http://{0}/walla_vod/_definst_/amlst:{1}.High.smil/playlist.m3u8'.format(random.choice(servers), result['vimmeId'])
       
        return link
def get_nickjr(url,icon,image,plot_o):
    from kidstv import getData
   
    __BASE_URL_NICK__ = 'https://nick.walla.co.il/'
    
    contentType, page = getData(url)
    
    matches = re.compile('/TVEpisode.*?href="(.*?)".*?:&quot;(.*?)&quot;.*?src="(.*?)".*?title>(.*?)</span>',re.DOTALL).findall(page)
                                                
    for link, description, image, name in matches:
     
      link = '{0}{1}'.format(__BASE_URL_NICK__[:-1], link)
      if len(name)>100:
        name="No Name"
      iconImage = 'http:' + image
      

     
      plot=plot_o+'-HebDub-'
      video_data={}
      video_data['title']=name
      video_data['icon']=iconImage
      video_data['fanart']=image
      video_data['plot']=plot
      
      addLink( name, link,5,False,iconImage,iconImage,plot+'-KIDSSECTION-',video_info=json.dumps(video_data),dont_earse=True,kids_movies=True)
    
    regex= '<section class="fc common-section grid-1" > <section class="sequence common-items (five-in-row|not-carousel)"(.*?)</section>'
    match=re.compile(regex,re.DOTALL).findall(page)
    if len(match)==0:
      xbmcgui.Dialog().ok('Error occurred','מצטערים אין פרקים לסדרה זו')
      sys.exit()
    urlMatch=re.compile('<a href="/(.*?)"').findall(match[0][1])

    if len (urlMatch)>0:
      
        contentType, page = getData(__BASENICKJADD__+urlMatch[0])
    
        matches = re.compile('/TVEpisode.*?href="(.*?)".*?:&quot;(.*?)&quot;.*?src="(.*?)".*?title>(.*?)</span>',re.DOTALL).findall(page)
                                                    
        for link, description, image, name in matches:

          link = '{0}{1}'.format(__BASE_URL_NICK__[:-1], link)
          if len(name)>100:
            name="No Name"
          iconImage = 'http:' + image
          

          
         
          plot=plot_o+'-HebDub-'
          video_data={}
          video_data['title']=name
          video_data['icon']=iconImage
          video_data['fanart']=image
          video_data['plot']=plot
          addLink( name,  link,5,False,iconImage,iconImage,plot+'-KIDSSECTION-',video_info=json.dumps(video_data),dont_earse=True,kids_movies=True)
def get_nicolodian(inUrl,icon,image,plot_o):
     from kidstv import getMatches,getData
     __BASE_URL_NICK__ = 'https://nick.walla.co.il/'
     nextPage_number=10
     current_page=1
     list=[]
     list_name=[]
     inUrl=inUrl.replace('tvshow','item')
     while nextPage_number > current_page:
      
      if not 'page' in inUrl:
            
            contentType,block = getMatches(inUrl, '<section class="fc common-section grid-1" > <section class="sequence common-items (five-in-row|not-carousel)"(.*?)</section>')
            urlMatch=re.compile('<a href="/(.*?)"').findall(block[0][1])
            if (len(urlMatch)) < 1:
                return
            inUrl=__BASE_URL_NICK__+urlMatch[0]

      
        
        
      contentType,mainPage = getData(inUrl.replace('" rel="next',''))
      urls = re.compile('/TVEpisode.*?href="(.*?)".*?:&quot;(.*?)&quot;.*?src="(.*?)".*?title>(.*?)</span>').findall(mainPage)
      num_live=0
      for url, description, image, title in urls:
            
            url = '{0}{1}'.format(__BASE_URL_NICK__[:-1], url)
            iconImage = 'http:{0}'.format(image)
          
       
            num_live+=1
            #url = getLink(url)
            #url = 'http://62.90.90.56/walla_vod/_definst_/mp4:media/0' + id[:2] + '/' + id[2:] + '/' + vidid + '-40.mp4/playlist.m3u8'
            
            plot=plot_o+'-HebDub-'
            video_data={}
            video_data['title']=title
            video_data['icon']=iconImage
            video_data['fanart']=image
            video_data['plot']=plot
            addLink( title,  url,5,False,iconImage,iconImage,plot+'-KIDSSECTION-',video_info=json.dumps(video_data),dont_earse=True,kids_movies=True)
      
      nav = re.compile('class="pager"(.*?)</nav>').findall(mainPage)
      if len(nav) > 0:
            pages = re.compile('href="(.*?)" class="(.*?)"').findall(nav[0])
         
            if len(pages) > 0 and pages[-1][1] == 'icon-right'  :
                inUrl= pages[-1][0]
                current_page=current_page+1
            else:
              break
      else:
        break
      xbmc.sleep(100)
def get_aven(name,url,icon,image,plot):
    global all_ep
    regex='--(.+?)--'
    m=re.compile(regex).findall(plot)
    if len(m)>0:
        plot=plot.replace(m[0],'')
    plot='[COLOR lightblue]Aven[/COLOR]\n'+plot
    import cache
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    
    
    l_list='https://raw.githubusercontent.com/kodimen/Steve-Rogers/master/%D7%94%D7%A0%D7%95%D7%A7%D7%9D%20%D7%94%D7%A8%D7%90%D7%A9%D7%95%D7%9F.txt'
    cacheFile=os.path.join(user_dataDir2,'localfile.txt')
    
    


    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    try:
        dbcur.execute("SELECT * FROM MyTable where replace(replace(replace(replace(replace(father,'-',''),':',''),'*',''),'מדובב',''),' ','')  like replace(replace(replace(replace(replace('%{0}%','-',''),':',''),'*',''),'מדובב',''),' ','') and type='item'".format('[B][COLOR deepskyblue] הנוקם הראשון סדרות בתרגום מובנה [/COLOR][/B]סדרות מדובבות לילדים'+name.replace("'",'%27')))
        
        match = dbcur.fetchall()
    except:
        download_file(l_list,user_dataDir2)

        unzip(os.path.join(user_dataDir2, "fixed_list.txt"),user_dataDir2)
        dbcur.execute("SELECT * FROM MyTable where replace(replace(replace(replace(replace(father,'-',''),':',''),'*',''),'מדובב',''),' ','')  like replace(replace(replace(replace(replace('%{0}%','-',''),':',''),'*',''),'מדובב',''),' ','') and type='item'".format('[B][COLOR deepskyblue] הנוקם הראשון סדרות בתרגום מובנה [/COLOR][/B]סדרות מדובבות לילדים'+name.replace("'",'%27')))
        log.warning('הנוקם הראשון סדרות בתרגום מובנהסדרות מדובבות לילדים'+name.replace("'",'%27'))
        match = dbcur.fetchall()
    log.warning('All results')
    log.warning(len(match))
    
    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        plot='[COLOR lightblue]Aven[/COLOR]\n'+plot
        data=data.replace('%27',"'")
        try:
            f_link=gdecom(f_link)
        except:
           pass
   
        
        if len(data)<10:
            data={}
      
            data['title']=name
            data['plot']=plot
            
        try:
            aa=json.loads(data)
            season=aa['Season']
            episode=aa['Episode']
            txt='[COLOR lightblue][I] מדובב [/I][/COLOR]'+'עונה %s פרק %s'%(season,episode)
            data={}
           
            data['title']=txt
            data['plot']=plot
            
        except:
            data=data.replace('[',' ').replace(']',' ').replace('	','').replace("\\"," ").replace(': """",',': "" "",').replace(': """"}',': "" ""}').replace(': "",',': " ",').replace(': ""}',': " "}').replace('""','"').replace('\n','').replace('\r','')
            try:
                aa=json.loads(data)
                
                season=aa['Season']
                episode=aa['Episode']
                txt='[COLOR lightblue][I] מדובב [/I][/COLOR]'+'עונה %s פרק %s'%(season,episode)
                data={}
           
                data['title']=txt
                data['plot']=plot
            except Exception as e:
                
                data={}
                log.warning('shortyyyyyyyyyy')
                log.warning(str(e))
                data['title']=name
                data['plot']=plot
                txt=name
        all_ep.append((txt,f_link,icon,fanart,plot+'-KIDSSECTION-',(data),'Aven',season,episode))
        #addLink( txt,  f_link,5,False,icon,fanart,plot+'-KIDSSECTION-',video_info=json.dumps(data),dont_earse=True)
def get_ghost(name,url,icon,image,plot):
    global ep
    regex='--(.+?)--'
    m=re.compile(regex).findall(plot)
    if len(m)>0:
        plot=plot.replace(m[0],'')
    plot='[COLOR lightblue]Ghost[/COLOR]\n'+plot
    import cache
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    
    #l_list='https://files.fm/pa/moshep1977/upload/1.txt'
    l_list=Addon.getSetting("ghaddr").decode('base64')
    log.warning(l_list)
    cacheFile=os.path.join(user_dataDir,'localfile.txt')
    
    


    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    try:
        dbcur.execute("SELECT * FROM MyTable where replace(replace(replace(replace(replace(father,'-',''),':',''),'*',''),'מדובב',''),' ','') like replace(replace(replace(replace(replace('%{0}%','-',''),':',''),'*',''),'מדובב',''),' ','') and type='item'".format('[B][COLOR orange]ילדים[/B][/COLOR][B]סדרות לילדים מדובבים[/B]'+name.replace("'",'%27')))
        match = dbcur.fetchall()
        
    except:
        download_file(l_list,user_dataDir)

        unzip(os.path.join(user_dataDir, "fixed_list.txt"),user_dataDir)
        dbcur.execute("SELECT * FROM MyTable where replace(replace(replace(replace(replace(father,'-',''),':',''),'*',''),'מדובב',''),' ','') like replace(replace(replace(replace(replace('%{0}%','-',''),':',''),'*',''),'מדובב',''),' ','') and type='item'".format('[B][COLOR orange]ילדים[/B][/COLOR][B]סדרות לילדים מדובבים[/B]'+name.replace("'",'%27')))
        match = dbcur.fetchall()
    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
        
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        plot='[COLOR lightblue]Ghost[/COLOR]\n'+plot
        data=data.replace('%27',"'")
        try:
            f_link=gdecom(f_link)
        except:
           pass
        try:
            aa=json.loads(data)
            season=aa['Season']
            episode=aa['Episode']
            txt='[COLOR lightblue][I] מדובב [/I][/COLOR]'+'עונה %s פרק %s'%(season,episode)
            data={}
           
            data['title']=txt
            data['plot']=plot
            
        except:
            data=data.replace('[',' ').replace(']',' ').replace('	','').replace("\\"," ").replace(': """",',': "" "",').replace(': """"}',': "" ""}').replace(': "",',': " ",').replace(': ""}',': " "}').replace('""','"').replace('\n','').replace('\r','')
            try:
                aa=json.loads(data)
                
                season=aa['Season']
                episode=aa['Episode']
                txt='[COLOR lightblue][I] מדובב [/I][/COLOR]'+'עונה %s פרק %s'%(season,episode)
                data={}
           
                data['title']=txt
                data['plot']=plot
            except Exception as e:
                
                data={}
                log.warning('shortyyyyyyyyyy')
                log.warning(str(e))
                data['title']=name
                data['plot']=plot
                txt=name
        all_ep.append((txt,f_link,icon,fanart,plot+'-KIDSSECTION-',(data),'Ghost',season,episode))
        #addLink( txt,  f_link,5,False,icon,fanart,plot+'-KIDSSECTION-',video_info=json.dumps(data),dont_earse=True)
def get_ghostK(name,url,icon,image,plot):
    global ep
    regex='--(.+?)--'
    m=re.compile(regex).findall(plot)
    if len(m)>0:
        plot=plot.replace(m[0],'')
    plot='[COLOR lightblue]Ghost[/COLOR]\n'+plot
    import cache
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    
    l_list='https://raw.githubusercontent.com/moshep15/back/master/onlykids.txt'
    #l_list=Addon.getSetting("ghaddr").decode('base64')
    log.warning(l_list)
    cacheFile=os.path.join(user_dataDir,'localfile.txt')
    
    


    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    try:
        dbcur.execute("SELECT * FROM MyTable where replace(replace(replace(replace(replace(father,'-',''),':',''),'*',''),'מדובב',''),' ','') like replace(replace(replace(replace(replace('%{0}%','-',''),':',''),'*',''),'מדובב',''),' ','') and type='item'".format('[B][COLOR orange]ילדים[/B][/COLOR][B]סדרות לילדים מדובבים[/B]'+name.replace("'",'%27')))
        
        match = dbcur.fetchall()
        
    except:
        download_file(l_list,user_dataDir)

        unzip(os.path.join(user_dataDir, "fixed_list.txt"),user_dataDir)
        dbcur.execute("SELECT * FROM MyTable where replace(replace(replace(replace(replace(father,'-',''),':',''),'*',''),'מדובב',''),' ','') like replace(replace(replace(replace(replace('%{0}%','-',''),':',''),'*',''),'מדובב',''),' ','') and type='item'".format('[B][COLOR orange]ילדים[/B][/COLOR][B]סדרות לילדים מדובבים[/B]'+name.replace("'",'%27')))
        match = dbcur.fetchall()
    
    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
        
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        plot='[COLOR lightblue]Ghost[/COLOR]\n'+plot
        data=data.replace('%27',"'")
        try:
            f_link=gdecom(f_link)
        except:
           pass
        try:
            aa=json.loads(data)
            season=aa['Season']
            episode=aa['Episode']
            txt='[COLOR lightblue][I] מדובב [/I][/COLOR]'+'עונה %s פרק %s'%(season,episode)
            data={}
           
            data['title']=txt
            data['plot']=plot
            
        except:
            data=data.replace('[',' ').replace(']',' ').replace('	','').replace("\\"," ").replace(': """",',': "" "",').replace(': """"}',': "" ""}').replace(': "",',': " ",').replace(': ""}',': " "}').replace('""','"').replace('\n','').replace('\r','')
            try:
                aa=json.loads(data)
                
                season=aa['Season']
                episode=aa['Episode']
                txt='[COLOR lightblue][I] מדובב [/I][/COLOR]'+'עונה %s פרק %s'%(season,episode)
                data={}
           
                data['title']=txt
                data['plot']=plot
            except Exception as e:
                
                data={}
                log.warning('shortyyyyyyyyyy')
                log.warning(str(e))
                data['title']=name
                data['plot']=plot
                txt=name
        log.warning(f_link)
        all_ep.append((txt,f_link,icon,fanart,plot+'-KIDSSECTION-',(data),'GhostK',season,episode))
def get_youtube(name,url,icon,image,plot_o):
   from kidstv import getData
   global all_ep
   contentType, page = getData(url)
   regex='--(.+?)--'
   m=re.compile(regex).findall(plot_o)
   if len(m)>0:
        plot_o=plot_o.replace(m[0],'')
   plot_o='[COLOR lightblue]Youtube[/COLOR]\n'+plot_o
   matche = re.compile('data-video-id="(.+?)"').findall(page)
   matche2 = re.compile('data-video-title="(.+?)"').findall(page)
   matche3 = re.compile('data-thumbnail-url="(.+?)"').findall(page)
   
   for link in  matche:
    name=matche2[matche.index(link)]
    image=matche3[matche.index(link)]
    
    name=html_decode(name)
    #log.warning(link)
    #link='https://www.youtube.com/watch?v='+link
   
    if not 'Deleted video'  in name:
     if not 'Private video' in name:
        plot=plot_o+'-HebDub-'
        video_data={}
        video_data['title']=name
        video_data['icon']=icon
        video_data['fanart']=image
        video_data['plot']=plot
        all_ep.append((name,domain_s+'www.youtube.com/watch?v='+link,image,image,plot+'-KIDSSECTION-',(video_data),'Youtube','%20','%20'))
        #addLink( name,domain_s+'www.youtube.com/watch?v='+  link,5,False,image,image,plot+'-KIDSSECTION-',video_info=json.dumps(video_data),dont_earse=True)
            
      
def get_anime(name,link,icon,image,plot):
    headers = {
            
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    html=requests.get(link,headers=headers).content
    regex_pre='<div id="sirEpItems">(.+?)</section>'
    match_pre=re.compile(regex_pre,re.DOTALL).findall(html)
    for items in match_pre:
        regex='<a href="(.+?)" class="item ep".+?img src="(.+?)".+?<h4>(.+?)</h4>'
        match=re.compile(regex,re.DOTALL).findall(items)


        for link,image,plot in match:
            
            video_data={}
            video_data['title']=plot
            
            video_data['icon']=image
            video_data['fanart']=image
            video_data['plot']=plot+'-HebDub-'
            addLink( plot,link,5,False,image,image,plot+'-HebDub--KIDSSECTION-',video_info=json.dumps(video_data),dont_earse=True,kids_movies=True)
def run_thread_links(name,link,icon,image,plot,page,sys_arg_1_data):
    log.warning('link')
    log.warning(link)
    log.warning(name)
    if '[[Sdarot]]' in link:
        get_sdarot_season(link.replace('[[Sdarot]]',''),icon,image,plot,page)
    if '[[Small]]' in link:
        get_small(link.replace('[[Small]]',''),icon,image,plot)
    if '[[nickjr]]' in link:
        get_nickjr(link.replace('[[nickjr]]',''),icon,image,plot)
    if '[[Nicolodian]]' in link:
        get_nicolodian(link.replace('[[Nicolodian]]',''),icon,image,plot)
    if '[[Ghost]]' in link:
        get_ghost(name,link.replace('[[Ghost]]',''),icon,image,plot)
    if '[[GhostK]]' in link:
        get_ghostK(name,link.replace('[[GhostK]]',''),icon,image,plot)
    if '[[Aven]]' in link:
        get_aven(name,link.replace('[[Aven]]',''),icon,image,plot)
    if '[[youtube]]' in link:
        get_youtube(name,link.replace('[[youtube]]',''),icon,image,plot)
    if '[[anime]]' in link:
        get_anime(name,link.replace('[[anime]]',''),icon,image,plot)
    xbmcplugin.addSortMethod(int(sys_arg_1_data), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
def get_all_ep(name,link,icon,image,plot,page,sys_arg_1_data):
    global all_ep
    all_ep=[]
    all_links={}
    if '$$$' in link:
      links=link.split('$$$')
      for link1 in links:
        run_thread_links(name,link1,icon,image,plot,page,sys_arg_1_data)
    else:
       run_thread_links(name,link,icon,image,plot,page,sys_arg_1_data)
    for name1,link,icon,image,plot,video_data,origin,season,episode in all_ep:
        if 'rapidv' in link:
            continue
        origin_n=origin.replace('[','').replace(']','')
        if name1 not in all_links:
   
             
             all_links[name1]={}
             all_links[name1]['icon']=icon
             all_links[name1]['image']=image
             all_links[name1]['plot']=plot
             all_links[name1]['season']=season
             all_links[name1]['episode']=episode
             all_links[name1]['link']=link
             all_links[name1]['origin']=origin_n
        else:
               if link not in all_links[name1]['link']:
                 if '$$$' in link:
                      links=link.split('$$$')
                      for link in links:
                        all_links[name1]['link']='[[%s]]'%all_links[name1]['origin']+all_links[name1]['link']+'$$$'+'[[%s]]'%origin+link
                 else:
                   all_links[name1]['link']='[[%s]]'%all_links[name1]['origin']+all_links[name1]['link']+'$$$'+'[[%s]]'%origin+link
                 all_links[name1]['origin']=all_links[name1]['origin']+','+origin_n
    
    all_w={}

    if len(Addon.getSetting("firebase"))>0:
            all_db=read_firebase('last_played_tv_seek_time')
            match=[]
            for itt in all_db:
                
                items=all_db[itt]
                all_w[items['name']]={}
                all_w[items['name']]['seek_time']=items['seek_time']
                all_w[items['name']]['total_time']=items['total_time']
    return all_links,all_w
def get_seasons(name,link,icon,image,plot,page,rand=False,sys_arg_1_data=""):
    from resources.modules import cache
    all_ep=[]
    all_d=[]
    log.warning('GET SEASON')
    log.warning(name)
    log.warning(link)
    log.warning('icon:'+icon)
    dd=[]
    dd.append((name,link,icon,image,plot))
    all_links={}
    all_links,all_w=cache.get(get_all_ep,12,name,link,icon,image,plot,page,sys_arg_1_data, table='cookies')
    log.warning('Page:'+str(page))
    
    
    
    next_page=None
    for items in all_links:
        
        link=all_links[items]['link']
        if items=='עמוד הבא':
            next_page=link
            continue
        icon=all_links[items]['icon']
        image=all_links[items]['image']
        plot=all_links[items]['plot']
        origin=all_links[items]['origin']
        season=all_links[items]['season']
        episode=all_links[items]['episode']
        video_data={}
        video_data['title']=items
        video_data['original_title']=name
        
        video_data['icon']=icon
        video_data['fanart']=image
        video_data['season']=season
        video_data['episode']=episode
        video_data['plot']='--[COLOR lightblue]'+origin+'[/COLOR]-- \n[COLOR yellow][B][I] שם הסדרה:'+name+'[/I][/B][/COLOR]\n'+plot
        video_data['fast']=1    
        video_data['tv_title']='true'
        if rand:
            return items,link,icon,image,plot,video_data
        else:
            all_d.append(addLink( items,  link,5,False,icon,image,plot,video_info=json.dumps(video_data),all_w=all_w,original_title=name))
    if next_page:
     
        for name,link,icon,image,plot in dd:
            all_d.append(addDir3('עמוד הבא',link,46,icon,image,plot,next_page=next_page))
    if not rand:
        xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_d,len(all_d))
    