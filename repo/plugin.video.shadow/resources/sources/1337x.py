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
    from resources.modules.general import Addon
except:
  import Addon
type=['movie']

import urllib,logging,base64,json
import concurrent.futures
from concurrent.futures import wait
global all_links
all_links=[]
def trd_data(lk,nm,size):
   
   global all_links,global_var
   try:
    y=get_html('https://www.1337xxx.to'+lk,headers=base_header,timeout=10,verify=False).content()
    
                
                
    regex='href="magnet(.+?)"'
    m2=re.compile(regex,re.DOTALL).findall(y)
    
    title=nm
    
    
    res_c=title
    if '4k' in res_c:
          res='2160'
    elif '2160' in res_c:
          res='2160'
    elif '1080' in res_c:
          res='1080'
    elif '720' in res_c:
          res='720'
    elif '480' in res_c:
          res='480'
    elif '360' in res_c:
          res='360'
    else:
          res='HD'
    try:
         o_size=size
         
         size=float(o_size.replace('GB','').replace('MB','').replace(",",'').strip())
         if 'MB' in o_size:
           size=size/1000
    except Exception as e:
        
        size=0



              
      
    max_size=int(Addon.getSetting("size_limit"))
    
    if size<max_size:
       
       all_links.append((title,'magnet'+m2[0],str(size),res))
   
       global_var=all_links
   except Exception as e:
       log.warning('Error 1337x:'+str(e))
def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all,all_links
  
    if tv_movie=='movie':
        search_url=clean_name(original_title,1).replace(' ','%20')
    else:
        
        if Addon.getSetting('debrid_select')=='0' :
                
            search_url=[clean_name(original_title,1).replace(' ','%20')+'%20'+'S'+season_n,clean_name(original_title,1).replace(' ','%20')+'%20'+'s'+season_n+'e'+episode_n,clean_name(original_title,1).replace(' ','%20')+'%20'+'season '+season]
        else:
            search_url=clean_name(original_title,1).replace(' ','%20')+'%20s{0}e{1}'.format(season_n,episode_n)
        
      
    
      
    
    
    all_links=[]
    
    all_l=[]
    
    for search_url_1 in search_url:
      
        
        if stop_all==1:
            break
        x=get_html('https://www.1337xxx.to/search/%s/1/'%(search_url_1),headers=base_header,timeout=10,verify=False).content()
        log.warning('https://www.1337xxx.to/search/%s/1/'%(search_url_1))
        regex='<tr>(.+?)</tr'
        m_pre=re.compile(regex,re.DOTALL).findall(x)
      
        for item in m_pre:
            if stop_all==1:
                break
            regex='flaticon-.+?a href="(.+?)">(.+?)<.+?"coll-4 size.+?">(.+?)<'
            m=re.compile(regex,re.DOTALL).findall(item)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                i=0
                for lk,nm,size in m:
                    
                    futures.append(executor.submit(trd_data, lk,nm,size))
                    i+=1
                wait(futures)
        
        global_var=all_links
               
                
                         
    
    return global_var
        
    