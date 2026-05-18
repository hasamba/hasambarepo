# -*- coding: utf-8 -*-
"""Experimental helpers to launch an external VLC player with a URL."""

from __future__ import annotations

import os
import subprocess
import sys
import shutil

import requests
from requests.auth import HTTPBasicAuth
import xbmc
import xbmcgui

from resources.lib.easynews import context as ctx

_LOG = "plugin.video.easynewsx"

def _is_android() -> bool:
    try:
        # Kodi condition is typically lowercase.
        return bool(
            xbmc.getCondVisibility("system.platform.android")
            or xbmc.getCondVisibility("System.Platform.Android")
        )
    except Exception:
        return False


def _windows_vlc_exe() -> str | None:
    """Resolve vlc.exe on Windows. Do not use shell ``start <https-url>`` — that opens the default browser."""
    for p in (
        r"C:\Program Files\VideoLAN\VLC\vlc.exe",
        r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
    ):
        if p and os.path.isfile(p):
            return p
    try:
        la = os.path.expandvars(r"%LOCALAPPDATA%\Programs\VideoLAN\VLC\vlc.exe")
        if la and r"%LOCALAPPDATA%" not in la and os.path.isfile(la):
            return la
    except Exception:
        pass
    w = shutil.which("vlc")
    if w and os.path.isfile(w):
        return w
    return None


def vlc_is_installed() -> bool:
    """
    Best-effort check for VLC presence without launching it.

    - Android: uses `pm path org.videolan.vlc` (may not exist on all builds).
    - Desktop: checks PATH and a few common install locations.
    """
    try:
        if _is_android():
            try:
                p = subprocess.Popen(
                    ["pm", "path", "org.videolan.vlc"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                )
                out, _ = p.communicate(timeout=2)
                if p.returncode == 0 and out and b"package:" in out:
                    return True
                return False
            except Exception:
                return False

        if shutil.which("vlc"):
            return True

        plat = sys.platform.lower()
        if plat.startswith("darwin"):
            return os.path.exists("/Applications/VLC.app")
        if plat.startswith("win"):
            return _windows_vlc_exe() is not None
        # linux/other: PATH check above is usually enough
        return False
    except Exception:
        return False


def _copy_to_clipboard(text: str) -> bool:
    """
    Best-effort clipboard copy.
    Kodi builds differ a lot; try xbmcgui first, then OS fallbacks.
    """
    if not text:
        return False
    try:
        # Kodi 20+ typically provides this.
        xbmcgui.Clipboard().set(text)  # type: ignore[attr-defined]
        return True
    except Exception:
        pass
    try:
        # Older Kodi: this may exist (varies by platform).
        xbmcgui.Window(10000).setProperty("plugin.video.easynewsx.clipboard", text)
    except Exception:
        pass

    plat = sys.platform.lower()
    try:
        if plat.startswith("darwin"):
            p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            p.communicate(input=text.encode("utf-8"))
            return p.returncode == 0
        if plat.startswith("win"):
            p = subprocess.Popen(["cmd", "/c", "clip"], stdin=subprocess.PIPE)
            p.communicate(input=text.encode("utf-8"))
            return p.returncode == 0
        # linux / others
        for cmd in (["wl-copy"], ["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]):
            try:
                p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                p.communicate(input=text.encode("utf-8"))
                if p.returncode == 0:
                    return True
            except Exception:
                continue
    except Exception:
        return False
    return False


def _launch_command(argv: list[str]) -> tuple[bool, str]:
    """Run argv without blocking Kodi; returns (ok, error_str)."""
    try:
        subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
        return True, ""
    except Exception as e:
        return False, repr(e)

def _resolve_easynews_redirect_url(members_url: str) -> tuple[str, str]:
    """
    Resolve the expiring CDN URL (302 Location) from an Easynews members dl URL.

    Returns (resolved_url, diag) where diag is empty on success.
    """
    if not members_url:
        return members_url, "missing_url"
    probe = None
    try:
        probe = requests.get(
            members_url,
            auth=HTTPBasicAuth(ctx.username, ctx.password),
            cookies=ctx.easynews_chickenlicker_cookies_dict(),
            allow_redirects=False,
            timeout=20,
        )
        status = probe.status_code
        location = probe.headers.get("Location") or probe.headers.get("location")
        location = location.strip() if location else None
        if status in (301, 302, 303, 307, 308) and location:
            # Keep behaviour consistent with playback.py.
            from urllib.parse import urljoin

            return urljoin(members_url, location), ""
        if status == 200:
            # No redirect: return original.
            return members_url, ""
        return members_url, "http_status={}".format(status)
    except Exception as e:
        return members_url, "resolve_err={}".format(repr(e))
    finally:
        try:
            if probe is not None:
                probe.close()
        except Exception:
            pass


def _runtime_int(runtime):
    if runtime is None or runtime == "":
        return None
    try:
        return int(float(runtime))
    except (TypeError, ValueError):
        return None


def open_in_vlc(
    url: str | None,
    title: str | None = None,
    thumb: str | None = None,
    plot: str | None = None,
    runtime=None,
    newsgroups: str | None = None,
    resolve_redirect: bool = False,
):
    """
    Attempt to open the provided URL in external VLC.

    If resolve_redirect=True, first resolve the expiring CDN URL (Location redirect)
    and pass that to VLC instead.
    """
    if not url:
        xbmcgui.Dialog().notification("EasyNews", "Missing URL.", xbmcgui.NOTIFICATION_ERROR, 5000)
        return

    # Some callers pass EasyNews URLs with Kodi-style headers after a pipe.
    members_url = url.split("|", 1)[0]
    final_url = members_url
    diag = ""
    if resolve_redirect:
        final_url, diag = _resolve_easynews_redirect_url(members_url)
        if diag:
            xbmc.log("{}: open_in_vlc resolve redirect issue: {}".format(_LOG, diag), xbmc.LOGDEBUG)

    plat = sys.platform.lower()
    launched = False
    err = ""

    # Android / Shield: launch VLC via Android intent
    if _is_android():
        try:
            pkg = "org.videolan.vlc"
            intent = "android.intent.action.VIEW"
            data_type = "video/*"
            data_uri = final_url.replace('"', '\\"')
            xbmc.executebuiltin(
                'StartAndroidActivity("{}", "{}", "{}", "{}")'.format(
                    pkg, intent, data_type, data_uri
                )
            )
            launched, err = True, ""
        except Exception as e:
            launched, err = False, repr(e)

    # Prefer explicit VLC invocation when possible (so it doesn't pick another app).
    if not launched and plat.startswith("darwin"):
        # macOS: open VLC.app directly if installed in /Applications; otherwise fall back to 'vlc' on PATH.
        if os.path.exists("/Applications/VLC.app"):
            launched, err = _launch_command(["open", "-a", "VLC", final_url])
        if not launched:
            launched, err = _launch_command(["vlc", final_url])
    elif not launched and plat.startswith("win"):
        # Windows: only invoke vlc.exe (standard paths or PATH). Never ``start <url>`` — that
        # delegates https to the default browser and looks like a hijack.
        vlc_exe = _windows_vlc_exe()
        if vlc_exe:
            launched, err = _launch_command([vlc_exe, final_url])
        else:
            launched, err = False, "vlc.exe not found"
    elif not launched:
        # Linux: try vlc, then xdg-open.
        launched, err = _launch_command(["vlc", final_url])
        if not launched:
            launched, err = _launch_command(["xdg-open", final_url])

    copied = _copy_to_clipboard(final_url)

    if launched:
        # Mirror playback.py behaviour: store the members URL in history (not the expiring CDN URL).
        ctx.play_history.add(
            title or "",
            members_url,
            thumb=thumb,
            plot=plot,
            runtime=_runtime_int(runtime),
            newsgroups=newsgroups,
        )
        xbmc.log(
            "{}: open_in_vlc launched external player; url_len={} title={}".format(
                _LOG, len(final_url), (title or "")[:120]
            ),
            xbmc.LOGINFO,
        )
        msg = "Opened in VLC (experimental)."
        if copied:
            msg += " URL copied."
        xbmcgui.Dialog().notification("EasyNews", msg, xbmcgui.NOTIFICATION_INFO, 5000)
        return

    xbmc.log("{}: open_in_vlc failed: {}".format(_LOG, err), xbmc.LOGWARNING)
    lines = [
        "Could not launch VLC on this system.",
        "",
        "The URL is shown below{}:".format(" (also copied to clipboard)" if copied else ""),
        "",
        final_url,
    ]
    if err:
        lines += ["", "Error:", err]
    xbmcgui.Dialog().textviewer("Open in VLC (experimental)", "\n".join(lines))

