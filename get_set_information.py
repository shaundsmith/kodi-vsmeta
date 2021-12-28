import json
import os.path

SET_INFO_FILE = ".setinfo"
SET_POSTER = "set-poster.jpg"
SET_FANART = "set-backdrop.jpg"


class SetInformation:
    title: str
    sort_title: str
    summary: str
    poster: bytes
    fanart: bytes


# Returns set information for the given movie
# Expects the set information to be in a .setinfo file adjacent to the scraped file
#   file_path: The path of the file being scraped
#   image_directory: The image directory to retrieve the set images from
def get(file_path, image_directory):
    set_information = SetInformation()

    file_name = os.path.splitext(os.path.basename(file_path))[0]
    directory = os.path.dirname(file_path)
    set_information_file = os.path.join(directory, SET_INFO_FILE)
    print("Searching for set information in " + str(set_information_file) + " for " + file_name)
    if os.path.exists(set_information_file):
        file_handle = open(set_information_file, "rb")
        raw_set_information = json.load(file_handle)
        file_handle.close()

        set_information.title = raw_set_information["title"]
        set_information.summary = raw_set_information["summary"]
        if "order" in raw_set_information and file_name in raw_set_information["order"]:
            sort_index = str(raw_set_information["order"].index(file_name)).rjust(2, '0')
            set_information.sort_title = raw_set_information["title"] + sort_index
    if os.path.exists(os.path.join(directory, image_directory, SET_POSTER)):
        set_information.poster = os.path.join(directory, image_directory, SET_POSTER)
    if os.path.exists(os.path.join(directory, image_directory, SET_POSTER)):
        set_information.fanart = os.path.join(directory, image_directory, SET_FANART)

    return set_information
