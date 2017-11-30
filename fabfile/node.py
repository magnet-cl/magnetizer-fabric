from fabric.api import sudo
from fabric.api import task
from fabric.colors import green

from fabtools import deb

from fabfile import utils


@task
def install(version='8'):
    """Install node."""

    print(green('Running script from NodeSource'))
    cmd = 'curl -sL https://deb.nodesource.com/setup_{}.x | bash -'
    cmd = cmd.format(version)
    sudo(cmd)

    print(green('Installing nodejs'))
    utils.deb.install('nodejs', upgrade=True)

    print(green('Adding support to compile and install native addons'))
    utils.deb.install('build-essential')


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
