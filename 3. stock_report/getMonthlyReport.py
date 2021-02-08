import csv
import datetime
import fractions

import loguru
import munch
import requests
import pyquery


def extractStockDailyReport(resp_type, response):
    if resp_type == 'json':
        body = response.json()
        return [
            bday
            for bday in body['data']
        ]
    if resp_type == 'csv':
        body = response.text
        return [
            line
            for line in body.split('\r\n')
            if line
        ][1:-4]
    if resp_type == 'html':
        dom = pyquery.PyQuery(response.text)
        rows = dom('table > tbody > tr')
        return rows.items()
    return None


def convertStockDailyReport(resp_type, items):
    bdays = None
    if resp_type == 'json':
        bdays = [
            {
                'date': [
                    int(part)
                    for part in item[0].split('/')
                ],
                'close':item[6]
            }
            for item in items
        ]

    if resp_type == 'csv':
        reader = csv.DictReader(items)
        rows = list(reader)
        bdays = [
            {
                'date': [
                    int(part)
                    for part in row['日期'].split('/')
                ],
                'close':row['收盤價']
            }
            for row in rows
        ]

    if resp_type == 'html':
        bdays = [
            {
                'date': [
                    int(part)
                    for part in list(row('td').items())[0].text().split('/')
                ],
                'close': list(row('td').items())[6].text()
            }
            for row in items
        ]

    if bdays is None:
        return[]
    for bday in bdays:
        bday['date'] = datetime.datetime(
            bday['date'][0] + 1911, bday['date'][1], bday['date'][2])
        bday['close'] = fractions.Fraction(bday['close'])
    return bdays


def getStockMonthlyReport(resp_type, year, month, stock_no):
    response = requests.get(
        f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response={resp_type}&date={year}{month:02}01&stockNo={stock_no}')
    bdays = extractStockDailyReport(resp_type, response)
    if bdays is None:
        print('no data')
        return
    bdays = convertStockDailyReport(resp_type, bdays)
    bdays = munch.munchify(bdays)
    for bday in bdays:
        print(f'{bday.date.strftime("%Y-%m-%d")} {float(bday.close)} ')


if __name__ == "__main__":
    loguru.logger.info('json')
    getStockMonthlyReport('json', 2020, 10, '2330')
    loguru.logger.info('csv')
    getStockMonthlyReport('csv', 2020, 10, '2330')
    loguru.logger.info('html')
    getStockMonthlyReport('html', 2020, 10, '2330')
