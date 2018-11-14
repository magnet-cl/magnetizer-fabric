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
    deb.update_index(quiet=False)

    print(green('Installing PostgreSQL and its development packages.'))
    utils.deb.install('postgresql')
    utils.deb.install('postgresql-contrib')
    utils.deb.install('libpq-dev')
    utils.deb.install('pg-activity')


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
