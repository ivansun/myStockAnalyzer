from YahooFinance import Share
from const import *
from ConvertHelper import ConvertHelper
from StockDrawer import *

from pprint import pprint
import time
import datetime
import json

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import matplotlib
import pylab


class OrdRecord(object):
    def __init__(self):
        pass

    def set_start_date(self, start_date):
        self.start_date = start_date

    def get_start_date(self):
        return self.start_date

    def set_ord_volume(self, ord_volume):
        self.ord_volume = ord_volume

    def get_ord_volume(self):
        return self.ord_volume

    def set_trend(self, trend):
        self.trend = trend

    def get_trend(self):
        return self.trend

    def set_price(self, low_or_high_price):
        self.price = low_or_high_price

    def get_price(self):
        return self.price

    def __str__(self):
        return self.start_date+": "+str(self.ord_volume)+": "+str(self.trend)+": "+str(self.price)

class Analyzer(object):

    def __init__(self, share, drawer):
        self.share = share
        self.drawer = drawer

    def set_drawer(self, drawer):
        self.drawer = drawer

    def get_drawer(self):
        return self.drawer

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

    
    '''
    zoom: days to decide high-end point. The date that is higher/lower than +-'zoom' days will be the high/low point
    cur_date: current date
    historical_data: historical data
    '''
    def _is_top(self, zoom, cur_date, historical_data):
        historical_data_length = len(historical_data)
        for index in range(historical_data_length):
            cur_date_in_history = historical_data[index]['Date']
            #print(cur_date_in_history)
            if cur_date_in_history == cur_date:
                #print(index)
                
                for inner_index in range(1, zoom+1):
                    #print(inner_index)
                    # Check previous
                    if index-inner_index >= 0 and float(historical_data[index-inner_index]['High'])>float(historical_data[index]['High']):
                        return False

                    # Check following
                    if index+inner_index < historical_data_length and float(historical_data[index+inner_index]['High'])>float(historical_data[index]['High']):
                        return False
                return True
            
        return False


    '''
    zoom: days to decide high-end point. The date that is higher/lower than +-'zoom' days will be the high/low point
    cur_date: current date
    historical_data: historical data
    '''
    def _is_bottom(self, zoom, cur_date, historical_data):
        historical_data_length = len(historical_data)
        for index in range(historical_data_length):
            cur_date_in_history = historical_data[index]['Date']
            #print(cur_date_in_history)
            if cur_date_in_history == cur_date:
                #print(index)
                
                for inner_index in range(1, zoom+1):
                    #print(inner_index)
                    # Check previous
                    if index-inner_index >= 0 and float(historical_data[index-inner_index]['Low'])<float(historical_data[index]['Low']):
                        return False

                    # Check following
                    if index+inner_index < historical_data_length and float(historical_data[index+inner_index]['Low'])<float(historical_data[index]['Low']):
                        return False
                return True
            
        return False
    
    '''
    historical_data: historical data
    top_bottom_points: the top boottom points from the historical data
    '''
    def _update_ord_volume(self, historical_data, top_bottom_points):
        for index in range(len(top_bottom_points)):
            cur_point = top_bottom_points[len(top_bottom_points)-index-1]
            next_point = None
            if index != len(top_bottom_points)-1:
                next_point = top_bottom_points[len(top_bottom_points)-index-2]
                
            total_volumn = 0
            total_days = 0
            for cur_data in reversed(historical_data):
                cur_data_fmtdate = datetime.datetime.strptime(cur_data['Date'], "%Y-%m-%d").date()
                cur_point_fmtdate = datetime.datetime.strptime(cur_point.get_start_date(), "%Y-%m-%d").date()
                next_point_fmtdate = None
                if next_point is not None:
                    next_point_fmtdate = datetime.datetime.strptime(next_point.get_start_date(), "%Y-%m-%d").date()
                    
                if cur_data_fmtdate >= cur_point_fmtdate and next_point_fmtdate is not None and cur_data_fmtdate < next_point_fmtdate:
                    total_volumn = total_volumn + int(cur_data['Volume'])
                    total_days = total_days + 1
                elif cur_data_fmtdate >= cur_point_fmtdate and next_point is None:
                    total_volumn = total_volumn + int(cur_data['Volume'])
                    total_days = total_days + 1
                elif next_point_fmtdate is not None and cur_data_fmtdate >= next_point_fmtdate:
                    break
                

            #print(str(total_volumn) + ": " + str(total_days))
            cur_point.set_ord_volume(total_volumn/total_days)    
            #print(cur_point)
        return 
    
    '''
    zoom: days to decide high-end point. The date that is higher/lower than +-'zoom' days will be the high/low point
    historical_data: historical data
    '''
    def get_top_bottom_points(self, zoom, historical_data):
        # Define result list
        result_list = []
        
        for index in range(len(historical_data)):
            cur_date = historical_data[index]['Date']

            is_top = self._is_top(zoom, cur_date, historical_data)
            is_bottom = self._is_bottom(zoom, cur_date, historical_data)

            if is_top == True:
                ord_record = OrdRecord()
                ord_record.set_start_date(cur_date)
                ord_record.set_ord_volume(0)
                ord_record.set_trend(TREND_DOWN)
                ord_record.set_price(historical_data[index]['High'])
                #print(ord_record)
                if len(result_list) == 0:
                    result_list.append(ord_record)
                else:
                    last_result = result_list.pop()
                    if last_result.get_trend() != TREND_DOWN:
                        result_list.append(last_result)
                        result_list.append(ord_record)
                    else:
                        if last_result.get_price() >= ord_record.get_price():
                            result_list.append(last_result)
                        else:
                            result_list.append(ord_record)
                
            elif is_bottom == True:
                ord_record = OrdRecord()
                ord_record.set_start_date(cur_date)
                ord_record.set_ord_volume(0)
                ord_record.set_trend(TREND_UP)
                ord_record.set_price(historical_data[index]['Low'])
                #print(ord_record)
                if len(result_list) == 0:
                    result_list.append(ord_record)
                else:
                    last_result = result_list.pop()
                    if last_result.get_trend() != TREND_UP:
                        result_list.append(last_result)
                        result_list.append(ord_record)
                    else:
                        if last_result.get_price() <= ord_record.get_price():
                            result_list.append(last_result)
                        else:
                            result_list.append(ord_record)

        self._update_ord_volume(historical_data, result_list)
        
        return result_list

if __name__ == "__main__":
    stock = raw_input('Stock to plot: ')
    share = Share(stock)
    ord_drawer = OrdDrawer()
    ord_analyzer = Analyzer(share, ord_drawer)

    start_date = '2014-07-01'
    end_date = datetime.date.today().strftime('%d-%b-%Y')
    data_range_type = DAILY_DATA
    historical_data = ord_analyzer._get_historical_date_by_data_range_type(start_date, end_date, data_range_type)
    #print historical_data
    top_bottom_points = ord_analyzer.get_top_bottom_points(10, historical_data)
    for i in range(0, len(top_bottom_points)):
        print(top_bottom_points[i])

    convertHelper = ConvertHelper()
    np_historical_data = convertHelper.historical_data_to_nparray(historical_data)
    #print np_historical_data
    np_top_bottom_points = convertHelper.top_bottom_points_to_nparray(top_bottom_points)
    #print np_top_bottom_points


    
    ord_analyzer.get_drawer().draw_historical_data(np_historical_data)
    ord_analyzer.get_drawer().draw_rsi(np_historical_data)
    ord_analyzer.get_drawer().draw_ord_volume_data(np_top_bottom_points)
    
    ord_analyzer.get_drawer().show()
    
    '''
    date, open_price, close_price, high_price, low_price, volume = np.loadtxt('test.rtf', delimiter=' ', unpack=True,
                                                                              converters={0: mdates.strpdate2num("%Y-%m-%d")})
    print type(open_price)
    print open_price
    '''
    
