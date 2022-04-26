This is a very early and experimental version of a DCA backtesting script.
You should use this software for testing purposes only!  (LOL)

The idea behind it is that anyone with basic Python knowledge should be able to make their own backtests with the goal to find the best settings for each market conditions.

Many thanks first of all to TradeAlt and the fantastic community on his discord.
TA Community Discord: https://discord.com/invite/tradealts 												

Many thanks also to Sellium, Ribsy and all the other "config creators".
Sellium has shared a list of the most popular configs here:

https://docs.google.com/spreadsheets/d/1cQ68_Sl70SRFRMeGu0zgBhTCuQvSf6ENi_obLhr7kpw

You should download the latest version as csv file to the configs folder and name it bot_configs.csv

bot_config.py

This script reads the bot_config.csv and provides the data in a form we can work with.

getAllConfigs()

provides an array of all configs.. each element has the class bot_config as defined in bot_config.py.

getSingleConfig('ta_standard')

provides one config. you can loop over getAllConfigs() and print 'config_name' to get the valid names.

getMax(config)

calculates max_safety_order_price_deviation and max_amount_for_bot_usage for a given config.

config.to_json()

provides the config in a readable json format - if you can read json ;-)

for you own settings you could either add them to the bot_config.csv or use the class my_own_config
the my_own_config is added to the array provided by getAllConfigs()

fetch_data.py
This script fetches the price_data (1minute candles - ohlc) from binance and stores it into textfiles into the folder data. e.g. data/SOLUSDT.txt

I normally use mongodb / mongoengine to store data but in this case storing the data in txt-files was a lot faster then using mongodb.

initialStartDate = date(2022,4,1).strftime("%s")+'000'  // this is the oldest date from which we want pricedata from.
Changing the initialStartDate after fetching data doesnt work, you definetly have to redownload everything by setting latest_data = 0 (see below)

pairs =['SOLUSDT','LUNAUSDT','AVAXUSDT','ADAUSDT','ATOMUSDT'] // the pairs we like to have data for.

PLEASE USE THIS WITH CAUTION. IF YOU TRY TO PULL DATA FOR 100 COINS SINCE 2017 THEN YOU COULD HIT THE BINANCE API LIMIT

I have not tested with other pairs then USDT. I think it should work fine will all USD pairs so also BUSD should work.
I think that BTC / ETH pairs will not work. (have not tested this!)

updatePriceData('SOLUSDT') - fetch the latest data for a given pair

updateAllData() - fetches the latest data for all symbols defined in pairs

checkCache('SOLUSDT') - check if data is already available to make sure we only download new data

If you want to redownload the data then you could either delete the txt-files in the data folder or set the variable
latest_data = 0 in the downloadPriceData function...



backtest.py
THIS IS THE TRICKY PART. A SMALL ERROR IN OUR startBacktest FUNCTION AND THE RESULTS ARE USELESS.
The results i was getting from my own backtesting are looking reasonable. I have compared the deals i am running live with the backtesting data and the safety_orders filled / bot_volume looks almost the same. sometimes with one safety_order more or less. the profit / loss looks ok.. sometimes it is very exact and then it is a few % difference. nevertheless, I must currently assume that the code contains errors and the results are therefore inaccurate. especially because the results are different from the ones posted by snurg (thanks for all your efforts and the analysis you have shared!)

PLEASE KEEP IN MIND THAT THIS IS A EARLY VERSION OF THE SCRIPT!!!

BASICALLY, YOU SHOULD TEST EACH CONFIGURATION FOR SEVERAL WEEKS IN 3COMMAS PAPER TRADING MODE. THE IDEA OF THIS SCRIPT IS TO FIND THE CONFIGURATIONS THAT ARE WORTH LOOKING AT MORE CLOSELY.

startBacktest(config,pair,startDate='',endDate=''):
config must be a single config (bot_config class) we are getting from getSingleConfig('SOLUSDT')
pair is a single pair e.g. 'SOLUSDT'

startDate = date(2022,4,1).strftime("%Y-%m-%d %H:%M:%S")
#this date can be different from the initialStartDate we used to fetch our data.
#so we can download all data from the last 6 months but we start our backtest 3 months ago.. or 3 days.. whatever
#we will format this date as a string and it should look like this 2021-11-01 00:00:00
#the format found in the price files ('SOLUSDT.txt') needs to be the same format!!!

endDate = date(2022,4,30).strftime("%Y-%m-%d %H:%M:%S")
#the date at which the backtest should end. by default the test runs as long as data is avaiable..

You will find examples for the testing of single config / multi configs and multiple pairs in the test scripts within this folder.

the function startBacktest returns an json_array with the results.

config_name = the name of the config like 'ta_standard'
pair = the pair we tested like 'SOLUSDT'
bot_total_volume = the total volume currently assumed by the bot (deal volume)
bot_current_profit = the profit or loss of the current deal.. (should be deal_current_profit.. will fix this later..)
bot_current_profit_percent = profit of current deal in percent (..)
avaiable_capital = the capital that is not invested at the moment.
total_capital = this is the bot_volume + avaiable_capital
total_deals = the number of deals closed
highest_so = the highest safety order that got filled
avg_so = the average amount of safety orders that got filled
backtest_start = the start date you submitted in the function startBacktest
backtest_end = the end date you submitted in the function startBacktest
max_amount_for_bot_usage = the max amount the bot can use from our config
max_safety_order_price_deviation = the deviation of the bot like 60%
profit = the total profit / loss of the bot
profit_percent = the total profit / loss in percent

ROADMAP
dont expect an update on the scripts every day.. But i am happy if someone is sharing some improvements or a bugfix in case you find anything.
i will definetly work on some kind of storing the results in a csv file for further analysis in the next few days (end of april / early may)

cheers and happy backtesting..
dd
