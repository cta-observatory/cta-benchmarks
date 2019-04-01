# cta-benchmarks
Collection of benchmarking code for cta

[![Build Status](https://travis-ci.org/cta-observatory/cta-benchmarks.svg?branch=master)](https://travis-ci.org/cta-observatory/cta-benchmarks)

Note that the benchmarks require some input data that is
not provided in the repository.  *No data files should be included in
this repo to avoid causing its size to increase rapidly* instead, raw
data files are provided on a dedicated server.

# General Structure

* **Preparation**: notebooks that generate testing data (e.g. process raw data and produce data products that are needed as input for various benchmarks)
* **Benchmarks**: notebooks that perform a certain benchmark. These should produce a final plot or value that can be recorded using the storage functionality of *papermill*
* **Summaries**: notebooks that collect the final results from multiple *Benchmarks* and present an executive summary of the results. 

# Guidelines

General:
* Do not commit notebooks to this repo that contain output (please strip the output first). This makes the repo size stay small and makes looking at differences much easier.  The outputs will eventually be included automatically in the documentation, not in the repo. 
* Do not commit input or output data files to this repo (see above)
* separate the production of benchmark data (e.g. DL1, DL2, or DL3 files) from the benchmarks themselves.  The production of data files should be in notebooks in the `Preparation/` directory (data prep). 

From [this Netflix post](https://medium.com/netflix-techblog/scheduling-notebooks-348e6c14cfd6):

* **Low Branching Factor**: Keep your notebooks fairly linear. If you have many conditionals or potential execution paths, it becomes hard to ensure end-to-end tests are covering the desired use cases well.
* **Library Functions in Libraries**: If you do end up with complex functions which you might reuse or refactor independently, these are good candidates for a coding library rather than in a notebook. Providing your notebooks in git repositories means you can position shared unit-tested code in that same repository as your notebooks, rather than trying to unit test complex notebooks.
* **Short and Simple is Better**: A notebook which generates lots of useful outputs and visuals with a few simple cells is better than a ten page manual. This makes your notebooks more shareable, understandable, and maintainable.

## Submit a benchmark

- You may open an issue to discuss the benchmark you want to create before
- Add your notebook to the relevant folder
- Use the standard input parameters (see below)
- Strip out the outputs : `nbstripout your-awesome-benchmark.ipynb`
- Check that your notebook in running well with `papermill your-awesome-benchmark.ipynb awesome-output.ipynb -f yourparameterfile.yml` and check that `awesome-output.ipynb` looks like what you expect
- Make a pull request

Note: create `yourparameterfile.yml` by copying and modifying `config/parameters_jenkins.yml` to your local data paths.

## Parameterise your notebook

In `cta-benchmarks` with use `papermill` to run parameterized notebooks.
When you create a benchmark, tag a cell with `parameters` (see the [papermill page](https://github.com/nteract/papermill)).
The parameters are global and common to all benchmarks.
Especially:
- the path to raw data directory is given by `input_dir`
- the path to the prepared data (output of the notebooks in `Preparation`) is given by `prepared_data_dir`



## Available data on the running server
(see `config/parameters_jenkins.yml`)

- gamma_diffuse: 'gamma_40deg_0deg_run102___cta-prod3-lapalma3-2147m-LaPalma_cone10.simtel.gz'


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


