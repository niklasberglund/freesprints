#!/usr/bin/python 

from distutils.core import setup

setup (name = 'FSMenu',
          description = "Pygame menu module",
          author = "Niklas Berglund",
          author_email = "niklas.berglund@gmail.com",
          version = '1.0.0',
          packages = [
              'FSMenu',
              'FakeRPiGPIO'
              ]
              
        )
