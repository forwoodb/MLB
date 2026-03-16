import pandas as pd

class Spelling:
    
    # Spelling Discrepencies
    csv_name_spelling = pd.read_csv('./Spelling/name_spelling.csv')
    csv_team_abbr = pd.read_csv('./Spelling/team_abb.csv')

    # Convert to dataframes.
    df_name_spelling = pd.DataFrame(csv_name_spelling)
    df_team_abbr = pd.DataFrame(csv_team_abbr)
