import logging
from datetime import date, timedelta
import tokens
import gspread_authorize
import yandex_data
from gspread.exceptions import CellNotFound


def main():
    """
    Run scripts that gets income and expenses
    in order to write this information to spreadsheet.
    """

    write_to_spreadsheet(yandex_data.get_expenses('YESTERDAY'))


def get_yesterday_date():
    """ Get today's and yesterdays dates. """

    today = date.today()
    delta = timedelta(days=1)
    yesterday = (today - delta).strftime('%d/%m/%Y')
    return yesterday


def write_to_spreadsheet(*args):
    """Write data to spreadsheet."""

    logging.basicConfig(
        filename='daily.log',
        level=logging.INFO,
        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S'
        )

    ya_spend = args[0]

    # Get date
    yesterday = get_yesterday_date()

    # Gspread authorize
    gc = gspread_authorize.authorize()

    # Open worksheet
    worksheet = gspread_authorize.open_sheet(
        gc,
        tokens.SPREADSHEET_INCOME,
        'daily')
    try:
        date_cell = worksheet.find('{}'.format(yesterday))
        worksheet.update_cell(date_cell.row, 10, ya_spend)
        logging.info('Yandex data %s for %s written',
                     ya_spend,
                     get_yesterday_date())

    except CellNotFound:
        logging.warning('There is no yesterday date in the sheet.')


if __name__ == '__main__':
    main()
