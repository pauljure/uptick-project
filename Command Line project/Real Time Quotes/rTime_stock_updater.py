#updates rTime_stocks
# IMPORTS #
import time


import pandas as pd

import numpy as np
import datetime as dt

from copy import copy
import google_sheets_api as sheet

apikey = '0adbf00b462c1acca954a43d94279b92' #barchart key

##points to our google sheet "STOCKS LIST" gets the values and makes it a pandas dataframe to manipulate
def getStockList():
    sheetsList = sheet.stockList.get_all_values()
    sheetsList = sheetsList[1:] #remove "STOCKS" title
    ##print(sheetsList)
    sheetsList = flatten(sheetsList)
    #print(sheetsList)
    #create new df
    df = pd.DataFrame({'STOCKS':sheetsList})
    return df

##takes a 2d list and flattens it to 1d
def flatten(input):
    new_list = []
    for i in input:
        for j in i:
            new_list.append(j)
    return new_list

#setting list of stock symbols to var syms
syms = getStockList() #dataframe of the stocks we are getting data for
print(syms)

#BARCHART API
def construct_barChart_url(sym, api_key=apikey):
    '''Function to construct barchart api url'''
    
    url = 'http://marketdata.websol.barchart.com/getQuote.csv?' +\
        'key={}&symbols='.format(api_key, sym)
    return url

import ondemand
# get quote data for Apple and Microsoft
def getStockLiveData(stock):
    od = ondemand.OnDemandClient(api_key=apikey, end_point='https://marketdata.websol.barchart.com/')
    quote = od.quote(stock)['results']
    print(quote)
    return (quote)

getStockLiveData('AAPL')

def sendDataToSheets():
    stocks = syms['STOCKS'].values.tolist()
    for s in stocks:
        time.sleep(0.21)
        print(s)
        stockData = getStockLiveData(s)
        print(stockData)
        
        timestamp = str(dt.datetime.now().time())
        
        if(s == 'AAPL'):
            print("adding AAPL")
            sheet.APPL_rTime.append_row([timestamp, stockData[0]['symbol'], str(dt.date.today()), stockData[0]['lastPrice'], stockData[0]['open'], stockData[0]['high'], stockData[0]['low'], stockData[0]['netChange'], stockData[0]['volume']])
        elif (s == 'VZ'):
            print("adding VZ")
            sheet.VZ_rTime.append_row([timestamp, stockData[0]['symbol'], str(dt.date.today()), stockData[0]['lastPrice'], stockData[0]['open'], stockData[0]['high'], stockData[0]['low'], stockData[0]['netChange'], stockData[0]['volume']])
        elif (s == 'TSLA'):
            print("adding TSLA")
            sheet.TSLA_rTime.append_row([timestamp, stockData[0]['symbol'], str(dt.date.today()), stockData[0]['lastPrice'], stockData[0]['open'], stockData[0]['high'], stockData[0]['low'], stockData[0]['netChange'], stockData[0]['volume']])
        elif (s == 'AMZN'):
            print("adding AMZN")
            sheet.AMZN_rTime.append_row([timestamp, stockData[0]['symbol'], str(dt.date.today()), stockData[0]['lastPrice'], stockData[0]['open'], stockData[0]['high'], stockData[0]['low'], stockData[0]['netChange'], stockData[0]['volume']])
        elif (s == 'MSFT'):
            print("adding MSFT")
            sheet.MSFT_rTime.append_row([timestamp, stockData[0]['symbol'], str(dt.date.today()), stockData[0]['lastPrice'], stockData[0]['open'], stockData[0]['high'], stockData[0]['low'], stockData[0]['netChange'], stockData[0]['volume']])
        elif (s == 'GOOGL'):
            print("adding GOOGL")
            sheet.GOOGL_rTime.append_row([timestamp, stockData[0]['symbol'], str(dt.date.today()), stockData[0]['lastPrice'], stockData[0]['open'], stockData[0]['high'], stockData[0]['low'], stockData[0]['netChange'], stockData[0]['volume']])
        elif (s == 'INTC'):
            print("adding INTC")
            sheet.INTC_rTime.append_row([timestamp, stockData[0]['symbol'], str(dt.date.today()), stockData[0]['lastPrice'], stockData[0]['open'], stockData[0]['high'], stockData[0]['low'], stockData[0]['netChange'], stockData[0]['volume']])
        elif (s == 'CSCO'):
            print("adding CSCO")
            sheet.CSCO_rTime.append_row([timestamp, stockData[0]['symbol'], str(dt.date.today()), stockData[0]['lastPrice'], stockData[0]['open'], stockData[0]['high'], stockData[0]['low'], stockData[0]['netChange'], stockData[0]['volume']])
        elif (s == 'ORCL'):
            print("adding ORCL")
            sheet.ORCL_rTime.append_row([timestamp, stockData[0]['symbol'], str(dt.date.today()), stockData[0]['lastPrice'], stockData[0]['open'], stockData[0]['high'], stockData[0]['low'], stockData[0]['netChange'], stockData[0]['volume']])
        elif (s == 'QCOM'):
            print("adding QCOM")
            sheet.QCOM_rTime.append_row([timestamp, stockData[0]['symbol'], str(dt.date.today()), stockData[0]['lastPrice'], stockData[0]['open'], stockData[0]['high'], stockData[0]['low'], stockData[0]['netChange'], stockData[0]['volume']])
        elif (s == 'FB'):
            print("adding FB")
            sheet.FB_rTime.append_row([timestamp, stockData[0]['symbol'], str(dt.date.today()), stockData[0]['lastPrice'], stockData[0]['open'], stockData[0]['high'], stockData[0]['low'], stockData[0]['netChange'], stockData[0]['volume']])
        elif (s == 'IBM'):
            print("adding IBM")
            sheet.IBM_rTime.append_row([timestamp, stockData[0]['symbol'], str(dt.date.today()), stockData[0]['lastPrice'], stockData[0]['open'], stockData[0]['high'], stockData[0]['low'], stockData[0]['netChange'], stockData[0]['volume']])

def update_rTime_Quotes():
    sendDataToSheets()
