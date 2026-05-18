# -*- coding: utf-8 -*-
"""Fetch members 3.0 home HTML and scrape account plan + gigs from #ENAccount."""

from __future__ import annotations

import html as html_stdlib
import json
import re
import time
import urllib.error

import xbmc
import xbmcgui

from resources.lib.easynews import context as ctx
from resources.lib.easynews import credentials
from resources.lib.easynews.api import get_https_with_auth
from resources.lib.easynews.constants import ACCOUNT_MENU_LABEL_CACHE

_LOG = "plugin.video.easynewsx"
_MEMBERS_30_BASE = "https://members.easynews.com/3.0/"

# Second <p> in .col.s8: plan span, <br>, "N.NN Gigs available" span
_EN_ACCOUNT_S8_RE = re.compile(
    r'<div\s+class=["\'][^"\']*\bcol\s+s8\b[^"\']*["\']\s*>'
    r'\s*<p>\s*<span>(?P<email>[^<]*)</span>\s*</p>\s*'
    r'<p>\s*<span>(?P<plan>[^<]+)</span>\s*'
    r'<br\s*/?\s*>\s*'
    r'<span>(?P<gigs>[^<]+)</span>',
    re.IGNORECASE | re.DOTALL,
)


def _parse_plan_and_gigs_line(html_text: str):
    """Return (plan, gigs_line) or None."""
    start = html_text.find('id="ENAccount"')
    if start == -1:
        start = html_text.find("id='ENAccount'")
    if start == -1:
        return None
    end = html_text.find('id="FileBucketMenu"', start)
    if end == -1:
        end = start + 12000
    section = html_text[start:end]
    m = _EN_ACCOUNT_S8_RE.search(section)
    if not m:
        return None
    plan = html_stdlib.unescape(m.group("plan").strip())
    gigs = html_stdlib.unescape(m.group("gigs").strip())
    return plan, gigs


def _format_label(plan: str, gigs_line: str) -> str:
    """Single-line summary; Kodi [COLOR] tags for list label/plot."""
    return "[COLOR yellow]{}, {}[/COLOR]".format(plan, gigs_line)


def _fetch_account_summary_from_network():
    """Hit /3.0/ and return label text (errors as user-facing strings)."""
    try:
        url = "{}?_={}".format(_MEMBERS_30_BASE, int(time.time()))
        raw, _, _meta = get_https_with_auth(url, timeout=45)
        text = raw.decode("utf-8", errors="replace") if isinstance(raw, (bytes, bytearray)) else str(raw)
        parsed = _parse_plan_and_gigs_line(text)
        if not parsed:
            xbmc.log(
                "{}: account scrape: ENAccount / col s8 pattern not found".format(_LOG),
                xbmc.LOGDEBUG,
            )
            return "Could not read account info from EasyNews. The page layout may have changed."
        plan, gigs_line = parsed
        return _format_label(plan, gigs_line)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return "[COLOR red]EasyNews login failed. Check username and password in settings.[/COLOR]"
        if e.code == 403:
            return "EasyNews denied access (HTTP 403). Check your account status."
        return "EasyNews returned an error (HTTP {}).".format(e.code)
    except urllib.error.URLError:
        return "Could not reach EasyNews. Check your connection."
    except Exception as err:
        xbmc.log("{}: account scrape failed: {}".format(_LOG, err), xbmc.LOGDEBUG)
        return "Could not load EasyNews account info."


def _read_label_cache():
    raw = ctx.vfs.read(ACCOUNT_MENU_LABEL_CACHE)
    if not raw:
        return None
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and data.get("label"):
            return str(data["label"])
    except (TypeError, ValueError):
        pass
    return None


def _write_label_cache(label: str):
    try:
        ctx.vfs.save_obj_to_json(ACCOUNT_MENU_LABEL_CACHE, {"label": label})
    except Exception:
        pass


def account_menu_label():
    """
    Main-menu row label.

    Before login or before a successful fetch: fixed prompt (#33059).
    After fetch: yellow plan/gigs line only (from cache).
    """
    cached = _read_label_cache()
    if credentials.account_configured() and cached:
        return cached
    return ctx.addon.getLocalizedString(33059)


def account_menu_plot():
    """Info panel text for the account row (no network)."""
    if not credentials.account_configured():
        return ctx.addon.getLocalizedString(33060)
    cached = _read_label_cache()
    if cached:
        return "{}\n\n[COLOR gray]Select this row again to refresh.[/COLOR]".format(cached)
    return ctx.addon.getLocalizedString(33061)


def run_account_refresh_action():
    """
    User selected the account row: pull /3.0/, update disk cache, refresh current folder.
    Does not call main_menu (avoids pushing another level on Kodi's back stack).
    """
    if not credentials.require_account_dialog():
        return
    label = _fetch_account_summary_from_network()
    _write_label_cache(label)
    xbmc.executebuiltin(
        'Notification(EasyNews,Account info refreshed.,2000,,false)'
    )
    xbmc.executebuiltin("Container.Refresh")
