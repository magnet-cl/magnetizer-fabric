from fabric.api import sudo
from fabric.api import task
from fabric.colors import green

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
