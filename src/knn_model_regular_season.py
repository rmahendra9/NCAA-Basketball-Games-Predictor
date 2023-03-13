import math
import pandas as pd

"""
Step 1: Create a similarity metric based on distance between teams AdjOE/AdjDE (scaled from 0 to 1)
Step 2: d_norm / max(distance) and sim = 1 - d_norm

Sim score between games: A/B and C/D
Take Sim(A,C), Sim(A,D), Sim(B,C), Sim(B,D)
Weight(A/C) = Similarity Score(A,C) / (Similarity Score(A,C) + Similarity Score(A,D))
Weight(A/D) = Similarity Score(A,D) / (Similarity Score(A,C) + Similarity Score(A,D)) 
Weight(B/C) = Similarity Score(B,C) / (Similarity Score(B,C) + Similarity Score(B,D))
Weight(B/D) = Similarity Score(B,D) / (Similarity Score(B,C) + Similarity Score(B,D))
Unified Similarity Score = (Weight(A/C) * Similarity Score(A,C)) + (Weight(A/D) * Similarity Score(A,D)) + (Weight(B/C) * Similarity Score(B,C)) + (Weight(B/D) * Similarity Score(B,D))

Option 2: (A,B) in a vector, just find distance to (C,D) (higher seed first) and do distance on pairs

"""
def get_max_dist(df):
    max_dist = float("-inf")
    for i in range(len(df.index)):
        for j in range(i+1, len(df.index)):
            team_a_adjoe = df.loc[df.index[i]]['AdjOE']
            team_a_adjde = df.loc[df.index[i]]['AdjDE']
            team_b_adjoe = df.loc[df.index[j]]['AdjOE']
            team_b_adjde = df.loc[df.index[j]]['AdjDE']
            dist = math.sqrt((team_a_adjoe - team_b_adjoe)**2 + (team_a_adjde - team_b_adjde)**2)
            max_dist = max(max_dist, dist)
    return max_dist

def get_sim_score(team_a, team_b, stats_df, MAX_DIST):
    #If a team is not in the stats_df, return
    if team_a not in stats_df.index or team_b not in stats_df.index:
        return 0
    team_a_adjoe = stats_df.loc[team_a]['AdjOE']
    team_a_adjde = stats_df.loc[team_a]['AdjDE']
    team_b_adjoe = stats_df.loc[team_b]['AdjOE']
    team_b_adjde = stats_df.loc[team_b]['AdjDE']
    dist = math.sqrt((team_a_adjoe - team_b_adjoe)**2 + (team_a_adjde - team_b_adjde)**2)
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
    #Get top 20 opponents
    top_sim_opp = top_sim_opp[:20]
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
    #Get top 20 opponents
    top_sim_opp = top_sim_opp[:20]
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

def main(team_a, team_b):
    #Read CSV
    stats_df = pd.read_csv("NCAA_School_Stats_Tempo_Free.csv")
    gamelog_df = pd.read_csv("NCAA_Game_Log.csv")
    #Set_indexes
    stats_df = stats_df.set_index("Team")
    gamelog_df = gamelog_df.set_index("School")
    #Get max_dist
    MAX_DIST = 42.240598070221495
    outcome = get_outcome(team_a, team_b, gamelog_df, stats_df, MAX_DIST)
    print("Team A: " + team_a + "\tTeam B: " + team_b + "\t" + str(outcome))

if __name__ == "__main__":
    import sys
    if(len(sys.argv) < 3):
        print("Usage: knn_model_regular_season.py <Team A> <Team B>")
        exit(-1)
    team_a = sys.argv[1]
    team_b = sys.argv[2]
    main(team_a, team_b)




