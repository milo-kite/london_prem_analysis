import pandas as pd
import config

def refresh_analysis():
    # reading data
    print('Performing analysis')
    league_data = pd.read_csv(config.local_storage + config.raw_data + ".csv")
    league_data['weighting'] = 1

    # aggregating all actions into player data
    print('Calculating player stats')
    pivoted_league_data = league_data.groupby(['Player', 'type', 'Team']).count()
    pivoted_league_data = pd.pivot_table(pivoted_league_data, index=['Player', 'Team'], columns='type',
                                         values='weighting').fillna(0).astype(int)
    pivoted_league_data['Goals'] = pivoted_league_data['Field Goal'] + pivoted_league_data['Penalty Corner']
    pivoted_league_data = pivoted_league_data.reset_index()
    pivoted_league_data = pivoted_league_data.sort_values('Goals', ascending=False)
    pivoted_league_data.to_csv(config.local_storage + config.analysed_player_filename + ".csv", index=False)

    # aggregating all actions further into team data
    print('Calculating team stats')
    team_data = league_data.groupby(['type', 'Team']).count()
    team_data = pd.pivot_table(team_data, index='Team', columns='type', values='weighting').fillna(0).astype(int)
    team_data['Goals'] = team_data['Field Goal'] + team_data['Penalty Corner']
    team_data = team_data.sort_values('Goals', ascending=False)
    team_data.to_csv(config.local_storage + config.analysed_team_filename + ".csv")