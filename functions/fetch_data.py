import json,sys,os,requests
from datetime import datetime,date,timedelta
from time import sleep
import time

#folder to store the data in
folder = 'data/'

#this is the date where we start downloading our prices..
#if you already have data and want to change the initialStartDate then
#make sure to reforce a complete download by using latest_data = 0 in updatePriceData function
initialStartDate = date(2021,11,1).strftime("%s")+'000'

#put in all pairs you like to download data for.. keep in mind, that it will take some time to download all data if you start a few months back!
pairs =['SOLUSDT','LUNAUSDT','AVAXUSDT','ADAUSDT','ATOMUSDT','ROSEUSDT','SANDUSDT','APEUSDT','DOTUSDT','LTCUSDT','TRXUSDT','OCEANUSDT','SHIBUSDT','DOGEUSDT','CRVUSDT','NEARUSDT','RUNEUSDT','ZILUSDT','MATICUSDT','FTTUSDT','XRPUSDT','UNIUSDT','LINKUSDT','VETUSDT','AAVEUSDT','CHZUSDT','FTMUSDT','HNTUSDT','AXSUSDT','MANAUSDT','SYSUSDT','BCHUSDT','AMPUSDT','ZECUSDT','FILUSDT','ONEUSDT','ETCUSDT','BATUSDT','EOSUSDT','YFIUSDT','COMPUSDT','MKRUSDT','SKLUSDT','OGNUSDT','ALGOUSDT','ZENUSDT','LPTUSDT','XLMUSDT']


#This function downloads all 1m data into a local file. e.g. MATICUSDT.txt
def downloadPriceData(symbol,startTime):

    endTime = datetime.now().strftime("%s")+'000'

    #this is the lowest we can get.. changing that doesnt make sense
    interval='1m'

    #we want as much data as we get per call. the limit is 1500
    limit = '1500'

    while int(endTime) > int(startTime):
        print ("Downloading Price Data: " + symbol)
        interval='1m'

        url = 'https://api.binance.com/api/v3/klines?symbol='+symbol+'&interval='+interval+'&limit='+str(limit)+'&startTime='+str(startTime)

        data = requests.get(url).json()

        #lets store everything locally.
        file_name=symbol + ".txt"
        f = open(folder + file_name, "a")

        for x in data:

            date = datetime.fromtimestamp(x[0]/1000)
            int_date = int(time.mktime(date.timetuple())*1000)

            if int_date < getCurrentTime():
                price_open = float(x[2])
                price_high = float(x[2])
                price_low = float(x[3])
                price_close = float(x[4])
                f.write(date.strftime("%Y-%m-%d %H:%M:%S") + ';' + str(price_open) + ';' + str(price_high) + ';' + str(price_low)+ ';' + str(price_close) + '\n')

        f.close()

        #next dataset
        startTime = int(x[0]) + 60000

def checkCache(symbol):

    #do we already have some data?
    file_name=symbol + ".txt"
    try:
        f = open(folder + file_name, "r")
        content = f.readlines()
        #we are returning the last line to get the latest timestamp from
        return [content[-1]]
    except:
        return 0

def getCurrentTime():
    now = datetime.now().replace(microsecond=0).replace(second=0)
    now = int(time.mktime(now.timetuple())*1000)
    return now

def updatePriceData(pair):

    #checking the cache to get the time of the latest data
    latest_data = checkCache(pair)

    #Set latest_data=0 to force a fresh update with the given start date
    #latest_data=0

    if latest_data ==0:

        try:
            file_name= pair + ".txt"
            os.remove(folder + file_name)
        except:
            pass

        print ('download all data')
        startTime = initialStartDate
        downloadPriceData(pair,startTime)
        #download all dataset
    else:
        #fetch only new data
        last_date = latest_data[0].strip().split(';')[0]
        last_date = datetime.strptime(last_date, "%Y-%m-%d %H:%M:%S")

        last_date = last_date + timedelta(minutes=1)

        last_date = int(time.mktime(last_date.timetuple())*1000)

        if getCurrentTime() > last_date:
            downloadPriceData(pair,last_date)
def updateAllData():
    for symbol in pairs:
        updatePriceData(symbol)
