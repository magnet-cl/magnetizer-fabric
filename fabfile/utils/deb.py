from fabric.api import sudo
from fabtools.deb import install as deb_install
from fabtools import deb


def install(package, upgrade=False):
    """
    Helper method to install a deb package.

    If the package is already installed and the parameter 'upgrade' is True,
    then it will be upgraded if possible.

    """
    if not is_installed(package):
        deb_install(package)

    if upgrade:
        cmd = 'apt-get install --only-upgrade {}'.format(package)
        sudo(cmd)


def update_index():
    deb.update_index()


def is_installed(pkg_name):
    deb.is_installed(pkg_name)

