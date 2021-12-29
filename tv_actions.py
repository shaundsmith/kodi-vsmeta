import os
from pathlib import Path

import xbmc
import xbmcgui

import MediaType
from VideoInfoBuilder import VideoInfoBuilder, MetaDataField
from lib import vsmeta_parser


def find(title, metadata, file_path):
    tv_show_directory = str(os.path.dirname(file_path))
    list_item = xbmcgui.ListItem(title, offscreen=True)
    list_item.setInfo("video", VideoInfoBuilder()
                      .with_field("plot", MetaDataField(metadata, "tv_data.summary"))
                      .with_field("plotoutline", MetaDataField(metadata, "tv_data.summary"))
                      .with_field("title", MetaDataField(metadata, "title"))
                      .with_field("originaltitle", MetaDataField(metadata, "title"))
                      .with_field("tvshowtitle", MetaDataField(metadata, "title"))
                      .with_field_value("mediatype", MediaType.TV_SHOW)
                      .with_field_value("episodeguide", tv_show_directory)
                      .with_field("year", MetaDataField(metadata, "tv_data.year"))
                      .with_field("premiered", MetaDataField(metadata, "tv_data.release_date"))
                      .build())

    return {
        "list_item": list_item,
        "url": tv_show_directory
    }


def get_details(title, metadata, file_path):
    tv_show_directory = str(os.path.dirname(file_path))
    list_item = xbmcgui.ListItem(title, offscreen=True)
    list_item.setInfo("video", VideoInfoBuilder()
                      .with_field("plot", MetaDataField(metadata, "tv_data.summary"))
                      .with_field("plotoutline", MetaDataField(metadata, "tv_data.summary"))
                      .with_field("title", MetaDataField(metadata, "title"))
                      .with_field("originaltitle", MetaDataField(metadata, "title"))
                      .with_field("tvshowtitle", MetaDataField(metadata, "title"))
                      .with_field_value("mediatype", MediaType.TV_SHOW)
                      .with_field_value("episodeguide", tv_show_directory)
                      .with_field("year", MetaDataField(metadata, "tv_data.year"))
                      .with_field("premiered", MetaDataField(metadata, "tv_data.release_date"))
                      .with_field("credits", MetaDataField(metadata, "credits.cast"))
                      .with_field("genre", MetaDataField(metadata, "credits.genre"))
                      .build())
    if hasattr(metadata, "tv_data") and metadata.tv_data.poster.path:
        list_item.addAvailableArtwork(str(metadata.tv_data.poster.path), "poster")
    if hasattr(metadata, "tv_data") and metadata.tv_data.backdrop.path:
        list_item.setAvailableFanart([{"image": str(metadata.tv_data.backdrop.path)}])

    return list_item


def get_episode_list(title, url):
    paths = Path(url).rglob("*.vsmeta")
    episodes = []
    for path in paths:
        xbmc.log(f"Getting episode details for {title} in {path}", xbmc.LOGINFO)
        metadata = vsmeta_parser.parse(str(path), False)
        episode_path = str(os.path.splitext(path)[0])
        list_item = xbmcgui.ListItem(episode_path, offscreen=True)
        list_item.setInfo("video", VideoInfoBuilder()
                          .with_field("title", MetaDataField(metadata, "tag_line"))
                          .with_field("season", MetaDataField(metadata, "tv_data.season"))
                          .with_field("episode", MetaDataField(metadata, "tv_data.episode"))
                          .with_field_value("mediatype", MediaType.TV_EPISODE)
                          .with_field("aired", MetaDataField(metadata, "release_date"))
                          .build())
        episodes.append({
            "list_item": list_item,
            "url": episode_path
        })
    return episodes


def get_episode_details(url):
    metadata = vsmeta_parser.parse(url, True)
    episode_path = str(os.path.splitext(url)[0])
    list_item = xbmcgui.ListItem(episode_path, offscreen=True)
    list_item.setInfo("video", VideoInfoBuilder()
                      .with_field("title", MetaDataField(metadata, "tag_line"))
                      .with_field("season", MetaDataField(metadata, "tv_data.season"))
                      .with_field("episode", MetaDataField(metadata, "tv_data.episode"))
                      .with_field_value("mediatype", MediaType.TV_EPISODE)
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

    return list_item
