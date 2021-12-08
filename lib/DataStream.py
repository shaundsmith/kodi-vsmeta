import base64
import binascii
import re
from datetime import datetime
import time

DATE_FORMAT = "%Y-%m-%d"


# Class for incrementally reading a stream of bytes
class DataStream:
    data: bytes
    position: int = 0

    def __init__(self, data: bytes):
        self.data = data

    # Reads a date from the data stream.
    def read_date(self) -> datetime:
        string_date = self.read_string()
        try:
            res = datetime.strptime(string_date, DATE_FORMAT)
        except TypeError:
            res = datetime(*(time.strptime(string_date, DATE_FORMAT)[0:6]))
        return res

    # Reads a timestamp from the data stream.
    def read_timestamp(self) -> datetime:
        return datetime.fromtimestamp(self.read_integer())

    # Reads an image from the data stream.
    def read_image(self) -> bytes:
        image = bytes()
        try:
            image_string = self.read_string()
            image = base64.b64decode(re.sub(r"\s+", "", image_string))
        except binascii.Error:
            print("Image in invalid format")
        return image

    # Reads a variable-length set of bytes as a string from the data stream.
    def read_string(self) -> str:
        string_bytes = self.read_bytes()

        return string_bytes.decode("utf-8")

    # Reads a set of bytes from the data stream.
    # An optional fixed length can be provided for the set of bytes.
    # If no length is provided, the length is calculated based on the next byte in the stream.
    def read_bytes(self, *args) -> bytes:
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

    # Reads an integer from the data stram.
    def read_integer(self) -> int:
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

    # Reads a single byte from the data stream.
    # Returns 'None' if there is no further data in the data stream
    def read_byte(self) -> int:
        byte = None
        if self.has_data():
            byte = self.data[self.position]
            self.position += 1

        return byte

    # Returns true if the data stream still contains data.
    def has_data(self):
        return self.position < len(self.data)


# Class for constructing data streams from file paths.
class DataStreamFactory:

    # Constructs a DataStream from the given file path
    @staticmethod
    def from_file(file_path: str) -> DataStream:
        file_contents = []
        file_handle = open(file_path, "rb")
        buffer = file_handle.read(1)
        file_contents.append(buffer)
        while buffer:
            buffer = file_handle.read(1)
            file_contents.append(buffer)
        file_handle.close()

        return DataStream(bytes.join(bytes(), file_contents))
