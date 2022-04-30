import json,sys,os,requests
from datetime import datetime,date,timedelta
from time import sleep
import time

sys.path.insert(0,'functions')

from bot_config import *
from fetch_data import *
from backtest import *

try:
    import xlwt
except:
    print ('Please install the module xlwt to export .xls files / pip install xlwt')
    sys.exit()

results_folder = 'results/'

def saveXLS(results_grouped,summary,file_name):
    wb = xlwt.Workbook()
    sh = wb.add_sheet('Summary')

    col=0
    for x in summary[0]:
        sh.write(0, col, x)
        col +=1
    row=1
    col=0
    for result in summary:
        for x in result:
            sh.write(row, col, result[x])
            col +=1
        row +=1
        col=0

    for results_group in results_grouped:
        #print (results_group[0])
        if len(results_group[0]['config_name']) > 30:
            sh = wb.add_sheet(results_group[0]['config_name'][0:30])
        else:
            sh = wb.add_sheet(results_group[0]['config_name'])
        col=0
        for x in results_group[0]:
           sh.write(0, col, x)
           col +=1
        row=1
        col=0
        for result in results_group:
            for x in result:
                sh.write(row, col, result[x])
                col +=1
            row +=1
            col=0

    wb.save(results_folder + file_name)

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
#whitelist = ['ta_standard','profundity','verrb','banshee','euphoria','alpha','nutcracker-2','scarta+','set_5_-_test_6','bitman','hybrid','catalyst']
whitelist=['euphoria','ta_standard','outrider']

#we are overwriting pairs here.. pairs is defined in fetch_data.. but in this example we want only two pairs..
pairs=['SOLUSDT','LUNAUSDT']
for pair in pairs:
  updatePriceData(pair)

results=[]
results_grouped=[]
summary=[]

for config in config_list:
    if config.config_name in whitelist or whitelist==[]:
        total_bot_profit = 0
        total_capital = 0
        highest_so = 0
        avg_so = 0
        max_deal_time =  0
        avg_deal_time = 0
        bot_total_volume = 0
        total_deals = 0
        avaiable_capital = 0
        bot_current_profit  = 0
        for pair in pairs:
            result = startBacktest(config,pair,startDate,endDate)
            total_bot_profit = total_bot_profit + result['profit']
            total_capital =  total_capital + result['total_capital']
            if result['highest_so'] > highest_so:
                highest_so = result['highest_so']
            if result['max_deal_time'] > max_deal_time:
                max_deal_time = result['max_deal_time']

            avg_so = avg_so + result['avg_so']
            avg_deal_time = avg_deal_time + result['avg_deal_time']
            total_deals = total_deals + result['total_deals']
            bot_total_volume = bot_total_volume + result['bot_total_volume']
            avaiable_capital = avaiable_capital + result['avaiable_capital']
            bot_current_profit = bot_current_profit + result['bot_current_profit']

            results.append(result)
            #print (config.config_name, pair, result['profit'],result['max_amount_for_bot_usage'],result['profit_percent'])

        results_grouped.append(results)
        results=[]

        total_bot_profit = round(total_bot_profit,2)
        total_bot_profit_percent = round (100 / (config.max_amount_for_bot_usage  * len(pairs)) * total_bot_profit,4)

        bot_current_profit_percent = round (100 / bot_total_volume * bot_current_profit,4)

        avg_so = round(avg_so / (len(pairs)),2)
        avg_deal_time = round(avg_deal_time / len(pairs),2)

        max_amount_for_bot_usage = config.max_amount_for_bot_usage  * len(pairs)

        total = {'config_name':config.config_name, 'pair':'Total','total_capital':total_capital,'profit':total_bot_profit,'profit_percent':total_bot_profit_percent,'bot_total_volume':bot_total_volume,'bot_current_profit':bot_current_profit,'bot_current_profit_percent':bot_current_profit_percent,'avaiable_capital':avaiable_capital, 'max_amount_for_bot_usage':max_amount_for_bot_usage,'max_safety_order_price_deviation':config.max_safety_order_price_deviation, 'total_deals':total_deals,'highest_so':highest_so,'avg_so':avg_so,'backtest_start':result['backtest_start'],'backtest_end':result['backtest_end'],'max_deal_time':max_deal_time,'avg_deal_time':avg_deal_time}

        summary.append(total)

        print (config.config_name,config.max_amount_for_bot_usage, total_bot_profit, total_bot_profit_percent)

saveXLS(results_grouped,summary,'multiple_configs_and_pairs.xls')
