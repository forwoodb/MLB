import pandas as pd
import numpy as np


csv_dk = pd.read_csv('./Data/DKSalaries.csv')
csv_b_stats = pd.read_csv('./Data/br_b_stats.csv')
csv_p_stats = pd.read_csv('./Data/br_p_stats.csv')
csv_starting_lineups = pd.read_csv('./Data/Lineups_2021_04_23.csv')
csv_name_spelling = pd.read_csv('./Data/name_spelling.csv')
csv_team_abbr = pd.read_csv('./Data/team_abb.csv')

df_b_stats = pd.DataFrame(csv_b_stats)
df_p_stats = pd.DataFrame(csv_p_stats)
df_dk = pd.DataFrame(csv_dk)
df_lineups = pd.DataFrame(csv_starting_lineups)
df_name_spelling = pd.DataFrame(csv_name_spelling)
df_team_abbr = pd.DataFrame(csv_team_abbr)

df_lineups = df_lineups.rename(columns={' player name': 'Name'})
df_lineups = df_lineups.replace(list(df_name_spelling["BaseballMonster"]), list(df_name_spelling["DraftKings"]))
df_lineups = df_lineups.replace(list(df_team_abbr["BaseballMonster"]), list(df_team_abbr["DraftKings"]))

availables = pd.merge(df_lineups, df_dk, on='Name', how='inner')

# Batting Stats
singles = ((df_b_stats['H']-df_b_stats['2B']-df_b_stats['3B']-df_b_stats['HR']) * 3)/df_b_stats['G']
doubles = (df_b_stats['2B'] * 5)/df_b_stats['G']
triples = (df_b_stats['3B'] * 8)/df_b_stats['G']
home_runs = (df_b_stats['HR'] * 10)/df_b_stats['G']
RBIs = (df_b_stats['RBI'] * 2)/df_b_stats['G']
runs = (df_b_stats['R'] * 2)/df_b_stats['G']
walks = (df_b_stats['BB'] * 2)/df_b_stats['G']
HBP = (df_b_stats['HBP'] * 2)/df_b_stats['G']
stolen_bases = (df_b_stats['SB'] * 5)/df_b_stats['G']

proj_pts = (singles + doubles + triples + home_runs + RBIs + runs + walks + HBP + stolen_bases)
df_b_stats['proj_pts'] = round(proj_pts, 2)
df_b_stats.sort_values(by=['proj_pts'], inplace=True, ascending=False)

# # Starting Pitcher Factors for Batting
df_p_stats.drop(df_p_stats.tail(1).index,inplace=True)
name = df_p_stats['Name'].str.split('\\', n=1, expand=True)
# name = df_p_stats['Name'].replace('*', '_')
df_p_stats['Name'] = name[0]
factors = df_p_stats[['Name','IP','H']]
lg_innings_pitched = factors['IP'].sum()
lg_hits_allowed = factors['H'].sum()
hits_ip = factors['H']/factors['IP']
factors.insert(3, 'h_factor', round(hits_ip, 2))
print(factors)
# print(hits_allowed)
#
# #Starting Pitcher Stats
#
# game_info = availables['Game Info'].str.split('@', n=1, expand=True)
# availables['team_1'] = game_info[0]
# availables['team_2'] = game_info[1]
#
# team_2 = availables['team_2'].str.split(' ', n=1, expand=True)
# availables['team_2'] = team_2[0]
# availables['date/time'] = team_2[1]
#
# availables['Opp'] = None
#
# for i in availables.index:
#     if availables['TeamAbbrev'][i] == availables['team_1'][i]:
#         availables['Opp'][i] = availables['team_2'][i]
#     else:
#         availables['Opp'][i] = availables['team_1'][i]
#
# starting_pitchers = {}
# for pos in availables[' batting order'].unique():
#     if pos == 'SP':
#         availables_sp = availables[availables[' batting order'] == pos]
#         starting_pitchers = list(availables_sp[['TeamAbbrev', 'Name']].set_index('TeamAbbrev').to_dict().values())[0]
#
# print(starting_pitchers)
# availables['vSP'] = None
#
# for i in availables.index:
#     # availables['vSP'] =
#     for j in starting_pitchers:
#         if availables['Opp'][i] == j:
#             availables['vSP'][i] = starting_pitchers[j]
#
#
# # for i in availables.index:
# #     availables['vSP'][i] = availables['Opp'][i]
# #
# # for i in availables.index:
# #     if availables['Opp'][i] == 'DET':
# #         availables['vSP'][i] ==
# # for team in availables['team_1']:
# #     for i in availables.index:
# #         if team == availables['team code'][i]:
# #             availables['team code'][i]
#             # vSP = availables['team code'][i]
#     # availables['vSP'][i] = availables['team code']
#     # if availables['team code'][j] == availables['Opp'][i]:
#     #     availables['vSP'][i] == availables['team code'][j]
#     # availables['Opp'][i]].isin(availables['team code'])
#     # if df_lineups['team code'][i] == availables['Opp'][i]:
#     #     availables['vSP'][i] = df_lineups['team code'][i]
#
#
# # display entire dataframe in console
# pd.set_option('display.max_rows', None)
# # pd.set_option('display.max_columns', None)
# print(availables)