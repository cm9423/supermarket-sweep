from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import MetaTrader5 as mt5
import volatility_calculator as vc
import binary_from_ema as bfe

def main():
    no_of_pairs = 0
    default_periods = None

    currency_pairs = ["GBPUSDme", "EURUSDme", "EURGBPme", "USDJPYme",
                    "GBPJPYme", "USDCHFme", "AUDCADme", "EURJPYme",
                    "NZDUSDme", "AUDUSDme", "USDCADme"]
                    
    while no_of_pairs < 1 or no_of_pairs > 11:
        try:
            no_of_pairs = int(input('How many pairs would you like to sweep? (1-11) '))
        except ValueError:
            print("please insert an integer between 1 and 11")

    currency_pairs = currency_pairs[:no_of_pairs]

    while default_periods != 'y' and default_periods != 'n':
        default_periods = input('Would you like default EMA periods? (y/n) ')

    if default_periods == 'y':
        m1_m5_m15_period = [50, 200]
        m30_h1_h4_period = [50, 200]
        d1_w1_mn1_period = [8, 21]

    elif default_periods == 'n':
        m1_m5_m15_period = list(map(int, input("\nInput M1, M5, M15 EMA periods : ").strip().split()))[:2]
        m30_h1_h4_period = list(map(int, input("\nInput M30, H1, H4 EMA periods : ").strip().split()))[:2]
        d1_w1_mn1_period = list(map(int, input("\nInput D1, W1, MN1 EMA periods : ").strip().split()))[:2]

        m1_m5_m15_period.sort()
        m30_h1_h4_period.sort()
        d1_w1_mn1_period.sort()


    periods = {"m1_m5_m15":m1_m5_m15_period,
                "m30_h1_h4":m30_h1_h4_period,
                "d1_w1_mn1":d1_w1_mn1_period}

    # connect to MetaTrader 5
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()



    total = vc.all_volatility(currency_pairs)

    pcent = vc.percent_of_last(currency_pairs)

    pcent = list(np.around(np.array(pcent), 4))

    jpy_indexes = [idx for idx, element in enumerate(currency_pairs) if 'JPY' in element]

    total_in_pips = [i * 10000 for i in total]  # changing from decimal to pips
    for idx in jpy_indexes:
        total_in_pips[idx] = total_in_pips[idx]/100

    total_in_pips = list(np.around(np.array(total_in_pips), 1))  # Volatility in pips

    pairs = currency_pairs
    full_color_map = bfe.produce_binary_map(pairs, periods)
    full_color_map = np.delete(full_color_map, 0, 0)
    dct = {0: 8.5, 1: 5., 2: 10}

    m = [[dct[i] for i in j] for j in full_color_map]

    timeframes = ["M1", "M5", "M15",
                "M30", "H1", "H4", "D1", "W1", "MN1"]

    fig, ax = plt.subplots()
    im = ax.imshow(full_color_map)
    plt.imshow(m, cmap='nipy_spectral', vmin=1, vmax=10)
    ax.set_xticks(np.arange(len(timeframes)))
    ax.set_yticks(np.arange(len(pairs)))
    ax.set_xticklabels(timeframes)
    plt.setp(ax.get_yticklabels(), rotation=30, ha="left", position=(-0.18, 0),
                rotation_mode="anchor")
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right",
                rotation_mode="anchor")

    yticks = [i+0.5 for i, _ in enumerate(pairs)]
    xticks = [i+0.5 for i, _ in enumerate(timeframes)]
    ax.set_yticks(yticks, minor=False)
    ax.set_xticks(xticks, minor=True)
    ax.yaxis.grid(True, which='major')
    ax.xaxis.grid(True, which='minor')

    ax.set_yticklabels(pairs)

    ax.set_title("Supermarket Sweep\n")
    for idx, pair in enumerate(pairs):
        print(f"{pair} M15 Volatility: {str(total_in_pips[idx])} pips, {str(float(pcent[idx]))}%")

    plt.show()

    mt5.shutdown()

if __name__ == '__main__':
    main()