# cta-benchmarks
Collection of benchmarking code for cta

Note that currently these benchmarks require some input data that is
not provided in the repository.  *No data files should be included in
this repo to avoid causing its size to increase rapidly* instead, raw
data files will be provided on a dedicated server, and outputs should
be written locally.

# Guidelines

General:
* Do not commit notebooks to this repo that contain output (please strip the output first). This makes the repo size stay small and makes looking at differences much easier.  The outputs will eventually be included automatically in the documentation, not in the repo. 
* Do not commit input or output data files to this repo (see above)

From [this Netflix post](https://medium.com/netflix-techblog/scheduling-notebooks-348e6c14cfd6):

* **Low Branching Factor**: Keep your notebooks fairly linear. If you have many conditionals or potential execution paths, it becomes hard to ensure end-to-end tests are covering the desired use cases well.
* **Library Functions in Libraries**: If you do end up with complex functions which you might reuse or refactor independently, these are good candidates for a coding library rather than in a notebook. Providing your notebooks in git repositories means you can position shared unit-tested code in that same repository as your notebooks, rather than trying to unit test complex notebooks.
* **Short and Simple is Better**: A notebook which generates lots of useful outputs and visuals with a few simple cells is better than a ten page manual. This makes your notebooks more shareable, understandable, and maintainable.

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


