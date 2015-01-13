from YahooFinance import Share
from pprint import pprint
import datetime
import json
from const import *

import numpy as np
import matplotlib.dates as mdates

class ConvertHelper(object):
    def historical_data_to_nparray(self, historical_data):

        tmp_result_historical_data_array = []

        historical_data_length = len(historical_data)
        for index in range(historical_data_length):
            new_historical_data = []
            cur_data = historical_data[historical_data_length-index-1]
            new_historical_data.append(mdates.date2num(datetime.datetime.strptime(str(cur_data['Date']), "%Y-%m-%d").date()))
            new_historical_data.append(float(cur_data['Open']))
            new_historical_data.append(float(cur_data['Close']))
            new_historical_data.append(float(cur_data['High']))
            new_historical_data.append(float(cur_data['Low']))
            new_historical_data.append(float(cur_data['Volume']))
            
            tmp_result_historical_data_array.append(new_historical_data)

        result_historical_data_array = np.array(tmp_result_historical_data_array)                    
        #pprint(result_historical_data_array)
        #print type(result_historical_data_array)

        return result_historical_data_array

    def top_bottom_points_to_nparray(self, top_bottom_points):
        tmp_result_top_bottom_points_array = []
        
        top_bottom_points_length = len(top_bottom_points)
        for index in range(top_bottom_points_length):
            new_point = []
            cur_point = top_bottom_points[top_bottom_points_length-index-1]
            new_point.append(mdates.date2num(datetime.datetime.strptime(cur_point.get_start_date(), "%Y-%m-%d").date()))
            new_point.append(float(cur_point.get_ord_volume()))
            new_point.append(str(cur_point.get_trend()))
            new_point.append(float(cur_point.get_price()))

            tmp_result_top_bottom_points_array.append(new_point)
        
        result_top_bottom_points_array = np.array(tmp_result_top_bottom_points_array)
        #pprint(result_top_bottom_points_array)
        #print type(result_top_bottom_points_array)
        
        return result_top_bottom_points_array


if __name__ == "__main__":
    convertHelper = ConvertHelper()

    start_date = '2015-01-04'
    end_date = '2015-01-09'
    share = Share("AAPL")
    historical_data = share.get_historical(start_date, end_date)
    #convertHelper.historical_data_to_nparray(historical_data)
 
