import os
import pandas as pd

from pandas.tseries.offsets import BDay

TRAIN_BY_YOURSELF = False

DATA_DIR = '../../results/BlackScholes/'
CKP_DIR = '../../data/BlackScholes/checkpoints/'

os.makedirs(DATA_DIR, exist_ok=True)


# Number of test sets
NUM_TEST = 20
    


"""
Simulation setup.
"""
UNDERLYINGPARAS = {
    's0': 2000.,
    'volatility': 0.2,
    'mu': 0.1,
    'start_date': pd.Timestamp('2018/07/01'),
    'end_date': pd.Timestamp('2018/07/01') + pd.Timedelta('450D')
} 

DATE_BREAK = pd.Timestamp('2018/07/01') + pd.Timedelta('360D') # 360D 
N_ofTestDays = pd.Timedelta('90D') # 90D  






