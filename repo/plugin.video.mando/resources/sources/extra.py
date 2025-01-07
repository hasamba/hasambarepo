# -*- coding: utf-8 -*-
import re
import time
from  resources.modules.client import get_html
global global_var,stop_all#global
from resources.modules import log
global_var=[]
stop_all=0
try:
 import xbmcgui
 local=False
except:
 local=True
 
from resources.modules.general import clean_name,check_link,server_data,replaceHTMLCodes,domain_s,similar,all_colors,base_header
try:
    from resources.modules.general import Addon
except:
  import Addon
type=['movie','tv','torrent']

import urllib,logging,base64,json

color=all_colors[110]
def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all
    all_links=[]
    try:
        que=urllib.quote_plus
    except:
        que=urllib.parse.quote_plus
   

    if tv_movie=='movie':
     cat='201'
     search_url=[('%s+%s'%(clean_name(original_title,1).replace(' ','+'),show_original_year)).lower()]
    else:
     cat='205'
     if Addon.getSetting('debrid_select')=='0' :
        
        search_url=[('%s+s%se%s'%(clean_name(original_title,1).replace(' ','+'),season_n,episode_n)).lower(),('%s+s%s'%(clean_name(original_title,1).replace(' ','+'),season_n)).lower(),('%s-season-%s'%(clean_name(original_title,1).replace(' ','+'),season)).lower()]
     else:
        search_url=[('%s+s%se%s'%(clean_name(original_title,1).replace(' ','+'),season_n,episode_n)).lower()]
    regex='<tr>(.+?)</tr>'
    regex1=re.compile(regex,re.DOTALL)
    
    regex='a href="magnet(.+?)".+?td class="tli".+?title="(.+?)"'
    regex2=re.compile(regex,re.DOTALL)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Alt-Used': 'extratorrent.cyou',
        'Connection': 'keep-alive',
        
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers',
    }

    


    for itt in search_url:
      
        params = (
            ('url', '/q.php?q='+itt),
            ('cat', ''),
        )

        

        x=get_html('https://extratorrent.cyou/api.php',headers=headers, params=params).json()
    
        
        
        
        for items in x:
            
            if stop_all==1:
                break
            
            size=items.get('size',0)
            try:
                size=int(size)/(1024*1024*1024)
            except:
                size=0
      
            
            
            
            
            
            title=items.get('name',0)
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
            
            
            o_link='magnet:?xt=urn:btih:%s&dn=%s'%(items.get('info_hash',0),que(title))
             
            max_size=int(Addon.getSetting("size_limit"))
      
            if size<max_size:
               
               all_links.append((title,o_link,str(size),res))
           
               global_var=all_links
    return global_var
        
    