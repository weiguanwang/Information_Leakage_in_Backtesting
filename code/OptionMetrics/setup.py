import getpass
import sys
import os
import numpy as np
import pandas as pd

from pandas.tseries.offsets import BDay


TRAIN_BY_YOURSELF = False

DATA_DIR = '../../results/OptionMetrics/'
CKP_DIR = '../../data/OptionMetrics/checkpoints/'
RAW_DATA_DIR = '../../data/OptionMetrics/RawData/'

os.makedirs(DATA_DIR, exist_ok=True)

RANDOM_SEED = 600


""" Dictionary of offsets for data preparation """
OFFSET_DICT = {
    '1D': [BDay(1), '_1D'],
    '2D': [BDay(2), '_2D'],
    '5D': [BDay(5), '_5D']
}

VIXPARAS = {
    'vix0': 13,
    'kappa': 1,
    'sigma': 25,
    'mu': 15
}

# normalized prices with this factor
NORM_FACTOR = 100.


# Choose hedge time frequency.
# this is the gap between current and next time stamp.
# Choose 1 for daily, 5 for weekly. Business day convention.
FREQ = '1D'
if FREQ == '1D':    
    DT = 1 / 253.
   

"""
Choose how to fill in the missing implied vol and greeks.
"""
FEED_MISSING = 'replace_missing'



""" Choose to remove samples for which tomorrow's volume is also zero """
REMOVE_TMR_ZERO_VOLUME = False  # set to false as default


# Rolling window setup
DATE_BEGIN = pd.Timestamp('2010-01-01')
DATE_END = pd.Timestamp('2019-06-27')

span_train = '720D'
span_val = '180D'
span_test = '180D'
date_window = '180D'



SPAN_TRAIN = pd.Timedelta(span_train)
SPAN_VAL = pd.Timedelta(span_val)
SPAN_TEST = pd.Timedelta(span_test)
DATE_WINDOW = pd.Timedelta(date_window)


""" choose in-the-money or out-of-money, or both. """
# 'otm' means out-of-money only, 'itm' in the money only, 'both' keep both half
HALF_MONEY = 'otm'
MIN_M, MAX_M = 0.8, 1.5


MIN_TAU_Days = 0
MIN_TAU = MIN_TAU_Days / 253.

# Permuate training and test set.
PERMUTE = False
NUM_PERMUTE = 1 #5

# Add VIX
VIX = True


    
"""
Network related paras
"""

# Output activation function.
OUTACT = 'linear'

# Network feature choice
FEATURE_SET = 'delta_vega'

# Hyper parameters tuning
NUM_PERIOD_END = 4
NUM_REPEATS = 5



