import os
import sys
import logging
from datetime import date, timedelta

import gspread_authorize
import yandex_data
import yandex_data_regions


def get_yesterday_date():
    """ Get yesterday dates. """

    delta = timedelta(days=1)
    return (date.today() - delta).strftime('%d/%m/%Y')


def write_to_spreadsheet(period, regions=None):
    """period: str 'TODAY' or 'YESTERDAY' """

    logging.basicConfig(
        filename=f'{period}.log',
        level=logging.INFO,
        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S'
    )

    gc = gspread_authorize.authorize()

    if regions:
        sheet = f'Regions {period}'
        worksheet = gspread_authorize.open_sheet(
            gc, os.getenv('SPREADSHEET_INCOME'), sheet
        )

        print(worksheet)

        if period == 'hourly':
            ya_spend = yandex_data_regions.get_expenses('TODAY')
            date_column = worksheet.cell(2, 1).value.split()
            today = date.today().strftime('%d.%m')
            if today in date_column:
                cell_shift = 7
                for i in ya_spend:
                    worksheet.update_cell(2, cell_shift, ya_spend[i])
                    cell_shift += 3

        if period == 'daily':
            ya_spend = yandex_data_regions.get_expenses('YESTERDAY')
            yesterday = get_yesterday_date()
            date_cell = worksheet.find('{}'.format(yesterday))
            if date_cell:
                cell_shift = 7
                for i in ya_spend:
                    worksheet.update_cell(date_cell.row, cell_shift, ya_spend[i])
                    cell_shift += 3

    else:
        worksheet = gspread_authorize.open_sheet(
            gc, os.getenv('SPREADSHEET_INCOME'), period
        )

        print(worksheet)

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
    try:
        regions = sys.argv[2]
    except IndexError:
        regions = None
    write_to_spreadsheet(period, regions)
