import os
import json
from time import sleep
import requests

dict_cities={'Москва': 0, 'СПб': 0, 'Архангельск': 0, 'Астрахань': 0, 'Балашиха': 0, 'Барнаул': 0, 'Белгород': 0, 'Благовещенск': 0, 'Брянск': 0, 'Владивосток': 0, 'Владимир': 0, 'Волгоград': 0, 'Вологда': 0, 'Воронеж': 0, 'Екатеринбург': 0, 'Ижевск': 0, 'Иркутск': 0, 'Казань': 0, 'Калининград': 0, 'Калуга': 0, 'Кемерово': 0, 'Киров': 0, 'Краснодар': 0, 'Красноярск': 0, 'Курск': 0, 'Липецк': 0, 'Майкоп': 0, 'Махачкала': 0, 'Нальчик': 0, 'Набережные': 0, 'Нижний Новгород': 0, 'Новокузнецк': 0, 'Новосибирск': 0, 'Омск': 0, 'Оренбург': 0, 'Пенза': 0, 'Пермь': 0, 'Ростов-на-Дону': 0, 'Рязань': 0, 'Самара': 0, 'Саратов': 0, 'Севастополь': 0, 'Ставрополь': 0, 'Тольятти': 0, 'Томск': 0, 'Тюмень': 0, 'Ульяновск': 0, 'Уфа': 0, 'Хабаровск': 0, 'Челябинск': 0, 'Ярославль': 0, 'Partner promo': 0}

def group_by_city(report, dict_cities):
    report=report.splitlines()
    for i in report:
        # счетчик для проверки что ключ словаря найден в строке
        c=0
        for j in dict_cities:
           # Сверка каждого ключа с частью строки до тире
            if j in i.partition('-')[0]:
               # последняя часть строки добавляеться к текущему значению
                dict_cities[j]+=float(i.split('-')[-1].split()[-1])
                break
            else:
                c+=1
    #    if c==len(dict_cities):
    #        print("НЕ НАЙДЕНО:", i)
    #  округление всех значений словаря        
    for j in dict_cities:
        dict_cities[j]=round(dict_cities[j], 2)
    return dict_cities
    
    
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
        "Authorization": "Bearer " + os.getenv('TOKEN', ''),
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
                "CampaignName",
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
                return group_by_city(req.text, dict_cities)
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
