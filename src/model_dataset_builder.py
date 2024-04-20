import pandas as pd
import numpy as np

#For each tournament game, add in team A data, team B data, cross data and winner/loser (as 1 or 0 for team A win)

#Read in datasets
game_log_2023_df = pd.read_csv("NCAA_Tournament_Game_Log_2023.csv")
school_stats_2023_df = pd.read_csv("Cleaned_Merged_Stats_2023.csv")

game_log_2022_df = pd.read_csv("NCAA_Tournament_Game_Log_2022.csv")
school_stats_2022_df = pd.read_csv("Cleaned_Merged_Stats_2022.csv")

game_log_2021_df = pd.read_csv("NCAA_Tournament_Game_Log_2021.csv")
school_stats_2021_df = pd.read_csv("Cleaned_Merged_Stats_2021.csv")

def build_model_data(game_log_df, school_stats_df):
    model_dataset_df = pd.DataFrame(columns=['Team_A_AdjO','Team_A_AdjD','Team_A_SOS (AdjEM)','Team_A_R+T', 'Team_A_3Pt%', 
                                             'Team_A_OReb%', 'Team_A_2Pt%D', 'Team_A_FTR', 'Team_A_Scoring_Margin', 
                                             'Team_B_AdjO','Team_B_AdjD','Team_B_SOS (AdjEM)','Team_B_R+T', 'Team_B_3Pt%', 
                                             'Team_B_OReb%', 'Team_B_2Pt%D', 'Team_B_FTR', 'Team_B_Scoring_Margin',
                                             'AdjO_Diff','AdjD_Diff','SOS_Diff (AdjEM)','R+T_Diff', '3Pt%_Diff', 
                                             'OReb%_Diff', '2Pt%D_Diff', 'FTR_Diff', 'Scoring_Margin_Diff', 'Outcome'])
    for index, row in game_log_df.iterrows():
        team_a = row['School']
        team_b = row['Opponent']
        team_a_stats = school_stats_df[school_stats_df['Team'] == team_a].values
        team_a_stats = team_a_stats[0][2:]
        team_b_stats = school_stats_df[school_stats_df['Team'] == team_b].values
        team_b_stats = team_b_stats[0][2:]
        cross_stats = team_a_stats - team_b_stats
        outcome = 1 if row['Result/Line'] == 'W' else 0
        new_row = np.concatenate((team_a_stats, team_b_stats, cross_stats))
        new_row = np.append(new_row, outcome)
        entry = pd.DataFrame([new_row], columns=model_dataset_df.columns)
        model_dataset_df = pd.concat([model_dataset_df, entry], ignore_index=True)
    return model_dataset_df

model_data_2023_df = build_model_data(game_log_2023_df, school_stats_2023_df)
model_data_2022_df = build_model_data(game_log_2022_df, school_stats_2022_df)
model_data_2021_df = build_model_data(game_log_2021_df, school_stats_2021_df)

model_dataset_df = pd.concat([model_data_2021_df, model_data_2022_df, model_data_2021_df], ignore_index=True)

rows = model_dataset_df.values
headers = model_dataset_df.columns
table_name = "model_data_more_features"
pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")


    
