#THIS IS THE MAIN EXECUTION FILE THAT HANDLES
#IMPORTS AND TIMING OF UPDATING ALL THE SHEETS

# TEAM UPTICK

#file paths management
import sys
sys.path.insert(0, './Legacy Quotes')
sys.path.insert(0, './Legacy News')
sys.path.insert(0, './Legacy Tweets')

sys.path.insert(0, './Real Time News')
sys.path.insert(0, './Real Time Quotes')
sys.path.insert(0, './Real Time tweets')


#import each helper file that is in charge of updating specific sheets
import legacy_stocks_updater as LSU #10 legacy tech quotes
import tech_sector_quote_updater as TSQU #legacy hourly sector data
import AAPL_news_data_updater as ANDU #legacy news about apple
import sector_news_data_updater as SNDU #legacy news about tech sector
import APPL_News_rTime_updater as ANRTU #real time apple news events
import sector_News_rTime_updater as SNRTU #real time tech sector news events
import rTime_stock_updater as RTSU  #real time quote updater
import rTime_sector_quote_updater as RTSQU #real time sector updater
import AAPL_tweets_data_updater as ATDU #legacy tweets
import APPL_rTime_tweet_updater as ARTTU #real time tweets

#import google_sheets_api as sheet
#import yahoo as news

#LSU.legacy_stock_updator() # will run once a day
#TSQU.update_sector_performance() # will run once a day
#ANDU.update_APPL_news_data() # will run once a day
#SNDU.update_sector_news_data() # will run once a day
#ANRTU.update_APPL_news_rTime() #will run every hour
#SNRTU.update_sector_News_rTime() # will run every hour
#RTSU.update_rTime_Quotes()  # will run every 10 min
#RTSQU.update_sector_rTime() # will run every 10 min
#ATDU.update_AAPL_tweets_data() #will run once a day
ARTTU.update_AAPL_tweets_rTime() #will run every hour
