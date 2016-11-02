""" tasks related to the configuration of virtual servers """
from fabric.api import env
from fabric.api import run
from fabric.api import task
from fabric.colors import blue

from fabfile import admin
from fabfile import node
from fabfile import postgresql
from fabfile import ruby
from fabfile import ssh
from fabfile import utils
from fabfile import vim
from fabfile import zsh

# limit fabric namespace
__all__ = ['init', 'install_utils', 'muni_setup', 'wordpress_setup']


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

    print(blue('set log level to verbose'))
    ssh.set_log_level()

    print(blue('change environment user to the admin_user'))
    env.user = admin_user

    print(blue("add public ssh key to magnet's authorized keys"))
    ssh.add_authorized_key()

    print(blue('reload ssh configuration'))
    ssh.reload_configuration()

    print(blue('upgrade installed packages'))
    admin.full_upgrade(ask_confirmation=False)

    print(blue('timezone configuration'))
    admin.configure_timezone()

    print(blue('NTP installation and configuration'))
    admin.install_ntp()

    print(blue('add swap partition'))
    admin.add_swap()

    print(blue('generate SSH key'))
    ssh.generate_key()

    print(blue('set default locale'))
    admin.set_default_locale()


@task
def install_utils(admin_user='magnet'):
    """ Installs utilities on the target VPS """

    print(blue('set target user: {}'.format(admin_user)))
    env.user = admin_user

    print(blue('curl, htop, git'))
    utils.deb.install('curl')
    utils.deb.install('htop')
    utils.deb.install('git')

    print(blue('github and bitbucket ssh handshake'))
    ssh.services_handshake()

    print(blue('zsh installation'))
    zsh.install()

    print(blue('nodejs installation'))
    node.install()

    print(blue('vim installation'))
    vim.install()

    print(blue('postgreSQL installation and role creation'))
    postgresql.install()
    postgresql.create_user()


@task
def muni_setup():
    """ Installs utilities on the target VPS with a muni flavor"""

    print(blue('Add your own public key to authorized hosts'))
    ssh.add_authorized_key()

    print(blue('Generate the ssh config file to connect to all magnet hosts'))
    ssh.generate_config_file()

    print(blue('upgrade installed packages'))
    admin.full_upgrade(ask_confirmation=False)

    print(blue('NTP installation and configuration'))
    admin.install_ntp()

    install_utils(run('whoami'))

    print(blue('install vim-gtk'))
    utils.deb.install('vim-gtk')

    print(blue('install zsh theme: powerline'))
    zsh.install_theme('powerline')

    print(blue('install ruby'))
    ruby.install()

    print(blue('install rails'))
    ruby.install_rails()

    print(blue('install git-smart'))
    run('gem install git-smart')

    print(blue('install zsh muni flavor'))
    zsh.install_flavor('muni')


@task
def wordpress_setup():
    """ Installs utilities on the target VPS with a Wordpress flavor"""

    print(blue('initial setup'))
    init()

    print(blue('github and bitbucket ssh handshake'))
    ssh.services_handshake()

    print(blue('zsh installation'))
    zsh.install()

    print(blue('vim installation'))
    vim.install()

    print(blue('git', 'curl, htop'))
    utils.deb.install('git')
    utils.deb.install('curl')
    utils.deb.install('htop')
