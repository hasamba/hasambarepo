
from  resources.modules.client import get_html
from resources.modules import cache
from resources.modules import log
import pkgutil,os,xbmcgui,json
import xbmcvfs,xbmcaddon,base64
import time,xbmc,random,sys,re
from resources.modules.general import fix_q
from resources.skin_file import ContextMenu_new4
from resources.default import ContextMenu_new2,play_link
Addon = xbmcaddon.Addon()
xbmc_tranlate_path=xbmcvfs.translatePath
addonPath = xbmc_tranlate_path(Addon.getAddonInfo("path"))
addon_id=Addon.getAddonInfo("id")
import concurrent.futures,hashlib
from concurrent.futures import wait
from resources.modules import real_debrid
rd = real_debrid.RealDebrid()
from  resources.modules.public import user_dataDir
user_dataDir = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
window=xbmcgui.Window(10000)
class get_sources:
    def __init__(self,name,iconimage,fanart,description,show_original_year,original_title,id,season,episode,heb_name,selected_scrapers='All'):
        self.Addon = xbmcaddon.Addon()
        self.name=name
        self.iconimage=iconimage
        self.fanart=fanart
        self.description=description
        self.show_original_year=show_original_year
        self.heb_name=heb_name
        self.original_title=original_title
        self.season=season
        self.episode=episode
        self.selected_scrapers=selected_scrapers
        self.id=id
        self.all_sources=[]
        self.all_ok={}
        self.all_mag={}
        self.all_mag[0]=[]
        self.hash_index={}
        self.all_names={}
        self.all_q={}
        self.page_index=0
        self.all_lk_in=[]
        self.all_rej=[]
        self.all_hased=[]
        self.complete_hash=[]
        self.all_ok=[]
        self.elapsed_time=0
        self.start_time=time.time()
        self.all_data=[]
        self.all_rejected=[]
        self.all_filted=[]
        self.all_filted_rejected=[]
        self.dd=[]
        self.all_finish_data=''
        self.dp = ''
        
      
        
        
        try:
            s=int(season)
            tv_movie='tv'
            
        except:
            tv_movie='movie'
        if len(season)==1:
          self.season_n="0"+season
        else:
          self.season_n=season
        if len(episode)==1:
          self.episode_n="0"+episode
        else:
          self.episode_n=episode
        self.tv_movie=tv_movie
        self.collect_files()
    def get_modules(self,loader, items, is_pkg):
        
            
            if is_pkg: 
                return 0
            
            added=''
            if self.tv_movie=='tv':
                added='_tv'
            try:
                module = loader.find_module(items).load_module(items)
            except Exception as e:
               log.warning('Fault module:'+items)
               log.warning(e)
               
               return 0
            test_scr=self.Addon.getSetting(items+added)
            
            if self.selected_scrapers!='All' and len(self.selected_scrapers)>0:
            
                if items==self.selected_scrapers:
                
                    test_scr='true'
                else:
                    test_scr='false'
                
                if test_scr=='false':
                  return 0
            
            if  items and 'init' not in items and test_scr=='true':
                impmodule = __import__(items)
                
                
                
                impmodule.stop_all=0
                impmodule.global_var=[]
                self.all_sources.append((items,impmodule))
        
    def trd_get_modules(self,source_dir):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                i=0
                for loader, items, is_pkg in pkgutil.walk_packages([source_dir]):
                    
                    futures.append(executor.submit(self.get_modules, loader, items, is_pkg))
                    i+=1
                wait(futures)
            return self.all_sources
    def get_links(self):
        executor= concurrent.futures.ThreadPoolExecutor(max_workers=100)
        futures = []
        max_time=int(self.Addon.getSetting("time_s"))
        
        for items,impmodule in self.all_sources:
            futures.append((executor.submit(impmodule.get_links, self.tv_movie,self.original_title,self.season_n,self.episode_n,self.season,self.episode,self.show_original_year,self.id),items))
        if len(futures)>0:
            exit_now=False
            while(1):
                still_alive=False
                num_live=0
                string_dp2=''
                living=[]
                for td,nm in futures:
                    
                    if td.running():
                        
                        if string_dp2=='':
                            string_dp2=nm
                        else:
                            
                            string_dp2=string_dp2+','+nm
                        still_alive=True
                        num_live+=1
                        living.append(nm)
              
                if num_live>10:
            
                    string_dp2=Addon.getLocalizedString(32075)+str(num_live)+' - '+random.choice (living)
                if not still_alive:
                    exit_now=True
                    
                self.f_result={}
                
                string_dp=''
                
                still_alive=0
                count_2160=0
                count_1080=0
                count_720=0
                count_480=0
                count_rest=0
                count_alive=0
                count_found=0;
                all_alive={}
                if self.dp.iscanceled():
                    exit_now=True
                for name1,items in self.all_sources:
                    self.f_result[name1]={}
                    self.f_result[name1]['links']=items.global_var
                for data in self.f_result:
                    
                    if len (self.f_result[data]['links'])>0:
                           count_found+=1
                           
                    if 'links' in self.f_result[data] and len (self.f_result[data]['links'])>0:
                         
                        for links_in in self.f_result[data]['links']:
                            
                             
                             
                            name1,links,server,res=links_in
                            if links==None:
                                continue
                            new_res=0
                            if '2160' in res:
                               count_2160+=1
                               new_res=2160
                            if '1080' in res:
                               count_1080+=1
                               new_res=1080
                            elif '720' in res:
                               count_720+=1
                               new_res=720
                            elif '480' in res:
                               count_480+=1
                               new_res=480
                            else:
                               count_rest+=1
                            try:
                                res_c=int(res)
                            except:
                                res_c=480
                total=count_1080+count_720+count_480+count_rest
                string_dp="4K: [COLOR yellow]%s[/COLOR] 1080: [COLOR khaki]%s[/COLOR] 720: [COLOR gold]%s[/COLOR] 480: [COLOR silver]%s[/COLOR] %s: [COLOR burlywood]%s[/COLOR]  T: [COLOR darksalmon]%s[/COLOR] "%(count_2160,count_1080,count_720,count_480,Addon.getLocalizedString(32078),count_rest,total)
                self.elapsed_time = time.time() - self.start_time
                if self.elapsed_time>max_time:
                    exit_now=True
                if exit_now:
                    for td,nm in futures:
                        td.cancel()
                    break
                self.dp.update(int(((num_live* 100.0)/(len(futures))) ), Addon.getLocalizedString(32072)+ time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time))+'\n'+string_dp+'\n'+string_dp2)
                xbmc.sleep(100)
        self.f_result={}
        for name1,items in self.all_sources:
            self.f_result[name1]={}
            self.f_result[name1]['links']=items.global_var
                    
         
    def trd_anaylze(self,name_f):
        
        for name,link,server,quality in self.f_result[name_f]['links']:
            self.elapsed_time = time.time() - self.start_time
            self.dp.update(0, 'Analyze_data'+ time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time))+name)
            if link==None:
                continue
            if 'magnet' in link:
                self.statistics['magnet']+=1
                try:
                    #hash = str(re.findall(r'btih:(.*?)&', link)[0].lower())
                    hash=link.split('btih:')[1]
                    if '&' in hash:
                        hash=hash.split('&')[0]
                except:
                    try:
                        hash =link.split('btih:')[1]
                    except:
                        continue
                hash=hash.lower()
                self.complete_hash.append(hash)
                if hash not in self.all_lk_in:
                    
                    self.all_lk_in.append(hash)
                    self.statistics['d_unique']+=1
                   
                    
                        
                    
                    
                    self.hash_index[hash]=link
                    self.all_names[hash]=name
                    self.all_q[hash]=quality.lower().replace('hd','720')
                    
    def anaylze_data(self):
        
        self.all_lk_in=[]
        self.all_ok=[]
        self.all_mag={}
        
        self.all_mag[0]=[]
 
        self.hash_index={}
        self.all_names={}
        self.all_q={}
        self.complete_hash=[]
        self.page_index=0
        
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                i=0
                for name_f in self.f_result:
                    
                    futures.append(executor.submit(self.trd_anaylze,name_f))
                    i+=1
                wait(futures)
        counter_hash=0
       
        for hash in self.all_lk_in:
            self.all_mag[self.page_index].append(hash)
            counter_hash+=1
            if counter_hash>150:
                self.page_index+=1
                self.all_mag[self.page_index]=[]
                counter_hash=0
        
        return self.all_mag,self.hash_index,self.all_names,self.all_q
    def trd_mass_hash(self,items):
        self.elapsed_time = time.time() - self.start_time
        self.dp.update(0, 'Analyze_data'+ time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time))+str(items))
        hashCheck=''
        try:
          hashCheck = rd.checkHash(self.all_mag[items])
        except:
          time.sleep(0.3)
          hashCheck = rd.checkHash(self.all_mag[items])
        log.warning('Trd:'+str(items))
        if isinstance(hashCheck, dict):
             for hash in hashCheck:
                ok=False
                try:
                    if 'rd' in hashCheck[hash]:
                        ok=True
                except Exception as e: 
                    log.warning(hash)
                    log.warning('Found error:'+str(e))
                    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Error', 'In RD55 %s:'%str(e))))
                    ok=False
                if ok and len(hashCheck[hash]['rd'])>0:
                    found_c_h=False
                    if self.tv_movie=='tv':
                        for storage_variant in hashCheck[hash]['rd']:
                            key_list = storage_variant.keys()
                            if found_c_h:
                                break
                            for items_t in hashCheck[hash]['rd']:
                               
                               if found_c_h:
                                  break
                               for itt in items_t:
                                if itt in self.all_rej:
                                    continue
                                test_name=items_t[itt]['filename'].lower() 
                                
                                if 1:#itt in key_list :
                                        if ('s%se%s.'%(self.season_n,self.episode_n) in test_name or 's%se%s '%(self.season_n,self.episode_n) in test_name or 'ep '+self.episode_n in test_name):
                                            found_c_h=True
                                            
                                            break
                                else:
                                    self.all_rej.append(itt)
                    else:
                        found_c_h=True
                        
                    if found_c_h and ('.mkv' in str(hashCheck[hash]['rd']) or '.avi' in str(hashCheck[hash]['rd'])  or '.mp4' in str(hashCheck[hash]['rd'])  or '.m4v' in str(hashCheck[hash]['rd'])):
                        self.all_hased.append(hash)
    def check_mass_hash(self):
        self.all_rej=[]
        self.all_hased=[]
        #for items in self.all_mag:
        #    self.trd_mass_hash(items)
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                i=0
                for items in self.all_mag:
                    
                    futures.append(executor.submit(self.trd_mass_hash,items))
                    i+=1
                wait(futures)
        self.all_ok=[]
        for items in self.all_hased:
            
            
            self.all_ok.append(self.hash_index[items.lower()])
        return self.all_hased,self.all_ok
        
    def save_for_nextup(self):
        self.dd=[]
        self.dd.append((self.name,self.show_original_year,self.original_title,self.id,self.season,self.episode,self.show_original_year,''))
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""data TEXT);" % 'nextup')
        
        dbcur.execute("DELETE FROM nextup")
        code=(base64.b64encode(json.dumps(self.dd).encode("utf-8"))).decode("utf-8")
        try:
           dbcur.execute("INSERT INTO nextup Values ('%s')"%(code))
        except:
            dbcur.execute("DROP TABLE IF EXISTS nextup;")
            dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""data TEXT);" % 'nextup')
            dbcur.execute("INSERT INTO nextup Values ('%s')"%(code))
        dbcon.commit()
        
        dbcur.close()
        dbcon.close()
    def filter_sources(self):
        max_q_t=[720,1080,2160]
        min_q_t=[0,720,1080,2160]
        if self.tv_movie=='movie':
            added=''
        else:
            added='_tv'
        self.max_q=max_q_t[int(self.Addon.getSetting('max_q'+added))]
        self.min_q=min_q_t[int(self.Addon.getSetting('min_q'+added))]
        
        self.disable_3d=self.Addon.getSetting('3d'+added)=='false'
        self.disable_hdvc=self.Addon.getSetting('hdvc'+added)=='false'
        self.disable_low=self.Addon.getSetting('low_q'+added)=='false'
        self.encoding_filter=self.Addon.getSetting('encoding_filter'+added)=='true'
    def clean_title(title, broken=None):
        title = title.lower()
        # title = tools.deaccentString(title)
        
        title = ''.join(char for char in title if char in string.printable)
        title= title.encode('ascii', errors='ignore').decode('ascii', errors='ignore')
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
    def getInfo(release_title):
        info = []
        
        release_title=self.clean_title(release_title)
        #release_title=release_title.lower().replace('.',' ')
        
        if any(i in release_title for i in ['x265', 'x 265', 'h265', 'h 265', 'hevc','hdr']):
            info.append('HEVC')

        

        

        if any(i in release_title for i in [' cam ', 'camrip', 'hdcam', 'hd cam', ' ts ', 'hd ts', 'hdts', 'telesync', ' tc ', 'hd tc', 'hdtc', 'telecine', 'xbet']):
            info.append('CAM')
        if any(i in release_title for i in [' 3d']):
            info.append('3D')
            
        return info
    def clean_marks(self,title):
        regex='\[(.+?)\]'
        m=re.compile(regex).findall(title)
        
        for items in m:
            title=title.replace('[%s]'%items,'')
        regex='[0-9]{1,2}x[0-9]*'
        m=re.compile(regex).findall(title)
        if len(m)>0:
            title=title.replace(m[0],'').strip()
        return title
    def is_hebrew(self,term):
        try:
            import unicodedata
            hebrew=False
            for i in term:
                
                
                if 'HEBREW' in unicodedata.name(i.strip()):
                    hebrew=True
                    break

            return hebrew
        except Exception as e:
            log.warning('Error in is_hebrew:'+str(e))
            log.warning(term)
        
    def check_rejected(self,name):
       try:
        
        show_original_year,season,episode,original_title,tv_movie,heb_name,filter_lang=self.show_original_year,self.season,self.episode,self.original_title,self.tv_movie,self.heb_name,self.filter_lang
        rejedcted=False
        cl_name=self.clean_marks(name)
        c_name=cl_name.replace('%27','').replace("'",'').replace('%20',' ').replace('and','').replace('.&.','').replace(' & ','').replace(' and ','').replace('_','.').replace('%3A','.').replace('%3a','.').replace(':','').replace('-','.').replace('[','(').replace(']',')').replace('  ','.').replace(' ','.').replace('....','.').replace('...','.').replace('..','.').replace("'",'').strip().lower()
        heb_name=heb_name.replace('_','.').replace('%3A','.').replace('%3a','.').replace(':','').replace('-','.').replace('[','(').replace(']',')').replace('  ','.').replace(' ','.').replace('....','.').replace('...','.').replace('..','.').replace("'",'').strip().lower()
        
            
        
        '''
        info=(PTN.parse(c_name))
        try:
            info['title'] = re.findall("[a-zA-Z0-9. -_]+",info['title'])[0].encode('utf-8')
        except:
            pass
        try:
            info['title']=info['title'].encode('utf-8')
        except:
            pass
        '''
        original_title=original_title.replace('%27','').replace("'",'').replace('%20',' ').replace('and','').replace('_','.').replace('%3A','.').replace('%3a','.').replace(':','').replace('-','.').replace('[','(').replace(']',')').replace('  ','.').replace(' ','.').replace('....','.').replace('...','.').replace('..','.').replace("'",'').strip().lower()
     
        original_title_alt=original_title.replace('%20',' ').replace('and','').replace('.&.','').replace(' & ','').replace(' and ','').replace('_','.').replace('%3A','.').replace('%3a','.').replace(':','').replace('-','.').replace('[','(').replace(']',')').replace('  ','.').replace(' ','.').replace('....','.').replace('...','.').replace('..','.').replace("'",'').strip().lower()
        #c_name=c_name.replace('&','').replace('and','')
        if 'stargirl' in original_title.lower():
            original_title=original_title.replace("dcs.",'')
            original_title=original_title.replace("dc%27s.",'')
        reject=False
        if tv_movie=='movie':
            if original_title not in c_name and original_title_alt not in c_name:
                #log.warning('c_name:'+c_name)
                #log.warning('original_title:'+original_title)
                reject=True
        else:
            clean_title_pre=re.compile('(.*?)?(\.|-)s?(\d{1,2})?e?(\d{2})\.(.*)').findall(cl_name.lower().replace(' ','.').replace('-','.'))
            log.warning(c_name)
            log.warning(clean_title_pre)
            
            clean_title=None
            try:
                if len(clean_title_pre)>0:
                    
                    clean_title=clean_title_pre[0][0]
            except:
                pass
            log.warning(clean_title)
            if len(season)==1:
              season_n="0"+season
            else:
              season_n=season
            if len(episode)==1:
              episode_n="0"+episode
            else:
              episode_n=episode
            
            if not clean_title: 
            #if original_title.replace('.','') not in c_name.replace('.','') and original_title_alt.replace('.','') not in c_name.replace('.',''):
            #if original_title.replace('.','') != c_name.replace('.','') and original_title_alt.replace('.','') != c_name.replace('.',''):
                log.warning('r1')
                reject=True
            elif clean_title.lower()!=original_title:
                reject=True
            elif 's%se%s.'%(season_n,episode_n) in c_name or 's%se%s###'%(season_n,episode_n) in c_name+'###'  or 's%se%s###'%(season,episode) in c_name+'###' or 's%se%s.'%(season,episode) in c_name:
                log.warning('r2')
                reject=False
            elif 'season' in c_name:
              
              if 'season.%s.'%season not in c_name.lower() and 'season.%s$$$'%season not in (c_name.lower()+'$$$') and 'season.%s$$$'%season_n not in (c_name.lower()+'$$$') and 'season.%s.'%season_n not in c_name.lower() and 'season %s'%season_n not in c_name and 'season %s '%season not in c_name and 's%s '%season not in c_name:
                log.warning('r3')
                reject=True
            elif '.s%s.'%season_n in c_name:
                log.warning('r4')
                reject=False
            else:
                log.warning('r5')
                reject=True
            log.warning(reject)
        if ' 3d' in original_title.lower() and '3d' not in name.lower():
             reject=True
        if filter_lang:
            all_lang=['rus','russian','fr','french','TrueFrench','ita','italiano','castellano','spanish','swedish','dk','danish','german','nordic','exyu','chs','hindi','polish','mandarin','kor','korean']
            for itt in all_lang:
                if '.'+itt+'.' in c_name and '.en.' not in c_name and '.eng.' not in c_name and '.english.' not in c_name:
                    reject=True
                    break
        
        h_name=heb_name.replace('.','')
        cc_name=c_name.replace('.','')
        
        if h_name in cc_name and self.is_hebrew(cc_name):
            
            if tv_movie=='tv':
                heb_name=heb_name.replace('.','').replace(' ','').replace('"','')
                c_name=c_name.replace('.','').replace(' ','').replace('"','')
                options=[heb_name+' ע%s פ%s'%(season,episode),heb_name+' ע%sפ%s'%(season,episode),heb_name+' עונה %s פרק %s'%(season,episode),original_title.replace('%20','.').replace(' ','.').replace('%27',"'").replace('%3a',":")+'.S%sE%s'%(season_n,episode_n)]
                
                if tv_movie=='tv':
                   reject=True
                   for it in options:
                    
                    if it.replace(' ','.').replace('.','').replace(' ','').lower() in c_name.replace(' ','.').replace('.','').replace(' ','').lower():
                        
                        reject=False
                        break
            
           
        return reject
        #info['title']=get_title(name)
        
        
        
        
        reject=False
        if tv_movie=='movie':
            
            
            if 'year' in info:
                if str(info['year'])==str(info['title']):
                  reject=False
                elif str(info['year'])!=show_original_year:
                    
                    reject=True
        else:
            if len(season)==1:
              season_n="0"+season
            else:
              season_n=season
            if len(episode)==1:
              episode_n="0"+episode
            else:
              episode_n=episode
            if 'year' in info:
                if str(info['year'])!=show_original_year:
                    reject=True
            if 'season' in info and 'episode' in info:
                if str(info['season'])!=season or str(info['episode'])!=episode:
                    reject=True
            
            elif 'season' in c_name.lower():
                
                if 'season %s'%season not in c_name.lower().replace('.','') and 'season %s'%season_n not in c_name.lower().replace('.',''):
                    reject=True
            elif ' s%s '%season_n in name.lower().replace('.',' '):
                
                reject=False
            else:
                
                reject=True
            
        try:
            o_name=clean_name(original_title,1).encode('utf-8').lower().replace('\'','').replace('&','and').replace(':',' ').replace('%3a',' ').replace('view ','').replace('(',' ').replace(')',' ').replace('.',' ').replace('  ',' ').replace('!','').replace('3d','').strip()

            m_name=(info['title'].lower().replace('\'','').replace('&','and').replace(':',' ').replace('%3a',' ').replace('view ','').replace('[I]','').replace('.',' ').replace('(',' ').replace(')',' ').replace('  ',' ').replace('!','')).replace('3d','').strip()
            heb_name=heb_name.lower().replace('\'','').replace('&','and').replace(':',' ').replace('%3a',' ').replace('view ','').replace('[I]','').replace('.',' ').replace('(',' ').replace(')',' ').replace('  ',' ').replace('!','').replace('3d','').strip()
        except:
             return False
        '''
        import difflib

        cases=[(o_name,m_name)] 

        for a,b in cases:     
            log.warning('{} => {}'.format(a,b))  
            for i,s in enumerate(difflib.ndiff(a, b)):
                if s[0]==' ': continue
                elif s[0]=='-':
                    log.warning(u'Delete "{}" from position {}'.format(s[-1],i))
                elif s[0]=='+':
                    log.warning(u'Add "{}" to position {}'.format(s[-1],i))    
        '''
        if ' 3d' in original_title.lower() and '3d' not in name.lower():
             rejedcted=True
        if filter_lang:
            
            if 'language' in info:
                
                if 'English' not in info['language'] and 'english' not in info['language']:
                    
                    reject=True
       
        if o_name != m_name or reject:
            
            rejedcted=True
        
        if heb_name in m_name:
            rejedcted=False
       
        

        return rejedcted
       
       except Exception as e:
        import linecache
        sources_searching=False
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        log.warning('ERROR IN rejedcted IN:'+str(lineno))
        log.warning('inline:'+line)
        log.warning('Error:'+str(e))
       
        return True
    def trd_orginize(self,items):
        for name,lk,data,quality in self.f_result[items]['links']:
                self.elapsed_time = time.time() - self.start_time
                continue_next=False
               
                try:
                   int_q=int(quality)
                   if int_q<self.min_q or int_q>self.max_q:
                    continue_next=True
                except:
                   if self.min_q>0:
                      continue_next=True
                   pass
               
                if self.encoding_filter:
                   data_name=self.getInfo(name)
                 
                   if 'CAM' in data_name and self.disable_low:
                     continue_next=True
                   if 'HEVC' in data_name and self.disable_hdvc:
                     continue_next=True
                   if '3D' in data_name and self.disable_3d:
                     continue_next=True
                
                
                
                if lk in self.all_ok:
                    self.statistics['cached']+=1
                    if self.check_rejected(name) :
                        
                        if continue_next:
                            self.all_filted_rejected.append(('[COLOR red][I]'+name+'[/I][/COLOR]',lk,data,fix_q(quality),quality,items.replace('magnet_','').replace('.py',''),))
                            continue
                        
                        self.all_rejected.append(('[COLOR red][I]'+name+'[/I][/COLOR]',lk,data,fix_q(quality),quality,items.replace('magnet_','').replace('.py',''),))
                    else:
                        if continue_next:
                            self.all_filted.append((name,lk,data,fix_q(quality),quality,items.replace('magnet_','').replace('.py',''),))
                            continue
                        self.all_data.append((name,lk,data,fix_q(quality),quality,items.replace('magnet_','').replace('.py',''),))
    def orginize_sources(self):
        self.all_data=[]
        self.all_rejected=[]
        self.all_filted=[]
        self.all_filted_rejected=[]
        self.filter_lang=Addon.getSetting("filter_non_e")=='true'
        al_lk_count=0
        all_dup=0
        all_cached=0
        all_unc=0
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            i=0
            for items in self.f_result:
                
                futures.append(executor.submit(self.trd_orginize,items))
                i+=1
            wait(futures)
            
        
            
        if len(self.all_data)==0:
            xbmc.executebuiltin((u'Notification(%s,%s)' % (self.Addon.getAddonInfo('name'), self.Addon.getLocalizedString(32085))))
            
            cache.clear(['sources'])
        else:
            self.all_data=sorted(self.all_data, key=lambda x: x[3], reverse=False)
        return self.all_data
    def check_forbiden(self,nm):
        forbidden_words=[' xxx ',' cock ',' lesbian ',' horny ',' ass ',' gay ',' porn ','adulttime','fuck','brazzers','cock',' anal ','mature','pornstar',' sucking ','bigtits','boobs','masturbate',' milf ']
        forbidden_end_with_words=[' xxx',' cock',' lesbian',' horny',' ass',' gay',' porn']

        n_test=nm.lower().replace('.',' ').replace('-',' ').replace('_',' ')
        continue_next=False
        for itt in forbidden_end_with_words:
         
          if n_test.endswith(itt):
            continue_next=True
            break
        
        for itt in forbidden_words:
          
          
          if itt in n_test:
                    
                    continue_next=True
                    break
        return continue_next  
    
    def orginize_quality(self):
        all_2160_fav=[]
        all_1080_fav=[]
        all_720_fav=[]
        all_rest_fav=[]
        
            
        all_2160=[]
        all_1080=[]
        all_720=[]
        all_rest=[]
        all_rejected_orginged=[]
        for name,lk,data,fix,quality,source in self.all_rejected:
            
            
            
            in_2160=all_2160
            in_1080=all_1080
            in_720=all_720
            in_rest=all_rest
                
            self.elapsed_time = time.time() - self.start_time
            
            try:
                data_f=float(data)
            except:
                data_f=0
            
            if fix==1:
                in_2160.append((name,lk,data_f,fix,quality,source))
            elif fix==2:
                in_1080.append((name,lk,(data_f),fix,quality,source))
            elif fix==3:
                in_720.append((name,lk,(data_f),fix,quality,source))
            else:
                in_rest.append((name,lk,(data_f),fix,quality,source))
        all_2160=sorted(all_2160, key=lambda x: x[2], reverse=True)
        all_1080=sorted(all_1080, key=lambda x: x[2], reverse=True)
        all_720=sorted(all_720, key=lambda x: x[2], reverse=True)
        all_rest=sorted(all_rest, key=lambda x: x[2], reverse=True)
        
        
        
        all_rejected_orginged=all_2160+all_1080+all_720+all_rest
        
        
        all_2160=[]
        all_1080=[]
        all_720=[]
        all_rest=[]
        
        for name,lk,data,fix,quality,source in self.all_data:
            
            
            
            in_2160=all_2160
            in_1080=all_1080
            in_720=all_720
            in_rest=all_rest
                
            self.elapsed_time = time.time() - self.start_time
            
            try:
                data_f=float(data)
            except:
                data_f=0
            
            if fix==1:
                in_2160.append((name,lk,data_f,fix,quality,source))
            elif fix==2:
                in_1080.append((name,lk,(data_f),fix,quality,source))
            elif fix==3:
                in_720.append((name,lk,(data_f),fix,quality,source))
            else:
                in_rest.append((name,lk,(data_f),fix,quality,source))
        
        all_2160=sorted(all_2160, key=lambda x: x[2], reverse=True)
        all_1080=sorted(all_1080, key=lambda x: x[2], reverse=True)
        all_720=sorted(all_720, key=lambda x: x[2], reverse=True)
        all_rest=sorted(all_rest, key=lambda x: x[2], reverse=True)
        
        self.all_data=all_2160+all_1080+all_720+all_rest+all_rejected_orginged
        all_c_name=[]
        all_dd=[]
        menu=[]
        all_f_sources=[]
        choise=[]
        for name,lk,data,fix,quality,source in self.all_data:
                self.elapsed_time = time.time() - self.start_time
                
                color='white'
                if '2160' in quality or '4k' in quality.lower():
                    color='yellow'
                elif '1080' in quality:
                    color='lightblue'
                elif '720' in quality:
                    color='lightgreen'
                if '5.1' in name or '5 1' in name:
                    sound='-[COLOR khaki]5.1[/COLOR]-'
                elif '7.1' in name  or '7 1' in name:
                    sound='-[COLOR khaki]7.1[/COLOR]-'
                else:
                    sound=''
                data=str(round(float(data), 2))
                
                try:
                    nm='[COLOR lightblue][B]'+name+'[/B][/COLOR]\n' 
                except:
                  try:
                    nm='[COLOR lightblue][B]'+name+'[/B][/COLOR]\n'
                  except:
                    nm=name
                
                continue_next=self.check_forbiden(name)
                
                if continue_next:
                    continue
                menu.append([source, source,sound,quality,nm,data+'GB',lk,''])
                all_c_name.append(name)
                all_f_sources.append(source)
                all_dd.append((name, lk, self.iconimage,self.fanart,nm+self.description,data,self.id,self.season,self.episode,self.original_title,self.show_original_year,json.dumps(self.dd)))
                choise.append(('[COLOR %s]%s-[/COLOR]%s[COLOR bisque][I]%s[/I][/COLOR]-%s'%(color,quality,sound,data+'GB',source,)))
        self.dp.close()
        result_string=''
        self.all_finish_data="plugin://%s/"%addon_id, menu,self.iconimage,self.fanart,self.description,str(result_string),'','',self.tv_movie,self.id,'',self.season,self.episode,self.show_original_year,self.original_title,self.heb_name,all_dd,all_f_sources,all_c_name
    def get_property(self,prop):
        return window.getProperty(prop)
    def set_property(self,prop,value):
        return window.setProperty(prop,value)
    def local_cache(self,function,timeout,*arg):
        return_value=[]
        a = hashlib.md5()
        b=[]
        for i in arg:
            a.update(str(i).encode('utf-8'))
            b.append(i)
        a = str(a.hexdigest())
        t=time.time()
        cachedata = self.get_property(a)
        if cachedata:
            return_value,saved_time=eval(cachedata)
            
            t1 = int(saved_time)
            t2 = int(time.time())

            update = (abs(t2 - t1) / 3600) >= int(timeout)
            
            if update == True:
               
                
                return_value=function(*arg)
                
                c=(return_value,t)
                c = self.set_property(a,repr(c))
        else:
            return_value=function(*arg)
            c=(return_value,t)
            c = self.set_property(a,repr(c))
        return return_value
    def all_tasks(self,id,season,episode):
        self.statistics={}
        self.statistics['magnet']=0
        self.statistics['cached']=0
        self.statistics['d_unique']=0
        self.dp = xbmcgui . DialogProgress ( )
        
        self.dp.create(Addon.getLocalizedString(32072),Addon.getLocalizedString(32073)+'\n'+ ''+'\n'+'')
        source_dir = os.path.join(addonPath, 'resources', 'sources')
        self.all_sources=self.trd_get_modules(source_dir)
        self.get_links()
        self.anaylze_data()
        self.check_mass_hash()
        self.save_for_nextup()
        self.filter_sources()
        self.all_data=self.orginize_sources()
        self.orginize_quality()
        self.dp.close() 
        return self.all_finish_data,self.statistics
        
    def collect_files(self):
        self.all_finish_data,self.statistics=self.local_cache(self.all_tasks,72,self.id,self.season,self.episode)
        #self.all_finish_data=cache.get(self.all_tasks,self.id,self.season,self.episode, 72,table='pages')
        
        addonid_task, menu,self.iconimage,self.fanart,self.description,result_string,temp1,temp2,self.tv_movie,self.id,temp3,self.season,self.episode,self.show_original_year,self.original_title,self.heb_name,all_dd,all_f_sources,all_c_name=self.all_finish_data
        result_string=Addon.getLocalizedString(32089)+str(self.statistics['magnet'])+Addon.getLocalizedString(32090)+str(self.statistics['d_unique'])+Addon.getLocalizedString(32091)+str(self.statistics['cached'])+'[/COLOR]'
        if self.Addon.getSetting("sources_window_n")=='2': 
            menu2 = ContextMenu_new4(addonid_task, menu,self.iconimage,self.fanart,self.description,str(result_string),'','',self.tv_movie,self.id,'',self.season,self.episode,self.show_original_year,self.original_title,self.heb_name)
        else:
            menu2 = ContextMenu_new2("plugin://%s/"%addon_id, menu,self.iconimage,self.fanart,self.description,str(result_string),'','',self.tv_movie,self.id,'',self.season,self.episode,self.show_original_year,self.original_title,self.heb_name)
        
        menu2.doModal()
        ret=menu2.selected_index_in
        del menu2
        log.warning('ret:'+str(ret))
        if ret!=-1:
            
            name,url,iconimage,fanart,description,data,id,season,episode,original_title,show_original_year,dd=all_dd[ret]
            try:
                f_name=all_c_name[ret]
            except:
                f_name=name
            try:
                f_source=all_f_sources[ret]
            except:
                 sys.exit(1)
            log.warning(play_link)
            play_link(f_name,url,iconimage,fanart,description,data,original_title,id,season,episode,show_original_year,dd,self.heb_name,nextup='true',video_data_exp={},all_dd=all_dd,start_index=ret,all_w={},source=f_source,tvdb_id='')
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            
        
        
        