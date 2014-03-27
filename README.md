# Spotify CLI

Super hacky spotify CLI. Will improve as I find more time.

## Usage

    sli [ -t | -a | -l ] query...

Searches spotify API by track, artist, and album, respectively.

    sli [ -h | -v ]

Shows usage information and version number, respectively.

## TODO

Lots! PRs are welcome. Some initial TODOs:

- Only track searches work for now
  - Get artist/album searches working (easy)
  - I'm ignoring lots of information from tracks. So maybe use/display that
- Paging by 10 tracks at a time. Make this configurable?
- Selecting a track is done by entering the track number right now. Move selection logic to arrow keys or something
- Uses applescript to play the selected tracks. Abstract this, or make something more general. (but how?)
- Add caching
- BETTER ERROR HANDLING. like omg, I have none of it

## Notes

`api_endpoint.py` is a misleading name, as it really is just the whole
application right now. Will eventually break things up.
