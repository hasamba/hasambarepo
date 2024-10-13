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





color=all_colors[112]
        


def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all

    all_links=[]
    headers = {
        'authority': 'lookmovie.io',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'dnt': '1',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',

        'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
        
    }

    params = (
        ('q', original_title),
    )

    if tv_movie=='tv':
        t_title=clean_name(original_title,1)+'.S%sE%s'%(season_n,episode_n)
    else:
        t_title=clean_name(original_title,1)+'.'+show_original_year
        
    if tv_movie=='tv':
        r = get_html('https://lookmovie.io/api/v1/shows/search/', headers=headers, params=params).json()
        for items in r['result']:
            if items['title'].lower()==clean_name(original_title,1).lower() and show_original_year==items['year']:
                lk='https://lookmovie.io/shows/view/'+items['slug']
                x=get_html(lk,header=headers).content()
                regex='seasons: \[(.+?)\]'
                m='['+re.compile(regex,re.DOTALL).findall(x)[0].replace('title',"'title'").replace(' season'," 'season'").replace('id_episode',"'id_episode'").replace(' episode'," 'episode'").replace("'",'"')+']'
                m=m.split("},")
                for itt in m:
                    
                    regex='"episode": "%s", "id_episode": (.+?), "season": "%s"'%(episode,season)
                    m=re.compile(regex).findall(itt)
                    if len(m)>0:
                        
                        params = (
                            ('slug', items['slug']),
                        )
                        
                        y = get_html('https://false-promise.lookmovie.io/api/v1/storage/shows', headers=headers, params=params).json()
                        
                        link='https://lookmovie.io/manifests/shows/json/%s/%s/%s/master.m3u8'%(y['data']['accessToken'],y['data']['expires'],m[0])
                        z=get_html(link,headers=headers).json()
                        for itt2 in z:
                            if 'auto' in itt2 or 'dummy/earth' in z[itt2]:
                                continue
                            all_links.append((t_title,'Direct_link$$$resolveurl'+z[itt2],'0',itt2))
                            global_var=all_links
                
                
        
    else:
        r = get_html('https://lookmovie.io/api/v1/movies/search/', headers=headers, params=params).json()
        for items in r['result']:
            if items['title'].lower()==clean_name(original_title,1).lower() and show_original_year==items['year']:
                lk='https://lookmovie.io/movies/view/'+items['slug']
                
                x=get_html(lk,header=headers).content()
                regex='id_movie\: (.+?),'
                m=re.compile(regex).findall(x)[0]
                params = (
                    ('id_movie', m),
                )
               
                r=get_html('https://false-promise.lookmovie.io/api/v1/storage/movies',header=headers, params=params).json()
                
                link='https://lookmovie.io/manifests/movies/json/%s/%s/%s/master.m3u8'%(m,r['data']['expires'],r['data']['accessToken'])
                      
                z=get_html(link,headers=headers).json()
                
                for itt2 in z:
                
                    if 'auto' in itt2 or 'dummy/earth' in z[itt2]:
                        continue
                    
                    all_links.append((t_title,'Direct_link$$$resolveurl'+z[itt2],'0',itt2.replace('p','')))
                    global_var=all_links
    return all_links
	