import requests
import json
import csv


def getHisseler():
    url = "http://bigpara.hurriyet.com.tr/api/v1/hisse/list"

    headers = {
        'cache-control': "no-cache",
        'postman-token': "fb97e4a7-abc8-7a00-a116-2ecc1ae88d07"
    }

    response = requests.request("GET", url, headers=headers)

    hisse = json.loads(response.text)
    return hisse['data']


def getMaliTablo(hisse, year1, period1, year2, period2, year3, period3, year4, period4, exchange='TRY', financialGroup='XI_29'):
    url = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
    querystring = {"companyCode": hisse, "exchange": exchange, "financialGroup": financialGroup, "year1": year1, "period1": period1, "year2": year2, "period2": period2, "year3": year3,
                   "period3": period3, "year4": year4, "period4": period4}

    headers = {
        'cache-control': "no-cache",
        'postman-token': "76a327e4-d953-59ed-218a-9205de973797"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    tablo = json.loads(response.text)

    print(hisse + ' ' + str(year1))
    return tablo['value']


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

    hisseler = getHisseler()

    writeHeader = False
    fieldnames = []
    with open('example2.csv', 'w', encoding="utf8", newline='') as csvfile:
        for hisse in hisseler:
            for year in range(2018, 2019):
                yearlyFundemantalTable = getMaliTablo(hisse['kod'], year, 3, year, 6, year, 9, year, 12)
                if yearlyFundemantalTable:
                    if not fieldnames:
                        fieldnames = ['year', 'period', 'hisse']
                        for field in yearlyFundemantalTable:
                            fieldnames.append(field['itemDescTr'].strip())
                            # fieldnames.append(field['itemDescEng'].strip())
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
                        writer.writeheader()
                    writePeriodFundemental(3)
                    writePeriodFundemental(6)
                    writePeriodFundemental(9)
                    writePeriodFundemental(12)
