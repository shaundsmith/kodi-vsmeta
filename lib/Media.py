import datetime


# Data structures for the parsed media information


class Image:
    data: bytes
    path: str
    md5: str
    timestamp: datetime

    def __init__(self):
        self.path = ""

    def __repr__(self):
        return str(self.__dict__)


class Credits:
    cast: list
    genre: list
    director: list
    writer: list

    def __init__(self):
        self.cast = []
        self.genre = []
        self.director = []
        self.writer = []

    def __repr__(self):
        return str(self.__dict__)


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
