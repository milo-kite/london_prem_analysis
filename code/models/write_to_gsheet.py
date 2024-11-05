import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import csv
from datetime import datetime

# contains your login details
import config


def write_to_gsheet():
    # writing to GSheet
    print("Writing to GSheet")
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    credentials = None
    if os.path.exists("credentials/token.json"):
        # giving authorisation to gsheets
        credentials = Credentials.from_authorized_user_file(
            "credentials/token.json", scopes
        )

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/gsheet_oauth_budget.json", scopes
            )
            credentials = flow.run_local_server(port=0)
        with open("credentials/token.json", "w") as token:
            token.write(credentials.to_json())

    service = build("sheets", "v4", credentials=credentials)

    with open(
        config.local_storage + config.analysed_team_filename + ".csv",
        mode="r",
        newline="",
        encoding="utf-8",
    ) as csvfile:
        reader = csv.reader(csvfile)
        team_stats = list(reader)

    body = {"values": team_stats}
    service.spreadsheets().values().update(
        spreadsheetId=config.spreadsheet_id,
        range="'Team View'!A1",
        valueInputOption="RAW",
        body=body,
    ).execute()

    with open(
        config.local_storage + config.analysed_player_filename + ".csv",
        mode="r",
        newline="",
        encoding="utf-8",
    ) as csvfile:
        reader = csv.reader(csvfile)
        player_stats = list(reader)

    body = {"values": player_stats}
    service.spreadsheets().values().update(
        spreadsheetId=config.spreadsheet_id,
        range="'Player View'!A1",
        valueInputOption="RAW",
        body=body,
    ).execute()
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    service.spreadsheets().values().update(
        spreadsheetId=config.spreadsheet_id,
        range="'Player View'!J3",
        valueInputOption="RAW",
        body={"values": [[current_datetime]]},
    ).execute()

    service.spreadsheets().values().update(
        spreadsheetId=config.spreadsheet_id,
        range="'Team View'!I3",
        valueInputOption="RAW",
        body={"values": [[current_datetime]]},
    ).execute()

    return None
