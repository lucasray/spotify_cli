#!/usr/bin/env python

# imports
import sys
import urllib
import re
import json
import getopt
import os

_VERSION = 0.1

# constants
API_URL = 'http://ws.spotify.com/search/1/'
_BY_TRACK = 'track'
_BY_ARTIST = 'artist'
_BY_ALBUM = 'album'
_IN_JSON = '.json'
_COLORS = {
  'black'       : '\x1B[0;30m',
  'red'         : '\x1B[0;31m',
  'green'       : '\x1B[0;32m',
  'yellow'      : '\x1B[0;33m',
  'blue'        : '\x1B[0;34m',
  'purple'      : '\x1B[0;35m',
  'cyan'        : '\x1B[0;36m',
  'light_grey'  : '\x1B[0;37m',
  'dark_grey'   : '\x1B[1;30m',
  'bold_red'    : '\x1B[1;31m',
  'bold_green'  : '\x1B[1;32m',
  'bold_yellow' : '\x1B[1;33m',
  'bold_blue'   : '\x1B[1;34m',
  'bold_purple' : '\x1B[1;35m',
  'bold_cyan'   : '\x1B[1;36m',
  'white'       : '\x1B[1;37m'
}
_TERMINAL_COLOR = '\x1B[0m'

_PAGE_SIZE = 10

def search(url):
  fp = urllib.urlopen(url)
  jsonObj = json.load(fp)
  return jsonObj

def searchByTrack(track):
  params = {
    'q': track
  }
  query = addParams(API_URL + _BY_TRACK + _IN_JSON, params)
  jsonObj = search(query)

  page = jsonObj['tracks'][0:_PAGE_SIZE]
  index = 0
  for track in page:
    index += 1
    try:
      trackName = colorize(track['name'], 'cyan')
      trackArtist = colorize(track['artists'][0]['name'], 'green')
      print "  {:2d}. {} - {}".format(index, trackName, trackArtist)
    except UnicodeEncodeError:
      print "  {:2d}. Error".format(index)

  promptForSelection(page)

def colorize(text, color):
  colorString = _COLORS[color]
  return "{}{}{}".format(colorString, text, _TERMINAL_COLOR)

def promptForSelection(page):
  selection = raw_input("\nSelect a track: ")
  try:
    intSelection = int(selection)
  except ValueError:
    print "Invalid selection."
    sys.exit(2)

  if (intSelection < 1) or (intSelection > _PAGE_SIZE):
    print "Invalid selection."
    sys.exit(2)

  track = page[intSelection - 1]
  playTrack(track)

def playTrack(track):
  os.system("osascript -e 'tell application \"Spotify\" to play track \"{}\"'".format(track['href']))

def searchByArtist(artist):
  params = {
    'q': artist
  }
  query = addParams(API_URL + _BY_ARTIST + _IN_JSON, params)
  search(query)

def searchByAlbum(album):
  params = {
    'q': album
  }
  query = addParams(API_URL + _BY_ALBUM + _IN_JSON, params)
  search(query)

def addParams(baseUrl, params):
  return baseUrl + '?' + urllib.urlencode(params)

def version():
  print "sli version " + str(_VERSION)

def usage():
  print "usage: sli [-a | -t | -l | -h | -v] query..."
  print "  -a query, --artist query"
  print "    Search by artist."
  print "  -t query, --track query"
  print "    Search by track."
  print "  -l query, --album query"
  print "    Search by album."
  print "  -h, --help"
  print "    Show this screen."
  print "  -v, --version"
  print "    Print the current version"

def main():
  # Parse args
  try:
    optString = "a:t:l:hv"
    optArr = ["help", "version", "artist=", "track=", "album="]
    opts, args = getopt.getopt(sys.argv[1:], optString, optArr)
  except getopt.GetoptError as err:
    print str(err)
    usage()
    sys.exit(2)

  searchFn = None
  args = None
  for o, a in opts:
    if o in ('-a', '--artist'):
      searchFn = searchByArtist
      args = a
    elif o in ('-t', '--track'):
      searchFn = searchByTrack
      args = a
    elif o in ('-l', '--album'):
      searchFn = searchByAlbum
      args = a
    elif o in ('-h', '--help'):
      usage()
      sys.exit(0)
    elif o in ('-v', '--version'):
      version()
      sys.exit(0)

  if searchFn is None:
    usage()
    sys.exit(2)

  if args is None:
    usage()
    sys.exit(2)

  # Run the specified search
  searchFn(a)

if __name__ == '__main__':
  main()
