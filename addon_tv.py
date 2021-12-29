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

    file_path = next(Path(root_directory).rglob(title + "*" + ".vsmeta"), None)
    if file_path:
        xbmc.log("Found + " + str(file_path))
        metadata = parse(str(file_path), False)
        tv_show_directory = os.path.dirname(file_path)
        list_item = xbmcgui.ListItem(title, offscreen=True)
        list_item.setInfo("video", VideoInfoBuilder()
                          .with_field("plot", MetaDataField(metadata, "tv_data.summary"))
                          .with_field("plotoutline", MetaDataField(metadata, "tv_data.summary"))
                          .with_field("title", MetaDataField(metadata, "title"))
                          .with_field("originaltitle", MetaDataField(metadata, "title"))
                          .with_field("tvshowtitle", MetaDataField(metadata, "title"))
                          .with_field_value("mediatype", "tvshow")
                          .with_field_value("episodeguide", str(tv_show_directory))
                          .with_field("year", MetaDataField(metadata, "tv_data.year"))
                          .with_field("premiered", MetaDataField(metadata, "tv_data.release_date"))
                          .build())
        xbmcplugin.addDirectoryItem(handle=plugin_handle, url=tv_show_directory, listitem=list_item, isFolder=False)
elif action == "getdetails":
    url = params.get("url")
    file_path = next(Path(url).rglob("*.vsmeta"), None)
    tv_show_directory = os.path.dirname(file_path)
    metadata = parse(str(file_path), True)
    list_item = xbmcgui.ListItem(title, offscreen=True)
    list_item.setInfo("video", VideoInfoBuilder()
                      .with_field("plot", MetaDataField(metadata, "tv_data.summary"))
                      .with_field("plotoutline", MetaDataField(metadata, "tv_data.summary"))
                      .with_field("title", MetaDataField(metadata, "title"))
                      .with_field("originaltitle", MetaDataField(metadata, "title"))
                      .with_field("tvshowtitle", MetaDataField(metadata, "title"))
                      .with_field_value("mediatype", "tvshow")
                      .with_field_value("episodeguide", str(tv_show_directory))
                      .with_field("year", MetaDataField(metadata, "tv_data.year"))
                      .with_field("premiered", MetaDataField(metadata, "tv_data.release_date"))
                      .with_field("credits", MetaDataField(metadata, "credits.cast"))
                      .build())
    if hasattr(metadata, "tv_data") and metadata.tv_data.poster.path:
        list_item.addAvailableArtwork(str(metadata.tv_data.poster.path), "poster")
    if hasattr(metadata, "tv_data") and metadata.tv_data.backdrop.path:
        list_item.setAvailableFanart([{"image": str(metadata.tv_data.backdrop.path)}])
    xbmcplugin.setResolvedUrl(handle=plugin_handle, succeeded=True, listitem=list_item)

elif action == "getepisodelist":
    url = params.get("url")
    paths = Path(url).rglob("*.vsmeta")
    for path in paths:
        xbmc.log("Path: " + str(path) + " for " + url)
        metadata = parse(str(path), False)
        episode_path = str(os.path.splitext(path)[0])
        list_item = xbmcgui.ListItem(episode_path, offscreen=True)
        list_item.setInfo("video", VideoInfoBuilder()
                          .with_field("title", MetaDataField(metadata, "tag_line"))
                          .with_field("season", MetaDataField(metadata, "tv_data.season"))
                          .with_field("episode", MetaDataField(metadata, "tv_data.episode"))
                          .with_field_value("mediatype", "episode")
                          .with_field("aired", MetaDataField(metadata, "release_date"))
                          .build())
        xbmcplugin.addDirectoryItem(plugin_handle,
                                    url=episode_path,
                                    listitem=list_item,
                                    isFolder=True)
elif action == "getepisodedetails":
    url = params.get("url")
    metadata_path = url + ".vsmeta"
    if metadata_path:
        metadata = parse(str(metadata_path), True)
        episode_path = str(os.path.splitext(metadata_path)[0])
        list_item = xbmcgui.ListItem(episode_path, offscreen=True)
        list_item.setInfo("video", VideoInfoBuilder()
                          .with_field("title", MetaDataField(metadata, "tag_line"))
                          .with_field("season", MetaDataField(metadata, "tv_data.season"))
                          .with_field("episode", MetaDataField(metadata, "tv_data.episode"))
                          .with_field_value("mediatype", "episode")
                          .with_field("aired", MetaDataField(metadata, "release_date"))
                          .with_field("premiered", MetaDataField(metadata, "release_date"))
                          .with_field("plot", MetaDataField(metadata, "summary"))
                          .with_field("plotoutline", MetaDataField(metadata, "summary"))
                          .with_field("rating", MetaDataField(metadata, "rating"))
                          .with_field("cast", MetaDataField(metadata, "credits.cast"))
                          .with_field("director", MetaDataField(metadata, "credits.director"))
                          .with_field("mpaa", MetaDataField(metadata, "classification"))
                          .with_field("writer", MetaDataField(metadata, "credits.writer"))
                          .build())
        if metadata.poster.path:
            list_item.addAvailableArtwork(metadata.poster.path, 'thumb')
        xbmcplugin.setResolvedUrl(plugin_handle, True, list_item)
    else:
        xbmcplugin.setResolvedUrl(plugin_handle, False, xbmcgui.ListItem(offscreen=True))

xbmcplugin.endOfDirectory(plugin_handle)
