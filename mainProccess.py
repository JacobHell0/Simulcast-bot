from SharedTools import getRTN, generateDict
from dataBaseFns import removeTracks, removeKeyWords, harnOrThor, inWoodbineTrackDatabase, setWoodbineTrack
from SendEmail import sendEmail
from fpdf import FPDF, FontFace
from datetime import datetime
from pytz import timezone
from iteration_utilities import unique_everseen, duplicates
from difflib import SequenceMatcher  # used to match woodbine tracks vs rtn tracks

from SharedTools import timeToDec
from SharedTools import timeToDecMixed
from grabPost import grabPost

# environmental variables
import os
from dotenv import load_dotenv

TRACKS_ON_PAGE = 30

load_dotenv()


# def sortKey(list_object):	#contains by what value lowest_post is sorted
# 	if (list_object[0][5:9] == 'a.m.')):
# 		list_object[0] = '0' + list_object[0][:]
# 	return list_object[0]

def sortKey(list_object):  # contains by what value lowest_post is sorted
	# if (list_object[0][5:9] == 'a.m.')):
	# 	list_object[0] = '0' + list_object[0][:]

	return timeToDec(list_object[0])


def sortKeyWoodbine(list_object):  # contains by what value lowest_post is sorted
	# if (list_object[0][5:9] == 'a.m.')):
	# 	list_object[0] = '0' + list_object[0][:]
	# print(f"trying to convert: {list_object}")
	return timeToDecMixed(list_object[0])


def makeLowestPostListRTN(tabledict):
	"""takes in a dictionary of tracks tabledict[key] = [RTN, start_time,
	 duration] and returns a list formated as [airtime, duration,
	track, roberts, recon(space)] """
	lowest_post = []
	channel_number = []
	for key in tabledict:
		# airtime, duration, track, roberts, recon(space)
		lowest_post.append([tabledict[key][1], tabledict[key][2], key, ' ' + tabledict[key][0], "     ", "   "])
		# add 97 numbers to separate list, to check for duplicates
		channel_number.append(tabledict[key][0])
	# go through and mark duplicates with an asterisk
	dupes = list(unique_everseen(duplicates(channel_number)))
	# go through each channel number and check if it is a dupe
	for x in lowest_post:
		if x[3][1:] in dupes:
			x[3] = '*' + x[3][1:]

	print("lowest post")
	for key in lowest_post:
		print(key)
	lowest_post.sort(key=sortKey)
	print("lowest post after sort -----------------")
	for key in lowest_post:
		print(key)

	for sublist in lowest_post:
		type = harnOrThor(sublist[2])
		print('track: ' + sublist[2] + ' | type: ' + type)
		if type != 'E':
			sublist[2] = sublist[2] + ' (' + type + ')'

	return lowest_post


def compareTracks(trackA, trackB):
	if trackA in trackB:
		return True

	if trackB in trackA:
		return True

	# sequence matcher, must be used, make log
	if SequenceMatcher(None, trackA, trackB).ratio() >= .9:  # fallback
		f = open("error-log.txt", "a")
		dt = datetime.now(timezone('EST'))
		f.write(dt.strftime("%A, %B %d"))
		f.write("   |   ")
		f.write("SequenceMatcher Used on trackA: " + trackA + ", trackB: " + trackB + ". Prob: " + str(
			SequenceMatcher(None, trackA, trackB).ratio()) + "\n")
		f.close()
		return True

	return False


def makeLowestPostWoodbine(tabledict):
	'''takes in a dictionary of tracks tabledict[key] = [RTN, start_time,
	duration] and returns a list formated as [airtime, duration, 
	track, roberts, recon(space)] '''
	lowest_post = []
	channel_number = []

	woodbine_times = grabPost()

	print(f"woodbine times:\n")
	for key in woodbine_times.keys():
		print("key: " + key, "value: ", woodbine_times[key])

	for key in tabledict:
		post_time = ""
		T_or_H = ""
		# search through woodbine tracks for post time
		for track in woodbine_times.keys():
			if inWoodbineTrackDatabase(key):
				# rename key without renaming actual dict key
				if compareTracks(setWoodbineTrack(key), track):
					post_time = woodbine_times[track][0]
					T_or_H = woodbine_times[track][1]
					break
			elif compareTracks(key, track):
				post_time = woodbine_times[track][0]
				T_or_H = woodbine_times[track][1]
		# if no post time was found: create error
		if post_time == "":
			post_time = "~" + tabledict[key][1]
			T_or_H = harnOrThor(key)
			f = open("error-log.txt", "a")
			dt = datetime.now(timezone('EST'))
			f.write(dt.strftime("%A, %B %d"))
			f.write("   |   ")
			f.write("RTN: " + key + "\n")
			f.close()

		# posttime, duration, track, roberts, recon(space)
		lowest_post.append([post_time, tabledict[key][2],
							key + " (" + T_or_H + ")", ' ' + tabledict[key][0], "     ", "   "])
		# add 97 numbers to seperate list, to check for duplicates
		channel_number.append(tabledict[key][0])
	# go through and mark duplicates with an asterisk
	dupes = list(unique_everseen(duplicates(channel_number)))
	# go through each channel number and check if it is a dupe
	for x in lowest_post:
		if x[3][1:] in dupes:
			x[3] = '*' + x[3][1:]

	print("lowest post")
	for key in lowest_post:
		print(key)
	lowest_post.sort(key=sortKeyWoodbine)
	print("lowest post after sort -----------------")
	for key in lowest_post:
		print(key)

	return lowest_post


def convertToPdf(lowest_post):
	"""takes in a list of lists in the format [[airtimes], [durations],
	[tracks], [97##], [blank spaces]], appends post time so the list looks like this:
	[[post_times], [durations], [tracks], [97##], [blank spaces]]
	"""


	# airtime, duration, track, roberts, recon(space)
	lowest_post.insert(0, ["Post Time", "Duration", "Track Name",
						   "Roberts", "Recon", " ® "])
	# temporary date, replace with actual title not in table
	dt = datetime.now(timezone('EST'))

	lowest_post.insert(0, ["-", "-", "~ = on airtime, * = repeat 97## number",
						   "-", "-", "-"])

	lowest_post.insert(0, ["-", "-", dt.strftime("%A, %B %d"),
						   "-", "-", "-"])

	pdf = FPDF()
	pdf.add_page()
	# pdf.set_font("helvetica", size=12)
	pdf.set_font(family='Times', size=12)
	pdf.table()
	with pdf.table(width=190, col_widths=(12, 11, 40, 8, 10, 8),
				   text_align=("CENTER", "CENTER", "LEFT", "CENTER", "CENTER", "CENTER")) as table:
		for data_row in lowest_post:
			row = table.row()
			for datum in data_row:
				if " a.m. " in datum:
					datum = datum.replace(" a.m. ", " AM ")
				if " p.m. " in datum:
					datum = datum.replace(" p.m. ", " PM ")
				if ("Ajax Downs" in datum) or ("Woodbine" in datum):
					pdf.set_font(style="B")
				# check if item is in db and weather to assign it TB or H
				# if() #if 'T' or 'H' or 'E'
				row.cell(datum)
				pdf.set_font(style="")

	pdf.output('RTN_Tracks.pdf')


def addPage(table_data, date, pdf):
	"""helper function to add a page with a table filled with table_data to the document, returns nothing"""
	pdf.add_page()

	# set margins
	pdf.set_margins(7.5, 15, 7.5)

	pdf.image("resources/logo.png", x=10, y=8.5, w=20, h=33)  # aspect ratio is 20:33
	pdf.image("resources/Watermark.png", x=9, y=6, w=739 * 0.262, h=986 * 0.262)  # aspect ratio is 739:986

	# draw border
	# pdf.rect(x=4, y=4, w=200, h=250)
	pdf.rect(x=5, y=4, w=199.6, h=288)
	pdf.rect(x=6, y=5, w=197.6, h=286)
	# pdf.rect(x=4, y=4, w=200, h=300)

	pdf.set_font('Arial', 'BU', 32)
	pdf.cell(w=0, h=10, text=date, ln=2, align='C', fill=False)
	pdf.set_font('Arial', 'B', 32)  # have to turn underline off, so it doesn't underline the space
	pdf.cell(w=0, h=10, text=" ", ln=2)

	pdf.set_font(family='Roman', size=18, style="")

	pdf.set_xy(x=45, y=35)
	with pdf.table(text_align="LEFT", first_row_as_headings=False, borders_layout="NONE", align="LEFT") as table:

		for data_row in table_data:
			row = table.row()
			for datum in data_row:
				if " a.m. " in datum:
					datum = datum.replace(" a.m. ", " AM ")
				if " p.m. " in datum:
					datum = datum.replace(" p.m. ", " PM ")
				if ("Ajax Downs" in datum) or ("Woodbine" in datum):
					pdf.set_font(style="B")

				row.cell(datum, padding=-2.4)
				pdf.set_font(style="")

def convertToPdfTracksheet(lowest_post):
	pdf = FPDF()
	date = lowest_post[0][2]

	# Keep cells [0] and [2] (post time and track name)
	# post_times = [["", date]]

	pdf.add_font("Roman", fname="resources/times.ttf")
	pdf.add_font("Roman", style="B", fname="resources/timesbd.ttf")

	post_times = []
	for item in lowest_post:
		post_times.append(["• " + item[0] + " " + item[2]])

	post_times.pop(0)  # remove top 3 cells they are useless, includes date, and 2 headings
	post_times.pop(0)
	post_times.pop(0)

	while post_times:
		limited_post_times = post_times[0:TRACKS_ON_PAGE]
		post_times = post_times[TRACKS_ON_PAGE:]
		addPage(limited_post_times, date, pdf)

	pdf.output('Track_Sheet.pdf')

def mainProccess(email):
	# -------------------------------
	table = getRTN()  # make request to rtn.tv and parse it with bs4
	if table == -1:
		return

	tabledict = generateDict(table)  # convert into dict
	removeTracks(tabledict)  # remove unwanted tracks
	removeKeyWords(tabledict)  # removes instances of words like racing and park

	# make the list in order of post time
	lowest_post = makeLowestPostWoodbine(tabledict)

	convertToPdf(lowest_post)
	convertToPdfTracksheet(lowest_post)
	# ---------------------------------

	sendEmail(os.environ[email])

