import logging
from datetime import date, datetime
import tokens
import yandex_data
import gspread_authorize


def write_to_spreadsheet(*args):
    """Write data to spreadsheet."""

    logging.basicConfig(
        filename='hourly.log',
        level=logging.INFO,
        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S'
        )

    ya_spend = args[0]

    # Get date
    today = date.today().strftime('%d.%m')
    gc = gspread_authorize.authorize()

    # Open worksheet
    worksheet = gspread_authorize.open_sheet(
        gc,
        tokens.SPREADSHEET_INCOME,
        'hourly')
    date_column = worksheet.cell(2, 1).value.split()

    # Check if date in the first row is today
    if today in date_column:
        worksheet.update_cell(2, 5, ya_spend)
        logging.info('Yandex data for %s written', datetime.now())
    else:
        logging.warning('There is no today date in the sheet.')


if __name__ == '__main__':
    write_to_spreadsheet(yandex_data.get_expenses('TODAY'))
