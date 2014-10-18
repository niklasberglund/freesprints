#!/bin/bash

cd lib/FSMenu
sudo python2.7 setup.py install

cd ../FakeRPiGPIO
sudo python2.7 setup.py install

sudo pip install rainbow_logging_handler
