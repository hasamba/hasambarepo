# -*- coding: utf-8 -*-
"""Preferred Easynews search resolution (main menu + results banner)."""
import urllib.parse
from urllib.parse import urlencode

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.easynews import context as ctx

SETTING_ID = "general.search_resolution"


def get_search_resolution_setting():
    """Return '' (all), or '2160' / '1080' / '720'."""
    try:
        raw = (ctx.addon.getSetting(SETTING_ID) or "").strip().lower()
    except Exception:
        raw = ""
    if raw in ("all", ""):
        return ""
    if raw in ("2160", "1080", "720"):
        return raw
    return ""


def resolution_display_name(res):
    if not res:
        return "All resolutions"
    return {"2160": "4K / 2160p", "1080": "1080p", "720": "720p"}.get(res, res)


def set_search_resolution_setting(value):
    v = (value or "").strip().lower()
    if v in ("all", ""):
        ctx.addon.setSetting(SETTING_ID, "all")
    elif v in ("2160", "1080", "720"):
        ctx.addon.setSetting(SETTING_ID, v)
    else:
        ctx.addon.setSetting(SETTING_ID, "all")


def _has_search_context(query):
    return bool((query or "").replace("+", " ").strip())


def query_display_label(query, max_len=48):
    q = urllib.parse.unquote_plus((query or "").replace("+", " ")).strip()
    if len(q) > max_len:
        return q[: max_len - 3] + "..."
    return q or "search"


def searchresults_plugin_url(query, newsgroup, page="1"):
    d = {"query": query or "", "page": str(page)}
    if newsgroup:
        d["newsgroup"] = newsgroup
    return ctx.addon_base + "/searchresults?" + urlencode(d)


def resolution_picker_url(query="", newsgroup="", page="1"):
    if not _has_search_context(query):
        return ctx._url_base + "/search/resolution"
    return ctx._url_base + "/search/resolution?" + urlencode(
        {
            "query": query or "",
            "newsgroup": newsgroup or "",
            "page": str(page),
        }
    )


def _picker_context_qs(query, newsgroup, page):
    if not _has_search_context(query):
        return {}
    return {
        "query": query or "",
        "newsgroup": newsgroup or "",
        "page": str(page),
    }


def apply_search_resolution_action(value, query="", newsgroup="", page="1"):
    """Persist tier; refresh picker, or re-open search results when opened from a search."""
    set_search_resolution_setting(value)
    res_name = resolution_display_name(get_search_resolution_setting())
    if _has_search_context(query):
        q_label = query_display_label(query)
        try:
            xbmcgui.Dialog().notification(
                "EasyNews",
                ctx.addon.getLocalizedString(33054) % (q_label, res_name),
                xbmcgui.NOTIFICATION_INFO,
                3500,
            )
        except Exception:
            pass
        xbmc.sleep(100)
        xbmc.executebuiltin(
            "Container.Update({})".format(searchresults_plugin_url(query, newsgroup, "1"))
        )
        return
    try:
        xbmcgui.Dialog().notification(
            "EasyNews",
            "Video size: {}".format(res_name),
            xbmcgui.NOTIFICATION_INFO,
            2500,
        )
    except Exception:
        pass
    xbmc.executebuiltin("Container.Refresh")


def search_resolution_menu(query="", newsgroup="", page="1"):
    """Folder: pick default video size (same as Add-on settings → General)."""
    xbmcplugin.setPluginCategory(ctx._handle, "Video size")
    xbmcplugin.setContent(ctx._handle, "videos")
    is_folder = True
    cur = get_search_resolution_setting()
    from_results = _has_search_context(query)

    if from_results:
        li = xbmcgui.ListItem(label=ctx.addon.getLocalizedString(33053))
        li.setProperty("IsPlayable", "false")
        xbmcplugin.addDirectoryItem(
            ctx._handle,
            searchresults_plugin_url(query, newsgroup, page),
            li,
            is_folder,
        )
        again_lbl = ctx.addon.getLocalizedString(33051) % (
            query_display_label(query),
            resolution_display_name(cur),
        )
        li = xbmcgui.ListItem(label="[COLOR yellow][B]{}[/B][/COLOR]".format(again_lbl))
        li.setInfo(
            "video",
            {"plot": ctx.addon.getLocalizedString(33052), "mediatype": "video"},
        )
        li.setProperty("IsPlayable", "false")
        xbmcplugin.addDirectoryItem(
            ctx._handle,
            searchresults_plugin_url(query, newsgroup, "1"),
            li,
            is_folder,
        )
    else:
        li = xbmcgui.ListItem(label="[COLOR yellow]<< Main menu[/COLOR]")
        li.setProperty("IsPlayable", "false")
        xbmcplugin.addDirectoryItem(ctx._handle, ctx.addon_base + "/root", li, is_folder)

    choices = (
        ("all", "All resolutions"),
        ("2160", "4K / 2160p"),
        ("1080", "1080p"),
        ("720", "720p"),
    )
    tip = ctx.addon.getLocalizedString(33055) if from_results else (
        "Used for every text search (keyboard, TMDB, history). "
        "Appends 720, 1080, or 2160 to your search terms for the chosen tier."
    )
    for val, title in choices:
        pick = "" if val == "all" else val
        is_sel = (not pick and not cur) or (pick == cur)
        label = ("[COLOR lime]✓ [/COLOR]" if is_sel else "") + title
        if from_results:
            label += " — [COLOR gray]search again[/COLOR]"
        li = xbmcgui.ListItem(label=label)
        li.setInfo("video", {"plot": tip, "mediatype": "video"})
        li.setProperty("IsPlayable", "false")
        qs = _picker_context_qs(query, newsgroup, page)
        qs["set"] = val
        u = ctx.addon_base + "/search_resolution?" + urlencode(qs)
        xbmcplugin.addDirectoryItem(ctx._handle, u, li, False)

    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)


def main_menu_resolution_row_label():
    """Single-line label for the root menu."""
    cur = get_search_resolution_setting()
    name = resolution_display_name(cur)
    if not cur:
        return "Video size: [COLOR khaki]{}[/COLOR]  [COLOR gray](tap to set)[/COLOR]".format(name)
    return "Video size: [COLOR khaki]{}[/COLOR]  [COLOR gray](tap to change)[/COLOR]".format(name)
