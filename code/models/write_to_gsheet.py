import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import csv
from datetime import datetime
import pandas as pd

import config


def write_values(service, file, starting_cell):
    body = {"values": file}
    service.spreadsheets().values().update(
        spreadsheetId=config.spreadsheet_id,
        range=starting_cell,
        valueInputOption="RAW",
        body=body,
    ).execute()


def read_csv(filename):
    with open(
        config.local_storage + filename + ".csv",
        mode="r",
        newline="",
        encoding="utf-8",
    ) as csvfile:
        reader = csv.reader(csvfile)
        file = list(reader)
    return file


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

    # writing team stats to GSheet
    team_stats = read_csv(config.analysed_team_filename)
    write_values(service, team_stats, "'Team View'!A1")

    # writing player stats to GSheet
    player_stats = read_csv(config.analysed_player_filename)
    write_values(service, player_stats, "'Player View'!A1")

    # writing last updated time to GSheet
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_values(service, [[current_datetime]], "'Player View'!L3")
    write_values(service, [[current_datetime]], "'Team View'!R3")

    # find the next team THD are playing
    schedule = pd.read_csv(config.local_storage + config.schedule_data + ".csv")
    schedule["Date"] = pd.to_datetime(schedule["Date"], format="%d-%m-%Y")
    now = datetime.today()
    today = datetime(now.year, now.month, now.day)
    teams = list(schedule[schedule["Date"] >= today].sort_values(by="Date").iloc[0])[1:]
    next_game = list(filter(lambda team: team != "Tulse Hill & Dulwich M1", teams))[0]

    # highlighting players from next game
    format_requests = []
    rows = [i for i, row in enumerate(player_stats) if row[1] == next_game]

    # clearing colour
    clear_format_request = {
        "requests": [
            {
                "updateCells": {
                    "range": {
                        "sheetId": 1476248146,
                        "startRowIndex": 1,
                        "endRowIndex": 200,
                        "startColumnIndex": 0,
                        "endColumnIndex": 9,
                    },
                    "rows": [
                        {
                            "values": [
                                {
                                    "userEnteredFormat": {
                                        "backgroundColor": {
                                            "red": 1.0,
                                            "green": 1.0,
                                            "blue": 1.0,
                                        }
                                    }
                                }
                                for _ in range(9)
                            ]
                        }
                        for _ in range(199)
                    ],
                    "fields": "userEnteredFormat(backgroundColor)",
                }
            }
        ]
    }

    # Send the request to the API
    service.spreadsheets().batchUpdate(
        spreadsheetId=config.spreadsheet_id, body=clear_format_request
    ).execute()

    for row in rows:
        request = {
            "updateCells": {
                "range": {
                    "sheetId": 1476248146,
                    "startRowIndex": row,
                    "endRowIndex": row + 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 9,
                },
                "rows": [
                    {
                        "values": [
                            {
                                "userEnteredFormat": {
                                    "backgroundColor": {
                                        "red": 1.0,
                                        "green": 1.0,
                                        "blue": 0.6,
                                    },
                                    "textFormat": {
                                        "foregroundColor": {
                                            "red": 0,
                                            "green": 0,
                                            "blue": 0,
                                        }
                                    },
                                }
                            }
                            for _ in range(9)
                        ]
                    }
                ],
                "fields": "userEnteredFormat(backgroundColor, textFormat)",
            }
        }

        format_requests.append(request)

    print(format_requests)

    service.spreadsheets().batchUpdate(
        spreadsheetId=config.spreadsheet_id, body={"requests": format_requests}
    ).execute()

    return None
