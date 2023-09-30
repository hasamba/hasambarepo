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
type=['tv','non_rd']

import urllib2,urllib,logging,base64,json

from resources.modules import log
import urllib2,urllib,logging,base64,json


color=all_colors[112]
def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all
    all_links=[]
    if tv_movie=='movie':
        return []
    c_name=clean_name(original_title,1).lower()
    search_string=c_name+' season '+season
    headers = {
        'authority': 'tvshows.cc',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': 'text/plain, */*; q=0.01',
        'dnt': '1',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://tvshows.cc',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        
        
        
    }

    data = {
      'action': 'ajaxsearchlite_search',
      'aslp': search_string,
      'asid': '1',
      'options': 'qtranslate_lang=0&set_intitle=None&customset%5B%5D=seasons'
    }

    x = get_html('https://tvshows.cc/wp-content/plugins/ajax-search-lite/ajax_search.php', headers=headers, data=data).content()
    regex="<div class='asl_content'>(.+?)<div class='clear'>"
    m=re.compile(regex,re.DOTALL).findall(x)
    div=1024*104*1024
    for items in m:
        regex="class=\"asl_res_url\" href='(.+?)'>(.+?)<"
        m2=re.compile(regex,re.DOTALL).findall(x)
        for lk,nm in m2:
        
            if c_name in nm.lower()   and 'season %s '%season in nm.lower():
                log.warning('INININ')
                y = get_html(lk,headers=headers).content()
                
                regex='<div itemprop="episode"(.+?)</a></div></div></div></div></div>'
                m3=re.compile(regex,re.DOTALL).findall(y)
                
                for itt in m3:
                    if 'Episode %s:'%episode in itt:
                        regex='<a id="btn-(.+?)" href="\#" class="main-btn with-download-icon small" data-type="(.+?)">'
                        m4=re.compile(regex).findall(itt)
                        log.warning(m4)
                        f_idd=''
                        for idd, ser in m4:
                            if ser=='Keep2Share':
                               f_idd=idd
                        if f_idd!='':
                               regex='arr\["btn-%s"\] \= "(.+?)"'%f_idd
                               m5=re.compile(regex,re.DOTALL).findall(y)
                               log.warning(regex)
                               log.warning(m5)
                               f_lk=(m5[0].decode('base64'))
                               
                               headers = {
                                    'authority': 'api.k2s.cc',
                                    'pragma': 'no-cache',
                                    'cache-control': 'no-cache',
                                    'accept': 'application/json, text/plain, */*',
                                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
                                    'dnt': '1',
                                    'origin': 'https://k2s.cc',
                                    'sec-fetch-site': 'same-site',
                                    'sec-fetch-mode': 'cors',
                                    'sec-fetch-dest': 'empty',
                                    'referer': f_lk,
                                    'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
                                    
                                }
                               regex='file/(.+?)/'
                               f_id=re.compile(regex).findall(f_lk)[0]
   

                               data = {"grant_type":"client_credentials","client_id":"k2s_web_app","client_secret":"pjc8pyZv7vhscexepFNzmu4P"}
                               token,cook=get_html('https://api.k2s.cc/v1/auth/token',headers=headers,data=data,get_cookies=True).content()
                     
                               log.warning(token)
                               log.warning(cook)
                               log.warning('https://api.k2s.cc/v1/files/{0}?referer=https%3A%2F%2Ftvshows.cc'.format(f_id))
                               z=get_html('https://api.k2s.cc/v1/files/{0}?referer=https%3A%2F%2Ftvshows.cc'.format(f_id),headers=headers,cookies=cook).json()
                               nm=z['name']
                               size=0
                               
                               try:
                                   size=z['size']/div
                               except:
                                   pass
                               if '4k' in nm:
                                          res='2160'
                               elif '2160' in nm:
                                      res='2160'
                               elif '1080' in nm:
                                      res='1080'
                               elif '720' in nm:
                                      res='720'
                               elif '480' in nm:
                                      res='480'
                               elif '360' in nm:
                                      res='360'
                               else:
                                      res='HD'
            
                               f_link=z['videoPreview']['alternativeResolutions'][0]['url']
                               all_links.append((nm,f_link,str(size),res))
           
                               global_var=all_links
               
        break

                

    
    return global_var