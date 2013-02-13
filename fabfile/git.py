from fabric.api import run

from utils import deb_install_if_not_installed


def git_clone(url, path):
    """ Utility method to clone git repositories. """
    cmd = 'git clone %s %s' % (url, path)
    run(cmd)


def git_install():
    """ Utility method that installs git if is not available. """
    deb_install_if_not_installed('git')
