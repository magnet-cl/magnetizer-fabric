#!/usr/bin/env bash

# pre-requisites installation
sudo apt-get update
sudo apt-get install -y openssh-server
sudo apt-get install -y python-dev
sudo apt-get install -y python-pip

# update pip
sudo pip install -U pip

# update setuptools
sudo pip install -U setuptools

# fabric installation through pip
sudo pip install -U fabric fabtools

# list the available commands
fab -l
