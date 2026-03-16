import pandas as pd

from contest import Contest
from spelling import Spelling

class Lineups:

    # Import data.
    csv_starting_lineups = pd.read_csv('./Data/' + Contest.date + '/Lineups_' + Contest.year + '_' + Contest.month + '_' + Contest.day + '.csv')

    # Convert to dataframes.
    df_lineups = pd.DataFrame(csv_starting_lineups)

    # Clean up lineup data.
    df_lineups = df_lineups.rename(columns={' player name': 'Name'})
    df_lineups = df_lineups.rename(columns={' batting order': 'b_o'})
    df_lineups = df_lineups.rename(columns={'team code': 'team'})
    
    df_lineups = df_lineups.replace(
        list(Spelling.df_name_spelling["BaseballMonster"]), list(Spelling.df_name_spelling["DraftKings"]))
    df_lineups = df_lineups.replace(
        list(Spelling.df_team_abbr["BaseballMonster"]), list(Spelling.df_team_abbr["DraftKings"]))

    pd.set_option('display.max_columns', None)
    print(df_lineups)
