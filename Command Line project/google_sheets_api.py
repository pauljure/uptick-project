#this handles all the google sheets varibles and names of sheets

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
stockList = client.open("STOCKS LIST").sheet1
AAPL_data = client.open("AAPL_data").sheet1
VZ_data = client.open("VZ_data").sheet1
AMZN_data = client.open("AMZN_data").sheet1
MSFT_data = client.open("MSFT_data").sheet1
TSLA_data = client.open("TSLA_data").sheet1
GOOGL_data = client.open("GOOGL_data").sheet1
INTC_data = client.open("INTC_data").sheet1
CSCO_data = client.open("CSCO_data").sheet1
ORCL_data = client.open("ORCL_data").sheet1
QCOM_data = client.open("QCOM_data").sheet1
FB_data = client.open("FB_data").sheet1
IBM_data = client.open("IBM_data").sheet1
sector_data = client.open("sector_data").sheet1

AAPL_news_data = client.open("AAPL_news_data").sheet1
sector_news_data = client.open("sector_news_data").sheet1

AAPL_news_rTime = client.open("AAPL_news_rTime").sheet1
sector_news_rTime = client.open("sector_news_rTime").sheet1

AAPL_tweets_data = client.open("AAPL_tweets_data").sheet1
AAPL_tweets_rTime = client.open("AAPL_tweets_rTime").sheet1

#real time sheets
APPL_rTime = client.open("AAPL_rTime").sheet1
TSLA_rTime = client.open("TSLA_rTime").sheet1
MSFT_rTime = client.open("MSFT_rTime").sheet1
VZ_rTime = client.open("VZ_rTime").sheet1
AMZN_rTime = client.open("AMZN_rTime").sheet1
GOOGL_rTime = client.open("GOOGL_rTime").sheet1
INTC_rTime = client.open("INTC_rTime").sheet1
CSCO_rTime = client.open("CSCO_rTime").sheet1
ORCL_rTime = client.open("ORCL_rTime").sheet1
QCOM_rTime = client.open("QCOM_rTime").sheet1
FB_rTime = client.open("FB_rTime").sheet1
IBM_rTime = client.open("IBM_rTime").sheet1
sector_rTime = client.open("sector_rTime").sheet1



