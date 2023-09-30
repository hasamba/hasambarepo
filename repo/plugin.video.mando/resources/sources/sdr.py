# -*- coding: utf-8 -*-
import re,xbmcaddon
import time,sys

global global_var,stop_all#global
global_var=[]
stop_all=0
from  resources.modules.client import get_html
 
from resources.modules.general import clean_name,check_link,server_data,replaceHTMLCodes,domain_s,similar,all_colors,base_header
from  resources.modules import cache
try:
    from resources.modules.general import Addon,get_imdb
except:
  import Addon
type=['movie','tv','torrent']

import urllib,logging,base64,json


from resources.modules import log

import xbmcvfs,urllib,urllib.parse
xbmc_tranlate_path=xbmcvfs.translatePath

color=all_colors[112]
def load_requests_lib():
    path1=xbmc_tranlate_path('special://home/addons/script.module.requests/lib')
    sys.path.append( path1)
    path1=xbmc_tranlate_path('special://home/addons/script.module.urllib3/lib')
    sys.path.append( path1)
    path1=xbmc_tranlate_path('special://home/addons/script.module.chardet/lib')
    sys.path.append( path1)
    path1=xbmc_tranlate_path('special://home/addons/script.module.certifi/lib')
    sys.path.append( path1)
    path1=xbmc_tranlate_path('special://home/addons/script.module.idna/lib')
    sys.path.append( path1)
    path1=xbmc_tranlate_path('special://home/addons/script.module.futures/lib')
    sys.path.append( path1)
def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all
    all_links=[]
    if (tv_movie=='tv'):
        load_requests_lib()
        from resources.modules.sdr_api import search_all,login,check_connection,get_token,get_play_link
        Addon = xbmcaddon.Addon()
        if (Addon.getSetting('username')!=""):
            cookie=cache.get(login, 0,Addon.getSetting('username'),Addon.getSetting('Password_sdr'),table='sdr')
            connected,cookie=check_connection(cookie)
        
           
            all_items,max_count=search_all(original_title)
            
            
            log.warning(cookie)
            token=get_token(all_items[0]['sid'],season,episode,cookie)
            log.warning(token)
            link,head=get_play_link(token,all_items[0]['sid'],season,episode,cookie)
            log.warning(link)
            res='480'
            if 'HD/1080' in link:
                res='1080'
       
                
            size='0'
            all_links.append((original_title+' S'+season_n+'E'+episode_n,link,str(size),res))
                       
            global_var=all_links
    return global_var