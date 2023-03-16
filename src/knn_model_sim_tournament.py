import pandas as pd
import math
"""
Sim score between games: A/B and C/D
Take Sim(A,C), Sim(A,D), Sim(B,C), Sim(B,D)
Weight(A/C) = Similarity Score(A,C) / (Similarity Score(A,C) + Similarity Score(A,D))
Weight(A/D) = Similarity Score(A,D) / (Similarity Score(A,C) + Similarity Score(A,D)) 
Weight(B/C) = Similarity Score(B,C) / (Similarity Score(B,C) + Similarity Score(B,D))
Weight(B/D) = Similarity Score(B,D) / (Similarity Score(B,C) + Similarity Score(B,D))
Unified Similarity Score = (Weight(A/C) * Similarity Score(A,C)) + (Weight(A/D) * Similarity Score(A,D)) + (Weight(B/C) * Similarity Score(B,C)) + (Weight(B/D) * Similarity Score(B,D))

Option 2: (A,B) in a vector, just find distance to (C,D) (higher seed first) and do distance on pairs

"""
def add_data(df):
    df_2021 = pd.read_csv("NCAA_School_Stats_Tempo_Free_2021.csv")
    df_2019 = pd.read_csv("NCAA_School_Stats_Tempo_Free_2019.csv")
    df_2018 = pd.read_csv("NCAA_School_Stats_Tempo_Free_2018.csv")
    df_2017 = pd.read_csv("NCAA_School_Stats_Tempo_Free_2017.csv")
    df_2016 = pd.read_csv("NCAA_School_Stats_Tempo_Free_2016.csv")
    df_2015 = pd.read_csv("NCAA_School_Stats_Tempo_Free_2015.csv")
    df_2021.set_index('Team', inplace=True)
    df_2019.set_index('Team', inplace=True)
    df_2018.set_index('Team', inplace=True)
    df_2017.set_index('Team', inplace=True)
    df_2016.set_index('Team', inplace=True)
    df_2015.set_index('Team', inplace=True)
    w_adjoe = [None]*len(df.index)
    l_adjoe = [None]*len(df.index)
    w_adjde = [None]*len(df.index)
    l_adjde = [None]*len(df.index)
    w_pyth = [None]*len(df.index)
    l_pyth = [None]*len(df.index)
    w_ftr = [None]*len(df.index)
    l_ftr = [None]*len(df.index)
    w_tor = [None]*len(df.index)
    l_tor = [None]*len(df.index)
    w_tord = [None]*len(df.index)
    l_tord = [None]*len(df.index)
    w_adjt = [None]*len(df.index)
    l_adjt = [None]*len(df.index)
    for i in range(len(df.index)):
        team_w = df.iloc[i]['WTEAM']
        team_l = df.iloc[i]['LTEAM']
        year = df.iloc[i]['YEAR']
        if year == 2021:
            w_adjoe[i] = df_2021.loc[team_w]['AdjOE']
            l_adjoe[i] = df_2021.loc[team_l]['AdjOE']
            w_adjde[i] = df_2021.loc[team_w]['AdjDE']
            l_adjde[i] = df_2021.loc[team_l]['AdjDE']
            w_ftr[i] = df_2021.loc[team_w]['FTR']
            l_ftr[i] = df_2021.loc[team_l]['FTR']
            w_tor[i] = df_2021.loc[team_w]['TOR']
            l_tor[i] = df_2021.loc[team_l]['TOR']
            w_tord[i] = df_2021.loc[team_w]['TORD']
            l_tord[i] = df_2021.loc[team_l]['TORD']
            w_adjt[i] = df_2021.loc[team_w]['Adj T.']
            l_adjt[i] = df_2021.loc[team_l]['Adj T.']
        elif year == 2019:
            w_adjoe[i] = df_2019.loc[team_w]['AdjOE']
            l_adjoe[i] = df_2019.loc[team_l]['AdjOE']
            w_adjde[i] = df_2019.loc[team_w]['AdjDE']
            l_adjde[i] = df_2019.loc[team_l]['AdjDE']
            w_ftr[i] = df_2019.loc[team_w]['FTR']
            l_ftr[i] = df_2019.loc[team_l]['FTR']
            w_tor[i] = df_2019.loc[team_w]['TOR']
            l_tor[i] = df_2019.loc[team_l]['TOR']
            w_tord[i] = df_2019.loc[team_w]['TORD']
            l_tord[i] = df_2019.loc[team_l]['TORD']
            w_adjt[i] = df_2019.loc[team_w]['Adj T.']
            l_adjt[i] = df_2019.loc[team_l]['Adj T.']
        elif year == 2018:
            w_adjoe[i] = df_2018.loc[team_w]['AdjOE']
            l_adjoe[i] = df_2018.loc[team_l]['AdjOE']
            w_adjde[i] = df_2018.loc[team_w]['AdjDE']
            l_adjde[i] = df_2018.loc[team_l]['AdjDE']
            w_ftr[i] = df_2018.loc[team_w]['FTR']
            l_ftr[i] = df_2018.loc[team_l]['FTR']
            w_tor[i] = df_2018.loc[team_w]['TOR']
            l_tor[i] = df_2018.loc[team_l]['TOR']
            w_tord[i] = df_2018.loc[team_w]['TORD']
            l_tord[i] = df_2018.loc[team_l]['TORD']
            w_adjt[i] = df_2018.loc[team_w]['Adj T.']
            l_adjt[i] = df_2018.loc[team_l]['Adj T.']
        elif year == 2017:
            w_adjoe[i] = df_2017.loc[team_w]['AdjOE']
            l_adjoe[i] = df_2017.loc[team_l]['AdjOE']
            w_adjde[i] = df_2017.loc[team_w]['AdjDE']
            l_adjde[i] = df_2017.loc[team_l]['AdjDE']
            w_ftr[i] = df_2017.loc[team_w]['FTR']
            l_ftr[i] = df_2017.loc[team_l]['FTR']
            w_tor[i] = df_2017.loc[team_w]['TOR']
            l_tor[i] = df_2017.loc[team_l]['TOR']
            w_tord[i] = df_2017.loc[team_w]['TORD']
            l_tord[i] = df_2017.loc[team_l]['TORD']
            w_adjt[i] = df_2017.loc[team_w]['Adj T.']
            l_adjt[i] = df_2017.loc[team_l]['Adj T.']
        elif year == 2016:
            w_adjoe[i] = df_2016.loc[team_w]['AdjOE']
            l_adjoe[i] = df_2016.loc[team_l]['AdjOE']
            w_adjde[i] = df_2016.loc[team_w]['AdjDE']
            l_adjde[i] = df_2016.loc[team_l]['AdjDE']
            w_ftr[i] = df_2016.loc[team_w]['FTR']
            l_ftr[i] = df_2016.loc[team_l]['FTR']
            w_tor[i] = df_2016.loc[team_w]['TOR']
            l_tor[i] = df_2016.loc[team_l]['TOR']
            w_tord[i] = df_2016.loc[team_w]['TORD']
            l_tord[i] = df_2016.loc[team_l]['TORD']
            w_adjt[i] = df_2016.loc[team_w]['Adj T.']
            l_adjt[i] = df_2016.loc[team_l]['Adj T.']
        elif year == 2015:
            w_adjoe[i] = df_2015.loc[team_w]['AdjOE']
            l_adjoe[i] = df_2015.loc[team_l]['AdjOE']
            w_adjde[i] = df_2015.loc[team_w]['AdjDE']
            l_adjde[i] = df_2015.loc[team_l]['AdjDE']   
            w_ftr[i] = df_2015.loc[team_w]['FTR']
            l_ftr[i] = df_2015.loc[team_l]['FTR']
            w_tor[i] = df_2015.loc[team_w]['TOR']
            l_tor[i] = df_2015.loc[team_l]['TOR']
            w_tord[i] = df_2015.loc[team_w]['TORD']
            l_tord[i] = df_2015.loc[team_l]['TORD']
            w_adjt[i] = df_2015.loc[team_w]['Adj T.']
            l_adjt[i] = df_2015.loc[team_l]['Adj T.']
        w_pyth[i] = (w_adjoe[i] ** 11.5) / (w_adjoe[i] ** 11.5 + w_adjde[i] ** 11.5)
        l_pyth[i] = (l_adjoe[i] ** 11.5) / (l_adjoe[i] ** 11.5 + l_adjde[i] ** 11.5)
    df['WPyth'] = w_pyth
    df['LPyth'] = l_pyth
    df['WAdjOE'] = w_adjoe
    df['LAdjOE'] = l_adjoe
    df['WAdjDE'] = w_adjde
    df['LAdjDE'] = l_adjde
    df['WTOR'] = w_tor
    df['WTORD'] = w_tord
    df['LTOR'] = l_tor
    df['LTORD'] = l_tord 
    df['WAdjT'] = w_adjt
    df['LAdjT'] = l_adjt
    return df

def get_sim_score(team_a, team_b_index, df_2023, previous_ncaa_games_df, MAX_DIST, w_team):
    team_a_pyth = df_2023.loc[team_a]['Pyth']
    if w_team:
        team_b_pyth = previous_ncaa_games_df.iloc[team_b_index]['WPyth']
    else:
        team_b_pyth = previous_ncaa_games_df.iloc[team_b_index]['LPyth']
    dist = math.fabs(team_a_pyth - team_b_pyth)
    return 1 - (dist/MAX_DIST)


def get_max_distance(previous_ncaa_games_df, df_2023):
    max_pyth = max(df_2023['Pyth'])
    min_pyth = min(min(previous_ncaa_games_df['WPyth']),min(previous_ncaa_games_df['LPyth']))
    return max_pyth - min_pyth

def get_pyth(team_a, df_2023):
    team_a_adjoe = df_2023.loc[team_a]['AdjOE']
    team_a_adjde = df_2023.loc[team_a]['AdjDE']
    return (team_a_adjoe**11.5) / (team_a_adjoe**11.5 + team_a_adjde**11.5)

def get_outcome(team_a, team_b, df_2023, previous_ncaa_games_df, MAX_DIST):
    top = []
    for i in range(len(previous_ncaa_games_df.index)):
        team_c = previous_ncaa_games_df.iloc[i]['WTEAM']
        team_d = previous_ncaa_games_df.iloc[i]['LTEAM']
        year = previous_ncaa_games_df.iloc[i]['YEAR']
        sim_a_c = get_sim_score(team_a, i, df_2023, previous_ncaa_games_df, MAX_DIST, True)
        sim_a_d = get_sim_score(team_a, i, df_2023, previous_ncaa_games_df, MAX_DIST, False)
        sim_b_c = get_sim_score(team_b, i, df_2023, previous_ncaa_games_df, MAX_DIST, True)
        sim_b_d = get_sim_score(team_b, i, df_2023, previous_ncaa_games_df, MAX_DIST, False)
        weight_a_c = sim_a_c / (sim_a_c + sim_a_d)
        weight_a_d = sim_a_d / (sim_a_c + sim_a_d)
        weight_b_c = sim_b_c / (sim_b_c + sim_b_d)
        weight_b_d = sim_b_d / (sim_b_c + sim_b_d)
        unified_sim_score = (weight_a_c * sim_a_c + weight_a_d * sim_a_d + weight_b_c * sim_b_c + weight_b_d * sim_b_d)/2
        top.append([team_c, team_d, year, unified_sim_score, sim_a_c, sim_a_d, sim_b_c, sim_b_d])
    top.sort(key=lambda x:x[3], reverse=True)
    #Get top 30 games
    top = top[:45]
    w_ab = 0
    l_ab = 0
    l_ba = 0
    w_ba = 0
    for i in range(len(top)):
        w_ab += top[i][4]*top[i][3]
        l_ab += top[i][5]*top[i][3]
        w_ba += top[i][6]*top[i][3]
        l_ba += top[i][7]*top[i][3]
    p_ab = (w_ab + l_ba) / (w_ab + l_ab + w_ba + l_ba)
    return p_ab
    

def main():
    print("Setting up preliminaries...")
    # Set up dataframes
    df = pd.read_csv("data_cleaned.csv")
    previous_ncaa_games_df = add_data(df)
    df_2023 = pd.read_csv("NCAA_School_Stats_Tempo_Free_2023.csv")
    df_2023.set_index('Team', inplace=True)
    # Calculate Pythagorean Expectation
    pyth = [None]*len(df_2023.index)
    for i in range(len(df_2023.index)):
        pyth[i] = get_pyth(df_2023.index[i], df_2023)
    df_2023['Pyth'] = pyth
    # Calculate max distance
    MAX_DIST = get_max_distance(previous_ncaa_games_df, df_2023)
    #Get team names
    while True:
        team_a = input("Enter team A: ")
        team_b = input("Enter team B: ")
        outcome = get_outcome(team_a, team_b, df_2023, previous_ncaa_games_df, MAX_DIST)
        if outcome > 0.5:
            outcome = round(outcome*100, 3)
            print(f"{team_a} has a {outcome}% chance of winning the game")
        else:
            outcome = 1 - outcome
            outcome = round(outcome*100, 3)
            print(f"{team_b} has a {outcome}% chance of winning the game")
        cont = input("Continue (Y/N)? ")
        if cont != "Y":
            break

if __name__ == '__main__':
    main()