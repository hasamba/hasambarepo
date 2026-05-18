# -*- coding: utf-8 -*-
"""In-add-on user guide (content from resources/userguide.json)."""
import json
import os

import xbmc
import xbmcgui

from resources.lib.easynews import context as ctx

_LOG = "plugin.video.easynewsx"
_GUIDE_REL = os.path.join("resources", "userguide.json")


def _load_chapters():
    path = os.path.join(ctx.addon.getAddonInfo("path"), _GUIDE_REL)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return [c for c in data if isinstance(c, dict) and c.get("title") and c.get("body")]
    except (OSError, ValueError, TypeError) as e:
        xbmc.log("{}: userguide load failed: {}".format(_LOG, e), xbmc.LOGWARNING)
    return [
        {
            "title": "User guide",
            "body": "Add or fix resources/userguide.json in the add-on folder — a JSON array of objects with \"title\" and \"body\" strings.",
        }
    ]


def _full_guide_text(chapters):
    parts = []
    for ch in chapters:
        parts.append("{}\n\n{}".format(ch["title"], ch["body"].strip()))
    return "\n\n———\n\n".join(parts)


def show_full_guide():
    """Kodi full-screen text viewer with every section from userguide.json."""
    chapters = _load_chapters()
    body = _full_guide_text(chapters)
    title = ctx.addon.getLocalizedString(33042)
    xbmcgui.Dialog().textviewer(title, body)
