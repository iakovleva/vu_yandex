import os
import sys
import logging
from datetime import date, timedelta

import gspread_authorize
import yandex_data


def get_yesterday_date():
    """ Get yesterday dates. """

    delta = timedelta(days=1)
    return (date.today() - delta).strftime('%d/%m/%Y')


def write_to_spreadsheet(period):
    """period: str 'TODAY' or 'YESTERDAY' """

    logging.basicConfig(
        filename=f'{period}.log',
        level=logging.INFO,
        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S'
        )

    gc = gspread_authorize.authorize()
    worksheet = gspread_authorize.open_sheet(
        gc, os.getenv('SPREADSHEET_INCOME'), period
    )

    if period == 'hourly':
        ya_spend = yandex_data.get_expenses('TODAY')
        date_column = worksheet.cell(2, 1).value.split()
        today = date.today().strftime('%d.%m')
        if today in date_column:
            worksheet.update_cell(2, 5, ya_spend)

    if period == 'daily':
        ya_spend = yandex_data.get_expenses('YESTERDAY')
        yesterday = get_yesterday_date()
        date_cell = worksheet.find('{}'.format(yesterday))
        if date_cell:
            worksheet.update_cell(date_cell.row, 10, ya_spend)


if __name__ == '__main__':
    period = sys.argv[1]
    write_to_spreadsheet(period)
