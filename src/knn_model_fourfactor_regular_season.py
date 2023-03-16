import math
import pandas as pd

def get_max_dist(df):
    max_dist = float("-inf")
    for i in range(len(df.index)):
        for j in range(i+1,len(df.index)):
            team_a_efg = df.iloc[i]['EFG%'] / 100
            team_b_efg = df.iloc[j]['EFG%'] / 100
            team_a_tov = (df.iloc[i]['TORD'] - df.iloc[i]['TOR']) / 100
            team_b_tov = (df.iloc[j]['TORD'] - df.iloc[j]['TOR']) / 100
            team_a_ftr = df.iloc[i]['FTR'] / 100
            team_b_ftr = df.iloc[j]['FTR'] / 100
            team_a_orb = df.iloc[i]['ORB'] / 100
            team_b_orb = df.iloc[j]['ORB'] / 100
            team_a_drb = df.iloc[i]['DRB'] / 100
            team_b_drb = df.iloc[j]['DRB'] / 100
            dist = math.sqrt((team_a_efg - team_b_efg)**2 + (team_a_tov - team_b_tov)**2 + (team_a_ftr - team_b_ftr)**2 + (team_a_orb - team_b_orb)**2 + (team_a_drb + team_b_drb)**2)
            max_dist = max(max_dist, dist)
    return max_dist

def get_sim_score(team_a, team_b, stats_df, MAX_DIST):
    #If a team is not in the stats_df, return
    if team_a not in stats_df.index or team_b not in stats_df.index:
        return 0
    team_a_efg = stats_df.loc[team_a]['EFG%'] / 100
    team_b_efg = stats_df.loc[team_b]['EFG%'] / 100
    team_a_tov = (stats_df.loc[team_a]['TORD'] - stats_df.loc[team_a]['TOR']) / 100
    team_b_tov = (stats_df.loc[team_b]['TORD'] - stats_df.loc[team_b]['TOR']) / 100
    team_a_ftr = stats_df.loc[team_a]['FTR'] / 100
    team_b_ftr = stats_df.loc[team_b]['FTR'] / 100
    team_a_orb = stats_df.loc[team_a]['ORB'] / 100
    team_b_orb = stats_df.loc[team_b]['ORB'] / 100
    team_a_drb = stats_df.loc[team_a]['DRB'] / 100
    team_b_drb = stats_df.loc[team_b]['DRB'] / 100
    dist = math.sqrt((team_a_efg - team_b_efg)**2 + (team_a_tov - team_b_tov)**2 + (team_a_ftr - team_b_ftr)**2 + (team_a_orb - team_b_orb)**2 + (team_a_drb + team_b_drb)**2)
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

def main():
    print("Setting up preliminaries...")
    #Read CSV
    stats_df = pd.read_csv("NCAA_School_Stats_Tempo_Free_2023.csv")
    gamelog_df = pd.read_csv("NCAA_Game_Log.csv")
    #Set_indexes
    stats_df = stats_df.set_index("Team")
    gamelog_df = gamelog_df.set_index("School")
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