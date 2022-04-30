import json,sys,os,requests
from datetime import datetime,date,timedelta
from time import sleep
import time

sys.path.insert(0,'functions')

from bot_config import *
from fetch_data import *
from backtest import *


#lets define the pair we want to backtest
pair = 'ZILUSDT'

#update the price data for this pair.. you should comment it out to avoid fetching data every time you are testing --> put a # in front of the line.
updatePriceData(pair)

#the bot_config we like to backtest
config = getSingleConfig('euphoria')

#print(config.to_json())

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



#we can adjust every config paramater on the fly to find the sweet spot.
#in this case we are first doing a loop over the deviation_to_open_safety_order from 1.5 to 3
#within the first loop we are doing another loop to adjust the safety_order_volume_scale and the safety_order_step_scale
#this shows us that even for a coin like ZILUSDT in April we would find configs that were profitable

config.max_safety_orders = 8
config.deviation_to_open_safety_order=1.5
safety_order_volume_scale = config.safety_order_volume_scale
safety_order_step_scale = config.safety_order_step_scale
results=[]

while config.deviation_to_open_safety_order <= 3:
    while config.safety_order_volume_scale <= 2:
        config.max_safety_order_price_deviation,config.max_amount_for_bot_usage = getMax(config)
        #print (config.to_json())
        result =  startBacktest(config,pair,startDate,endDate)

        print (pair, result['profit_percent'],config.max_amount_for_bot_usage,result['profit'],round(config.safety_order_volume_scale,2),config.safety_order_step_scale,config.max_safety_order_price_deviation,round(config.deviation_to_open_safety_order,2))
        config.safety_order_step_scale -=0.01
        config.safety_order_volume_scale +=0.01
        results.append(result)
    config.safety_order_volume_scale = safety_order_volume_scale
    config.safety_order_step_scale = safety_order_step_scale
    config.deviation_to_open_safety_order +=0.05
saveResult(results,'looping_parameters.csv')
