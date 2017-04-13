#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='iPlant Backend',
    version='0.1.0',
    description='iPlant backend',
    long_description=readme,
    author='Juan Insuasti',
    author_email='juan.insuasti@gmail.com',
    url='https://github.com/locke189/iplant-backend',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
