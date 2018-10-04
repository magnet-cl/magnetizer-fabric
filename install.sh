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

    sudo apt install software-properties-common python-software-properties
    sudo add-apt-repository ppa:pypa/ppa
    sudo apt update
    sudo apt install pipenv

elif [[ "$OSTYPE" == "darwin"* ]]; then

    print_green "Enable remote login on osx"
    sudo systemsetup -setremotelogin on

    print_green "Check to see if Homebrew is installed, and install it if it is not"
    command -v brew >/dev/null 2>&1 || { echo >&2 "Installing Homebrew Now"; \
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"; }

    print_green "Installing wget" 
    brew install wget

    print_green "Install pyenv to install python 2.7"
    brew install pyenv

    print_green "Install pipenv"
    brew install pipenv

    if [[ -z "${LANG}" ]]; then
        print_green "LANG environment varialbe is not set. Required for pipenv" 
        echo "export LANG=en_US.UTF-8" >> ~/.bash_profile
    fi

    if [[ -z "${LC_ALL}" ]]; then
        print_green "LC_ALL environment varialbe is not set. Required for pipenv" 
        echo "export LC_ALL=en_US.UTF-8" >> ~/.bash_profile
    fi

    source ~/.bash_profile
fi

pipenv install

print_green 'list the available commands'
pipenv run fab -l
