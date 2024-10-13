# -*- coding: utf-8 -*-
import re
import time
from  resources.modules.client import get_html
global global_var,stop_all#global
global_var=[]
stop_all=0

 
from resources.modules.general import clean_name,check_link,server_data,replaceHTMLCodes,domain_s,similar,all_colors,base_header
from  resources.modules import cache
try:
    from resources.modules.general import Addon,get_vstram_title
except:
  import Addon
type=['movie','tv','non_rd']

import urllib2,urllib,logging,base64,json


import urllib2,urllib,logging,base64,json

from resources.modules import log
color=all_colors[112]

def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all
    all_links=[]
    
    url='https://mixdrop.me/?s='+original_title.replace(' ','%20')
    log.warning(url)
    x = get_html(url, headers=base_header).content()
    regex='<div class="result-item">(.+?)</article>'

    m=re.compile(regex,re.DOTALL).findall(x)
    
    for items in m:
        regex='<div class="title"><a href="(.+?)">(.+?)<.+?class="year">(.+?)<'

        m2=re.compile(regex,re.DOTALL).findall(items)
        for lk,nm,yr in m2:
            if nm.lower()==clean_name(original_title,1).lower() and yr==show_original_year:
                y = get_html(lk, headers=base_header).content()
                regex='data-vs="(.+?)"'

                m3=re.compile(regex,re.DOTALL).findall(y)
                z=get_html(m3[0], headers=base_header).content()
                regex='form method="post" action="(.+?)"'
                m4=re.compile(regex,re.DOTALL).findall(z)
                log.warning(m4)
                regex='name="playID" value="(.+?)"'
                m5=re.compile(regex).findall(z)[0]
                headers = {
                    'authority': 'videospider.stream',
                    'pragma': 'no-cache',
                    'cache-control': 'no-cache',
                    'upgrade-insecure-requests': '1',
                    'origin': 'https://videospider.stream',
                    'content-type': 'application/x-www-form-urlencoded',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'referer': m4[0],
                    'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
                    'cookie': '__cfduid=dd9044067d20ba63a4ceed4c48303e4fa1605435532',
                }

                

                data = {
                  'playID': m5
                }

                response = get_html(m4[0], headers=headers, data=data).content()
                log.warning(response)

                #all_links.append((title,'Direct_link$$$resolveurlresolveprime'+lkk,str(0),str(res)))

                #global_var=all_links
                            
    return global_var