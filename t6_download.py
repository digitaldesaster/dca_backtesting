import json,sys,os,requests
from datetime import datetime,date,timedelta
from time import sleep
import time

sys.path.insert(0,'functions')

from bot_config import *
from fetch_data import *
from backtest import *


#lets define the pair we want to backtest
pair = 'ETHUSDT'

#update the price data for this pair.. you should comment it out to avoid fetching data every time you are testing --> put a # in front of the line.
updatePriceData(pair)
