from lib import Media
from lib.DataStream import DataStream


def parse(data_stream: DataStream) -> Media.Credits:
    """
    Parses a credits group from the given datastream.

    :param data_stream: the datastream containing the credits group

    :return: the parsed credits group
    """
    media_credits = Media.Credits()

    def add_cast(cast_member):
        media_credits.cast.append(cast_member)

    def add_director(director):
        media_credits.director.append(director)

    def add_genre(genre):
        media_credits.genre.append(genre)

    def add_writer(writer):
        media_credits.writer.append(writer)

    fields = {
        0x0a: add_cast,
        0x12: add_director,
        0x1a: add_genre,
        0x22: add_writer
    }

    while data_stream.has_data():
        field_type = data_stream.read_integer()
        if field_type in fields:
            fields[field_type](data_stream.read_string())

    return media_credits
