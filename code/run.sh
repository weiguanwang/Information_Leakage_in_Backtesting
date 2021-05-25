#!/bin/bash
set -ex

# Render the notebook to HTML
jupyter nbconvert --ExecutePreprocessor.allow_errors=True --ExecutePreprocessor.timeout=-1 --output-dir=../results/BlackScholes/ --to='html' --execute Simulation/1_Generate_Data.ipynb

jupyter nbconvert --ExecutePreprocessor.allow_errors=True --ExecutePreprocessor.timeout=-1 --output-dir=../results/BlackScholes/ --to='html' --execute Simulation/2_Regression_Generate.ipynb 
  
jupyter nbconvert --ExecutePreprocessor.allow_errors=True --ExecutePreprocessor.timeout=-1 --output-dir=../results/BlackScholes/ --to='html' --execute Simulation/3_Network.ipynb 

jupyter nbconvert --ExecutePreprocessor.allow_errors=True --ExecutePreprocessor.timeout=-1 --output-dir=../results/BlackScholes/ --to='html' --execute Simulation/4_Permute_VIX_Analysis.ipynb 
