# -*- coding: utf-8 -*-

# standard library
import os

# fabric
from fabric.api import sudo
from fabric.api import task
from fabric.colors import cyan
from fabric.colors import green
from fabric.colors import red
from fabric.contrib.files import upload_template

# fabtools
from fabtools import deb

from fabfile import ssh
from fabfile import utils
from fabfile import vim
from fabfile import zsh

ROOT_FOLDER = os.path.dirname(__file__)

#
# limit fabric namespace
__all__ = [
    'initial_setup', 'install', 'configure_nginx', 'enable_ssl'
]


@task
def initial_setup():
    """ Installs basic utilities """
    print(green('curl, htop, git, tig'))
    utils.deb.install('curl')
    utils.deb.install('htop')
    utils.deb.install('git')
    utils.deb.install('tig')

    print(green('github and bitbucket ssh handshake'))
    ssh.services_handshake()

    print(green('zsh installation'))
    zsh.install()

    print(green('vim installation'))
    vim.install()


@task
def install():
    """ Installs Odoo Community Edition 10 """
    # update apt index
    deb.update_index(quiet=False)

    print(green('Adding odoo key'))
    cmd = 'wget -O - https://nightly.odoo.com/odoo.key | apt-key add -'
    sudo(cmd)

    print(green('Adding source to APT'))
    cmd = (
        'echo "deb http://nightly.odoo.com/10.0/nightly/deb/ ./" >> '
        '/etc/apt/sources.list.d/odoo.list'
    )
    sudo(cmd)

    # update apt index
    deb.update_index(quiet=False)

    print(green('Installing odoo'))
    utils.deb.install('odoo')

    print(green('The configuration file can be found at ' +
                cyan('/etc/odoo/odoo.conf')))


@task
def configure_nginx(domain=None):
    """ Installs and configures an nginx site proxy """
    if not domain:
        print(red('A domain must be specified'))
        exit()

    print(green('Installing nginx'))
    utils.deb.install('nginx')

    print(green('Uploading site for nginx'))
    site_file = 'odoo_nginx_site.conf'
    site_file_path = '{}/templates/{}'.format(ROOT_FOLDER, site_file)
    target_dir = '/etc/nginx/sites-available/'
    context = {
        'domain': domain,
    }
    upload_template(site_file_path, target_dir, context=context,
                    use_sudo=True)

    # change config file owner to root
    cmd = 'chown root:root {}{}'.format(target_dir, site_file)
    sudo(cmd)

    print(green('Enabling site'))
    cmd = (
        'ln -s /etc/nginx/sites-available/{} '
        '/etc/nginx/sites-enabled/'.format(site_file)
    )
    sudo(cmd)

    print(cyan('You must check other enabled sites and restart nginx'))


@task
def enable_ssl():
    """ Gets a SSL certificate (certbot) and enables odoo proxy mode """
    from fabfile import certbot

    print(green('Installing letsencrypt certbot'))
    certbot.install()

    print(green('Getting ssl certificate'))
    certbot.get_certificate()

    print(green('Enabling proxy mode'))
    cmd = 'echo "proxy_mode = True" >> /etc/odoo/odoo.conf'
    sudo(cmd)

    print(green('Restarting Odoo'))
    cmd = 'systemctl restart odoo'
    sudo(cmd)
