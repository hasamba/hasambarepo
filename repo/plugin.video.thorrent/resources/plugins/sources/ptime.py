# -*- coding: utf-8 -*-
import re
import time

global global_var,stop_all#global
global_var=[]
stop_all=0

from  resources.modules.client import get_html
from resources.modules.general import clean_name,check_link,server_data,replaceHTMLCodes,domain_s,similar,all_colors,base_header
from  resources.modules import cache
try:
    from resources.modules.general import Addon,get_imdb
except:
  import Addon
type=['movie','tv','torrent']

import urllib,logging,base64,json
from resources.modules import log

def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all
    try:
        que=urllib.quote_plus
    except:
        que=urllib.parse.quote_plus
    imdb_id=cache.get(get_imdb, 999,tv_movie,id,table='pages')
    
  
    
    
    all_links=[]
    if tv_movie=='tv':
     search_url='http://api.apiumadomain.com/show?ver=3.6.7&imdb={0}&os=android10&device_type=phone&app_id=T4P_AND&device=B&quality=720p%2C1080p%2C2160p'.format(imdb_id)
    else:
      search_url='http://api.apiumadomain.com/movie?ver=3.6.7&imdb={0}&ep={1}&os=android10&device_type=phone&app_id=T&device=BBB&quality=720p%2C1080p%2C2160p'.format(imdb_id,season)
        
    div=1024*1024*1024
    
      

    y=get_html(search_url,headers=base_header,timeout=10).json()

    if tv_movie=='tv':
      for items in y[season]:
 
        if int(items['episode'])!=int(episode) or int(items['season'])!=int(season):
            continue
        if stop_all==1:
            break
        for itm in items['items']:
            
                     lk=itm['torrent_magnet']
                     title=itm['file']
                     size=itm['size_bytes']/(div)
                     seed=itm.get('torrent_seeds','0')
                     peer=itm.get('torrent_peers','0')
                     if stop_all==1:
                        break
                     
                     
                    
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
                    
                    
                   
                     
                     max_size=int(Addon.getSetting("size_limit"))
              
                     if size<max_size:
                  
                       all_links.append((title+'^^^'+str(peer)+'/'+str(seed),lk,str(size),res))
                   
                       global_var=all_links
    else:
        
        for itm in y['items']:
        
                 lk=itm['torrent_magnet']
                 title=itm['file']
                 size=itm['size_bytes']/(div)
                 seed=itm.get('torrent_seeds','0')
                 peer=itm.get('torrent_peers','0')
                 if stop_all==1:
                    break
                 
                 
                
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
                
                
               
                 
                 max_size=int(Addon.getSetting("size_limit"))
          
                 if size<max_size:
              
                   all_links.append((title+'^^^'+str(peer)+'/'+str(seed),lk,str(size),res))
               
                   global_var=all_links
    return global_var
        
    