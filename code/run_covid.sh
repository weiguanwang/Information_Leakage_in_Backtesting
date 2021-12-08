#!/bin/bash
set -ex

# Render the notebook to HTML
jupyter nbconvert --ExecutePreprocessor.allow_errors=True --ExecutePreprocessor.timeout=-1 --output-dir=../results/Covid/ --to='html' --execute Covid/owid-covid.ipynb
