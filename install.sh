#!/usr/bin/env bash

# pre-requisites installation
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    sudo apt-get update
    sudo apt-get install -y openssh-server
    sudo apt-get install -y python-dev
    sudo apt-get install -y python-pip
    sudo apt-get install -y aptitude
elif [[ "$OSTYPE" == "darwin"* ]]; then
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew install python

    # Enable remote login on osx
    sudo systemsetup -setremotelogin on
fi

# update pip
sudo -H pip install -U pip

# update setuptools
sudo -H pip install -U setuptools

# fabric installation through pip
sudo -H pip install -U fabric fabtools

# list the available commands
fab -l
