# https://stackoverflow.com/questions/66326293/python-pulp-positional-constraints-for-a-lineup-generator
from pulp import *
import pandas as pd
import csv

day = '24'
month = '04'
year = '2021'
date = '4-' + day + '-21'

# import past csv data
csv_dk = pd.read_csv('./PastData/' + date + '/DKSalaries.csv')
csv_b_stats = pd.read_csv('./PastData/' + date + '/br_b_stats.csv')
csv_p_stats = pd.read_csv('./PastData/' + date + '/br_p_stats.csv')
csv_t_stats = pd.read_csv('./PastData/' + date + '/br_t_stats.csv')
csv_starting_lineups = pd.read_csv('./PastData/' + date + '/Lineups_' + year + '_' + month + '_' + day + '.csv')

# # import current csv data
# csv_dk = pd.read_csv('./Data/DKSalaries.csv')
# starting_lineups = pd.read_csv('./Data/Lineups_2021_04_28.csv')
name_spelling = pd.read_csv('./Data/name_spelling.csv')
projections = pd.read_csv('./projections.csv')

# convert to dataframe
df_dk = pd.DataFrame(csv_dk)
df_lineups = pd.DataFrame(csv_starting_lineups)
df_name_spelling = pd.DataFrame(name_spelling)
# df_projections = pd.DataFrame(projections)
# df_projections = df_projections[['Name','pj_vO']]

#re-organize data
new = df_dk['Roster Position'].str.split('/', n=1, expand=True)

df_dk['position_1'] = new[0]
df_dk['position_2'] = new[1]
df_dk.drop(columns=['Roster Position'], inplace = True)

df_lineups = df_lineups.rename(columns={' player name': 'Name'})
df_lineups = df_lineups.replace(list(df_name_spelling["BaseballMonster"]), list(df_name_spelling["DraftKings"]))

availables = pd.merge(df_lineups, df_dk, on='Name', how='inner')
# availables = pd.merge(df_projections, availables, on='Name', how='inner')

pitcher = availables[(availables['position_1'] == 'P') | (availables['position_2'] == 'P')]
catcher = availables[(availables['position_1'] == 'C') | (availables['position_2'] == 'C')]
first = availables[(availables['position_1'] == '1B') | (availables['position_2'] == '1B')]
second = availables[(availables['position_1'] == '2B') | (availables['position_2'] == '2B')]
third = availables[(availables['position_1'] == '3B') |(availables['position_2'] == '3B') ]
short = availables[(availables['position_1'] == 'SS') | (availables['position_2'] == 'SS')]
outfield = availables[(availables['position_1'] == 'OF') | (availables['position_2'] == 'OF')]

# Lists
# positions = ['P', 'C', '1B', '2B', '3B', 'SS', 'OF']
positions = 10
available_players = list(availables['Name'])
points = list(availables['AvgPointsPerGame'])
# points = list(availables['pj_vO'])
salaries = list(availables['Salary'])
position_1 = list(availables['position_1'])
position_2 = list(availables['position_2'])
# num_available = list(availables[' game_number'])
for v in availables.position_2.unique():
	if v is None:
		v = []

# Dictionaries
# player_num_available = dict(zip(available_players, num_available))
player_points = dict(zip(available_players, points))
positions = list(zip(position_1, position_2))
# player_position_2 = dict(zip(available_players, position_2))
player_salary = dict(zip(available_players, salaries))
roster_spots = {'P', 'C', '1B', '2B', '3B', 'SS', 'OF'}

player_positions = dict(zip(available_players, positions))

for player in player_positions:
	set_pos = set(player_positions[player])
	player_positions[player] = set_pos

legal_assignments_set = { (k,v) for k in player_positions.keys() for v in player_positions[k]}

print(legal_assignments_set)

# # More Lists
# pitcher = []
# catcher = []
# first = []
# second = []
# third = []
# short = []
# outfield = []
#
# for v in player_position_1:
# 	if player_position_1[v] == 'P':
# 		pitcher.append(v)
# 	elif player_position_1[v] == 'C':
# 		catcher.append(v)
# 	if player_position_1[v] == '1B':
# 		first.append(v)
# 	elif player_position_1[v] == '2B':
# 		second.append(v)
# 	elif player_position_1[v] == '3B':
# 		third.append(v)
# 	elif player_position_1[v] == 'SS':
# 		short.append(v)
# 	elif player_position_1[v] == 'OF':
# 		outfield.append(v)
#
# for v in player_position_2:
# 	if player_position_2[v] == 'P':
# 		pitcher.append(v)
# 	elif player_position_2[v] == 'C':
# 		catcher.append(v)
# 	if player_position_2[v] == '1B':
# 		first.append(v)
# 	elif player_position_2[v] == '2B':
# 		second.append(v)
# 	elif player_position_2[v] == '3B':
# 		third.append(v)
# 	elif player_position_2[v] == 'SS':
# 		short.append(v)
# 	elif player_position_2[v] == 'OF':
# 		outfield.append(v)
#
# # print(pitcher)
# # print(catcher)
# # print(first)
# # print(second)
# # print(third)
# # print(short)
# # print(outfield)
#
# Set the problem variable
prob = LpProblem('MLB', LpMaximize)
#
# # Set decision variables
# use_vars = LpVariable.dicts('Start', available_players, 0,1,LpBinary)
# # use_vars = {k: LpVariable.dict(k, v, cat="Binary") for k, v in player_points.items()}
#
# # objective function
# SALARY_CAP = 50000
#
# dk_costs =[]
# dk_points = []
#
# dk_costs += lpSum(player_salary[v] * use_vars[v] for v in available_players)
# dk_points += lpSum(player_points[v] * use_vars[v] for v in available_players)
#
# prob += lpSum(dk_points)
# prob += lpSum(dk_costs) <= SALARY_CAP
#
# # for v in use_vars:
# # 	print(use_vars[v])
# # for v in outfield:
# # 	print(v)
#
# # constraints
# # prob += lpSum(use_vars[v] for v in available_players) == 10
# prob += lpSum(use_vars[v] for v in pitcher) == 2
# prob += lpSum(use_vars[v] for v in catcher) == 1
# prob += lpSum(use_vars[v] for v in first) == 1
# prob += lpSum(use_vars[v] for v in second) == 1
# prob += lpSum(use_vars[v] for v in third) == 1
# prob += lpSum(use_vars[v] for v in short) == 1
# prob += lpSum(use_vars[v] for v in outfield) == 3
#
# # solver = pulp.GLPK(msg=0)
# # solver = pulp.CPLEX(msg=0)
#
# prob.solve()
# print("Status: ", LpStatus[prob.status])
# print(value(prob.objective))
#
# # print(prob)
#
# # TOL = .00001
#
# # for i in available_players:
# #     if use_vars[i].varValue > TOL:
# #         print("Put into lineup", i)
#
# # appg = [date, 'APPG']
# # pj_vO = [date, 'pj_vO']
#
#
#
# print("Projected points", value(prob.objective))
#
# def summary(prob):
# 	div = '---------------------------------------\n'
# 	print("Variables:\n")
# 	score = str(prob.objective)
# 	constraints = [str(const) for const in prob.constraints.values()]
# 	for v in prob.variables():
# 		score = score.replace(v.name, str(v.varValue))
# 		constraints = [const.replace(v.name, str(v.varValue)) for const in constraints]
# 		if v.varValue != 0:
# 			print(v.name, "=", v.varValue)
#
# 			# to list
# 			# appg.append(v.name)
# 			# pj_vO.append(v.name)
#
# 	# # to lineups.csv
# 	# with open('./lineups.csv', 'r') as fp:
# 	# 	r = csv.reader(fp)
# 	#
# 	# 	# need blank row at bottom of csv
# 	# 	with open('./lineups.csv', 'a') as fp:
# 	# 		wr = csv.writer(fp)
# 	# 		for row in r:
# 	# 			wr.writerow(appg)
# 	# 			# wr.writerow(pj_vO)
# 	print(div)
# 	print("Constraints:")
# 	for constraint in constraints:
# 	    constraint_pretty = " + ".join(re.findall("[0-9\.]*\*1.0", constraint))
# 	    if constraint_pretty != "":
# 	        print("{} = {}".format(constraint_pretty, eval(constraint_pretty)))
# 	print(div)
# 	print("Score:")
# 	score_pretty = " + ".join(re.findall("[0-9\.]+\*1.0", score))
# 	print("{} = {}".format(score_pretty, eval(score)))
#
# summary(prob)
