import json
import os
import re
import sys
import urllib2
import urlparse,logging

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"

try:
    import xbmc

    KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
    KODI = True
except ImportError:
    KODI_VERSION = 17
    KODI = False


def log_error(message):
    if KODI:
        xbmc.log("JKSP[%s]: %s" % (os.path.basename(__file__), message), level=xbmc.LOGERROR)
    else:
        print("JKSP[%s]: %s" % (os.path.basename(__file__), message))

def fetch_url(url, headers={}, direct=False, size=None):
    hdr={
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language': "en-US,en;q=0.5",
        'Referer': url,
        'User-Agent': USER_AGENT
    }
    hdr.update(headers)

    try:
        req = urllib2.Request(url, headers=hdr)
        x= urllib2.urlopen(req).read(size)
        if 'Our systems have detected unusual traffic' in x:
            logging.warning('try by prx')
            x=getby_prx2(url)
            if 'Our systems have detected unusual traffic' in x:
                logging.warning('try by prx2')
                x=getby_prx(url)
        return x
    except urllib2.URLError, e:
        log_error(str(e))
        return False


def resolve_video(url):
    html = fetch_url(url)
    logging.warning('f_url')
    r = re.search(r'<source src="(.+?)" type="video/mp4"', html)
    
    if r:
        return r.group(1)

    else:
        return None
def getby_prx2(video_id):
    import requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'http://www.onlinecodebeautify.com/html-beautifier.php',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    data = {
      'url': video_id
    }

    response = requests.post('http://www.onlinecodebeautify.com/get_data.php', headers=headers, data=data).content
    return response
def getby_prx(video_id):
    import requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://codebeautify.org/source-code-viewer',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://codebeautify.org',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }

    data = {
      'path': video_id
    }

    response = requests.post('https://codebeautify.com/URLService', headers=headers, data=data).content
    return response
def resolve(video_id):
    main_url =  video_id

    main_html = fetch_url(main_url)

    

    if main_html is False:
        log_error("Failed to load main URL")
        return None
    logging.warning('qualities')
    qualities = re.findall(r'source src="(.+?)" type="video/mp4" label="(.+?)"', main_html) #% main_url.replace("?","").replace("=","/"), main_html)
    xbmc.sleep(500)
    videos = {}
    for link,quality in qualities:
        logging.warning(main_url + "&q=" + quality)
        
        #video = resolve_video(main_url + "&q=" + quality)
        
        videos[quality] = link
    if len(qualities)==0:
        regex='<source src="(.+?)"'
        match=re.compile(regex).findall(main_html)
        videos['777']=match[0]
        subs = {}
        return {'videos':videos,
            'subs': subs}
    
    subs = {}
    '''
    s = re.finditer(r'<track src="<(/loadvtt\.php\?f=/srt/.+?)" kind="subtitles" .*label="(.+?)"', main_html)
    for r in re.finditer(r'<track src="(?P<U>/loadvtt\.php\?f=/srt/.+?)" kind="subtitles" .*label="(?P<L>.+?)"', main_html):
        subs[r.group(2)] = "https://www.rapidvideo.com" + r.group(1)
    '''
    return {'videos': videos,
            'subs': subs}


if __name__ == '__main__':
    movie_data = resolve(sys.argv[1])
    if movie_data:
        videos = movie_data['videos']
        for x in videos:
            print videos[x], x

        subs = movie_data['subs']
        for x in subs:
            print subs[x], x

    else:
        print("failed!")