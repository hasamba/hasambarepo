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
        


def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all

    all_links=[]
    
    if tv_movie=='tv':
        search_string=clean_name(original_title,1).lower().replace(' ','%20')+'%20season%20'+season
    else:
        search_string=clean_name(original_title,1).lower().replace(' ','%20')
    c_name=clean_name(original_title,1).lower().replace(':','')
    headers = {
        'authority': 'primewire.show',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
        
    }
    
    x = get_html('https://primewire.show/search/'+search_string, headers=headers).content()


    regex='data-rating\="(.+?)</p>'
    m=re.compile(regex,re.DOTALL).findall(x)

    div_1g=1024*1024*1024
    for items in m:

        regex='a href="(.+?)".+?title="(.+?)"'
        m2=re.compile(regex,re.DOTALL).findall(items)
        for lk,nm in m2:
 
        
            if tv_movie=='tv':
                
                if c_name in nm.lower().replace(':','') and ' season %s$'%season in nm.lower()+'$':
                    
                    y=get_html('https://primewire.show'+lk, headers=headers).content()
                    
                    regex='"episode": \[(.+?)\]'
                    m3=re.compile(regex,re.DOTALL).findall(y)
                    j_m=json.loads('['+m3[0]+']')
                    for it in j_m:
                        if str(it['episodeNumber'])==episode:
                            f_url=it['url']
                            headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
                                'Accept': 'text/html, */*; q=0.01',
                                'Accept-Language': 'en-US,en;q=0.5',
                                'X-Requested-With': 'XMLHttpRequest',
                                'Connection': 'keep-alive',
                               
                                'Pragma': 'no-cache',
                                'Cache-Control': 'no-cache',
                                'TE': 'Trailers',
                            }
                            url=f_url
                            log.warning(f_url)
                            x=get_html(url,headers=headers).json()
                            link=x[0]['src'].replace(str(x[0]['label']),str(x[0]['max']))
                            title=re.compile('name=(.+?)\&').findall(link)[0]
                            size=0
                 
                            if 'Content-Length' in try_head:
              
                                if int(try_head['Content-Length'])>(1024*1024):
                                    size=round(float(try_head['Content-Length'])/(1024*1024*1024),2)
                            if 'content-length' in try_head:
              
                                if int(try_head['content-length'])>(1024*1024):
                                    size=round(float(try_head['content-length'])/(1024*1024*1024),2)
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
                            all_links.append((title,'Direct_link$$$resolveurl'+link,str(size),res))
                            global_var=all_links
            else:
                if (c_name in nm.lower().replace(':','') and show_original_year in nm) or (c_name == nm.lower().replace(':','')):
                            url='https://primewire.show'+lk
               
                            z=get_html(url,headers=headers).content()
                            regex="window\.history\.pushState\(\{\},'', '(.+?)'"
                            ur=re.compile(regex).findall(z)[0]
              
                            headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
                                'Accept': 'text/html, */*; q=0.01',
                                'Accept-Language': 'en-US,en;q=0.5',
                                'X-Requested-With': 'XMLHttpRequest',
                                'Connection': 'keep-alive',
                               
                                'Pragma': 'no-cache',
                                'Cache-Control': 'no-cache',
                                'TE': 'Trailers',
                            }

                            x=get_html('https://primewire.show'+ur,headers=headers).json()
                          
                            link=x[0]['src'].replace(str(x[0]['label']),str(x[0]['max']))
                            title=re.compile('name=(.+?)\&').findall(link)[0]
                            try_head = get_html(link,headers=base_header, stream=True,verify=False,timeout=15).headers()
                            size=0
              
                            if 'Content-Length' in try_head:
              
                                if int(try_head['Content-Length'])>(1024*1024):
                                    size=round(float(try_head['Content-Length'])/(1024*1024*1024),2)
                            if 'content-length' in try_head:
              
                                if int(try_head['content-length'])>(1024*1024):
                                    size=round(float(try_head['content-length'])/(1024*1024*1024),2)
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
                            all_links.append((title,'Direct_link$$$resolveurl$$$direct'+link,str(size),res))
                            global_var=all_links
     
    return all_links
	