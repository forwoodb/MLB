import pandas as pd

# date = '04-30-21'
dates = ['04-30-21','04-28-21','04-24-21']

for date in dates:
    csv_results = pd.read_csv('./Data/' + date + '/results.csv')

    df_results = pd.DataFrame(csv_results)

    strategies = []
    scores = []
    contest_dates = []

    for col in df_results.columns:
        if 'Total' in col:
            strategies.append(col)

    for col in df_results:
        if 'Total' in col:
            scores.append(round(df_results[col][11], 2))

    for col in df_results:
        if pd.isnull(df_results[col][0]) == False and df_results[col][0] != 0:
            contest_dates.append(df_results[col][0])
            # print(df_results[col][0])

    df_strat = pd.DataFrame()
    df_strat['Date'] = contest_dates
    df_strat['Name'] = strategies
    df_strat['Points'] = scores

    df_strat = df_strat.sort_values( by = ['Date', 'Points'], ascending = [False, False])


    # print(contest_dates)
    # print(strategies)
    print(df_strat)