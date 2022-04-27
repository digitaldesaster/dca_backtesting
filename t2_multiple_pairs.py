import json,sys,os,requests
from datetime import datetime,date,timedelta
from time import sleep
import time

sys.path.insert(0,'functions')

from bot_config import *
from fetch_data import *
from backtest import *

#this updates all prices for all pairs as defined in the fetch_data.py
updateAllData()

#the bot_config we like to backtest
config = getSingleConfig('euphoria')

#to see which names are available just use..
#for config in getAllConfigs():
#    print (config.config_name)

#if we like to check the config we can print the json_array
#print (config.to_json())

#we can adjust the config it we want...
#config.base_order = 15
#config.safety_order = 15
#config.max_safety_orders=9
#we need to update max_safety_order_price_deviation and max_amount_for_bot_usage !!!!!
#config.max_safety_order_price_deviation,config.max_amount_for_bot_usage = getMax(config)

#the date from which the backtest should start
startDate = date(2022,4,1).strftime("%Y-%m-%d %H:%M:%S")
#this date can be different from the initialStartDate we used to fetch our data.
#so we can download all data from the last 6 months but we start our backtest 3 months ago.. or 3 days.. whatever
#we will format this date as a string and it should look like this 2021-11-01 00:00:00
#the format found in the price files ('SOLUSDT.txt') needs to be the same format!!!

#the date at which the backtest should end. by default the test runs as long as data is avaiable..
endDate = date(2022,4,30).strftime("%Y-%m-%d %H:%M:%S")

#we can test one config against all pairs:
results=[]
for pair in pairs:
    result = startBacktest(config,pair,startDate,endDate)
    results.append(result)
    print (pair, result['profit'],result['max_amount_for_bot_usage'],result['profit_percent'])

#we can save the result to a csv file for further analysis (folder = results)
saveResult(results,'multiple_pairs.csv')
