import pandas as pd
import numpy as np


csv_dk = pd.read_csv('./Data/DKSalaries.csv')
csv_b_stats = pd.read_csv('./Data/FanGraphs Leaderboard.csv')
csv_starting_lineups = pd.read_csv('./Data/Lineups_2021_04_20.csv')

df_b_stats = pd.DataFrame(csv_b_stats)
df_dk = pd.DataFrame(csv_dk)
df_lineups = pd.DataFrame(csv_starting_lineups)


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

game_info = df_dk['Game Info'].str.split('@', n=1, expand=True)
df_dk['team_1'] = game_info[0]
df_dk['team_2'] = game_info[1]

team_2 = df_dk['team_2'].str.split(' ', n=1, expand=True)
df_dk['team_2'] = team_2[0]
df_dk['date/time'] = team_2[1]

df_dk['Opp'] = None

for i in df_dk.index:
    if df_dk['TeamAbbrev'][i] == df_dk['team_1'][i]:
        # print(df_dk.index)
        df_dk['Opp'][i] = df_dk['team_2'][i]
    else:
        df_dk['Opp'][i] = df_dk['team_1'][i]

df_dk['vSP'] = None

# display entire dataframe in console
pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
print(df_dk)