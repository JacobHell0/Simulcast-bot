import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

def getDate():
	# returns the current day and month in the format (day, month) (int, int)
	dt = datetime.now(timezone('EST'))
	return(dt.day, dt.month)

def getCurrentCol(tables):
	""" searches through the different tables to find the tracklist for the current day.
	returns a tuple of the tables index and column number -> (table_index, column num)"""

	# load dictionary that contains month to day

	month_to_num = {
		"Jan" : 1,
		"Feb" : 2,
		"Mar" : 3,
		"Apr" : 4,
		"May" : 5,
		"Jun" : 6,
		"Jul" : 7,
		"Aug" : 8,
		"Sep" : 9,
		"Oct" : 10,
		"Nov" : 11,
		"Dec" : 12,
	}
	
	current_date = getDate()  # in format (day, month)

	# the first table is garbage, skip
	# table 1 is week 1, table 2 is week 2, etc...

	# init i and j to keep track of the table and column
	i, j = (0, 0)

	for table in tables[1:]:
		columns = table.find("thead").find_all("th")
		for column in columns:
			# print(column)
			# for each th element
			date = column.text.split() 
			# date is in format [weekday name, month, day]
			# print(date)

			# check if the table is current day
			# print(f"checking: {int(date[2])} vs {current_date[0]}", end = " ")
			# print(f"and {month_to_num[date[1]]} vs {current_date[1]}")

			if(int(date[2]) == current_date[0] and month_to_num[date[1]] == current_date[1]):
				return i + 1, j  # +1 because we ignore first table
			j += 1
		i += 1
		j = 0


def getPostFromTBody(tables, index):
	tracks = tables[index[0]].find("tbody").find_all("td")[index[1]].text.split("\n")
	return_dict = {}
	
	# seperate the time, post time, and name with string manipulation
	for track in tracks:
		if track == '':
			continue
		TB_or_H = track[-3:-1]
		track = track[:-3] #strip the TB or SB off

		#take first 2 words, this may solve your dictionary issue
		temp_track_name = track.split()[2:4]
		track_name = " ".join(temp_track_name)

		#finally the fabled post time, must convert to format that looks good in table
		temp_post_time = track.split()[0:2]

		#interpret the first entry as a number and subtract 12 from it
		if int(temp_post_time[0][:2]) >= 13:
			temp_post_time[0] = str(int(temp_post_time[0][:2]) - 12) + temp_post_time[0][2:]

		post_time = (" ".join(temp_post_time))	

		# create dictionary in format {track : [post_time, TB or SB]}
		if track_name not in return_dict:
			return_dict[track_name] = [post_time, TB_or_H]

	return return_dict


def grabPost():
	# go to here https://woodbine.com/simulcasts/
	# and grab post times, return a dictionary in format: 
	# {track : [post_time, TB or SB],
	#  track : [post_time, TB or SB]} etc...

	res = requests.get("https://woodbine.com/simulcasts/")

	print(res)
	if res.status_code != 200:
	  print("error")
	  return -1

	soup = BeautifulSoup(res.text, 'html.parser')
	# table = soup.find_all("table", id="simulcast")
	# print(table)
	tables = soup.find_all('table')


	# find current day and month in table by searching through the Thead elements
	# honestly, it is safer to just search them all because I don't want to risk a really obscure bug
	index = getCurrentCol(tables) #index will be in format (table, column)

	# now go to the table and column in the <tr> element and grab the post times
	return getPostFromTBody(tables, index)
	

if __name__ == "__main__":
	print("track list: ")
	result = grabPost()
	print(result)
	for track in result:
		print(track)