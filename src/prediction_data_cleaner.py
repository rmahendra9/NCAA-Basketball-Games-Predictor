import pandas as pd

#Read Data
school_stats_2024_df = pd.read_csv("Tempo_Free_Statistics_2024.csv")
rt_rating_2024_df = pd.read_csv("R+T_Rating_2024.csv")

#Data Preprocessing of Tempo Free Stats
def clean_tempo_free_stats(df):
    df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    df.set_index('Team')

clean_tempo_free_stats(school_stats_2024_df)

cols = ['Team', 'R+T']
def clean_rt_rating_stats(df):
    new_df = df[cols]
    new_df.set_index('Team')
    return new_df

rt_rating_2024_df = clean_rt_rating_stats(rt_rating_2024_df)

#Merge Dataset
all_stats_2024_df = pd.merge(school_stats_2024_df, rt_rating_2024_df, on='Team', how='inner')

cols = ['Team', 'AdjO', 'AdjD', 'SOS (AdjEM)', 'R+T']
def clean_merged_stats(df):
    new_df = df[cols]
    new_df.set_index('Team')
    return new_df

all_stats_2024_df = clean_rt_rating_stats(all_stats_2024_df)

#Save dataframe
def save_dfs(name, df):
    rows = df.values
    headers = df.columns
    table_name = name
    pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")

save_dfs("Cleaned_Merged_Stats_2024", all_stats_2024_df)