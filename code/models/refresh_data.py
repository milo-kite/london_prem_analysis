import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import config


def refresh_data():
    # initialising lists to add game data into
    minute = []
    player = []
    action = []
    team = []
    game_id = []

    with requests.session() as s:
        print("Refreshing game data")

        # log in and open game ids generated above
        s.post(config.login_url, data=config.login_payload)

        with open(
            config.local_storage + config.game_id_filename + ".json", "r"
        ) as infile:
            game_urls = json.load(infile)

        # loop through game ids to extract the data
        for n, game_url in enumerate(game_urls):
            # finding the table that shows the game actions
            r = s.get(config.fixture_view + game_url)
            if r.status_code != 200:
                raise Exception(f"Unable to find game id {game_id}")
            soup = BeautifulSoup(r.content, "html.parser")
            table = soup.find_all("table")[-1]
            for row in table.find_all("tr", {"class": "view_list_row"}):
                # adding the team names
                if row.find("td", {"class": "view_list_data"}) is None:
                    entries = row.find_all("th")
                    away_team = entries[1].text
                    home_team = entries[2].text
                    print(f"Writing {home_team} vs. {away_team}")

                # adding the cards and goals
                else:
                    game_id.append(n + 1)
                    entries = row.find_all("td")
                    minute.append(entries[0].text.strip())

                    split_data = entries[1].text.strip().split("\n")
                    if len(split_data) == 2:
                        row_player, row_type = split_data
                        team.append(home_team)
                    elif len(split_data) == 3:
                        row_player, _, row_type = split_data
                        team.append(away_team)

                    player.append(row_player)
                    action.append(row_type)

    # creating a dataFrame from all the gathered data
    df = pd.DataFrame(
        {
            "minute": minute,
            "Player": player,
            "type": action,
            "Team": team,
            "game_id": game_id,
        }
    )

    df["type"] = df["type"].map(config.mapping_dictionary)
    df["Player"] = df["Player"].map(str.title)

    # writing to local storage
    df.to_csv(config.local_storage + config.raw_data + ".csv", index=False)
