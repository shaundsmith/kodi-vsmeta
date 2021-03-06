import os

from lib.Media import Media

POSTER_SUFFIX = "-poster.jpg"
BACKDROP_SUFFIX = "-backdrop.jpg"


def write_images(file_path: str, media: Media, image_directory: str):
    """
    Writes all images in the parsed Media object to the filesystem.

    :param file_path: the path to the vsmeta file that was parsed
    :param media: the parsed vsmeta file
    :param image_directory: the directory to write the images to
    """
    file_name = os.path.basename(file_path)
    directory = os.path.dirname(file_path)

    image_directory = os.path.join(directory, image_directory)
    if not os.path.exists(image_directory):
        os.mkdir(image_directory)

    def get_file_name():
        media_file_name = file_name.replace(".vsmeta", "")
        return os.path.splitext(media_file_name)[0]

    def make_safe_file_name(raw_file_name):
        safe_characters = (' ', '.', '-', '_', '&')
        return "".join([char for char in raw_file_name if char.isalnum() or char in safe_characters]).rstrip()

    def write_image(image_name, image_data):
        image_path = os.path.join(image_directory, make_safe_file_name(image_name))
        image_file = open(image_path, "wb")
        image_file.write(image_data)
        image_file.close()

        return image_path

    def has_image_data(image):
        return hasattr(image, "data") and len(image.data) > 0

    if media.is_tv_show():
        if has_image_data(media.tv_data.poster):
            path = write_image(media.title + POSTER_SUFFIX, media.tv_data.poster.data)
            media.tv_data.poster.path = path
        if has_image_data(media.tv_data.backdrop):
            path = write_image(media.title + BACKDROP_SUFFIX, media.tv_data.backdrop.data)
            media.tv_data.backdrop.path = path
        if has_image_data(media.poster):
            path = write_image(get_file_name() + "-episode-image.jpg", media.poster.data)
            media.poster.path = path
    else:
        if has_image_data(media.poster):
            path = write_image(get_file_name() + POSTER_SUFFIX, media.poster.data)
            media.poster.path = path
        if has_image_data(media.backdrop):
            path = write_image(get_file_name() + BACKDROP_SUFFIX, media.backdrop.data)
            media.backdrop.path = path
