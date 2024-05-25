import requests
from bs4 import BeautifulSoup


def timeToDec(time):
	# in format #:## a.m.
	firstBit = True
	hour = ""
	minute = ""
	for letter in time:
		if letter == ":":
			firstBit = False
			continue
		if letter == "a":
			break
		elif letter == "p":
			if time[0] + time[1] == '12':
				hour = int(hour)
				break
			hour = int(hour) + 12
			break

		if firstBit:
			hour = hour + letter
		else:
			minute = minute + letter

	print("input =", time, "output =", int(hour) + int(minute) / 60)
	return int(hour) + int(minute) / 60


def timeToDecMixed(time):
	"""convert a post time obtained from woodbine"""
	# in format #:## a.m.
	# or format ~#:## p.m.

	if time[0] == "~":
		return timeToDec(time[1:])  # since in RTN format use original timeToDec fn

	split_time = time.split(" ")
	time_to_add = 0

	# go through number and convert to decimal
	first_bit = True
	hour = ""
	minute = ""
	for letter in split_time[0]:
		if letter == ":":
			first_bit = False
			continue

		if first_bit:
			hour = hour + letter
		else:
			minute = minute + letter

	if split_time[1] == "PM":
		if split_time[0][0] + split_time[0][1] == '12':
			hour = int(hour)
		else:
			hour = int(hour) + 12

	print("input =", time, "output =", int(hour) + int(minute) / 60)
	return int(hour) + int(minute) / 60


def sortKey(list_object):
	return list_object[2]


def getRTN():
	res = requests.get("https://www.rtn.tv/schedule/schedule.aspx", timeout=(3, 27))
	if res.status_code != 200:
		print("error")
		return -1
	# print(res.text)
	soup = BeautifulSoup(res.text, 'html.parser')
	return soup.find(class_='scheduleContainer')


def makeLowestPostList(tabledict):
	lowest_post = []
	for key in tabledict:
		lowest_post.append([key, tabledict[key][0], tabledict[key][1], tabledict[key][2], ])

	lowest_post.sort(key=sortKey)
	return lowest_post


def generateDict(table):
	"""takes in a BS4 object and returns a dictionary based off the scraped
	information"""
	ourlist = table.find_all("tr")
	tabledict = {}
	for item in ourlist[1:-1]:
		# skip first and last line
		column = item.find_all("td")
		# dict[track name] = [RTN#, start_time, duration]
		# test for duplicate name
		# if tabledict.has_key(column[1].text.replace(' (HD)','')):
		# 	tabledict[column[1].text.replace(' (HD)',' 2')] = \
		# 	[column[0].text[2:4], #RTN
		# 	column[2].text, 	  #start_time
		# 	column[3].text]		  #duration
		# else:
		tabledict[column[1].text.replace(' (HD)', '')] = \
			[column[0].text[2:4],  # RTN
			 column[2].text,  # start_time
			 column[3].text]  # duration

	return tabledict


if __name__ == "__main__":
	print(timeToDecMixed("13:10 PM"))