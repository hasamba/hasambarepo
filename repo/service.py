# Clean standalone service for Kodi POV IL AI Subtitles.
#
# This file is intentionally minimal. It does not install or heal the
# Kodi POV IL build tools, does not rewrite POV menus/favourites/home nodes,
# and does not touch unrelated update state. It only keeps the AI
# subtitle flow and required DarkSubs/OpenSubtitles integration alive.

import os

try:
    import xbmc
except ImportError:
    xbmc = None

ADDON_ID = 'service.subtitles.kodipovilai'
FIRST_RUN_MARKER = '.disable_on_first_run'
_subs_filename_publisher = None
TEMP_PURGE_VERSION = '2'
CACHE_RTL_FIX_VERSION = '4'


def _check_first_run_marker():
    if xbmc is None:
        return False
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        marker = os.path.join(here, FIRST_RUN_MARKER)
        if not os.path.isfile(marker):
            return False
        try:
            os.remove(marker)
        except OSError:
            pass
        try:
            import json as _json
            xbmc.executeJSONRPC(_json.dumps({
                'jsonrpc': '2.0',
                'id': 1,
                'method': 'Addons.SetAddonEnabled',
                'params': {'addonid': ADDON_ID, 'enabled': False},
            }))
        except Exception:
            try:
                xbmc.executebuiltin('DisableAddon(' + ADDON_ID + ')')
            except Exception:
                pass
        return True
    except Exception:
        return False


def _prune_once():
    try:
        from resources.lib import cache, kodi_utils
        removed, freed = cache.prune()
        if removed:
            kodi_utils.log(
                'Cache prune: {0} files removed, {1:.1f} MB freed'.format(
                    removed, freed / (1024.0 * 1024.0)),
                level='INFO')
        else:
            kodi_utils.log('Cache prune: nothing to remove', level='DEBUG')
    except Exception:
        pass


def _maybe_purge_temp_once():
    try:
        from resources.lib import kodi_utils
    except Exception:
        return
    try:
        if kodi_utils.get_setting('_temp_purge_done', '') == TEMP_PURGE_VERSION:
            return
        temp_dir = kodi_utils.translate_path('special://temp/')
        if temp_dir and os.path.isdir(temp_dir):
            for fn in os.listdir(temp_dir):
                if fn.lower().endswith(('.srt', '.sub', '.ass', '.ssa', '.vtt')):
                    try:
                        os.remove(os.path.join(temp_dir, fn))
                    except OSError:
                        pass
        kodi_utils.set_setting('_temp_purge_done', TEMP_PURGE_VERSION)
    except Exception:
        pass


def _maybe_repair_rtl_cache():
    try:
        from resources.lib import kodi_utils, srt
    except Exception:
        return
    try:
        if kodi_utils.get_setting('_rtl_fix_done', '') == CACHE_RTL_FIX_VERSION:
            return
        translated_dir = os.path.join(kodi_utils.cache_dir(), 'translated')
        if os.path.isdir(translated_dir):
            for fn in os.listdir(translated_dir):
                if not fn.endswith('.srt'):
                    continue
                p = os.path.join(translated_dir, fn)
                try:
                    with open(p, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                    fixed = srt.fix_rtl_punctuation(content)
                    if fixed != content:
                        tmp = p + '.aitmp'
                        with open(tmp, 'w', encoding='utf-8') as f:
                            f.write(fixed)
                        os.replace(tmp, p)
                except OSError:
                    pass
        kodi_utils.set_setting('_rtl_fix_done', CACHE_RTL_FIX_VERSION)
    except Exception:
        pass


def _maybe_default_fast_first_chunk():
    try:
        from resources.lib import kodi_utils
        if kodi_utils.get_setting('_fast_first_chunk_default_done', '') == '1':
            return
        if kodi_utils.get_setting('fast_first_chunk', '') in ('', 'false'):
            kodi_utils.set_setting('fast_first_chunk', 'true')
        kodi_utils.set_setting('_fast_first_chunk_default_done', '1')
    except Exception:
        pass


def _run(label, func):
    try:
        func()
    except Exception as e:
        try:
            from resources.lib import kodi_utils
            kodi_utils.log('{0} failed: {1}'.format(label, e), level='WARNING')
        except Exception:
            pass


def _maybe_patch_darksubs():
    from resources.lib import dark_subs_integration
    dark_subs_integration.maybe_patch_darksubs()


def _maybe_patch_darksubs_download_sub():
    from resources.lib import darksubs_download_sub_patcher
    darksubs_download_sub_patcher.ensure_patched()


def _maybe_patch_darksubs_opensubtitles():
    from resources.lib import darksubs_opensubtitles_patcher
    darksubs_opensubtitles_patcher.ensure_patched()


def _maybe_patch_darksubs_embedded_demote():
    from resources.lib import darksubs_embedded_demote_patcher
    status = darksubs_embedded_demote_patcher.ensure_patched()
    if status == 'patched':
        from resources.lib import darksubs_reload
        darksubs_reload.note_patched()


def _maybe_patch_darksubs_embedded_insert():
    from resources.lib import darksubs_embedded_insert_patcher
    status = darksubs_embedded_insert_patcher.ensure_patched()
    if status == 'patched':
        from resources.lib import darksubs_reload
        darksubs_reload.note_patched()


def _maybe_patch_darksubs_subwindow_demote():
    from resources.lib import darksubs_subwindow_demote_patcher
    status = darksubs_subwindow_demote_patcher.ensure_patched()
    if status == 'patched':
        from resources.lib import darksubs_reload
        darksubs_reload.note_patched()


def _maybe_surface_darksubs_status():
    from resources.lib import darksubs_hook_diagnostics
    darksubs_hook_diagnostics.surface_status_if_problem()


def _maybe_patch_darksubs_filename():
    from resources.lib import darksubs_filename_fallback_patcher
    darksubs_filename_fallback_patcher.ensure_patched()


def _maybe_patch_skin_dialog_subtitles():
    from resources.lib import skin_dialog_subtitles_patcher
    skin_dialog_subtitles_patcher.ensure_patched()


def _maybe_patch_skin_dialog_subtitles_rows():
    from resources.lib import skin_dialog_subtitles_row_patcher
    skin_dialog_subtitles_row_patcher.ensure_patched()


def _maybe_patch_darksubs_picker_label():
    from resources.lib import darksubs_picker_label_patcher
    darksubs_picker_label_patcher.ensure_patched()


def _maybe_patch_darksubs_picker_height():
    from resources.lib import darksubs_picker_height_patcher
    darksubs_picker_height_patcher.ensure_patched()


def _maybe_patch_all_subs_samefile():
    from resources.lib import all_subs_samefile_patcher
    all_subs_samefile_patcher.ensure_patched()


def main():
    if xbmc is None:
        return
    if _check_first_run_marker():
        return

    _prune_once()
    _maybe_purge_temp_once()

    _run('darksubs integration', _maybe_patch_darksubs)
    _run('darksubs download_sub patch', _maybe_patch_darksubs_download_sub)
    _run('darksubs OpenSubtitles patch', _maybe_patch_darksubs_opensubtitles)
    _run('darksubs embedded demote patch', _maybe_patch_darksubs_embedded_demote)
    _run('darksubs embedded insert patch', _maybe_patch_darksubs_embedded_insert)
    _run('darksubs subwindow demote patch', _maybe_patch_darksubs_subwindow_demote)
    _run('darksubs status diagnostics', _maybe_surface_darksubs_status)
    _run('darksubs filename fallback patch', _maybe_patch_darksubs_filename)
    _run('subtitle dialog filename patch', _maybe_patch_skin_dialog_subtitles)
    _run('subtitle dialog row patch', _maybe_patch_skin_dialog_subtitles_rows)
    _run('darksubs picker label patch', _maybe_patch_darksubs_picker_label)
    _run('darksubs picker height patch', _maybe_patch_darksubs_picker_height)
    _run('allsubs samefile patch', _maybe_patch_all_subs_samefile)

    try:
        from resources.lib import darksubs_reload
        darksubs_reload.reload_if_patched()
    except Exception:
        pass

    _maybe_repair_rtl_cache()
    _maybe_default_fast_first_chunk()

    global _subs_filename_publisher
    try:
        from resources.lib import subs_filename_publisher
        _subs_filename_publisher = subs_filename_publisher.SubsFilenamePublisher()
    except Exception:
        pass

    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        if monitor.waitForAbort(24 * 3600):
            break
        _prune_once()


main()
