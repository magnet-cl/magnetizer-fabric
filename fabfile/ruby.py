from fabric.api import task, run, prefix
from fabric.operations import prompt
from fabric.colors import green, red
from fabric.contrib.files import exists, append
from fabtools.deb import update_index
from re import search

from fabfile import utils


@task
def install():
    """ Installs and configures ruby """
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
        utils.deb.install(dependency)

    # rvm installation
    install_rvm()

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
        install_ruby_version()


@task
def install_rvm():
    run('gpg --keyserver hkp://keys.gnupg.net --recv-keys D39DC0E3')
    cmd = '\curl -sSL https://get.rvm.io | bash -s stable'
    run(cmd)


@task
def install_ruby_version():
    """ Installs a particular ruby version """
    if exists('.rvm/scripts/rvm'):
        rvm_path = 'source "$HOME/.rvm/scripts/rvm"'

        with prefix(rvm_path):
            text = 'You can specify the complete version (e.g. 2.0.0)'
            text += ' in which rvm downloads the latest patch,'
            text += ' or you can define it yourself (e.g. 2.0.0p247)'
            print(text)
            p_t = 'Do you wish to know all installed ruby versions?'
            result = prompt(p_t, default='yes')
            if (result == 'yes'):
                print(green('Currently installed ruby versions:'))
                cmd = 'rvm list'
                run(cmd)

            p_t = 'Do you wish to know all *known* ruby versions rvm supports?'
            result = prompt(p_t, default='yes')
            if (result == 'yes'):
                cmd = 'rvm list known'
                run(cmd)
            rv = prompt('Specify a ruby version', default='2.0.0-p247')
            cmd = 'rvm autolibs enable'
            run(cmd)
            cmd = 'rvm --verify-downloads 1 install ' + rv
            run(cmd)
            cmd = 'rvm use ' + rv
            run(cmd)
            p_t = 'Do you wish to set this version'
            p_t += ' [' + rv + '] as the system\'s default?'
            result = prompt(p_t, default='yes')
            if (result == 'yes'):
                cmd = 'rvm --default use ' + rv
                run(cmd)
    else:
        print(red('Ruby is not installed, please run "ruby.install" first.'))


@task
def install_rails(version=None):
    """ Installs rails. """

    if exists('.rvm/scripts/rvm'):
        rvm_path = 'source "$HOME/.rvm/scripts/rvm"'
        with prefix(rvm_path):
            cmd = 'gem install --no-rdoc --no-ri rails'
            if version:
                cmd = '{} -v {}'.format(cmd, version)
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
