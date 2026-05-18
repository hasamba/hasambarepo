# -*- coding: utf-8 -*-
"""URL router for plugin endpoints."""
import sys
from urllib.parse import parse_qsl, urlparse

import xbmc
import xbmcplugin

from resources.lib.easynews import addon_news
from resources.lib.easynews import browse
from resources.lib.easynews import context as ctx
from resources.lib.easynews import downloads
from resources.lib.easynews import external_links
from resources.lib.easynews import inputs
from resources.lib.easynews import listing_restore
from resources.lib.easynews import main_menu
from resources.lib.easynews import members_home
from resources.lib.easynews import play_history
from resources.lib.easynews import playback
from resources.lib.easynews import search_history
from resources.lib.easynews import search_resolution
from resources.lib.easynews import search_ui
from resources.lib.easynews import split_files
from resources.lib.easynews import tmdb_ui
from resources.lib.easynews import tools
from resources.lib.easynews import userguide
from resources.lib.easynews import vlc as vlc_launcher

_LOG = "plugin.video.easynewsx"


def router(paramstring):
    parsed = urlparse(sys.argv[0])
    endpoint = parsed.path
    xbmc.log("{}: router parsed: {}".format(_LOG, parsed), xbmc.LOGDEBUG)
    xbmc.log("{}: router endpoint: {}".format(_LOG, endpoint), xbmc.LOGDEBUG)

    params = dict(parse_qsl(paramstring, keep_blank_values=True))
    xbmc.log("{}: router params: {}".format(_LOG, params), xbmc.LOGDEBUG)

    query = ""
    if "query" in params:
        query = params["query"].replace(" ", "+")
    filename = ""
    if "filename" in params:
        filename = params["filename"]
    newsgroup = ""
    if "newsgroup" in params:
        newsgroup = params["newsgroup"]
    genre = ""
    if "genre" in params:
        genre = params["genre"]
    title = ""
    if "title" in params:
        title = params["title"]
    page = "1"
    if "page" in params:
        page = params["page"]
    video = None
    if "video" in params:
        video = params["video"]
    action = None
    if "action" in params:
        action = params["action"]

    download_url = None
    if "download_url" in params:
        download_url = params["download_url"]

    if endpoint == "/search/resolution":
        search_resolution.search_resolution_menu(query, newsgroup, page)
    elif endpoint == "/search_resolution":
        search_resolution.apply_search_resolution_action(
            params.get("set") or "all",
            query=params.get("query") or "",
            newsgroup=params.get("newsgroup") or "",
            page=params.get("page") or "1",
        )
    elif endpoint == "/search":
        if not listing_restore._try_restore_listing("/search"):
            inputs.get_search_term()
    elif endpoint == "/searchresults" and (query != "" or newsgroup != ""):
        page = 1
        if "page" in params:
            page = params["page"]
        search_ui.show_easynews_results(query=query, newsgroup=newsgroup, page=page)
    elif endpoint == "/downloads":
        downloads.download_folder_listing(params.get("relpath") or "")
    elif endpoint == "/downloads_delete":
        downloads.download_delete_file(params.get("relpath") or "")
    elif endpoint == "/searchhistory":
        search_history.search_history_menu(action, query)
    elif endpoint == "/playhistory":
        play_history.play_history_menu(action, video)
    elif endpoint == "/browse":
        browse.browse_menu(action, query)
    elif endpoint == "/addnewsgroup":
        if not listing_restore._try_restore_listing("/addnewsgroup"):
            inputs.get_browse_term()
    elif endpoint == "/searchwithinng":
        if not listing_restore._try_restore_listing("/searchwithinng", url_newsgroup=newsgroup):
            inputs.get_search_within_newsgroup_term(newsgroup)
    elif endpoint == "/tmdb/movie/popular":
        tmdb_ui.tmdb_chart("movie", "popular", page)
    elif endpoint == "/tmdb/movie/top_rated":
        tmdb_ui.tmdb_chart("movie", "top_rated", page)
    elif endpoint == "/tmdb/tv/popular":
        tmdb_ui.tmdb_chart("tv", "popular", page)
    elif endpoint == "/tmdb/tv/top_rated":
        tmdb_ui.tmdb_chart("tv", "top_rated", page)
    elif endpoint == "/tmdb/movie":
        tmdb_ui.tmdb_hub_movie()
    elif endpoint == "/tmdb/tv":
        tmdb_ui.tmdb_hub_tv()
    elif endpoint == "/tmdb":
        tmdb_ui.tmdb_menu()
    elif endpoint == "/tmdb/search":
        inputs.get_tmdb_search_term()
    elif endpoint == "/tmdb/search/results":
        tmdb_ui.tmdb_search(title, page)
    elif endpoint == "/tmdb/genres":
        tmdb_ui.tmdb_genres()
    elif endpoint == "/tmdb/discover":
        tmdb_ui.tmdb_discover(genre, page, "movie")
    elif endpoint == "/tmdb/tv/search":
        inputs.get_tmdb_tv_search_term()
    elif endpoint == "/tmdb/tv/search/results":
        tmdb_ui.tmdb_search_tv(title, page)
    elif endpoint == "/tmdb/tv/genres":
        tmdb_ui.tmdb_genres("tv")
    elif endpoint == "/tmdb/tv/discover":
        tmdb_ui.tmdb_discover(genre, page, "tv")
    elif endpoint == "/tmdb/tv/detail":
        tmdb_ui.tmdb_tv_detail(params.get("tv") or "")
    elif endpoint == "/tmdb/tv/season":
        tmdb_ui.tmdb_tv_season(
            params.get("tv") or "",
            params.get("sn") or "1",
            params.get("show") or "",
        )
    elif endpoint == "/play":
        thumb = params.get("thumb") or None
        plot = params.get("plot") or None
        runtime = params.get("runtime")
        newsgroups = params.get("newsgroups") or None
        playback.play_video(
            video,
            title=title or None,
            thumb=thumb,
            plot=plot,
            runtime=runtime,
            newsgroups=newsgroups,
        )
    elif endpoint == "/find_split_files":
        filename = filename.replace(".001", "")
        split_files.find_split_files(filename, newsgroup)
    elif endpoint == "/download":
        downloads.download_file(download_url)
    elif endpoint == "/vlc_resolved":
        # Experimental: resolve CDN redirect URL first, then hand off to VLC.
        if not vlc_launcher.vlc_is_installed():
            import xbmcgui

            xbmcgui.Dialog().notification(
                "EasyNews",
                "VLC not installed (experimental feature).",
                xbmcgui.NOTIFICATION_ERROR,
                6000,
            )
            xbmcplugin.endOfDirectory(ctx._handle, succeeded=False, cacheToDisc=False)
            return
        thumb = params.get("thumb") or None
        plot = params.get("plot") or None
        runtime = params.get("runtime")
        newsgroups = params.get("newsgroups") or None
        vlc_launcher.open_in_vlc(
            video,
            title=title or None,
            thumb=thumb,
            plot=plot,
            runtime=runtime,
            newsgroups=newsgroups,
            resolve_redirect=True,
        )
    elif endpoint == "/guide":
        userguide.show_full_guide()
        xbmcplugin.endOfDirectory(ctx._handle, succeeded=True, cacheToDisc=False)
    elif endpoint == "/github":
        external_links.open_github_repo()
    elif endpoint == "/root":
        main_menu.main_menu()
    elif endpoint == "/account_label":
        # Action only: fetch + cache + Container.Refresh (no main_menu → no extra back-stack).
        members_home.run_account_refresh_action()
    elif endpoint == "/vlc_info":
        xbmc.executebuiltin("Container.Refresh")
    elif endpoint == "/tools":
        if action == "apply":
            tools.tools_apply_kodi_network_timeouts()
        elif action == "remove":
            tools.tools_remove_kodi_network_timeouts()
        elif action == "probe_route":
            tools.tools_probe_easynews_route()
        elif action == "show_news":
            addon_news.show_addon_news_dialog(mark_seen=False)
        else:
            tools.tools_menu()
    else:
        main_menu.main_menu()
