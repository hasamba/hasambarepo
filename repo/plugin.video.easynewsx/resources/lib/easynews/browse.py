# -*- coding: utf-8 -*-
"""Saved newsgroups browser."""
import urllib.parse
from urllib.parse import urlencode

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.easynews import api
from resources.lib.easynews import context as ctx

_LOG = "plugin.video.easynewsx"


def _refresh_listing_after_history_change():
    """
    After RunPlugin add/remove/clear on saved groups, refresh only when the visible
    listing is Browse Saved Newsgroups (/browse). Container.Refresh re-invokes the
    plugin URL of the folder on screen; paths like /search run get_search_term()
    again and would show the keyboard. Allowlisting /browse matches how Kodi
    add-ons usually treat RunPlugin: side effects plus a targeted refresh, not a
    global Container.Refresh on whatever view happens to be underneath.
    """
    folder = (xbmc.getInfoLabel("Container.FolderPath") or "").strip()
    if not folder:
        return
    try:
        ep = (urllib.parse.urlparse(folder).path or "").rstrip("/")
    except Exception:
        return
    if ep != "/browse":
        return
    xbmc.executebuiltin("Container.Refresh")


def browse_menu(action, newsgroup):
    xbmcplugin.setPluginCategory(ctx._handle, 'Browse Newsgroups')
    xbmcplugin.setContent(ctx._handle, 'videos')
    is_folder = True
    # RunPlugin add/remove/clear: return immediately (don't list menu; first item would open add dialog).
    if action == "remove":  # remove a saved newsgroup
        xbmc.log(
            "{}: browse remove action={} newsgroup={}".format(_LOG, action, newsgroup),
            xbmc.LOGDEBUG,
        )
        ctx.saved_newsgroups.remove(newsgroup)
        _refresh_listing_after_history_change()
        return
    if action == "clear":
        ctx.saved_newsgroups.clear()
        _refresh_listing_after_history_change()
        return
    if action == "add":
        ctx.saved_newsgroups.add(newsgroup)
        xbmc.executebuiltin(
            "Notification(Saved, {} added to saved groups)".format(api.ng_condense(newsgroup))
        )
        _refresh_listing_after_history_change()
        return
    # add a newsgroup
    li = xbmcgui.ListItem(label="[COLOR yellow]Add a Newsgroup[/COLOR]")
    li.setInfo("video", {
        "plot": "Enter a full or partial newsgroup to browse. The newsgroup will be saved here for next time.\n\n" +
                "You can also add newsgroups from the context menu of any video search result"})
    url = ctx._url_base + "/addnewsgroup"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
    history = ctx.saved_newsgroups.get()
    for k in sorted(list(history), reverse=True):
        newsgroup = history[k].get("newsgroup")
        if not newsgroup:
            continue
        li = xbmcgui.ListItem(label=newsgroup)
        remove_action = ctx.addon_base + "/browse?" + urlencode({"action": "remove", "query": newsgroup})
        clear_action = ctx.addon_base + "/browse?" + urlencode({"action": "clear"})
        li.addContextMenuItems([
            ("Remove", "RunPlugin({})".format(remove_action)),
            ("Clear all", "RunPlugin({})".format(clear_action)),
        ])
        url = ctx._url_base + "/searchresults?" + "query=&" + "newsgroup=" + newsgroup
        xbmc.log("{}: browse listing url: {}".format(_LOG, url), xbmc.LOGDEBUG)
        xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
        # list_item = xbmcgui.ListItem(label=query)
        # list_item.addContextMenuItems(self._search_context_menu(query))
        # url = self.ctx.addon_base + PATH_SEARCH + "?" + urllib.parse.urlencode({
        #     "query": history[k].get("query")
        # })
        # items.append((url, list_item, True))
    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
