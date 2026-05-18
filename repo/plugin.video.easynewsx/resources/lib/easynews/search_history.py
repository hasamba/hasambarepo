# -*- coding: utf-8 -*-
"""Recent search query history (rolling 10)."""
import urllib.parse
from urllib.parse import urlencode

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.easynews import context as ctx


def _refresh_listing():
    folder = (xbmc.getInfoLabel("Container.FolderPath") or "").strip()
    if not folder:
        return
    try:
        ep = (urllib.parse.urlparse(folder).path or "").rstrip("/")
    except Exception:
        return
    if ep != "/searchhistory":
        return
    xbmc.executebuiltin("Container.Refresh")


def search_history_menu(action, query):
    xbmcplugin.setPluginCategory(ctx._handle, ctx.addon.getLocalizedString(33032))
    xbmcplugin.setContent(ctx._handle, "videos")
    is_folder = True

    if action == "remove":
        ctx.search_query_history.remove(query)
        _refresh_listing()
        return
    if action == "clear":
        ctx.search_query_history.clear()
        _refresh_listing()
        return

    history = ctx.search_query_history.get()
    listed = 0
    for k in sorted(list(history), reverse=True):
        q = history[k].get("query")
        if not q:
            continue
        listed += 1
        li = xbmcgui.ListItem(label=q)
        remove_action = ctx.addon_base + "/searchhistory?" + urlencode({"action": "remove", "query": q})
        clear_action = ctx.addon_base + "/searchhistory?" + urlencode({"action": "clear"})
        li.addContextMenuItems(
            [
                (ctx.addon.getLocalizedString(33034), "RunPlugin({})".format(remove_action)),
                (ctx.addon.getLocalizedString(33035), "RunPlugin({})".format(clear_action)),
            ]
        )
        url = ctx._url_base + "/searchresults?" + urlencode({"query": q, "page": "1"})
        xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)

    if listed == 0:
        li = xbmcgui.ListItem(
            label="[COLOR gray]{}[/COLOR]".format(ctx.addon.getLocalizedString(33033))
        )
        li.setInfo("video", {"plot": ctx.addon.getLocalizedString(33036)})
        li.setProperty("IsPlayable", "false")
        # Non-folder row (hint only). URL re-opens this folder so nothing navigates away.
        url = ctx._url_base + "/searchhistory"
        xbmcplugin.addDirectoryItem(ctx._handle, url, li, False)

    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
