# -*- coding: utf-8 -*-
import re
import time

global global_var,stop_all#global
global_var=[]
stop_all=0

from  resources.modules.client import get_html
from resources.modules.general import clean_name,check_link,server_data,replaceHTMLCodes,domain_s,similar,all_colors,base_header
from  resources.modules import cache,prime_decode
try:
    from resources.modules.general import Addon,get_imdb
except:
  import Addon
type=['movie','tv','non_rd']



from resources.modules import log
import urllib,logging,base64,json


color=all_colors[112]
def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all
    all_links=[]
    headers = {
        'authority': 'primewire.unblockit.buzz',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
        
    }
    imdb_id=cache.get(get_imdb, 999,tv_movie,id,table='pages')
        
    
    x,cook=get_html("https://primewire.unblockit.buzz/?s=%s&t=y&m=m&w=q"%(imdb_id),headers=base_header,get_cookies=True,timeout=10).content()
   
    
   
    regex='div class="index_item index_item_ie".+?a href="(.+?)"'
    
    m=re.compile(regex,re.DOTALL).findall(x)[0]
    #time.sleep(1)
    y=get_html('https://primewire.unblockit.buzz'+m,headers=headers,cookies=cook).content()
    log.warning('https://primewire.unblockit.buzz'+m)
    if tv_movie=='tv':
        regex='<div class="tv_episode_item">(.+?)</div>'
        m_pre=re.compile(regex,re.DOTALL).findall(y)
        for items in m_pre:
            regex='a href="(.+?)"'
            m2=re.compile(regex,re.DOTALL).findall(items)[0]+'$$$'
            
            if 'season-%s-episode-%s$$$'%(season,episode) in m2:
                    #time.sleep(1)
                    y=get_html('https://primewire.unblockit.buzz'+m2.replace('$$$',''),headers=headers,cookies=cook).content()
                    regex='span id="user-data".+?v="(.+?)"'
                    m3=re.compile(regex).findall(y)[0]
                  
                    all_p_links=prime_decode.decode(m3)
                    nam=original_title+'.S%sE%s'%(season_n,episode_n)
                    for link in all_p_links:
                        all_links.append((nam,'Direct_link$$$resolveurlresolveprime'+link,'0','HD'))

                        global_var=all_links
    else:
            regex='span id="user-data".+?v="(.+?)"'

            
            m3=re.compile(regex).findall(y)[0]
            
            all_p_links=prime_decode.decode(m3)
            nam=original_title
            for link in all_p_links:
                all_links.append((nam,'Direct_link$$$resolveurlresolveprime'+link,'0','HD'))

                global_var=all_links

    
    return global_var