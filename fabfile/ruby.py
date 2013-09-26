from fabric.api import task, run, prefix
from fabric.colors import green, red
from fabric.contrib.files import exists, append
from fabtools.deb import update_index
from re import search

import utils


@task
def install():
    """ Installs and configures ruby 1.9.3 """
    # update apt index
    update_index(quiet=False)

    # rvm requirements
    dependencies = ['build-essential', 'openssl', 'libreadline6',
                    'libreadline6-dev', 'curl', 'git-core', 'zlib1g',
                    'zlib1g-dev', 'libssl-dev', 'libyaml-dev',
                    'libsqlite3-dev', 'sqlite3', 'libxml2-dev', 'libxslt-dev',
                    'autoconf', 'libc6-dev', 'ncurses-dev', 'automake',
                    'libtool', 'bison', 'subversion', 'pkg-config']
    for dependency in dependencies:
        utils._deb.install(dependency)

    # rvm installation
    cmd = 'curl -L https://get.rvm.io | bash -s stable'
    run(cmd)

    # rvm path added depending on the shell
    rvm_path = 'source "$HOME/.rvm/scripts/rvm"'
    cmd = 'echo $SHELL'
    shell = run(cmd)
    if search('zsh', shell):
        if exists('.zshrc'):
            print(green('Adding rvm to .zshrc'))
            append('.zshrc', rvm_path)
    elif search('bash', shell):
        if exists('.bashrc'):
            print(green('Adding rvm to .bashrc'))
            append('.bashrc', rvm_path)
    else:
        print(red('Shell not supported'))

    # ruby installation
    with prefix(rvm_path):
        cmd = 'rvm autolibs enable'
        run(cmd)
        cmd = 'rvm install ruby-1.9.3'
        run(cmd)
        cmd = 'rvm use 1.9.3'
        run(cmd)


@task
def install_rails():
    """ Installs rails. """

    if exists('.rvm/scripts/rvm'):
        rvm_path = 'source "$HOME/.rvm/scripts/rvm"'
        with prefix(rvm_path):
            cmd = 'gem install --no-rdoc --no-ri rails'
            run(cmd)
    else:
        print(red('Ruby is not installed, please run "ruby.install" first.'))


@task
def install_wirble():
    """ Installs wirble, irb console enhancer. """

    if exists('.rvm/scripts/rvm'):
        rvm_path = 'source "$HOME/.rvm/scripts/rvm"'
        with prefix(rvm_path):
            cmd = 'gem install --no-rdoc --no-ri wirble'
            run(cmd)

        if not exists('.irbrc'):
            cmd = 'touch .irbrc'
            run(cmd)

        wirble_configuration = ("require 'rubygems'\n"
                                "require 'wirble'\n"
                                "Wirble.init\n"
                                "Wirble.colorize")

        append('.irbrc', wirble_configuration)

    else:
        print(red('Ruby is not installed, please run "ruby.install" first.'))
