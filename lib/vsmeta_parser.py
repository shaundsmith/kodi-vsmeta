from lib import Media, image_writer, backdrop_parser, credit_parser, tv_data_parser
from lib.DataStream import DataStream, DataStreamFactory

DEFAULT_IMAGE_DIRECTORY = ".media-art"


def parse(file_path: str, extract_images: bool) -> Media:
    """
    Parses a Synology Videostation vsmeta file into a Media object.

    :param file_path: the path to the vsmeta file
    :param extract_images: whether to extract images into separate files. The extracted images are stored in the
     `.media-art/` adjacent to the vsmeta file.

    :return: the Media object representing the vsmeta file contents
    """
    data_stream = DataStreamFactory().from_file(file_path)

    magic = data_stream.read_byte()
    version = data_stream.read_byte()
    if magic != 0x08:
        raise IOError("Invalid VSMeta file")
    else:
        print("Reading vsmeta file with version %d" % version)

    media = Media.Media()

    def add_title():
        media.title = data_stream.read_string()

    def add_title_2():
        media.title_2 = data_stream.read_string()

    def add_tag_line():
        media.tag_line = data_stream.read_string()

    def add_year():
        media.year = data_stream.read_integer()

    def add_release_date():
        media.release_date = data_stream.read_date()

    def add_locked():
        media.locked = data_stream.read_integer() != 0

    def add_summary():
        media.summary = data_stream.read_string()

    def add_metadata():
        media.metadata = data_stream.read_string()

    def add_credits_or_backdrop():
        group = data_stream.read_bytes()
        if hasattr(media, "credits"):
            media.backdrop = backdrop_parser.parse(DataStream(group))
        else:
            media.credits = credit_parser.parse(DataStream(group))

    def add_backdrop():
        group = data_stream.read_bytes()
        media.backdrop = backdrop_parser.parse(DataStream(group))

    def add_classification():
        media.classification = data_stream.read_string()

    def add_rating():
        media.rating = data_stream.read_integer() / 10

    def add_poster_data():
        media.poster.data = data_stream.read_image()

    def add_poster_md5():
        media.poster.md5 = data_stream.read_string()

    def add_tv_data():
        group = data_stream.read_bytes()
        media.tv_data = tv_data_parser.parse(DataStream(group))

    fields = {
        0x12: add_title,
        0x1a: add_title_2,
        0x22: add_tag_line,
        0x28: add_year,
        0x32: add_release_date,
        0x38: add_locked,
        0x42: add_summary,
        0x4a: add_metadata,
        0x52: add_credits_or_backdrop,
        0x5a: add_classification,
        0x60: add_rating,
        0x8a: add_poster_data,
        0x92: add_poster_md5,
        0x9a: add_tv_data,
        0xaa: add_backdrop
    }

    while data_stream.has_data():
        field_type = data_stream.read_integer()
        if field_type in fields:
            fields[field_type]()

    if extract_images:
        image_writer.write_images(file_path, media, DEFAULT_IMAGE_DIRECTORY)

    return media
