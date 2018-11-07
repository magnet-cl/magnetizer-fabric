# -*- coding: utf-8 -*-

from fabric.api import run
from fabric.api import task
from fabric.colors import green
from fabric.contrib.files import append
from fabric.contrib.files import exists
from fabric.operations import prompt


@task
def install():
    """Install pyenv"""
    if exists('.pyenv'):
        print(green('pyenv already installed'))
        if prompt('Check for updates?', default='yes') in ('yes', 'Y', 'y'):
            cmd = 'cd .pyenv && git pull'
            run(cmd)
    else:
        print(green('Cloning pyenv'))
        cmd = 'git clone https://github.com/pyenv/pyenv.git ~/.pyenv'
        run(cmd)

    print(green('Defining environment variables for pyenv'))
    append('.zshrc', 'export PYENV_ROOT="$HOME/.pyenv"')
    append('.zshrc', 'export PATH="$PYENV_ROOT/bin:$PATH"')
    append('.zshrc', 'eval "$(pyenv init -)"')


@task
def update():
    """Update pyenv"""
    print(green('Checking if pyenv is installed'))
    if exists('.pyenv'):
        print(green('Updating pyenv'))
        run('cd .pyenv && git pull')
    else:
        install()
