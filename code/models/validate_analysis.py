import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

import config


def validate_analysis():
    day_of_week = datetime.now().strftime("%A")
    if day_of_week != "Saturday":
        # reading goals scored from hockeyfixtures
        print("Validating that all goals have been extracted")
        r = requests.get(config.hockey_fixtures_url)
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", {"class": "league_table"})
        rows = table.find_all("tr", {"class": ""})

        # reading goals scored from london_prem_analysis
        team_data = pd.read_csv(
            config.local_storage + config.analysed_team_filename + ".csv"
        )

        for row in rows[1:]:
            entries = row.find_all("td")
            club = entries[2].text
            calculated_goals_scored = int(entries[7].text)

            official_goals_scored = int(
                team_data[team_data["Team"] == club]["Total Goals Scored"].values[0]
            )

            if official_goals_scored != calculated_goals_scored:
                raise Exception(
                    f"Mismatch in number of goals scored for {club}. There are {official_goals_scored} "
                    f"on hockeyfixtures.co.uk and {calculated_goals_scored} from london_prem_analysis."
                )

        print("Goals scored has been validated")
    else:
        print("Skipping goals scored validation since it's a Saturday")
    return None
