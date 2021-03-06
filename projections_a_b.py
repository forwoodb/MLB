import pandas as pd
import numpy as np
import re

day = '24'
month = '04'
year = '2021'

date = month + '-' + day + '-21'
slate = '6'

# Spelling Discrepencies
csv_name_spelling = pd.read_csv('./Spelling/name_spelling.csv')
csv_team_abbr = pd.read_csv('./Spelling/team_abb.csv')

# Import data.
csv_dk = pd.read_csv('./Data/' + date + '/' + slate + '/DKSalaries.csv')
csv_starting_lineups = pd.read_csv('./Data/' + date + '/Lineups_' + year + '_' + month + '_' + day + '.csv')
# Baseball Reference
# csv_b_stats = pd.read_csv('./Data/' + date + '/br_b_stats.csv')
csv_p_stats = pd.read_csv('./Data/' + date + '/br_p_stats.csv')
csv_t_stats = pd.read_csv('./Data/' + date + '/br_t_stats.csv')
# FanGraphs
csv_b_stats = pd.read_csv('./Data/' + date + '/fgbatters.csv')
# csv_p_stats = pd.read_csv('./Data/' + date + '/fgpitchers.csv')
# csv_t_stats = pd.read_csv('./Data/' + date + '/fgteamb.csv')

# Park Factor
csv_bp_stats = pd.read_csv('./DKMLB Park Factor - Average.csv')

# Convert to dataframes.
df_dk = pd.DataFrame(csv_dk)
df_b_stats = pd.DataFrame(csv_b_stats)
df_p_stats = pd.DataFrame(csv_p_stats)
df_t_stats = pd.DataFrame(csv_t_stats)
df_lineups = pd.DataFrame(csv_starting_lineups)
df_name_spelling = pd.DataFrame(csv_name_spelling)
df_team_abbr = pd.DataFrame(csv_team_abbr)
df_bp_stats = pd.DataFrame(csv_bp_stats)

# Clean up lineup data.
df_lineups = df_lineups.rename(columns={' player name': 'Name'})
df_lineups = df_lineups.rename(columns={' batting order': 'b_o'})
df_lineups = df_lineups.rename(columns={'team code': 'team'})
df_lineups = df_lineups.replace(list(df_name_spelling["BaseballMonster"]), list(df_name_spelling["DraftKings"]))
df_lineups = df_lineups.replace(list(df_team_abbr["BaseballMonster"]), list(df_team_abbr["DraftKings"]))

def bottom_rows(df):
    df.drop(df.tail(1).index,inplace=True)
    name = df['Name'].str.split('\*|\#', n=1, expand=True)
    name = name[0].str.split('\\', n=1, expand=True)
    df['Name'] = name[0]

# Batting Stats
def batters(df):
    df = df_dk
    df_batters = df_b_stats
    df_vP = df_p_stats
    df_vBP = df_bp_stats
    df_lineups_bat = df_lineups

    bottom_rows(df_batters)

    df = df[['Name','Game Info','TeamAbbrev','AvgPointsPerGame']]
    df = df.rename(columns={'TeamAbbrev': 'TmAbb','AvgPointsPerGame': 'APPG'})
    df_lineups_bat = df_lineups_bat[['team','Name','b_o']]
    df_batters = df_batters[['Name','G','H','2B','3B','HR','BB','R','RBI','HBP','SB']]

    df_batters = df_batters.replace(list(df_team_abbr["BaseballReference"]), list(df_team_abbr["DraftKings"]))
    df_batters = df_batters.replace(list(df_name_spelling["BaseballReference"]), list(df_name_spelling["DraftKings"]))
    df_batters = df_batters.replace(list(df_name_spelling["FanGraphs"]), list(df_name_spelling["DraftKings"]))

    # df_vP = df_vP.replace(list(df_team_abbr["BaseballReference"]), list(df_team_abbr["DraftKings"]))
    # df_vP = df_vP.replace(list(df_name_spelling["BaseballReference"]), list(df_name_spelling["DraftKings"]))

    df = pd.merge(df_lineups_bat, df, on='Name', how='inner')
    df = pd.merge(df, df_batters, on='Name', how='inner')

    # DraftKings Batting Stats
    singles = ((df['H']-df['2B']-df['3B']-df['HR']) * 3)/df['G']
    doubles = (df['2B'] * 5)/df['G']
    triples = (df['3B'] * 8)/df['G']
    home_runs = (df['HR'] * 10)/df['G']
    RBIs = (df['RBI'] * 2)/df['G']
    runs = (df['R'] * 2)/df['G']
    walks = (df['BB'] * 2)/df['G']
    HBP = (df['HBP'] * 2)/df['G']
    stolen_bases = (df['SB'] * 5)/df['G']

    df['H'] = round(singles, 2)
    df['2B'] = round(doubles, 2)
    df['3B'] = round(triples, 2)
    df['HR'] = round(home_runs, 2)
    df['RBI'] = round(RBIs, 2)
    df['R'] = round(runs, 2)
    df['BB'] = round(walks, 2)
    df['HBP'] = round(HBP, 2)
    df['SB'] = round(stolen_bases, 2)

    proj_pts = (singles + doubles + triples + home_runs + RBIs + runs + walks + HBP + stolen_bases)
    df['pj_pts'] = round(proj_pts, 2)

    # # Starting Pitcher Factors for Batting
    bottom_rows(df_vP)

    df_vP = df_vP[['Name','IP','H','HR','R','BB']]

    lg_innings_pitched = df_vP['IP'].sum()

    lg_hits_allowed = df_vP['H'].sum() - df_vP['HR'].sum()
    lg_hits_ip = lg_hits_allowed/lg_innings_pitched
    hits_ip = (df_vP['H'] - df_vP['HR'])/df_vP['IP']
    hits_fac = hits_ip/lg_hits_ip
    df_vP.insert(3, 'h_fac', round(hits_fac, 2))

    lg_hr_allowed = df_vP['HR'].sum()
    lg_hr_ip = lg_hr_allowed/lg_innings_pitched
    hr_ip = df_vP['HR']/df_vP['IP']
    hr_fac = hr_ip/lg_hr_ip
    df_vP.insert(5, 'hr_fac', round(hr_fac, 2))

    lg_r_allowed = df_vP['R'].sum()
    lg_r_ip = lg_r_allowed/lg_innings_pitched
    r_ip = df_vP['R']/df_vP['IP']
    r_fac = r_ip/lg_r_ip
    df_vP.insert(7, 'r_fac', round(r_fac, 2))

    lg_bb_allowed = df_vP['BB'].sum()
    lg_bb_ip = lg_bb_allowed/lg_innings_pitched
    bb_ip = df_vP['BB']/df_vP['IP']
    bb_fac = bb_ip/lg_bb_ip
    df_vP.insert(9, 'bb_fac', round(bb_fac, 2))

    #Starting Pitcher Stats
    game_info = df['Game Info'].str.split('@', n=1, expand=True)
    df['Away'] = game_info[0]
    df['Home'] = game_info[1]

    Home = df['Home'].str.split(' ', n=1, expand=True)
    df['Home'] = Home[0]
    df.drop(columns=['Game Info'], inplace=True)

    df['Opp'] = None

    for i in df.index:
        if df['TmAbb'][i] == df['Away'][i]:
            df['Opp'][i] = df['Home'][i]
        else:
            df['Opp'][i] = df['Away'][i]

    starting_pitchers = {}
    for pos in df_lineups_bat['b_o'].unique():
        if pos == 'SP':
            availables_sp = df_lineups_bat[df_lineups_bat['b_o'] == pos]
            starting_pitchers = list(availables_sp[['team', 'Name']].set_index('team').to_dict().values())[0]

    df['vSP'] = None

    for i in df.index:
        for j in starting_pitchers:
            if df['Opp'][i] == j:
                df['vSP'][i] = starting_pitchers[j]


    df_vP = df_vP.rename(columns={'Name': 'vSP'})
    # df.drop(columns=['Away','Home'], inplace=True)

    none = [{'vSP':None,'h_fac':1,'hr_fac':1,'r_fac':1,'bb_fac':1}]
    df_vP = df_vP.append(none)

    sp_list = list(set(list(df['vSP'])))

    df_vP = df_vP[df_vP['vSP'].isin(sp_list)]

    df_vP = df_vP[['vSP','h_fac','hr_fac','r_fac','bb_fac']]

    # # Ballpark Factors for Batting
    df_vBP = df_vBP[['PARK NAME','RUNS','HR','H','2B','3B','BB']]

    # Ballpark Stats

    df_vBP = df_vBP.replace(list(df_team_abbr["BallParksESPN"]), list(df_team_abbr["DraftKings"]))
    df_vBP = df_vBP.rename(columns={'PARK NAME': 'Home','RUNS': 'R_FAC','HR': 'HR_FAC','H': 'H_FAC','2B': '2B_FAC','3B': '3B_FAC','BB': 'BB_FAC'})

    # Eliminate batting order positions
    df = df[df['b_o'] != 'SP']

    # df = pd.merge(df, df_vP, on='vSP', how='inner')
    df = pd.merge(df, df_vP, on='vSP', how='outer').fillna(1)
    df = pd.merge(df, df_vBP, on='Home', how='inner')

    # # Adjusted Batting Projections
    proj_hits = (df['H'] + df['2B'] + df['3B']) * df['h_fac']  * df['H_FAC']
    proj_hr = df['HR'] * df['hr_fac']  * df['HR_FAC']
    proj_r = (df['R'] + df['RBI']) * df['r_fac']  * df['R_FAC']
    proj_bb = df['BB'] * df['bb_fac'] * df['BB_FAC']

    # * check total hits vs individual 1B, 2B, 3B
    proj_pts_vP = proj_hits + proj_hr + proj_r + proj_bb + df['HBP'] + df['SB']

    df['pj_vO'] = round(proj_pts_vP, 2)
    df = df[df['pj_vO'] > 0]

    # # # # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)
    # print(df)
    #
    return df


def pitchers(df):
    df = df_dk
    df_pitchers = df_p_stats
    df_vT = df_t_stats
    df_vBP = df_bp_stats
    df_lineups_pitchers = df_lineups

    df = df[['Name','Game Info','TeamAbbrev','AvgPointsPerGame']]
    df = df.rename(columns={'TeamAbbrev': 'TmAbb','AvgPointsPerGame': 'APPG'})
    df_lineups_pitchers = df_lineups_pitchers[['team','Name','b_o']]
    # BR
    df_pitchers = df_pitchers[['Name','G','IP','SO','W','ER','H','BB','HBP','CG','SHO']]
    # FG
    # df_pitchers = df_pitchers[['Name','G','IP','SO','W','ER','H','BB','HBP','CG','ShO']]

    df_vT = df_vT.replace(list(df_team_abbr["BaseballReference"]), list(df_team_abbr["DraftKings"]))
    df_vT = df_vT.replace(list(df_name_spelling["BaseballReference"]), list(df_name_spelling["DraftKings"]))

    df = pd.merge(df_lineups_pitchers, df, on='Name', how='inner')
    df = pd.merge(df, df_p_stats, on='Name', how='inner')

    # DraftKings Pitching Stats
    hits_allowed = (df['H'] * -0.6)/df['G']
    innings = (df['IP'] * 2.25)/df['G']
    strike_outs = (df['SO'] * 2)/df['G']
    wins = (df['W'] * 4)/df['G']
    comp_gm = (df['CG'] * 2.5)/df['G']
    earned_runs = (df['ER'] * -2)/df['G']
    walks = (df['BB'] * -0.6)/df['G']
    HBP = (df['HBP'] * -0.6)/df['G']
    # BR
    shut_outs = (df['SHO'] * 2.5)/df['G']
    # FG
    # shut_outs = (df['ShO'] * 2.5)/df['G']

    df['H'] = round(hits_allowed, 2)
    df['IP'] = round(innings, 2)
    df['SO'] = round(strike_outs, 2)
    df['W'] = round(wins, 2)
    df['CG'] = round(comp_gm, 2)
    df['ER'] = round(earned_runs, 2)
    df['BB'] = round(walks, 2)
    df['HBP'] = round(HBP, 2)
    # BR
    df['SHO'] = round(shut_outs, 2)
    # FG
    # df['ShO'] = round(shut_outs, 2)

    proj_pts = (hits_allowed + innings + strike_outs + wins + comp_gm + earned_runs + walks + HBP + shut_outs)
    df['pj_pts'] = round(proj_pts, 2)


    # # Team Factors for Pitching
    df_vT.drop(df_vT.tail(2).index,inplace=True)
    name = df_p_stats['Name'].str.split('*', n=1, expand=True)
    name = name[0].str.split('\\', n=1, expand=True)
    df_p_stats['Name'] = name[0]

    # vs Team Batting
    # BR
    df_vT = df_vT[['Tm','G','SO','H','R','BB']]
    # FG
    # df_vT = df_vT[['Team','G','SO','H','R','BB']]

    games = df_vT['G'].sum()

    lg_hits = df_vT['H'].sum()
    lg_hits_g = lg_hits/games
    hits_g = df_vT['H']/df_vT['G']
    hits_fac = hits_g/lg_hits_g
    df_vT.insert(3, 'h_fac', round(hits_fac, 2))

    lg_so = df_vT['SO'].sum()
    lg_so_g = lg_so/games
    so_g = df_vT['SO']/df_vT['G']
    so_fac = so_g/lg_so_g
    df_vT.insert(5, 'so_fac', round(so_fac, 2))

    lg_r = df_vT['R'].sum()
    lg_r_g = lg_r/games
    r_g = df_vT['R']/df_vT['G']
    r_fac = r_g/lg_r_g
    df_vT.insert(7, 'r_fac', round(r_fac, 2))

    lg_bb = df_vT['BB'].sum()
    lg_bb_g = lg_bb/games
    bb_g = df_vT['BB']/df_vT['G']
    bb_fac = bb_g/lg_bb_g
    df_vT.insert(9, 'bb_fac', round(bb_fac, 2))

    #Starting Pitcher Stats
    game_info = df['Game Info'].str.split('@', n=1, expand=True)
    df['Away'] = game_info[0]
    df['Home'] = game_info[1]
    #
    Home = df['Home'].str.split(' ', n=1, expand=True)
    df['Home'] = Home[0]
    df.drop(columns=['Game Info'], inplace=True)

    df['Opp'] = None

    for i in df.index:
        if df['TmAbb'][i] == df['Away'][i]:
            df['Opp'][i] = df['Home'][i]
        else:
            df['Opp'][i] = df['Away'][i]

    # BR
    df_vT = df_vT.rename(columns={'Tm': 'Opp'})
    # FG
    # df_vT = df_vT.rename(columns={'Team': 'Opp'})

    # df.drop(columns=['Away','Home'], inplace=True)

    df_vT = df_vT[['Opp','h_fac','so_fac','r_fac','bb_fac']]
    df = df[df['b_o'] == 'SP']
    df = pd.merge(df, df_vT, on='Opp', how='inner')

    # vs Ballpark
    df_vBP = df_vBP.replace(list(df_team_abbr["BallParksESPN"]), list(df_team_abbr["DraftKings"]))
    df_vBP = df_vBP.rename(columns={'PARK NAME': 'Home','RUNS': 'R_FAC','HR': 'HR_FAC','H': 'H_FAC','2B': '2B_FAC','3B': '3B_FAC','BB': 'BB_FAC'})
    df = pd.merge(df, df_vBP, on='Home', how='inner')

    # Adjusted Pitching Projections
    proj_hits = df['H'] * df['h_fac'] * df['H_FAC']
    proj_so = df['SO'] * df['so_fac']
    proj_r = df['ER'] * df['r_fac'] * df['R_FAC']
    proj_bb = df['BB'] * df['bb_fac'] * df['BB_FAC']

    # BR
    proj_pts_vP = proj_hits + proj_so + proj_r + proj_bb + df['HBP'] + df['IP'] + df['W'] + df['CG'] + df['SHO']
    # FG
    # proj_pts_vP = proj_hits + proj_so + proj_r + proj_bb + df['HBP'] + df['IP'] + df['W'] + df['CG'] + df['ShO']

    df['pj_vO'] = round(proj_pts_vP, 2)

    # print(df)
    return df

# batters(df_dk)
b_proj = batters(df_dk)

b_proj = b_proj[['team', 'Name','b_o', 'pj_vO']]

p_proj = pitchers(df_dk)
p_proj = p_proj[['team', 'Name','b_o', 'pj_vO']]

df_proj = b_proj
df_proj = df_proj.append(p_proj)
#
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(df_proj)

df_proj.to_csv('./Data/' + date + '/' + slate + '/projections_a_b.csv')
#
# # * Two players named Will Smith produces doubles
