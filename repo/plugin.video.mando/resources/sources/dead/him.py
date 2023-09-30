# -*- coding: utf-8 -*-

import time

global global_var,stop_all#global
global_var=[]
stop_all=0

import re


type=['tv','movie','non_rd']

import urllib,logging,base64,json
from  resources.modules.client import get_html
def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all

    
    if tv_movie=='movie':
        search_url=original_title+'.'+show_original_year
    else:
        search_url=original_title+'.S%sE%s'%(season_n,episode_n)
    all_links=[]
    
    headers = {
        'authority': 'drive.himanshurahi.workers.dev',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://drive.himanshurahi.workers.dev',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://drive.himanshurahi.workers.dev/0:search?q=rampage.2018',
        'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '__cfduid=d5d59c5d1be02ae8684b36fb8a51995cc1605419008',
    }

    data = {
      'q': search_url,
      'page_token': '',
      'page_index': '0'
    }

    response = get_html('https://drive.himanshurahi.workers.dev/0:search', headers=headers, data=data).json()
    
    all_ep=[' s%se%s '%(season_n,episode_n),'.s%se%s.'%(season_n,episode_n),' s%s e%s '%(season_n,episode_n),'.s%s.e%s.'%(season_n,episode_n),'.s%s e%s.'%(season_n,episode_n)]
    search_term=original_title
    div_1g=1024*1024*1024
    for items in response['data']['files']:
       
     if search_term.lower().replace('%20',' ').replace(' ','.') in items['name'].lower().replace(' ','.'):
            lk='https://drive.google.com/file/d/%s/view'%items['id']
            size=0
            try:
                size=items['size']/div_1g
            except:
                pass
            nam=items['name']
            if '4k' in nam:
                  res='2160'
            elif '2160' in nam:
                  res='2160'
            elif '1080' in nam:
                  res='1080'
            elif '720' in nam:
                  res='720'
            elif '480' in nam:
                  res='480'
            elif '360' in nam:
                  res='360'
            else:
                 res='HD'
            all_links.append((items['name'],'Direct_link$$$resolveurlresolveprime'+lk,size,res))
            global_var=all_links
    return global_var