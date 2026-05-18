# -*- coding: utf-8 -*-
"""Merge Kodi userdata advancedsettings.xml <network> timeouts without clobbering other options."""

from __future__ import annotations

import os
import shutil
import xml.etree.ElementTree as ET

import xbmc
import xbmcvfs

# Tags this add-on may set under <network>; removing them restores Kodi built-in defaults.
_NETWORK_TIMEOUT_TAGS = frozenset({"curlclienttimeout", "curllowspeedtime"})


def advancedsettings_path() -> str:
    return xbmcvfs.translatePath("special://userdata/advancedsettings.xml")


def _ensure_network(adv: ET.Element) -> ET.Element:
    for child in adv:
        if child.tag == "network":
            return child
    return ET.SubElement(adv, "network")


def _set_child_text(parent: ET.Element, tag: str, value: int) -> None:
    s = str(int(value))
    for child in parent:
        if child.tag == tag:
            child.text = s
            return
    el = ET.SubElement(parent, tag)
    el.text = s


def merge_network_curl_settings(
    curlclienttimeout: int,
    curllowspeedtime: int,
) -> tuple[bool, str]:
    """
    Update or create <network><curlclienttimeout> and <curllowspeedtime> under
    <advancedsettings>. Preserves other root elements and other <network> children.

    Returns (ok, message_for_user).
    """
    path = advancedsettings_path()
    backup_path = path + ".easynews.bak"

    if curlclienttimeout < 5 or curlclienttimeout > 3600:
        return False, "HTTP timeout must be between 5 and 3600 seconds."
    if curllowspeedtime < 5 or curllowspeedtime > 3600:
        return False, "Low-speed time must be between 5 and 3600 seconds."

    tree = None
    root = None
    if xbmcvfs.exists(path):
        try:
            tree = ET.parse(path)
            root = tree.getroot()
        except ET.ParseError as e:
            return (
                False,
                "Your existing advancedsettings.xml is not valid XML. Fix it manually "
                "or rename it, then try again.\n\n{}".format(e),
            )
        if root is None or root.tag != "advancedsettings":
            return (
                False,
                "Your advancedsettings.xml root must be <advancedsettings>. "
                "This add-on will not modify it.",
            )
    else:
        root = ET.Element("advancedsettings")
        tree = ET.ElementTree(root)

    net = _ensure_network(root)
    _set_child_text(net, "curlclienttimeout", curlclienttimeout)
    _set_child_text(net, "curllowspeedtime", curllowspeedtime)

    try:
        if xbmcvfs.exists(path):
            shutil.copy2(path, backup_path)
    except OSError as e:
        xbmc.log(
            "plugin.video.easynewsx: could not backup advancedsettings: {}".format(e),
            xbmc.LOGWARNING,
        )

    try:
        ET.indent(tree, space="  ")
    except AttributeError:
        pass
    try:
        tree.write(path, encoding="utf-8", xml_declaration=True)
    except OSError as e:
        return False, "Could not write advancedsettings.xml:\n{}".format(e)

    return (
        True,
        "Wrote network timeouts to:\n{}\n\n"
        "Backup (if the file existed before): {}\n\n"
        "Restart Kodi for changes to take effect.".format(path, backup_path),
    )


def remove_network_curl_settings() -> tuple[bool, str]:
    """
    Remove curlclienttimeout and curllowspeedtime from <network> if present.
    Drops an empty <network> block. Deletes advancedsettings.xml if the document
    would otherwise be an empty <advancedsettings> root (so Kodi has no custom file).

    Returns (ok, message_for_user).
    """
    path = advancedsettings_path()
    backup_path = path + ".easynews.bak"

    if not xbmcvfs.exists(path):
        return (
            False,
            "No advancedsettings.xml found in your Kodi profile — nothing to remove.",
        )

    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except ET.ParseError as e:
        return (
            False,
            "Your existing advancedsettings.xml is not valid XML. Fix it manually "
            "or rename it, then try again.\n\n{}".format(e),
        )

    if root is None or root.tag != "advancedsettings":
        return (
            False,
            "Your advancedsettings.xml root must be <advancedsettings>. "
            "This add-on will not modify it.",
        )

    modified = False
    for net in list(root):
        if net.tag != "network":
            continue
        for child in list(net):
            if child.tag in _NETWORK_TIMEOUT_TAGS:
                net.remove(child)
                modified = True
        if len(list(net)) == 0:
            root.remove(net)
            modified = True

    if not modified:
        return (
            False,
            "curlclienttimeout / curllowspeedtime were not found in advancedsettings.xml. "
            "Kodi is already using its built-in defaults for those values.",
        )

    try:
        shutil.copy2(path, backup_path)
    except OSError as e:
        xbmc.log(
            "plugin.video.easynewsx: could not backup advancedsettings: {}".format(e),
            xbmc.LOGWARNING,
        )

    try:
        if len(list(root)) == 0:
            os.remove(path)
            return (
                True,
                "Removed the network timeout entries. Your profile had no other "
                "advanced settings, so advancedsettings.xml was deleted.\n\n"
                "Backup of the previous file: {}\n\n"
                "Restart Kodi to be sure defaults apply everywhere.".format(backup_path),
            )

        try:
            ET.indent(tree, space="  ")
        except AttributeError:
            pass
        tree.write(path, encoding="utf-8", xml_declaration=True)
    except OSError as e:
        return False, "Could not update advancedsettings.xml:\n{}".format(e)

    return (
        True,
        "Removed curlclienttimeout and curllowspeedtime from:\n{}\n\n"
        "Backup: {}\n\n"
        "Restart Kodi for changes to take effect.".format(path, backup_path),
    )
