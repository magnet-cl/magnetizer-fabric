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
    utils.deb.install('postgresql-9.1')
    utils.deb.install('postgresql-server-dev-9.1')
    utils.deb.install('libpq-dev')


@task
def create_user():
    """
    Creates a role for the user given through fabric.

    """
    cmd = "sudo -u postgres createuser -s {}".format(env.user)
    sudo(cmd)
