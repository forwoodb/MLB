import pandas as pd

day = '28'
month = '4'
year = '2021'
date = month + '-' + day + '-' + '21'

# Spelling Discrepencies
name_spelling = pd.read_csv('./Spelling/name_spelling.csv')

# Import csv data.
csv_lineups = pd.read_csv('./lineups.csv')
csv_stats_batter = pd.read_csv('./Data/' + date + '/FanGraphs Leaderboard bat 4-28-21.csv')

# Convert csv data to dataframe.
df_lineups = pd.DataFrame(csv_lineups)
df_stats_batter = pd.DataFrame(csv_stats_batter)

# Get DraftKings score for players.
def clean_names(num):
    new = df_lineups[num].str.split('_', n=2, expand=True)
    df_lineups['first'] = new[1]
    df_lineups['last'] = new[2]
    df_lineups.drop(columns=[num], inplace=True)
    df_lineups['player' + num] = df_lineups['first'] + ' ' + df_lineups['last']
    df_lineups.drop(columns=['first'], inplace=True)
    df_lineups.drop(columns=['last'], inplace=True)

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

print(df_totals)