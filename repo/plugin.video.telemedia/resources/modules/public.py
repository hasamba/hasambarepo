import sys,urllib,logging,os
from resources.modules import log
import xbmcgui,xbmcplugin,xbmc,xbmcaddon,xbmcvfs
lang=xbmc.getLanguage(0)
import base64
Addon = xbmcaddon.Addon()
import xbmcvfs
from urllib.parse import parse_qsl
xbmc_tranlate_path=xbmcvfs.translatePath

user_dataDir = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
if not xbmcvfs.exists(user_dataDir+'/'):
     os.makedirs(user_dataDir)
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
if KODI_VERSION<=18:
    que=urllib.quote_plus
    url_encode=urllib.urlencode
    unque_n=urllib.unquote
else:
    que=urllib.parse.quote_plus
    url_encode=urllib.parse.urlencode
    unque_n=urllib.parse.unquote
    
def addNolink( name, url,mode,isFolder,fan='DefaultFolder.png', iconimage="DefaultFolder.png",plot=' ',year=' ',generes=' ',rating=' ',trailer=' ',original_title=' ',short=False):
 

            name=name.replace("|",' ')
            plot=plot.replace("|",' ')
            original_title=original_title.replace("|",' ')
            params={}
            params['name']=name
            params['iconimage']=iconimage
            params['fanart']=fan
            params['description']=plot
            params['url']=url
            params['original_title']=original_title
            if KODI_VERSION<19:
                all_ur=utf8_urlencode(params)
                u=sys.argv[0]+"?&mode="+str(mode)+'&'+all_ur
            else:
                u=sys.argv[0]+"?&mode="+str(mode)+'&name='+que(name)+'&iconimage='+iconimage+'&fanart='+fan+'&description='+que(plot)+'&url='+que(url)+'&original_title='+original_title
           
            video_data={}
            video_data['title']=name
            
            
            if year!='':
                video_data['year']=year
            if generes!=' ':
                video_data['genre']=generes
            video_data['rating']=str(rating)
        
    
            video_data['plot']=plot
            if trailer!='':
                video_data['trailer']=trailer
            
            liz = xbmcgui.ListItem( name)

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
                
                
            else:
                liz.setInfo( type="Video", infoLabels=video_data)
            liz.setProperty( "Fanart_Image", fan )
            liz.setProperty("IsPlayable","false")
            art = {}
            art.update({'poster': iconimage})
            liz.setArt(art)
            if (short):
                return u,liz
            else:
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)
###############################################################################################################        
def utf8_urlencode(params):
    import urllib as u
    # problem: u.urlencode(params.items()) is not unicode-safe. Must encode all params strings as utf8 first.
    # UTF-8 encodes all the keys and values in params dictionary
    for k,v in params.items():
        # TRY urllib.unquote_plus(artist.encode('utf-8')).decode('utf-8')
        if type(v) in (int, long, float):
            params[k] = v
        else:
            try:
                params[k.encode('utf-8')] = v.encode('utf-8')
            except Exception as e:
                log.warning( '**ERROR utf8_urlencode ERROR** %s' % e )
    
    return u.urlencode(params.items()).decode('utf-8')
def meta_get(video_data,item):
    if item=='year' or item=='rating' or item=='votes' or item=='duration':
        return video_data.get(item,'0')
    if item=='country':
        return video_data.get(item,[])
    return video_data.get(item,' ')
def addDir3(name,url,mode,iconimage,fanart,description,image_master='',last_id='',video_info={},data=' ',original_title=' ',id=' ',season=' ',episode=' ',tmdbid=' ',eng_name=' ',show_original_year=' ',rating=0,heb_name=' ',isr=0,generes=' ',trailer=' ',dates=' ',watched='no',fav_status='false',collect_all=False,ep_number='',watched_ep='',remain='',groups_id='0',hist='',join_menu=False,menu_leave=False,remove_from_fd_g=False,all_w={},next_page='0'):
        
        name=name.replace("|",' ')
        description=description.replace("|",' ')
        original_title=original_title.replace("|",' ')

        params={}
        params['iconimage']=iconimage
        params['fanart']=fanart
        params['description']=description
        params['next_page']=next_page
        params['url']=url
        if KODI_VERSION<19:
            all_ur=utf8_urlencode(params)
            u=sys.argv[0]+"?mode="+str(mode)+"&name="+(name)+"&image_master="+(image_master)+"&heb_name="+(heb_name)+"&last_id="+(last_id)+"&dates="+(dates)+"&data="+str(data)+"&original_title="+(original_title)+"&id="+(id)+"&season="+str(season)+"&episode="+str(episode)+"&tmdbid="+str(tmdbid)+"&eng_name="+(eng_name)+"&show_original_year="+(show_original_year)+"&isr="+str(isr)+'&'+all_ur+"&fav_status="+fav_status+"&groups_id="+groups_id
        else:
            u=sys.argv[0]+"?mode="+str(mode)+"&iconimage="+iconimage+"&fanart="+fanart+"&description="+ que(description)+"&url="+ que(url)+"&name="+que(name)+"&image_master="+(image_master)+"&heb_name="+(heb_name)+"&last_id="+(last_id)+"&dates="+(dates)+"&data="+str(data)+"&original_title="+(original_title)+"&id="+(id)+"&season="+str(season)+"&episode="+str(episode)+"&tmdbid="+str(tmdbid)+"&eng_name="+(eng_name)+"&show_original_year="+(show_original_year)+"&isr="+str(isr)+"&fav_status="+fav_status+"&groups_id="+groups_id+"&next_page="+next_page
        ok=True
        show_sources=True
        if mode==20 or mode==15:
            if Addon.getSetting("one_click")=='true':
                if Addon.getSetting("sh_one_click")=='false':
                   show_sources=False
        menu_items=[]
        menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32063), 'Action(Info)'))
        if remove_from_fd_g:
            #Remove from FD groups
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32082), 'RunPlugin(%s)' % ('%s?url=%s&mode=35&name=%s')%(sys.argv[0],url,que(name))))
        if join_menu:
            #join Channel
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32062), 'RunPlugin(%s)' % ('%s?url=%s&mode=22&name=join')%(sys.argv[0],url)))
        if menu_leave:
            #Leave Channel
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32031), 'RunPlugin(%s)' % ('%s?url=%s&mode=23&name=%s')%(sys.argv[0],url,que(name))))
        
        if mode==16:
            #Remove
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32056), 'RunPlugin(%s)' % ('%s?url=%s&mode=29&name=%s')%(sys.argv[0],url,que(name))))
        if mode==16:
            #add to my TV
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32069), 'RunPlugin(%s)' % ('%s?url=%s&mode=27&name=%s&data=%s&iconimage=%s&fanart=%s&description=%s')%(sys.argv[0],id,que(name),data,iconimage,fanart,que(description))))
        if mode==2:
            #add to my TV
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32080), 'RunPlugin(%s)' % ('%s?url=%s&mode=34&name=%s&data=%s&iconimage=%s&fanart=%s&description=%s')%(sys.argv[0],url,que(name),data,iconimage,fanart,que(description))))
        video_data={}
        video_data['title']=name
        if (episode!=' ' and episode!='%20' and episode!=None) :
          video_data['mediatype']='tvshow'
          video_data['TVshowtitle']=original_title
          video_data['Season']=int(str(season).replace('%20','0'))
          video_data['Episode']=int(str(episode).replace('%20','0'))
          tv_show='tv'
        else:
           video_data['mediatype']='movies'
           video_data['TVshowtitle']=''
          
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
    
      
        video_data['plot']=description
        if trailer!=' ':
            video_data['trailer']=trailer
      

        
        '''
        str_e1=list(u.encode('utf8'))
        for i in range(0,len(str_e1)):
           str_e1[i]=str(ord(str_e1[i]))
        str_e='$$'.join(str_e1)
        '''
        if tv_show=='tv':
            ee=str(episode)
        else:
            ee=str(id)
        if video_info!={}:
            
            video_data=video_info
        if ee in all_w:
            
            video_data['playcount']=0
            video_data['overlay']=0
            
           
            name=name.replace('[COLOR white]','[COLOR lightblue]')
            video_data['title']=name
            
        liz=xbmcgui.ListItem(name)
        liz.addContextMenuItems(menu_items, replaceItems=False)
        

        if ee in all_w:
            
            try:
                if Addon.getSetting("filter_watched")=='true':
                    time_to_filter=float(Addon.getSetting("filter_watched_time"))
                    pre_time=float((float(all_w[ee]['resume'])*100)/float(all_w[ee]['totaltime']))
                    if pre_time>time_to_filter:
                        return u,None,show_sources
            except:
                pass
        
        art = {}
        art.update({'poster': iconimage})
        liz.setArt(art)
        video_data['title']=video_data['title'].replace("|",' ')
        video_data['plot']=video_data['plot'].replace("|",' ')
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
            info_tag.setRating(float(meta_get(video_data,'rating')))
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
            if ee in all_w:
                info_tag.setResumePoint(float(all_w[ee]['resume']),float(all_w[ee]['totaltime']))
                
            
        else:
            liz.setInfo( type="Video", infoLabels=video_data)
            if ee in all_w:
                liz.setProperty('ResumeTime', all_w[ee]['resume'])
                liz.setProperty('TotalTime', all_w[ee]['totaltime'])
            
        liz.setProperty( "Fanart_Image", fanart )
        art = {}
        art.update({'poster': iconimage})
        liz.setArt(art)
        #ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
        return u,liz,show_sources



def addLink( name, url,mode,isFolder, iconimage,fanart,description,data='',rating='',generes='',no_subs='0',tmdb='0',season='0',episode='0',original_title='',da='',year=0,all_w={},in_groups=False,short=False,watched=False):
          name=name.replace("|",' ')
          description=description.replace("|",' ')
          original_title=original_title.replace("|",' ')
          params={}
          params['name']=name
          params['iconimage']=iconimage
          params['fanart']=fanart
          params['description']=description
          params['url']=url
          if KODI_VERSION<19:
            all_ur=utf8_urlencode(params)
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&no_subs="+str(no_subs)+"&season="+str(season)+"&episode="+str(episode)+"&mode="+str(mode)+"&original_title="+str(original_title)+"&id="+str(tmdb)+"&data="+str(data)+'&'+all_ur
          else:
            u=sys.argv[0]+"?url="+ que(url)+"&name="+que(name)+"&iconimage="+iconimage+"&fanart="+fanart+"&description="+que(description)+"&url="+que(url)+"&no_subs="+str(no_subs)+"&season="+str(season)+"&episode="+str(episode)+"&mode="+str(mode)+"&original_title="+str(original_title)+"&id="+str(tmdb)+"&data="+str(data)
 

          video_data={}
          video_data['title']=name
            
            
          if year!='':
                video_data['year']=year
          if generes!='':
                video_data['genre']=generes
          if rating!=0:
            video_data['rating']=str(rating)
        
       
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
          #u=sys.argv[0]+"?url="+ que(url)+"&mode="+str(mode)+"&name="+ que(name)
          liz = xbmcgui.ListItem( name)
          if in_groups:
              #ee=base64.b64encode(str(name).replace("'","%27"))
              
              ee=str(name)
              if ee in all_w:
                
                video_data['playcount']=0
                video_data['overlay']=0
                video_data['title']='[COLOR lightblue]'+name+'[/COLOR]'
                liz.setProperty('ResumeTime', all_w[ee]['resume'])
                liz.setProperty('TotalTime', all_w[ee]['totaltime'])
                try:
                    if Addon.getSetting("filter_watched")=='true':
                        time_to_filter=float(Addon.getSetting("filter_watched_time"))
                        pre_time=float((float(all_w[ee]['resume'])*100)/float(all_w[ee]['totaltime']))
                        if pre_time>time_to_filter:
                            return 0
                except:
                    pass
          if watched:
                
                video_data['title']="[COLOR blue]"+name+"[/COLOR]"
          
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
          else:
                liz.setInfo( type="Video", infoLabels=video_data)
          
          art = {}
          art.update({'poster': iconimage})
          liz.setArt(art)
          liz.setProperty("IsPlayable","true")
          liz.setProperty( "Fanart_Image", fanart )
          if (short):
                return u,liz
          else:
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)