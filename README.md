# cta-benchmarks
Collection of benchmarking code for cta

Note that currently these benchmarks require some input data that is
not provided in the repository.  *No data files should be included in
this repo to avoid causing its size to increase rapidly* instead, raw
data files will be provided on a dedicated server, and outputs should
be written locally.

# Setup for automatic running of all benchmarks:

This software uses the Anaconda python distribution, which must be
installed first.  


## 1. Create benchmark environment:

```sh
conda env create --file environment.yml
```

This will install ctapipe and all dependencies needed to run the benchmarks. This only needs to be done once. 

## 2. Change to the benchmark environment

```sh
conda activate cta-benchmarks
```

This must be done every time you open a new terminal and want to run the benchmarks.


## 3. Run the benchmarks:

```sh
python build.py
```

This will run all notebooks in each of the following directories in order:

* Preparation/
* Benchmarks/
* Summaries/

The output will be in a directory called `BUILD/`


You can of course run each benchmark individually using `jupyter notebook` or `jupyter lab` (the latter requires that you run `conda install jupyter-lab` first)


