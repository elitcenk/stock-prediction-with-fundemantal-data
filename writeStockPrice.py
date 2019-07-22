import requests
import json
import csv
from yahoofinancials import YahooFinancials
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


def getHisseler():
    url = "http://bigpara.hurriyet.com.tr/api/v1/hisse/list"

    headers = {
        'cache-control': "no-cache",
        'postman-token': "fb97e4a7-abc8-7a00-a116-2ecc1ae88d07"
    }

    response = requests.request("GET", url, headers=headers)

    hisse = json.loads(response.text)
    return hisse['data']

# Function to clean data extracts
def clean_stock_data(stock_data_list):
    new_list = []
    for rec in stock_data_list:
        if 'type' not in rec.keys():
            new_list.append(rec)
    return new_list


def writePeriodFundemental(period):
    isWriteRow = True
    monthlyFundemantalTable = {'year': year, 'hisse': hisse['kod'], 'period': period}
    if (yearlyFundemantalTable[0]['value' + str(int(period / 3))] == None) or yearlyFundemantalTable[0]['value' + str(int(period / 3))] == '0':
        return
    for field in yearlyFundemantalTable:
        # if not field['value' + str(int(period / 3))]:
        #     isWriteRow = False
        #     break
        monthlyFundemantalTable[field['itemDescTr'].strip()] = field['value' + str(int(period / 3))]
    if isWriteRow:
        writer.writerow(monthlyFundemantalTable)

if __name__ == '__main__':

    freq = 'monthly'
    start_date = '2008-01-01'
    end_date = '2019-01-31'
    hisseler = getHisseler()

    with open('example2.csv', 'w', encoding="utf8", newline='') as csvfile:
        fieldnames = ['high', 'adjclose', 'close','date','volume','open','low', 'ticker']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for hisse in hisseler:
            financials = YahooFinancials(hisse['kod']+ '.IS')
            monthly_data = clean_stock_data(financials.get_historical_price_data(start_date, end_date, freq)[hisse['kod']+ '.IS']['prices'])
            row = {}
            row['ticker'] = monthly_data
            writePeriodFundemental(3)
            writePeriodFundemental(6)
            writePeriodFundemental(9)
            writePeriodFundemental(12)