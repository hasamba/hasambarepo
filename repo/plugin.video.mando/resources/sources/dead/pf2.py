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
    from resources.modules.general import Addon,get_imdb,get_vstram_title
except:
  import Addon
type=['movie','tv','non_rd']

import urllib,logging,base64,json
from resources.modules import log



color=all_colors[112]
        
def random_agent():
    import random
    BR_VERS = [
        ['%s.0' % i for i in xrange(18, 43)],
        ['37.0.2062.103', '37.0.2062.120', '37.0.2062.124', '38.0.2125.101', '38.0.2125.104', '38.0.2125.111',
         '39.0.2171.71', '39.0.2171.95', '39.0.2171.99', '40.0.2214.93', '40.0.2214.111',
         '40.0.2214.115', '42.0.2311.90', '42.0.2311.135', '42.0.2311.152', '43.0.2357.81', '43.0.2357.124',
         '44.0.2403.155', '44.0.2403.157', '45.0.2454.101', '45.0.2454.85', '46.0.2490.71',
         '46.0.2490.80', '46.0.2490.86', '47.0.2526.73', '47.0.2526.80'],
        ['11.0']]
    WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1',
                'Windows NT 6.0', 'Windows NT 5.1', 'Windows NT 5.0']
    FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
    RAND_UAS = ['Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
                'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
                'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko']
    index = random.randrange(len(RAND_UAS))
    return RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES),
                                  br_ver=random.choice(BR_VERS[index]))

def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all

    all_links=[]
    imdb=cache.get(get_imdb, 999,tv_movie,id,table='pages')
      
   
    base_link = 'https://vidsrc.me/embed/'
    if tv_movie=='movie':
      get_link = base_link + '%s/' %(imdb)
    else:
 
      get_link = base_link + '%s/%s-%s/' %(imdb,season,episode)
 
    
    #html = get_html(get_link,headers=headers,data=data,verify=False).content
    if tv_movie=='tv':
       
        rf_link='https://vidsrc.me/embed/%s/%s-%s/'%(imdb,season,episode)
    else:
       
        rf_link='https://vidsrc.me/embed/%s/'%imdb
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    x=get_html(rf_link,headers=headers).content()
    regex='hash="(.+?)"'
    m=re.compile(regex,re.DOTALL).findall(x)
    for items in m:
        

        headers = {
            'authority': 'v2.vidsrc.me',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'iframe',
            'referer': 'https://v2.vidsrc.me/source/'+items,
            
            
        }
        try:
            
            y,html = get_html('https://v2.vidsrc.me/src/'+items, headers=headers,get_content=True).geturl()
            log.warning(y)
        except:
            continue

        title=original_title
        res='HD'
        
            
        
        title=get_vstram_title(original_title,html)
        if tv_movie=='tv' and 's%se%s'%(season_n,episode_n) not in title:
            title=original_title+'.s%se%s'%(season_n,episode_n)
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
        if '404' in title or 'file not found' in title.lower():
            continue
        if len(title)<2:
            continue
        all_links.append((title,'Direct_link$$$resolveurl'+y,'0',res))
        global_var=all_links
        
     
    return all_links
	