# Module: main
# Author: Roman V. M.
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
"""
EasyNews video plugin for Kodi 19+ (Matrix and above).
"""
import os
import sys
import platform
import struct

ADDON_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(ADDON_DIR, "resources", "lib")
if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)

import xbmc
import xbmcaddon

def _tail_path(p, parts=3):
    try:
        if not p:
            return "unknown"
        p2 = p.replace("\\", "/").rstrip("/")
        segs = [s for s in p2.split("/") if s]
        return "/".join(segs[-parts:]) if segs else "unknown"
    except Exception:
        return "unknown"


def _get_module_version(module_name, attr="__version__"):
    try:
        mod = __import__(module_name)
    except Exception:
        return "missing"
    try:
        v = getattr(mod, attr, None)
        return v if v else "unknown"
    except Exception:
        return "unknown"


def _get_module_file(module_name):
    try:
        mod = __import__(module_name)
    except Exception:
        return "missing"
    try:
        p = getattr(mod, "__file__", None)
        return p if p else "unknown"
    except Exception:
        return "unknown"


def _get_env_diagnostics():
    bits = struct.calcsize("P") * 8
    system = platform.system() or "unknown"
    release = platform.release() or "unknown"
    machine = platform.machine() or "unknown"
    try:
        py_info = "{}.{}.{}".format(*sys.version_info[:3])
    except Exception:
        py_info = "unknown"
    try:
        _ = tuple[int]  # noqa: F841
        tuple_subscript_ok = True
    except Exception:
        tuple_subscript_ok = False
    try:
        py_impl = platform.python_implementation() or "unknown"
    except Exception:
        py_impl = "unknown"
    try:
        py_exe = sys.executable or "unknown"
    except Exception:
        py_exe = "unknown"
    try:
        tuple_type = type(tuple).__name__
    except Exception:
        tuple_type = "unknown"
    try:
        tuple_repr = repr(tuple)
        tuple_repr = tuple_repr[:120] + ("…" if len(tuple_repr) > 120 else "")
    except Exception:
        tuple_repr = "unknown"
    return {
        "os": f"{system} {release}",
        "arch": machine,
        "bits": bits,
        "py_info": py_info,
        "py_impl": py_impl,
        "py_executable": py_exe,
        "tuple_subscript_ok": tuple_subscript_ok,
        "tuple_type": tuple_type,
        "tuple_repr": tuple_repr,
        "deps": {
            "requests": _get_module_version("requests"),
            "urllib3": _get_module_version("urllib3"),
            "certifi": _get_module_version("certifi"),
        },
        "dep_files": {
            "requests": _get_module_file("requests"),
            "urllib3": _get_module_file("urllib3"),
            "certifi": _get_module_file("certifi"),
        },
    }


_addon = xbmcaddon.Addon()
_env = _get_env_diagnostics()
xbmc.log(
    "plugin.video.easynewsx: easynews diagnostic version={} kodi={} python={} py_info={} py_impl={} py_exe_tail={} addon_path_tail={} profile_tail={} tuple_subscript_ok={} tuple_type={} tuple_repr={} os={} arch={} bits={} deps=requests:{} urllib3:{} certifi:{} dep_files_tail=requests:{} urllib3:{} certifi:{}".format(
        _addon.getAddonInfo("version"),
        xbmc.getInfoLabel("System.BuildVersion"),
        sys.version.split()[0],
        _env["py_info"],
        _env["py_impl"],
        _tail_path(_env["py_executable"], parts=2),
        _tail_path(_addon.getAddonInfo("path"), parts=4),
        _tail_path(_addon.getAddonInfo("profile"), parts=4),
        _env["tuple_subscript_ok"],
        _env["tuple_type"],
        _env["tuple_repr"],
        _env["os"],
        _env["arch"],
        _env["bits"],
        _env["deps"]["requests"],
        _env["deps"]["urllib3"],
        _env["deps"]["certifi"],
        _tail_path(_env["dep_files"]["requests"], parts=3),
        _tail_path(_env["dep_files"]["urllib3"], parts=3),
        _tail_path(_env["dep_files"]["certifi"], parts=3),
    ),
    xbmc.LOGINFO,
)

from resources.lib.easynews.context import init_context

init_context()

from resources.lib.easynews.router import router


if __name__ == "__main__":
    xbmc.log(
        "plugin.video.easynewsx: argv: {}".format(sys.argv),
        xbmc.LOGDEBUG,
    )
    router(sys.argv[2][1:])
    from resources.lib.easynews import applog

    applog.join_startup_ping(timeout=0.5)
