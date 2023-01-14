import os
from binance.client import Client
import pandas as pd
import numpy as np
import requests
import warnings
from datetime import datetime, time


def monte_carlo(url):
    print('startei mano')

    extreme_values = []

    def fxn():
        warnings.warn("deprecated", DeprecationWarning)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fxn()

        # from src.router.crypto_router import CryptoRouter
        # conn = Connection()

        # crypto_router = CryptoRouter(conn.connection)

        r = requests.get(
            url).json()

        array_symbols = []
        stable_coins = ['usdt', 'dai', 'busd', 'tusd', 'usdc', 'ust', 'dgx']

        for i in range(len(r)):
            if r[i]['symbol'] not in stable_coins:
                array_symbols.append(r[i]['symbol'].upper()+'USDT')
            else:
                continue

        array_symbols = list(dict.fromkeys(array_symbols))
        

        api_key = os.getenv('BINANCE_KEY')
        api_secret = os.getenv('SECRET_KEY')

        # the sequence of columns of kline-interval-dataframe in binance is?
        # ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
        # 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']

        today = pd.Timestamp.today()
        today_day = today.day
        today_month = pd.Timestamp(today).strftime('%B')[:3]
        today_year = today.year

        date_30_ago = today - pd.Timedelta(days=30)
        date_7_forward = today + pd.Timedelta(days=7)
        date_30_ago_day = date_30_ago.day
        date_30_ago_month = pd.Timestamp(date_30_ago).strftime('%B')[:3]
        date_30_ago_year = date_30_ago.year

        client = Client(api_key, api_secret)

        start_date_binance = f"{date_30_ago_day} {date_30_ago_month}, {date_30_ago_year}"
        end_date_binance = f"{today_day} {today_month}, {today_year}"

        get_all_coins = client.get_all_tickers()

        array_binance_symbols = []
        for coin in range(len(get_all_coins)):
            # get last 4 letters of symbol
            symbol_usdt = get_all_coins[coin]['symbol'][-4:]
            if(symbol_usdt == 'USDT'):
                array_binance_symbols.append(get_all_coins[coin]['symbol'])

        
        symbol_intersection = set.intersection(
            set(array_binance_symbols), set(array_symbols))
        symbol_intersection = sorted(list(symbol_intersection))

        for x in range(len(symbol_intersection)):
            klines = client.get_historical_klines(
                symbol_intersection[x], Client.KLINE_INTERVAL_1DAY, start_date_binance, end_date_binance)

            klines_data = pd.DataFrame(klines)
            df = pd.DataFrame(klines_data[3].astype(float)).rename(
                columns={3: 'Close'}).assign(Return=0.0000)

            for y in range(len(df)-1):

                df.iloc[y, 1] = np.log(df.iloc[y, 0]/df.iloc[y+1, 0])

            last_price = df.iloc[-1, 0]

            daily_volatility = np.std(df['Return'])
            # print('“The daily volatility of the bitcoin is:”',
            #       '{:.2%}'.format(daily_volatility))

            annual_volatility = daily_volatility*np.sqrt(252)
            # print('The annualized volatility of the bitcoin is:',
            #       '{:.2%}'.format(annual_volatility))

            number_simulations = 100
            number_days = 7

            simulation_df = pd.DataFrame()
            
            

            for x1 in range(number_simulations):
                count = 0
                price_series = []

                price = last_price * \
                    (1 + np.random.normal(0, daily_volatility))
                price_series.append(price)

                for y in range(number_days):
                    if count == number_days-1:
                        break
                    price = price_series[count] * \
                        (1 + np.random.normal(0, daily_volatility))
                    price_series.append(price)
                    count += 1

                simulation_df[x1] = price_series

            Q1 = simulation_df.quantile(0.25)
            Q3 = simulation_df.quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5*IQR
            upper_bound = Q3 + 1.5*IQR

            array_outliers = []
            for x2 in range(len(simulation_df)):
                array_outliers.append(simulation_df[x2][(simulation_df[x2] >= lower_bound[x2]) & (
                    simulation_df[x2] <= upper_bound[x2])])

            array_to_pd = pd.DataFrame(array_outliers)

            min_max_array = {min: [], max: []}

            for x3 in range(len(array_to_pd)):
                min_max_array[min].append(array_to_pd[x3].min())
                min_max_array[max].append(array_to_pd[x3].max())

            extreme_values.append([symbol_intersection[x], pd.DataFrame(
                min_max_array[min]).min().values, pd.DataFrame(min_max_array[max]).max().values])


        start_moment = datetime.combine(date_30_ago.date(), time.min)
        end_moment = datetime.combine(today.date(), time.max)
        # next_moment = datetime.combine(date_7_forward , time(16, 30, 00))
        next_moment = datetime.combine(date_7_forward , time.min)
   
        print('opar',{'extreme': extreme_values, 'start': start_moment, 'end': end_moment, 'next': next_moment})
    


    return {'extreme': extreme_values, 'start': start_moment, 'end': end_moment, 'next': next_moment}