import json,sys,os,requests,csv
from datetime import datetime,date,timedelta
from time import sleep
import time
from fetch_data import folder

def readPriceData(pair):
    file_name=pair + ".txt"
    f = open(folder + file_name, "r")
    content = f.readlines()
    return content

def saveResult(results,file_name):
    data_file = open('results/' + file_name, 'w')
    csv_writer = csv.writer(data_file)

    count = 0

    for result in results:
        if count == 0:
            header = result.keys()
            csv_writer.writerow(header)
            count += 1

        csv_writer.writerow(result.values())

    data_file.close()

def startBacktest(config,pair,startDate='',endDate=''):
    content = readPriceData(pair)

    start_capital = config.max_amount_for_bot_usage
    avaiable_capital=start_capital
    trading_fee = 0.075
    start = False
    stop = False
    total_deals = 0

    highest_so = 0
    total_so = 0
    max_deal_time = 0

    backtest_start = ''
    backtest_end = ''

    deal_times = []

    reset_data = True

    for line in content:
        data = line.strip().split(';')
        price_date = data[0]

        if startDate=='':
            start = True
            #print ('Start Backtest: ' + price_date)
        else:
            if start ==False:
                if price_date >= startDate:
                    start = True
                    backtest_start = price_date
                    #print ('Start Backtest: ' + price_date)

        if endDate !='':
            if stop == False:
                if price_date >= endDate:
                    stop = True
                    backtest_end = price_date
                    #print ('Stop Backtest: ' + price_date)


        if start == True and stop==False:

            open_price = float(data[1])
            high_price = float(data[2])
            low_price = float(data[3])
            close_price = float(data[4])

            if reset_data:
                bot_total_volume=0
                bot_total_coins = 0
                bot_avg_price = 0

                next_so_buy_price = 0
                sell_price = 0

                safety_order_amount = 0
                safety_order_deviation = 0
                current_safety_order=0
                reset_data=False
                deal_start=price_date
                deal_end=''


            if bot_total_volume==0:
                total_deals +=1
                buy_amount = config.base_order / float(close_price)
                bot_avg_price = close_price

                bot_total_coins += buy_amount
                next_so_buy_price = close_price - (close_price / 100 * config.deviation_to_open_safety_order)

                safety_order_deviation = config.deviation_to_open_safety_order * config.safety_order_step_scale

                sell_price = close_price + (close_price / 100 * config.take_profit)
                bot_total_volume = config.base_order
                avaiable_capital = avaiable_capital - config.base_order
                avaiable_capital = avaiable_capital - (config.base_order/100*trading_fee)

            else:
                #to fill our safety_orders we are looking at the lowest_price of the minute!!!!

                if low_price <=next_so_buy_price:
                    if current_safety_order < config.max_safety_orders:
                        if current_safety_order ==0:
                            safety_order_amount = config.safety_order
                        else:
                            safety_order_amount = safety_order_amount * config.safety_order_volume_scale


                        avaiable_capital = avaiable_capital - safety_order_amount
                        avaiable_capital = avaiable_capital - (safety_order_amount/100*trading_fee)
                        buy_amount = safety_order_amount / float(next_so_buy_price)

                        bot_total_volume = bot_total_volume + safety_order_amount


                        current_safety_order +=1
                        bot_total_coins += buy_amount
                        next_so_buy_price = next_so_buy_price - (next_so_buy_price / 100 * safety_order_deviation)
                        safety_order_deviation = safety_order_deviation * config.safety_order_step_scale


                        bot_avg_price = bot_total_volume / bot_total_coins
                        sell_price = bot_avg_price + (bot_avg_price / 100 * config.take_profit)



                #for our sell orders we are using the highest_price of this minute..
                elif high_price >=sell_price:

                    if highest_so < current_safety_order:
                        highest_so=current_safety_order
                    total_so += current_safety_order

                    sell_amount = bot_total_coins * sell_price

                    avaiable_capital = avaiable_capital + sell_amount

                    #calculating the deal_times
                    deal_end = price_date
                    d_start = datetime.strptime(deal_start,"%Y-%m-%d %H:%M:%S")
                    d_end = datetime.strptime(deal_end,"%Y-%m-%d %H:%M:%S")
                    duration = round((d_end - d_start).total_seconds()/3600,2)

                    if duration > max_deal_time:
                        max_deal_time=duration

                    deal_times.append(duration)

                    reset_data = True


    avg_so = round(total_so / total_deals,2)

    avaiable_capital = round(avaiable_capital,2)
    bot_total_volume = round(bot_total_volume,2)

    bot_capital = round(bot_total_coins*close_price,2)

    bot_current_profit = round(bot_capital-bot_total_volume,2)

    bot_current_profit_percent = round((100/bot_total_volume*bot_capital) - 100,2)

    if endDate !='':
        backtest_end=price_date

    #calculating the average deal_time
    try:
        avg_deal_time=0
        for x in deal_times:
            avg_deal_time = avg_deal_time + x
        avg_deal_time = round(avg_deal_time / len(deal_times),2)
    except:
        avg_deal_time=0
        max_deal_time=0
        pass

    total_capital = round(avaiable_capital + bot_capital,2)
    profit = round(total_capital - start_capital,2)
    profit_percent = round(100 / start_capital * profit,2)

    return {'config_name':config.config_name, 'pair':pair,'total_capital':total_capital,'profit':profit,'profit_percent':profit_percent,'bot_total_volume':bot_total_volume,'bot_current_profit':bot_current_profit,'bot_current_profit_percent':bot_current_profit_percent,'avaiable_capital':avaiable_capital, 'max_amount_for_bot_usage':config.max_amount_for_bot_usage,'max_safety_order_price_deviation':config.max_safety_order_price_deviation, 'total_deals':total_deals,'highest_so':highest_so,'avg_so':avg_so,'backtest_start':backtest_start,'backtest_end':backtest_end,'max_deal_time':max_deal_time,'avg_deal_time':avg_deal_time}
