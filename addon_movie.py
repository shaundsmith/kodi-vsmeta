import os
import sys
import urllib.parse
from pathlib import Path

import xbmc
import xbmcgui
import xbmcplugin

from VideoInfoBuilder import VideoInfoBuilder, MetaDataField
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

if action == "find":
    folder_path = xbmc.getInfoLabel('Container.FolderPath')
    if os.path.exists(folder_path):
        root_directory = folder_path
    else:
        root_directory = find_source_path(title)
    file_path = next(Path(root_directory).rglob(title + ".*" + ".vsmeta"), None)
    if file_path:
        metadata = parse(str(file_path), False)
        list_item = xbmcgui.ListItem(title, offscreen=True)
        list_item.setInfo("video", VideoInfoBuilder()
                          .with_field("genre", MetaDataField(metadata, "credits.genre"))
                          .with_field("year", MetaDataField(metadata, "year"))
                          .with_field("rating", MetaDataField(metadata, "rating"))
                          .with_field("title", MetaDataField(metadata, "title"))
                          .build())
        xbmcplugin.addDirectoryItem(handle=plugin_handle, url=str(file_path), listitem=list_item, isFolder=False)
elif action == "getdetails":
    url = params.get("url")

    metadata = parse(url, True)

    list_item = xbmcgui.ListItem(title, offscreen=True)
    list_item.setInfo("video", VideoInfoBuilder()
                      .with_field("genre", MetaDataField(metadata, "credits.genre"))
                      .with_field("year", MetaDataField(metadata, "year"))
                      .with_field("rating", MetaDataField(metadata, "rating"))
                      .with_field("cast", MetaDataField(metadata, "credits.cast"))
                      .with_field("director", MetaDataField(metadata, "credits.director"))
                      .with_field("mpaa", MetaDataField(metadata, "classification"))
                      .with_field("plot", MetaDataField(metadata, "summary"))
                      .with_field("plotoutline", MetaDataField(metadata, "summary"))
                      .with_field("title", MetaDataField(metadata, "title"))
                      .with_field("tagline", MetaDataField(metadata, "tag_line"))
                      .with_field("writer", MetaDataField(metadata, "credits.writer"))
                      .build())

    if metadata.poster.path:
        list_item.addAvailableArtwork(str(metadata.poster.path), "poster")
    if metadata.backdrop.path:
        list_item.setAvailableFanart([{"image": str(metadata.backdrop.path)}])

    xbmcplugin.setResolvedUrl(handle=plugin_handle, succeeded=True, listitem=list_item)

xbmcplugin.endOfDirectory(plugin_handle)
