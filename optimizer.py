from pulp import *
import pandas as pd
import csv

day = '18'
month = '05'
year = '2021'

date = month + '-' + day + '-21'
slate = '14'

# Spelling Discrepencies
name_spelling = pd.read_csv('./Spelling/name_spelling.csv')
projections = pd.read_csv('./Data/' + date + '/' + slate + '/projections.csv')
projections_a = pd.read_csv('./Data/' + date + '/' + slate + '/projections_a.csv')

# import csv data
csv_dk = pd.read_csv('./Data/' + date + '/' + slate + '/DKSalaries.csv')
csv_starting_lineups = pd.read_csv('./Data/' + date + '/Lineups_' + year + '_' + month + '_' + day + '.csv')

# convert to dataframe
df_dk = pd.DataFrame(csv_dk)
df_lineups = pd.DataFrame(csv_starting_lineups)
df_name_spelling = pd.DataFrame(name_spelling)

# Projections
df_projections = pd.DataFrame(projections)
df_projections = df_projections[['Name','pj_vO']]

df_projections_a = pd.DataFrame(projections_a)
df_projections_a = df_projections_a[['Name','pj_vO']]

#re-organize data
new = df_dk['Roster Position'].str.split('/', n=1, expand=True)

df_dk['position_1'] = new[0]
df_dk['position_2'] = new[1]
df_dk.drop(columns=['Roster Position'], inplace = True)

df_lineups = df_lineups.rename(columns={' player name': 'Name'})
df_lineups = df_lineups.replace(list(df_name_spelling["BaseballMonster"]), list(df_name_spelling["DraftKings"]))

availables = pd.merge(df_lineups, df_dk, on='Name', how='inner')

pitcher = availables[(availables['position_1'] == 'P') | (availables['position_2'] == 'P')]
catcher = availables[(availables['position_1'] == 'C') | (availables['position_2'] == 'C')]
first = availables[(availables['position_1'] == '1B') | (availables['position_2'] == '1B')]
second = availables[(availables['position_1'] == '2B') | (availables['position_2'] == '2B')]
third = availables[(availables['position_1'] == '3B') |(availables['position_2'] == '3B') ]
short = availables[(availables['position_1'] == 'SS') | (availables['position_2'] == 'SS')]
outfield = availables[(availables['position_1'] == 'OF') | (availables['position_2'] == 'OF')]

projections = pd.merge(df_projections, availables, on='Name', how='inner')
projections_a = pd.merge(df_projections_a, availables, on='Name', how='inner')
# projections = pd.merge(df_projections, projections, on='Name', how='inner')

# print(projections_a)
# print(projections)


def optimize(pool, points, new_list):
	# Lists
	available_players = list(pool['Name'])
	points
	salaries = list(pool['Salary'])
	position_1 = list(pool['position_1'])
	position_2 = list(pool['position_2'])
	for v in pool.position_2.unique():
		if v is None:
			v = []

	# Dictionaries
	player_points = dict(zip(available_players, points))
	player_position_1 = dict(zip(available_players, position_1))
	player_position_2 = dict(zip(available_players, position_2))
	player_salary = dict(zip(available_players, salaries))

	# More Lists
	pitcher = []
	catcher = []
	first = []
	second = []
	third = []
	short = []
	outfield = []

	for v in player_position_1:
		if player_position_1[v] == 'P':
			pitcher.append(v)
		elif player_position_1[v] == 'C':
			catcher.append(v)
		if player_position_1[v] == '1B':
			first.append(v)
		elif player_position_1[v] == '2B':
			second.append(v)
		elif player_position_1[v] == '3B':
			third.append(v)
		elif player_position_1[v] == 'SS':
			short.append(v)
		elif player_position_1[v] == 'OF':
			outfield.append(v)

	for v in player_position_2:
		if player_position_2[v] == 'P':
			pitcher.append(v)
		elif player_position_2[v] == 'C':
			catcher.append(v)
		if player_position_2[v] == '1B':
			first.append(v)
		elif player_position_2[v] == '2B':
			second.append(v)
		elif player_position_2[v] == '3B':
			third.append(v)
		elif player_position_2[v] == 'SS':
			short.append(v)
		elif player_position_2[v] == 'OF':
			outfield.append(v)

	# Set the problem ?variable?
	prob = LpProblem('MLB', LpMaximize)

	# Set decision variables (problem variables?)
	use_vars = LpVariable.dicts('Start', available_players, 0,1,LpBinary)
	# use_vars = {k: LpVariable.dict(k, v, cat="Binary") for k, v in player_points.items()}

	# objective function
	SALARY_CAP = 50000

	dk_costs =[]
	dk_points = []

	dk_costs += lpSum(player_salary[v] * use_vars[v] for v in available_players)
	dk_points += lpSum(player_points[v] * use_vars[v] for v in available_players)

	prob += lpSum(dk_points)
	prob += lpSum(dk_costs) <= SALARY_CAP

	# constraints
	prob += lpSum(use_vars[v] for v in available_players) == 10
	prob += lpSum(use_vars[v] for v in pitcher) == 2
	prob += lpSum(use_vars[v] for v in catcher) == 1
	prob += lpSum(use_vars[v] for v in first) == 1
	prob += lpSum(use_vars[v] for v in second) == 1
	prob += lpSum(use_vars[v] for v in third) == 1
	prob += lpSum(use_vars[v] for v in short) == 1
	prob += lpSum(use_vars[v] for v in outfield) == 3

	prob.solve()
	print("Status: ", LpStatus[prob.status])
	print(value(prob.objective))

	# TOL = .00001

	# for i in available_players:
	#     if use_vars[i].varValue > TOL:
	#         print("Put into lineup", i)

	new_list

	print("Projected points", value(prob.objective))

	def summary(prob):
		div = '---------------------------------------\n'
		print("Variables:\n")
		score = str(prob.objective)
		constraints = [str(const) for const in prob.constraints.values()]
		for v in prob.variables():
			score = score.replace(v.name, str(v.varValue))
			constraints = [const.replace(v.name, str(v.varValue)) for const in constraints]
			if v.varValue != 0:
				print(v.name, "=", v.varValue)

				# to new_list
				new_list.append(v.name)



		print(div)
		print("Constraints:")
		for constraint in constraints:
		    constraint_pretty = " + ".join(re.findall("[0-9\.]*\*1.0", constraint))
		    if constraint_pretty != "":
		        print("{} = {}".format(constraint_pretty, eval(constraint_pretty)))
		print(div)
		print("Score:")
		score_pretty = " + ".join(re.findall("[0-9\.]+\*1.0", score))
		print("{} = {}".format(score_pretty, eval(score)))

		# to new_list
		new_list.append(eval(score))



		# # to lineups.csv
		# with open('./lineups.csv', 'r') as fp:
		# 	r = csv.reader(fp)

		#  * need blank row at bottom of csv
		with open('./Data/' + date + '/' + slate + '/lineups.csv', 'a') as f:
			wr = csv.writer(f)
			wr.writerow(new_list)


	summary(prob)


#### Strategies ####

# # APPGa
# points = list(availables['AvgPointsPerGame'])
# new_list = [date, 'APPGa']
# optimize(availables, points, new_list)
#
# # APPG
# points = list(projections['AvgPointsPerGame'])
# new_list = [date, 'APPG']
# optimize(projections, points, new_list)
#
# # pj_vO
# points = list(projections['pj_vO'])
# new_list = [date, 'pj_vO']
# optimize(projections, points, new_list)
#
# # pj_vOa
# points = list(projections_a['pj_vO'])
# new_list = [date, 'pj_vOa']
# optimize(projections_a, points, new_list)
#
# # APPGa 1-6
# availables = availables[availables[' batting order'] != '9']
# availables = availables[availables[' batting order'] != '8']
# availables = availables[availables[' batting order'] != '7']
# points = list(availables['AvgPointsPerGame'])
# new_list = [date, 'APPGa_1-6']
# optimize(availables, points, new_list)
#
# # APPG 1-6
# projections = projections[projections[' batting order'] != '9']
# projections = projections[projections[' batting order'] != '8']
# projections = projections[projections[' batting order'] != '7']
# points = list(projections['AvgPointsPerGame'])
# new_list = [date, 'APPG_1-6']
# optimize(projections, points, new_list)
#
# # pj_vO 1-6
# projections = projections[projections[' batting order'] != '9']
# projections = projections[projections[' batting order'] != '8']
# projections = projections[projections[' batting order'] != '7']
# points = list(projections['pj_vO'])
# new_list = [date, 'pj_vO_1-6']
# optimize(projections, points, new_list)
#
# # pj_vOa 1-6
# projections_a = projections_a[projections_a[' batting order'] != '9']
# projections_a = projections_a[projections_a[' batting order'] != '8']
# projections_a = projections_a[projections_a[' batting order'] != '7']
# points = list(projections_a['pj_vO'])
# new_list = [date, 'pj_vOa_1-6']
# optimize(projections_a, points, new_list)
#
# # APPGa 1-5
# availables = availables[availables[' batting order'] != '9']
# availables = availables[availables[' batting order'] != '8']
# availables = availables[availables[' batting order'] != '7']
# availables = availables[availables[' batting order'] != '6']
# points = list(availables['AvgPointsPerGame'])
# new_list = [date, 'APPGa_1-5']
# optimize(availables, points, new_list)

# APPG 1-5
projections = projections[projections[' batting order'] != '9']
projections = projections[projections[' batting order'] != '8']
projections = projections[projections[' batting order'] != '7']
projections = projections[projections[' batting order'] != '6']
points = list(projections['AvgPointsPerGame'])
new_list = [date, 'APPG_1-5']
optimize(projections, points, new_list)
#
# # pj_vO 1-5
# availables = availables[availables[' batting order'] != '9']
# availables = availables[availables[' batting order'] != '8']
# availables = availables[availables[' batting order'] != '7']
# projections = projections[projections[' batting order'] != '6']
# points = list(projections['pj_vO'])
# new_list = [date, 'pj_vO_1-5']
# optimize(projections, points, new_list)
#
# # pj_vOa 1-5
# projections_a = projections_a[projections_a[' batting order'] != '9']
# projections_a = projections_a[projections_a[' batting order'] != '8']
# projections_a = projections_a[projections_a[' batting order'] != '7']
# projections_a = projections_a[projections_a[' batting order'] != '6']
# points = list(projections_a['pj_vO'])
# new_list = [date, 'pj_vOa_1-5']
# optimize(projections_a, points, new_list)
#
# # APPGa 1-4
# availables = availables[availables[' batting order'] != '9']
# availables = availables[availables[' batting order'] != '8']
# availables = availables[availables[' batting order'] != '7']
# availables = availables[availables[' batting order'] != '6']
# availables = availables[availables[' batting order'] != '5']
# points = list(availables['AvgPointsPerGame'])
# new_list = [date, 'APPGa_1-4']
# optimize(availables, points, new_list)
#
# # APPG 1-4
# projections = projections[projections[' batting order'] != '5']
# points = list(projections['AvgPointsPerGame'])
# new_list = [date, 'APPG_1-4']
# optimize(projections, points, new_list)
#
# # pj_vO 1-4
# projections = projections[projections[' batting order'] != '5']
# points = list(projections['pj_vO'])
# new_list = [date, 'pj_vO_1-4']
# optimize(projections, points, new_list)
#
# # pj_vOa 1-4
# projections_a = projections_a[projections_a[' batting order'] != '5']
# points = list(projections_a['pj_vO'])
# new_list = [date, 'pj_vOa_1-4']
# optimize(projections_a, points, new_list)
#
# # APPGa 1-3
# availables = availables[availables[' batting order'] != '9']
# availables = availables[availables[' batting order'] != '8']
# availables = availables[availables[' batting order'] != '7']
# availables = availables[availables[' batting order'] != '6']
# availables = availables[availables[' batting order'] != '5']
# availables = availables[availables[' batting order'] != '4']
# points = list(availables['AvgPointsPerGame'])
# new_list = [date, 'APPGa_1-3']
# optimize(availables, points, new_list)
#
# # APPG 1-3
# projections = projections[projections[' batting order'] != '4']
# points = list(projections['AvgPointsPerGame'])
# new_list = [date, 'APPG_1-3']
# optimize(projections, points, new_list)
#
# # pj_vO 1-3
# projections = projections[projections[' batting order'] != '4']
# points = list(projections['pj_vO'])
# new_list = [date, 'pj_vO_1-3']
# optimize(projections, points, new_list)
#
# # pj_vOa 1-3
# projections_a = projections_a[projections_a[' batting order'] != '4']
# points = list(projections_a['pj_vO'])
# new_list = [date, 'pj_vOa_1-3']
# optimize(projections_a, points, new_list)
