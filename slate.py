import pandas as pd
from contest import Contest

class Slate:
    # Import data.
    csv_dk = pd.read_csv('./Data/' + Contest.date + '/' + Contest.slate + '/DKSalaries.csv')

    # Convert to dataframes.
    df_dk = pd.DataFrame(csv_dk)

    # Game Info
    game_info = df_dk['Game Info'].str.split('@', n=1, expand=True)
    df_dk['Away'] = game_info[0]
    df_dk['Home'] = game_info[1]

    home = df_dk['Home'].str.split(' ', n=1, expand=True)
    df_dk['Home'] = home[0]
    df_dk.drop(columns=['Game Info'], inplace=True)

    df_dk['Opp'] = None

    for i in df_dk.index:
        if df_dk['TeamAbbrev'][i] == df_dk['Away'][i]:
            df_dk['Opp'][i] = df_dk['Home'][i]
        else:
            df_dk['Opp'][i] = df_dk['Away'][i]

    df_dk = df_dk.rename(columns={'TeamAbbrev': 'TmAbb', 'AvgPointsPerGame': 'APPG'})

    # df_dk = df_dk[['Name', 'Roster Position', 'TeamAbbrev', 'Opp', 'Home']]

    pd.set_option('display.max_columns', None)
    print(df_dk)
