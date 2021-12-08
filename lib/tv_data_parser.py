from lib import Media, backdrop_parser
from lib.DataStream import DataStream


# Parses a tv data group from the vsmeta file
#   data_stream: the data stream for the backdrop group
def parse(data_stream: DataStream) -> Media.TvData:
    tv_show_data = Media.TvData()

    def add_season():
        tv_show_data.season = data_stream.read_integer()

    def add_episode():
        tv_show_data.episode = data_stream.read_integer()

    def add_year():
        tv_show_data.year = data_stream.read_integer()

    def add_release_date():
        tv_show_data.release_date = data_stream.read_date()

    def add_locked():
        tv_show_data.locked = data_stream.read_integer() != 0

    def add_summary():
        tv_show_data.summary = data_stream.read_string()

    def add_poster_data():
        tv_show_data.poster.data = data_stream.read_image()

    def add_poster_md5():
        tv_show_data.poster.md5 = data_stream.read_string()

    def add_metadata():
        tv_show_data.metadata = data_stream.read_string()

    def add_backdrop():
        group = data_stream.read_bytes()
        tv_show_data.backdrop = backdrop_parser.parse(DataStream(group))

    fields = {
        0x08: add_season,
        0x10: add_episode,
        0x18: add_year,
        0x22: add_release_date,
        0x28: add_locked,
        0x32: add_summary,
        0x3A: add_poster_data,
        0x42: add_poster_md5,
        0x4A: add_metadata,
        0x52: add_backdrop
    }

    while data_stream.has_data():
        field_type = data_stream.read_integer()
        if field_type in fields:
            fields[field_type]()

    return tv_show_data
