# -*- coding: utf-8 -*-

import time

global global_var,stop_all#global
global_var=[]
stop_all=0

import re


type=['tv','movie','non_rd']

import urllib,base64,json
from resources.modules import log
from  resources.modules.client import get_html as get_html_o
from resources.modules.general import Addon,get_imdb,base_header
from  resources.modules import cache



def get_html(url,headers,data,method,data2={}):
    import cookielib,urllib,urllib2
    cookjar = cookielib.CookieJar()
    #data=urllib.urlencode(data)

    handlers = [urllib2.HTTPCookieProcessor(cookjar),urllib2.HTTPHandler(), urllib2.HTTPSHandler()]
                   
    opener = urllib2.build_opener(*handlers)
   
   
    if len(data2)>0:
        request = urllib2.Request(url,  headers=headers,data=urllib.urlencode(data2))
    elif len(data)>0:
       
        request = urllib2.Request(url,  headers=headers,data=json.dumps(data).encode("utf-8"))
    else:
        request = urllib2.Request(url,  headers=headers)
    request.get_method = lambda: method

    prehtml = opener.open(request,timeout=10).read()
    
    return prehtml
def get_token():
    headers={'accept': 'application/json, text/plain, */*',
    'eleven': 'false',
    'poorman': 'U2FsdGVkX19qg5Mof6tWREhZE1NNfgxb+9smoDJIV3tzWIjHLAW2yBRfAFqaRXkHj1siJlhf9IOznWZ21ON/2w=a',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'utf-8',
    'User-Agent': 'okhttp/3.12.1'}
    data={'apiLevel':'23',
          'brand':'Coolpad',
          'bundleId':'com.eleven.project.free',
          'deviceName':'cool33',
          'os':'android',
          'phoneNumber':'unknown',
          'uuid':'Ab3974ab7f1xxxxxx'}
    data='apiLevel=23&brand=Coolpad&bundleId=com.eleven.project.free&deviceName=cool33&os=android&phoneNumber=unknown&uuid=Ab3974ab7f1xxxxxx'
    url='https://cnh.tmdbapi.ru/api/mobile/1/device/add'
    x=get_html(url,headers,data,'POST')
    return json.loads(x)['data']['t']
def search_item(token,title,year,tv_movie):



    headers={'accept': 'application/json, text/plain, */*',
        'eleven': str(token),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '47',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'utf-8',
        
        'User-Agent': 'okhttp/3.12.1'}

    data={'keyword':title,
          'page':'1',
          'sortBy':'relevant',
          'type':tv_movie}
    #data='keyword=the flash&page=1&sortBy=relevant&type=tv'
    url='https://cnh.tmdbapi.ru/api/mobile/1/movie/search2'
    
    x=get_html(url,headers,data,'POST',data2=data)
    found_id=0
  
    for items in json.loads(x)['data']:
        if title.lower()==items['title'].lower() and year==str(items['release_date']):
            if tv_movie=='movie' and items['latest_season']!=None:
                continue
            found_id=items['id']
    return found_id
def get_play_link(token,id,season,episode,tv_movie):
    headers={'accept': 'application/json, text/plain, */*',
    'eleven':token,

    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'utf-8',

    'User-Agent': 'okhttp/3.12.1'}
   
    data={}
    
    
    if tv_movie=='tv':
        url='http://cnh.tmdbapi.ru/api/mobile/1/movie/detail/%s/2/null'%id
    
        x=get_html(url,headers,data,'GET')
        ep_id=None
       
        for items in json.loads(x)['data']['seasons']:
            if str(items['season_number'])!=season:
                continue
            for items_in in items['episodes']:
                if str(items_in['episode_number'])==episode:
                    ep_id=str(items_in['episode_id'])
    else:
        url='http://cnh.tmdbapi.ru/api/mobile/1/movie/detail/%s/1/null'%id
    
        x=get_html(url,headers,data,'GET')
        ep_id=str(json.loads(x)['data']['episode_id'])
    
    headers={'accept': 'application/json, text/plain, */*',
            'eleven': token,
            'Content-Type': 'application/x-www-form-urlencoded',


            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'utf-8',
      
            'User-Agent': 'okhttp/3.12.1'}
    url='https://cnh.tmdbapi.ru/api/mobile/1/episode/play_source/8768b5f938cf1da64b2c3e610c082f41'
    data2={'clientCountry':'US',
    'clientIp':'99.199.299.199',
    'episodeId':ep_id,
    'platform':'android',
    'userId':''}
    
    x=get_html(url,headers,data,'POST',data2=data2)
    print x
    found_id=0
    return x




def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all
    token=get_token()
    id=search_item(token,original_title,show_original_year,tv_movie)
    link=get_play_link(token,id,season,episode,tv_movie)
    j_link=json.loads(link)
    all_links=[]
    if tv_movie=='tv':
        nm=original_title+'.S%sE%s'%(season_n,episode_n)
    else:
        nm=original_title
    for items in j_link['data']:
        for itt in j_link['data'][items]:
            '''
            try:
                try_head = get_html_o(itt['url'],headers=base_header, stream=True,verify=False,timeout=3)
                log.warning(try_head.headers())

                if 'Content-Length' in try_head.headers():
                   if int(try_head.headers['Content-Length'])>(1024*1024):
                    size=(round(float(try_head.headers['Content-Length'])/(1024*1024*1024), 2))
            
                        
            
            except:
                size=0
            '''
            all_links.append((nm,'Direct_link$$$resolveurl'+itt['url'],str(0),str(itt['quality'])))
            global_var=all_links
                
    return global_var