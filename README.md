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

J. Ruf and W. Wang (2021b), Information leakage in backtesting. SSRN 3836631. Download at https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3836631

**Supplementary reading:**

J. Ruf and W. Wang (2021), Hedging with linear regressions and neural networks, SSRN 3580132, 2021. Forthcoming in the *Journal of Business and Economic Statistics*. Download at https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3580132
    

J. Ruf and W. Wang (2020a), Neural networks for option pricing and hedging: A literature review, *Journal of Computational Finance*, volume 24, number 1, pages 1-45. Download at  https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3486363

## Introduction

This code reproduces the results in the paper Ruf and Wang 2021b “Information leakage in backtesting”. It works on two datasets, the simulated data under the Black-Scholes model and real-world S&P 500 data obtained from OptionMetrics. 

This code repo comes with two folder: `code` and `data`. The “data” folder contains the saved ANN weights that one can use to reproduce our results if one does not want to train the ANNs by himself. Otherwise, change the `TRAIN_BY_YOURSELF` parameter in the `setup.py` to True. 

To use the code for the simulation data, one can run the `run.sh`  script in a Linux-like shell from the directory `code`.  The resulting notebooks in HTML format, Figure 2 of our paper, and all intermediate CSV files will appear in `results/BlackScholes` folder. Users can also execute notebooks one-by-one without using the shell script.

The `run_OptionMetrics.sh` is used for the S&P 500 data. However, one needs to download raw data from providers and put into `data/OptionMetrics/RawData` folder before running the shell script; see [Data folder structure](#Data-folder-structure) for managing file names. We are not able to provide this raw data since it is a commercial one. The resulting notebooks in HTML format, Figure 3 of our paper, and all intermediate CSV files will appear in `results/OptionMetrics` folder.

In the following, we explain in more detail the organisation of the code and data folders.

## Code structure

The code consists of three subfolders. They are `libaray`, `Simulation`, and `OptionMetrics`. The `library` folder contains functions used by other parts of the code. The `library` consists of:

1. `bs.py` : This file contains a function used to simulate the Black-Scholes dataset.
2. `cleaner_aux.py`: This file contains functions used to clean raw data.
3. `common.py` : This file contains functions that calculate and inspect the hedging error.
4. `loader_aux.py` : This file contains functions used to load clean data (before training the ANN or linear regressions).
5. `network.py` : This file implements HedgeNet and auxiliary functions.
6. `plot.py`: This file contains functions used to plot diagnostic figures. 
7. `regression_aux.py`: This file contains functions that implement the linear regression methods.
8. `simulation.py`: This file contains functions that implement the CBOE rules, and organize data.
9.  `vix.py`: This file contains the function that simulates an Ornstein-Uhlenbeck  process, used as the fake VIX feature.



In each of the other two folder, there are two python files that are used by other notebooks:

1. `setup.py`: This file contains all the flags to configure experiments. It varies by datasets, and contains two major configurations:
   1. It specifies the hedging period, time window size, data cleaning choice, and other experimental setup.
   2. It specifies the location of raw data, clean data, and the stored results.
2.  `Load_Clean_aux.py` loads the clean data and implements some extra cleaning, before running linear regressions or ANNs.

The notebooks have a very similar structure as follows:

1. In the simulation folder, the first notebook implements the data simulation. In the OptionMetrics folder, the first notebook implements the cleaning of the historical raw dataset downloaded from data providers. 
2. `2_Regression_Generate.ipynb` implements all linear regressions on sensitivities and stores the PNL (MSHE) files.
4. `3_Network.ipynb` implements the training of the ANN and stores the PNL files (MSHE of ANN).
5. `4_Permute_VIX_Analysis.ipynb` implements the analysis of permutation and fake VIX experiments. The implementation of the experiment is done in notebook 2 and 4, by giving the corresponding setup flags. 

## Data folder structure

Before running the code, one needs to specify the directory that stores the simulation data, (or historical data) and the results. This is done by overwriting the `DATA_DIR` variable in each of the `setup.py` file. 

The data folders  have two common subfolders,

1. `CleanData`: It stores the simulated data in case of Black-Scholes data, or cleaned data generated by `1_Clean.ipynb` in case of historical data.
2. `Result`: It store the PNL files and other auxiliary files, either from the linear regressions or ANN. They also include  tables made by `5_Diagnostic.ipynb`. For the ANN, it additionally contains loss plots, checkpoints, etc. For the linear regression, it additionally contains regression coefficients, standard errors, etc.

For the historical dataset, there is an extra folder `RawData` to store data given by data providers. Data needs to be arranged and renamed in the following way for the code to run.

- For the S\&P 500 data. There are 4 files:

  1. `option_price.csv` contains option quotes downloaded from OptionMetrics. 

  2. `spx500.csv` contains the close-of-day price of S\&P 500. 

  3. `onr.csv` contains the overnight LIBOR rate downloaded from Bloomberg.

  4. `interest_rate.csv` contains the interest rate derived from zero-coupon bond for maturity larger than 7 days, downloaded from OptionMetrics.

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

