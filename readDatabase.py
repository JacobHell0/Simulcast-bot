import json
# functions responsible for reading from text documents into lists, this allows easy editing of the lists


def readIntoList(filename):
    """Helper function to read a comma seperated list into a python list"""
    with open(f"database/{filename}", "r") as f:
        data = f.read().replace("\n", "").split(",")

    return data
def readTorH():
    """returns a tuple containing a list where the first item is harness tracks and the second is thor"""
    thor = readIntoList("thor.txt")
    harn = readIntoList("harn.txt")

    return harn, thor

def readCustomTrackName():
    """Returns a dictionary containing the custom track name dictionary"""
    with open("database/CustomTrack.json", "r") as f:
        tracks = f.read()

    return json.loads(tracks)


def readExclude():
    """Returns a list containing the excluded words"""
    return readIntoList("excluded.txt")


def readWordsToRemove():
    """Returns a list containg the words to remove list"""
    data = readIntoList("wordsToRemove.txt")
    data.append("racing, gaming & hotel")  # not an elegant solution but it will do
    return data

def readBannedTrack():
    return readIntoList("bannedTrack.txt")

def readWoodbine_to_RTN():
    with open("database/woodbineToRtn.json", "r") as f:
        dict = f.read()
    return json.loads(dict)

readBannedTrack()
