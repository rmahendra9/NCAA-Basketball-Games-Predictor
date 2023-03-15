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

