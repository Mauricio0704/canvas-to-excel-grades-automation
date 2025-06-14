import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

scopes = ["https://www.googleapis.com/auth/spreadsheets"]

def get_sheets_client():
    credentials = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(credentials)
    return client


def get_worksheet(sheet_id, worksheet_name):
    client = get_sheets_client()
    sheet = client.open_by_key(sheet_id)
    return sheet.worksheet(worksheet_name)

def get_service():
    credentials = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    service = build("sheets", "v4", credentials=credentials)
    return service