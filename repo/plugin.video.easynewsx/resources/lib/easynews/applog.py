# -*- coding: utf-8 -*-
"""Anonymous startup ping (install + session id) for usage stats."""

from __future__ import annotations

import platform
import struct
import threading
import uuid
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import xbmc
import xbmcgui

from resources.lib.easynews.constants import APPLOG_BASE_URL, INSTALL_ID_FILENAME

_LOG = "plugin.video.easynewsx"

# Kodi re-runs main.py on almost every plugin action. WINDOW_HOME (10000) keeps
# properties for the whole Kodi process so we only ping once per Kodi session.
_HOME_WINDOW_ID = 10000
# v3: session flag set only in the worker's ``finally`` after the HTTP attempt
# finishes. ``main`` calls ``join_startup_ping(0.5)`` so the UI waits at most
# ~500ms for that attempt; if it still runs, we exit anyway (may retry next open).
_KODI_SESSION_SENT_PROP = "plugin.video.easynewsx.applog.kodi_session_v3"
_last_ping_thread = None


def _ping_env_fields():
    """Kodi build + host platform (aligned with main.py diagnostic)."""
    kodi = ""
    try:
        kodi = (xbmc.getInfoLabel("System.BuildVersion") or "").strip()
    except Exception:
        pass
    system = platform.system() or "unknown"
    release = platform.release() or "unknown"
    machine = platform.machine() or "unknown"
    try:
        bits = struct.calcsize("P") * 8
    except Exception:
        bits = None
    out = {
        "k": kodi,
        "os": "{} {}".format(system, release).strip(),
        "arch": machine,
    }
    if bits is not None:
        out["bits"] = str(bits)
    return out


def _get_or_create_install_id(vfs):
    data = vfs.get_json_as_obj(INSTALL_ID_FILENAME, default={})
    iid = (data.get("install_id") or "").strip()
    if not iid:
        iid = str(uuid.uuid4())
        vfs.save_obj_to_json(INSTALL_ID_FILENAME, {"install_id": iid})
    return iid


def _ping_worker(vfs, addon_version):
    try:
        install_id = _get_or_create_install_id(vfs)
        session_id = str(uuid.uuid4())
        q = {
            "i": install_id,
            "s": session_id,
            "v": addon_version or "",
        }
        for key, val in _ping_env_fields().items():
            if val:
                q[key] = val
        query = urlencode(q)
        url = APPLOG_BASE_URL.rstrip("/") + "/?" + query
        req = Request(url, headers={"User-Agent": "Kodi-EasyNews/{}".format(addon_version or "?")})
        urlopen(req, timeout=3).read()
        xbmc.log("{}: applog ping ok".format(_LOG), xbmc.LOGINFO)
    except Exception as e:
        xbmc.log("{}: applog ping skipped: {}".format(_LOG, e), xbmc.LOGDEBUG)
    finally:
        try:
            xbmcgui.Window(_HOME_WINDOW_ID).setProperty(_KODI_SESSION_SENT_PROP, "1")
        except Exception:
            pass


def schedule_startup_ping(vfs, addon_version):
    """Start one GET per Kodi session; pair with ``join_startup_ping`` from main."""
    global _last_ping_thread
    win = xbmcgui.Window(_HOME_WINDOW_ID)
    if win.getProperty(_KODI_SESSION_SENT_PROP):
        return

    t = threading.Thread(
        target=_ping_worker,
        args=(vfs, addon_version),
        name="easynews-applog",
    )
    t.daemon = True
    _last_ping_thread = t
    t.start()


def join_startup_ping(timeout=0.5):
    """Wait up to ``timeout`` seconds for the ping thread (cap UI delay)."""
    global _last_ping_thread
    t = _last_ping_thread
    _last_ping_thread = None
    if t is None:
        return
    if t.is_alive():
        t.join(timeout=timeout)
