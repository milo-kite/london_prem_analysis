# London Prem Analysis

This repository can be used by hockey players playing in the Men's or Women's English Hockey League to track your league's hockey statistics in greater detail. 

## Privacy Policy

**london_prem_analysis** ("the App") is committed to protecting your privacy. This Privacy Policy explains how we handle data collected and processed through the App. By using the App, you agree to the terms outlined below.

---

### 1. Information We Collect

The App does not collect or process any personal information from users. The following information is used by the App as part of its core functionality:

- **Hockey Data**: Publicly available data scraped from third-party websites.
- **Google Sheets Integration**: Scraped data is written to a private Google Sheet controlled by the App's administrator. Users have read-only access to this data.

---

### 2. Use of Data

- The hockey data retrieved by the App is stored in a private Google Sheet controlled by the App's administrator.
- Users are granted read-only access to view this data.
- This data is not shared, sold, or disclosed to any third parties.
- No personal user information is collected, stored, or processed by the App.

---

### 3. Google API Usage

The App uses the Google Sheets API to:

- Write scraped hockey data to a private Google Sheet.
- Provide users with read-only access to the Google Sheet.

### OAuth and API Key Usage

- The App uses an API key to authenticate requests to the Google Sheets API.
- OAuth is used to securely connect the App to the private Google Sheet controlled by the App's administrator.

---

### 4. Data Security

- Data scraped and processed by the App is stored securely in the private Google Sheet.
- Users have read-only access and cannot modify the data.
- All communication with the Google Sheets API is encrypted using HTTPS.

---

### 5. User Permissions

- Users are provided read-only access to the private Google Sheet.
- The App's administrator retains full control over the data and permissions.

---

## 6. Third-Party Websites

The App scrapes publicly available data from third-party websites. These websites may have their own privacy policies and terms of service, which are not governed by this Privacy Policy.

---

### 7. Updates to this Privacy Policy

We may update this Privacy Policy from time to time. Any changes will be posted on this page with an updated "Effective Date."

---

### 8. Contact Us

If you have any questions or concerns about this Privacy Policy, please contact us at:

- **Email**: milokite@gmail.com

---

#### Important Notes

- **No Personal Data**: This app does not collect or process personal data.
- **Controlled Access**: Users are provided read-only access to the data, which is controlled by the App's administrator.

## Terms of Service


Welcome to **london_prem_analysis** ("the App"). By accessing and using the App, you agree to be bound by these Terms of Service ("Terms"). Please read them carefully. If you do not agree to these Terms, you may not use the App.

---

### 1. Description of the App

The App retrieves publicly available hockey data from third-party websites and stores it in a private Google Sheet. Users are granted read-only access to this data, which is managed and controlled by the App's administrator.

---

### 2. User Access and Restrictions

By using the App, you agree to the following:

- **Read-Only Access**: Users may view the data in the private Google Sheet but are not permitted to modify, download, or redistribute it.
- **No Ownership**: Users acknowledge that all data provided through the App is controlled by the App's administrator and that access may be revoked at any time without prior notice.
- **Prohibited Activities**:
  - Attempting to modify, hack, or gain unauthorized access to the private Google Sheet or the App.
  - Using the App or its data for illegal purposes or activities that violate third-party rights.

---

### 3. Data Usage

- The data provided in the private Google Sheet is for informational purposes only and is based on publicly available sources.
- The App does not guarantee the accuracy, completeness, or timeliness of the data.

---

### 4. Intellectual Property

- All content and materials provided by the App, including the scraped data, are the property of the App's administrator unless otherwise stated.
- Users may not reproduce, distribute, or use the data for commercial purposes without prior written consent from the App's administrator.

---

### 5. Third-Party Websites

The App retrieves data from publicly available third-party websites. These websites may have their own terms of service and privacy policies, which are not governed by these Terms. The App assumes no responsibility for the content or practices of these third-party websites.

---

### 6. Limitation of Liability

The App and its administrator are not liable for:

- Any errors, inaccuracies, or omissions in the data provided.
- Any actions taken based on the data retrieved and displayed by the App.
- Any direct, indirect, incidental, or consequential damages resulting from the use of the App.

---

### 7. Termination of Access

The App's administrator reserves the right to revoke user access to the private Google Sheet or terminate the App at any time for any reason, without prior notice.

---


### 8. Governing Law

These Terms are governed by the laws of the United Kingdom. Any disputes arising out of or related to these Terms will be subject to the exclusive jurisdiction of the courts in United Kingdom.

---

### 9. Contact Information

If you have any questions or concerns about these Terms, please contact us at:

- **Email**: milokite@gmail.com

---

#### Important Notes

- **No Warranties**: The App is provided "as is," without any warranties or guarantees of any kind.
- **Administrator Control**: The App's administrator retains full control over the data and access permissions.



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
