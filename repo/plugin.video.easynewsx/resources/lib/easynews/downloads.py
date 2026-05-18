# -*- coding: utf-8 -*-
"""Download folder browser and file download."""
import os
import socket
import time
import urllib.parse
import urllib.request
from urllib.parse import urlencode

import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
import requests
from requests.auth import HTTPBasicAuth

from resources.lib.easynews import context as ctx

_LOG = "plugin.video.easynewsx"


def _vfs_dir_usable(path):
    """
    Kodi's xbmcvfs.exists() often returns False for real folders without a trailing
    slash, or for paths that only work with os.path. Resolve to a path we can use.
    """
    if path is None:
        return None
    p = str(path).strip()
    if not p:
        return None
    n = os.path.normpath(p.rstrip("/\\"))
    seen = set()
    candidates = []
    for c in (p, n, p.rstrip("/\\"), n + os.sep, n + "/", p + os.sep, p + "/"):
        if c and c not in seen:
            seen.add(c)
            candidates.append(c)
    for c in candidates:
        try:
            if xbmcvfs.exists(c):
                return os.path.normpath(str(c).rstrip("/\\"))
        except Exception:
            continue
    try:
        if os.path.isdir(n):
            return n
    except OSError:
        pass
    return None


def _vfs_try_listdir(path):
    last_exc = None
    n = os.path.normpath(str(path).rstrip("/\\"))
    for v in (path, n, n + os.sep, n + "/"):
        try:
            return xbmcvfs.listdir(v)
        except Exception as exc:
            last_exc = exc
    if last_exc:
        raise last_exc
    return [], []


def get_download_path(create=True):
    """
    Folder for “Download file” and split-part downloads.
    Uses setting general.download_folder if set; otherwise <profile>/downloads.
    Paths are translated (special://, etc.) for the current platform.
    """
    custom = (ctx.addon.getSetting("general.download_folder") or "").strip()
    if custom:
        path = xbmcvfs.translatePath(custom) or custom
    else:
        path = xbmcvfs.translatePath(os.path.join(ctx.addon_profile_path, "downloads"))
    if create and path and _vfs_dir_usable(path) is None:
        try:
            xbmcvfs.mkdirs(path)
        except Exception:
            pass
    return path


def _safe_download_subpath(relpath):
    if not relpath:
        return ""
    parts = []
    for p in str(relpath).replace("\\", "/").split("/"):
        if not p or p == ".":
            continue
        if p == "..":
            if parts:
                parts.pop()
        else:
            parts.append(p)
    return "/".join(parts)


def _download_root_and_current(relpath):
    raw = get_download_path(create=True)
    if not raw:
        return None, None
    root = _vfs_dir_usable(raw)
    if not root:
        return None, None
    sub = _safe_download_subpath(relpath)
    if sub:
        current = os.path.normpath(os.path.join(root, *sub.split("/")))
    else:
        current = root
    try:
        if os.path.commonpath([root, current]) != root:
            return root, root
    except ValueError:
        return root, root
    return root, current


def _relpath_under_download_root(root, current):
    try:
        rel = os.path.relpath(current, root)
    except ValueError:
        return ""
    if rel == ".":
        return ""
    return rel.replace(os.sep, "/")


def download_folder_listing(relpath):
    xbmcplugin.setPluginCategory(ctx._handle, "Download folder")
    xbmcplugin.setContent(ctx._handle, "videos")
    is_folder = True
    root, current = _download_root_and_current(relpath)
    if not root:
        xbmcgui.Dialog().ok(
            "EasyNews",
            "Download folder is not available.\n"
            "Configure it under Add-on settings → Downloads.",
        )
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    cur_ok = _vfs_dir_usable(current)
    if cur_ok is None:
        if current != root:
            xbmcgui.Dialog().notification(
                "EasyNews", "That folder is no longer there.", xbmcgui.NOTIFICATION_INFO
            )
        current = root
    else:
        current = cur_ok
    url_sub = _relpath_under_download_root(root, current)
    try:
        dir_list, file_list = _vfs_try_listdir(current)
    except Exception:
        xbmcgui.Dialog().ok("EasyNews", "Could not read the download folder.")
        xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
        return
    if url_sub:
        parent_sub = "/".join(url_sub.split("/")[:-1])
        li = xbmcgui.ListItem(label="[COLOR yellow]..[/COLOR]")
        li.setInfo(
            "video",
            {"title": "..", "plot": "Go to the parent folder"},
        )
        parent_url = (
            ctx._url_base + "/downloads?" + urlencode({"relpath": parent_sub})
            if parent_sub
            else ctx._url_base + "/downloads"
        )
        xbmcplugin.addDirectoryItem(ctx._handle, parent_url, li, is_folder)
    for name in sorted(dir_list, key=str.lower):
        child_rel = f"{url_sub}/{name}" if url_sub else name
        li = xbmcgui.ListItem(label=name)
        li.setInfo("video", {"title": name})
        url = ctx._url_base + "/downloads?" + urlencode({"relpath": child_rel})
        xbmcplugin.addDirectoryItem(ctx._handle, url, li, is_folder)
    for name in sorted(file_list, key=str.lower):
        path = os.path.join(current, name)
        li = xbmcgui.ListItem(label=name)
        li.setInfo("video", {"title": name})
        rel_file = f"{url_sub}/{name}" if url_sub else name
        del_url = ctx.addon_base + "/downloads_delete?" + urlencode({"relpath": rel_file})
        li.addContextMenuItems([("Delete file", 'RunPlugin("{}")'.format(del_url))])
        xbmcplugin.addDirectoryItem(ctx._handle, path, li, False)
    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)


def _refresh_if_viewing_download_folder():
    folder = (xbmc.getInfoLabel("Container.FolderPath") or "").strip()
    try:
        ep = (urllib.parse.urlparse(folder).path or "").rstrip("/")
    except Exception:
        return
    if ep == "/downloads":
        xbmc.executebuiltin("Container.Refresh")


def download_delete_file(relpath):
    relpath = _safe_download_subpath(relpath or "")
    if not relpath:
        return
    raw = get_download_path(create=False)
    root = _vfs_dir_usable(raw) if raw else None
    if not root:
        xbmcgui.Dialog().ok(
            "EasyNews",
            "Download folder is not available.\n"
            "Configure it under Add-on settings → Downloads.",
        )
        return
    parts = [p for p in relpath.replace("\\", "/").split("/") if p]
    full = os.path.normpath(os.path.join(root, *parts))
    try:
        if os.path.commonpath([root, full]) != root:
            return
    except ValueError:
        return
    if os.path.isdir(full):
        return
    gone = not xbmcvfs.exists(full) and not os.path.isfile(full)
    if gone:
        xbmcgui.Dialog().notification(
            "EasyNews", "File is already gone.", xbmcgui.NOTIFICATION_INFO
        )
        _refresh_if_viewing_download_folder()
        return
    base = os.path.basename(full)
    if not xbmcgui.Dialog().yesno(
        "EasyNews",
        f"Delete this file?\n\n{base}",
    ):
        return
    try:
        if not xbmcvfs.delete(full) and os.path.isfile(full):
            os.remove(full)
    except Exception as e:
        try:
            if os.path.isfile(full):
                os.remove(full)
            else:
                xbmcgui.Dialog().ok("EasyNews", f"Could not delete file:\n{e}")
                return
        except OSError as e2:
            xbmcgui.Dialog().ok("EasyNews", f"Could not delete file:\n{e2}")
            return
    xbmcgui.Dialog().notification("EasyNews", "File deleted.", xbmcgui.NOTIFICATION_INFO)
    _refresh_if_viewing_download_folder()

def _basename_from_download_url(url):
    """Last path segment only — strip ?sig=… and other query/fragment (not part of the file name)."""
    raw = (url or "").split("|", 1)[0].strip()
    if not raw:
        return "download.bin"
    parsed = urllib.parse.urlparse(raw)
    name = os.path.basename(parsed.path or "")
    if not name:
        return "download.bin"
    return urllib.parse.unquote(name)


def _normalize_download_fetch_url(url):
    """Kodi may pass members or CDN URL; return a single https URL for requests."""
    raw = (url or "").split("|", 1)[0].strip()
    if not raw:
        return ""
    parsed = urllib.parse.urlparse(raw)
    if parsed.scheme in ("http", "https"):
        return raw
    if raw.startswith("//"):
        return "https:" + raw
    return "https://" + raw.lstrip("/")


def download_file(url):
    downloadname = _basename_from_download_url(url)
    url = _normalize_download_fetch_url(url)
    if not url:
        xbmcgui.Dialog().ok("EasyNews", "Download failed: missing URL.")
        return
    xbmc.log("{}: download_file URL: {}".format(_LOG, url), xbmc.LOGDEBUG)
    path = get_download_path()
    if not path or _vfs_dir_usable(path) is None:
        dialog = xbmcgui.Dialog()
        dialog.ok(
            "EasyNews",
            "Download folder is missing or not writable.\n"
            "Configure it under Add-on settings → Downloads.",
        )
        return
    dest = os.path.join(path, downloadname)

    class _DownloadCancelled(Exception):
        pass

    dp = xbmcgui.DialogProgress()
    dp.create("Download", "Downloading file " + downloadname)
    # urllib reporthook runs after every 8 KiB read+write. On a fast disk, those
    # callbacks can be microseconds apart while data is still coming in at wire
    # speed — per-callback db/dt measures TCP-buffer drain, not throughput.
    # Use a wall-clock window so the number matches OS/network activity monitors.
    win_seconds = 0.75
    win_t0 = time.monotonic()
    win_b0 = 0
    disp_bps = 0.0

    # Stream download with explicit short read timeout so Cancel can abort quickly.
    # Using requests here avoids urllib's blocking urlretrieve() and allows us to
    # re-check dp.iscanceled() frequently even on stalled connections.
    resp = None
    out_f = None
    try:
        resp = requests.get(
            url,
            stream=True,
            auth=HTTPBasicAuth(ctx.username, ctx.password),
            cookies=ctx.easynews_chickenlicker_cookies_dict(),
            headers={"User-Agent": "Kodi"},
            # (connect_timeout, read_timeout)
            # Read timeout is the "no bytes received" window, not overall download time.
            # Keep it reasonably high for slow links, but not infinite so Cancel still works.
            timeout=(15, 10),
        )
        resp.raise_for_status()
        try:
            total = int(resp.headers.get("Content-Length") or "0")
        except (TypeError, ValueError):
            total = 0

        out_f = open(dest, "wb")

        # Prefer reading from the underlying raw stream so we can treat read timeouts
        # as "no data yet" (and still honor Cancel quickly).
        resp.raw.decode_content = True
        downloaded = 0
        last_ui = 0.0
        chunk_size = 256 * 1024
        while True:
            if dp.iscanceled():
                raise _DownloadCancelled()
            try:
                chunk = resp.raw.read(chunk_size)
            except (requests.exceptions.ReadTimeout, socket.timeout):
                # No bytes arrived within the read-timeout window.
                # Treat as "still downloading" so slow connections don't fail.
                continue
            if not chunk:
                break
            out_f.write(chunk)
            downloaded += len(chunk)

            now = time.monotonic()
            if (now - win_t0) >= win_seconds:
                dt = now - win_t0
                db = downloaded - win_b0
                if dt >= 0.05 and db >= 0:
                    disp_bps = db / dt
                win_t0 = now
                win_b0 = downloaded

            # Throttle UI updates a little to reduce overhead.
            if (now - last_ui) >= 0.25 or (total and downloaded >= total):
                last_ui = now
                pct = int(min(100 * downloaded / total, 100)) if total > 0 else 0
                mbps = round(1e-6 * disp_bps, 2)
                dp.update(pct, f"Downloading {downloadname}\n{mbps} MB/s")

        dp.close()
        xbmcgui.Dialog().notification("EasyNews", "Download complete.", xbmcgui.NOTIFICATION_INFO, 4000)
    except _DownloadCancelled:
        try:
            dp.close()
        except Exception:
            pass
        try:
            if out_f is not None:
                out_f.close()
        except Exception:
            pass
        try:
            if xbmcvfs.exists(dest):
                xbmcvfs.delete(dest)
            elif os.path.exists(dest):
                os.remove(dest)
        except Exception:
            pass
        xbmcgui.Dialog().notification("EasyNews", "Download cancelled.", xbmcgui.NOTIFICATION_INFO, 4000)
    except requests.exceptions.HTTPError as e:
        xbmc.log("{}: download_file HTTPError: {}".format(_LOG, e), xbmc.LOGERROR)
        try:
            dp.close()
        except Exception:
            pass
        code = getattr(getattr(e, "response", None), "status_code", None)
        xbmcgui.Dialog().ok("EasyNews", "Download failed (HTTP {}).".format(code or "?"))
    except requests.exceptions.RequestException as e:
        xbmc.log("{}: download_file RequestException: {}".format(_LOG, e), xbmc.LOGERROR)
        try:
            dp.close()
        except Exception:
            pass
        xbmcgui.Dialog().ok("EasyNews", "Could not reach EasyNews.\n\n{}".format(repr(e)))
    except Exception as e:
        xbmc.log("{}: download_file error: {}".format(_LOG, e), xbmc.LOGERROR)
        try:
            dp.close()
        except Exception:
            pass
        xbmcgui.Dialog().ok("EasyNews", "Download failed.\n\n{}".format(repr(e)))
    finally:
        try:
            if resp is not None:
                resp.close()
        except Exception:
            pass
        try:
            if out_f is not None:
                out_f.close()
        except Exception:
            pass
