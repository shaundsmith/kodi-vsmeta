import datetime
from dataclasses import dataclass


# Data structures for the parsed media information


@dataclass(init=False)
class Image:
    data: bytes
    path: str
    md5: str
    timestamp: datetime

    def __repr__(self):
        return str(self.__dict__)


@dataclass
class Credits:
    cast: list
    genre: list
    director: list
    writer: list


@dataclass(init=False)
class TvData:
    season: int
    episode: int
    year: int
    release_date: datetime
    locked: bool
    summary: str
    poster: Image
    metadata: str
    backdrop: Image

    def __init__(self):
        self.locked = False
        self.backdrop = Image()
        self.poster = Image()

    def __repr__(self):
        return str(self.__dict__)


@dataclass(init=False)
class Media:
    title: str
    title_2: str
    tag_line: str
    year: int
    release_date: datetime
    locked: bool
    summary: str
    metadata: str
    credits: Credits
    backdrop: Image
    classification: str
    rating: float
    poster: Image
    tv_data: TvData

    def __init__(self):
        self.locked = False
        self.backdrop = Image()
        self.poster = Image()

    def is_tv_show(self) -> bool:
        return hasattr(self, "tv_data")

    def __repr__(self):
        return str(self.__dict__)
