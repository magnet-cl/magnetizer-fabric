#!/usr/bin/env bash

# pre-requisites installation
sudo apt-get update
sudo apt-get install -y openssh-server
sudo apt-get install -y python-pip

# fabric installation through pip
sudo pip install fabric

# list the available commands
fab -l
