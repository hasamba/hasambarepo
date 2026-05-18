# -*- coding: utf-8 -*-
"""Show addon.xml <news> once per content change (digest), not per version."""
import hashlib
import os
import xml.etree.ElementTree as ET

import xbmc
import xbmcgui

from resources.lib.easynews import context as ctx
from resources.lib.easynews.constants import ADDON_NEWS_SEEN_CACHE

_LOG = "plugin.video.easynewsx"


def _normalize_news_text(text):
    if not text:
        return ""
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").split("\n")).strip()


def _news_digest(text):
    normalized = _normalize_news_text(text)
    if not normalized:
        return ""
    return hashlib.md5(normalized.encode("utf-8")).hexdigest()  # nosec - content fingerprint only


def _news_from_addon_xml():
    try:
        path = os.path.join(ctx.addon.getAddonInfo("path"), "addon.xml")
        if not os.path.isfile(path):
            return ""
        tree = ET.parse(path)
        root = tree.getroot()
        for ext in root.findall("extension"):
            if ext.get("point") != "xbmc.addon.metadata":
                continue
            node = ext.find("news")
            if node is not None and (node.text or "").strip():
                return node.text
    except Exception as e:
        xbmc.log("{}: addon_news xml parse failed: {}".format(_LOG, e), xbmc.LOGDEBUG)
    return ""


def get_addon_news_text():
    """Plain text from addon metadata <news> (or changelog.txt fallback via Kodi)."""
    try:
        text = ctx.addon.getAddonInfo("changelog")
        if text and str(text).strip():
            return str(text)
    except Exception:
        pass
    return _news_from_addon_xml()


def _read_seen_digest():
    try:
        data = ctx.vfs.get_json_as_obj(ADDON_NEWS_SEEN_CACHE, default={})
        if isinstance(data, dict):
            return str(data.get("digest") or "")
    except Exception:
        pass
    return ""


def _write_seen_digest(digest):
    if not digest:
        return
    try:
        ctx.vfs.save_obj_to_json(ADDON_NEWS_SEEN_CACHE, {"digest": digest})
    except Exception as e:
        xbmc.log("{}: addon_news save seen failed: {}".format(_LOG, e), xbmc.LOGDEBUG)


def show_addon_news_dialog(mark_seen=True):
    """Text viewer for latest <news>; optionally record digest as shown."""
    text = _normalize_news_text(get_addon_news_text())
    if not text:
        xbmcgui.Dialog().ok(
            "EasyNews",
            "No release notes are available for this build.",
        )
        return False
    title = ctx.addon.getLocalizedString(33056)
    xbmcgui.Dialog().textviewer(title, text)
    if mark_seen:
        digest = _news_digest(text)
        if digest:
            _write_seen_digest(digest)
    return True


def maybe_show_on_main_menu_entry():
    """If <news> content changed since last shown, display once then remember digest."""
    text = _normalize_news_text(get_addon_news_text())
    digest = _news_digest(text)
    if not digest:
        return
    if digest == _read_seen_digest():
        return
    show_addon_news_dialog(mark_seen=True)
