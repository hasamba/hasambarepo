import xbmcgui,xbmcaddon,xbmc
import re
from  resources.modules.client import get_html
from resources.modules import cache
from resources.modules import log
from resources.default import get_extra_art
from resources.modules.general import tmdb_key
lang=xbmc.getLanguage(0)
Addon = xbmcaddon.Addon()
import threading

ACTION_PREVIOUS_MENU 			=  10	## ESC action
ACTION_NAV_BACK 				=  92	## Backspace action
ACTION_MOVE_LEFT				=   1	## Left arrow key
ACTION_MOVE_RIGHT 				=   2	## Right arrow key
ACTION_MOVE_UP 					=   3	## Up arrow key
ACTION_MOVE_DOWN 				=   4	## Down arrow key
ACTION_MOUSE_WHEEL_UP 			= 104	## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN			= 105	## Mouse wheel down
ACTION_MOVE_MOUSE 				= 107	## Down arrow key
ACTION_SELECT_ITEM				=   7	## Number Pad Enter
ACTION_BACKSPACE				= 110	## ?
ACTION_MOUSE_LEFT_CLICK 		= 100
ACTION_MOUSE_LONG_CLICK 		= 108

ACTION_PLAYER_STOP = 13
ACTION_BACK          = 92
ACTION_NAV_BACK =  92## Backspace action
ACTION_PARENT_DIR    = 9
ACTION_PREVIOUS_MENU = 10
ACTION_CONTEXT_MENU  = 117
ACTION_C_KEY         = 122

ACTION_LEFT  = 1
ACTION_RIGHT = 2
ACTION_UP    = 3
ACTION_DOWN  = 4
domain_s='https://'
COLOR1         = 'gold'
COLOR2         = 'white'
# Primary menu items   / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'

class Thread (threading.Thread):
       def __init__(self, target, *args):
        super().__init__(target=target, args=args)
        
       def run(self, *args):
          try:
            self._target(*self._args)

          except Exception as e:
              log.error(e)
          return 0
class ContextMenu_new4(xbmcgui.WindowXMLDialog):
    
    def __new__(cls, addonID, menu,icon,fan,txt,results,po_watching,l_full_stats,tv_movie,id,tvdb_id,season,episode,show_original_year,original_title,heb_name):
        FILENAME='contextMenu_new4.xml'
        
        
        return super(ContextMenu_new4, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
    def clean_title(self,title, broken=None):
        title = title.lower()
        # title = tools.deaccentString(title)
        #title = tools.strip_non_ascii_and_unprintable(title)

        if broken == 1:
            apostrophe_replacement = ''
        elif broken == 2:
            apostrophe_replacement = ' s'
        else:
            apostrophe_replacement = 's'
        title = title.replace("\\'s", apostrophe_replacement)
        title = title.replace("'s", apostrophe_replacement)
        title = title.replace("&#039;s", apostrophe_replacement)
        title = title.replace(" 039 s", apostrophe_replacement)

        title = re.sub(r'\:|\\|\/|\,|\!|\?|\(|\)|\'|\"|\\|\[|\]|\-|\_|\.', ' ', title)
        title = re.sub(r'\s+', ' ', title)
        title = re.sub(r'\&', 'and', title)

        return title.strip()
    def  getInfo(self,release_title):
        info = {}
        release_title = self.clean_title(release_title)
        info['encoding']=[]
        info['audio']=[]
        info['channels']=[]
        info['source']=[]
        info['language']=[]
            
        #info.video
        '''
        if any(i in release_title for i in ['x264', 'x 264', 'h264', 'h 264', 'avc']):
            info['encoding'].append('AVC')
        if any(i in release_title for i in ['x265', 'x 265', 'h265', 'h 265', 'hevc']):
            info['encoding'].append('HEVC')
        if any(i in release_title for i in ['xvid']):
            info['encoding'].append('XVID')
        if any(i in release_title for i in ['divx']):
            info['encoding'].append('DIVX')
        if any(i in release_title for i in ['mp4']):
            info['encoding'].append('MP4')
        if any(i in release_title for i in ['wmv']):
            info['encoding'].append('WMV')
        if any(i in release_title for i in ['mpeg']):
            info['encoding'].append('MPEG')
        if any(i in release_title for i in ['remux', 'bdremux']):
            info['encoding'].append('REMUX')
        '''
        if any(i in release_title for i in [' hdr ', 'hdr10', 'hdr 10']):
            info['encoding'].append('[COLOR yellow]HDR[/COLOR]')
        if any(i in release_title for i in [' sdr ']):
            info['encoding'].append('SDR')
        
        #info.audio
        '''
        if any(i in release_title for i in ['aac']):
            info['audio'].append('AAC')
        
        if any(i in release_title for i in ['hd ma' , 'hdma']):
            info['audio'].append('HD-MA')
        
        if any(i in release_title for i in ['truehd', 'true hd']):
            info['audio'].append('TRUEHD')
        if any(i in release_title for i in ['ddp', 'dd+', 'eac3']):
            info['audio'].append('DD+')
        if any(i in release_title for i in [' dd ', 'dd2', 'dd5', 'dd7', ' ac3']):
            info['audio'].append('DD')
        if any(i in release_title for i in ['mp3']):
            info['audio'].append('MP3')
        if any(i in release_title for i in [' wma']):
            info['audio'].append('WMA')
        '''
        #info.channels
        if any(i in release_title for i in ['atmos']):
            info['audio'].append('ATMOS')
        if any(i in release_title for i in ['dts']):
            info['audio'].append('DTS')
        if any(i in release_title for i in ['2 0 ', '2 0ch', '2ch']):
            info['channels'].append('2.0')
        if any(i in release_title for i in ['5 1 ', '5 1ch', '6ch']):
            info['channels'].append('5.1')
        if any(i in release_title for i in ['7 1 ', '7 1ch', '8ch']):
            info['channels'].append('7.1')
        
        #info.source 
        # no point at all with WEBRip vs WEB-DL cuz it's always labeled wrong with TV Shows 
        # WEB = WEB-DL in terms of size and quality.
        '''
        if any(i in release_title for i in ['bluray' , 'blu ray' , 'bdrip', 'bd rip', 'brrip', 'br rip']):
            info['source'].append('BLURAY')
        if any(i in release_title for i in [' web ' , 'webrip' , 'webdl', 'web rip', 'web dl']):
            info['source'].append('WEB')
        if any(i in release_title for i in ['hdrip', 'hd rip']):
            info['source'].append('HDRIP')
        if any(i in release_title for i in ['dvdrip', 'dvd rip']):
            info['source'].append('DVDRIP')
        if any(i in release_title for i in ['hdtv']):
            info['source'].append('HDTV')
        if any(i in release_title for i in ['pdtv']):
            info['source'].append('PDTV')
        if any(i in release_title for i in [' cam ', 'camrip', 'hdcam', 'hd cam', ' ts ', 'hd ts', 'hdts', 'telesync', ' tc ', 'hd tc', 'hdtc', 'telecine', 'xbet']):
            info['source'].append('CAM')
        if any(i in release_title for i in ['dvdscr', ' scr ', 'screener']):
            info['source'].append('SCR')
        if any(i in release_title for i in ['korsub', ' kor ', ' hc']):
            info['source'].append('HC')
        if any(i in release_title for i in ['blurred']):
            info['source'].append('BLUR')
        if any(i in release_title for i in [' 3d']):
            info['source'].append('3D')
        '''
        all_lang=['en','eng','english','rus','russian','fr','french','TrueFrench','ita','italian','italiano','castellano','spanish','swedish','dk','danish','german','nordic','exyu','chs','hindi','polish','mandarin','kor','korean','koraen','multi']
        all_lang_des=['English','English','English','Russian','Russian','French','French','French','Italiano','Italiano','Italiano','Castellano','Spanish','Swedish','Danish','Danish','German','Nordic','ExYu','Chinese','Hindi','Polish','Mandarin','Korean','Korean','Korean','Multi']
        index=0

        for itt in all_lang:
            if ' '+itt+' ' in release_title.lower():
                if all_lang_des[index] not in info['language']:
                    info['language'].append(all_lang_des[index])
            index+=1
            
        fixed_info={}
        for key in info:
            if len(info[key])>0:
                fixed_info[key]=info[key]
                
        return fixed_info
    def __init__(self, addonID, menu,icon,fan,txt,results,po_watching,l_full_stats,tv_movie,id,tvdb_id,season,episode,show_original_year,original_title,heb_name):
        
        super(ContextMenu_new4, self).__init__()
        self.clicked=False
        self.heb_name=heb_name
        self.id=id
        self.menu=menu
        self.show_original_year=show_original_year
        self.original_title=original_title
        self.episode=episode
        self.season=season
        self.results=results
        self.selected_index_in=0
        if len(episode)==1:
          self.episode_n="0"+episode
        else:
           self.episode_n=episode
        if len(season)==1:
          self.season_n="0"+season
        else:
          self.season_n=season
      
        
        self.tv_movie=tv_movie
        self.tvdb_id=tvdb_id
        self.done_extra_fanart=False
        
        thread=[]
        thread.append(Thread(self.add_extra_art))
        thread[len(thread)-1].setName('fill_table')
        
        thread[0].start()
        
    def add_extra_art(self):
        
        log.warning('Start Extra')
        
        all_logo,all_n_fan,all_banner,all_clear_art,r_logo,r_art=get_extra_art(self.id,self.tv_movie,self.tvdb_id)
        log.warning(r_logo)
        self.getControl(3).setImage(r_logo)
        self.getControl(4).setImage(r_art)
    def cached_poster(self,idd):
        if self.tv_movie=='tv':
            x=f'http://api.themoviedb.org/3/tv/%s?api_key={tmdb_key}&language=%s&page=1'%(idd,lang)
        else:
            x=f'http://api.themoviedb.org/3/movie/%s?api_key={tmdb_key}&language=%s&page=1'%(idd,lang)
     
        
        
        html=get_html(x).json()
        return html
    def fill_table(self):
        self.list = self.getControl(2)
        
        html=cache.get(self.cached_poster, 999,self.id,table='pages') 
       
       
        if 'poster_path' in html:
            if html['poster_path']!=None:
                self.icon='https://image.tmdb.org/t/p/original/'+html['poster_path']
            else:
                self.icon=' '
            self.getControl(1).setImage(self.icon)
        self.getControl(5).setLabel(self.results)
        count=0
        all_liz_items=[]
        xbmc_list=xbmcgui.ListItem
        for item in self.menu:
                
                if self.clicked:
                    break
                self.getControl(5).setLabel("Please wait %s/%s"%(str(count),len(self.menu)))
                count+=1
                info=self.getInfo(item[4])
                #info={}
                add_d=[]
                
                
                counter_page=0
                nxt=0
                
               
                #self.getControl(202).setLabel(str(((count*100)/len(self.menu))) + Addon.getLocalizedString(32010))
                
               
                '''
                info=(PTN.parse(item[0]))
                if 'excess' in info:
                    if len(info['excess'])>0:
                        item[0]='.'.join(info['excess'])
                '''
                golden=False
                #if 'Cached ' in item[0]:
                #    golden=True
                #item[0]=item[0].replace('Cached ','')
                item[4] = (item[4][:80] + '..') if len(item[4]) > 110 else item[4]
               
                title ='[COLOR deepskyblue][B]'+item[0] +'[/B][/COLOR]'
                if len(item[1].strip())<2:
                    item[1]=''
                if len(item[2].strip())<2:
                    item[2]=''
                if len(item[3].strip())<2:
                    item[3]=''
                if len(item[4])<2:
                    item[4]=''
                try:
                    if len(item[5])<2:
                        item[5]=''
                except:
                    item[5]=''
                server=item[1]
                pre_n='[COLOR lime]'+item[2]+'[/COLOR]'
                q=item[3]
                
                if item[5]=='0.0GB':
                    size=''
                else:
                    size='[COLOR yellow]'+item[5]+'[/COLOR]'
                link=item[6]
                if Addon.getSetting("add_colors")=='true':
                    original_title_wd=self.original_title.replace(' ','.')
                    if 'stargirl' in original_title_wd.lower():
                        original_title_wd=original_title_wd.replace("DC's.",'')
                    original_title_alt=self.original_title.replace('&','and').replace("'","").replace('%3A',':').replace('%27','').replace('%20',' ')
                    heb_name_wd=self.heb_name.replace(' ','.')
                    
                    item[4]=item[4].replace('-','.').replace('_','.').replace('.',' ').replace('%27','').replace('%20',' ').replace("'","")
                  
                    item[4]=item[4].replace(original_title_alt,'[COLOR yellow]'+original_title_alt+'[/COLOR]')
                    
                    item[4]=item[4].replace('  ',' ').replace(self.original_title.lower()+' ',self.original_title+' ')
                    item[4]=item[4].replace('S%sE%s'%(self.season_n,self.episode_n),'[COLOR lime]S%sE%s[/COLOR]'%(self.season_n,self.episode_n))
                    item[4]=item[4].replace(self.original_title+' ','[COLOR yellow]'+self.original_title+'[/COLOR]'+' ').replace(original_title_wd+' ','[COLOR yellow]'+self.original_title+'[/COLOR]'+' ')
                    
                    item[4]=item[4].replace(self.show_original_year,'[COLOR plum]'+self.show_original_year+'[/COLOR]')
                    #heb
                    if (len(self.heb_name)>2):
                        item[4]=item[4].replace(self.heb_name,'[COLOR yellow]'+self.heb_name+'[/COLOR]').replace(heb_name_wd,'[COLOR yellow]'+self.heb_name+'[/COLOR]')
                    item[4]=item[4].replace('עונה %s פרק %s'%(self.season,self.episode),'[COLOR lime]עונה %s פרק %s[/COLOR]'%(self.season,self.episode))
                    item[4]=item[4].replace('ע%s פ%s'%(self.season,self.episode),'[COLOR lime]ע%s פ%s[/COLOR]'%(self.season,self.episode))
                    item[4]=item[4].replace('ע%sפ%s'%(self.season,self.episode),'[COLOR lime]ע%sפ%s[/COLOR]'%(self.season,self.episode))
                added_h=''
                
                if 'https://' in item[6]:
                    
                    r=item[6].split('//')[1].split('/')[0]
                    #r=re.compile('//(.+?)/').findall(item[6])
                    if len(r)>0:
                        added_h='['+ r[0].replace('.com','').replace('www.','').capitalize()+'] '
                    
                    
                
                if q=='2160':
                    q='4k'
                if q.lower()=='hd':
                    q='unk'
                all_info=[]
                if len(q)>0:
                    all_info=['[COLOR %s][B]'%'yellow'+q+'[/B][/COLOR]']
                
                for key in info:
                    if type(info[key])==list:
                        
                        try:
                            info_key=','.join(info[key])
                        except:
                            info_key=str(info[key])
                    else:
                        info_key=str(info[key])
                    if key=='language':
                        color='pink'
                    else:
                        color='khaki'
                    all_info.append('[COLOR %s]'%color+info_key+'[/COLOR]')
                supplay='[COLOR pink][B]'+size+'[/B][/COLOR] , '+','.join(all_info)
                
                
                
                liz   = xbmc_list()
                if 'אוסף' not in server:
                    ncolor='lime'
                else:
                    ncolor='pink'
                
                liz.setProperties({'title':supplay,
                                    'pre':pre_n,
                                    'image_collection':item[7],
                                    'Quality': q,
                                    'supply':'[COLOR %s]['%ncolor+server.capitalize() +'][/COLOR] '+added_h +pre_n+item[4] ,
                                    'size': size})
                                    
                #liz.setProperty('title','[COLOR lime]['+server.capitalize() +'][/COLOR] '+added_h +pre_n+item[4].encode('ascii', errors='ignore').decode('ascii', errors='ignore'))
                #liz.setProperty('server', '')#server
                #liz.setProperty('pre',pre_n)
                #if 'https' in item[7]:
                #    liz.setProperty('image_collection',item[7])
                #    #liz.setProperty('collection','yes')
                #liz.setProperty('Quality', q)
                #liz.setProperty('supply', supplay)
                #liz.setProperty('size', size)
              
                
                #liz.setProperty('server_v','100')
           
                
                #all_liz_items.append(liz)
                
                pre_pos=self.list.getSelectedPosition()
                self.list.addItem(liz)
                self.list.selectItem(pre_pos)
                self.setFocus(self.list)
                
        self.getControl(5).setLabel(self.results)
        log.warning(' Done Loading')
        
        #self.list.addItems(all_liz_items)

        self.setFocus(self.list)
    def onInit(self):
        
        thread=[]
        thread.append(Thread(self.fill_table))
        thread[len(thread)-1].setName('fill_table')
        log.warning('trd s')
        thread[0].start()
        
        
    def onAction(self, action):  
        global done1_1,selected_index
        actionId = action.getId()
        #log.warning('actionId:'+str(actionId))
        self.tick=60
        #log.warning('ACtion:'+ str(actionId))
        
            
        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            log.warning('Close:5')
            self.params = 888
            selected_index=-1
            self.selected_index_in=-1
            self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK,ACTION_NAV_BACK]:
            self.params = 888
            selected_index=-1
            self.selected_index_in=-1
            self.close()

    
    def onClick(self, controlId):
        global playing_text,done1_1,selected_index
        self.tick=60
        
        if controlId != 3001:
            self.clicked=True
            '''
            self.getControl(3000).setVisible(False)
            self.getControl(102).setVisible(False)
            self.getControl(505).setVisible(False)
            self.getControl(909).setPosition(1310, 40)
            self.getControl(2).setPosition(1310, 100)
            self.getControl(self.imagecontrol).setVisible(False)
            self.getControl(303).setVisible(False)
            self.story_gone=1
            '''
            index = self.list.getSelectedPosition()        
            
            try:    
                self.params = index
                log.warning('Clicked:'+str(controlId)+':'+str(index))
            except:
                self.params = None
            #playing_text=''
            xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
            selected_index=self.params
            self.selected_index_in=self.params
            self.close()
            #return self.params
        else:
            log.warning('Close:7')
            selected_index=-1
            self.selected_index_in=-1
            self.close()
        
    def close_now(self):
        global done1_1
        log.warning('Close:8')
        self.params = 888
        self.done=1
        xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
        xbmc.sleep(1000)
        log.warning('Close now CLosing')
        done1_1=3
        self.close()
    def onFocus(self, controlId):
        pass