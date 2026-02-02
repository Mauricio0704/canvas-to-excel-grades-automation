import os
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

scopes = ["https://www.googleapis.com/auth/spreadsheets"]


def _get_creds_path():
    env_path = os.getenv("CREDS_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return Path(__file__).parent / "creds.json"


def get_sheets_client():
    credentials = Credentials.from_service_account_file(
        str(_get_creds_path()), scopes=scopes
    )
    client = gspread.authorize(credentials)
    return client


def get_worksheet(sheet_id, worksheet_name):
    client = get_sheets_client()
    sheet = client.open_by_key(sheet_id)
    return sheet.worksheet(worksheet_name)


def get_service():
    credentials = Credentials.from_service_account_file(
        str(_get_creds_path()), scopes=scopes
    )
    service = build("sheets", "v4", credentials=credentials)
    return service
