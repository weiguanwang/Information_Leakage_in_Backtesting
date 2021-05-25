import os
import numpy as np
import pandas as pd


TRAIN_BY_YOURSELF = False

DATA_DIR = '../../results/OptionMetrics/'
CKP_DIR = '../../data/OptionMetrics/checkpoints/'
RAW_DATA_DIR = '../../data/OptionMetrics/RawData/'

os.makedirs(DATA_DIR, exist_ok=True)

RANDOM_SEED = 600

# number of permutations
NUM_PERMUTE = 1


# Rolling window setup
DATE_BEGIN = pd.Timestamp('2010-01-01')
DATE_END = pd.Timestamp('2019-06-27')

SPAN_TRAIN = pd.Timedelta('720D')
SPAN_VAL = pd.Timedelta('180D')
SPAN_TEST = pd.Timedelta('180D')
DATE_WINDOW = pd.Timedelta('180D')