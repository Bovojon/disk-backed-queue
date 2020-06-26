#!/usr/bin/python

"""Copyright (c) 2018 Classify & Process Inc."""

import setuptools

with open('requirements.txt') as f:
    REQUIREMENTS = f.read().splitlines()

setuptools.setup(
    name='take_home',
    version='0.1.0',
    install_requires=REQUIREMENTS,
    packages=setuptools.find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    zip_safe=False,
    entry_points='',
)
