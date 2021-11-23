import MetaTrader5 as mt5
import statistics
from datetime import datetime as dt


m = 50

def volatility(forex_pair):

    rates_m15 = mt5.copy_rates_from(forex_pair, mt5.TIMEFRAME_M15, dt(2022, 9, 23), m)

    volat = statistics.stdev(rates_m15['close'])
    return volat


def last(fx_pair):
    rates_m15_last = mt5.copy_rates_from(fx_pair, mt5.TIMEFRAME_M15, dt(2022, 1, 28), 1)
    rates_last = rates_m15_last['close']
    return rates_last


def percent_of_last(pairs_v):
    all_volatility_list = []
    percent_last = []
    for i in range(len(pairs_v)):
        volatility_m15 = volatility(pairs_v[i])
        all_volatility_list.append(volatility_m15)
        percent = 100 * volatility_m15/last(pairs_v[i])
        percent_last.append(percent)
    return percent_last


def all_volatility(pairs_a_v):
    all_volatility_list = []

    for i in range(len(pairs_a_v)):
        volatility_m15 = volatility(pairs_a_v[i])
        all_volatility_list.append(volatility_m15)

    return all_volatility_list