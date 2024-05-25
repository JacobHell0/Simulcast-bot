my_list = ['Georgian', "Harrah's Philadelphia", 'Hippodrome Trois Rivieres', 'Pocono', 'Northfield', 'Ocean', 'Running Aces', 'Saratoga Harness', 'Tioga', 'Eldorado Scioto', 'Harrington Raceway', 'Hoosier', 'Monticello Raceway', 'Plainridge Casino', 'Red Mile', 'Woodbine Mohawk', 'Yonkers Raceway', 'Ellis Park', 'Arapahoe', 'Canterbury', 'Del Mar', 'Emerald', 'Fort Erie', 'Gulfstream', 'Hastings Racecourse', 'Hawthorne', 'Laurel', 'Los Alamitos', 'Louisiana', 'Monmouth', 'Mountaineer', 'Prairie Meadows', 'Ruidoso', 'Saratoga', 'Woodbine', 'Assiniboia', 'Belterra', 'Finger Lakes', 'Thistledown', 'Presque Isle']

harn = ['Georgian', "Harrah's Philadelphia", 'Hippodrome Trois Rivieres', 'Pocono', 'Northfield', 'Ocean', 'Running Aces', 'Saratoga Harness', 'Tioga', 'Eldorado Scioto', 'Harrington Raceway', 'Hoosier', 'Monticello Raceway', 'Plainridge Casino', 'Red Mile', 'Woodbine Mohawk', 'Yonkers Raceway']

thor = ['Ellis Park', 'Arapahoe', 'Canterbury', 'Del Mar', 'Emerald', 'Fort Erie', 'Gulfstream', 'Hastings Racecourse', 'Hawthorne', 'Laurel', 'Los Alamitos', 'Louisiana', 'Monmouth', 'Mountaineer', 'Prairie Meadows', 'Ruidoso', 'Saratoga', 'Woodbine', 'Assiniboia', 'Belterra', 'Finger Lakes', 'Thistledown', 'Presque Isle']

def main():
	
	for item in my_list:
		if (item in harn) or (item in thor):
			continue
		val = input("is " + item + ' T or H: ')
		if val.lower() == 't':
			thor.append(item)
		elif val.lower() == 'h':
			harn.append(item)

	print("harness")
	harn.sort()
	print(harn)
	print("thor")
	thor.sort()
	print(thor)
	print("true if the lists contain no duplicates")
	joinedlist = thor + harn
	print(len(joinedlist) == len(set(joinedlist)))
	return
main()