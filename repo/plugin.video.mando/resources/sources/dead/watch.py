# -*- coding: utf-8 -*-

import time

global global_var,stop_all#global
global_var=[]
stop_all=0

import re


type=['tv','movie','non_rd']
from resources.modules import log
import urllib,logging,base64,json
from  resources.modules.client import get_html
from resources.modules.general import Addon,get_imdb
from  resources.modules import cache
def get_key():
    
    headers={

    'user-agent': 'WATCHED/1.0.2 (android)',
    'accept': 'application/json',
    'Content-Type': 'application/json',


    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
    }
    data={"x":"dGVzdGluZzoHfbiCN4XyBnPD7qt8ccvSEzjS/1zg9hbb5etgJKvIAsqSFb2rgsogKfijBVTiyU9BecL54Q1TvGxZJXQvbIopbAXybzN54CQ783NROu3dtnw7z4h8+cPec5AKCg2xZibWVtpOO8IN7Tux82Q98+rrWk9cPMYZ7pM5sSicELLdjj8Z5yjAvITU6/Mqj7HrSJ0bAUzjlrYF5r6BFDjhffugqPICZizwk0eL+InZDyjtW2d6Z2x1B1Q4CDVUuyR+LrqYN491wv25BMi/Y3rRKKiJ+VXEDaLONLrPK7D+uJ303OUMg4PyKb/4KevlteMXJDbk9JxZEeL2zoTW0RG/EOFiKfvGpbXbZ2AUDKp0yGgFc6o7WVMSNmOk8ac69BmMLEuP7fh8rqc2v9W85/XQDqSGJUeqT/JPCruDv7ehE9+U2cWyJqVkaq9wRcCW86DG9ISM/OBihf9eoy9pkLMgOAkjpIyOtKjaq2QoX/8Ob3qnDys4eWGiVB77Z0zN/WmrS87CBtgWFsYw0xwUvfpoKQJqjBUKXAcydaMEtDc6qB/lZZ0CPaqj0gpXHNYRlGnBY10KZiBD+4ihprNxyS0bkN7Y3VLsHpTasYyyEqUeaXFQvMNfns2bowPc8UIUg5MtlvHnEzwwNK6KLdInGWK8JNAr5i3IF99jYL6W/6xkBZrJOf4RfWTunT801rSXkLdUvTSZqGAQYDxMww3JU5L4Le6eP7aX6WT/r/stO6QtND/hh3NN4xYMvUoJTDA3KB+aVYgIkspaHmGBKAJcJSZc5vtte8bGnTH1QHiNmyVfFxSnaYdfVDGElhf1fhl0pP/ci3wr1HrueLfZsGD1XS/Aac77eUWcLWhA4bdS1joCfhItd0Cz6Qizbgx7zUfDByWtN+jstzmzUbz7tA23CBIrXEDMLktSib1wDPt0xt0TE0ocFY1XdZbZnwUvvI6mYiGe07Xj09WXJvCzU6cFgxZk0A/E3mytAvWV63H/olm3wA+RiAr3rp8vb7ToYEb4yF9fVNhPm0opTLa3snH9+pAH80p13b+l+rhhitETTz0qHlryw0A7YdfWQQ0/U4dK+hHSlKyksph4dSINchD2fm43Ky+xsOaMnBvQeibvFe5xl0bRym6+au8Bh5oAnf2SApILM2cOJk538C3xOfNozAUzilcLyC9mXBI2ianF5zeWLYuDsHpca07Lsegi3NquoZoM1HcjPVLJN0+VoxO7M13vyJVjx0TgjbRyvPSQAPNlRed6nU6FJFQbbtr5THbDjgivmMq1vsloF6b217PxSJkmtiQT9c/WR3c6ghT5Z216Igeh2lfN2LQhstg7UF62CDrsYxssO8CE26o9lrDSM2d792janF98yk8cd1F3db9NaAL7buySYLbqEhDEPC/6AQjrsDxl+zMDxsCW8UIZSID4qysqkGSoZFvn/5kUbpMc9yh/Sy/lCSi4NfcdIY/wACTMce7thMo6dGZhTJbo0B6EfYHgma4OqRhtBCkhew20kpt9ZuKY8hQwhcPft8MFh4tRUScgE9wJZGeIUfjkEMHqHAgjFl3MXwS5WpbK/sFuD2UChDbKaafFDdRx1EanRvreoPrwcZQYnCsEhdltIR9XH3SuECzNIlU/9DLPcaVSs5wDz09fx+8DU2SD8qhqoqf6pk3KCekxUMdy/V3dyJfVuhaaFrOzriyCm+SfLdUif8aSJlrIEbujBVuHVx+97JuIaPJX3ib78FWoEierWUyxE8Zu3FJrWE37uBUhPaq8V4Fsfshp+kMz9ieKBbvgQKgyBOEAahrWF1cS0GLbuyuftKrEVXf/VuBmYI8hEu56o6JvZtO1fJQpqtC42wcUzX/oPZvCz3IF+to8GYWJbAjq/Qemue8frZhDeO3f9lGOA/9Ovw=="}
    x=get_html("https://www.watched.com/api/box/ping",json=data,headers=headers).json()
    log.warning('Key:')
    key=x['response']['signed']
    log.warning(key)
    return key
def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all
    base_url='http://huhu.to/%s.watched'
    servers=['hot-series-de/item','hot/source','english-hd-2/source','english-hd-3/source','english-hd-4/source','hot-series-de-2/source']
    key=get_key()
    imdb_id=cache.get(get_imdb, 999,tv_movie,id,table='pages')
    headers={

        'watched-sig': key,
        'user-agent': 'WATCHED/0.17.3 (android)',
        'Content-Type': 'application/json',


        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'utf-8'}


    if tv_movie=='tv':
        Body={
            "language":"en",
            "region":"US",
            "type":"series",
            "ids":{
                "tmdb_id":int(id),
                "imdb_id":imdb_id,

            },
            "name":original_title,

            "originalName":original_title,
            "releaseDate":"%s-10-07"%show_original_year,
            "episode":{
                
                
                "season":int(season),
                "episode":int(episode)
            }
        }
    else:
        Body={
        "language":"en",
        "region":"US",
        "type":'movie',
        "ids":{
            "tmdb_id":int(id),
            "imdb_id":imdb_id,
            "facebook":"",
            "instagram":"",
            "twitter":""
        },
        "name":original_title,
        "nameTranslations":{

        },
        "originalName":original_title,
        "originalName":original_title,
        "releaseDate":"%s-01-01"%show_original_year,
        "episode":{
            
        }
    }
    
    all_links=[]
    for items in servers:
        log.warning(items)
        x=get_html(base_url%items,headers=headers,json=Body).json()
        log.warning(json.dumps(x))
        if x :
         if 'episodes' in x:
             
             for itt in x['episodes']:
                
                 if str(itt['season'])==season and str(itt['episode'])==episode:
                     
                     for itt2 in itt['sources']:
                        lk=itt2['url']
                        if itt2['languages'][0]=='en':
                            
                            if '4k' in lk:
                                      res='2160'
                            elif '2160' in lk:
                                  res='2160'
                            elif '1080' in lk:
                                  res='1080'
                            elif '720' in lk:
                                  res='720'
                            elif '480' in lk:
                                  res='480'
                            elif '360' in lk:
                                  res='360'
                            else:
                                  res='HD'
                            nm=original_title
                            if tv_movie=='tv':
                                nm=original_title+'.S%sE%s'%(season_n,episode_n)
                            all_links.append((nm,'Direct_link$$$resolveurl'+lk,str(0),res))
                            global_var=all_links
         else:
          for itt in x:
           if 'url' in itt:
            lk=itt['url']
            if itt['languages'][0]=='en':
                if '4k' in lk:
                          res='2160'
                elif '2160' in lk:
                      res='2160'
                elif '1080' in lk:
                      res='1080'
                elif '720' in lk:
                      res='720'
                elif '480' in lk:
                      res='480'
                elif '360' in lk:
                      res='360'
                else:
                      res='HD'
                nm=original_title
                if tv_movie=='tv':
                    nm=original_title+'.S%sE%s'%(season_n,episode_n)
                all_links.append((nm,'Direct_link$$$resolveurl'+lk,str(0),res))
                global_var=all_links
                
    return global_var