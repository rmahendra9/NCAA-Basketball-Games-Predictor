import math
import pandas as pd

def get_max_dist(df):
    return max(df['Pyth']) - min(df['Pyth'])

def get_sim_score(team_a, team_b, stats_df, MAX_DIST):
    #If a team is not in the stats_df, return
    if team_a not in stats_df.index or team_b not in stats_df.index:
        return 0
    team_a_pyth = stats_df.loc[team_a]['Pyth']
    team_b_pyth = stats_df.loc[team_b]['Pyth']
    dist = math.fabs(team_a_pyth - team_b_pyth)
    return 1 - (dist/MAX_DIST)

def get_outcome(team_a, team_b, gamelog_df, stats_df, MAX_DIST):
    #Get list of opponents for team A in regular season
    opponents_df = gamelog_df.loc[team_a]
    opponents_df = opponents_df.set_index("Opponent")
    top_sim_opp = []
    #Get sim score for team A opponents with team B
    for i in range(len(opponents_df.index)):
        sim_score = get_sim_score(team_b, opponents_df.index[i], stats_df, MAX_DIST)
        top_sim_opp.append([opponents_df.index[i], sim_score, opponents_df.iloc[i]['Result/Line']])
    #Sort the result
    top_sim_opp.sort(key=lambda x:x[1], reverse=True)
    #Get top 25 opponents
    top_sim_opp = top_sim_opp[:25]
    #Calculate Wa,b and La,b
    wab = 0
    lab = 0
    for i in range(len(top_sim_opp)):
        if top_sim_opp[i][2] == 'W':
            wab += top_sim_opp[i][1]
        else:
            lab += top_sim_opp[i][1]
    #Get list of opponents for team B in regular season
    opponents_df = gamelog_df.loc[team_b]
    opponents_df = opponents_df.set_index("Opponent")
    top_sim_opp = []
    #Get sim score for team B opponents with team A
    for i in range(len(opponents_df.index)):
        sim_score = get_sim_score(team_a, opponents_df.index[i], stats_df, MAX_DIST)
        top_sim_opp.append([opponents_df.index[i], sim_score, opponents_df.iloc[i]['Result/Line']])
    #Sort the result
    top_sim_opp.sort(key=lambda x:x[1], reverse=True)
    #Get top 25 opponents
    top_sim_opp = top_sim_opp[:25]
    #Calculate Wb,a and Lb,a
    wba = 0
    lba = 0
    for i in range(len(top_sim_opp)):
        if top_sim_opp[i][2] == 'W':
            wba += top_sim_opp[i][1]
        else:
            lba += top_sim_opp[i][1]
    #Calculate Pa,b
    pab = (wab + lba) / (wab + lba + wba + lab)
    return pab

def get_pyth(team_a, stats_df):
    team_a_adjoe = stats_df.loc[team_a]['AdjOE']
    team_a_adjde = stats_df.loc[team_a]['AdjDE']
    return (team_a_adjoe**11.5) / (team_a_adjoe**11.5 + team_a_adjde**11.5)

def main():
    print("Setting up preliminaries...")
    #Read CSV
    stats_df = pd.read_csv("NCAA_School_Stats_Tempo_Free_2023.csv")
    gamelog_df = pd.read_csv("NCAA_Game_Log.csv")
    #Set_indexes
    stats_df = stats_df.set_index("Team")
    gamelog_df = gamelog_df.set_index("School")
    pyth = [None]*len(stats_df.index)
    #Calcuate pythagorean expectation
    for i in range(len(stats_df.index)):
        pyth[i] = get_pyth(stats_df.index[i], stats_df)
    stats_df['Pyth'] = pyth
    #Get max_dist
    MAX_DIST = get_max_dist(stats_df)
    while True:
        team_a = input("Enter team A: ")
        team_b = input("Enter team B: ")
        outcome = get_outcome(team_a, team_b, gamelog_df, stats_df, MAX_DIST)
        winning_team = team_a if outcome > 0.5 else team_b
        outcome = outcome if outcome > 0.5 else 1 - outcome
        print("The winning team of this matchup is " + winning_team + " with a " + str(round(outcome*100, 3)) + "%" + " chance of winning")
        cont = input("Continue (Y/N): ")
        if cont != "Y":
            break
    
if __name__ == "__main__":
    main()