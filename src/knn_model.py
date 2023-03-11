import pandas as pd
import math

"""
Formulas: Wa,b = db,t * Oa,t for k-similar teams t to b
          La,b = db,t * (1 - Oa,t) k-similar teams t to b

Pa,b = Wa,b + Lb,a / (Wa,b + Lb,a + Wb,a + La,b)

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

def get_similarity_scores(df):
    max_dist = float("-inf")
    for i in range(len(df.index)):
        for j in range(i+1,len(df.index)):
            team_a_adjoe = df.loc[df.index[i]]["AdjOE"]
            team_a_adjde = df.loc[df.index[i]]["AdjDE"]
            team_b_adjoe = df.loc[df.index[j]]["AdjOE"]
            team_b_adjde = df.loc[df.index[j]]["AdjDE"]
            dist = math.sqrt((team_a_adjoe - team_b_adjoe)**2 + (team_a_adjde - team_b_adjde)**2)
            max_dist = max(max_dist, dist)
    


df = pd.read_csv("NCAA_School_Stats_Tempo-Free.csv")
df = df.set_index("Team")
get_similarity_scores(df)




