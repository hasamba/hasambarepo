# -*- coding: utf-8 -*-
"""Keyboard / search term entry."""
from urllib.parse import urlencode

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.easynews import api
from resources.lib.easynews import context as ctx
from resources.lib.easynews import credentials
from resources.lib.easynews.listing_restore import _save_listing_restore
from resources.lib.easynews.search_ui import show_easynews_results
from resources.lib.easynews import tmdb_ui


def get_url(**kwargs):
    """Create a URL for calling the plugin recursively from keyword arguments."""
    return "{0}?{1}".format(ctx._url, urlencode(kwargs))


def get_user_input(header):
    dialog = xbmcgui.Dialog()
    d = dialog.input(header)
    if not d:
        return ""
    return d.strip()


def get_search_term():
    """Fill this folder with Easynews hits (same invocation)."""
    if not credentials.require_account_dialog():
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        credentials.go_to_plugin_root()
        return
    query = get_user_input("Search Easynews")
    if not query:
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    query = query.replace(" ", "+")
    _save_listing_restore("/search", query, "", 1)
    show_easynews_results(query=query, newsgroup="", page=1)


def get_browse_term():
    newsgroup = get_user_input("Browse Newsgroup")
    if not newsgroup:
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    newsgroup = newsgroup.replace(" ", "+")
    ctx.saved_newsgroups.add(newsgroup)
    xbmc.executebuiltin(
        "Notification(Saved, {} added to saved groups)".format(api.ng_condense(newsgroup))
    )
    _save_listing_restore("/addnewsgroup", "", newsgroup, 1)
    show_easynews_results(query="", newsgroup=newsgroup, page=1)


def get_tmdb_search_term():
    """Run TMDB title search in this folder (same invocation)."""
    if not tmdb_ui._require_tmdb_key():
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    title = get_user_input("Search TMDB")
    if not title:
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    title = title.replace(" ", "+")
    tmdb_ui.tmdb_search(title, "1")


def get_tmdb_tv_search_term():
    """Run TMDB TV title search in this folder (same invocation)."""
    if not tmdb_ui._require_tmdb_key():
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    title = get_user_input("Search TV on TMDB")
    if not title:
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    title = title.replace(" ", "+")
    tmdb_ui.tmdb_search_tv(title, "1")


def get_search_within_newsgroup_term(newsgroup):
    query = get_user_input("Search within {}".format(api.ng_condense(newsgroup)))
    if not query:
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    query = query.replace(" ", "+")
    _save_listing_restore("/searchwithinng", query, newsgroup, 1)
    show_easynews_results(query=query, newsgroup=newsgroup, page=1)
