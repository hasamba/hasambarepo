# -*- coding: utf-8 -*-
"""Kodi listings for Easynews search results."""
import hashlib
import json
import os
import time
import urllib.parse
from urllib.parse import urlencode

import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs

from resources.lib.easynews import api
from resources.lib.easynews import context as ctx
from resources.lib.easynews import credentials
from resources.lib.easynews import search_resolution
from resources.lib.easynews import vlc as vlc_launcher

_LOG = "plugin.video.easynewsx"

_SEARCH_RESULTS_CACHE_TTL_MIN = 30
_SEARCH_RESULTS_CACHE_MAX_FILES = 60
_SEARCH_RESULTS_CACHE_CLEANUP_INTERVAL_SEC = 10 * 60
_WINDOW_PROP_SEARCH_CACHE_CLEANUP_TS = "plugin.video.easynewsx.search_cache_cleanup_ts"


def _search_cache_key(query: str, newsgroup: str, page: int) -> dict:
    """
    Inputs/settings that influence the returned listing.

    Keep this conservative: if any setting changes results or filtering, include it.
    query must be the full gps string sent to EasyNews (including resolution terms).
    """
    return {
        "v": 4,
        "query": query or "",
        "newsgroup": newsgroup or "",
        "page": int(page) if page else 1,
        "type": "VIDEO",
        "results_per_page": int(getattr(ctx, "results_per_page", 50) or 50),
        "exclude_erotica": bool(getattr(ctx, "exclude_erotica", False)),
        "date_sort_order": int(getattr(ctx, "date_sort_order", 0) or 0),
    }


def _search_cache_filename(key_obj: dict) -> str:
    blob = json.dumps(key_obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hashlib.md5(blob).hexdigest()  # nosec - non-crypto, filename key only
    return "searchresults_{}.json".format(digest)


def _search_cache_get(query: str, newsgroup: str, page: int):
    """Return (video_data, results, page) if available/fresh, else None."""
    try:
        key_obj = _search_cache_key(query, newsgroup, page)
        filename = _search_cache_filename(key_obj)
        raw = ctx.cache.get(filename, age=_SEARCH_RESULTS_CACHE_TTL_MIN)
        if not raw:
            return None
        data = json.loads(raw)
        if not isinstance(data, dict):
            return None
        video_data = data.get("video_data")
        results = data.get("results")
        cached_page = data.get("page")
        if not isinstance(video_data, list):
            return None
        if not isinstance(results, int) or not isinstance(cached_page, int):
            return None
        xbmc.log(
            "{}: searchresults cache hit (ttl={}m) q={!r} ng={!r} p={}".format(
                _LOG, _SEARCH_RESULTS_CACHE_TTL_MIN, query, newsgroup, cached_page
            ),
            xbmc.LOGDEBUG,
        )
        return video_data, results, cached_page
    except Exception as e:
        xbmc.log("{}: searchresults cache read failed: {}".format(_LOG, e), xbmc.LOGDEBUG)
        return None


def _search_cache_prune():
    """Best-effort: keep cache directory from growing without bound."""
    try:
        cache_dir = getattr(ctx.vfs_cache, "path", None)
        if not cache_dir or not xbmcvfs.exists(cache_dir):
            return
        _dirs, files = xbmcvfs.listdir(cache_dir)
        files = [f for f in files if f.startswith("searchresults_") and f.endswith(".json")]
        if len(files) <= _SEARCH_RESULTS_CACHE_MAX_FILES:
            return
        files_with_mtime = []
        for f in files:
            try:
                stat = xbmcvfs.Stat(os.path.join(cache_dir, f))
                files_with_mtime.append((stat.st_mtime(), f))
            except Exception:
                continue
        files_with_mtime.sort(key=lambda t: t[0])
        overflow = len(files_with_mtime) - _SEARCH_RESULTS_CACHE_MAX_FILES
        for _mtime, f in files_with_mtime[:overflow]:
            try:
                xbmcvfs.delete(os.path.join(cache_dir, f))
            except Exception:
                pass
    except Exception:
        pass


def _search_cache_cleanup_expired():
    """
    Best-effort cleanup of expired search cache files.

    Rate-limited via Window(10000) property so "Back to results" doesn't stat/listdir every time.
    """
    try:
        now = int(time.time())
        win = xbmcgui.Window(10000)
        last_raw = win.getProperty(_WINDOW_PROP_SEARCH_CACHE_CLEANUP_TS) or ""
        try:
            last = int(last_raw)
        except (TypeError, ValueError):
            last = 0
        if last and (now - last) < _SEARCH_RESULTS_CACHE_CLEANUP_INTERVAL_SEC:
            return
        win.setProperty(_WINDOW_PROP_SEARCH_CACHE_CLEANUP_TS, str(now))

        cache_dir = getattr(ctx.vfs_cache, "path", None)
        if not cache_dir or not xbmcvfs.exists(cache_dir):
            return
        _dirs, files = xbmcvfs.listdir(cache_dir)
        if not files:
            return
        ttl_sec = int(_SEARCH_RESULTS_CACHE_TTL_MIN) * 60
        for f in files:
            if not (f.startswith("searchresults_") and f.endswith(".json")):
                continue
            try:
                stat = xbmcvfs.Stat(os.path.join(cache_dir, f))
                if (now - int(stat.st_mtime())) > ttl_sec:
                    xbmcvfs.delete(os.path.join(cache_dir, f))
            except Exception:
                continue
    except Exception:
        pass


def _search_cache_put(query: str, newsgroup: str, page: int, video_data, results: int):
    try:
        key_obj = _search_cache_key(query, newsgroup, page)
        filename = _search_cache_filename(key_obj)
        payload = {
            "key": key_obj,
            "saved_at": int(time.time()),
            "video_data": video_data,
            "results": int(results),
            "page": int(page),
        }
        ctx.vfs_cache.save_obj_to_json(filename, payload)
        _search_cache_prune()
    except Exception as e:
        xbmc.log("{}: searchresults cache write failed: {}".format(_LOG, e), xbmc.LOGDEBUG)



def _show_search_fetch_failed(reason, query, newsgroup, page):
    """Finish the directory after a failed API call so Kodi does not hang on the busy spinner."""
    xbmcplugin.setPluginCategory(ctx._handle, "Search Results")
    xbmcplugin.setContent(ctx._handle, "videos")
    parsed = urllib.parse.urlparse(ctx._url)
    base = parsed.scheme + "://" + parsed.netloc
    xbmc.log("{}: search fetch failed: {}".format(_LOG, reason), xbmc.LOGERROR)
    xbmcgui.Dialog().notification("EasyNews", reason, xbmcgui.NOTIFICATION_ERROR, 8000)
    li = xbmcgui.ListItem("[COLOR red]{}[/COLOR]".format(reason))
    li.setProperty("IsPlayable", "false")
    xbmcplugin.addDirectoryItem(ctx._handle, "", li, False)
    retry = xbmcgui.ListItem("[COLOR yellow]Retry this search[/COLOR]")
    retry.setProperty("IsPlayable", "false")
    retry_url = ctx.addon_base + "/searchresults?" + urlencode(
        _searchresults_nav_params(query, newsgroup, page)
    )
    xbmcplugin.addDirectoryItem(ctx._handle, retry_url, retry, True)
    new_search = xbmcgui.ListItem("[COLOR yellow][New Search][/COLOR]")
    new_search.setProperty("IsPlayable", "false")
    xbmcplugin.addDirectoryItem(ctx._handle, base, new_search, True)
    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=True)


def show_easynews_results(query, newsgroup, page, res=None):
    if not credentials.require_account_dialog():
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=True)
        credentials.go_to_plugin_root()
        return
    try:
        page_i = int(page)
    except Exception:
        page_i = 1

    if res is None:
        res = search_resolution.get_search_resolution_setting()
    res = (res or "").strip().lower()
    if res not in ("", "all", "2160", "1080", "720"):
        res = ""

    base_query = query or ""
    query_gps = api.easynews_gps_with_resolution_term(base_query, res)

    # Global search only (same rule as keyboard search): rolling history, page 1 only.
    if page_i == 1 and not (newsgroup or "").strip():
        q_hist = urllib.parse.unquote_plus(base_query.strip())
        if q_hist:
            ctx.search_query_history.add(q_hist)

    _search_cache_cleanup_expired()
    cached = _search_cache_get(query_gps, newsgroup, page_i)
    if cached:
        video_data, results, cached_page = cached
        xbmcplugin.setPluginCategory(ctx._handle, "Search Results")
        xbmcplugin.setContent(ctx._handle, "videos")
        list_videos(
            video_data,
            results,
            cached_page,
            base_query,
            newsgroup,
            res=res,
        )
        return
    try:
        video_data, results, page = api.get_easynews_results(
            query_gps, newsgroup, page_i, "VIDEO", 0
        )
        _search_cache_put(query_gps, newsgroup, int(page), video_data, int(results))
    except api.EasynewsSearchFailed as e:
        _show_search_fetch_failed(e.reason, base_query, newsgroup, page_i)
        return
    xbmcplugin.setPluginCategory(ctx._handle, "Search Results")
    xbmcplugin.setContent(ctx._handle, "videos")
    list_videos(
        video_data,
        results,
        page,
        base_query,
        newsgroup,
        res=res,
    )


def _searchresults_nav_params(base_query, newsgroup, page):
    d = {"query": base_query or "", "page": str(page)}
    if newsgroup:
        d["newsgroup"] = newsgroup
    return d


def list_videos(
    video_data,
    results: int,
    page: int,
    query: str,
    newsgroup: str,
    res="",
):
    """
    Create the list of playable videos in the Kodi interface.

    :param video_data: parsed video search results
    :param results: total number of results from EasyNews
    :param page: which page of search results back from EasyNews
    :param query: base search term for navigation (without auto-appended resolution tokens)
    :param newsgroup: newsgroup to search
    :param res: resolution tier '' / '2160' / '1080' / '720'
    """

    res = (res or "").strip().lower()
    if res not in ("", "all", "2160", "1080", "720"):
        res = ""

    videos = video_data
    try:
        page_i = int(page)
    except (TypeError, ValueError):
        page_i = 1

    parsed = urllib.parse.urlparse(ctx._url)
    base_root = parsed.scheme + "://" + parsed.netloc
    allow_size_line = bool((query or "").replace("+", " ").strip())

    if len(videos) == 0:  # no search results
        li = xbmcgui.ListItem("[COLOR yellow]NO RESULTS, PLEASE TRY AGAIN[/COLOR]")
        url = base_root + "/"
        if query != "" and newsgroup != "":
            li = xbmcgui.ListItem(
                "[COLOR yellow]NO RESULTS, PLEASE TRY SEARCHING {} AGAIN[/COLOR]".format(
                    api.ng_condense(newsgroup)
                )
            )
            url = base_root + "/searchwithinng?newsgroup=" + newsgroup
        if query == "" and newsgroup != "":
            li = xbmcgui.ListItem(
                "[COLOR yellow]NO VIDEOS FOUND IN {}, TRY ANOTHER GROUP[/COLOR]".format(
                    api.ng_condense(newsgroup)
                )
            )
            url = base_root + "/browse"
        xbmcplugin.addDirectoryItem(ctx._handle, url, li, True)
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=True)
    else:
        lastpage = 1 + int(results / ctx.results_per_page)
        results_header = "[B]"
        results_header += f"{results} result{'s' if results > 1 else ''} "
        if lastpage > 1:
            results_header += f"/ Page {page_i} of {lastpage} "
        if res:
            tag = {"2160": "4K", "1080": "1080p", "720": "720p"}.get(res, res)
            results_header += " · [COLOR khaki]{}[/COLOR] ".format(tag)
        results_header += "--- [COLOR yellow][New Search][/COLOR][/B]"
        # results header
        li = xbmcgui.ListItem(results_header)
        li.setProperty("IsPlayable", "false")
        url = base_root
        xbmcplugin.addDirectoryItem(ctx._handle, url, li, True)
        if allow_size_line:
            tip = search_resolution.resolution_display_name(res)
            ch = xbmcgui.ListItem(
                "[COLOR khaki]Video size: {}[/COLOR] — [COLOR yellow]tap to change[/COLOR]".format(tip)
            )
            ch.setInfo(
                "video",
                {
                    "plot": "Tap to change video size for this search.",
                    "mediatype": "video",
                },
            )
            ch.setProperty("IsPlayable", "false")
            xbmcplugin.addDirectoryItem(
                ctx._handle,
                search_resolution.resolution_picker_url(query, newsgroup, page_i),
                ch,
                True,
            )
        # search within ng browse
        if newsgroup != "":
            li = xbmcgui.ListItem("Search within group {}".format(api.ng_condense(newsgroup)))
            li.setProperty("IsPlayable", "false")
            url = base_root + "/searchwithinng?" + "newsgroup=" + newsgroup
            xbmcplugin.addDirectoryItem(ctx._handle, url, li, True)
        # pager nav
        next_page_li = None
        if results > ctx.results_per_page and page_i < lastpage:
            pager = "[COLOR yellow][B]Next Page >>[/B][/COLOR]"
            next_p = page_i + 1
            url = ctx.addon_base + "/searchresults?" + urlencode(
                _searchresults_nav_params(query, newsgroup, next_p)
            )
            xbmc.log("{}: search results next page url: {}".format(_LOG, url), xbmc.LOGDEBUG)
            next_page_li = {"item": xbmcgui.ListItem(pager), "url": url}
            xbmcplugin.addDirectoryItem(ctx._handle, next_page_li["url"], next_page_li["item"], True)
        excluded = 0
        for video in videos:
            if ctx.exclude_erotica and "erotica" in video["newsgroups"]:
                xbmc.log(
                    "{}: excluded erotica result: {}".format(_LOG, str(video)[:800]),
                    xbmc.LOGDEBUG,
                )
                excluded += 1
        if excluded > 0:
            li = xbmcgui.ListItem(
                f"[COLOR blue]{excluded} result{'s' if excluded > 1 else ''} excluded[/COLOR]"
            )
            url = ""
            xbmcplugin.addDirectoryItem(ctx._handle, url, li, False)

        # Expensive environment checks should not run per-item.
        vlc_installed = False
        try:
            vlc_installed = bool(vlc_launcher.vlc_is_installed())
        except Exception:
            vlc_installed = False

        for video in videos:
            filtered = False
            if ctx.exclude_erotica and "erotica" in video["newsgroups"]:
                filtered = True
            if not filtered:
                # Create a list item with a text label and a thumbnail image.
                li = xbmcgui.ListItem(label=video["name"])
                plot = api.video_list_item_plot(video)
                try:
                    vdur = int(video["runtime"])
                except (TypeError, ValueError):
                    vdur = 0
                li.setInfo(
                    "video",
                    {
                        "title": video["name"],
                        "plot": plot,
                        "duration": vdur,
                        "mediatype": "video",
                    },
                )
                li.setArt({"thumb": video["thumb"], "icon": video["thumb"]})
                li.setProperty("IsPlayable", "true")
                # Kodi resume seeks on tokenised EasyNews CDN URLs can fail; disable resume prompt.
                li.setProperty("ResumeTime", "0")
                li.setProperty("TotalTime", "0")

                context_actions = []

                # add a menu context item to download the file to local storage
                dl_url = video["video"]
                download_action = (
                    ctx.addon_base
                    + "/download?"
                    + urlencode({"download_url": dl_url})
                )
                context_actions.append(("Download file", "RunPlugin({})".format(download_action)))

                # Experimental: resolve and hand off expiring CDN URL to VLC
                # Only show the entry when VLC is detected (matches main menu status line).
                # (use urlencode so the tokenised URL survives query parsing)
                if vlc_installed:
                    try:
                        vlc_resolved_url = ctx.addon_base + "/vlc_resolved?" + urlencode(
                            {
                                "video": video["video"],
                                "title": video.get("name") or "",
                                "thumb": video.get("thumb") or "",
                                "plot": plot or "",
                                "runtime": str(vdur),
                                "newsgroups": (video.get("newsgroups") or "").strip(),
                            }
                        )
                        context_actions.append(
                            ("Open in VLC (experimental)", 'RunPlugin("{}")'.format(vlc_resolved_url))
                        )
                    except Exception as e:
                        xbmc.log(
                            "{}: failed to add VLC context menu: {}".format(_LOG, e),
                            xbmc.LOGDEBUG,
                        )

                # if filename is .001 then give context menu item to lookup, dl and join
                newsgroups = video["newsgroups"].split(" ")
                if video["file_ext"] == "001":
                    url = (
                        ctx.addon_base
                        + "/"
                        + f"find_split_files?filename={video['downloadname']}&newsgroup={newsgroups[0]}"
                    )
                    context_actions.append(("Find split files", 'RunPlugin(\"{}\")'.format(url)))

                # add a menu context item of all newsgroups, so any can be added to browse newsgroup menu

                # Cap context items: large cross-post lists can slow directory building on some devices.
                added_ng = 0
                for ng in newsgroups:
                    if not ng:
                        continue
                    if added_ng >= 3:
                        break
                    url = ctx.addon_base + "/browse?" + urlencode({"action": "add", "query": ng})
                    context_actions.append(
                        ("Add {}".format(api.ng_condense(ng)), 'RunPlugin("{}")'.format(url))
                    )
                    added_ng += 1

                li.addContextMenuItems(context_actions)
                play_qs = {
                    "video": video["video"],
                    "title": video["name"],
                    "thumb": video["thumb"],
                    "plot": plot,
                    "runtime": str(vdur),
                }
                ng = (video.get("newsgroups") or "").strip()
                if ng:
                    play_qs["newsgroups"] = ng
                url = parsed.scheme + "://" + parsed.netloc + "/play?" + urlencode(play_qs)
                is_folder = False
                xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
        if next_page_li:
            xbmcplugin.addDirectoryItem(ctx._handle, next_page_li["url"], next_page_li["item"], True)
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=True)

