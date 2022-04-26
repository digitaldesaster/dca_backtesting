import json,sys,os,requests
from datetime import datetime,date,timedelta
from time import sleep
import time

sys.path.insert(0,'functions')

from bot_config import *
from fetch_data import *
from backtest import *

#lets define the pair we want to backtest
pair = 'SOLUSDT'

#update the price data for this pair.. you should comment it out to avoid fetching data every time you are testing --> put a # in front of the line.
#updatePriceData(pair)

#the date from which the backtest should start
startDate = date(2022,1,1).strftime("%Y-%m-%d %H:%M:%S")
#this date can be different from the initialStartDate we used to fetch our data.
#so we can download all data from the last 6 months but we start our backtest 3 months ago.. or 3 days.. whatever
#we will format this date as a string and it should look like this 2021-11-01 00:00:00
#the format found in the price files ('SOLUSDT.txt') needs to be the same format!!!

#the date at which the backtest should end. by default the test runs as long as data is avaiable..
endDate = date(2022,4,30).strftime("%Y-%m-%d %H:%M:%S")

#we can also test one pair against all configs.
config_list = getAllConfigs()

#we can whitelist configs.. so we load all, but test only against the ones that are whitelisted..
#set whitelist=[] to test against all configs
whitelist = ['ta_standard','profundity','verrb','banshee','euphoria','alpha','nutcracker-2','scarta+','set_5_-_test_6','bitman']
#whitelist=[]
results=[]
for config in config_list:
    if config.config_name in whitelist or whitelist==[]:
        result = startBacktest(config,pair,startDate,endDate)
        #lets say we only want to find the configs with a profit of at least 5 percent
        #if result['profit_percent'] > 5:
            #print (result['config_name'],result['profit'],result['max_safety_order_price_deviation'],result['max_amount_for_bot_usage'],result['profit_percent'])
        results.append(result)
#we can save the result to a csv file for further analysis (folder = results)
saveResult(results,'multiple_configs.csv')
