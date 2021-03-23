#!/bin/bash

# Execute all the notebook and convert them to html


jupyter nbconvert --to html --execute Benchmarks/DL1/*.ipynb

cp Benchmarks/DL1/*.html .