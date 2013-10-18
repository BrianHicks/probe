#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='probe',
    version='0.0.1',
    description='Probe lets you ship personal metrics (feelings, energy level, productivity) to external services for analysis.',
    long_description=readme + '\n\n' + history,
    author='Brian Hicks',
    author_email='brian@brianthicks.com',
    url='https://github.com/BrianHicks/probe',
    packages=[
        'probe',
    ],
    entry_points={
        'console_scripts': [
            'probe = probe.cli:main'
        ]
    },
    package_dir={'probe': 'probe'},
    include_package_data=True,
    install_requires=[
        "pyyaml==3.10",
        "recurrent==0.2.4",
        "python-dateutil==2.1",
    ],
    license="BSD",
    zip_safe=False,
    keywords='probe',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
