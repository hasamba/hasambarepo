# -*- coding: utf-8 -*-
"""Open project URLs in the system browser (best-effort)."""
import webbrowser

import xbmcgui

GITHUB_REPO_URL = "https://github.com/tetsuosoft/EasyNewsKodi"


def open_github_repo():
    try:
        webbrowser.open(GITHUB_REPO_URL)
    except Exception as e:
        xbmcgui.Dialog().notification(
            "EasyNews",
            str(e),
            xbmcgui.NOTIFICATION_WARNING,
        )
