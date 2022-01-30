# kodi-vsmeta

Kodi plugin for scraping data from Synology Videostation VSMeta files for both TV shows and movies.

## Usage

The plugin is very particular about the naming conventions used for movies and TV shows.

### Movies

Movies can be stored individually or as part of a set.

Individual movies can be stored within their own directories, or in a single directory.

Sets must be stored in a single directory per set. Sets require a 

### TV Shows

Episodes for a given TV show must appear within a single directory. The episode file names must match the directory name
and be in the format: `*name*.Sxx.Eyy`, where `xx` is the season number and `yy` is the episode number.

Episodes may also be stored in sub directories name `Season yy`, where `xx` is the season.

E.g. Both are valid structures
```
TV Shows
  | - The Simpsons
  |        | - The Simpsons.S01.E01.avi
  |        | - The Simpsons.S01.E02.avi
  |        | - The Simpsons.S02.E01.avi
  |
  | - Futurama
         | - Season 1
               | - Futurama.S01.E01.avi
               | - Futurama.S01.E02.avi
         | - Season 2
               | - Futurama.S02.E01.avi
```


## Known Issues

* Occasionally, the wrong VSMeta file will be used for analysis if a TV Show and Movie exist with the same name.
* The performance is quite poor, primarily due to the Kodi scraper flow. \
  Scraping movies requires 2 steps, and requires the VSMeta file to be parsed twice.\
  TV shows require 4 steps, and requires `2n+2` VSMeta files to be parsed, where `n` is the number of episodes in the TV
  show.

## Future Work

* Investigate ways to improve performance when scraping data.
* Add possibility of season posters