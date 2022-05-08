import xbmcaddon ,os ,xbmc ,xbmcgui ,urllib  ,re ,xbmcplugin ,sys ,logging ,random #line:2
import mediaurl ,json ,time ,requests ,datetime ,zlib,base64 #line:3
from cfscrape import run_dds #line:4
import cache #line:5
from shutil import copyfile #line:6
__USERAGENT__ ='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'#line:7
Addon =xbmcaddon .Addon ()#line:9
__settings__ =Addon #line:10
__PLUGIN_PATH__ =Addon .getAddonInfo ('path')#line:11
addon_id =Addon .getAddonInfo ('id')#line:12
home_path =xbmc .translatePath ("special://home/addons/")#line:13
__plugin__ =Addon .getAddonInfo ('path').replace (home_path ,'')#line:15
import defen #line:18
parts =getattr (defen ,'parts',False )#line:20
year_cat =getattr (defen ,'year_cat',False )#line:21
a_b_cat =getattr (defen ,'a_b_cat',False )#line:22
ranking_cat =getattr (defen ,'ranking_cat',False )#line:23
all_m_cat =getattr (defen ,'all_m_cat',False )#line:24
cat_cat =getattr (defen ,'cat_cat',False )#line:25
cat_chan =getattr (defen ,'cat_chan',False )#line:26
enter =getattr (defen ,'enter',False )#line:27
link_enter =getattr (defen ,'link',False )#line:28
add_res =getattr (defen ,'add_res',False )#line:30
wh_new =getattr (defen ,'wh_new',False )#line:31
error_ad_w =getattr (defen ,'errors',False )#line:32
if error_ad_w :#line:33
    if len (error_ad_w )>2 :#line:34
        error_ad =error_ad_w #line:35
msg_mast =getattr (defen ,'msg_mast',False )#line:36
user_dataDir =(xbmc.translatePath(Addon .getAddonInfo ("profile")))
#user_dataDir =xbmc .translatePath (Addon .getAddonInfo ("profile"))#line:39
if not os .path .exists (user_dataDir ):#line:40
     os .makedirs (user_dataDir )#line:41
__addon__ =xbmcaddon .Addon ()#line:43
__cwd__ =xbmc .translatePath (__addon__ .getAddonInfo ('path'))#line:44
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
try:
    import HTMLParser
    html_parser = HTMLParser.HTMLParser()
   
except:
    import html as html_parser

if KODI_VERSION<=18:
    que=urllib.quote_plus
    url_encode=urllib.urlencode
else:
    que=urllib.parse.quote_plus
    url_encode=urllib.parse.urlencode
if KODI_VERSION<=18:
    unque=urllib.unquote_plus
    unque_plus=unque
else:
    unque=urllib.parse.unquote_plus
    unque_plus=unque
USER_AGENT ="Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"#line:48
TMDB_API_URL ="http://api.themoviedb.org/3/"#line:50
TMDB_API_KEY ='34142515d9d23817496eeb4ff1d223d0'#line:51
TMDB_NEW_API =7777 #line:52
ALL_MOVIE_PROPS ="account_states,alternative_titles,credits,images,keywords,releases,videos,translations,similar,reviews,lists,rating"#line:53
max_per_page =int (Addon .getSetting ("max_per_page2"))#line:54
__REQ_URL__ ='http://www.strimm.com/WebServices/ChannelWebService.asmx/GetCurrentlyPlayingChannelData?clientTime=!!!!!!&channelId=$$$$$&isEmbeddedChannel=false&userId=0'#line:55
sort_option =True #line:56
standalone =True #line:57
sort_option_cat =False #line:58
global local_list_data #line:59
import socket #line:60
if KODI_VERSION<=18:#kodi18
    if Addon.getSetting('debug')=='false':
        reload (sys )#line:61
        sys .setdefaultencoding ('utf8')#line:62
else:#kodi19
    import importlib
    importlib.reload (sys )#line:61
socket .setdefaulttimeout (60.0 )#line:63
exec ("temp=[] \ntemp.append('%s') \ntemp.append('%s') \ntemp.append('%s') \ntemp.append('%s') \nt1='' \nlists=[] \nfor items in temp: \n \t\t t1=t1+base64.b64decode(items).decode('utf-8') \nlists.append(t1) \n"%(parts [0 ],parts [1 ],parts [2 ],parts [3 ]))#line:64
l_list =lists [0 ]#line:66
logging.warning(l_list)
nanscarper =False #line:70
c_addon_name =Addon .getAddonInfo ('name')#line:71
local_list_c =True #line:73
local_list =os .path .join (__cwd__ ,'resources','fixed_list.zip')#line:75
subtitle_addr =['']#line:82
import threading #line:83
CONTACTICON ='https://comps.canstockphoto.com/oops-emoticon-clipart-vector_csp50993858.jpg'#line:89
CONTACTFANART ='http://'#line:90
COLOR1 ='gold'#line:92
COLOR2 ='white'#line:93
COLOR3 ='red'#line:94
COLOR3 ='blue'#line:95
THEME2 ='[COLOR '+COLOR2 +']%s[/COLOR]'#line:98
THEME3 ='[COLOR '+COLOR1 +']%s[/COLOR]'#line:100
ACTION_PREVIOUS_MENU =10 #line:103
ACTION_SELECT_ITEM =7 #line:104
ACTION_MOVE_UP =3 #line:105
ACTION_MOVE_DOWN =4 #line:106
ACTION_STEP_BACK =21 #line:107
ACTION_NAV_BACK =92 #line:108
ACTION_MOUSE_RIGHT_CLICK =101 #line:109
ACTION_MOUSE_MOVE =107 #line:110
ACTION_BACKSPACE =110 #line:111
KEY_BUTTON_BACK =275 #line:112
def contact (title ='',msg =""):#line:114
	class O0O00OO0O0000OO0O (xbmcgui .WindowXMLDialog ):#line:115
		def __init__ (O00O0O0O0O00O0OOO ,*OO0000O0O0OOO0O00 ,**O0O0O00O000O00000 ):#line:116
			O00O0O0O0O00O0OOO .title =THEME3 %O0O0O00O000O00000 ["title"]#line:117
			O00O0O0O0O00O0OOO .image =O0O0O00O000O00000 ["image"]#line:118
			O00O0O0O0O00O0OOO .fanart =O0O0O00O000O00000 ["fanart"]#line:119
			O00O0O0O0O00O0OOO .msg =THEME2 %O0O0O00O000O00000 ["msg"]#line:120
		def onInit (O00OOOOO00O00O0OO ):#line:122
			O00OOOOO00O00O0OO .fanartimage =101 #line:123
			O00OOOOO00O00O0OO .titlebox =102 #line:124
			O00OOOOO00O00O0OO .imagecontrol =103 #line:125
			O00OOOOO00O00O0OO .textbox =104 #line:126
			O00OOOOO00O00O0OO .scrollcontrol =105 #line:127
			O00OOOOO00O00O0OO .button =199 #line:128
			O00OOOOO00O00O0OO .showdialog ()#line:129
		def showdialog (OO00000OOO0O00O00 ):#line:131
			OO00000OOO0O00O00 .getControl (OO00000OOO0O00O00 .imagecontrol ).setImage (OO00000OOO0O00O00 .image )#line:132
			OO00000OOO0O00O00 .getControl (OO00000OOO0O00O00 .fanartimage ).setImage (OO00000OOO0O00O00 .fanart )#line:133
			OO00000OOO0O00O00 .getControl (OO00000OOO0O00O00 .fanartimage ).setColorDiffuse ('9FFFFFFF')#line:134
			OO00000OOO0O00O00 .getControl (OO00000OOO0O00O00 .textbox ).setText (OO00000OOO0O00O00 .msg )#line:135
			OO00000OOO0O00O00 .getControl (OO00000OOO0O00O00 .titlebox ).setLabel (OO00000OOO0O00O00 .title )#line:136
			OO00000OOO0O00O00 .setFocusId (OO00000OOO0O00O00 .button )#line:141
		def onAction (OO0OOO0O00O0OOO0O ,OO0OOOO00O0OO0OO0 ):#line:143
			if OO0OOOO00O0OO0OO0 ==ACTION_PREVIOUS_MENU :OO0OOO0O00O0OOO0O .close ()#line:144
			elif OO0OOOO00O0OO0OO0 ==ACTION_NAV_BACK :OO0OOO0O00O0OOO0O .close ()#line:145
	O00O0O0OOO0OO0OO0 =O0O00OO0O0000OO0O ("Contact.xml",Addon .getAddonInfo ('path'),'DefaultSkin',title =title ,fanart =CONTACTFANART ,image =CONTACTICON ,msg =msg )#line:147
	O00O0O0OOO0OO0OO0 .doModal ()#line:148
	del O00O0O0OOO0OO0OO0 #line:149
class f_msg (xbmcgui .WindowXMLDialog ):#line:151
    def __init__ (OO00O0O00OOOO0O00 ,*O0000O0O0O00OO0O0 ,**OO00OOOOO0O0OOOOO ):#line:152
        OO00O0O00OOOO0O00 .title =THEME3 %OO00OOOOO0O0OOOOO ["title"]#line:153
        OO00O0O00OOOO0O00 .image =OO00OOOOO0O0OOOOO ["image"]#line:154
        OO00O0O00OOOO0O00 .fanart =OO00OOOOO0O0OOOOO ["fanart"]#line:155
        OO00O0O00OOOO0O00 .msg =THEME2 %OO00OOOOO0O0OOOOO ["msg"]#line:156
        OO00O0O00OOOO0O00 .msg2 =THEME2 %OO00OOOOO0O0OOOOO ["msg2"]#line:157
    def onInit (O00000O000OOO00OO ):#line:158
        O00000O000OOO00OO .fanartimage =101 #line:159
        O00000O000OOO00OO .titlebox =102 #line:160
        O00000O000OOO00OO .imagecontrol =103 #line:161
        O00000O000OOO00OO .textbox =104 #line:162
        O00000O000OOO00OO .textbox2 =106 #line:163
        O00000O000OOO00OO .scrollcontrol =105 #line:164
        O00000O000OOO00OO .button =199 #line:165
        O00000O000OOO00OO .showdialog ()#line:166
    def showdialog (OOOOOO00000O00OO0 ):#line:168
        OOOOOO00000O00OO0 .getControl (OOOOOO00000O00OO0 .imagecontrol ).setImage (OOOOOO00000O00OO0 .image )#line:169
        OOOOOO00000O00OO0 .getControl (OOOOOO00000O00OO0 .fanartimage ).setImage (OOOOOO00000O00OO0 .fanart )#line:170
        OOOOOO00000O00OO0 .getControl (OOOOOO00000O00OO0 .fanartimage ).setColorDiffuse ('9FFFFFFF')#line:171
        OOOOOO00000O00OO0 .getControl (OOOOOO00000O00OO0 .textbox ).setText (OOOOOO00000O00OO0 .msg2 )#line:172
        OOOOOO00000O00OO0 .getControl (OOOOOO00000O00OO0 .textbox2 ).setText (OOOOOO00000O00OO0 .msg )#line:173
        OOOOOO00000O00OO0 .getControl (OOOOOO00000O00OO0 .titlebox ).setLabel (OOOOOO00000O00OO0 .title )#line:174
        OOOOOO00000O00OO0 .setFocusId (OOOOOO00000O00OO0 .button )#line:179
    def onAction (O00O000OOOO0O0000 ,O00OOOO0OO0O00OOO ):#line:181
        if O00OOOO0OO0O00OOO ==ACTION_PREVIOUS_MENU :O00O000OOOO0O0000 .close ()#line:182
        elif O00OOOO0OO0O00OOO ==ACTION_NAV_BACK :O00O000OOOO0O0000 .close ()#line:183
progress_bar =Addon .getSetting ("Progress")#line:187
cat_images =['http://ngarba.xyz/adds/yos/18.jpg','https://static2.cbrimages.com/wordpress/wp-content/uploads/2018/12/avengers-4-end-game-2019-06-2560x1600.jpg']#line:188
in_cat =['http://www.hdiphone6wallpapers.net/iphone-6-backgrounds/iphone-6-wallpapers-1/iphone-6-wallpapers-hd-722bq7l7-1080x1920.jpg','https://www.planwallpaper.com/static/images/2015-wallpaper_111525594_269.jpg']#line:189

year_img =['http://ngarba.xyz/adds/yos/20.jpg','https://hdqwalls.com/download/2016-x-men-apocalypse-movie-hd-2560x1600.jpg']#line:191
in_year_img =['http://media.148apps.com/screenshots/1002084089/us-iphone-5-best-hd-science-fiction-wallpapers-for-ios-8-backgrounds-sci-fi-theme-pictures-collection.jpeg','https://www.planwallpaper.com/static/images/3865967-wallpaper-full-hd_XNgM7er.jpg']#line:192
letter_img =['http://ngarba.xyz/adds/yos/1.jpg','http://www.wallpapermaiden.com/wallpaper/28553/download/2560x1600/alita-battle-angel-sci-fi-movies.jpeg']#line:194
in_letter_img =['http://www.4usky.com/data/out/100/164911738-war-machine-wallpapers.jpg','https://wallpaperstudio10.com/static/wpdb/wallpapers/1920x1080/176076.jpg']#line:195
ratin_img =['http://ngarba.xyz/adds/yos/14.jpg','https://images6.alphacoders.com/402/402184.jpg']#line:197
in_ratin_img =['https://i.pinimg.com/originals/60/f3/2a/60f32aa4aef73050d8e36d2bf3853b96.jpg','http://wallpaperget.com/images/new-wallpaper-hd-38.jpg']#line:198
all_img =['http://ngarba.xyz/adds/yos/21.jpg','https://alltop10.org/wp-content/uploads/2018/07/Tor-Ragnarek.jpg']#line:200
tv_images =['http://ngarba.xyz/adds/yos/10.jpg','https://www.wallpapermaiden.com/wallpaper/30253/download/2560x1600/alita-battle-angel-animation-sci-fi-movies.jpeg']#line:202
chek_img =['https://i.imgur.com/ZZq5O7I.png','https://wallpapercave.com/wp/SmJpcB0.jpg']#line:204
server =['https://i.imgur.com/89hvDUu.png','https://www.planwallpaper.com/static/images/3865967-wallpaper-full-hd_XNgM7er.jpg']#line:206
path =os .path .join (__PLUGIN_PATH__ ,"resources")#line:208
from data import *#line:210
global dbcur ,dbcon #line:211
cacheFile =os .path .join (user_dataDir ,'localfile.txt')#line:212
logging .warning (cacheFile )#line:213
logging .warning (os .path .exists (cacheFile ))#line:214

if not os .path .exists (cacheFile ):#line:216
    logging .warning ('IN')#line:217
    path =os .path .join (__PLUGIN_PATH__ ,"resources")#line:218
    download_file (l_list ,path )#line:219
    logging .warning ('Unzipping')#line:221
    unzip (os .path .join (path ,"fixed_list.zip"))#line:222
    dbcon =database .connect (cacheFile )#line:226
    dbcur =dbcon .cursor ()#line:227
else :#line:228
    logging .warning ('HERE:'+cacheFile)#line:231
    dbcon =database .connect (cacheFile )#line:232
    dbcur =dbcon .cursor ()#line:233
    
        
watched =os .path .join (user_dataDir ,'watched.db')#line:236
dbcon_w =database .connect (watched )#line:238
dbcur_w =dbcon_w .cursor ()#line:239
dbcur_w .execute ("CREATE TABLE IF NOT EXISTS watched ( " "name TEXT," "link TEXT, " "data TEXT, " "op1 TEXT, " "op2 TEXT, " "op3 TEXT);")#line:244
domain_s ='https://'#line:245
dbcon .commit ()#line:247
try :#line:248
    dbcur .execute ("SELECT * FROM settings")#line:249
    match =dbcur .fetchall ()#line:251
    all_values =[]#line:252
    for name ,value in match :#line:253
        all_values .append (value )#line:254
    cat_cat =all_values [0 ]=='True'#line:256
    year_cat =all_values [1 ]=='True'#line:257
    a_b_cat =all_values [2 ]=='True'#line:258
    ranking_cat =all_values [3 ]=='True'#line:259
    all_m_cat =all_values [4 ]=='True'#line:260
    cat_chan =all_values [5 ]=='True'#line:262
    add_res =all_values [6 ]=='True'#line:263
    enter =all_values [7 ]#line:264
    link_enter =all_values [8 ]#line:265
    error_ad =all_values [9 ]#line:266
    msg_mast =all_values [10 ]#line:267
    sort_option_cat =all_values [12 ]=='True'#line:268
except Exception as e :#line:269
    logging .warning (e )#line:270
    pass #line:271
sort_by_episode =False #line:275
def _OOOO0OO000O0O00OO (O0O0OO000O000O0OO ,headers ={}):#line:276
    if not headers .has_key ('User-Agent'):#line:277
        headers ['User-Agent']=USER_AGENT #line:278
    OO0OOO0OOOOO00O0O =urllib2 .Request (url =O0O0OO000O000O0OO ,headers =headers )#line:280
    try :#line:281
        return urllib2 .urlopen (OO0OOO0OOOOO00O0O ,timeout =3 ).read ()#line:282
    except urllib2 .HTTPError as O000O0OO0000OO00O :#line:284
        return O000O0OO0000OO00O .code #line:285
def imdb_get_info (O0OOOO00OO00O0000 ):#line:286
    O0O00O00OOO0O0O00 ={}#line:287
    O0OOO00OO0OO0OOOO =_OOOO0OO000O0O00OO ("http://www.imdb.com/title/%s"%O0OOOO00OO00O0000 )#line:289
    if isinstance (O0OOO00OO0OO0OOOO ,int ):#line:290
        if O0OOO00OO0OO0OOOO ==404 :#line:291
            print ("IMDB Error: Movie '%s' not found."%O0OOOO00OO00O0000 )#line:292
        else :#line:293
            print ("IMDB Error: Unknown error (%s)."%O0OOO00OO0OO0OOOO )#line:294
        return {}#line:295
    OOOOO0O000O0O000O =re .search ('<time itemprop="duration" datetime="PT(\d+)M">',O0OOO00OO0OO0OOOO )#line:297
    if OOOOO0O000O0O000O :#line:298
        O0O00O00OOO0O0O00 ['duration']=int (OOOOO0O000O0O000O .group (1 ))#line:299
    OO00O00O00000O0OO =re .search ('itemprop="ratingValue">([\d\.]+)<',O0OOO00OO0OO0OOOO )#line:301
    O000O0OOOO0O0000O =re .search ('itemprop="ratingCount">([\d,]+)<',O0OOO00OO0OO0OOOO )#line:302
    if OO00O00O00000O0OO and O000O0OOOO0O0000O :#line:303
        O0O00O00OOO0O0O00 .update ({'rating':round (float (OO00O00O00000O0OO .group (1 )),1 ),'votes':O000O0OOOO0O0000O .group (1 )})#line:305
    return O0O00O00OOO0O0O00 #line:306
def decode (O0OO0O00000000O0O ,OO0OO00OOOOO0OOOO ):#line:307
    import base64 #line:308
    O00OO0OOO00000OO0 =[]#line:309
    if (len (O0OO0O00000000O0O ))!=4 :#line:311
     return 10 #line:312
    OO0OO00OOOOO0OOOO =base64 .urlsafe_b64decode (OO0OO00OOOOO0OOOO )#line:313
    for O0OOO0O0O0OO0O000 in range (len (OO0OO00OOOOO0OOOO )):#line:314
        OOOO0O00O0O00OO0O =O0OO0O00000000O0O [O0OOO0O0O0OO0O000 %len (O0OO0O00000000O0O )]#line:315
        O0OO0O0OO0O0O0OO0 =chr ((256 +ord (OO0OO00OOOOO0OOOO [O0OOO0O0O0OO0O000 ])-ord (OOOO0O00O0O00OO0O ))%256 )#line:316
        O00OO0OOO00000OO0 .append (O0OO0O0OO0O0O0OO0 )#line:317
    return "".join (O00OO0OOO00000OO0 )#line:318
def tmdb_list (O00O0O00OOOO0O00O ):#line:319
    OO0OOOOO0000OO0O0 =decode ("7643",O00O0O00OOOO0O00O )#line:322
    return int (OO0OOOOO0000OO0O0 )#line:325
def u_list (O0O0000O0O0OOO000 ):#line:326
    OO0O000OO000O00OO =tmdb_list (TMDB_NEW_API )#line:329
    OOO00000OOO0OO0O0 =str ((getHwAddr ('eth0'))*OO0O000OO000O00OO ).encode ('base64')#line:330
    OO000O0OOO0OOOOOO =int (__settings__ .getSetting ("pass"))#line:331
    OO0OOO0OOOO000O00 =int (OOO00000OOO0OO0O0 .decode ('base64'))/OO000O0OOO0OOOOOO #line:333
    OOO0OOOOOOOOO00O0 =decode (str (OO0OOO0OOOO000O00 ),O0O0000O0O0OOO000 )#line:335
    return OOO0OOOOOOOOO00O0 #line:336
def disply_hwr ():#line:337
   O000000OO00OOOOO0 =tmdb_list (TMDB_NEW_API )#line:338
   OOO00O00O0O0000O0 =str ((getHwAddr ('eth0'))*O000000OO00OOOOO0 ).encode ('base64')#line:340
   OO0O000O000OOO00O ={'api_dev_key':'57fe1369d02477a235057557cbeabaa1','api_option':'paste','api_paste_code':OOO00O00O0O0000O0 }#line:341
   OO0000OO00O00OOO0 =urllib .urlopen ('http://pastebin.com/api/api_post.php',urllib .urlencode (OO0O000O000OOO00O ))#line:342
   O0000OO00OO0O0O0O =OO0000OO00O00OOO0 .read ()#line:344
   xbmcgui .Dialog ().ok ("Own HWR",OOO00O00O0O0000O0 +'\n'+O0000OO00OO0O0O0O )#line:348
def read_youtube_html (O00OOO000OOOO00OO ):#line:349
    import requests #line:350
    O0000OO00OO0000O0 ={'PREF':'HIDDEN_MASTHEAD_ID=wo5p019sJqo&f5=30&al=iw&f1=50000000','VISITOR_INFO1_LIVE':'gAV32V2Yoj8','CONSENT':'YES+DE.iw+V8','_ga':'GA1.2.1102943109.1491329246','SID':'dwUD0z1Qek9KRby-x5XPgGDzQVG-F22gAWRG-hIZ0T85iPLxHTZ1qeV7Kr9HAIecMfmbUw.','HSID':'AHjPEdvJ_szjJ5F2Z','SSID':'ASgUq0eqtQ0f_-MKn','APISID':'3FDXL0Fkpx4JsALg/ADDeScfwowfIywKQ-','SAPISID':'ngB1aCu7aYw_K80J/AbvIGXHBVhRKkBkEB','LOGIN_INFO':'ACn9GHowRQIhAOJM7W72jweA43hTqrmGr838IybkLYvnhyBxe14lKurkAiAIkD_J906auUMSZBMOtsow__mxSrq8DeL7IHhyb33DIQ:QUxJMndvSEU5akJPZnd2ZmE3dWgtVW9Tbl9QRUNXMTNfWGJlUTNRaFFzYUtfNXlPeEtTcHJOb0piY0Z1NjllVUNEQm5tU1JHSm9YY0dIYXJ6cm41Z0NMTmtZZVpCRi1sUk1jamhLU3VzTlR0dWZxM1doU3pyZEhUdzBJcnhfQi1McVZqTE5lTEFaTGNYOC1JdU8yM2djQWVnblhZc0xVSGxBbVNhd2tYTXdBd2lRMjl2eUJMaW0w','YSC':'K7YgNPoPQDY','s_gl':'d51766b086658500406c2f99316de348cwIAAABJTA==',}#line:365
    OOO0OO00OOOO00OOO ={'Host':'www.youtube.com','User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3','Connection':'keep-alive','Upgrade-Insecure-Requests':'1','Pragma':'no-cache','Cache-Control':'no-cache',}#line:376
    OOO0O0O00OO00OO0O =requests .get (O00OOO000OOOO00OO ,headers =OOO0OO00OOOO00OOO ).text #line:378
    if 'ytInitialData'not in OOO0O0O00OO00OO0O :#line:379
      OOO0O0O00OO00OO0O =requests .get (O00OOO000OOOO00OO ,headers =OOO0OO00OOOO00OOO ).text #line:380
    return OOO0O0O00OO00OO0O .encode ('utf8')#line:381
def getHwAddr (O0OOOOO000OOO0O0O ):#line:382
   import subprocess #line:383
   O0OO0000OO0O0000O ='windows'#line:384
   if xbmc .getCondVisibility ('system.platform.android'):#line:385
       O0OO0000OO0O0000O ='android'#line:386
   if (O0OO0000OO0O0000O =='android'):#line:387
     O0OO00OO000OO0O0O =subprocess .Popen (["exec ''ip link''"],executable ='/system/bin/sh',shell =True ,stdout =subprocess .PIPE ,stderr =subprocess .STDOUT ).communicate ()[0 ].splitlines ()#line:388
     O0OOOOO0OO00000OO =re .compile ('link/ether (.+?) brd').findall (str (O0OO00OO000OO0O0O ))#line:390
     for O0O0O0OOOOO000000 in O0OOOOO0OO00000OO :#line:391
      if O0OOOOO0OO00000OO !='00:00:00:00:00:00':#line:392
          O00OOO00OOO0O000O =O0O0O0OOOOO000000 #line:393
          break #line:394
   else :#line:395
       O0OO0O0O0000OO00O =0 #line:396
       while (1 ):#line:397
         O00OOO00OOO0O000O =xbmc .getInfoLabel ("network.macaddress")#line:398
         if O00OOO00OOO0O000O !="Busy"and O00OOO00OOO0O000O !=' עסוק':#line:400
            break #line:402
         else :#line:403
           O0OO0O0O0000OO00O =O0OO0O0O0000OO00O +1 #line:404
           time .sleep (1 )#line:405
           if O0OO0O0O0000OO00O >30 :#line:406
            break #line:407
   O00O0O0O0OO0O0O0O =int (O00OOO00OOO0O000O .replace (':',''),16 )#line:409
   return O00O0O0O0OO0O0O0O #line:410
def _O00O00O00OO00O00O (OOOO0O0OO0000OO00 ,get ={},post =None ):#line:411
    get ['api_key']=TMDB_API_KEY #line:412
    get =dict ((O0O0OO0000O0O00OO ,O000OO0O00OOOOOO0 )for (O0O0OO0000O0O00OO ,O000OO0O00OOOOOO0 )in get .iteritems ()if O000OO0O00OOOOOO0 )#line:413
    get =dict ((O00O0O0OO000O00O0 , (O000OO0OO00000O00 ))for (O00O0O0OO000O00O0 ,O000OO0OO00000O00 )in get .iteritems ())#line:414
    OOOO0O00OO00O00OO ="%s%s?%s"%(TMDB_API_URL ,OOOO0O0OO0000OO00 ,urllib .urlencode (get ))#line:415
    O0O000OOO0OO0OO00 =urllib2 .Request (url =OOOO0O00OO00O00OO ,data =post ,headers ={'Accept':'application/json','Content-Type':'application/json','User-agent':USER_AGENT })#line:420
    try :#line:421
        O0O0O0O00O00O0O00 =urllib2 .urlopen (O0O000OOO0OO0OO00 ,timeout =10 ).read ()#line:422
    except urllib2 .HTTPError as O000O00O0OOO0OOOO :#line:424
        return O000O00O0OOO0OOOO .code #line:425
    return json .loads (O0O0O0O00O00O0O00 )#line:427
def imdb_id_to_tmdb (O000OOOO0O0OOOO00 ):#line:428
    O00O00O00OOO0OOO0 ={"external_source":"imdb_id"}#line:429
    OOO0O0000OO0OOOO0 =_O00O00O00OO00O00O ("find/%s"%O000OOOO0O0OOOO00 ,get =O00O00O00OOO0OOO0 )#line:431
    if isinstance (OOO0O0000OO0OOOO0 ,int ):#line:432
        if OOO0O0000OO0OOOO0 ==401 :#line:433
            print ("TMDB Error: Not authorized.")#line:434
        elif OOO0O0000OO0OOOO0 ==404 :#line:435
            print ("TMDB Error: IMDB id '%s' not found."%O000OOOO0O0OOOO00 )#line:436
        else :#line:437
            print ("TMDB Error: Unknown error.")#line:438
        return None #line:439
    elif not OOO0O0000OO0OOOO0 :#line:441
        print ("TMDB Error: Could not translate IMDB id to TMDB id")#line:442
        return None #line:443
    if len (OOO0O0000OO0OOOO0 ['movie_results']):#line:445
        return OOO0O0000OO0OOOO0 ['movie_results'][0 ]['id']#line:446
    else :#line:447
        return None #line:448
def tmdb_get_trailer (OO0O0O0OOOOOO0OOO ,language ="he"):#line:449
    O000OOOO00000OO00 ={"language":language }#line:450
    O000OO0OOOO0OOOOO =_O00O00O00OO00O00O ("movie/%s/videos"%OO0O0O0OOOOOO0OOO ,get =O000OOOO00000OO00 )#line:452
    if isinstance (O000OO0OOOO0OOOOO ,int ):#line:453
        if O000OO0OOOO0OOOOO ==401 :#line:454
            print ("TMDB Error: Not authorized.")#line:455
        elif O000OO0OOOO0OOOOO ==404 :#line:456
            print ("TMDB Error: Movie '%s' not found."%OO0O0O0OOOOOO0OOO )#line:457
        else :#line:458
            print ("TMDB Error: Unknown error.")#line:459
        return {language :None }#line:460
    elif not O000OO0OOOO0OOOOO :#line:462
        print ("TMDB Error: Could not get movie trailer")#line:463
        return {language :None }#line:464
    O00O00OO00000O000 =dict ((O0OOOO0O00O0O00O0 ['iso_639_1'],O0OOOO0O00O0O00O0 ['key'])for O0OOOO0O00O0O00O0 in O000OO0OOOO0OOOOO ['results']if O0OOOO0O00O0O00O0 ['site']=="YouTube"and O0OOOO0O00O0O00O0 ['type']=="Trailer")#line:467
    return {language :O00O00OO00000O000 .get (language ,None )}#line:468
def tmdb_movie_info (O0O00O000O0000000 ):#line:469
    OOO0O0O0000000O00 ={"append_to_response":ALL_MOVIE_PROPS ,"language":"he","include_image_language":"en,null,he"}#line:472
    O00OOOO0OOOO00O00 =_O00O00O00OO00O00O ("movie/%s"%O0O00O000O0000000 ,get =OOO0O0O0000000O00 )#line:474
    if isinstance (O00OOOO0OOOO00O00 ,int ):#line:475
        if O00OOOO0OOOO00O00 ==401 :#line:476
            print ("TMDB Error: Not authorized.")#line:477
        elif O00OOOO0OOOO00O00 ==404 :#line:478
            print ("TMDB Error: Movie '%s' not found."%O0O00O000O0000000 )#line:479
        else :#line:480
            print ("TMDB Error: Unknown error.")#line:481
        return {}#line:482
    elif not O00OOOO0OOOO00O00 :#line:484
        print ("TMDB Error: Could not get movie information")#line:485
        return {}#line:486
    return O00OOOO0OOOO00O00 #line:488
def add_movie (OOOO0000O00O0O00O ,youtube_trailer_id =None ):#line:489
    OOO0OO0OO0O0O0O0O =tmdb_movie_info (OOOO0000O00O0O00O )#line:491
    if not OOO0OO0OO0O0O0O0O :#line:492
        return None #line:493
    O00O0OO0000OOOOO0 =OOO0OO0OO0O0O0O0O ['title']#line:497
    OOOO0O00OO00OOOO0 =dict ((O000O000O0O000O00 ['iso_639_1'],O000O000O0O000O00 ['key'])for O000O000O0O000O00 in OOO0OO0OO0O0O0O0O ['videos']['results']if O000O000O0O000O00 ['site']=="YouTube"and O000O000O0O000O00 ['type']=="Trailer")#line:499
    OOOOOO000OOO000O0 =youtube_trailer_id or OOOO0O00OO00OOOO0 .get ('he',None )or tmdb_get_trailer (OOOO0000O00O0O00O ,"en").get ('en',None )#line:500
    OO0OO00OO0000O00O =[OOO00OO00O0O0O00O for OOO00OO00O0O0O00O in OOO0OO0OO0O0O0O0O ['releases'].get ('countries',[])if OOO00OO00O0O0O00O ['iso_3166_1']=="US"]#line:503
    if OO0OO00OO0000O00O :#line:504
        O0OOOOOO0OO0OO0O0 =OO0OO00OO0000O00O [0 ]['certification']#line:505
    elif OOO0OO0OO0O0O0O0O ['releases']['countries']:#line:506
        O0OOOOOO0OO0OO0O0 =OOO0OO0OO0O0O0O0O ['releases']['countries'][0 ]['certification']#line:507
    else :#line:508
        O0OOOOOO0OO0OO0O0 =""#line:509
    O00OOO0OOO0OOO0OO =OOO0OO0OO0O0O0O0O .get ('belongs_to_collection')#line:511
    OOOO00OOO0O0O00O0 =" / ".join ([OO00O0OO000O0OOO0 ['name']for OO00O0OO000O0OOO0 in OOO0OO0OO0O0O0O0O ['genres']])#line:512
    O0OOOOO0O0O0O00O0 =" / ".join ([O00000OO0OOO00000 ['name']for O00000OO0OOO00000 in OOO0OO0OO0O0O0O0O ['credits']['crew']if O00000OO0OOO00000 ['department']=="Writing"])#line:513
    OOO000000OO000O0O =" / ".join ([O0OO00O0O0O0000O0 ['name']for O0OO00O0O0O0000O0 in OOO0OO0OO0O0O0O0O ['credits']['crew']if O0OO00O0O0O0000O0 ['department']=="Directing"])#line:514
    O0OOO00O0OOOOO00O =" / ".join ([OOO0O0OO0OOOO0OO0 ['name']for OOO0O0OO0OOOO0OO0 in OOO0OO0OO0O0O0O0O ['production_companies']])#line:515
    O000O0OO0OOO0OOO0 =[{'name':O0O0OOO0OO000O000 ['name'],'role':O0O0OOO0OO000O000 ['character'],'thumbnail':"https://image.tmdb.org/t/p/w640/%s"%O0O0OOO0OO000O000 ['profile_path']if O0O0OOO0OO000O000 ['profile_path']else "",'order':O0O0OOO0OO000O000 ['order']}for O0O0OOO0OO000O000 in OOO0OO0OO0O0O0O0O ['credits']['cast']]#line:520
    O000O0OO0OOO0OOO0 =[dict ((O0OO0OO0OO0000OOO ,OOOO0OO0OO0O0OO00 )for (O0OO0OO0OO0000OOO ,OOOO0OO0OO0O0OO00 )in OO000O000000OOO0O .iteritems ()if OOOO0OO0OO0O0OO00 )for OO000O000000OOO0O in O000O0OO0OOO0OOO0 ]#line:521
    OOOO000000O0OO0O0 =None #line:523
    O0O0000O0000O0O0O =OOO0OO0OO0O0O0O0O .get ('imdb_id',"")#line:524
    if O0O0000O0000O0O0O :#line:525
        OOOO000000O0OO0O0 =imdb_get_info (O0O0000O0000O0O0O )#line:527
        if OOOO000000O0OO0O0 :#line:528
            O00O000OOOOO0OOOO =OOOO000000O0OO0O0 ['rating']#line:529
            OOOO00O000O0OOOOO =OOOO000000O0OO0O0 ['votes']#line:530
        else :#line:533
            O00O000OOOOO0OOOO =round (OOO0OO0OO0O0O0O0O .get ('vote_average',0 ),1 )#line:534
            OOOO00O000O0OOOOO =OOO0OO0OO0O0O0O0O .get ('vote_count',0 )#line:535
            print ("IMDB query failed, defaulting to TMDB rating and votes")#line:536
    else :#line:538
        print ("Warning: TMDB movie '%s' had no IMDB id!"%OOOO0000O00O0O00O )#line:539
    OO00OOOOOOO0OO0O0 =(OOOO000000O0OO0O0 ['duration']if OOOO000000O0OO0O0 and 'duration'in OOOO000000O0OO0O0 else OOO0OO0OO0O0O0O0O .get ('runtime',0 ))*60 #line:541
    if OOO0OO0OO0O0O0O0O ['production_countries']:#line:542
        O0O000OOO000O0O0O =OOO0OO0OO0O0O0O0O ['production_countries'][0 ]["name"]#line:543
    else :#line:544
        O0O000OOO000O0O0O =OOO0OO0OO0O0O0O0O .get ('original_language',"")#line:545
    O0OOO0O000000OOOO ={'genre':OOOO00OOO0O0O00O0 ,'country':O0O000OOO000O0O0O ,'year':int (OOO0OO0OO0O0O0O0O .get ('release_date',"0")[:4 ]),'rating':O00O000OOOOO0OOOO ,'director':OOO000000OO000O0O ,'mpaa':O0OOOOOO0OO0OO0O0 ,'plot':OOO0OO0OO0O0O0O0O .get ('overview',""),'originaltitle':OOO0OO0OO0O0O0O0O .get ('original_title',""),'duration':OO00OOOOOOO0OO0O0 ,'studio':O0OOO00O0OOOOO00O ,'writer':O0OOOOO0O0O0O00O0 ,'premiered':OOO0OO0OO0O0O0O0O .get ('release_date',""),'set':O00OOO0OOO0OOO0OO .get ("name")if O00OOO0OOO0OOO0OO else "",'setid':O00OOO0OOO0OOO0OO .get ("id")if O00OOO0OOO0OOO0OO else "",'imdbnumber':O0O0000O0000O0O0O ,'votes':OOOO00O000O0OOOOO ,'dateadded':time .strftime ("%Y-%m-%d %H:%M:%S"),'trailer':OOOOOO000OOO000O0 }#line:564
    O0OOO0O000000OOOO =dict ((O00000O00OOOOOOOO ,O0O0O000OOO00O00O )for (O00000O00OOOOOOOO ,O0O0O000OOO00O00O )in O0OOO0O000000OOOO .iteritems ()if O0O0O000OOO00O00O )#line:565
    OO0000O000OO0O0OO ={'video_id':'','thumb':"https://image.tmdb.org/t/p/original/%s"%OOO0OO0OO0O0O0O0O .get ('poster_path'),'fanart':"https://image.tmdb.org/t/p/original/%s"%OOO0OO0OO0O0O0O0O .get ('backdrop_path'),'video_info':O0OOO0O000000OOOO ,'actors':O000O0OO0OOO0OOO0 ,'stream_info':''}#line:574
    return (O0OOO0O000000OOOO )#line:580
def get_params ():#line:581
        O0OOO0000OO0OO0O0 =[]#line:582
        if len (sys .argv )>=2 :#line:583
          O000O00O0OO0000O0 =sys .argv [2 ]#line:585
          if len (O000O00O0OO0000O0 )>=2 :#line:587
                O00000OOO000OO00O =sys .argv [2 ]#line:588
                OOO0000OOO00OOO0O =O00000OOO000OO00O .replace ('?','')#line:589
                if (O00000OOO000OO00O [len (O00000OOO000OO00O )-1 ]=='/'):#line:590
                        O00000OOO000OO00O =O00000OOO000OO00O [0 :len (O00000OOO000OO00O )-2 ]#line:591
                O0OOOOO0O00000OOO =OOO0000OOO00OOO0O .split ('&')#line:592
                O0OOO0000OO0OO0O0 ={}#line:593
                for OO00OOO00000O0OOO in range (len (O0OOOOO0O00000OOO )):#line:595
                        O000O0O00OOO0OO00 ={}#line:596
                        O000O0O00OOO0OO00 =O0OOOOO0O00000OOO [OO00OOO00000O0OOO ].split ('=')#line:597
                        if (len (O000O0O00OOO0OO00 ))==2 :#line:598
                                O0OOO0000OO0OO0O0 [O000O0O00OOO0OO00 [0 ]]=O000O0O00OOO0OO00 [1 ]#line:599
        return O0OOO0000OO0OO0O0 #line:601
def addNolink (OOOO000O0OOOOO0OO ,OOO0OO0OOOO00O00O ,O0O000O0O00OOOOO0 ,OOOOO000OOO000OO0 ,iconimage ="DefaultFolder.png",fanart ="DefaultFolder.png"):#line:604
          iconimage =iconimage .strip ().replace("http://image.tmdb.org", "https://image.tmdb.org")
          fanart =fanart .strip ().replace("http://image.tmdb.org", "https://image.tmdb.org")
          OOOO000O0OOOOO0OO ='[COLOR pink][I]'+OOOO000O0OOOOO0OO +'[/I][/COLOR]'#line:608
          O00OOO0O000O0O0O0 =sys .argv [0 ]+"?url="+que (OOO0OO0OOOO00O00O )+"&mode="+str (O0O000O0O00OOOOO0 )+"&name="+que (OOOO000O0OOOOO0OO )#line:609
          if KODI_VERSION<=18:
                O00O00O0OOOO0OOOO =xbmcgui .ListItem (OOOO000O0OOOOO0OO ,iconImage =iconimage ,thumbnailImage =iconimage )#line:626
          else:
                O00O00O0OOOO0OOOO =xbmcgui .ListItem (OOOO000O0OOOOO0OO)
            
          
          O00O00O0OOOO0OOOO .setInfo (type ="Video",infoLabels ={"Title":unque (OOOO000O0OOOOO0OO )})#line:612
          O00O00O0OOOO0OOOO .setProperty ("Fanart_Image",fanart )#line:613
          O00O00O0OOOO0OOOO .setProperty ("IsPlayable","false")#line:614
          xbmcplugin .addDirectoryItem (handle =int (sys .argv [1 ]),url =O00OOO0O000O0O0O0 ,listitem =O00O00O0OOOO0OOOO ,isFolder =OOOOO000OOO000OO0 )#line:616
def addDir3 (O00OO00OOOO0OO00O ,OOO0000O00O0OO0OO ,OOO0OOOO0000OO0O0 ,O0O0OOO00O0OO0OOO ,OO000000000OO0000 ,O00O00OOOO0O00OOO ,count =0 ,page ='',imdbid =' ',cat_level =' ',data =" ",plot =" ",selected_list =" ",lang ="eng"):#line:617
        data =data.replace("http://image.tmdb.org", "https://image.tmdb.org")
        O00OO00OOOO0OO00O =O00OO00OOOO0OO00O .replace ('%27',"'")#line:618
        O00O00OOOO0O00OOO =O00O00OOOO0O00OOO .replace ('%27',"'")#line:619
        O0O0OOO00O0OO0OOO =O0O0OOO00O0OO0OOO .strip ().replace("http://image.tmdb.org", "https://image.tmdb.org")
        OO000000000OO0000 =OO000000000OO0000 .strip ().replace("http://image.tmdb.org", "https://image.tmdb.org")
        O00OOO00000O00OOO =sys .argv [0 ]+"?url="+que (OOO0000O00O0OO0OO )+"&mode="+str (OOO0OOOO0000OO0O0 )+"&name="+que (O00OO00OOOO0OO00O )+"&iconimage="+que (O0O0OOO00O0OO0OOO )+"&fanart="+que (OO000000000OO0000 )+"&description="+que (O00O00OOOO0O00OOO )+"&count="+str (count )+"&page="+str (page )+"&cat_level="+str (cat_level )+"&index_depth="+str (index_depth )+"&selected_list="+str (selected_list )+"&lang="+str (lang )#line:623
        O0000000OO00OOO0O =True #line:625
        if KODI_VERSION<=18:
            O0O00OOOO000OO00O =xbmcgui .ListItem (O00OO00OOOO0OO00O ,iconImage =O0O0OOO00O0OO0OOO ,thumbnailImage =O0O0OOO00O0OO0OOO )#line:626
        else:
            O0O00OOOO000OO00O =xbmcgui .ListItem (O00OO00OOOO0OO00O)
        O0O00OOOO000OO00O .setProperty ("Fanart_Image",OO000000000OO0000 )#line:628
        if data !=" ":#line:630
            OO00000O000OO00OO =json .loads (data .replace ('[',' ').replace (']',' ').replace ('	','').replace ("\\"," ").replace (': """",',': "" "",').replace (': """"}',': "" ""}').replace (': "",',': " ",').replace (': ""}',': " "}').replace ('""','"').replace ('\n','').replace ('\r',''))#line:633
            OO00000O000OO00OO ['title']=OO00000O000OO00OO ['title'].replace ('%27',"'")#line:634
            OO00000O000OO00OO ['plot']=OO00000O000OO00OO ['plot'].replace ('%27',"'")#line:635
            if "poster"in OO00000O000OO00OO :#line:636
              OO00000O000OO00OO ["poster"] = OO00000O000OO00OO ["poster"] .strip ().replace("http://image.tmdb.org", "https://image.tmdb.org")
              OO00000O000OO00OO ["banner"]=OO00000O000OO00OO ["poster"]#line:637
            else :#line:638
              OO00000O000OO00OO ["banner"]=OO000000000OO0000 #line:639
            if "duration"in OO00000O000OO00OO :#line:640
              OO00000O000OO00OO ["duration"]=int (OO00000O000OO00OO ["duration"])*60 #line:641
            if 'trailer'in OO00000O000OO00OO :#line:642
               OO00000O000OO00OO ['trailer']="plugin://plugin.video.youtube?&action=play_video&videoid=%s"%OO00000O000OO00OO ['trailer']#line:643
            if "mediatype"in OO00000O000OO00OO :#line:644
              if OO00000O000OO00OO ['mediatype']=='tv':#line:645
                 OO00000O000OO00OO ['mediatype']='tvshow'#line:646
            if "icon"not in OO00000O000OO00OO :#line:648
              OO00000O000OO00OO ['icon']=O0O0OOO00O0OO0OOO #line:650
            else :#line:651
               if 'http'not in (OO00000O000OO00OO ['icon']):#line:652
                    logging .warning ('not in')#line:653
                    OO00000O000OO00OO ['icon']=O0O0OOO00O0OO0OOO #line:654
            if 'writers'in OO00000O000OO00OO :#line:655
              OO00000O000OO00OO ['writer']=OO00000O000OO00OO ['writers']#line:656
            if 'directors'in OO00000O000OO00OO :#line:657
              OO00000O000OO00OO ['director']=OO00000O000OO00OO ['directors']#line:658
            if 'originaltitle'in OO00000O000OO00OO and 'title'not in OO00000O000OO00OO :#line:659
              OO00000O000OO00OO ['title']=OO00000O000OO00OO ['originaltitle'].replace ('%27',"'")#line:660
            if 'imdbnumber'in OO00000O000OO00OO and 'code'not in OO00000O000OO00OO :#line:661
              OO00000O000OO00OO ['code']=OO00000O000OO00OO ['imdbnumber']#line:662
              OO00000O000OO00OO ['imdb']=OO00000O000OO00OO ['imdbnumber']#line:663
            if "poster"not in OO00000O000OO00OO :#line:664
              OO00000O000OO00OO ['poster']=O0O0OOO00O0OO0OOO #line:665
            else :#line:666
              if 'http'not in OO00000O000OO00OO ['poster']:#line:667
                OO00000O000OO00OO ['poster']=O0O0OOO00O0OO0OOO #line:668
            if len (OO00000O000OO00OO ['plot'])<20 :#line:669
                OO00000O000OO00OO ['plot']=O00O00OOOO0O00OOO .replace ('%27',"'")#line:670
            O0O00OOOO000OO00O .setInfo ('video',OO00000O000OO00OO )#line:671
            O0O0O000OOO000000 ={}#line:674
            O0O0O000OOO000000 .update ({'poster':OO00000O000OO00OO ['poster']})#line:675
            O0O00OOOO000OO00O .setArt (O0O0O000OOO000000 )#line:676
        else :#line:677
            O0O00OOOO000OO00O .setInfo (type ="Video",infoLabels ={"Title":O00OO00OOOO0OO00O ,"Plot":O00O00OOOO0O00OOO })#line:678
        OO00OO0O00OO0000O =[]#line:679
        OO00OO0O00OO0000O .append (("[COLOR purple][I]Save STRM[/I][/COLOR]",'PlayMedia(%s?url=%s&mode=17&name=%s&description=%s&data=%s&index_depth=%s&lang=%s&cat_level=%s)'%(sys .argv [0 ],que (OOO0000O00O0OO0OO ),que (O00OO00OOOO0OO00O ),que (O00O00OOOO0O00OOO ),que (data ),str (index_depth ),str (lang ),cat_level )))#line:681
        O0O00OOOO000OO00O .addContextMenuItems (OO00OO0O00OO0000O ,replaceItems =False )#line:682
        
        if 'PlayMedia('in OOO0000O00O0OO0OO or 'plugin' in OOO0000O00O0OO0OO.lower():#line:767
            folder=False
        else:
            folder=True
        return O00OOO00000O00OOO ,O0O00OOOO000OO00O ,folder #line:683
        
        O0000000OO00OOO0O =xbmcplugin .addDirectoryItem (handle =int (sys .argv [1 ]),url =O00OOO00000O00OOO ,listitem =O0O00OOOO000OO00O ,isFolder =True )#line:684
        return O0000000OO00OOO0O #line:686
def addLink2 (OO00OOO0O000O00O0 ,O00OOOOO0000O0O0O ,OO00OOOO0O0OOOOOO ,O0O00O000OOOOOOO0 ,iconimage ="DefaultFolder.png",fanart ="DefaultFolder.png",description ='',imdbid =' ',year =' ',data =" ",index_depth =0 ):#line:689
        iconimage =iconimage .strip ().replace("http://image.tmdb.org", "https://image.tmdb.org")
        OOO00OO0O0OOOOO0O =xbmcgui .ListItem (OO00OOO0O000O00O0 ,iconImage =iconimage ,thumbnailImage =iconimage )#line:690
        OOO00OO0O0OOOOO0O .setInfo (type ="Video",infoLabels ={"Title":unque (OO00OOO0O000O00O0 ),"Duration":time ,"Plot":unque (description )})#line:691
        OOO00OO0O0OOOOO0O .setProperty ("Fanart_Image",iconimage )#line:692
        OOO000OO000O0OO00 =xbmcplugin .addDirectoryItem (handle =int (sys .argv [1 ]),url =O00OOOOO0000O0O0O ,listitem =OOO00OO0O0OOOOO0O )#line:693
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
                #logging.warning( '**ERROR utf8_urlencode ERROR** %s' % e )
    
    return enc(params).encode().decode('utf-8')
def addLink (OOO000000000OO000 ,OOOOO0OO0OO00OOO0 ,O0O0OOO000OOO0000 ,O00OO00000000OOOO ,iconimage ="DefaultFolder.png",fanart ="DefaultFolder.png",description ='',imdbid =' ',year =' ',data =" ",index_depth =0 ,lang ="eng",epg ='no'):#line:695
          data =data.replace("http://image.tmdb.org", "https://image.tmdb.org")
          OOO000000000OO000 =str(OOO000000000OO000) .replace ('%27',"'")#line:698
          description =str(description) .replace ('%27',"'")#line:699
          iconimage =str(iconimage) .strip ().replace("http://image.tmdb.org", "https://image.tmdb.org")
          fanart =str(fanart) .strip ().replace("http://image.tmdb.org", "https://image.tmdb.org")
          params={}
          params['name']=OOO000000000OO000
          params['iconimage']=iconimage
          params['fanart']=fanart
          params['description']=description
          params['url']=OOOOO0OO0OO00OOO0
 
          params['mode']=O0O0OOO000OOO0000
         
     
          params['data']=str(data) .replace ("&","and")
          params['index_depth']=index_depth
          params['lang']=lang
          
          all_ur=utf8_urlencode(params)

          OOO0OOO00O0OOOO00=sys.argv[0]+"?"+'&'+all_ur
          
          logging.warning(OOO000000000OO000)
          if KODI_VERSION<=18:
            OO000O0O000O0O000 =xbmcgui .ListItem (OOO000000000OO000 ,iconImage =iconimage ,thumbnailImage =iconimage )#line:705
          else:
            OO000O0O000O0O000 =xbmcgui .ListItem (OOO000000000OO000 )
          O0O00OOOOOOO00OOO =''#line:706
          if data !=" ":#line:708
            
            O0O00OOOOOOO00OOO =json .loads (data .replace ('[',' ').replace (']',' ').replace ('	','').replace ("\\"," ").replace (': """",',': "" "",').replace (': """"}',': "" ""}').replace (': "",',': " ",').replace (': ""}',': " "}').replace ('""','"').replace ('\n','').replace ('\r',''))#line:710
            O0O00OOOOOOO00OOO ['title']=O0O00OOOOOOO00OOO ['title'].replace ('%27',"'")#line:711
            O0O00OOOOOOO00OOO ['plot']=O0O00OOOOOOO00OOO ['plot'].replace ('%27',"'")#line:712
            if "duration"in O0O00OOOOOOO00OOO :#line:713
              O0O00OOOOOOO00OOO ["duration"]=int (O0O00OOOOOOO00OOO ["duration"])*60 #line:714
            if "poster"in O0O00OOOOOOO00OOO :#line:715
              O0O00OOOOOOO00OOO ["poster"] = O0O00OOOOOOO00OOO ["poster"] .strip ().replace("http://image.tmdb.org", "https://image.tmdb.org")
              O0O00OOOOOOO00OOO ["banner"]=O0O00OOOOOOO00OOO ["poster"]#line:716
            else :#line:717
              O0O00OOOOOOO00OOO ["banner"]=fanart #line:718
            if 'trailer'in O0O00OOOOOOO00OOO :#line:719
               O0O00OOOOOOO00OOO ['trailer']="plugin://plugin.video.youtube?&action=play_video&videoid=%s"%O0O00OOOOOOO00OOO ['trailer']#line:720
            if "mediatype"in O0O00OOOOOOO00OOO :#line:721
             if O0O00OOOOOOO00OOO ['mediatype']=='tv':#line:722
               O0O00OOOOOOO00OOO ['mediatype']='tvshow'#line:723
            if "icon"not in O0O00OOOOOOO00OOO :#line:724
              O0O00OOOOOOO00OOO ['icon']=iconimage #line:725
            else :#line:726
              if 'http'not in O0O00OOOOOOO00OOO ['icon']:#line:727
                O0O00OOOOOOO00OOO ['icon']=iconimage #line:728
            if 'writers'in O0O00OOOOOOO00OOO :#line:729
              O0O00OOOOOOO00OOO ['writer']=O0O00OOOOOOO00OOO ['writers']#line:730
            if 'directors'in O0O00OOOOOOO00OOO :#line:731
              O0O00OOOOOOO00OOO ['director']=O0O00OOOOOOO00OOO ['directors']#line:732
            O0O00OOOOOOO00OOO ['title']=OOO000000000OO000 #line:733
            if 'originaltitle'in O0O00OOOOOOO00OOO and 'title'not in O0O00OOOOOOO00OOO :#line:734
              O0O00OOOOOOO00OOO ['title']=O0O00OOOOOOO00OOO ['originaltitle']#line:735
            if 'imdbnumber'in O0O00OOOOOOO00OOO and 'code'not in O0O00OOOOOOO00OOO :#line:736
              O0O00OOOOOOO00OOO ['code']=O0O00OOOOOOO00OOO ['imdbnumber']#line:737
              O0O00OOOOOOO00OOO ['imdb']=O0O00OOOOOOO00OOO ['imdbnumber']#line:738
            if "poster"not in O0O00OOOOOOO00OOO :#line:739
              O0O00OOOOOOO00OOO ['poster']=fanart #line:740
            else :#line:741
              if 'http'not in O0O00OOOOOOO00OOO ['poster']:#line:742
                O0O00OOOOOOO00OOO ['poster']=fanart #line:743
            OO0OO0OO00O000OO0 =sys .argv [0 ]#line:744
            if epg =='yes':#line:745
              O0O00OOOOOOO00OOO ['plot']=description .replace ('%27',"'")#line:746
            if 'imdbnumber'in O0O00OOOOOOO00OOO :#line:748
              if 'tt'in O0O00OOOOOOO00OOO ['imdbnumber']:#line:749
                OOOOO0O0O00O0OO00 =[]#line:750
                if nanscarper ==True :#line:751
                  OOOOO0O0O00O0OO00 .append (("[COLOR aqua][I]מקורות נוספים[/I][/COLOR]",'PlayMedia(%s?mode=%s&name=%s&url=%s&data=%s)'%(OO0OO0OO00O000OO0 ,3 ,que (OOO000000000OO000 )," ",que (data .replace ("&","and")))))#line:752
                OOOOO0O0O00O0OO00 .append (("[COLOR purple][I]Save STRM[/I][/COLOR]",'PlayMedia(%s?url=%s&mode=16&name=%s&description=%s&data=%s&index_depth=%s&lang=%s)'%(OO0OO0OO00O000OO0 ,que (OOOOO0OO0OO00OOO0 ),que (OOO000000000OO000 ),que (description ),que (data ),str (index_depth ),str (lang ))))#line:753
                OO000O0O000O0O000 .addContextMenuItems (OOOOO0O0O00O0OO00 ,replaceItems =False )#line:754
            if 'ערוץ'in OOO000000000OO000 :#line:755
                OO000O0O000O0O000 .setProperty ('ResumeTime','0')#line:756
                OO000O0O000O0O000 .setProperty ('TotalTime','1')#line:757
            OO000O0O000O0O000 .setInfo (type ='Video',infoLabels =(O0O00OOOOOOO00OOO ))#line:758
            O00OOO00000000O00 ={}#line:759
            O00OOO00000000O00 .update ({'poster':O0O00OOOOOOO00OOO ['icon']})#line:760
            OO000O0O000O0O000 .setArt (O00OOO00000000O00 )#line:761
          else :#line:762
            OO000O0O000O0O000 .setInfo (type ="Video",infoLabels ={"Title":unque (OOO000000000OO000 ),"Year":year ,"Plot":description })#line:763
          OO000O0O000O0O000 .setProperty ("poster",iconimage )#line:766
          try:
            new=run_dds (OOOOO0OO0OO00OOO0)
          except:
            new=OOOOO0OO0OO00OOO0
          
          if 'PlayMedia('in new or 'plugin' in new.lower():#line:767
            OO000O0O000O0O000 .setProperty ("IsPlayable","false")#line:768
            O00OO00000000OOOO=False
          else :#line:769
            
            OO000O0O000O0O000 .setProperty ("IsPlayable","true")#line:770
          OO000O0O000O0O000 .setProperty ("Fanart_Image",fanart )#line:771
          art = {}
          art.update({'poster': iconimage})
          OO000O0O000O0O000.setArt(art)
        
          return OOO0OOO00O0OOOO00 ,OO000O0O000O0O000 ,O00OO00000000OOOO #line:772
          
          xbmcplugin .addDirectoryItem (handle =int (sys .argv [1 ]),url =OOO0OOO00O0OOOO00 ,listitem =OO000O0O000O0O000 ,isFolder =O00OO00000000OOOO )#line:773
def read_cookie_html (O0000O0OO0O0000OO ):#line:775
    import cookielib #line:776
    import urllib2 #line:777
    OO00OOO0OOOOOOO00 =''#line:778
    O0O00OO00OO0OOO00 =cookielib .LWPCookieJar ()#line:779
    O0O00OO00O00OOOO0 =[urllib2 .HTTPHandler (),urllib2 .HTTPSHandler (),urllib2 .HTTPCookieProcessor (O0O00OO00OO0OOO00 )]#line:784
    O00O000O0O0O0O00O =urllib2 .build_opener (*O0O00OO00O00OOOO0 )#line:785
    OOO0O0O0OOO000O00 =urllib2 .Request (O0000O0OO0O0000OO )#line:786
    OOO0O0O0OOO000O00 .add_header ('User-agent',__USERAGENT__ )#line:787
    OO0OO0OO0OO00000O =O00O000O0O0O0O00O .open (OOO0O0O0OOO000O00 )#line:788
    return O0O00OO00OO0OOO00 #line:791
def read_site_html (OO0O0OOO0O000O0OO ):#line:792
    import cookielib #line:794
    import urllib2 #line:795
    O0O0O0O0O0000O00O =''#line:796
    OO00O00OO0000OOO0 =cookielib .LWPCookieJar ()#line:797
    OOOOO0OO0OO00OOOO =[urllib2 .HTTPHandler (),urllib2 .HTTPSHandler (),urllib2 .HTTPCookieProcessor (OO00O00OO0000OOO0 )]#line:802
    O000000OOOO0000O0 =urllib2 .build_opener (*OOOOO0OO0OO00OOOO )#line:803
    OO00O0OO00OOO00OO =urllib2 .Request (OO0O0OOO0O000O0OO )#line:804
    OO00O0OO00OOO00OO .add_header ('User-agent',__USERAGENT__ )#line:805
    O0O0O00OO0OO00O00 =O000000OOOO0000O0 .open (OO00O0OO00OOO00OO )#line:806
    for OO0OO0O00OO0O0OOO in OO00O00OO0000OOO0 :#line:807
        if OO0OO0O00OO0O0OOO .name =='DRIVE_STREAM':#line:808
          O0O0O0O0O0000O00O =OO0OO0O00OO0O0OOO .value #line:809
    return O0O0O00OO0OO00O00 .read (),O0O0O0O0O0000O00O #line:811
def read_site_html2 (O0O0O0000O00OO000 ):#line:812
    O0000O0O0OO00O00O =urllib2 .Request (O0O0O0000O00OO000 )#line:814
    O0000O0O0OO00O00O .add_header ('User-agent',__USERAGENT__ )#line:815
    OO000O0OO0OO00OO0 =urllib2 .urlopen (O0000O0O0OO00O00O ).read ()#line:816
    return OO000O0OO0OO00OO0 #line:817
def read_old_paste (OOO0000000OO00OOO ,OOO0OO00OO00O0O00 ):#line:818
  if OOO0OO00OO00O0O00 ==0 :#line:819
   OO000O00O0O00O0OO ='<category>\n'#line:820
  else :#line:821
   OO000O00O0O00O0OO ='<category-%s>\n'%OOO0OO00OO00O0O00 #line:822
  OO000O00O0O00O0OO =OO000O00O0O00O0OO +'<category_name>name="%s List"&icon=" "&fanart=" "</category_name>\n'%c_addon_name #line:823
  O000O0O0OOO0OOO00 =re .compile ('^#EXTINF:(.*?)",(.*?)$\n^(.*?)$',re .I +re .M +re .U +re .S ).findall (OOO0000000OO00OOO )#line:824
  for O0O0O0OOO0O0O0000 ,O00000O00000O0000 ,OOOOOOO00OOOOO00O in O000O0O0OOO0OOO00 :#line:826
    OOOOO0O0000OO000O =' tvg-log.+?"(.+?)"'#line:829
    O0OOOO0OO00OOO000 =re .compile (OOOOO0O0000OO000O ).findall (O0O0O0OOO0O0O0000 )#line:830
    if len (O0OOOO0OO00OOO000 )>0 :#line:831
     OOO0OO00OO0OOO00O =O0OOOO0OO00OOO000 [0 ].replace ('"','')#line:832
    else :#line:833
      OOO0OO00OO0OOO00O =' '#line:834
    if len (OOO0OO00OO0OOO00O )==0 :#line:835
      OOO0OO00OO0OOO00O =' '#line:836
    OO000O00O0O00O0OO =OO000O00O0O00O0OO +'<item>name="%s"&link="%s"&icon="%s"&fanart="%s"&plot=" "</item>\n'%(O00000O00000O0000 ,OOOOOOO00OOOOO00O ,OOO0OO00OO0OOO00O ,OOO0OO00OO0OOO00O )#line:838
  if OOO0OO00OO00O0O00 ==0 :#line:839
    OO000O00O0O00O0OO =OO000O00O0O00O0OO +'</category>'#line:840
  else :#line:841
    OO000O00O0O00O0OO =OO000O00O0O00O0OO +'</category-%s>\n'%OOO0OO00OO00O0O00 #line:842
  return OO000O00O0O00O0OO #line:844
def read_sub_old_paste (O0OOOOO000O0OO0OO ):#line:846
  O000OOOO00O0000OO =''#line:848
  O0OO0000000O0O00O =re .compile ('^#EXTINF:-?[0-9]*(.*?),(.*?)\n(.*?)$',re .I +re .M +re .U +re .S ).findall (O0OOOOO000O0OO0OO )#line:849
  for O0OO000OOOO00000O ,OOO000O0O00OO00O0 ,O0O0000O0OOOOO000 in O0OO0000000O0O00O :#line:850
    if 'tvg-logo'in O0OO000OOOO00000O :#line:852
     O0000O0OO000OO0OO =' tvg-logo=(.+?)"'#line:853
     O00O00O0O0000OOO0 =re .compile (O0000O0OO000OO0OO ).findall (O0OO000OOOO00000O )#line:854
     O0O00OO00O0O0OOOO =O00O00O0O0000OOO0 [0 ].replace ('"','')#line:856
    else :#line:857
      O0O00OO00O0O0OOOO =' '#line:858
    if len (O0O00OO00O0O0OOOO )==0 :#line:859
      O0O00OO00O0O0OOOO =' '#line:860
    O000OOOO00O0000OO =O000OOOO00O0000OO +'<item>name="%s"&link="%s"&icon="%s"&fanart=" "&plot=" "</item>\n'%(OOO000O0O00OO00O0 ,O0O0000O0OOOOO000 ,O0O00OO00O0O0OOOO )#line:861
  return O000OOOO00O0000OO #line:864
def main_menu ():#line:868
    global dbcur
    dbcur .execute ("SELECT * FROM MyTable where father=''")#line:871
    
    O0OOOO0OOOOOO0000 =[]#line:872
    O0OOO0OO0OO0O0000 =dbcur .fetchall ()#line:873
    if len (O0OOO0OO0OO0O0000 )==1 :#line:874
        OO0OOO0OOO0OOO0O0 ,OO0O00OOOOO00O0OO ,O0OO0O0000O00O000 ,OO000O000O0OOOOO0 ,OOOOO0OO0O00OO00O ,O0OOO0OO0O0OOO0O0 ,OO0000O0O000000O0 ,O0OOOO0O00O0000OO ,O000OOOO0OOOOOOOO ,OOOO0O000OO0000OO ,OOO0O0OOOOO00O000 ,O00OOOO00O00O00O0 =O0OOO0OO0OO0O0000 [0 ]#line:875
        dbcur .execute ("SELECT * FROM MyTable where father='%s'"%OO0O00OOOOO00O0OO )#line:876
        O0OOOO0OOOOOO0000 =[]#line:877
        O0OOO0OO0OO0O0000 =dbcur .fetchall ()#line:878
    for OO0OOO0OOO0OOO0O0 ,OO0O00OOOOO00O0OO ,O0OO0O0000O00O000 ,OO000O000O0OOOOO0 ,OOOOO0OO0O00OO00O ,O0OOO0OO0O0OOO0O0 ,OO0000O0O000000O0 ,O0OOOO0O00O0000OO ,O000OOOO0OOOOOOOO ,OOOO0O000OO0000OO ,OOO0O0OOOOO00O000 ,O00OOOO00O00O00O0 in O0OOO0OO0OO0O0000 :#line:879
      if KODI_VERSION>18:
          OO0O00OOOOO00O0OO =OO0O00OOOOO00O0OO 
          O0OO0O0000O00O000 =O0OO0O0000O00O000 
          OO000O000O0OOOOO0 =OO000O000O0OOOOO0 
          OOOOO0OO0O00OO00O =OOOOO0OO0O00OO00O 
          O0OOO0OO0O0OOO0O0 =O0OOO0OO0O0OOO0O0 
          OO0000O0O000000O0 =OO0000O0O000000O0 
          O0OOOO0O00O0000OO =O0OOOO0O00O0000OO 
          O000OOOO0OOOOOOOO =O000OOOO0OOOOOOOO 
          OOOO0O000OO0000OO =OOOO0O000OO0000OO 
          OOO0O0OOOOO00O000 =OOO0O0OOOOO00O000 
          O00OOOO00O00O00O0 =O00OOOO00O00O00O0 
      else:
          OO0O00OOOOO00O0OO =OO0O00OOOOO00O0OO.encode('utf-8')
          O0OO0O0000O00O000 =O0OO0O0000O00O000 .encode('utf-8')
          OO000O000O0OOOOO0 =OO000O000O0OOOOO0 .encode('utf-8')
          OOOOO0OO0O00OO00O =OOOOO0OO0O00OO00O .encode('utf-8')
          O0OOO0OO0O0OOO0O0 =O0OOO0OO0O0OOO0O0 .encode('utf-8')
          OO0000O0O000000O0 =OO0000O0O000000O0 .encode('utf-8')
          O0OOOO0O00O0000OO =O0OOOO0O00O0000OO .encode('utf-8')
          O000OOOO0OOOOOOOO =O000OOOO0OOOOOOOO .encode('utf-8')
          OOOO0O000OO0000OO =OOOO0O000OO0000OO .encode('utf-8')
          OOO0O0OOOOO00O000 =OOO0O0OOOOO00O000 .encode('utf-8')
          O00OOOO00O00O00O0 =O00OOOO00O00O00O0 .encode('utf-8')
      if 'ערוץ' in OO0O00OOOOO00O0OO and "@" not in OO0O00OOOOO00O0OO :#line:891
        continue #line:892
      if O00OOOO00O00O00O0 =='category':#line:894
            if 'ערוץ'in OO0O00OOOOO00O0OO and "@"not in OO0O00OOOOO00O0OO :#line:895
                continue #line:896
            if 'ערוץ'in OO0O00OOOOO00O0OO :#line:897
                O0OOOO0OOOOOO0000 .append (addLink (OO0O00OOOOO00O0OO .replace ('@',''),OO0O00OOOOO00O0OO ,14 ,False ,OO000O000O0OOOOO0 ,OOOOO0OO0O00OO00O ,O0OOO0OO0O0OOO0O0 ,data =OO0000O0O000000O0 .replace ("OriginalTitle","originaltitle")))#line:898
            else :#line:899
                O0OOOO0OOOOOO0000 .append (addDir3 (OO0O00OOOOO00O0OO ,OO0O00OOOOO00O0OO ,5 ,OO000O000O0OOOOO0 ,OOOOO0OO0O00OO00O ,O0OOO0OO0O0OOO0O0 ,data =OO0000O0O000000O0 .replace ("OriginalTitle","Originaltitle")))#line:900
      else :#line:901
               O0OOOO0OOOOOO0000 .append (addLink (OO0O00OOOOO00O0OO ,O0OO0O0000O00O000 ,3 ,False ,OO000O000O0OOOOO0 ,OOOOO0OO0O00OO00O ,O0OOO0OO0O0OOO0O0 ,data =OO0000O0O000000O0 .replace ("OriginalTitle","originaltitle")))#line:902
    O0OOOO0OOOOOO0000 .append  (addDir3 ('[B][COLOR burlywood]חי[/COLOR][/B][B][COLOR aqua]פוש[/COLOR][/B]','movie',6 ,'http://ngarba.xyz/adds/yos/8.jpg','http://b2acpa.com/~bairdcpa/images/Terminator.jpg','',lang =lang ))#line:907
    if cat_cat :#line:908
        O0OOOO0OOOOOO0000 .append (addDir3 ('[B][COLOR burlywood]קטגו[/COLOR][/B][B][COLOR aqua]ריות[/COLOR][/B]','cat',11 ,cat_images [0 ],cat_images [1 ],'',lang =lang ))#line:909
    if year_cat :#line:910
        O0OOOO0OOOOOO0000 .append (addDir3 ('[B][COLOR burlywood]-שנים [/COLOR][/B][B][COLOR aqua]לפי- [/COLOR][/B]','year',11 ,year_img [0 ],year_img [1 ],'',lang =lang ))#line:911
    if a_b_cat :#line:912
        O0OOOO0OOOOOO0000 .append (addDir3 ('[B][COLOR burlywood]-א-ב [/COLOR][/B][B][COLOR aqua]לפי- [/COLOR][/B]','aleph',11 ,letter_img [0 ],letter_img [1 ],'',lang =lang ))#line:913
    if ranking_cat :#line:914
        O0OOOO0OOOOOO0000 .append (addDir3 ('[B][COLOR burlywood]-דירוג [/COLOR][/B][B][COLOR aqua]לפי- [/COLOR][/B]','rating',11 ,ratin_img [0 ],ratin_img [1 ],'',lang =lang))#line:915
    if all_m_cat :#line:916
        logging .warning (all_img )#line:917
        O0OOOO0OOOOOO0000 .append (addDir3 ('[B][COLOR burlywood]-הסרטים [/COLOR][/B][B][COLOR aqua]כל- [/COLOR][/B]','all',12 ,all_img [0 ],all_img [1 ],'',lang =lang ))#line:918
    if cat_chan :#line:919
        O0OOOO0OOOOOO0000 .append (addDir3 ('[B][COLOR burlywood]-הערוצים [/COLOR][/B][B][COLOR aqua]כל- [/COLOR][/B]','tv',13 ,tv_images [0 ],tv_images [1 ],'',lang =lang ))#line:920
    if add_res :#line:921
       O0OOOO0OOOOOO0000 .append (addDir3 ('[B][COLOR burlywood]סרטים [/COLOR][/B][B][COLOR aqua]אחרונים[/COLOR][/B]','movie',18 ,'http://ngarba.xyz/adds/yos/16.jpg','http://sf.co.ua/12/09/wallpaper-2230830.jpg','',lang =lang ))#line:922
       if Addon .getSetting ("last_ep")=='true':#line:923
        O0OOOO0OOOOOO0000 .append (addDir3 ('[B][COLOR burlywood]פרקים [/COLOR][/B][B][COLOR aqua]אחרונים[/COLOR][/B]','tv',18 ,'http://ngarba.xyz/adds/yos/24.jpg','https://images.hdqwalls.com/download/assassins-creed-valhalla-female-eivor-axe-8k-bn-1920x1080.jpg','',lang =lang ))#line:924
    xbmcplugin .addDirectoryItems (int (sys .argv [1 ]),O0OOOO0OOOOOO0000 ,len (O0OOOO0OOOOOO0000 ))#line:925
    #addNolink ('[B][COLOR burlywood]-קישור [/COLOR][/B][B][COLOR aqua]הרץ- [/COLOR][/B]','www',19 ,False ,iconimage ="https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/91/2a/f6/912af665-90ac-5cc9-b988-5e3b023f867c/source/512x512bb.jpg",fanart ="https://wallpaperplay.com/walls/full/7/8/a/86954.jpg")#line:926
#line:926.1
    addNolink ('[B][COLOR burlywood]ניקוי [/COLOR][/B][B][COLOR aqua]קאש[/COLOR][/B]','www',99 ,False ,iconimage ="http://ngarba.xyz/adds/yos/6.jpg",fanart ="http://www.wallpapermaiden.com/image/2017/02/14/green-lantern-ray-reynolds-mask-movies-13335.jpg")#line:926.3
ACTION_PREVIOUS_MENU =10 #line:927
ACTION_NAV_BACK =92 #line:928
def TextBox (OOO00OOO0O000O000 ,O0O0O0O0000O0OOO0 ):#line:929
	class O0O0O0OOOO00OOOO0 (xbmcgui .WindowXMLDialog ):#line:930
		def onInit (O00OOO0OOO0OOOOOO ):#line:931
			O00OOO0OOO0OOOOOO .title =101 #line:932
			O00OOO0OOO0OOOOOO .msg =102 #line:933
			O00OOO0OOO0OOOOOO .scrollbar =103 #line:934
			O00OOO0OOO0OOOOOO .okbutton =201 #line:935
			O00OOO0OOO0OOOOOO .y =0 #line:936
			O00OOO0OOO0OOOOOO .showdialog ()#line:937
		def showdialog (O0000O00OO0000O0O ):#line:939
			O0000O00OO0000O0O .getControl (O0000O00OO0000O0O .title ).setLabel (OOO00OOO0O000O000 )#line:940
			O0000O00OO0000O0O .getControl (O0000O00OO0000O0O .msg ).setText (O0O0O0O0000O0OOO0 )#line:941
			O0000O00OO0000O0O .setFocusId (O0000O00OO0000O0O .okbutton )#line:942
		def onClick (OO00OOO000OO0O0OO ,O00OOOO00OO0O000O ):#line:944
			if (O00OOOO00OO0O000O ==OO00OOO000OO0O0OO .okbutton ):#line:945
				OO00OOO000OO0O0OO .close ()#line:946
		def onAction (OOO00O00OO0O000O0 ,O0OOO000OO000O00O ):#line:948
			if O0OOO000OO000O00O ==ACTION_PREVIOUS_MENU :OOO00O00OO0O000O0 .close ()#line:949
			elif O0OOO000OO000O00O ==ACTION_NAV_BACK :OOO00O00OO0O000O0 .close ()#line:950
	OOO0000OO00OO00O0 =O0O0O0OOOO00OOOO0 ("Textbox.xml",__settings__ .getAddonInfo ('path'),'DefaultSkin',title =OOO00OOO0O000O000 ,msg =O0O0O0O0000O0OOO0 )#line:953
	OOO0000OO00OO00O0 .doModal ()#line:954
	del OOO0000OO00OO00O0 #line:955
def fix_data (OOO00OO00000OOOOO ):#line:956
    return OOO00OO00000OOOOO .replace ('[',' ').replace (']',' ').replace ('	','').replace ("\\"," ").replace ("\n"," ").replace ("\r"," ").replace ("\t"," ")#line:957
def check_updted (OOOO0OO0O0O000OOO ):#line:958
    import datetime ,time #line:959
    import _strptime #line:960
    O0O0OOO0OOO0OO00O =[]#line:961
    OOOOO000OO0OO0OOO =[]#line:962
    O0OO00OOOOOOO0O0O =os .path .join (user_dataDir ,'database2.db')#line:963
    OO00O00OOOOO0OO00 =database .connect (O0OO00OOOOOOO0O0O )#line:964
    O0O00O0O0OOOOO000 =OO00O00OOOOO0OO00 .cursor ()#line:965
    O0O00O0O0OOOOO000 .execute ("CREATE TABLE IF NOT EXISTS news ( " "name TEXT," "link TEXT, " "data TEXT);")#line:968
    O0O00O0O0OOOOO000 .execute ("CREATE TABLE IF NOT EXISTS data ( " "name TEXT," "link TEXT, " "data TEXT );")#line:969
    O0OOOOO0000000000 ='https://'#line:970
    O0O00O0O0OOOOO000 .execute ("SELECT name FROM data")#line:972
    OOOOO0O00000O0O0O =O0O00O0O0OOOOO000 .fetchone ()#line:973
    OOOO000O0000O0O0O =0 #line:974
    logging .warning (len (OOOO0OO0O0O000OOO ))#line:975
    logging .warning (OOOOO0O00000O0O0O )#line:976
    try :#line:978
        if len (OOOO0OO0O0O000OOO )!=int (OOOOO0O00000O0O0O [0 ]):#line:980
            OOOO000O0000O0O0O =1 #line:981
            O0O00O0O0OOOOO000 .execute ("INSERT INTO data Values ('%s','%s','%s');"%(str (len (OOOO0OO0O0O000OOO )),'',''))#line:982
            OO00O00OOOOO0OO00 .commit ()#line:983
    except :#line:984
        OOOO000O0000O0O0O =1 #line:985
        O0O00O0O0OOOOO000 .execute ("DELETE FROM data")#line:986
        O0O00O0O0OOOOO000 .execute ("INSERT INTO data Values ('%s','%s','%s');"%(str (len (OOOO0OO0O0O000OOO )),'',''))#line:987
        OO00O00OOOOO0OO00 .commit ()#line:988
    OO00O00OOOOO0OO00 .commit ()#line:993
    logging .warning ('checking update')#line:995
    OO0O0000OO0O00O00 =''#line:1000
    O0OO0000000OOOOOO =[]#line:1001
    O0000O00O0OOO0OO0 =0 #line:1002
    O0OOOO00OO0OO00OO =''#line:1003
    if 1 :#line:1004
        O0O0O0O0O0O0O0OO0 =0 #line:1006
        OO00O0OOOOO00O0OO =0 #line:1008
        for OOO0000O0000O000O ,OO0O00OOO0O000O0O ,O0O000O0OOO0O0O00 ,O0OO00O00O00OO00O ,O0OOOO0O0O0O00O0O ,OO0OO00OOOOO00OOO ,OO000OOOO0OOO00O0 ,OO000O0O00OOO0OO0 ,OOO0O0OO0OO0000OO ,OOOO00O00OO000OOO ,O00OOOOOOO000O00O ,OOO0OOOO0000O0000 in OOOO0OO0O0O000OOO :#line:1009
            O0000O00O0OOO0OO0 =1 #line:1012
            O0000O00O0OOO0OO0 =2 #line:1014
            try :#line:1018
                if '{'in OO000OOOO0OOO00O0 :#line:1019
                  OO000OOOO0OOO00O0 =OO000OOOO0OOO00O0 .replace ('[',' ').replace (']',' ').replace ('	','').replace ("\\"," ").replace (': """",',': "" "",').replace (': """"}',': "" ""}').replace (': "",',': " ",').replace (': ""}',': " "}').replace ('""','"').replace ('\n','').replace ('\r','')#line:1020
                  OOOO0O0OO0O0O00OO =json .loads (OO000OOOO0OOO00O0 )#line:1021
                  O00O00O0OOO0OOOOO =OOOO0O0OO0O0O00OO ['dateadded']#line:1022
                  if OOOO0O0OO0O0O00OO ['mediatype']=='tv':#line:1023
                    OO0O00OOO0O000O0O =' - [COLOR yellow][I]'+OOOO0O0OO0O0O00OO ['originaltitle']+'[/I][/COLOR] - S'+str (OOOO0O0OO0O0O00OO ['Season'])+'E'+str (OOOO0O0OO0O0O00OO ['Episode'])#line:1024
                  try :#line:1025
                    O00O00O0OOO0OOOOO =time .strptime (OOOO0O0OO0O0O00OO ['dateadded'],"%Y-%m-%d %H:%M:%S")#line:1026
                  except :#line:1027
                    O00O00O0OOO0OOOOO =time .strptime ("2000-01-01 01:01:00","%Y-%m-%d %H:%M:%S")#line:1028
                  O0O0OOO0OOO0OO00O .append ((OO0O00OOO0O000O0O ,OOOO0O0OO0O0O00OO ['year'],O00O00O0OOO0OOOOO ))#line:1029
                  O00O0OO00000O00O0 =time .strftime ("%d-%m-%Y",O00O00O0OOO0OOOOO )#line:1030
                  if OO00O0OOOOO00O0OO <100 :#line:1032
                    if O00O0OO00000O00O0 !=O0OOOO00OO0OO00OO :#line:1033
                        OO0O0000OO0O00O00 =OO0O0000OO0O00O00 +'[COLOR aqua]'+'התווסף בתאריך -- '+O00O0OO00000O00O0 +'[/COLOR]\n'#line:1034
                    O0OOOO00OO0OO00OO =O00O0OO00000O00O0 #line:1035
                    OO0O0000OO0O00O00 =OO0O0000OO0O00O00 +OO0O00OOO0O000O0O +' ('+OOOO0O0OO0O0O00OO ['year']+') '+'\n'#line:1036
                  OO00O0OOOOO00O0OO +=1 #line:1037
                  if OOOO000O0000O0O0O ==1 :#line:1038
                      logging .warning ('1')#line:1039
            except Exception as OO0OO0OO0OO0OO0O0 :#line:1041
                logging .warning ('Error in whatsnew: '+str (OO0OO0OO0OO0OO0O0 ))#line:1042
                O0O0OOO0OOO0OO00O .append (('[COLOR red]'+OO0O00OOO0O000O0O +'[/COLOR]'+' - '+str (OO0OO0OO0OO0OO0O0 ),'0',time .strptime ('2000-01-01 01:01:00',"%Y-%m-%d %H:%M:%S")))#line:1043
            O0O0O0O0O0O0O0OO0 =O0O0O0O0O0O0O0OO0 +1 #line:1045
        O0000O00O0OOO0OO0 =3 #line:1047
        logging .warning ('checking update level 2')#line:1048
        O0000O00O0OOO0OO0 =4 #line:1055
        '''
        for name,year,added in whats_new:
          added=time.strftime("%d-%m-%Y",added)
          if added!=added_prev:
            wh_string=wh_string+'[COLOR aqua]'+'התווסף בתאריך -- '+added+'[/COLOR]\n'
            wh_string=wh_string+name+' ('+year+') '+'\n'
          else:
            wh_string=wh_string+name+' ('+year+') '+'\n'
          added_prev=added
        '''#line:1065
        O0000O00O0OOO0OO0 =5 #line:1066
        O0OOO0OO000O000OO =0 #line:1067
        logging .warning ('get mssg')#line:1068
        OOOOO0000O0O0O0OO =''#line:1069
        if msg_mast :#line:1070
            OO0OO00O00O000O0O ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-US,en;q=0.5','Content-Type':'application/x-www-form-urlencoded','Connection':'keep-alive','Upgrade-Insecure-Requests':'1',}#line:1081
            logging .warning ('get mssg1')#line:1082
            OOOOO0000O0O0O0OO =requests .get (msg_mast ,headers =OO0OO00O00O000O0O ).content #line:1083
            logging .warning ('get mssg2')#line:1084
            O0O00O0O0OOOOO000 .execute ("SELECT * FROM news")#line:1085
            OOOOO0O00000O0O0O =O0O00O0O0OOOOO000 .fetchone ()#line:1086
            O0OOO0OO000O000OO =0 #line:1087
            if OOOOO0O00000O0O0O ==None :#line:1088
                logging .warning ('NONONON')#line:1089
                O0O00O0O0OOOOO000 .execute ("INSERT INTO news Values ('%s','%s','%s');"%(OOOOO0000O0O0O0OO .replace ("'","%27"),'',''))#line:1090
                OO00O00OOOOO0OO00 .commit ()#line:1091
                O0OOO0OO000O000OO =1 #line:1093
            else :#line:1094
               OO0O00OOO0O000O0O ,OO0O0O0OOOOOO00O0 ,O0OOOO00OO0OOO00O =OOOOO0O00000O0O0O #line:1095
               if OO0O00OOO0O000O0O .replace ("%27","'")!=OOOOO0000O0O0O0OO :#line:1097
                logging .warning ('changed')#line:1098
                O0O00O0O0OOOOO000 .execute ("DELETE FROM news")#line:1099
                O0O00O0O0OOOOO000 .execute ("INSERT INTO news Values ('%s','%s','%s');"%(OOOOO0000O0O0O0OO .replace ("'","%27"),'',''))#line:1101
                OO00O00OOOOO0OO00 .commit ()#line:1102
                O0OOO0OO000O000OO =1 #line:1104
        logging .warning ('news')#line:1105
        logging .warning (OOOO000O0000O0O0O )#line:1106
        logging .warning (O0OOO0OO000O000OO )#line:1107
        if OOOO000O0000O0O0O >0 or O0OOO0OO000O000OO ==1 :#line:1110
          if Addon .getSetting ("new")=='true':#line:1112
             logging .warning ('in1')#line:1113
             if wh_new !='no':#line:1114
                logging .warning ('3')#line:1115
                OOO00O0OOOOOO00OO ='http://cache.desktopnexus.com/thumbseg/1647/1647926-bigthumbnail.jpg'#line:1116
                OOO000OO0OOOO000O =f_msg ("Contact2.xml",Addon .getAddonInfo ('path'),'DefaultSkin',title ='מה חדש',fanart =CONTACTFANART ,image =OOO00O0OOOOOO00OO ,msg =OO0O0000OO0O00O00 ,msg2 =OOOOO0000O0O0O0OO )#line:1117
                OOO000OO0OOOO000O .doModal ()#line:1118
                del OOO000OO0OOOO000O #line:1119
        logging .warning ('Clean')#line:1120
        OO00O00OOOOO0OO00 .close ()#line:1122
        logging .warning ('Done')#line:1123
def tv_channels ():#line:1130
    OO000O00O00O0OOOO =[]#line:1131
    dbcur .execute ("SELECT * FROM MyTable where name like '%ערוץ %'")#line:1132
    O000OOO0OO00O0O0O =xbmc .PlayList (xbmc .PLAYLIST_VIDEO )#line:1133
    O000OOO0OO00O0O0O .clear ()#line:1134
    OOOO00O0OOO0OO0O0 =0 #line:1135
    OOO0000OOO00O0000 =[]#line:1136
    OOOO0OOO00O000000 =xbmc .translatePath ("special://home/addons/")#line:1137
    OOOO00O00O0OOOOOO =Addon .getAddonInfo ('path').replace (OOOO0OOO00O000000 ,'')#line:1138
    O00O0O0OO000OOOOO =dbcur .fetchall ()#line:1139
    if len (O00O0O0OO000OOOOO )==0 :#line:1140
        xbmcgui .Dialog ().ok ("תוכן חסר","ערוץ זה יתווסף בהמשך")#line:1141
        return 0 #line:1142
    for OOOOO00000O00OOO0 ,O000OOO0OOOOO00O0 ,O00OO0OOOOO000O0O ,O00O000O00O0O000O ,O0O00O00O0OO0OO00 ,OO0O0OOOO0OO0OO0O ,O00OO000OO0O00OOO ,OOO0OOO000OOOO0OO ,O00000O0O000000OO ,OOOO000O0O0O0O000 ,OOO00OO0OOO00O0O0 ,OOOO0O0O000O00O00 in O00O0O0OO000OOOOO :#line:1143
        O000OOO0OOOOO00O0 =O000OOO0OOOOO00O0 .encode ('utf8')#line:1144
        O00OO0OOOOO000O0O =O00OO0OOOOO000O0O .encode ('utf8')#line:1145
        O00O000O00O0O000O =O00O000O00O0O000O .encode ('utf8')#line:1146
        O0O00O00O0OO0OO00 =O0O00O00O0OO0OO00 .encode ('utf8')#line:1147
        OO0O0OOOO0OO0OO0O =OO0O0OOOO0OO0OO0O .encode ('utf8')#line:1148
        O00OO000OO0O00OOO =O00OO000OO0O00OOO .encode ('utf8')#line:1149
        OOO0OOO000OOOO0OO =OOO0OOO000OOOO0OO .encode ('utf8')#line:1150
        O00000O0O000000OO =O00000O0O000000OO .encode ('utf8')#line:1151
        OOOO000O0O0O0O000 =OOOO000O0O0O0O000 .encode ('utf8')#line:1152
        OOO00OO0OOO00O0O0 =OOO00OO0OOO00O0O0 .encode ('utf8')#line:1153
        OOOO0O0O000O00O00 =OOOO0O0O000O00O00 .encode ('utf8')#line:1154
        if OOOO0O0O000O00O00 =='item':#line:1155
            OO000O00O00O0OOOO .append (addLink (O000OOO0OOOOO00O0 .replace ('@',''),O00OO0OOOOO000O0O ,3 ,False ,O00O000O00O0O000O ,O0O00O00O0OO0OO00 ,OO0O0OOOO0OO0OO0O ,data =O00OO000OO0O00OOO .replace ("OriginalTitle","originaltitle")))#line:1156
        else :#line:1157
            OO000O00O00O0OOOO .append (addLink (O000OOO0OOOOO00O0 .replace ('@',''),OOO00OO0OOO00O0O0 +O000OOO0OOOOO00O0 ,14 ,False ,O00O000O00O0O000O ,O0O00O00O0OO0OO00 ,OO0O0OOOO0OO0OO0O ,data =O00OO000OO0O00OOO .replace ("OriginalTitle","originaltitle")))#line:1158
    xbmcplugin .addDirectoryItems (int (sys .argv [1 ]),OO000O00O00O0OOOO ,len (OO000O00O00O0OOOO ))#line:1159
def play_tv (OO00000O0O0000O00 ):#line:1160
    dbcur .execute ("SELECT * FROM MyTable where father='%s'"%OO00000O0O0000O00 )#line:1161
    logging .warning ('nameeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')#line:1162
    logging .warning (OO00000O0O0000O00 )#line:1163
    OO000OOOO00O0O00O =xbmc .PlayList (xbmc .PLAYLIST_VIDEO )#line:1165
    OO000OOOO00O0O00O .clear ()#line:1166
    OOO0000OOO0OOO000 =0 #line:1167
    O0OO00O0O0OO00O0O =[]#line:1168
    O0O0OO0OO0O0000OO =xbmc .translatePath ("special://home/addons/")#line:1169
    O000O0OOOO0000O00 =Addon .getAddonInfo ('path').replace (O0O0OO0OO0O0000OO ,'')#line:1170
    O0O0OO0000OO0OOO0 =dbcur .fetchall ()#line:1171
    if len (O0O0OO0000OO0OOO0 )==0 :#line:1172
        xbmcgui .Dialog ().ok ("תוכן חסר","ערוץ זה יתווסף בהמשך")#line:1173
        return 0 #line:1174
    for O00OO0OO0OO0OO000 ,OO00000O0O0000O00 ,OO000O00O0O00O0O0 ,OO000OOOOO0OO0O00 ,O00OO0O00OOO00O0O ,O000O000O0000OOOO ,O00OOO000O00O00OO ,OOOO0O0O0O00OO00O ,O0O00000O00OO00OO ,O00OO00O00000OO00 ,O00OOO00OO000OO00 ,O000O00O0O00OOOOO in O0O0OO0000OO0OOO0 :#line:1175
        OO00000O0O0000O00 =OO00000O0O0000O00 .encode ('utf8').replace ('%27',"'")#line:1177
        OO000O00O0O00O0O0 =OO000O00O0O00O0O0 .encode ('utf8')#line:1178
        OO000OOOOO0OO0O00 =OO000OOOOO0OO0O00 .encode ('utf8')#line:1179
        O00OO0O00OOO00O0O =O00OO0O00OOO00O0O .encode ('utf8')#line:1180
        O000O000O0000OOOO =O000O000O0000OOOO .encode ('utf8').replace ('%27',"'")#line:1181
        OOOO0O0O0O00OO00O =OOOO0O0O0O00OO00O .encode ('utf8')#line:1183
        O0O00000O00OO00OO =O0O00000O00OO00OO .encode ('utf8')#line:1184
        O00OO00O00000OO00 =O00OO00O00000OO00 .encode ('utf8')#line:1185
        O00OOO00OO000OO00 =O00OOO00OO000OO00 .encode ('utf8')#line:1186
        O000O00O0O00OOOOO =O000O00O0O00OOOOO .encode ('utf8')#line:1187
        if '$$$'in OO000O00O0O00O0O0 :#line:1192
           OO000O00O0O00O0O0 =OO000O00O0O00O0O0 .split ('$$$')[0 ]#line:1193
        if len (O00OOO000O00O00OO )>2 :#line:1194
            O0O0000O0O00OOO0O =json .loads (O00OOO000O00O00OO .replace ('[',' ').replace (']',' ').replace ('	','').replace ("\\"," ").replace (': """",',': "" "",').replace (': """"}',': "" ""}').replace (': "",',': " ",').replace (': ""}',': " "}').replace ('""','"').replace ('\n','').replace ('\r',''))#line:1195
            if "duration"in O0O0000O0O00OOO0O :#line:1197
              O0O0000O0O00OOO0O ["duration"]=int (O0O0000O0O00OOO0O ["duration"])*60 #line:1198
            if "poster"in O0O0000O0O00OOO0O :#line:1199
              O0O0000O0O00OOO0O ["banner"]=O0O0000O0O00OOO0O ["poster"]#line:1200
            else :#line:1201
              O0O0000O0O00OOO0O ["banner"]=O00OO0O00OOO00O0O #line:1202
            if 'trailer'in O0O0000O0O00OOO0O :#line:1203
               O0O0000O0O00OOO0O ['trailer']="plugin://plugin.video.youtube?&action=play_video&videoid=%s"%O0O0000O0O00OOO0O ['trailer']#line:1204
            if "mediatype"in O0O0000O0O00OOO0O :#line:1205
             if O0O0000O0O00OOO0O ['mediatype']=='tv':#line:1206
               O0O0000O0O00OOO0O ['mediatype']='tvshow'#line:1207
            if "icon"not in O0O0000O0O00OOO0O :#line:1208
              O0O0000O0O00OOO0O ['icon']=iconimage #line:1209
            else :#line:1210
              if 'http'not in O0O0000O0O00OOO0O ['icon']:#line:1211
                O0O0000O0O00OOO0O ['icon']=iconimage #line:1212
            if 'writers'in O0O0000O0O00OOO0O :#line:1213
              O0O0000O0O00OOO0O ['writer']=O0O0000O0O00OOO0O ['writers']#line:1214
            if 'directors'in O0O0000O0O00OOO0O :#line:1215
              O0O0000O0O00OOO0O ['director']=O0O0000O0O00OOO0O ['directors']#line:1216
            O0O0000O0O00OOO0O ['title']=OO00000O0O0000O00 #line:1217
            if 'originaltitle'in O0O0000O0O00OOO0O and 'title'not in O0O0000O0O00OOO0O :#line:1218
              O0O0000O0O00OOO0O ['title']=O0O0000O0O00OOO0O ['originaltitle']#line:1219
            if 'imdbnumber'in O0O0000O0O00OOO0O and 'code'not in O0O0000O0O00OOO0O :#line:1220
              O0O0000O0O00OOO0O ['code']=O0O0000O0O00OOO0O ['imdbnumber']#line:1221
              O0O0000O0O00OOO0O ['imdb']=O0O0000O0O00OOO0O ['imdbnumber']#line:1222
            if "poster"not in O0O0000O0O00OOO0O :#line:1223
              O0O0000O0O00OOO0O ['poster']=O00OO0O00OOO00O0O #line:1224
            else :#line:1225
              if 'http'not in O0O0000O0O00OOO0O ['poster']:#line:1226
                O0O0000O0O00OOO0O ['poster']=O00OO0O00OOO00O0O #line:1227
            if link_enter :#line:1228
                O000O000O0000OOOO =O000O000O0000OOOO +'_pass_ok_'#line:1229
            O0OO0000OOOOOOO00 ='plugin://%s/?url=%s&mode=3&name=%s&description=%s&data=%s'%(O000O0OOOO0000O00 ,que (OO000O00O0O00O0O0 ),que (OO00000O0O0000O00 ),que (O000O000O0000OOOO ),que (json .dumps (O0O0000O0O00OOO0O )))#line:1230
            O0O0000O0O00OOO0O ['title']=O0O0000O0O00OOO0O ['title'].replace ('%27',"'")#line:1233
            O0O0000O0O00OOO0O ['plot']=O0O0000O0O00OOO0O ['plot'].replace ('%27',"'")#line:1234
        else :#line:1235
            O0O0000O0O00OOO0O ={}#line:1236
            O0O0000O0O00OOO0O ['title']=OO00000O0O0000O00 #line:1237
        OO000OOOO0O0OO00O =xbmcgui .ListItem (OO00000O0O0000O00 ,thumbnailImage =O00OO0O00OOO00O0O )#line:1239
        OO000OOOO0O0OO00O .setInfo ('video',O0O0000O0O00OOO0O )#line:1240
        O0OO00O0O0OO00O0O .append (OO000OOOO0O0OO00O )#line:1241
        OO000OOOO00O0O00O .add (url =O0OO0000OOOOOOO00 ,listitem =OO000OOOO0O0OO00O ,index =OOO0000OOO0OOO000 )#line:1242
        OOO0000OOO0OOO000 =OOO0000OOO0OOO000 +1 #line:1243
    OO000OOOO00O0O00O .shuffle ()#line:1244
    O0000OO00OO00O0O0 =random .choice (O0OO00O0O0OO00O0O )#line:1245
    xbmcplugin .setResolvedUrl (handle =int (sys .argv [1 ]),succeeded =True ,listitem =O0000OO00OO00O0O0 )#line:1247
def get_epg_plot2 (OO00OOO0OO0OO0O00 ,OO0000OOOOO0OO00O ):#line:1251
   OO000O00O0O0OO00O ='<img class="channelpic" src=".+?">(.+?)</a></h3>(.+?)</ul></li>'#line:1255
   O0O00O00O000OO00O =re .compile (OO000O00O0O0OO00O ,re .DOTALL ).findall (OO0000OOOOO0OO00O )#line:1256
   O00O00OOO00O00000 =''#line:1257
   for O0OOO0OOOOOOOO0O0 ,OOO0OOOO0O000OO0O in O0O00O00O000OO00O :#line:1259
      OOOO00O0OOOO00OO0 =OO00OOO0OO0OO0O00 .strip ().split (" ")#line:1260
      O0OO00O00OO000OOO =OOOO00O0OOOO00OO0 [0 ]+OOOO00O0OOOO00OO0 [1 ]#line:1261
      O0O000OO0OO0O00OO =O0OOO0OOOOOOOO0O0 .split (" ")#line:1262
      O00O0O0O0OO00O0O0 =O0O000OO0OO0O00OO [0 ]+O0O000OO0OO0O00OO [1 ]#line:1263
      if len (O0O000OO0OO0O00OO )>2 :#line:1265
          if OOOO00O0OOOO00OO0 [1 ]=='11':#line:1267
            OOOO00O0OOOO00OO0 [1 ]='1'#line:1268
          if OOOO00O0OOOO00OO0 [1 ]==O0O000OO0OO0O00OO [2 ]:#line:1272
            OOOOOO00O00OO0OO0 ='<time datetime=.+?>(.+?)<.+?<li class="info">(.+?)</li>'#line:1275
            O000O00OOO000OOO0 =re .compile (OOOOOO00O00OO0OO0 ,re .DOTALL ).findall (OOO0OOOO0O000OO0O )#line:1276
            O00O00OOO00O00000 =''#line:1277
            for OO0000OO0O0O0O0O0 ,O00O0O0OO0OOOOO00 in O000O00OOO000OOO0 :#line:1279
               O00O00OOO00O00000 =O00O00OOO00O00000 +OO0000OO0O0O0O0O0 +': '+O00O0O0OO0OOOOO00 +'\n'#line:1280
            return O00O00OOO00O00000 #line:1281
   return O00O00OOO00O00000 #line:1282
def deep_scrape (O000000O00000OOO0 ,O0OOO000OOO0000O0 ,O0O0OO0OOOOOO00O0 ,OO0O00OOOOO00OO00 ,O000OO000O0O00O0O ,O00O00O0O0OOO0OO0 ):#line:1283
    logging .warning ("Ain")#line:1284
    dbcur .execute ("SELECT * FROM MyTable where REPLACE(father,' ','')=REPLACE('%s',' ','')"%(O0OOO000OOO0000O0 ))#line:1286
    logging .warning ("in")#line:1287
    global sort_by_episode #line:1288
    O0O00OO00O000O00O =dbcur .fetchall ()#line:1289
    O00O0000OO0OOOO0O =int (OO0O00OOOOO00OO00 )#line:1290
    O0000O0O00O0O00O0 =0 #line:1291
    OO0O00O0OOOO0O00O =0 #line:1292
    O0O0O00OOO0O0O00O =[]#line:1293
    for O0OOO00000O000000 ,O000000O00000OOO0 ,O0000OO0OO00OOOOO ,O0O00O0O000OO00OO ,OOO00OOO000OOO0O0 ,OOOOOO0OO0OOO0OO0 ,O00OOOOO0OOO00O0O ,O00O000000000O0OO ,OO000O0OO0OOOO0OO ,O0O0O00000O000000 ,OO0O0O0O00O0OOOOO ,OOO0O0000OOOOO0OO in O0O00OO00O000O00O :#line:1294
      if KODI_VERSION>18:
          O000000O00000OOO0 =O000000O00000OOO0 
          O0000OO0OO00OOOOO =O0000OO0OO00OOOOO 
          O0O00O0O000OO00OO =O0O00O0O000OO00OO 
          OOO00OOO000OOO0O0 =OOO00OOO000OOO0O0 
          OOOOOO0OO0OOO0OO0 =OOOOOO0OO0OOO0OO0 
          O00OOOOO0OOO00O0O =O00OOOOO0OOO00O0O 
          O00O000000000O0OO =O00O000000000O0OO 
          OO000O0OO0OOOO0OO =OO000O0OO0OOOO0OO 
          O0O0O00000O000000 =O0O0O00000O000000 
          OO0O0O0O00O0OOOOO =OO0O0O0O00O0OOOOO 
          OOO0O0000OOOOO0OO =OOO0O0000OOOOO0OO
      else:
          O000000O00000OOO0 =O000000O00000OOO0 .encode('utf-8')
          O0000OO0OO00OOOOO =O0000OO0OO00OOOOO .encode('utf-8')
          O0O00O0O000OO00OO =O0O00O0O000OO00OO .encode('utf-8')
          OOO00OOO000OOO0O0 =OOO00OOO000OOO0O0 .encode('utf-8')
          OOOOOO0OO0OOO0OO0 =OOOOOO0OO0OOO0OO0 .encode('utf-8')
          O00OOOOO0OOO00O0O =O00OOOOO0OOO00O0O .encode('utf-8')
          O00O000000000O0OO =O00O000000000O0OO .encode('utf-8')
          OO000O0OO0OOOO0OO =OO000O0OO0OOOO0OO .encode('utf-8')
          O0O0O00000O000000 =O0O0O00000O000000 .encode('utf-8')
          OO0O0O0O00O0OOOOO =OO0O0O0O00O0OOOOO .encode('utf-8')
          OOO0O0000OOOOO0OO =OOO0O0000OOOOO0OO.encode('utf-8')
      try :#line:1306
          O00OOOOO0OOO00O0O =O00OOOOO0OOO00O0O .replace ('[',' ').replace (']',' ').replace ('	','').replace ("\\"," ").replace (': """",',': "" "",').replace (': """"}',': "" ""}').replace (': "",',': " ",').replace (': ""}',': " "}').replace ('""','"').replace ('\n','').replace ('\r','')#line:1307
          OO000O00000OOOOO0 =json .loads (O00OOOOO0OOO00O0O )#line:1308
          OO0O00OO0O0O000OO =OO000O00000OOOOO0 ['Season']#line:1309
          O0OOOO00OO00OO000 =OO000O00000OOOOO0 ['Episode']#line:1310
          logging .warning (OO0O00OO0O0O000OO )#line:1311
          logging .warning (O0OOOO00OO00OO000 )#line:1312
          OO0O00O0OOOO0O00O =1 #line:1313
      except :#line:1314
        pass #line:1315
      if O0000O0O00O0O00O0 >=int (OO0O00OOOOO00OO00 ):#line:1316
            if OOO0O0000OOOOO0OO =='category':#line:1317
                if 'ערוץ'in O000000O00000OOO0 and "@"not in O000000O00000OOO0 :#line:1318
                    continue #line:1319
                if 'ערוץ'in O000000O00000OOO0 :#line:1320
                    O0O0O00OOO0O0O00O .append (addLink (O000000O00000OOO0 .replace ('@',''),O0OOO000OOO0000O0 +O000000O00000OOO0 ,14 ,False ,O0O00O0O000OO00OO ,OOO00OOO000OOO0O0 ,OOOOOO0OO0OOO0OO0 ,data =O00OOOOO0OOO00O0O .replace ("OriginalTitle","originaltitle")))#line:1321
                else :#line:1322
                    O0O0O00OOO0O0O00O .append (addDir3 (O000000O00000OOO0 ,O0OOO000OOO0000O0 +O000000O00000OOO0 ,5 ,O0O00O0O000OO00OO ,OOO00OOO000OOO0O0 ,OOOOOO0OO0OOO0OO0 ,data =O00OOOOO0OOO00O0O .replace ("OriginalTitle","Originaltitle")))#line:1323
            else :#line:1324
                   O0O0O00OOO0O0O00O .append (addLink (O000000O00000OOO0 ,O0000OO0OO00OOOOO ,3 ,False ,O0O00O0O000OO00OO ,OOO00OOO000OOO0O0 ,OOOOOO0OO0OOO0OO0 ,data =(O00OOOOO0OOO00O0O).replace ("OriginalTitle","originaltitle")))#line:1325
            if (O00O0000OO0OOOO0O >(int (OO0O00OOOOO00OO00 )+max_per_page )):#line:1327
                O0O0O00OOO0O0O00O .append (addDir3 ('[COLOR aqua][I]עמוד הבא[/I][/COLOR]',O0OOO000OOO0000O0 ,5 ,__PLUGIN_PATH__ +"\\resources\\next_icon.gif",__PLUGIN_PATH__ +"\\resources\\next.gif",'Next page',count =O00O0000OO0OOOO0O ,cat_level =O0O0OO0OOOOOO00O0 ,data =" ",selected_list =O000OO000O0O00O0O ,lang =O00O00O0O0OOO0OO0 ))#line:1329
                break #line:1331
            O00O0000OO0OOOO0O =O00O0000OO0OOOO0O +1 #line:1332
      O0000O0O00O0O00O0 =O0000O0O00O0O00O0 +1 #line:1333
    xbmcplugin .addDirectoryItems (int (sys .argv [1 ]),O0O0O00OOO0O0O00O ,len (O0O0O00OOO0O0O00O ))#line:1334
    if OO0O00O0OOOO0O00O >0 :#line:1335
        sort_by_episode =True #line:1336
def play_myfile (O0OO0O0O00OO0O0OO ):#line:1338
    OO000O00000OO000O ,OOOO0000OOOO0O0OO =read_site_html (O0OO0O0O00OO0O0OO )#line:1341
    OO0OO0O0OO0O00OO0 ="window.location='(.+?)'"#line:1342
    O00O00OO00OO0OO0O =re .compile (OO0OO0O0OO0O00OO0 ).findall (OO000O00000OO000O )#line:1345
    O00OOOOOOO0O0O0OO =O00O00OO00OO0OO0O [1 ]#line:1347
    return (O00OOOOOOO0O0O0OO )#line:1350
def get_upfile_det (O0O00O0OO000OOOOO ):#line:1351
    OO0OOOO0O00OO00O0 ,OO0O0OO000O0OOO00 =read_site_html (O0O00O0OO000OOOOO )#line:1353
    O0OO0OO0O0OO0OO0O ='<title>(.+?)</title>.+?<input type="hidden" value="(.+?)" name="hash">'#line:1354
    O00OOO0O0O0O0OO0O =re .compile (O0OO0OO0O0OO0OO0O ,re .DOTALL ).findall (OO0OOOO0O00OO00O0 )#line:1355
    for O00000OOO0O00O0O0 ,O0OO0OO000OOO0OO0 in O00OOO0O0O0O0OO0O :#line:1356
      OOO00O0O0OOOOOO0O =O0O00O0OO000OOOOO .split ('/')[-1 ]#line:1357
      OOO00O0O0OOOOOO0O =OOO00O0O0OOOOOO0O .replace ('.html','').replace ('.htm','')#line:1358
      OOO00O00O000OOO00 ='http://down.upfile.co.il/downloadnew/file/%s/%s'%(OOO00O0O0OOOOOO0O ,O0OO0OO000OOO0OO0 )#line:1360
    return O00000OOO0O00O0O0 ,OOO00O00O000OOO00 #line:1361
def get_q (O00OOO0O0O0000OO0 ):#line:1364
    OOOOOO0000OOO0OO0 ='"fmt_list","(.+?)"'#line:1365
    OO0O0O000OO0O00OO =re .compile (OOOOOO0000OOO0OO0 ).findall (O00OOO0O0O0000OO0 )#line:1366
    OO0O0OO000O0O0O0O =OO0O0O000OO0O00OO [0 ].split (',')#line:1368
    return OO0O0OO000O0O0O0O #line:1369
def getPublicStream (O0OO0OO0O0OOOO00O ):#line:1370
        import cookielib #line:1371
        OOOOOOOOOOOOOO0O0 =-1 #line:1374
        O0O00O0OOOOOO00O0 =-1 #line:1375
        OO0O0000OO00O000O =-1 #line:1376
        O0O000OO0OOOO00O0 =[]#line:1378
        OO00OOO00000OOOOO =cookielib .LWPCookieJar ()#line:1381
        O0OO0OOOO00O0O0O0 =[urllib2 .HTTPHandler (),urllib2 .HTTPSHandler (),urllib2 .HTTPCookieProcessor (OO00OOO00000OOOOO )]#line:1386
        OO0O00OOO0OO0OO0O =urllib2 .build_opener (*O0OO0OOOO00O0O0O0 )#line:1387
        O0OO0O0000O0OO0OO =urllib2 .Request (O0OO0OO0O0OOOO00O )#line:1388
        O0OO0O0000O0OO0OO .add_header ('User-agent',__USERAGENT__ )#line:1390
        OO00OO00O0OO000OO =OO0O00OOO0OO0OO0O .open (O0OO0O0000O0OO0OO )#line:1391
        for O0OOOOOO00O0O000O in OO00OOO00000OOOOO :#line:1392
            if O0OOOOOO00O0O000O .name =='DRIVE_STREAM':#line:1393
              OO000OO00000O00O0 =O0OOOOOO00O0O000O .value #line:1394
        OO00OOOOO0OO0OOOO =OO00OO00O0OO000OO .read ()#line:1398
        for O000OO000OO0OO0O0 in re .finditer ('\"fmt_list\"\,\"([^\"]+)\"',OO00OOOOO0OO0OOOO ,re .DOTALL ):#line:1406
            O0O00OO0OOO00O000 =O000OO000OO0OO0O0 .group (1 )#line:1407
        O00OO0OO0O000000O =''#line:1409
        for O000OO000OO0OO0O0 in re .finditer ('\"title\"\,\"([^\"]+)\"',OO00OOOOO0OO0OOOO ,re .DOTALL ):#line:1411
            O00OO0OO0O000000O =O000OO000OO0OO0O0 .group (1 )#line:1412
        OO00OO0000000OO00 ={}#line:1416
        O0OO00OOO00OO0OO0 ={'x-flv':'flv','webm':'WebM','mp4;+codecs="avc1.42001E,+mp4a.40.2"':'MP4'}#line:1417
        for O000OO000OO0OO0O0 in re .finditer ('(\d+)/(\d+)x(\d+)/(\d+/\d+/\d+)\&?\,?',O0O00OO0OOO00O000 ,re .DOTALL ):#line:1419
              (O00OOO0OO0OOOO0OO ,O0000OOOO0000OO0O ,OOOOOOOOOO0O0000O ,OOO0OO000O0O000OO )=O000OO000OO0OO0O0 .groups ()#line:1420
              if OOO0OO000O0O000OO =='9/0/115':#line:1422
                OO00OO0000000OO00 [O00OOO0OO0OOOO0OO ]={'resolution':OOOOOOOOOO0O0000O ,'codec':'h.264/aac'}#line:1423
              elif OOO0OO000O0O000OO =='99/0/0':#line:1424
                OO00OO0000000OO00 [O00OOO0OO0OOOO0OO ]={'resolution':OOOOOOOOOO0O0000O ,'codec':'VP8/vorbis'}#line:1425
              else :#line:1426
                OO00OO0000000OO00 [O00OOO0OO0OOOO0OO ]={'resolution':OOOOOOOOOO0O0000O }#line:1427
        for O000OO000OO0OO0O0 in re .finditer ('\"url_encoded_fmt_stream_map\"\,\"([^\"]+)\"',OO00OOOOO0OO0OOOO ,re .DOTALL ):#line:1430
            O0O0OOO0OOO00O0O0 =O000OO000OO0OO0O0 .group (1 )#line:1431
        O0O0OOO0OOO00O0O0 =unque (unque (unque (unque (unque (O0O0OOO0OOO00O0O0 )))))#line:1435
        O0O0OOO0OOO00O0O0 =re .sub ('\\\\u003d','=',O0O0OOO0OOO00O0O0 )#line:1436
        O0O0OOO0OOO00O0O0 =re .sub ('\\\\u0026','&',O0O0OOO0OOO00O0O0 )#line:1437
        O0O0OOO0OOO00O0O0 =re .sub ('\&url\='+'https://','\@',O0O0OOO0OOO00O0O0 )#line:1441
        O00OOOO0O0000OO00 =0 #line:1449
        for O000OO000OO0OO0O0 in re .finditer ('\@([^\@]+)',O0O0OOO0OOO00O0O0 ):#line:1450
                OO00O0O0OOO0OO0O0 =O000OO000OO0OO0O0 .group (1 )#line:1451
                for O0O00OO0OOOOOOO00 in re .finditer ('itag\=(\d+).*?type\=video\/([^\&]+)\&quality\=(\w+)',OO00O0O0OOO0OO0O0 ,re .DOTALL ):#line:1453
                    (O00OOO0OO0OOOO0OO ,OO0OO0O0O0OOO000O ,OOO0O0OOO0O0O0OOO )=O0O00OO0OOOOOOO00 .groups ()#line:1454
                    O00OOOO0O0000OO00 =O00OOOO0O0000OO00 +1 #line:1455
                    O0OOO0O0O0OO0OO00 =0 #line:1456
                    if OOOOOOOOOOOOOO0O0 >-1 or O0O00O0OOOOOO00O0 >-1 or OO0O0000OO00O000O >-1 :#line:1457
                        if int (OO00OO0000000OO00 [O00OOO0OO0OOOO0OO ]['resolution'])==1080 :#line:1458
                            if OOOOOOOOOOOOOO0O0 ==0 :#line:1459
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +1000 #line:1460
                            elif OOOOOOOOOOOOOO0O0 ==1 :#line:1461
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +3000 #line:1462
                            elif OOOOOOOOOOOOOO0O0 ==3 :#line:1463
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +9000 #line:1464
                        elif int (OO00OO0000000OO00 [O00OOO0OO0OOOO0OO ]['resolution'])==720 :#line:1465
                            if OOOOOOOOOOOOOO0O0 ==0 :#line:1466
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +2000 #line:1467
                            elif OOOOOOOOOOOOOO0O0 ==1 :#line:1468
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +1000 #line:1469
                            elif OOOOOOOOOOOOOO0O0 ==3 :#line:1470
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +9000 #line:1471
                        elif int (OO00OO0000000OO00 [O00OOO0OO0OOOO0OO ]['resolution'])==480 :#line:1472
                            if OOOOOOOOOOOOOO0O0 ==0 :#line:1473
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +3000 #line:1474
                            elif OOOOOOOOOOOOOO0O0 ==1 :#line:1475
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +2000 #line:1476
                            elif OOOOOOOOOOOOOO0O0 ==3 :#line:1477
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +1000 #line:1478
                        elif int (OO00OO0000000OO00 [O00OOO0OO0OOOO0OO ]['resolution'])<480 :#line:1479
                            if OOOOOOOOOOOOOO0O0 ==0 :#line:1480
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +4000 #line:1481
                            elif OOOOOOOOOOOOOO0O0 ==1 :#line:1482
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +3000 #line:1483
                            elif OOOOOOOOOOOOOO0O0 ==3 :#line:1484
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +2000 #line:1485
                    try :#line:1486
                        if OO00OO0000000OO00 [O00OOO0OO0OOOO0OO ]['codec']=='VP8/vorbis':#line:1487
                            if OO0O0000OO00O000O ==1 :#line:1488
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +90000 #line:1489
                            else :#line:1490
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +10000 #line:1491
                    except :#line:1492
                        O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +30000 #line:1493
                    try :#line:1495
                        if O0OO00OOO00OO0OO0 [OO0OO0O0O0OOO000O ]=='MP4':#line:1496
                            if O0O00O0OOOOOO00O0 ==0 or O0O00O0OOOOOO00O0 ==1 :#line:1497
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +100 #line:1498
                            elif O0O00O0OOOOOO00O0 ==3 or O0O00O0OOOOOO00O0 ==4 :#line:1499
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +200 #line:1500
                            else :#line:1501
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +300 #line:1502
                        elif O0OO00OOO00OO0OO0 [OO0OO0O0O0OOO000O ]=='flv':#line:1503
                            if O0O00O0OOOOOO00O0 ==2 or O0O00O0OOOOOO00O0 ==3 :#line:1504
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +100 #line:1505
                            elif O0O00O0OOOOOO00O0 ==1 or O0O00O0OOOOOO00O0 ==5 :#line:1506
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +200 #line:1507
                            else :#line:1508
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +300 #line:1509
                        elif O0OO00OOO00OO0OO0 [OO0OO0O0O0OOO000O ]=='WebM':#line:1510
                            if O0O00O0OOOOOO00O0 ==4 or O0O00O0OOOOOO00O0 ==5 :#line:1511
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +100 #line:1512
                            elif O0O00O0OOOOOO00O0 ==0 or O0O00O0OOOOOO00O0 ==1 :#line:1513
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +200 #line:1514
                            else :#line:1515
                                O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +300 #line:1516
                        else :#line:1517
                            O0OOO0O0O0OO0OO00 =O0OOO0O0O0OO0OO00 +100 #line:1518
                    except :#line:1519
                        pass #line:1520
                    try :#line:1522
                        O0O000OO0OOOO00O0 .append (mediaurl .mediaurl ('https://'+OO00O0O0OOO0OO0O0 ,OO00OO0000000OO00 [O00OOO0OO0OOOO0OO ]['resolution']+' - '+O0OO00OOO00OO0OO0 [OO0OO0O0O0OOO000O ]+' - '+OO00OO0000000OO00 [O00OOO0OO0OOOO0OO ]['codec'],str (OO00OO0000000OO00 [O00OOO0OO0OOOO0OO ]['resolution'])+'_'+str (O0OOO0O0O0OO0OO00 +O00OOOO0O0000OO00 ),O0OOO0O0O0OO0OO00 +O00OOOO0O0000OO00 ,title =O00OO0OO0O000000O ))#line:1523
                    except KeyError :#line:1524
                        O0O000OO0OOOO00O0 .append (mediaurl .mediaurl ('https://'+OO00O0O0OOO0OO0O0 ,OO00OO0000000OO00 [O00OOO0OO0OOOO0OO ]['resolution']+' - '+OO0OO0O0O0OOO000O ,str (OO00OO0000000OO00 [O00OOO0OO0OOOO0OO ]['resolution'])+'_'+str (O0OOO0O0O0OO0OO00 +O00OOOO0O0000OO00 ),O0OOO0O0O0OO0OO00 +O00OOOO0O0000OO00 ,title =O00OO0OO0O000000O ))#line:1525
        return O0O000OO0OOOO00O0 ,OO000OO00000O00O0 #line:1527
def res_q(quality):
    f_q=' '
    if '2160' in quality:
      f_q='2160'
    elif '1080' in quality:
      f_q='1080'
    elif '720' in quality:
      f_q='720'
    elif '480' in quality:
      f_q='480'
    elif 'hd' in quality.lower() or 'hq' in quality.lower():
      f_q='720'
    elif '360' in quality or 'sd' in quality.lower():
      f_q='360'
    elif '240' in quality:
      f_q='240'
    return f_q
def download_subs(url,headers):
    local_filename = os.path.join(user_dataDir, 'sub.srt')
    # NOTE the stream=True parameter below
    with requests.get(url,headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename
def get_ip():
    x=requests.get('https://bot.whatismyipaddress.com').content
    return x
def get_token(token):
    headers = {
            'Connection': 'Keep-Alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; Redmi Note 4X MIUI/V10.2.1.0.MBFMIXM)'
    }
    
    url='https://drive-login.herokuapp.com/refresh'
    body='refresh_token=%s&provider=googledrive'%token
    headers={'addon': 'plugin.noone 1.0.2/1.0.2'}
    x=requests.post(url,headers=headers,params=body).content
    
    x=json.loads(x)
    return x
def googledrive_resolve (OO000OO00OOOOO0O0 ):
    
    try:
        my_ip=get_ip()
    except:
        my_ip=''
    
    x='https://drive.google.com/file/d/'+OO000OO00OOOOO0O0 +'/view'
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
            'Accept-Language': 'en-US,en;q=0.5',
           
            'Connection': 'keep-alive',
            
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
    y=requests.get(x,headers=headers).content.decode('utf-8')
    
    if 'קבלת גישה ל' in y:
        xbmcgui .Dialog ().ok ("Error",'דרושה לך הרשאת גישה')#line:2307
        return 0,None
    nm=re.compile('meta property="og\:title" content="(.+?)"').findall(y)[0]
    logging.warning(nm[0])
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f_dir=os.path.join(dir_path,'accounts.db')
    
    cacheFile =f_dir#line:212
    logging .warning (cacheFile )#line:213
    j_data={}
    if  os .path .exists (cacheFile ):#line:216
        logging .warning ('IN')#line:217
        path =os .path .join (__PLUGIN_PATH__ ,"resources")#line:218
        download_file (l_list ,path )#line:219
        logging .warning ('Unzipping')#line:221
        unzip (os .path .join (path ,"fixed_list.zip"))#line:222
        dbcon =database .connect (cacheFile )#line:226
        dbcur =dbcon .cursor ()#line:227
        dbcur .execute ("SELECT * FROM store")#line:2995
        
        match =dbcur .fetchall ()#line:2997
        for key,value in match:
            #logging.warning(value.replace("u'","'").replace("'",'"'))
            j_data[key]=json.loads(value.replace("u'","'").replace("'",'"'))
        dbcur .close ()#line:3761
        dbcon .close ()#line:3762
    else:
        f_dir=os.path.join(dir_path,'accounts.cfg')
        file =open (f_dir ,'r')#line:3488
        f_data =file .read ()#line:3490
        file .close ()#line:3491
        j_data=json.loads(f_data)
   
    dr_data={}
    for items in j_data:
        #logging.warning(j_data[items])
        for itt in j_data[items]['drives']:
            dr_data[itt['id']]={}
            dr_data[itt['id']]['name']=itt['name']
            dr_data[itt['id']]['drivers_id']=itt['id']
          
            dr_data[itt['id']]['type']=itt['type']
            dr_data[itt['id']]['token']=j_data[items]['access_tokens']['refresh_token']
        
    
    
    all_links=[]
    stop_all=0
    for items in dr_data:
        if stop_all==1:
            break
        logging.warning('Now Drive:'+items)
        drive_id=dr_data[items]['drivers_id']
      
        search_name=nm.replace('&#39;',"'").replace('&amp;',"&")
        drive_type=dr_data[items]['type']

        x=cache.get(get_token,24,dr_data[items]['token'], table='pages')
        logging.warning('drive_type:'+drive_type)

        if 'drive#drive' in drive_type:
            url='https://www.googleapis.com/drive/v3/files?q=fullText contains "%s" or fullText contains "%s"&spaces=drive&includeTeamDriveItems=true&prettyPrint=false&fields=files(id,name,modifiedTime,size,mimeType,description,hasThumbnail,thumbnailLink,owners(permissionId),parents,trashed,imageMediaMetadata(width),videoMediaMetadata)&teamDriveId=%s&corpora=teamDrive&supportsTeamDrives=true'%(search_name,search_name,drive_id)
            logging.warning('Team Url')
        else:
            data={'q': 'fullText contains "%s" or fullText contains "%s"'%(search_name,search_name), 'fields': 'files(id,name,modifiedTime,size,mimeType,description,hasThumbnail,thumbnailLink,owners(permissionId),parents,trashed,imageMediaMetadata(width),videoMediaMetadata),kind,nextPageToken', 'spaces': 'drive', 'prettyPrint': 'false','spaces': 'drive','supportsAllDrives': 'true'}
            url="https://www.googleapis.com/drive/v3/files?quotaUser=%s&"%my_ip+ url_encode(data)
        headers= {'Authorization': u'Bearer %s'%x['access_token']}
        logging.warning(url)
        y=requests.get(url,headers=headers).json()
        
        if 'error' in y:
        
            if y['error']['message']=='Invalid Credentials':
                x=cache.get(get_token,0,dr_data[items]['token'], table='pages')
                headers= {'Authorization': u'Bearer %s'%x['access_token']}
                y=requests.get(url,headers=headers).json()
            
        logging.warning('Found Resuls')
        logging.warning(json.dumps(y))
        s_items=items
        for items2 in y['files']:
           
           
            
            name1=items2['name']
           
            if base64.b64encode(name1.strip().encode('utf-8')).decode('utf-8').replace('\r','').replace('\n','').replace('\t','')!=base64.b64encode(search_name.strip().encode('utf-8')).decode('utf-8').replace('\r','').replace('\n','').replace('\t',''):
                continue
            logging.warning('YESSSSSSSSSSS')
            id=items2['id']
            #url='https://www.googleapis.com/drive/v3/files/%s?access_token=y%s&alt=media'%(id,x['access_token'])
            url='https://www.googleapis.com/drive/v3/files/%s?alt=media&quotaUser=%s'%(id,my_ip)
            
            if 'video' in items2['mimeType']:
                progress='getting'
                #z=requests.get(url,headers=headers,stream=True).url
           
                z=url+"|"+ url_encode(headers)
                res=res_q(name1)
                #try_head = requests.head(z,headers=base_header, stream=True,verify=False,timeout=15)
                if 'size' in items2:
                    f_size2='0.0 GB'
                    if int(items2['size'])>(1024*1024):
                        f_size2=str(round(float(items2['size'])/(1024*1024*1024), 2))+' GB'
                    if f_size2!='0.0 GB':
                        s_name='Google'+' - '+f_size2
                    else:
                        s_name='Google'
                all_links.append((name1,z))                
                
                global_var=all_links
                stop_all=1
                break
    #subs
    stop_all2=0
    z_subs=None
    logging.warning(s_items)
    items=s_items
    if 1:#for items in dr_data:
        #if stop_all2==1:
        #   break

        drive_id=dr_data[items]['drivers_id']
        search_name=nm.replace('&#39;',"'").replace('.mp4','.srt').replace('.avi','.srt').replace('.mkv','.srt')
        drive_type=dr_data[items]['type']
        logging.warning('search_name:'+search_name)
        headers = {
            'Connection': 'Keep-Alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; Redmi Note 4X MIUI/V10.2.1.0.MBFMIXM)'
        }
        
        url='https://drive-login.herokuapp.com/refresh'
        body='refresh_token=%s&provider=googledrive'%dr_data[items]['token']
        headers={'addon': 'plugin.noone 1.0.2/1.0.2'}
        x=requests.post(url,headers=headers,params=body).content
        
        x=json.loads(x)
        logging.warning(json.dumps(x))
        if 'teamDrive' in drive_type:
            url='https://www.googleapis.com/drive/v3/files?q=fullText contains "%s" or fullText contains "%s"&spaces=drive&includeTeamDriveItems=true&prettyPrint=false&fields=files(id,name,modifiedTime,size,mimeType,description,hasThumbnail,thumbnailLink,owners(permissionId),parents,trashed,imageMediaMetadata(width),videoMediaMetadata)&teamDriveId=%s&corpora=teamDrive&supportsTeamDrives=true'%(search_name,search_name,drive_id)
        else:
            data={'q': 'fullText contains "%s" or fullText contains "%s"'%(search_name,search_name), 'fields': 'files(id,name,modifiedTime,size,mimeType,description,hasThumbnail,thumbnailLink,owners(permissionId),parents,trashed,imageMediaMetadata(width),videoMediaMetadata),kind,nextPageToken', 'spaces': 'drive', 'prettyPrint': 'false'}
            url="https://www.googleapis.com/drive/v3/files?"+ url_encode(data)
        headers= {'authorization': u'Bearer %s'%x['access_token']}
        logging.warning(url)
        y=requests.get(url,headers=headers).json()
        logging.warning('Found Resuls subs')
        logging.warning(json.dumps(y))
        logging.warning(items)
        for items2 in y['files']:
           
           
            
            name1=items2['name']
            
            if base64.b64encode(name1.strip().encode('utf-8')).decode('utf-8')!=base64.b64encode(search_name.strip().encode('utf-8')).decode('utf-8'):
                continue
                
            logging.warning('Found subs')
            logging.warning(name1)
            id=items2['id']
            #url='https://www.googleapis.com/drive/v3/files/%s?access_token=y%s&alt=media'%(id,x['access_token'])
            url='https://www.googleapis.com/drive/v3/files/%s?alt=media'%(id)
            
            if 1:
                progress='getting'
                #z=requests.get(url,headers=headers,stream=True).url
           
                z_subs=url+"|"+ url_encode(headers)
                res=res_q(name1)
                #try_head = requests.head(z,headers=base_header, stream=True,verify=False,timeout=15)
                if 'size' in items2:
                    f_size2='0.0 GB'
                    if int(items2['size'])>(1024*1024):
                        f_size2=str(round(float(items2['size'])/(1024*1024*1024), 2))+' GB'
                    if f_size2!='0.0 GB':
                        s_name='Google'+' - '+f_size2
                    else:
                        s_name='Google'
                all_links.append((name1,z_subs))                
                    
                global_var=all_links
                stop_all2=1
                break
    f_subs=None
    if z_subs:
        download_subs(url,headers)
        f_subs=os.path.join(user_dataDir, 'sub.srt')
        
    return z,f_subs

def googledrive_resolve_old (OO000OO00OOOOO0O0 ):#line:1529
    import resolveurl
    link =resolveurl .HostedMediaFile (url ='https://drive.google.com/file/d/'+OO000OO00OOOOO0O0 +'/view' ).resolve ()#line:2687
    return link
    OO0OO0O000O0OO0OO ,O000O0OO0O00O0000 =getPublicStream ('https://drive.google.com/file/d/'+OO000OO00OOOOO0O0 +'/view')#line:1533
    O000O0000O0OOOOOO =sorted (OO0OO0O000O0OO0OO )#line:1535
    OOOOOO000O00O0OO0 =[]#line:1536
    OO0OO0OOOO00OOO00 =[]#line:1537
    for OOO000000O0OOOO0O in O000O0000O0OOOOOO :#line:1538
        if '4k'in OOO000000O0OOOO0O .qualityDesc :#line:1540
           OOOOOO000O00O0OO0 .append ('4000')#line:1542
        elif '1080'in OOO000000O0OOOO0O .qualityDesc :#line:1543
           OOOOOO000O00O0OO0 .append ('1080')#line:1545
        elif '720'in OOO000000O0OOOO0O .qualityDesc :#line:1546
           OOOOOO000O00O0OO0 .append ('720')#line:1548
        elif '480'in OOO000000O0OOOO0O .qualityDesc :#line:1549
           OOOOOO000O00O0OO0 .append ('480')#line:1551
        elif '360'in OOO000000O0OOOO0O .qualityDesc :#line:1552
           OOOOOO000O00O0OO0 .append ('360')#line:1554
        elif '240'in OOO000000O0OOOO0O .qualityDesc :#line:1555
           OOOOOO000O00O0OO0 .append ('240')#line:1557
        else :#line:1558
           OOOOOO000O00O0OO0 .append ('0')#line:1560
        OO0OO0OOOO00OOO00 .append ((OOO000000O0OOOO0O .url ,fix_q (OOO000000O0OOOO0O .qualityDesc )))#line:1561
    O000OOOOO0OOO00OO =OOOOOO000O00O0OO0 #line:1562
    O000OOOOO0OOO00OO =sorted (OOOOOO000O00O0OO0 ,key =lambda O00O00O000OOO0OOO :O00O00O000OOO0OOO [0 ],reverse =True )#line:1563
    OO0OO0OOOO00OOO00 =sorted (OO0OO0OOOO00OOO00 ,key =lambda O000O00O0O0OOOO00 :O000O00O0O0OOOO00 [1 ],reverse =True )#line:1564
    if Addon .getSetting ("auto_q")=='true':#line:1566
            O00O0O00O0OOO0OOO =O000OOOOO0OOO00OO [0 ]#line:1567
            OOOOO0OO000OOOO00 =int (Addon .getSetting ("quality"))#line:1568
            OOOO00OOO00O0O000 =0 #line:1570
            OO00O0OOOO0OO0OOO =[]#line:1571
            for O0O0O00O0O000OO00 in O000OOOOO0OOO00OO :#line:1572
               if fix_q (O0O0O00O0O000OO00 )<OOOOO0OO000OOOO00 :#line:1574
                 OO00O0OOOO0OO0OOO .append (OOOO00OOO00O0O000 )#line:1576
               OOOO00OOO00O0O000 +=1 #line:1577
            O000OO0O00O00O0O0 =0 #line:1578
            OO0000O00OO00OO00 =[]#line:1579
            for O0O0O00O0O000OO00 in O000OOOOO0OOO00OO :#line:1580
                 if O000OO0O00O00O0O0 not in OO00O0OOOO0OO0OOO :#line:1581
                  OO0000O00OO00OO00 .append (O0O0O00O0O000OO00 )#line:1582
                 O000OO0O00O00O0O0 +=1 #line:1583
            O000OOOOO0OOO00OO =OO0000O00OO00OO00 #line:1584
            if len (O000OOOOO0OOO00OO )>0 :#line:1585
              O00O0O00O0OOO0OOO =len (O000OOOOO0OOO00OO )-1 #line:1586
            O000O00OO0O0OO000 ,O0O0OOOOOOOO0O0OO =OO0OO0OOOO00OOO00 [O00O0O00O0OOO0OOO ]#line:1588
    else :#line:1590
        O0OOOO00OOO000000 =xbmcgui .Dialog ().select ("בחר איכות",OOOOOO000O00O0OO0 )#line:1591
        if O0OOOO00OOO000000 ==-1 :#line:1592
            sys .exit ()#line:1593
        O000O00OO0O0OO000 =O000O0000O0OOOOOO [O0OOOO00OOO000000 ].url #line:1595
    O000OO00000O00O0O =O000O00OO0O0OO000 #line:1598
    return (O000OO00000O00O0O +'||Cookie=DRIVE_STREAM%3D'+O000O0OO0O00O0000 )#line:1599
def get_epg_plot (O0O0O0O0000OO00OO ,O0OOO00OOOO000OO0 ):#line:1600
    import datetime #line:1601
    import _strptime #line:1602
    O000O000OOO0OOOOO ='<programme start=(.+?)</programme>'#line:1605
    OO0O000O00OO0000O =re .compile (O000O000OOO0OOOOO ,re .DOTALL ).findall (O0OOO00OOOO000OO0 )#line:1606
    OO00OO00OO0O000OO =(datetime .datetime .now ().strftime ("%Y%m%d%H%M%S"))#line:1609
    OOOOOO0OOOOOO0OOO =((datetime .datetime .now ()-datetime .timedelta (minutes =10080 )).strftime ("%Y%m%d%H%M%S"))#line:1610
    OO00O0OO0OOOOOOOO =(datetime .datetime .now ().strftime ("%Y%m%d"))#line:1612
    O0OOOO0000OOO00OO =((datetime .datetime .now ()-datetime .timedelta (minutes =10080 )).strftime ("%Y%m%d"))#line:1613
    OO0O00O0O000OO0O0 =''#line:1614
    OOOOO00OO00OO0OOO =''#line:1615
    O000OOOOO000O00OO =''#line:1616
    for O00OO00OO00OO00O0 in OO0O000O00OO0000O :#line:1617
      OOO0000O0000OOOO0 ='"(.+?)" stop="(.+?)" channel="%s">.+?<desc lang="he">(.+?)</desc>'%O0O0O0O0000OO00OO #line:1619
      OOO0O0OO0O0O0OO00 =re .compile (OOO0000O0000OOOO0 ,re .DOTALL ).findall (O00OO00OO00OO00O0 )#line:1620
      for O0OO0OOO0O0O0O0OO ,OO0OOOO0O0OOOOO00 ,O000OOOOO000O00OO in OOO0O0OO0O0O0OO00 :#line:1622
       O0000O0O0OO00OO00 =O0OO0OOO0O0O0O0OO .split (" ")[0 ]#line:1623
       if OO00O0OO0OOOOOOOO in O0OO0OOO0O0O0O0OO :#line:1624
         OOO000OOO0O0OOOOO =OO00OO00OO0O000OO #line:1625
       else :#line:1626
         OOO000OOO0O0OOOOO =OOOOOO0OOOOOO0OOO #line:1627
       if int (OOO000OOO0O0OOOOO )<=int (O0000O0O0OO00OO00 ):#line:1628
          if OO0O00O0O000OO0O0 !='':#line:1630
            try :#line:1632
                OOOO00O0OO0O00OO0 =datetime .datetime .strptime (OO0O00O0O000OO0O0 ,"%Y%m%d%H%M%S")#line:1633
            except TypeError :#line:1634
                OOOO00O0OO0O00OO0 =datetime .datetime (*(time .strptime (OO0O00O0O000OO0O0 ,"%Y%m%d%H%M%S")[0 :6 ]))#line:1635
            try :#line:1638
                O0OO0000000000000 =datetime .datetime .strftime (OOOO00O0OO0O00OO0 ,"%H:%M")#line:1639
            except TypeError :#line:1640
                O0OO0000000000000 =datetime .datetime (*(time .strftime (OOOO00O0OO0O00OO0 ,"%H:%M")[0 :6 ]))#line:1641
            OOOOO00OO00OO0OOO =OOOOO00OO00OO0OOO +O0OO0000000000000 +': '+O000OOOOO000O00OO +'\n'#line:1644
            OO0O00O0O000OO0O0 =''#line:1645
          else :#line:1646
            try :#line:1647
                OOOO00O0OO0O00OO0 =datetime .datetime .strptime (O0000O0O0OO00OO00 ,"%Y%m%d%H%M%S")#line:1648
            except TypeError :#line:1649
                OOOO00O0OO0O00OO0 =datetime .datetime (*(time .strptime (O0000O0O0OO00OO00 ,"%Y%m%d%H%M%S")[0 :6 ]))#line:1650
            try :#line:1653
                O0OO0000000000000 =datetime .datetime .strftime (OOOO00O0OO0O00OO0 ,"%H:%M")#line:1654
            except TypeError :#line:1655
                O0OO0000000000000 =datetime .datetime (*(time .strftime (OOOO00O0OO0O00OO0 ,"%H:%M")[0 :6 ]))#line:1656
            OOOOO00OO00OO0OOO =OOOOO00OO00OO0OOO +O0OO0000000000000 +': '+O000OOOOO000O00OO +'\n'#line:1658
       else :#line:1660
         OO0O00O0O000OO0O0 =O0000O0O0OO00OO00 #line:1661
    return OOOOO00OO00OO0OOO #line:1663
def get_strimm_link (O00OO0OO000000000 ):#line:1664
    O00OO0OO000000000 =O00OO0OO000000000 .strip ("")#line:1665
    OO0OOOO0OO0OOOO00 =read_site_html2 (O00OO0OO000000000 )#line:1667
    OOOO0O0000O0O0OO0 =time .strftime ("%m-%d-%Y-%H-%M")#line:1668
    OOOO0O0O0000O00O0 ='channelTubeId = "(.+?)"'#line:1669
    OOOO00O0OO000000O =re .compile (OOOO0O0O0000O00O0 ).findall (OO0OOOO0OO0OOOO00 )#line:1670
    OO0OOOO0OO0OOOO00 =read_site_html2 (__REQ_URL__ .replace ("$$$$$",OOOO00O0OO000000O [0 ]).replace ('!!!!!!',str (OOOO0O0000O0O0OO0 )))#line:1671
    OOO000O000OOO00OO =__REQ_URL__ .replace ("$$$$$",OOOO00O0OO000000O [0 ]).replace ('!!!!!!',str (OOOO0O0000O0O0OO0 ))#line:1672
    OO0OOOO0OO0OOOO00 =read_site_html2 (OOO000O000OOO00OO )#line:1673
    OOOO0O0O0000O00O0 ='<Playlist>(.+?)</Playlist>'#line:1674
    OOOO00O0OO000000O =re .compile (OOOO0O0O0000O00O0 ,re .DOTALL ).findall (OO0OOOO0OO0OOOO00 )#line:1675
    OOOO0O0O0000O00O0 ='<VideoTubeTitle>(.+?)</VideoTubeTitle>.+?<ProviderVideoId>(.+?)</ProviderVideoId>.+?<Thumbnail>(.+?)</Thumbnail>'#line:1677
    O00OOOOO000O0O0OO =re .compile (OOOO0O0O0000O00O0 ,re .DOTALL ).findall (OOOO00O0OO000000O [0 ])#line:1678
    O000000000OOOO000 =xbmc .PlayList (xbmc .PLAYLIST_VIDEO )#line:1679
    O000000000OOOO000 .clear ()#line:1680
    O0OO00O0OOOO0O0O0 =0 #line:1681
    for O000O0O0000O0OOOO ,O0O00OOOO00O0000O ,OO00OO0OOOOOOOOO0 in O00OOOOO000O0O0OO :#line:1682
        if Addon .getSetting ("youtube")=="0":#line:1686
          OOO000O000OOO00OO ='plugin://plugin.video.youtube/play/?video_id='+O0O00OOOO00O0000O #line:1688
        else :#line:1689
         O000OO0O00OO0O0OO ='/watch?v=%s'%O0O00OOOO00O0000O #line:1690
         O000OO0O00OO0O0OO ='videoid@@@@'+O000OO0O00OO0O0OO .replace ("=","@@@@@@").replace ("&","*****").replace ("?","!!!!!!")#line:1691
         OOO000O000OOO00OO ='plugin://plugin.video.MyYoutube/?mode=3&name=%s&url=%s'%(O000O0O0000O0OOOO ,O000OO0O00OO0O0OO )#line:1692
        O000OO0000O0O0O00 =xbmcgui .ListItem (O000O0O0000O0OOOO ,thumbnailImage =OO00OO0OOOOOOOOO0 )#line:1695
        O000OO0000O0O0O00 .setInfo ('video',{'Title':O000O0O0000O0OOOO })#line:1696
        O000000000OOOO000 .add (url =OOO000O000OOO00OO ,listitem =O000OO0000O0O0O00 ,index =O0OO00O0OOOO0O0O0 )#line:1697
        O0OO00O0OOOO0O0O0 =O0OO00O0OOOO0O0O0 +1 #line:1698
    O000000000OOOO000 .shuffle ()#line:1699
    return 'DONE'#line:1705
def change_aspect ():#line:1706
    import glob ,sqlite3 #line:1707
    OO0O0OOOOO00O0O00 =glob .glob (xbmc .translatePath ('special://Database')+'/MyVideos*.db')#line:1708
    if len (OO0O0OOOOO00O0O00 ):#line:1709
        O0O0000OOOOOO0OO0 =sqlite3 .connect (OO0O0OOOOO00O0O00 [0 ])#line:1710
        OO00OO0O00OOO00OO =O0O0000OOOOOO0OO0 .cursor ()#line:1711
        xbmc .Player ().stop ()#line:1714
        while True :#line:1719
            OO00OO0O00OOO00OO .execute ("SELECT idFile FROM files WHERE strFilename LIKE ? ESCAPE '$'",(file ,))#line:1720
            OO0O00O0O00OO0OO0 =OO00OO0O00OOO00OO .fetchone ()#line:1721
            if OO0O00O0O00OO0OO0 !=None :#line:1722
                print (OO0O00O0O00OO0OO0 [0 ])#line:1723
                OO00OO0O00OOO00OO .execute ("UPDATE settings SET ViewMode = 6, PixelRatio = 0.5 WHERE idFile = ?",(OO0O00O0O00OO0OO0 [0 ],))#line:1724
                O0O0000OOOOOO0OO0 .commit ()#line:1725
                break #line:1726
            xbmc .sleep (100 )#line:1727
        OO00OO0O00OOO00OO .close ()#line:1731
def get_auro_link (O0OO0O000O0O000O0 ):#line:1732
   OO0O0000O0OOO0O0O ,OOO0O0O0O000O0O00 =read_site_html (O0OO0O000O0O000O0 )#line:1733
   O0OO00OO00000OOOO ="<source src=\"(.+?)\" type="#line:1734
   OOOOOO0O00O000OO0 =re .compile (O0OO00OO00000OOOO ).findall (OO0O0000O0OOO0O0O )#line:1735
   OOO0OOOO0O0OO0O00 =xbmcgui .Dialog ().select ("בחר מקור",OOOOOO0O00O000OO0 )#line:1736
   if OOO0OOOO0O0OO0O00 ==-1 :#line:1737
            sys .exit ()#line:1738
   return OOOOOO0O00O000OO0 [0 ].strip (" \n")+'|User-Agent=%s'%__USERAGENT__ #line:1739
def get_whole_link (OO0OOO0OO000000O0 ):#line:1741
    OO000OO00O00OO000 ,O0OOOOO0OO0O0O00O =read_site_html (OO0OOO0OO000000O0 )#line:1743
    OO000OO00OO0000OO ='<input type="hidden" name="stepkey" value="(.+?)"><Br>'#line:1744
    OOOOOOO0O0O00OOOO =re .compile (OO000OO00OO0000OO ).findall (OO000OO00O00OO000 )#line:1745
    O00000O00O0O00O0O ={'Host':'www.wholecloud.net','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-US,en;q=0.5','Referer':OO0OOO0OO000000O0 ,'Content-Type':'application/x-www-form-urlencoded','Connection':'keep-alive','Upgrade-Insecure-Requests':'1',}#line:1765
    OO0OOOO0OO0000O0O =[('stepkey',OOOOOOO0O0O00OOOO [0 ]),('submit','submit'),('ab','1'),]#line:1771
    O00000OOOOO0OO000 =requests .post (OO0OOO0OO000000O0 ,headers =O00000O00O0O00O0O ,data =OO0OOOO0OO0000O0O ).text #line:1773
    OO000OO00OO0000OO ="<source src=\"(.+?)\" type="#line:1776
    OOOOOOO0O0O00OOOO =re .compile (OO000OO00OO0000OO ).findall (O00000OOOOO0OO000 )#line:1777
    OOOO0O0O000O0OOOO =xbmcgui .Dialog ().select ("בחר מקור",OOOOOOO0O0O00OOOO )#line:1778
    if OOOO0O0O000O0OOOO ==-1 :#line:1779
            sys .exit ()#line:1780
    return OOOOOOO0O0O00OOOO [OOOO0O0O000O0OOOO ].strip (" \n")+'|User-Agent=%s'%__USERAGENT__ #line:1781
def get_vidlox (OO0O0OO0OOO0O0O0O ):#line:1782
   O000O0OO00O0O0O0O ,OO0O0OOO00OO000OO =read_site_html (OO0O0OO0OOO0O0O0O )#line:1783
   OOOO000OOOO000O00 ="sources:(.+?)]"#line:1785
   OOOO0OOO0OO0OOO0O =re .compile (OOOO000OOOO000O00 ).findall (O000O0OO00O0O0O0O )#line:1786
   OO00OOO0OO0O00O0O ='"(.+?)"'#line:1787
   O000000O0OOOO0OOO =re .compile (OO00OOO0OO0O00O0O ).findall (OOOO0OOO0OO0OOO0O [0 ])#line:1788
   OOO00000OOO0O0000 =xbmcgui .Dialog ().select ("בחר מקור",O000000O0OOOO0OOO )#line:1790
   if OOO00000OOO0O0000 ==-1 :#line:1791
            sys .exit ()#line:1792
   return O000000O0OOOO0OOO [OOO00000OOO0O0000 ].strip (" \n")+'|User-Agent=%s'%__USERAGENT__ #line:1795
def get_vidi (O00OO0O00O0OOO00O ):#line:1796
   from open import __getMediaLinkForGuest_vidzi #line:1797
   OO0OO0OOOO0OO0000 ,O00OO0O00O0OOO00O =__getMediaLinkForGuest_vidzi (O00OO0O00O0OOO00O )#line:1798
   return O00OO0O00O0OOO00O #line:1800
   OO0O00O0OO000O000 ,OO00O0OOO0O00O00O =read_site_html (O00OO0O00O0OOO00O )#line:1801
   OOO0OO0OO0O00OOOO ="sources:(.+?)]"#line:1803
   O0OO00OO0O00OO000 =re .compile (OOO0OO0OO0O00OOOO ).findall (OO0O00O0OO000O000 )#line:1804
   OO00000OOO0OOO00O ='file: "(.+?)"'#line:1805
   OO00O0000000OOOO0 =re .compile (OO00000OOO0OOO00O ).findall (O0OO00OO0O00OO000 [0 ])#line:1806
   O0O00O0O0O000OOO0 =xbmcgui .Dialog ().select ("בחר מקור",OO00O0000000OOOO0 )#line:1808
   if O0O00O0O0O000OOO0 ==-1 :#line:1809
            sys .exit ()#line:1810
   return OO00O0000000OOOO0 [O0O00O0O0O000OOO0 ].strip (" \n")+'|User-Agent=%s'%__USERAGENT__ #line:1813
def dailymotion (O00OOOO00O0000OO0 ):#line:1814
   O00O00000O000OO0O ,O0O000OOO0OOOO000 =read_site_html (O00OOOO00O0000OO0 )#line:1815
   O0000OO00O000OO00 ="var __PLAYER_CONFIG__ = (.+?);\n"#line:1817
   O0O00O0OOO0O0OOOO =re .compile (O0000OO00O000OO00 ).findall (O00O00000O000OO0O )#line:1818
   O0O0O0O000O0O0OO0 =json .loads (O0O00O0OOO0O0OOOO [0 ])#line:1820
   OO0000O00OOO00O00 =[]#line:1821
   OOOOO0O0OOO00OO00 =[]#line:1822
   OOOOOOO00O0O0000O =[]#line:1823
   for O0O0OOO0OOOO0O00O in O0O0O0O000O0O0OO0 ['metadata']['qualities']:#line:1824
       for O000O0O0O0O00O0O0 in O0O0O0O000O0O0OO0 ['metadata']['qualities'][O0O0OOO0OOOO0O00O ]:#line:1827
         OOOOOOO00O0O0000O .append ((O000O0O0O0O00O0O0 ['type'],O0O0OOO0OOOO0O00O ,O000O0O0O0O00O0O0 ['url']))#line:1829
   OOOOOOO00O0O0000O .sort (key =lambda O0O0O0O0OOO00OO00 :O0O0O0O0OOO00OO00 [1 ],reverse =True )#line:1830
   for O0O0OOO0OOOO0O00O in OOOOOOO00O0O0000O :#line:1831
         OO0000O00OOO00O00 .append ('[COLOR aqua]'+O0O0OOO0OOOO0O00O [0 ]+'[/COLOR]'+" - "+O0O0OOO0OOOO0O00O [1 ]+'p')#line:1832
         OOOOO0O0OOO00OO00 .append (O0O0OOO0OOOO0O00O [2 ])#line:1834
   OO0OO0000O0OOOOOO =xbmcgui .Dialog ()#line:1836
   OOOO0O0O0O0OOO000 =OO0OO0000O0OOOOOO .select ("Choose quality to play",OO0000O00OOO00O00 )#line:1837
   if OOOO0O0O0O0OOO000 !=-1 :#line:1838
        OO00OOOO0OOOOOO00 =OOOOO0O0OOO00OO00 [OOOO0O0O0O0OOO000 ]#line:1839
   else :#line:1840
     sys .exit ()#line:1841
   return OO00OOOO0OOOOOO00 #line:1842
def resolve_bitpor (OOOO0OOOOO0O0O00O ):#line:1843
    import cloudflare #line:1844
    O0O0OO0000000OOO0 ={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-US,en;q=0.5','Cache-Control':'no-cache','Connection':'keep-alive','Pragma':'no-cache','Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',}#line:1854
    O00O00O00OOO00O0O ,OO0OOO0O0OO000OO0 =cloudflare .request (OOOO0OOOOO0O0O00O )#line:1856
    O00000O0000O0OOOO ='<source src="(.+?)" type="video/mp4" data-res="(.+?)"'#line:1857
    O0OOO00000O0O0OO0 =re .compile (O00000O0000O0OOOO ).findall (O00O00O00OOO00O0O )#line:1859
    if len (O0OOO00000O0O0OO0 )==0 :#line:1860
       O00000O0000O0OOOO ="<source src=\"(.+?)\" type='video/mp4'.+?res='(.+?)'"#line:1861
       O0OOO00000O0O0OO0 =re .compile (O00000O0000O0OOOO ).findall (O00O00O00OOO00O0O )#line:1863
    OO0OO00OO0OOOO0OO =[]#line:1866
    OOO00O00O0O0O0OOO =[]#line:1867
    for O0OO0OO000OOO0O0O ,O0O0O0OOO0O0OOOOO in O0OOO00000O0O0OO0 :#line:1868
       if len (O0O0O0OOO0O0OOOOO )>1 :#line:1869
         if 'x'in O0O0O0OOO0O0OOOOO :#line:1870
           O0O0O0OOO0O0OOOOO =O0O0O0OOO0O0OOOOO .split ('x')[1 ]#line:1871
         OO0OO00OO0OOOO0OO .append (O0O0O0OOO0O0OOOOO )#line:1872
         OOO00O00O0O0O0OOO .append (O0OO0OO000OOO0O0O )#line:1873
    O0O0000OO0O0OOO00 =xbmcgui .Dialog ().select ("Choose quality to play",OO0OO00OO0OOOO0OO )#line:1875
    if O0O0000OO0O0OOO00 !=-1 :#line:1876
        return OOO00O00O0O0O0OOO [O0O0000OO0O0OOO00 ]#line:1877
    else :#line:1878
     sys .exit ()#line:1879
def fix_q (O000O000O0OO000O0 ):#line:1880
    if '1080'in O000O000O0OO000O0 :#line:1883
      O0OOOO0O00O00O0O0 =0 #line:1884
    elif '720'in O000O000O0OO000O0 :#line:1885
      O0OOOO0O00O00O0O0 =1 #line:1886
    elif '480'in O000O000O0OO000O0 :#line:1887
      O0OOOO0O00O00O0O0 =2 #line:1888
    elif '360'in O000O000O0OO000O0 or 'sd'in O000O000O0OO000O0 .lower ():#line:1890
      O0OOOO0O00O00O0O0 =3 #line:1891
    else :#line:1892
      O0OOOO0O00O00O0O0 =4 #line:1893
    return O0OOOO0O00O00O0O0 #line:1894
def streamango_decode (O000OO0OOOO000O00 ,O000OO0000OOOO00O ):#line:1895
        _OOOO00O00O00O00O0 =""#line:1897
        OOOOOO000000O0O00 ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='#line:1898
        OOOOOO000000O0O00 =OOOOOO000000O0O00 [::-1 ]#line:1899
        OOO0OOO00OOOOO0OO =0 #line:1901
        for OOOOO0O0OOOOOOOO0 in range (0 ,len (O000OO0OOOO000O00 )-1 ):#line:1903
            while OOO0OOO00OOOOO0OO <=len (O000OO0OOOO000O00 )-1 :#line:1904
                _O00O0O0OO000OOOO0 =OOOOOO000000O0O00 .index (O000OO0OOOO000O00 [OOO0OOO00OOOOO0OO ])#line:1905
                OOO0OOO00OOOOO0OO +=1 #line:1906
                _O00O0O0O00O000O00 =OOOOOO000000O0O00 .index (O000OO0OOOO000O00 [OOO0OOO00OOOOO0OO ])#line:1907
                OOO0OOO00OOOOO0OO +=1 #line:1908
                _O0OOO0O0O00OO000O =OOOOOO000000O0O00 .index (O000OO0OOOO000O00 [OOO0OOO00OOOOO0OO ])#line:1909
                OOO0OOO00OOOOO0OO +=1 #line:1910
                _O0OO000OO000O00O0 =OOOOOO000000O0O00 .index (O000OO0OOOO000O00 [OOO0OOO00OOOOO0OO ])#line:1911
                OOO0OOO00OOOOO0OO +=1 #line:1912
                _O0000OOOOO000000O =((_O00O0O0OO000OOOO0 <<2 )|(_O00O0O0O00O000O00 >>4 ))#line:1914
                _OO0O000000O0000OO =(((_O00O0O0O00O000O00 &15 )<<4 )|(_O0OOO0O0O00OO000O >>2 ))#line:1915
                _OO0O00000O0O00OOO =((_O0OOO0O0O00OO000O &3 )<<6 )|_O0OO000OO000O00O0 #line:1916
                _O0000OOOOO000000O =_O0000OOOOO000000O ^O000OO0000OOOO00O #line:1917
                _OOOO00O00O00O00O0 =str (_OOOO00O00O00O00O0 )+chr (_O0000OOOOO000000O )#line:1919
                if _O0OOO0O0O00OO000O !=64 :#line:1921
                    _OOOO00O00O00O00O0 =str (_OOOO00O00O00O00O0 )+chr (_OO0O000000O0000OO )#line:1922
                if _O0OOO0O0O00OO000O !=64 :#line:1923
                    _OOOO00O00O00O00O0 =str (_OOOO00O00O00O00O0 )+chr (_OO0O00000O0O00OOO )#line:1924
        return _OOOO00O00O00O00O0 #line:1926
def cloudflare_request(url, post=None, headers={}, mobile=False, safe=False,get_url=False, timeout=30):
    import run,urlparse
    parsed_uri = urlparse.urlparse( url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    if get_url:
        domain=url
    
    #print run.get_tokens_with_headers(domain,headers,get_url)
    if safe:
        
        x,token=cache.get(run.get_tokens_with_headers,0,domain,headers,get_url, table='cookies')
         
        
        if get_url:
            
            result= x
        else:
            result=requests.get(url,headers=token[1],cookies=token[0],timeout=10)   
            result=result.content
        
        
    else:
        run.get_tokens_with_headers(domain,headers,get_url)
        x,token=cache.get(run.get_tokens_with_headers,1,domain,headers,get_url, table='cookies')
       
        counter=0
        if 'jschl-answer' in x:
            x,token=cache.get(run.get_tokens_with_headers,1,url,headers,get_url, table='cookies')
        if 'jschl-answer' in x:
            
            while 'jschl-answer' in x:
                x,token=cache.get(run.get_tokens_with_headers,0,domain,headers,get_url, table='cookies')
                
                if get_url:
                    
                    result= x
                else:
                    result=requests.get(url,headers=token[1],cookies=token[0],timeout=10)   
                    
                    result=result.content
                    if 'jschl-answer' in result:
                        x=result
                counter+=1
                
                if counter>5:
                    return '',[]
        else:
               
            if get_url:
                
                result= x
            else:
            
                result=requests.get(url,headers=token[1],cookies=token[0],timeout=10)
                result=result.content
           
                if 'jschl-answer' in result:
                        
                        x,token=cache.get(run.get_tokens_with_headers,0,url,headers,get_url, table='cookies')
                        result=requests.get(url,headers=token[1],cookies=token[0],timeout=10)   
                    
                        result=result.content
        if x=='NOTCF':
            result=requests.get(url,headers=token[1],timeout=10)
            result=result.content
    return result,token
def resolve_streamango (O0O0OO00O00OOO00O ):#line:1929
        OOO0O0OOO0OO0OO0O =False #line:1930
        OO00OOOO000000O00 ={'Pragma':'no-cache','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Cache-Control':'no-cache','Connection':'keep-alive',}#line:1940
        OO0OO0OOO0O00OO0O =requests .get (O0O0OO00O00OOO00O ,headers =OO00OOOO000000O00 ).content #line:1942
        O0000OO00OO0O0O00 ="\"video/mp4\",src:d\('(.+?)',(.+?)\)"#line:1943
        O00O00O0OOO00OO00 =re .compile (O0000OO00OO0O0O00 ).findall (OO0OO0OOO0O00OO0O )#line:1944
        OO00O0OO00OOOOOOO ,OO0OOO0000O0OOO0O =O00O00O0OOO00OO00 [0 ]#line:1946
        if (O00O00O0OOO00OO00 ):#line:1950
            OOO0O0OOO0OO0OO0O =streamango_decode (OO00O0OO00OOOOOOO ,int (OO0OOO0000O0OOO0O ))#line:1951
            if OOO0O0OOO0OO0OO0O .endswith ('@'):#line:1952
              OOO0O0OOO0OO0OO0O =OOO0O0OOO0OO0OO0O [:-1 ]#line:1953
            OOO0O0OOO0OO0OO0O ='http:'+OOO0O0OOO0OO0OO0O #line:1954
            return OOO0O0OOO0OO0OO0O #line:1957
def resolver (OOO00O00O00OOO00O ):#line:1958
  subs=None
  OOO00O00O00OOO00O =OOO00O00O00OOO00O .strip ()#line:1962
  OOO00O00O00OOO00O =OOO00O00O00OOO00O .replace (' ','%20')#line:1963
  if 'rtmp'not in OOO00O00O00OOO00O and 'estream'not in OOO00O00O00OOO00O :#line:1965
    OO00OO00O00OO0OOO =1 #line:1968
  if 'upfile'in OOO00O00O00OOO00O or 'www.upf.co.il'in OOO00O00O00OOO00O :#line:1969
   O0O0000OOO000O00O ,OOO00O00O00OOO00O =get_upfile_det (OOO00O00O00OOO00O )#line:1970
  elif 'https://vidzi.tv/'in OOO00O00O00OOO00O :#line:1971
    OOO00O00O00OOO00O =get_vidi (OOO00O00O00OOO00O )#line:1972
  elif 'vidlox.tv'in OOO00O00O00OOO00O :#line:1973
    OOO00O00O00OOO00O =get_vidlox (OOO00O00O00OOO00O )#line:1974
  elif 'https://www.wholecloud.net'in OOO00O00O00OOO00O :#line:1975
    OOO00O00O00OOO00O =get_whole_link (OOO00O00O00OOO00O )#line:1976
  elif 'http://www.auroravid.to'in OOO00O00O00OOO00O :#line:1979
    OOO00O00O00OOO00O =get_auro_link (OOO00O00O00OOO00O )#line:1980
  elif 'myfile'in OOO00O00O00OOO00O :#line:1981
     OOO00O00O00OOO00O =(play_myfile (OOO00O00O00OOO00O ))#line:1983
  elif 'dailymotion.com'in OOO00O00O00OOO00O :#line:1984
     OOO00O00O00OOO00O =(dailymotion (OOO00O00O00OOO00O ))#line:1986
  elif 'vidto.me'in OOO00O00O00OOO00O :#line:1987
      from vidtodo import __get_vidto #line:1988
      if 'embed'in OOO00O00O00OOO00O :#line:1990
              OOO000OOOO000O000 ='vidto.me/embed-(.+?)-'#line:1991
              OO000OO0OO00O0O0O =re .compile (OOO000OOOO000O000 ).findall (OOO00O00O00OOO00O )[0 ]#line:1992
              OOO00O00O00OOO00O ='http://vidto.me/%s.html'%OO000OO0OO00O0O0O #line:1993
      OOO00O00O00OOO00O =__get_vidto (OOO00O00O00OOO00O )[1 ]#line:1994
  elif 'vidtodo'in OOO00O00O00OOO00O :#line:1995
      from vidtodo import VidToDoResolver #line:1996
      OOO00O00O00OOO00O =VidToDoResolver (OOO00O00O00OOO00O )#line:1997
  elif 'streamango'in OOO00O00O00OOO00O :#line:1998
      OOO00O00O00OOO00O =resolve_streamango (OOO00O00O00OOO00O )#line:1999
  elif 'https://dood' in OOO00O00O00OOO00O:
        import resolveurl
                

        OOO00O00O00OOO00O = resolveurl.HostedMediaFile(url=OOO00O00O00OOO00O).resolve()
        '''
        headers = {
            'authority': 'dood.to',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'iframe',
            'referer': OOO00O00O00OOO00O,
            'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
           }
        OOO00O00O00OOO00O=OOO00O00O00OOO00O.replace('/d/','/e/')
        logging.warning(OOO00O00O00OOO00O)
        x=requests.get(OOO00O00O00OOO00O,headers=headers).content.decode('utf-8')
        regex="'/pass_md5/(.+?)'"

        m=re.compile(regex,re.DOTALL).findall(x)
        x=requests.get('https://dood.to/pass_md5/'+m[0],headers=headers).content.decode('utf-8')
        
        logging.warning(x)
        tokens=m[0].split('/')
        token=tokens[len(tokens)-1]
        expiry=int(time.time()*1000)
        
        a='?token=5trtb3h06c50mgjd5yih06se&expiry=1596976834003'
        a='?token=%s&expiry=%s'%(token,expiry)
        logging.warning(a)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
            'Accept-Language': 'en-US,en;q=0.5',
           
            'Connection': 'keep-alive',
            'Referer': OOO00O00O00OOO00O,
        }
        OOO00O00O00OOO00O= x+a+"|"+ url_encode(headers)
        
        
        '''
  elif 'rapid'in OOO00O00O00OOO00O :#line:2000
      from raptu import resolve #line:2001
      O0000OO0O000O00O0 =xbmcgui .Dialog ()#line:2002
      O0OOO0O00OOO0OOO0 =resolve (OOO00O00O00OOO00O )#line:2003
      O00OO0OO0000O000O =O0OOO0O00OOO0OOO0 ['videos']#line:2005
      O000O00OOOO000000 =O0OOO0O00OOO0OOO0 ['subs']#line:2006
      OOOO0OO0OO00O0000 =sorted ([_O0OOOOOOOOOOO0O0O .encode ("UTF8")for _O0OOOOOOOOOOO0O0O in O00OO0OO0000O000O .keys ()],key =lambda _O0OO00OO000O000OO :int (filter (str .isdigit ,_O0OO00OO000O000OO )))#line:2008
      if '777'in OOOO0OO0OO00O0000 :#line:2009
        OOO00O00O00OOO00O =O00OO0OO0000O000O ['777']#line:2011
      else :#line:2012
          if Addon .getSetting ("auto_q")=='true':#line:2013
            O0O0O000O0O000000 =OOOO0OO0OO00O0000 [0 ]#line:2014
            O0000OO00O0OO0OOO =int (Addon .getSetting ("quality"))#line:2015
            OOO0OOO000OO00O0O =0 #line:2017
            O0OO000O00O0OO000 =[]#line:2018
            for O0O00O0O0O00OOO00 in OOOO0OO0OO00O0000 :#line:2019
               if fix_q (O0O00O0O0O00OOO00 )<O0000OO00O0OO0OOO :#line:2021
                 O0OO000O00O0OO000 .append (OOO0OOO000OO00O0O )#line:2023
               OOO0OOO000OO00O0O +=1 #line:2024
            OO0O000000O000OOO =0 #line:2025
            OOOOO0O0OOOO0OO00 =[]#line:2026
            for O0O00O0O0O00OOO00 in OOOO0OO0OO00O0000 :#line:2027
                 if OO0O000000O000OOO not in O0OO000O00O0OO000 :#line:2028
                  OOOOO0O0OOOO0OO00 .append (O0O00O0O0O00OOO00 )#line:2029
                 OO0O000000O000OOO +=1 #line:2030
            OOOO0OO0OO00O0000 =OOOOO0O0OOOO0OO00 #line:2031
            if len (OOOO0OO0OO00O0000 )>0 :#line:2032
              O0O0O000O0O000000 =OOOO0OO0OO00O0000 [len (OOOO0OO0OO00O0000 )-1 ]#line:2033
            OOO00O00O00OOO00O =O00OO0OO0000O000O [O0O0O000O0O000000 ]#line:2035
          else :#line:2036
              O0O0OOOO0O0OOO0O0 =O0000OO0O000O00O0 .select ("Choose quality to play",OOOO0OO0OO00O0000 )#line:2037
              if O0O0OOOO0O0OOO0O0 !=-1 :#line:2038
                OOO00O00O00OOO00O =O00OO0OO0000O000O [OOOO0OO0OO00O0000 [O0O0OOOO0O0OOO0O0 ]]#line:2039
              else :#line:2040
                sys .exit ()#line:2041
      if len (O000O00OOOO000000 .values ())>0 :#line:2042
        OOO00O00O00OOO00O =OOO00O00O00OOO00O +'%%%%'+O000O00OOOO000000 .values ()[0 ]#line:2043
  elif 'google'in OOO00O00O00OOO00O and 'video-downloads'not in OOO00O00O00OOO00O and 'doc-'not in OOO00O00O00OOO00O :#line:2044
      if '='in OOO00O00O00OOO00O :#line:2046
        OO000OO0OO00O0O0O =OOO00O00O00OOO00O .split ('=')[-1 ]#line:2047
      else :#line:2049
       OOO000OOOO000O000 ='/d/(.+?)/view'#line:2050
       OO000OOOOO0O0000O =re .compile (OOO000OOOO000O000 ).findall (OOO00O00O00OOO00O )#line:2051
       if len (OO000OOOOO0O0000O )>0 :#line:2052
         OO000OO0OO00O0O0O =OO000OOOOO0O0000O [0 ]#line:2053
       else :#line:2054
         OOO000OOOO000O000 ='/d/(.+?)/preview'#line:2055
         OO000OOOOO0O0000O =re .compile (OOO000OOOO000O000 ).findall (OOO00O00O00OOO00O )#line:2056
         OO000OO0OO00O0O0O =OO000OOOOO0O0000O [0 ]#line:2057
      dir_path = os.path.dirname(os.path.realpath(__file__))
      f_dir=os.path.join(dir_path,'accounts.db')
      if os.path.exists(f_dir):
        OOO00O00O00OOO00O,subs =googledrive_resolve (OO000OO0OO00O0O0O )#line:2058
      else:
        OOO00O00O00OOO00O =googledrive_resolve_old (OO000OO0OO00O0O0O )#line:2058
  elif 'www.you'in OOO00O00O00OOO00O :#line:2059
    if 'list'in OOO00O00O00OOO00O :#line:2061
      if Addon .getSetting ("youtube")=="0":#line:2063
          OOOO000OO000O0OOO =xbmc .PlayList (xbmc .PLAYLIST_VIDEO )#line:2064
          OOOO000OO000O0OOO .clear ()#line:2065
          O00000000O000O0O0 =OOO00O00O00OOO00O .split ('list=')[1 ]#line:2066
          OOO00O00O00OOO00O =get_all_youtube_items (name ,OOO00O00O00OOO00O ,OOOO000OO000O0OOO )#line:2067
      else :#line:2069
          O00000000O000O0O0 ='playlistId@@@@'+OOO00O00O00OOO00O .replace ('https://www.youtube.com',"").replace ("=","@@@@@@").replace ("&","*****").replace ("?","!!!!!!")#line:2070
          OOO00O00O00OOO00O ='plugin://plugin.video.MyYoutube/?mode=3&name=%s&url=%s'%(name ,O00000000O000O0O0 )#line:2071
    else :#line:2073
       if Addon .getSetting ("youtube")=="0":#line:2074
          O00000000O000O0O0 =OOO00O00O00OOO00O .split ('v=')[1 ]#line:2075
          OOO00O00O00OOO00O ='plugin://plugin.video.youtube/play/?video_id=%s'%O00000000O000O0O0 #line:2076
       else :#line:2077
          O00000000O000O0O0 ='videoid@@@@'+OOO00O00O00OOO00O .replace ('https://www.youtube.com',"").replace ("=","@@@@@@").replace ("&","*****").replace ("?","!!!!!!")#line:2078
          OOO00O00O00OOO00O ='plugin://plugin.video.MyYoutube/?mode=3&name=%s&url=%s'%(name ,O00000000O000O0O0 )#line:2079
  elif ('openload'in OOO00O00O00OOO00O or 'oload.stream'in OOO00O00O00OOO00O or 'oload.win'in OOO00O00O00OOO00O or 'oload.download'in OOO00O00O00OOO00O ):#line:2080
      if Addon .getSetting ("vummo3")=='1':#line:2081
        OOO0OOO000OOOO0O0 =requests .get ('https://www.saveitoffline.com/process/?url='+que (OOO00O00O00OOO00O )).json ()#line:2083
        if 'urls'in OOO0OOO000OOOO0O0 :#line:2085
         if len (OOO0OOO000OOOO0O0 ['urls'])>0 :#line:2086
            OOO00O00O00OOO00O =OOO0OOO000OOOO0O0 ['urls'][0 ]['id']#line:2087
      elif Addon .getSetting ("vummo3")=='0':#line:2088
       xbmc .executebuiltin ((u'Notification(%s,%s)'%('EverySource','Vimoo Source')).encode ('utf-8'))#line:2089
       from open import getMediaLinkForGuest #line:2090
       O0OOOOO0O0OOO00OO =getMediaLinkForGuest (OOO00O00O00OOO00O )#line:2091
       OOO00O00O00OOO00O =O0OOOOO0O0OOO00OO #line:2093
       xbmc .executebuiltin ((u'Notification(%s,%s)'%('EverySource','[COLOR lighgreen]Vimoo OK[/COLOR]')).encode ('utf-8'))#line:2094
      else :#line:2095
       xbmc .executebuiltin ((u'Notification(%s,%s)'%('EverySource','Vimoo Source')).encode ('utf-8'))#line:2096
       from open_new import getMediaLinkForGuest_new #line:2098
       O0OOOOO0O0OOO00OO =getMediaLinkForGuest_new (OOO00O00O00OOO00O )#line:2099
       OOO00O00O00OOO00O =O0OOOOO0O0OOO00OO #line:2101
       xbmc .executebuiltin ((u'Notification(%s,%s)'%('EverySource','[COLOR lighgreen]Vimoo OK[/COLOR]')).encode ('utf-8'))#line:2102
       '''
       import requests
       Domain=Addon.getSetting("server")
       En_Domain=Addon.getSetting("serveroption")
       if 'openload' in url and  len(Domain)>0 and En_Domain=='true':
           if 'http' not in Domain:
                  Domain='http://'+Domain
           new_serv=Domain+":8080/GetVideoUrl?url="+(url)
           new_serv=new_serv.replace("openload.co",'oload.stream').replace("embed",'f')

           try:
             
               x=requests.get(new_serv, timeout=70).content
               regex='>(.+?)<'
               link=re.compile(regex).findall(x)[0]
               
         
                       
           except:
                import resolveurl
                try:

                    videoPlayListUrl = resolveurl.HostedMediaFile(url=link).resolve()
                    match=videoPlayListUrl.split("/")[-1]
                    link=videoPlayListUrl.replace(match,que(match))
                    
                except:
               
                 link=link
       '''#line:2132
  elif 'bitporno'in OOO00O00O00OOO00O or 'estream'in OOO00O00O00OOO00O :#line:2133
     OOO00O00O00OOO00O =resolve_bitpor (OOO00O00O00OOO00O )#line:2135
  elif 'letsupload'in OOO00O00O00OOO00O :#line:2137
         
         
         
         O00O000O0O000OO00 ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0','Accept':'application/json, text/javascript, */*; q=0.01','Accept-Language':'en-US,en;q=0.5','Referer':'https://letsupload.co/search.html','X-Requested-With':'XMLHttpRequest','Connection':'keep-alive','Pragma':'no-cache','Cache-Control':'no-cache',}#line:2147
         OOO000OOOO000O000 ='https://letsupload.co/(.+?)/'#line:2148
         OOOO00O0OO00O0000 =re .compile (OOO000OOOO000O000 ).findall (OOO00O00O00OOO00O )[0 ]#line:2149
         O0000O0OO0O0O00O0 ='http://letsupload.co/plugins/mediaplayer/site/_embed.php?u=%s&w=1920&h=1080'%OOOO00O0OO00O0000 #line:2151
         OO0O0O000OO0000O0 ,cookie=cloudflare_request (O0000O0OO0O0O00O0 ,headers =O00O000O0O000OO00 ) #line:2153
         OOO000OOOO000O000 ='file: "(.+?)"'#line:2154
         OO000OOOOO0O0000O =re .compile (OOO000OOOO000O000 ).findall (OO0O0O000OO0000O0 )#line:2155
         if len (OO000OOOOO0O0000O )==0 :#line:2156
            OOO000OOOO000O000 ='<embed.+?src="(.+?)"'#line:2157
            OOO00O00O00OOO00O =re .compile (OOO000OOOO000O000 ,re .DOTALL ).findall (OO0O0O000OO0000O0 )[0 ]#line:2158
         else :#line:2159
            OOO00O00O00OOO00O =OO000OOOOO0O0000O [0 ]#line:2160
  elif 'moviefiles.org'in OOO00O00O00OOO00O :#line:2161
        O00O000O0O000OO00 =[('Host','moviefiles.org'),('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv,60.0) Gecko/20100101 Firefox/60.0'),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),('Accept-Language','en-US,en;q=0.5'),('Connection','keep-alive'),('Upgrade-Insecure-Requests','1'),('Pragma','no-cache'),('Cache-Control','no-cache'),]#line:2171
        from cookielib import CookieJar #line:2172
        O0O00OOOOOOOOO0O0 =CookieJar ()#line:2174
        O0O00OOOOO0OOOO0O =urllib2 .build_opener (urllib2 .HTTPCookieProcessor (O0O00OOOOOOOOO0O0 ))#line:2175
        O0O00OOOOO0OOOO0O .addheaders =(O00O000O0O000OO00 )#line:2177
        O0O00O0OOO00O0OOO =O0O00OOOOO0OOOO0O .open (OOO00O00O00OOO00O )#line:2178
        O00O000O0O000OO00 ={'Host':'moviefiles.org','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-US,en;q=0.5','Connection':'keep-alive','Upgrade-Insecure-Requests':'1','Pragma':'no-cache','Cache-Control':'no-cache',}#line:2192
        OO0OOOOOOO00OO0OO =requests .get (OOO00O00O00OOO00O ,headers =O00O000O0O000OO00 ,cookies =O0O00OOOOOOOOO0O0 ).content #line:2195
        OOO000OOOO000O000 ="<p><a href='(.+?)'"#line:2198
        OOO00O00O00OOO00O =re .compile (OOO000OOOO000O000 ).findall (OO0OOOOOOO00OO0OO )[0 ]#line:2199
  elif 'sratim-il.com'in OOO00O00O00OOO00O :#line:2201
          logging .warning ('resolveing sratim')#line:2202
          OOO000OOOO000O000 ='/(.+?).mp4'#line:2203
          OO000OOOOO0O0000O =re .compile (OOO000OOOO000O000 ).findall (OOO00O00O00OOO00O )#line:2204
          OOO000OOOO000O000 ='//(.+?)/'#line:2205
          OO00O00O00O0OO000 =re .compile (OOO000OOOO000O000 ).findall (OOO00O00O00OOO00O )[0 ]#line:2206
          class OOO00OOOO00OO0OO0 :#line:2207
                 name =''#line:2208
                 value =''#line:2209
          O00O000O0O000OO00 ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0','Accept':'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5','Accept-Language':'en-US,en;q=0.5','Host':OO00O00O00O0OO000 ,'Connection':'keep-alive','Pragma':'no-cache','Cache-Control':'no-cache',}#line:2220
          OOO0OOO000OOOO0O0 =requests .get (OOO00O00O00OOO00O .replace ('.mp4','')+'/',headers =O00O000O0O000OO00 ,verify =False ).cookies #line:2221
          for OOO00OOOO00OO0OO0 in OOO0OOO000OOOO0O0 :#line:2222
              logging .warning (OOO00OOOO00OO0OO0 .name )#line:2223
              logging .warning (OOO00OOOO00OO0OO0 .value )#line:2224
          O00O000O0O000OO00 ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0','Accept':'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5','Accept-Language':'en-US,en;q=0.5','Referer':'https://www.sratim.co/'+OO000OOOOO0O0000O [0 ],'Host':OO00O00O00O0OO000 ,'Connection':'keep-alive','Pragma':'no-cache','Cache-Control':'no-cache',}#line:2236
          O0OOOO000000O00OO =urllib .urlencode (O00O000O0O000OO00 )#line:2237
          OOO00O00O00OOO00O =OOO00O00O00OOO00O +"|"+O0OOOO000000O00OO #line:2238
  elif 'm3u8'not in url and 'rtmp'not in OOO00O00O00OOO00O :#line:2240
    import resolveurl #line:2242
    try :#line:2243
        OO0OOO0OOOO0O00O0 =resolveurl .HostedMediaFile (url =OOO00O00O00OOO00O ).resolve ()#line:2245
        OO000OOOOO0O0000O =OO0OOO0OOOO0O00O0 .split ("/")[-1 ]#line:2246
        OOO00O00O00OOO00O =OO0OOO0OOOO0O00O0 .replace (OO000OOOOO0O0000O ,que (OO000OOOOO0O0000O ))#line:2247
    except :#line:2249
       OOO00O00O00OOO00O =OOO00O00O00OOO00O #line:2250
  return OOO00O00O00OOO00O .replace (' ','%20'),subs#line:2252
def update_view (O00OO0O0O00O0OO0O ):#line:2253
    OO00O0OOOO0000OOO =True #line:2255
    logging .warning ('Container.Update(%s)'%O00OO0O0O00O0OO0O )#line:2256
    xbmc .executebuiltin ('Container.Update(%s)'%O00OO0O0O00O0OO0O )#line:2257
    xbmc .sleep (500 )#line:2259
    xbmc .executebuiltin ('Dialog.Close(okdialog, true)')#line:2261
    xbmc .sleep (500 )#line:2262
    xbmc .executebuiltin ('Dialog.Close(okdialog, true)')#line:2264
    xbmc .sleep (500 )#line:2265
    xbmc .executebuiltin ('Dialog.Close(okdialog, true)')#line:2267
    xbmc .sleep (500 )#line:2268
    xbmc .executebuiltin ('Dialog.Close(okdialog, true)')#line:2270
    xbmc .sleep (500 )#line:2271
    xbmc .executebuiltin ('Dialog.Close(okdialog, true)')#line:2273
    xbmc .sleep (500 )#line:2274
    xbmc .executebuiltin ('Dialog.Close(okdialog, true)')#line:2276
    xbmc .sleep (5000 )#line:2277
    xbmc .executebuiltin ('Dialog.Close(okdialog, true)')#line:2279
    logging .warning ('DONE JUMP')#line:2280
    return OO00O0OOOO0000OOO #line:2281
def get_links (OOO00O0O0000O000O ,OOO00000O00O0OO0O ,O0OO0O000O0O0O00O ):#line:2283
    import nanscrapers ,resolveurl #line:2284
    O0OO0O000O0O0O00O =O0OO0O000O0O0O00O .replace ('[',' ').replace (']',' ').replace ('	','').replace ("\\"," ").replace (': """",',': "" "",').replace (': """"}',': "" ""}').replace (': "",',': " ",').replace (': ""}',': " "}').replace ('""','"').replace ('\n','').replace ('\r','')#line:2285
    OO000O0OOOOOOOO0O =json .loads (O0OO0O000O0O0O00O )#line:2286
    def O00O0O0000000O0OO (OOOO0OO000OO0O0O0 ):#line:2288
            OO0000O00O0OOO0O0 =OOOO0OO000OO0O0O0 [1 ][0 ]["quality"]#line:2289
            if OO0000O00O0OOO0O0 =="1080":OO0000O00O0OOO0O0 ="HDa"#line:2290
            if OO0000O00O0OOO0O0 =="720":OO0000O00O0OOO0O0 ="HDb"#line:2291
            if OO0000O00O0OOO0O0 =="560":OO0000O00O0OOO0O0 ="HDc"#line:2292
            if OO0000O00O0OOO0O0 =="HD":OO0000O00O0OOO0O0 ="HDd"#line:2293
            if OO0000O00O0OOO0O0 =="480":OO0000O00O0OOO0O0 ="SDa"#line:2294
            if OO0000O00O0OOO0O0 =="360":OO0000O00O0OOO0O0 ="SDb"#line:2295
            if OO0000O00O0OOO0O0 =="SD":OO0000O00O0OOO0O0 ="SDc"#line:2296
            return OO0000O00O0OOO0O0 #line:2298
    if 'tvshow'in O0OO0O000O0O0O00O :#line:2299
      O00OOO00000OOOO00 =nanscrapers .scrape_episode_with_dialog (OO000O0OOOOOOOO0O ['originaltitle'],OO000O0OOOOOOOO0O ['year'],int (OO000O0OOOOOOOO0O ['year']),int (OO000O0OOOOOOOO0O ['Season']),int (OO000O0OOOOOOOO0O ['Episode']),OO000O0OOOOOOOO0O ['imdbnumber'],None )#line:2302
    else :#line:2304
      O00OOO00000OOOO00 =nanscrapers .scrape_movie_with_dialog (OO000O0OOOOOOOO0O ['originaltitle'],OO000O0OOOOOOOO0O ['year'],OO000O0OOOOOOOO0O ['imdbnumber'],timeout =600 ,sort_function =O00O0O0000000O0OO )#line:2305
    if O00OOO00000OOOO00 is False :#line:2306
        xbmcgui .Dialog ().ok ("Movie not found","No Links Found for "+OOO00O0O0000O000O +" ("+year +")")#line:2307
    else :#line:2308
        if O00OOO00000OOOO00 :#line:2309
            OOO00000O00O0OO0O =O00OOO00000OOOO00 ['url']#line:2310
            return OOO00000O00O0OO0O #line:2311
def dis_or_enable_addon (OOO00O0O000OO000O ,enable ="true"):#line:2312
    import json #line:2313
    OOO0000OOOOOOOOOO ='"%s"'%OOO00O0O000OO000O #line:2314
    if xbmc .getCondVisibility ("System.HasAddon(%s)"%OOO00O0O000OO000O )and enable =="true":#line:2315
        return xbmc .log ("### Skipped %s, reason = allready enabled"%OOO00O0O000OO000O )#line:2317
    elif not xbmc .getCondVisibility ("System.HasAddon(%s)"%OOO00O0O000OO000O )and enable =="false":#line:2318
        return xbmc .log ("### Skipped %s, reason = not installed"%OOO00O0O000OO000O )#line:2319
    else :#line:2320
        OOO00O0O00O00O0OO ='{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{"addonid":%s,"enabled":%s}}'%(OOO0000OOOOOOOOOO ,enable )#line:2321
        OOOO00O0O0O0OO00O =xbmc .executeJSONRPC (OOO00O0O00O00O0OO )#line:2322
        O00OOO00000OO0OOO =json .loads (OOOO00O0O0O0OO00O )#line:2323
        if enable =="true":#line:2324
            xbmc .log ("### Enabled %s, response = %s"%(OOO00O0O000OO000O ,O00OOO00000OO0OOO ))#line:2325
        else :#line:2326
            xbmc .log ("### Disabled %s, response = %s"%(OOO00O0O000OO000O ,O00OOO00000OO0OOO ))#line:2327
    return xbmc .executebuiltin ('Container.Update(%s)'%xbmc .getInfoLabel ('Container.FolderPath'))#line:2328
def downloader_is (OOOO0000OO0OOOO00 ,OO0OO0O0OOOO0O000 ,OOOOOOOOO00OO00O0 ):#line:2329
 import downloader ,extract #line:2330
 OOOO0OO0O000O0OO0 =xbmc .getInfoLabel ("System.ProfileName")#line:2331
 O0O000O000O0O0O0O =xbmc .translatePath (os .path .join ('special://home',''))#line:2332
 OO0000OO0O0OO0OO0 =xbmcgui .Dialog ()#line:2333
 if OO0OO0O0OOOO0O000 .find ('repo')<0 and OOOOOOOOO00OO00O0 =='yes':#line:2334
     O0000OO000OO000O0 =OO0000OO0O0OO0OO0 .yesno ("XBMC ISRAEL","Yes to install",OO0OO0O0OOOO0O000 )#line:2335
 else :#line:2336
     O0000OO000OO000O0 =True #line:2337
 if O0000OO000OO000O0 :#line:2338
  OOOOO00O00OO000O0 =xbmc .translatePath (os .path .join ('special://home/addons','packages'))#line:2339
  O00OOOOOOOO00OOO0 =xbmcgui .DialogProgress ()#line:2340
  O00OOOOOOOO00OOO0 .create ("XBMC ISRAEL","Downloading "+OO0OO0O0OOOO0O000 ,'','Please Wait')#line:2341
  O0OOOO00O000O0O0O =os .path .join (OOOOO00O00OO000O0 ,'isr.zip')#line:2342
  try :#line:2343
     os .remove (O0OOOO00O000O0O0O )#line:2344
  except :#line:2345
      pass #line:2346
  downloader .download (OOOO0000OO0OOOO00 ,O0OOOO00O000O0O0O ,OO0OO0O0OOOO0O000 ,O00OOOOOOOO00OOO0 )#line:2347
  OOO0O0O0000O0O000 =xbmc .translatePath (os .path .join ('special://home','addons'))#line:2348
  O00OOOOOOOO00OOO0 .update (0 ,OO0OO0O0OOOO0O000 ,"Extracting Zip Please Wait")#line:2349
  extract .all (O0OOOO00O000O0O0O ,OOO0O0O0000O0O000 ,O00OOOOOOOO00OOO0 )#line:2351
  O00OOOOOOOO00OOO0 .update (0 ,OO0OO0O0OOOO0O000 ,"Downloading")#line:2352
  O00OOOOOOOO00OOO0 .update (0 ,OO0OO0O0OOOO0O000 ,"Extracting Zip Please Wait")#line:2353
  xbmc .executebuiltin ('UpdateLocalAddons ')#line:2354
  xbmc .executebuiltin ("UpdateAddonRepos")#line:2355
def install_package (O0000OO0OOO00OOO0 ,O000OOOO0OO0OOO00 ):#line:2357
    O00O0O00OOOO00OO0 =xbmcgui .Dialog ()#line:2358
    O0OOO0OOOOOO0OOO0 =O00O0O00OOOO00OO0 .yesno (c_addon_name ,'','[B][COLOR red]Install %s[/COLOR][/B]'%O0000OO0OOO00OOO0 )#line:2359
    if O0OOO0OOOOOO0OOO0 :#line:2360
      downloader_is (O000OOOO0OO0OOO00 ,O0000OO0OOO00OOO0 ,"No")#line:2361
      OOO0000OOOO000O0O =O000OOOO0OO0OOO00 .split ('/')#line:2362
      if '-'in OOO0000OOOO000O0O :#line:2364
        OOO0000OOOO000O0O =OOO0000OOOO000O0O [len (OOO0000OOOO000O0O )-1 ].split ("-")[0 ]#line:2365
      else :#line:2366
        OOO0000OOOO000O0O =OOO0000OOOO000O0O .replace ('.zip','')#line:2367
      dis_or_enable_addon (OOO0000OOOO000O0O )#line:2369
      dis_or_enable_addon (O0000OO0OOO00OOO0 .rstrip ('\r\n'))#line:2379
      time .sleep (10 )#line:2380
      xbmc .executebuiltin ('SendClick(yesnodialog,11)')#line:2381
def unshorten_url (O0OO0000O0O00OOOO ):#line:2385
    import urlparse ,httplib #line:2386
    OOO0O000OO0OOOO00 =urlparse .urlparse (O0OO0000O0O00OOOO )#line:2387
    O00000O00OO0OOOOO =httplib .HTTPConnection (OOO0O000OO0OOOO00 .netloc )#line:2388
    O00000O00OO0OOOOO .request ('HEAD',OOO0O000OO0OOOO00 .path )#line:2389
    OOOO00OOOO0O00000 =O00000O00OO0OOOOO .getresponse ()#line:2390
    if OOOO00OOOO0O00000 .status /100 ==3 and OOOO00OOOO0O00000 .getheader ('Location'):#line:2391
        return OOOO00OOOO0O00000 .getheader ('Location')#line:2392
    else :#line:2393
        return O0OO0000O0O00OOOO #line:2394
def getall_youtube (OO00000O0OOO000OO ,OOOO0O0O00OO00OO0 ,OOOO0OO0000OO0000 ):#line:2395
     O0O0O0000000OOO0O =0 #line:2396
     O0OO000O00OO0OO0O =0 #line:2397
     while (O0O0O0000000OOO0O ==0 ):#line:2398
          if 'items'not in OO00000O0OOO000OO :#line:2399
            return None #line:2400
          for O00O0O00O00OO000O in OO00000O0OOO000OO ['items']:#line:2401
                 OO0O00O0OOO00OOOO =xbmcgui .ListItem (O00O0O00O00OO000O ['snippet']['title'],thumbnailImage =' ')#line:2403
                 OO0O00O0OOO00OOOO .setInfo ('video',{'Title':O00O0O00O00OO000O ['snippet']['title']})#line:2404
                 O000O0O00000OO00O ='plugin://plugin.video.youtube/play/?video_id=%s'%(O00O0O00O00OO000O ['snippet']['resourceId']['videoId'])#line:2405
                 OOOO0O0O00OO00OO0 .add (url =O000O0O00000OO00O ,listitem =OO0O00O0OOO00OOOO ,index =O0OO000O00OO0OO0O )#line:2407
                 O0OO000O00OO0OO0O =O0OO000O00OO0OO0O +1 #line:2409
          if 'nextPageToken'in OO00000O0OOO000OO :#line:2410
             O000OO0OOOOOO00OO ='https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s&maxResults=50&pageToken=%s&key=AIzaSyClvQA4Zjs3ZwWBkjVG4hlMrT98JnINDII'%(OOOO0OO0000OO0000 ,OO00000O0OOO000OO ['nextPageToken'])#line:2412
             OO00000O0OOO000OO =requests .get (O000OO0OOOOOO00OO ).json ()#line:2413
          else :#line:2415
             O0O0O0000000OOO0O =1 #line:2416
     OOOO0O0O00OO00OO0 .shuffle ()#line:2417
def get_all_youtube_items3 (OO0O0O00OOO000OO0 ,OO000OOO000O000OO ,O0000O0O0O0000000 ):#line:2418
    O0O0OO00000O0OOOO =OO000OOO000O000OO .split ('list=')[1 ]#line:2419
    return 'plugin://plugin.video.youtube/play/?playlist_id=%s&order=shuffle'%O0O0OO00000O0OOOO #line:2420
def get_all_youtube_items2 (OO000000OO000O000 ,OO0OOO00O0OOOOO0O ,O00OOOO0OOO00O0OO ):#line:2421
     O000O00O000O0OOO0 =OO0OOO00O0OOOOO0O .split ('list=')[1 ]#line:2423
     O0000O0OO0O000OO0 ='https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s&maxResults=50&key=AIzaSyClvQA4Zjs3ZwWBkjVG4hlMrT98JnINDII'%O000O00O000O0OOO0 #line:2425
     O0OO0OOO0OO0OO00O =requests .get (O0000O0OO0O000OO0 ).json ()#line:2427
     threading .Thread (target =getall_youtube ,args =(O0OO0OOO0OO0OO00O ,O00OOOO0OOO00O0OO ,O000O00O000O0OOO0 )).start ()#line:2429
     if 'items'in O0OO0OOO0OO0OO00O :#line:2431
       return ('plugin://plugin.video.youtube/play/?video_id=%s'%(O0OO0OOO0OO0OO00O ['items'][0 ]['snippet']['resourceId']['videoId']))#line:2432
     else :#line:2433
       return 'playlist_all'#line:2434
def getPlaylistUrlID (OO00000OO0OOOOOO0 ):#line:2435
    if 'list='in OO00000OO0OOOOOO0 :#line:2436
        OO0O0O0OOOO000000 =OO00000OO0OOOOOO0 .index ('=')+1 #line:2437
        OOO0OOO00OOO00OOO =OO00000OO0OOOOOO0 [OO0O0O0OOOO000000 :]#line:2438
        if '&'in OO00000OO0OOOOOO0 :#line:2439
            OO0000O00OO0O000O =OO00000OO0OOOOOO0 .index ('&')#line:2440
            OOO0OOO00OOO00OOO =OO00000OO0OOOOOO0 [OO0O0O0OOOO000000 :OO0000O00OO0O000O ]#line:2441
    return OOO0OOO00OOO00OOO #line:2442
def getFinalVideoUrl (OOO0OO0000O000O00 ):#line:2444
    O0OO0OO0OO00OO00O =[]#line:2445
    for OO000OO0OOO0O000O in OOO0OO0000O000O00 :#line:2446
        OOOO0O00000OOO000 =len (OO000OO0OOO0O000O )#line:2447
        if '&'in OO000OO0OOO0O000O :#line:2448
            OOOO0O00000OOO000 =OO000OO0OOO0O000O .index ('&')#line:2449
        O0OO0OO0OO00OO00O .append ('http://www.youtube.com/'+OO000OO0OOO0O000O [:OOOO0O00000OOO000 ])#line:2450
    return O0OO0OO0OO00OO00O #line:2451
def getData (O0O000OO0OO0000O0 ):#line:2452
 try :#line:2454
            OOOOOOO0OO000O0O0 =urllib2 .Request (O0O000OO0OO0000O0 )#line:2457
            OOOOOOO0OO000O0O0 .add_header ('User-Agent',__USERAGENT__ )#line:2458
            O00O0OO00OOO0OOO0 =urllib2 .urlopen (OOOOOOO0OO000O0O0 )#line:2459
            OO00OOOO0OOOO00OO =O00O0OO00OOO0OOO0 .headers ['content-type']#line:2460
            OOO0O0O0O0000OOO0 =O00O0OO00OOO0OOO0 .read ().replace ("\n","").replace ("\t","").replace ("\r","")#line:2462
            O00O0OO00OOO0OOO0 .close ()#line:2464
            return OO00OOOO0OOOO00OO ,OOO0O0O0O0000OOO0 #line:2467
 except Exception as OO00OOOOOOOO00OOO :#line:2468
    xbmc .sleep (100 )#line:2469
    O00O0OO00OOO0OOO0 =urllib2 .urlopen (OOOOOOO0OO000O0O0 )#line:2471
    OO00OOOO0OOOO00OO =O00O0OO00OOO0OOO0 .headers ['content-type']#line:2472
    OOO0O0O0O0000OOO0 =O00O0OO00OOO0OOO0 .read ().replace ("\n","").replace ("\t","").replace ("\r","")#line:2474
    O00O0OO00OOO0OOO0 .close ()#line:2476
    return OO00OOOO0OOOO00OO ,OOO0O0O0O0000OOO0 #line:2479
def html_decode (O0O0OO0O0OOO00OO0 ):#line:2481
    ""#line:2486
    OOOOOO0OOO00OO0OO =(("'",'&#39;'),('"','&quot;'),('>','&gt;'),('<','&lt;'),('-','&#8211;'),('&','&amp;'))#line:2494
    for O0O00OOOO000OOO00 in OOOOOO0OOO00OO0OO :#line:2495
        O0O0OO0O0OOO00OO0 =O0O0OO0O0OOO00OO0 .replace (O0O00OOOO000OOO00 [1 ],O0O00OOOO000OOO00 [0 ])#line:2496
    return O0O0OO0O0OOO00OO0 #line:2497
def get_all_youtube_items (OO000OOOOO00O00OO ,OO0O000O00OO00O0O ,OOOOOO00O0O000000 ):#line:2498
   import random #line:2499
   try:
       OOO000O0O0O0O0O00 ,OO0O0O0000OOO000O =getData (OO0O000O00OO00O0O )#line:2501

       O0OO0O0000000OO0O =re .compile ('"videoId":"(.+?)"').findall (OO0O0O0000OOO000O )#line:2503
       OOOOOO00O00OOO0OO =re .compile ('"text":"(.+?)"').findall (OO0O0O0000OOO000O )#line:2504
       O000O0OOOOOOO0O00 =re .compile ('"url":"(.+?)"').findall (OO0O0O0000OOO000O )#line:2505
       O0000O00O0O0O00O0 =[]#line:2506
       OO00OOOOOOOOO00OO =0 #line:2507
       for O000OOOO0O00OO00O in O0OO0O0000000OO0O :#line:2508
       
        OO000OOOOO00O00OO =OOOOOO00O00OOO0OO [O0OO0O0000000OO0O .index (O000OOOO0O00OO00O )]#line:2509
        OOO0OO000O0O00OOO =O000O0OOOOOOO0O00 [O0OO0O0000000OO0O .index (O000OOOO0O00OO00O )]#line:2510
        OO000OOOOO00O00OO =html_decode (OO000OOOOO00O00OO )#line:2512
        if not 'Deleted video'in OO000OOOOO00O00OO :#line:2516
         if not 'Private video'in OO000OOOOO00O00OO :#line:2517
            O0OOO00O00OOO00O0 ={}#line:2518
            O0OOO00O00OOO00O0 ['title']=OO000OOOOO00O00OO #line:2519
            O0000OOOO0O00O0OO =xbmcgui .ListItem (OO000OOOOO00O00OO ,thumbnailImage =' ')#line:2521
            O0000OOOO0O00O0OO .setInfo ('video',O0OOO00O00OOO00O0 )#line:2522
            OOO0000O00O0O0OOO ='plugin://%s/?mode=10&url=%s&name=%s'%(__plugin__ ,que (domain_s +'www.youtube.com/watch?v='+O000OOOO0O00OO00O ),que (OO000OOOOO00O00OO ))#line:2523
            OOOOOO00O0O000000 .add (url =OOO0000O00O0O0OOO ,listitem =O0000OOOO0O00O0OO ,index =OO00OOOOOOOOO00OO )#line:2525
            OO00OOOOOOOOO00OO =OO00OOOOOOOOO00OO +1 #line:2526
            O0000O00O0O0O00O0 .append ((que (domain_s +'www.youtube.com/watch?v='+O000OOOO0O00OO00O ),OO000OOOOO00O00OO ))#line:2527
            OOOOOO00O0O000000 .shuffle ()#line:2528
       OO000000000OOO000 =random .choice (O0000O00O0O0O00O0 )#line:2529
       return ('plugin://%s/?mode=10&url=%s&name=%s'%(__plugin__ ,OO000000000OOO000 [0 ],OO000000000OOO000 [1 ]))#line:2530
   except Exception as e :#line:2956
                logging.warning(e)
                import linecache
                exc_type, exc_obj, tb = sys.exc_info()
                f = tb.tb_frame
                lineno = tb.tb_lineno
                filename = f.f_code.co_filename
                linecache.checkcache(filename)
                line = linecache.getline(filename, lineno, f.f_globals)
                logging.warning(lineno)
def get_all_youtube_items4 (O00O0O0O000000O0O ,OOOO0OO0O0O0OOO00 ,OOOOO00OOO00OOO00 ):#line:2531
        import random #line:2532
        O0O00O0O0O00OOOO0 =read_youtube_html (OOOO0OO0O0O0OOO00 )#line:2534
        O000O00O00OOOOOO0 =getPlaylistUrlID (url )#line:2536
        OO000OOOO00O00O00 =re .compile (r'watch\?v=(.+?)0026list='+O000O00O00OOOOOO0 ).findall (O0O00O0O0O00OOOO0 )#line:2538
        OOO0O00O0OOO0OO0O =0 #line:2540
        O0000O0000OO0O0OO =[]#line:2541
        if OO000OOOO00O00O00 :#line:2543
             for O0O0OOO0OOOO0OO0O in OO000OOOO00O00O00 :#line:2546
                O00OO000OO0000O0O =len (O0O0OOO0OOOO0OO0O )#line:2547
                if '&'in O0O0OOO0OOOO0OO0O :#line:2548
                    O00OO000OO0000O0O =O0O0OOO0OOOO0OO0O .index ('&')#line:2549
                OO0OOOO00OOO00O0O =('http://www.youtube.com/'+O0O0OOO0OOOO0OO0O [:O00OO000OO0000O0O ])#line:2550
                O0OO0O00O0OOOOO0O ='"videoId":"%s".+?"label":"(.+?)"'%O0O0OOO0OOOO0OO0O [:O00OO000OO0000O0O ].split ('\\')[0 ].split ('=')[1 ]#line:2553
                OO0OOO0O0000O00OO =re .compile (O0OO0O00O0OOOOO0O ,re .DOTALL ).findall (O0O00O0O0O00OOOO0 )#line:2554
                O0O0OOO0OOO0O0000 ={}#line:2556
                O0O0OOO0OOO0O0000 ['title']=OO0OOO0O0000O00OO [0 ]#line:2557
                O00O0O0O000000O0O =OO0OOO0O0000O00OO [0 ]#line:2558
                O0000O0000OO0O0OO .append ((que (OO0OOOO00OOO00O0O ),O00O0O0O000000O0O ))#line:2559
                O0O0OOO0OOOOO0OOO =xbmcgui .ListItem (OO0OOO0O0000O00OO [0 ],thumbnailImage =' ')#line:2561
                O0O0OOO0OOOOO0OOO .setInfo ('video',O0O0OOO0OOO0O0000 )#line:2562
                OO0000O00O0OOO0OO ='plugin://%s/?mode=10&url=%s&name=%s'%(__plugin__ ,que (OO0OOOO00OOO00O0O ),que (OO0OOO0O0000O00OO [0 ]))#line:2563
                OOOOO00OOO00OOO00 .add (url =OO0000O00O0OOO0OO ,listitem =O0O0OOO0OOOOO0OOO ,index =OOO0O00O0OOO0OO0O )#line:2565
                OOO0O00O0OOO0OO0O =OOO0O00O0OOO0OO0O +1 #line:2566
        OOOOO00OOO00OOO00 .shuffle ()#line:2568
        OO0000O0000O00OO0 =random .choice (O0000O0000OO0O0OO )#line:2569
        return ('plugin://%s/?mode=10&url=%s&name=%s'%(__plugin__ ,OO0000O0000O00OO0 [0 ],OO0000O0000O00OO0 [1 ]))#line:2570
def gdecom (OO0O0O0000000OO00 ):#line:2571
    import base64
    import zlib
    a+=1
    data = OO0O0O0000000OO00

    json_str = zlib.decompress(base64.b64decode(data), 16 + zlib.MAX_WBITS).decode('utf-8')
    return json_str
    if '99999****'in OO0O0O0000000OO00 :#line:2578
        O00OO0OOOO000O0O0 +=1 #line:2579
    import StringIO ,gzip #line:2580
    OO0OOOOOOOOO0000O =StringIO .StringIO ()#line:2581
    OO0OOOOOOOOO0000O .write (OO0O0O0000000OO00 .decode ('base64'))#line:2582
    OO0OOOOOOOOO0000O .seek (0 )#line:2587
    return gzip .GzipFile (fileobj =OO0OOOOOOOOO0000O ,mode ='rb').read ()#line:2588
def get_google_subs(url):
    from xmlsub import xml2srt
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
            'Accept-Language': 'en-US,en;q=0.5',
           
            'Connection': 'keep-alive',
            
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
    
    x=requests.get(url.strip(),headers=headers).content
    
    regex='"ttsurl","(.+?)"'
    m=re.compile(regex).findall(x.decode('utf-8'))
    if len(m)==0:
        return False
        
    url=m[0].decode('unicode_escape')+'&ts=%s&type=track&lang=iw&format=1&kind='%(str(time.time()*100))
    
    x=requests.get(url,headers=headers).content
    if len(x)<10:
        url=m[0].decode('unicode_escape')+'&ts=%s&type=track&lang=en&format=1&kind='%(str(time.time()*100))
    
        x=requests.get(url,headers=headers).content
    xml2srt(x,os.path.join(user_dataDir, 'sub.srt'))

    return os.path.join(user_dataDir, 'sub.srt')
def play_link (OO0OO00OOOOOO00OO ,O0000000OO0O0OOO0 ,OOOO00000OOOOOOOO ,OO0OO0O0O0O00000O ,OOO000OOO00OO0OOO ,OO00O0OO0OO0OO00O ):#line:2590
   sub=None
   logging.warning('playing:')
   logging.warning(O0000000OO0O0OOO0)
   if 'nofile.io'in O0000000OO0O0OOO0 :#line:2592
      O0O0OO00OO00OO0OO ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3','Content-Type':'application/x-www-form-urlencoded','Connection':'keep-alive','Upgrade-Insecure-Requests':'1','Pragma':'no-cache','Cache-Control':'no-cache',}#line:2603
      OOO00000O00OOOO0O =requests .get (O0000000OO0O0OOO0 ,headers =O0O0OO00OO00OO0OO ).content #line:2604
      O0O0OOO0OO00O0OO0 ='<hr class="visible-xs visible-sm".+?<a href="(.+?)"'#line:2605
      O000O0O0O0OOO0O0O =re .compile (O0O0OOO0OO00O0OO0 ,re .DOTALL ).findall (OOO00000O00OOOO0O )#line:2606
      O0000000OO0O0OOO0 ='https://nofile.io'+O000O0O0O0OOO0O0O [0 ]#line:2607
   if 'files.fm'in O0000000OO0O0OOO0 :#line:2608
    O0O0OO00OO00OO0OO ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3','Referer':'https://www.hidemyass-freeproxy.com/en-ww','Content-Type':'application/x-www-form-urlencoded','Connection':'keep-alive','Upgrade-Insecure-Requests':'1','Pragma':'no-cache','Cache-Control':'no-cache',}#line:2619
    OOOO00000OOOOOOOO ={'form[url]':O0000000OO0O0OOO0 ,'form[dataCenter]':'random'}#line:2624
    O0000000OO0O0OOO0 =requests .post ('https://www.hidemyass-freeproxy.com/process/en-ww',headers =O0O0OO00OO00OO0OO ,data =OOOO00000OOOOOOOO ,stream =True ).url #line:2626
   try :#line:2629
        logging.warning('Deconding:')
        O0000000OO0O0OOO0 =gdecom (O0000000OO0O0OOO0 )#line:2630
   except :#line:2631
       try :#line:2633
        O0000000OO0O0OOO0 =run_dds (O0000000OO0O0OOO0 )#line:2634
       except Exception as O0O0O00OOOO0OOO0O :#line:2635
        logging .warning ('ERROR PLAYING:'+str (O0O0O00OOOO0OOO0O ))#line:2636
        pass #line:2637

   #O0000000OO0O0OOO0 =run_dds (O0000000OO0O0OOO0 )#line:2634

   if 1:#try :#line:2628
    try :#line:2629
        O0000000OO0O0OOO0 =gdecom (O0000000OO0O0OOO0 )#line:2630
    except :#line:2631
       try :#line:2633
        O0000000OO0O0OOO0 =run_dds (O0000000OO0O0OOO0 )#line:2634
       except Exception as O0O0O00OOOO0OOO0O :#line:2635
        logging .warning ('ERROR PLAYING:'+str (O0O0O00OOOO0OOO0O ))#line:2636
        pass #line:2637
    logging.warning('f_link:'+O0000000OO0O0OOO0)
    if  'google' in O0000000OO0O0OOO0:
        logging.warning('In subg')
        sub=get_google_subs(O0000000OO0O0OOO0)
        logging.warning('Got In subg')
        logging.warning(sub)
    O00O00000OO0OO0O0 =OO0OO00OOOOOO00OO #line:2639
    O0O00O00O0OOOOOO0 =OO0OO00OOOOOO00OO #line:2640
    O0O00OOOOO0O0O0O0 =True #line:2641
    O00OOOO0O0O0OO00O =O0000000OO0O0OOO0 #line:2642
    
    O00O00O00OO000OOO =getattr (defen ,'link',False )#line:2643
    if O00O00O00OO000OOO and '_pass_ok_'not in OOO000OOO00OO0OOO :#line:2644
        OO0OO0O0O0OOOO00O =''#line:2645
        OOO000OO0OOO0O0OO =False #line:2646
        O00OO0OO00000O0O0 =xbmc .Keyboard (OO0OO0O0O0OOOO00O ,'הכנס סיסמא')#line:2647
        O00OO0OO00000O0O0 .doModal ()#line:2648
        if O00OO0OO00000O0O0 .isConfirmed ():#line:2649
                    OO0OO0O0O0OOOO00O =O00OO0OO00000O0O0 .getText ()#line:2650
                    OOO00000O00OOOO0O =requests .get (O00O00O00OO000OOO [0 ].decode ('base64')).content #line:2651
                    if OO0OO0O0O0OOOO00O !=OOO00000O00OOOO0O :#line:2652
                       sys .exit ()#line:2653
                    else :#line:2654
                      OOO000OO0OOO0O0OO =True #line:2655
        if not OOO000OO0OOO0O0OO :#line:2656
            sys .exit ()#line:2657
    O0OO000OOOO0OOO00 =O0000000OO0O0OOO0 #line:2659
    if 'goo.gl'in O0000000OO0O0OOO0 :#line:2660
     try :#line:2661
      O0000000OO0O0OOO0 =unshorten_url (O0000000OO0O0OOO0 )#line:2662
     except :#line:2663
      pass #line:2664
    OO0O0O00OOOO000OO =0 #line:2665
    if '.zip'in O0000000OO0O0OOO0 :#line:2666
      install_package (OO0OO00OOOOOO00OO ,O0000000OO0O0OOO0 )#line:2667
      sys .exit ()#line:2668
    try :#line:2670
        try :#line:2671
            O0O00O0OOOO0O0OOO =json .loads (OOOO00000OOOOOOOO )#line:2672
        except :#line:2673
            OOOO00000OOOOOOOO =OOOO00000OOOOOOOO .replace ('[',' ').replace (']',' ').replace ('	','').replace ("\\"," ").replace (': """",',': "" "",').replace (': """"}',': "" ""}').replace (': "",',': " ",').replace (': ""}',': " "}').replace ('""','"').replace ('\n','').replace ('\r','')#line:2674
            O0O00O0OOOO0O0OOO =json .loads (OOOO00000OOOOOOOO )#line:2675
        if 'tt'in O0O00O0OOOO0O0OOO ['imdbnumber']and nanscarper ==True and len (O0000000OO0O0OOO0 )<5 :#line:2677
         O0000O0OOOOO00O0O =[]#line:2679
         O0000O0OOOOO00O0O .append ("ניגון ישיר")#line:2680
         O0000O0OOOOO00O0O .append ("חפש מקורות ניגון")#line:2681
         if len (O0000000OO0O0OOO0 )<5 :#line:2682
           import resolveurl #line:2683
           OOOOOO00O0O00OOO0 =get_links (OO0OO00OOOOOO00OO ,O0000000OO0O0OOO0 ,OOOO00000OOOOOOOO )#line:2684
           OO0O0O00OOOO000OO =1 #line:2685
           O0000000OO0O0OOO0 =resolveurl .HostedMediaFile (url =O0000000OO0O0OOO0 ).resolve ()#line:2687
           if O0000000OO0O0OOO0 ==False :#line:2691
            O0000000OO0O0OOO0 =OOOOOO00O0O00OOO0 #line:2692
         else :#line:2694
             O0O0O0OO0O0OOOOOO =xbmcgui .Dialog ().select ("בחר מקור",O0000O0OOOOO00O0O )#line:2695
             if O0O0O0OO0O0OOOOOO ==1 :#line:2697
                   O0000000OO0O0OOO0 =get_links (OO0OO00OOOOOO00OO ,O0000000OO0O0OOO0 ,OOOO00000OOOOOOOO )#line:2698
                   OO0O0O00OOOO000OO =1 #line:2699
             if O0O0O0OO0O0OOOOOO ==-1 :#line:2700
                  sys .exit ()#line:2701
    except Exception as O0O0O00OOOO0OOO0O :#line:2703
      logging .warning (O0O0O00OOOO0OOO0O )#line:2704
      pass #line:2705
    if '$$$'in O0000000OO0O0OOO0 and ('playlist_all'not in O0000000OO0O0OOO0 or 'playlist_all=True'in O0000000OO0O0OOO0 ):#line:2707
       O0000O0OOOOO00O0O =[]#line:2708
       O0O0O000O0OO0O0O0 =O0000000OO0O0OOO0 .split ('$$$')#line:2709
       OOO00000O00OOOO0O =1 #line:2710
       for OOOO00OOO0OOO0O00 in O0O0O000O0OO0O0O0 :#line:2711
        if '//'in OOOO00OOO0OOO0O00 :#line:2712
            OO0000000OOO0OO0O ='//(.+?)/'#line:2713
            OOO000O00OO0OO0OO =re .compile (OO0000000OOO0OO0O ).findall (OOOO00OOO0OOO0O00 )#line:2714
            if 'pluggin'in OOOO00OOO0OOO0O00 :#line:2715
              O0000O0OOOOO00O0O .append (' מקור ')+str (OOO00000O00OOOO0O ).replace ('openload','vummo')#line:2717
              OOO00000O00OOOO0O =OOO00000O00OOOO0O +1 #line:2718
            else :#line:2719
              if OOO000O00OO0OO0OO [0 ]!=None :#line:2720
                O0000O0OOOOO00O0O .append (OOO000O00OO0OO0OO [0 ].replace ('openload','vummo'))#line:2721
       O0O0O0OO0O0OOOOOO =xbmcgui .Dialog ().select ("בחר מקור",O0000O0OOOOO00O0O )#line:2724
       if O0O0O0OO0O0OOOOOO ==-1 :#line:2725
         O0O00OOOOO0O0O0O0 =False #line:2726
         sys .exit ()#line:2727
       O0000000OO0O0OOO0 =O0O0O000O0OO0O0O0 [O0O0O0OO0O0OOOOOO ]#line:2730
       O00OOOO0O0O0OO00O =O0000000OO0O0OOO0 #line:2731
    logging .warning ('oooo___url')#line:2732
    logging .warning (O0000000OO0O0OOO0 )#line:2733
    logging.warning(O0000000OO0O0OOO0)
    if 'uptobox' in O0000000OO0O0OOO0 or 'uptostream' in O0000000OO0O0OOO0:
        import uptobox
        upto = uptobox.cHoster()
        
        s_url=upto.setUrl(O0000000OO0O0OOO0)
        s_url=upto.getMediaLink()
        logging.warning(s_url)
        O0000000OO0O0OOO0= s_url
    if not 'plugin://'in O0000000OO0O0OOO0 or ('plugin://'in O0000000OO0O0OOO0 and 'PlayMedia'in O0000000OO0O0OOO0 ):#line:2734
      logging .warning ('IN 1')#line:2735
      if O0O00OOOOO0O0O0O0 ==True :#line:2736
       if not 'plugin://'in O0000000OO0O0OOO0 :#line:2737
        logging .warning ('IN 2')#line:2738
        if OO0O0O00OOOO000OO ==0 :#line:2739
          if '$$$'in O0000000OO0O0OOO0 :#line:2741
                O0O0O000O0OO0O0O0 =O0000000OO0O0OOO0 .split ('$$$')#line:2743
                OOO00000O00OO00OO =xbmc .PlayList (xbmc .PLAYLIST_VIDEO )#line:2745
                OOO00000O00OO00OO .clear ()#line:2746
                OOO00000O00OOOO0O =0 #line:2747
                for OOO0O00O000OOOO0O in O0O0O000O0OO0O0O0 :#line:2749
                  if 'www.you'in OOO0O00O000OOOO0O and 'list'in OOO0O00O000OOOO0O :#line:2751
                    O0000000OO0O0OOO0 =get_all_youtube_items (OO0OO00OOOOOO00OO ,OOO0O00O000OOOO0O ,OOO00000O00OO00OO )#line:2753
                  if OOO0O00O000OOOO0O !="playnext=1"and OOO0O00O000OOOO0O !='playlist_all'and OOO0O00O000OOOO0O !='playlist_all=True':#line:2756
                      if 'www.you'not in OOO0O00O000OOOO0O and 'list'not in OOO0O00O000OOOO0O :#line:2758
                        O00OOOO0O0O0OO00O =OOO0O00O000OOOO0O #line:2759
                        O0000000OO0O0OOO0,sub =resolver (OOO0O00O000OOOO0O )
                        O0000000OO0O0OOO0=O0000000OO0O0OOO0.strip ().replace ('\\r','').replace ('\\n','')#line:2760
                      OO00OOOOOO0OOO0O0 =xbmcgui .ListItem (OO0OO00OOOOOO00OO ,thumbnailImage =' ')#line:2762
                      try :#line:2763
                          try :#line:2764
                                O00O000O00OOO0OO0 =json .loads (OOOO00000OOOOOOOO )#line:2765
                          except :#line:2766
                                OOOO00000OOOOOOOO =OOOO00000OOOOOOOO .replace ('[',' ').replace (']',' ').replace ('	','').replace ("\\"," ").replace (': """",',': "" "",').replace (': """"}',': "" ""}').replace (': "",',': " ",').replace (': ""}',': " "}').replace ('""','"').replace ('\n','').replace ('\r','')#line:2767
                                O00O000O00OOO0OO0 =json .loads (OOOO00000OOOOOOOO )#line:2768
                          if sub:
                                O00O000O00OOO0OO0 [u'mpaa']= ('heb' )#line:2775
                                
                          if Addon .getSetting ("subs")=='2345':#line:2769
                            O00O000O00OOO0OO0 [u'Tagline']=O0OO000OOOO0OOO00 #line:2770
                          try :#line:2771
                              OOO0OO0O00OO000OO =urllib2 .urlopen (subtitle_addr [0 ]).readlines ()#line:2772
                              if OO0OO0O0O0O00000O =='heb'and OO0O0O00OOOO000OO ==0 :#line:2774
                                 O00O000O00OOO0OO0 [u'mpaa']= (OO0OO0O0O0O00000O )#line:2775
                              if 'title'not in O00O000O00OOO0OO0 and 'originaltitle'in O00O000O00OOO0OO0 :#line:2776
                                 O00O000O00OOO0OO0 ['title']=O00O000O00OOO0OO0 ['originaltitle']#line:2777
                              if O00O000O00OOO0OO0 ['plot']=='':#line:2778
                                O00O000O00OOO0OO0 ['plot']=OOO000OOO00OO0OOO #line:2779
                              for OO0OO000O0OOO0OOO in OOO0OO0O00OO000OO :#line:2781
                                 OO00OO0OOOO0O0OOO =OO0OO000O0OOO0OOO .split (":::")[0 ]#line:2782
                                 O0OO0O00OO0OOO00O =OO0OO000O0OOO0OOO .split (":::")[1 ]#line:2783
                                 OO00O0OOO0O0O0O00 =OO0OO000O0OOO0OOO .split (":::")[2 ]#line:2784
                                 OO000O0O00OO0OOO0 =OO0OO000O0OOO0OOO .split (":::")[3 ]#line:2785
                                 O0000O00OOOOOO000 =OO0OO000O0OOO0OOO .split (":::")[4 ]#line:2786
                                 if O0OO0O00OO0OOO00O .strip ()==O0OO000OOOO0OOO00 :#line:2787
                                   O00O000O00OOO0OO0 [u'title']=OO00OO0OOOO0O0OOO #line:2788
                          except :#line:2789
                            pass #line:2790
                          OO00OOOOOO0OOO0O0 .setInfo (type ='Video',infoLabels =O00O000O00OOO0OO0 )#line:2792
                          OO00OOOOOO0OOO0O0 .setInfo (type ="Music",infoLabels =O00O000O00OOO0OO0 )#line:2793
                      except :#line:2794
                          OO00OOOOOO0OOO0O0 .setInfo (type ='Video',infoLabels ={"Title":OO0OO00OOOOOO00OO })#line:2795
                          OO00OOOOOO0OOO0O0 .setInfo (type ="Music",infoLabels ={"Title":OO0OO00OOOOOO00OO })#line:2796
                      if 'www.you'not in OOO0O00O000OOOO0O and 'list='not in OOO0O00O000OOOO0O :#line:2799
                        OOO00000O00OO00OO .add (url =O0000000OO0O0OOO0 ,listitem =OO00OOOOOO0OOO0O0 ,index =OOO00000O00OOOO0O )#line:2801
                      if OOO00000O00OOOO0O ==0 :#line:2802
                        
                        
                        xbmcplugin .setResolvedUrl (handle =int (sys .argv [1 ]),succeeded =True ,listitem =OO00OOOOOO0OOO0O0 )#line:2803
                      OOO00000O00OOOO0O =OOO00000O00OOOO0O +1 #line:2804
                O0000000OO0O0OOO0 ="DONE"#line:2810
          else :#line:2811
            logging .warning ('resolver')#line:2812
            O0000000OO0O0OOO0,sub =resolver (O0000000OO0O0OOO0 )
            O0000000OO0O0OOO0=O0000000OO0O0OOO0.strip ().replace ('\\r','').replace ('\\n','')#line:2813
        O0000000OO0O0OOO0 =O0000000OO0O0OOO0 .replace ('%7C','|')#line:2814
        if O0000000OO0O0OOO0 !="DONE":#line:2815
            OO00000000OO00OO0 =False #line:2824
            if '%%%%'in O0000000OO0O0OOO0 :#line:2825
               OO00000000OO00OO0 =O0000000OO0O0OOO0 .split ('%%%%')[1 ]#line:2826
               O0000000OO0O0OOO0 =O0000000OO0O0OOO0 .split ('%%%%')[0 ]#line:2827
            logging .warning ('Final_url')#line:2828
            logging .warning (O0000000OO0O0OOO0 )#line:2829
            O0OO0000OO0O000O0 =xbmcgui .ListItem (OO0OO00OOOOOO00OO ,path =O0000000OO0O0OOO0 )#line:2830
            try :#line:2831
              try :#line:2833
                    O00O000O00OOO0OO0 =json .loads (OOOO00000OOOOOOOO )#line:2834
              except :#line:2835
                    OOOO00000OOOOOOOO =OOOO00000OOOOOOOO .replace ('[',' ').replace (']',' ').replace ('	','').replace ("\\"," ").replace (': """",',': "" "",').replace (': """"}',': "" ""}').replace (': "",',': " ",').replace (': ""}',': " "}').replace ('""','"').replace ('\n','').replace ('\r','')#line:2836
                    O00O000O00OOO0OO0 =json .loads (OOOO00000OOOOOOOO )#line:2837
              if 'originaltitle'in O00O000O00OOO0OO0 :#line:2838
                O0O00O00O0OOOOOO0 =O00O000O00OOO0OO0 ['originaltitle']#line:2839
              if Addon .getSetting ("subs")=='2345':#line:2840
                O00O000O00OOO0OO0 [u'Tagline']=O0OO000OOOO0OOO00 #line:2841
              try :#line:2842
                  OOO0OO0O00OO000OO =urllib2 .urlopen (subtitle_addr [0 ]).readlines ()#line:2843
                  if OO0OO0O0O0O00000O =='heb'and OO0O0O00OOOO000OO ==0 :#line:2846
                     O00O000O00OOO0OO0 [u'mpaa']= (OO0OO0O0O0O00000O )#line:2847
                  if 'title'not in O00O000O00OOO0OO0 and 'originaltitle'in O00O000O00OOO0OO0 :#line:2848
                     O00O000O00OOO0OO0 ['title']=O00O000O00OOO0OO0 ['originaltitle']#line:2849
                  if O00O000O00OOO0OO0 ['plot']=='':#line:2850
                    O00O000O00OOO0OO0 ['plot']=OOO000OOO00OO0OOO #line:2851
                  O00O00000OO0OO0O0 =O00O000O00OOO0OO0 ['title']#line:2853
                  for OO0OO000O0OOO0OOO in OOO0OO0O00OO000OO :#line:2855
                                 OO00OO0OOOO0O0OOO =OO0OO000O0OOO0OOO .split (":::")[0 ]#line:2856
                                 O0OO0O00OO0OOO00O =OO0OO000O0OOO0OOO .split (":::")[1 ]#line:2857
                                 OO00O0OOO0O0O0O00 =OO0OO000O0OOO0OOO .split (":::")[2 ]#line:2858
                                 OO000O0O00OO0OOO0 =OO0OO000O0OOO0OOO .split (":::")[3 ]#line:2859
                                 O0000O00OOOOOO000 =OO0OO000O0OOO0OOO .split (":::")[4 ]#line:2860
                                 if O0OO0O00OO0OOO00O .strip ()==O0OO000OOOO0OOO00 :#line:2861
                                   O00O000O00OOO0OO0 [u'title']=OO00OO0OOOO0O0OOO #line:2862
              except :#line:2863
                pass #line:2864
              if sub:
                O00O000O00OOO0OO0 [u'mpaa']= ('heb' )#line:2847
              logging .warning (O00O000O00OOO0OO0 )#line:2865
              O0OO0000OO0O000O0 .setInfo (type ='Video',infoLabels =O00O000O00OOO0OO0 )#line:2866
              O0OO0000OO0O000O0 .setInfo (type ="Music",infoLabels =O00O000O00OOO0OO0 )#line:2867
            except :#line:2868
              O0OO0000OO0O000O0 .setInfo (type ='Video',infoLabels ={"Title":OO0OO00OOOOOO00OO })#line:2869
              O0OO0000OO0O000O0 .setInfo (type ="Music",infoLabels ={"Title":OO0OO00OOOOOO00OO })#line:2870
            O0OO0000OO0O000O0 .setProperty ('IsPlayable','true')#line:2871
            if sub:
                O0OO0000OO0O000O0.setSubtitles([sub])
            xbmcplugin .setResolvedUrl (handle =int (sys .argv [1 ]),succeeded =True ,listitem =O0OO0000OO0O000O0 )#line:2873
            logging.warning('subs:'+str(sub))
            
            if 0:#OO00000000OO00OO0 or sub:#line:2874
                O000OO00O000OO00O =xbmc .Player ()#line:2875
                for _OO00OO0O00O0O00OO in xrange (30 ):#line:2877
                    logging.warning('in subs:'+str(O000OO00O000OO00O .isPlaying ()))
                    if O000OO00O000OO00O .isPlaying () :#line:2878
                        vidtime = xbmc.Player().getTime()
                        logging.warning('vidtime:'+str(vidtime))
                        if  vidtime>0:
                            if sub:
                                O000OO00O000OO00O .setSubtitles (sub )#line:2879
                            else:
                                O000OO00O000OO00O .setSubtitles (OO00000000OO00OO0 )#line:2879
                            break #line:2880
                    elif xbmc .abortRequested :#line:2882
                        break #line:2883
                    xbmc .sleep (1000 )#line:2885
                
            dbcur_w .execute ("INSERT INTO watched Values ('%s', '%s','%s','%s','%s','%s');"%(OO00O0OO0OO0OO00O .replace ("'","%27"),O00OOOO0O0O0OO00O .replace ("'","%27"),OOOO00000OOOOOOOO .replace ("'","%27"),'','',''))#line:2889
            dbcon_w .commit ()#line:2890
       else :#line:2892
        logging .warning ('Running Plugin')#line:2905
        xbmc .executebuiltin (O0000000OO0O0OOO0 .replace ('&amp;mode','&mode').replace ('&quot;',""))#line:2906
        '''
        regexss='name=(.+?)&'
        matchss=re.compile(regexss).findall(matchss_up[0])
        if len(matchss)>0:
            url=matchss_up[0].replace(matchss[0],que(matchss[0])).replace('amp;','')
        regexss='url=(.+?)&'
        matchss=re.compile(regexss).findall(matchss_up[0])
        if len(matchss)>0:
            url=matchss_up[0].replace(matchss[0],urllib.unquote(matchss[0]))
        
        '''#line:2919
    else :#line:2922
      logging .warning ('ELSE')#line:2925
      OO0O000O00OO0O0OO ='&quot;(.+?)&quot;'#line:2927
      O0OOOOO0OO0O00OO0 =re .compile (OO0O000O00OO0O0OO ).findall (O0000000OO0O0OOO0 )#line:2928
      if len (O0OOOOO0OO0O00OO0 )>0 :#line:2929
        update_view (O0OOOOO0OO0O00OO0 [0 ])#line:2930
      else :#line:2931
        update_view (O0000000OO0O0OOO0 )#line:2932
    O0O0OOO00OOO000OO =True #line:2933
    logging.warning ('o_link')#line:2940
    logging .warning (O00OOOO0O0O0OO00O )#line:2941
    xbmc .sleep (500 )#line:2942
    xbmc .executebuiltin ('Dialog.Close(okdialog, true)')#line:2943
    if not O0O0OOO00OOO000OO and 'plugin'not in O00OOOO0O0O0OO00O :#line:2944
        O00OOOO0O0O0O0OOO ='''\
         1 שגיאת מקור יטופל בקרוב
שם:%s
שגיאה: %s
מקור:%s
שורה:%s
        
        '''#line:2951
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        if error_ad :#line:2953
            OOO00000O00OOOO0O =requests .get (error_ad .decode ('base64')+O00OOOO0O0O0O0OOO %(O00O00000OO0OO0O0 ,'Error',O00OOOO0O0O0OO00O,str(lineno) )).content #line:2954
        contact (title =O0O00O00O0OOOOOO0 .strip ().replace ('\r','').replace ('\n',''),msg =O00OOOO0O0O0O0OOO %(O00O00000OO0OO0O0 ,O0O0O00OOOO0OOO0O ,O0O00O00O0OOOOOO0,str(lineno) ))#line:2955
    return 0
def run_addon (OOO00O00OO000000O ):#line:2971
  xbmc .executebuiltin (html_parser .unescape (OOO00O00OO000000O ))#line:2973
  xbmc .executebuiltin ('xbmc.PlayerControl(RepeatOff)')#line:2974
  OOO00OO0OO0OO0O00 =99 #line:2975
  sys .exit ()#line:2976
  return '0'#line:2977
def search_all (OO0000OOO000OO000 ,OOOOOOOOO00OOOO0O ,OOO0O000OOOOOO000 ):#line:2978
    OO00OO0O0O000000O =''#line:2979
    O000O00O000OOOOO0 =xbmc .Keyboard (OO00OO0O0O000000O ,'הכנס מילות חיפוש כאן')#line:2980
    O000O00O000OOOOO0 .doModal ()#line:2981
    OOOO000O0O00O0O00 =[]#line:2982
    if O000O00O000OOOOO0 .isConfirmed ():#line:2983
                OO00OO0O0O000000O =O000O00O000OOOOO0 .getText ()#line:2984
    if standalone ==False :#line:2985
        OO0000OOO000OO000 =[]#line:2986
        for O00O000O000O00O00 in range (1 ,40 ):#line:2988
         OO0000OOO000OO000 .append (Addon .getSetting ("Pastebin"+str (O00O000O000O00O00 )))#line:2989
    OO00O000O0O0O0O00 =[]#line:2990
    if OO00OO0O0O000000O !='':#line:2991
        dbcur .execute ("SELECT * FROM MyTable where name like '%{0}%'".format (OO00OO0O0O000000O ))#line:2995
        OOOO00O00OO00O00O =dbcur .fetchall ()#line:2997
        logging .warning (len (OOOO00O00OO00O00O ))#line:2998
        for O00OOO0000OO00O00 ,O0O0O0000OOOO0000 ,OO00OO00OOOO0OO00 ,O00000O00O00OO0O0 ,OOO0O0OO0OOO0OO00 ,O0OOO00O00OO00OOO ,O0O00000OOO0OO000 ,OOO000000OO000O00 ,OOOO0O000OOO0O0OO ,OO00O00O0OO00OO00 ,O00000000O00OOOOO ,OO000O0O00OO000OO in OOOO00O00OO00O00O :#line:2999
          O0O0O0000OOOO0000 =O0O0O0000OOOO0000 
          OO00OO00OOOO0OO00 =OO00OO00OOOO0OO00 #line:3001
          O00000O00O00OO0O0 =O00000O00O00OO0O0 #line:3002
          OOO0O0OO0OOO0OO00 =OOO0O0OO0OOO0OO00 #line:3003
          O0OOO00O00OO00OOO =O0OOO00O00OO00OOO #line:3004
          O0O00000OOO0OO000 =O0O00000OOO0OO000 #line:3005
          OOO000000OO000O00 =OOO000000OO000O00 #line:3006
          OOOO0O000OOO0O0OO =OOOO0O000OOO0O0OO #line:3007
          OO00O00O0OO00OO00 =OO00O00O0OO00OO00 #line:3008
          O00000000O00OOOOO =O00000000O00OOOOO #line:3009
          OO000O0O00OO000OO =OO000O0O00OO000OO #line:3010
          logging .warning (O0O0O0000OOOO0000 )#line:3011
          if OO000O0O00OO000OO =='category':#line:3013
            if 'ערוץ'in O0O0O0000OOOO0000 :#line:3014
                OOOO000O0O00O0O00 .append (addLink (O0O0O0000OOOO0000 .replace ('@',''),O00000000O00OOOOO +O0O0O0000OOOO0000 ,14 ,False ,O00000O00O00OO0O0 ,OOO0O0OO0OOO0OO00 ,O0OOO00O00OO00OOO ,data =O0O00000OOO0OO000 .replace ("OriginalTitle","originaltitle")))#line:3015
            else :#line:3016
                 OOOO000O0O00O0O00 .append (addDir3 (O0O0O0000OOOO0000 ,O00000000O00OOOOO +O0O0O0000OOOO0000 ,5 ,O00000O00O00OO0O0 ,OOO0O0OO0OOO0OO00 ,O0OOO00O00OO00OOO ,data =O0O00000OOO0OO000 .replace ("OriginalTitle","Originaltitle")))#line:3017
          else :#line:3018
               OOOO000O0O00O0O00 .append (addLink (O0O0O0000OOOO0000 ,OO00OO00OOOO0OO00 ,3 ,False ,O00000O00O00OO0O0 ,OOO0O0OO0OOO0OO00 ,O0OOO00O00OO00OOO ,data =O0O00000OOO0OO000 .replace ("OriginalTitle","originaltitle")))#line:3020
        xbmcplugin .addDirectoryItems (int (sys .argv [1 ]),OOOO000O0O00O0O00 ,len (OOOO000O0O00O0O00 ))#line:3021
def play_youtube (O000OO0O0000OO0OO ,OO0OO00OO0OO0O000 ):#line:3025
    if O000OO0O0000OO0OO .endswith ('/'):#line:3026
        O000OO0O0000OO0OO =O000OO0O0000OO0OO [:-1 ]#line:3027
    O00OO0O000OO000OO =O000OO0O0000OO0OO .split ('v=')[1 ]#line:3028
    O00O00OO00OO0OOOO ='plugin://plugin.video.youtube/play/?video_id='+O00OO0O000OO000OO #line:3029
    '''
    from pytube import YouTube
   
    all_streams=(YouTube(url).streams.all())
    

    
    
    regex='itag="(.+?)".+?res="(.+?)".+?codec="(.+?)"'
    match=re.compile(regex).findall(str(all_streams))
    all_res=[]
    for itag,res,codec in match:
        
          all_res.append((itag,res.replace('p','')))
        
    all_res=sorted(all_res, key=lambda x: x[1], reverse=False)
    logging.warning(all_res)
    
    playback_url = YouTube(url).streams.get_by_itag(all_res[0][0]).download()
     
   
    '''#line:3052
    O000O0000000O0O00 =xbmcgui .ListItem (path =O00O00OO00OO0OOOO )#line:3054
    O000O0000000O0O00 .setInfo (type ="Video",infoLabels ={"Title":unque (OO0OO00OO0OO0O000 )})#line:3055
    xbmcplugin .setResolvedUrl (int (sys .argv [1 ]),True ,O000O0000000O0O00 )#line:3056
def make_strm (OO000OO0O0OOOOOO0 ,OOO0O00O0000O0O00 ,OO0O00O000O0O0OOO ,OOO00000O0OOO00O0 ,O00OOOOOO0O0OOOO0 ,OOOO00O0OOOO00OOO ):#line:3057
    import xbmcvfs #line:3058
    O0OO00OO000O000O0 =Addon .getSetting ("strm")#line:3059
    if O0OO00OO000O000O0 =='':#line:3060
      O0OO00OO000O000O0 =xbmcgui .Dialog ().browse (0 ,"בחר תקייה",'files','',False ,False ,'')#line:3061
      Addon .setSetting ("strm",O0OO00OO000O000O0 )#line:3062
    O0OOOOOOOO0000O00 =json .loads (OOO00000O0OOO00O0 )['originaltitle'].replace ('[','(').replace (']',')').replace ('(Video ','(').strip ()#line:3063
    OOOOOOOOOO000O00O =json .loads (OOO00000O0OOO00O0 )['imdb']#line:3064
    OOOOOO00O0O0O0OO0 =str (O0OO00OO000O000O0 )+'/'+str (O0OOOOOOOO0000O00 )+'.strm'#line:3066
    O0OO00O00000O0OOO =xbmcvfs .File (OOOOOO00O0O0O0OO0 ,"w")#line:3069
    O0O00O0000O0OOOO0 =sys .argv [0 ]#line:3070
    OO0OO00O0OOOO00O0 =('%s?url=%s&mode=3&name=%s&description=%s&data=%s&index_depth=%s&lang=%s'%(O0O00O0000O0OOOO0 ,(OOO0O00O0000O0O00 ),(OO000OO0O0OOOOOO0 ),(OO0O00O000O0O0OOO ),(OOO00000O0OOO00O0 ),str (O00OOOOOO0O0OOOO0 ),str (OOOO00O0OOOO00OOO )))#line:3071
    O0OO00O00000O0OOO .write (OO0OO00O0OOOO00O0 +'\n')#line:3072
    O0OO00O00000O0OOO .close ()#line:3073
    return 0 #line:3077
params =get_params ()#line:3079
url =None #line:3081
name =None #line:3082
mode =None #line:3083
iconimage =None #line:3084
fanart =None #line:3085
description =' '#line:3086
count =0 #line:3087
cat_level =" "#line:3088
index_depth =0 #line:3089
page =None #line:3090
data =" "#line:3091
selected_list =""#line:3092
lang =" "#line:3093

try :#line:3095
        url =unque_plus (params ["url"])#line:3096
except :#line:3097
        pass #line:3098
try :#line:3099
        name =unque_plus (params ["name"])#line:3100
except :#line:3101
        pass #line:3102
try :#line:3103
        iconimage =unque_plus (params ["iconimage"])#line:3104
except :#line:3105
        pass #line:3106
try :#line:3107
        mode =int (params ["mode"])#line:3108
except :#line:3109
        pass #line:3110
try :#line:3111
        fanart =unque_plus (params ["fanart"])#line:3112
except :#line:3113
        pass #line:3114
try :#line:3115
        description =unque_plus (params ["description"])#line:3116
except :#line:3117
        pass #line:3118
try :#line:3119
        count =unque_plus (params ["count"])#line:3120
except :#line:3121
        pass #line:3122
try :#line:3123
        page =unque_plus (params ["page"])#line:3124
except :#line:3125
        pass #line:3126
try :#line:3127
        cat_level =unque_plus (params ["cat_level"])#line:3128
except :#line:3129
        pass #line:3130
try :#line:3131
        index_depth =unque_plus (params ["index_depth"])#line:3132
except :#line:3133
        pass #line:3134
try :#line:3135
        data =unque_plus (params ["data"])#line:3136
except :#line:3137
        pass #line:3138
try :#line:3139
        selected_list =unque_plus (params ["selected_list"])#line:3140
except :#line:3141
        pass #line:3142
try :#line:3143
        lang =unque_plus (params ["lang"])#line:3144
except :#line:3145
        pass #line:3146
selected_list =""#line:3147
def cat (O00OOO00OO0000OO0 ,OOO0OO0OOO0000000 ):#line:3149
    logging .warning ('url')#line:3150
    logging .warning (O00OOO00OO0000OO0 )#line:3151
    global sort_option #line:3152
    OO000000O0OO0OOO0 =[]#line:3153
    if 'cat'in O00OOO00OO0000OO0 :#line:3154
      O0000O0O00O0O00OO =domain_s +'api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'#line:3155
      O000000O0O0OOOO0O =requests .get (O0000O0O00O0O00OO ).json ()#line:3156
      for OOO00O00O0O0OO0O0 in O000000O0O0OOOO0O ['genres']:#line:3157
        dbcur .execute ("SELECT * FROM MyTable where data like '%{0}%'".format (OOO00O00O0O0OO0O0 ['name']))#line:3159
        OO000OO0O0O0O0O0O =dbcur .fetchone ()#line:3161
        if OO000OO0O0O0O0O0O !=None :#line:3162
          if KODI_VERSION>18:
            OO000000O0OO0OOO0 .append (addDir3 (OOO00O00O0O0OO0O0 ['name'],'www',12 ,in_cat [0 ],in_cat [1 ],OOO00O00O0O0OO0O0 ['name']))#line:3163
          else:
            OO000000O0OO0OOO0 .append (addDir3 (OOO00O00O0O0OO0O0 ['name'].encode ('utf8'),'www',12 ,in_cat [0 ],in_cat [1 ],OOO00O00O0O0OO0O0 ['name'].encode ('utf8')))#line:3163
    elif 'year'in O00OOO00OO0000OO0 :#line:3164
        import datetime #line:3165
        O0O0OOOO00OO00OOO =datetime .datetime .now ()#line:3166
        for O0O00O00O0O0O0O00 in range ((O0O0OOOO00OO00OOO .year ),1950 ,-1 ):#line:3168
         dbcur .execute ("SELECT * FROM MyTable where data like '%\"year\": \"{0}\"%' ".format (str (O0O00O00O0O0O0O00 )))#line:3169
         OO000OO0O0O0O0O0O =dbcur .fetchone ()#line:3171
         if OO000OO0O0O0O0O0O !=None :#line:3172
          OO000000O0OO0OOO0 .append (addDir3 (str (O0O00O00O0O0O0O00 ),'year$$$$$'+str (O0O00O00O0O0O0O00 ),12 ,in_year_img [0 ],in_year_img [1 ],str (O0O00O00O0O0O0O00 )))#line:3173
        sort_option =False #line:3174
    elif 'aleph'in O00OOO00OO0000OO0 :#line:3175
      OOO0O0OOOO0OOOO0O =['1-2','א','ב','ג','ד','ה','ו','ז','ח','ט','י','כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']#line:3176
      for OOO00O00O0O0OO0O0 in OOO0O0OOOO0OOOO0O :#line:3177
        OO000000O0OO0OOO0 .append (addDir3 (OOO00O00O0O0OO0O0 ,'letters',12 ,in_letter_img [0 ],in_letter_img [1 ],OOO00O00O0O0OO0O0 ))#line:3178
    elif 'rating'in O00OOO00OO0000OO0 :#line:3179
      for O0O00O00O0O0O0O00 in range (10 ,0 ,-1 ):#line:3180
         dbcur .execute ("SELECT * FROM MyTable where data like '%\"rating\": \"{0}\"%'".format (str (O0O00O00O0O0O0O00 )))#line:3181
         OO000OO0O0O0O0O0O =dbcur .fetchone ()#line:3183
         if OO000OO0O0O0O0O0O !=None :#line:3184
          OO000000O0OO0OOO0 .append (addDir3 (str (O0O00O00O0O0O0O00 ),'rating',12 ,in_ratin_img [0 ],in_ratin_img [1 ],str (O0O00O00O0O0O0O00 )))#line:3185
      sort_option =False #line:3186
    xbmcplugin .addDirectoryItems (int (sys .argv [1 ]),OO000000O0OO0OOO0 ,len (OO000000O0OO0OOO0 ))#line:3187
def cat_sel (OO00O000O0OO00O0O ,OOOOO0O00OO0OOOOO ,OO000OOOOOOO0O0OO ,O0OOOOO000O00O0O0 ):#line:3188
        OO0000O0OOOO0O0OO =[]#line:3189
        OO00O000O0OO00O0O =OO00O000O0OO00O0O .replace ('[COLOR aqua][I]-עמוד הבא-[/I][/COLOR]','')#line:3190
        OO0OO00OOO00O000O =OO00O000O0OO00O0O #line:3191
        logging .warning (OO00O000O0OO00O0O )#line:3192
        if OOOOO0O00OO0OOOOO =='letters':#line:3193
          if OO00O000O0OO00O0O =='1-2':#line:3194
           dbcur .execute ("SELECT * FROM MyTable WHERE  name LIKE '0%' or name LIKE '1%' or name LIKE '2%' or name LIKE '3%' or name LIKE '4%' or name LIKE '5%' or name LIKE '6%' or name LIKE '7%' or name LIKE '8%' or name LIKE '9%' ")#line:3196
          else :#line:3197
           dbcur .execute ("SELECT * FROM MyTable WHERE name like '{0}%'".format (OO00O000O0OO00O0O ))#line:3198
        elif OOOOO0O00OO0OOOOO =='rating':#line:3199
           dbcur .execute ("SELECT * FROM MyTable where data like '%\"rating\": \"{0}\"%'".format (OO00O000O0OO00O0O ))#line:3200
        elif OO00O000O0OO00O0O .isdigit ():#line:3201
          logging .warning ('name')#line:3202
          logging .warning (OO00O000O0OO00O0O )#line:3203
          dbcur .execute ("SELECT * FROM MyTable where data like '%\"{0}\"%'".format (OO00O000O0OO00O0O .strip ()))#line:3204
          logging .warning ("SELECT * FROM MyTable where data like '%\"{0}\"%'".format (OO00O000O0OO00O0O .strip ()))#line:3205
        else :#line:3206
          if '[B][COLOR burlywood]-הסרטים [/COLOR][/B][B][COLOR aqua]כל- [/COLOR][/B]'in OO00O000O0OO00O0O :#line:3207
            dbcur .execute ("SELECT * FROM MyTable where type='item'")#line:3208
          else :#line:3210
            dbcur .execute ("SELECT * FROM MyTable where data like '%{0}%' and type='item'".format (OO00O000O0OO00O0O ))#line:3211
        O00OO00OOOOO000OO =dbcur .fetchall ()#line:3212
        O00OO0O00O00OOO00 =[]#line:3213
        O00OOO000OOO0O0O0 =int (O0OOOOO000O00O0O0 )#line:3214
        logging .warning (len (O00OO00OOOOO000OO ))#line:3215
        logging .warning ((int (O0OOOOO000O00O0O0 )+max_per_page ))#line:3216
        O0O00000O00OOOOO0 =0 #line:3217
        for O0OOOO0OOOOOOO0OO ,OO00O000O0OO00O0O ,OOO00OOO0OO0OOOOO ,O0OOOOO00O0O0O00O ,O00O00O0O00OO0OOO ,OOOOOOOO00OO0O0OO ,OOOO00OOOO0000O0O ,OOO0000O0OOO0O000 ,OOO0OOO000OOOOOO0 ,OOO0O0O000OOO0O00 ,OO00OO00OO00O0OO0 ,O0O0OO0O00OOOO0OO in O00OO00OOOOO000OO :#line:3218
          if O0O00000O00OOOOO0 >=int (O0OOOOO000O00O0O0 ):#line:3219
              try :#line:3220
                  OOOO00OOOO0000O0O =OOOO00OOOO0000O0O .replace ('[',' ').replace (']',' ').replace ('	','').replace ("\\"," ").replace (': """",',': "" "",').replace (': """"}',': "" ""}').replace (': "",',': " ",').replace (': ""}',': " "}').replace ('""','"').replace ('\n','').replace ('\r','')#line:3221
                  try :#line:3222
                    OO00O000OOOO000OO =json .loads (OOOO00OOOO0000O0O )#line:3223
                  except :#line:3224
                    OO00O000OOOO000OO ={}#line:3225
                    OO00O000OOOO000OO ['plot']=OOOOOOOO00OO0O0OO #line:3226
                    OO00O000OOOO000OO ['icon']=O0OOOOO00O0O0O00O #line:3227
                    OO00O000OOOO000OO ['poster']=O00O00O0O00OO0OOO #line:3228
                  OO0OOO0OOO0OOOO0O =OOO00OOO0OO0OOOOO #line:3229
                  if OO0OOO0OOO0OOOO0O .strip ()not in O00OO0O00O00OOO00 :#line:3231
                      O00OO0O00O00OOO00 .append (OO0OOO0OOO0OOOO0O .strip ())#line:3232
                      
                      OO0000O0OOOO0O0OO .append (addLink (OO00O000O0OO00O0O .replace ("%27","'"),OO0OOO0OOO0OOOO0O .strip (),3 ,False ,OO00O000OOOO000OO ['icon'],OO00O000OOOO000OO ['poster'],OO00O000OOOO000OO ['plot'].replace ("%27","'"),data =OOOO00OOOO0000O0O .replace ("OriginalTitle","originaltitle").replace ("%27","'") ))#line:3235
                      O00OOO000OOO0O0O0 =O00OOO000OOO0O0O0 +1 #line:3236
                  if (O00OOO000OOO0O0O0 >(int (O0OOOOO000O00O0O0 )+max_per_page )):#line:3237
                    logging .warning ('x:'+str (O00OOO000OOO0O0O0 ))#line:3238
                    OO0000O0OOOO0O0OO .append (addDir3 ('[COLOR aqua][I]-עמוד הבא-[/I][/COLOR]'+OO0OO00OOO00O000O .replace (' עמוד הבא ',''),OOOOO0O00OO0OOOOO ,12 ,__PLUGIN_PATH__ +"\\resources\\next_icon.gif",__PLUGIN_PATH__ +"\\resources\\next.gif",'Next page',count =O00OOO000OOO0O0O0 ,lang =OO000OOOOOOO0O0OO ))#line:3239
                    break #line:3240
              except Exception as OOOOO00OOO000O00O :#line:3243
                logging .warning (OOOOO00OOO000O00O )#line:3244
                logging .warning (OO00O000O0OO00O0O )#line:3245
                pass #line:3246
          O0O00000O00OOOOO0 +=1 #line:3247
        xbmcplugin .addDirectoryItems (int (sys .argv [1 ]),OO0000O0OOOO0O0OO ,len (OO0000O0OOOO0O0OO ))#line:3248
def check_link (O00O0O0O00O0O0O00 ,full_data =False ):#line:3249
    O0O0OOO0OOO0O0OOO =["The video has been blocked at the copyright owner".lower (),"his stream doesn't exist !".lower (),'Invalid Download Link'.lower (),'page not found','this file has been removed ','removed due a copyright violation','no longer available','file has been deleted','Page Not Found','got removed by the owner.','it maybe got deleted','file not found','file was deleted','<title>Error 404</title>','<H2>Error 404</H2>','<h1>Not Found</h1>','<b>File Not Found</b>']#line:3250
    if full_data ==False :#line:3251
      O00O0OO00OOO0OO0O =O00O0O0O00O0O0O00 .content #line:3252
    else :#line:3253
      O00O0OO00OOO0OO0O =O00O0O0O00O0O0O00 #line:3254
    if len (O00O0OO00OOO0OO0O )<20 :#line:3255
      return False ,'Len'#line:3256
    OOO00OO0O0OOOO0OO =0 #line:3257
    OO00OO00000OO00O0 =0 #line:3258
    for OO0000OO0OO000O0O in O0O0OOO0OOO0O0OOO :#line:3259
        if OO0000OO0OO000O0O in O00O0OO00OOO0OO0O .lower ():#line:3260
            OO00OO00000OO00O0 =1 #line:3261
            break #line:3262
        OOO00OO0O0OOOO0OO +=1 #line:3263
    if OO00OO00000OO00O0 ==1 :#line:3264
      return False ,'String Error: '+O0O0OOO0OOO0O0OOO [OOO00OO0O0OOOO0OO ]#line:3265
    else :#line:3266
      return True ,'ok'#line:3267
def server_data (O0O0OO00000OOO000 ,c_head ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}):#line:3268
       try :#line:3269
        import resolveurl #line:3272
        if 'nowvideo.sx'in O0O0OO00000OOO000 :#line:3273
          return True ,'ok'#line:3274
        OO0O000OOOOOO0OO0 =resolveurl .HostedMediaFile (O0O0OO00000OOO000 ).valid_url ()#line:3275
        if OO0O000OOOOOO0OO0 ==False :#line:3278
          if 'sratim-il.com'in O0O0OO00000OOO000 :#line:3280
              OOO0OOOOOO00O00O0 ='/(.+?).mp4'#line:3281
              OO0OOO0OOOOOOO0O0 =re .compile (OOO0OOOOOO00O00O0 ).findall (O0O0OO00000OOO000 )#line:3282
              OOO0OOOOOO00O00O0 ='//(.+?)/'#line:3283
              OOOO00O0OOOO0OO0O =re .compile (OOO0OOOOOO00O00O0 ).findall (O0O0OO00000OOO000 )[0 ]#line:3284
              class O0OOO00O0OO00OOO0 :#line:3285
                 name =''#line:3286
                 value =''#line:3287
              c_head ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0','Accept':'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5','Accept-Language':'en-US,en;q=0.5','Host':OOOO00O0OOOO0OO0O ,'Connection':'keep-alive','Pragma':'no-cache','Cache-Control':'no-cache',}#line:3298
              O00OOOOO0O0O00O00 =requests .get (O0O0OO00000OOO000 .replace ('.mp4','')+'/',headers =c_head ,verify =False ).cookies #line:3299
              for O0OOO00O0OO00OOO0 in O00OOOOO0O0O00O00 :#line:3300
                  logging .warning (O0OOO00O0OO00OOO0 .name )#line:3301
                  logging .warning (O0OOO00O0OO00OOO0 .value )#line:3302
              c_head ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0','Accept':'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5','Accept-Language':'en-US,en;q=0.5','Referer':'https://www.sratim.co/'+OO0OOO0OOOOOOO0O0 [0 ],'Host':OOOO00O0OOOO0OO0O ,'Cookie':'%s=%s'%(O0OOO00O0OO00OOO0 .name ,O0OOO00O0OO00OOO0 .value ),'Connection':'keep-alive','Pragma':'no-cache','Cache-Control':'no-cache',}#line:3313
          if 'http://cdn1.smotrim.live'in O0O0OO00000OOO000 or 'letsupload'in O0O0OO00000OOO000 :#line:3314
           return True ,'ok'#line:3315
          O00OOOOO0O0O00O00 =requests .head (O0O0OO00000OOO000 ,headers =c_head ,timeout =20 ,verify =False )#line:3316
          logging .warning ('f_link')#line:3317
          logging .warning (O0O0OO00000OOO000 )#line:3318
          logging .warning (O00OOOOO0O0O00O00 .status_code )#line:3319
          logging .warning (O00OOOOO0O0O00O00 )#line:3320
          if O00OOOOO0O0O00O00 .status_code !=200 and O00OOOOO0O0O00O00 .status_code !=302 :#line:3321
            return False ,'status_code: '+str (O00OOOOO0O0O00O00 .status_code )#line:3322
          return True ,'ok'#line:3324
        if 'http'not in O0O0OO00000OOO000 :#line:3325
           return False ,'no HTTP'#line:3326
        if 'estream'in O0O0OO00000OOO000 :#line:3327
          return False ,'estream'#line:3328
        O0O0OO0O0OO0OOO00 =requests .get (O0O0OO00000OOO000 ,headers =c_head ,timeout =10 ).content #line:3332
        if 'google'in O0O0OO00000OOO000 and 'video-downloads'not in O0O0OO00000OOO000 and 'doc-'not in O0O0OO00000OOO000 :#line:3334
            if 'fmt_list'not in O0O0OO0O0OO0OOO00 :#line:3335
                return False ,'NO GOOGLE Stream'#line:3336
        O00000OOO00O0OOO0 ,O0OOOOOO0OO0OO0OO =check_link (O0O0OO0O0OO0OOO00 ,full_data =True )#line:3337
        return O00000OOO00O0OOO0 ,O0OOOOOO0OO0OO0OO #line:3338
       except Exception as O0OOOOOO0OO0OO0OO :#line:3339
          logging .warning (O0OOOOOO0OO0OO0OO )#line:3340
          logging .warning (O0O0OO00000OOO000 )#line:3341
          return False ,O0OOOOOO0OO0OO0OO #line:3342
#if os .path .getsize (os .path .join (os .path .dirname (__file__ ),'cfscrape.py'))!=11082 :#line:3343
#    mode ='next'#line:3344
#    url ='www'#line:3345
def check_all ():#line:3346
    dbcur .execute ("SELECT * FROM MyTable where type='item'")#line:3347
    import time #line:3348
    O0000O0O0O0O0OOOO =dbcur .fetchall ()#line:3349
    OO00OO00OO0O00O00 =[]#line:3350
    O0O00O0OO00OOOOOO =xbmcgui .DialogProgress ()#line:3351
    O0O00O0OO00OOOOOO .create ('בודק קישורים',"[COLOR orange][B]טוען רשימות[/B][/COLOR]",'')#line:3352
    O0O00O0OO00OOOOOO .update (0 ,'אנא המתן',c_addon_name ,'')#line:3353
    OO00O0OOOO0O00000 =0 #line:3354
    O00O000OO00OOOOOO =[]#line:3355
    O00OOOO00000O0OO0 =time .time ()#line:3356
    for OO0O0OO00OOOO0OOO ,O0O0OO0OO0OOO0OO0 ,OOOOOOOOOOOO0000O ,OOO0000O00000O000 ,OOOOO0OOO0O00O0O0 ,O0O00OO00OOOOOOO0 ,O0OOOOO00O00OOO00 ,O00OOOO00000OOOO0 ,OO00O0O0000O00O0O ,O00OO0OOOO00O0OOO ,OOO000O0OO00OOOOO ,OOO00000O0O000O0O in O0000O0O0O0O0OOOO :#line:3357
      try :#line:3358
        OOOOOOOOOOOO0000O =gdecom (OOOOOOOOOOOO0000O )#line:3359
      except :#line:3360
       pass #line:3361
      OOOOOOOOOOOO0000O =OOOOOOOOOOOO0000O .replace ('\n','').replace ('\r','').strip ()#line:3362
      logging .warning (O0OOOOO00O00OOO00 )#line:3363
      try :#line:3364
        O0OOOOO00O00OOO00 =O0OOOOO00O00OOO00 .replace ('[',' ').replace (']',' ').replace ('	','').replace ("\\"," ").replace (': """",',': "" "",').replace (': """"}',': "" ""}').replace (': "",',': " ",').replace (': ""}',': " "}').replace ('""','"').replace ('\n','').replace ('\r','')#line:3365
        OOO0OOO00O0O0OO00 =json .loads (O0OOOOO00O00OOO00 )#line:3366
      except :#line:3367
        OOO0OOO00O0O0OO00 =""#line:3368
      if '$$$'in OOOOOOOOOOOO0000O :#line:3370
           OO0OOOO0OO00OOOO0 =OOOOOOOOOOOO0000O .split ('$$$')#line:3372
           for OOOOOOOOOOOO0000O in OO0OOOO0OO00OOOO0 :#line:3373
             if O0O00O0OO00OOOOOO .iscanceled ():#line:3374
                O0O00O0OO00OOOOOO .close ()#line:3375
                break #line:3376
             O0O00O0O0OO0OO0O0 ,OO00O0O0OOO0O0000 =server_data (OOOOOOOOOOOO0000O )#line:3377
             OO0OO0O00OO0O0OO0 ='white'#line:3378
             if not O0O00O0O0OO0OO0O0 :#line:3379
                OO0OO0O00OO0O0OO0 ='red'#line:3380
                O00O000OO00OOOOOO .append ((O0O0OO0OO0OOO0OO0 ,OOO0OOO00O0O0OO00 ,OOOOOOOOOOOO0000O ))#line:3382
             OOO00OO000OO00OO0 =time .time ()-O00OOOO00000O0OO0 #line:3383
             O0O00O0OO00OOOOOO .update (int ((OO00O0OOOO0O00000 )/float (len (O0000O0O0O0O0OOOO ))*100 ),time .strftime ("%H:%M:%S",time .gmtime (OOO00OO000OO00OO0 )),'[COLOR %s]'%OO0OO0O00OO0O0OO0 +O0O0OO0OO0OOO0OO0 +' - '+str (O0O00O0O0OO0OO0O0 )+'[/COLOR]',str (OO00O0OOOO0O00000 )+'/'+str (len (O0000O0O0O0O0OOOO )))#line:3384
             OO00O0OOOO0O00000 =OO00O0OOOO0O00000 +1 #line:3385
      else :#line:3386
          if O0O00O0OO00OOOOOO .iscanceled ():#line:3387
                O0O00O0OO00OOOOOO .close ()#line:3388
                break #line:3389
          O0O00O0O0OO0OO0O0 ,OO00O0O0OOO0O0000 =server_data (OOOOOOOOOOOO0000O )#line:3390
          OO0OO0O00OO0O0OO0 ='white'#line:3391
          if not O0O00O0O0OO0OO0O0 :#line:3392
            OO0OO0O00OO0O0OO0 ='red'#line:3393
            O00O000OO00OOOOOO .append ((O0O0OO0OO0OOO0OO0 ,OOO0OOO00O0O0OO00 ,OOOOOOOOOOOO0000O ))#line:3395
          OOO00OO000OO00OO0 =time .time ()-O00OOOO00000O0OO0 #line:3396
          O0O00O0OO00OOOOOO .update (int ((OO00O0OOOO0O00000 )/float (len (O0000O0O0O0O0OOOO ))*100 ),time .strftime ("%H:%M:%S",time .gmtime (OOO00OO000OO00OO0 )),'[COLOR %s]'%OO0OO0O00OO0O0OO0 +O0O0OO0OO0OOO0OO0 +' - '+str (O0O00O0O0OO0OO0O0 )+'[/COLOR]',str (OO00O0OOOO0O00000 )+'/'+str (len (O0000O0O0O0O0OOOO )))#line:3397
          OO00O0OOOO0O00000 =OO00O0OOOO0O00000 +1 #line:3398
    OOO0O00OOO0O000O0 =''#line:3399
    for O0O0OO0OO0OOO0OO0 ,O0OOOOO00O00OOO00 ,OOOOOOOOOOOO0000O in O00O000OO00OOOOOO :#line:3401
      OOO0O00OOO0O000O0 =OOO0O00OOO0O000O0 +O0O0OO0OO0OOO0OO0 +' - '+O0OOOOO00O00OOO00 ['year']+' - '+OOOOOOOOOOOO0000O +'\n'#line:3402
    if len (O00O000OO00OOOOOO )>0 :#line:3403
            O0O0OOO000000OOO0 =os .path .join (user_dataDir ,'server_text_result.txt')#line:3404
            OO00OOO0O00OOO0O0 =open (O0O0OOO000000OOO0 ,'w')#line:3405
            OO00OOO0O00OOO0O0 .write (OOO0O00OOO0O000O0 )#line:3407
            OO00OOO0O00OOO0O0 .close ()#line:3410
            TextBox (' - התקולים'+str (len (O00O000OO00OOOOOO )),OOO0O00OOO0O000O0 )#line:3412
def latest (O000000O000OOO0O0 ):#line:3415
        import datetime ,time #line:959
        import _strptime 
    
        OOOOOOOOOO000O000 =os .path .join (__PLUGIN_PATH__ ,"resources")#line:3416
        O000OO0OO00OO0O0O =[]#line:3419
        OO00OOO0O0000OO0O =[]#line:3420
        OO0OO00O0OOOOOOO0 =[]#line:3421
        if O000000O000OOO0O0 =='movie':#line:3422
            O000OO00OO0000000 ='\'%"mediatype": "movie"%\''#line:3423
        else :#line:3424
            O000OO00OO0000000 ='\'%"mediatype": "tv"%\''#line:3425
        logging .warning (O000OO00OO0000000 )#line:3426
        dbcur .execute ("SELECT * FROM MyTable where type='item' and data like "+O000OO00OO0000000 )#line:3427
        O0OOOO0000O000000 =dbcur .fetchall ()#line:3429
        for OO0000O000O00OOOO ,O00000O000OO0OOO0 ,O0O0OOO0OOO0O0O00 ,O00OOO00OOO00O0O0 ,O0OO0O00000000000 ,O00OO00OO00OO00OO ,O00OOO0O000OO0OO0 ,O0OO0OO00OO00O00O ,O0O0OOOO0OOOO00OO ,O0O0O0O000000000O ,O000OOOOOOO00O000 ,OOOO000O00OOO0O00 in O0OOOO0000O000000 :#line:3430
          if KODI_VERSION<=18:
              O00000O000OO0OOO0 =O00000O000OO0OOO0 .encode ('utf8')#line:3431
              O0O0OOO0OOO0O0O00 =O0O0OOO0OOO0O0O00 .encode ('utf8')#line:3432
              O00OOO00OOO00O0O0 =O00OOO00OOO00O0O0 .encode ('utf8')#line:3433
              O0OO0O00000000000 =O0OO0O00000000000 .encode ('utf8')#line:3434
              O00OO00OO00OO00OO =O00OO00OO00OO00OO .encode ('utf8')#line:3435
              O00OOO0O000OO0OO0 =O00OOO0O000OO0OO0 .encode ('utf8')#line:3436
              O0OO0OO00OO00O00O =O0OO0OO00OO00O00O .encode ('utf8')#line:3437
              O0O0OOOO0OOOO00OO =O0O0OOOO0OOOO00OO .encode ('utf8')#line:3438
              O0O0O0O000000000O =O0O0O0O000000000O .encode ('utf8')#line:3439
              O000OOOOOOO00O000 =O000OOOOOOO00O000 .encode ('utf8')#line:3440
              OOOO000O00OOO0O00 =OOOO000O00OOO0O00 .encode ('utf8')#line:3441
          else:
              O00000O000OO0OOO0 =O00000O000OO0OOO0 #line:3431
              O0O0OOO0OOO0O0O00 =O0O0OOO0OOO0O0O00 #line:3432
              O00OOO00OOO00O0O0 =O00OOO00OOO00O0O0 #line:3433
              O0OO0O00000000000 =O0OO0O00000000000 #line:3434
              O00OO00OO00OO00OO =O00OO00OO00OO00OO #line:3435
              O00OOO0O000OO0OO0 =O00OOO0O000OO0OO0 #line:3436
              O0OO0OO00OO00O00O =O0OO0OO00OO00O00O #line:3437
              O0O0OOOO0OOOO00OO =O0O0OOOO0OOOO00OO #line:3438
              O0O0O0O000000000O =O0O0O0O000000000O #line:3439
              O000OOOOOOO00O000 =O000OOOOOOO00O000 #line:3440
              OOOO000O00OOO0O00 =OOOO000O00OOO0O00 #line:3441
          try :#line:3445
            if '{'in O00OOO0O000OO0OO0 :#line:3446
              O00OOO0O000OO0OO0 =O00OOO0O000OO0OO0 .replace ('[',' ').replace (']',' ').replace ('	','').replace ("\\"," ").replace (': """",',': "" "",').replace (': """"}',': "" ""}').replace (': "",',': " ",').replace (': ""}',': " "}').replace ('""','"').replace ('\n','').replace ('\r','')#line:3447
              OOO00O000OOOO0OO0 =json .loads (O00OOO0O000OO0OO0 )#line:3448
              try :#line:3449
                  O0OO0000000O000OO =datetime .datetime .strptime (OOO00O000OOOO0OO0 ['dateadded'],'%Y-%m-%d %H:%M:%S')#line:3450
              except TypeError :#line:3451
                  O0OO0000000O000OO =datetime .datetime (*(time .strptime (OOO00O000OOOO0OO0 ['dateadded'],'%Y-%m-%d %H:%M:%S')[0 :6 ]))#line:3452
              O0000O0OOOO000OOO =time .mktime (O0OO0000000O000OO .timetuple ())#line:3454
              if OOO00O000OOOO0OO0 ['mediatype']=='tv':#line:3455
                    O00000O000OO0OOO0 =' - [COLOR yellow][I]'+OOO00O000OOOO0OO0 ['originaltitle']+'[/I][/COLOR] - S'+str (OOO00O000OOOO0OO0 ['Season'])+'E'+str (OOO00O000OOOO0OO0 ['Episode'])#line:3456
              O000OO0OO00OO0O0O .append ((O00000O000OO0OOO0 ,O0O0OOO0OOO0O0O00 .strip (),OOO00O000OOOO0OO0 ['icon'],OOO00O000OOOO0OO0 ['poster'],OOO00O000OOOO0OO0 ['plot'],O00OOO0O000OO0OO0 .replace ("OriginalTitle","originaltitle"),"",O0000O0OOOO000OOO ))#line:3457
          except Exception as O0OOO0O00000O0OO0 :#line:3458
           logging .warning ('Error latest::'+str(O0OOO0O00000O0OO0 ))#line:3460
           pass #line:3461
        O000OO0OO00OO0O0O =sorted (O000OO0OO00OO0O0O ,key =lambda OO000OOOO0O0000OO :OO000OOOO0O0000OO [7 ],reverse =True )#line:3463
        OOOO0OOO0O000OO0O =int (Addon .getSetting ("max_new"))#line:3464
        OOOOO00000O00OO0O =0 #line:3465
        for O00000O000OO0OOO0 ,O0O0000000O00000O ,O00OOO00OOO00O0O0 ,O0OO0O00000000000 ,O00OO00OO00OO00OO ,O00OOO0O000OO0OO0 ,O0000OOOO00000O00 ,OOO000OO00O0000OO in O000OO0OO00OO0O0O :#line:3466
            if O0O0000000O00000O .strip ()not in OO0OO00O0OOOOOOO0 :#line:3468
              OO0OO00O0OOOOOOO0 .append (O0O0000000O00000O .strip ())#line:3469
              OO00OOO0O0000OO0O .append (addLink (O00000O000OO0OOO0 ,O0O0000000O00000O ,3 ,False ,O00OOO00OOO00O0O0 ,O0OO0O00000000000 ,O00OO00OO00OO00OO ,data =O00OOO0O000OO0OO0 ))#line:3472
              if OOOOO00000O00OO0O >OOOO0OOO0O000OO0O :#line:3473
                break #line:3474
              OOOOO00000O00OO0O +=1 #line:3475
        xbmcplugin .addDirectoryItems (int (sys .argv [1 ]),OO00OOO0O0000OO0O ,len (OO00OOO0O0000OO0O ))#line:3476
def check_update_from_master ():#line:3477
    from shutil import copyfile ,copytree ,rmtree #line:3478
    from os import listdir #line:3479
    from os .path import isfile ,join #line:3480
    OO000O0OO000O0OOO =xbmc .translatePath ("special://home/addons/plugin.program.master_pen/")#line:3481
    if os .path .exists (OO000O0OO000O0OOO ):#line:3482
        OO000O0OO0O000000 =xbmcaddon .Addon (id ='plugin.program.master_pen')#line:3483
        O0OO00OOO0000OOOO =int (OO000O0OO0O000000 .getAddonInfo ("version").replace ('.',''))#line:3484
        OOO0000O00O00O000 =OO000O0OO0O000000 .getAddonInfo ("version")#line:3485
        OOO0OO0O0OO0OOOOO =os .path .join (__PLUGIN_PATH__ ,'addon.xml')#line:3486
        O0OOOOOOO00OO0OO0 =open (OOO0OO0O0OO0OOOOO ,'r')#line:3488
        O00OO00OO000O0OOO =O0OOOOOOO00OO0OO0 .read ()#line:3490
        O0OOOOOOO00OO0OO0 .close ()#line:3491
        OOOOO0000OO000OO0 ='name=".+?version="(.+?)"'#line:3492
        OOO0O0OOO0O0OO0OO =re .compile (OOOOO0000OO000OO0 ,re .DOTALL ).findall (O00OO00OO000O0OOO )[0 ]#line:3493
        O0OO000OO0OOO0OO0 =int (OOO0O0OOO0O0OO0OO .replace ('.',''))#line:3494
        OO0OOOO00O0O00000 =os .path .join (__PLUGIN_PATH__ ,'pytube','__init__.py')#line:3496
        O0OOOOOOO00OO0OO0 =open (OO0OOOO00O0O00000 ,'r')#line:3498
        O0OOO0000O000000O =O0OOOOOOO00OO0OO0 .read ()#line:3500
        O0OOOOOOO00OO0OO0 .close ()#line:3501
        OOOOO0000OO000OO0 ="__version__ = '(.+?)'"#line:3502
        O0O0OOOOOO00O0OOO =re .compile (OOOOO0000OO000OO0 ,re .DOTALL ).findall (O0OOO0000O000000O )[0 ]#line:3503
        OOOO0O0O0OOO0O0OO =O0O0OOOOOO00O0OOO #line:3504
        OO0OOO000OOOO0O0O =xbmc .translatePath ("special://home/addons/plugin.program.master_pen/")#line:3505
        if O0OO00OOO0000OOOO >O0OO000OO0OOO0OO0 or OOOO0O0O0OOO0O0OO !='9.3.1'or (not os .path .exists (os .path .join (__PLUGIN_PATH__ ,'resources','skins','DefaultSkin','1080i','Contact2.xml'))):#line:3506
            if O0OO000OO0OOO0OO0 <533 :#line:3507
                   O0OOOOO0OOOOOOO00 =os .path .join (user_dataDir ,'database2.db')#line:3508
                   if os .path .exists (O0OOOOO0OOOOOOO00 ):#line:3509
                        OOO00000OO0OOO000 =database .connect (O0OOOOO0OOOOOOO00 )#line:3511
                        OOO00000OO0OOO000 .close ()#line:3512
                        os .unlink (O0OOOOO0OOOOOOO00 )#line:3513
            OOO00O000O0OO0000 =xbmcgui .DialogProgress ()#line:3514
            OOO00O000O0OO0000 .create (c_addon_name ,"[COLOR orange][B]נמצא עדכון מעדכן...[/B][/COLOR]")#line:3515
            OOO00O000O0OO0000 .update (0 ,'אנא המתן',c_addon_name )#line:3516
            OO000O0000O00O0O0 =[O000OO0O00OOO0OO0 for O000OO0O00OOO0OO0 in listdir (OO0OOO000OOOO0O0O )if isfile (join (OO0OOO000OOOO0O0O ,O000OO0O00OOO0OO0 ))]#line:3518
            O00OOOO000OO0O00O =0 #line:3519
            for O0OOO0O0000O00OOO in OO000O0000O00O0O0 :#line:3520
              if 'defen.py'not in O0OOO0O0000O00OOO and 'fanart.jpg'not in O0OOO0O0000O00OOO and 'icon.png'not in O0OOO0O0000O00OOO and 'addon.xml'not in O0OOO0O0000O00OOO :#line:3521
                OOO00O000O0OO0000 .update (int ((O00OOOO000OO0O00O )/float (len (OO000O0000O00O0O0 ))*100 ),'טוען',O0OOO0O0000O00OOO )#line:3522
                OO0O00OOOO0000O0O =os .path .join (OO0OOO000OOOO0O0O ,O0OOO0O0000O00OOO )#line:3523
                OOO0O0OOOO00O0O00 =os .path .join (__PLUGIN_PATH__ ,O0OOO0O0000O00OOO )#line:3524
                copyfile (OO0O00OOOO0000O0O ,OOO0O0OOOO00O0O00 )#line:3525
            OOO00O000O0OO0000 .update (90 ,c_addon_name ,'מעדכן js2py עלול לקחת קצת זמן...')#line:3526
            OO0000OO00OOO00O0 =os .path .join (OO0OOO000OOOO0O0O ,'js2py')#line:3527
            OOO0O0OOO0000000O =os .path .join (__PLUGIN_PATH__ ,'js2py')#line:3528
            rmtree (OOO0O0OOO0000000O )#line:3529
            OO0O00OOOO0000O0O =OO0000OO00OOO00O0 #line:3530
            OOO0O0OOOO00O0O00 =OOO0O0OOO0000000O #line:3531
            copytree (OO0O00OOOO0000O0O ,OOO0O0OOOO00O0O00 )#line:3532
            OOO00O000O0OO0000 .update (90 ,c_addon_name ,'מעדכן pytube עלול לקחת קצת זמן...')#line:3534
            O0OOOO000O000O00O =os .path .join (OO0OOO000OOOO0O0O ,'pytube')#line:3535
            OO00000OO0O00O0O0 =os .path .join (__PLUGIN_PATH__ ,'pytube')#line:3536
            rmtree (OO00000OO0O00O0O0 )#line:3537
            OO0O00OOOO0000O0O =O0OOOO000O000O00O #line:3538
            OOO0O0OOOO00O0O00 =OO00000OO0O00O0O0 #line:3539
            copytree (OO0O00OOOO0000O0O ,OOO0O0OOOO00O0O00 )#line:3540
            O0OOOO000O000O00O =os .path .join (OO0OOO000OOOO0O0O ,'resources','skins')#line:3542
            OO00000OO0O00O0O0 =os .path .join (__PLUGIN_PATH__ ,'resources','skins')#line:3543
            rmtree (OO00000OO0O00O0O0 )#line:3544
            OO0O00OOOO0000O0O =O0OOOO000O000O00O #line:3545
            OOO0O0OOOO00O0O00 =OO00000OO0O00O0O0 #line:3546
            copytree (OO0O00OOOO0000O0O ,OOO0O0OOOO00O0O00 )#line:3547
            O0OO000O00O000OOO =xbmc .translatePath ("special://home/addons/")#line:3549
            OOOO000O00OOO0OOO =Addon .getAddonInfo ('path').replace (O0OO000O00O000OOO ,'')#line:3550
            OO00OO0O0000000O0 =os .path .join (OO000O0OO000O0OOO ,'resources','settings.xml')#line:3552
            O0OOOOOOO00OO0OO0 =open (OO00OO0O0000000O0 ,'r')#line:3553
            O00O00O00OO00O0OO =O0OOOOOOO00OO0OO0 .read ()#line:3555
            O0OOOOOOO00OO0OO0 .close ()#line:3556
            O00O00O00OO00O0OO =O00O00O00OO00O0OO .replace ('addon_name',OOOO000O00OOO0OOO )#line:3558
            OO0O0OOO00000O0OO =os .path .join (__PLUGIN_PATH__ ,'resources','settings.xml')#line:3559
            O0OOOOOOO00OO0OO0 =open (OO0O0OOO00000O0OO ,'w')#line:3562
            O0OOOOOOO00OO0OO0 .write (O00O00O00OO00O0OO )#line:3564
            O0OOOOOOO00OO0OO0 .close ()#line:3565
            O00OO00OO000O0OOO =O00OO00OO000O0OOO .replace ('version="%s"   '%OOO0O0OOO0O0OO0OO ,'version="%s"   '%OOO0000O00O00O000 )#line:3570
            O0OOOOOOO00OO0OO0 =open (OOO0OO0O0OO0OOOOO ,'w')#line:3572
            O0OOOOOOO00OO0OO0 .write (O00OO00OO000O0OOO )#line:3575
            O0OOOOOOO00OO0OO0 .close ()#line:3576
            OOO00O000O0OO0000 .close ()#line:3578
            '''
            my_defen_file=os.path.join(__PLUGIN_PATH__,'defen.py')
            file = open(my_defen_file, 'r') 

            my_defen_data=file.read() 
            file.close()
            
            if 'whats_new=True' not in my_defen_data and 'whats_new=False' not in my_defen_data:
                my_defen_data=my_defen_data+'\nwhats_new=True'

            
                file = open(my_defen_file,'w') 
     
                file.write(my_defen_data) 
                file.close()
            '''#line:3594
            xbmc .executebuiltin ((u'Notification(%s,%s)'%('עדכון',' - העדכון הסתיים '+OOO0000O00O00O000 )).encode ('utf-8'))#line:3596
            xbmc .executebuiltin (('ActivateWindow(10025,"plugin://%s/?name=' '&mode=None",return)'%addon_id ))#line:3597
            sys .exit ()#line:3600
    return 0 #line:3601
def run_link (OO0000O0OOO00O0O0 ):#line:3602
    OOOO0000O0O0O0O0O =''#line:3603
    O0000000OO0OO0OOO =xbmc .Keyboard (OOOO0000O0O0O0O0O ,'הכנס קישור')#line:3604
    O0000000OO0OO0OOO .doModal ()#line:3605
    if O0000000OO0OO0OOO .isConfirmed ():#line:3606
        OOOO0000O0O0O0O0O =O0000000OO0OO0OOO .getText ()#line:3607
        OOOO0O0000OO00O0O =xbmc .translatePath ("special://home/addons/")#line:3609
        O00O0O00O00OO0000 =Addon .getAddonInfo ('path').replace (OOOO0O0000OO00O0O ,'')#line:3610
        OO0000O0OOO00O0O0 ='plugin://%s?mode=3&url=%s'%(O00O0O00O00OO0000 ,que (OOOO0000O0O0O0O0O ))#line:3612
        xbmc .executebuiltin ('XBMC.PlayMedia("%s")'%OO0000O0OOO00O0O0 )#line:3613
def renew_data ():#line:3614
    global dbcur ,dbcon #line:3615
    dbcur .close ()#line:3616
    dbcon .close ()#line:3617
    logging .warning ('Download')#line:3618
    OO00O00O0OOO00000 =os .path .join (__PLUGIN_PATH__ ,"resources")#line:3619
    download_file (l_list ,OO00O00O0OOO00000 )#line:3620
    logging .warning ('Extract')#line:3622
    logging .warning ('Extract2')#line:3625
    unzip (os .path .join (OO00O00O0OOO00000 ,"fixed_list.zip"))#line:3628
    dbcon =database .connect (cacheFile )#line:3629
    dbcur =dbcon .cursor ()#line:3630
    logging .warning ('Done Extract')#line:3631
    dbcur .execute ("SELECT * FROM MyTable sort order by strftime('%Y-%m-%d %H:%M:%S',date) DESC")#line:3633
    O00OO00O0O000OO00 =dbcur .fetchall ()#line:3635
    threading .Thread (target =check_updted ,args =(O00OO00O0O000OO00 ,)).start ()#line:3637
    return 'ok'#line:3639
logging .warning ('mode1111111111111111111111111111')#line:3640
logging .warning (mode )#line:3641
#check_update_from_master ()#line:3643
'''
if standalone==True:
    if mode==None:
      
       if enter:
        pass_ok=False
        search_entered =''
        keyboard = xbmc.Keyboard(search_entered, 'הכנס סיסמא')
        keyboard.doModal()
        if keyboard.isConfirmed():
                    search_entered = keyboard.getText()
                    x=requests.get(enter[0].decode('base64')).content
                    if search_entered!=x:
                       sys.exit()
                    else:
                      pass_ok=True
        if not pass_ok:
          sys.exit()
       check,a_data=check_jump_stage(name,url,lang)
       if check:
         
         name,url,mode,iconimage,fanart,description,data,cat_level,selected_list,lang=a_data
'''#line:3666
#renew_data()
logging.warning('Mode:')
logging .warning (mode )#line:3668
logging .warning ('url')#line:3669
logging .warning (url )#line:3670
tts =int (Addon .getSetting ("save_data"))#line:3672
logging.warning('tts')
logging.warning(tts)

all_img2 =cache .get (renew_data ,tts ,table ='posters')#line:3674
logging .warning ('Starting1111111')#line:3675
logging .warning ('Mode')#line:3677
logging .warning (mode )#line:3678
if mode ==None or url ==None or len (url )<1 :#line:3679
        import os #line:3680
        main_menu ()#line:3683
elif mode ==2 :#line:3688
     scrape_all (name ,url ,lang )#line:3689
elif mode ==3 :#line:3690
     logging.warning('Starting Play')
     play_link (name ,url ,data ,lang ,description ,cat_level )#line:3691
elif mode ==4 :#line:3692
     ok =run_addon (url )#line:3693
elif mode ==5 :#line:3694
  logging .warning ('deep')#line:3695
  deep_scrape (name ,url ,cat_level ,count ,selected_list ,lang )#line:3696
elif mode ==6 :#line:3697
    search_all (lists ,lang ,url )#line:3698
elif mode ==7 :#line:3699
    display_shop (url )#line:3700
elif mode ==8 :#line:3701
    install_list (url )#line:3702
elif mode ==9 :#line:3703
    disply_hwr ()#line:3704
elif mode ==10 :#line:3705
    play_youtube (url ,name )#line:3707
elif mode ==11 :#line:3708
    cat (url ,lang )#line:3710
elif mode ==12 :#line:3711
    cat_sel (name ,url ,lang ,count )#line:3712
elif mode ==13 :#line:3713
    tv_channels ()#line:3714
elif mode ==14 :#line:3715
    play_tv (url )#line:3716
elif mode ==15 :#line:3717
    check_all ()#line:3718
elif mode ==16 :#line:3719
    make_strm (name ,url ,description ,data ,index_depth ,lang )#line:3720
elif mode ==17 :#line:3721
    make_strm_folder (name ,url ,description ,data ,index_depth ,lang ,cat_level )#line:3722
elif mode ==18 :#line:3723
    latest (url )#line:3724
elif mode ==19 :#line:3725
    run_link (url )#line:3726
elif mode ==99 :#line:3727
   import shutil #line:3728
   cacheFile2 =os .path .join (user_dataDir ,'localfile.txt')#line:3730
   cache .clear (['posters'])#line:3731
   if os .path .exists (cacheFile2 ):#line:3732
    dbcur .close ()#line:3735
    dbcon .close ()#line:3736
    os .remove (cacheFile2 )#line:3737
   xbmcgui .Dialog ().ok ('ניקוי',"[B][COLOR burlywood] לחץ אישור [/COLOR][/B][B][COLOR aqua]ההרחבה נוקתה  [/COLOR][/B]")#line:3740
if Addon .getSetting ("lock_dis")=='false':#line:3741
    xbmcplugin .setContent (int (sys .argv [1 ]),"movies")#line:3742
if sort_option ==True and sort_by_episode ==False and mode !=18 :#line:3744
    if mode ==None and sort_option_cat :#line:3745
       checked =True #line:3746
    elif mode ==None :#line:3747
       checked =False #line:3748
    else :#line:3749
        checked =True #line:3750
    if checked :#line:3751
        xbmcplugin .addSortMethod (int (sys .argv [1 ]),xbmcplugin .SORT_METHOD_VIDEO_SORT_TITLE )#line:3752
        xbmcplugin .addSortMethod (int (sys .argv [1 ]),xbmcplugin .SORT_METHOD_VIDEO_YEAR )#line:3753
        xbmcplugin .addSortMethod (int (sys .argv [1 ]),xbmcplugin .SORT_METHOD_DATEADDED )#line:3754
        xbmcplugin .addSortMethod (int (sys .argv [1 ]),xbmcplugin .SORT_METHOD_VIDEO_RATING )#line:3755
elif sort_by_episode ==True and sort_option ==True :#line:3757
    xbmcplugin .addSortMethod (int (sys .argv [1 ]),xbmcplugin .SORT_METHOD_EPISODE )#line:3759
try :#line:3760
    dbcur .close ()#line:3761
    dbcon .close ()#line:3762
except :#line:3763
    pass #line:3764
xbmcplugin .endOfDirectory (int (sys .argv [1 ]),succeeded =True ,cacheToDisc =True )#line:3765
