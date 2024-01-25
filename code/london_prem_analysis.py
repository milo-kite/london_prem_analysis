import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from datetime import date

# contains your login details
import creds

if creds.email == 'your@email.com' or creds.password == 'your_password':
        raise Exception(f'Update your username and password in the creds.py file')

# toggle to run relevant parts of the code
refresh_game_urls = True
refresh_data = True
refresh_analysis = True
validate_game_numbers = True

# pandas display options
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 300)

# urls needed to read and write data
login_url = r"https://secure.whostheumpire.com/db_admin/index.php?login=Y"
fixtures_search = r"https://secure.whostheumpire.com/db_admin/fixtures.php?function=view&api_output_type=html"
fixture_view = r"https://secure.whostheumpire.com/db_admin/fixtures.php?function=view&index_key="
hockey_fixtures_url = r"https://hockeyfixtures.co.uk/league/view/240"

# run configurations, replace with your username
current_directory = os.getcwd()
local_storage = current_directory + r"/data/ones/"
game_id_filename = "game_ids"
raw_data = "thd_data"
analysed_player_filename = "analysed_player_data"
analysed_team_filename = "analysed_team_data"
league_id = '2D2C4D7E1C5A5E5B8D'
today = date.today().strftime('%d-%m-%Y')

# info needed for logging in. Replace with your email and password
login_payload = {
    'email': creds.email,
    'password': creds.password,
    'databasetouse': 'hockey',
    't_and_c_agreement_run': 'on'
}

# info needed to search for league games
fixtures_payload = {
    'clicked_find_counter': '0',
    'find_from_date': '01-09-2023',
    'find_team_index_key': '0',
    'find_month': '0',
    'find_dow': '0',
    'find_fixture_status': '0',
    'find_level': '*',
    'find_to_date': today,
    'find_competition_index_key': league_id,
    'find_venue_index_key': '0',
    'find_organisation_index_key': '0',
    'find_gender': 'E',
    'find': 'go',
    'limit_start': '0'
}

# making acronyms more readable
mapping_dictionary = {
    'GC': 'Green Card',
    'PC': 'Penalty Corner',
    'YC': 'Yellow Card',
    'FG': 'Field Goal',
}

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
        s.post(login_url, data=login_payload)
        print('Searching for league games')
        r = s.post(fixtures_search, data=fixtures_payload)

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
        if not os.path.isdir(local_storage):
            print('Directory does not exist for local storage so creating one')
            os.mkdir(local_storage)
        json_game_urls = json.dumps(game_urls)
        with open(local_storage + game_id_filename + ".json", "w") as outfile:
            outfile.write(json_game_urls)

if validate_game_numbers:
    print('Validating that all games from gms have been extracted')
    r = requests.get(hockey_fixtures_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find("table", {"class": "league_table"})
    rows = table.find_all('tr', {"class": ""})
    for row in rows[1:]:
        entries = row.find_all('td')
        total_games += int(entries[3].text)

    with open(local_storage + game_id_filename + ".json", "r") as infile:
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
        s.post(login_url, data=login_payload)

        with open(local_storage + game_id_filename + ".json", "r") as infile:
            game_urls = json.load(infile)

        # loop through game ids to extract the data
        for n, game_url in enumerate(game_urls):

            # finding the table that shows the game actions
            r = s.get(fixture_view + game_url)
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

    df['type'] = df['type'].map(mapping_dictionary)
    df['Player'] = df['Player'].map(str.title)

    # writing to local storage
    df.to_csv(local_storage + raw_data + ".csv", index=False)

if refresh_analysis:

    # reading data
    print('Performing analysis')
    league_data = pd.read_csv(local_storage + raw_data + ".csv")
    league_data['weighting'] = 1

    # aggregating all actions into player data
    print('Calculating player stats')
    pivoted_league_data = league_data.groupby(['Player', 'type', 'Team']).count()
    pivoted_league_data = pd.pivot_table(pivoted_league_data, index=['Player', 'Team'], columns='type',
                                         values='weighting').fillna(0).astype(int)
    pivoted_league_data['Goals'] = pivoted_league_data['Field Goal'] + pivoted_league_data['Penalty Corner']
    pivoted_league_data = pivoted_league_data.reset_index()
    pivoted_league_data = pivoted_league_data.sort_values('Goals', ascending=False)
    pivoted_league_data.to_csv(local_storage + analysed_player_filename + ".csv", index=False)

    # aggregating all actions further into team data
    print('Calculating team stats')
    team_data = league_data.groupby(['type', 'Team']).count()
    team_data = pd.pivot_table(team_data, index='Team', columns='type', values='weighting').fillna(0).astype(int)
    team_data['Goals'] = team_data['Field Goal'] + team_data['Penalty Corner']
    team_data = team_data.sort_values('Goals', ascending=False)
    team_data.to_csv(local_storage + analysed_team_filename + ".csv")

