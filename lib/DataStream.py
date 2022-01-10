import base64
import binascii
import re
from datetime import datetime
import time

DATE_FORMAT = "%Y-%m-%d"


class DataStream:
    """
    Class for incrementally reading a stream of bytes.
    """
    data: bytes
    position: int = 0

    def __init__(self, data: bytes):
        """
        Initialises the datastream.

        :param data: data to use for the datastream
        """
        self.data = data

    def read_date(self) -> datetime:
        """
        Reads a date from the current position in the data stream.

        :return: the date
        """
        string_date = self.read_string()
        try:
            res = datetime.strptime(string_date, DATE_FORMAT)
        except TypeError:
            res = datetime(*(time.strptime(string_date, DATE_FORMAT)[0:6]))
        return res

    def read_timestamp(self) -> datetime:
        """
        Reads a timestamp from the current position in the data stream.

        :return: the timestamp
        """
        return datetime.fromtimestamp(self.read_integer())

    def read_image(self) -> bytes:
        """
        Reads an image as a series of bytes from the current position in the data stream.

        :return: the image byte array
        """
        image = bytes()
        try:
            image_string = self.read_string()
            image = base64.b64decode(re.sub(r"\s+", "", image_string))
        except binascii.Error:
            print("Image in invalid format")
        return image

    def read_string(self) -> str:
        """
        Reads a variable length string from the current position in the data stream.

        :return: the string
        """
        string_bytes = self.read_bytes()

        return string_bytes.decode("utf-8")

    def read_bytes(self, *args) -> bytes:
        """
        Reads an array of bytes from the current position in the data stream.

        An optional fixed length can be provided specifying the length of the byte array. If no length is provided then
        the length is calculated based on the next byte in the stream.

        :param args: arguments containing the optional fixed length

        :return: the byte array
        """
        bytes_read = []

        if len(args) == 1:
            length = args[0]
        else:
            length = self.read_integer()

        if not length:
            length = 0

        for _ in range(length):
            byte_read = self.read_byte()
            if byte_read is not None:
                bytes_read.append(byte_read)
        return bytes(bytes_read)

    def read_integer(self) -> int:
        """
        Reads an integer from the current position in the data stream.

        :return: the integer
        """
        integer = 0
        offset = 0
        while True:
            v = self.read_byte()
            if not v:
                break
            integer = integer | (v & 0x7f) << offset
            offset += 7
            if v & 0x80 == 0 or not self.has_data():
                break
        return integer

    def read_byte(self) -> int:
        """
        Reads a single byte from the current position in the data stream.

        :return: the byte, or None if there is no further data in the stream
        """
        byte = None
        if self.has_data():
            byte = self.data[self.position]
            self.position += 1

        return byte

    def has_data(self):
        """
        Returns true if the data stream still contains data.

        :return: true if the data stream still contains data, false otherwise
        """
        return self.position < len(self.data)


class DataStreamFactory:

    @staticmethod
    def from_file(file_path: str) -> DataStream:
        """
        Constructs a DataStream from the given file path

        :param file_path: the path of the file that is to be loaded as a DataStream

        :return: the DataStream for the file
        """
        file_contents = []
        file_handle = open(file_path, "rb")
        buffer = file_handle.read(1)
        file_contents.append(buffer)
        while buffer:
            buffer = file_handle.read(1)
            file_contents.append(buffer)
        file_handle.close()

        return DataStream(bytes.join(bytes(), file_contents))
