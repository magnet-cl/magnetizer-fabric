# -*- coding: utf-8 -*-

# standard library
import os

# fabric
from fabric.api import cd
from fabric.api import env
from fabric.api import prompt
from fabric.api import put
from fabric.api import run
from fabric.api import sudo
from fabric.api import task
from fabric.colors import blue
from fabric.colors import green
from fabric.colors import red
from fabric.contrib.files import append
from fabric.contrib.files import exists as path_exists
from fabric.contrib.files import sed
from fabric.contrib.files import upload_template

# fabtools
from fabtools import cron
from fabtools import service
from fabtools.deb import update_index
from fabtools.user import create
from fabtools.user import exists

from fabfile import utils
from fabfile.git import git_clone
from fabfile.git import git_install
from fabfile.git import git_pull

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
def adjust_swappiness(swappiness=10):
    try:
        parsed_value = int(swappiness)
    except ValueError:
        print(red('Invalid parameter: {}'.format(swappiness)))
        exit()
    else:
        if parsed_value not in range(0, 101):
            print(red('Not in range: [0-100]'))
            exit()

    print(green('Swappiness set to: {}'.format(swappiness)))
    cmd = 'sysctl vm.swappiness={}'.format(swappiness)
    sudo(cmd)

    print(green('Adjusting swappiness permanently'))
    swappiness_setting = 'vm.swappiness={}'.format(swappiness)
    append('/etc/sysctl.conf', swappiness_setting, use_sudo=True)


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


@task
def install_ntp():
    """ Installs and configures the NTP daemon """
    # update apt index
    update_index(quiet=False)

    print(blue('Installing NTP daemon'))
    utils.deb.install('ntp')

    print(blue('Configuring NTP servers to use US pool zone'))
    # patterns
    before = 'ubuntu\.pool\.ntp\.org'
    after = 'us\.pool\.ntp\.org'

    # ntp configuration file
    config_file = '/etc/ntp.conf'
    sed(config_file, before, after, use_sudo=True)

    print(blue('Restarting NTP server'))
    service.restart('ntp')


@task
def full_upgrade(ask_confirmation=True):
    """
    Upgrades installed packages to their most recent version, removing or
    installing packages as necessary.

    """
    # update apt index
    update_index(quiet=False)

    # install aptitude
    utils.deb.install('aptitude')

    # full upgrade
    cmd = 'aptitude full-upgrade'

    if not ask_confirmation:
        cmd = '{} -y'.format(cmd)

    sudo(cmd)


@task
def safe_upgrade():
    """ Upgrades installed packages to their most recent version """
    # update apt index
    update_index(quiet=False)

    # safe upgrade
    cmd = 'aptitude safe-upgrade'
    sudo(cmd)


@task
def install_db_backups_manager():
    """ Installs project py-db-backup """

    if path_exists('py-db-backup'):
        update_manager = prompt(green('DB backups manager already installed. '
                                      'Would you like to update it?'),
                                default='Yes')
        if update_manager in ('Yes', 'yes', 'Y', 'y'):
            with cd('py-db-backup'):
                git_pull()

        return

    # install git if is not available
    git_install()

    print(green('Cloning py-db-backup repository.'))
    git_clone('git://github.com/magnet-cl/py-db-backup.git', 'py-db-backup')

    print(green('Installing py-db-backup'))
    with cd('py-db-backup'):
        cmd = './install.sh'
        run(cmd)


@task
def configure_db_backups_manager(config_file=None):
    """ Generates the config file for the db backups """

    with cd('py-db-backup'):
        # user input
        if not config_file:
            config_file = prompt(green('Please specify the config file name:'),
                                 default='config.ini')
        db_name = prompt(green('Please specify the database name to backup:'))

        # initial config file
        cmd = 'cp config.ini.default {}'.format(config_file)
        run(cmd)

        # replace db name
        before = "^name = .*"
        after = "name = {}".format(db_name)
        sed(config_file, before, after, backup='')

        config_file_path = blue('{}/{}'.format(run('pwd', quiet=True),
                                               config_file))
        print green('If you want to backup on Amazon S3, please set the '
                    'credentials directly on: {}'.format(config_file_path))


@task
def register_db_backup(cron_user='magnet', config_file=None):
    """ Registers a daily db backup on cron """

    script_path = run('pwd', quiet=True)
    script_path = '{}/{}'.format(script_path, 'py-db-backup')
    cron_task = 'cd {} && ./{}'.format(script_path, 'backup-db.py')
    cron_name = 'backup-db'

    if config_file:
        # add the config file argument to cron command
        cron_task = '{} -c {}'.format(cron_task, config_file)
        # add suffix to cron task name based on config_file
        cron_name = '{}-{}'.format(cron_name, os.path.splitext(config_file)[0])

    print(green('Registering cron task at midnight'))
    cron.add_task(cron_name, '@midnight', cron_user, cron_task)

    # change cron task owner to root
    cmd = 'chown root:root {}/{}'.format('/etc/cron.d', cron_name)
    sudo(cmd)


@task
def add_db_backups(cron_user='magnet', config_file=None):
    """ Installs and configures py-db-backup and registers on cron """

    install_db_backups_manager()
    configure_db_backups_manager(config_file)
    register_db_backup(cron_user, config_file)


@task
def install_remote_syslog(version='0.13', port='58173'):
    """ Installs and configures remote_syslog to send events to papertrail """

    package_name = 'remote_syslog_linux_amd64.tar.gz'
    folder = 'remote_syslog'

    url = ('https://github.com/papertrail/remote_syslog2/releases/download/'
           'v{}/{}')
    url = url.format(version, package_name)

    print(blue('Downloading remote syslog'))
    cmd = 'wget {} -O {}'.format(url, package_name)
    run(cmd)

    print(blue('Unpacking remote syslog'))
    cmd = 'tar xvf {}'.format(package_name)
    run(cmd)

    print(blue('Installing remote syslog'))
    cmd = 'cp {}/remote_syslog /usr/local/bin/'.format(folder)
    sudo(cmd)

    print(blue('Uploading config file'))
    config_file = 'remote_syslog.yml'
    config_file_path = '{}/templates/{}'.format(ROOT_FOLDER, config_file)
    target_dir = '/etc/'
    context = {
        'user': env.user,
        'port': port,
    }
    upload_template(config_file_path, target_dir, context=context,
                    use_sudo=True)

    # change config file owner to root
    cmd = 'chown root:root {}{}'.format(target_dir, config_file)
    sudo(cmd)

    print(blue('Registering at system startup'))
    upstart_file = 'remote_syslog.conf'
    upstart_file_path = '{}/templates/{}'.format(ROOT_FOLDER, upstart_file)
    upstart_dir = '/etc/init/'
    put(upstart_file_path, upstart_dir, use_sudo=True, mode=0644)

    # change config file owner to root
    cmd = 'chown root:root {}{}'.format(upstart_dir, upstart_file)
    sudo(cmd)

    service.start('remote_syslog')

    print(blue('Cleaning installation files'))
    cmd = 'rm -rf {} {}'.format(folder, package_name)
    run(cmd)


@task
def upgrade_timezone_data():
    """ Upgrades timezone data deb package """

    # update apt index
    update_index(quiet=False)

    cmd = 'apt-get install --only-upgrade tzdata'
    sudo(cmd)

    print(green('Timezone data successfully upgraded.'))


@task
def set_default_locale(locale='en_US.UTF-8'):
    locale_setup = 'LC_ALL="{}"'.format(locale)
    append('/etc/environment', locale_setup, use_sudo=True)

    print(green('Default locale set to {}').format(locale))
