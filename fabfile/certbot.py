from fabric.api import sudo
from fabric.api import task
from fabric.colors import green
from fabtools import deb

from fabfile import utils


@task
def install():
    """ Installs certbot for nginx """

    # update apt index
    deb.update_index(quiet=False)

    # requirements
    utils.deb.install('software-properties-common')

    print(green('Adding certbot PPA'))
    cmd = 'add-apt-repository -y ppa:certbot/certbot'
    sudo(cmd)

    # update apt index
    deb.update_index(quiet=False)

    print(green('Installing certbot'))
    utils.deb.install('python-certbot-nginx')


@task
def get_certificate():
    """ Gets the certificate and configures nginx """

    cmd = 'certbot --nginx'
    sudo(cmd)
