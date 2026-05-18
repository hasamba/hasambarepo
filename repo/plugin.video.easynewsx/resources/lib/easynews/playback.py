# -*- coding: utf-8 -*-
"""Resolve Easynews URL and hand off to Kodi player."""
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth
import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.easynews import context as ctx

def _runtime_int(runtime):
    if runtime is None or runtime == "":
        return None
    try:
        return int(float(runtime))
    except (TypeError, ValueError):
        return None


def play_video(path, title=None, thumb=None, plot=None, runtime=None, newsgroups=None):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    :param title: Optional display title for play history (from search results).
    :param thumb: Optional Easynews thumbnail URL (for list art + play history).
    :param plot: Optional info-panel plot (newsgroups, subject, res, fps).
    :param runtime: Optional duration in seconds (string or number from router).
    :param newsgroups: Optional space-separated newsgroup names (for play history context menu).
    """
    _log = "plugin.video.easynewsx"
    initial_url = path
    # One lightweight probe (no follow): Easynews 302 → CDN URL, or 200 → same URL.
    # Do not open the stream again in Python — only VideoPlayer should pull the file. A second
    # requests session competes with Kodi's curl for CDN/range reads on large MKV and can worsen
    # timeouts; users should not need to edit advancedsettings.xml for that.
    probe = requests.get(
        initial_url,
        auth=HTTPBasicAuth(ctx.username, ctx.password),
        cookies=ctx.easynews_chickenlicker_cookies_dict(),
        allow_redirects=False,
        timeout=15,
    )
    try:
        status = probe.status_code
        location = probe.headers.get("Location") or probe.headers.get("location")
        location = location.strip() if location else None

        streaming_url = None
        if status in (301, 302, 303, 307, 308):
            if not location:
                xbmc.log(
                    "{}: play_video initial probe HTTP {} redirect but no Location header".format(
                        _log, status
                    ),
                    xbmc.LOGDEBUG,
                )
                xbmcgui.Dialog().ok(
                    "EasyNews",
                    "Could not resolve stream URL (redirect without Location).",
                )
                return
            streaming_url = urljoin(initial_url, location)
            xbmc.log(
                "{}: play_video redirect HTTP {} -> {}".format(_log, status, streaming_url),
                xbmc.LOGDEBUG,
            )
        elif status == 200:
            if location:
                streaming_url = urljoin(initial_url, location)
                xbmc.log(
                    "{}: play_video HTTP 200 with Location (using redirect target) -> {}".format(
                        _log, streaming_url
                    ),
                    xbmc.LOGDEBUG,
                )
            else:
                streaming_url = initial_url
                xbmc.log(
                    "{}: play_video HTTP 200 direct stream URL (no Location; same as request URL)".format(
                        _log
                    ),
                    xbmc.LOGDEBUG,
                )
        else:
            xbmc.log(
                "{}: play_video initial probe failed: HTTP {}".format(_log, status),
                xbmc.LOGDEBUG,
            )
            if status == 401:
                xbmcgui.Dialog().ok(
                    "EasyNews",
                    "Authentication failed (HTTP 401).\n\nCheck your username and password in settings.",
                )
                return
            if status == 403:
                xbmcgui.Dialog().ok(
                    "EasyNews",
                    "Acccess denied / failed (HTTP 403).\n\nCheck your EasyNews account status and try again.",
                )
                return
            xbmcgui.Dialog().ok(
                "EasyNews",
                "Failed to obtain stream URL (HTTP {}).".format(status),
            )
            return

        xbmcgui.Dialog().notification(
            "EasyNews Video", "Opening stream...", xbmcgui.NOTIFICATION_INFO
        )
        play_item = xbmcgui.ListItem(path=streaming_url)
        # These streams are served via tokenised CDN URLs; Kodi resume seeks can be unreliable.
        # Force "start from beginning" to avoid Kodi attempting a large resume byte-offset seek.
        play_item.setProperty("ResumeTime", "0")
        play_item.setProperty("TotalTime", "0")
        if thumb:
            play_item.setArt({"thumb": thumb, "icon": thumb})
        dur = _runtime_int(runtime)
        vinfo = {"mediatype": "video"}
        if title:
            vinfo["title"] = title
        if plot:
            vinfo["plot"] = plot
        if dur is not None:
            vinfo["duration"] = dur
        play_item.setInfo("video", vinfo)
        try:
            vtag = play_item.getVideoInfoTag()
            vtag.setMediaType("video")
            try:
                vtag.setResumePoint(0.0, 0.0)
            except TypeError:
                vtag.setResumePoint(0.0)
        except AttributeError:
            pass
        xbmc.log(
            "{}: play_video handing off to player (single connection; no duplicate stream fetch)".format(
                _log
            ),
            xbmc.LOGDEBUG,
        )
        ctx.play_history.add(
            title or "",
            initial_url,
            thumb=thumb,
            plot=plot,
            runtime=dur,
            newsgroups=newsgroups,
        )
        xbmcplugin.setResolvedUrl(ctx._handle, True, listitem=play_item)
    except requests.exceptions.RequestException as e:
        xbmc.log("{}: play_video probe failed: {}".format(_log, e), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            "Playback Error", "Could not reach EasyNews: {}".format(str(e)), xbmcgui.NOTIFICATION_ERROR
        )
    finally:
        probe.close()

