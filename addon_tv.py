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

xbmc.log("Action: " + action)
if action == "find":
    folder_path = xbmc.getInfoLabel('Container.FolderPath')
    if os.path.exists(folder_path):
        root_directory = folder_path
    else:
        root_directory = find_source_path(title)

    file_path = next(Path(root_directory).rglob(title + "*" + ".vsmeta"), None)
    if file_path:
        metadata = parse(str(file_path), False)
        tv_show_directory = os.path.dirname(file_path)
        list_item = xbmcgui.ListItem(title, offscreen=True)
        list_item.setInfo("video",
                          {
                              "plot": metadata.tv_data.summary,
                              "plotoutline": metadata.tv_data.summary,
                              "title": metadata.title,
                              "originaltitle": metadata.title,
                              "tvshowtitle": metadata.title,
                              "mediatype": "tvshow",
                              "episodeguide": tv_show_directory,
                              "year": metadata.tv_data.year,
                              "premiered": str(metadata.tv_data.release_date)
                          })
        xbmcplugin.addDirectoryItem(handle=plugin_handle, url=tv_show_directory, listitem=list_item, isFolder=False)
elif action == "getdetails":
    url = params.get("url")
    file_path = next(Path(url).rglob("*.vsmeta"), None)
    tv_show_directory = os.path.dirname(file_path)
    metadata = parse(str(file_path), True)
    list_item = xbmcgui.ListItem(title, offscreen=True)
    list_item.setInfo("video",
                      {
                          "plot": metadata.tv_data.summary,
                          "plotoutline": metadata.tv_data.summary,
                          "title": metadata.title,
                          "originaltitle": metadata.title,
                          "tvshowtitle": metadata.title,
                          "mediatype": "tvshow",
                          "episodeguide": tv_show_directory,
                          "year": metadata.tv_data.year,
                          "premiered": str(metadata.tv_data.release_date),
                          "credits": metadata.credits.cast
                      })
    list_item.addAvailableArtwork(str(metadata.tv_data.poster.path), "poster")
    list_item.setAvailableFanart([{"image": str(metadata.tv_data.backdrop.path)}])
    xbmcplugin.setResolvedUrl(handle=plugin_handle, succeeded=True, listitem=list_item)

elif action == "getepisodelist":
    # Scan directory
    url = params.get("url")
    paths = Path(url).rglob("*.vsmeta")
    for path in paths:
        xbmc.log("Path: " + str(path) + " for " + url)
        metadata = parse(str(path), False)
        episode_path = str(os.path.splitext(path)[0])
        list_item = xbmcgui.ListItem(episode_path, offscreen=True)
        video = {
            "title": metadata.tag_line,
            "season": metadata.tv_data.season,
            "episode": metadata.tv_data.episode,
            "mediatype": "episode",
            "aired": str(metadata.release_date),
        }
        xbmc.log("Found " + str(video) + " for " + str(episode_path))
        list_item.setInfo("video", video)
        xbmcplugin.addDirectoryItem(plugin_handle,
                                    url=episode_path,
                                    listitem=list_item,
                                    isFolder=True)
elif action == "getepisodedetails":
    url = params.get("url")
    metadata_path = url + ".vsmeta"
    if metadata_path:
        metadata = parse(str(metadata_path), False)
        episode_path = str(os.path.splitext(metadata_path)[0])
        list_item = xbmcgui.ListItem(episode_path, offscreen=True)
        video = {
            "title": metadata.tag_line,
            "season": metadata.tv_data.season,
            "episode": metadata.tv_data.episode,
            "mediatype": "episode",
            "aired": str(metadata.release_date),
            "premiered": str(metadata.release_date),
            "plot": metadata.summary,
            "plotoutline": metadata.summary,
            "rating": metadata.rating,
            "cast": metadata.credits.cast,
            "director": metadata.credits.director,
            "mpaa": metadata.classification,
            "writer": metadata.credits.writer
        }
        list_item.setInfo("video", video)
        xbmcplugin.setResolvedUrl(plugin_handle, True, list_item)
    else:
        xbmcplugin.setResolvedUrl(HANDLE, False, xbmcgui.ListItem(offscreen=True))


xbmcplugin.endOfDirectory(plugin_handle)
