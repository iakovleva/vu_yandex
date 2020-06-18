import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def authorize():
    """Make authorization in a Google Spreadsheet."""

    # Gspread authorize
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    cred_file = os.getenv('CRED_FILE')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        cred_file,
        scope
        )
    return gspread.authorize(credentials)


def open_sheet(gc, url, worksheet):
    """Open Google Spreadsheet."""

    gc = authorize()
    try:
        spreadsheet = gc.open_by_url(url)
        worksheet = spreadsheet.worksheet(worksheet)
    except gspread.exceptions.GSpreadException as e:
        print(e)
    except:
        print('Spreadsheet {} was not opened'.format(worksheet))
    return worksheet
