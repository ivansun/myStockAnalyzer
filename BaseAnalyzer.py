from YahooFinance import Share
from pprint import pprint
import datetime
import json
from const import *

import numpy as np

class BaseAnalyzer(object):

    '''
    yahoo_finance_api page:
    https://pypi.python.org/pypi/yahoo-finance

    Online Test:
    https://developer.yahoo.com/yql/console/?q=show%20tables&env=store://datatables.org/alltableswithkeys#h=select+*+from+yahoo.finance.quotes+where+symbol+%3D+%22YHOO%22

    Share Function List:
    get_price()
    get_change()
    get_volume()
    get_prev_close()
    get_open()
    get_avg_daily_volume()
    get_stock_exchange()
    get_market_cap()
    get_book_value()
    get_ebitda()
    get_dividend_share()
    get_dividend_yield()
    get_earnings_share()
    get_days_high()
    get_days_low()
    get_year_high()
    get_year_low()
    get_50day_moving_avg()
    get_200day_moving_avg()
    get_price_earnings_ratio()
    get_price_earnings_growth_ratio()
    get_price_sales()
    get_price_book()
    get_short_ratio()
    get_trade_datetime()
    get_historical(start_date, end_date)
    get_info()
    refresh()
    '''

    def __init__(self, share):
        self.share = share

    '''
    start_date: start date
    '''
    def _get_safe_start_date(self, start_date):
        '''
        stock_start_date = self.share.get_info()["start"]
        try:
            stock_start_date_datefmt = datetime.datetime.strptime(stock_start_date, "%Y-%m-%d").date()
        except Exception:
            return start_date

        start_date_datefmt = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        #print(stock_start_date_datefmt)
        
        if stock_start_date_datefmt > start_date_datefmt:
            return stock_start_date
        else:
            return start_date
        '''
        return start_date

    '''
    end_date: end date
    '''
    def _get_safe_end_date(self, end_date):
        return end_date

    '''
    data_range_type: daily, weekly, monthly, etc
    '''
    def _get_historical_date_by_data_range_type(self, start_date, end_date, data_range_type):
        historical_data = self.share.get_historical(start_date, end_date)
        if data_range_type == DAILY_DATA:
            return historical_data
        elif data_range_type == WEEKLY_DATA:
            return None
        elif data_range_type == MONTHLY_DATA:
            return None

    
            

if __name__ == "__main__":
    share = Share("AAPL")
    base_analyzer = BaseAnalyzer(share)
    #base_analyzer.get_top_bottom_points(10, '2014-10-01', '2015-01-01', DAILY_DATA)
    '''
    start_date=datetime.datetime.strptime('2015-01-05', "%Y-%m-%d").date()
    end_date=datetime.datetime.strptime('2015-01-09', "%Y-%m-%d").date()

    if start_date < end_date:
        print('test')

    print(start_date-end_date)

    print(start_date.strftime('%Y%m%d'))    
    '''
