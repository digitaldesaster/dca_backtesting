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
startDate = date(2022,4,1).strftime("%Y-%m-%d %H:%M:%S")
#this date can be different from the initialStartDate we used to fetch our data.
#so we can download all data from the last 6 months but we start our backtest 3 months ago.. or 3 days.. whatever
#we will format this date as a string and it should look like this 2021-11-01 00:00:00
#the format found in the price files ('SOLUSDT.txt') needs to be the same format!!!

#the date at which the backtest should end. by default the test runs as long as data is avaiable..
endDate = date(2022,4,30).strftime("%Y-%m-%d %H:%M:%S")


#i added getConfigbyBudget in the bot_config.py you define your budget, the amount of bots you want to run and the min_deviation you want to cover..like 40% in our example
#it will give you all the bots the costs around 500$ per bot .. its +- 10%.. so in this case you will also get bots the cost 450 and bots the cots 550$..
#keep in mind that you would be 10% overextended if you use the 550$ configs!!!
config_list = getConfigsbyBudget(budget=5000,bot_count=10,min_deviation=40)

whitelist=[]
results=[]
for config in config_list:
    if config.config_name in whitelist or whitelist==[]:
        result = startBacktest(config,pair,startDate,endDate)
        results.append(result)
        print (config.config_name, result['profit'],result['max_amount_for_bot_usage'],result['profit_percent'])
#we can save the result to a csv file for further analysis (folder = results)
if results!=[]:
    saveResult(results,'bots_by_budget.csv')
