from fabric.api import task, run
from fabric.contrib.files import append

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
def add_user(user):
    cmd = 'adduser %s' % user
    run(cmd)


def mkdir_ssh():
    """ Helper method to make the ssh directory with proper permissions. """
    cmd = 'mkdir -p -m 0700 .ssh'
    run(cmd)
