from yahoofinancials import YahooFinancials
import pandas as pd

# Select Tickers and stock history dates
ticker = 'SISE.IS'
ticker2 = 'MSFT'
ticker3 = 'INTC'
index = '^NDX'
freq = 'monthly'
start_date = '2008-01-01'
end_date = '2019-12-31'


# Function to construct data frame based on a stock and it's market index
def build_data_frame(data_list1, data_list2, data_list3, data_list4):
    data_dict = {}
    i = 0
    for list_item in data_list2:
        if 'type' not in list_item.keys():
            data_dict.update({list_item['formatted_date']: {'NDX': data_list1[i]['close'], 'AAPL': list_item['close'],
                                                            'MSFT': data_list3[i]['close'],
                                                            'INTL': data_list4[i]['close']}})
            i += 1
    tseries = pd.to_datetime(list(data_dict.keys()))
    df = pd.DataFrame(data=list(data_dict.values()), index=tseries,
                      columns=['NDX', 'AAPL', 'MSFT', 'INTL']).sort_index()
    return df

# Function to clean data extracts
def clean_stock_data(stock_data_list):
    new_list = []
    for rec in stock_data_list:
        if 'type' not in rec.keys():
            new_list.append(rec)
    return new_list

# Construct yahoo financials objects for data extraction
aapl_financials = YahooFinancials(ticker)
mfst_financials = YahooFinancials(ticker2)
intl_financials = YahooFinancials(ticker3)
index_financials = YahooFinancials(index)

# Clean returned stock history data and remove dividend events from price history
daily_aapl_data = clean_stock_data(aapl_financials.get_historical_price_data(start_date, end_date, freq)[ticker]['prices'])

daily_msft_data = clean_stock_data(mfst_financials
                                   .get_historical_price_data(start_date, end_date, freq)[ticker2]['prices'])
daily_intl_data = clean_stock_data(intl_financials
                                   .get_historical_price_data(start_date, end_date, freq)[ticker3]['prices'])
daily_index_data = index_financials.get_historical_price_data(start_date, end_date, freq)[index]['prices']
stock_hist_data_list = [{'NDX': daily_index_data}, {'AAPL': daily_aapl_data}, {'MSFT': daily_msft_data},
                        {'INTL': daily_intl_data}]


a = build_data_frame(daily_aapl_data, daily_intl_data, daily_msft_data, daily_index_data)

print(a);