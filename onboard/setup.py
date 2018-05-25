#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='rscsp.onboard',
    version='0.9.0',
    description='GPIO wrapper module for devices on KP-RSCSP sensor board',
    author='Kyohritsu Electronic Industry Co., Ltd.',
    author_email='wonderkit@keic.jp',
    install_requires=['RPi.GPIO'],
    url='https://github.com/kyohritsu/KP-RSCSP',
    packages=['rscsp'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Hardware',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
