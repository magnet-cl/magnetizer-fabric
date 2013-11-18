from fabric.api import run
from fabric.api import task
from fabric.colors import green
from fabric.contrib.files import append
from fabric.contrib.files import contains
from fabric.contrib.files import sed
from fabtools import service

from os.path import expanduser


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
    pub_key = open('%s/%s' % (expanduser('~'), pub_key_file))
    append('~/.ssh/authorized_keys', pub_key)


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

    # reload configuration
    service.reload('ssh')


def mkdir_ssh():
    """ Helper method to make the ssh directory with proper permissions. """
    cmd = 'mkdir -p -m 0700 .ssh'
    run(cmd)
