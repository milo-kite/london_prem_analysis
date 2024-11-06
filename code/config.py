import pandas as pd
from datetime import date
import os

email = "your@email.com"
password = "your_password"

# pandas display options
pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 10)
pd.set_option("display.width", 300)

# run configurations, replace with your username
current_directory = os.getcwd()
local_storage = current_directory + r"/data/ones/"
game_id_filename = "game_ids"
raw_data = "thd_data"
analysed_player_filename = "analysed_player_data"
analysed_team_filename = "analysed_team_data"
competition_index_key = "6E0F8F4C7D5C2E7D1E"
today = date.today().strftime("%d-%m-%Y")
spreadsheet_id = "spreadsheet_id"

# urls needed to read and write data
login_url = r"https://secure.whostheumpire.com/db_admin/index.php?login=Y"
fixtures_search = "https://secure.whostheumpire.com/db_admin/fixtures.php?function=view"
fixture_view = (
    r"https://secure.whostheumpire.com/db_admin/fixtures.php?function=view&index_key="
)
hockey_fixtures_url = r"https://hockeyfixtures.co.uk/league/view/240"

# info needed for logging in. Replace with your email and password
login_payload = {
    "email": email,
    "password": password,
    "databasetouse": "hockey",
    "t_and_c_agreement_run": "on",
}

# info needed to search for league games
fixtures_payload = {
    "clicked_find_counter": 0,
    "find_from_date": "01-09-2024",
    "find_team_index_key": 0,
    "find_month": 0,
    "find_dow": 0,
    "find_fixture_status": 0,
    "find_level": "*",
    "find_to_date": today,
    "find_competition_index_key": competition_index_key,
    "find_venue_index_key": 0,
    "find_organisation_index_key": 0,
    "find_gender": "E",
    "find": "go",
}

# making acronyms more readable
mapping_dictionary = {
    "GC": "Green Card",
    "YC": "Yellow Card",
    "RC": "Red Card",
    "FG": "Field Goal",
    "PS": "Penalty Stroke",
    "PC": "Penalty Corner",
}
