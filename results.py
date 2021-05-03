import pandas as pd

day = '28'
month = '4'
year = '2021'
date = month + '-' + day + '-' + '21'

# Spelling Discrepencies
name_spelling = pd.read_csv('./Spelling/name_spelling.csv')

# Import csv data.
csv_lineups = pd.read_csv('./Data/' + date + '/lineups.csv')
csv_stats_batter = pd.read_csv('./Data/' + date + '/FanGraphs Leaderboard bat.csv')
csv_stats_pitcher = pd.read_csv('./Data/' + date + '/FanGraphs Leaderboard pitch.csv')

# Convert csv data to dataframe.
df_name_spelling = pd.DataFrame(name_spelling)
df_lineups = pd.DataFrame(csv_lineups)
df_stats_batter = pd.DataFrame(csv_stats_batter)
df_stats_pitcher = pd.DataFrame(csv_stats_pitcher)

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

# Batter Stats
df_stats_batter['dk_1B'] = df_stats_batter['1B']*3
df_stats_batter['dk_2B'] = df_stats_batter['2B']*5
df_stats_batter['dk_3B'] = df_stats_batter['3B']*8
df_stats_batter['dk_HR'] = df_stats_batter['HR']*10
df_stats_batter['dk_R'] = df_stats_batter['R']*2
df_stats_batter['dk_RBI'] = df_stats_batter['RBI']*2
df_stats_batter['dk_BB'] = df_stats_batter['BB']*2
df_stats_batter['dk_HBP'] = df_stats_batter['HBP']*2
df_stats_batter['dk_SB'] = df_stats_batter['SB']*5
df_stats_batter['Total'] = df_stats_batter['dk_1B'] + df_stats_batter['dk_2B'] + df_stats_batter['dk_3B'] + df_stats_batter['dk_HR'] + df_stats_batter['dk_R'] + df_stats_batter['dk_RBI'] + df_stats_batter['dk_BB'] + df_stats_batter['dk_HBP'] + df_stats_batter['dk_SB']

# Pitcher Stats
df_stats_pitcher['dk_IP'] = df_stats_pitcher['IP']*2.25
df_stats_pitcher['dk_SO'] = df_stats_pitcher['SO']*2
df_stats_pitcher['dk_W'] = df_stats_pitcher['W']*4
df_stats_pitcher['dk_ER'] = df_stats_pitcher['ER']*-2
df_stats_pitcher['dk_H'] = df_stats_pitcher['H']*-0.6
df_stats_pitcher['dk_BB'] = df_stats_pitcher['BB']*-0.6
df_stats_pitcher['dk_HBP'] = df_stats_pitcher['HBP']*-0.6
df_stats_pitcher['dk_CG'] = df_stats_pitcher['CG']*2.5
df_stats_pitcher['dk_ShO'] = df_stats_pitcher['ShO']*2.5
df_stats_pitcher['Total'] = df_stats_pitcher['dk_IP'] + df_stats_pitcher['dk_SO'] + df_stats_pitcher['dk_W'] + df_stats_pitcher['dk_ER'] + df_stats_pitcher['dk_H'] + df_stats_pitcher['dk_BB'] + df_stats_pitcher['dk_HBP'] + df_stats_pitcher['dk_CG'] + df_stats_pitcher['dk_ShO']

df_totals = df_stats_batter[['Name', 'Total']]
df_totals = df_totals.append(df_stats_pitcher[['Name', 'Total']])
df_totals = df_totals.replace(list(df_name_spelling["FanGraphs"]), list(df_name_spelling["DraftKings"]))
df_totals = df_totals.replace(list(df_name_spelling["FanGraphs"]), list(df_name_spelling["DraftKings"]))


df_totals_APPG = df_totals.rename(columns={'Name': 'Name_APPG','Total': 'Total APPG'})
df_totals_pj_vO = df_totals.rename(columns={'Name': 'Name_pj_vO','Total': 'Total_pj_vO'})
df_totals_APPG_6 = df_totals.rename(columns={'Name': 'Name_APPG_1-6','Total': 'Total_APPG_1-6'})
df_totals_APPG_5 = df_totals.rename(columns={'Name': 'Name_APPG_1-5','Total': 'Total_APPG_1-5'})
df_totals_APPG_4= df_totals.rename(columns={'Name': 'Name_APPG_1-4','Total': 'Total_APPG_1-4'})
df_totals_APPG_3= df_totals.rename(columns={'Name': 'Name_APPG_1-3','Total': 'Total_APPG_1-3'})
df_totals_pj_vO_6 = df_totals.rename(columns={'Name': 'Name_pj_vO_1-6','Total': 'Total_pj_vO_1-6'})
df_totals_pj_vO_5 = df_totals.rename(columns={'Name': 'Name_pj_vO_1-5','Total': 'Total_pj_vO_1-5'})
df_totals_pj_vO_4= df_totals.rename(columns={'Name': 'Name_pj_vO_1-4','Total': 'Total_pj_vO_1-4'})
df_totals_pj_vO_3= df_totals.rename(columns={'Name': 'Name_pj_vO_1-3','Total': 'Total_pj_vO_1-3'})

# With transpose
df_lineups = df_lineups.T
df_lineups.columns=df_lineups.iloc[1]

df_lineups = df_lineups.reindex(df_lineups.index.drop('Lineup Type'))

df_lineups = pd.merge(df_lineups, df_totals_APPG, how='left', left_on='APPG', right_on='Name_APPG')
df_lineups = pd.merge(df_lineups, df_totals_pj_vO, how='left', left_on='pj_vO', right_on='Name_pj_vO')
df_lineups = pd.merge(df_lineups, df_totals_APPG_6, how='left', left_on='APPG 1-6', right_on='Name_APPG_1-6')
df_lineups = pd.merge(df_lineups, df_totals_APPG_5, how='left', left_on='APPG 1-5', right_on='Name_APPG_1-5')
df_lineups = pd.merge(df_lineups, df_totals_APPG_4, how='left', left_on='APPG 1-4', right_on='Name_APPG_1-4')
# df_lineups = pd.merge(df_lineups, df_totals_APPG_3, how='left', left_on='APPG 1-3', right_on='Name_APPG_1-3')
df_lineups = pd.merge(df_lineups, df_totals_pj_vO_6, how='left', left_on='pj_vO 1-6', right_on='Name_pj_vO_1-6')
df_lineups = pd.merge(df_lineups, df_totals_pj_vO_5, how='left', left_on='pj_vO 1-5', right_on='Name_pj_vO_1-5')
df_lineups = pd.merge(df_lineups, df_totals_pj_vO_4, how='left', left_on='pj_vO 1-4', right_on='Name_pj_vO_1-4')
# df_lineups = pd.merge(df_lineups, df_totals_pj_vO_3, how='left', left_on='pj_vO 1-3', right_on='Name_pj_vO_1-3')

df_lineups['Total APPG'][11] = df_lineups['Total APPG'].sum()
df_lineups['Total_pj_vO'][11] = df_lineups['Total_pj_vO'].sum()
df_lineups['Total_APPG_1-6'][11] = df_lineups['Total_APPG_1-6'].sum()
df_lineups['Total_APPG_1-5'][11] = df_lineups['Total_APPG_1-5'].sum()
df_lineups['Total_APPG_1-4'][11] = df_lineups['Total_APPG_1-4'].sum()
# df_lineups['Total_APPG_1-3'][11] = df_lineups['Total_APPG_1-3'].sum()
df_lineups['Total_pj_vO_1-6'][11] = df_lineups['Total_pj_vO_1-6'].sum()
df_lineups['Total_pj_vO_1-5'][11] = df_lineups['Total_pj_vO_1-5'].sum()
df_lineups['Total_pj_vO_1-4'][11] = df_lineups['Total_pj_vO_1-4'].sum()
# df_lineups['Total_pj_vO_1-3'][11] = df_lineups['Total_pj_vO_1-3'].sum()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(df_lineups)

df_lineups.to_csv('./Data/' + date + '/results.csv')