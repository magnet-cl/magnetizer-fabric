# fabric
from fabric.api import sudo
from fabric.api import task
from fabric.colors import green
from fabric.contrib.files import uncomment
from fabric.operations import prompt

# fabtools
from fabtools import deb
from fabtools import service

from fabfile import utils


@task
def install_passenger():
    """ Installs nginx with passenger support """

    # add pgp key
    print(green('Adding PGP key'))
    deb.add_apt_key(keyid='561F9B9CAC40B2F7', keyserver='keyserver.ubuntu.com')

    # add https support for apt
    utils.deb.install('apt-transport-https')

    # We obtain the Ubuntu version name
    print 'You need to specify the Ubuntu version'
    p_t = 'Do you wish to see the version names?'
    p_r = prompt(p_t, default='yes')
    if (p_r == 'yes'):
        print('12.04 -> ' + green('Precise', True) + ' Pangolin')
        print('12.10 -> ' + green('Quantal', True) + ' Quetzal')
        print('13.04 -> ' + green('Raring', True) + ' Ringtail')
        print('13.10 -> ' + green('Saucy', True) + ' Salamander')
        print('14.04 -> ' + green('Trusty', True) + ' Thar')
    p_t = 'What version are you deploying to? (only first name needed)'
    version = prompt(p_t, default='Trusty')
    version = version.lower()

    # ubuntu 12.04 (precise)
    cmd = ('echo "deb https://oss-binaries.phusionpassenger.com/apt/passenger '
           + version + ' main" > /etc/apt/sources.list.d/passenger.list')
    sudo(cmd)
    cmd = 'sudo chmod 644 /etc/apt/sources.list.d/passenger.list'
    sudo(cmd)

    # update apt index
    deb.update_index(quiet=False)

    print(green('Installing nginx and passenger'))
    utils.deb.install('nginx-full')
    utils.deb.install('passenger')

    print(green('Activating passenger'))
    uncomment('/etc/nginx/nginx.conf', 'passenger_root', use_sudo=True)
    uncomment('/etc/nginx/nginx.conf', 'passenger_ruby', use_sudo=True)


@task
def enable_gzip():
    """ Enables gzip compression """

    uncomment('/etc/nginx/nginx.conf', 'gzip_types', use_sudo=True)
    service.reload('nginx')
