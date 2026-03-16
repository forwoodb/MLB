import pandas as pd
from contest import Contest
from spelling import Spelling


class BaseballReference:
    # csv_b_stats = pd.read_csv('./Data/' + Contest.date + '/br_b_stats.csv')
    csv_p_stats = pd.read_csv('./Data/' + Contest.date + '/br_p_stats.csv')
    csv_t_stats = pd.read_csv('./Data/' + Contest.date + '/br_t_stats.csv')

    df_p_stats = pd.DataFrame(csv_p_stats)
    df_t_stats = pd.DataFrame(csv_t_stats)

    df_p_stats = df_p_stats.replace(
        list(Spelling.df_team_abbr["BaseballReference"]), list(Spelling.df_team_abbr["DraftKings"]))
    df_p_stats = df_p_stats.replace(list(
        Spelling.df_name_spelling["BaseballReference"]), list(Spelling.df_name_spelling["DraftKings"]))
