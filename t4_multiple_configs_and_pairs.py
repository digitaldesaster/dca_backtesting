import json,sys,os,requests
from datetime import datetime,date,timedelta
from time import sleep
import time

sys.path.insert(0,'functions')

from bot_config import *
from fetch_data import *
from backtest import *

#the date from which the backtest should start
startDate = date(2022,4,1).strftime("%Y-%m-%d %H:%M:%S")
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

#we are overwriting pairs here.. pairs is defined in fetch_data.. but in this example we want only two pairs..
pairs=['SOLUSDT','ZILUSDT']
for pair in pairs:
    updatePriceData(pair)

results=[]
for config in config_list:
    if config.config_name in whitelist or whitelist==[]:
        for pair in pairs:
            result = startBacktest(config,pair,startDate,endDate)
            results.append(result)
            print (config.config_name, pair, result['profit'],result['max_amount_for_bot_usage'],result['profit_percent'])
saveResult(results,'multiple_configs_and_pairs.csv')
