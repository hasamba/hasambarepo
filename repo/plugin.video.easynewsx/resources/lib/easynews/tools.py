# -*- coding: utf-8 -*-
"""Kodi advancedsettings.xml network timeout helpers."""
import json
from urllib.parse import urlencode, urljoin, urlparse

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.kodi.advancedsettings import (
    merge_network_curl_settings,
    remove_network_curl_settings,
)
from resources.lib.easynews import addon_news
from resources.lib.easynews import api
from resources.lib.easynews import context as ctx
from resources.lib.easynews import credentials

_LOG = "plugin.video.easynewsx"

def tools_menu():
    """Folder: user guide, then apply or remove curl timeouts in userdata advancedsettings.xml."""
    xbmcplugin.setPluginCategory(ctx._handle, ctx.addon.getLocalizedString(33027))
    xbmcplugin.setContent(ctx._handle, "videos")
    li = xbmcgui.ListItem(label=ctx.addon.getLocalizedString(33042))
    li.setInfo(
        "video",
        {
            "plot": ctx.addon.getLocalizedString(33043),
        },
    )
    li.setProperty("IsPlayable", "false")
    url = ctx._url_base + "/guide"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, False)
    li = xbmcgui.ListItem(label=ctx.addon.getLocalizedString(33057))
    li.setInfo(
        "video",
        {
            "plot": ctx.addon.getLocalizedString(33058),
        },
    )
    li.setProperty("IsPlayable", "false")
    url = ctx._url_base + "/tools?action=show_news"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, False)
    li = xbmcgui.ListItem(label=ctx.addon.getLocalizedString(33028))
    li.setInfo(
        "video",
        {
            "plot": ctx.addon.getLocalizedString(33029),
        },
    )
    li.setProperty("IsPlayable", "false")
    url = ctx._url_base + "/tools?action=apply"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, False)
    li = xbmcgui.ListItem(label=ctx.addon.getLocalizedString(33030))
    li.setInfo(
        "video",
        {
            "plot": ctx.addon.getLocalizedString(33031),
        },
    )
    li.setProperty("IsPlayable", "false")
    url = ctx._url_base + "/tools?action=remove"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, False)

    li = xbmcgui.ListItem(label="Probe EasyNews route (dlFarm/dlPort/CDN)")
    li.setInfo(
        "video",
        {
            "plot": (
                "Probes Easynews to show the current Download Farm and Download Port. If you are "
                "experiencing timeouts or slow downloads / streams, you can often increase performance "
                "by manually setting your network route in the EasyNews members area."
            ),
        },
    )
    li.setProperty("IsPlayable", "false")
    url = ctx._url_base + "/tools?action=probe_route"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, False)
    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)


def tools_apply_kodi_network_timeouts():
    curl_t = ctx.addon.getSettingInt("tools.kodi_curlclienttimeout")
    low_t = ctx.addon.getSettingInt("tools.kodi_curllowspeedtime")
    if curl_t < 10:
        curl_t = 300
    if low_t < 20:
        low_t = 120
    body = "{}\n\n{}: {} s\n{}: {} s".format(
        ctx.addon.getLocalizedString(33029),
        ctx.addon.getLocalizedString(33024),
        curl_t,
        ctx.addon.getLocalizedString(33026),
        low_t,
    )
    if not xbmcgui.Dialog().yesno(ctx.addon.getLocalizedString(33028), body):
        return
    ok, msg = merge_network_curl_settings(curl_t, low_t)
    if ok:
        xbmcgui.Dialog().ok(ctx.addon.getLocalizedString(33027), msg)
    else:
        xbmcgui.Dialog().ok("EasyNews", msg)


def tools_remove_kodi_network_timeouts():
    if not xbmcgui.Dialog().yesno(
        ctx.addon.getLocalizedString(33030),
        ctx.addon.getLocalizedString(33031),
    ):
        return
    ok, msg = remove_network_curl_settings()
    if ok:
        xbmcgui.Dialog().ok(ctx.addon.getLocalizedString(33027), msg)
    else:
        xbmcgui.Dialog().ok("EasyNews", msg)


def tools_probe_easynews_route():
    """
    Action: probe current Solr-provided dlFarm/dlPort and the real redirect CDN host:port.

    This does NOT change settings; it's only a diagnostics helper.
    """
    if not credentials.require_account_dialog():
        return
    # Minimal Solr2 call (1 result) to read dlFarm/dlPort/downURL and a sample item's sig.
    # Use a stable query that usually yields results for most accounts.
    solr_url = (
        "https://members.easynews.com/2.0/search/solr-search/advanced?"
        + urlencode(
            {
                "gps": "shawshank",
                "sbj": "",
                "ns": "",
                "pno": "1",
                "pby": "1",
                "u": "1",
                "s1": "dtime",
                "s1d": "-",
                "s2": "nrfile",
                "s2d": "-",
                "st": "adv",
                "safeO": "",
            },
            doseq=True,
        )
        + "&fty[]=VIDEO"
    )

    try:
        raw, _cookies, _meta = api.get_https_with_auth(solr_url, timeout=30)
        resp = json.loads(raw or b"{}")
    except Exception as e:
        xbmc.log("{}: tools probe_route solr error: {}".format(_LOG, repr(e)), xbmc.LOGDEBUG)
        xbmcgui.Dialog().notification(
            "EasyNews",
            "Route probe failed (Solr request). See debug log.",
            xbmcgui.NOTIFICATION_ERROR,
            7000,
        )
        return

    dl_farm = (resp.get("dlFarm") or "").strip()
    dl_port = str(resp.get("dlPort") or "").strip()
    down_url = (resp.get("downURL") or "").strip().rstrip("/")
    data = resp.get("data") or []

    cdn_hostport = ""
    sample_members_url = ""
    location_url = ""
    try:
        if isinstance(data, list) and data:
            # Reuse existing parsing to build the correct members /dl URL (route-aware when possible)
            videos = api.parse_easynews_data(
                data,
                dl_farm=dl_farm or None,
                dl_port=dl_port or None,
                down_url=down_url or None,
            )
            if videos:
                sample_members_url = videos[0].get("video") or ""
    except Exception:
        sample_members_url = ""

    if sample_members_url:
        try:
            import requests
            from requests.auth import HTTPBasicAuth

            r = requests.get(
                sample_members_url,
                auth=HTTPBasicAuth(ctx.username, ctx.password),
                cookies=ctx.easynews_chickenlicker_cookies_dict(),
                allow_redirects=False,
                timeout=(10, 15),
                headers={"User-Agent": "{} {}".format(_LOG, getattr(ctx, "addon_version", ""))},
            )
            try:
                status = int(getattr(r, "status_code", 0) or 0)
            except Exception:
                status = 0
            loc = r.headers.get("Location") or r.headers.get("location") or ""
            loc = loc.strip() if isinstance(loc, str) else ""
            if status in (301, 302, 303, 307, 308) and loc:
                location_url = urljoin(sample_members_url, loc)
                cdn_hostport = urlparse(location_url).netloc
            elif status == 200 and loc:
                location_url = urljoin(sample_members_url, loc)
                cdn_hostport = urlparse(location_url).netloc
            elif status == 200:
                # No redirect; not a CDN URL, but keep diagnostics clear.
                cdn_hostport = ""
            else:
                cdn_hostport = ""
            try:
                r.close()
            except Exception:
                pass
        except Exception as e:
            xbmc.log("{}: tools probe_route redirect error: {}".format(_LOG, repr(e)), xbmc.LOGDEBUG)

    body = "EasyNews dlFarm: {}\nEasyNews dlPort: {}\n".format(dl_farm or "?", dl_port or "?")
    if cdn_hostport:
        body += "Redirect CDN: {}\n".format(cdn_hostport)
    else:
        body += "Redirect CDN: (could not resolve)\n"
    body += "You can set your routing in Easynews members area.\n"

    xbmc.log(
        "{}: tools probe_route dlFarm={} dlPort={} cdn={}".format(
            _LOG, dl_farm or "?", dl_port or "?", cdn_hostport or "?"
        ),
        xbmc.LOGDEBUG,
    )
    xbmcgui.Dialog().ok("EasyNews route probe", body)
