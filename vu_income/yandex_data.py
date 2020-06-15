import json
from time import sleep
import requests
import tokens


def get_expenses(period):
    """ Gets expenses per period from website's API.

    Parameters:
    period(str): 'TODAY' or 'YESTERDAY'.

    Returns:
    total_sum(int): sum of expenses from all campaigns or prints error if fails.
    """

    # --- Входные данные ---
    reports_url = 'https://api.direct.yandex.com/json/v5/reports'
    #ReportsURL = 'https://api-sandbox.direct.yandex.com/json/v5/reports'

    # Создание HTTP-заголовков запроса
    headers = {
        "Authorization": "Bearer " + tokens.TOKEN,
        "Accept-Language": "ru",
        "processingMode": "auto",
        # Формат денежных значений в отчете
        "returnMoneyInMicros": "false",
        # Не выводить в отчете строку с названием отчета и диапазоном дат
        "skipReportHeader": "true",
        # Не выводить в отчете строку с названиями полей
        "skipColumnHeader": "true",
        # Не выводить в отчете строку с количеством строк статистики
        "skipReportSummary": "true"
        }

    # Создание тела запроса
    body = {
        "params": {
            "SelectionCriteria": {
            },
            "FieldNames": [
                "Cost"
            ],
            "ReportName": "TODAY's Income",
            "ReportType": "CAMPAIGN_PERFORMANCE_REPORT",
            "DateRangeType": period,
            "Format": "TSV",
            "IncludeVAT": "YES",
            "IncludeDiscount": "NO"
        }
    }

    # Кодирование тела запроса в JSON
    body = json.dumps(body, indent=4)

    # --- Запуск цикла для выполнения запросов ---
    # Если получен HTTP-код 200, то выводится содержание отчета
    # Если получен HTTP-код 201 или 202, выполняются повторные запросы
    while True:
        try:
            req = requests.post(reports_url, body, headers=headers)
            req.encoding = 'utf-8'  # Принудительная обработка ответа в кодировке UTF-8
            if req.status_code == 400:
                print("Параметры запроса указаны неверно или достигнут лимит отчетов в очереди")
                print("JSON-код ответа сервера: \n{}".format(req.json()))
                break
            elif req.status_code == 200:
                total_sum = 0
                for i in req.text.split():
                    total_sum += float(i)
                return total_sum
                break
            elif req.status_code == 201:
                print("Отчет успешно поставлен в очередь в режиме офлайн")
                retryIn = int(req.headers.get("retryIn", 60))
                sleep(retryIn)
            elif req.status_code == 202:
                print("Отчет формируется в режиме офлайн")
                retryIn = int(req.headers.get("retryIn", 60))
                sleep(retryIn)
            elif req.status_code == 500:
                print("При формировании отчета произошла ошибка. Пожалуйста, попробуйте повторить запрос позднее")
                print("JSON-код ответа сервера: \n{}".format(req.json()))
                break
            elif req.status_code == 502:
                print("Время формирования отчета превысило серверное ограничение.")
                print("Пожалуйста, попробуйте изменить параметры запроса - уменьшить период и количество запрашиваемых данных.")
                print("JSON-код ответа сервера: \n{}".format(req.json()))
                break
            else:
                print("Произошла непредвиденная ошибка")
                print("JSON-код ответа сервера: \n{}".format(req.json()))
                break

        # Обработка ошибки, если не удалось соединиться с сервером API Директа
        except ConnectionError:
            print("Произошла ошибка соединения с сервером API")
            break

        # Если возникла какая-либо другая ошибка
        except:
            print("Произошла непредвиденная ошибка")
            break
