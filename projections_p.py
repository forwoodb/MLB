import pandas as pd
import numpy as np
import re

# Import data.
csv_dk = pd.read_csv('./Data/DKSalaries.csv')
# csv_b_stats = pd.read_csv('./Data/br_b_stats.csv')
csv_p_stats = pd.read_csv('./Data/br_p_stats.csv')
csv_t_stats = pd.read_csv('./Data/br_t_stats.csv')
csv_starting_lineups = pd.read_csv('./Data/Lineups_2021_04_24.csv')
csv_name_spelling = pd.read_csv('./Data/name_spelling.csv')
csv_team_abbr = pd.read_csv('./Data/team_abb.csv')

# Convert to dataframes.
# df_p_stats = pd.DataFrame(csv_b_stats)
df_p_stats = pd.DataFrame(csv_p_stats)
df_t_stats = pd.DataFrame(csv_t_stats)
df_dk = pd.DataFrame(csv_dk)
df_lineups = pd.DataFrame(csv_starting_lineups)
df_name_spelling = pd.DataFrame(csv_name_spelling)
df_team_abbr = pd.DataFrame(csv_team_abbr)

# Clean up lineup data.
df_lineups = df_lineups.rename(columns={' player name': 'Name'})
df_lineups = df_lineups.rename(columns={' batting order': ' b/o'})
df_lineups = df_lineups.rename(columns={'team code': 'team'})
df_lineups = df_lineups.replace(list(df_name_spelling["BaseballMonster"]), list(df_name_spelling["DraftKings"]))
df_lineups = df_lineups.replace(list(df_team_abbr["BaseballMonster"]), list(df_team_abbr["DraftKings"]))


# # Batting Stats
df_p_stats.drop(df_p_stats.tail(1).index,inplace=True)
name = df_p_stats['Name'].str.split('\*|\#', n=1, expand=True)
name = name[0].str.split('\\', n=1, expand=True)
df_p_stats['Name'] = name[0]

df_dk = df_dk[['Name','Game Info','TeamAbbrev','AvgPointsPerGame']]
df_dk = df_dk.rename(columns={'TeamAbbrev': 'TmAbb','AvgPointsPerGame': 'APPG'})
df_lineups = df_lineups[['team','Name',' b/o']]
df_p_stats = df_p_stats[['Name','G','IP','SO','W','ER','H','BB','HBP','CG','SHO']]

df_p_stats = df_p_stats.replace(list(df_team_abbr["BaseballReference"]), list(df_team_abbr["DraftKings"]))
df_p_stats = df_p_stats.replace(list(df_name_spelling["BaseballReference"]), list(df_name_spelling["DraftKings"]))

df_dk = pd.merge(df_lineups, df_dk, on='Name', how='inner')
df_dk = pd.merge(df_dk, df_p_stats, on='Name', how='inner')

# DraftKings Pitching Stats
hits_allowed = (df_dk['H'] * -0.6)/df_dk['G']
innings = (df_dk['IP'] * 2.25)/df_dk['G']
strike_outs = (df_dk['SO'] * 2)/df_dk['G']
wins = (df_dk['W'] * 4)/df_dk['G']
comp_gm = (df_dk['CG'] * 2.5)/df_dk['G']
earned_runs = (df_dk['ER'] * -2)/df_dk['G']
walks = (df_dk['BB'] * -0.6)/df_dk['G']
HBP = (df_dk['HBP'] * -0.6)/df_dk['G']
shut_outs = (df_dk['SHO'] * 2.5)/df_dk['G']

df_dk['H'] = round(hits_allowed, 2)
df_dk['IP'] = round(innings, 2)
df_dk['SO'] = round(strike_outs, 2)
df_dk['W'] = round(wins, 2)
df_dk['CG'] = round(comp_gm, 2)
df_dk['ER'] = round(earned_runs, 2)
df_dk['BB'] = round(walks, 2)
df_dk['HBP'] = round(HBP, 2)
df_dk['SHO'] = round(shut_outs, 2)

proj_pts = (hits_allowed + innings + strike_outs + wins + comp_gm + earned_runs + walks + HBP + shut_outs)
df_dk['pj_pts'] = round(proj_pts, 2)

# # Team Factors for Pitching
df_t_stats.drop(df_t_stats.tail(2).index,inplace=True)
name = df_p_stats['Name'].str.split('*', n=1, expand=True)
name = name[0].str.split('\\', n=1, expand=True)
df_p_stats['Name'] = name[0]

df_t_stats = df_t_stats[['Tm','G','SO','H','R','BB']]

games = df_p_stats['G'].sum()

lg_hits = df_t_stats['H'].sum()
lg_hits_g = lg_hits/games
hits_g = df_t_stats['H']/df_t_stats['G']
hits_fac = hits_g/lg_hits_g
df_t_stats.insert(3, 'h_fac', round(hits_fac, 2))

lg_so = df_t_stats['SO'].sum()
lg_so_g = lg_so/games
so_g = df_t_stats['SO']/df_t_stats['G']
so_fac = so_g/lg_so_g
df_t_stats.insert(5, 'so_fac', round(so_fac, 2))

lg_r = df_t_stats['R'].sum()
lg_r_g = lg_r/games
r_g = df_t_stats['R']/df_t_stats['G']
r_fac = r_g/lg_r_g
df_t_stats.insert(7, 'r_fac', round(r_fac, 2))

lg_bb = df_t_stats['BB'].sum()
lg_bb_g = lg_bb/games
bb_g = df_t_stats['BB']/df_t_stats['G']
bb_fac = bb_g/lg_bb_g
df_t_stats.insert(9, 'bb_fac', round(bb_fac, 2))

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

# starting_pitchers = {}
# for pos in df_dk[' b/o'].unique():
#     if pos == 'SP':
#         availables_sp = df_dk[df_dk[' b/o'] == pos]
#         starting_pitchers = list(availables_sp[['TmAbb', 'Name']].set_index('TmAbb').to_dict().values())[0]

# df_dk['vT'] = None
#
# for i in df_dk.index:
#     for j in starting_pitchers:
#         if df_dk['Opp'][i] == j:
#             df_dk['vT'][i] = starting_pitchers[j]
#
df_t_stats = df_t_stats.rename(columns={'Tm': 'Opp'})
df_dk.drop(columns=['team_1','team_2'], inplace=True)
#
df_t_stats = df_t_stats[['Opp','h_fac','so_fac','r_fac','bb_fac']]
df_dk = pd.merge(df_dk, df_t_stats, on='Opp', how='inner')

# Adjusted Pitching Projections
proj_hits = df_dk['H'] * df_dk['h_fac']
proj_so = df_dk['SO'] * df_dk['so_fac']
proj_r = df_dk['ER'] * df_dk['r_fac']
proj_bb = df_dk['BB'] * df_dk['bb_fac']

proj_pts_vP = proj_hits + proj_so + proj_r + proj_bb + df_dk['HBP']

df_dk['pj_vP'] = round(proj_pts_vP, 2)

pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
print(df_dk)

# * Two players named Will Smith produces double entries

# df_dk.to_csv('./projections_p.csv')