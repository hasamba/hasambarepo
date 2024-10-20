# -*- coding: utf-8 -*-
from resources.modules import cache
import random,time,urllib
global all_dub,all_dub2,all_dub3,all_dub4,all_dub5,all_dub6,all_dub7,all_dub8,all_dub9,all_dub10,html_g_movie
from resources.modules import log
import  threading,xbmcplugin,sys,os,re,requests,logging,json,xbmcaddon
dir_path = os.path.dirname(os.path.realpath(__file__))
global trd_response,global_name
global_name=''
trd_response={}
import xbmc
import xbmcvfs
from urllib.parse import parse_qsl
xbmc_tranlate_path=xbmcvfs.translatePath
    
Addon = xbmcaddon.Addon()
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
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
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database
    
from resources.modules.addall import addLink
import xbmcvfs
from urllib.parse import parse_qsl
xbmc_tranlate_path=xbmcvfs.translatePath

user_dataDir_pre = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
from resources.modules.pen_addons import download_file,unzip,gdecom
base_header={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',

            'Pragma': 'no-cache',
            
           
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            }
if KODI_VERSION>=17:
 
  domain_s='https://'
elif KODI_VERSION<17:
  domain_s='http://'
all_dub=[]
all_dub2=[]
all_dub3=[]
all_dub4=[]
all_dub5=[]
all_dub6=[]
all_dub7=[]

all_dub8=[]
all_dub9=[]
all_dub10=[]

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
        
user_dataDir=os.path.join(user_dataDir_pre,'cache_f','ghost')

if not os.path.exists(user_dataDir):
    os.makedirs(user_dataDir)
user_dataDir2=os.path.join(user_dataDir_pre,'cache_f','avegner')

if not os.path.exists(user_dataDir2):
    os.makedirs(user_dataDir2)
user_dataDir3=os.path.join(user_dataDir_pre,'cache_f','orn')


if not os.path.exists(user_dataDir3):
    os.makedirs(user_dataDir3)
    
user_dataDir4=os.path.join(user_dataDir_pre,'cache_f','dragonFRD')


if not os.path.exists(user_dataDir4):
    os.makedirs(user_dataDir4)
    
user_dataDir5=os.path.join(user_dataDir_pre,'cache_f','fhd')


if not os.path.exists(user_dataDir5):
    os.makedirs(user_dataDir5)
    
user_dataDir7=os.path.join(user_dataDir_pre,'cache_f','hp')


if not os.path.exists(user_dataDir7):
    os.makedirs(user_dataDir7)
user_dataDir8=os.path.join(user_dataDir_pre,'cache_f','ghk')


if not os.path.exists(user_dataDir8):
    os.makedirs(user_dataDir8)
def renew_data(path,l_list):


    download_file(l_list,path)

    unzip(os.path.join(path, "fixed_list.txt"),path)

    return 'ok'

def fix_data(data):
    return data.replace('[',' ').replace(']',' ').replace('	','').replace("\\"," ").replace("\n"," ").replace("\r"," ").replace("\t"," ")
def get_dub_movies():
    global all_dub
    l_list='https://github.com/oren2706/Multimedialist/blob/master/hebdub%20list%20(VER_5).txt?raw=true'
    
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    
   
   
    cacheFile=os.path.join(user_dataDir3,'localfile.txt')
    if not os.path.exists(cacheFile):
       
        download_file(l_list,user_dataDir3)

        unzip(os.path.join(user_dataDir3, "fixed_list.txt"),user_dataDir3)

    else:

        all_img=cache.get(renew_data,1,user_dataDir3,l_list, table='posters')
    
    


    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM MyTable where REPLACE(father,' ','')=REPLACE('סרטים מדובבים',' ','')")
    match = dbcur.fetchall()
    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        data=data.replace('%27',"'")
        
        try:
            f_link=gdecom(f_link)
        except Exception as e:
           
           pass

    
            
        all_dub.append((name,f_link,5,'[[ON]]',icon,fanart,plot,data.replace("OriginalTitle","originaltitle")))
def get_dub_movies2():
    global all_dub2
    
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
    dbcur.execute("SELECT * FROM MyTable where  REPLACE(father,' ','') like REPLACE('%[B][COLOR orange]ילדים[/B][/COLOR][B]סרטים מדובבים לילדים[/B]%',' ','') or REPLACE(father,' ','') like REPLACE('%[B][COLOR orange]ילדים[/B][/COLOR][B]סרטים מדובבים 1[/B]%',' ','')  or REPLACE(father,' ','') like REPLACE('%[B][COLOR orange]ילדים[/B][/COLOR][B]סרטים מדובבים 2[/B]%',' ','') and type='item'")
    match = dbcur.fetchall()
 
    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        data=data.replace('%27',"'")
        try:
            f_link=gdecom(f_link)
        except:
           pass
        all_dub2.append((name,f_link,5,'[[GH]]',icon,fanart,plot,data.replace("OriginalTitle","originaltitle")))
    
def get_dub_movies3():
    global all_dub3

    l_list='https://raw.githubusercontent.com/kodimen/Steve-Rogers/master/%D7%94%D7%A0%D7%95%D7%A7%D7%9D%20%D7%94%D7%A8%D7%90%D7%A9%D7%95%D7%9F.txt'
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    
    
   
    cacheFile=os.path.join(user_dataDir2,'localfile.txt')
    if not os.path.exists(cacheFile):
       
        download_file(l_list,user_dataDir2)

        unzip(os.path.join(user_dataDir2, "fixed_list.txt"),user_dataDir2)

    else:

        all_img=cache.get(renew_data,1,user_dataDir2,l_list, table='posters')
    
    


    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM MyTable where REPLACE(father,' ','')=REPLACE('[B][COLOR deepskyblue] הנוקם הראשון סרטים בתרגום מובנה [/COLOR][/B][B][COLOR deepskyblue] עולם הילדים [/COLOR][/B]מדובבים',' ','') or REPLACE(father,' ','')=REPLACE('[B][COLOR deepskyblue] הנוקם הראשון סרטים בתרגום מובנה [/COLOR][/B][B][COLOR deepskyblue] עולם הילדים [/COLOR][/B]מדובבים HD',' ','')")
    
       
        
    match = dbcur.fetchall()
    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        data=data.replace('%27',"'")
        try:
            f_link=gdecom(f_link)
        except:
           pass
        all_dub3.append((name,f_link,5,'[[AV]]',icon,fanart,plot,data.replace("OriginalTitle","originaltitle")))
def get_dub_movies4():
    global all_dub4
 
    

    l_list='https://github.com/hpotter1234/matrix/raw/master/dubbed.txt'
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    
    
   
    cacheFile=os.path.join(user_dataDir7,'localfile.txt')
    if not os.path.exists(cacheFile):
       
        download_file(l_list,user_dataDir7)

        unzip(os.path.join(user_dataDir7, "fixed_list.txt"),user_dataDir7)

    else:

        all_img=cache.get(renew_data,1,user_dataDir7,l_list, table='posters')
    
    


    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM MyTable where type='item'")
    
       
        
    match = dbcur.fetchall()
    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        data=data.replace('%27',"'")
        try:
            f_link=gdecom(f_link)
        except:
           pass
        all_dub4.append((name,f_link,5,'[[HP]]',icon,fanart,plot,data.replace("OriginalTitle","originaltitle")))
def get_dub_movies5():
    global all_dub5
 
    

    l_list='https://raw.githubusercontent.com/moshep15/back/master/onlykids.txt'
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    
    
   
    cacheFile=os.path.join(user_dataDir8,'localfile.txt')
    if not os.path.exists(cacheFile):
       
        download_file(l_list,user_dataDir8)

        unzip(os.path.join(user_dataDir8, "fixed_list.txt"),user_dataDir8)

    else:

        all_img=cache.get(renew_data,1,user_dataDir8,l_list, table='posters')
    
    


    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM MyTable   where father like '%מדובבים%' and type='item'")
    
       
        
    match = dbcur.fetchall()
    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        data=data.replace('%27',"'")
        try:
            f_link=gdecom(f_link)
        except:
           pass
        all_dub5.append((name,f_link,5,'[[GHK]]',icon,fanart,plot,data.replace("OriginalTitle","originaltitle")))
def get_dub_movies5_dead():
        global all_dub5
        all_dub5=[]
        url=domain_s+'raw.githubusercontent.com/Jksp/jksp.repo/master/db/HebDub.json'
        html=requests.get(url).json()
        
        for item in html['movies']:
            
             
             
               name1=item
               link="https://www.rapidvideo.com/v/%s" % html['movies'][item]['video_id']
               icon=html['movies'][item]['thumb']
               image=html['movies'][item]['fanart']
               plot=html['movies'][item]['video_info']['plot']
               data={}
               
               data['title']=name1
         
               data['poster']=image
               data['plot']=plot
               data['genre']=html['movies'][item]['video_info']['genre']
               data['year']=html['movies'][item]['video_info']['year']
               
               #addLink(name1,link,5,False,icon,image,plot,video_info=data)
               all_dub5.append((name1,link,5,'[[JK]]',icon,image,plot,json.dumps(data)))
def get_dub_movies6():
    global all_dub6
    import urllib
    all_dub6=[]
    
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("path"))
    tmdb_data_dir = os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'hebdub.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM hebdub")
    match = dbcur.fetchall()

    for name,link,img,plot,cat,date_added in match:
            data={}
            name=html_decode(name)
            #name=replaceHTMLCodes(name)
            plot=html_decode(plot)
            data['title']=name.replace('*מדובב לעברית*','').strip()

            data['poster']=img
            data['plot']=plot.replace('\n','').replace('\r','').replace('\t','').replace('"',"'").strip()
            data['dateadded']=date_added

            #addLink(name1,link,5,False,icon,image,plot,video_info=data)
            all_dub6.append((name.replace('*מדובב לעברית*','').strip(),link,5,'[[OS]]',img.encode('utf8'),img.encode('utf8'),plot.replace('\n','').replace('\r','').replace('\t','').strip(),json.dumps(data)))
    log.warning('Done 6')
def get_dub_movies9():
    global all_dub9
    import urllib
    all_dub9=[]
    
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("path"))
    tmdb_data_dir = os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'se_hebdub.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM hebdub")
    match = dbcur.fetchall()

    for name,link,img,plot,cat in match:
            data={}
            name=html_decode(name)
            #name=replaceHTMLCodes(name)
            plot=html_decode(plot)
            data['title']=name.replace('*מדובב לעברית*','').strip()

            data['poster']=img
            data['plot']=plot.replace('\n','').replace('\r','').replace('\t','').replace('"',"'").strip()


            #addLink(name1,link,5,False,icon,image,plot,video_info=data)
            all_dub9.append((name.replace('*מדובב לעברית*','').strip(),unque(link),5,'[[SE]]',img.encode('utf8'),img.encode('utf8'),plot.replace('\n','').replace('\r','').replace('\t','').strip(),json.dumps(data)))
    log.warning('Done 9')

def get_dub_movies7():
    global all_dub7
    log.warning('Dragon:'+Addon.getSetting("unfilter_test"))
    
    l_list='https://github.com/moris0371/CHICCO/raw/master/moris.txt'
    
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    
   
   
    cacheFile=os.path.join(user_dataDir4,'localfile.txt')
    if not os.path.exists(cacheFile):
       
        download_file(l_list,user_dataDir4)

        unzip(os.path.join(user_dataDir4, "fixed_list.txt"),user_dataDir4)

    else:

        all_img=cache.get(renew_data,1,user_dataDir4,l_list, table='posters')
    
    

    
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM MyTable where REPLACE(father,' ','')=REPLACE('סרטיםסרטים מדובבים',' ','')")
    match = dbcur.fetchall()
    log.warning('Dragon Found:'+str(len(match)))
    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
       
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        data=data.replace('%27',"'")
        
        
        try:
            f_link=gdecom(f_link)
        except:
           pass
        try:
            data=json.loads(data)
            data['title']=data['title'].replace(' [COLOR coral]מדובב [/COLOR]','').replace('[COLOR coral]מדובב [/COLOR]','')
            data=json.dumps(data)
        except:
            try:
                data=json.dumps(data)
            except:
                pass
            pass
            
        all_dub7.append((name.replace(' [COLOR coral]מדובב [/COLOR]','').replace('[COLOR coral]מדובב [/COLOR]',''),f_link,5,'[[Dr]]',icon,fanart,plot,data.replace("OriginalTitle","originaltitle")))
    dbcur.execute("SELECT * FROM MyTable where REPLACE(father,' ','')=REPLACE('[B][COLOR   aqua]   ילדים [/COLOR][/B][B][COLOR   aqua] סרטים לילדים ולנוער [/COLOR][/B][B][COLOR   aqua]$ סרטים מדובבים חדשים $ [/COLOR][/B]',' ','')")
    match = dbcur.fetchall()
    log.warning('Dragon Found:'+str(len(match)))
    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
       
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        data=data.replace('%27',"'")
        
        
        try:
            f_link=gdecom(f_link)
        except:
           pass
        try:
            data=json.loads(data)
            data['title']=data['title'].replace(' [COLOR coral]מדובב [/COLOR]','').replace('[COLOR coral]מדובב [/COLOR]','')
            data=json.dumps(data)
        except:
            try:
                data=json.dumps(data)
            except:
                pass
            pass
            
        all_dub7.append((name.replace(' [COLOR coral]מדובב [/COLOR]','').replace('[COLOR coral]מדובב [/COLOR]',''),f_link,5,'[[Dr]]',icon,fanart,plot,data.replace("OriginalTitle","originaltitle")))
def get_dub_movies7_old():
    global all_dub7
    if Addon.getSetting("unfilter_test") !='1122':
        return []
    l_list='http://ngarba.xyz/adds/yos/333.txt'
    log.warning('Start 7')
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    
   
   
    cacheFile=os.path.join(user_dataDir4,'localfile.txt')
    if not os.path.exists(cacheFile):
       
        download_file(l_list,user_dataDir4)

        unzip(os.path.join(user_dataDir4, "fixed_list.txt"),user_dataDir4)

    else:

        all_img=cache.get(renew_data,1,user_dataDir4,l_list, table='posters')
    
    


    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM MyTable where REPLACE(father,' ','')=REPLACE('[B][COLOR   aqua] ילדים [/COLOR][/B][B][COLOR   aqua] סרטים לילדים   [/COLOR][/B][B][COLOR   aqua] #סרטים מדובבים#   [/COLOR][/B]',' ','')")
    match = dbcur.fetchall()
    log.warning('Dragon Found:'+str(len(match)))
    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
       
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        data=data.replace('%27',"'")
        try:
            f_link=gdecom(f_link)
        except:
           pass
        try:
            data=json.loads(data)
            data['title']=data['title'].replace(' [COLOR coral]מדובב [/COLOR]','').replace('[COLOR coral]מדובב [/COLOR]','')
            data=json.dumps(data)
        except:
            try:
                data=json.dumps(data)
            except:
                pass
            pass
            
        all_dub7.append((name.replace(' [COLOR coral]מדובב [/COLOR]','').replace('[COLOR coral]מדובב [/COLOR]',''),f_link,5,'[[Dr]]',icon,fanart,plot,data.replace("OriginalTitle","originaltitle")))
        
def get_dub_movies8():
    global all_dub8

    log.warning('Source 8 Start:')
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    log.warning('Source 8 Start1:')
    #l_list='https://files.fm/pa/moshep1977/upload/1.txt'
    l_list='https://github.com/hpotter1234/new/raw/master/dubbed%20movies%20update.txt'
    cacheFile=os.path.join(user_dataDir5,'localfile.txt')
    if not os.path.exists(cacheFile):
       
        download_file(l_list,user_dataDir5)

        unzip(os.path.join(user_dataDir5, "fixed_list.txt"),user_dataDir5)

    else:

        all_img=cache.get(renew_data,1,user_dataDir5,l_list, table='posters')
    
    log.warning('Source 8 Start2:')


    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    try:
        dbcur.execute("SELECT * FROM MyTable where  REPLACE(father,' ','') like REPLACE('פוטר מדובביםמדובביםמדובבים',' ','') or  REPLACE(father,' ','') like REPLACE('פוטר מדובביםמדובביםמדובבים HD',' ','') and type='item'")
        match = dbcur.fetchall()
        log.warning('Source 8 :'+str(len(match)))
    except Exception as e:
        log.warning(e)
    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
        name=name.replace('%27',"'")
        plot=plot.replace('%27',"'")
        data=data.replace('%27',"'")
        try:
            f_link=gdecom(f_link)
        except Exception as e:
           log.warning('Error decode:'+str(e))
           pass
        all_dub8.append((name,f_link,5,'[[FH]]',icon,fanart,plot,data.replace("OriginalTitle","originaltitle")))
def get_movie_data_trd(url,tmdb_id):
    global trd_response
    headers = {
            'Accept': 'Retry-After,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            
            'Pragma': 'no-cache',
            
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        }
        
    
    response=requests.get(url,headers=headers,timeout=10)
   
    if '200' in str(response):
        trd_response[tmdb_id]=response.json()
        return response
    elif 'Retry-After' in response.headers:
      
        timeout = response.headers['Retry-After']
        
        time.sleep(int(timeout) + 1)
        return get_movie_data_trd(url,tmdb_id)
    else: 
        log.warning("error_in tmdb")
        log.warning(response.headers)
        log.warning(url)
        return tmdb_id
        
def update_now(progress=False):
    global all_dub,all_dub2,all_dub3,all_dub4,all_dub5,all_dub7,all_dub6,all_dub8,all_dub9,all_dub10,global_name
    import time
    from time import gmtime, strftime
    import datetime
    import _strptime
    from datetime import datetime
    start_time=time.time()
    
    
    
    
    if (progress):
        import xbmcgui
        dp = xbmcgui . DialogProgress ( )
        dp.create('אנא המתן','מעדכן סרטים'+'\n'+ ''+'\n'+'')
        dp.update(0, 'אנא המתן'+'\n'+'מעדכן סרטים'+'\n'+ '' )
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""con1 TEXT,""origin TEXT,""icon TEXT, ""image TEXT,""plot TEXT,""data TEXT);"% 'kids_movie')
    
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""con1 TEXT,""origin TEXT,""icon TEXT, ""image TEXT,""plot TEXT,""data TEXT);"% 'newones')

    thread=[]
    
    thread.append(Thread(get_dub_movies))
    thread[len(thread)-1].setName('ORN')
    #thread.append(Thread(get_dub_movies2))
    #thread.append(Thread(get_dub_movies3))
    thread.append(Thread(get_dub_movies4))
    thread[len(thread)-1].setName('hpotter')
    #thread.append(Thread(get_dub_movies5))
    #thread.append(Thread(get_dub_movies6))
    #thread[len(thread)-1].setName('hebdub')
    
    thread.append(Thread(get_dub_movies7))
    thread[len(thread)-1].setName('drmpon')
    #thread.append(Thread(get_dub_movies8))
    #thread.append(Thread(get_dub_movies9))
    thread[len(thread)-1].setName('se_hebdub')
    thread.append(Thread(get_telegram_movies))
    thread[len(thread)-1].setName('Telegram')
    
    for td in thread:
          td.start()
    if (progress):
        elapsed_time = time.time() - start_time
        dp.update(0, 'אנא המתן'+'\n'+'מעדכן סדרות'+'\n'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+ '\nמתחיל סריקה' )
    while 1:

    
        for threads in thread:
            all_alive=[]
            all_d=0
            still_alive=0
            for yy in range(0,len(thread)):
                    if thread[yy].is_alive():
                      all_alive.append(thread[yy].getName())
                      still_alive=1
                    else:
                        all_d+=1
            if (progress):
                elapsed_time = time.time() - start_time
                dp.update(int(((all_d* 100.0)/(len(thread))) ), 'אנא המתן'+'\n'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+ ','.join(all_alive)+', '+global_name)
            xbmc.sleep(300)
        if still_alive==0:
          break
        xbmc.sleep(100)
    log.warning('all_dub:'+str(len(all_dub)))
    #log.warning('all_dub2:'+str(len(all_dub2)))
    #log.warning('all_dub3:'+str(len(all_dub3)))
    log.warning('all_dub4:'+str(len(all_dub4)))
    #log.warning('all_dub5:'+str(len(all_dub5)))
    log.warning('all_dub6:'+str(len(all_dub6)))
    log.warning('all_dub7:'+str(len(all_dub7)))
    #log.warning('all_dub8:'+str(len(all_dub8)))
    #log.warning('all_dub9:'+str(len(all_dub9)))
    log.warning('all_dub10:'+str(len(all_dub10)))
    
    all_data_tog=all_dub+all_dub2+all_dub3+all_dub4+all_dub5+all_dub6+all_dub7+all_dub8+all_dub9+all_dub10
    '''
    for name1,link,con1,origin,icon,image,plot,data in all_data_tog:
    
        dbcur.execute("SELECT * FROM kids_movie where name='%s'"%name1)
        match = dbcur.fetchall()
        if match==None:
            dbcur.execute("INSERT INTO %s Values (?,?,?,?,?,?,?,?)" % 'newones', (name1,link,con1,origin,icon,image,plot,data))
    '''
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""date TEXT,""type TEXT);" % 'updated')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""con1 TEXT,""origin TEXT,""icon TEXT, ""image TEXT,""plot TEXT,""data TEXT);"% 'kids_movie')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT, ""image TEXT,""plot TEXT,""data TEXT,""tmdbid TEXT,""date_added TEXT);"% 'kids_movie_ordered')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""icon TEXT, ""image TEXT,""plot TEXT,""data TEXT,""tmdbid TEXT,""date_added TEXT,""year TEXT);"% 'kids_movie_year')


                                                        
    dbcur.execute("DELETE FROM kids_movie")
    dbcur.execute("DELETE FROM kids_movie_ordered")
    dbcur.execute("DELETE FROM kids_movie_year")
    for name1,link,con1,origin,icon,image,plot,data in all_data_tog:
        if KODI_VERSION<19:
            dbcur.execute("INSERT INTO %s Values (?,?,?,?,?,?,?,?)" % 'kids_movie', (name1.decode('utf-8'),link.decode('utf-8'),con1,origin.decode('utf-8'),icon.decode('utf-8'),image.decode('utf-8'),plot.decode('utf-8'),data.decode('utf-8')))
        else:
            dbcur.execute("INSERT INTO %s Values (?,?,?,?,?,?,?,?)" % 'kids_movie', (name1,link,con1,origin,icon,image,plot,data))
    dbcur.execute("DELETE FROM updated  where type='movies'")
    now = datetime.now()
    a = now.strftime('%H:%M:%S %d/%m/%Y')
    
    dbcur.execute("INSERT INTO updated Values ('%s','%s')"%(str(a),'movies'))
    dbcon.commit()
    
    
    
    
    
    
    dbcur.execute("SELECT * FROM kids_movie")
    all_l=[]
    match = dbcur.fetchall()
    all_links={}
    all_names=[]
    xx=0
    tele_source=False
    
    try:
        resuaddon=xbmcaddon.Addon('plugin.video.telemedia')
        listen_port=resuaddon.getSetting('port')
        data={'type':'checklogin',
             'info':''
             }
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        if event['status']==2 or event['status']=='Needs to log from setting':
            tele_source=False
            
        else:
            tele_source=True
    except:
        tele_source=False
    
    for name1,link,con1,origin,icon,image,plot,data in match:
      
      if 'letsupload.co' in link or 'openload.co' in link or 'sratim-il' in link:
            continue
      if '%%%TEME' in link and not tele_source:
        continue
      if 'rapidv' in link:
        continue
      if (progress):
          elapsed_time = time.time() - start_time
          dp.update(int(((xx* 100.0)/(len(match))) ), 'אנא המתן'+'\n'+'אוסף'+'\n'+ name1 )
          xx+=1
      name1=name1.strip().replace('*מדובב*','').replace('*','').replace('-',' ')
      name1=replaceHTMLCodes(name1)
      fault_data=0
      
      dd=''
      data2={}
      date_added=''
      try:
        name1=json.loads(data)['title'].replace('-',' ')
        data2=json.loads(data)
      
        if 'dateadded' in data2:
            dd=data2['dateadded']
            date_added=dd
      except Exception as e:
       
        try:
         
         data=data.replace('[',' ').replace(']',' ').replace('	','').replace("\\"," ").replace(': """",',': "" "",').replace(': """"}',': "" ""}').replace(': "",',': " ",').replace(': ""}',': " "}').replace('""','"').replace('\n','').replace('\r','')
         #name1=json.loads(data)['title'].replace('-',' ')
         
         data2=json.loads(data)
         if 'dateadded' in data2:
            dd=data2['dateadded']
            date_added=dd
         #dd=json.loads(data)['dateadded']
        except Exception as e:
         #log.warning('Error in dub2:'+str(e))
         
         fault_data=1
         pass
      
      if name1 not in all_names:
         tmdb_id=''
         try:
            data2['plot']=origin.replace('[','').replace(']','')+'\n[COLOR lightblue]'+dd+'[/COLOR]\n'+data2['plot']
            data2['title']=replaceHTMLCodes(data2['title'])
            tmdb_id=data2['tmdb']
            data=json.dumps(data2)
            date_added=dd
         except Exception as e:
            log.warning('Error Hebdub:'+str(e))
            data=json.dumps(data2)
            pass
         
         if tmdb_id==None:
            tmdb_id=''
         all_names.append(name1)
         all_links[name1]={}
         all_links[name1]['icon']=icon
         all_links[name1]['image']=image
         all_links[name1]['plot']=plot
         all_links[name1]['data']=data
         all_links[name1]['link']=origin+link
         all_links[name1]['origin']=origin.replace('[','').replace(']','')
         all_links[name1]['tmdb']=tmdb_id
         all_links[name1]['dateadded']=date_added
      else:
           if link not in all_links[name1]['link']:
             
             all_links[name1]['origin']=all_links[name1]['origin']+','+origin.replace('[','').replace(']','')
             try:
                data2['plot']=all_links[name1]['origin']+'\n[COLOR lightblue]'+dd+'[/COLOR]\n'+data2['plot']
                new_date=data2['dateadded']
                old_date=json.loads(all_links[name1]['data'])['dateadded']
                all_links[name1]['dateadded']=dd
                if new_date<old_date:
                    data2['dateadded']=json.loads(all_links[name1]['data'])['dateadded']
                    data2['plot']=data2['dateadded']+'\n'+data2['plot']
                    all_links[name1]['dateadded']=data2['dateadded']
                data=json.dumps(data2)
                
                
                all_links[name1]['data']=data
             except Exception as e:
                #log.warning('Error Hebdub:'+str(e))
                pass
             if '$$$' in link:
                  links=link.split('$$$')
                  for link in links:
                    all_links[name1]['link']=all_links[name1]['link']+'$$$'+origin+link
             else:
               all_links[name1]['link']=all_links[name1]['link']+'$$$'+origin+link
    
    xx=0
    thread=[]
    global trd_response
    trd_response={}
    
    for items in all_links:
        if (progress):
          elapsed_time = time.time() - start_time
          dp.update(int(((xx* 100.0)/(len(all_links))) ), 'אנא המתן'+'\n'+'שלב 2'+'\n'+ items )
          xx+=1
        
        link=all_links[items]['link']
        icon=all_links[items]['icon']
        image=all_links[items]['image']
        plot=all_links[items]['plot']
        data=all_links[items]['data']
        tmdb_id=all_links[items]['tmdb']
        date_added=all_links[items]['dateadded']
        if 1:
        
          if fault_data==1:
            log.warning('Fault:')
            data={}
            data['title']=items
            
            data['poster']=image
            data['Plot']=plot
          try:
            aa=json.loads(data)['title'].replace('-',' ')
          except:
            
            data={}
            data['title']=items
            
            data['poster']=image
            data['Plot']=plot
          try:
            a=int(tmdb_id)
            
            thread.append(Thread(get_movie_data_trd,'http://api.themoviedb.org/3/movie/%s?api_key=653bb8af90162bd98fc7ee32bcbbfb3d&language=he&append_to_response=external_ids'%tmdb_id,tmdb_id))
            thread[len(thread)-1].setName(tmdb_id.encode('utf8'))
                
            
              
            
            #icon='http://image.tmdb.org/t/p/original'+str(x['poster_path'])
            #image='http://image.tmdb.org/t/p/original'+str(x['backdrop_path'])
          except:
            pass
          all_l.append((items,link,icon,image,replaceHTMLCodes(plot),data,tmdb_id,date_added))
    for trd in thread:
        trd.start()
    still_alive=True
    while(still_alive):
        still_alive=False
        for thd in thread:
            
            
            if (thd.is_alive()):
                still_alive=True
                elapsed_time = time.time() - start_time
                if (progress):
                    dp.update(0, Addon.getLocalizedString(32072)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+thd.getName()+'\n'+'')
        if not still_alive:
            xbmc.sleep(100)
            break
        xbmc.sleep(100) 
    
        
    all_l=sorted(all_l, key=lambda x: x[7], reverse=False)
    for name1,link,icon,image,plot,data,tmdb_id,date_added in all_l:
        if tmdb_id in trd_response:
            icon=icon='http://image.tmdb.org/t/p/original'+str(trd_response[tmdb_id]['poster_path'])
            image='http://image.tmdb.org/t/p/original'+str(trd_response[tmdb_id]['backdrop_path'])
        if type(data)==dict:
            data=json.dumps(data)
            
        dbcur.execute("INSERT INTO %s Values (?,?,?,?,?,?,?,?)" % 'kids_movie_ordered', (name1,link,icon,image,plot,data,tmdb_id,date_added))
        if (progress):
            elapsed_time = time.time() - start_time
            dp.update(int(((xx* 100.0)/(len(all_links))) ), 'אנא המתן'+'\n'+'שומר'+'\n'+ name1 )
    for name1,link,icon,image,plot,data,tmdb_id,date_added in all_l:
        if tmdb_id in trd_response:
            icon=icon='http://image.tmdb.org/t/p/original'+str(trd_response[tmdb_id]['poster_path'])
            image='http://image.tmdb.org/t/p/original'+str(trd_response[tmdb_id]['backdrop_path'])
        year=0
        if type(data)==dict:
            try:
                year=data['year']
            except:
                pass
            data=json.dumps(data)
        else:
            try:
                d=json.loads(data)
                year=d['year']
            except:
                pass
        dbcur.execute("INSERT INTO %s Values (?,?,?,?,?,?,?,?,?)" % 'kids_movie_year', (name1,link,icon,image,plot,data,tmdb_id,date_added,year))
        if (progress):
            elapsed_time = time.time() - start_time
            dp.update(int(((xx* 100.0)/(len(all_links))) ), 'אנא המתן'+'\n'+'שומר'+'\n'+ name1 )
            
    dbcon.commit()
    dbcur.close()
    dbcon.close()
    update_library()
    if progress:
        dp.close()
        xbmc.executebuiltin('Container.Refresh')
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kids new', 'הכל עודכן')))
    log.warning('Done Update')
    
def get_background_data():
    global all_dub,all_dub2,all_dub3,all_dub4,all_dub5,all_dub7,all_dub6,all_dub8,all_dub9,all_dub10
    while 1:
        if  xbmc.Player().isPlaying() :
            if  xbmc.Player().getTime()>10:
                break
        xbmc.sleep(100)
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""con1 TEXT,""origin TEXT,""icon TEXT, ""image TEXT,""plot TEXT,""data TEXT);"% 'kids_movie')
    
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""con1 TEXT,""origin TEXT,""icon TEXT, ""image TEXT,""plot TEXT,""data TEXT);"% 'newones')
    
    log.warning('Waiting for play')
    
    
    log.warning('Done Waiting')
    thread=[]
    
    thread.append(Thread(get_dub_movies))
    thread.append(Thread(get_dub_movies2))
    #thread.append(Thread(get_dub_movies3))
    thread.append(Thread(get_dub_movies4))
    thread.append(Thread(get_dub_movies5))
    thread.append(Thread(get_dub_movies6))
    
    thread.append(Thread(get_dub_movies7))
    #thread.append(Thread(get_dub_movies8))
    #thread.append(Thread(get_dub_movies9))
    thread.append(Thread(get_telegram_movies))
    
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
    #log.warning('all_dub2:'+str(len(all_dub2)))
    #log.warning('all_dub3:'+str(len(all_dub3)))
    log.warning('all_dub4:'+str(len(all_dub4)))
    #log.warning('all_dub5:'+str(len(all_dub5)))
    log.warning('all_dub6:'+str(len(all_dub6)))
    #log.warning('all_dub7:'+str(len(all_dub7)))
    #log.warning('all_dub8:'+str(len(all_dub8)))
    #log.warning('all_dub9:'+str(len(all_dub9)))
    log.warning('all_dub10:'+str(len(all_dub10)))
    
    all_data_tog=all_dub+all_dub2+all_dub3+all_dub4+all_dub5+all_dub6+all_dub7+all_dub8+all_dub9+all_dub10
    '''
    for name1,link,con1,origin,icon,image,plot,data in all_data_tog:
    
        dbcur.execute("SELECT * FROM kids_movie where name='%s'"%name1)
        match = dbcur.fetchall()
        if match==None:
            dbcur.execute("INSERT INTO %s Values (?,?,?,?,?,?,?,?)" % 'newones', (name1,link,con1,origin,icon,image,plot,data))
    '''
    dbcur.execute("DELETE FROM kids_movie")
    for name1,link,con1,origin,icon,image,plot,data in all_data_tog:
       
       dbcur.execute("INSERT INTO %s Values (?,?,?,?,?,?,?,?)" % 'kids_movie', (name1,link,con1,origin,icon,image,plot,data))
    dbcur.execute("DELETE FROM updated  where type='movies'")
    from time import gmtime, strftime
    a=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    dbcur.execute("INSERT INTO updated Values ('%s','%s')"%(str(a),'movies'))
    dbcon.commit()
    dbcur.close()
    dbcon.close()
    
    log.warning('Done Update')
def html_decode(s):
   
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ("'", '&#039;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('-','&#8211;'),
            ('...','&#8230;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s
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
    all_f=['xvid','EVO1','EVO2','RIp','נועםם','BDRiP','x265','HeBDub',' DivX',' WS','XViD','(',')','אלירן','WEB','H264',' Br','DVDRiP','HEBDUB',' BRrip','DVDRIP','עי יוסי','נתי מ ','ע"י sagi','BDRIP','נתי ','עי אורי המלך','לולו ','כל סרט ','כ.ס ','כ ס ','נמ ','H 264','HEVC','  ','לעברית','גזלן','מדיה סנטר']

    name=name.replace(' ','.').replace('_','.').replace('-','.').replace('%20',' ').replace('5.1','').replace('AAC','').replace('2CH','').replace('.mp4','').replace('.avi','').replace('.mkv','').replace(original_title,'').replace('מדובב','').replace('גוזלן','').replace('BDRip','').replace('BRRip','')

    name=name.replace('1080p','').replace('720p','').replace('480p','').replace('360p','').replace('BluRay','').replace('ח1','').replace('ח2','').replace('נתי.מדיה','').replace('נ.מ.','').replace('..','.').replace('.',' ').replace('WEB-DL','').replace('WEB DL','').replace('נ מדיה','')

    name=name.replace('HDTV','').replace('DVDRip','').replace('WEBRip','')

    name=name.replace('דב סרטים','').replace('לולו סרטים','').replace('דב ס','').replace('()','').replace('חן סרטים','').replace('ק סרטים','').replace('חננאל סרטים','').replace('יוסי סרטים','').replace('נריה סרטים','').replace('HebDub','').replace('NF','').replace('HDCAM','').replace('@yosichen','')

    name=name.replace('BIuRay','').replace('x264','').replace('Hebdub','').replace('XviD','')

    name=name.replace('Silver007','').replace('Etamar','').replace('iSrael','').replace('DVDsot','').replace('אלי ה סרטים','').replace('PCD1','').replace('PCD2','').replace('CD1','').replace('CD2','').replace('CD3','').replace('Gramovies','').replace('BORip','').replace('200P','').replace('מס1','1').replace('מס2','2').replace('מס3','3').replace('מס4','4').replace('מס 3','3').replace('מס 2','2').replace('מס 1','1')

    name=name.replace('900p','').replace('PDTV','').replace('VHSRip','').replace('UPLOAD','').replace('TVRip','').replace('Heb Dub','').replace('MP3','').replace('AC3','').replace('SMG','').replace('Rip','').replace('6CH','').replace('XVID','')

    name=name.replace('HD','').replace('WEBDL','').replace('DVDrip','')
    
    name=name.replace('מצוירים','').replace('ת מ ','').replace('חננאל ס','').replace('Empire סרטים','').replace('heb dub','')
    name=name.replace('2נתי','2').replace('1נתי','1').replace('זירה מדיה','')
    
   
    for items in all_f:
        
       
        name=name.replace(items,'')
        
   
    name=name.strip()

    #info=(PTN.parse(name))
    regex='.*([1-3][0-9]{3})'
    year_pre=re.compile(regex).findall(name)
    year=0
    if len(year_pre)>0:
        year=year_pre[0]
     
        name=name.replace(year,'')
    pre_year=year
    if year!=0:
        
        url2='http://api.themoviedb.org/3/search/movie?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&year=%s&language=he&append_to_response=origin_country&page=1'%(name,year)
    else:
        url2='http://api.themoviedb.org/3/search/movie?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&language=he&append_to_response=origin_country&page=1'%(name)
    
    y=requests.get(url2).json()
    
    
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
    else:
        
        x=requests.get('https://www.google.com/search?client=firefox-b-d&q=%s+tmdb'%name.replace(' ','+'),headers=base_header).content
        regex='https://www.themoviedb.org/movie/(.+?)(?:-|/)'
        m=re.compile(regex).findall(x.decode('utf-8'))
        
        if len(m)>0:
            z=requests.get('http://api.themoviedb.org/3/movie/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&append_to_response=external_ids'%m[0],headers=base_header).json()
            if 1:#'results' in z and len(z['results'])>0:
                res=z
                if 'title' not in res:
                    log.warning('http://api.themoviedb.org/3/movie/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&append_to_response=external_ids'%(m[0].replace('?','')))
                    log.warning('https://www.google.com/search?client=firefox-b-d&q=%s+tmdb'%name.replace(' ','+'))
                    log.warning(z)
                name=res['title']
                if 'release_date' in res:
                   year=str(res['release_date'].split("-")[0])
                if year!=pre_year and len(z)>1:
                    
                    items_in=z
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
            
        else:
            
            log.warning('Not Found in google AT ALL:'+name)
        
    return name,year,plot,genere,icon,fan,original_name,rating,tmdb
def get_html_g():
    try:
        url_g='https://api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'
        html_g_tv=requests.get(url_g).json()
         
   
        url_g='https://api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'
        html_g_movie=requests.get(url_g).json()
    except Exception as e:
        log.warning('Err in HTML_G:'+str(e))
    return html_g_tv,html_g_movie
html_g_tv,html_g_movie=cache.get(get_html_g,72, table='posters_n')
def get_telegram_movies(test=False):
    
    global all_dub10,html_g_movie,global_name

    if test:
        import xbmcgui
        dp = xbmcgui . DialogProgress ( )
        dp.create('אנא המתן','טוען', '','')
        dp.update(0, 'אנא המתן','טוען', '' )
            
    resuaddon=xbmcaddon.Addon('plugin.video.telemedia')
    listen_port=resuaddon.getSetting('port')
    import xbmcgui
    
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'telehebdub.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
     
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""url TEXT, ""icon TEXT, ""fan TEXT,""plot TEXT,""year TEXT,""original_title TEXT,""generes TEXT,""rating TEXT,""id TEXT,""file_name TEXT,""date_added TEXT);" % 'hebdub')
    
    dbcon.commit()
    
    
    
    
    dbcur.execute("SELECT * FROM hebdub")
    match = dbcur.fetchall()
    all_fnames_tele=[]
    zzz=0
    for nm,ur,ic,fan,pl,ye,ori,ge,ra,idd,fn,dadd in match:
        if test:
             dp.update(int(((zzz* 100.0)/(len(match))) ), 'אנא המתן','במטמון', nm )
             zzz+=1
        v_data={}
        v_data['title']=nm.replace('%27',"'")
        v_data['icon']=ic
        v_data['fanart']=fan
        v_data['plot']=pl.replace('%27',"'")+'TEME'
        v_data['year']=ye
        v_data['OriginalTitle']=ori
        v_data['genre']=ge
        v_data['rating']=ra
        v_data['mediatype']='movies'
        v_data['dateadded']=dadd
        v_data['tmdb']=idd
        all_dub10.append((nm.replace('%27',"'").strip(),fn+'%%%TEME_'+ur,5,'[[TE]]',ic,fn,pl.replace('\n','').replace('\r','').replace('\t','').strip()+'TEME',json.dumps(v_data)))
        all_fnames_tele.append(ur)
        if nm=="4K WEB-DL 2020 זירה מדיה הקרודים 2 ח2.mkv":
            
            log.warning('IN DB:'+nm)
    last_id=0
    icon_pre='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSLd1qz7vDQz79zTTgddDCanmev34lU4E246XoMPYIwJ0q-m5ud&s'
    fan_pre='https://blog.pearachutekids.com/wp-content/uploads/2019/06/netflix-Cover.jpg'
    if icon_pre==None:
        icon_pre=''
    if fan_pre==None:
        fan_pre='' 
    num=random.randint(1,60000)
    new_kids=-1001109238401
    my_media=-1001405124454
    KIDS_CHAT_ID=-1001088055486
    nati_media_kids=-1001251653717
    
    mine=-1001185960400
    #new=-1001194480952
    new2=-1001312351447
    socko=-1001423506163
    medovav=-1001537597189
    amasalempovies=-1001330000060
    try:
        last_id=int(last_id)
    except:
        last_id=0
    chan_ids=[amasalempovies,mine,new_kids,KIDS_CHAT_ID,nati_media_kids,new2,socko,medovav]
    amount_found=100
    search_filter_arr=['searchMessagesFilterVideo','searchMessagesFilterDocument']
    index_group=0
    for search_filter in search_filter_arr:
     for chan_id in chan_ids:
        index_group+=1
        last_id=0
        log.warning('Chat id44:'+str(chan_id))
        data={'type':'td_send',
             'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': search_filter},'limit':100, '@extra': num})
             }
       
       

        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        num=random.randint(1,60000)
        
            
            
        
        
        
        if 'message' in event :
                if event['message']=='Chat not found':
            
                    log.warning('Dead chat chan_id:'+str(chan_id))
                log.warning('event in message')
                
                join_type=0
                found=False
                if int(chan_id)==mine:
                    chant_id='@myuploadsdub'
                    found=True
                elif int(chan_id)==nati_media_kids:
                    chant_id='@NatiMediaTG'
                    found=True
                if found:
                    num=random.randint(1,60000)
                    data={'type':'td_send',
                             'info':json.dumps({'@type': 'searchPublicChat', 'username': chant_id, '@extra': num})
                             }
                    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                    if 'id' in event:
                        if int(chan_id)!=nati_media_kids:
                            chan_id=event['id']
                            data={'type':'td_send',
                             'info':json.dumps({'@type': 'joinChat', 'chat_id': event['id'], '@extra': num})
                             }
                            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                            log.warning('event in message2')
                            log.warning(event)
                    data={'type':'td_send',
                         'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': search_filter},'limit':100, '@extra': num})
                         }
                   
                   

                    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                
        amount_found=100
        pages=0
        count_uq=0
        while amount_found>0:
            
            
            log.warning('chan_id:'+str(chan_id))
            
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': search_filter},'limit':100, '@extra': num})
                 }
           
           
                
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            if 'total_count' not in event:
                break
            amount_found=int(event['total_count'])-(100*pages)
            pages+=1
            log.warning('new amount_found:'+str(amount_found)+',chatid:'+str(chan_id))
            if amount_found==0:
                continue
            zzz=0
            if 0:#chan_id==socko:
                log.warning('MSG tele2:')
                log.warning(json.dumps(event['messages']))
            if chan_id==amasalempovies:
                log.warning(event)
            for items in event['messages']:  
                
                amount_found-=1
                if 'video' in items['content']:
                    name=items['content']['video']['file_name']
                    
                    regex=' ע(.+?) פ(.+?) '
                    mmm=re.compile(regex).findall(name)
                    if len(mmm)>0:
                        log.warning('tv')
                        log.warning(name)
                        continue
                    file_name=name=items['content']['video']['file_name']
                    num=random.randint(1,60000)
                    
                    if test:
                        dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), 'אנא המתן',str(amount_found)+' , '+str(count_uq), name )
                        if dp.iscanceled():
                            amount_found=0
                            dp.close()
                    #f_name=items['content']['document']['document']['remote']['id']
                    plot=''
                    if 'caption' in items['content']:
                        if 'text' in items['content']['caption']:
                            plot=items['content']['caption']['text']
                    
                    if file_name.replace("'","%27")  in all_fnames_tele:
                        continue
                    if '.mkv' not in name and '.mp4' not in name and '.avi' not in name:
                            
                            continue
                    
                    if 'מדובב' not in name and 'hebdub' not in name.lower() and 'heb dub' not in name.lower() and 'מדובב' not in plot and 'hebdub' not in plot.lower() and 'heb dub' not in plot.lower():
                        #log.warning('Not hebrew:'+name)
                        continue
                    
                    data={'type':'td_send',
                         'info':json.dumps({'@type': 'getMessageLink','message_id':items['id'],'chat_id':chan_id, '@extra': num})
                         }
                   
                   
                    
                    event_f_name=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                    
                    if 'link' in event_f_name:
                        f_name=event_f_name['link']
                    else:
                        f_name=event_f_name['url']
                    size=items['content']['video']['video']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    da=''
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                   
                    
                    
                    
                       
                    o_name=name
                    icon=icon_pre
                    fan=fan_pre
                    original_title=''
                    
                    tmdb='0'
                    
                    #name,year,plot,genere,icon,fan,original_name,rating,tmdb=clean_name2(name,original_title,html_g_movie,icon_pre,fan_pre)
                    #name,year,plot,genere,icon,fan,original_name,rating,tmdb=clean_name2(name,original_title,html_g_movie,icon_pre,fan_pre)
                    try:
                        name,year,plot,genere,icon,fan,original_name,rating,tmdb=cache.get(clean_name2,0,name,original_title,html_g_movie,icon_pre,fan_pre, table='cookies')
                    except:
                        pass
                    #name,year,plot,genere,icon,fan,original_name,rating=clean_name2(name,original_title,html_g_movie,icon_pre,fan_pre)
                    
                    #addLink( name, str(items['content']['document']['document']['id']),3,False, icon,fan,'[COLOR blue]'+o_name+'[/COLOR]\n'+f_size2+'\n'+plot,data=year,original_title=original_name,generes=genere,rating=rating,id=tmdb)
                    
                    f_plot='[COLOR blue]'+o_name+'[/COLOR]\n'+f_size2+'\n'+plot
                    dbcur.execute("INSERT INTO hebdub Values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" %  (name.replace("'","%27"),file_name.replace("'","%27"),icon,fan,f_plot.replace("'","%27"),year,original_name.replace("'","%27"),genere,rating,tmdb,f_name.replace("'","%27"),da))
                    v_data={}
                    v_data['title']=name
                    v_data['icon']=icon
                    v_data['fanart']=fan
                    v_data['plot']=f_plot+'TEME'
                    v_data['year']=year
                    v_data['OriginalTitle']=original_name
                    v_data['genre']=genere
                    v_data['rating']=rating
                    v_data['mediatype']='movies'
                    v_data['dateadded']=da
                    v_data['tmdb']=tmdb
                    count_uq+=1
                    global_name=name
                    all_dub10.append((name.replace('%27',"'").strip(),f_name+'%%%TEME_'+file_name,5,'[[TE]]',icon,fan,'Tele source:'+str(index_group)+f_plot.replace('\n','').replace('\r','').replace('\t','').strip()+'TEME',json.dumps(v_data)))
                    all_fnames_tele.append(file_name)
                    if file_name=="4K WEB-DL 2020 זירה מדיה הקרודים 2 ח2.mkv":
            
                        log.warning('IN DB2:'+file_name)
                elif 'document' in items['content']:
                    
                    
                        
                    name=items['content']['document']['file_name']
                  
                        
                    if chan_id==new2:
                        log.warning('New 2 titles:'+name)
                    regex=' ע(.+?) פ(.+?) '
                    mmm=re.compile(regex).findall(name)
                    if len(mmm)>0:
                        log.warning('tv')
                        log.warning(name)
                        continue
                    file_name=name
                    num=random.randint(1,60000)
                    
                    if test:
                        dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), 'אנא המתן',str(amount_found)+' , '+str(count_uq), name )
                        if dp.iscanceled():
                            amount_found=0
                            dp.close()
                    #f_name=items['content']['document']['document']['remote']['id']
                    plot=''
                    if 'caption' in items['content']:
                        if 'text' in items['content']['caption']:
                            plot=items['content']['caption']['text']
                    if file_name.replace("'","%27")  in all_fnames_tele:
                        if chan_id==new2:
                            log.warning('Found Mine2:'+name)
                        continue
                    if chan_id==new2:
                        log.warning('Mine2:'+name)
                    if '.mkv' not in name and '.mp4' not in name and '.avi' not in name:
                            
                            continue
                    if chan_id==new2:
                        log.warning('Mine3:'+name)
                    if 'מדובב' not in name and 'hebdub' not in name.lower() and 'heb dub' not in name.lower() and 'מדובב' not in plot and 'hebdub' not in plot.lower() and 'heb dub' not in plot.lower():
                        #log.warning('Not hebrew:'+name)
                        continue
                    if chan_id==new2:
                        log.warning('Mine4:'+name)
                    data={'type':'td_send',
                         'info':json.dumps({'@type': 'getMessageLink','message_id':items['id'],'chat_id':chan_id, '@extra': num})
                         }
                   
                   
                    
                    event_f_name=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                    
                    if 'link' in event_f_name:
                        f_name=event_f_name['link']
                    else:
                        f_name=event_f_name['url']
                    size=items['content']['document']['document']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    da=''
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                   
                    
                    
                    
                       
                    o_name=name
                    icon=icon_pre
                    fan=fan_pre
                    original_title=''
                    
                    tmdb='0'
                    
                    #name,year,plot,genere,icon,fan,original_name,rating,tmdb=clean_name2(name,original_title,html_g_movie,icon_pre,fan_pre)
                    #name,year,plot,genere,icon,fan,original_name,rating,tmdb=clean_name2(name,original_title,html_g_movie,icon_pre,fan_pre)
                    name,year,plot,genere,icon,fan,original_name,rating,tmdb=cache.get(clean_name2,0,name,original_title,html_g_movie,icon_pre,fan_pre, table='cookies')
                    #name,year,plot,genere,icon,fan,original_name,rating=clean_name2(name,original_title,html_g_movie,icon_pre,fan_pre)
                    
                    #addLink( name, str(items['content']['document']['document']['id']),3,False, icon,fan,'[COLOR blue]'+o_name+'[/COLOR]\n'+f_size2+'\n'+plot,data=year,original_title=original_name,generes=genere,rating=rating,id=tmdb)
                    
                    f_plot='[COLOR blue]'+o_name+'[/COLOR]\n'+f_size2+'\n'+plot
                    dbcur.execute("INSERT INTO hebdub Values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" %  (name.replace("'","%27"),file_name.replace("'","%27"),icon,fan,f_plot.replace("'","%27"),year,original_name.replace("'","%27"),genere,rating,tmdb,f_name.replace("'","%27"),da))
                    v_data={}
                    v_data['title']=name
                    v_data['icon']=icon
                    v_data['fanart']=fan
                    v_data['plot']=f_plot+'TEME'
                    v_data['year']=year
                    v_data['OriginalTitle']=original_name
                    v_data['genre']=genere
                    v_data['rating']=rating
                    v_data['mediatype']='movies'
                    v_data['dateadded']=da
                    v_data['tmdb']=tmdb
                    count_uq+=1
                    
                    all_dub10.append((name.replace('%27',"'").strip(),f_name+'%%%TEME_'+file_name,5,'[[TE]]',icon,fan,'Tele source:'+str(index_group)+f_plot.replace('\n','').replace('\r','').replace('\t','').strip()+'TEME',json.dumps(v_data)))
                    all_fnames_tele.append(file_name)
                
            dbcon.commit()
            all_d=[]
            last_id=str(items['id'])
            xbmc.sleep(100)
    
    
    if test:
        dp.close()
    dbcur.close()
    dbcon.close()
    return all_dub10
def get_background_data_tr():
        thread=[]
        thread.append(Thread(get_background_data))
        thread[0].start()
        return 'OK'
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
    
                
    count=0
    import codecs
    for name ,link,icon, image,plot,data,tmdbid ,date_added in match:
            template='''\
<tvshow>
    <title>%s</title>
    <originaltitle>%s</originaltitle>
    <showtitle>%s</showtitle>
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
</tvshow>
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
                new_items=(template%(title,original_title,title,rating,votes,plot,runtime,path,strm_path,strm_path,tmdb_id,generes,year,trailer,icon,fanart,fanart,dateadded))
                new_strm=strm%(que(title),que(link),que(icon),que(fanart)," ",tmdb_id,"ss")
                
                final='<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n'+new_items
                file = codecs.open(os.path.join(movie_path, c_title+'.nfo'), "w", "utf-8")

                file.write(final)
                file.close()
    
                file = open(strm_path+'.strm', "w")

                file.write(new_strm)
                file.close()
                
                
    xbmc.executebuiltin('UpdateLibrary(video)')
    
    
        
        
def get_dub(page,search_entered='',sys_arg_1_data=""):
        global all_dub,all_dub2,all_dub3,all_dub4,all_dub5
        import xbmcgui
        #get_telegram_movies(test=True)
        #return 0
        if Addon.getSetting("kids_dp")=='true':
            dp = xbmcgui . DialogProgress ( )
            if KODI_VERSION<19:
                dp.create('אנא המתן','טוען', '','')
                dp.update(0, 'אנא המתן','טוען', '' )
            else:
                dp.create('אנא המתן','טוען'+'\n'+ ''+'\n'+ '')
                dp.update(0, 'אנא המתן'+'\n'+ 'טוען'+'\n'+  '' )
        
    
        all_l=[]
        #get_background_data()
        addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
        tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
        tmdb_cacheFile = os.path.join(tmdb_data_dir, 'youtube.db')
        dbcon = database.connect(tmdb_cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""con1 TEXT,""origin TEXT,""icon TEXT, ""image TEXT,""plot TEXT,""data TEXT);"% 'kids_movie')
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""date TEXT,""type TEXT);" % 'updated')
        dbcon.commit()
        dbcur.execute("SELECT * FROM kids_movie")

        match = dbcur.fetchall()

        all_links={}
        all_names=[]
        xx=0
        tele_source=False
        
        try:
            resuaddon=xbmcaddon.Addon('plugin.video.telemedia')
            listen_port=resuaddon.getSetting('port')
            data={'type':'checklogin',
                 'info':''
                 }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            if event['status']==2 or event['status']=='Needs to log from setting':
                tele_source=False
                
            else:
                tele_source=True
        except:
            tele_source=False
        
        for name1,link,con1,origin,icon,image,plot,data in match:
          
          if 'letsupload.co' in link or 'openload.co' in link or 'sratim-il' in link:
                continue
          if '%%%TEME' in link and not tele_source:
            continue
          if 'rapidv' in link:
            continue
          if Addon.getSetting("kids_dp")=='true':
              if KODI_VERSION<19:
                dp.update(int(((xx* 100.0)/(len(match))) ), 'אנא המתן','אוסף', name1 )
              else:
                  dp.update(int(((xx* 100.0)/(len(match))) ), 'אנא המתן'+'\n'+ 'אוסף'+'\n'+  name1 )
                  
              xx+=1
          name1=name1.strip().replace('*מדובב*','').replace('*','').replace('-',' ')
          name1=replaceHTMLCodes(name1)
          fault_data=0
          
          dd=''
          data2={}
          
          try:
            name1=json.loads(data)['title'].replace('-',' ')
            data2=json.loads(data)
          
            if 'dateadded' in data2:
                dd=data2['dateadded']
          except Exception as e:
           
            try:
             
             data=data.replace('[',' ').replace(']',' ').replace('	','').replace("\\"," ").replace(': """",',': "" "",').replace(': """"}',': "" ""}').replace(': "",',': " ",').replace(': ""}',': " "}').replace('""','"').replace('\n','').replace('\r','')
             #name1=json.loads(data)['title'].replace('-',' ')
             
             data2=json.loads(data)
             if 'dateadded' in data2:
                dd=data2['dateadded']
             #dd=json.loads(data)['dateadded']
            except Exception as e:
             #log.warning('Error in dub2:'+str(e))
             
             fault_data=1
             pass
          
          if name1 not in all_names:
             tmdb_id=''
             try:
                data2['plot']=origin.replace('[','').replace(']','')+'\n[COLOR lightblue]'+dd+'[/COLOR]\n'+data2['plot']
                data2['title']=replaceHTMLCodes(data2['title'])
                tmdb_id=data2['tmdb']
                data=json.dumps(data2)
             except Exception as e:
                log.warning('Error Hebdub:'+str(e))
                data=json.dumps(data2)
                pass
             if tmdb_id==None:
                tmdb_id=''
             all_names.append(name1)
             all_links[name1]={}
             all_links[name1]['icon']=icon
             all_links[name1]['image']=image
             all_links[name1]['plot']=plot
             all_links[name1]['data']=data
             all_links[name1]['link']=origin+link
             all_links[name1]['origin']=origin.replace('[','').replace(']','')
             all_links[name1]['tmdb']=tmdb_id
          else:
               if link not in all_links[name1]['link']:
                 
                 all_links[name1]['origin']=all_links[name1]['origin']+','+origin.replace('[','').replace(']','')
                 try:
                    data2['plot']=all_links[name1]['origin']+'\n[COLOR lightblue]'+dd+'[/COLOR]\n'+data2['plot']
                    new_date=data2['dateadded']
                    old_date=json.loads(all_links[name1]['data'])['dateadded']
                    if new_date<old_date:
                        data2['dateadded']=json.loads(all_links[name1]['data'])['dateadded']
                        data2['plot']=data2['dateadded']+'\n'+data2['plot']
                    data=json.dumps(data2)
                    
                    
                    all_links[name1]['data']=data
                 except Exception as e:
                    #log.warning('Error Hebdub:'+str(e))
                    pass
                 if '$$$' in link:
                      links=link.split('$$$')
                      for link in links:
                        all_links[name1]['link']=all_links[name1]['link']+'$$$'+origin+link
                 else:
                   all_links[name1]['link']=all_links[name1]['link']+'$$$'+origin+link
        
        xx=0
        for items in all_links:
            if Addon.getSetting("kids_dp")=='true':
              if KODI_VERSION<19:
                dp.update(int(((xx* 100.0)/(len(all_links))) ), 'אנא המתן','שלב 2', items )
              else:
                  dp.update(int(((xx* 100.0)/(len(all_links))) ), 'אנא המתן'+'\n'+'שלב 2'+'\n'+ items )
              xx+=1
            
            link=all_links[items]['link']
            icon=all_links[items]['icon']
            image=all_links[items]['image']
            plot=all_links[items]['plot']
            data=all_links[items]['data']
            tmdb_id=all_links[items]['tmdb']
            if search_entered=='':
            
              if fault_data==1:
                log.warning('Fault:')
                data={}
                data['title']=items
                
                data['poster']=image
                data['Plot']=plot
              try:
                aa=json.loads(data)['title'].replace('-',' ')
              except:
                
                data={}
                data['title']=items
                
                data['poster']=image
                data['Plot']=plot
             
       
                  
              all_l.append(addLink(items,link,5,False,icon,image,replaceHTMLCodes(plot),video_info=data,id=tmdb_id))
            else:
              if search_entered in items  :
                all_l.append(addLink(items,link,5,False,icon,image,replaceHTMLCodes(plot),video_info=data,id=tmdb_id))
        if Addon.getSetting("kids_dp")=='true':
              if KODI_VERSION<19:
                dp.update(100, 'אנא המתן','סיימתי', ' ' )
              else:
                  dp.update(100, 'אנא המתן'+'\n'+'סיימתי'+'\n'+ ' ' )
              
              dp.close()
        xbmcplugin .addDirectoryItems(int(sys_arg_1_data),all_l,len(all_l))
        xbmcplugin.addSortMethod(int(sys_arg_1_data), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
        xbmcplugin.addSortMethod(int(sys_arg_1_data), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
        xbmcplugin.addSortMethod(int(sys_arg_1_data), xbmcplugin.SORT_METHOD_DATEADDED)
        xbmcplugin.addSortMethod(int(sys_arg_1_data), xbmcplugin.SORT_METHOD_VIDEO_RATING)
        
        
        dbcur.close()
        dbcon.close()
        all_img=cache.get(get_background_data_tr,24, table='posters')

        









        