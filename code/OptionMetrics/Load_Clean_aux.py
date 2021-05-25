import pandas as pd
import numpy as np

import sys
import os
# Append the library path to PYTHONPATH, so library can be imported.
sys.path.append(os.path.dirname(os.getcwd()))
from pandas.tseries.offsets import BDay

from library import common as cm
from library import loader_aux as laux

import setup

# choosing 'otm' means out-of-money only
HALF_MONEY = 'otm'
MIN_M, MAX_M = 0.8, 1.5

MIN_TAU_Days = 0  # minimum time to maturity
MIN_TAU = MIN_TAU_Days / 253.


# Hedging period. 1D for daily hedging.
DT = 1 / 253.


file_dir = setup.DATA_DIR + 'CleanData/'

file_path = f'{file_dir}processed.csv'

df = pd.read_csv(
    file_path, 
    parse_dates=['date', 'exdate', 'last_date'],
    dtype={'cp_flag': 'category', 'cp_int': np.int32},
    index_col=0
)
df = df.reset_index(drop=True)
ori_size = df.shape[0]


"""
We need to decide what implied volatility or greeks to use.
For option metrics data, we replace missing implied vols and greeks with our own calculated greeks.
"""
cols_original = {'implvol0': 'implvol0_o',
        'delta_bs': 'delta_bs_o',
        'vega_n': 'vega_o_n',
        'gamma_n': 'gamma_o_n'}
cols_calculated = {
    'implvol0': 'implvol0_c',
    'delta_bs': 'delta_bs_c',
    'vega_n': 'vega_c_n',
    'gamma_n': 'gamma_c_n'
}
        

bl_replace = df[list(cols_original.values())].isna().max(axis=1) 
for key, value in cols_original.items():
    df[key] = df[value].copy()
    df.loc[bl_replace, key] = df.loc[bl_replace, cols_calculated[key]].copy()
        

df.rename(columns={'vanna_c_n': 'vanna_n'}, inplace=True)        
df['on_ret'] = np.exp(df['short_rate'] * DT)

    
"""
We need to drop quotes where the one-step-ahead prices are not found.
"""
bl = df['V1'].notna()
cm.print_removal(df.shape[0], sum(bl), ori_size, 'We remove samples when the next trade is not available')
df = df.loc[bl]


"""
If we still have NAs for implied volatility at this point of time, we have no way but to drop them. 
"""
bl = df['implvol0'].isna()
if sum(bl) > 0.5:
    print('Check Why implvol is not available!\n\n')
assert df['implvol0'].isna().sum() < 0.5



bl = (df['implvol0'] <= 1.) & (df['implvol0'] >= 0.01)
cm.print_removal(df.shape[0], sum(bl), ori_size, 'We remove unreasonable implvol0')
df = df.loc[bl]


bl = df['tau0'] > MIN_TAU
cm.print_removal(df.shape[0], sum(bl), ori_size, 
                 f'We remove samples that have time to maturity less than {MIN_TAU_Days} day')
df = df.loc[bl]


"""
1. We choose out-of-money calls and puts only.
2. We further restrict the range of moneyness, so that deep out-of-money are excluded.
"""
# To make sure no NAs in columns
assert df['delta_bs'].isna().sum() < 0.5

df = laux.choose_half_shrink_moneyness(df, ori_size, HALF_MONEY, MIN_M, MAX_M)

df = laux.make_features(df)

"""
Rolling window
"""

df, df_dates = laux.rolling_window(
    df,
    date_begin=setup.DATE_BEGIN,
    span_train=setup.SPAN_TRAIN,
    span_val=setup.SPAN_VAL,
    span_test=setup.SPAN_TEST,
    date_window=setup.DATE_WINDOW,
    date_end=setup.DATE_END,
    offset=BDay(1)
)

