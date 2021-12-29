from datetime import datetime
from typing import Any

from lib.Media import Media


class MetaDataField:
    metadata: Media
    field_value: Any

    def __init__(self, metadata, field_locator):
        self.metadata = metadata
        self.field_value = MetaDataField._get_field_value(metadata, field_locator)

    @staticmethod
    def _get_field_value(metadata, field_locator):
        value = metadata
        for field in field_locator.split("."):
            if not hasattr(value, field): return None
            value = getattr(value, field)
        return value

    def has_value(self):
        return self.field_value is not None

    def get_value(self):
        return str(self.field_value) if isinstance(self.field_value, datetime) else self.field_value


class VideoInfoBuilder:
    video_info: dict

    def __init__(self):
        self.video_info = {}

    def with_field(self, field_name, metadata_field):
        if metadata_field.has_value():
            self.video_info[field_name] = metadata_field.get_value()
        return self

    def with_field_value(self, field_name, field_value):
        self.video_info[field_name] = field_value
        return self

    def build(self):
        return self.video_info
