# -*- coding: utf-8 -*-
"""Recently played streams (rolling 10)."""
import urllib.parse
from urllib.parse import urlencode

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.easynews import api
from resources.lib.easynews import context as ctx
from resources.lib.easynews import vlc as vlc_launcher


def _newsgroups_string(entry):
    """Space-separated newsgroups from stored field or legacy plot (first block before \\n\\n)."""
    ng = entry.get("newsgroups")
    if isinstance(ng, str) and ng.strip():
        return ng.strip()
    plot = entry.get("plot") or ""
    if "\n\n" in plot:
        first = plot.split("\n\n", 1)[0].strip()
        if first:
            return first
    return ""


def _refresh_listing():
    folder = (xbmc.getInfoLabel("Container.FolderPath") or "").strip()
    if not folder:
        return
    try:
        ep = (urllib.parse.urlparse(folder).path or "").rstrip("/")
    except Exception:
        return
    if ep != "/playhistory":
        return
    xbmc.executebuiltin("Container.Refresh")


def play_history_menu(action, video_remove):
    xbmcplugin.setPluginCategory(ctx._handle, ctx.addon.getLocalizedString(33037))
    xbmcplugin.setContent(ctx._handle, "videos")

    if action == "remove":
        ctx.play_history.remove(video_remove)
        _refresh_listing()
        return
    if action == "clear":
        ctx.play_history.clear()
        _refresh_listing()
        return

    history = ctx.play_history.get()
    listed = 0
    for k in sorted(list(history), reverse=True):
        entry = history[k]
        if not isinstance(entry, dict):
            continue
        title = entry.get("title")
        video = entry.get("video")
        if not video:
            continue
        listed += 1
        label = title or video
        li = xbmcgui.ListItem(label=label)
        plot = entry.get("plot") or video
        plot = api.append_duration_to_plot(plot, entry.get("runtime"))
        vinfo = {"title": label, "plot": plot, "mediatype": "video"}
        if entry.get("runtime") is not None:
            try:
                vinfo["duration"] = int(entry["runtime"])
            except (TypeError, ValueError):
                pass
        li.setInfo("video", vinfo)
        li.setProperty("IsPlayable", "true")
        li.setProperty("ResumeTime", "0")
        li.setProperty("TotalTime", "0")
        thumb = entry.get("thumb") or api.easynews_thumbnail_url_from_dl_url(video)
        if thumb:
            li.setArt({"thumb": thumb, "icon": thumb})
        play_params = {"video": video, "title": label}
        if thumb:
            play_params["thumb"] = thumb
        if plot:
            play_params["plot"] = plot
        if entry.get("runtime") is not None:
            play_params["runtime"] = str(entry["runtime"])
        ng_str = _newsgroups_string(entry)
        if ng_str:
            play_params["newsgroups"] = ng_str
        remove_action = ctx.addon_base + "/playhistory?" + urlencode({"action": "remove", "video": video})
        clear_action = ctx.addon_base + "/playhistory?" + urlencode({"action": "clear"})
        context_actions = [
            (ctx.addon.getLocalizedString(33034), "RunPlugin({})".format(remove_action)),
            (ctx.addon.getLocalizedString(33035), "RunPlugin({})".format(clear_action)),
        ]
        if vlc_launcher.vlc_is_installed():
            vlc_params = dict(play_params)
            vlc_action = ctx.addon_base + "/vlc_resolved?" + urlencode(vlc_params)
            context_actions.append(("Open in VLC (experimental)", 'RunPlugin("{}")'.format(vlc_action)))
        for ng in ng_str.split():
            if not ng:
                continue
            add_url = ctx.addon_base + "/browse?" + urlencode({"action": "add", "query": ng})
            context_actions.append(
                ("Add {}".format(api.ng_condense(ng)), 'RunPlugin("{}")'.format(add_url)),
            )
        li.addContextMenuItems(context_actions)
        play_url = ctx._url_base + "/play?" + urlencode(play_params)
        xbmcplugin.addDirectoryItem(ctx._handle, play_url, li, False)

    if listed == 0:
        li = xbmcgui.ListItem(
            label="[COLOR gray]{}[/COLOR]".format(ctx.addon.getLocalizedString(33038))
        )
        li.setInfo("video", {"plot": ctx.addon.getLocalizedString(33039)})
        li.setProperty("IsPlayable", "false")
        url = ctx._url_base + "/playhistory"
        xbmcplugin.addDirectoryItem(ctx._handle, url, li, False)

    xbmcplugin.endOfDirectory(ctx._handle, cacheToDisc=False)
