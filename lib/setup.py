#!/usr/bin/python 

from distutils.core import setup

setup (
    name = 'FSMenu',
    description = "Menu module for use with Pygame",
    author = "Niklas Berglund",
    author_email = "niklas.berglund@gmail.com",
    version = '1.0.0',
    packages = [
        'FSMenu',
        'FakeRPiGPIO'
        ]      
    )

