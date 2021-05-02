import pandas as pd

day = '28'
month = '4'
year = '2021'
date = month + '-' + day + '-' + '21'

# Spelling Discrepencies
name_spelling = pd.read_csv('./Spelling/name_spelling.csv')

# Import csv data.
csv_lineups = pd.read_csv('./lineups.csv')
csv_stats_batter = pd.read_csv('./Data/' + date + '/FanGraphs Leaderboard bat.csv')

# Convert csv data to dataframe.
df_lineups = pd.DataFrame(csv_lineups)
df_stats_batter = pd.DataFrame(csv_stats_batter)

def clean_names(num):
    for item in df_lineups[num]:
        name = item.split('_')
        name.pop(0)
        name = ' '.join(name)
        df_lineups[num].replace({item: name}, inplace=True)

clean_names('1')
clean_names('2')
clean_names('3')
clean_names('4')
clean_names('5')
clean_names('6')
clean_names('7')
clean_names('8')
clean_names('9')
clean_names('10')

df_stats_batter['dk_1B'] = df_stats_batter['1B']*3
df_stats_batter['dk_2B'] = df_stats_batter['2B']*5
df_stats_batter['dk_3B'] = df_stats_batter['3B']*8
df_stats_batter['dk_HR'] = df_stats_batter['HR']*10
df_stats_batter['dk_R'] = df_stats_batter['R']*2
df_stats_batter['dk_RBI'] = df_stats_batter['RBI']*2
df_stats_batter['dk_BB'] = df_stats_batter['BB']*2
df_stats_batter['dk_HBP'] = df_stats_batter['HBP']*2
df_stats_batter['dk_SB'] = df_stats_batter['SB']*5
df_stats_batter['Total'] = df_stats_batter['1B'] + df_stats_batter['2B'] + df_stats_batter['3B'] + df_stats_batter['HR'] + df_stats_batter['R'] + df_stats_batter['RBI'] + df_stats_batter['BB'] + df_stats_batter['HBP'] + df_stats_batter['SB']

df_totals = df_stats_batter[['Name', 'Total']]

def get_scores(num):
    pd.merge(df_lineups[num], df_totals, left_on=num, right_on='Name', on=num, how='inner')

get_scores('1')
# totals = dict(zip(df_stats_batter['Name'], df_stats_batter['Total']))


# df_lineups = df_lineups.T
# df_lineups.columns=df_lineups.iloc[1]
# df_lineups = df_lineups.reindex(df_lineups.index.drop('Lineup Type'))

# df_roster = df_lineups[['1','2','3','4','5','6','7','8','9','10']]
# rosters = df_roster.values.tolist()

# for list in rosters:
#     print(list)
#
# for k in rosters[0]:
#     if k in totals:
#         print(k, totals[k])

# df_pivot_lineups = df_lineups.pivot_table(index='')
# scores = pd.merge(df_lineups, df_totals)
# scores = pd.merge(df_lineups, df_totals, left_on='APPG', right_on='Name')
# scores = pd.merge(df_lineups, df_totals, left_on='pj_vO', right_on='Name')
# scores = pd.merge(df_lineups, df_totals, left_on='3', right_on='Name')
# scores = pd.merge(df_lineups, df_totals, left_on='4', right_on='Name')
# scores = pd.merge(df_lineups, df_totals, left_on='5', right_on='Name')
# scores = pd.merge(df_lineups, df_totals, left_on='6', right_on='Name')
# scores = pd.merge(df_lineups, df_totals, left_on='7', right_on='Name')
# scores = pd.merge(df_lineups, df_totals, left_on='8', right_on='Name')
# scores = pd.merge(df_lineups, df_totals, left_on='9', right_on='Name')
# scores = pd.merge(df_lineups, df_totals, left_on='10', right_on='Name')
# scores = pd.merge(df_lineups, df_stats_batter, on='Name', how='inner')

pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
print(df_lineups)