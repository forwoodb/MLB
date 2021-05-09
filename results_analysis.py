import pandas as pd

# date = '04-30-21'
# dates = ['05-04-21']
dates = ['05-07-21','05-04-21','05-03-21','04-30-21','04-28-21','04-24-21']


contests = []

for date in dates:
    csv_results = pd.read_csv('./Data/' + date + '/results.csv')

    df_results = pd.DataFrame(csv_results)

    contests.append(df_results)

strategies = []
scores = []
contest_dates = []

for df in contests:
    for col in df:
        if 'Total' in col:
            strategies.append(col)

for df in contests:
    for col in df:
        if 'Total' in col:
            scores.append(round(df[col][11], 2))

for df in contests:
    for col in df:
        if pd.isnull(df[col][0]) == False and df[col][0] != 0:
            contest_dates.append(df[col][0])
            # print(df_results[col][0])

df_strat = pd.DataFrame()
df_strat['Date'] = contest_dates
df_strat['Name'] = strategies
df_strat['Points'] = scores

df_strat = df_strat.sort_values( by = ['Date', 'Points'], ascending = [False, False])

df_strat['Rank'] = df_strat.groupby(['Date'])['Points'].rank(pct=True)

pd.set_option('display.max_rows', None)
print(df_strat)

df_points = df_strat.groupby('Name')['Points'].mean()
# df_ranks = df_strat[['Name','Points']].groupby('Name')['Points'].mean()

# Win % Required
df_ranks = (df_strat[df_strat['Rank'] > .5].groupby('Name')['Rank'].count())/(df_strat.groupby(['Name'])['Name'].count())

df_ranks = pd.merge(df_points.to_frame(), df_ranks.to_frame(), on='Name', how='inner')

df_ranks = df_ranks.sort_values(by=0, ascending=False)
# df_points = df_points.sort_values(ascending=False)


pd.set_option('display.max_rows', None)
# print(df_points)
print(df_ranks)

# strats = []
#
# for i in strategies:
#     if i not in strats:
#         strats.append(i)
#
# df_ranks = df_strat.groupby(['Name']).sum()
# df_ranks = df_ranks.sort_values(by=['Rank'], ascending=False)
#
# pd.set_option('display.max_columns', None)
# print(df_ranks)
