#!/bin/env python
"""
Setuptools file for c20
"""
from setuptools import (
    setup,
    find_packages,
)

setup(
    name='c20',
    author='marhag87',
    author_email='marhag87@gmail.com',
    url='https://github.com/marhag87/c20',
    version='0.1.1',
    packages=find_packages(),
    license='WTFPL',
    description='Calculate value of c20 tokens',
    long_description='A simple module for calculating the value of c20 tokens.',
    install_requires=[
        'requests',
        'pyyamlconfig',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    scripts=['bin/c20'],
)
