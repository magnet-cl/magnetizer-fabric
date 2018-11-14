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
    sudo apt-get install -y libssl-dev

    pip install --user pipenv

elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Check to see if Homebrew is installed, and install it if it is not
    command -v brew >/dev/null 2>&1 || { echo >&2 "Installing Homebrew Now"; \
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"; }

    # install pyenv to install python 2.7
    brew install pyenv

    # install pipenv
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

if [ -d ~/.magnetizer ]; then
    print_green 'updating repository at ~/.magnetizer'
    cd ~/.magnetizer && git pull origin master
else
    print_green 'cloning repository into ~/.magnetizer'
    git clone https://github.com/magnet-cl/magnetizer.git ~/.magnetizer
    git checkout feature/cli  # tmp branch
fi

print_green 'install magnetizer with pipenv'
pipenv install -e .

mkdir -p ~/bin
if [ ! -f ~/bin/magnetizer ]; then
    print_green 'creating symlink for magnetizer at ~/bin/'
    ln -s $(pipenv --venv)/bin/magnetizer ~/bin/
fi

print_green 'spawn a new shell to use "magnetizer" as binary'
