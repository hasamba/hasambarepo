# -*- coding: utf-8 -*-
"""TMDB discovery and search listings (movies + TV drill-down)."""
import os
from urllib.parse import quote, quote_plus, urlencode

import requests
import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.easynews import api
from resources.lib.easynews import context as ctx
from resources.lib.easynews.constants import TMDB_V3_API_KEY

_tmdb_json_headers = {"accept": "application/json"}
_LOG = "plugin.video.easynewsx"


def _tmdb_brand_art():
    """Bundled TMDB mark for list art; source noted in strings #33050."""
    try:
        p = os.path.join(ctx.addon.getAddonInfo("path"), "resources", "tmdb_logo.png")
        if os.path.isfile(p):
            return {"icon": p, "thumb": p}
    except Exception:
        pass
    return {}


def get_tmdb_api_key():
    k = (TMDB_V3_API_KEY or "").strip()
    if k:
        return k
    return (ctx.addon.getSetting("general.tmdb_api_key") or "").strip()


def _require_tmdb_key():
    k = get_tmdb_api_key()
    if k:
        return k
    xbmcgui.Dialog().ok(
        "TMDB",
        "TMDB discovery is unavailable (no API key in this build).\n"
        "Install the latest add-on update, or report on GitHub.",
    )
    return ""


def _tmdb_http_ok(response):
    if response.status_code == 200:
        return True
    xbmcgui.Dialog().ok(
        "TMDB",
        "The Movie Database request failed (HTTP {}). "
        "Try again later or report on GitHub.".format(response.status_code),
    )
    return False


def _poster_url(path):
    if not path:
        return ""
    return "https://image.tmdb.org/t/p/w500/" + path


def _searchresults_url(strip_query: str):
    return ctx._url_base + "/searchresults?query=" + quote_plus(strip_query.strip())


def _year_from_air_or_release(row, *, tv=False):
    key = "first_air_date" if tv else "release_date"
    d = row.get(key) or ""
    return d[:4] if len(d) >= 4 else ""


def _render_tmdb_result_rows(results, media):
    """Append list items for one page of TMDB movie or TV results (discover / charts)."""
    is_folder = True
    for row in results:
        if media == "tv":
            name = row.get("name") or row.get("original_name") or "TV"
            yr = _year_from_air_or_release(row, tv=True)
            label = "{} ({})".format(name, yr) if yr else name
            plot = row.get("overview") or ""
            plot += "\n\nVote average: {}\nVote count: {}\nPopularity: {}".format(
                row.get("vote_average"),
                row.get("vote_count"),
                row.get("popularity"),
            )
            li = xbmcgui.ListItem(label=label)
            pu = _poster_url(row.get("poster_path"))
            if pu:
                li.setArt({"thumb": pu, "icon": pu})
            li.setInfo("video", {"title": name, "plot": plot, "mediatype": "video"})
            tid = row.get("id")
            if tid:
                nurl = ctx._url_base + "/tmdb/tv/detail?" + urlencode({"tv": str(tid)})
                xbmcplugin.addDirectoryItem(ctx._handle, nurl, li, is_folder)
        else:
            movie = row
            mt = movie.get("title") or "Movie"
            rd = (movie.get("release_date") or "")[:4]
            li = xbmcgui.ListItem(label=mt + (" ({})".format(rd) if rd else ""))
            pu = _poster_url(movie.get("poster_path"))
            if pu:
                li.setArt({"thumb": pu, "icon": pu})
            overview = (movie.get("overview") or "") + "\n\n"
            overview += "Vote average: {}\nVote count: {}\nPopularity: {}".format(
                movie.get("vote_average"),
                movie.get("vote_count"),
                movie.get("popularity"),
            )
            li.setInfo(
                "video",
                {"title": mt, "plot": overview, "mediatype": "video"},
            )
            surl = _searchresults_url(api.easynews_search_strip((mt + " " + rd).strip()))
            xbmcplugin.addDirectoryItem(ctx._handle, surl, li, is_folder)


def tmdb_menu():
    if not _require_tmdb_key():
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    xbmcplugin.setPluginCategory(ctx._handle, "TMDB")
    xbmcplugin.setContent(ctx._handle, "videos")
    is_folder = True
    li = xbmcgui.ListItem(label="[COLOR yellow]<< Back to main menu[/COLOR]")
    xbmcplugin.addDirectoryItem(ctx._handle, ctx._url_base, li, is_folder)

    _ba = _tmdb_brand_art()
    li = xbmcgui.ListItem(label="[B]Movies[/B]")
    li.setInfo(
        "video",
        {"plot": "Search, genres, popular and top rated films, then open Easynews from a title."},
    )
    if _ba:
        li.setArt(_ba)
    xbmcplugin.addDirectoryItem(ctx._handle, ctx._url_base + "/tmdb/movie", li, is_folder)

    li = xbmcgui.ListItem(label="[B]TV shows[/B]")
    li.setInfo(
        "video",
        {"plot": "Search, genres, popular and top rated series, then seasons and episodes (like TMDb Helper)."},
    )
    if _ba:
        li.setArt(_ba)
    xbmcplugin.addDirectoryItem(ctx._handle, ctx._url_base + "/tmdb/tv", li, is_folder)

    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)


def tmdb_hub_movie():
    if not _require_tmdb_key():
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    xbmcplugin.setPluginCategory(ctx._handle, "TMDB — Movies")
    xbmcplugin.setContent(ctx._handle, "videos")
    is_folder = True
    li = xbmcgui.ListItem(label="[COLOR yellow]<< TMDB[/COLOR]")
    xbmcplugin.addDirectoryItem(ctx._handle, ctx._url_base + "/tmdb", li, is_folder)

    li = xbmcgui.ListItem(label="Search by title")
    li.setInfo("video", {"plot": "Search TMDB for a film, then open Easynews results for that title."})
    xbmcplugin.addDirectoryItem(ctx._handle, ctx._url_base + "/tmdb/search", li, is_folder)

    li = xbmcgui.ListItem(label="Browse by genre")
    li.setInfo("video", {"plot": "Pick a genre, then pick a film from TMDB’s list."})
    xbmcplugin.addDirectoryItem(ctx._handle, ctx._url_base + "/tmdb/genres", li, is_folder)

    li = xbmcgui.ListItem(label="Popular")
    li.setInfo("video", {"plot": "TMDB’s current popular movies."})
    xbmcplugin.addDirectoryItem(ctx._handle, ctx._url_base + "/tmdb/movie/popular", li, is_folder)

    li = xbmcgui.ListItem(label="Top rated")
    li.setInfo("video", {"plot": "TMDB’s top rated movies (by vote average)."})
    xbmcplugin.addDirectoryItem(ctx._handle, ctx._url_base + "/tmdb/movie/top_rated", li, is_folder)

    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)


def tmdb_hub_tv():
    if not _require_tmdb_key():
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    xbmcplugin.setPluginCategory(ctx._handle, "TMDB — TV")
    xbmcplugin.setContent(ctx._handle, "videos")
    is_folder = True
    li = xbmcgui.ListItem(label="[COLOR yellow]<< TMDB[/COLOR]")
    xbmcplugin.addDirectoryItem(ctx._handle, ctx._url_base + "/tmdb", li, is_folder)

    li = xbmcgui.ListItem(label="Search by title")
    li.setInfo("video", {"plot": "Search TMDB for a series, then choose season and episode."})
    xbmcplugin.addDirectoryItem(ctx._handle, ctx._url_base + "/tmdb/tv/search", li, is_folder)

    li = xbmcgui.ListItem(label="Browse by genre")
    li.setInfo("video", {"plot": "Pick a TV genre, then a show, then season and episode."})
    xbmcplugin.addDirectoryItem(ctx._handle, ctx._url_base + "/tmdb/tv/genres", li, is_folder)

    li = xbmcgui.ListItem(label="Popular")
    li.setInfo("video", {"plot": "TMDB’s current popular TV shows."})
    xbmcplugin.addDirectoryItem(ctx._handle, ctx._url_base + "/tmdb/tv/popular", li, is_folder)

    li = xbmcgui.ListItem(label="Top rated")
    li.setInfo("video", {"plot": "TMDB’s top rated TV shows (by vote average)."})
    xbmcplugin.addDirectoryItem(ctx._handle, ctx._url_base + "/tmdb/tv/top_rated", li, is_folder)

    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)


def tmdb_genres(media="movie"):
    key = _require_tmdb_key()
    if not key:
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    label = "TMDB — TV genres" if media == "tv" else "TMDB — Movie genres"
    xbmcplugin.setPluginCategory(ctx._handle, label)
    xbmcplugin.setContent(ctx._handle, "videos")
    is_folder = True
    hub = ctx._url_base + ("/tmdb/tv" if media == "tv" else "/tmdb/movie")
    hub_lbl = "TV" if media == "tv" else "Movies"
    li = xbmcgui.ListItem(label="[COLOR yellow]<< TMDB — {}[/COLOR]".format(hub_lbl))
    xbmcplugin.addDirectoryItem(ctx._handle, hub, li, is_folder)
    kind = "tv" if media == "tv" else "movie"
    tmdb_url = "https://api.themoviedb.org/3/genre/{}/list?language=en-US&api_key={}".format(kind, key)
    response = requests.get(tmdb_url, headers=_tmdb_json_headers, timeout=30)
    if not _tmdb_http_ok(response):
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    genres = response.json()["genres"]
    xbmc.log("{}: TMDB genres ({}): {}".format(_LOG, kind, genres), xbmc.LOGDEBUG)
    for genre in genres:
        li = xbmcgui.ListItem(label=genre["name"])
        if media == "tv":
            url = ctx._url_base + "/tmdb/tv/discover?" + urlencode({"genre": str(genre["id"])})
        else:
            url = ctx._url_base + "/tmdb/discover?" + urlencode({"genre": str(genre["id"])})
        xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)


def tmdb_discover(genre: str, page: str, media: str = "movie"):
    key = _require_tmdb_key()
    if not key:
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    if media == "tv":
        url = (
            "https://api.themoviedb.org/3/discover/tv?"
            "include_adult=false&language=en-US"
            f"&page={quote(str(page), safe='')}"
            "&sort_by=popularity.desc"
            "&vote_count.gte=50"
            f"&with_genres={quote(str(genre), safe='')}"
            f"&api_key={key}"
        )
    else:
        url = (
            "https://api.themoviedb.org/3/discover/movie?"
            "include_adult=false&include_video=false&language=en-US"
            f"&page={quote(str(page), safe='')}"
            "&sort_by=vote_average.desc"
            "&vote_count.gte=250"
            f"&with_genres={quote(str(genre), safe='')}"
            f"&api_key={key}"
        )
    xbmc.log("{}: TMDB discover URL: {}".format(_LOG, url), xbmc.LOGDEBUG)
    response = requests.get(url, headers=_tmdb_json_headers, timeout=30)
    if not _tmdb_http_ok(response):
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    payload = response.json()
    results = payload["results"]
    xbmcplugin.setPluginCategory(ctx._handle, "TMDB Discover")
    xbmcplugin.setContent(ctx._handle, "videos")
    is_folder = True
    page = payload["page"]
    total_pages = payload["total_pages"]
    hub = ctx._url_base + ("/tmdb/tv" if media == "tv" else "/tmdb/movie")
    li = xbmcgui.ListItem(
        label="Page {} of {} --- [COLOR yellow]{}[/COLOR]".format(
            page, total_pages, "Back to TV" if media == "tv" else "Back to Movies"
        )
    )
    xbmcplugin.addDirectoryItem(ctx._handle, hub, li, is_folder)
    if int(page) < int(total_pages):
        li_next = xbmcgui.ListItem(label="[COLOR yellow]Next page >>[/COLOR]")
        if media == "tv":
            nurl = ctx._url_base + "/tmdb/tv/discover?" + urlencode(
                {"genre": str(genre), "page": str(int(page) + 1)}
            )
        else:
            nurl = ctx._url_base + "/tmdb/discover?" + urlencode(
                {"genre": str(genre), "page": str(int(page) + 1)}
            )
        xbmcplugin.addDirectoryItem(ctx._handle, nurl, li_next, is_folder)
    _render_tmdb_result_rows(results, media)
    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=True)


def tmdb_chart(media: str, chart: str, page: str):
    """TMDB movie/tv popular or top_rated lists (paged)."""
    key = _require_tmdb_key()
    if not key:
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    if chart not in ("popular", "top_rated"):
        chart = "popular"
    if media not in ("movie", "tv"):
        media = "movie"
    segment = "tv" if media == "tv" else "movie"
    api_url = "https://api.themoviedb.org/3/{}/{}?language=en-US&page={}&api_key={}".format(
        segment,
        chart,
        quote(str(page), safe=""),
        key,
    )
    xbmc.log("{}: TMDB chart URL: {}".format(_LOG, api_url), xbmc.LOGDEBUG)
    response = requests.get(api_url, headers=_tmdb_json_headers, timeout=30)
    if not _tmdb_http_ok(response):
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    payload = response.json()
    results = payload.get("results") or []
    titles = {
        ("movie", "popular"): "TMDB — Popular movies",
        ("movie", "top_rated"): "TMDB — Top rated movies",
        ("tv", "popular"): "TMDB — Popular TV",
        ("tv", "top_rated"): "TMDB — Top rated TV",
    }
    xbmcplugin.setPluginCategory(ctx._handle, titles.get((media, chart), "TMDB"))
    xbmcplugin.setContent(ctx._handle, "videos")
    is_folder = True
    page = payload.get("page") or 1
    total_pages = payload.get("total_pages") or 1
    hub = ctx._url_base + ("/tmdb/tv" if media == "tv" else "/tmdb/movie")
    route = "/tmdb/tv/{}" if media == "tv" else "/tmdb/movie/{}"
    route = route.format(chart)
    li = xbmcgui.ListItem(
        label="Page {} of {} --- [COLOR yellow]{}[/COLOR]".format(
            page, total_pages, "Back to TV" if media == "tv" else "Back to Movies"
        )
    )
    xbmcplugin.addDirectoryItem(ctx._handle, hub, li, is_folder)
    if int(page) < int(total_pages):
        li_next = xbmcgui.ListItem(label="[COLOR yellow]Next page >>[/COLOR]")
        nurl = ctx._url_base + route + "?" + urlencode({"page": str(int(page) + 1)})
        xbmcplugin.addDirectoryItem(ctx._handle, nurl, li_next, is_folder)
    _render_tmdb_result_rows(results, media)
    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=True)


def tmdb_search(title: str, page: str):
    key = _require_tmdb_key()
    if not key:
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    q = title.replace("+", " ").strip()
    url = f"https://api.themoviedb.org/3/search/movie?" \
          "include_adult=false&include_video=false&language=en-US" \
          f"&page={quote(str(page), safe='')}" \
          "&vote_count.gt=50" \
          f"&query={quote(q, safe='')}" \
          f"&api_key={key}"
    xbmc.log("{}: TMDB search URL: {}".format(_LOG, url), xbmc.LOGDEBUG)
    response = requests.get(url, headers=_tmdb_json_headers, timeout=30)
    if not _tmdb_http_ok(response):
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    payload = response.json()
    xbmc.log(
        "{}: TMDB search response (truncated): {}".format(_LOG, str(payload)[:4000]),
        xbmc.LOGDEBUG,
    )
    total_results = int(payload.get("total_results") or 0)
    page = payload["page"]
    total_pages = payload["total_pages"]
    movies = payload["results"]
    xbmcplugin.setPluginCategory(ctx._handle, 'TMDB Search')
    xbmcplugin.setContent(ctx._handle, 'videos')
    is_folder = True
    if total_results == 0:
        #  no dice amigo
        li = xbmcgui.ListItem(label="[COLOR yellow]No results sorry, try another search[/COLOR]")
        li.setInfo('video', {'plot': "boop!",
                             'mediatype': 'video'})
        url = ctx._url_base + "/tmdb/movie"
        xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
    else:
        # search results header
        li = xbmcgui.ListItem(label="Page {} of {}".format(page, total_pages) + " --- [COLOR yellow]New Search[/COLOR]")
        url = ctx._url_base + "/tmdb/movie"
        xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
        # pager
        if int(page) < int(total_pages):
            li_next_page = xbmcgui.ListItem(label="[COLOR yellow]Next page >>[/COLOR]")
            url = ctx._url_base + "/tmdb/search/results?" + urlencode(
                {"title": title, "page": str(int(page) + 1)}
            )
            xbmcplugin.addDirectoryItem(ctx._handle, url, li_next_page, is_folder)
        for movie in movies:
            rd = (movie.get("release_date") or "")[:4]
            li = xbmcgui.ListItem(label=movie.get("title", "Movie") + (" ({})".format(rd) if rd else ""))
            pu = _poster_url(movie.get("poster_path"))
            if pu:
                li.setArt({"thumb": pu, "icon": pu})
            overview = (movie.get("overview") or "") + "\n\n"
            overview += "Vote average: {}\nVote count: {}\nPopularity: {}".format(
                movie.get("vote_average"),
                movie.get("vote_count"),
                movie.get("popularity"),
            )
            li.setInfo(
                "video",
                {"title": movie.get("title"), "plot": overview, "mediatype": "video"},
            )
            url = _searchresults_url(
                api.easynews_search_strip((movie.get("title", "") + " " + rd).strip())
            )
            xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=True)


def tmdb_search_tv(title: str, page: str):
    key = _require_tmdb_key()
    if not key:
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    q = title.replace("+", " ").strip()
    url = (
        "https://api.themoviedb.org/3/search/tv?"
        "include_adult=false&language=en-US"
        f"&page={quote(str(page), safe='')}"
        f"&query={quote(q, safe='')}"
        f"&api_key={key}"
    )
    xbmc.log("{}: TMDB TV search URL: {}".format(_LOG, url), xbmc.LOGDEBUG)
    response = requests.get(url, headers=_tmdb_json_headers, timeout=30)
    if not _tmdb_http_ok(response):
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    payload = response.json()
    total_results = int(payload.get("total_results") or 0)
    page = payload["page"]
    total_pages = payload["total_pages"]
    shows = payload["results"]
    xbmcplugin.setPluginCategory(ctx._handle, "TMDB TV search")
    xbmcplugin.setContent(ctx._handle, "videos")
    is_folder = True
    if total_results == 0:
        li = xbmcgui.ListItem(label="[COLOR yellow]No results — try another title[/COLOR]")
        li.setInfo("video", {"plot": "No TV shows matched that search.", "mediatype": "video"})
        url = ctx._url_base + "/tmdb/tv"
        xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
    else:
        li = xbmcgui.ListItem(
            label="Page {} of {} --- [COLOR yellow]New search[/COLOR]".format(page, total_pages)
        )
        url = ctx._url_base + "/tmdb/tv"
        xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
        if int(page) < int(total_pages):
            li_next = xbmcgui.ListItem(label="[COLOR yellow]Next page >>[/COLOR]")
            nurl = ctx._url_base + "/tmdb/tv/search/results?" + urlencode(
                {"title": title, "page": str(int(page) + 1)}
            )
            xbmcplugin.addDirectoryItem(ctx._handle, nurl, li_next, is_folder)
        for show in shows:
            name = show.get("name") or show.get("original_name") or "TV"
            yr = _year_from_air_or_release(show, tv=True)
            label = "{} ({})".format(name, yr) if yr else name
            plot = (show.get("overview") or "") + "\n\n"
            plot += "Vote average: {}\nVote count: {}\nPopularity: {}".format(
                show.get("vote_average"),
                show.get("vote_count"),
                show.get("popularity"),
            )
            li = xbmcgui.ListItem(label=label)
            pu = _poster_url(show.get("poster_path"))
            if pu:
                li.setArt({"thumb": pu, "icon": pu})
            li.setInfo("video", {"title": name, "plot": plot, "mediatype": "video"})
            sid = show.get("id")
            if sid:
                durl = ctx._url_base + "/tmdb/tv/detail?" + urlencode({"tv": str(sid)})
                xbmcplugin.addDirectoryItem(ctx._handle, durl, li, is_folder)
    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=True)


def tmdb_tv_detail(tv_id: str):
    key = _require_tmdb_key()
    if not key or not str(tv_id).strip():
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    url = "https://api.themoviedb.org/3/tv/{}?language=en-US&api_key={}".format(
        quote(str(tv_id), safe=""),
        key,
    )
    response = requests.get(url, headers=_tmdb_json_headers, timeout=30)
    if not _tmdb_http_ok(response):
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    data = response.json()
    show_name = data.get("name") or data.get("original_name") or "TV"
    xbmcplugin.setPluginCategory(ctx._handle, show_name)
    xbmcplugin.setContent(ctx._handle, "videos")
    is_folder = True
    li = xbmcgui.ListItem(label="[COLOR yellow]<< TMDB — TV[/COLOR]")
    xbmcplugin.addDirectoryItem(ctx._handle, ctx._url_base + "/tmdb/tv", li, is_folder)
    overview = data.get("overview") or ""
    overview += "\n\nStatus: {}\nFirst air: {}\nEpisodes: {}".format(
        data.get("status"),
        data.get("first_air_date"),
        data.get("number_of_episodes"),
    )
    overview += "\n\n[COLOR yellow]Open to search Easynews for this series title.[/COLOR]"
    li = xbmcgui.ListItem(label="Search Easynews — {}".format(show_name))
    pu = _poster_url(data.get("poster_path"))
    if pu:
        li.setArt({"thumb": pu, "icon": pu})
    li.setInfo("video", {"title": show_name, "plot": overview, "mediatype": "video"})
    li.setProperty("IsPlayable", "false")
    xbmcplugin.addDirectoryItem(
        ctx._handle,
        _searchresults_url(api.easynews_search_strip(show_name.strip())),
        li,
        is_folder,
    )
    seasons = data.get("seasons") or []
    for s in sorted(seasons, key=lambda x: int(x.get("season_number") or -1)):
        sn = s.get("season_number")
        if sn is None:
            continue
        ep_count = s.get("episode_count")
        sn_lbl = "Season {}".format(sn)
        if ep_count is not None:
            sn_lbl += " ({} eps)".format(ep_count)
        li = xbmcgui.ListItem(label=sn_lbl)
        li.setInfo("video", {"title": sn_lbl, "mediatype": "video"})
        surl = ctx._url_base + "/tmdb/tv/season?" + urlencode(
            {"tv": str(tv_id), "sn": str(int(sn)), "show": show_name}
        )
        xbmcplugin.addDirectoryItem(ctx._handle, surl, li, is_folder)
    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=True)


def tmdb_tv_season(tv_id: str, sn: str, show_name: str):
    key = _require_tmdb_key()
    if not key or not str(tv_id).strip():
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    try:
        snum = int(sn)
    except (TypeError, ValueError):
        snum = 1
    if not (show_name or "").strip():
        u0 = "https://api.themoviedb.org/3/tv/{}?language=en-US&api_key={}".format(
            quote(str(tv_id), safe=""),
            key,
        )
        r0 = requests.get(u0, headers=_tmdb_json_headers, timeout=30)
        if r0.status_code != 200:
            xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
            return
        show_name = r0.json().get("name") or r0.json().get("original_name") or ""
    url = "https://api.themoviedb.org/3/tv/{}/season/{}?language=en-US&api_key={}".format(
        quote(str(tv_id), safe=""),
        snum,
        key,
    )
    response = requests.get(url, headers=_tmdb_json_headers, timeout=30)
    if not _tmdb_http_ok(response):
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    payload = response.json()
    episodes = payload.get("episodes") or []
    xbmcplugin.setPluginCategory(ctx._handle, "{} — S{:02d}".format(show_name, snum))
    xbmcplugin.setContent(ctx._handle, "videos")
    is_folder = True
    li = xbmcgui.ListItem(label="[COLOR yellow]<< {}[/COLOR]".format(show_name))
    xbmcplugin.addDirectoryItem(
        ctx._handle,
        ctx._url_base + "/tmdb/tv/detail?" + urlencode({"tv": str(tv_id)}),
        li,
        is_folder,
    )
    for ep in episodes:
        enum = ep.get("episode_number")
        if enum is None:
            continue
        etitle = ep.get("name") or "Episode {}".format(enum)
        label = "S{:02d}E{:02d} — {}".format(snum, int(enum), etitle)
        plot = (ep.get("overview") or "").strip()
        if ep.get("air_date"):
            plot = ("Aired: {}\n\n".format(ep["air_date"])) + plot
        li = xbmcgui.ListItem(label=label)
        st = ep.get("still_path")
        pu = _poster_url(st) if st else _poster_url(payload.get("poster_path"))
        if pu:
            li.setArt({"thumb": pu, "icon": pu})
        li.setInfo("video", {"title": etitle, "plot": plot, "mediatype": "episode"})
        q = api.easynews_search_strip(
            "{} S{:02d}E{:02d}".format(show_name.strip(), snum, int(enum))
        )
        play_url = _searchresults_url(q)
        xbmcplugin.addDirectoryItem(ctx._handle, play_url, li, is_folder)
    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=True)
