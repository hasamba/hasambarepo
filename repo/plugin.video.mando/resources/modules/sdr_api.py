import requests,time,re
import json,base64,sys,os
import urllib.parse as urlparse

try:
    import xbmcgui,xbmcaddon,xbmcvfs
    Addon = xbmcaddon.Addon()
    from resources.modules import cache
    from resources.modules import log
    user_dataDir = xbmcvfs.translatePath(Addon.getAddonInfo("profile"))
except:
    import cache
    import logging as log
   
    pass
import threading
BASE_URL='https://www.sdarot.tw'
IMAGE_BASE='https://static.sdarot.tw'
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import urllib
import urllib.parse
que_n=urllib.parse.quote
class Thread (threading.Thread):
       def __init__(self, target, *args):
        super().__init__(target=target, args=args)
       def run(self, *args):
          
          self._target(*self._args)
          return 0
user_dataDir_img=os.path.join(user_dataDir,'sdr_images')
if not os.path.exists(user_dataDir_img):
    os.makedirs(user_dataDir_img)
url_encode=urllib.parse.urlencode
headers = {
    'authority': BASE_URL.replace('https://',''),
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'referer': BASE_URL,
    'Host': BASE_URL.replace('https://',''),
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}
def c_get_html(url,headers={},params={},cookies={},data={},verify=False,get_cookies=False,get_url=False,allow_redirects=True):
    if data!={}:
        
        x=requests.post(url,headers=headers,params=params,cookies=cookies,data=data,verify=verify,allow_redirects=allow_redirects)
      
    else:
     
        x=requests.get(url,headers=headers,params=params,cookies=cookies,verify=verify,allow_redirects=allow_redirects)
        
       
    if (get_url):
        return x.url
    if (get_cookies):
        return x.cookies.get_dict()
    try:
        return x.json()
    except:
        return x.text
def get_html(url,headers={},params={},cookies={},data={},verify=False,get_cookies=False,get_url=False,allow_redirects=True,use_cache=True):
    if use_cache:
        x=cache.get(c_get_html,12,url,headers,params,cookies,data,verify,get_cookies,get_url,allow_redirects,table='sdr')
    else:
        x=cache.get(c_get_html,0,url,headers,params,cookies,data,verify,get_cookies,get_url,allow_redirects,table='sdr')
        
    return x
def checkip(ips):
    try:
        import urllib.request,ssl
        from urllib.request import Request, urlopen
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE


        
        

        req = Request('https://'+BASE_URL.replace(BASE_URL,ips)+'/series',headers=headers)
        
        content = urlopen(req, context=ctx,timeout=10).read()
        log.warning(content)
        return True
    except:
        return False
def c_check_ip(url):
    
    import urllib.request,ssl
    from urllib.request import Request, urlopen
    
    req = (base64.b64decode('aHR0cHM6Ly9kbnMuZ29vZ2xlLmNvbS9yZXNvbHZlP25hbWU9').decode('utf-8')+url.replace('https://',''))
    with urllib.request.urlopen(req) as response:
       html = response.read()

    
    
    data=json.loads(html)
    all_ips=[]
    log.warning(req)
    log.warning(data)
    for ips in data['Answer']:
        all_ips.append(ips['data'])
    found=False
    if 'www' in url:
        for ips in all_ips:
        
                check=checkip(ips)
                
                if check:
                    found=True
                    break
    else:
        found=True
    if not found:
        #xbmcgui.Dialog().ok("שגיאה",'תקלה בחיבור לסדרות , שנה הגדרות DNS')
        sys.exit(1)
        return ''
    return ips
def get_ip(url):
        
        f_ip=cache.get(c_check_ip,72,url,table='sdr')
        

        
           
            
        return f_ip
        
from urllib3.util import connection

#_orig_create_connection = connection.create_connection
def patched_create_connection(address, *args, **kwargs):
    """Wrap urllib3's create_connection to resolve the name elsewhere"""
    # resolve hostname to an ip address; use your own
    # resolver here, as otherwise the system resolver will be used.
    host, port = address
    hostname = MyResolver(host)

    return _orig_create_connection((hostname, port), *args, **kwargs)


#connection.create_connection = patched_create_connection

def MyResolver(host):
  '''
  import dns.resolver
  
  dns_value='1.1.1.1'
  dns.resolver.default_resolver=dns.resolver.Resolver(configure=True)
  dns.resolver.default_resolver.nameservers=[dns_value]
  
  answer = dns.resolver.query(host)
  log.warning (answer[0].address)
  '''
  if 'sdarot' in host:
    answer=get_ip(host)
  else:
    answer=host
  
 
  
  
    
  return answer#'37.221.65.66'#answer[0].address
  

def logout(cookies={}):


    response = get_html(BASE_URL+'/logout', headers=headers,cookies=cookies,verify=False)


def login(username,password):
    data = {
        'location': '/login',
        'username': username,
        'password': password,
        'submit_login': '',
    }

    cookies = get_html(BASE_URL+'/login', headers=headers, data=data,allow_redirects=False,verify=False,get_cookies=True,use_cache=False)
    return (cookies)


def get_token(sid,season,episode,cookies):
    data = {
        'preWatch': 'true',
        'SID': sid,
        'season': season,
        'ep': episode,
    }

    token = get_html(BASE_URL+'/ajax/watch', cookies=cookies, headers=headers, data=data,verify=False,use_cache=False)
  
    return token
def get_play_link(token,sid,season,episode,cookies):
    Addon = xbmcaddon.Addon()
    data = {
        'vast': 'true',
    }

    response = get_html(BASE_URL+'/ajax/watch', cookies=cookies, headers=headers, data=data,verify=False)

    




    data = {
        'watch': 'false',
        'token': token,
        'serie': sid,
        'season': season,
        'episode': episode,
        'type': 'episode',
    }
    
    response = get_html(BASE_URL+'/ajax/watch', cookies=cookies, headers=headers, data=data,verify=False)
    log.warning(response)
    if 'error' in response:
        dp = xbmcgui.DialogProgress()
        dp.create("לצפייה באיכות HD וללא המתנה ניתן לרכוש מנוי","[COLOR orange][B]לרכישת מנוי להיכנס בדפדפן - https://sdarot.tw/signup[/B][/COLOR]")
        s=0
    
        msg="אנא המתן 30 שניות"
        
        tm=re.findall(r' \d+ ', response['error'])
        try:
            tm=int (tm[0].strip())
        except:
            #xbmcgui.Dialog().ok("שגיאה",response['error'].replace('<br //>','\n').replace('<a href="//status">','').replace('</b>',''))
            sys.exit(1)
            return ''
        if (tm>0):
            for s in range(tm, -1, -1):
                time.sleep(1)
                
                    
                dp.update(int(((tm - s)* 100.0) / (tm+1) ),msg+'\n'+ 'עוד {0} שניות'.format(s)+'\n'+  "[COLOR orange][B]לרכישת מנוי להיכנס בדפדפן - https://sdarot.tw/signup[/B][/COLOR]")
                
                if dp.iscanceled():
                    dp.close()
                    return ""
          
        response = get_html(BASE_URL+'/ajax/watch', cookies=cookies, headers=headers, data=data,verify=False)
            
        response=response
        log.warning(response)
        dp.close()
        if 'error' in response:
            #xbmcgui.Dialog().ok("שגיאה",response['error'].replace('<br //>','\n').replace('<a href="//status">','').replace('</b>',''))
            sys.exit(1)
            return ''
        
        
        dp.close()
    link=response['watch']
    max_settings_q=Addon.getSetting('max_quality')
    if (max_settings_q=='0'):
        max_settings_q=480
    elif (max_settings_q=='0'):
        max_settings_q=720 
    else:
        max_settings_q=1080
    max_q=0
    for items in response['watch']:
        if int(items)>max_q and int(items)<=max_settings_q:
            max_q=int(items)
    max_q=str(max_q)
    
    
    headers['Cookie']='Sdarot='+cookies.get('Sdarot')
    head=url_encode(headers)
    f_link='https:'+link[max_q]+"|"+head
    

        
    
 
    return f_link,head

def get_sdarot_category(cookies={}):

    url=BASE_URL+'/series'
    
    x = get_html(url,headers=headers,cookies=cookies,verify=False)

    regex='<select name="genre.+?>(.+?)</div>'
    m_pre=re.compile(regex,re.DOTALL).findall(x)
   
    regex='<option value="(.+?)" >(.+?)</option>'
    try:
        
        m=re.compile(regex,re.DOTALL).findall(m_pre[0]) 
    except:
      
        log.warning(x)
    ret_data={}
    for cat_id,name in m:
        name=name.replace('\n','').replace('\t','').strip()
        ret_data[name]=cat_id
    return ret_data
def get_cat_data(cat_id,from_year="",to_year="",cookies={},page='1'):


  
    if (page=='0'):
        data = {
            'loadMore': '48',
            'start': str(int(page)*48),
            'genre[]': cat_id,
            'from': from_year,
            'to': to_year,
            'country': '',
            'production': '',
            'order': '',
            'dir': '',
            'filter': 'go',
        }
        x = get_html(BASE_URL+'/series', cookies=cookies, headers=headers, data=data,verify=False)
    else:
        params = {
            'loadMore': '48',
            'start': str(int(page)*48),
            'search[genre][]': cat_id,
            'search[from]': from_year,
            'search[to]': to_year,
            'search[country]': '',
            'search[production]': '',
            'search[order]': '',
            'search[dir]': '',
        }

        x = get_html(BASE_URL+'/ajax/series', params=params, cookies=cookies, headers=headers)
   
    
    #output_json = html_to_json.convert(response)
    #base=output_json['html'][0]['body'][0]['div'][1]['section'][0]['div'][1]['div'][1]['div']
  
    regex='<div class="col-lg-2 col-md-2 col-sm-3 col-xs-6 col-tn-12">.+?</div>'
    all_data_pre=re.compile(regex,re.DOTALL).findall(x)
    all_data={}
    threads=[]
    for item in all_data_pre:
        regex='src="(.+?)".+?alt="(.+?)".+?href="(.+?)".+?<p>.+?</strong>(.+?)</p>.+?<p>.+?</strong>(.+?)</p>.+?<p>.+?</strong>(.+?)</p>.+?<p>(.+?)</p>'
        m=re.compile(regex,re.DOTALL).findall(item)
        
        for img,name,link,year,genre,watch,rating in m:
            img_n=img.split('/')
            f_img=img_n[len(img_n)-1].replace('/','')
            f_save=os.path.join(user_dataDir_img,f_img)
            
            rating=rating.split('(')[1].split(')')[0]
            all_data[name]={}
            sid=re.compile('/watch/(.+?)-').findall(link)[0]
            all_data[name]['sid']=sid
            all_data[name]['img']='https:'+img
            all_data[name]['url']=link
            all_data[name]['genre']=genre
            all_data[name]['watch_count']=watch.replace('\n','').replace('\r','')
            all_data[name]['rating']=rating
            
            if not os.path.exists(f_save):
                threads.append(Thread(download_images, 'https:'+img ))
    #for trd in threads:
    #    trd.start()
    return all_data

def search_all(keyword,cookies={},page='0',get_all=False):

    Addon = xbmcaddon.Addon()
    params = {
        'srl': '1',
    }
    max_per_page=int(Addon.getSetting('num_p'))
    response = get_html(BASE_URL+'/ajax/index', params=params, cookies=cookies, headers=headers,verify=False)
    all_data_pre=[]
    all_data=[]
    start_pos=int(page)*max_per_page
    end_pos=start_pos+max_per_page
    count=0
    for item in response:
         
            if keyword in item['heb'] or keyword.lower() in item['eng'].lower() or get_all:
                #if count>=start_pos and count<end_pos:
                all_data_pre.append((item['heb'],item['eng'],item['id'],IMAGE_BASE+'/series/'+item['poster'],'/watch/'+item['id']))
                #count+=1
    all_data_pre=sorted(all_data_pre, key=lambda x: x[0], reverse=False)
    for name,eng_name,sid,img,link in all_data_pre:
        if count>=start_pos and count<end_pos:
            all_data.append({'name':name,'eng_name':eng_name,'sid':sid,'img':img,'link':link})
        count+=1
    return all_data,len(response)
def check_connection(cookies={}):
    Addon = xbmcaddon.Addon()
    url=BASE_URL+'/usercp'
    log.warning('s1')
    x=get_html(url,headers=headers,cookies=cookies,verify=False,get_url=True,use_cache=False)
    log.warning('ds1')
    if (x==BASE_URL+'/login'):
        cookies=cache.get(login, 0,Addon.getSetting('username'),Addon.getSetting('Password_sdr'),table='sdr')
        
        url=BASE_URL+'/usercp'
        x=get_html(url,headers=headers,cookies=cookies,verify=False,get_url=True,use_cache=False)
        if (x!=BASE_URL+'/login'):
            return True,cookies
        return False,{}
    else:
        return True,cookies
def trakt_tv(cookies={}):
 


    response = get_html(BASE_URL+'/tracking', cookies=cookies, headers=headers,verify=False)
def get_seasons(url,cookies={}):
    all_data={}
    x = get_html(BASE_URL+url, cookies=cookies, headers=headers)
    
    regex='id="season">(.+?)</ul>'
    m=re.compile(regex,re.DOTALL).findall(x)
    for items in m:
        regex='<a class="text-center" href="(.+?)">(.+?)</a>'
        m2=re.compile(regex).findall(items)
        
        for link,season in m2:
            all_data[season]=link
    return all_data
def get_episodes(url,cookies={}):
    all_data=[]
    
    x = get_html(BASE_URL+url, cookies=cookies, headers=headers,verify=False,use_cache=False)
    regex='id="episode">(.+?)</ul>'
    m=re.compile(regex,re.DOTALL).findall(x)

    for items in m:
        
        regex='<li data-episode=.+?class="(.+?)".+?<a class="text-center" href="(.+?)">(.+?)</a>'
        m2=re.compile(regex,re.DOTALL).findall(items)
        
        for watched,link,episode in m2:
            all_data.append({'episode':episode,'link':link,'watched':('watched' in watched)})
    regex='var SID.+?= (.+?);'
    sid=re.compile(regex).findall(x)[0]
    
    return all_data,sid
def mark_as_watched(sid,season,episode,watched,cookies):



    data = {
        'SID': sid,
        'season': season,
        'episode': episode,
        'watched': watched,
    }
    log.warning(data)
    response = get_html(BASE_URL+'/ajax/watch', cookies=cookies, headers=headers, data=data,verify=False)
def get_tracking(cookies):
    all_data=[]
    response = get_html(BASE_URL+'/tracking', cookies=cookies, headers=headers,verify=False)

    regex='<div data-serie="(.+?)" class="row">(.+?)aria-valuemax="100">'
    m=re.compile(regex,re.DOTALL).findall(response)

    threads=[]
    all_img=[]
    for sid,items in m:
        regex='<img class="img-responsive img-rounded" src="(.+?)".+?<h4><a href="(.+?)">(.+?)</a>.+?<h5><a href=".+?">(.+?)</a>.+?<p class="help-block">(.+?)</p>.+?aria-valuenow="(.+?)"'
        m2=re.compile(regex,re.DOTALL).findall(items)
        for img,link,name,eng_name,plot,progress in m2:
            
            img_n=img.split('/')
            f_img=img_n[len(img_n)-1].replace('/','')
            f_save=os.path.join(user_dataDir_img,f_img)
            
            all_data.append({'img':'https:'+img ,
                         'sid':sid,
                         'link':link,
                         'name':name,
                         'eng_name':eng_name,
                         'plot':plot.replace('<strong>','[B]').replace('</strong>','[/B]'),
                         'progress':progress})
            
            
            if not os.path.exists(f_save):
                threads.append(Thread(download_images, 'https:'+img ))
    #thread = Thread(download_images, all_img )
    #thread.start()
    #for trd in threads:
    #    trd.start()
    return all_data
def download_images(url):
    import shutil
    headers = {
        'authority': 'static.sdarot.tw',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79',
    }

    if 1:#for url in all_img:
        img_n=url.split('/')
        f_img=img_n[len(img_n)-1].replace('/','')
       
        f_save=os.path.join(user_dataDir_img,f_img)
        log.warning(url)
        img=b''
        response = requests.get(url, headers=headers,stream=True)
     
        
        for chunk in response.iter_content():
                img+=(chunk)
        with open(f_save, 'wb') as out_file:
            out_file.write(img)
    del response
def new_tv_show(page='1',cookies={}):
    if page=='0':
        page='1'
    params = {
        'tab': 'topnew',
        'page': page,
    }
    threads=[]
    all_data=[]
    x = get_html(BASE_URL+'/ajax/index', params=params, cookies=cookies, headers=headers)
    regex='div class="col(.+?)<span>'
    m=re.compile(regex,re.DOTALL).findall(x)

    for items in m:
        regex='img class="img-rounded img-responsive pointer" src="(.+?)".+?<h4><a href="(.+?)">(.+?)</a>.+?<h5><a href=".+?">(.+?)</a>.+?<p>(.+?)</p>.+?<p>(.+?)</p>.+?<p>(.+?)</p>'
        m2=re.compile(regex,re.DOTALL).findall(items)
   
        for img,link,name,eng_name,plot,plot1,plot2 in m2:
            
            img_n=img.split('/')
            f_img=img_n[len(img_n)-1].replace('/','')
            f_save=os.path.join(user_dataDir_img,f_img)
            plot=plot.replace('\n','').replace('\t','')+'\n'+plot1.replace('\n','').replace('\t','')+'\n'+plot2.replace('\n','').replace('\t','')
            all_data.append({'img':'https:'+img ,
                         'generes':plot1.replace('\n','').replace('\t','').replace("<strong>ז'אנר:</strong>",''),
                         'link':link,
                         'name':name,
                         'eng_name':eng_name,
                         'plot':plot.replace('<strong>','[B]').replace('</strong>','[/B]'),
                         })
            
            
            if not os.path.exists(f_save):
                threads.append(Thread(download_images, 'https:'+img ))
    #thread = Thread(download_images, all_img )
    #thread.start()
    #for trd in threads:
    #    trd.start()
    return all_data
def system_msg():
    x = get_html(BASE_URL,   headers=headers)
    regex='<div class="item">(.+?)</div>'
    m=re.compile(regex,re.DOTALL).findall(x)
    log.warning(m)
    plot=[]
    for items in m:
        regex_date='<span class="date">(.+?)</span>'
        date_m=re.compile(regex_date).findall(items)[0]
        plot.append('\n')
        plot.append('[COLOR lightblue][B]'+date_m+'[/B][/COLOR]')
        regex='<p>(.+?)</p>'
        m3=re.compile(regex,re.DOTALL).findall(items)
        for p_items in m3:
            p_items=p_items.replace('<span style="font-size:18px">','').replace('<span style="font-size:22px">','').replace('<strong>','[B]').replace('</strong>','[/B]').replace('</span>','').replace('<span style="font-size:16px">','').replace('<a href=','[I]').replace('</a>','[/I]').replace('&nbsp;',' ')
            plot.append(p_items)

    return '\n'.join(plot)
#x=get_episodes('https://sdarot.tw/watch/2354-הרעשנים-מדובב-the-loud-house/season/1/episode/5')
'''
cookie=cache.get(login, 0,'penebs','penebs1234',table='login')
print (cookie)
get_tracking(cookie)

cookie=cache.get(login, 24,'penebs','penebs1234',table='login')
print (cookie)
#cookie=login('penebs','penebs1234')
connected=check_connection(cookie)
print (connected)

#cat=get_sdarot_category()
#print (cat)

#result=search_all('sabrina')
#print (result)

#all_data=get_cat_data('7')
#print (json.dumps(all_data))


cookie=login('penebs','penebs1234')
token=get_token('9634','1','11',cookie)

link=get_play_link(token,'9634','1','11',cookie)
print (link)
'''
























