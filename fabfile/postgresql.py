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
