from googleapiclient.discovery import build
from auth import get_credentials


def get_sheets_service():
    creds = get_credentials()
    return build("sheets", "v4", credentials=creds)


def append_row(service, spreadsheet_id, range_name, row_values):
    body = {"values": [row_values]}

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
