#!/usr/bin/env bash

function print_green(){
    echo -e "\033[32m$1\033[39m"
}

print_green 'pre-requisites installation'

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    sudo apt-get update
    sudo apt-get install -y openssh-server
    sudo apt-get install -y python-dev
    sudo apt-get install -y python-pip
    sudo apt-get install -y aptitude
    sudo apt-get install -y libssl-dev

elif [[ "$OSTYPE" == "darwin"* ]]; then
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew install python
fi

print_green 'update pip'
sudo -H pip install -U pip

print_green 'update setuptools'
sudo -H pip install -U setuptools

print_green 'fabric installation through pip'
sudo -H pip install -U fabric fabtools

print_green 'list the available commands'
fab -l
