# -*- coding: utf-8 -*-
"""Plugin-wide state set once by init_context() before routing."""

from __future__ import annotations

import http.cookiejar as cookielib
import os
import sys
import urllib.parse

from http.cookiejar import Cookie

import xbmcaddon
import xbmcvfs

from resources.lib.easynews import applog
from resources.lib.easynews.constants import ADDON_VERSION
from resources.lib.kodi.cache import Cache
from resources.lib.kodi.items import Items
from resources.lib.kodi.saved_newsgroups import SavedNewsgroups
from resources.lib.kodi.play_history import PlayHistory
from resources.lib.kodi.search_query_history import SearchQueryHistory
from resources.lib.kodi.settings import Settings
from resources.lib.kodi.vfs import VFS

_url = ""
_handle = 0
parsed = None
_url_base = ""
addon = None
addon_id = ""
addon_base = ""
addon_profile_path = ""
addon_version = ""
username = ""
password = ""
results_per_page = 50
date_sort_order = 0
exclude_erotica = False
vfs = None
vfs_cache = None
settings = None
cache = None
saved_newsgroups = None
search_query_history = None
play_history = None
listItems = None


def init_context():
    """Call once at plugin entry (after sys.path is set)."""
    global _url, _handle, parsed, _url_base, addon, addon_id, addon_base, addon_profile_path
    global username, password, results_per_page, date_sort_order, exclude_erotica, addon_version
    global vfs, vfs_cache, settings, cache, saved_newsgroups, search_query_history, play_history, listItems

    _url = sys.argv[0]
    _handle = int(sys.argv[1])
    parsed = urllib.parse.urlparse(_url)
    _url_base = parsed[0] + "://" + parsed[1]

    addon = xbmcaddon.Addon()
    addon_id = addon.getAddonInfo("id")
    addon_base = "plugin://" + addon_id
    addon_profile_path = xbmcvfs.translatePath(addon.getAddonInfo("profile"))
    addon_version = addon.getAddonInfo("version") or ADDON_VERSION
    username = addon.getSetting("general.username")
    password = addon.getSetting("general.password")

    results_per_page = addon.getSettingInt("general.results_per_page")
    date_sort_order = addon.getSettingInt("general.date_sort_order")
    exclude_erotica = addon.getSettingBool("general.newsgroup_exclusions.erotica")

    vfs = VFS(addon_profile_path)
    vfs_cache = VFS(os.path.join(addon_profile_path, "cache/"))
    applog.schedule_startup_ping(vfs, addon_version)
    settings = Settings(addon)
    cache = Cache(settings, vfs_cache)
    saved_newsgroups = SavedNewsgroups(settings, vfs)
    search_query_history = SearchQueryHistory(vfs)
    play_history = PlayHistory(vfs)
    listItems = Items(addon, addon_base, settings, saved_newsgroups, vfs)


def easynews_chickenlicker_cookie_value():
    """EasyNews chickenlicker cookie value: username and password with ':' as %3A."""
    return "{0}%3A{1}".format(username or "", password or "")


def easynews_chickenlicker_cookie_header():
    """Full ``Cookie`` header field for chickenlicker (urllib ``Request.add_header``)."""
    return "chickenlicker={0}".format(easynews_chickenlicker_cookie_value())


def easynews_chickenlicker_cookies_dict():
    """For ``requests`` ``cookies=`` (search, playback probe, split downloads)."""
    return {"chickenlicker": easynews_chickenlicker_cookie_value()}


def easynews_members_cookie_jar():
    """CookieJar with chickenlicker scoped to members.easynews.com (urllib openers)."""
    jar = cookielib.CookieJar()
    val = easynews_chickenlicker_cookie_value()
    ck = Cookie(
        0,
        "chickenlicker",
        val,
        None,
        False,
        "members.easynews.com",
        True,
        False,
        "/",
        True,
        True,
        None,
        True,
        None,
        None,
        {},
        False,
    )
    jar.set_cookie(ck)
    return jar
