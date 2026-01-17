# -*- coding: utf-8 -*- 
'''
***********************************************************
*
* @file addon.py
* @package script.module.thecrew
*
* Created on 2024-03-08.
* Copyright 2024 by The Crew. All rights reserved.
*
* @license GNU General Public License, version 3 (GPL-3.0)
*
********************************************************cm*
'''

import re
import os
import sys
import json
import html
import base64
import requests
from urllib.parse import urlencode, unquote, parse_qsl, quote_plus, urlparse, urljoin
from datetime import datetime, timezone
import time
import xbmc
import xbmcvfs
import xbmcgui
import xbmcplugin
import xbmcaddon

DADDYLIVE_PROXY_CACHE = {} 

addon_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = dict(parse_qsl(sys.argv[2][1:]))
addon = xbmcaddon.Addon(id='plugin.video.daddylive')
mode = addon.getSetting('mode')

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
FANART = addon.getAddonInfo('fanart')
ICON = addon.getAddonInfo('icon')

SEED_BASEURL = 'https://daddylive.sx/'
EXTRA_M3U8_URL = 'http://drewlive2423.duckdns.org:8081/DrewLive/MergedPlaylist.m3u8'

RAILWAY_PROXY = "https://maneproxy-production.up.railway.app/proxy"
RAILWAY_API_KEY = "SD5NEo2pGgO976Q0B914q3jyQ31DnbMTUQo0NtYL1eWKsRcp8lGmtr9uFJzGOigHfs46rWhZYK4i78tZvZ6Mh9cbNlWHGDSb1Ti6STqLKj0uSrd7kW77xh1FtsGEMKTc9vLxpdNmcn4tByMxzqPZ44OzmiCQgFlOS7YZhqI7QBJbXLX6UntD95k3gaAYykgMRFLaZDGh1jGZgNiQOik486bosYeaKiC5J4KUs3mnHRyCtJignCjkQXiFhppeGqIp"

EXTRA_CHANNELS_DATA = {} 

CACHE_URLS = [
    "index.php",
    "24-7-channels.php"
]

NO_CACHE_URLS = [
    "watch.php",
    "watchs2watch.php"
]

def log(msg):
    logpath = xbmcvfs.translatePath('special://logpath/')
    filename = 'daddylive.log'
    log_file = os.path.join(logpath, filename)
    try:
        if isinstance(msg, str):
            _msg = f'\n    {msg}'
        else:
            _msg = f'\n    {repr(msg)}'
        if not os.path.exists(log_file):
            with open(log_file, 'w', encoding='utf-8'):
                pass
        with open(log_file, 'a', encoding='utf-8') as f:
            line = '[{} {}]: {}'.format(datetime.now().date(), str(datetime.now().time())[:8], _msg)
            f.write(line.rstrip('\r\n') + '\n')
    except Exception as e:
        try:
            xbmc.log(f'[ Daddylive ] Logging Failure: {e}', 2)
        except:
            pass

def should_cache_url(url: str) -> bool:
    """
    Determine if this URL is cacheable.
    Cache:
        - index.php pages (category, schedule, etc.)
        - 24-7-channels.php
    Do NOT cache:
        - watch.php (stream URLs)
    """
    if 'watch.php' in url:
        return False
    if 'index.php' in url or '24-7-channels.php' in url:
        return True
    return False


CACHE_URLS = [
    "index.php",
    "24-7-channels.php"
]

NO_CACHE_URLS = [
    "watch.php",
    "watchs2watch.php"
]

CACHE_EXPIRY = 12 * 60 * 60 

def fetch_via_proxy(url, method='get', data=None, headers=None, use_cache=True):
    headers = headers or {}
    headers['X-API-Key'] = RAILWAY_API_KEY

    should_cache = should_cache_url(url)

    cached = {}
    if should_cache:
        saved = addon.getSetting('proxy_cache')
        if saved:
            try:
                cached = json.loads(saved)
            except Exception as e:
                log(f"[fetch_via_proxy] Failed to load cache: {e}")
                cached = {}

        if url in cached:
            entry = cached[url]
            if isinstance(entry, dict) and 'data' in entry and 'timestamp' in entry:
                timestamp = entry.get('timestamp', 0)
                if time.time() - timestamp < CACHE_EXPIRY:
                    log(f"[fetch_via_proxy] Returning cached data for {url}")
                    return entry.get('data', '')
            else:
                log(f"[fetch_via_proxy] Old cache format found for {url}, refreshing")

    try:
        if method.lower() == 'get':
            resp = requests.get(RAILWAY_PROXY, headers=headers, params={'url': url}, timeout=15)
        else:
            resp = requests.post(RAILWAY_PROXY, headers=headers, data={'url': url}, timeout=15)
        resp_text = resp.text

        if should_cache:
            cached[url] = {
                'timestamp': int(time.time()),
                'data': resp_text
            }
            try:
                addon.setSetting('proxy_cache', json.dumps(cached))
            except Exception as e:
                log(f"[fetch_via_proxy] Failed to save cache: {e}")

        return resp_text

    except Exception as e:
        log(f"[fetch_via_proxy] Proxy fetch failed: {url} error={e}")
        return ''




def normalize_origin(url):
    try:
        u = urlparse(url)
        return f'{u.scheme}://{u.netloc}/'
    except:
        return SEED_BASEURL

def resolve_active_baseurl(seed):
    try:
        _ = fetch_via_proxy(seed, headers={'User-Agent': UA})
        return normalize_origin(seed)
    except Exception as e:
        log(f'Active base resolve failed, using seed. Error: {e}')
        return normalize_origin(seed)

def get_active_base():
    base = addon.getSetting('active_baseurl')
    if not base:
        base = resolve_active_baseurl(SEED_BASEURL)
        addon.setSetting('active_baseurl', base)
    if not base.endswith('/'):
        base += '/'
    return base

def set_active_base(new_base: str):
    if not new_base.endswith('/'):
        new_base += '/'
    addon.setSetting('active_baseurl', new_base)

def abs_url(path: str) -> str:
    return urljoin(get_active_base(), path.lstrip('/'))

def get_local_time(utc_time_str):
    if not utc_time_str:
        return ''
    try:
        utc_now = datetime.utcnow()
        event_time_utc = datetime.strptime(utc_time_str, '%H:%M')
        event_time_utc = event_time_utc.replace(year=utc_now.year, month=utc_now.month, day=utc_now.day)
        event_time_utc = event_time_utc.replace(tzinfo=timezone.utc)
        local_time = event_time_utc.astimezone()
        time_format_pref = addon.getSetting('time_format')
        if time_format_pref == '1':
            return local_time.strftime('%H:%M')
        else:
            return local_time.strftime('%I:%M %p').lstrip('0')
    except Exception as e:
        log(f"Failed to convert time: {e}")
        return utc_time_str or ''


def build_url(query):
    return addon_url + '?' + urlencode(query)

def addDir(title, dir_url, is_folder=True, logo=None):
    li = xbmcgui.ListItem(title)
    clean_plot = re.sub(r'<[^>]+>', '', title)
    labels = {'title': title, 'plot': clean_plot, 'mediatype': 'video'}
    if getKodiversion() < 20:
        li.setInfo("video", labels)
    else:
        infotag = li.getVideoInfoTag()
        infotag.setMediaType(labels.get("mediatype", "video"))
        infotag.setTitle(labels.get("title", "Daddylive"))
        infotag.setPlot(labels.get("plot", labels.get("title", "Daddylive")))

    logo = logo or ICON  
    li.setArt({'thumb': logo, 'poster': logo, 'banner': logo, 'icon': logo, 'fanart': FANART})
    li.setProperty("IsPlayable", 'false' if is_folder else 'true')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=dir_url, listitem=li, isFolder=is_folder)


def closeDir():
    xbmcplugin.endOfDirectory(addon_handle)

def getKodiversion():
    try:
        return int(xbmc.getInfoLabel("System.BuildVersion")[:2])
    except:
        return 18

def Main_Menu():
    menu = [
        ['[B][COLOR gold]LIVE SPORTS SCHEDULE[/COLOR][/B]', 'sched', None],
        ['[B][COLOR gold]LIVE TV CHANNELS[/COLOR][/B]', 'live_tv', None],
        ['[B][COLOR gold]EXTRA CHANNELS / VODS[/COLOR][/B]', 'extra_channels',
         'https://images-ext-1.discordapp.net/external/fUzDq2SD022-veHyDJTHKdYTBzD9371EnrUscXXrf0c/%3Fsize%3D4096/https/cdn.discordapp.com/icons/1373713080206495756/1fe97e658bc7fb0e8b9b6df62259c148.png?format=webp&quality=lossless'],
        ['[B][COLOR gold]SEARCH EVENTS SCHEDULE[/COLOR][/B]', 'search', None],
        ['[B][COLOR gold]SEARCH LIVE TV CHANNELS[/COLOR][/B]', 'search_channels', None],
        ['[B][COLOR gold]REFRESH CATEGORIES[/COLOR][/B]', 'refresh_sched', None],
        ['[B][COLOR gold]SET ACTIVE DOMAIN (AUTO)[/COLOR][/B]', 'resolve_base_now', None],
    ]

    for title, mode_name, logo in menu:
        addDir(title, build_url({'mode': 'menu', 'serv_type': mode_name}), True, logo=logo)

    closeDir()

def getCategTrans():
    schedule_url = abs_url('index.php')
    try:
        html_text = fetch_via_proxy(schedule_url, headers={'User-Agent': UA, 'Referer': get_active_base()})
        log(html_text[:1000])
        m = re.search(r'<div[^>]+class="filters"[^>]*>(.*?)</div>', html_text, re.IGNORECASE | re.DOTALL)
        if not m:
            log("getCategTrans(): filters block not found")
            return []

        block = m.group(1)
        anchors = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', block, re.IGNORECASE | re.DOTALL)
        if not anchors:
            log("getCategTrans(): no <a> items in filters block")
            return []

        categs = []
        seen = set()
        for href, text_content in anchors:
            name = html.unescape(re.sub(r'\s+', ' ', text_content)).strip()
            if not name or name.lower() == 'all':
                continue
            if name in seen:
                continue
            seen.add(name)
            categs.append((name, '[]'))

        return categs
    except Exception as e:
        xbmcgui.Dialog().ok("Error", f"Error fetching category data: {e}")
        log(f'index parse fail: url={schedule_url} err={e}')
        return []

def Menu_Trans():
    categs = getCategTrans()
    if not categs:
        return
    for categ_name, _ in categs:
        addDir(categ_name, build_url({'mode': 'showChannels', 'trType': categ_name}))
    closeDir()

def ShowChannels(categ, channels_list):
    for item in channels_list:
        title = item.get('title')
        addDir(title, build_url({'mode': 'trList', 'trType': categ, 'channels': json.dumps(item.get('channels'))}), True)
    closeDir()

def getTransData(categ):
    try:
        url = abs_url('index.php?cat=' + quote_plus(categ))
        html_text = fetch_via_proxy(url, headers={'User-Agent': UA, 'Referer': get_active_base()})
        cut = re.search(r'<h2\s+class="collapsible-header\b', html_text, re.IGNORECASE)
        if cut:
            html_text = html_text[:cut.start()]

        events = re.findall(
            r'<div\s+class="schedule__event">.*?'
            r'<div\s+class="schedule__eventHeader"[^>]*?>\s*'
            r'(?:<[^>]+>)*?'
            r'<span\s+class="schedule__time"[^>]*data-time="([^"]+)"[^>]*>.*?</span>\s*'
            r'<span\s+class="schedule__eventTitle">\s*([^<]+)\s*</span>.*?'
            r'</div>\s*'
            r'<div\s+class="schedule__channels">(.*?)</div>',
            html_text, re.IGNORECASE | re.DOTALL
        )

        trns = []
        for time_str, event_title, channels_block in events:
            event_time_local = get_local_time(time_str.strip())
            title = f'[COLOR gold]{event_time_local}[/COLOR] {html.unescape(event_title.strip())}'

            chans = []
            for href, title_attr, link_text in re.findall(
                r'<a[^>]+href="([^"]+)"[^>]*title="([^"]*)"[^>]*>(.*?)</a>',
                channels_block, re.IGNORECASE | re.DOTALL
            ):
                try:
                    u = urlparse(href)
                    qs = dict(parse_qsl(u.query))
                    cid = qs.get('id') or ''
                except Exception:
                    cid = ''
                name = html.unescape((title_attr or link_text).strip())
                if cid:
                    chans.append({'channel_name': name, 'channel_id': cid})

            if chans:
                trns.append({'title': title, 'channels': chans})

        return trns
    except Exception as e:
        log(f'getTransData error for categ={categ}: {e}')
        return []

def TransList(categ, channels):
    for channel in channels:
        channel_title = html.unescape(channel.get('channel_name'))
        channel_id = str(channel.get('channel_id', '')).strip()
        if not channel_id:
            continue
        addDir(channel_title, build_url({'mode': 'trLinks', 'trData': json.dumps({'channels': [{'channel_name': channel_title, 'channel_id': channel_id}]})}), False)
    closeDir()

def getSource(trData):
    try:
        data = json.loads(unquote(trData))
        channels_data = data.get('channels')
        if channels_data and isinstance(channels_data, list):
            cid = str(channels_data[0].get('channel_id', '')).strip()
            if not cid:
                return
            if '%7C' in cid or '|' in cid:
                url_stream = abs_url('watchs2watch.php?id=' + cid)
            else:
                url_stream = abs_url('watch.php?id=' + cid)
            xbmcplugin.setContent(addon_handle, 'videos')
            PlayStream(url_stream)
    except Exception as e:
        log(f'getSource failed: {e}')

def list_gen():
    chData = channels()
    for c in chData:
        addDir(c[1], build_url({'mode': 'play', 'url': abs_url(c[0])}), False)
    closeDir()

def channels():
    url = abs_url('24-7-channels.php')
    headers = {'Referer': get_active_base(), 'User-Agent': UA}

    try:
        resp = fetch_via_proxy(url, headers=headers)
    except Exception as e:
        log(f"[DADDYLIVE] channels(): request failed: {e}")
        return []

    card_rx = re.compile(
        r'<a\s+class="card"[^>]*?href="(?P<href>[^"]+)"[^>]*?data-title="(?P<data_title>[^"]*)"[^>]*>'
        r'.*?<div\s+class="card__title">\s*(?P<title>.*?)\s*</div>'
        r'.*?ID:\s*(?P<id>\d+)\s*</div>'
        r'.*?</a>',
        re.IGNORECASE | re.DOTALL
    )

    items = []
    for m in card_rx.finditer(resp):
        href_rel = m.group('href').strip()
        title_dom = html.unescape(m.group('title').strip())
        title_attr = html.unescape(m.group('data_title').strip())
        name = title_dom or title_attr

        is_adult = (
            '18+' in name.upper() or
            'XXX' in name.upper() or
            name.strip().startswith('18+')
        )

        if is_adult:
            continue

        name = re.sub(r'^\s*\d+(?=[A-Za-z])', '', name).strip()
        items.append([href_rel, name])

    return items

def show_adult():
    """Return True if adult content is enabled in settings"""
    return addon.getSettingBool('show_adult')

def PlayStream(link):
    try:
        log(f'[PlayStream] Starting: {link}')

        # Extract channel number
        channel_match = re.search(r'(\d{3})', link)
        if not channel_match:
            resp = fetch_via_proxy(link, headers={'User-Agent': UA})
            channel_match = re.search(r'(\d{3})', resp)

        if not channel_match:
            log('[PlayStream] No channel number found')
            return

        channel_id = channel_match.group(1)
        log(f'[PlayStream] Using channel: {channel_id}')

        target_m3u8 = f'https://chevy.giokko.ru/tv/premium{channel_id}/5893{channel_id}.m3u8'
        encoded_target = quote_plus(target_m3u8)
        proxy_url = f'http://drewlive2423.duckdns.org:4123?url={encoded_target}&channel={channel_id}'

        log(f'[PlayStream] Proxy URL: {proxy_url}')

        liz = xbmcgui.ListItem(f'Channel {channel_id}', path=proxy_url)
        liz.setProperty('inputstream', 'inputstream.adaptive')
        liz.setProperty('inputstream.adaptive.manifest_type', 'hls')
        liz.setMimeType('application/x-mpegURL')
        liz.setProperty('IsPlayable', 'true')

        xbmcplugin.setResolvedUrl(addon_handle, True, liz)
        log('[PlayStream] Stream started')

    except Exception as e:
        log(f'[PlayStream] Error: {e}')

def Search_Events():
    keyboard = xbmcgui.Dialog().input("Enter search term", type=xbmcgui.INPUT_ALPHANUM)
    if not keyboard or keyboard.strip() == '':
        return
    term = keyboard.lower().strip()

    try:
        html_text = fetch_via_proxy(abs_url('index.php'), headers={'User-Agent': UA, 'Referer': get_active_base()})
        events = re.findall(
            r"<div\s+class=\"schedule__event\">.*?"
            r"<div\s+class=\"schedule__eventHeader\"[^>]*?>\s*"
            r"(?:<[^>]+>)*?"
            r"<span\s+class=\"schedule__time\"[^>]*data-time=\"([^\"]+)\"[^>]*>.*?</span>\s*"
            r"<span\s+class=\"schedule__eventTitle\">\s*([^<]+)\s*</span>.*?"
            r"</div>\s*"
            r"<div\s+class=\"schedule__channels\">(.*?)</div>",
            html_text, re.IGNORECASE | re.DOTALL
        )

        rows = {}
        seen = set()
        for time_str, raw_title, channels_block in events:
            title_clean = html.unescape(raw_title.strip())
            if term not in title_clean.lower():
                continue
            if title_clean in seen:
                continue
            seen.add(title_clean)
            event_time_local = get_local_time(time_str.strip())
            rows[title_clean] = channels_block

        for title, chblock in rows.items():
            links = []
            for href, title_attr, link_text in re.findall(
                r'<a[^>]+href="([^"]+)"[^>]*title="([^"]*)".*?>(.*?)</a>', 
                chblock, re.IGNORECASE | re.DOTALL
            ):
                name = html.unescape(title_attr or link_text)
                links.append({'channel_name': name, 'channel_id': href})
            addDir(title, build_url({'mode': 'trLinks', 'trData': json.dumps({'channels': links})}), False)

        closeDir()
    except Exception as e:
        log(f'Search_Events error: {e}')

def Search_Channels():
    keyboard = xbmcgui.Dialog().input("Enter channel name", type=xbmcgui.INPUT_ALPHANUM)
    if not keyboard or keyboard.strip() == '':
        return
    term = keyboard.lower().strip()
    chData = channels()
    for href, title in chData:
        if term in title.lower():
            addDir(title, build_url({'mode': 'play', 'url': abs_url(href)}), False)
    closeDir()

def load_extra_channels(force_reload=False):
    global EXTRA_CHANNELS_DATA
    CACHE_EXPIRY = 24 * 60 * 60

    saved = addon.getSetting('extra_channels_cache')
    if saved and not force_reload:
        try:
            saved_data = json.loads(saved)
            if time.time() - saved_data.get('timestamp', 0) < CACHE_EXPIRY:
                EXTRA_CHANNELS_DATA = saved_data.get('channels', {})
                if EXTRA_CHANNELS_DATA:
                    return EXTRA_CHANNELS_DATA
        except:
            pass

    try:
        resp = requests.get(EXTRA_M3U8_URL, headers={'User-Agent': UA}, timeout=10).text
    except Exception as e:
        xbmcgui.Dialog().ok("Error", f"Failed to fetch extra channels: {e}")
        return {}

    categories = {}
    lines = resp.splitlines()

    for i, line in enumerate(lines):
        if not line.startswith('#EXTINF:'):
            continue

        title_match = re.search(r',(.+)$', line)
        cat_match = re.search(r'group-title="([^"]+)"', line)
        logo_match = re.search(r'tvg-logo="([^"]+)"', line)

        if not title_match:
            continue

        title = title_match.group(1).strip()
        category = cat_match.group(1).strip() if cat_match else 'Uncategorized'
        logo = logo_match.group(1) if logo_match else ICON

        is_adult = (
            '18+' in category.upper() or
            'XXX' in category.upper() or
            '18+' in title.upper() or
            'XXX' in title.upper()
        )

        if is_adult:
            continue

        stream_url = lines[i + 1].strip() if i + 1 < len(lines) else ''
        if not stream_url:
            continue

        categories.setdefault(category, []).append({
            'title': title,
            'url': stream_url,
            'logo': logo
        })

    EXTRA_CHANNELS_DATA = categories

    addon.setSetting(
        'extra_channels_cache',
        json.dumps({'timestamp': int(time.time()), 'channels': EXTRA_CHANNELS_DATA})
    )

    return EXTRA_CHANNELS_DATA

def ExtraChannels_Main():
    global EXTRA_CHANNELS_DATA
    if not EXTRA_CHANNELS_DATA:
        load_extra_channels() 
        if not EXTRA_CHANNELS_DATA:
            xbmcgui.Dialog().ok("Error", "Extra channels could not be loaded.")
            return

    addDir('[B][COLOR gold]Search Extra Channels / VODs[/COLOR][/B]',
           build_url({'mode': 'extra_search'}), True)

    for cat in sorted(EXTRA_CHANNELS_DATA.keys()):
        is_adult_cat = (
            '18+' in cat.upper() or
            'XXX' in cat.upper()
        )

        if is_adult_cat:
            continue
    
        addDir(cat, build_url({'mode': 'extra_list', 'category': cat}), True, logo="https://images-ext-1.discordapp.net/external/fUzDq2SD022-veHyDJTHKdYTBzD9371EnrUscXXrf0c/%3Fsize%3D4096/https/cdn.discordapp.com/icons/1373713080206495756/1fe97e658bc7fb0e8b9b6df62259c148.png?format=webp&quality=lossless")

    
    closeDir()



def ExtraChannels_Search():
    """
    Open a dialog to search for a channel or VOD in the extra list.
    """
    keyboard = xbmcgui.Dialog().input("Search Extra Channels / VODs", type=xbmcgui.INPUT_ALPHANUM)
    if not keyboard or keyboard.strip() == '':
        return
    search_term = keyboard.strip()
    ExtraChannels_List(None, search_term) 


def ExtraChannels_List(category=None, search=None):
    """
    List ExtraChannels, optionally filtering by category or search term,
    enforcing adult access where needed.
    """
    global EXTRA_CHANNELS_DATA
    if not EXTRA_CHANNELS_DATA:
        load_extra_channels()  
        if not EXTRA_CHANNELS_DATA:
            xbmcgui.Dialog().ok("Error", "Extra channels could not be loaded.")
            return

    items_to_show = []

    for cat, streams in EXTRA_CHANNELS_DATA.items():
        if category and cat != category:
            continue

        is_adult_cat = (
            '18+' in cat.upper() or
            'XXX' in cat.upper()
        )
        if is_adult_cat:
            continue

        for item in streams:
            if category and cat != category:
                continue
            if search and search.lower() not in item['title'].lower():
                continue

            is_adult = (
                '18+' in item['title'].upper() or
                'XXX' in item['title'].upper()
            )
            if is_adult:
                continue

            items_to_show.append({
                'title': item['title'],
                'url': item['url'],
                'logo': item.get('logo', ICON)
            })

    for item in items_to_show:
        addDir(
            item['title'],
            build_url({'mode': 'extra_play', 'url': item['url'], 'logo': item.get('logo', ICON), 'name': item['title']}),
            False,
            logo=item.get('logo', ICON)
        )

    closeDir()


def ExtraChannels_Play(url, name='Extra Channel', logo=ICON):
    """
    Play a channel or VOD from ExtraChannels, enforcing adult access.
    """
    try:

        log(f'[ExtraChannels_Play] Original URL: {url}')

        if 'a1xmedia' in url.lower() or 'a1xs.vip' in url.lower():
            headers = {
                'User-Agent': UA,
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://a1xs.vip/'
            }
            try:
                response = requests.head(url, headers=headers, allow_redirects=True, timeout=10)
                url = response.url
                log(f'[ExtraChannels_Play] Resolved A1XMedia URL: {url}')
            except Exception as e:
                log(f'[ExtraChannels_Play] Failed to resolve A1XMedia URL, using original: {e}')

        elif 'daddylive' in url.lower():
            channel_match = re.search(r'(\d{3})', url)
            if channel_match:
                channel_id = channel_match.group(1)
                target_m3u8 = f'https://chevy.giokko.ru/tv/premium{channel_id}/5893{channel_id}.m3u8'
                encoded_target = quote_plus(target_m3u8)
                url = f'http://drewlive2423.duckdns.org:4123?url={encoded_target}&channel={channel_id}'
                log(f'[ExtraChannels_Play] Constructed Daddylive URL: {url}')

        logo = logo or ICON
        liz = xbmcgui.ListItem(name, path=url)
        liz.setArt({'thumb': logo, 'icon': logo, 'fanart': FANART})
        liz.setInfo('video', {'title': name, 'plot': name})

        if '.m3u8' in url.lower():
            liz.setProperty('inputstream', 'inputstream.adaptive')
            liz.setProperty('inputstream.adaptive.manifest_type', 'hls')
            liz.setMimeType('application/vnd.apple.mpegurl')
            log('[ExtraChannels_Play] HLS stream detected')
        elif url.lower().endswith('.mp4'):
            liz.setMimeType('video/mp4')
            log('[ExtraChannels_Play] MP4 stream detected')
        else:
            liz.setMimeType('video')
            log('[ExtraChannels_Play] Generic video stream')

        liz.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(addon_handle, True, liz)
        log(f'[ExtraChannels_Play] Stream started for: {name}')

    except Exception as e:
        log(f'[ExtraChannels_Play] Error: {e}')
        import traceback
        log(f'Traceback: {traceback.format_exc()}')
        xbmcgui.Dialog().notification("Daddylive", "Failed to play channel", ICON, 3000)

def refresh_active_base():
    new_base = resolve_active_baseurl(SEED_BASEURL)
    set_active_base(new_base)
    xbmcgui.Dialog().ok("Daddylive", f"Active base set to:\n{new_base}")
    xbmc.executebuiltin('Container.Refresh')


if not params.get('mode'): 
    load_extra_channels()
    Main_Menu()
else:
    mode = params.get('mode')

    if mode == 'menu':
        servType = params.get('serv_type')
        if servType == 'sched':
            Menu_Trans()
        elif servType == 'live_tv':
            list_gen()
        elif servType == 'extra_channels':
            ExtraChannels_Main()
        elif servType == 'search':
            Search_Events()
        elif servType == 'search_channels':
            Search_Channels()
        elif servType == 'refresh_sched':
            xbmc.executebuiltin('Container.Refresh')

    elif mode == 'showChannels':
        transType = params.get('trType')
        channels_list = getTransData(transType)
        ShowChannels(transType, channels_list)

    elif mode == 'trList':
        transType = params.get('trType')
        channels_list = json.loads(params.get('channels'))
        TransList(transType, channels_list)

    elif mode == 'trLinks':
        trData = params.get('trData')
        getSource(trData)

    elif mode == 'play':
        link = params.get('url')
        PlayStream(link)

    elif mode == 'resolve_base_now':
        refresh_active_base()

    elif mode == 'extra_channels':
        ExtraChannels_Main()

    elif mode == 'extra_search':
        ExtraChannels_Search()

    elif mode == 'extra_list':  
        cat = params.get('category')
        search_term = params.get('search')
        ExtraChannels_List(cat, search_term)

    elif mode == 'extra_play':
        url = params.get('url')
        logo = params.get('logo', ICON)
        name = params.get('name', 'Extra Channel')
        ExtraChannels_Play(url, name=name, logo=logo)

