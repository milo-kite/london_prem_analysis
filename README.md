# London Prem Analysis

This repository can be used by hockey players playing in the Men's or Women's English Hockey League to track your league's hockey statistics in greater detail. 

## Views

This produces two tables.

### Team View

This table produces summary statistics at the team level. It can be used to scout how disciplined a team is, as well as if they have a corner threat. Here is the schema:

| Field | Description | Type |
|-------|-------------|------|
| Team | Team Name | String |
| Field Goal | Total open play goals | Integer |
| Green Card | Total green cards | Integer |
| Penalty Corner | Total penalty corner goals | Integer |
| Yellow Card | Total yellow cards | Integer |
| Goals | Total goals | Integer |

### Player View

This table produces summary statistics at the player level. It can be used to scout top goal scorers, as well as card liabilities. Here is the schema:

| Field | Description | Type |
|-------|-------------|------|
| Player | Player Name | String |
| Team | Team Name | String |
| Field Goal | Total open play goals | Integer |
| Green Card | Total green cards | Integer |
| Yellow Corner | Total yellow cards | Integer |
| Goals | Total goals | Integer |

## Set-up

This setup works for UNIX like operating systems. This setup assumes you have:

- pip
- python
- gmail account
- login for whostheumpire.com

### GSheet API

To write to a GSheet you need to run an app that calls a Google Workspace API. To set this up we'll be following this [setup guide](https://developers.google.com/sheets/api/quickstart/python)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/welcome)
2. Create a new project by:
    - Clicking `Select a project`
    - Clicking `NEW PROJECT`
    - Calling your project `Hockey`
3. Enable the `Hockey` project [here](https://console.cloud.google.com/flows/enableapi?apiid=sheets.googleapis.com)
    - Click `NEXT`
    - Click `ENABLE`
4. Configure the OAuth consent by:
    - Going to the [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent)
    - Select `External`
    - Select `Create`
    - Complete the registration form
    - Skip adding scopes
    - Review the app registration summary
5. Authorise your credentials
    - Going to the [Credentials](https://console.cloud.google.com/apis/credentials) page
    - `+ Create Credentials`
    - Click OAuth client ID
    - Choose a `Desktop App` and name in Monzo
    - A pop-up saying OAuth client create will appear. 
6. Download JSON to save your credentials, we'll keep these handy for later.
7. Rename the credentials to `gsheet_oauth_budget.json` and move them into this repository under the `credentials/` file in this repository.

### GSheet

1. Go to [GSheets](https://docs.google.com/spreadsheets/u/0/) in your browser
2. Make two tabs called `Team View` and `Player View`
3. Note the `spreadsheet_id` in the URL (it's the characters after `/d/` and before `/edit/`)

### Find your Competition Index Key

This is the identifier for your league in "whostheumpire". It's a bit fiddly. I recommend using Chrome as your browser for this.

1. Login on [whostheumpire](https://secure.whostheumpire.com/db_admin/index.php?login=Y)
2. Go to [Fixtures Search](https://secure.whostheumpire.com/db_admin/fixtures.php?function=view)
3. Change the Competition dropdown to your league
4. Right-hand click and open up Inspect
5. Go to the Network tab
6. Search for the fixtures in your browser by hitting Find
7. Click on the event entitled fixtures.php?function=view
8. Go to Payload
9. Note the value under Form Data next to `find_competition_index_key`. It should be a random string of numbers and letters from A->F.

### Credentials

Go to `config.py` and update:
- email for whostheumpire
- password for whostheumpire
- `competition_index_key`
- `spreadsheet_id`

### Virtual Environment

1. Install your virtual environment using `brew install pyenv-virtualenv` for macOS
2. Add virtual environment to your shell by adding these lines to your shell:
    - `export PATH="$HOME/.pyenv/bin:$PATH"`
    - `eval "$(pyenv init --path)"`
    - `eval "$(pyenv init -)"`
    - `eval "$(pyenv virtualenv-init -)" `
    followed by `source ~/.zshrc`
3. Create your pyenv using `make pyenv`
4. Activate your virtual environment using `pyenv activate ${VENV_NAME}`

### Requirements

Run `make requirements` to install your requirements.
Install your pre-commit hook using `pre-commit install`

### Airflow

1. Run `airflow db init` to initialise your airflow metadatabase.
2. Run `airflow webserver --daemon` to start the webserver.
3. Run `airflow scheduler --daemon` to start the scheduler.
4. Run `make deploy_dag` to deploy your DAG to airflow
5. Run `make airflow_ui` to open the Airflow UI in your browser.
