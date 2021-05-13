import getpass
import os
import sys
import pandas as pd

from pandas.tseries.offsets import BDay

TRAIN_BY_YOURSELF = False

DATA_DIR = '../../results/'
CKP_DIR = '../../data/BlackScholes/checkpoints/'

os.makedirs(DATA_DIR, exist_ok=True)

UNDERLYING_MODEL = 'BS'
CONFIG = '1'

"""
Simulation setup.
"""
DATE_BREAK = pd.Timestamp('2018/07/01') + pd.Timedelta('360D') # 360D
N_ofTestDays = pd.Timedelta('90D') # 90D


DATA_DIR += 'BlackScholes/'
if CONFIG == '1':
    # configuration for paper
    UNDERLYINGPARAS = {
        's0': 2000.,
        'volatility': 0.2,
        'mu': 0.1,
        'start_date': pd.Timestamp('2018/07/01'),
        'end_date': pd.Timestamp('2018/07/01') + pd.Timedelta('450D')
    }   


        
OPTIONPARAS = {
    'threshold': 1,
    'step_K': 5
}

    

VIXPARAS = {
    'vix0': 13,
    'kappa': 1,
    'sigma': 25,
    'mu': 15
}

OTHERPARAS = {
    'short_rate': 0.,
    'norm_factor': 100.
}
""" Dictionary of offsets for data preparation """
OFFSET_DICT = {
    '1D': [BDay(1), '_1D'],
    '2D': [BDay(2), '_2D'],
    '5D': [BDay(5), '_5D']
}

# Samples with option prices less than this threshold will be removed.
THRESHOLD_REMOVE_DATA = 0.01


# this is the gap between current and next time stamp.
# Choose 1 for daily, 5 for weekly. Business day convention.
FREQ = '1D'
if FREQ == '1D':    
    DT = 1 / 253.  


# Monte Carlo setup
NUM_TEST = 20


    
"""
Data selection in the Load data.
"""
# 'otm' means out-of-money only, 'itm' in the money only, 'both' keep both half
HALF_MONEY = 'otm'
MIN_M, MAX_M = 0.8, 1.5






