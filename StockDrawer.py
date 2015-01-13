from YahooFinance import Share
from BaseAnalyzer import BaseAnalyzer
from const import *
from ConvertHelper import ConvertHelper

from pprint import pprint
import datetime
import json
import locale

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import matplotlib

from matplotlib.finance import candlestick_ochl


locale.setlocale(locale.LC_ALL, 'en_US')

class StockDrawer(object):
    def __init__(self):
        self.plt = plt
        self.fig=self.plt.figure()
        self.axis_list = []

    def rsi_calculator(self, prices, n=14):
        
        deltas = np.diff(prices)
        seed = deltas[:n+1]
        up = seed[seed>=0].sum()/n
        down = -seed[seed<0].sum()/n
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:n] = 100. - 100./(1.+rs)

        for i in range(n, len(prices)):
            delta = deltas[i-1] # cause the diff is 1 shorter

            if delta>0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up*(n-1) + upval)/n
            down = (down*(n-1) + downval)/n

            rs = up/down
            rsi[i] = 100. - 100./(1.+rs)

        return rsi

    def draw_rsi(self, np_historical_data):
        np_historical_data_trans = np.transpose(np_historical_data)
        date = np_historical_data_trans[0]
        open_price = np_historical_data_trans[1]
        close_price = np_historical_data_trans[2]
        high_price = np_historical_data_trans[3]
        low_price = np_historical_data_trans[4]
        volume = np_historical_data_trans[5]
        
        
        ax0 = self.plt.subplot2grid((6,4), (4,0), sharex=self.axis_list[0], rowspan=1, colspan=4, axisbg='#07000d')
        rsi = self.rsi_calculator(close_price)
        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'

        ax0.plot(date[:], rsi[:], rsiCol, linewidth=1.5)
        ax0.axhline(70, color=negCol)
        ax0.axhline(30, color=posCol)
        ax0.fill_between(date[:], rsi[:], 70, where=(rsi[:]>=70), facecolor=negCol, edgecolor=negCol, alpha=0.5)
        ax0.fill_between(date[:], rsi[:], 30, where=(rsi[:]<=30), facecolor=posCol, edgecolor=posCol, alpha=0.5)
        ax0.set_yticks([30,70])
        ax0.yaxis.label.set_color("w")
        ax0.spines['bottom'].set_color("#5998ff")
        ax0.spines['top'].set_color("#5998ff")
        ax0.spines['left'].set_color("#5998ff")
        ax0.spines['right'].set_color("#5998ff")
        ax0.tick_params(axis='y', colors='w')
        ax0.tick_params(axis='x', colors='w')
        plt.ylabel('RSI')
        self.axis_list.append(ax0)


    def draw_historical_data(self, np_historical_data):
        
        np_historical_data_trans = np.transpose(np_historical_data)
        date = np_historical_data_trans[0]
        open_price = np_historical_data_trans[1]
        close_price = np_historical_data_trans[2]
        high_price = np_historical_data_trans[3]
        low_price = np_historical_data_trans[4]
        volume = np_historical_data_trans[5]
        
        
        ax1=self.plt.subplot2grid((6,4), (0,0), rowspan=3, colspan=4, axisbg='#07000d')
        candlestick_ochl(ax1, np_historical_data, width=0.5, colorup='#9eff15', colordown='#ff1717')
        self.plt.ylabel("Stock Price")
        ax1.grid(True, color='w')
        ax1.yaxis.label.set_color("w")
        ax1.spines['top'].set_color("#5998ff")
        ax1.spines['bottom'].set_color("#5998ff")
        ax1.spines['left'].set_color("#5998ff")
        ax1.spines['right'].set_color("#5998ff")
        ax1.tick_params(axis='y', colors='w')
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        self.axis_list.append(ax1)

        ax2 = self.plt.subplot2grid((6,4), (3,0), rowspan=1, colspan=4, axisbg='#07000d',
                                    sharex=self.axis_list[0])
        ax2.bar(date, volume)
        self.plt.ylabel("Volume")
        ax2.grid(True, color='w')
        ax2.yaxis.label.set_color("w")
        ax2.spines['top'].set_color("#5998ff")
        ax2.spines['bottom'].set_color("#5998ff")
        ax2.spines['left'].set_color("#5998ff")
        ax2.spines['right'].set_color("#5998ff")
        ax2.tick_params(axis='y', colors='w')
        self.axis_list.append(ax2)

        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(90)
        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(90)

        

    def show(self):
        matplotlib.rcParams.update({'font.size': 9})
        self.plt.subplots_adjust(left=.10, bottom=.10, right=.93, top=.95, wspace=.20, hspace=.00)

        # Remove all the axis labels but the last one
        for index in range(len(self.axis_list)):
            if index == len(self.axis_list):
                break
            self.plt.setp(self.axis_list[index].get_xticklabels(), visible=False)
        
        self.plt.xlabel("Date")
        self.plt.suptitle("Stock Price and Volume and Ord Volume")
        self.plt.show()
        

class OrdDrawer(StockDrawer):
    def draw_ord_volume_data(self, np_top_bottom_points):

        np_top_bottom_points_trans = np.transpose(np_top_bottom_points)
        date = np_top_bottom_points_trans[0]
        ord_volume = np_top_bottom_points_trans[1]
        trend = np_top_bottom_points_trans[2]
        price = np_top_bottom_points_trans[3]

        ax1=self.plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, axisbg='#07000d',
                                  sharex=self.axis_list[0])
        ax1.plot(date, price)
        self.plt.ylabel("Ord Volume")
        ax1.grid(True, color='w')
        ax1.yaxis.label.set_color("w")
        ax1.spines['top'].set_color("#5998ff")
        ax1.spines['bottom'].set_color("#5998ff")
        ax1.spines['left'].set_color("#5998ff")
        ax1.spines['right'].set_color("#5998ff")
        ax1.tick_params(axis='y', colors='w')

        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(45)

        for index in range(len(date)):
            if trend[index] == TREND_UP:
                ax1.annotate(str(locale.format("%d", float(ord_volume[index]), grouping=True)+str('(U)')),
                             (date[index], price[index]),
                             fontsize="9", color='r',
                             horizontalalignment='left', verticalalignment='top')
            else:
                ax1.annotate(str(locale.format("%d", float(ord_volume[index]), grouping=True)+str('(D)')),
                             (date[index], price[index]),
                             fontsize="9", color='r',
                             horizontalalignment='left', verticalalignment='bottom')

if __name__ == "__main__":
    print 'HI'
