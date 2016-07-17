# -*- coding: utf-8 -*-

# standard library
import os
import re

# fabric
from fabric.api import get
from fabric.api import local
from fabric.api import put
from fabric.api import run
from fabric.api import sudo
from fabric.api import task
from fabric.colors import blue
from fabric.colors import green
from fabric.colors import red
from fabric.contrib.files import append
from fabric.contrib.files import contains
from fabric.contrib.files import sed

# fabtools
from fabtools import service
from fabtools.deb import update_index

ROOT_FOLDER = os.path.dirname(__file__)


@task
def generate_key(output_file='.ssh/id_rsa'):
    """ Generates a ssh-key. """
    mkdir_ssh()
    cmd = 'ssh-keygen -t rsa -f %s' % output_file
    run(cmd)


@task
def add_authorized_key(pub_key_file='.ssh/id_rsa.pub', key_name=None):
    """
    Adds local ssh pub key to remote authorized keys.

    Example: Add muni.pub key on keygen to magnet time server

        $ fab ssh.add_authorized_key:key_name=muni.pub -H time
    """
    mkdir_ssh()

    if key_name:
        repo = 'git@bitbucket.org/magnet-cl/keygen.git'

        local('git archive --remote=ssh://{} master {} | tar -x'.format(
            repo, key_name)
        )

        pub_key = open(key_name)
        append('~/.ssh/authorized_keys', pub_key)
        local('rm {}'.format(key_name))
    else:
        pub_key = open('%s/%s' % (os.path.expanduser('~'), pub_key_file))
        append('~/.ssh/authorized_keys', pub_key)


@task
def generate_config_file():
    """
    Generates an ssh_config file by merging a local config file with a remote
    file on a private repository.

    """
    repository = 'git@bitbucket.org/magnet-cl/keygen.git'
    remote_config_file = 'ssh_config'

    print(green('Getting remote configuration file'))
    local('git archive --remote=ssh://{} master {} | tar -x'.format(
        repository, remote_config_file)
    )
    remote_config = open(remote_config_file)

    print(green('Merging configuration files into ~/.ssh/config'))
    put(remote_config, '~/.ssh/config_magnet')
    run('touch ~/.ssh/config_local')
    run('cat ~/.ssh/config_local ~/.ssh/config_magnet > ~/.ssh/config')

    # cleanup
    remote_config.close()
    local('rm {}'.format(remote_config_file))


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

    for ser in services:
        run('ssh-keyscan -t rsa {} >> ~/.ssh/known_hosts'.format(ser))


@task
def upgrade_server():
    """ Helper method to upgrade the SSH server """

    # update apt index
    update_index(quiet=False)

    cmd = 'apt-get install --only-upgrade openssh-server'
    sudo(cmd)

    print(green('SSH server successfully upgraded.'))


def mkdir_ssh():
    """ Helper method to make the ssh directory with proper permissions. """
    cmd = 'mkdir -p -m 0700 .ssh'
    run(cmd)


@task
def list_authorized_keys(remote_keys=None):
    """ List the authorized keys on the remote host """
    remote_keys_path = get_authorized_keys()

    local('cat {}'.format(remote_keys_path))


@task
def get_authorized_keys(remote_keys_path=None):
    """ Gets the authorized keys file """
    if not remote_keys_path:
        remote_keys_path = '~/.ssh/authorized_keys'

    print(green('Getting the remote list.'))
    return get(remote_keys_path)[0]


@task
def list_authorized_keys_of_magnet(remote_keys_path=None):
    """
    List the authorized keys on the remote host matching against the keys on
    the magnet's keygen repository.

    """
    if not remote_keys_path:
        remote_keys_path = '~/.ssh/authorized_keys'

    repo = 'git@bitbucket.org/magnet-cl/keygen.git'
    tmp_path = '.tmp_keygen'

    print(green('Getting keys from magnet keygen'))
    local('mkdir -p {}'.format(tmp_path))
    local('git archive --remote=ssh://{} master | tar -x -C {}'.format(
        repo, tmp_path))

    authorized = []

    remote_keys = get_authorized_keys(remote_keys_path)

    print(green('Checking keys...'))
    for filename in os.listdir(tmp_path):
        if filename.endswith('.pub'):
            filepath = '{}/{}'.format(tmp_path, filename)
            with open(filepath, 'r') as key_file:
                if is_key_authorized(key_file.read(), remote_keys):
                    authorized.append(filename)

    print(green('Authorized keys (magnet): '))
    for key in authorized:
        print(blue(key))

    # compare the number of magnet keys with the total keys
    with open(remote_keys, 'r') as remote_keys_file:
        remote_keys_count = len(re.findall('ssh-rsa', remote_keys_file.read()))
        other_keys_count = remote_keys_count - len(authorized)
    if other_keys_count > 0:
        print(red("Non-magnet authorized keys: {}".format(other_keys_count)))

    print(green('Cleaning temporary files.'))
    cmd = 'rm -rf {}'.format(tmp_path)
    local(cmd)


def is_key_authorized(key_file, remote_keys):
    """ Checks if the given key content is authorized on the remote keys """
    with open(remote_keys, 'r') as remote_keys_file:
        remote_keys_content = remote_keys_file.read()
        if key_file in remote_keys_content:
            return True
        else:
            return False


@task
def set_log_level(level='VERBOSE'):
    """ Sets the ssh server log level """
    configuration_file = '/etc/ssh/sshd_config'

    # patterns
    before = '^LogLevel .*$'
    after = 'LogLevel {}'.format(level)

    sed(configuration_file, before, after, use_sudo=True)

    print(green('Log level set to: {}'.format(level)))
