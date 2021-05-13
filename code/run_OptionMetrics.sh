#!/bin/bash
set -ex

# Render the notebook to HTML
jupyter nbconvert --ExecutePreprocessor.allow_errors=True --ExecutePreprocessor.timeout=-1 --output-dir=../results/OptionMetrics/ --to='html' --execute OptionMetrics/1_Clean.ipynb

jupyter nbconvert --ExecutePreprocessor.allow_errors=True --ExecutePreprocessor.timeout=-1 --output-dir=../results/OptionMetrics/ --to='html' --execute OptionMetrics/2_Regression_Generate.ipynb

jupyter nbconvert --ExecutePreprocessor.allow_errors=True --ExecutePreprocessor.timeout=-1 --output-dir=../results/OptionMetrics/ --to='html' --execute OptionMetrics/3_Network.ipynb

jupyter nbconvert --ExecutePreprocessor.allow_errors=True --ExecutePreprocessor.timeout=-1 --output-dir=../results/OptionMetrics/ --to='html' --execute OptionMetrics/4_Permute_VIX_Analysis.ipynb