import pandas as pd
import numpy as np
import re

# Import data.
csv_dk = pd.read_csv('./Data/DKSalaries.csv')
csv_b_stats = pd.read_csv('./Data/br_b_stats.csv')
csv_p_stats = pd.read_csv('./Data/br_p_stats.csv')
# csv_t_stats = pd.read_csv('./Data/br_p_stats.csv')
csv_starting_lineups = pd.read_csv('./Data/Lineups_2021_04_24.csv')
csv_name_spelling = pd.read_csv('./Data/name_spelling.csv')
csv_team_abbr = pd.read_csv('./Data/team_abb.csv')

# Convert to dataframes.
df_b_stats = pd.DataFrame(csv_b_stats)
df_p_stats = pd.DataFrame(csv_p_stats)
# df_t_stats = pd.DataFrame(csv_t_stats)
df_dk = pd.DataFrame(csv_dk)
df_lineups = pd.DataFrame(csv_starting_lineups)
df_name_spelling = pd.DataFrame(csv_name_spelling)
df_team_abbr = pd.DataFrame(csv_team_abbr)

# Clean up lineup data.
df_lineups = df_lineups.rename(columns={' player name': 'Name'})
df_lineups = df_lineups.rename(columns={' batting order': 'b_o'})
df_lineups = df_lineups.rename(columns={'team code': 'team'})
df_lineups = df_lineups.replace(list(df_name_spelling["BaseballMonster"]), list(df_name_spelling["DraftKings"]))
df_lineups = df_lineups.replace(list(df_team_abbr["BaseballMonster"]), list(df_team_abbr["DraftKings"]))

# # Batting Stats
df_b_stats.drop(df_b_stats.tail(1).index,inplace=True)
name = df_b_stats['Name'].str.split('\*|\#', n=1, expand=True)
name = name[0].str.split('\\', n=1, expand=True)
df_b_stats['Name'] = name[0]

df_dk = df_dk[['Name','Game Info','TeamAbbrev','AvgPointsPerGame']]
df_dk = df_dk.rename(columns={'TeamAbbrev': 'TmAbb','AvgPointsPerGame': 'APPG'})
df_lineups = df_lineups[['team','Name','b_o']]
df_b_stats = df_b_stats[['Name','G','H','2B','3B','HR','BB','R','RBI','HBP','SB']]

df_b_stats = df_b_stats.replace(list(df_team_abbr["BaseballReference"]), list(df_team_abbr["DraftKings"]))
df_b_stats = df_b_stats.replace(list(df_name_spelling["BaseballReference"]), list(df_name_spelling["DraftKings"]))

df_dk = pd.merge(df_lineups, df_dk, on='Name', how='inner')
df_dk = pd.merge(df_dk, df_b_stats, on='Name', how='inner')

# DraftKings Batting Stats
singles = ((df_dk['H']-df_dk['2B']-df_dk['3B']-df_dk['HR']) * 3)/df_dk['G']
doubles = (df_dk['2B'] * 5)/df_dk['G']
triples = (df_dk['3B'] * 8)/df_dk['G']
home_runs = (df_dk['HR'] * 10)/df_dk['G']
RBIs = (df_dk['RBI'] * 2)/df_dk['G']
runs = (df_dk['R'] * 2)/df_dk['G']
walks = (df_dk['BB'] * 2)/df_dk['G']
HBP = (df_dk['HBP'] * 2)/df_dk['G']
stolen_bases = (df_dk['SB'] * 5)/df_dk['G']

df_dk['H'] = round(singles, 2)
df_dk['2B'] = round(doubles, 2)
df_dk['3B'] = round(triples, 2)
df_dk['HR'] = round(home_runs, 2)
df_dk['RBI'] = round(RBIs, 2)
df_dk['R'] = round(runs, 2)
df_dk['BB'] = round(walks, 2)
df_dk['HBP'] = round(HBP, 2)
df_dk['SB'] = round(stolen_bases, 2)

proj_pts = (singles + doubles + triples + home_runs + RBIs + runs + walks + HBP + stolen_bases)
df_dk['pj_pts'] = round(proj_pts, 2)

# # Starting Pitcher Factors for Batting
df_p_stats.drop(df_p_stats.tail(1).index,inplace=True)
name = df_p_stats['Name'].str.split('*', n=1, expand=True)
name = name[0].str.split('\\', n=1, expand=True)
df_p_stats['Name'] = name[0]

df_p_stats = df_p_stats[['Name','IP','H','HR','R','BB']]

lg_innings_pitched = df_p_stats['IP'].sum()

lg_hits_allowed = df_p_stats['H'].sum() - df_p_stats['HR'].sum()
lg_hits_ip = lg_hits_allowed/lg_innings_pitched
hits_ip = (df_p_stats['H'] - df_p_stats['HR'])/df_p_stats['IP']
hits_fac = hits_ip/lg_hits_ip
df_p_stats.insert(3, 'h_fac', round(hits_fac, 2))

lg_hr_allowed = df_p_stats['HR'].sum()
lg_hr_ip = lg_hr_allowed/lg_innings_pitched
hr_ip = df_p_stats['HR']/df_p_stats['IP']
hr_fac = hr_ip/lg_hr_ip
df_p_stats.insert(5, 'hr_fac', round(hr_fac, 2))

lg_r_allowed = df_p_stats['R'].sum()
lg_r_ip = lg_r_allowed/lg_innings_pitched
r_ip = df_p_stats['R']/df_p_stats['IP']
r_fac = r_ip/lg_r_ip
df_p_stats.insert(7, 'r_fac', round(r_fac, 2))

lg_bb_allowed = df_p_stats['BB'].sum()
lg_bb_ip = lg_bb_allowed/lg_innings_pitched
bb_ip = df_p_stats['BB']/df_p_stats['IP']
bb_fac = bb_ip/lg_bb_ip
df_p_stats.insert(9, 'bb_fac', round(bb_fac, 2))

#Starting Pitcher Stats
game_info = df_dk['Game Info'].str.split('@', n=1, expand=True)
df_dk['team_1'] = game_info[0]
df_dk['team_2'] = game_info[1]
#
team_2 = df_dk['team_2'].str.split(' ', n=1, expand=True)
df_dk['team_2'] = team_2[0]
df_dk.drop(columns=['Game Info'], inplace=True)

df_dk['Opp'] = None

for i in df_dk.index:
    if df_dk['TmAbb'][i] == df_dk['team_1'][i]:
        df_dk['Opp'][i] = df_dk['team_2'][i]
    else:
        df_dk['Opp'][i] = df_dk['team_1'][i]

starting_pitchers = {}
for pos in df_dk['b_o'].unique():
    if pos == 'SP':
        availables_sp = df_dk[df_dk['b_o'] == pos]
        starting_pitchers = list(availables_sp[['TmAbb', 'Name']].set_index('TmAbb').to_dict().values())[0]

# pd.set_option('display.max_rows', None)
# print(df_dk)

df_dk['vSP'] = None
#
for i in df_dk.index:
    for j in starting_pitchers:
        if df_dk['Opp'][i] == j:
            df_dk['vSP'][i] = starting_pitchers[j]

df_p_stats = df_p_stats.rename(columns={'Name': 'vSP'})
df_dk.drop(columns=['team_1','team_2'], inplace=True)

df_p_stats = df_p_stats[['vSP','h_fac','hr_fac','r_fac','bb_fac']]
df_dk = df_dk[df_dk['b_o'] != 'SP']
df_dk = pd.merge(df_dk, df_p_stats, on='vSP', how='inner')

# Adjusted Batting Projections
proj_hits = (df_dk['H'] + df_dk['2B'] + df_dk['3B']) * df_dk['h_fac']
proj_hr = df_dk['HR'] * df_dk['hr_fac']
proj_r = (df_dk['R'] + df_dk['RBI']) * df_dk['r_fac']
proj_bb = df_dk['BB'] * df_dk['bb_fac']

# * check total hits vs individual 1B, 2B, 3B
proj_pts_vP = proj_hits + proj_hr + proj_r + proj_bb + df_dk['HBP'] + df_dk['SB']

df_dk['pj_vP'] = round(proj_pts_vP, 2)

pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
print(df_dk)

# * Two players named Will Smith produces doubles

df_dk.to_csv('./projections.csv')