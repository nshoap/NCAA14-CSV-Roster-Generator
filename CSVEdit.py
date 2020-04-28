import csv

from pathlib import Path
import random
import math

path_string = input("Please put the path of the .csv file you wish to edit: \n")
output_string = input("Please put the path of the .csv file you wish to output to: \n")
#If the user pastes a path with quotes, such as "C:\User\Desktop\test.csv", Path errors; removing the "" fixes this.
path_string = path_string.replace('"', '')
output_string = output_string.replace('"', '')

data = Path(path_string)
output = Path(output_string)

#All the rows from the .csv file are inserted into stored_data
stored_data = []

#The first row, or stored_data[column_row], is inserted into columns; this row is generally the dict row in most files that I know of.
columns = []
column_row = 0

teams = []
team_ratings = {}

#This is things like speed, accelerations, strength, etc.  This is just in case we need to generate these seperately from skill attributes.
physical_attributes = ['PSPD', 'PACC', 'PAGI', 'PSTA', 'PSTR', 'PJMP']

attributes = ['PESV', 'PSMV', 'PPMV', 'PJMV', 'PFMV', 'PZCV', 'PMCV', 'PBCV', 'PKRT', 'PHIT', 'SPCT', 'PYRS', 'PPRS', 'RELS', 'PAWR', 'PRTR', 'PKPR', 'PSAR', 'PCAR', 'PTHP', 'PIBL', 'PBTK', 'PTRK', 'PRBK', 'PPBK', 'PTAK', 'PCTH', 'PBSH', 'TRAF', 'PPRC', 'PKAC', 'PTHA']

TGID = 0



def createTeamRatings():
	print("Teams remaining:", teams)


	for six_star_team in range(0,8):
		team_id = teams[random.randint(0,len(teams)-1)]
		team_ratings[team_id] = 6
		print("Team:", team_id, " has been chosen to be a six star team!")
		teams.remove(team_id)
		print("Teams remaining:", teams)

	for five_star_team in range(0,16):
		team_id = teams[random.randint(0,len(teams)-1)]
		team_ratings[team_id] = 5
		print("Team:", team_id, " has been chosen to be a five star team!")
		teams.remove(team_id)
		print("Teams remaining:", teams)

	for four_star_team in range(0,32):
		team_id = teams[random.randint(0,len(teams)-1)]
		team_ratings[team_id] = 4
		print("Team:", team_id, " has been chosen to be a four star team!")
		teams.remove(team_id)
		print("Teams remaining:", teams)

	for three_star_team in range(0,32):
		team_id = teams[random.randint(0,len(teams)-1)]
		team_ratings[team_id] = 3
		print("Team:", team_id, " has been chosen to be a three star team!")
		teams.remove(team_id)
		print("Teams remaining:", teams)

	for two_star_team in range(0,20):
		team_id = teams[random.randint(0,len(teams)-1)]
		team_ratings[team_id] = 2
		print("Team:", team_id, " has been chosen to be a two star team!")
		teams.remove(team_id)
		print("Teams remaining:", teams)

	for one_star_team in range(0,18):
		team_id = teams[random.randint(0,len(teams)-1)]
		team_ratings[team_id] = 1
		print("Team:", team_id, " has been chosen to be a one star team.  Sorry :(")
		teams.remove(team_id)
		print("Teams remaining:", teams)

	print("Teams remaining:", teams)

def findDictPosition(text):
	for pos in range(0, len(columns)-1):
		if (columns[pos] == text):
			return pos

#with open(data, newline='') as csvfile:
def tempMethod():

	csv_read = csv.reader(open(data))
	stored_data = list(csv_read)

	#If the .csv file is exported by 'NCAA Dynasty Editor', row 0 has the column names.  If it is exported by 'EA DB Editor', it will be row 1 provided row 0 is a key row.
	if (stored_data[0][0] == 'BSAA'):
		column_row = 0
	elif (stored_data[1][0] == 'BSAA'):
		column_row = 1

	#Add the columns to the columns list, print them out to the user so the user knows what dicts are available to modify, also sets TGID.
	for column in stored_data[column_row]:
		if (column == 'TGID'):
			TGID = len(columns)
		columns.insert(len(columns), column)

	#Adds all the teams to an array for later use.	
	for row in stored_data:
		if (row != stored_data[0] and row != stored_data[column_row]):
			found = False

			for team in teams:
				if (team == row[TGID]):
					found = True

			if (not found):
				teams.insert(len(teams), row[TGID])
				print("Adding team:", row[TGID])

	print(len(teams)-1, " teams")

	#Creates team ratings
	createTeamRatings()

	for player in stored_data:
		if (player != stored_data[0] and player != stored_data[column_row]):
			p_TGID = player[findDictPosition('TGID')]
			p_OVR = findDictPosition('POVR')
			p_total_points = 0
			p_total_attributes = 0
			star = team_ratings[p_TGID]

			for attribute in physical_attributes:
				column = findDictPosition(attribute)
				player[column] = (40 + (star * 9) + random.randint(-5,5))
				p_total_points = p_total_points + player[column]
				p_total_attributes = p_total_attributes + 1

			for attribute in attributes:
				column = findDictPosition(attribute)
				player[column] = (40 + (star * 9) + random.randint(-5,5))
				p_total_points = p_total_points + player[column]
				p_total_attributes = p_total_attributes + 1

			player[p_OVR] = round(p_total_points / p_total_attributes)
			print(player[findDictPosition('PFNA')], player[findDictPosition('PLNA')], "for team", p_TGID, " is rated", player[p_OVR])


	ready = input("Ready?")



	#Prints out the created dicts.
	#print("Dicts loaded from .csv file:", columns)

	'''
	This is for manually modifying the roster, which I no longer intend to do.


	def modifyDict(current_dict):
		if (current_dict.lower() != 'done'):
			print("Selected:", current_dict)
			column = 0

			for x in columns:
				if (x == current_dict):
					print("Found!")
					break
				column = column + 1

			change = input("Input a value to change this dict to: (ex. 40 for default bad rating)")

			for row in stored_data:
				if (row != stored_data[column_row]):
					row[column] = change
					print(row)

			next_dict = input("Select a dict to modify: (type 'done' to stop)")
			modifyDict(next_dict)


	selected_dict = input("Select a dict to modify: (type 'done' to stop)")
	modifyDict(selected_dict)
	'''

	csv_write = csv.writer(open(output, 'w', newline=''))
	csv_write.writerows(stored_data)

tempMethod()