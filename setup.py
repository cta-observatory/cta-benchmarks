#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import setuptools

import ctabench

setuptools.setup(name='ctabench',
      version=ctabench.__version__,
      description="library for CTA benchmarks",
      # these should be minimum list of what is needed to run
      packages=setuptools.find_packages(),
      install_requires=['ctapipe==0.8.0',
                        'seaborn',
                        'pandas',
                        ],
      tests_require=['pytest'],
      author='',
      author_email='',
      license='',
      url='https://github.com/cta-observatory/cta-benchmarks',
      long_description=open('README.md').read(),
      )
