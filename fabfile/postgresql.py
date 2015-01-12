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


@task
def create_user():
    """
    Creates a role for the user given through fabric.

    """
    cmd = "sudo -u postgres createuser -s {}".format(env.user)
    sudo(cmd)

    cmd = "sudo -u postgres createdb -O {} '{}'".format(env.user, env.user)
    sudo(cmd)
