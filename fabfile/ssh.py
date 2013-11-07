from fabric.api import task, run, sudo
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
def add_user(user=None, sudo=False):

    if user is None:
        print "User not found. Example: ssh.add_user:<username>"
        return

    run('adduser %s' % user)

    if sudo:
        run('adduser %s sudo' % user)


@task
def sudo_without_password():
    """
    Changes the configuration of sudoers file to avoid asking
    the password to members of the sudoers group
    """
    # replace the configuration
    search = "%sudo\tALL=(ALL\:ALL)\ ALL"
    replace = "%sudo ALL=(ALL) NOPASSWD: ALL"
    sed_over_sudoers(search, replace)


@task
def sudo_with_password():
    """
    Changes the configuration of sudoers file to avoid asking
    the password to members of the sudoers group
    """
    # replace the configuration
    search = "%sudo\ ALL=(ALL)\ NOPASSWD\:\ ALL"
    replace = "%sudo\tALL=(ALL:ALL) ALL"
    sed_over_sudoers(search, replace)


def sed_over_sudoers(search, replace):
    """
    runs the sed command over the sudoers file, making backups to
    avoid problems
    """
    # back up the configuration
    sudo("cp /etc/sudoers /etc/sudoers.bak")
    sudo("cp /etc/sudoers /etc/sudoers.tmp")

    # change the permissions on the sudoers.tmp file
    sudo("chmod 0640 /etc/sudoers.tmp")

    # replace the configuration
    cmd = 'sed -i "s/%s/%s/g" /etc/sudoers.tmp' % (search, replace)
    sudo(cmd)

    # restore permissions
    sudo("chmod 0440 /etc/sudoers.tmp")

    # restore sudoers file
    sudo("mv /etc/sudoers.tmp /etc/sudoers")


def mkdir_ssh():
    """ Helper method to make the ssh directory with proper permissions. """
    cmd = 'mkdir -p -m 0700 .ssh'
    run(cmd)
