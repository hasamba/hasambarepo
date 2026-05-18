# -*- coding: utf-8 -*-
"""EasyNews member account (username / password) checks."""

import xbmc
import xbmcgui

from resources.lib.easynews import context as ctx


def account_configured():
    u = (ctx.username or "").strip()
    p = (ctx.password or "").strip()
    return bool(u and p)


def require_account_dialog():
    """If username/password are missing, show a dialog and return False."""
    if account_configured():
        return True
    xbmcgui.Dialog().ok(
        ctx.addon.getLocalizedString(33040),
        ctx.addon.getLocalizedString(33041),
    )
    return False


def go_to_plugin_root():
    """After endOfDirectory, force the video browser to this add-on's root (main menu)."""
    xbmc.sleep(100)
    root = ctx.addon_base + "/root"
    xbmc.executebuiltin("Container.Update({})".format(root))
