#!/usr/bin/env python
# coding: utf-8

# In this notebook, we prepare data. The underlying stock price is simulated under the Black-Scholes or Heston model. A set of European options is created with the CBOE rule. We then apply some proper filtering. 

# In[ ]:


import sys
import os
# Append the library path to PYTHONPATH, so library can be imported.
sys.path.append(os.path.dirname(os.getcwd()))
import datetime
import copy

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from library import bs, plot, vix
from library import common as cm
from library import simulation as sim
from library import cleaner_aux as caux


# In[ ]:


get_ipython().run_line_magic('run', 'setup.py')
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

# If you want to run this notebook independent of '0_Generate_Data', you need to set RANDOM_SEED by hand.
# RANDOM_SEED = 200
np.random.seed(RANDOM_SEED)
sns.set(style='darkgrid')


# In[ ]:


def createCleanData(
        strike_per_maturity=None,
        underlying_model=None,
        underlying_paras=None,
        option_paras=None,
        offset_dict=None,
        vix_paras=None,
        other_paras=None,
        making_tests=False
    ):
    if underlying_model == 'BS':
        path = bs.simulate_geometric_bm(underlying_paras)
    else:
        raise NotImplementedError('Underlying type is not implemented!')
    
    options, strike_per_maturity = sim.find_option_seq_jan_cycle(
        path, strike_per_maturity=strike_per_maturity,
        step_K=option_paras['step_K'], threshold=option_paras['threshold']
    )
    print('Number of options: {}'.format(len(options)))
    
    df_call = sim.get_hedge_df(
        options,
        interest_rate=other_paras['short_rate'],
        display=False
    )

    df_call['r'] = df_call['short_rate'].values
    
    vix_path = vix.simulate_fake_vix(vix_paras, underlying_paras['start_date'], underlying_paras['end_date'])
    df_call = df_call.join(vix_path, on='date')
    
    if underlying_model == 'BS':
        df_call['implvol0'] = underlying_paras['volatility']        
        df_call['V0'] = caux.bs_call_price(vol=df_call['implvol0'], 
                                          S=df_call['S0'], 
                                          K=df_call['K'], 
                                          tau=df_call['tau0'], 
                                          r=df_call['r'])    
        df_call['cp_int'] = 0      
        
    else: 
        raise NotImplementedError('Underlying type is not implemented!')
        

    """ 
    Copy before normalizing, add_tomorrow or calculate greeks
    Put prices can be calculate by put-call parity
    implied volatility are the same.
    """
    df_put = df_call.copy()
    df_put['cp_int'] = 1
    df_put['V0'] = (df_call['V0'] - df_call['S0'] 
                    + df_call['K'] * np.exp(-1 * df_call['short_rate'] * df_call['tau0']))

    
    for key, value in OFFSET_DICT.items():
        df_call = caux.add_tomorrow(
            df_call, 
            offset_bday=value[0], offset_key=value[1]
        )
        df_put = caux.add_tomorrow(
            df_put,
            offset_bday=value[0], offset_key=value[1]
        )

                       
    """
    Normalize all prices and different offsets.
    """
    cols_to_normalize = (['S' + value[1] for key, value in offset_dict.items()]
                         + ['V' + value[1] for key, value in offset_dict.items()])
    df_call = caux.normalize_prices(
        df_call,
        s_divisor=df_call['S0'],
        norm_factor=other_paras['norm_factor'],
        cols=['S0', 'V0', 'K'] + cols_to_normalize
    )
    df_put = caux.normalize_prices(
        df_put,
        s_divisor=df_put['S0'],
        norm_factor=other_paras['norm_factor'],
        cols=['S0', 'V0', 'K'] + cols_to_normalize
    )
    
    
    """ Calculate Greeks """
    df_call['delta_bs'] = caux.bs_call_delta(
        vol=df_call['implvol0'], S=df_call['S0_n'], K=df_call['K_n'], tau=df_call['tau0'], r=df_call['r'])    
    df_put['delta_bs'] = caux.bs_put_delta(
        vol=df_put['implvol0'], S=df_put['S0_n'], K=df_put['K_n'], tau=df_put['tau0'], r=df_put['r'])
    
    for df_tmp in [df_call, df_put]:
    
        df_tmp['vega_n'] = caux.bs_vega(
            vol=df_tmp['implvol0'], S=df_tmp['S0_n'], K=df_tmp['K_n'], tau=df_tmp['tau0'], r=df_tmp['r'])
        df_tmp['gamma_n'] = caux.bs_gamma(
            vol=df_tmp['implvol0'], S=df_tmp['S0_n'], K=df_tmp['K_n'], tau=df_tmp['tau0'], r=df_tmp['r'])
        df_tmp['vanna_n'] = caux.bs_vanna(
            vol=df_tmp['implvol0'], S=df_tmp['S0_n'], K=df_tmp['K_n'], tau=df_tmp['tau0'], r=df_tmp['r'])
    
    
    return {'call': df_call, 'put': df_put, 
            'path': path, 'vix_path': vix_path, 
            'strike_per_maturity': strike_per_maturity}


# In[ ]:





# # Generate train and validation set
# We generate a stock path, under the Black-Scholes or Heston. Along this path, a set of European option is generated. With this set of options, we construct a dataframe for the use of hedging. This dataframe is then split into a training sete and a validation set.
# 
# In the dataframe, we calculate the true option prices by the Black-Scholes formula or Heston, and further calculate sensitivities.
# 
# Then, an integer flag for option type is added. Samples with option price less than threshold are removed.

# In[ ]:


paras = {
    'underlying_model': UNDERLYING_MODEL,
    'underlying_paras': UNDERLYINGPARAS,
    'option_paras': OPTIONPARAS,
    'offset_dict': OFFSET_DICT,
    'vix_paras': VIXPARAS,
    'other_paras': OTHERPARAS
}


# In[ ]:


res_dict = createCleanData(strike_per_maturity=None, **paras)
df_call, df_put = res_dict['call'], res_dict['put']
df_call['Is_In_Some_Test'], df_put['Is_In_Some_Test'] = False, False
path, vix_path = res_dict['path'], res_dict['vix_path']
strike_per_maturity = res_dict['strike_per_maturity']


# In[ ]:


total_call, total_put = df_call.shape[0], df_put.shape[0]

df_call = df_call.loc[(df_call['V0'] > THRESHOLD_REMOVE_DATA)]
num_rem_call = total_call - df_call.shape[0]

df_put = df_put.loc[(df_put['V0'] > THRESHOLD_REMOVE_DATA)]
num_rem_put = total_put - df_put.shape[0]

df_both = df_call.append(df_put, ignore_index=True)


# In[ ]:


sub_dir = DATA_DIR + f'CleanData/CONFIG={CONFIG}/'
os.makedirs(sub_dir, exist_ok=True)
df_both.to_csv(sub_dir + 'train_val_sim.csv')


# # Generate Monte Carlo test sets
# As before, we generate a set of options on each Monte Carlo set. Each of the sets gives again a dataframe.

# In[ ]:


under_params = copy.deepcopy(UNDERLYINGPARAS)
plot.plot_stock_test_prices(path, UNDERLYING_MODEL, under_params, 
                                N_ofTestDays, DATE_BREAK, paras['underlying_paras']['end_date'])


# In[ ]:


init_test_value = path.iloc[-1]
init_vix_value = vix_path.iloc[-1]


# In[ ]:


test_start_date = paras['underlying_paras']['end_date']
test_end_date = paras['underlying_paras']['end_date'] + N_ofTestDays


# In[ ]:


paras['underlying_paras']['start_date'] = test_start_date
paras['underlying_paras']['end_date'] = test_end_date
paras['vix_paras']['vix0'] = init_vix_value['fake_vix']

paras['underlying_paras']['s0'] = init_test_value['S0']
if UNDERLYING_MODEL == 'Heston':
    paras['underlying_paras']['v0'] = init_test_value['Var0']


# In[ ]:


sub_dir = DATA_DIR + f'CleanData/CONFIG={CONFIG}/MC/'
os.makedirs(sub_dir, exist_ok=True)

test_sizes = []


# In[ ]:


np.random.seed(2 * RANDOM_SEED)
        
for i in range(NUM_TEST):
    res_dict = createCleanData(making_tests=True, strike_per_maturity=strike_per_maturity, **paras)
    df_call, df_put = res_dict['call'], res_dict['put']
    df_call['Is_In_Some_Test'], df_put['Is_In_Some_Test'] = True, True
    path, vix_path = res_dict['path'], res_dict['vix_path']
    df_call = df_call.loc[(df_call['V0'] > THRESHOLD_REMOVE_DATA)]
    df_put = df_put.loc[(df_put['V0'] > THRESHOLD_REMOVE_DATA)]
    
    df_both = df_call.append(df_put, ignore_index=True)
    

    " Include one-month, ATM options "
    df_both = caux.append_1M_ATM_option(df_both, paras)
    
    
    test_sizes.append(df_both.shape[0])
    df_both.to_csv(sub_dir + 'mc{}.csv'.format(i))


# In[ ]:


with open(f'{DATA_DIR}CleanData/CONFIG={CONFIG}/paras.txt', 'w+') as file:
    for n, x in [
        ('Date and time', datetime.datetime.now()),
    	('Random seed', RANDOM_SEED),
    	('Normalized price', paras['other_paras']['norm_factor']),
    	('Training start date', paras['underlying_paras']['start_date']),
        ('Initial total samples', total_call + total_put),
        ('The number of calls samples removed in training and val, due to threshold', num_rem_call),
        ('The number of puts samples removed in training and val, due to threshold', num_rem_put),
    	('Test start date', test_start_date),
    	('Test end date', test_end_date),
    ]:
        file.write(f'{n} = {x}\n')


# In[ ]:




