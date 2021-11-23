import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import numpy as np


def most_recent_ema_position(forex_pair, n_of_bars, periods):
    # connect to MetaTrader 5
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    future_date = datetime(2022, 9, 30)
    rates_m1 = pd.DataFrame(mt5.copy_rates_from(forex_pair, mt5.TIMEFRAME_M1, future_date, n_of_bars))
    rates_m5 = pd.DataFrame(mt5.copy_rates_from(forex_pair, mt5.TIMEFRAME_M5, future_date, n_of_bars))
    rates_m15 = pd.DataFrame(mt5.copy_rates_from(forex_pair, mt5.TIMEFRAME_M15, future_date, n_of_bars))
    rates_m30 = pd.DataFrame(mt5.copy_rates_from(forex_pair, mt5.TIMEFRAME_M30, future_date, n_of_bars))
    rates_h1 = pd.DataFrame(mt5.copy_rates_from(forex_pair, mt5.TIMEFRAME_H1, future_date, n_of_bars))
    rates_h4 = pd.DataFrame(mt5.copy_rates_from(forex_pair, mt5.TIMEFRAME_H4, future_date, n_of_bars))
    rates_d1 = pd.DataFrame(mt5.copy_rates_from(forex_pair, mt5.TIMEFRAME_D1, future_date, n_of_bars))
    rates_w1 = pd.DataFrame(mt5.copy_rates_from(forex_pair, mt5.TIMEFRAME_W1, future_date, n_of_bars))
    rates_mn1 = pd.DataFrame(mt5.copy_rates_from(forex_pair, mt5.TIMEFRAME_MN1, future_date, n_of_bars))

    mt5.shutdown()

    def ema_calculation(period, data):
        K = 2 / (period + 1)
        ema_list = []
        for i in range(len(data)):
            if i == 0:
                ema_now = data[0]
            else:
                close = data[i]
                ema_previous = ema_now
                ema_now = (close * K) + (ema_previous * (1 - K))
            ema_list.append(ema_now)
        return ema_list

    rates_m1 = pd.DataFrame(rates_m1)
    rates_m5 = pd.DataFrame(rates_m5)
    rates_m15 = pd.DataFrame(rates_m15)
    rates_m30 = pd.DataFrame(rates_m30)
    rates_h1 = pd.DataFrame(rates_h1)
    rates_h4 = pd.DataFrame(rates_h4)
    rates_d1 = pd.DataFrame(rates_d1)
    rates_w1 = pd.DataFrame(rates_w1)
    rates_mn1 = pd.DataFrame(rates_mn1)

    ema_50_m1 = ema_calculation(periods["m1_m5_m15"][0], rates_m1['close'])
    ema_200_m1 = ema_calculation(periods["m1_m5_m15"][1], rates_m1['close'])

    ema_50_m5 = ema_calculation(periods["m1_m5_m15"][0], rates_m5['close'])
    ema_200_m5 = ema_calculation(periods["m1_m5_m15"][1], rates_m5['close'])

    ema_50_m15 = ema_calculation(periods["m1_m5_m15"][0], rates_m15['close'])
    ema_200_m15 = ema_calculation(periods["m1_m5_m15"][1], rates_m15['close'])

    ema_50_m30 = ema_calculation(periods["m30_h1_h4"][0], rates_m30['close'])
    ema_200_m30 = ema_calculation(periods["m30_h1_h4"][1], rates_m30['close'])

    ema_50_h1 = ema_calculation(periods["m30_h1_h4"][0], rates_h1['close'])
    ema_200_h1 = ema_calculation(periods["m30_h1_h4"][1], rates_h1['close'])

    ema_50_h4 = ema_calculation(periods["m30_h1_h4"][0], rates_h4['close'])
    ema_200_h4 = ema_calculation(periods["m30_h1_h4"][1], rates_h4['close'])

    ema_8_d1 = ema_calculation(periods["d1_w1_mn1"][0], rates_d1['close'])
    ema_21_d1 = ema_calculation(periods["d1_w1_mn1"][1], rates_d1['close'])

    ema_8_w1 = ema_calculation(periods["d1_w1_mn1"][0], rates_w1['close'])
    ema_21_w1 = ema_calculation(periods["d1_w1_mn1"][1], rates_w1['close'])

    ema_8_mn1 = ema_calculation(periods["d1_w1_mn1"][0], rates_mn1['close'])
    ema_21_mn1 = ema_calculation(periods["d1_w1_mn1"][1], rates_mn1['close'])

    eurusd_all_timeframes_ema = [ema_50_m1[-1], ema_200_m1[-1], ema_50_m5[-1], ema_200_m5[-1], ema_50_m15[-1],
                                 ema_200_m15[-1], ema_50_m30[-1], ema_200_m30[-1], ema_50_h1[-1], ema_200_h1[-1],
                                 ema_50_h4[-1], ema_200_h4[-1], ema_8_d1[-1], ema_21_d1[-1], ema_8_w1[-1],
                                 ema_21_w1[-1], ema_8_mn1[-1], ema_21_mn1[-1]]
    return eurusd_all_timeframes_ema


def produce_binary_map(pairs, periods):
    binary = [2] * 9
    n_of_bars = 10 
    for idx, pair in enumerate(pairs):
        print('loading ' + pair)
        color_map = []
        all_timeframes_ema = most_recent_ema_position(pair, n_of_bars, periods)

        for i in range(len(all_timeframes_ema)):
            if i % 2 == 0:
                if all_timeframes_ema[i] > all_timeframes_ema[i + 1]:
                    k = 1
                else:
                    k = 0
                color_map.append(k)
        binary = np.vstack([binary, color_map])

    return binary