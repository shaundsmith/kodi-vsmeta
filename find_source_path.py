from pathlib import Path
import xbmc
import json


# Returns the source path for a given media title.
#   title: the title of the media
def find_source_path(title: str) -> str:
    response = xbmc.executeJSONRPC('{"jsonrpc": "2.0","id":1,"method":"Files.GetSources","params":{"media": "video"}}')
    parsed_response = json.loads(response)

    sources = parsed_response['result']['sources']

    source_path = None
    for source in sources:
        if any(True for _ in Path(source["file"]).rglob(title + ".*")):
            source_path = source["file"]
            break

    return source_path
