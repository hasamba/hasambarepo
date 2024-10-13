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
def get_vstram_title(original_name,html2):
    name1=original_name
   
    regex='"og:title" content="(.+?)"'
    match4=re.compile(regex).findall(html2)
  
    
    if len( match4)==0:
        
        regex='<Title>(.+?)</Title>'
        
        match4=re.compile(regex,re.DOTALL).findall(html2)
    if len(match4)==0:
         regex='name="fname" value="(.+?)"'
         match4=re.compile(regex,re.DOTALL).findall(html2)
    if len(match4)==0:
         regex='<title>(.+?)</title>'
         match4=re.compile(regex,re.DOTALL).findall(html2)
    if len(match4)==0:
         regex="title: '(.+?)',"
         match4=re.compile(regex,re.DOTALL).findall(html2)
    if len(match4)==0:
         regex='><span title="(.+?)"'
         match4=re.compile(regex,re.DOTALL).findall(html2)
    if len(match4)==0:
         regex='description" content="(.+?)"'
         match4=re.compile(regex,re.DOTALL).findall(html2)
    if len(match4)==0:
        regex='"title","(.+?)"'
        match4=re.compile(regex,re.DOTALL).findall(html2)
    if len(match4)>0:
        name1=match4[0]
    
    return name1.replace("."," ").replace('Watch','').replace('watch','').replace(' mp4','').replace('watch','').replace(' MP4','').replace(' mkv','').replace(' MKV','').replace("_",".")
    
def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all
    all_links=[]
    if tv_movie=='tv':
        nam=original_title+'.S%sE%s'%(season_n,episode_n)
        x=get_html('https://www.2embed.ru/embed/tmdb/tv?id=%s&s=%s&e=%s'%(id,season,episode),headers=base_header).content()
        regex='data-id="(.+?)"'
        m=re.compile(regex).findall(x)
        for items in m:
                y=get_html('https://www.2embed.ru/ajax/embed/play?id=%s&_token='%items,headers=base_header).json()
                title=nam
                res='HD'
                if not 'vidcloud' in y['link'].lower():
                    
                    html=get_html(y['link'],headers=base_header).content()
                    title=get_vstram_title(original_title,html)
                                
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
                all_links.append((title,'Direct_link$$$resolveurl'+y['link'],'0',res))

                global_var=all_links

    else:
        nam=original_title
        x=get_html('https://www.2embed.ru/embed/tmdb/movie?id=%s'%(id),headers=base_header).content()
        regex='data-id="(.+?)"'
        m=re.compile(regex).findall(x)
        
        for items in m:
                
                y=get_html('https://www.2embed.ru/ajax/embed/play?id=%s&_token='%items,headers=base_header).json()
                title=nam
                res='HD'
                if not 'vidcloud' in y['link'].lower():
                    
                    html=get_html(y['link'],headers=base_header).content()
                    title=get_vstram_title(original_title,html)
                                
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
                                
                all_links.append((title,'Direct_link$$$resolveurl'+y['link'],'0',res))

                global_var=all_links

    return global_var