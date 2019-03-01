# -*- coding: utf-8 -*-

# fabric
from fabric.api import sudo
from fabric.api import task
from fabric.colors import green

# fabtools
from fabtools import deb
from fabtools.deb import update_index

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


@task
def upgrade_client():
    """Upgrade certbot client"""
    # update apt index
    update_index(quiet=False)

    cmd = 'apt-get install --only-upgrade python-certbot-nginx'
    sudo(cmd)

    print(green('Certbot successfully upgraded.'))


@task
def remove_vulnerable_validation():
    """Remove vulnerable validations from renewal configuration"""
    cmd = (
        "sed -i.bak -e 's/^\(pref_challs.*\)tls-sni-01\(.*\)/\1http-01\2/g' "
        "/etc/letsencrypt/renewal/*; rm -f /etc/letsencrypt/renewal/*.bak"
    )
    sudo(cmd, shell_escape=False)


@task
def renew_certificate(dry_run=True):
    """Renew certificate"""
    cmd = 'certbot renew'
    if dry_run:
        cmd = '{} --dry-run'.format(cmd)

    sudo(cmd)
