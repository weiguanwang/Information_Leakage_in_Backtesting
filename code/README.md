# README	
- [README](#readme)
  - [Contact and citation](#contact-and-citation)
  - [Introduction](#introduction)
  - [Code structure](#code-structure)
  - [Data folder structure](#data-folder-structure)
  - [Package information](#package-information)


## Contact and citation

**Authors and affiliations:**

Johannes Ruf [j.ruf@lse.ac.uk](), http://www.maths.lse.ac.uk/Personal/jruf/, London School of Economics and Political Science

Weiguan Wang [weiguanwang@outlook.com](), https://weiguanwang.github.io/, Shanghai University

29 April 2021

**Suggested citation:**

J. Ruf and W. Wang (2021b), Information Leakage in Backtesting. SSRN 3836631. Download at https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3836631

**Supplementary reading:**

J. Ruf and W. Wang (2021), Hedging with linear regressions and neural networks, SSRN 3580132, 2021. Forthcoming in the *Journal of Business & Economic Statistics*. Download at https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3580132
    

J. Ruf and W. Wang (2020a), Neural networks for option pricing and hedging: A literature review, *Journal of Computational Finance*, volume 24, number 1, pages 1-45. Download at  https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3486363

## Introduction

This code reproduces the results in Ruf and Wang (2021b) "Information leakage in backtesting". It covers two datasets, simulated data under the Black-Scholes model and real-world S&P 500 data obtained from OptionMetrics. 

This code repository comes with two folders: `code` and `data`. The ``data`` folder contains the trained artificial neural networks (ANNs). They can be used to reproduce the paper's results. The code also allows to train the ANNs again. In order to do so, change the `TRAIN_BY_YOURSELF` parameter in the `setup.py` to `True`. 

To use the code for the simulation data, one can run the `run.sh`  script in a Linux-like shell from the directory `code`.  The resulting notebooks in HTML format, Figure 2 of the paper, and all intermediate CSV files will appear in the `results/BlackScholes` folder. Users can also execute notebooks one-by-one without using the shell script.

The real-world data experiment requires  raw data from OptionMetrics. We are not able to provide this raw data due to its commercial nature.  They can be obtained from Wharton Research Data Services. Within the OptionMetrics subscription, one can then download the relevant data. To query option prices, one needs to access "Ivy DB US - Option Prices", choose the Date Range "2010 to 2019", Company Code "SECID 108105", Option Type "Both", Exercise Style "European", Security Type "Index", Query Variables "All", Output Fromat "comma-delimited text (*.csv)", Date Format "YYMMDDs10. (e.g. 1984/07/25)", and then click `Submit Query`. To obtain the files for the S&P 500 price, one instead goes to "Ivy DB US - Security - Security Prices" and chooses the same Date Range, Company Code, Query Variables, and Query Output. To obtain interest rates, one goes to “"Ivy DB US - Market - Zero Coupon Yield Curve" and choose the same Date Range, Query Variables, and Query Output. These data then need to be put into the `data/OptionMetrics/RawData` folder before running the shell script; see [Data folder structure](#Data-folder-structure) for managing file names.

After obtaining the OptionMetrics data, the file`run_OptionMetrics.sh` is used for the S&P 500 data. The resulting notebooks in HTML format, Figure 3 in the paper, and all intermediate CSV files will appear in the `results/OptionMetrics` folder.

In the following, we explain in more detail the organisation of the code and data folders.

## Code structure

The code consists of three subfolders. They are `libaray`, `Simulation`, and `OptionMetrics`. The `library` folder contains auxiliary tools in the following files:

1. `bs.py`:  tools to simulate the Black-Scholes dataset.
2. `cleaner_aux.py:  tools to clean raw data.
3. `common.py`:  tools to calculate and inspect the hedging error.
4. `loader_aux.py`:  tools to load clean data (before training the ANNs or the linear regressions).
5. `network.py`: tools to implement HedgeNet and auxiliary tools.
6. `plot.py`:  tools to plot diagnostic figures. 
7. `regression_aux.py`:  tools to implement the linear regressions.
8. `simulation.py`:  tools to implement the CBOE rules for option generation and to organise the simulated data.
9.  `vix.py`: tools to simulate an Ornstein-Uhlenbeck  process, used as the fake VIX feature.



In each of the other two folders, there are two Python files that are used by other notebooks:

1. `setup.py` contains flags to configure the experiments.
2.  `Load_Clean_aux.py` loads the clean data and implements some extra cleaning, before running the linear regressions and ANNs.

The notebooks in both folders have a similar structure:

1. In the ``Simulation`` folder, the first notebook implements the data simulation. In the ``OptionMetrics` folder, the first notebook implements the cleaning of the raw dataset. 
2. `2_Regression_Generate.ipynb` implements the linear regressions on sensitivities and stores the PNL (MSHE) files.
3. `3_Network.ipynb` implements the training of the ANNs and stores the PNL files (MSHE of ANNs).
4. `4_Permute_VIX_Analysis.ipynb` implements the analysis of permutation and fake VIX experiments. The implementation of the experiment is done in notebooks 2 and 4, by giving the corresponding setup flags. 

## Data folder structure

Before running the code, one needs to specify the directory that stores the simulation data (or historical data) and the results. This is done by overwriting the `DATA_DIR` variable in each of the `setup.py` file. 

The data folders have two common subfolders:

1. `CleanData` either stores the simulated data or the cleaned data generated by `1_Clean.ipynb` in case of using real-world data.
2. `Result` stores the PNL (MSHE) files and other auxiliary files, either from the linear regressions or from the ANNs. They also include  tables created by `5_Diagnostic.ipynb`. For the ANNs, it additionally contains loss plots, checkpoints, etc. For the linear regressions, it additionally contains regression coefficients, standard errors, etc.

For the historical dataset, there is an extra folder `RawData` to store the historical real-world data. Data needs to be arranged and renamed in the following way for the code to run.

1. `option_price.csv` contains option quotes, downloaded from OptionMetrics. 

2. `spx500.csv` contains the close-of-day price of S\&P 500, downloaded from OptionMetrics. 

3. `onr.csv` contains the overnight LIBOR rates downloaded from Bloomberg.

4. `interest_rate.csv` contains the interest rate derived from zero-coupon bond for maturity larger than 7 days, downloaded from OptionMetrics.

Comment: The results are not sensitive with respect to the interest rates used. If Bloomberg is not available, other data sources can also be used. The ``onr.csv`` file used by us has three columns named `date`, ``rate``, and `days`. For each of the days between 04/01/2010 and 31/12/2019 we have one row. Rates are given in percentage terms (e.g., the second column has the entry 1.54263 on 31/12/2019). The third column has always entry 1.

   

## Known issues

1. We use business day convention when counting and offsetting days, where business days consist of all weekdays. However, the stock/option trading days are a subset of  business days due to the existence of certain public holidays. For instance, Martin Luther King Day is not a trading day on the Chicago Board Option Exchange, where the S\&P 500 options are traded.  The current code does not take this difference into account, and hence unnecessarily removes samples when it cannot obtain the stock/option price at the end of a hedging period. This problem has no significant impact for the results and conclusions presented here as it only reduces the sample size, and only by a miniscule amount.

2. We use continuous compounding in this code for computing the single-period return on the risk-free asset. However, Equation (1) in our paper uses simple compounding. We admits this inconsistency, but it will only change the results by a miniscule amount. 

We thank Yiren Wu and Max Yang for reporting these two issues to us.

## Package information

| Package      | Version |
| ------------ | ------- |
| Python       | 3.7     |
| Numpy        | 1.19  |
| Pandas       | 1.2 |
| Scikit-learn | 0.24  |
| Scipy        | 1.6   |
| Seaborn      | 0.11    |
| Tensorflow   | 2.4     |

