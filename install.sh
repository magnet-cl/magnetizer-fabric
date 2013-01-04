#!/usr/bin/env bash

# pre-requisites installation
sudo apt-get install --assume-yes openssh-server
sudo apt-get install --assume-yes python-pip

# fabric installation through pip
sudo pip install fabric

# list the available commands
fab -l
