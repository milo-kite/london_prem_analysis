# London Prem Analysis

This repository can be used by hockey players playing in the Men's or Women's English Hockey League to track your league's hockey statistics in greater detail. 


## Views

This produces two tables.

### Team View

This table produces summary statistics at the team level. It can be used to scout how disciplined a team is, as well as if they have a corner threat. Here is the schema:

| Field | Description | Type |
|-------|-------------|------|
| Team | Team Name | String |
| Green Card Conceded | Total green cards conceded | Integer |
| Yellow Card Conceded | Total yellow cards conceded | Integer |
| Red Card Conceded | Total red cards conceded | Integer |
| Penalty Stroke Conceded | Total penalty stroke goals conceded | Integer |
| Penalty Corner Conceded | Total penalty corner goals conceded | Integer |
| Field Goal Conceded | Total open play goals conceded | Integer |
| Total Goals Conceded | Total goals conceded | Integer |
| Green Card Drawn | Total green cards drawn | Integer |
| Yellow Card Drawn | Total yellow cards drawn | Integer |
| Red Card Drawn | Total red cards drawn | Integer |
| Penalty Stroke Scored | Total penalty stroke goals scored | Integer |
| Penalty Corner Scored | Total penalty corner goals scored | Integer |
| Field Goal Scored | Total open play goals scored | Integer |
| Total Goals Scored | Total goals scored | Integer |

### Player View

This table produces summary statistics at the player level. It can be used to scout top goal scorers, as well as card liabilities. Here is the schema:

| Field | Description | Type |
|-------|-------------|------|
| Player | Player Name | String |
| Team | Team Name | String |
| Green Card | Total green cards | Integer |
| Yellow Card | Total yellow cards | Integer |
| Red Card | Total red cards | Integer |
| Penalty Stroke | Total penalty strokes | Integer |
| Penalty Corner | Total penalty corners | Integer |
| Field Goal | Total open play goals | Integer |
| Total Goals | Total goals | Integer |

## Set-up

This setup works for UNIX like operating systems. This setup assumes you have:

- pip
- python
- gmail account
- login for whostheumpire.com

### GSheet API

To write to a GSheet you need to run an app that calls a Google Workspace API. To set this up we'll be following this [guide](https://support.google.com/a/answer/7378726?hl=en) to create your service account. Turn on the GSheets API. Make sure to save your key locally as `service_account_key.json`.

### GSheet

1. Go to [GSheets](https://docs.google.com/spreadsheets/u/0/) in your browser
2. Make two tabs called `Team View` and `Player View`
3. Note the `sheet_id` of your second tab in the URL (it's the characters after `gid=`)
4. Note the `spreadsheet_id` in the URL (it's the characters after `/d/` and before `/edit/`)

### Find your  & Team Index Key

This is the identifier for your league in "whostheumpire". It's a bit fiddly. I recommend using Chrome as your browser for this.

1. Login on [whostheumpire](https://secure.whostheumpire.com/db_admin/index.php?login=Y)
2. Go to [Fixtures Search](https://secure.whostheumpire.com/db_admin/fixtures.php?function=view)
3. Change the Competition dropdown to your league and team dropdown to your team
4. Right-hand click and open up Inspect
5. Go to the Network tab
6. Search for the fixtures in your browser by hitting Find
7. Click on the event entitled fixtures.php?function=view
8. Go to Payload
9. Note the values under Form Data next to `find_competition_index_key` and `find_team_index_key`. They should be a random string of numbers and letters from A->F.

### Credentials

Go to `config.py` and update:
- email for whostheumpire
- password for whostheumpire
- `competition_index_key`
- `find_team_index_key`
- `spreadsheet_id`
- `sheet_id`

### Virtual Environment

1. Install your virtual environment manager using `brew install pyenv-virtualenv` for macOS
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

### Docker

1. Download [Docker](https://www.docker.com/products/docker-desktop/)
2. Open Docker Desktop
3. Verify installation by reopening your terminal and entering `docker --version`
4. Deploy using `make deploy`
5. Navigate to `http://localhost:8080/dags` and enter your username and password
6. Turn your DAG on