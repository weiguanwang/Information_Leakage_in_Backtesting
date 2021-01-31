import getpass
import os
import sys
import pandas as pd

from pandas.tseries.offsets import BDay

if getpass.getuser() in ['Weiguan', 'weiguan']:
    if sys.platform == 'win32':
        DATA_DIR = 'C:\\Users\\Weiguan\\Dropbox\\Research\\01_DeepHedging\\Data_OK\\' 
    if sys.platform == 'linux':
        DATA_DIR = '/home/weiguan/Dropbox/Research/DeepHedging/Data/'
if getpass.getuser() in ['rufj']:
        DATA_DIR = '/Users/rufj/Desktop/Weiguan/Weiguan Data/'

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
if FREQ == '2D':
    DT = 2 / 253.
if FREQ == '5D':
    DT = 5 / 253.    


# Monte Carlo setup
NUM_TEST = 2



""" Permutation """
PERMUTE = True

"""
Fake VIX
"""
VIX = False


    
"""
Data selection in the Load data.
"""
# 'otm' means out-of-money only, 'itm' in the money only, 'both' keep both half
HALF_MONEY = 'otm'
MIN_M, MAX_M = 0.8, 1.5



"""
Network feature choice
"""
#FEATURE_SET = 'normal_feature'
FEATURE_SET = 'delta_vega'
#FEATURE_SET = 'delta_vega_vanna'



"""
Set result folder
"""
res_dir = f'{DATA_DIR}Result/CONFIG={CONFIG}/FREQ={FREQ}_HALFMONEY={HALF_MONEY}_MINM={MIN_M}_MAXM={MAX_M}_Permute={PERMUTE}_VIX={VIX}/'

