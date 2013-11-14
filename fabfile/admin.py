from fabric.api import sudo
from fabric.api import task
from fabric.colors import green
from fabric.colors import red

from fabtools.user import exists
from fabtools.user import create


@task
def add_user(user=None, group=None):
    """ Adds user, group can also be specified. """

    if user is None:
        print(red(
            "User not specified. Usage: admin.add_user:<username>,<group>"))
        return

    if not exists(user):
        create(name=user, group=group, password=user, shell='/bin/bash')
        print(green("User succesfully created."))
    else:
        print(red("User already exists."))


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
