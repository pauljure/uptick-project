#UPDATES legacy_stocks_updater google sheet

# IMPORTS #
import time
import datetime as dt

import pandas as pd
import numpy as np
from copy import copy

import legacy_stocks_updater as LSU
import google_sheets_api as sheet

apikey = '0adbf00b462c1acca954a43d94279b92' #barchart api key



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
syms = getStockList()
print(syms)

#BARCHART API
def construct_barChart_url(sym, start_date, freq, interval, api_key=apikey):
    '''Function to construct barchart api url'''
    
    url = 'http://marketdata.websol.barchart.com/getHistory.csv?' +\
        'key={}&symbol={}&type={}&startDate={}&interval={}'.format(api_key, sym, freq, start_date, interval)
    return url

#get minute data for a specified period for a stock
def get_minute_data(start):
    print("minute data:")
    '''Function to Retrieve <= 3 months of minute data for SP500 components'''
    
    # This is the required format for datetimes to access the API
    # You could make a function to translate datetime to this format
    #start = '20181008' #start data doesnt matter as long as its more then a month older
    #end = d
    freq = 'minutes'
    interval = 10 #minutes
    prices = {}
    symbol_count = len(syms)
    N = copy(symbol_count)
    try:
        for i, sym in syms.iterrows():
            
            print(sym["STOCKS"])
            api_url = construct_barChart_url(sym["STOCKS"], start, freq, interval , api_key=apikey)
            print(api_url)
            try:
                csvfile = pd.read_csv(api_url, parse_dates=['timestamp'])
                csvfile.set_index('timestamp', inplace=True)
                prices[sym["STOCKS"]] = csvfile
            except:
                continue
            N -= 1
            pct_total_left = (N/symbol_count)
            print('{}..[done] | {} of {} symbols collected | percent remaining: {:>.2%}'.format(\
                                                                                                sym, i, symbol_count, pct_total_left))
    except Exception as e:
        print(e)
    finally:
        pass
        px = pd.Panel.from_dict(prices)
    
    return px


#helper function
def getStockDataFromDate(start):
    print(syms)
    pxx = get_minute_data(start)
    # convert timestamps to EST
    pxx.major_axis = pxx.major_axis.tz_localize('utc').tz_convert('US/Eastern')
    return pxx

#sends pxx stock data to google sheets. will append pxx to gsheets
def sendLocalStockDataToSheets(pxx):
    print("Sending to google sheets")
    #curr_stock = AAPL_data
    for i, sym in syms.iterrows(): #iterate through the panel symbols
        for index, row in pxx[sym['STOCKS']].iterrows(): #iterate through each row in each symbol
            try:
                time.sleep(0.21)
                print("adding Row to legacy quote sheets...",i)
                if(row.symbol == 'AAPL'):
                    sheet.AAPL_data.append_row([str(row.name), row.symbol, row.tradingDay, row.open, row.high, row.low, row. close, row.volume])
                elif (row.symbol == 'VZ'):
                    sheet.VZ_data.append_row([str(row.name), row.symbol, row.tradingDay, row.open, row.high, row.low, row. close, row.volume])
                elif (row.symbol == 'TSLA'):
                    sheet.TSLA_data.append_row([str(row.name), row.symbol, row.tradingDay, row.open, row.high, row.low, row. close, row.volume])
                elif (row.symbol == 'AMZN'):
                    sheet.AMZN_data.append_row([str(row.name), row.symbol, row.tradingDay, row.open, row.high, row.low, row. close, row.volume])
                elif (row.symbol == 'MSFT'):
                    sheet.MSFT_data.append_row([str(row.name), row.symbol, row.tradingDay, row.open, row.high, row.low, row. close, row.volume])
                elif (row.symbol == 'IBM'):
                    sheet.IBM_data.append_row([str(row.name), row.symbol, row.tradingDay, row.open, row.high, row.low, row. close, row.volume])
                elif (row.symbol == 'FB'):
                    sheet.FB_data.append_row([str(row.name), row.symbol, row.tradingDay, row.open, row.high, row.low, row. close, row.volume])
                elif (row.symbol == 'QCOM'):
                    sheet.QCOM_data.append_row([str(row.name), row.symbol, row.tradingDay, row.open, row.high, row.low, row. close, row.volume])
                elif (row.symbol == 'ORCL'):
                    sheet.ORCL_data.append_row([str(row.name), row.symbol, row.tradingDay, row.open, row.high, row.low, row. close, row.volume])
                elif (row.symbol == 'CSCO'):
                    sheet.CSCO_data.append_row([str(row.name), row.symbol, row.tradingDay, row.open, row.high, row.low, row. close, row.volume])
                elif (row.symbol == 'INTC'):
                    sheet.INTC_data.append_row([str(row.name), row.symbol, row.tradingDay, row.open, row.high, row.low, row. close, row.volume])
                elif (row.symbol == 'GOOGL'):
                    sheet.GOOGL_data.append_row([str(row.name), row.symbol, row.tradingDay, row.open, row.high, row.low, row. close, row.volume])
        
            except:
                print("Error adding row!", row)
                continue


#updates the google sheets tables
def updateSheetsWithLatest():
    print("updating:")
    serverData = sheet.AAPL_data.get_all_values() #only gets the date of AAPL since they should all be uniform
    lastRowOnServer = serverData[-1]
    lastTimestampOnServer = lastRowOnServer[2]
    lastTimestampOnServer_noDash = lastTimestampOnServer.replace("-", "") #remove the dast
    
    localData = getStockDataFromDate(lastTimestampOnServer_noDash)
    sendLocalStockDataToSheets(localData)


#main call for exector, runs script
def legacy_stock_updator():
    updateSheetsWithLatest()
