import os
import sys
import urllib.parse
from pathlib import Path

import xbmc
import xbmcgui
import xbmcplugin

from find_source_path import find_source_path
from lib.vsmeta_parser import parse


def get_params():
    param_string = sys.argv[2][1:]
    if param_string:
        return dict(urllib.parse.parse_qsl(param_string))
    return {}


xbmc.log(str(sys.argv))
params = get_params()
plugin_handle = int(sys.argv[1])
action = params.get('action')
title = params.get("title")
file_path = ""


item = xbmcgui.ListItem(title, offscreen=True)
print(item.getPath())

if action == "find":
    folder_path = xbmc.getInfoLabel('Container.FolderPath')
    if os.path.exists(folder_path):
        root_directory = folder_path
    else:
        root_directory = find_source_path(title)
    for path in Path(root_directory).rglob(title + "*" + ".vsmeta"):
        file_path = str(path)
    if file_path:
        metadata = parse(file_path, False)
        list_item = xbmcgui.ListItem(title, offscreen=True)
        list_item.setInfo("video",
                          {
                        "genre": metadata.credits.genre,
                        "year": metadata.year,
                        "rating": metadata.rating,
                        "title": metadata.title

                    })
        xbmcplugin.addDirectoryItem(handle=plugin_handle, url=file_path, listitem=list_item, isFolder=False)
elif action == "getdetails":
    url = params.get("url")
    xbmc.log("Url:" + url)
    metadata = parse(url, True)
    list_item = xbmcgui.ListItem(title, offscreen=True)
    list_item.setInfo("video",
                      {
                    "genre": metadata.credits.genre,
                    "year": metadata.year,
                    "rating": metadata.rating,
                    "cast": metadata.credits.cast,
                    "director": metadata.credits.director,
                    "mpaa": metadata.classification,
                    "plot": metadata.summary,
                    "plotoutline": metadata.summary,
                    "title": metadata.title,
                    "tagline": metadata.tag_line,
                    "writer": metadata.credits.writer
                })
    list_item.addAvailableArtwork(str(metadata.poster.path), "poster")
    list_item.setAvailableFanart([{"image": str(metadata.backdrop.path)}])
    xbmcplugin.setResolvedUrl(handle=plugin_handle, succeeded=True, listitem=list_item)

xbmcplugin.endOfDirectory(plugin_handle)
