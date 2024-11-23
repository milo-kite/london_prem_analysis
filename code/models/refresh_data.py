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
    other_team = []
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
                        other_team.append(away_team)
                    elif len(split_data) == 3:
                        row_player, _, row_type = split_data
                        team.append(away_team)
                        other_team.append(home_team)

                    player.append(row_player)
                    action.append(row_type)

    # creating a dataFrame from all the gathered data
    df = pd.DataFrame(
        {
            "minute": minute,
            "Player": player,
            "type": action,
            "Team": team,
            "Other Team": other_team,
            "game_id": game_id,
        }
    )

    df["type"] = df["type"].map(config.mapping_dictionary)
    df["Player"] = df["Player"].map(str.title)

    # writing to local storage
    df.to_csv(config.local_storage + config.raw_data + ".csv", index=False)

    print("Searching for team's schedule")
    r = s.post(config.fixtures_search, data=config.schedule_payload)

    # structure html and find table containing game ids
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", {"id": "queryResultsTable_2"})
    else:
        raise Exception(
            f"Unable to refresh game urls. Status code {r.status_code} returned"
        )

    print("Extracting fixtures")
    # extract fixtures

    game_dates = []
    home_teams = []
    away_teams = []
    if table:
        for row in table.find_all("tr"):
            row = row.find_all("td", {"class": "view_list_data"})
            game_date = [
                span.text
                for r in row
                for span in r.find_all("span")
                if span.get("title")
            ]
            if game_date:
                home_team = row[6].find("a").get_text(strip=True)
                away_team = row[5].find("a").get_text(strip=True)

                game_dates.append(game_date[0])
                home_teams.append(home_team)
                away_teams.append(away_team)
    else:
        raise ValueError("No table found :(")

    schedule_df = pd.DataFrame(
        {
            "Date": game_dates,
            "Home": home_teams,
            "Away": away_teams,
        }
    )

    schedule_df.to_csv(
        config.local_storage + config.schedule_data + ".csv", index=False
    )
