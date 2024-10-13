
# -*- coding: utf-8 -*-

import time,os
from  resources.modules import cache
global progress
progress=''
global global_var,stop_all#global
global_var=[]
stop_all=0
from resources.modules.general import Addon

import re
from resources.modules.pen_addons import download_file,unzip,gdecom
from resources.modules.general import clean_name,check_link,server_data,replaceHTMLCodes,domain_s,similar,cloudflare_request,all_colors,base_header
type=['movie','subs','non_rd']

import urllib2,urllib,logging,base64,json
from resources.modules import log
color=all_colors[6]
try:
    import xbmc,xbmcaddon
    dataDir = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
    user_dataDir=os.path.join(dataDir,'cache_f','dragon')

except Exception as e:
   
    dir_path = os.path.dirname(os.path.realpath(__file__))
    mypath=os.path.join(dir_path,'..\done')
    user_dataDir=os.path.join(mypath,'cache_f','dragon')
if not os.path.exists(user_dataDir):
    os.makedirs(user_dataDir)
        
from  resources.modules.client import get_html
def renew_data(path,l_list):

    log.warning('Downloaing')
    
    download_file(l_list,path)
    log.warning('Extract')

    unzip(os.path.join(path, "fixed_list.txt"),user_dataDir)
    log.warning('Done D')

    
    
    return 'ok'

def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all,progress
    from resources.modules.google_solve import googledrive_resolve
    if Addon.getSetting("unfilter_test") !='1122':
        return []
    tmdbKey='653bb8af90162bd98fc7ee32bcbbfb3d'
    if tv_movie=='tv':
  
       url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&append_to_response=external_ids&language=he'%(id,tmdbKey)
       n_value='name'
    else:
       
       url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&append_to_response=external_ids&language=he'%(id,tmdbKey)
       n_value='title'
    try:
        
        name=get_html(url2,timeout=10).json()[n_value]
    except:
        name=original_title
        
    all_links=[]
    name=name.replace("'","")
    progress='Start'
    start_time=time.time()
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    
    l_list='http://ngarba.xyz/adds/xyz/RD.txt'
    
    cacheFile=os.path.join(user_dataDir,'localfile.txt')
    
    if not os.path.exists(cacheFile):
        
        all_img=cache.get(renew_data,0,user_dataDir,l_list, table='posters')
    else:
        
        
        all_img=cache.get(renew_data,72,user_dataDir,l_list, table='posters')

    

    progress='DB'
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    try:
        dbcur.execute("SELECT * FROM MyTable where name like '%{0}%' and year ='{1}' ".format(name,show_original_year))
    except:
        all_img=cache.get(renew_data,0,user_dataDir,l_list, table='posters')
        
    if tv_movie=='movie':
        dbcur.execute("SELECT * FROM MyTable where name like '%{0}%' and year ='{1}' ".format(name,show_original_year))
    else:
        dbcur.execute("SELECT * FROM MyTable where father like '%{0}%' and father like '%{1}%'".format(name,'עונה '+season))
    try:
       match = dbcur.fetchall()
    except:
        renew_data(user_dataDir,l_list)
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        if tv_movie=='movie':
            dbcur.execute("SELECT * FROM MyTable where name like '%{0}%' and year ='{1}' ".format(name,show_original_year))
        else:
            dbcur.execute("SELECT * FROM MyTable where father like '%{0}%' and father like '%{1}%'".format(name,'עונה '+season))
        
        match = dbcur.fetchall()
    count=0
    if len(match)==0 and tv_movie=='tv':
        dbcur.execute("SELECT * FROM MyTable where data like  '%\"tmdb\": \"{0}\"%' and data like '%\"Season\": \"{1}\",  \"Episode\": \"{2}\",%'".format(id,season,episode))
        match = dbcur.fetchall()
    
    
    
    for index,name,f_link,icon,fanart,plot,data,date,year,genre,father,type in match:
        progress='Links-'+str(count)
        count+=1
        try:
            f_link=gdecom(f_link)
        except:
           pass
        
        try:
                data=json.loads(data)
         
        except:
                data={'originaltitle':name,'Season':'%20','Episode':'%20'}
                
        if tv_movie=='tv':

            if not ((data['Season'].strip()==season and data['Episode'].strip()==episode) or (('עונה#%s#פרק#%s"'%(season,episode)).decode('utf8') in name.replace(' ','#'))):
                
                continue
        f_link=f_link.replace('\n',"").replace('\r',"")
        if '$$$' in f_link:
            f_link_s=f_link.split('$$$')
            for link_in in f_link_s:
                progress='Check-'+str(count)
                
                size=0
                 
                
            
                if "1080" in name:
                  res="1080"
                elif "720" in name:
                  res="720"
                elif "480" in name:
                   res="480"
                else:
                    res='1080'
                if tv_movie=='tv':
                    name1=original_title.replace('FHD','1080').replace('HD','720')+'.S%sE%s'%(season_n,episode_n)
                else:
                    name1=original_title.replace('FHD','1080').replace('HD','720')+'.'+show_original_year
                
                all_links.append((name1,'HEBSOURCE$$$'+link_in,str(size),res))
                global_var=all_links
        else:
            progress='Check2-'+str(count)
            #name1,match_s,res,check=server_data(f_link,original_title)
            
            size=0
             
            
            if tv_movie=='tv':
                name1=original_title.replace('FHD','1080').replace('HD','720')+'.S%sE%s'%(season_n,episode_n)
            else:
                name1=original_title.replace('FHD','1080').replace('HD','720')+'.'+show_original_year
         
            if "1080" in name:
              res="1080"
            elif "720" in name:
              res="720"
            elif "480" in name:
               res="480"
            else:
                res='1080'
           
            all_links.append((name1,'HEBSOURCE$$$'+f_link,str(size),res))
            global_var=all_links
               
    elapsed_time = time.time() - start_time
    progress=' Done '+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    return global_var
    