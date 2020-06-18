# VU_Income

Regularly collects data from Yandex Direct. Stores this data in Google Spreadsheet. 

### Prerequisites

Script uses:
- Yandex Direct API
- Gspread for authorization in Google SpreadSheets

## Getting Started

1. Create Google SpreadSheet
2. In SpreadSheet:
   - Create 2 tabs called 'hourly', 'daily'.
   - Add headers in the first row: 'Date/Time', '', '', 'Google', 'Yandex'
   - In the first column of 'daily' tab write yesterday's date, i.e. '08.01.18'
   - In the first column of 'hourly' tab write today's date and time, i.e. '09.01 12:00'

3. Create project

```
git clone https://github.com/iakovleva/vu_yandex
cd vu_yandex
```

4. Get Google API credentials for Gspread authorize. 
Follow https://gspread.readthedocs.io/en/latest/oauth2.html
Save JSON file with credentials in the current directory. 

5. Add env variables to .env file
 
CRED_FILE - JSON file with Google API credentials 
TOKEN - Yandex OAuth-токен пользователя
SPREADSHEET_INCOME - Google Spreadsheet URL

6. Build image and run container

```
docker build . -t vu_income:yandex
docker run --env-file .env vu_income:yandex hourly 
docker run --env-file .env vu_income:yandex daily 
```

7. Optionally add cron job 

```
* * * * * /usr/bin/docker run --env-file .env vu_income:yandex hourly > ~/vu_yandex/hourly.log
```
