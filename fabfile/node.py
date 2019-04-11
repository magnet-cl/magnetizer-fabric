# standard library
import platform

# fabric
from fabric.api import sudo
from fabric.api import run
from fabric.api import task
from fabric.colors import green, yellow, cyan
from fabric.contrib.files import exists

from fabtools import deb

from fabfile import utils


@task
def install(version='--lts'):
    """Install Node.js with NVM. Defaults to latest LTS."""

    if run('uname -o', quiet=True) == 'GNU/Linux':
        print(green('Adding support to compile and install native addons'))
        utils.deb.install('build-essential')

    # NVM updates itself if it's already installed,
    # so no need to check if already installed.

    script_file = '__nvm_install.sh'

    download_install_script = (
        'wget -q '      # assume OS X has already installed wget
        '-O {0} '
        'https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh '
        '&& chmod +x {0}'
    ).format(script_file)

    print(green('Installing NVM'))
    run(download_install_script)
    run('./' + script_file)

    # NVM is now instaled. But Fabric runs commands with Bash, so NVM source
    # string is only in .bashrc
    if exists('~/.zshrc'):
        # Add source string to .zshrc too
        run('PROFILE=~/.zshrc ./' + script_file)
    run('rm ' + script_file)

    # run('source ~/.bashrc')
    #   Doesn't work because the default .bashrc contains code that "If not
    #   running interactively, don't do anything".
    #   So manually load it:
    load_nvm = 'export NVM_DIR="$HOME/.nvm" && . "$NVM_DIR/nvm.sh"'
    # run(load_nvm)
    #   Works but it's not persisted to the next run, so run both at the same
    #   time:
    print(green('Installing Node {} with NVM'.format(version)))
    run('{} && nvm install {}'.format(load_nvm, version))
    print(yellow('You must restart open terminals (or source .*rc) to activate ' + cyan('nvm')))


@task
def install_yarn():
    """Install yarn."""

    print(green('Adding gpg key'))
    cmd = 'curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -'
    sudo(cmd)

    print(green('Adding apt repository'))
    cmd = ('echo "deb https://dl.yarnpkg.com/debian/ stable main" | '
           'tee /etc/apt/sources.list.d/yarn.list')
    sudo(cmd)

    # update apt index
    deb.update_index(quiet=False)

    print(green('Installing yarn'))
    utils.deb.install('yarn')
