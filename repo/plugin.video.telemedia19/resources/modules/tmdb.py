# -*- coding: utf-8 -*-
from .public import addNolink,addDir3,addLink,lang,user_dataDir

import threading,urllib,os
import re,logging,sys,time,requests
import xbmcaddon,xbmc,xbmcgui
import xbmcplugin
Addon = xbmcaddon.Addon()
from resources.modules import cache
logging.warning('LANG:'+lang)
domain_s='https://'
def get_html_g():
    try:
        url_g='https://api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language='+lang
        html_g_tv=requests.get(url_g).json()
         
   
        url_g='https://api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language='+lang
        html_g_movie=requests.get(url_g).json()
    except Exception as e:
        logging.warning('Err in HTML_G:'+str(e))
    return html_g_tv,html_g_movie
html_g_tv,html_g_movie=cache.get(get_html_g,72, table='posters_n')
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
if KODI_VERSION<=18:
    que=urllib.quote_plus
else:
    que=urllib.parse.quote_plus
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
else:
   
    class Thread(threading.Thread):
        def __init__(self, target, *args):
           
            self._target = target
            self._args = args
            
            
            threading.Thread.__init__(self)
            
        def run(self):
            
            self._target(*self._args)
def get_tmdb_data(new_name_array,html_g,fav_search_f,fav_servers_en,fav_servers,google_server,rapid_server,direct_server,heb_server,url,isr,xxx):
          
          try:
           global all_d
           if Addon.getSetting("use_trak")=='true':
               i = (call_trakt('/users/me/watched/movies'))
               all_movie_w=[]
               for ids in i:
                  all_movie_w.append(str(ids['movie']['ids']['tmdb']))
          

           html=requests.get(url).json()
           max_page=html['total_pages']
           logging.warning('max_page:'+str(max_page))
           all_res=html['total_results']
          
           count=0
           
           for data in html['results']:
           
             count+=1
             if 'vote_average' in data:
               rating=data['vote_average']
             else:
              rating=0
             if 'first_air_date' in data:
               year=str(data['first_air_date'].split("-")[0])
             elif 'release_date' in data:
                year=str(data['release_date'].split("-")[0])
             else:
                year='0'
             if data['overview']==None:
               plot=' '
             else:
               plot=data['overview']
             if 'title' not in data:
               tv_movie='tv'
               new_name=data['name']
             else:
               tv_movie='movie'
               new_name=data['title']
              
             
             f_subs=[]
             if 'original_title' in data:
               original_name=data['original_title']
               mode=15
               
               id=str(data['id'])
               if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
                 import cache
                 from subs import get_links
                 f_subs=cache.get(get_links,9999,'movie',original_name,original_name,'0','0','0','0',year,id,True, table='pages')
               if data['original_language']!='en':
                
                html2=requests.get('http://api.themoviedb.org/3/movie/%s?api_key=34142515d9d23817496eeb4ff1d223d0'%id).json()
                original_name=html2['title']
                
               
             else:
               original_name=data['original_name']
               id=str(data['id'])
               
               mode=16
               
               if data['original_language']!='en':
                
                    html2=requests.get('http://api.themoviedb.org/3/tv/%s?api_key=34142515d9d23817496eeb4ff1d223d0'%id).json()
                    if 'name' in html2:
                        original_name=html2['name']
                    #if 'name' in data:
                    #    original_name=data['name']
             
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
               fan='https://image.tmdb.org/t/p/original/'+fan
             if 'http' not in icon:
               icon='https://image.tmdb.org/t/p/original/'+icon
             genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                    if i['name'] is not None])
             try:genere = u' / '.join([genres_list[x] for x in data['genre_ids']])
             except:genere=''
             
             trailer = "plugin://plugin.video.allmoviesin?mode=25&url=www&id=%s&tv_movie=%s" % (id,tv_movie)
             if new_name not in new_name_array:
              new_name_array.append(new_name)
              if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
                  if len(f_subs)>0:
                    color='white'
                  else:
                    color='red'
                    
              else:
                 color='white'
              start_time = time.time()
              
              
              
              
              
              
              elapsed_time = time.time() - start_time
              
              
              if  Addon.getSetting("disapear")=='true' and color=='red' and mode!=7:
                a=1
              else:
                color='white'
                
                watched='no'
                if Addon.getSetting("use_trak")=='true':
                    if id in all_movie_w:
                        watched='yes'
                if  mode==4 and fav_search_f=='true' and fav_servers_en=='true' and (len(fav_servers)>0 or heb_server=='true' or google_server=='true' or rapid_server=='true' or direct_server=='true'):
                
                    fav_status='true'
                else:
                    fav_status='false'
            
                
                all_d.append(('[COLOR '+color+']'+new_name+'[/COLOR]',url,mode,icon,fan,plot,year,original_name,id,rating,new_name,year,isr,genere,trailer,watched,fav_status,xxx,max_page,all_res))
              
           
           
          except Exception as e:
            import linecache,sys
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Victory', 'No Trailer...Line:'+str(lineno)+' E:'+str(e))).encode('utf-8'))
            logging.warning('ERROR IN GET TMDB:'+str(lineno))
            logging.warning('inline:'+line)
            logging.warning(e)
            logging.warning(html_t)
            logging.warning('BAD Trailer play')
def get_all_data(first,last,url,link,new_name_array,isr):
    try:
        
        global all_d
        
        all_d=[]
        xxx=0
        logging.warning('1')
        if '/tv/' in url:
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
        logging.warning('2')
   
              
              
        if '/tv/' in url:
             url_g='https://api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language='+lang
             
             html_g=html_g_tv
        else:
             url_g='https://api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language='+lang
             html_g=html_g_movie
        #html_g=requests.get(url_g).json()
        logging.warning('3')
        if Addon.getSetting("dp")=='true' and (last-first)>1:
                dp = xbmcgui.DialogProgress()
                dp.create("Loading", "Please Wait", '')
                dp.update(0)
        thread=[]
        logging.warning('4')
        for i in range(first,last):
           logging.warning('5')
           url=link+'page='+str(i)
          
           
           thread.append(Thread(get_tmdb_data,new_name_array,html_g,fav_search_f,fav_servers_en,fav_servers,google_server,rapid_server,direct_server,heb_server,url,isr,xxx))
           thread[len(thread)-1].setName('Page '+str(i))
           xxx+=1
       

           
          
           
           

                #addDir3('[COLOR '+color+']'+new_name+'[/COLOR]',url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer,watched=watched,fav_status=fav_status)
    except Exception  as err:
            import traceback
            from os.path import basename
            exc_info=sys.exc_info()
            e=(traceback.format_exc())
            et=e.split(',')
          
            e=','.join(et).replace('UnboundLocalError: ','')
            home1=xbmc.translatePath("special://home/")
            e_al=e.split(home1)
            logging.warning(e_al)
            e=e_al[len(e_al)-1].replace(home1,'')
            logging.warning('Error TMDB:'+str(e))
    start_time=time.time()
    for td in thread:
        td.start()
        if 1:
            
            while td.is_alive():
                xbmc.sleep(100)
            
        if Addon.getSetting("dp")=='true' and (last-first)>1:
                elapsed_time = time.time() - start_time
                dp.update(0, ' Activating '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),td.name," ")
        
        #xbmc.sleep(255)
        
    while 1:

          still_alive=0
          all_alive=[]
          for yy in range(0,len(thread)):
            
            if  thread[yy].is_alive():
              
              still_alive=1
              all_alive.append(thread[yy].name)
          if still_alive==0:
            break
          if Addon.getSetting("dp")=='true' and (last-first)>1:
                elapsed_time = time.time() - start_time
                dp.update(0, ' Please Wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),','.join(all_alive)," ")
          xbmc.sleep(100)
    if Addon.getSetting("dp")=='true' and (last-first)>1:
        dp.close()
    return all_d
    
def get_movies(url,local=False,reco=0):
   
   new_name_array=[]
   isr=0

   all_years=[]
   import datetime
   all_d=[]
   now = datetime.datetime.now()
   for year in range(now.year,1970,-1):
         all_years.append(str(year))
   if 'advance' in url:
        window = adv_gen_window(url.split('_')[1])
        window.doModal()
        all_g=window.all_clicked
        start_y=window.fromy
        end_y=window.toy
    
        del window
        url='http://api.themoviedb.org/3/discover/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&sort_by=popularity.desc&primary_release_date.gte=%s-01-01&primary_release_date.lte=%s-12-31&with_genres=%s&page=1'%(url.split('_')[1],lang,start_y,end_y,','.join(all_g))
   if url=='movie_years&page=1':
     
      
      if Addon.getSetting("dip_dialog")=='0':
          ret=ret = xbmcgui.Dialog().select("Choose", all_years)
          if ret!=-1:
            
              url='https://api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&sort_by=popularity.desc&include_adult=false&include_video=false&primary_release_year=%s&with_original_language=en&page=1'%(lang,all_years[ret])
            
          else:
            return 0
      else:
        for items in all_years:
            
            url='https://api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&sort_by=popularity.desc&include_adult=false&include_video=false&primary_release_year=%s&with_original_language=en&page=1'%(lang,items)
            if 0:
               if  name not in all_n:
                all_n.append(name)
                
                aa=addDir3(items,url,14,'https://www.techniquetuesday.com/mm5/graphics/00000001/Technique-Tuesday-Calendar-Years-Clear-Stamps-Large_329x400.jpg','https://images.livemint.com/rf/Image-621x414/LiveMint/Period2/2018/08/16/Photos/Processed/investment-knrG--621x414@LiveMint.jpg',items,collect_all=True)
                all_d.append(aa)
            else:
                aa=addDir3(items,url,14,'https://www.techniquetuesday.com/mm5/graphics/00000001/Technique-Tuesday-Calendar-Years-Clear-Stamps-Large_329x400.jpg','https://images.livemint.com/rf/Image-621x414/LiveMint/Period2/2018/08/16/Photos/Processed/investment-knrG--621x414@LiveMint.jpg',items,collect_all=True)
                all_d.append(aa)
        
   if url=='tv_years&page=1' and 'page=1' in url:
      if Addon.getSetting("dip_dialog")=='0':
          ret=ret = xbmcgui.Dialog().select("Choose", all_years)
          if ret!=-1:
            url='https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&sort_by=popularity.desc&first_air_date_year=%s&include_null_first_air_dates=false&with_original_language=en&page=1'%(lang,all_years[ret])
           
          else:
            sys.exit()
      else:
        for items in all_years:
            url='https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&sort_by=popularity.desc&first_air_date_year=%s&include_null_first_air_dates=false&with_original_language=en&page=1'%(lang,items)
            
            aa=addDir3(items,url,14,'https://www.techniquetuesday.com/mm5/graphics/00000001/Technique-Tuesday-Calendar-Years-Clear-Stamps-Large_329x400.jpg','https://images.livemint.com/rf/Image-621x414/LiveMint/Period2/2018/08/16/Photos/Processed/investment-knrG--621x414@LiveMint.jpg',items,collect_all=True)
            all_d.append(aa)
        
   if '/search' in url and 'page=1' in url and '%s' in url:
        
        
        
        search_entered =''
        keyboard = xbmc.Keyboard(search_entered, 'Enter Search')
        keyboard.doModal()
        if keyboard.isConfirmed() :
               search_entered = keyboard.getText()
               if search_entered=='':
                sys.exit()
               url=url%que(search_entered)
               if '/tv?' in url:
                type_in='tv'
               else:
                type_in='movie'
               
              
          
        else:
          
          
          sys.exit()
   
   html={}
   html['results']=[]
   regex='page=(.+?)$'
   match=re.compile(regex).findall(url)
   # first=int(match[0])
   # last=int(match[0])+1
   # link=url.split('page=')[0]
   if len(match)==0 or reco==1:
    first=1
    last=2
    link=url.split('page=')[0]
   else:
       link=url.split('page=')[0]
       first=int(match[0])
       s_last=int(Addon.getSetting("num_p"))
       if s_last>10:
         s_last=10
       last=first+int(s_last)


   

   

   #all_in_data=get_all_data(first,last,url,link,new_name_array,isr)
   logging.warning('Insert Got All Data')
  
   all_in_data=cache.get(get_all_data,24,first,last,url,link,new_name_array,isr, table='pages')
   logging.warning('Insert Got All Data2')
   if '/search' in url:
    all_in_data=sorted(all_in_data, key=lambda x: x[6], reverse=True)
   else:
   
    all_in_data=sorted(all_in_data, key=lambda x: x[17], reverse=False)
   max_page=-1
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
            ee=str(tm)
            all_w[ee]={}
            all_w[ee]['resume']=str(p)
            all_w[ee]['totaltime']=str(t)
   for  name,url,mode,icon,fan,plot,year,original_name,id,rating,new_name,year,isr,genere,trailer,watched,fav_status,xxx,max_page,all_res in all_in_data:
            if local:
                addNolink( new_name, id,27,False,fan=fan, iconimage=icon,plot=plot,year=year,generes=genere,rating=rating,trailer=trailer)
            else:
                
                aa=addDir3(name,url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer,watched=watched,fav_status=fav_status,collect_all=True,all_w=all_w)
                all_d.append(aa)
   logging.warning('Got All Data')
   regex='page=(.+?)$'
   match=re.compile(regex).findall(url)
   link=url.split('page=')[0]
   if   max_page==-1:
        xbmcgui.Dialog().ok('Telemedia','[COLOR aqua][I] אין תוצאות[/I][/COLOR]')
        sys.exit()
   
   if max_page>int(match[0]):
        if local:
            mode=26
        else:
            mode=14
        aa=addDir3(('[COLOR yellow][I]עמוד %s מתוך %s (%s תוצאות)[/I][/COLOR]'%(str(int(match[0])+1),str(max_page),str(all_res))),link+'page='+str(int(match[0])+1),mode,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTNmz-ZpsUi0yrgtmpDEj4_UpJ1XKGEt3f_xYXC-kgFMM-zZujsg','https://cdn4.iconfinder.com/data/icons/arrows-1-6/48/1-512.png','Results',isr=isr,show_original_year='999',data='999',collect_all=True)
        all_d.append(aa)
     
   if 0:
       xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
       xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
       

       xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
   xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
   dbcur.close()
   dbcon.close()
   return new_name_array
   
def get_seasons(name,url,iconimage,fanart,description,data,original_title,id,heb_name,isr):
   all_d=[]
   payload= {
                    "apikey": "0629B785CE550C8D",
                    "userkey": "",
                    "username": ""
   }
   tmdbKey = '653bb8af90162bd98fc7ee32bcbbfb3d'
   #headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Accept-Language': 'he'}
   #r = requests.post(domain_s+'api.thetvdb.com/login', json=payload, headers=headers)
   #r_json = r.json()

   url=domain_s+'api.themoviedb.org/3/tv/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=he,en&append_to_response=external_ids'%id
   logging.warning(url)
   html=requests.get(url).json()
   if 'first_air_date' in html:
    show_original_year=html['first_air_date'].split("-")[0]
   else:
    show_original_year=0
   #tmdb data
   #headers['Authorization'] = "Bearer %s" %  str(r_json.get('token'))
   tmdbid=html['external_ids']['tvdb_id']
   if tmdbid==None:
     response2 = requests.get(domain_s+'www.thetvdb.com/?string=%s&searchseriesid=&tab=listseries&function=Search'%name).content
     
     SearchSeriesRegexPattern = 'a href=".+?tab=series.+?id=(.+?)mp'
     match=re.compile(SearchSeriesRegexPattern).findall(response2)
   
     for tmnum in match:
       tmnum=tmnum.replace("&a","")
       if len(tmnum)>0:
         tmdbid=tmnum

   response = requests.get('http://thetvdb.com/api/0629B785CE550C8D/series/%s/all/he.xml'%html['external_ids']['tvdb_id']).content
  
   attr=['Combined_season','FirstAired']
   regex='<Episode>.+?<EpisodeName>(.+?)</EpisodeName>.+?<EpisodeNumber>(.+?)</EpisodeNumber>.+?<FirstAired>(.+?)</FirstAired>.+?<SeasonNumber>(.+?)</SeasonNumber>'
   match=[]
   #match=re.compile(regex,re.DOTALL).findall(response.decode('utf-8'))
   #seasons_tvdb=parseDOM(response,'Episode', attr)
   all_season=[]
   all_season_tvdb_data=[]
    
   all_season_imdb=[]
   all_season_imdb_data=[]
   for ep_name,ep_num,aired,s_number in match:
     if s_number not in all_season:

       all_season.append(str(s_number))
       all_season_tvdb_data.append({"name":ep_name,"episode_number":ep_num,"air_date":aired,"season_number":s_number,"poster_path":iconimage})
   try:
       url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=he&append_to_response=external_ids'%(id,tmdbKey)
      
       
       imdb_id=requests.get(url2).json()['external_ids']['imdb_id']
       xx=requests.get('https://www.imdb.com/title/%s/episodes'%imdb_id).content
       regex='<label for="bySeason">(.+?)</div'
       match_imdb_s_pre=re.compile(regex,re.DOTALL).findall(xx)[0]
       regex='<option.+?value="(.+?)"'
       match_imdb_s=re.compile(regex).findall(match_imdb_s_pre)
       regex_img='<img itemprop="image".+?src="(.+?)"'
       img_imdb_pre=re.compile(regex_img,re.DOTALL).findall(xx)
       if len (img_imdb_pre)>0:
            img_imdb=img_imdb_pre[0]
       else:
            img_imdb=' '
       for s_number in match_imdb_s:
            all_season_imdb.append(str(s_number))
            all_season_imdb_data.append({"name":'0',"episode_number":'0',"air_date":' ',"season_number":s_number,"poster_path":img_imdb,'backdrop_path':img_imdb})
   except:
    pass
   all_season_tmdb=[]
   for data in html['seasons']:
      all_season_tmdb.append(str(data['season_number']))
   for items_a in all_season:
     if items_a not in all_season_tmdb:
       html['seasons'].append(all_season_tvdb_data[all_season.index(items_a)])
       
   for items_a in all_season_imdb:
     if items_a not in all_season_tmdb:
       html['seasons'].append(all_season_imdb_data[all_season_imdb.index(items_a)])
   plot=html['overview']
   original_name=html['original_name']
   for data in html['seasons']:
   
     new_name=' Season '+str(data['season_number'])
     if data['air_date']!=None:
         year=str(data['air_date'].split("-")[0])
     else:
       year=0
     season=str(data['season_number'])
     if data['poster_path']==None:
      icon=iconimage
     else:
       icon=data['poster_path']
     if 'backdrop_path' in data:
         if data['backdrop_path']==None:
          fan=fanart
         else:
          fan=data['backdrop_path']
     else:
        fan=html['backdrop_path']
     ep_number=''
     if 'episode_count' in data:
        ep_number=data['episode_count']
        
     if plot==None:
       plot=' '
     if fan==None:
       fan=fanart
     if 'http' not in fan:
       fan=domain_s+'image.tmdb.org/t/p/original/'+fan
     if 'http' not in icon:
       icon=domain_s+'image.tmdb.org/t/p/original/'+icon
     
     watched=''
     remain=''
      
     
     color='white'
     try:
        if 'air_date' in data:
           
               datea='[COLOR aqua]'+str(time.strptime(data['air_date'], '%Y-%m-%d'))+'[/COLOR]\n'
               
               a=(time.strptime(data['air_date'], '%Y-%m-%d'))
               b=time.strptime(str(time.strftime('%Y-%m-%d')), '%Y-%m-%d')
               
           
               if a>b:
                 color='red'
                 txt_1=' Wait until ... '
               else:
                 txt_1=' Aired At '
                 color='white'
        datea='[COLOR aqua]'+txt_1+time.strftime( "%d-%m-%Y",a) + '[/COLOR]\n'
     except:
             
             datea=''
             color='red'
     if 'season 0' in new_name:
        continue
     aa=addDir3( '[COLOR %s]'%color+new_name+'[/COLOR]',url,19,icon,fan,datea+plot,data=year,original_title=original_name,id=id,season=season,tmdbid=tmdbid,show_original_year=show_original_year,heb_name=heb_name,isr=isr,ep_number=ep_number,watched_ep=watched,remain=remain)
     all_d.append(aa)
   xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def get_episode_data(id,season,episode,yjump=True):
    url='http://api.themoviedb.org/3/tv/%s/season/%s/episode/%s?api_key=653bb8af90162bd98fc7ee32bcbbfb3d&language=%s&append_to_response=external_ids'%(id,season,episode,lang)
    
    html=requests.get(url).json()
    if yjump:
      if 'status_code' in html:
        url='http://api.themoviedb.org/3/tv/%s/season/%s/episode/%s?api_key=653bb8af90162bd98fc7ee32bcbbfb3d&language=%s&append_to_response=external_ids'%(id,str(int(season)+1),'1',lang)
        html=requests.get(url).json()
        episode='1'
        season=str(int(season)+1)
    if 'name' in html:
        name=html['name']
        plot=html['overview']
        if html['still_path']!=None:
          image=domain_s+'image.tmdb.org/t/p/original/'+html['still_path']
        else:
          image=' '
        return name,plot,image,season,episode
    else:
       return ' ',' ',' ',' ',' '
def get_episode(name,url,iconimage,fanart,description,data,original_title,id,season,tmdbid,show_original_year,heb_name,isr):
   import _strptime
   all_d=[]
   url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s'%(id,season,lang)
   tmdbKey = '653bb8af90162bd98fc7ee32bcbbfb3d'
   html=requests.get(url).json()
   #tmdb data
   if 'episodes'  in html:
       if html['episodes'][0]['name']=='':
         url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=eng'%(id,season)
         html=requests.get(url).json()
   response = requests.get('http://thetvdb.com/api/0629B785CE550C8D/series/%s/all/he.xml'%tmdbid).content
   
   attr=['Combined_season','FirstAired']
   regex='<Episode>.+?<EpisodeName>(.+?)</EpisodeName>.+?<EpisodeNumber>(.+?)</EpisodeNumber>.+?<FirstAired>(.+?)</FirstAired>.+?<Overview>(.+?)</Overview>.+?<SeasonNumber>(.+?)</SeasonNumber>'
   #match=re.compile(regex,re.DOTALL).findall(response)
   regex_eng='<slug>(.+?)</slug>'
   #match_eng=re.compile(regex_eng).findall(response)
   match=[]
   match_eng=[]
   eng_name=name
   if len (match_eng)>0:
     eng_name=match_eng[0]

   #seasons_tvdb=parseDOM(response,'Episode', attr)

   all_episodes=[]
   all_season_tvdb_data=[]
   
   all_episodes_imdb=[]
   all_episodes_imdb_data=[]
   image2=' '
   for ep_name,ep_num,aired,overview,s_number in match:
     
     image2=fanart
     if s_number==season:
         if ep_num not in all_episodes:
           
           all_episodes.append(str(ep_num))
           all_season_tvdb_data.append({"name":ep_name,"episode_number":ep_num,"air_date":aired,"overview":overview,"season_number":s_number,"still_path":iconimage,"poster_path":image2})
   
   url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=he&append_to_response=external_ids'%(id,tmdbKey)
      
       
    
      
       
   imdb_id=requests.get(url2).json()['external_ids']['imdb_id']
   xx=requests.get('https://www.imdb.com/title/%s/episodes?season=%s'%(imdb_id,season)).content

   regex='div class="image">.+?title="(.+?)"(.+?)meta itemprop="episodeNumber" content="(.+?)".+?itemprop="description">(.+?)<'
   match_imdb_s_pre=re.compile(regex,re.DOTALL).findall(xx.decode('utf-8'))
  
   for ep_name,poster,ep_num,plot in match_imdb_s_pre:
        if 'src="' in poster:
            regex='src="(.+?)"'
            poster=re.compile(regex).findall(poster)[0]
        else:
            poster=' '
        all_episodes_imdb.append(str(ep_num))
        all_episodes_imdb_data.append({"name":ep_name,"episode_number":ep_num,"air_date":' ',"season_number":season,"poster_path":poster,'still_path':poster,"overview":plot})
   
  
   all_episodes_tmdb=[]

   if 'episodes' not in html:
     html['episodes']=[]
     html['poster_path']=fanart
   else:
       for data in html['episodes']:
          all_episodes_tmdb.append(str(data['episode_number']))
   for items_a in all_episodes:
     if items_a not in all_episodes_tmdb:
       html['episodes'].append(all_season_tvdb_data[all_episodes.index(items_a)])
   for items_a in all_episodes_imdb:
     if items_a not in all_episodes_tmdb:
       html['episodes'].append(all_episodes_imdb_data[all_episodes_imdb.index(items_a)])
       
   original_name=original_title
   if Addon.getSetting("dp")=='true' and (Addon.getSetting("disapear")=='true' or Addon.getSetting("check_subs")=='true'):
            dp = xbmcgui.DialogProgress()
            dp.create("Loading", "Please wait", '')
            dp.update(0)
   xxx=0
   start_time = time.time()
   
   if Addon.getSetting("use_trak")=='true':
       i = (call_trakt('/users/me/watched/shows?extended=full'))
       all_tv_w={}
       for ids in i:
         all_tv_w[str(ids['show']['ids']['tmdb'])]=[]
         for seasons in ids['seasons']:
          for ep in seasons['episodes']:
            all_tv_w[str(ids['show']['ids']['tmdb'])].append(str(seasons['number'])+'x'+str(ep['number']))
   
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
   from datetime import datetime
   try:
        from sqlite3 import dbapi2 as database
   except:
        from pysqlite2 import dbapi2 as database
   cacheFile=os.path.join(user_dataDir,'database.db')
   dbcon = database.connect(cacheFile)
   dbcur = dbcon.cursor()
   dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
   dbcon.commit()
    
   dbcur.execute("SELECT * FROM playback where tmdb='%s' and season='%s' "%(id,str(season).replace('%20','0').replace(' ','0')))
   match = dbcur.fetchall()
   all_w={}
   logging.warning('found match:')
   logging.warning(match)
   for n,t,s,e,p,t,f in match:
        ee=str(e)
        all_w[ee]={}
        all_w[ee]['resume']=str(p)
        all_w[ee]['totaltime']=str(t)
    
            
   for data in html['episodes']:
     plot=data['overview']
     new_name=str(data['episode_number'])+" . "+data['name']
     air_date=''
     if 'air_date' in data:
       if data['air_date']!=None:
         
         year=str(data['air_date'].split("-")[0])
       else:
         year=0
     else:
       year=0
     
     if data['still_path']!=None:
       if 'https' not in data['still_path']:
         image=domain_s+'image.tmdb.org/t/p/original/'+data['still_path']
       else:
         image=data['still_path']
       
     elif html['poster_path']!=None:
      if 'https' not in html['poster_path']:
       image=domain_s+'image.tmdb.org/t/p/original/'+html['poster_path']
      else:
         image=html['poster_path']
     else:
       image=fanart
     if html['poster_path']!=None:
      if 'https' not in html['poster_path']:
       icon=domain_s+'image.tmdb.org/t/p/original/'+html['poster_path']
      else:
        icon=html['poster_path']
     else:
       icon=iconimage
     #if image2==fanart:
     #  icon=iconimage
      
     #  image=fanart
     color2='white'
     try:
        if 'air_date' in data:
           
               datea='[COLOR aqua]'+str(time.strptime(data['air_date'], '%Y-%m-%d'))+'[/COLOR]\n'
               
               a=(time.strptime(data['air_date'], '%Y-%m-%d'))
               b=time.strptime(str(time.strftime('%Y-%m-%d')), '%Y-%m-%d')
               
           
               if a>b:
                 color2='red'
               else:
                 
                 color2='white'
        datea='[COLOR aqua]'+' שודר בתאריך '+time.strftime( "%d-%m-%Y",a) + '[/COLOR]\n'
     except:
             
             datea=''
             color2='red'
     f_subs=[]
     
     
     if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
         import cache
         from subs import get_links
         f_subs=cache.get(get_links,9999,'tv',original_name,original_name,season,str(data['episode_number']),season,str(data['episode_number']),year,id,True, table='pages')
         
         
     
     

     
     color=color2
     if season!=None and season!="%20":
        tv_movie='tv'
     else:
       tv_movie='movie'
     
     elapsed_time = time.time() - start_time
     if (Addon.getSetting("check_subs")=='true'  or Addon.getSetting("disapear")=='true') and Addon.getSetting("dp")=='true':
        dp.update(int(((xxx* 100.0)/(len(html['episodes']))) ), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'[COLOR'+color+']'+new_name+'[/COLOR]')
     xxx=xxx+1
     if  Addon.getSetting("disapear")=='true' and color=='red':
        a=1
     else:
     
       watched='no'
       if Addon.getSetting("use_trak")=='true':
           if id in all_tv_w:
             if season+'x'+str(data['episode_number']) in all_tv_w[id]:
              watched='yes'
       
       
       aa=addDir3( '[COLOR %s]'%color+new_name+'[/COLOR]', url,20, icon,image,datea+plot,data=year,original_title=original_name,id=id,season=season,episode=data['episode_number'],eng_name=eng_name,show_original_year=show_original_year,heb_name=heb_name,isr=isr,watched=watched,fav_status=fav_status,all_w=all_w)
       all_d.append(aa)
   dbcur.close()
   dbcon.close()
   xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
     #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_EPISODE)
     #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
     