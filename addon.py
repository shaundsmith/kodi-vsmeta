import os
import sys
from pathlib import Path

import xbmc
import xbmcgui
import xbmcplugin

import MediaType
import movie_actions
import param_reader
import tv_actions
from find_source_path import find_source_path
from lib import vsmeta_parser

# Actions performed by Kodi
FIND_ACTION = "find"
GET_DETAILS_ACTION = "getdetails"
GET_EPISODE_LIST_ACTION = "getepisodelist"
GET_EPISODE_DETAILS_ACTION = "getepisodedetails"


def get_file_path(title):
    """
    Returns the file path of the given media title.

    :param title: the media title

    :return: the file path to the media title, or None if the file path cannot be determined
    """
    folder_path = xbmc.getInfoLabel('Container.FolderPath')
    if os.path.exists(folder_path):
        root_directory = folder_path
    else:
        root_directory = find_source_path(title)
    return next(Path(root_directory).rglob(title + ".*" + ".vsmeta"), None) if root_directory else None


def is_tv_show(title):
    """
    Returns true if the media title is a TV show.
    This requires the initial "find" action to be performed on the media source beforehand.

    :param title: The media title

    :return: true if the item is a TV show, false otherwise
    """
    list_item = xbmcgui.ListItem(title, offscreen=True)
    media_type = list_item.getVideoInfoTag().getMediaType()
    xbmc.log(f"Media Type: {media_type}")
    return MediaType.is_tv(media_type)


def get_vsmeta_path(url):
    if not os.path.exists(url):
        return None

    if os.path.isfile(url):
        return Path(url + ".vsmeta")
    else:
        return next(Path(url).rglob("*.vsmeta"), None)


def find(title, plugin_handle):
    xbmc.log(f"Searching for title: {title}", xbmc.LOGINFO)
    file_path = get_file_path(title)
    if file_path:
        xbmc.log(f"Using path '{file_path}' for analyzing {title}", xbmc.LOGDEBUG)

        metadata = vsmeta_parser.parse(str(file_path), False)

        if metadata.is_tv_show():
            item_details = tv_actions.find(title, metadata, file_path)
        else:
            item_details = movie_actions.find(title, metadata, file_path)

        xbmcplugin.addDirectoryItem(handle=plugin_handle,
                                    url=str(item_details["url"]),
                                    listitem=item_details["list_item"],
                                    isFolder=False)
    else:
        xbmc.log(f"No vsmeta file found for {title}", xbmc.LOGWARNING)


def get_details(title, url, plugin_handle):
    xbmc.log(f"Getting details for {url}", xbmc.LOGINFO)
    file_path = get_vsmeta_path(url)
    if file_path:
        metadata = vsmeta_parser.parse(str(file_path), True)

        if metadata.is_tv_show():
            list_item = tv_actions.get_details(title, metadata, file_path) if file_path else None
        else:
            list_item = movie_actions.get_details(title, metadata, url)
        xbmcplugin.setResolvedUrl(handle=plugin_handle, succeeded=True, listitem=list_item)
    else:
        xbmc.log(f"No vsmeta file found for at {url}", xbmc.LOGWARNING)


def get_episode_list(title, url, plugin_handle):
    if os.path.exists(url):
        episodes = tv_actions.get_episode_list(title, url)
        [xbmcplugin.addDirectoryItem(plugin_handle,
                                     url=episode["url"],
                                     listitem=episode["list_item"],
                                     isFolder=True)
         for episode in episodes]
    else:
        xbmc.log(f"No vsmeta file found for {title} at {url}", xbmc.LOGWARNING)


def get_episode_details(title, url, plugin_handle):
    metadata_path = url + ".vsmeta"
    xbmc.log(f"Reading ${metadata_path}")
    if os.path.exists(metadata_path):
        list_item = tv_actions.get_episode_details(metadata_path)
        xbmcplugin.setResolvedUrl(plugin_handle, True, list_item)
    else:
        xbmc.log(f"No vsmeta file found for {title} at {url}", xbmc.LOGWARNING)
        xbmcplugin.setResolvedUrl(plugin_handle, False, xbmcgui.ListItem(offscreen=True))


def scrape(params, plugin_handle):
    """
    Scrapes the Synology Videostation VSMeta files to analyze Kodi media items.

    Movies and TV shows take slightly different flows.
    Movies use a two-stage analysis process:
        1. The "find" action is initially performed to obtain the title.
        2. The "getdetails" action is performed to obtain the movie details.
    TV Shows use a four-stage analysis process:
        1. The "find" action is initially performed to obtain the TV show title.
        2. The "getdetails" action is performed to obtain the TV show details.
        3. The "getepisodelist" action is performed on the TV show title-level to get the list of episodes.
        4. Finally, the "getepisodedetails" action is performed on each TV show episode to get the details for the episodes.

    :param params: the scraper parameters
    :param plugin_handle: the plugin handle ID
    :return: Nothing
    """
    action = params.get('action')
    url = params.get('url')
    title = params.get("title")

    if action == FIND_ACTION:
        find(title, plugin_handle)
    elif action == GET_DETAILS_ACTION:
        get_details(title, url, plugin_handle)
    elif action == GET_EPISODE_LIST_ACTION:
        get_episode_list(title, url, plugin_handle)
    elif action == GET_EPISODE_DETAILS_ACTION:
        get_episode_details(title, url, plugin_handle)
    else:
        xbmc.log(f"Unsupported action {action} provided for analyzing {title}", xbmc.LOGWARNING)

    xbmcplugin.endOfDirectory(plugin_handle)


scrape(param_reader.read(), int(sys.argv[1]))
