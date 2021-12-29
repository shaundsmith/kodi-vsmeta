import os.path

import xbmcgui

import MediaType
import get_set_information
from VideoInfoBuilder import MetaDataField, VideoInfoBuilder
from lib import vsmeta_parser


def find(title, metadata, file_path):
    movie_path = str(os.path.splitext(file_path)[0])
    list_item = xbmcgui.ListItem(title, offscreen=True)
    list_item.setInfo("video", VideoInfoBuilder()
                      .with_field("genre", MetaDataField(metadata, "credits.genre"))
                      .with_field("year", MetaDataField(metadata, "year"))
                      .with_field("rating", MetaDataField(metadata, "rating"))
                      .with_field("title", MetaDataField(metadata, "title"))
                      .with_field_value("mediatype", MediaType.MOVIE)
                      .build())
    return {
        "list_item": list_item,
        "url": movie_path
    }


def get_details(title, metadata, url):
    set_information = get_set_information.get(url, vsmeta_parser.DEFAULT_IMAGE_DIRECTORY)

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
                      .with_field("set", MetaDataField(set_information, "title"))
                      .with_field("setoverview", MetaDataField(set_information, "summary"))
                      .with_field("sorttitle", MetaDataField(set_information, "sort_title"))
                      .with_field_value("mediatype", MediaType.MOVIE)
                      .build())

    if metadata.poster.path:
        list_item.addAvailableArtwork(str(metadata.poster.path), "poster")
    if metadata.backdrop.path:
        list_item.setAvailableFanart([{"image": str(metadata.backdrop.path)}])
    if hasattr(set_information, "fanart"):
        list_item.addAvailableArtwork(set_information.fanart, "set.fanart")
    if hasattr(set_information, "poster"):
        list_item.addAvailableArtwork(set_information.poster, "set.poster")

    return list_item
