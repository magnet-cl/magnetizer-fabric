#!/usr/bin/env bash

# pre-requisites installation
sudo apt-get update
sudo apt-get install -y openssh-server
sudo apt-get install -y python-dev
sudo apt-get install -y python-pip
sudo apt-get install -y aptitude

# update pip
sudo -H pip install -U pip

# update setuptools
sudo -H pip install -U setuptools

# fabric installation through pip
sudo -H pip install -U fabric fabtools

# list the available commands
fab -l
