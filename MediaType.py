MOVIE = "movie"
MOVIE_SET = "set"
TV_SHOW = "tvshow"
TV_SEASON = "season"
TV_EPISODE = "episode"


def is_tv(media_type):
    return media_type == TV_SHOW or media_type == TV_SEASON or media_type == TV_EPISODE
