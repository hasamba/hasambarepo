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

import urllib,logging,base64,json
from resources.modules import log
try:
    url_encode=urllib.urlencode
except:
    
    url_encode=urllib.parse.urlencode
    



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
        lk='https://vidsrc.me/embed/%s/%s-%s/'%(imdb,season,episode)
        rf_link='https://vidsrc.me/server1/%s/%s-%s/'%(imdb,season,episode)
    else:
        lk='https://v2.vidsrc.me/embed/%s/'%imdb
        rf_link='https://vidsrc.me/server1/%s/'%imdb
        
        x=get_html(lk,headers=base_header).content()
     
        regex='data-hash="(.+?)"'
        m=re.compile(regex).findall(x)
     
        for items in m:
            log.warning(items)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://v2.vidsrc.me/',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'iframe',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'cross-site',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
            }

            response = get_html('https://v2.vidsrc.me/src/'+items, headers=headers).content()
            log.warning(response)
            continue
            regex='"file": "(.+?)"'
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Origin': 'https://vidsrc.stream',
                'Connection': 'keep-alive',
                'Referer': 'https://vidsrc.stream/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
            }

            link=re.compile(regex).findall(response)[0]
            
            head=url_encode(headers)
            link=link+"|"+head
           
            res='720'
            res1=res.replace('p','')
            #name1,match_s,res,check=server_data(items['file'],name)
                
            if 1:#check:
                if tv_movie=='tv':
                    title=clean_name(original_title,1)+'.S%sE%s'%(season_n,episode_n)
                else:
                    title=clean_name(original_title,1)+'.'+show_original_year
                all_links.append((title,'Direct_link$$$resolveurl'+link,'0',res1))
                global_var=all_links
        
     
    return all_links
	