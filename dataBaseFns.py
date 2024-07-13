import string

# harness and thoroughbred database
harn = ['Eldorado Scioto', 'Georgian Downs', "Harrah's Philadelphia",
        'Harrington', 'Hippodrome Trois Rivieres', 'Hoosier',
        'Monticello', 'Northfield', 'Ocean', 'Plainridge Casino',
        'Pocono', 'Red Mile', 'Red Shores', 'Running Aces',
        'Saratoga Harness', 'Tioga', 'Woodbine Mohawk', 'Yonkers', 'Freehold',
        'The Meadows', 'Vernon Downs', 'batavia', 'tioga downs',
        'Northville', 'Grand River', 'Ocean Downs', 'Flamboro', 'Meadowlands',
        'Delaware County Fair', 'Red Shores - Summerside', 'Rideau Carleton', 'Fraser']

# applied after the custom track name fn
thor = ['Arapahoe', 'Assiniboia', 'Australian Racing', 'Belterra',
        'Canterbury', 'Del Mar', 'Ellis Park', 'Emerald', 'Finger Lakes',
        'Fort Erie',
        'Gulfstream', 'Hastings Racecourse', 'Hawthorne',
        'Horseshoe Indianapolis', 'Laurel',
        'Los Alamitos', 'Louisiana', 'Monmouth', 'Mountaineer', 'Parx Racing',
        'Prairie Meadows', 'Presque Isle', 'Ruidoso', 'Saratoga',
        'Sis Australia Racing', 'Thistledown', 'Woodbine', 'Colonial',
        'Penn National', 'Charles Town', 'Delta Downs', 'Century Mile',
        'Remington Park', 'Delaware', 'Retama', 'Pimlico', 'Caymanas', 'Golden Gate', 'Lone Star', 'Century Downs',
        'Kentucky Downs', 'Ajax Downs', 'Churchill', 'Will Rogers Downs', 'Belmont', 'Fairmount',
        'Santa Anita']  # check if there is a harness version of century mile

# restricted words and ignored database. Any word in wordsToRemove will
# be removed from the track name. Any words in exlcuded will be ignored
# from the wordsToRemove list
wordsToRemove = ["park", "downs", "racetrack", "(quarter horse)",  # must be
                 "(harness) hd", "(harness)", "jack", "race course", "racino",  # lowercase
                 "mohegan sun", "thordoughbred club", "race track",
                 "the", "- charlottetown driving", "raceway",
                 "and casino hd", 'races', 'fields', 'racing, gaming & hotel',
                 "(quarter horse )"]

excluded = ["ellis park", "tioga downs", "georgian downs", "arapahoe park",
            "ocean downs", "ajax downs", 'australian racing',
            'sis australian racing', 'the meadows', 'vernon downs',
            'delta downs', 'remington park', 'kentucky downs', 'century downs']

# banned tracks databse, any word in here will bar any track contining this
# word from the final list
bannedTrack = ["event name", "greyhound", "africa", "pmu", "mardi gras", "american racing", "cumberland", "sonoma",
               "wheeling", "skowhegan", 'timonium fair', 'carf - ferndale',
               'illinois fair racing', 'bangor raceway', 'hong kong jockey club', 'arapahoe park', 'at albuquerque',
               'keeneland horse', 'magic city jai alai', 'shenandoah', 'farmington fair', 'fanduel racing tv', 'carf',
               'columbus', 'gran premio', 'energy']  # has to be lowercase

# if a track has a word that must be removed but you also want to keep one of
# the banned words, put it in here, i.e Delta downs
customTrackName = {'The Meadows Racetrack': 'The Meadows',
                   'Delta Downs (Quarter Horse)': 'Delta Downs',
                   'Delta Downs Racetrack and Casino HD': 'Delta Downs',
                   'Century Downs Racetrack': 'Century Downs',
                   'Will Rogers Hd': 'Will Rogers Downs',
                   # 'FanDuel Racing TV' : 'Fanduel - Fairmount',
                   'Fanduel Sportsbook and Horse Racing': 'Fairmount',
                   }

# wordlist for woodbine tracks being converted to RTN tracks
# to use, simply put RTN Track : Corresponding WDBN Track
woodbine_to_RTN = {'Belmont At Aqueduct': 'Belmont @ The Big A',
				   'Woodbine Mohawk': 'Woodbine Stbd ',
                   'Gulfstream': 'Gulfstream',
                   'Woodbine': 'Woodbine Thbd',
                   "Harrah's Philadelphia": "Harrah's Philly",
                   "Saratoga": "Saratoga Race Course"
				   }


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


def removeTracks(tabledict):
    """takes in a dictionary and removes any item containing a word
	 from the list bannedTrack"""

    for key in list(tabledict.keys()):
        if any(substring in key.lower() for substring in bannedTrack):
            # print(key)
            del tabledict[key]


def removeKeyWords(tabledict):
    """takes in a dictionary and removes specific keywords from them
	unless the track is in the excluded list returns nothing"""
    # go through and check if any keys exactly match the dict customTrackName
    for key in list(tabledict.keys()):
        if key in customTrackName:
            tabledict[customTrackName[key]] = tabledict.pop(key)
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
