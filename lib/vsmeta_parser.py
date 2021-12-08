from lib import Media, image_writer, backdrop_parser, credit_parser, tv_data_parser
from lib.DataStream import DataStream, DataStreamFactory


# Parses a Synology Videostation vsmeta file into a Python data structure.
#   file_path: The path to the vsmeta file
#   extract_images: Whether to extract images into separate files.
#                   The extracted images are stored in .media-art/ adjacent to the vsmeta file
def parse(file_path: str, extract_images: bool) -> Media:
    data_stream = DataStreamFactory().from_file(file_path)

    magic = data_stream.read_byte()
    version = data_stream.read_byte()
    if magic != 0x08:
        raise IOError("Invalid VSMeta file")
    else:
        print("Reading vsmeta file with version %d" % version)

    media = Media.Media()

    def add_title():
        print("Parsing title")
        media.title = data_stream.read_string()

    def add_title_2():
        print("Parsing title 2")
        media.title_2 = data_stream.read_string()

    def add_tag_line():
        print("Tag Line")
        media.tag_line = data_stream.read_string()

    def add_year():
        print("Parsing year")
        media.year = data_stream.read_integer()

    def add_release_date():
        print("Parsing release date")
        media.release_date = data_stream.read_date()

    def add_locked():
        print("Parsing locked")
        media.locked = data_stream.read_integer() != 0

    def add_summary():
        print("Parsing summary")
        media.summary = data_stream.read_string()

    def add_metadata():
        print("Parsing metadata")
        media.metadata = data_stream.read_string()

    def add_credits_or_backdrop():
        print("Parsing credits/backdrop")
        group = data_stream.read_bytes()
        if hasattr(media, "credits"):
            media.backdrop = backdrop_parser.parse(DataStream(group))
        else:
            media.credits = credit_parser.parse(DataStream(group))

    def add_backdrop():
        print("Parsing backdrop")
        group = data_stream.read_bytes()
        media.backdrop = backdrop_parser.parse(DataStream(group))

    def add_classification():
        print("Parsing classification")
        media.classification = data_stream.read_string()

    def add_rating():
        print("Parsing rating")
        media.rating = data_stream.read_integer() / 10

    def add_poster_data():
        print("Parsing poster data")
        media.poster.data = data_stream.read_image()

    def add_poster_md5():
        print("Parsing poster md5")
        media.poster.md5 = data_stream.read_string()

    def add_tv_data():
        print("Parsing tv data")
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
        image_writer.write_images(file_path, media)

    return media
