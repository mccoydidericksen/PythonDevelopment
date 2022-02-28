import json
import requests
import time
import pandas as pd
from datetime import datetime
import pytz
# --------------------------------------------------------------------
# perform a mean reversion strategy with shorting on list of stock prices
# --------------------------------------------------------------------
def meanReversionStrategy(prices, ticker):
    i = 0
    buy = 0
    short = 0
    total_profit = 0
    today = datetime.now(pytz.timezone('US/Mountain'))
    for current_price in prices:
        if i > 5: 
        # if i >= 5, slice out previous 5 stock prices by subtracting from i and using as index
        # calculate 5 day avg_price by summing up values in last_five list and divide by 5
            index_first = i - 6
            index_last = i - 1 
            price_list = pd.DataFrame(prices)
            price_list = price_list['close'].tolist()
            last_five = price_list[index_first:index_last]
            last_five = [(round(int(price), 2)) for price in last_five]
            moving_average = round(sum(last_five) / 5, 2)
            if current_price['close'] < moving_average * .95 and buy == 0: #buy
                buy = round(int(current_price['close']), 2)
                if short != 0 and buy != 0:
                    total_profit += (short - buy)
                if str(current_price['date']) == today.strftime("%Y-%m-%d"):
                    print('You should buy ' + ticker + ' today for $' + str(current_price['close']))
                short = 0
            elif current_price['close'] > moving_average * 1.05 and short == 0: #sell (same as short)
                short = round(int(current_price['close']), 2)
                if short != 0 and buy != 0:
                    total_profit += (short - buy)
                if str(current_price['date']) == today.strftime("%Y-%m-%d"):
                    print('You should sell ' + ticker + ' today for $' + str(current_price['close']))
                buy = 0
        # add one to n (number of iterations) and set current price to i
        i += 1
    total_percentage = round(int((total_profit / int(prices[0]['close']))), 2) * 100
    print("total profit:", str(total_profit) + "%")
    print("final percentage:", str(total_percentage) + "%")
    
    return total_profit, total_percentage
# --------------------------------------------------------------------
# perform a simple moving average strategy on list of stock prices
# --------------------------------------------------------------------    
def simpleMovingAverageStrategy(prices, ticker):
    n = 0
    buy_count = 0
    total_profit = 0
    sell_count = 0
    avg_price = 0
    today = datetime.now(pytz.timezone('US/Mountain'))
    for current_price in prices:
        # add one to n (number of iterations) and set current price to i
        n += 1
        # if n >= 5, slice out previous 5 stock prices by subtracting from n and using as index
        # calculate 5 day avg_price by summing up values in last_five list and divide by 5
        if n > 5:
            index_first = n - 6
            index_last = n - 1 
            price_list = pd.DataFrame(prices)
            price_list = price_list['close'].tolist()
            last_five = price_list[index_first:index_last]
            last_five = [(round(int(price), 2)) for price in last_five]
            avg_price = round(sum(last_five) / 5, 2)
            # if current_price is lass than 5 day average, buy stock
            if current_price['close'] > avg_price:
                # if buy_first == 1, keep track of first buy, add 1 to buy_count variable
                if buy_count == 0:
                    buy_count += 1
                    buy = round(int(current_price['close']), 2)
                    if str(current_price['date']) == today.strftime("%Y-%m-%d"):
                        print('You should buy ' + ticker + ' today for $' + str(current_price['close']))
                    first_buy = current_price['close']
                # if sell_count == buy_count, buy stock, add one to buy_count
                elif sell_count == buy_count:
                    buy_count += 1
                    buy = current_price['close']
            # if current_price is greater than 5 day average and sell_count is less than buy_count, sell stock
            elif (current_price['close'] < avg_price) and (sell_count < buy_count): 
                # add one to sell_count, set sell variable to current_price, calculate profit of sell
                # keep a running total of profit for after loop
                sell_count += 1
                sell = round(int(current_price['close']), 2)
                if str(current_price['date']) == today.strftime("%Y-%m-%d"):
                    print('You should sell ' + ticker + ' today for $' + str(current_price['close']))
                profit = sell - buy
                total_profit += profit 

    # print total profit, first buy price, and calculate return percentage and print that too
    print('total profit:', str(round(total_profit, 2)) + '%')
    percentage_returns = (total_profit / first_buy) * 100
    print('final percentage: ' + str(round(percentage_returns, 2)) + '%')
    
    return total_profit, percentage_returns
    
# --------------------------------------------------------------------
# perform a bollinger bands strategy on list of stock prices
# --------------------------------------------------------------------    
def bollingerBands(prices, ticker):
    n = 0
    buy_count = 0
    total_profit = 0
    sell_count = 0
    avg_price = 0
    today = datetime.now(pytz.timezone('US/Mountain'))
    for current_price in prices:
        # add one to n (number of iterations) and set current price to i
        n += 1
        # if n >= 5, slice out previous 5 stock prices by subtracting from n and using as index
        # calculate 5 day avg_price by summing up values in last_five list and divide by 5
        if n > 5:
            index_first = n - 6
            index_last = n - 1 
            price_list = pd.DataFrame(prices)
            price_list = price_list['close'].tolist()
            last_five = price_list[index_first:index_last]
            last_five = [(round(int(price), 2)) for price in last_five]
            avg_price = round(sum(last_five) / 5, 2)
            # if current_price is lass than 5 day average, buy stock
            if current_price['close'] > (avg_price * 1.05):
                # if buy_first == 1, keep track of first buy, add 1 to buy_count variable
                if buy_count == 0:
                    buy_count += 1
                    buy = round(int(current_price['close']), 2)
                    if str(current_price['date']) == today.strftime("%Y-%m-%d"):
                        print('You should buy ' + ticker + ' today for $' + str(current_price['close']))
                    first_buy = current_price['close']
                # if sell_count == buy_count, buy stock, add one to buy_count
                elif sell_count == buy_count:
                    buy_count += 1
                    buy = current_price['close']
            # if current_price is greater than 5 day average and sell_count is less than buy_count, sell stock
            elif (current_price['close'] < (avg_price * .95)) and (sell_count < buy_count): 
                # add one to sell_count, set sell variable to current_price, calculate profit of sell
                # keep a running total of profit for after loop
                sell_count += 1
                sell = round(int(current_price['close']), 2)
                if str(current_price['date']) == today.strftime("%Y-%m-%d"):
                    print('You should sell ' + ticker + ' today for $' + str(current_price['close']))
                profit = sell - buy
                total_profit += profit 

    # print total profit, first buy price, and calculate return percentage and print that too
    print('total profit:', str(round(total_profit, 2)) + '%')
    percentage_returns = (total_profit / first_buy) * 100
    print('final percentage: ' + str(round(percentage_returns, 2)) + '%')
    
    return total_profit, percentage_returns
# --------------------------------------------------------------------
# saves results to json file
# --------------------------------------------------------------------    
def saveResults(results):
    json.dump(results, open('/home/ubuntu/environment/final_project/results.json', 'w'))

# --------------------------------------------------------------------
# loop through ticker list, open stock data files, convert to list with rounded price values, 
# call functions to calculate stategy results, call function to save results 
# --------------------------------------------------------------------
def perform_strategies(tickers):
    results = {}
    for ticker in tickers:
        ticker_csv = pd.read_csv('/home/ubuntu/environment/final_project/data/' + ticker + '.csv')
        prices = ticker_csv[['close', 'date']].to_dict('records')
        print(ticker + ' Mean Reversion Strategy Output:')
        print('---------------------------')
        total_profit, percentage_returns = meanReversionStrategy(prices, ticker)
        print('---------------------------')
        results[ticker + '_mr_profit'] = round(total_profit, 2)
        results[ticker + '_mr_percentage_returns'] = round(percentage_returns, 2)
        print(ticker + ' Moving Average Strategy Output:')
        print('---------------------------')
        total_profit, percentage_returns = simpleMovingAverageStrategy(prices, ticker)
        print('---------------------------')
        results[ticker + '_sma_profit'] = round(total_profit, 2)
        results[ticker + '_sma_percentage_returns'] = round(percentage_returns, 2)
        print(ticker + ' Bollinger Bands Strategy Output:')
        print('---------------------------')
        total_profit, percentage_returns = bollingerBands(prices, ticker)
        print('---------------------------')
        results[ticker + '_bb_profit'] = round(total_profit, 2)
        results[ticker + '_bb_percentage_returns'] = round(percentage_returns, 2)
    results_df = pd.DataFrame(results, index=[0])
    best_performer = str(results_df.idxmax(axis=1))
    best_performer = best_performer.replace(' ', '').replace('0', '').replace('dtype:object', '')
    best_performer = best_performer.strip()
    print('The best stock and strategy performance was:', best_performer)
    results['best_performer'] = best_performer
    saveResults(results)
# --------------------------------------------------------------------
# creates initial data to csv files
# --------------------------------------------------------------------  
def create_data(tickers):
    for ticker in tickers:
        url = 'http://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&outputsize=full&apikey=LG0ZM035TH6O0MEI'
        print(url)
        request = requests.get(url)
        rqst_dict = json.loads(request.text)
        key_series = "Time Series (Daily)"
        key_open = '1. open'
        key_close = '4. close'
        key_hi = '2. high'
        key_lo = '3. low'
        prices = []
        for date in rqst_dict[key_series]:
            row = ""
            row += date + ","
            row += rqst_dict[key_series][date][key_open] + ","
            row += rqst_dict[key_series][date][key_hi] + ","
            row += rqst_dict[key_series][date][key_lo] + ","
            row += rqst_dict[key_series][date][key_close] + "\n"
            prices.append(row)
        prices.reverse()
        csv_file = open('/home/ubuntu/environment/final_project/data/' + ticker + ".csv", "w")
        csv_file.write("date,open,hi,lo,close\n")
        
        for row in prices:
            csv_file.write(row)
            
        csv_file.close()
        time.sleep(12)
# --------------------------------------------------------------------
# appends new data to csv files
# --------------------------------------------------------------------    
def append_data(tickers):
    for ticker in tickers:
        url = 'http://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&outputsize=full&apikey=LG0ZM035TH6O0MEI'
        request = requests.get(url)
        rqst_dict = json.loads(request.text)
        
        key_series = "Time Series (Daily)"
        key_open = '1. open'
        key_close = '4. close'
        key_hi = '2. high'
        key_lo = '3. low'
        
        # get the last day, of data
        file = open('/home/ubuntu/environment/final_project/data/' + ticker + ".csv")
        lines = file.readlines()
        last_line = lines[-1]
        items = last_line.split(",")
        last_date = items[0]
        
        # append new data to csv file
        prices = []
        for date in rqst_dict[key_series]:
            row = ""
            row += date + ","
            row += rqst_dict[key_series][date][key_open] + ","
            row += rqst_dict[key_series][date][key_hi] + ","
            row += rqst_dict[key_series][date][key_lo] + ","
            row += rqst_dict[key_series][date][key_close] + "\n"
            if date > last_date:
                prices.append(row)
        prices.reverse()
        csv_file = open('/home/ubuntu/environment/final_project/data/' + ticker + ".csv", "a")
        for row in prices:
            csv_file.write(row)
        csv_file.close()
        time.sleep(12)

# --------------------------------------------------------------------
# calls other functions
# --------------------------------------------------------------------   
tickers = ['AAPL', 'ADBE', 'CRWD', 'GMED', 'GOOG', 'INTU', 'MRNA', 'PINS', 'SHOP', 'TSLA']    
# create_data(tickers)
append_data(tickers)
perform_strategies(tickers)
