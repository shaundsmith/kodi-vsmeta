import json
import os.path

SET_INFO_FILE = ".setinfo"
SET_POSTER = "set-poster.jpg"
SET_FANART = "set-backdrop.jpg"


class SetInformation:
    title: str
    summary: str
    poster: bytes
    fanart: bytes


# Returns set information for the given movie
# Expects the set information to be in a .setinfo file adjacent to the scraped file
#   file_path: The path of the file being scraped
#   image_directory: The image directory to retrieve the set images from
def get(file_path, image_directory):
    set_information = SetInformation()

    directory = os.path.dirname(file_path)
    set_information_file = os.path.join(directory, SET_INFO_FILE)
    print("Searching for set information in " + str(set_information_file))
    if os.path.exists(set_information_file):
        file_handle = open(set_information_file, "rb")
        raw_set_information = json.load(file_handle)
        file_handle.close()

        set_information.title = raw_set_information["title"]
        set_information.summary = raw_set_information["summary"]
    if os.path.exists(os.path.join(directory, image_directory, SET_POSTER)):
        set_information.poster = os.path.join(directory, image_directory, SET_POSTER)
    if os.path.exists(os.path.join(directory, image_directory, SET_POSTER)):
        set_information.fanart = os.path.join(directory, image_directory, SET_FANART)

    return set_information
