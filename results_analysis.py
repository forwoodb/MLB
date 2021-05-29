import pandas as pd
import os

dates = ['05-18-21','05-16-21','05-15-21','05-14-21','05-13-21','05-12-21','05-10-21','05-09-21','05-08-21','05-07-21','05-04-21','05-03-21','04-30-21','04-28-21','04-24-21']
# dates = ['05-03-21']
slates = ['14','12','13','11','10','7','7t','6','6t','5n','5t','4','4n','4t','3','3a','3e','3ln','3n','3t','2ln','2n','2t']
# slates = ['4','4n','4t','3','3a','3e','3ln','3n','3t','2ln','2n','2t']


contests = []
contest_slates = []

for date in dates:
    for slate in slates:
        date_path = './Data/' + date + '/' + slate + '/'
        if not os.path.isdir(date_path):
            continue
        elif not os.path.isfile(date_path + 'results.csv'):
            continue
        else:
            csv_results = pd.read_csv(date_path + 'results.csv')
            df_results = pd.DataFrame(csv_results)
            # df_results['Slate'].append(slate)
            contests.append(df_results)
            contest_slates.append(slate)

contests = tuple(zip(contest_slates,contests))

strategies = []
scores = []
contest_dates = []
contest_slates = []

xstrategies = []
# xstrategies = ['Total_pj_vO_1-3','pj_vO_1-3','Total_pj_vOa_1-3', 'pj_vOa_1-3', 'Total_APPG_1-3', 'APPG_1-3', 'Total_pj_vO_1-5', 'pj_vO_1-5']

for df in contests:
    for col in df[1]:
        if 'Total' in col and col not in xstrategies:
            contest_slates.append(df[0])

for df in contests:
    for col in df[1]:
        if 'Total' in col and col not in xstrategies:
            strategies.append(col)

for df in contests:
    for col in df[1]:
        if 'Total' in col and col not in xstrategies:
            scores.append(round(df[1][col][11], 2))

for df in contests:
    for col in df[1]:
        if pd.isnull(df[1][col][0]) == False and df[1][col][0] != 0 and col not in xstrategies:
            contest_dates.append(df[1][col][0])

df_strat = pd.DataFrame()
df_strat['Date'] = contest_dates
df_strat['Slate'] = contest_slates
df_strat['Name'] = strategies
df_strat['Points'] = scores

df_strat = df_strat.sort_values( by = ['Date','Slate','Points'], ascending = [True,False,False])

df_strat['Rank'] = df_strat.groupby(['Date','Slate'])['Points'].rank(pct=True)

pd.set_option('display.max_rows', None)
print(df_strat)

df_points = df_strat.groupby('Name')['Points'].mean()
# df_ranks = df_strat[['Name','Points']].groupby('Name')['Points'].mean()

# Win % Required
df_ranks = (df_strat[df_strat['Rank'] > .5].groupby('Name')['Rank'].count())/(df_strat.groupby(['Name'])['Name'].count())

df_ranks = pd.merge(df_points.to_frame(), df_ranks.to_frame(), on='Name', how='inner')
df_ranks = df_ranks.sort_values(by=0, ascending=False)

pd.set_option('display.max_rows', None)
# print(df_points)
print(df_ranks)
print('----------')
print('Sample Size: ' + str(len(contests)))
