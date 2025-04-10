 # -*- coding: utf-8 -*-
import sys,urllib,logging,json,os
from resources.modules import cache
import xbmcgui,xbmcplugin,xbmc,xbmcaddon,xbmcvfs
global pre_mode

from resources.modules import log

pre_mode=''
lang=xbmc.getLanguage(0)
Addon = xbmcaddon.Addon()
tmdb_key=Addon.getSetting("tmdb_api")


KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
if KODI_VERSION>18:
    user_dataDir = xbmcvfs.translatePath(Addon.getAddonInfo("profile"))
else:
    import xbmcvfs
    user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile"))
if not xbmcvfs.exists(user_dataDir+'/'):
     os.makedirs(user_dataDir)
if KODI_VERSION<=18:
    que=urllib.quote_plus
    url_encode=urllib.urlencode
else:
    import urllib.parse
    que=urllib.parse.quote_plus
    url_encode=urllib.parse.urlencode
addon_id=Addon.getAddonInfo("id")
def get_html_g():
    from  resources.modules.client import get_html
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }
    
    try:
        html_g_tv={}
        url_g=f'https://api.themoviedb.org/3/genre/tv/list?api_key={tmdb_key}&language='+lang
        log.warning(url_g)
        html_g_tv=get_html(url_g,headers=headers).json()
         
        html_g_movie={}
        url_g=f'https://api.themoviedb.org/3/genre/movie/list?api_key={tmdb_key}&language='+lang
        html_g_movie=get_html(url_g,headers=headers).json()
    except Exception as e:
        log.warning('Err in HTML_G:'+str(e))
    return html_g_tv,html_g_movie
time_to_save=int(Addon.getSetting("save_time"))
#html_g_tv,html_g_movie=get_html_g()
html_g_tv,html_g_movie=cache.get(get_html_g,time_to_save, table='posters')
def meta_get(video_data,item):
    if item=='year' or item=='rating' or item=='votes' or item=='duration':
        try:
            int(video_data.get(item,'0'))
        except:
            try:
                float(video_data.get(item,'0'))
            except:
                video_data[item]='0'
        return video_data.get(item,'0')
    if item=='country' or item=='cast':
        return video_data.get(item,[])
    return video_data.get(item,' ')
    
def addNolink( name, url,mode,isFolder,fanart='DefaultFolder.png', iconimage="DefaultFolder.png",plot=' ',all_w_trk='',all_w={},heb_name=' ',data=' ',year=' ',generes=' ',rating=' ',trailer=' ',watched='no',original_title=' ',id=' ',season=' ',episode=' ' ,eng_name=' ',show_original_year=' ',dates=' ',dd=' ',dont_place=False):
 
            added_pre=''
            if 'http' not in fanart:
                fanart='https://'+fanart
            
            if (episode!=' ' and episode!='%20' and episode!=None) :
             
              tv_show='tv'
            else:
                tv_show='movie'
            if '%' in str(episode):
                episode=' '
            
            
            if tv_show=='tv':
                ee=str(episode)
            else:
                ee=str(id)
            
            
            time_to_save_trk=int(Addon.getSetting("time_to_save"))
            if all_w_trk!='':
                if float(all_w_trk)>=time_to_save_trk:
                    added_pre='  [COLOR yellow][I]'+'√'+'[/I][/COLOR] \n '
                elif float(all_w_trk)>1:# and float(all_w_trk)<time_to_save_trk:
                    added_pre=' [COLOR yellow][I]'+all_w_trk+'%[/I][/COLOR] \n '
            elif ee in all_w:
                    
                    
                    try:
                      if '%' in str(all_w[ee]['resume']):
                            all_w_time=all_w[ee]['resume'].replace('%','')
                      else:
                            all_w_time=int((float(all_w[ee]['resume'])*100)/float(all_w[ee]['totaltime']))
                      
                      if float(all_w_time)>=time_to_save_trk:
                        added_pre=' [COLOR yellow][I]'+'√'+'[/I][/COLOR] \n '
                      elif float(all_w_time)>1:# and float(all_w_time)<time_to_save_trk:
                        added_pre=' [COLOR yellow][I]'+str(all_w_time)+'%[/I][/COLOR] \n '
                    except Exception as e:
                        log.warning('Error in addnolink:'+str(e))
                        pass
            
            params={}
            params['name']=name
            params['iconimage']=iconimage
            params['fanart']=fanart.replace('/original//','/original/')
            params['description']=added_pre+plot.replace("%27","'")
            params['url']=url
            params['data']=data
            params['original_title']=original_title
            params['id']=id
            params['heb_name']=heb_name
            params['season']=season
            params['episode']=episode
            params['eng_name']=original_title
            params['show_original_year']=show_original_year
            params['dates']=dates
            params['dd']=dd
            params['all_w']=json.dumps(all_w)
            menu_items=[]
            
            if mode==146 or mode==15:
                if mode==15:
                    tv_movie='movie'
                else:
                    tv_movie='tv'
                menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32161), 'RunPlugin(%s)' % ('%s?url=www&original_title=%s&mode=34&name=%s&id=%s&season=%s&episode=%s')%("plugin://%s/"%addon_id,que(original_title),que(name),id,season,episode)))
                if len(id)>1:
                    if tv_movie=='tv':
                        tv_mov='tv'
                    else:
                        tv_mov='movie'
                    menu_items.append((Addon.getLocalizedString(32162), 'Action(Queue)' ))
                    menu_items.append((Addon.getLocalizedString(32163), 'RunPlugin(%s)' % ('%s?url=%s&mode=150&name=%s&data=%s')%("plugin://%s/"%addon_id,id,original_title,tv_mov) ))
                    menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32164), 'RunPlugin(%s)' % ('%s?url=www&original_title=add&mode=65&name=%s&id=%s&season=%s&episode=%s')%("plugin://%s/"%addon_id,tv_movie,id,season,episode))) 
                    
                    menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32165), 'RunPlugin(%s)' % ('%s?url=www&original_title=remove&mode=65&name=%s&id=%s&season=%s&episode=%s')%("plugin://%s/"%addon_id,tv_movie,id,season,episode))) 
                    
                    type_info='extendedtvinfo'
                    if mode==15:
                        type_info='extendedinfo'
                    menu_items.append(('[I]OpenInfo[/I]','RunScript(script.extendedinfo,info=%s,dbid=,id=%s,name=%s,tvshow=%s,season=%s,episode=%s)'%(type_info,id,que(original_title),que(original_title),season,episode)))
            if Addon.getSetting("clear_Cache")=='true':
                        menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32176), 'RunPlugin(%s)' % ('%s?url=www&mode=35')%("plugin://%s/"%addon_id)))
            all_ur=utf8_urlencode(params)
            u="plugin://%s/"%addon_id+"?&mode="+str(mode)+'&'+all_ur
            
            video_data={}
            video_data['title']=name+added_pre.replace('\n','')
            if watched=='yes':
              video_data['playcount']=1
              video_data['overlay']=7
            
            if year!='':
                video_data['year']=year
            if generes!=' ':
                video_data['genre']=generes
            video_data['rating']=str(rating)
        
            #video_data['poster']=fanart
            video_data['plot']=added_pre+plot.replace("%27","'")
            if trailer!='':
                video_data['trailer']=trailer
            if KODI_VERSION<=18:#kodi18
                liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)
            else:
                liz = xbmcgui.ListItem(offscreen=True)
                liz.setLabel(name)
            '''
            if tv_show=='tv':
                ee=str(episode)
            else:
                ee=str(id)
            if ee in all_w:
            
               liz.setProperty('ResumeTime', all_w[ee]['resume'])
               liz.setProperty('TotalTime', all_w[ee]['totaltime'])
            '''
            if KODI_VERSION>19:
                info_tag = liz.getVideoInfoTag()
                info_tag.setMediaType(meta_get(video_data,'mediatype'))
                info_tag.setTitle(meta_get(video_data,'title'))
                info_tag.setPlot(meta_get(video_data,'plot'))
                try:
                    year_info=int(meta_get(video_data,'year'))
                    if (year_info>0):
                        info_tag.setYear(year_info)
                except:
                    pass
                try:
                    info_tag.setRating(float(meta_get(video_data,'rating')))
                except:
                    pass
                info_tag.setVotes(int(meta_get(video_data,'votes')))
                info_tag.setMpaa(meta_get(video_data,'mpaa'))
                info_tag.setDuration(int(meta_get(video_data,'duration')))
                info_tag.setCountries(meta_get(video_data,'country'))
                
                info_tag.setTrailer(meta_get(video_data,'trailer'))
                info_tag.setPremiered(meta_get(video_data,'premiered'))
                info_tag.setTagLine(meta_get(video_data,'tagline'))
                info_tag.setStudios((meta_get(video_data,'studio') or '',))
                info_tag.setUniqueIDs({'imdb': meta_get(video_data,'imdb'), 'tmdb':meta_get(video_data,'tmdb')})
                info_tag.setGenres(meta_get(video_data,'genre').split(', '))
                info_tag.setWriters(meta_get(video_data,'writer').split(', '))
                info_tag.setDirectors(meta_get(video_data,'director').split(', '))
                info_tag.setCast([xbmc_actor(name=item['name'], role=item['role'], thumbnail=item['thumbnail']) for item in meta_get(video_data,'cast')])
            else:
                liz.setInfo(type="Video", infoLabels=video_data)
            
            liz.setProperty( "Fanart_Image", fanart )
            liz.setProperty("IsPlayable","false")
            liz.addContextMenuItems(menu_items, replaceItems=False)
            art = {}
            art.update({'poster': iconimage,'icon': iconimage,'thumb': iconimage})
            liz.setArt(art)
            if dont_place:
                return u,liz,False
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)
###############################################################################################################        
def utf8_urlencode(params):
    try:
        import urllib as u
        enc=u.urlencode
    except:
        from urllib.parse import urlencode
        enc=urlencode
    # problem: u.urlencode(params.items()) is not unicode-safe. Must encode all params strings as utf8 first.
    # UTF-8 encodes all the keys and values in params dictionary
    for k,v in list(params.items()):
        # TRY urllib.unquote_plus(artist.encode('utf-8')).decode('utf-8')
        if type(v) in (int, float):
            params[k] = v
        else:
            try:
                params[k.encode('utf-8')] = v.encode('utf-8')
            except Exception as e:
                pass
                #log.warning( '**ERROR utf8_urlencode ERROR** %s' % e )
    
    return enc(params).encode().decode('utf-8')
def addDir3(name,url,mode,iconimage,fanart,description,premired=' ',image_master='',all_w_trk='',last_id='',video_info={},data=' ',original_title=' ',id=' ',season=' ',episode=' ',tmdbid=' ',eng_name=' ',show_original_year=' ',rating=0,heb_name=' ',isr=0,generes=' ',trailer=' ',dates=' ',watched='no',fav_status='false',collect_all=False,ep_number='',watched_ep='',remain='',hist='',join_menu=False,menu_leave=False,remove_from_fd_g=False,all_w={},mark_time=False,ct_date='',search_db='',from_seek=False,extra_data={},duration=''):
        if Addon.getSetting("stop_where")=='1':
            return 0
        import logging
        logging.warning('Start dir6')
        name=name.replace("|",' ')
        description=description.replace("|",' ')
        original_title=original_title.replace("|",' ')
        if 'http' not in fanart:
            fanart='https://'+fanart
        if '%' in str(episode):
            episode=' '
        added_pre=''
        if (episode!=' ' and episode!='%20' and episode!=None) :
              tv_movie='tv'
        else:
              tv_movie='movie'
              
        if tv_movie=='tv':
                ee=str(episode)
        else:
            ee=str(id)
        time_to_save_trk=int(Addon.getSetting("time_to_save"))
        if Addon.getSetting("stop_where")=='2':
            return 0
        if all_w_trk!='':
            if float(all_w_trk)>=time_to_save_trk:
                added_pre='  [COLOR yellow][I]'+'√'+'[/I][/COLOR] \n '
            elif float(all_w_trk)>1:# and float(all_w_trk)<time_to_save_trk:
                added_pre=' [COLOR yellow][I]'+str(int(float(all_w_trk)))+'%[/I][/COLOR] \n '
        elif ee in all_w:
              
              if '%' in str(all_w[ee]['resume']):
                all_w_time=all_w[ee]['resume'].replace('%','')
              else:
                all_w_time=int((float(all_w[ee]['resume'])*100)/float(all_w[ee]['totaltime']))
              
              if float(all_w_time)>=time_to_save_trk:
                    added_pre=' [COLOR yellow][I]'+'√'+'[/I][/COLOR] \n '
              elif float(all_w_time)>1:# and float(all_w_time)<time_to_save_trk:
               added_pre=' [COLOR yellow][I]'+str(all_w_time)+'%[/I][/COLOR] \n '
        
        params={}
        params['iconimage']=iconimage
        params['fanart']=fanart.replace('/original//','/original/')
        params['description']=added_pre+description.replace("%27","'")
        params['url']=url
        params['name']=name
        params['image_master']=image_master
        params['heb_name']=heb_name
        params['last_id']=last_id
        params['dates']=dates
        params['data']=data
        params['original_title']=original_title
        params['id']=id
        params['season']=season
        params['episode']=episode
        params['tmdbid']=tmdbid
        params['eng_name']=eng_name
        params['show_original_year']=show_original_year
        params['isr']=isr
        params['fav_status']=fav_status
        params['all_w']=json.dumps(all_w)
        params['search_db']=search_db
        params['from_seek']=from_seek
       
        if Addon.getSetting("stop_where")=='3':
            return 0
        all_ur=utf8_urlencode(params)
        plugin_link=False
        
        u="plugin://%s/"%addon_id+"?mode="+str(mode)+'&'+all_ur
        if Addon.getSetting("stop_where")=='4':
            return 0
        ok=True
        
        show_sources=True
        try:
            a=int(season)
            check=True
        except:
            check=False
        
        menu_items=[]
        if mode==15:
            
            if tv_movie=='movie':
                se='one_click'
                
            else:
                se='one_click_tv'
            if Addon.getSetting(se)=='true':
                
                show_sources=False
            if Addon.getSetting("better_look")=='true':
                show_sources=False
            if Addon.getSetting("cast")=='true':
                menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32248), 'ActivateWindow(10025,"%s?mode=177&url=%s&id=%s&season=%s&episode=%s",return)'  % ( "plugin://%s/"%addon_id ,tv_movie,id,season,episode)))
        if (episode!=' ' and episode!='%20' and episode!=None) :
         
          tv_show='tv'
        else:
            tv_show='movie'
        
        if Addon.getSetting("stop_where")=='5':
            return 0
        menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32166), 'Action(Info)'))
        if Addon.getSetting("play_trailer")=='true':
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32167), 'PlayMedia(%s)' % trailer))
        if Addon.getSetting("settings_content")=='true':
            menu_items.append(('%s'%Addon.getLocalizedString(32168), 'RunPlugin(%s?mode=151&url=www)' % "plugin://%s/"%addon_id ))
        if description=='Tmdb_custom':
            menu_items.append(('Remove', 'RunPlugin(%s?mode=203&url=%s)' % ("plugin://%s/"%addon_id ,que(url))))
        if len(id)>1:
         
            if '/tv' in url or '/shows' in url:
                tv_mov='tv'
            else:
                tv_mov='movie'
            if Addon.getSetting("queue_item")=='true':
                menu_items.append(('%s'%Addon.getLocalizedString(32169), 'Action(Queue)' ))
            if Addon.getSetting("trakt_manager")=='true':
                menu_items.append((Addon.getLocalizedString(32170), 'RunPlugin(%s)' % ('%s?url=%s&mode=150&name=%s&data=%s')%("plugin://%s/"%addon_id,id,original_title,tv_mov) ))
            if Addon.getSetting("trakt_watched")=='true':
                menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32171), 'RunPlugin(%s)' % ('%s?url=www&original_title=add&mode=65&name=%s&id=%s&season=%s&episode=%s')%("plugin://%s/"%addon_id,tv_show,id,season,episode))) 
            if Addon.getSetting("trakt_unwatched")=='true':
                menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32172), 'RunPlugin(%s)' % ('%s?url=www&original_title=remove&mode=65&name=%s&id=%s&season=%s&episode=%s')%("plugin://%s/"%addon_id,tv_show,id,season,episode))) 
            if Addon.getSetting("openinfo")=='true':
                type_info='extendedinfo'
                if mode==16:
                    type_info='extendedtvinfo'
                if mode==19:
                    type_info='seasoninfo'
                if mode==15 and tv_movie=='tv':
                    type_info='extendedepisodeinfo'
                menu_items.append(('[I]OpenInfo[/I]','RunScript(script.extendedinfo,info=%s,dbid=,id=%s,name=%s,tvshow=%s,season=%s,episode=%s)'%(type_info,id,original_title,original_title,season,episode)))
        if mark_time:
            if Addon.getSetting("remove_resume_time")=='true':
                menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32173), 'RunPlugin(%s)' % ('%s?url=www&mode=160&name=%s&id=%s&season=%s&episode=%s&data=%s')%("plugin://%s/"%addon_id,name,id,season,episode,tv_movie))) 
        if mode==15:
            u2="plugin://%s/"%addon_id+"?mode="+str(16)+'&'+all_ur
            if Addon.getSetting("browse_series")=='true':
                menu_items.append((Addon.getLocalizedString(32174), 'Container.update("%s")' % (u2)))
        if mode==15 and hist=='true':
            if Addon.getSetting("remove_resume_point")=='true':
                menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32175), 'RunPlugin(%s)' % ('%s?url=%s&mode=159&name=%s&id=%s&season=%s&episode=%s')%("plugin://%s/"%addon_id,tv_show,name.replace("'",'%27').replace(",",'%28'),id,season,episode))) 
         
        if Addon.getSetting("clear_Cache")=='true':
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32176), 'RunPlugin(%s)' % ('%s?url=www&mode=35')%("plugin://%s/"%addon_id)))
        if Addon.getSetting("set_view_type")=='true' and Addon.getSetting("display_lock")=='true':
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32177), 'RunPlugin(%s)' % ('%s?url=%s&mode=167')%("plugin://%s/"%addon_id,str(pre_mode))))
        
        if Addon.getSetting("stop_where")=='6':
            return 0
        video_data={}
        video_data['title']=name
        if (episode!=' ' and episode!='%20' and episode!=None) :
          video_data['mediatype']='episode'
          video_data['TVshowtitle']=original_title
          video_data['Season']=int(str(season).replace('%20','0'))
          video_data['Episode']=int(str(episode).replace('%20','0'))
          
          if premired!=' ':
            video_data['premiered']=premired
          tv_show='tv'
        else:
           video_data['mediatype']='movie'
           video_data['TVshowtitle']=''
           #video_data['tvshow']=''
           video_data['season']=0
           video_data['episode']=0
           tv_show='movie'
        if  mode==7:
            tv_show='tv'
        video_data['OriginalTitle']=original_title
        if data!=' ':
            video_data['year']=data
        if generes!=' ':
            video_data['genre']=generes
        video_data['rating']=str(rating)
    
        #video_data['poster']=fanart
        if Addon.getSetting("stop_where")=='7':
            return 0
        video_data['plot']=added_pre+description.replace("%27","'")
        video_data['plot']=video_data['plot'].replace("|",' ')
        video_data['Tag']=str(pre_mode)
        if ct_date!='':
            video_data['date']=ct_date
        if trailer!=' ':
            video_data['trailer']=trailer
        
        

        
        
       
        if tv_show=='tv':
            ee=str(episode)
        else:
            ee=str(id)
        if video_info!={}:
            
            video_data=video_info
        if watched=='yes':
          video_data['playcount']=1
          video_data['overlay']=7
        if ee in all_w:
            
            #video_data['playcount']=0
            #video_data['overlay']=0
            
           
            name=name.replace('[COLOR white]','[COLOR lightblue]')
            
            video_data['title']=added_pre.replace('\n','')+name
        if Addon.getSetting("stop_where")=='8':
            return 0
        if KODI_VERSION<=18:#kodi18
            liz=xbmcgui.ListItem(added_pre.replace('\n','')+name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        else:#kodi19
            
            liz = xbmcgui.ListItem(offscreen=True)
            liz.setLabel(added_pre.replace('\n','')+name)
        if ep_number!='':
            
            liz.setProperty('totalepisodes', str(ep_number))
        if watched_ep!='':
             
               liz.setProperty('watchedepisodes', str(watched))

        if ee in all_w:
            if 0:
               liz.setProperty('ResumeTime', all_w[ee]['resume'])
               liz.setProperty('TotalTime', all_w[ee]['totaltime'])
            try:
                if Addon.getSetting("filter_watched")=='true':
                    time_to_filter=float(Addon.getSetting("filter_watched_time"))
                    pre_time=float((float(all_w[ee]['resume'])*100)/float(all_w[ee]['totaltime']))
                    if pre_time>time_to_filter:
                        return u,None,show_sources
            except:
                pass
        
        art = {}
        art.update({'poster': iconimage,'icon': iconimage,'thumb': iconimage})
        liz.setArt(art)
        video_data['title']=video_data['title'].replace("|",' ')
        video_data['plot']=video_data['plot'].replace("|",' ')
        
        video_streaminfo = {'codec': 'h264'}
                
        if len(id)>1:
            
            tt='Video'
        else:
            tt='Files'
        
        video_data['id']=id
        cast=[]
        imdb_id=''
        total_seasons, total_aired_eps ='',''
        if (extra_data!={}):
            meta_get_extra=extra_data[id].get
            total_seasons, total_aired_eps = meta_get_extra('total_seasons'), meta_get_extra('total_aired_eps')
            extra_data[id]['total_seasons']=''
            extra_data[id]['total_aired_eps']=''
            imdb_id=extra_data[id]['imdb']
            cast=extra_data[id]['cast']
            extra_data[id]['cast']=[]
            video_data.update(extra_data[id])
        video_data.pop('imdb', None)
        video_data.pop('id', None)
        video_data.pop('total_aired_eps', None)
        video_data.pop('country_codes', None)
        video_data.pop('total_seasons', None)
        if duration!='':
            video_data['duration']=duration
        if KODI_VERSION>19:
                info_tag = liz.getVideoInfoTag()
                info_tag.setMediaType(meta_get(video_data,'mediatype'))
                info_tag.setTitle(meta_get(video_data,'title'))
                info_tag.setPlot(meta_get(video_data,'plot'))
                try:
                    year_info=int(meta_get(video_data,'year'))
                    if (year_info>0):
                        info_tag.setYear(year_info)
                except:
                    pass
                try:
                    info_tag.setRating(float(meta_get(video_data,'rating')))
                except:
                    pass
                info_tag.setVotes(int(meta_get(video_data,'votes')))
                info_tag.setMpaa(meta_get(video_data,'mpaa'))
                info_tag.setDuration(int(meta_get(video_data,'duration')))
                info_tag.setCountries(meta_get(video_data,'country'))
                
                info_tag.setTrailer(meta_get(video_data,'trailer'))
                info_tag.setPremiered(meta_get(video_data,'premiered'))
                info_tag.setTagLine(meta_get(video_data,'tagline'))
                info_tag.setStudios((meta_get(video_data,'studio') or '',))
                info_tag.setUniqueIDs({'imdb': meta_get(video_data,'imdb'), 'tmdb':meta_get(video_data,'tmdb')})
                info_tag.setGenres(meta_get(video_data,'genre').split(', '))
                info_tag.setWriters(meta_get(video_data,'writer').split(', '))
                info_tag.setDirectors(meta_get(video_data,'director').split(', '))
                info_tag.setCast([xbmc_actor(name=item['name'], role=item['role'], thumbnail=item['thumbnail']) for item in meta_get(video_data,'cast')])
        else:
          
                liz.setInfo( type=tt, infoLabels=video_data)
                liz.setCast(cast)
                liz.setUniqueIDs({'imdb': imdb_id, 'tmdb': str(id)})
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "id", id )
        
        
        if total_aired_eps!='':
            liz.setProperty('totalepisodes', str(total_aired_eps))
        if total_seasons!='':
            liz.setProperty('totalseasons', str(total_seasons))
            
        all_v_data=json.dumps(video_data)
        
        if mode==15:
           
            if Addon.getSetting("s3d_scrape")=='true':
                params['original_title']=original_title+' 3D'
                params['mode']='15'
                all_ur2=utf8_urlencode(params)
                
                menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32178), 'RunPlugin(%s)' % ('%s?%s')%("plugin://%s/"%addon_id,all_ur2))) 
        liz.addContextMenuItems(menu_items, replaceItems=False)
        params={}
        params['video_data']=all_v_data
       
        all_ur=utf8_urlencode(params)
        if not plugin_link:
            
            u=u+'&'+all_ur
        if Addon.getSetting("stop_where")=='9':
            return 0
        art = {}
        art.update({'poster': iconimage,'icon': iconimage,'thumb': iconimage})
        liz.setArt(art)
        #ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        if (Addon.getSetting("one_click")=='true' and mode==15):
            show_sources=False
        return u,liz,show_sources



def addLink( name, url,mode,isFolder, iconimage,fanart,description,place_control=False,data='',from_seek=False,rating='',generes='',no_subs='0',tmdb='0',season='0',episode='0',original_title='',prev_name='',da='',year=0,all_w={},dd='',in_groups=False,video_info={},trailer=''):
          name=name.replace("|",' ')
          description=description.replace("|",' ')
          episode=episode.replace('%20',' ')
          season=season.replace('%20',' ')
          if 'http' not in fanart:
            fanart='https://'+fanart
          if not tmdb:
              tmdb=''
          params={}
          params['name']=name
          params['iconimage']=iconimage
          params['fanart']=fanart.replace('/original//','/original/')
          params['description']=description
          params['url']=url
          params['no_subs']=no_subs
          params['season']=season
          params['episode']=episode
          params['mode']=mode
          params['original_title']=original_title
          params['id']=tmdb
          params['dd']=dd
          params['data']=data
          params['prev_name']=prev_name
          params['nextup']='false'
          params['from_seek']=from_seek
          
          all_ur=utf8_urlencode(params)

          u="plugin://%s/"%addon_id+"?"+'&'+all_ur
          menu_items=[]
          if len(tmdb)>1:
            try:
                a=int(season)
                tv_show='tv'
                tv_mov='tv'
            except:
                tv_show='movie'
                tv_mov='movie'
            
            if Addon.getSetting("queue_item")=='true':
                menu_items.append(('%s'%Addon.getLocalizedString(32169), 'Action(Queue)' ))
            if Addon.getSetting("trakt_manager")=='true':
                menu_items.append((Addon.getLocalizedString(32170), 'RunPlugin(%s)' % ('%s?url=%s&mode=150&name=%s&data=%s')%("plugin://%s/"%addon_id,tmdb,original_title,tv_mov) ))
            if Addon.getSetting("trakt_watched")=='true':
                menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32171), 'RunPlugin(%s)' % ('%s?url=www&original_title=add&mode=65&name=%s&id=%s&season=%s&episode=%s')%("plugin://%s/"%addon_id,tv_show,tmdb,season,episode))) 
            if Addon.getSetting("trakt_unwatched")=='true':
                menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32172), 'RunPlugin(%s)' % ('%s?url=www&original_title=remove&mode=65&name=%s&id=%s&season=%s&episode=%s')%("plugin://%s/"%addon_id,tv_show,tmdb,season,episode))) 
            if Addon.getSetting("openinfo")=='true':
                type_info='extendedinfo'
                if mode==16:
                    type_info='extendedtvinfo'
                if mode==19:
                    type_info='seasoninfo'
                if mode==15 and tv_movie=='tv':
                    type_info='extendedepisodeinfo'
                menu_items.append(('[I]OpenInfo[/I]','RunScript(script.extendedinfo,info=%s,dbid=,id=%s,name=%s,tvshow=%s,season=%s,episode=%s)'%(type_info,tmdb,original_title,original_title,season,episode)))
          video_data={}
          video_data['title']=name
            
            
          if year!='':
                video_data['year']=year
          if generes!='':
                video_data['genre']=generes
          if rating!=0:
            video_data['rating']=str(rating)
        
          #video_data['poster']=fanart
          video_data['plot']=description
          f_text_op=Addon.getSetting("filter_text")
          filer_text=False
          if len(f_text_op)>0:
                filer_text=True
                if ',' in f_text_op:
                    all_f_text=f_text_op.split(',')
                else:
                    all_f_text=[f_text_op]
            
          if filer_text:
            for items_f in all_f_text:
                if items_f.lower() in name.lower():
                    return 0
          if KODI_VERSION<=18:#kodi18
            liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)
          else:
             
             liz = xbmcgui.ListItem(offscreen=True)
             liz.setLabel(name)
     
          if Addon.getSetting("set_view_type")=='true':
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32179), 'RunPlugin(%s)' % ('%s?url=%s&mode=167')%("plugin://%s/"%addon_id,str(pre_mode))))
          if mode==170:
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32180), 'RunPlugin(%s)' % ('%s?name=%s&url=www&id=%s&mode=171')%("plugin://%s/"%addon_id,name,tmdb)))
          liz.addContextMenuItems(menu_items, replaceItems=False)
          if video_info!={}:
              video_data=video_info
          if in_groups:
              ee=str(name).replace("'","%27").encode('base64')
              
             
              if ee in all_w:
                
                video_data['playcount']=0
                video_data['overlay']=0
                video_data['title']='[COLOR lightblue]'+original_title+'[/COLOR]'
                #liz.setProperty('ResumeTime', all_w[ee]['resume'])
                #liz.setProperty('TotalTime', all_w[ee]['totaltime'])
                try:
                    if Addon.getSetting("filter_watched")=='true':
                        time_to_filter=float(Addon.getSetting("filter_watched_time"))
                        pre_time=float((float(all_w[ee]['resume'])*100)/float(all_w[ee]['totaltime']))
                        if pre_time>time_to_filter:
                            return 0
                except:
                    pass
          if trailer!='':
                video_data['trailer']=trailer
          if KODI_VERSION>19:
                info_tag = liz.getVideoInfoTag()
                info_tag.setMediaType(meta_get(video_data,'mediatype'))
                info_tag.setTitle(meta_get(video_data,'title'))
                info_tag.setPlot(meta_get(video_data,'plot'))
                try:
                    year_info=int(meta_get(video_data,'year'))
                    if (year_info>0):
                        info_tag.setYear(year_info)
                except:
                    pass
                try:
                    info_tag.setRating(float(meta_get(video_data,'rating')))
                except:
                    pass
                info_tag.setVotes(int(meta_get(video_data,'votes')))
                info_tag.setMpaa(meta_get(video_data,'mpaa'))
                info_tag.setDuration(int(meta_get(video_data,'duration')))
                info_tag.setCountries(meta_get(video_data,'country'))
                
                info_tag.setTrailer(meta_get(video_data,'trailer'))
                info_tag.setPremiered(meta_get(video_data,'premiered'))
                info_tag.setTagLine(meta_get(video_data,'tagline'))
                info_tag.setStudios((meta_get(video_data,'studio') or '',))
                info_tag.setUniqueIDs({'imdb': meta_get(video_data,'imdb'), 'tmdb':meta_get(video_data,'tmdb')})
                info_tag.setGenres(meta_get(video_data,'genre').split(', '))
                info_tag.setWriters(meta_get(video_data,'writer').split(', '))
                info_tag.setDirectors(meta_get(video_data,'director').split(', '))
                info_tag.setCast([xbmc_actor(name=item['name'], role=item['role'], thumbnail=item['thumbnail']) for item in meta_get(video_data,'cast')])
          else:
            liz.setInfo(type="Video", infoLabels=video_data)
          art = {}
          art.update({'poster': iconimage,'icon': iconimage,'thumb': iconimage})
          liz.setArt(art)
          liz.setProperty("IsPlayable","true")
          liz.setProperty( "Fanart_Image", fanart )
          if place_control:
            return u,liz,False
          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)