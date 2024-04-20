import pandas as pd
import numpy as np

#Read in datasets
school_stats_2024_df = pd.read_csv("Cleaned_Merged_Stats_2024.csv")

teams = school_stats_2024_df['Team']

def build_prediction_data(teams, school_stats_df):
    prediction_dataset_df = pd.DataFrame(columns=['Team_A','Team_A_AdjO','Team_A_AdjD','Team_A_SOS (AdjEM)','Team_A_R+T', 'Team_A_3Pt%', 
                                             'Team_A_OReb%', 'Team_A_2Pt%D', 'Team_A_FTR', 'Team_A_Scoring_Margin', 'Team_B', 
                                             'Team_B_AdjO','Team_B_AdjD','Team_B_SOS (AdjEM)','Team_B_R+T', 'Team_B_3Pt%', 
                                             'Team_B_OReb%', 'Team_B_2Pt%D', 'Team_B_FTR', 'Team_B_Scoring_Margin',
                                             'AdjO_Diff','AdjD_Diff','SOS_Diff (AdjEM)','R+T_Diff', '3Pt%_Diff', 
                                             'OReb%_Diff', '2Pt%D_Diff', 'FTR_Diff', 'Scoring_Margin_Diff'])
    for i in range(len(teams)):
        for j in range(len(teams)):
            if (teams[i] == teams[j]):
                continue
            team_a = teams[i]
            team_b = teams[j]
            team_a_stats = school_stats_df[school_stats_df['Team'] == team_a].values
            team_a_stats = team_a_stats[0][2:]
            team_b_stats = school_stats_df[school_stats_df['Team'] == team_b].values
            team_b_stats = team_b_stats[0][2:]
            cross_stats = team_a_stats - team_b_stats
            new_row = np.concatenate(([team_a], team_a_stats, [team_b], team_b_stats, cross_stats))
            entry = pd.DataFrame([new_row], columns=prediction_dataset_df.columns)
            prediction_dataset_df = pd.concat([prediction_dataset_df, entry], ignore_index=True)
    return prediction_dataset_df

prediction_dataset_df = build_prediction_data(teams, school_stats_2024_df)

rows = prediction_dataset_df.values
headers = prediction_dataset_df.columns
table_name = "prediction_data_more_features"
pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")