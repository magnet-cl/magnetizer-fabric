from fabric.api import sudo
from fabric.api import task
from fabric.colors import green
from fabtools import deb

from fabfile import utils


@task
def install():
    """ Installs Oracle Java JDK """

    print(green('Adding Oracle Java PPA'))
    cmd = 'add-apt-repository -y ppa:webupd8team/java'
    sudo(cmd)

    # update apt index
    deb.update_index(quiet=False)

    # package name
    java_pkg = 'oracle-java7-installer'

    print(green('Accepting Oracle license'))
    debconf_params = {
        'shared/accepted-oracle-license-v1-1': ('select', 'true')
    }
    deb.preseed_package(java_pkg, debconf_params)

    print(green('Installing Oracle Java 1.7'))
    utils.deb.install(java_pkg)
