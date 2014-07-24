# limit fabric namespace
__all__ = ['init', 'install_utils']

from fabric.api import env
from fabric.api import task

from fabfile import admin
from fabfile import node
from fabfile import postgresql
from fabfile import ssh
from fabfile import vim
from fabfile import zsh


@task
def init(admin_user='magnet'):
    """ Initial tasks for the setup of the VPS """

    # set user to root
    env.user = 'root'

    # add the magnet user with sudo permissions
    admin.add_user(admin_user, 'sudo')

    # allow sudoers without password
    admin.sudo_without_password()

    # disable password authentication over ssh
    ssh.disable_password_authentication()

    # disable root login over ssh
    ssh.disable_root_login()

    # change environment user to the admin_user
    env.user = admin_user

    # add public ssh key to magnet's authorized keys
    ssh.add_authorized_key()

    # reload ssh configuration
    ssh.reload_configuration()


@task
def install_utils(admin_user='magnet'):
    """ Installs utilities on the target VPS """

    # set target user
    env.user = admin_user

    # github and bitbucket ssh handshake
    ssh.services_handshake()

    # zsh installation
    zsh.install()

    # vim installation
    vim.install()

    # postgreSQL installation and role creation
    postgresql.install()
    postgresql.create_user()

    # nodejs installation
    node.install()
