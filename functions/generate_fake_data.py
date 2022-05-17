import json,sys,os,requests
from datetime import datetime,date,timedelta
from time import sleep
import time

#folder to store the data in
folder = '../data/'

startDate = datetime.strptime('2022-05-01',"%Y-%m-%d")
endDate = datetime.strptime('2022-05-31',"%Y-%m-%d")

prices=[]

f = open(folder + "FAKEUSDT.txt", "w")

initial_price = 100
price = initial_price

#the price first moves from 100$ to 40$.. after reaching 40$ it increases to 60$

price_movements = [40,75,40,53.8]

i=0

while startDate <= endDate:
    #print (startDate,price)

    f.write(startDate.strftime("%Y-%m-%d %H:%M:%S") + ';' + str(price) + ';' + str(price) + ';' + str(price)+ ';' + str(price) + '\n')

    startDate= startDate + timedelta(minutes=1)

    #we are increasing or decreasing the price by 0.1$ every minute..
    if price_movements[i] < price:
        price = round(price - 0.1,2)
    elif price_movements[i] > price:
        price = round(price + 0.1,2)
    else:
        i=i+1
        if i + 1 > len(price_movements):
            break



f.close()
