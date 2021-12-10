import os

from lib.Media import Media


# Writes all images parsed as byte arrays to the filesystem.
# The images are written to the directory .media-art adjacent to the given file.
#   file_path: The path to the vsmeta file
#   media: The parsed media information from the vsmeta file
def write_images(file_path: str, media: Media):
    file_name = os.path.basename(file_path)
    directory = os.path.dirname(file_path)

    image_directory = os.path.join(directory, ".media-art")
    if not os.path.exists(image_directory):
        os.mkdir(image_directory)

    def get_file_name():
        media_file_name = file_name.replace(".vsmeta", "")
        return os.path.splitext(media_file_name)[0]

    def write_image(image_name, image_data):
        image_path = os.path.join(image_directory, image_name)
        image_file = open(image_path, "wb")
        image_file.write(image_data)
        image_file.close()

        return image_path

    if media.is_tv_show():
        if hasattr(media.tv_data.poster, "data") and len(media.tv_data.poster.data) > 0:
            path = write_image(media.title + "-poster.jpg", media.tv_data.poster.data)
            media.tv_data.poster.path = path
        if hasattr(media.tv_data.backdrop, "data") and len(media.tv_data.backdrop.data) > 0:
            path = write_image(media.title + "-backdrop.jpg", media.tv_data.backdrop.data)
            media.tv_data.backdrop.path = path
    else:
        if hasattr(media.poster, "data") and len(media.poster.data) > 0:
            path = write_image(get_file_name() + "-poster.jpg", media.poster.data)
            media.poster.path = path
        if hasattr(media.backdrop, "data") and len(media.backdrop.data) > 0:
            path = write_image(get_file_name() + "-backdrop.jpg", media.backdrop.data)
            media.backdrop.path = path
