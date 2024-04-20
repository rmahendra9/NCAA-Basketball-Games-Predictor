import pandas as pd
# This implements an idea found on this website: https://thepowerrank.com/cbb-analytics/

def main():
    #Preliminaries
    df = pd.read_csv("NCAA_School_Stats_Tempo_Free_2024.csv")
    df = df.set_index("Team")
    #Get team names
    POSSESSIONS = 70
    while True:
        team_a = input("Enter team A: ")
        team_b = input("Enter team B: ")
        # Get team A adjoe and team B adjde and subtract
        team_a_adjoe = df.loc[team_a]['AdjOE']
        team_b_adjde = df.loc[team_b]['AdjDE']
        team_a_predicted_adjoe = (team_a_adjoe - 100) - (100 - team_b_adjde) + 100
        team_a_predicted_points = (team_a_predicted_adjoe * POSSESSIONS) / 100
        # Repeat for team_b 
        team_b_adjoe = df.loc[team_b]['AdjOE']
        team_a_adjde = df.loc[team_a]['AdjDE']
        team_b_predicted_adjoe = (team_b_adjoe - 100) - (100 - team_a_adjde) + 100
        team_b_predicted_points = (team_b_predicted_adjoe * POSSESSIONS) / 100
        print(f'Predicted Result: {team_a} - {team_a_predicted_points} \t {team_b_predicted_points} - {team_b}')
        print(team_a + " wins") if team_a_predicted_points > team_b_predicted_points else print(team_b + " wins")
        cont = input("Continue (Y/N): ")
        if cont != "Y":
            break

if __name__ == '__main__':
    main()