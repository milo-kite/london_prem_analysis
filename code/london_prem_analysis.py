import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os

# contains your login details
import config

if config.email == 'your@email.com' or config.password == 'your_password':
        raise Exception(f'Update your username and password in the config.py file')

# toggle to run relevant parts of the code
refresh_game_urls = True
refresh_data = True
refresh_analysis = True
validate_game_numbers = True

# initialising lists to add game data into
minute = []
player = []
action = []
team = []
game_id = []

total_games = 0

if refresh_game_urls:
    with requests.session() as s:
        print('Refreshing the game urls')
        # login and search for league games
        print('Logging in')
        s.post(config.login_url, data=config.login_payload)
        print('Searching for league games')
        r = s.post(config.fixtures_search, data=config.fixtures_payload)

        # structure html and find table containing game ids
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.find_all('table', {'id': 'queryResultsTable_2'})
        else:
            raise Exception(f"Unable to refresh game urls. Status code {r.status_code} returned")

        # extract game ids
        for row in table:
            row = row.find_all('a', {'class': 'view_list_data'})
            game_urls = sorted([r['href'].split('=')[2] for r in row])

        print(f'Extracted {len(game_urls)} games')

        # write to local file
        print('Writing gms game ids to local storage')
        if not os.path.isdir(config.local_storage):
            print('Directory does not exist for local storage so creating one')
            os.mkdir(config.local_storage)
        json_game_urls = json.dumps(game_urls)
        with open(config.local_storage + config.game_id_filename + ".json", "w") as outfile:
            outfile.write(json_game_urls)

if validate_game_numbers:
    print('Validating that all games from gms have been extracted')
    r = requests.get(config.hockey_fixtures_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find("table", {"class": "league_table"})
    rows = table.find_all('tr', {"class": ""})
    for row in rows[1:]:
        entries = row.find_all('td')
        total_games += int(entries[3].text)

    with open(config.local_storage + config.game_id_filename + ".json", "r") as infile:
        game_urls = json.load(infile)

    if total_games/2 == len(game_urls):
        print(f'All {len(game_urls)} games extracted from last game_url extraction')
    else:
        raise Exception(f'Mismatch in number of games extracted. There are {int(total_games/2)} on hockeyfixtures.co.uk'
                        f' and {len(game_urls)} extracted from gms')

if refresh_data:
    with requests.session() as s:
        print('Refreshing game data')

        # log in and open game ids generated above
        s.post(config.login_url, data=config.login_payload)

        with open(config.local_storage + config.game_id_filename + ".json", "r") as infile:
            game_urls = json.load(infile)

        # loop through game ids to extract the data
        for n, game_url in enumerate(game_urls):

            # finding the table that shows the game actions
            r = s.get(config.fixture_view + game_url)
            if r.status_code != 200:
                raise Exception(f'Unable to find game id {game_id}')
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find_all('table')[-1]
            for row in table.find_all('tr', {'class': 'view_list_row'}):

                # adding the team names
                if row.find('td', {'class': 'view_list_data'}) is None:
                    entries = row.find_all('th')
                    away_team = entries[1].text
                    home_team = entries[2].text
                    print(f'Writing {home_team} vs. {away_team}')

                # adding the cards and goals
                else:
                    game_id.append(n+1)
                    entries = row.find_all('td')
                    minute.append(entries[0].text.strip())

                    split_data = entries[1].text.strip().split('\n')
                    if len(split_data) == 2:
                        row_player, row_type = split_data
                        team.append(home_team)
                    elif len(split_data) == 3:
                        row_player, _, row_type = split_data
                        team.append(away_team)

                    player.append(row_player)
                    action.append(row_type)

    # creating a dataFrame from all the gathered data
    df = pd.DataFrame({'minute': minute, 'Player': player, 'type': action, 'Team': team, 'game_id': game_id})

    df['type'] = df['type'].map(config.mapping_dictionary)
    df['Player'] = df['Player'].map(str.title)

    # writing to local storage
    df.to_csv(config.local_storage + config.raw_data + ".csv", index=False)

if refresh_analysis:

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

