from fabric.api import task, sudo
from fabric.colors import green
from fabric.contrib.files import uncomment
from fabtools import deb

from fabfile import utils


@task
def install_passenger():
    """ Installs nginx with passenger support """

    # add pgp key
    print(green('Adding PGP key'))
    deb.add_apt_key(keyid='561F9B9CAC40B2F7', keyserver='keyserver.ubuntu.com')

    # add https support for apt
    utils.deb.install('apt-transport-https')

    # ubuntu 12.04 (precise)
    cmd = ('echo "deb https://oss-binaries.phusionpassenger.com/apt/passenger '
           'precise main" > /etc/apt/sources.list.d/passenger.list')
    sudo(cmd)
    cmd = 'sudo chmod 600 /etc/apt/sources.list.d/passenger.list'
    sudo(cmd)

    # update apt index
    deb.update_index(quiet=False)

    print(green('Installing nginx and passenger'))
    utils.deb.install('nginx-full')
    utils.deb.install('passenger')

    print(green('Activating passenger'))
    uncomment('/etc/nginx/nginx.conf', 'passenger_root', use_sudo=True)
    uncomment('/etc/nginx/nginx.conf', 'passenger_ruby', use_sudo=True)
