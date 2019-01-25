# cta-benchmarks
Collection of benchmarking code for cta

# Setup

This software uses the Anaconda python distribution, which must be
installed first.


## 1. Create benchmark environment:

```sh
conda env create --file environment.yml
```

This will install ctapipe and dependencies needed to run the benchmarks. This only needs to be done once. 

## 2. Change to the benchmark 

```sh
conda activate cta-benchmarks
```

This must be done every time you open a new terminal


## 3. Run the benchmarks:

```sh
python build.py
```

This will run all notebooks in each of the following directories in order:

* Preparation/
* Benchmarks/
* Summaries/

The output will be in a directory called `BUILD/`

