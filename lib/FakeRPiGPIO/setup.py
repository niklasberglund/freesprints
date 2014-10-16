#!/usr/bin/python 

#from distutils.core import setup
from setuptools import setup, find_packages

setup (
    name = 'FakeRPi.GPIO',
    description = "Simulating RPi.GPIO",
    author = "Niklas Berglund",
    author_email = "niklas.berglund@gmail.com",
    version = '1.0.0',
    packages = find_packages()
    )
