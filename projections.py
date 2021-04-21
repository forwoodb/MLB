import pandas as pd

data = pd.read_csv('./Data/FanGraphs Leaderboard.csv')

df = pd.DataFrame(data)

singles = ((df['H']-df['2B']-df['3B']-df['HR']) * 3)/df['G']
doubles = (df['2B'] * 5)/df['G']
triples = (df['3B'] * 8)/df['G']
home_runs = (df['HR'] * 10)/df['G']
RBIs = (df['RBI'] * 2)/df['G']
runs = (df['R'] * 2)/df['G']
walks = (df['BB'] * 2)/df['G']
HBP = (df['HBP'] * 2)/df['G']
stolen_bases = (df['SB'] * 5)/df['G']

proj_pts = (singles + doubles + triples + home_runs + RBIs + runs + walks + HBP + stolen_bases)
df['proj_pts'] = round(proj_pts, 2)
df.sort_values(by=['proj_pts'], inplace=True, ascending=False)

# display entire dataframe in console
pd.set_option('display.max_rows', None)
print(df)