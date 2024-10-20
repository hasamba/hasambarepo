
import xbmcaddon,xbmcplugin,xbmcgui,sys,logging
from urllib.parse import parse_qsl
from urllib.parse import urlencode
import xbmcvfs,urllib,urllib.parse

Addon = xbmcaddon.Addon()
#import urllib.parse
params_pre=""

def routing(argv1,argv2):
    from resources.kids import refresh_list
    
    refresh_list(argv1,argv2)
    