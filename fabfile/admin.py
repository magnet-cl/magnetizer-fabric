from fabric.api import put
from fabric.api import run
from fabric.api import sudo
from fabric.api import task
from fabric.colors import green
from fabric.colors import red
from fabric.colors import blue

from fabtools.deb import update_index
from fabtools.user import exists
from fabtools.user import create

import os

from fabfile import utils

ROOT_FOLDER = os.path.dirname(__file__)


@task
def add_user(user=None, extra_group=None):
    """ Adds user, an extra group can also be specified. """

    if user is None:
        print(red(
            "User not specified. Usage: admin.add_user:<username>,<group>"))
        return

    if not exists(user):
        # the default group created is equal to the user, the extra_group is
        # added only if present
        if extra_group:
            create(name=user, group=user, extra_groups=[extra_group],
                   password=user, shell='/bin/bash')
        else:
            create(name=user, group=user, password=user, shell='/bin/bash')
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


@task
def add_swap(size='2G'):
    """ Adds a swap partition to the system """

    def check_swap():
        # check if the system already has a swap partition
        swap_partitions = run('swapon -s | wc -l')
        if int(swap_partitions) > 1:
            return True

    if check_swap():
        print(green('Swap partition already configured.'))
        return

    # preallocate swapfile
    cmd = 'fallocate -l {} /swapfile'.format(size)
    sudo(cmd)

    # adjust permissions
    cmd = 'chmod 600 /swapfile'
    sudo(cmd)

    # setup swap space
    cmd = 'mkswap /swapfile'
    sudo(cmd)

    # enable swap
    cmd = 'swapon /swapfile'
    sudo(cmd)

    # make the swap file permanent
    fstab_line = '/swapfile   none    swap    sw    0   0'
    cmd = 'echo "{}" >> /etc/fstab'.format(fstab_line)
    sudo(cmd)

    if check_swap():
        print(green('Swap partition successfully configured.'))
    else:
        print(red('The configuration did not work, '
                  'please contact your system administrator.'))


@task
def fix_shellshock():
    """ Upgrades bash in order to avoid the 'shellshock' vulnerability. """

    # update apt index
    update_index(quiet=False)

    cmd = 'apt-get install --only-upgrade bash'
    sudo(cmd)

    print(green('Bash successfully secured.'))


@task
def configure_logrotate(framework=None, skip_installation=False):
    """ Configures logrotate to listen for a given framework

    Frameworks supported:
        django
        rails

    Optionally you can skip the installation of logrotate through the
    skip_installation parameter.

    """

    if not framework:
        print(red('Please specify the framework to configure'))
        print(red('Usage:'))
        print(red('\tfab admin.configure_logrotate:rails'))
        print(red('\tfab admin.configure_logrotate:django'))
        return

    if not utils.arg_to_bool(skip_installation):
        # update apt index
        update_index(quiet=False)

        # install logrotate
        utils.deb.install('logrotate')

    # framework set
    if framework == 'rails':
        config_file = 'magnet-rails'
    elif framework == 'django':
        config_file = 'magnet-django'

        # create logs directory for django apps avoiding logrotate error
        cmd = 'mkdir -p logs'
        run(cmd)
    else:
        print(red('Framework not supported'))
        return

    # upload logrotate config file
    print(blue('Uploading logrotate config file'))
    config_file_path = '{}/templates/{}'.format(ROOT_FOLDER, config_file)
    logrotate_dir = '/etc/logrotate.d/'
    put(config_file_path, logrotate_dir, use_sudo=True, mode=0644)

    # change config file owner to root
    cmd = 'chown root:root {}{}'.format(logrotate_dir, config_file)
    sudo(cmd)

    # activate rotation
    print(blue('Activating logrotate config file'))
    cmd = 'logrotate -v {}{}'.format(logrotate_dir, config_file)
    sudo(cmd)


@task
def configure_timezone(timezone='Etc/UTC'):
    """ Configures the given timezone as system timezone """
    print(blue('Setting "{}" as system timezone').format(timezone))
    cmd = 'echo "{}" > /etc/timezone'.format(timezone)
    sudo(cmd)

    print(blue('Reconfiguring tzdata').format(timezone))
    cmd = 'dpkg-reconfigure --frontend noninteractive tzdata'
    sudo(cmd)
