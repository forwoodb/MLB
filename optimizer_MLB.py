from pulp import *
import pandas as pd

# import csv data
data = pd.read_csv('./Data/DKSalaries.csv')
starting_lineups = pd.read_csv('./Data/Lineups_2021_04_20.csv')
name_spelling = pd.read_csv('./Data/name_spelling.csv')

# convert to dataframe
df_dk = pd.DataFrame(data)
df_lineups = pd.DataFrame(starting_lineups)
df_name_spelling = pd.DataFrame(name_spelling)

#re-organize data
new = df_dk['Roster Position'].str.split('/', n=1, expand=True)

df_dk['position_1'] = new[0]
df_dk['position_2'] = new[1]
df_dk.drop(columns=['Roster Position'], inplace = True)

df_lineups = df_lineups.rename(columns={' player name': 'Name'})

availables = pd.merge(df_lineups, df_dk, on='Name', how='inner')

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
# num_available = list(availables[' game_number'])
points = list(availables['AvgPointsPerGame'])
salaries = list(availables['Salary'])
position_1 = list(availables['position_1'])
position_2 = list(availables['position_2'])
for v in availables.position_2.unique():
	if v is None:
		v = []

# Dictionaries
# player_num_available = dict(zip(available_players, num_available))
player_points = dict(zip(available_players, points))
player_position_1 = dict(zip(available_players, position_1))
player_position_2 = dict(zip(available_players, position_2))
player_salary = dict(zip(available_players, salaries))
# roster_spots = {
# 	'P': 2,
# 	'C': 1,
# 	'1B': 1,
# 	'2B': 1,
# 	'3B': 1,
# 	'SS': 1,
# 	'OF': 3
# }

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
# Set the problem variable
prob = LpProblem('MLB', LpMaximize)

# Set decision variables
use_vars = LpVariable.dicts('Start', available_players, 0,1,LpBinary)

# objective function
SALARY_CAP = 50000

dk_costs =[]
dk_points = []

dk_costs += lpSum(player_salary[v] * use_vars[v] for v in available_players)
dk_points += lpSum(player_points[v] * use_vars[v] for v in available_players)

prob += lpSum(dk_points)
prob += lpSum(dk_costs) <= SALARY_CAP

# constraints
prob += lpSum(use_vars[v] for v in pitcher) == 2
prob += lpSum(use_vars[v] for v in catcher) == 1
prob += lpSum(use_vars[v] for v in first) == 1
prob += lpSum(use_vars[v] for v in second) == 1
prob += lpSum(use_vars[v] for v in third) == 1
prob += lpSum(use_vars[v] for v in short) == 1
prob += lpSum(use_vars[v] for v in outfield) == 3

print(pitcher)

prob.solve()
print("Status: ", LpStatus[prob.status])
print(value(prob.objective))


# TOL = .00001
#
# # for i in available_players:
# #     if use_vars[i].varValue > TOL:
# #         print("Put into lineup", i)
#
# for v in prob.variables():
#     if v.varValue != 0:
#         print(v.name, "=", v.varValue)
#
# print("Projected points", value(prob.objective))

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

summary(prob)
