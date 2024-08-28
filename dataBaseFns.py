import string
import readDatabase

harn, thor = readDatabase.readTorH()

customTrackName = readDatabase.readCustomTrackName()

wordsToRemove = readDatabase.readWordsToRemove()

excluded = readDatabase.readExclude()

woodbine_to_RTN = readDatabase.readWoodbine_to_RTN()

bannedTrack = readDatabase.readBannedTrack()

def harnOrThor(track):
    '''takes in a track as a string and determines if it is
	harness or thoroughbred, returns 'T' or 'H' or 'E' '''
    # make thor and harn lists lowercase
    harness = [x.lower() for x in harn]  # must make new vars because harn
    thoro = [x.lower() for x in thor]  # and thor are not global vars
    track = track.lower()
    if track in harness:
        return 'SB'
    if track in thoro:
        return 'TB'
    return ''

# This function is run first
def removeTracks(tabledict):
    """takes in a dictionary and removes any item containing a word
	 from the list bannedTrack"""

    for key in list(tabledict.keys()):
        if any(substring in key.lower() for substring in bannedTrack):
            # print(key)
            del tabledict[key]

# Then removeKeyWords happens
def removeKeyWords(tabledict):
    """takes in a dictionary and removes specific keywords from them
	unless the track is in the excluded list returns nothing"""
    # go through and check if any keys exactly match the dict customTrackName
    for key in list(tabledict.keys()):
        # print("key in remove: " + key)
        if key in customTrackName:
            tabledict[customTrackName[key]] = tabledict.pop(key)
            # print("changed " + customTrackName[key])
    # iterate through dict.keys()
    for key in list(tabledict.keys()):
        if key.lower() in excluded:
            continue
        new_string = key.lower()
        # make new string, removing all substrings
        for sub in wordsToRemove:
            new_string = new_string.replace(sub, ' ')
        # clean up string, removing white space and capitalizing
        new_string = " ".join(new_string.split())
        new_string = string.capwords(new_string)
        # print("og: " + key + " ||| new: " + new_string)
        # replace item in dictionary
        tabledict[new_string] = tabledict.pop(key)


def inWoodbineTrackDatabase(track):
    """takes track and checks against a small wordlist to convert the track"""
    if track in woodbine_to_RTN:
        return True
    return False


def setWoodbineTrack(RTN_track):
    return woodbine_to_RTN[RTN_track]
