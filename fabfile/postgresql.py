# standard library
import platform

# fabric
from fabric.api import env
from fabric.api import sudo
from fabric.api import task
from fabric.colors import green
from fabtools import deb

from fabfile import utils


@task
def install():
    """
    Installs PostgreSQL and its development packages.

    """
    # update apt index
    utils.os_commands.update_index(quiet=False)

    print(green('Installing PostgreSQL and its development packages.'))
    utils.os_commands.install('postgresql')

    if platform.system().lower() != 'darwin':
        utils.os_commands.install('postgresql-contrib')
        utils.os_commands.install('libpq-dev')


@task
def create_user(target_user=None):
    """
    Creates a role for the given user or the user running the task.

    """
    if not target_user:
        target_user = env.user

    cmd = "sudo -u postgres createuser -s {}".format(target_user)
    sudo(cmd)

    cmd = "sudo -u postgres createdb -O {} '{}'".format(target_user,
                                                        target_user)
    sudo(cmd)
