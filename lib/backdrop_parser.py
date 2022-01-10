from lib import Media
from lib.DataStream import DataStream


def parse(data_stream: DataStream) -> Media.Image:
    """
    Parses a backdrop image group from the given data stream.

    :param data_stream: datastream containing the backdrop image group

    :return: the parsed backdrop image group
    """
    backdrop = Media.Image()

    def add_image():
        backdrop.data = data_stream.read_image()

    def add_md5():
        backdrop.md5 = data_stream.read_string()

    def add_timestamp():
        backdrop.timestamp = data_stream.read_timestamp()

    fields = {
        0x0a: add_image,
        0x12: add_md5,
        0x18: add_timestamp,
    }

    while data_stream.has_data():
        field_type = data_stream.read_integer()
        if field_type in fields:
            fields[field_type]()

    return backdrop
