import config
import requests
from bs4 import BeautifulSoup
import os
import json


def refresh_game_urls():
    with requests.session() as s:
        print("Refreshing the game urls")
        # login and search for league games
        print("Logging in")
        r = s.post(config.login_url, data=config.login_payload)

        if r.status_code == 200:
            print("Logged in successfully")
        else:
            raise Exception(
                f"Unable to refresh game urls. Status code {s.status_code} returned"
            )

        print("Searching for league games")
        r = s.post(config.fixtures_search, data=config.fixtures_payload)

        # structure html and find table containing game ids
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find_all("table", {"id": "queryResultsTable_2"})
        else:
            raise Exception(
                f"Unable to refresh game urls. Status code {r.status_code} returned"
            )

        # extract game ids
        if table:
            for row in table:
                row = row.find_all("a", {"class": "view_list_data"})
                game_urls = sorted([r["href"].split("=")[2] for r in row])
        else:
            raise ValueError("No table found :(")

        print(f"Extracted {len(game_urls)} games")

        # write to local file
        print("Writing gms game ids to local storage")
        if not os.path.isdir(config.local_storage):
            print("Directory does not exist for local storage so creating one")
            os.mkdir(config.local_storage)
        json_game_urls = json.dumps(game_urls)
        with open(
            config.local_storage + config.game_id_filename + ".json", "w"
        ) as outfile:
            outfile.write(json_game_urls)

    return None


if __name__ == "__main__":
    refresh_game_urls()
