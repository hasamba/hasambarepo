# -*- coding: utf-8 -*-
import re
import time
from  resources.modules.client import get_html
global global_var,stop_all#global
global_var=[]
stop_all=0
from resources.modules import log

from resources.modules.general import clean_name,check_link,server_data,replaceHTMLCodes,domain_s,similar,all_colors,base_header
from  resources.modules import cache
try:
    from resources.modules.general import Addon,get_imdb
except:
  import Addon
type=['movie','tv','torrent']

import urllib,logging,base64,json

def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all
    try:
        unque=urllib.unquote_plus
    except:
        unque=urllib.parse.unquote_plus
    imdb_id=cache.get(get_imdb, 999,tv_movie,id,table='pages')
    if tv_movie=='movie':
      type_item='movie'
      
    else:
      type_item='series'
      imdb_id=imdb_id+'%3A{0}%3A{1}'.format(season,episode)
    
    
    
    all_links=[]
    
    
    headers={'user-agent': 'Stremio/1.3.4 VersionCode/6304313 Package/com.stremio.one Coolpad/C103 Android/6.0.1 Dalvik/2.1.0 (Linux; U; Android 6.0.1; C103 Build/ZIXOSOP5801711191S)',

    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'utf-8'}
    try:
        que=urllib.quote_plus
    except:
        que=urllib.parse.quote_plus

    if 1:
                       
        x=get_html('http://5a0d1888fa64-torrentmafya-stremio-addon.baby-beamup.club/stream/%s/%s.json'%(type_item,imdb_id),headers=headers).json()
        log.warning(x)
        
       
        for items in x['streams']:
         if stop_all==1:
                break
            
         title=items['title'].split('[')[0]
         regex=' S\: (.+?)  L\: (.+?)\n'
         m=re.compile(regex).findall(items['title'])
         if len(m)>0:
             seed,peer=m[0]
         else:
             seed=0
             peer=0
         size=re.compile('\\n(.+?) ',re.DOTALL).findall(items['title'])[0]
         if '4k' in title:
              res='2160'
         elif '2160' in title:
              res='2160'
         elif '1080' in title:
              res='1080'
         elif '720' in title:
              res='720'
         elif '480' in title:
              res='480'
         elif '360' in title:
              res='360'
         else:
              res='HD'
        
       
       
         try:
             o_size=size
             size=float(o_size.replace('GiB','').replace('MiB','').replace(",",'').strip())
             if 'MB' in o_size:
               size=size/1000
         except Exception as e:
           
            size=0
         max_size=int(Addon.getSetting("size_limit"))
        
         if size<max_size:
           f_link=items['infoHash']
           lk='magnet:?xt=urn:btih:%s&dn=%s'%(f_link,que(title))
           all_links.append((title+'^^^'+peer+'/'+str(seed),lk,str(size),res))
       
           global_var=all_links
    return global_var
        
    