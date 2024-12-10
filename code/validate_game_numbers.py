import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

import config


def validate_game_numbers():
    day_of_week = datetime.now().strftime("%A")
    if day_of_week == "Monday":
        total_games = 0

        print("Validating that all games from gms have been extracted")
        r = requests.get(config.hockey_fixtures_url)
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", {"class": "league_table"})
        rows = table.find_all("tr", {"class": ""})
        for row in rows[1:]:
            entries = row.find_all("td")
            total_games += int(entries[3].text)

        with open(
            config.local_storage + config.game_id_filename + ".json", "r"
        ) as infile:
            game_urls = json.load(infile)

        if total_games / 2 == len(game_urls):
            print(f"All {len(game_urls)} games extracted from last game_url extraction")
        else:
            raise Exception(
                f"Mismatch in number of games extracted. There are {int(total_games/2)} on hockeyfixtures.co.uk"
                f" and {len(game_urls)} extracted from gms"
            )
    else:
        print("Skipping game numbers validation since it's not a Monday")
    return None


if __name__ == "__main__":
    validate_game_numbers()
