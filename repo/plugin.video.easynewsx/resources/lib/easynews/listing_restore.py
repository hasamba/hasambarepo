# -*- coding: utf-8 -*-
"""Persist and replay search listings after playback."""
import time

from resources.lib.easynews import context as ctx

LISTING_RESTORE_FILE = "listing_restore.json"
LISTING_RESTORE_MAX_AGE = 7 * 24 * 3600


def _clear_listing_restore():
    try:
        ctx.vfs.delete(LISTING_RESTORE_FILE)
    except Exception:
        pass


def _save_listing_restore(endpoint, query, newsgroup, page):
    ctx.vfs.save_obj_to_json(
        LISTING_RESTORE_FILE,
        {
            "endpoint": endpoint,
            "query": query or "",
            "newsgroup": newsgroup or "",
            "page": int(page),
            "ts": int(time.time()),
        },
    )


def _try_restore_listing(endpoint, url_newsgroup=None):
    """After playback, Kodi reloads the same plugin path (/search, etc.); replay listing without keyboard."""
    data = ctx.vfs.get_json_as_obj(LISTING_RESTORE_FILE, default=None)
    if not data or not isinstance(data, dict):
        return False
    if data.get("endpoint") != endpoint:
        return False
    if url_newsgroup is not None and data.get("newsgroup") != url_newsgroup:
        return False
    try:
        ts = int(data.get("ts", 0))
    except (TypeError, ValueError):
        return False
    if ts and (int(time.time()) - ts) > LISTING_RESTORE_MAX_AGE:
        return False
    query = data["query"] if "query" in data else ""
    newsgroup = data["newsgroup"] if "newsgroup" in data else ""
    try:
        page = int(data.get("page", 1))
    except (TypeError, ValueError):
        page = 1
    if endpoint == "/search" and not (query or "").strip():
        return False
    if endpoint == "/addnewsgroup" and not (newsgroup or "").strip():
        return False
    if endpoint == "/searchwithinng" and (
        not (query or "").strip() or not (newsgroup or "").strip()
    ):
        return False
    from resources.lib.easynews.search_ui import show_easynews_results
    show_easynews_results(query=query, newsgroup=newsgroup, page=page)
    return True
