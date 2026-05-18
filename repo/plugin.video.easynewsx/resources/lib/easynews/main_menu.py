# -*- coding: utf-8 -*-
"""Plugin root menu."""
import os

import xbmcgui
import xbmcplugin

from resources.lib.easynews import addon_news
from resources.lib.easynews import context as ctx
from resources.lib.easynews.external_links import GITHUB_REPO_URL
from resources.lib.easynews.listing_restore import _clear_listing_restore
from resources.lib.easynews import members_home
from resources.lib.easynews import search_resolution
from resources.lib.easynews import vlc as vlc_launcher

def main_menu():
    """Build the root menu listing."""
    addon_news.maybe_show_on_main_menu_entry()
    _clear_listing_restore()
    xbmcplugin.setPluginCategory(ctx._handle, 'Main Menu')
    xbmcplugin.setContent(ctx._handle, 'videos')
    is_folder = True
    _panel03 = os.path.join(ctx.addon.getAddonInfo("path"), "resources", "panel-03.jpg")
    _easynews_logo = os.path.join(ctx.addon.getAddonInfo("path"), "resources", "easynews_logo.png")
    _vlc_logo = os.path.join(ctx.addon.getAddonInfo("path"), "resources", "vlc_logo.png")
    # Account row: title + yellow plan/gigs on label when cached (/account_label refreshes).
    li = xbmcgui.ListItem(label=members_home.account_menu_label())
    if os.path.isfile(_easynews_logo):
        li.setArt({"icon": _easynews_logo, "thumb": _easynews_logo})
    li.setInfo(
        "video",
        {
            "plot": members_home.account_menu_plot(),
        },
    )
    li.setProperty("IsPlayable", "false")
    try:
        li.setIsFolder(False)
    except AttributeError:
        pass
    # Primary select: isFolder=False + plugin URL = Kodi's list-item equivalent of RunPlugin
    # (no extra folder on the back stack). Context entry uses explicit RunPlugin as a fallback.
    _acct_plugin = ctx.addon_base + "/account_label"
    li.addContextMenuItems(
        [
            (
                "Refresh EasyNews account",
                'RunPlugin("{}")'.format(_acct_plugin),
            ),
        ],
        replaceItems=False,
    )
    xbmcplugin.addDirectoryItem(ctx._handle, _acct_plugin, li, False)
    li = xbmcgui.ListItem(label=search_resolution.main_menu_resolution_row_label())
    li.setInfo(
        "video",
        {
            "plot": (
                "Default for all text searches (keyboard, TMDB, search history). "
                "Appends 720, 1080, or 2160 to your search terms for the chosen tier. "
                "You can also change this under Add-on settings → General → Search Results."
            ),
        },
    )
    url = ctx._url_base + "/search/resolution"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
    # main search
    li = xbmcgui.ListItem(label="Search EasyNews")
    li.setArt({"icon": _panel03, "thumb": _panel03})
    li.setInfo("video", {
        "plot": "Enter your EasyNews search, it's great, you'll find it no probs!\n"
                "Try searches like:\n"
                "\"john wick 2014\"\n"
                "\"once upon a time in hollywood\"\n"
                "\"the simpsons s03e11\"\n\n"
                "You can also save newsgroups from the context menu of any video search result"
    })
    url = ctx._url_base + "/search"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
    li = xbmcgui.ListItem(label=ctx.addon.getLocalizedString(33032))
    _panel02 = os.path.join(ctx.addon.getAddonInfo("path"), "resources", "panel-02.jpg")
    li.setArt({"icon": _panel02, "thumb": _panel02})
    li.setInfo(
        "video",
        {
            "plot": ctx.addon.getLocalizedString(33036),
        },
    )
    url = ctx._url_base + "/searchhistory"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
    li = xbmcgui.ListItem(label=ctx.addon.getLocalizedString(33037))
    _panel01 = os.path.join(ctx.addon.getAddonInfo("path"), "resources", "panel-01.jpg")
    li.setArt({"icon": _panel01, "thumb": _panel01})
    li.setInfo(
        "video",
        {
            "plot": ctx.addon.getLocalizedString(33039),
        },
    )
    url = ctx._url_base + "/playhistory"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
    # browse groups
    li = xbmcgui.ListItem(label="Browse Saved Newsgroups")
    li.setInfo("video", {
        "plot": "Browse a particular newsgroup, and save your groups for later"})
    url = ctx._url_base + "/browse"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
    # downloads folder (same path as add-on setting general.download_folder)
    li = xbmcgui.ListItem(label="Browse Download Folder")
    li.setInfo(
        "video",
        {
            "plot": "Open the folder where completed downloads are saved.\n\n"
            "Change the location under Add-on settings → Downloads."
        },
    )
    url = ctx._url_base + "/downloads"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
    # browse TMDB
    _tmdb_logo = os.path.join(ctx.addon.getAddonInfo("path"), "resources", "tmdb_logo.png")
    li = xbmcgui.ListItem(label="Find in TMDB (The Movie Database)")
    if os.path.isfile(_tmdb_logo):
        li.setArt({"icon": _tmdb_logo, "thumb": _tmdb_logo})
    li.setInfo(
        "video",
        {
            "plot": ctx.addon.getLocalizedString(33050),
        },
    )
    url = ctx._url_base + "/tmdb"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
    # optional: write Kodi advancedsettings.xml network timeouts (see add-on settings)
    li = xbmcgui.ListItem(label=ctx.addon.getLocalizedString(33027))
    li.setInfo(
        "video",
        {
            "plot": ctx.addon.getLocalizedString(33043)
            + "\n\n"
            + ctx.addon.getLocalizedString(33021),
        },
    )
    url = ctx._url_base + "/tools"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, True)
    # VLC status row: click runs /vlc_info (Container.Refresh only, no stack).
    vlc_ok = vlc_launcher.vlc_is_installed()
    if vlc_ok:
        msg = "VLC found. Search results can be opened in VLC"
        plot = (
            "VLC was detected on this device.\n\n"
            "You can use the context menu on a search result (or play history item) to choose "
            "\"Open in VLC (experimental)\".\n\n"
            "VLC often handles seeking much better than Kodi for problematic Easynews streams."
        )
    else:
        msg = "VLC not found. No VLC features enabled. Default Kodi player only"
        plot = (
            "VLC was not detected on this device.\n\n"
            "Install VLC to enable the experimental \"Open in VLC\" context-menu option.\n\n"
            "Until then, videos will play using Kodi's built-in player only."
        )
    vlc_label = "[COLOR deepskyblue]{}[/COLOR]".format(msg)
    li = xbmcgui.ListItem(label=vlc_label)
    if os.path.isfile(_vlc_logo):
        li.setArt({"icon": _vlc_logo, "thumb": _vlc_logo})
    li.setInfo("video", {"plot": plot})
    li.setProperty("IsPlayable", "false")
    try:
        li.setIsFolder(False)
    except AttributeError:
        pass
    _vlc_plugin = ctx.addon_base + "/vlc_info"
    li.addContextMenuItems(
        [
            (
                "Reload this menu",
                'RunPlugin("{}")'.format(_vlc_plugin),
            ),
        ],
        replaceItems=False,
    )
    xbmcplugin.addDirectoryItem(ctx._handle, _vlc_plugin, li, False)
    li = xbmcgui.ListItem(
        label="[COLOR yellow]Buy Me a Coffee at {}[/COLOR]".format(GITHUB_REPO_URL)
    )
    li.setArt({"icon": _panel03, "thumb": _panel03})
    li.setInfo(
        "video",
        {
            "plot": "Open the GitHub project page in your default web browser. You can Buy Me a Coffee there too!",
        },
    )
    li.setProperty("IsPlayable", "false")
    url = ctx._url_base + "/github"
    xbmcplugin.addDirectoryItem(ctx._handle, url, li, False)
    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)

