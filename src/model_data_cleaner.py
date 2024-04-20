import pandas as pd

#Read Data
school_stats_2021_df = pd.read_csv("Tempo_Free_Statistics_2021.csv")
school_stats_2022_df = pd.read_csv("Tempo_Free_Statistics_2022.csv")
school_stats_2023_df = pd.read_csv("Tempo_Free_Statistics_2023.csv")

rt_rating_2021_df = pd.read_csv("R+T_Rating_2021.csv")
rt_rating_2022_df = pd.read_csv("R+T_Rating_2022.csv")
rt_rating_2023_df = pd.read_csv("R+T_Rating_2023.csv")

#Data Preprocessing of Tempo Free Stats
def clean_tempo_free_stats(df):
    df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    df.set_index('Team')

clean_tempo_free_stats(school_stats_2021_df)
clean_tempo_free_stats(school_stats_2022_df)
clean_tempo_free_stats(school_stats_2023_df)

#Data Preprocessing of R+T Rating
cols = ['Team', 'R+T']
def clean_rt_rating_stats(df):
    new_df = df[cols]
    new_df.set_index('Team')
    return new_df

rt_rating_2021_df = clean_rt_rating_stats(rt_rating_2021_df)
rt_rating_2022_df = clean_rt_rating_stats(rt_rating_2022_df)
rt_rating_2023_df = clean_rt_rating_stats(rt_rating_2023_df)

#Merge Datasets
all_stats_2023_df = pd.merge(school_stats_2023_df, rt_rating_2023_df, on='Team', how='inner')
all_stats_2022_df = pd.merge(school_stats_2022_df, rt_rating_2022_df, on='Team', how='inner')
all_stats_2021_df = pd.merge(school_stats_2021_df, rt_rating_2021_df, on='Team', how='inner')

#Clean Merged Dataset down to requisite features
cols = ['Team', 'AdjO', 'AdjD', 'SOS (AdjEM)', 'R+T']
def clean_merged_stats(df):
    new_df = df[cols]
    new_df.set_index('Team')
    return new_df

all_stats_2021_df = clean_rt_rating_stats(all_stats_2021_df)
all_stats_2022_df = clean_rt_rating_stats(all_stats_2022_df)
all_stats_2023_df = clean_rt_rating_stats(all_stats_2023_df)

#Save dataframes
def save_dfs(name, df):
    rows = df.values
    headers = df.columns
    table_name = name
    pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")

save_dfs("Cleaned_Merged_Stats_2023", all_stats_2023_df)
save_dfs("Cleaned_Merged_Stats_2022", all_stats_2022_df)
save_dfs("Cleaned_Merged_Stats_2021", all_stats_2021_df)



