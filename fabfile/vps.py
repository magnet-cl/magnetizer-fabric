# limit fabric namespace
__all__ = ['init', 'install_utils']

from fabric.api import env
from fabric.api import task
from fabric.colors import blue

from fabfile import admin
from fabfile import node
from fabfile import postgresql
from fabfile import ssh
from fabfile import vim
from fabfile import zsh


@task
def init(admin_user='magnet'):
    """ Initial tasks for the setup of the VPS """

    print(blue('set user to root'))
    env.user = 'root'

    print(blue('add the magnet user with sudo permissions'))
    admin.add_user(admin_user, 'sudo')

    print(blue('allow sudoers without password'))
    admin.sudo_without_password()

    print(blue('disable password authentication over ssh'))
    ssh.disable_password_authentication()

    print(blue('disable root login over ssh'))
    ssh.disable_root_login()

    print(blue('change environment user to the admin_user'))
    env.user = admin_user

    print(blue("add public ssh key to magnet's authorized keys"))
    ssh.add_authorized_key()

    print(blue('reload ssh configuration'))
    ssh.reload_configuration()

    print(blue('upgrade installed packages'))
    admin.full_upgrade()

    print(blue('timezone configuration'))
    admin.configure_timezone()

    print(blue('NTP installation and configuration'))
    admin.install_ntp()

    print(blue('add swap partition'))
    admin.add_swap()


@task
def install_utils(admin_user='magnet'):
    """ Installs utilities on the target VPS """

    print(blue('set target user: {}'.format(admin_user)))
    env.user = admin_user

    print(blue('github and bitbucket ssh handshake'))
    ssh.services_handshake()

    print(blue('zsh installation'))
    zsh.install()

    print(blue('vim installation'))
    vim.install()

    print(blue('postgreSQL installation and role creation'))
    postgresql.install()
    postgresql.create_user()

    print(blue('nodejs installation'))
    node.install()
