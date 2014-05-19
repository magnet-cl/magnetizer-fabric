from fabric.api import put
from fabric.api import run
from fabric.api import task
from fabric.colors import green
from fabric.contrib.files import append
from fabric.contrib.files import contains
from fabric.contrib.files import sed
from fabtools import service

import os

ROOT_FOLDER = os.path.dirname(__file__)


@task
def generate_key(output_file='.ssh/id_rsa'):
    """ Generates a ssh-key. """
    mkdir_ssh()
    cmd = 'ssh-keygen -t rsa -f %s' % output_file
    run(cmd)


@task
def add_authorized_key(pub_key_file='.ssh/id_rsa.pub'):
    """ Adds local ssh pub key to remote authorized keys. """
    mkdir_ssh()
    pub_key = open('%s/%s' % (os.path.expanduser('~'), pub_key_file))
    append('~/.ssh/authorized_keys', pub_key)


@task
def generate_config_file():
    """
    Using the template 'fabfile/templates/ssh_config' file, this new command
    replaces the ~/.ssh/config_magnet file in the target server and touches
    the ./.ssh/config_local file. Then it merges them in the ./.ssh/config
    file.
    """

    put('{}/templates/ssh_config'.format(ROOT_FOLDER), '~/.ssh/config_magnet')
    run('touch ~/.ssh/config_local')
    run('cat ~/.ssh/config_local ~/.ssh/config_magnet > ~/.ssh/config')


@task
def disable_password_authentication():
    """ Disables password authentication. """

    configuration_file = '/etc/ssh/sshd_config'

    # ensure pubkey authentication is enabled
    if not contains(configuration_file, '^PubkeyAuthentication yes',
                    escape=False):
        # patterns
        before = '^#?PubkeyAuthentication.*$'
        after = 'PubkeyAuthentication yes'

        sed(configuration_file, before, after, use_sudo=True)

        print(green('Pubkey authentication enabled.'))
    else:
        print(green('Pubkey authentication already enabled.'))

    # disable password authentication
    if not contains(configuration_file, '^PasswordAuthentication no',
                    escape=False):
        # patterns
        before = '^#?PasswordAuthentication.*$'
        after = 'PasswordAuthentication no'

        sed(configuration_file, before, after, use_sudo=True)

        print(green('Password authentication disabled.'))
    else:
        print(green('Password authentication already disabled.'))


@task
def disable_root_login():
    """ Disables root login authentication over SSH. """
    configuration_file = '/etc/ssh/sshd_config'

    if not contains(configuration_file, '^PermitRootLogin no',
                    escape=False):
        # patterns
        before = '^#?PermitRootLogin.*$'
        after = 'PermitRootLogin no'

        sed(configuration_file, before, after, use_sudo=True)

        print(green('Root login disabled.'))
    else:
        print(green('Root login already disabled.'))


@task
def reload_configuration():
    """ Reloads SSH configuration. """
    service.reload('ssh')


@task
def services_handshake():
    """ Handshakes with Github and Bitbucket. """
    services = ['github.com', 'bitbucket.org']

    for service in services:
        run('ssh-keyscan -t rsa {} >> ~/.ssh/known_hosts'.format(service))


def mkdir_ssh():
    """ Helper method to make the ssh directory with proper permissions. """
    cmd = 'mkdir -p -m 0700 .ssh'
    run(cmd)
