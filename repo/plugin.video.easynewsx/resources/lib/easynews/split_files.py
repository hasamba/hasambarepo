# -*- coding: utf-8 -*-
"""Split RAR/001 multi-part download and join."""
import os
import time

import requests
from requests.auth import HTTPBasicAuth
import xbmc
import xbmcgui

from resources.lib.easynews import api
from resources.lib.easynews import context as ctx
from resources.lib.easynews import downloads

_LOG = "plugin.video.easynewsx"


def find_split_files(video_filename, newsgroup):
    files = []
    query = video_filename
    query = query.replace(" ", "+")
    page = 1
    total_size = 0
    # get the 001 file first, which easynews recognises as a VIDEO file type
    try:
        video_data, results, page = api.get_easynews_results(query, newsgroup, page, "VIDEO", 100)
    except api.EasynewsSearchFailed as e:
        xbmcgui.Dialog().ok("EasyNews", e.reason)
        return

    if results == 0:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok("No 001 file found", f"{video_filename}\nCouldn't find 001 file matching this filename, sorry!")
        return

    filename = video_data[0]["video"].rsplit("/", 1)[-1]
    vd = {
        "filename": filename,
        "url": video_data[0]["video"],
        "rawsize": video_data[0]["rawsize"],
    }
    files.append(vd)
    total_size += video_data[0]["rawsize"]

    # now get remaining archive / split files 002, 003, ...
    try:
        video_data, results, page = api.get_easynews_results(query, newsgroup, page, "ARCHIVE", 100)
    except api.EasynewsSearchFailed as e:
        xbmcgui.Dialog().ok("EasyNews", e.reason)
        return

    if results == 0:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok("No split files found",
                       f"{video_filename}\nCouldn't find any split files matching this filename, sorry!")
        return

    for video in video_data:
        filename = video["video"].rsplit("/", 1)[-1]
        vd = {
            "filename": filename,
            "url": video["video"],
            "rawsize": video["rawsize"],
        }
        total_size += video["rawsize"]
        files.append(vd)
    total_size = int(total_size / 1000000)
    files.sort(key=lambda x: x["filename"])
    files = remove_item_by_key(files, "filename",
                               video_filename + ".000")  # dont need the 000 file as it corrupts header
    dialog = xbmcgui.Dialog()
    message = "Do you want to download and join these files?\n"
    for file in files:
        message += file["filename"] + "\n"
    user_input = dialog.yesno(f"Download and join {len(files)} split files total {total_size}Mb", message)

    if user_input:
        save_directory = downloads.get_download_path()
        if not save_directory or downloads._vfs_dir_usable(save_directory) is None:
            xbmcgui.Dialog().ok(
                "EasyNews",
                "Download folder is missing or not writable.\n"
                "Set it in Add-on settings → Downloads.",
            )
            return
        progress = xbmcgui.DialogProgress()
        progress.create(f"Downloading {len(files)} Split Files Total {total_size}Mb", "downloading starting")
        counter = 0
        start_time = time.time()
        chunk_count = 0
        for file in files:
            initial_url = file["url"]
            filename = os.path.join(save_directory, file["filename"])
            response = requests.get(
                initial_url,
                auth=HTTPBasicAuth(ctx.username, ctx.password),
                stream=True,
                cookies=ctx.easynews_chickenlicker_cookies_dict(),
            )
            streaming_url = response.url
            counter += 1

            if progress.iscanceled():
                break

            filesize = int(response.headers["Content-Length"])

            chunk_size = 5000000
            try:
                with open(filename, "wb") as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if progress.iscanceled():
                            break
                        if chunk:
                            f.write(chunk)
                            chunk_count += 1
                            chunk_total = chunk_size * chunk_count
                            elapsed_time = time.time() - start_time
                            progress.update(int(100 * counter / len(files)),
                                            f"Downloading file {counter} of {len(files)}\n"
                                            f"{file['filename']}\n"
                                            f"{round(0.000001 * chunk_total / elapsed_time, 2)} MBps")
            except IOError as e:

                error_number = e.errno if hasattr(e, 'errno') else None
                dialog = xbmcgui.Dialog()
                msg = f"An error has occured: {e}"
                if error_number == 30:
                    msg += "\nCheck Add-on settings → Downloads for a valid folder."
                ok = dialog.ok("Error writing file",
                               msg)
                xbmc.log(
                    "{}: split download write error: {}".format(_LOG, e),
                    xbmc.LOGERROR,
                )
                break
        do_the_join = not progress.iscanceled()
        progress.close()
        if do_the_join:
            progress.create(f"Joining {len(files)} Archive Files", "process starting")
            join_split_files(files, video_filename, save_directory)
            progress.close()
        else:
            for file in files:
                filename = os.path.join(save_directory, file["filename"])
                if os.path.exists(filename):
                    # Delete the file
                    os.remove(filename)


def join_split_files(files, output_filename, directory):
    with open(os.path.join(directory, output_filename), 'wb') as output_file:
        for file in files:
            part_filename = os.path.join(directory, file["filename"])
            with open(part_filename, 'rb') as part_file:
                output_file.write(part_file.read())
            os.remove(part_filename)


def remove_item_by_key(input_list, key_to_remove, value_to_match):
    return [item for item in input_list if item.get(key_to_remove) != value_to_match]

